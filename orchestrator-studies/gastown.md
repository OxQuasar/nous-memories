# Gastown Architecture: High-Level Agent Coordination

## Core Metaphor: A "Town" of Specialized Agents

Gastown models multi-agent coordination as a **town** where different agents have distinct roles, all communicating through a shared database ("beads") and a mail system. Each agent runs as an independent **Claude Code session inside tmux**.

## Agent Hierarchy

```
Daemon (Go process, no LLM)
├── Mayor (LLM agent - town coordinator)
├── Deacon (LLM agent - persistent patrol/health)
│   ├── Boot (LLM agent - ephemeral triage per tick)
│   └── Dogs (LLM workers - cross-rig infrastructure)
├── Per-Rig agents:
│   ├── Witness (LLM agent - monitors polecats, verifies work)
│   ├── Refinery (LLM agent - merge queue processor)
│   └── Polecats (LLM workers - ephemeral, do actual coding)
└── Swarm (multi-agent task decomposition via beads epics)
```

## How Coordination Works

### 1. No shared memory, no channels, no callbacks

Agents are fully independent OS processes (Claude Code in tmux sessions). They coordinate through:

- **Mail** (`internal/mail/`) — typed messages (task, notification, scavenge, reply) with priority, threads, queues, and channels. Backed by the `beads` database (Dolt SQL). Supports direct messages, queue-based (first-come-first-served), and broadcast channels.
- **Protocol messages** (`internal/protocol/`) — typed inter-agent messages like `MERGE_READY`, `MERGED`, `MERGE_FAILED`, `REWORK_REQUEST` between Witness and Refinery.
- **Beads** (external `bd` CLI) — a Dolt-backed issue/task tracking database. All state is stored as beads issues with metadata in labels. State is "discovered, not tracked" (ZFC principle).

### 2. The Daemon

`internal/daemon/` is the only always-running Go process. It's **not** an LLM — it's a watchdog that:
- Runs a heartbeat loop (3-minute fixed interval)
- Ensures Deacon, Witnesses, and Refineries are alive (restarts dead tmux sessions)
- Detects crashed polecats (work-on-hook but dead session) and auto-restarts them
- Checks for GUPP violations (agents not making progress)
- Manages Dolt server lifecycle
- Detects mass death events (multiple sessions dying in 30s window)

### 3. Polecats

`internal/polecat/` are ephemeral worker agents. Each gets:
- A **git worktree** branched from the repo's bare `.repo.git` (fast, shared objects)
- A **tmux session** (`gt-<rig>-<name>`)
- An **agent bead** in the database tracking state
- A **name** from a pool (recycled after cleanup)
- Work assigned via `hook_bead` (atomically set at spawn time)

They self-nuke when done (`gt done`). No idle pool — polecats are born with work and die after completing it.

### 4. Swarms

`internal/swarm/` decompose large tasks into a dependency graph of sub-tasks (beads epics), each assigned to a polecat. The swarm manager queries beads for ready/active/blocked fronts.

## Key Design Principles

- **ZFC (Zero File Cache)**: State is derived from tmux sessions, git, and beads — never from JSON state files. "Discover, don't track."
- **GUPP**: Agents must make progress or get poked/restarted
- **Tmux as process supervisor**: All agent liveness is checked via tmux session existence
- **Postel's Law in addressing**: Liberal normalization of agent addresses

## Key Packages

| Package | Purpose |
|---------|---------|
| `internal/daemon/` | Go watchdog process — heartbeat loop, session recovery, mass death detection |
| `internal/mayor/` | Town coordinator agent lifecycle |
| `internal/deacon/` | Persistent health patrol agent lifecycle |
| `internal/boot/` | Ephemeral triage agent (spawned fresh each daemon tick) |
| `internal/polecat/` | Ephemeral worker agent lifecycle, git worktree management, name pool |
| `internal/refinery/` | Merge queue processor agent, MR types and state machine |
| `internal/swarm/` | Multi-agent task decomposition, swarm lifecycle states |
| `internal/mail/` | Inter-agent messaging — mailbox, routing, direct/queue/channel delivery |
| `internal/protocol/` | Typed Witness-Refinery protocol messages (MERGE_READY, etc.) |
| `internal/session/` | Tmux session lifecycle, town-level session management |
| `internal/rig/` | Repository configuration, git worktree shared bare repo |
| `internal/dog/` | Deacon helper workers for cross-rig infrastructure |
| `internal/wisp/` | Beads directory utilities, ephemeral config |
| `internal/convoy/` | Convoy observer (grouped work tracking) |
| `internal/feed/` | Event feed curator |
| `internal/events/` | Event types and logging |
| `internal/state/` | Daemon state persistence |
| `internal/tmux/` | Tmux wrapper — session creation, theming, nudging, health checks |
| `internal/beads/` | Beads CLI wrapper (Dolt-backed issue tracking) |

