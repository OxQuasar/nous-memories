# Nous Architecture

> Coding orchestration layer for trading strategy research and development.
> Go implementation. Always-on. Persistent memory. Multi-agent.

---

## 1. Design Principles

1. **Debuggable first.** Session context, memory state, and agent decisions must be extractable and inspectable at any point.
2. **Transparent logging.** Structured logs with subsystem tags. Every LLM call, tool invocation, and memory retrieval is logged.
3. **Single-user, single-platform.** Linux only. No plugin system. Change source directly.
4. **Clean flows.** Large-scale structural changes should remain possible.

---

## 2. Directory Layout

```
nous/
├── main.go                 # Entry: cmd.Execute()
├── config.json             # Provider, compaction, permissions, memory config
├── cron.json               # Scheduled jobs
├── internal/               # All Go packages
│   ├── cmd/                # CLI commands (daemon, tui, run, chat, sessions)
│   ├── director/           # Core: Gateway, Director, Runner, LiveSession, EventBus, Logos
│   ├── agent/              # Agent configs + tool system
│   │   ├── agent.go        # AgentInfo definitions (session, code, explore, plan, etc.)
│   │   ├── prompt.go       # System prompt assembly
│   │   ├── templates/      # Embedded .md prompt templates per agent
│   │   └── tools/          # Tool implementations + BgManager
│   ├── provider/           # LLM provider abstraction (Anthropic)
│   ├── session/            # Session persistence (JSONL store + service)
│   ├── compact/            # Compaction: prune + summarize
│   ├── memory/             # RAG client + manager
│   ├── message/            # Multi-part message format
│   ├── permission/         # Tool execution gating
│   ├── ui/                 # Bubbletea TUI
│   ├── telegram/           # Telegram bot frontend
│   ├── transport/          # Daemon↔TUI unix socket wire protocol
│   ├── config/             # Config structs + loading
│   ├── project/            # Context file discovery (CLAUDE.md, git)
│   ├── skill/              # Skill discovery (SKILL.md files)
│   ├── logos/              # Workflow YAML parsing + topo sort
│   ├── cron/               # Scheduled job execution
│   ├── pubsub/             # Generic typed Broker[T]
│   ├── auth/               # Token management
│   ├── csync/              # Thread-safe generics (Map, Slice, Value)
│   └── log/                # Structured logging setup
├── logos/                  # LOGOS.yaml workflow definitions
└── memories/               # RAG-indexed: sessions/, daily_logs/, texts/
```

### Session storage on disk
```
~/.nous/sessions/<session-id>/
├── session.json            # Metadata (ID, Title, TokenUsage, SummaryMessageID, etc.)
├── messages.jsonl          # Append-only message log
└── logos_checkpoint.json   # (optional) logos workflow state
```
Subagent sessions nest inside parent: `<parent-id>/<child-id>/`

---

## 3. Package Responsibilities

### `internal/director/` — Core Orchestration

| File | Key Types | Role |
|------|-----------|------|
| `gateway.go` | `Gateway`, `Connection`, `Request` | Frontend↔Director bridge. Session locking, request dispatch. `Serve()` = blocking dispatch loop. `runLoop()` = prompt execution + queue drain. Lock ordering: `gw.mu → c.mu → ls.mu` |
| `director.go` | `Director` | Singleton. Owns Provider, Sessions, Compactor, Memory, tool/agent registries. `Run()`, `Spawn()`, `SpawnCustom()`. Creates LiveSessions. |
| `runner.go` | `runner` | Ephemeral per-run. Core loop: build prompt → stream LLM → determine signal → execute tools → repeat. Handles compaction, title gen, doom loop detection. |
| `livesession.go` | `LiveSession` | Runtime state per active session. EventBus, ToolContext, Perms, prompt/notification queues. Survives disconnects via `gw.live`. |
| `event.go` | `Event`, `EventType` | ~20 event types for frontend communication. |
| `eventbus.go` | `EventBus` | Fan-out pub/sub per LiveSession. Turn-buffered for replay. |
| `signal.go` | `Signal` | Step outcome: Stop, Continue, Compact, DoomLoop, PauseTurn, MaxTokens. |
| `logos.go` | `LogosEngine` | Multi-stage workflow executor (solo/parallel/discuss/gate modes). |

### `internal/agent/` — Agent & Tool System

| File | Role |
|------|------|
| `agent.go` | `AgentInfo` definitions. Builtin agents: session, code, explore, research, review, plan, sage, captain, condense. Each defines Mode, MaxSteps, tool whitelist, InheritContext, Reuse. |
| `prompt.go` | `BuildSystemPrompt()`: base template + env + project context + memory + skills. |

Key tools in `tools/`:
| File | Tool |
|------|------|
| `bash.go` | Shell exec. Foreground timeout + Ctrl+Z → background. |
| `background.go` | `BgManager`. GNU screen persistence. `Start()`, `Recover()`, `OnDone` callback. |
| `armory.go` | Subagent spawner → `Director.Spawn()`. |
| `edit.go` | String-replace with LCS diff. |
| `write.go` / `read.go` | File I/O with snapshots for undo. |
| `memory.go` | RAG search via closure. |
| `tool.go` | `Tool` interface, `ToolContext`, `ToolResult`, `DiffLine`. |

