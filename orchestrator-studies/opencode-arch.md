# OpenCode Architectural Study

> Source: `~/code/deps/opencode`
> Purpose: Extract orchestration patterns applicable to our coding orchestration layer (nous).

---

## 1. Overview

OpenCode is a TypeScript monorepo providing an AI coding agent with TUI, Web, and Desktop interfaces. It focuses on **session-based coding workflows** with multi-agent orchestration, fine-grained permissions, and an extensible tool/plugin system.

| Aspect | Detail |
|--------|--------|
| Language | TypeScript (strict) |
| Runtime | Bun (primary), Node.js compatible |
| Monorepo | Bun workspaces + Turborepo |
| UI | Solid.js (TUI via OpenTUI, Web via Vite, Desktop via Tauri) |
| Server | Hono (HTTP + WebSocket + SSE) |
| Config | JSONC (JSON with comments), Zod-validated |
| LLM layer | Vercel AI SDK (`@ai-sdk/*`) |

---

## 2. Monorepo Layout

```
packages/
├── opencode/      # Core engine: CLI, agents, tools, sessions, providers
├── app/           # Web UI (Solid.js + Vite)
├── desktop/       # Desktop wrapper (Tauri)
├── ui/            # Shared UI components (Solid.js + Kobalte + Tailwind)
├── sdk/js/        # JS SDK (client + server exports)
├── plugin/        # Plugin framework (hooks, tool definitions)
├── util/          # Shared utilities (Zod schemas, errors)
├── script/        # Build scripts
├── console/       # SaaS console (Drizzle ORM, PlanetScale)
│   ├── core/      # Database/API
│   ├── app/       # Console UI (Solid Start)
│   ├── mail/      # Email
│   ├── resource/  # Resource management
│   └── function/  # Serverless functions
├── enterprise/    # Enterprise features
├── slack/         # Slack integration
├── extensions/    # Editor extensions
├── docs/          # Documentation
├── containers/    # Container configs
└── identity/      # Auth
```

The core engine lives in `packages/opencode/`. Everything else is delivery surface.

---

## 3. Agent System

### 3.1 Built-in Agents

| Agent | Mode | Purpose |
|-------|------|---------|
| `build` | primary | Default orchestrator — full coding capability |
| `plan` | primary | Research/planning mode — edit tools disabled |
| `general` | subagent | Multi-step parallel task execution |
| `explore` | subagent | Fast read-only codebase exploration |

### 3.2 Agent Schema

```typescript
{
  name: string
  mode: "primary" | "subagent" | "all"
  permission: Ruleset           // Tool-level allow/deny/ask rules
  model?: { modelID, providerID }
  prompt?: string               // Custom system prompt
  steps?: number                // Max turns for subagents
  options: Record<string, any>
  // display
  description?: string
  color?: string
  hidden?: boolean
}
```

### 3.3 Agent Lifecycle

1. Agent selected by user choice or internal routing
2. Permission ruleset merged: defaults + user config + agent-specific
3. Tool registry filtered by agent permissions
4. LLM invoked with agent-scoped tools and system prompt
5. Agent can spawn subagents (e.g., `build` spawns `explore` for search)

### 3.4 Key Takeaway

The **primary vs. subagent** distinction is clean. Primary agents run the top-level loop; subagents are scoped tasks with limited tools and step counts. Permissions are layered per-agent. **We should adopt this two-tier agent model with permission rulesets.**

---

## 4. Session & Message Architecture

### 4.1 Session

```typescript
{
  id: string
  slug: string                  // Human-readable
  projectID: string
  directory: string             // Working directory
  parentID?: string             // Fork parent
  title: string
  version: string
  time: { created, updated, compacting?, archived? }
  permission?: Ruleset          // Session-level overrides
  summary?: { additions, deletions, files, diffs }
  revert?: { messageID, snapshot, diff }
}
```

Sessions are project-scoped. They can be forked (branching conversation history).

### 4.2 Message Parts

Messages are decomposed into typed parts:

