# OpenClaw (moltbot) Architectural Study

> Source: `~/code/deps/moltbot`
> Purpose: Extract patterns applicable to our coding orchestration layer (nous).

---

## 1. Overview

OpenClaw is a TypeScript (ESM) always-on agent orchestration system. It runs as a persistent gateway server that manages multiple agents, each with their own workspace, memory, skills, and session state.

| Aspect | Detail |
|--------|--------|
| Language | TypeScript (strict, ESM) |
| Runtime | Node.js >= 22.12.0 |
| Package manager | pnpm |
| Build | tsdown (rolldown/esbuild) |
| Config format | JSON5 (Zod-validated) |
| Transport | WebSocket (ws, port 18789) |
| Storage | SQLite + sqlite-vec extension |

---

## 2. Project Layout

```
src/
├── cli/           # Commander.js CLI wiring
├── commands/      # Individual CLI commands (gateway, agent, onboard, etc.)
├── gateway/       # WebSocket control-plane server
├── agents/        # Agent orchestration, Pi runtime integration, tool wiring
├── memory/        # Persistent memory: embeddings, BM25, hybrid search
├── sessions/      # JSONL transcript storage, write locks
├── channels/      # Multi-channel inbox (Telegram, Discord, WhatsApp, etc.)
├── plugins/       # Plugin registry, discovery, runtime
├── config/        # JSON5 config loading, Zod validation, migration
├── hooks/         # Event hook system
├── providers/     # Model provider integrations (Anthropic, OpenAI, etc.)
├── routing/       # Session key normalization, agent routing
├── types/         # Shared TypeScript types
├── entry.ts       # CLI bootstrap
└── index.ts       # Main exports
```

---

## 3. Persistent Memory System

This is the most relevant subsystem for our needs. OpenClaw implements a **hybrid vector + keyword search** memory system.

### 3.1 Storage

- **Backend**: SQLite with the `sqlite-vec` vector extension
- **Location**: `~/.openclaw/workspace-{agentId}/memory.db` (agent-scoped)
- **Tables**:
  - `chunks_vec` — vector embeddings
  - `chunks_fts` — BM25 full-text search index
  - `embedding_cache` — avoids re-embedding unchanged content

### 3.2 Memory Sources

1. **User memory files** — Markdown files in `~/.openclaw/workspace-{agentId}/memory/`
2. **Session transcripts** — Auto-indexed from JSONL session files

### 3.3 Indexing Pipeline

```
Markdown files → Chunking (configurable token size + overlap)
                    → Embedding (OpenAI / Gemini / Voyage / local llama.cpp)
                        → SQLite vec insert
                        → FTS insert
```

- Debounced file watchers (5s) trigger re-indexing
- Batch processing with progress callbacks
- Embedding provider fallback chain with retries (3 attempts, exponential backoff)

### 3.4 Search

- `searchKeyword(query)` — BM25 full-text search
- `searchVector(query)` — Semantic similarity via embeddings
- `mergeHybridResults()` — Combined ranking from both
- Results filtered by min score, scoped to session

### 3.5 Key Takeaway

The hybrid approach (vector + BM25) is pragmatic. SQLite keeps it portable and zero-ops. The embedding provider abstraction with fallback chains makes it resilient. **We should adopt this pattern.**

---

## 4. Agent Orchestration

### 4.1 Agent Lifecycle

1. Agents defined in config: `agents.list[].id` (default: `"main"`)
2. Each agent gets an isolated workspace: `~/.openclaw/workspace-{agentId}/`
3. Session keys encode agent routing: `agent:{agentId}:{channelKey}`
4. Gateway dispatches inbound messages to the correct agent

### 4.2 Pi Agent Runtime

OpenClaw uses `@mariozechner/pi-*` packages (Pi agent runtime) as its LLM execution engine:

- **Streaming**: Block-based streaming with coalescing for UI output
- **Tool execution**: Tools registered per-agent with policy enforcement
- **Reasoning modes**: off / on / stream (extended thinking)
- **State tracking**: Per-session streaming state (assistant texts, tool metas, block buffers)

### 4.3 Multi-Agent