### `internal/provider/` — LLM

| File | Role |
|------|------|
| `provider.go` | `Provider` interface. `Stream(ctx, StreamRequest) → StreamResponse`. Streaming callbacks for text/tool/reasoning deltas. |
| `anthropic.go` | Anthropic SDK. Prompt caching (3 breakpoints: system, tools, last message). OAuth + API key auth. |
| `convert.go` | Session messages → provider messages. |

### `internal/session/` — Persistence

| File | Role |
|------|------|
| `session.go` | `Session` struct. Key fields: ID, ParentID, SummaryMessageID, TokenUsage, Telegram flag. |
| `service.go` | CRUD + `GetSessionMessages()` (handles summary pointer). `syncSessionText()` writes .md for RAG. |
| `store.go` | JSONL I/O. Append-only messages. Atomic metadata writes. Per-session mutex. |

### `internal/compact/` — Compaction

| File | Role |
|------|------|
| `compact.go` | `Compactor`. `ShouldCompact()` / `ShouldPreflightCompact()` check token headroom. `Compact()` = prune → summarize. |
| `prune.go` | Phase 1: Replace old tool outputs with placeholder. **Destructive** (rewrites JSONL). |
| `summarize.go` | Phase 2: LLM summary. **Non-destructive** — appends summary + protected tail to JSONL, sets `SummaryMessageID` pointer. |

### Frontends

| Package | Role |
|---------|------|
| `internal/ui/` | Bubbletea TUI. `App` owns ChatModel, InputModel, SidebarModel, PermissionModel, subagent panes. Slash command dispatch. |
| `internal/telegram/` | Telegram bot. Per-chat Connection. Message editing with 3s throttle, rolling at 4096 chars. |
| `internal/transport/` | Unix socket wire protocol. JSON-line encoding of Request/Event. Server bridges remote clients to Gateway. |

---

## 4. Core Flows

### Prompt → Response
```
TUI input → Request{ReqRun} → Conn.Send channel
  → [daemon: transport encodes over unix socket]
  → Connection.Serve() → dispatch() → ls.TryClaimRun()
  → go runLoop(ctx, ls, prompt)
    → dir.Run() → runner.run()
      → Store user message → pre-flight compact check → memory retrieval
      → LOOP: provider.Stream() → store assistant msg → determineSignal()
        → SignalContinue: executeTools() → store results → continue
        → SignalStop: return
      → Drain queued prompts → wait for bg processes → release run
    → ls.Emit(EventRunDone)
  → Events: runner → ls.Emit() → EventBus → Connection.viewCh → TUI
```

### Subagent Spawning
```
Agent calls armory → tctx.SpawnAgent() → Director.Spawn()
  → If taskID: resume existing session
  → Else if Reuse: find most recent idle child of same agent type
  → Else: CreateSession(childID, parentID)
  → newChildLS() (shares parent EventBus + Perms, depth+1)
  → If InheritContext && new session: inject parent messages as context
  → parent.Emit(EventSpawnStart)
  → runner.run(ctx, prompt) — events tagged with childID
  → parent.Emit(EventSpawnDone)
  → Return child's last text
```

### Detach / Reconnect
```
Detach: auto-approve pending perms → swap connCtx (old stays alive for runLoop)
  → cancel EventBus forwarding → persist in gw.live → unlock session
Reconnect: find gw.live[sessionID] → reuse LiveSession → re-attach EventBus
```

### Compaction
```
Phase 1 (prune): replace old tool outputs → rewrite JSONL (destructive)
Phase 2 (summarize): LLM summary → append to JSONL + set SummaryMessageID pointer
  → On load: GetSessionMessages skips everything before pointer (non-destructive)
```

### Permission
```
Default: read/glob/grep/ls → Allow, bash/write/edit → Ask
Ask: emit EventPermissionRequest → block on response channel
  → TUI shows overlay → user approves → ReqPermResponse → resolve
On Detach: auto-approve all, set autoApprove=true
```

---

## 5. Key Properties

- **LiveSession is the operational unit**, not Connection. Connections attach/detach as views.
- **EventBus is per-LiveSession**, shared with children. Child events tagged with childID.
- **JSONL on disk**, no database. Append-only messages, atomic metadata writes.
- **Compaction: prune is destructive, summarize is non-destructive** (pointer-based skip on load).
- **All time is UTC.**
- **Single-process**: Gateway + all agents + all sessions in one process.
- **GNU screen** for background process persistence across daemon restarts.
- **RAG is a Python sidecar** (`internal/memory/rag_server.py`), port **8103**, BGE-M3 embeddings. Spawned by daemon, health at `/health`.
- **Prompt caching**: 4 Anthropic cache breakpoints (shared system context, agent-specific system, tools, last message). System prompt split into shared context block (project files, env, skills) and agent-specific block (template, memory) for cross-agent prefix sharing. Default 5min TTL.