| Part | Purpose |
|------|---------|
| `TextPart` | User/assistant text |
| `ReasoningPart` | Extended thinking output |
| `ToolPart` | Tool call with state/input/output |
| `SnapshotPart` | File state capture |
| `PatchPart` | Git patch with hash |
| `FilePart` | Attachments (code snippets) |

### 4.3 Storage Model

Hierarchical path-based storage:
```
["session", projectID, sessionID]     → Session metadata
["message", sessionID, messageID]     → Message info (role, time, parent)
["part", messageID, partID]           → Individual parts
["session_diff", sessionID]           → File diffs
```

### 4.4 Session Events

Event bus publishes: `session.created`, `session.updated`, `session.deleted`, `session.diff`, `session.error`

### 4.5 Key Takeaway

The **part-based message model** is powerful — it separates text, tool calls, reasoning, and file state into independently addressable units. The hierarchical storage path pattern is elegant. **We should adopt the part-based message model and hierarchical storage.**

---

## 5. Tool System

### 5.1 Tool Interface

```typescript
Tool.Info<Parameters, Metadata> = {
  id: string
  init(ctx?): Promise<{
    description: string
    parameters: Parameters          // Zod schema
    execute(args, ctx): Promise<{
      title: string
      metadata: Metadata
      output: string
      attachments?: FilePart[]
    }>
  }>
}
```

### 5.2 Tool Context

```typescript
Tool.Context = {
  sessionID: string
  messageID: string
  agent: string
  abort: AbortSignal
  messages: MessageV2.WithParts[]
  metadata(input): void              // Update display metadata
  ask(input): Promise<void>          // Request permission
}
```

### 5.3 Built-in Tools (19+)

| Tool | Purpose |
|------|---------|
| `bash` | Shell execution with PTY |
| `read` | Read file contents |
| `write` | Create/write files |
| `edit` | Modify files (line-based or hunk-based) |
| `multiedit` | Edit multiple files |
| `apply_patch` | Apply unified diffs |
| `glob` | Find files by pattern |
| `grep` | Search file contents |
| `ls` | List directories |
| `webfetch` | Fetch web content |
| `websearch` | Web search |
| `codesearch` | Code search integration |
| `task` | Task management (create/list/get/update) |
| `skill` | Execute skills |
| `todo` | Todo management |
| `question` | Ask user questions |
| `plan` | Plan mode entry/exit |
| `lsp` | Language server queries |
| `batch` | Batch multiple operations |

### 5.4 Permission System

Pattern-based, per-tool:
```typescript
permission: {
  bash: "allow" | "deny" | "ask"
  read: {
    "*": "allow",
    "*.env": "ask"
  }
  edit: "deny"
  external_directory: {
    "/allowed/path/*": "allow"
  }
}
```

Rules merge: global defaults → agent-level → session-level.

### 5.5 Truncation

Output automatically truncated by configurable MAX_LINES / MAX_BYTES limits. Metadata flag `truncated` set when triggered.

### 5.6 Key Takeaway

The tool interface is clean — `init()` for one-time setup, `execute()` for invocation, `ctx.ask()` for permission escalation. The pattern-based permission system is well-designed. **We should adopt this tool interface and permission model.**

---

## 6. Skills

Skills are markdown files with frontmatter, discovered from:
- `.opencode/skills/`
- `.claude/skills/`
- `.agents/skills/`

Pattern: `**/SKILL.md`

They augment agent system prompts with domain-specific instructions. Lightweight — no code, just context.

### Key Takeaway

Skills-as-markdown is the simplest possible approach. Good for user-defined instructions. **Adopt as the base layer**, but we'll also want executable skills (from openclaw's model).

---

## 7. Provider Abstraction

### 7.1 Unified via Vercel AI SDK

OpenCode uses `@ai-sdk/*` packages for **20+ providers**:

Anthropic, OpenAI, Google, Vertex AI, AWS Bedrock, Azure, xAI, Mistral, Groq, DeepInfra, Cerebras, Cohere, Together AI, Perplexity, OpenRouter, GitLab, GitHub Copilot, and more.

