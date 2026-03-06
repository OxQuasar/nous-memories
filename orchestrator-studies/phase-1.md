# Phase 1 Implementation Plan: Nous Foundation

## Context

Nous is a Go-based coding orchestration layer for trading strategy R&D. The architecture is fully designed in `arch.md` but zero Go code exists. Phase 1 builds the minimum end-to-end loop: CLI prompt -> Anthropic streaming -> tool execution -> JSONL persistence -> conversation continuation. Everything else (TUI, gateway, Telegram, memory/RAG, skills, workflows, cron) is Phase 2+.

**End-state**: `nous run "write hello world to test.go"` works — loads config, creates session, streams response, executes tools, persists messages, supports compaction and session resumption.

---

## Step 1: Project Scaffold + csync + pubsub

Create Go module and the two foundational concurrency packages adapted from Crush.

**Files:**
```
go.mod                                    # module github.com/skipper/nous, go 1.23
.gitignore                                # Go standard ignores
main.go                                   # Placeholder: prints "nous" and exits
internal/csync/map.go                     # Thread-safe Map[K,V]
internal/csync/slice.go                   # Thread-safe Slice[T]
internal/csync/value.go                   # Thread-safe Value[T]
internal/pubsub/broker.go                 # Generic Broker[T] with buffered channels
internal/pubsub/broker_test.go
```

**Adapt from:** `~/code/deps/crush/internal/csync/` and `~/code/deps/crush/internal/pubsub/broker.go`

Key types:
- `Map[K,V]` — `sync.RWMutex`-wrapped map with `Get/Set/Del/Take/Copy/Len`
- `Slice[T]` — `sync.RWMutex`-wrapped slice with `Append/Get/SetSlice/Copy/Len`
- `Value[T]` — `sync.RWMutex`-wrapped scalar with `Get/Set`
- `Broker[T]` — buffered channel (64) pub/sub, non-blocking publish, context-aware unsubscribe

**Verify:** `go test -race ./internal/csync/... ./internal/pubsub/...`

---

## Step 2: Config + Logging

Load `~/.nous/config.json`, resolve `$ENV_VAR` references. Setup `log/slog` structured logging.

**Files:**
```
internal/config/config.go                 # Config struct, Load(), Resolve()
internal/config/config_test.go
internal/log/log.go                       # Setup(), Subsystem() logger factory
```

Key types:
```go
type Config struct {
    Provider    ProviderConfig    `json:"provider"`
    Compaction  CompactionConfig  `json:"compaction"`
    Permissions PermissionsConfig `json:"permissions"`
    DataDir     string            `json:"-"` // ~/.nous
    WorkDir     string            `json:"-"` // cwd
}

type ProviderConfig struct {
    APIKey       string `json:"api_key"`       // supports "$ANTHROPIC_API_KEY"
    DefaultModel string `json:"default_model"` // "claude-opus-4-6"
    SmallModel   string `json:"small_model"`   // "claude-haiku-4-5-20251001"
}

type CompactionConfig struct {
    Auto, Prune    bool
    Model          string   // default: SmallModel
    ProtectTokens  int      // default: 40000
    MinimumTokens  int      // default: 20000
    ProtectedTools []string // default: ["skill"]
}
```

`Load()` reads `~/.nous/config.json`, creates data dir if missing, resolves `$ENV_VAR` in string fields, applies defaults.

Logging: `log/slog` (stdlib) writing to `~/.nous/logs/nous.log` + stderr in debug mode.

**Verify:** `go test ./internal/config/...` — round-trip config, env var resolution, default population.

---

## Step 3: Message + Session Models and JSONL Storage

Define core data models and the JSONL persistence layer.

**Files:**
```
internal/message/message.go              # Message struct, Part types, helpers
internal/message/message_test.go
internal/session/session.go              # Session struct
internal/session/store.go                # JSONL file I/O
internal/session/service.go              # High-level service with pubsub
internal/session/store_test.go
```

