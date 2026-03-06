# Phase 3 Implementation Plan: Memory/RAG + TUI

## Context

Phase 2 delivered interactive chat, subagents, skills, permissions, and the fetch tool. The REPL works but is raw — no streaming display, no session sidebar, no visual tool call rendering. Memory is absent entirely: the agent has no recall across sessions.

Phase 3 adds two capabilities:
1. **Memory** — tiered memory system with RAG retrieval, injected into prompts so the agent has cross-session recall
2. **TUI** — Bubbletea terminal UI replacing the REPL with streaming display, session sidebar, permission prompts, and status bar

**End-state**: `nous` launches a full TUI with streaming markdown rendering, session management, and memory-augmented context. The REPL (`nous chat`) remains as a fallback. `nous run` also gets memory injection.

---

## Part A: Memory System

### Step 1: Memory Config + Package Scaffold

Add memory configuration and the `internal/memory/` package.

**Files:**
```
internal/config/config.go     # Modify: add MemoryConfig
internal/memory/memory.go     # New: Manager struct, Retrieve/Store interface
```

Config addition:
```go
type MemoryConfig struct {
    RAGUrl   string   `json:"rag_url"`   // e.g. "http://localhost:8103"
    Dirs     []string `json:"dirs"`      // memory directories to index (supports $ENV and ~)
    TopK     int      `json:"top_k"`     // results per query (default: 5)
    MinScore float64  `json:"min_score"` // minimum relevance (default: 0.3)
}
```

Defaults: `RAGUrl: ""` (disabled when empty), `TopK: 5`, `MinScore: 0.3`.

Memory manager:
```go
type Manager struct {
    client *RAGClient  // nil when RAGUrl is empty
    config MemoryConfig
    log    *slog.Logger
}

// Retrieve queries the RAG server and returns formatted context for prompt injection.
// Returns empty string when RAG is unavailable or no results found.
func (m *Manager) Retrieve(ctx context.Context, query string) string

// Reindex triggers the RAG server to rebuild its indices.
func (m *Manager) Reindex(ctx context.Context) error
```

The Manager is nil-safe — when RAG is not configured, `Retrieve` returns `""` and `Reindex` is a no-op. This keeps all callers simple.

**Verify:** Unit test with a mock HTTP server returning canned RAG responses.

---

### Step 2: RAG Client

HTTP client for the gandiva-memory RAG server (`POST /context`, `POST /index`, `GET /health`).

**Files:**
```
internal/memory/rag.go        # New: RAGClient
```

```go
type RAGClient struct {
    baseURL    string
    httpClient *http.Client
}

type ContextRequest struct {
    Query    string  `json:"query"`
    TopK     int     `json:"top_k"`
    MinScore float64 `json:"min_score"`
}

type ContextResponse struct {
    Context       string  `json:"context"`
    Chunks        []Chunk `json:"chunks"`
    QueryTimeMs   float64 `json:"query_time_ms"`
    BM25Boosted   bool    `json:"bm25_boosted"`
    BM25BoostCount int    `json:"bm25_boost_count"`
}

type Chunk struct {
    Text        string  `json:"text"`
    Source      string  `json:"source"`
    LineStart   int     `json:"line_start"`
    LineEnd     int     `json:"line_end"`
    Score       float64 `json:"score"`
    MatchSource string  `json:"match_source"`
}
```

The client has a 5-second timeout. `Retrieve` gracefully returns empty on connection failure (RAG server down should not block the agent).

**Verify:** Unit test with httptest server mimicking the gandiva RAG API.

---

### Step 3: Prompt Injection

Wire memory context into the system prompt. The runner calls `memory.Retrieve(ctx, prompt)` before each LLM call and passes the result into `PromptContext`.

**Files:**
```
internal/agent/runner.go      # Modify: add memory field, call Retrieve before each step
internal/agent/prompt.go      # Modify: add Memory field to PromptContext, render in prompt
internal/cmd/deps.go          # Modify: create Manager, add to Deps
internal/cmd/chat.go          # Modify: wire memory to runner
internal/cmd/run.go           # Modify: wire memory to runner
```

Runner gets a new field:
```go
type Runner struct {
    // ...
    memory *memory.Manager  // nil-safe, can be nil when RAG is not configured
}
```

New setter:
```go
func (r *Runner) SetMemory(m *memory.Manager) { r.memory = m }
```

In the main loop, before building the system prompt:
```go
var memoryContext string
if r.memory != nil {
    memoryContext = r.memory.Retrieve(ctx, prompt)  // use original user prompt
}
```

In the system prompt, after `</project_context>`:
```
<memory>
{retrieved context from RAG}
</memory>
```

Only injected when non-empty. The memory block is rebuilt each turn using the **original user prompt** (not the ongoing tool call chain), so retrieval stays focused on the user's intent.

