# Nous Architecture

> Coding orchestration layer for trading strategy research and development.
> Go implementation. Always-on. Persistent memory. Multi-agent.

---

## 1. Design Principles

1. **Debuggable first.** Session context, memory state, and agent decisions must be extractable and inspectable at any point.
2. **Transparent logging.** Structured logs with subsystem tags. Every LLM call, tool invocation, and memory retrieval is logged.
3. **Direct modification.** No plugin system. No multi-OS compatibility. We maintain source and change it directly.
4. **Clear flows.** Architecture should be legible enough that large-scale refactors are feasible. Prefer explicit wiring over magic.
5. **MVP-scoped.** Ship the core loop first. Defer what can be deferred.

---

## 2. High-Level Architecture

```
                         ┌──────────────────────────────┐
                         │         Gateway Daemon        │
                         │     (always-on, systemd)      │
                         │                               │
    Telegram ──────────▶ │  WebSocket + HTTP Server       │
    TUI ───────────────▶ │  (gorilla/websocket or nhooyr) │
    (WebUI later) ─────▶ │                               │
                         └──────────┬───────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
              ┌──────────┐  ┌────────────┐  ┌────────────┐
              │ Sessions │  │   Agents   │  │   Memory   │
              │ (JSONL)  │  │ (coordinator│  │ (tiered +  │
              │          │  │  + runners) │  │  RAG)      │
              └──────────┘  └─────┬──────┘  └────────────┘
                                  │
                            ┌─────▼──────┐
                            │   Tools    │
                            │ (bash,edit,│
                            │  grep,...) │
                            └─────┬──────┘
                                  │
                            ┌─────▼──────┐
                            │ Providers  │
                            │ (Anthropic)│
                            └────────────┘
```

---

## 3. Project Layout

```
nous/
├── main.go                         # Entry point: load config, start gateway or TUI
├── internal/
│   ├── gateway/                    # Always-on daemon, WebSocket server, client routing
│   ├── agent/                      # Agent orchestration
│   │   ├── coordinator.go          # Central coordinator (model resolution, tool building)
│   │   ├── agent.go                # Agent interface + session agent impl
│   │   ├── runner.go               # Agent execution loop (stream → process → store)
│   │   └── tools/                  # Built-in tools
│   │       ├── bash.go
│   │       ├── edit.go
│   │       ├── read.go
│   │       ├── write.go
│   │       ├── glob.go
│   │       ├── grep.go
│   │       ├── ls.go
│   │       ├── fetch.go
│   │       ├── skill.go            # Lazy skill loading tool
│   │       ├── armory.go           # Subagent spawn tool
│   │       └── descriptions/       # .md templates for tool descriptions
│   ├── skill/                      # Skill discovery and loading
│   ├── session/                    # Session lifecycle, JSONL storage
│   ├── message/                    # Message model (parts-based)
│   ├── memory/                     # Tiered memory system
│   │   ├── manager.go              # Memory tier coordinator
│   │   ├── rag.go                  # RAG client (calls gandiva-memory or built-in)
│   │   └── consolidator.go         # Periodic memory consolidation
│   ├── provider/                   # LLM provider abstraction
│   │   ├── provider.go             # Provider interface
│   │   ├── anthropic.go            # anthropic-sdk-go wrapper
│   │   └── stream.go               # Unified streaming interface
│   ├── config/                     # Configuration loading
│   ├── project/                    # Project context and scoping
│   ├── cron/                       # Internal cron scheduler
│   ├── telegram/                   # Telegram bot integration
│   ├── auth/                       # Anthropic auth (API key or Pro/Max subscription)
│   ├── compact/                    # Context compaction (pruning + LLM summary)
│   ├── pubsub/                     # Generic event broker
│   ├── csync/                      # Thread-safe concurrent types
│   ├── permission/                 # Tool permission service
│   ├── cmd/                        # CLI commands (Cobra)
│   │   ├── root.go                 # TUI mode (default)
│   │   ├── gateway.go              # Start daemon
│   │   └── run.go                  # Non-interactive single prompt
│   ├── ui/                         # TUI (Bubbletea v1)
│   │   ├── app.go                 # Root model, event routing, layout
│   │   ├── chat.go                # Chat viewport, streaming, diff rendering
│   │   ├── input.go               # Multi-line textarea input
│   │   ├── sidebar.go             # Session list panel
│   │   ├── status.go              # Bottom status bar
│   │   ├── permission.go          # Tool approval prompt
│   │   ├── events.go              # Typed event messages
│   │   └── theme.go               # Colors, styles, layout constants
│   └── log/                        # Structured logging
├── skills/                         # Skill definitions (markdown + frontmatter)
├── config.json                     # Example config
└── go.mod
```

---

## 4. Gateway Daemon

The gateway is an always-on process that persists across sessions, manages memory, runs cron jobs, and accepts connections from TUI/Telegram/WebUI.

### 4.1 Lifecycle

```
systemd start
    → Load config
    → Initialize memory system (connect to RAG, load tiers)
    → Start cron scheduler
    → Start Telegram bot (if configured)
    → Start WebSocket + HTTP server
    → Accept connections
    → On SIGUSR1: graceful restart
    → On SIGTERM: graceful shutdown
```

### 4.2 Transport

- **WebSocket**: Primary transport for TUI and WebUI clients. Bidirectional streaming.
- **HTTP**: Health checks, status, API endpoints for external integrations.
- **Protocol**: JSON-based RPC similar to OpenClaw:
  ```json
  { "method": "session.prompt", "payload": {...}, "id": "req-123" }
  → { "result": {...}, "id": "req-123" }
  ```
  Streaming events sent as one-way broadcasts (no `id`).

### 4.3 Installation

```bash
nous gateway --install    # Install systemd user service
nous gateway --start      # Start daemon
nous gateway --status     # Health check
```

### 4.4 Revisitable

- [ ] WebSocket library choice: `gorilla/websocket` vs `nhooyr.io/websocket` vs `coder/websocket`
- [ ] Whether to embed the HTTP server in the gateway or run separately
- [ ] Port selection and discovery (fixed port vs dynamic with lock file)

---

## 5. Agent System

Design synthesized from Crush (coordinator pattern, dependency injection, message queuing, csync) and OpenCode (agents as config, explicit loop, permission rulesets, doom loop detection).

### 5.1 Agents as Config

Agents are **stateless configuration records**, not runtime objects. Runtime state lives in sessions and the coordinator. This keeps agent definitions simple and composable.

```go
type AgentMode string

const (
    AgentModePrimary  AgentMode = "primary"
    AgentModeSubagent AgentMode = "subagent"
)

type AgentInfo struct {
    Name        string
    Description string
    Mode        AgentMode
    Permissions []PermissionRule  // Pattern-based allow/deny rules
    Model       string            // Model override (empty = use default)
    MaxSteps    int               // Max turns for subagents (0 = unlimited)
    Prompt      string            // Additional system prompt text
    Hidden      bool              // Utility agents (title, compaction) not shown to user
}

// PermissionRule controls tool access per agent (from OpenCode's pattern-based system)
type PermissionRule struct {
    Tool    string // Tool name or "*" for all
    Pattern string // Glob pattern for arguments (e.g., "*.env" for file paths)
    Action  string // "allow" | "deny" | "ask"
}
```