Storage layout:
```
~/.nous/sessions/{sessionID}/session.json      # metadata
~/.nous/sessions/{sessionID}/messages.jsonl    # append-only, one JSON object per line
```

Key types:
```go
// message.go
type Message struct {
    ID, SessionID string
    Role          Role      // "user" | "assistant"
    Parts         []Part
    Model         string
    IsSummary     bool
    CreatedAt     time.Time
}

type Part struct {
    Type PartType        // "text" | "tool_call" | "tool_result" | "reasoning"
    Data json.RawMessage
}

// Typed part data: TextData, ToolCallData, ToolResultData, ReasoningData
```

```go
// session/service.go
type Service struct { store *Store; broker *pubsub.Broker[Event] }

func (s *Service) CreateSession(dir, agentName string) (*Session, error)
func (s *Service) GetSession(id string) (*Session, error)
func (s *Service) AppendMessage(sessionID string, msg message.Message) error
func (s *Service) GetSessionMessages(sess Session) ([]message.Message, error)
// ^ handles summary rebuild: if SummaryMessageID set, truncate older messages
```

**Verify:** Unit tests for JSONL round-trip, session CRUD, summary truncation logic.

---

## Step 4: Provider Layer (Anthropic SDK Wrapper)

Thin wrapper around `github.com/anthropics/anthropic-sdk-go`. No Fantasy/Catwalk abstraction.

**Files:**
```
internal/provider/provider.go            # Provider interface, types
internal/provider/anthropic.go           # AnthropicProvider implementation
internal/provider/convert.go             # Message/tool conversion helpers
```

**New dependency:** `go get github.com/anthropics/anthropic-sdk-go`

Key interface:
```go
type Provider interface {
    Stream(ctx context.Context, req StreamRequest) (*StreamResponse, error)
    ContextWindow(model string) int64
}

type StreamRequest struct {
    Model, System string
    Messages      []Message
    Tools         []ToolDef
    MaxTokens     int
    OnTextDelta      func(string)
    OnToolCallStart  func(id, name string)
    OnToolCallDelta  func(id, partialJSON string)
    OnToolCallDone   func(id, name string, input json.RawMessage)
    OnReasoningDelta func(string)
}

type StreamResponse struct {
    StopReason  string // "end_turn" | "tool_use" | "max_tokens"
    Usage       TokenUsage
    ToolCalls   []ToolCall
    TextContent string
}
```

`AnthropicProvider.Stream()`:
1. Convert our `Message`/`ToolDef` types to SDK types (`anthropic.MessageParam`, `anthropic.ToolParam`)
2. Call `client.Messages.NewStreaming()`
3. Iterate `stream.Next()`, dispatch to callbacks on deltas
4. Accumulate via `message.Accumulate(event)`, return `StreamResponse`

**Verify:** Integration test (requires `ANTHROPIC_API_KEY`): simple streaming call, tool_use response handling.

---

## Step 5: Tool System (7 Core Tools)

Define Tool interface, implement bash/read/write/edit/glob/grep/ls with embedded `.md` descriptions.

**Files:**
```
internal/agent/tools/tool.go             # Tool interface, ToolContext, ToolResult
internal/agent/tools/bash.go
internal/agent/tools/read.go
internal/agent/tools/write.go
internal/agent/tools/edit.go
internal/agent/tools/glob.go
internal/agent/tools/grep.go
internal/agent/tools/ls.go
internal/agent/tools/descriptions/       # Embedded .md files for each tool
    bash.md, read.md, write.md, edit.md, glob.md, grep.md, ls.md
```

**Adapt from:** `~/code/deps/crush/internal/agent/tools/` (bash.go, view.go, write.go, edit.go, glob.go, grep.go, ls.go)

```go
type Tool interface {
    Name() string
    Description() string               // from //go:embed descriptions/*.md
    InputSchema() map[string]any       // JSON Schema
    Execute(ctx context.Context, tctx ToolContext, input json.RawMessage) (*ToolResult, error)
}

type ToolContext struct { SessionID, WorkDir string }
type ToolResult struct { Content string; IsError bool }
```