- Single gateway process hosts multiple isolated agents
- Subagent spawning for complex workflows via `subagent-registry.ts`
- Tool policy inheritance from parent to subagent

### 4.4 Key Takeaway

The agent-per-workspace isolation is clean. Session keys as the routing primitive is elegant. **We should adopt the session-key routing pattern** but use our own LLM execution layer rather than Pi.

---

## 5. Skills System

### 5.1 Skill Categories

| Type | Source | Location |
|------|--------|----------|
| Bundled | Ships with OpenClaw | `/dist/skills/` |
| Managed | Installed from npm/git | `node_modules/` |
| Workspace | Local YAML/JS files | `~/.openclaw/workspace-{agentId}/skills/` |

### 5.2 Skill Definition

```typescript
type SkillEntry = {
  skill: Skill;
  frontmatter: ParsedSkillFrontmatter;
  metadata?: {
    always?: boolean;        // Always include in context
    skillKey?: string;       // Config key
    emoji?: string;
    os?: string[];           // Platform filter
    requires?: {
      bins?: string[];       // Required binaries
      env?: string[];        // Required env vars
      config?: string[];     // Required config paths
    };
    install?: SkillInstallSpec[];
  };
};
```

### 5.3 Skill Eligibility

Before a skill is made available to an agent, OpenClaw checks:
1. OS compatibility (`os` field)
2. Required binaries exist on PATH
3. Required environment variables are set
4. Required config paths are truthy
5. Remote bin availability (SSH/container environments)

### 5.4 Skill Invocation

- Registered as tools in the agent runtime
- Two invocation modes: model-invocable (agent calls it) and user-invocable (human triggers via `/command`)
- Invocation policies control who can trigger what

### 5.5 Key Takeaway

The three-tier skill system (bundled/managed/workspace) with eligibility checks is well-designed. The YAML frontmatter approach for skill metadata is lightweight. **We should adopt the tiered skill system with eligibility gates.**

---

## 6. Gateway & Communication

### 6.1 Architecture

```
                    ┌─────────────┐
  Channels ───────▶ │   Gateway   │ ◀────── CLI / UI clients
  (Telegram,       │  (WebSocket) │
   Discord, etc.)  └──────┬──────┘
                          │
                    ┌─────▼──────┐
                    │   Agents   │
                    │ (Pi runtime)│
                    └─────┬──────┘
                          │
                    ┌─────▼──────┐
                    │  Memory /  │
                    │  Sessions  │
                    └────────────┘
```

### 6.2 WebSocket Protocol

- **RPC**: `{ method, payload?, id? }` → `{ result?, error?, id? }`
- **Broadcast**: `{ method, payload }` (no id, one-way)
- Key methods: `chat.send`, `agent.run`, `config.patch`, `sessions.list`
- Key events: `agent.event`, `chat.delta`, `health`, `presence`

### 6.3 Key Takeaway