**Verify:** Integration test: configure RAG URL, send a prompt, verify memory block appears in system prompt.

---

### Step 4: Memory Tool

A `memory_search` tool that lets the agent explicitly query memory mid-conversation, rather than relying solely on automatic injection.

**Files:**
```
internal/agent/tools/memory.go               # New: memory tool
internal/agent/tools/descriptions/memory.md  # New: tool description
internal/agent/tools/tool.go                 # Modify: add to AllTools(), extend ToolContext
```

```go
// Input: { "query": string, "top_k": int (optional, default 5) }
// Output: retrieved memory chunks formatted as text
```

ToolContext extension:
```go
type ToolContext struct {
    // ...
    MemoryQuery func(ctx context.Context, query string, topK int) (string, error)
}
```

The runner wires this closure from `memory.Manager`. When memory is not configured, the tool returns "memory system not configured".

Add `"memory_search"` to the compaction `ProtectedTools` default so memory results are never pruned.

**Verify:** Unit test: call tool with a query, verify it returns formatted chunks.

---

### Step 5: REPL Memory Commands

Add `/memory` command to the REPL for status and manual reindex.

**Files:**
```
internal/cmd/chat.go          # Modify: add /memory command
```

```
/memory          — show RAG connection status and index stats
/memory reindex  — trigger RAG reindex
```

Calls `GET /status` and `POST /index` on the RAG server.

**Verify:** Manual test with RAG server running.

---

## Part B: TUI

### Step 6: Dependencies + Package Scaffold

Add Bubbletea v2 and Lipgloss v2. Create the `internal/ui/` package structure.

**Files:**
```
go.mod                         # Modify: add bubbletea v2, lipgloss v2
internal/ui/app.go             # New: top-level Bubbletea model
internal/ui/theme.go           # New: Lipgloss styles, color palette
```

```bash
go get github.com/charmbracelet/bubbletea/v2 github.com/charmbracelet/lipgloss/v2
```

The App model owns all state and child components:
```go
type App struct {
    // Dependencies
    runner   *agent.Runner
    sessions *session.Service
    deps     *cmd.Deps
    sess     *session.Session

    // Components
    chat     ChatModel
    input    InputModel
    sidebar  SidebarModel
    status   StatusModel

    // State
    width, height int
    running       bool  // true while agent is executing
    focus         Focus // chat | input | sidebar
}
```

Theme: muted color palette. Dark background assumed. No emoji in code or UI labels.

**Verify:** `go build` succeeds with new dependencies.

---

### Step 7: Chat View

Scrollable message list with streaming text display and tool call indicators.

**Files:**
```
internal/ui/chat.go            # New: chat message list component
```

Rendering:
- **User messages**: dimmed prefix `>`, then text
- **Assistant text**: streamed character-by-character via `TextDelta` events
- **Tool calls**: `  > tool_name arg_summary` while running, ` + tool_name arg_summary` when done, `x tool_name error` on failure
- **Tool results**: collapsed by default (just the status indicator above)
- **Summary messages**: `[compacted]` marker

The chat view receives events from the runner via a channel:
```go
type RunnerEvent struct {
    Type      EventType  // TextDelta, ToolStart, ToolDone, RunDone, Error
    Text      string
    ToolName  string
    ToolInput string
    Error     error
}
```

The runner's streaming callbacks (`OnTextDelta`, etc.) push events onto this channel. The App model reads them via `tea.Sub` or a command that reads from the channel.

Viewport-based scrolling: auto-scroll when at bottom, manual scroll otherwise. Viewport height = terminal height - input height - status bar height.

**Verify:** Manual test: launch TUI, send a prompt, verify streaming text and tool call indicators render correctly.

---

### Step 8: Input Component

Multi-line text editor with submit and cancel.

**Files:**
```
internal/ui/input.go           # New: text input component
```

Behavior:
- `Enter`: submit message (when not empty)
- `Shift+Enter` or `Alt+Enter`: insert newline
- `Ctrl+C` while agent is running: stop the current run
- `Ctrl+C` at idle prompt: exit
- `Ctrl+D`: exit
- Input is disabled (grayed out) while the agent is running
- Slash commands (`/new`, `/quit`, etc.) handled before sending to runner

Use `charmbracelet/textarea` from Bubbletea's standard components, or a simple custom editor if the textarea API is awkward.

**Verify:** Manual test: multi-line input, submit, slash command handling.

---

### Step 9: Session Sidebar

Session list with selection and switching.

**Files:**
```
internal/ui/sidebar.go         # New: session sidebar component
```

Layout: left panel, fixed width (24 chars). Shows:
```
  Sessions
  ────────
  > my-session     12m
    debug-thing    2h
    research       1d
```

Active session highlighted. `Tab` to toggle focus to sidebar. `Up/Down` to navigate. `Enter` to switch session. `n` to create new session.

