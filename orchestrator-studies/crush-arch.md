# Crush Architectural Study

> Source: `~/code/deps/crush`
> Purpose: Extract Go-specific patterns applicable to our coding orchestration layer (nous).

---

## 1. Overview

Crush is a **Go-based AI coding agent** built by Charmbracelet. It's the most directly relevant reference for nous — same language, same problem domain, clean Go idioms.

| Aspect | Detail |
|--------|--------|
| Language | Go 1.25.5 |
| LLM abstraction | `charm.land/fantasy` + `catwalk` (Charm's own) |
| Database | SQLite (ncruces/go-sqlite3) |
| SQL codegen | sqlc |
| Migrations | goose |
| TUI | Bubbletea v2 + Lipgloss v2 |
| CLI | Cobra |
| MCP | modelcontextprotocol/go-sdk |
| LSP | charmbracelet/x/powernap |
| Config | JSON + env vars + JSON Schema |
| Shell | mvdan.cc/sh/v3 (cross-platform POSIX) |

---

## 2. Project Layout

```
crush/
├── main.go                    # Entry: loads .env, calls cmd.Execute()
├── internal/
│   ├── agent/                 # Agent orchestration
│   │   ├── agent.go           # SessionAgent interface + impl (1158 lines)
│   │   ├── coordinator.go     # Central coordinator (27.5KB)
│   │   └── tools/             # 20 built-in tools
│   │       ├── bash.go        # Shell execution
│   │       ├── edit.go        # File editing
│   │       ├── view.go        # File viewing
│   │       ├── write.go       # File writing
│   │       ├── glob.go        # Pattern matching
│   │       ├── grep.go        # Content search
│   │       ├── ls.go          # Directory listing
│   │       ├── fetch.go       # HTTP fetch
│   │       ├── web_search.go  # Web search
│   │       ├── diagnostics.go # LSP diagnostics
│   │       ├── todos.go       # Todo management
│   │       ├── multiedit.go   # Multi-file edits
│   │       ├── references.go  # Code references (Sourcegraph)
│   │       └── mcp/           # MCP tool integration
│   ├── app/                   # Application wiring
│   │   └── app.go             # Dependency injection, startup
│   ├── cmd/                   # CLI commands (Cobra)
│   │   ├── root.go            # Interactive TUI mode
│   │   └── run.go             # Non-interactive single-prompt mode
│   ├── config/                # Configuration loading + schema
│   ├── db/                    # SQLite + sqlc generated queries
│   │   └── migrations/        # goose migrations
│   ├── session/               # Session service + pub/sub
│   ├── message/               # Message service + pub/sub
│   ├── history/               # File version tracking
│   ├── filetracker/           # Track files read in sessions
│   ├── permission/            # Permission request/approval system
│   ├── lsp/                   # LSP client manager
│   ├── pubsub/                # Generic event broker
│   ├── csync/                 # Thread-safe concurrent types
│   ├── shell/                 # Shell execution abstraction
│   ├── ui/                    # TUI (Bubbletea v2)
│   │   ├── model/ui.go        # Main TUI model (3321 lines)
│   │   ├── chat/              # Message rendering
│   │   ├── dialog/            # Permission dialogs
│   │   └── completions/       # Path/command completions
│   └── event/                 # Event types
├── crush.json                 # Example config
├── schema.json                # JSON Schema for config validation
└── sqlc.yaml                  # SQL codegen config
```

Everything lives in `internal/` — clean Go convention, nothing exported.

---

## 3. Agent Orchestration

### 3.1 SessionAgent Interface

```go
type SessionAgent interface {
    Run(ctx context.Context, call SessionAgentCall) (*fantasy.AgentResult, error)
    SetModels(large, small Model)
    SetTools(tools []fantasy.AgentTool)
    SetSystemPrompt(systemPrompt string)
    Cancel(sessionID string)
    IsSessionBusy(sessionID string) bool
    Summarize(ctx context.Context, prompt string, opts fantasy.ProviderOptions) error
    Model() Model
}
```

### 3.2 SessionAgentCall

```go
type SessionAgentCall struct {
    Prompt      string
    Attachments []fantasy.Attachment
    Options     fantasy.ProviderOptions
    SessionID   string
}
```

### 3.3 Agent Lifecycle

```
User Input
    ↓
Coordinator.Run(ctx, call)
    ↓
Check: IsSessionBusy(sessionID)?
    ├── Yes → Queue in messageQueue (per-session FIFO)
    └── No  → Continue
    ↓
messages.Create() → Store user message in SQLite
    ↓
fantasy.Agent.Stream() with callbacks:
    ├── OnTextDelta()        → Streaming text
    ├── OnToolInputStart()   → Tool call beginning
    ├── OnToolCall()         → Tool execution
    ├── OnToolResult()       → Tool output
    ├── OnReasoningStart()   → Extended thinking
    ├── OnReasoningDelta()   → Thinking stream
    ├── OnReasoningEnd()     → Thinking complete
    └── OnStepFinish()       → Turn complete
    ↓
Update session usage stats (tokens, cost)
    ↓
Auto-summarize if context window > threshold (200K - 20K buffer)
    ↓
Process queued messages (if any)
```

### 3.4 Coordinator

The `Coordinator` is the central orchestration hub:

- Manages agents (currently 1 "coder", extensible)
- Handles model updates and provider initialization
- OAuth2 token refresh on 401 errors
- API key template resolution (`$OPENAI_API_KEY` → actual value)
- Tool building and registration
- LSP state callbacks
- Multi-level option merging (catwalk defaults → provider config → model config)

### 3.5 Key Takeaway

The `SessionAgent` interface is minimal and clean. The coordinator pattern centralizes cross-cutting concerns (auth, model resolution, tool registration) away from the agent itself. Message queuing per-session is a practical solution for concurrent requests. **Adopt the coordinator + session agent pattern.**

---

## 4. LLM Integration

### 4.1 Fantasy + Catwalk

Crush uses Charm's own LLM libraries:
- **Fantasy** (`charm.land/fantasy`): Agent runtime — streaming, tool calling, message management
- **Catwalk** (`charm.land/catwalk`): Model/provider catalog and configuration

### 4.2 Supported Providers

OpenAI, Anthropic, Google (Gemini), AWS Bedrock, Azure OpenAI, Vercel AI Gateway, OpenRouter, OpenAI-compatible APIs, Hyper (multi-model fallback).

### 4.3 Provider-Specific Options

The coordinator handles per-provider quirks:
- **OpenAI**: `reasoning_effort`, responses model support
- **Anthropic**: `thinking` budget, prompt caching (cache control on last tool + system message)
- **Google**: `thinking_config`
- **Vercel/OpenRouter**: reasoning options

### 4.4 Streaming Callbacks

```go
fantasy.Agent.Stream(ctx, opts) → callbacks:
    OnTextDelta(delta string)
    OnToolInputStart(toolName string)
    OnToolCall(name, input string)
    OnToolResult(name, result string)
    OnReasoningStart()
    OnReasoningDelta(delta string)
    OnReasoningEnd()
    OnStepFinish()
```

### 4.5 Key Takeaway

Fantasy/Catwalk are Charm-proprietary and not available to us. But the **callback-based streaming pattern** and **multi-level option merging** are worth adopting. We'll build our own thin provider abstraction over the official Anthropic and OpenAI Go SDKs. The provider-specific option handling shows what real-world normalization looks like.

---

## 5. Database & Persistence

### 5.1 SQLite Schema

```sql
sessions:
    id TEXT PRIMARY KEY
    parent_session_id TEXT (FK → sessions)
    title TEXT
    message_count INTEGER
    prompt_tokens INTEGER
    completion_tokens INTEGER
    cost REAL
    created_at, updated_at DATETIME

messages:
    id TEXT PRIMARY KEY
    session_id TEXT (FK → sessions)
    role TEXT
    parts JSON          -- Structured message parts
    model TEXT
    provider TEXT
    created_at, updated_at, finished_at DATETIME

files:
    id TEXT PRIMARY KEY
    session_id TEXT (FK → sessions)
    path TEXT
    content TEXT
    version INTEGER
    created_at, updated_at DATETIME

read_files:
    -- Tracks which files were read in sessions
```

### 5.2 SQL Tooling

- **sqlc**: Generates type-safe Go code from SQL queries
- **goose**: Schema migrations
- All database operations transactional

### 5.3 Key Takeaway

SQLite + sqlc + goose is a proven Go stack for embedded persistence. Message parts stored as JSON in a `parts` column — pragmatic, avoids join complexity. **Adopt SQLite + sqlc + goose for our persistence layer.**

---

## 6. Tool System

### 6.1 Tool Interface (via Fantasy)

Tools are `fantasy.AgentTool` with:
- Name
- Description
- Input JSON schema (Zod-equivalent for Go: struct → JSON Schema)
- ExecuteFn callback

### 6.2 Built-in Tools (20)

| Category | Tools |
|----------|-------|
| File ops | `view`, `write`, `edit`, `multiedit`, `ls`, `glob` |
| Search | `grep`, `references`, `sourcegraph` |
| Shell | `bash`, `job_kill`, `job_output` |
| Web | `fetch`, `web_search`, `download` |
| Code intel | `diagnostics`, `lsp_restart` |
| Management | `todos` |
| MCP | `read_mcp_resource`, `list_mcp_resources` |

### 6.3 Tool Registration

```go
coordinator.buildTools() → []fantasy.AgentTool
```

Filtering:
- `config.DisabledTools` — global disable list
- `config.Agent.AllowedTools` — per-agent allowlist
- `config.MCPConfig.DisabledTools` — per-MCP disable list

### 6.4 Tool Descriptions

Each tool has a companion `.md` template file (e.g., `bash.tpl`, `edit.md`) with detailed usage instructions injected into the tool description. This is a great pattern — rich tool descriptions without cluttering Go code.

### 6.5 Permission System

```go
permission.Service.Request(ctx, tool, args) → approve/deny
```

- UI shows permission dialog
- Can auto-approve for session or grant permanently
- Allowlist mode: `config.Permissions.AllowedTools`
- YOLO mode: `config.Permissions.SkipRequests`
- Custom error: `permission.ErrorPermissionDenied`

### 6.6 Key Takeaway

Tool descriptions as `.md` template files is excellent — keeps Go code clean while giving the LLM rich context. The three-layer filtering (global disable, per-agent allow, per-MCP disable) is practical. **Adopt template-based tool descriptions and the filtering pattern.**

---

## 7. Concurrency Patterns

### 7.1 Thread-Safe Types (`csync/`)

```go
csync.Map[K, V]     // RWMutex-wrapped map
csync.Slice[T]       // RWMutex-wrapped slice
csync.Value[T]       // RWMutex-wrapped single value
csync.VersionedMap   // Map with version tracking
```

These wrap the standard sync.RWMutex pattern into generic, reusable types. Clean and practical.

### 7.2 PubSub (`pubsub/`)

```go
Broker[T] struct {
    subscribers []chan T  // Buffered channels (64)
}

broker.Publish(event T)           // Fan-out to all subscribers
broker.Subscribe() <-chan T       // Returns receive channel
```

Every service (session, message, history, permission) embeds a `*Broker` and publishes events on mutations.

### 7.3 Concurrency Model

- **Per-session message queue**: If agent is busy, messages queued (FIFO)
- **Background goroutines**: Title generation, MCP init, update checks
- **Context cancellation**: All long-running ops take `context.Context`
- **No parallel tool execution**: Tools execute sequentially within a session

### 7.4 Key Takeaway

The `csync` package is small but valuable — avoids mutex boilerplate everywhere. The generic `Broker[T]` pub/sub is a clean Go pattern. **Adopt csync-style thread-safe wrappers and the generic broker pattern.**

---

## 8. MCP Support

### 8.1 Transport Types

- `stdio`: Subprocess execution
- `sse`: Server-sent events
- `http`: HTTP endpoints

### 8.2 State Machine

```
StateDisabled → StateStarting → StateConnected
                      ↓
                 StateError
```

### 8.3 Features

- Tools from MCP servers added to agent toolset
- Prompts from MCP servers available as shortcuts
- Resources can be read/listed
- Per-MCP disabled tools
- Auto-disable on initialization failure

### 8.4 Key Takeaway

MCP is straightforward in Go via the official SDK. The state machine pattern for connection lifecycle is clean. **Adopt MCP support with the state machine pattern.**

---

## 9. LSP Integration

### 9.1 Manager Pattern

```go
lsp.Manager:
    - Lazy-loads language servers based on file types
    - Root marker discovery (.git, go.mod, package.json, etc.)
    - Lifecycle: start, restart, shutdown
    - State callbacks notify coordinator when ready
```

### 9.2 Configuration

```go
LSPConfig struct {
    Command      string
    Args         []string
    Env          map[string]string
    FileTypes    []string
    RootMarkers  []string
    InitOptions  map[string]any
    Settings     map[string]any
    Timeout      time.Duration
}
```

### 9.3 Key Takeaway

Lazy-loading LSP servers by file type is the right approach — don't start gopls until you see a `.go` file. Root marker discovery determines the LSP workspace root. **Adopt lazy LSP with root marker detection.**

---

## 10. Configuration

### 10.1 Config Structure

```go
type Config struct {
    Providers   map[string]ProviderConfig
    Agents      map[string]Agent
    LSP         map[string]LSPConfig
    MCP         map[string]MCPConfig
    OAuth       map[string]OAuthConfig
    Options     Options
    Permissions *Permissions
    TUI         *TUIOptions
}
```

### 10.2 Loading Precedence

1. `.env` file (via godotenv)
2. `~/.crush/crush.json` (global)
3. `crush.json` (project-local)
4. Environment variable overrides in API keys (`$OPENAI_API_KEY`)

### 10.3 JSON Schema

Generated via `invopop/jsonschema` from Go structs. Provides editor autocompletion and validation.

### 10.4 Key Takeaway

JSON + JSON Schema from Go structs is a natural fit. No need for a separate schema language. **Adopt JSON config with generated JSON Schema.**

---

## 11. TUI Architecture

### 11.1 Bubbletea v2

The TUI is a single Bubbletea model (`ui.go`, 3321 lines) with states:

| State | Purpose |
|-------|---------|
| `uiOnboarding` | First-time setup |
| `uiInitialize` | Project init |
| `uiLanding` | Session list |
| `uiChat` | Active chat |

Focus states: `uiFocusEditor`, `uiFocusMain`, `uiFocusNone`

### 11.2 Components

- Chat message rendering (user/assistant/tool/error/reasoning)
- Multi-line text editor
- Session sidebar
- Permission dialogs
- File path completions
- Responsive layout (compact mode < 120 width)

### 11.3 Key Takeaway

Bubbletea v2 is the Go standard for TUIs. The single-model-with-states approach is typical for Bubbletea apps. **Adopt Bubbletea v2 for our TUI.**

---

## 12. Auto-Summarization

When context window approaches limits (200K tokens with 20K buffer):
1. Uses the small model to summarize old messages
2. Replaces original messages with summary
3. Preserves recent messages intact

This is a practical solution to infinite-session context management.

### Key Takeaway

**Adopt auto-summarization** for long sessions. Dual-model (large for coding, small for summarization) is cost-effective.

---

## 13. What to Adopt for Nous

| Pattern | Priority | Rationale |
|---------|----------|-----------|
| Coordinator + SessionAgent | **High** | Central orchestration with clean agent interface |
| SQLite + sqlc + goose | **High** | Proven Go persistence stack |
| `csync` thread-safe types | **High** | Eliminates mutex boilerplate |
| Generic PubSub broker | **High** | Clean event-driven communication |
| Callback-based LLM streaming | **High** | Natural Go streaming pattern |
| Template-based tool descriptions (.md) | **High** | Rich descriptions without code clutter |
| Tool permission system | **High** | Security for shell/file operations |
| Context propagation throughout | **High** | Standard Go concurrency pattern |
| MCP with state machine lifecycle | **Medium** | Protocol interop |
| Lazy LSP with root markers | **Medium** | Code intelligence on demand |
| Bubbletea v2 TUI | **Medium** | Go-native terminal UI |
| JSON config + generated JSON Schema | **Medium** | Editor-friendly config |
| Auto-summarization (dual model) | **Medium** | Long session support |
| Message queuing per session | **Medium** | Handle concurrent requests gracefully |
| Per-provider option merging | **Low** | Important but can be added incrementally |

## 14. What to Skip

- **Fantasy/Catwalk**: Charm-proprietary — we'll use official Anthropic/OpenAI SDKs directly
- **Sourcegraph integration**: Not needed initially
- **OAuth flow**: We'll use API keys first
- **Hyper multi-model fallback**: Over-engineered for MVP
- **PostHog metrics**: Not relevant

---

## 15. Three-Way Comparison: OpenClaw vs. OpenCode vs. Crush

| Concern | OpenClaw (TS) | OpenCode (TS) | Crush (Go) | Nous Should... |
|---------|---------------|---------------|------------|----------------|
| Always-on | Daemon gateway | Per-invocation | Per-invocation | **OpenClaw's daemon** + Crush's architecture |
| Memory | Vector+BM25 SQLite | None | Session history in SQLite | **OpenClaw's hybrid memory** in Go |
| Agent model | Multi-agent via session keys | Primary + subagent hierarchy | Single coordinator + session agent | **Combine**: coordinator + multi-agent hierarchy |
| LLM layer | Custom + fallback chains | Vercel AI SDK (20+ providers) | Fantasy/Catwalk | **Direct SDKs** (anthropic-sdk-go, openai-go) |
| Tools | Pi runtime | init/execute/ask interface | Fantasy AgentTool + .md templates | **Crush's pattern**: Go interface + .md descriptions |
| Persistence | JSONL files | Hierarchical path storage | SQLite + sqlc | **SQLite + sqlc** (Crush's approach) |
| Concurrency | WebSocket async | Typed event bus | csync + PubSub broker | **Crush's csync + broker** pattern |
| Config | JSON5 + Zod | JSONC + Zod | JSON + JSON Schema | **JSON + generated schema** (Go-native) |
| TUI | None (headless) | Solid.js OpenTUI | Bubbletea v2 | **Bubbletea v2** |
| MCP | None | Official SDK | Official Go SDK | **Official Go SDK** |
| LSP | None | TS/Deno servers | Lazy manager + powernap | **Crush's lazy LSP pattern** |
| Permissions | Tool policies per channel | Pattern-based rulesets | Request/approve + allowlists | **Crush's permission service** |
| Session mgmt | JSONL + write locks | Part-based hierarchical | SQLite rows + JSON parts | **SQLite** with OpenCode's part model inspiration |