Tool details:
- **bash**: `os/exec` with `bash -c`, 120s timeout, output truncated at 30K chars (keep first+last half)
- **read**: line-numbered output, offset/limit params, 2000 line default
- **write**: create dirs as needed, write content
- **edit**: find `old_string`, replace with `new_string`, fail if not unique (unless `replace_all`)
- **glob**: `doublestar` or `filepath.WalkDir` with pattern matching, cap at 100 results
- **grep**: exec `rg` if available, fallback to Go regex walk, cap results
- **ls**: `os.ReadDir`, format as tree, cap depth

Helper: `ToProviderToolDefs([]Tool) []provider.ToolDef` for converting to provider format.

**Verify:** Unit test per tool with temp files/dirs.

---

## Step 6: Agent Runner (Core Orchestration Loop)

The heart of Phase 1 — the loop that calls the provider, processes tool calls, feeds results back.

**Files:**
```
internal/agent/agent.go                  # AgentInfo config struct, built-in agents
internal/agent/runner.go                 # Runner.Run() orchestration loop
internal/agent/signal.go                 # SignalStop, SignalContinue, SignalCompact, SignalDoomLoop
internal/agent/prompt.go                 # BuildSystemPrompt()
internal/agent/templates/coder.md        # Base coder system prompt
internal/agent/templates/title.md        # Title generation prompt
```

**Adapt from:** `~/code/deps/crush/internal/agent/agent.go` (Run method, lines 300-550)

```go
type Runner struct {
    provider provider.Provider
    config   *config.Config
    sessions *session.Service
    tools    map[string]tools.Tool
    broker   *pubsub.Broker[session.Event]
}

func (r *Runner) Run(ctx context.Context, sessionID, prompt string) error {
    // 1. Get/create session, append user message
    // 2. Title generation on first message (goroutine)
    // 3. Main loop:
    for step := 0; ; step++ {
        msgs := r.sessions.GetSessionMessages(sess) // handles summary rebuild
        providerMsgs := r.toProviderMessages(msgs)
        systemPrompt := BuildSystemPrompt(r.config, agent, sess)

        resp, err := r.provider.Stream(ctx, StreamRequest{
            // ... messages, tools, system, callbacks (print text to stdout)
        })

        r.sessions.AppendMessage(sessionID, assistantMsg) // store LLM response

        signal := r.determineSignal(resp, sess, recentToolCalls)
        switch signal {
        case SignalStop:     return nil
        case SignalDoomLoop: return ErrDoomLoop
        case SignalCompact:  r.compact(ctx, sess); continue
        case SignalContinue:
            // Execute each tool call, store results
            for _, tc := range resp.ToolCalls {
                result := r.executeTool(ctx, sess, tc)
                r.sessions.AppendMessage(sessionID, toolResultMsg)
            }
            continue
        }
    }
}
```

Doom loop detection: track last 3 tool calls, if same name + same input hash, signal DoomLoop.

**Verify:** Integration test: prompt that triggers a tool call, verify the full loop executes and messages are persisted.

---

## Step 7: Context Compaction

Two-phase compaction from arch.md section 6.1.

**Files:**
```
internal/compact/compact.go              # ShouldCompact(), Compact()
internal/compact/prune.go                # Phase 1: tool output pruning
internal/compact/summarize.go            # Phase 2: LLM summarization
internal/compact/templates/summary.md    # Summary prompt (from Crush's summary.md)
internal/compact/prune_test.go
```

**Adapt from:** Crush's `internal/agent/agent.go` (lines 406-672) for threshold detection and summarization, arch.md section 6.1 for the two-phase algorithm.

```go
func (c *Compactor) ShouldCompact(contextWindow int64, usage provider.TokenUsage) bool
// Large models (>200K): threshold = 20K buffer
// Small models: threshold = 20% of context window

func (c *Compactor) Compact(ctx context.Context, sess *session.Session) error
// Phase 1: pruneToolOutputs — walk backwards, protect last 2 turns,
//          skip protected tools, replace old outputs with placeholder
// Sufficiency check: if post-prune < 80% context, DONE
// Phase 2: summarize — call LLM with Crush's summary.md template,
//          store summary message, update session.SummaryMessageID
```