When switching sessions, calls `runner.LoadContext(newSess.Directory, deps.Config.DataDir)` and reloads messages into the chat view.

The sidebar subscribes to session events via the pubsub broker to auto-refresh when sessions are created/updated.

**Verify:** Manual test: see sessions, switch, create new.

---

### Step 10: Status Bar

Bottom bar showing current state.

**Files:**
```
internal/ui/status.go          # New: status bar component
```

Format:
```
 model_name | session_id | 12K tokens | memory: connected
```

Fields:
- Model name (from config)
- Current session ID (truncated to 8 chars)
- Cumulative token usage for session
- Memory status: `connected` / `disconnected` / `off` (based on RAG health check)

Updates after each agent turn completes.

**Verify:** Visual inspection.

---

### Step 11: Permission Prompt

Overlay for tool approval that replaces the REPL's stdin-based ask.

**Files:**
```
internal/ui/permission.go      # New: permission prompt component
```

When a tool needs approval, the runner's `OnPermissionCheck` callback sends an event to the TUI. The TUI shows an overlay:

```
 Allow bash: git status ?
 [y] yes  [n] no  [a] always for this tool
```

Key handling:
- `y` or `Enter`: allow this call
- `n` or `Esc`: deny
- `a`: allow all future calls to this tool in this session

The overlay blocks the runner (via a channel) until the user responds.

**Verify:** Manual test: run a prompt that triggers bash, verify overlay appears, y/n/a work.

---

### Step 12: Wire TUI into CLI

Replace the default `nous` command with the TUI. Keep `nous chat` as the REPL fallback.

**Files:**
```
internal/cmd/root.go           # Modify: default to TUI
internal/cmd/tui.go            # New: TUI command wiring
internal/cmd/chat.go           # Modify: rename to explicit REPL fallback
```

```bash
nous              # launches TUI (default)
nous --repl       # launches REPL (fallback)
nous chat         # alias for --repl
nous run "prompt" # non-interactive (unchanged)
```

The TUI command:
1. Calls `setupDeps()`
2. Creates runner, wires memory, compaction, permissions
3. Creates `ui.App` with all dependencies
4. Calls `tea.NewProgram(app).Run()`

The REPL remains for environments without terminal capability (piped input, CI, etc.) and for debugging.

**Verify:** `nous` launches TUI. `nous --repl` launches REPL. `nous run "hello"` still works.

---

## Dependency Graph

```
Step 1: Memory config + scaffold ──────────┐
Step 2: RAG client ◄── Step 1              │
Step 3: Prompt injection ◄── Step 2        │
Step 4: Memory tool ◄── Step 2             ├── Memory complete
Step 5: REPL commands ◄── Step 2           │
                                            │
Step 6: TUI scaffold (independent) ────────┤
Step 7: Chat view ◄── Step 6              │
Step 8: Input component ◄── Step 6        │
Step 9: Sidebar ◄── Step 6                ├── TUI complete
Step 10: Status bar ◄── Step 6            │
Step 11: Permission prompt ◄── Step 6     │
Step 12: CLI wiring ◄── Steps 7-11 + 3   │
```

Memory steps 1-5 and TUI steps 6-11 are independent tracks and can be built in parallel. Step 12 ties them together.

---

## What Phase 3 Does NOT Include

- Gateway daemon / WebSocket server — Phase 4                    DONE
- Telegram bot — Phase 4                                         DONE
- Workflows / radio bus — Phase 4                                DONE
- Cron jobs / memory consolidation — Phase 4                     DONE
- Session export commands — Phase 4 
- Coordinator (replaces direct runner wiring) — Phase 4          DONE
- Message queuing — Phase 4 (TUI disables input while running)   DONE

Daemon -> Websocket (SSH conn) -> SSH TUI / Telegram

## Key Design Decisions

1. **RAG as optional HTTP dependency.** Memory gracefully degrades when the RAG server is down or not configured. No hard dependency, no startup failure.
2. **Memory injected per-turn, not per-session.** The system prompt is rebuilt every LLM call anyway. Memory retrieval uses the original user prompt for focused results, not the expanding tool-call chain.
3. **Memory tool supplements automatic injection.** Auto-injection gives baseline recall; the `memory_search` tool lets the agent do targeted queries when it needs specific knowledge.
4. **TUI events via typed channel, not pubsub.** Single consumer (the TUI), typed events, direct channel. Simpler than broadcast semantics.
5. **REPL preserved as fallback.** The REPL is useful for piped input, debugging, and CI. It stays as `nous chat` / `nous --repl`.
6. **Viewport-based chat scrolling.** Auto-scroll at bottom, manual scroll otherwise. Standard terminal UX.
7. **Permission overlay blocks runner.** The runner's permission callback sends an event and waits on a response channel. The TUI renders the overlay and unblocks when the user responds.