### 5.2 Built-in Agents

| Agent | Mode | Tools | Purpose |
|-------|------|-------|---------|
| `coder` | primary | All | Default — full coding capability |
| `planner` | primary | Read-only (no edit/write/bash) | Research and planning mode |
| `explorer` | subagent | glob, grep, read, ls | Fast read-only codebase search |
| `researcher` | subagent | fetch, read, grep, glob | Web search + document analysis |
| `title` | primary, hidden | None | Generates session titles (uses small model) |
| `compaction` | primary, hidden | None | Summarizes old context (uses small model) |

Hidden agents are internal — the coordinator uses them for housekeeping, they don't appear in agent selection UI.

### 5.3 Coordinator

The coordinator is the central hub (Crush's pattern). It owns all dependencies and orchestrates agent execution.

```go
type Coordinator struct {
    agents      map[string]AgentInfo         // Agent registry (config, not runtime)
    provider    *provider.AnthropicProvider  // LLM provider
    tools       []Tool                       // Full tool registry
    memory      *memory.Manager
    sessions    *session.Service
    messages    *message.Service
    permissions *permission.Service
    pubsub      *pubsub.Broker[Event]

    // Per-session runtime state (from Crush)
    activeRequests csync.Map[string, context.CancelFunc]  // Cancel tokens
    messageQueue   csync.Map[string, []QueuedPrompt]      // Per-session FIFO queue
}
```

**Responsibilities:**
- Agent registration and lookup
- Model resolution and auth refresh
- Tool registry construction per-agent (filter by agent's permission rules)
- Memory context injection before agent runs
- Session creation and message persistence
- Message queuing when agent is busy on a session
- Event publishing for UI/Telegram updates

### 5.4 Execution Loop

The coordinator runs an **explicit orchestration loop** (from OpenCode), not a hidden callback-driven stream. This makes the control flow visible and debuggable.

```go
func (c *Coordinator) Run(ctx context.Context, sessionID, prompt string) error {
    // Queue if session is busy (from Crush)
    if c.isSessionBusy(sessionID) {
        c.messageQueue.Append(sessionID, QueuedPrompt{Prompt: prompt})
        return nil
    }

    session := c.sessions.GetOrCreate(sessionID)
    agent := c.agents[session.AgentName]
    tools := c.buildToolsForAgent(agent)
    memoryCtx := c.memory.Retrieve(ctx, prompt, session.ProjectID)

    // Store user message
    c.messages.Append(sessionID, userMessage)

    // Title generation on first message (async, from Crush)
    if session.MessageCount == 0 {
        go c.generateTitle(ctx, sessionID, prompt)
    }

    // Main orchestration loop (from OpenCode)
    for step := 0; agent.MaxSteps == 0 || step < agent.MaxSteps; step++ {
        // Drain queued messages before each step (from Crush)
        c.drainQueue(sessionID)

        // Stream LLM response and process tool calls
        signal := c.processStream(ctx, sessionID, agent, tools, memoryCtx)

        switch signal {
        case SignalStop:
            return nil
        case SignalCompact:
            c.compact(ctx, sessionID)  // Uses hidden compaction agent
            continue
        case SignalContinue:
            continue  // Tool calls were made, loop for next turn
        case SignalDoomLoop:
            c.publishError(sessionID, "Agent stuck in loop, halting")
            return ErrDoomLoop
        }
    }
    return ErrMaxSteps
}
```

**Control signals** (from OpenCode's SessionProcessor):

| Signal | Meaning |
|--------|---------|
| `SignalStop` | Agent finished, no more tool calls |
| `SignalContinue` | Tool calls made, continue to next turn |
| `SignalCompact` | Context too large, summarize and continue |
| `SignalDoomLoop` | Repeated identical tool calls detected, halt |

### 5.5 Stream Processing

The stream processor handles LLM output and tool execution within a single turn:

```go
func (c *Coordinator) processStream(ctx, sessionID, agent, tools, memory) Signal {
    // Build system prompt (base + agent.Prompt + memory context + skill list)
    // Call provider.Stream() with callbacks:
    //   OnTextDelta     → publish to UI via pubsub
    //   OnToolCall      → check permissions, execute tool, return result
    //   OnReasoningDelta → publish to UI
    //   OnFinish        → update message, check token usage

    // Post-turn checks:
    // - If no tool calls → SignalStop
    // - If tokens > compaction threshold → SignalCompact
    // - If repeated tool call detected → SignalDoomLoop
    // - Otherwise → SignalContinue
}
```

### 5.6 Message Queuing (from Crush)

Essential for always-on operation. When a session is busy and a new prompt arrives (from Telegram, another TUI tab, or a cron job):

1. Prompt is queued in `messageQueue` (per-session FIFO)
2. At the start of each loop iteration, `drainQueue()` checks for queued messages
3. Queued messages are injected as additional user messages before the next LLM call
4. This lets users send follow-up instructions while the agent is working

### 5.7 Multi-Agent Orchestration

From the spec: agents should be composable in patterns like:
- 1 researcher + 1 reviewer, iterated N times
- N coders + M reviewers in pipeline
- LLM-determined parallelism (like OpenCode's plan mode)

**MVP approach**: The `armory` tool allows a primary agent to spawn subagents. The coordinator manages the subagent lifecycle — it calls `Run()` with the subagent's config and a new or child session.

**Post-MVP**: Complex multi-agent patterns are handled by **Workflows** (see section 12) — a separate concept from skills. A dedicated `Manager` agent for automation mode stands in for the user and executes workflows to drive sessions to completion.

### 5.8 Decisions

- **Subagents get their own sessions.** Isolated message history keeps context clean, allows independent compaction, and prevents subagent work from polluting the parent context. The parent receives a summary result via the `armory` tool response.

- **Runner has an explicit Stop function.** Each runner holds a cancellable context. Subagents can be stopped by user command or by the parent session; the main session is stopped by ctrl+c. `Stop()` cancels the runner's context, which propagates to the in-flight provider stream and any tool execution.

### 5.9 Revisitable

- [ ] Subagent result format (full messages vs. summary)
- [ ] Automation mode Manager agent design
- [ ] Anthropic prompt caching strategy (cache breakpoints on tools + system message, from Crush)

---

## 6. Execution Pipeline

```
User Input (TUI / Telegram / API)
    │
    ▼
Gateway receives prompt
    │
    ▼
Coordinator.Run(sessionID, prompt)
    │
    ├─► Session.GetOrCreate(sessionID)
    ├─► Memory.Retrieve(prompt, project, strategy)  ── fetch relevant context
    ├─► Agent.Select(session.agentName)
    ├─► Tools.BuildForAgent(agent.Info())            ── filter by permissions
    │
    ▼
Agent.Run(ctx, call)
    │
    ├─► Provider.Stream(messages, tools, systemPrompt)
    │       │
    │       ├── OnTextDelta(delta)      → publish to UI
    │       ├── OnToolCall(name, args)  → execute tool
    │       │       │
    │       │       ├── Permission.Check(tool, args)
    │       │       ├── Tool.Execute(ctx, args)
    │       │       └── return result to LLM
    │       ├── OnReasoningDelta(delta) → publish to UI
    │       └── OnFinish()
    │
    ▼
Post-processing
    ├─► Session.AppendMessages(messages)     ── persist to JSONL
    ├─► Compact.CheckThreshold(session)      ── prune if needed
    ├─► Memory.MaybeIndex(session)           ── index new content
    └─► Publish session.updated event
```

### 6.1 Context Compaction

Synthesized from moltbot (two-phase with short-circuit, configurable pruning), OpenCode (compaction agent, doom loop detection, non-destructive storage), and Crush (detailed summary template, interrupted tool call requeuing).

#### Detection

Check **after each LLM step completes** (OpenCode pattern). This is simpler than Crush's mid-stream interrupt and avoids losing partial work.

```go
func (c *Coordinator) shouldCompact(session *Session, usage TokenUsage) bool {
    if !c.config.Compaction.Auto {
        return false
    }
    contextWindow := c.provider.ContextWindow(session.Model)
    totalUsed := usage.PromptTokens + usage.CompletionTokens
    remaining := contextWindow - totalUsed

    // Large models (>200K): fixed 20K buffer
    // Small models: 20% of context window
    threshold := int64(20_000)
    if contextWindow <= 200_000 {
        threshold = int64(float64(contextWindow) * 0.2)
    }
    return remaining <= threshold
}
```

#### Phase 1: Tool Output Pruning (cheap, no LLM call)

Walk messages backwards, replace old tool outputs with placeholders. This is the moltbot pattern with OpenCode's protected tools.

```go
type PruneConfig struct {
    ProtectTokens  int      // Protect last N tokens of tool output (default: 40_000)
    MinimumTokens  int      // Only prune if saving >= N tokens (default: 20_000)
    ProtectedTools []string // Never prune these tools (default: ["skill", "memory_search"])
    ProtectTurns   int      // Never prune last N user turns (default: 2)
}

func (c *Coordinator) pruneToolOutputs(sessionID string, cfg PruneConfig) PruneResult {
    msgs := c.messages.List(sessionID)

    // Walk backwards from newest
    // 1. Skip last ProtectTurns user turns (preserve immediate context)
    // 2. Accumulate tool output tokens until ProtectTokens reached
    // 3. Everything older becomes a prune candidate
    // 4. Skip ProtectedTools (e.g. "skill") — always kept.
    //    AdjacentProtected tools (e.g. "read") in the same turn are also kept.
    //    Other tools in the same turn are still prunable.
    // 5. If pruneable >= MinimumTokens, replace content with "[output pruned for context]"
    //    and set prunedAt timestamp. Otherwise, leave untouched.

    return PruneResult{
        PrunedTokens int
        PrunedCount  int
        DidPrune     bool
    }
}
```

**Sufficiency check** (from moltbot): After pruning, re-estimate token usage. If post-prune usage is under 80% of context window, **skip the expensive LLM summarization entirely**. Most sessions only need pruning.

```go
if pruneResult.DidPrune {
    postPruneTokens := c.estimateSessionTokens(sessionID)
    if postPruneTokens < int64(float64(contextWindow) * 0.8) {
        return nil // Pruning was sufficient, no summarization needed
    }
}
```

#### Phase 2: LLM Summarization (expensive, only when pruning isn't enough)

Uses a hidden `compaction` agent with a configurable model (from OpenCode). Default: Haiku for cheap summarization.

```go
func (c *Coordinator) summarize(ctx context.Context, sessionID string) error {
    agent := c.agents["compaction"]  // Hidden agent, uses small model
    msgs := c.messages.List(sessionID)

    // Build summarization prompt (Crush's detailed template)
    // Includes: Current State, Files & Changes, Technical Context,
    //           Strategy & Approach, Exact Next Steps
    // If session has todos, include them in the prompt

    // Call LLM with full conversation + summary prompt
    // No tools available (compaction agent has deny-all permissions)
    summary := c.provider.Stream(ctx, StreamRequest{
        Model:    agent.Model,  // Haiku by default
        Messages: msgs,
        System:   compactionSystemPrompt,
        // ... no tools ...
    })

    // Store summary as a new message with IsSummary=true
    c.messages.Append(sessionID, Message{
        Role:      "assistant",
        IsSummary: true,
        Parts:     []MessagePart{{Type: "text", Data: summary}},
    })

    // Update session to point to summary
    c.sessions.SetSummaryMessageID(sessionID, summaryMsg.ID)

    // Requeue interrupted work (from Crush)
    if lastAssistantHadPendingToolCalls(msgs) {
        c.messageQueue.Append(sessionID, QueuedPrompt{
            Prompt: fmt.Sprintf(
                "The previous session was interrupted for context compaction. "+
                "The initial user request was: `%s`", originalPrompt),
        })
    }

    return nil
}
```

#### Summary Prompt Template

Adapted from Crush's `summary.md` — the most thorough of the three codebases:

```
You are summarizing a conversation to preserve context for continuing work.
This summary will be the ONLY context available when the conversation resumes.
Assume all previous messages will be lost. Be thorough.

Required sections:

## Current State
- What task is being worked on (exact user request)
- Current progress and what's been completed
- What's being worked on right now (incomplete work)
- What remains to be done (specific next steps)

## Files & Changes
- Files modified (with brief description of changes)
- Files read/analyzed (why they're relevant)
- Key files not yet touched but will need changes

## Technical Context
- Architecture decisions made and why
- Patterns being followed
- Commands that worked and failed
- Environment details

## Strategy & Approach
- Overall approach and why chosen
- Key insights or gotchas discovered
- Assumptions made

## Exact Next Steps
1. [Specific, numbered steps to continue]
```

#### Message Rebuild After Compaction

Non-destructive (from Crush and OpenCode). Old messages stay in JSONL but are skipped on load.

```go
func (s *Service) GetSessionMessages(sessionID string) []Message {
    msgs := s.store.LoadAll(sessionID)  // Full JSONL

    if session.SummaryMessageID != "" {
        // Find summary message position
        idx := findMessageIndex(msgs, session.SummaryMessageID)
        // Discard everything before it
        msgs = msgs[idx:]
        // Convert summary from assistant → user role (it becomes context input)
        msgs[0].Role = "user"
    }
    return msgs
}
```

#### Compaction Config

```go
type CompactionConfig struct {
    Auto           bool   `json:"auto"`            // Enable auto-compaction (default: true)
    Prune          bool   `json:"prune"`           // Enable tool output pruning (default: true)
    Model          string `json:"model"`           // Model for summarization (default: haiku)
    ProtectTokens  int    `json:"protect_tokens"`  // Tokens to protect from pruning (default: 40000)
    MinimumTokens  int    `json:"minimum_tokens"`  // Minimum savings to trigger prune (default: 20000)
    ProtectedTools    []string `json:"protected_tools"`    // Tools to never prune (default: ["skill"])
    AdjacentProtected []string `json:"adjacent_protected"` // Tools protected when in same turn as a ProtectedTool (default: ["read"])
}
```

#### Complete Compaction Sequence

```
1. DETECTION (after each LLM step)
   └─ (ContextWindow - TokensUsed) <= Threshold?

2. PHASE 1: PRUNE (cheap)
   ├─ Walk messages backwards
   ├─ Protect last 2 turns
   ├─ Protect skill/memory_search outputs
   ├─ Replace old tool outputs with "[output pruned for context]"
   └─ SUFFICIENCY CHECK: post-prune < 80% context? → DONE (skip Phase 2)

3. PHASE 2: SUMMARIZE (expensive, only if prune insufficient)
   ├─ Use compaction agent (Haiku by default)
   ├─ Send full conversation + detailed summary prompt
   ├─ Store summary message (IsSummary=true)
   ├─ Set session.SummaryMessageID
   └─ Requeue interrupted tool calls if any

4. REBUILD (on next message load)
   ├─ Find summary message position
   ├─ Discard messages before it
   ├─ Convert summary to user role
   └─ Continue with [summary] + [recent messages]
```

### 6.2 Doom Loop Detection

From OpenCode. If the agent makes 3 consecutive identical tool calls (same tool name + same input arguments), halt and report to the user. This is checked during stream processing, independent of compaction.

```go
const doomLoopThreshold = 3

func (c *Coordinator) isDoomLoop(recentToolCalls []ToolCallRecord) bool {
    if len(recentToolCalls) < doomLoopThreshold {
        return false
    }
    last := recentToolCalls[len(recentToolCalls)-doomLoopThreshold:]
    first := last[0]
    for _, tc := range last[1:] {
        if tc.ToolName != first.ToolName || tc.InputHash != first.InputHash {
            return false
        }
    }
    return true
}
```

**Response**: Publish error event to UI/Telegram. In interactive mode, ask user whether to continue or abort. In automation mode, halt and log.

### 6.3 Revisitable

- [ ] Multi-stage chunked summarization for extremely long sessions (moltbot pattern — split history into token-balanced chunks, summarize each, merge)
- [ ] Per-request soft-trim layer (moltbot's `contextPruning` — in-memory head+tail trim without rewriting session)
- [ ] Plugin-customizable compaction prompts (OpenCode's `experimental.session.compacting` hook)
- [ ] Whether compaction model should auto-upgrade to Opus for critical/complex sessions
- [ ] Token estimation: heuristic (`len/4`) vs actual tokenizer

---

## 7. Session Management

### 7.1 Session Model

```go
type Session struct {
    ID          string    `json:"id"`
    ProjectID   string    `json:"project_id"`
    Title       string    `json:"title"`
    AgentName   string    `json:"agent_name"`
    Directory   string    `json:"directory"`
    ParentID    string    `json:"parent_id,omitempty"` // For forks
    CreatedAt   time.Time `json:"created_at"`
    UpdatedAt   time.Time `json:"updated_at"`
    TokenUsage  TokenUsage `json:"token_usage"`
}
```

### 7.2 Storage

- **Session metadata**: `~/.nous/sessions/{projectID}/{sessionID}/session.json`
- **Messages**: `~/.nous/sessions/{projectID}/{sessionID}/messages.jsonl`
- **One line per message** in JSONL, append-only

### 7.3 Message Model (Parts-Based)

Inspired by OpenCode's part decomposition:

```go
type Message struct {
    ID        string        `json:"id"`
    Role      string        `json:"role"`  // "user" | "assistant" | "tool" | "system"
    Parts     []MessagePart `json:"parts"`
    Model     string        `json:"model,omitempty"`
    CreatedAt time.Time     `json:"created_at"`
}

type MessagePart struct {
    Type string `json:"type"` // "text" | "tool_call" | "tool_result" | "reasoning" | "file"
    Data json.RawMessage `json:"data"`
}
```

Part types:
- `text`: Plain text content
- `tool_call`: Tool name + input + state (pending/complete/error)
- `tool_result`: Tool output + metadata
- `reasoning`: Extended thinking content
- `file`: File attachment or snapshot

### 7.4 Revisitable

- [ ] Whether to add SQLite for session indexing/search alongside JSONL
- [ ] Session archival and cleanup policy
- [ ] Session forking implementation details

---

## 8. Memory System

The core differentiator. Three-tiered memory with automatic consolidation.

### 8.1 Memory Tiers

```
┌─────────────────────────────────┐
│     Tier 1: Strategy Memory     │  Per trading strategy
│  ~/code/gandiva/{strategy}/     │  Research done, results, what to try
│  memory/                        │
├─────────────────────────────────┤
│     Tier 2: Project Memory      │  Overall project state
│  ~/code/gandiva/memory/         │  Hypotheses, test results, patterns
│                                 │
├─────────────────────────────────┤
│     Tier 3: System Memory       │  General learnings
│  ~/.nous/memory/                │  Session transcripts, cross-project
│                                 │  patterns, tool usage insights
└─────────────────────────────────┘
```

### 8.2 RAG Integration

The existing Gandiva RAG server (`~/code/gandiva-memory/rag/server.py`) provides:
- FAISS vector search (semantic, `bge-base-en-v1.5`)
- BM25 keyword search
- Adaptive hybrid retrieval with dual-match boosting
- HTTP API: `POST /context`, `POST /index`, `GET /status`

**MVP approach**: Nous calls the RAG server as an HTTP client. The RAG server runs as a separate process (or systemd service).

```go
type RAGClient struct {
    baseURL string  // http://localhost:8103
}

func (r *RAGClient) Query(ctx context.Context, query string, topK int) ([]MemoryChunk, error)
func (r *RAGClient) Reindex(ctx context.Context) error
```

### 8.3 Memory Retrieval Flow

When a session prompt arrives:
1. Query RAG server with the prompt text
2. Scope results by tier:
   - If session is strategy-scoped → query strategy + project + system memory
   - If session is project-scoped → query project + system memory
3. Inject results into system prompt as context
4. Optionally: load pinned memory files directly (like `CLAUDE.md` pattern)

### 8.4 Memory Consolidation

Internal cron job (e.g., daily or on-demand):
1. Summarize recent session transcripts → write to system memory tier
2. Extract key findings from sessions → promote to project/strategy memory
3. Deduplicate and prune stale entries
4. Trigger RAG reindex

**MVP**: Manual trigger via command or cron. Use Haiku for summarization.

### 8.5 Revisitable

- [ ] Whether to rewrite the RAG server in Go or keep calling the Python service
- [ ] Embedding model choice (local vs API-based)
- [ ] Consolidation frequency and rules (what gets promoted upward)
- [ ] Whether strategy-level memory scoping works via directory convention or explicit config
- [ ] File watcher for automatic reindexing vs. manual/cron

---

## 9. Provider Layer

### 9.1 Interface

```go
type Provider interface {
    Stream(ctx context.Context, req StreamRequest) (*StreamResponse, error)
    Models() []ModelInfo
    Name() string
}

type StreamRequest struct {
    Model       string
    Messages    []ProviderMessage
    Tools       []ToolDef
    System      string
    MaxTokens   int
    Temperature float64
    // Callbacks
    OnTextDelta     func(delta string)
    OnToolCall      func(id, name string, input json.RawMessage)
    OnReasoningDelta func(delta string)
    OnFinish        func(usage TokenUsage)
}

type StreamResponse struct {
    Messages []ProviderMessage
    Usage    TokenUsage
    StopReason string
}
```

### 9.2 MVP: Anthropic Only

Use `anthropics/anthropic-sdk-go` directly.

```go
type AnthropicProvider struct {
    client *anthropic.Client
}
```

Models:
- **Opus 4.6** — primary model for coding, research, complex tasks
- **Haiku** — cron jobs, summarization, memory consolidation, compaction

### 9.3 Auth

From spec: use Anthropic Pro/Max subscription auth.

**MVP**: API key via environment variable (`ANTHROPIC_API_KEY`). Investigate OpenClaw's Pro/Max OAuth flow post-MVP.

### 9.4 Revisitable

- [ ] Adding OpenAI/other providers
- [ ] Pro/Max subscription auth (OAuth flow from OpenClaw)
- [ ] Model fallback chains
- [ ] Token cost tracking and budgets

---

## 10. Tool System

### 10.1 Interface

```go
type Tool interface {
    Name() string
    Description() string      // Loaded from .md template
    Parameters() JSONSchema   // JSON Schema for input
    Execute(ctx ToolContext, input json.RawMessage) (*ToolResult, error)
}

type ToolContext struct {
    SessionID   string
    MessageID   string
    AgentName   string
    WorkDir     string
    Abort       <-chan struct{}
    Permissions *permission.Service
}

type ToolResult struct {
    Output   string
    Metadata map[string]any
    Error    string
}
```

### 10.2 MVP Tools

| Tool | Purpose |
|------|---------|
| `bash` | Shell execution |
| `read` | Read file contents |
| `write` | Write/create files |
| `edit` | Modify files |
| `glob` | Find files by pattern |
| `grep` | Search file contents |
| `ls` | List directory |
| `fetch` | HTTP fetch + markdown convert |
| `skill` | Load skill context on demand |
| `armory` | Spawn subagent |

### 10.3 Tool Descriptions

Each tool has a companion `descriptions/{name}.md` file with detailed usage instructions. These are loaded at startup and passed to the LLM as the tool description. Keeps Go code clean, descriptions rich.

### 10.4 Permissions

Simple allowlist for MVP:

```go
type PermissionService struct {
    allowedTools []string    // Empty = all allowed
    autoApprove  bool        // YOLO mode from config
}
```

When a tool executes, check if it needs approval. TUI shows prompt; Telegram sends approval request; automation mode auto-approves.

### 10.5 Revisitable

- [ ] Pattern-based permissions (like OpenCode's `"*.env": "ask"`)
- [ ] Tool output truncation limits
- [ ] Parallel tool execution within a session
- [ ] LSP integration as a tool

---

## 11. Skills

Skills are **contextual knowledge documents** that the agent loads on demand. They are not eagerly injected into every prompt — the agent decides when it needs a skill and loads it via the `skill` tool (OpenCode pattern). This keeps the base context clean and lets us have many skills without bloating every request.

### 11.1 Discovery

Skills are `SKILL.md` files discovered from (in precedence order):
1. `.nous/skills/` in project directory (project-scoped, highest priority)
2. `~/.nous/skills/` (user-defined)
3. `skills/` in the nous repo (bundled, lowest priority)

Discovery scans for `**/SKILL.md` in each directory. If a skill name appears in multiple sources, the highest-precedence source wins.

### 11.2 Format

```markdown
---
name: backtest-review
description: Review a backtest result and suggest improvements
---

# Backtest Review

When reviewing a backtest result:

1. Load the backtest output file
2. Analyze key metrics: Sharpe ratio, max drawdown, win rate
3. Compare against baseline strategy
4. Identify potential improvements
5. Write findings to strategy memory
```

Frontmatter is minimal: `name` and `description` only. The body is the instruction content.

### 11.3 Skill Tool

The `skill` tool is a built-in tool available to all agents:

```go
// Tool: skill
// Parameters: { name: string }
// Output: skill markdown content wrapped in context markers
```

When the agent calls the skill tool:
1. Look up skill by name
2. Return the full markdown content
3. Content is injected into the conversation as a tool result
4. Agent now has the skill's instructions in context and can follow them

The agent also sees a list of available skills (name + description) in its system prompt, so it knows what's available to load.

### 11.4 User Invocation

Users can also trigger skills directly:
- `/backtest-review` in TUI or Telegram
- This injects the skill content as a user message prefix, prompting the agent to follow it

### 11.5 Skill Files

A skill directory can contain supporting files alongside `SKILL.md`:
```
skills/backtest-review/
├── SKILL.md              # Main skill instructions
├── metrics-reference.md  # Supporting reference doc
└── example-output.md     # Example of expected output
```

When loaded, the tool reports these companion files so the agent can read them if needed.

### 11.6 Revisitable

- [ ] Whether skills can define structured parameters
- [ ] Skill-level memory scoping (a skill that always loads specific files)
- [ ] Remote skill fetching (like OpenCode's `skills.urls`)

---

## 12. Workflows

Workflows are a separate concept from skills. While skills provide **knowledge and instructions**, workflows define **multi-agent orchestration patterns** — how agents should be composed and coordinated to accomplish complex tasks.

### 12.1 Core Model: Radio Bus + Captain

The workflow model is a **flat peer group with shared broadcast**. Instead of round-robin turns on a shared thread, agents run concurrently with their own sessions, connected by a broadcast bus ("radio"). A designated captain agent oversees the group.

```
Workflow starts
    ↓
Captain spawns N agents, each with a role prompt and own session
    ↓
All agents (including captain) subscribe to the Radio bus
    ↓
Agents work concurrently:
  - Each has its own session, tools scoped to role
  - When an agent produces text output, it broadcasts to Radio
  - All other agents receive the broadcast as input
  - Agents react, continue working, or broadcast back
    ↓
Captain monitors all broadcasts:
  - Resolves conflicts by prompting specific agents
  - Redirects work when agents are stuck or duplicating effort
  - Determines when the workflow is complete
    ↓
Captain signals done → all agent sessions end
```

This mirrors how a team with walkie-talkies works: everyone hears everything, a lead keeps things on track, each person works independently.

### 12.2 Radio Bus

The radio is a typed `pubsub.Broker[RadioMessage]` scoped to a single workflow. Every agent subscribes on start and unsubscribes when the workflow ends.

```go
type RadioMessage struct {
    FromAgent   string    // agent name/role that sent it
    FromSession string    // source session ID
    Text        string    // the broadcast content
    Type        RadioType // "output" | "status" | "request"
    Timestamp   time.Time
}

type RadioType string
const (
    RadioOutput  RadioType = "output"  // agent produced a result
    RadioStatus  RadioType = "status"  // progress update
    RadioRequest RadioType = "request" // asking for help or input
)
```

When an agent's runner produces a text response (not a tool call), the workflow wrapper broadcasts it to the radio. Incoming radio messages are injected into the agent's session as user messages tagged with the sender's role, so the agent sees them in context.

### 12.3 Captain Agent

The captain is a regular agent with an elevated role prompt and access to a `signal` tool for workflow control.

```go
type CaptainConfig struct {
    AgentName  string // which agent config to use (e.g. "coder")
    RolePrompt string // "You are the captain. Monitor progress, resolve conflicts..."
}
```

**Captain responsibilities:**
- Receives all radio broadcasts like any other agent
- Can send directed messages to specific agents (injected as user prompts into their sessions)
- Resolves conflicts (e.g. two agents editing the same file)
- Determines when the workflow objective is met
- Signals workflow completion via the `signal` tool

**Captain tools** (in addition to standard tools):
- `signal` — `{ "action": "done" | "abort", "summary": string }` — ends the workflow
- `direct` — `{ "agent": string, "message": string }` — sends a prompt to a specific agent without broadcasting

### 12.4 Workflow Definition

```go
type Workflow struct {
    Name        string
    Description string
    Captain     CaptainConfig
    Agents      []WorkflowAgent
    MaxTokens   int64             // Budget cap on total token spend across all agents
    Timeout     time.Duration     // Hard time limit
}

type WorkflowAgent struct {
    AgentName  string   // References AgentInfo from agent registry
    RolePrompt string   // "Implement the authentication module"
    Tools      []string // Tool whitelist override (nil = use agent default)
}
```

No round or turn concept — agents run freely. The captain and budget/timeout are the only controls.

### 12.5 Execution

```go
func (c *Coordinator) RunWorkflow(ctx context.Context, wf Workflow, initialPrompt string) error {
    ctx, cancel := context.WithTimeout(ctx, wf.Timeout)
    defer cancel()

    radio := pubsub.NewBroker[RadioMessage]()
    defer radio.Shutdown()

    // Spawn worker agents as goroutines, each with own session
    var wg sync.WaitGroup
    for _, wa := range wf.Agents {
        wg.Add(1)
        go func(wa WorkflowAgent) {
            defer wg.Done()
            c.runWorkflowAgent(ctx, wa, radio)
        }(wa)
    }

    // Run captain (blocks until captain signals done or ctx cancels)
    c.runCaptain(ctx, wf.Captain, radio, initialPrompt)

    cancel() // stop all worker agents
    wg.Wait()
    radio.Shutdown()

    return nil
}
```

### 12.6 Agent-Radio Integration

Each workflow agent's runner is wrapped with radio I/O:

```go
func (c *Coordinator) runWorkflowAgent(ctx context.Context, wa WorkflowAgent, radio *pubsub.Broker[RadioMessage]) {
    sess := c.sessions.Create(...)
    sub := radio.Subscribe()

    // Goroutine: inject incoming radio messages as user messages
    go func() {
        for msg := range sub {
            if msg.FromSession == sess.ID {
                continue // don't echo own broadcasts
            }
            inject := fmt.Sprintf("[%s]: %s", msg.FromAgent, msg.Text)
            c.sessions.AppendMessage(sess.ID, userMessage(inject))
            // Queue a re-prompt so the agent processes the new input
        }
    }()

    // Run the agent loop — on each text output, broadcast to radio
    runner := c.newRunner(wa, sess)
    runner.OnTextComplete = func(text string) {
        radio.Publish(RadioMessage{
            FromAgent:   wa.RolePrompt,
            FromSession: sess.ID,
            Text:        text,
            Type:        RadioOutput,
            Timestamp:   time.Now().UTC(),
        })
    }
    runner.Run(ctx, sess, wa.RolePrompt)
}
```

### 12.7 Examples

**Research + Review:**
```go
Workflow{
    Captain: CaptainConfig{
        AgentName:  "coder",
        RolePrompt: "Monitor the researcher and reviewer. When the report quality is sufficient, signal done.",
    },
    Agents: []WorkflowAgent{
        {AgentName: "researcher", RolePrompt: "Research X and write a report. Respond to reviewer feedback."},
        {AgentName: "researcher", RolePrompt: "Review reports broadcast on the radio. Critique gaps, suggest improvements."},
    },
}
```
The researcher broadcasts a report. The reviewer hears it, broadcasts critique. The researcher hears the critique, improves, broadcasts again. The captain watches and signals done when satisfied.

**Parallel coding:**
```go
Workflow{
    Captain: CaptainConfig{
        AgentName:  "coder",
        RolePrompt: "Coordinate three coders implementing features A, B, C. Resolve file conflicts. Review final output.",
    },
    Agents: []WorkflowAgent{
        {AgentName: "coder", RolePrompt: "Implement feature A. Avoid modifying files others are working on."},
        {AgentName: "coder", RolePrompt: "Implement feature B. Avoid modifying files others are working on."},
        {AgentName: "coder", RolePrompt: "Implement feature C. Avoid modifying files others are working on."},
    },
}
```
All three coders work simultaneously. When one broadcasts "done with feature A, modified files X, Y, Z", the others adjust. Captain resolves any conflicts.

### 12.8 Tradeoffs

| Concern | Mitigation |
|---------|------------|
| **Cost** — every agent sees every broadcast | Radio messages are short text summaries, not full sessions. Agents compact independently. |
| **Noise** — agents get distracted by irrelevant broadcasts | Captain can use `direct` for targeted messages. Role prompts tell agents what to ignore. |
| **Conflicts** — two agents edit the same file | Captain monitors and intervenes. Agents broadcast what files they're touching. |
| **Runaway** — agents keep working forever | Timeout + MaxTokens hard caps. Captain signals done. |
| **Context growth** — radio messages accumulate in each session | Each agent's session compacts independently. Old radio messages get pruned like any other input. |

### 12.9 Automation Mode

In automation mode, a **Manager agent** stands in for the user. The Manager can:
1. Execute pre-defined workflows (the Manager becomes the captain or spawns one)
2. Dynamically construct workflows — decide agent count, roles, and constraints based on the task
3. Use `armory` tool for simple one-off subagent spawning when a full workflow is overkill

### 12.10 Revisitable

- [ ] Workflow state persistence (resume interrupted workflows across restarts)
- [ ] Radio message filtering (agents opt into specific topics or roles)
- [ ] Per-agent token budgets (in addition to workflow-wide MaxTokens)
- [ ] Whether radio messages should be summarized before injection (to reduce context growth)
- [ ] Workflow definition format (Go code vs. YAML/JSON config files)
- [ ] Whether the captain should be an LLM agent or a deterministic state machine for simple workflows
- [ ] Workflow nesting (a workflow agent that itself runs a sub-workflow)

---

## 13. Telegram Integration

### 13.1 Architecture

The Telegram bot runs inside the gateway daemon as a goroutine.

```go
type TelegramBot struct {
    token       string
    coordinator *agent.Coordinator
    allowedUser int64   // Single authorized user ID
}
```

### 13.2 Features (MVP)

- Receive messages → create/continue session
- Stream agent responses back as Telegram messages
- `/new` — start new session
- `/sessions` — list recent sessions
- `/cancel` — cancel active agent run
- Permission approval via inline keyboard buttons

### 13.3 Revisitable

- [ ] Telegram library choice (`go-telegram-bot-api` vs `telebot` vs `gotd`)
- [ ] File/image attachment handling
- [ ] Message length limits and chunking

---

## 14. TUI

### 14.1 Framework

Bubbletea v1 + Lipgloss v1 + Bubbles v1. We use `github.com/charmbracelet/*` module paths — the v2 RC (`charm.land/*`) has broken module paths as of 2026-02 and should not be used.

### 14.2 Architecture

The TUI runs in standalone mode — it owns the Runner directly (no gateway). The App model is the root Bubbletea model. It communicates with the agent runner via a typed `events chan tea.Msg` channel. The runner pushes events (text deltas, tool start/done, subagent lifecycle) into the channel; a goroutine reads and feeds them into the Bubbletea program via `p.Send()`.

```
┌─────────────────────────────────────────────────────────┐
│                     Terminal (Alt Screen)                │
│                                                          │
│  ┌──────────┬───────────────────────────────────────┐   │
│  │          │  [Subagent Pane 1]  (if active)       │   │
│  │          ├───────────────────────────────────────┤   │
│  │ Sidebar  │  [Subagent Pane 2]  (if active)       │   │
│  │ (session │  ├─────────────────────────────────┤   │   │
│  │  list)   │  Main Chat (viewport)                 │   │
│  │          │                                       │   │
│  │          │                                       │   │
│  │          ├───────────────────────────────────────┤   │
│  │          │  Input / Permission Prompt             │   │
│  ├──────────┴───────────────────────────────────────┤   │
│  │  Status Bar                                       │   │
│  └───────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### 14.3 Components

| Component | File | Purpose |
|-----------|------|---------|
| `App` | `app.go` | Root model. Owns all sub-models, routes events, manages layout. |
| `ChatModel` | `chat.go` | Scrollable viewport for message rendering and streaming. |
| `InputModel` | `input.go` | Multi-line textarea for user input. |
| `SidebarModel` | `sidebar.go` | Session list with selection highlight. |
| `StatusModel` | `status.go` | Bottom bar: model, session ID, token count, memory status. |
| `PermissionModel` | `permission.go` | Inline tool approval prompt (y/n). |

**Theme** (`theme.go`): All colors, layout constants, and reusable styles in one place.

**Events** (`events.go`): Typed message structs for App ↔ Runner communication:
- `textDeltaMsg`, `toolStartMsg`, `toolDoneMsg`, `runDoneMsg`
- `subagentStartMsg`, `subagentDoneMsg`, `subagentTextDeltaMsg`, `subagentToolStartMsg`, `subagentToolDoneMsg`
- `permissionRequestMsg`, `memoryStatusMsg`, `tokenUpdateMsg`

### 14.4 Layout System

Height budget is calculated in `layout()`:
```
totalHeight = termHeight - inputHeight(3) - statusBar(1) - focusBorders(2)
chatWidth   = termWidth - sidebarWidth(26) - sidebarBorder(1) - padding
```

When subagent panes are active, the top portion of `totalHeight` is split evenly among them (capped at 40% or 10 lines each, minimum 5 per pane), with the remainder going to the main chat.

Output is force-clamped to exactly `termHeight` lines in `View()` to prevent terminal scrolling artifacts from lipgloss width-wrapping.

### 14.5 Subagent Split Panes

When the runner spawns subagents via the `armory` tool, each gets a dedicated `ChatModel` pane rendered above the main chat. Events are routed by child session ID.

- `subagentStartMsg` → create pane, recalculate layout
- `subagentTextDeltaMsg` / `subagentToolStartMsg` / `subagentToolDoneMsg` → forward to pane
- `subagentDoneMsg` → remove pane, recalculate layout

Multiple armory calls in the same turn execute concurrently (goroutines + WaitGroup in runner), so multiple panes stream simultaneously.

### 14.6 Permission Queuing

Only one permission prompt is shown at a time. When concurrent subagents both need tool approval, requests are queued in `permQueue []permissionRequestMsg`. After the user resolves the current prompt, the next queued request is shown. The permission prompt renders inline — it replaces the input area when active.

### 14.7 Scrolling and Input

- **Mouse wheel**: Default mode. `tea.WithMouseCellMotion()` captures mouse events; wheel scrolls the chat viewport by 3 lines.
- **Ctrl+S**: Toggles select mode (disables mouse capture for native terminal text selection). Status bar shows `SELECT` indicator.
- **PgUp/PgDn**: Half-page scroll in chat viewport.
- **Ctrl+Left/Right**: Word-level cursor navigation in input textarea.
- **Input stays active during streaming**: Users can type while the LLM runs; Enter is guarded by `!a.running`.

### 14.8 Animation

A single `tea.Tick` at 500ms in App drives all animation:
- Blinking dot (●) while waiting for LLM response
- Alternating tool spinner (▸/▹) during tool execution

`ChatModel.ToggleAnimation()` is called on each tick, toggling `dotVisible` and rebuilding the view only if animation is needed.

### 14.9 Chat Rendering

Content is built incrementally in a `strings.Builder`:
- User messages: styled with background, prefixed with `> `
- Tool calls: `+ toolName args` in muted style
- Tool errors: `x toolName args` in muted style
- Tool output: indented, truncated to 15 lines
- Edit diffs: colored add/remove/context lines with line numbers
- Streaming text: appended raw, flushed to content on completion

The viewport auto-scrolls to bottom when the user is already at the bottom (preserves scroll position if user has scrolled up).

### 14.10 Connection

Currently standalone — TUI owns the runner directly. Gateway mode (WebSocket connection) is deferred.

```bash
nous              # Start TUI (standalone, runs runner directly)
nous chat "prompt" # Non-interactive streaming to stdout
nous run "prompt"  # Non-interactive single prompt
```

### 14.11 Revisitable

- [ ] Gateway mode (TUI connects to daemon via WebSocket)
- [ ] Web UI via xterm.js + WebSocket (ttyd), Wish (SSH server), or Bubble Tea Live
- [ ] Session rendering detail level (collapsed/expanded tool calls)
- [ ] Vim-style keybindings

---

## 15. Cron System

Internal scheduler for recurring tasks.

### 15.1 Jobs (MVP)

| Job | Schedule | Purpose |
|-----|----------|---------|
| Memory consolidation | Daily | Summarize sessions, promote findings |
| RAG reindex | On memory change | Keep search index fresh |
| Health check | Every 5min | Gateway self-check |

### 15.2 Implementation

Simple ticker-based scheduler. No external dependencies.

```go
type CronService struct {
    jobs []CronJob
}

type CronJob struct {
    Name     string
    Schedule time.Duration  // MVP: simple intervals
    Run      func(ctx context.Context) error
}
```

### 15.3 Revisitable

- [ ] Cron expression syntax (like OpenClaw) vs. simple intervals
- [ ] User-defined cron jobs via config
- [ ] Cron jobs that trigger agent sessions (e.g., "check markets every morning")

---

## 16. Configuration

### 16.1 File

`~/.nous/config.json` (JSON, no schema validation for MVP)

```json
{
  "gateway": {
    "port": 18800,
    "bind": "127.0.0.1"
  },
  "provider": {
    "type": "anthropic",
    "api_key": "$ANTHROPIC_API_KEY",
    "default_model": "claude-opus-4-6",
    "small_model": "claude-haiku-4-5-20251001"
  },
  "telegram": {
    "token": "$TELEGRAM_BOT_TOKEN",
    "allowed_user": 123456789
  },
  "memory": {
    "strategy_dirs": ["~/code/gandiva/*/memory"],
    "project_dir": "~/code/gandiva/memory",
    "system_dir": "~/.nous/memory",
    "rag_url": "http://localhost:8103"
  },
  "projects": {
    "gandiva": {
      "directory": "~/code/gandiva",
      "context_files": ["CLAUDE.md", ".cursorrules"]
    }
  },
  "permissions": {
    "auto_approve": false
  }
}
```

### 16.2 Revisitable

- [ ] JSON Schema generation from Go structs (like Crush)
- [ ] Config validation at startup
- [ ] Per-project config overrides (`.nous/config.json` in project root)
- [ ] Config hot-reload vs. requiring restart

---

## 17. Logging & Observability

### 17.1 Structured Logging

```go
log.Info("agent.run",
    "session_id", sessionID,
    "agent", agentName,
    "model", modelID,
    "prompt_tokens", usage.PromptTokens,
)
```

Use `log/slog` (stdlib). Subsystem-tagged.

### 17.2 Session Export

For debugging and analysis:
```bash
nous session export {sessionID}          # Dump full session as JSON
nous session export {sessionID} --context # Dump what the LLM actually saw
nous session export {sessionID} --compact # Show compacted context
```

### 17.3 Revisitable

- [ ] Log rotation and retention
- [ ] Metrics collection (token usage over time, cost tracking)
- [ ] Log level configuration per subsystem

---

## 18. Concurrency Model

### 18.1 Thread-Safe Types (from Crush)

```go
// csync package
type Map[K comparable, V any]   // RWMutex-wrapped map
type Slice[T any]                // RWMutex-wrapped slice
type Value[T any]                // RWMutex-wrapped single value
```

### 18.2 Event Broker (from Crush)

```go
type Broker[T any] struct {
    subscribers []chan T   // Buffered channels (64)
}

func (b *Broker[T]) Publish(event T)
func (b *Broker[T]) Subscribe() <-chan T
```

Services publish events; TUI and gateway subscribe.

### 18.3 Patterns

- **Per-session message queue**: If agent is busy, queue incoming prompts
- **Goroutines for**: Telegram bot, cron jobs, WebSocket handlers, subagent execution
- **Context cancellation**: All operations take `context.Context`
- **Graceful shutdown**: `signal.NotifyContext` for SIGTERM/SIGINT

---

## 19. Data Flow Directories

```
~/.nous/                            # Nous home
├── config.json                     # Configuration
├── memory/                         # System-level memory (Tier 3)
│   ├── learnings.md
│   └── patterns.md
├── sessions/                       # All session data
│   └── {projectID}/
│       └── {sessionID}/
│           ├── session.json        # Session metadata
│           └── messages.jsonl      # Conversation transcript
├── logs/                           # Application logs
└── skills/                         # User-defined skills

~/code/gandiva/                     # Example project
├── memory/                         # Project memory (Tier 2)
├── {strategy}/
│   └── memory/                     # Strategy memory (Tier 1)
└── .nous/
    ├── config.json                 # Project-level config overrides
    └── skills/                     # Project-level skills
```

---

## 20. MVP Scope

### In Scope

- [ ] Gateway daemon with systemd installation
- [ ] WebSocket server for TUI connection
- [ ] Anthropic provider (Opus + Haiku, API key auth)
- [ ] Coordinator + single primary agent (`coder`)
- [ ] Core tools: bash, read, write, edit, glob, grep, ls, skill
- [ ] JSONL session storage
- [ ] Basic TUI: chat view, input, session list
- [ ] Telegram bot: receive/respond, session management
- [ ] Memory: RAG client calling existing Gandiva server
- [ ] Tiered memory loading into session context
- [ ] Context compaction (prune tool outputs + LLM summary)
- [ ] Structured logging with session export
- [ ] Configuration file loading
- [ ] Basic permission prompts (approve/deny per tool call)

### Deferred

- [ ] Subagent execution (`explorer`, `researcher` agents)
- [ ] WebUI
- [ ] Workflows (multi-agent orchestration patterns)
- [ ] Automation mode (Manager agent)
- [ ] Cron jobs
- [ ] Memory consolidation
- [ ] LSP integration
- [ ] MCP support
- [ ] Session forking
- [ ] Pro/Max subscription auth
- [ ] Additional providers

---

## 21. Dependency Shortlist

| Dependency | Purpose |
|------------|---------|
| `anthropics/anthropic-sdk-go` | Anthropic API client |
| `spf13/cobra` | CLI framework |
| `charmbracelet/bubbletea` (v1) | TUI framework |
| `charmbracelet/lipgloss` (v1) | TUI styling |
| `charmbracelet/bubbles` (v1) | TUI components (viewport, textarea) |
| `gorilla/websocket` or equivalent | WebSocket server |
| `log/slog` (stdlib) | Structured logging |
| `mvdan.cc/sh/v3` | Shell execution |
| `encoding/json` (stdlib) | JSON/JSONL handling |

Intentionally minimal. No ORM. No framework. Stdlib where possible.