### 7.2 Model Registry

```typescript
Provider.Model = {
  id: string
  providerID: string
  name: string
  contextWindow: number
  inputCost: number       // per 1M tokens
  outputCost: number
  cache?: { input, write }
  capabilities?: string[]
}
```

Models loaded from `models.dev` registry or cached locally.

### 7.3 Provider Transform

Normalizes tool calls across providers (different APIs, streaming behaviors).

### 7.4 Key Takeaway

The Vercel AI SDK abstraction is production-proven. The model registry with cost tracking is useful. **We should use `@ai-sdk/*` for provider abstraction** rather than building our own.

---

## 8. Execution Pipeline

The core orchestration flow:

```
User Input
    ↓
Message Creation (store user message parts)
    ↓
Agent Selection (mode/config determines agent)
    ↓
Tool Discovery (build registry filtered by agent permissions)
    ↓
System Prompt Construction (base + skills + context)
    ↓
LLM.stream() (Vercel AI SDK, streaming)
    ↓
SessionProcessor (extract reasoning, text, tool calls)
    ↓
Tool Execution (with permission checks via ctx.ask())
    ↓
Message Update (store assistant parts)
    ↓
Compaction (optional: compress long history)
    ↓
Revert Tracking (snapshot for undo)
```

**SessionProcessor** handles:
- Stream parsing into typed parts
- Tool failure retry logic
- Doom loop detection (excessive retries)
- Compaction triggering

### Key Takeaway

The pipeline is well-structured. Compaction and doom loop detection are important for long-running sessions. **Adopt this pipeline structure.**

---

## 9. Event Bus

Instance-scoped pub/sub:

```typescript
Bus.publish(eventDef, properties)     // Publish typed event
Bus.subscribe(eventDef, callback)     // Subscribe, returns unsubscribe fn
```

Events defined with `BusEvent.define()` + Zod schemas. Type-safe across the system.

Used for: session changes, message arrivals, permission requests, tool execution, UI updates.

### Key Takeaway

Typed event bus is essential for decoupling. Zod-validated events prevent runtime surprises. **Adopt this pattern.**

---

## 10. Instance Context

```typescript
Instance.provide({
  directory: string,
  fn: () => R
}): Promise<R>

Instance.state(init, dispose): () => S
```

Per-directory isolated state. All subsystems (sessions, storage, config) scoped to the instance. Automatic cleanup on disposal.

### Key Takeaway

This is the "always-on" enabler — state is scoped to working directory, not process. **Adopt instance context scoping.**

---

## 11. LSP Integration

Supported servers:
- TypeScript/JavaScript (`typescript-language-server`)
- Deno (`deno lsp`)

Provides: hover info, go-to-definition, auto-complete, diagnostics.

LSP servers spawned per root directory, reused across sessions.

### Key Takeaway

LSP gives agents code intelligence for free. **Adopt LSP integration** — start with TypeScript, extend later.

---

## 12. Server Architecture

**Framework**: Hono

**Route groups:**

| Route | Purpose |
|-------|---------|
| `/session` | Session CRUD, messages |
| `/project` | Project info |
| `/provider` | Provider/model listing |
| `/config` | Configuration |
| `/permission` | Permission requests |
| `/file` | File operations |
| `/mcp` | MCP integration |
| `/pty` | Pseudo-terminal |
| `/question` | User questions |

Features: OpenAPI spec generation, Zod validators, WebSocket + SSE streaming, optional basic auth.

### Key Takeaway

Hono is lightweight and fast. The route structure maps cleanly to domain concerns. **Adopt Hono for the HTTP/API layer.**

---

## 13. Plugin System

```typescript
Hooks = {
  auth?: { ... }           // Custom auth methods
  tool?: { [key]: Tool }   // Custom tools
  message?: Transform      // Message transforms
  system?: Transform       // System prompt transforms
  permission?: Handler     // Permission interceptors
  llm?: { headers, params }  // LLM parameter injection
}
```