---

## Comparison with Nous and OpenCode

### Similarities to Nous

| Aspect | Nous | Gastown |
|--------|------|---------|
| Language | Go | Go |
| CLI framework | Cobra | Cobra |
| TUI | Bubbletea | Bubbletea |
| LLM provider | Anthropic SDK | Claude Code CLI (wraps Anthropic) |
| Session storage | JSONL | JSONL + Dolt (beads) |
| Tool system | Internal tool registry | Tools via Claude Code's built-in tools + `gt` CLI commands |
| Agent loop | Runner with callbacks | Claude Code's internal loop; `gt` is the tool layer |

### Similarities to OpenCode

| Aspect | OpenCode | Gastown |
|--------|----------|---------|
| Language | TypeScript | Go |
| Agent types | Primary + subagent modes | Mayor, Deacon, Witness, Refinery, Polecat |
| Permission system | Per-agent rulesets | Per-role runtime settings |
| Session compaction | Yes | Delegated to Claude Code |
| Session management | SQLite-backed sessions | Beads (Dolt SQL) |
| Tool system | Zod-validated tools with categories | Tools via Claude Code + `gt`/`bd` CLI |

### Key Differences

#### 1. Agent Coordination Model

| | Nous | OpenCode | Gastown |
|---|------|----------|---------|
| Architecture | **Single-process, in-memory** | **Single-process, in-memory** | **Multi-process, filesystem/DB** |
| Agent communication | Callbacks + pubsub channels | Event bus (`bus` package) | **Mail system + beads DB** |
| Subagents | Same process, shared memory | Same process, different config | **Separate tmux sessions, separate Claude instances** |
| Process model | One LLM connection | One LLM connection | **N independent Claude Code processes** |

This is the fundamental difference. Nous and OpenCode are **single-process orchestrators** that manage one LLM conversation with tool calls. Gastown is a **multi-process agent swarm** where each agent is a full Claude Code instance in its own tmux session, coordinating through an external database.

#### 2. State Management

- **Nous**: In-memory message history + JSONL persistence. Runner holds all state.
- **OpenCode**: SQLite sessions, in-memory event bus, processor manages message state.
- **Gastown**: **No in-memory state.** Everything lives in beads (Dolt SQL) and git. State is "discovered" from tmux sessions, git branches, and database queries. This is the ZFC ("Zero File Cache") principle — if the process dies, no state is lost.

#### 3. LLM Integration

- **Nous**: Direct Anthropic SDK, streaming via `stream.Next()`, custom tool execution loop.
- **OpenCode**: Vercel AI SDK (`ai` package), multi-provider (Anthropic, OpenAI, etc.), streaming.
- **Gastown**: **Doesn't talk to LLMs directly.** Gastown is a coordination layer that launches Claude Code instances. The LLM interaction happens inside Claude Code. Gastown's Go code is purely orchestration, lifecycle management, and inter-agent messaging.

#### 4. Tool System

- **Nous**: 11 tools defined in Go, registered with the provider, executed in the runner loop.
- **OpenCode**: Tools defined as TypeScript objects with Zod schemas, executed by the session processor.
- **Gastown**: Tools are **`gt` CLI subcommands** that agents invoke via Claude Code's bash tool. `gt mail check`, `gt polecat spawn`, `gt mr create`, etc. The "tool system" is the CLI itself.

#### 5. Concurrency Model

- **Nous**: Single goroutine runner loop with callbacks. Subagents share the process.
- **OpenCode**: Single-threaded TypeScript with async/await. Event-driven.
- **Gastown**: **True OS-level parallelism.** Multiple polecats work simultaneously in separate tmux sessions on separate git worktrees. The daemon monitors them all. The swarm system can decompose an epic into N tasks and run them concurrently.

#### 6. Failure Handling

- **Nous/OpenCode**: If the process crashes, the session is lost (state can be recovered from persistence).
- **Gastown**: **Self-healing.** The daemon detects dead sessions via tmux and restarts them. Mass death detection alerts on correlated failures. Stuck agents get nudged, then killed and restarted. The Deacon auto-respawns via tmux hooks.

### Summary

**Nous** and **OpenCode** are **single-agent orchestrators** — one process, one LLM conversation, tools execute in-process. They're designed for interactive human-in-the-loop coding.

**Gastown** is a **multi-agent coordination platform** — many independent Claude Code instances running in tmux, coordinating through a shared Dolt database and a mail system, supervised by a Go daemon. It's designed for autonomous, parallel coding at scale where agents spawn workers, verify work, merge branches, and recover from failures — all without human intervention.

The closest analogy: Nous/OpenCode are like a single developer with tools. Gastown is like a software engineering team with a project manager (Mayor), QA (Witness), CI/CD (Refinery), and many junior devs (Polecats), all communicating via tickets and email.