The gateway-as-hub pattern is solid for always-on operation. WebSocket for both RPC and streaming is pragmatic. **We should adopt the gateway pattern** but may simplify the channel layer (we're focused on coding, not multi-channel chat).

---

## 7. Configuration

### 7.1 Config Stack

```
~/.openclaw/config.json5        # Primary config (JSON5, supports comments)
    ↓ validated by
Zod schema                      # Type-safe validation
    ↓ overridden by
Environment variables            # Runtime overrides
    ↓ migrated by
migrateLegacyConfig()           # Auto-upgrade old formats
```

### 7.2 Key Config Sections

- `gateway` — Bind address, auth, TLS
- `agents` — Agent list with models, skills, memory config
- `models` — Provider auth, fallback chains
- `tools` — Tool policies, exec approval
- `plugins` — Enable/disable
- `skills` — Bundled skill allowlist
- `hooks` — Event listeners

### 7.3 Key Takeaway

JSON5 + Zod is a good combo (comments in config + type safety). Config migration for schema evolution is important. **Adopt JSON5 + Zod for config.**

---

## 8. Session Management

- **Format**: JSONL transcript files per session
- **Location**: `~/.openclaw/sessions/{agentId}/`
- **Concurrency**: Write locks prevent race conditions
- **Pruning**: Configurable retention
- **Replay**: Delta-based partial replay for memory efficiency

### Key Takeaway

JSONL is good for append-only transcripts. Write locks are necessary for concurrent agent access. **Adopt JSONL sessions with write locks.**

---

## 9. Always-On Infrastructure

### 9.1 Daemon Installation

- **macOS**: launchd user agent (plist)
- **Linux**: systemd user service
- **Docker/Fly.io**: Container with persistent volume

### 9.2 Process Management

- SIGUSR1 triggers graceful restart
- Unhandled rejection handler prevents crashes
- Structured logging for observability

### 9.3 Health Monitoring

- Diagnostic heartbeat for long-running health
- Health snapshots broadcast via gateway
- Channel status polling

### Key Takeaway

Daemon installation is table stakes for always-on. Graceful restart via signals is important. **Adopt systemd/launchd service installation and signal-based lifecycle.**

---

## 10. Notable Design Patterns

### 10.1 Session Key Routing
All messages are routed by a composite key: `agent:{agentId}:{mainKey}`. This cleanly separates agent identity from conversation identity.

### 10.2 Tool Policy Layering
Policies stack: global defaults → agent-level → channel-level → group-level. This allows fine-grained control without complexity at each layer.

### 10.3 Embedding Provider Abstraction
A unified interface wraps OpenAI, Gemini, Voyage, and local models behind the same `embed(text) → vector` contract. Fallback chains add resilience.

### 10.4 Plugin Architecture
Channels, providers, and tools are all plugin-shaped. Registration happens at startup (no hot-reload). This keeps the runtime simple while allowing extensibility.

### 10.5 Stream Block Coalescing
The Pi runtime emits fine-grained streaming events. A coalescing layer (`pi-embedded-block-chunker.ts`) batches these into UI-friendly blocks before sending to clients.

---

## 11. What to Adopt for Nous

| Pattern | Priority | Rationale |
|---------|----------|-----------|
| Hybrid memory (vector + BM25 + SQLite) | **High** | Portable, zero-ops, good recall |
| Gateway server (WebSocket) | **High** | Always-on hub for agents |
| Agent workspace isolation | **High** | Clean separation of concerns |
| Session key routing | **High** | Scalable agent dispatch |
| JSONL session transcripts | **High** | Durable, appendable, replayable |
| Telegram | **High** | Telegram integration | 
| JSON5 + Zod config | **Medium** | Developer-friendly config with safety |
| Skills (bundled/managed/workspace) | **Medium** | Extensibility without complexity |
| Daemon installation (systemd/launchd) | **Medium** | Always-on requirement |
| WebUI | **Medium** |  Web UI Terminal over Tailscale | 
| Tool policy layering | **Low** | May be over-engineered for coding focus |
| Multi-channel inbox | **Low** | Not needed—we're coding-focused |
| Plugin system | **Low** | Start simple, add later if needed |


## 12. What to Skip or Simplify

- **Pi agent runtime**: We'll use our own LLM execution layer.
- **Canvas/browser subsystems**: Not relevant for coding orchestration.
- **Human delay simulation**: Not relevant.
- **Multi-platform mobile support (iOS/Android nodes)**: Not relevant.
- Plugins: Not going for wide adoption, going for self use, we will modify and maintain source code ourselves. 

---

## 13. Recommended Nous Architecture (Preview)

Based on this study, here's the high-level shape:

```
nous/
├── src/
│   ├── gateway/        # WebSocket server (always-on hub)
│   ├── agents/         # Agent definitions, lifecycle, dispatch
│   ├── memory/         # SQLite + vec hybrid memory
│   ├── sessions/       # JSONL transcripts, write locks
│   ├── skills/         # Tiered skill system
│   ├── projects/       # Project context, workspace management
│   ├── config/         # JSON5 + Zod config
│   ├── providers/      # LLM provider abstraction
│   ├── cli/            # CLI commands
│   └── types/          # Shared types
├── skills/             # Bundled skill definitions
└── package.json
```

This will be refined once we also study opencode's architecture.