**Verify:** Unit tests for pruning logic, threshold calculation. Integration test: create session with large tool outputs, trigger compaction.

---

## Step 8: Project Context + System Prompt

Build the system prompt sent with every LLM request.

**Files:**
```
internal/project/project.go             # LoadContextFiles()
```

`BuildSystemPrompt()` (in agent/prompt.go from Step 6) assembles:
1. Base coder prompt (`templates/coder.md`)
2. Agent-specific additions
3. Environment info (working dir, OS, date)
4. Project context files (CLAUDE.md, .cursorrules, etc.)

`LoadContextFiles()` scans working directory for known context files and reads them.

**Verify:** Unit test with temp dir containing a CLAUDE.md, verify it appears in system prompt.

---

## Step 9: CLI Entry Point

Wire everything together with Cobra.

**Files:**
```
main.go                                  # cmd.Execute()
internal/cmd/root.go                     # Root command with --cwd, --debug flags
internal/cmd/run.go                      # `nous run "prompt"` subcommand
internal/cmd/sessions.go                 # `nous sessions` list subcommand
```

**New dependencies:** `go get github.com/spf13/cobra github.com/google/uuid`

`nous run "prompt"`:
1. Load config
2. Setup logging
3. Create Anthropic provider
4. Create session store + service
5. Build tool list (all 7 tools)
6. Create/resume session (`--session` flag)
7. Create Runner, call `Run()`
8. Print session ID for resumption

`nous sessions`: list recent sessions (ID, title, date, message count).

**Verify:**
```bash
go build -o nous .
./nous run "what is 2+2"                           # streams response
./nous run "list files in current directory"       # triggers bash/ls tool
./nous run "write hello world to /tmp/test.go"     # triggers write tool
./nous run --session <id> "now read that file"     # resumes session
./nous sessions                                     # lists sessions
```

---

## Dependency Graph

```
Step 1: csync + pubsub ──────────────────────────┐
Step 2: config + logging ─────────────────────────┤
                                                   ▼
Step 3: message + session + JSONL ◄── Steps 1,2   │
Step 4: provider/anthropic ◄────── Step 2         │
Step 5: tool system ◄──────────── Step 4          │
                                                   ▼
Step 6: agent runner ◄─────────── Steps 3,4,5     │
Step 7: compaction ◄──────────── Steps 3,4,6      │
Step 8: project context ◄──────── Steps 2,3       │
                                                   ▼
Step 9: CLI wiring ◄──────────── ALL
```

Parallelizable: Steps 3+4+5 after Steps 1+2. Steps 7+8 after Step 6.

---

## What Phase 1 Does NOT Include

- TUI (Bubbletea) — Phase 2
- Gateway daemon / WebSocket — Phase 2
- Telegram bot — Phase 2
- Memory / RAG integration — Phase 2
- Skills system — Phase 2
- Workflows / multi-agent — Phase 2+
- Cron jobs — Phase 2+
- Permission prompts (auto-approve in Phase 1) — Phase 2
- Subagent execution (explorer, researcher) — Phase 2

## Key Design Decisions

1. **Direct anthropic-sdk-go**, no Fantasy/Catwalk wrapper. Keeps it debuggable, avoids Charm dependency tree.
2. **JSONL storage**, no SQLite. Debug with `cat messages.jsonl | jq`. Acceptable perf for Phase 1.
3. **Tools as Go structs** implementing `Tool` interface, descriptions from embedded `.md` files.
4. **Runner owns the loop**, AgentInfo is stateless config. Easy to swap agents, test loop independently.
5. **Compaction is a separate package**, not embedded in runner. Clean separation of concerns.
6. **Complete messages appended**, not updated mid-stream. Streaming callbacks are for display only.
7. **Auto-approve all tool calls** in Phase 1 (non-interactive CLI). Permission UI deferred to Phase 2.