Plugins loaded at startup from `.opencode/plugins/` or config.

### Key Takeaway

Hook-based plugins are simple and powerful. **Adopt the hook pattern** for extensibility.

---

## 14. Protocol Support

### MCP (Model Context Protocol)
Optional integration for additional tools, resources, prompts, sampling.

### ACP (Agent Context Protocol)
Agent coordination for sub-agent spawning, parent-child session relationships, task delegation.

### Key Takeaway

MCP support is table stakes. ACP is forward-looking. **Support MCP from the start; plan for ACP.**

---

## 15. What to Adopt for Nous

| Pattern | Priority | Rationale |
|---------|----------|-----------|
| Primary + subagent model | **High** | Clean orchestration hierarchy |
| Part-based message model | **High** | Granular message decomposition |
| Tool interface (init/execute/ask) | **High** | Clean, permission-aware tool contract |
| Session-based workflows | **High** | Natural unit of coding work |
| Execution pipeline (stream → process → store) | **High** | Well-structured orchestration |
| Vercel AI SDK for providers | **High** | 20+ providers, production-proven |
| Typed event bus | **High** | Decoupled component communication |
| Instance context scoping | **High** | Per-directory state isolation |
| Hierarchical storage paths | **High** | Clean persistence model |
| Pattern-based permissions | **Medium** | Fine-grained security |
| Hono server | **Medium** | Lightweight API layer |
| LSP integration | **Medium** | Code intelligence for agents |
| Skills as markdown | **Medium** | Simple user-defined context |
| Session forking | **Medium** | Branch exploration |
| Compaction + doom loop detection | **Medium** | Long session resilience |
| MCP support | **Medium** | Ecosystem interop |
| Plugin hooks | **Low** | Start simple, add later |
| ACP support | **Low** | Future protocol |

## 16. What to Skip or Simplify

- **TUI framework (OpenTUI)**: We'll likely use a simpler interface or defer to existing CLIs.
- **Web/Desktop apps**: Not needed initially — focus on the engine.
- **SaaS console**: Enterprise hosting layer — irrelevant.
- **Tauri desktop**: Not needed.
- **GitHub PR integration**: Nice-to-have later.
- **Shared UI component library**: Only if we build a frontend.

---

## 17. OpenCode vs. OpenClaw — Complementary Strengths

| Concern | OpenClaw | OpenCode | Nous Should... |
|---------|----------|----------|----------------|
| Always-on | Gateway daemon (systemd/launchd) | Instance-scoped (per-invocation) | **Combine**: daemon + instance context |
| Memory | Hybrid vector+BM25 | No persistent memory | **Adopt OpenClaw's** memory system |
| Agent model | Multi-agent via session keys | Primary + subagent hierarchy | **Adopt OpenCode's** hierarchy + OpenClaw's routing |
| Tools | Pi runtime tools | Clean init/execute/ask interface | **Adopt OpenCode's** tool interface |
| Skills | Tiered (bundled/managed/workspace) with eligibility | Markdown-only (context injection) | **Combine**: markdown context + executable skills |
| Provider | Custom with fallback chains | Vercel AI SDK (20+ providers) | **Adopt OpenCode's** AI SDK approach |
| Sessions | JSONL transcripts | Part-based hierarchical storage | **Adopt OpenCode's** part model + OpenClaw's JSONL durability |
| Config | JSON5 + Zod | JSONC + Zod | **Either works** — both Zod-validated |
| Events | WebSocket broadcast | Typed event bus | **Adopt OpenCode's** typed bus + OpenClaw's WebSocket transport |
| Permissions | Tool policies per channel/group | Pattern-based per-tool rulesets | **Adopt OpenCode's** pattern-based system |
| LSP | None | TypeScript, Deno | **Adopt OpenCode's** LSP integration |
| Protocols | None | MCP + ACP | **Adopt**: MCP support |

This comparison directly informs the nous architecture design.

