# Phase 2 Implementation Plan: Interactive Mode + Subagents

## Context

Phase 1 delivered the minimum end-to-end loop: single CLI prompt → Anthropic streaming → tool execution → JSONL persistence. Phase 2 makes it interactive and composable: a TUI for multi-turn conversation, cancellable runner, subagent spawning via a `armory` tool, the `fetch` tool for web content, and a skills system for on-demand context loading. The always-on gateway, Telegram, memory/RAG, workflows, and cron remain Phase 3+.

**End-state**: `nous` launches a TUI with streaming chat, tool approval prompts, session switching, and the ability to spawn subagent tasks. `nous run` continues to work for non-interactive use.

---

## Step 1: Runner Cancellation

The runner currently has no way to stop mid-execution. Add a cancellable context so ctrl+c in the REPL stops the current run without killing the process, and parent sessions can stop subagents.

**Files:**
```
internal/agent/runner.go           # Modify: add cancel context, Stop() method
```

Changes to `Runner`:
```go
type Runner struct {
    // ... existing fields ...
    cancel context.CancelFunc  // cancels the current Run
}

// Run wraps ctx with a cancellable child context.
func (r *Runner) Run(ctx context.Context, sess *session.Session, prompt string) error {
    ctx, r.cancel = context.WithCancel(ctx)
    defer func() { r.cancel = nil }()
    // ... existing loop, ctx propagates to provider.Stream and tool.Execute ...
}

// Stop cancels the in-flight Run.
func (r *Runner) Stop() {
    if r.cancel != nil {
        r.cancel()
    }
}
```

The provider stream and tool execution already take `ctx` — cancellation propagates naturally. The loop checks `ctx.Err()` after each step and returns early.

**Verify:** Unit test: start a Run in a goroutine, call Stop(), confirm it returns promptly without error (or with `context.Canceled`).

---

## Step 2: Interactive REPL Command

Add `nous chat` (or make bare `nous` launch it) — a loop that reads prompts from stdin, runs them through the runner, and accepts the next prompt when the run finishes.

**Files:**
```
internal/cmd/chat.go               # New: interactive REPL command
internal/cmd/root.go               # Modify: make chat the default command
```

`chat` command:
1. Load config, auth, create provider (same wiring as `run.go`)
2. Create or resume session
3. Loop:
   - Print prompt indicator (`> `)
   - Read input line(s) from stdin (support multi-line with `\` continuation or blank-line termination)
   - If input is a command (`/new`, `/sessions`, `/quit`, `/compact`), handle it
   - Otherwise, call `runner.Run(ctx, sess, input)`
   - On ctrl+c during a run: call `runner.Stop()`, print interruption notice, continue loop
   - On ctrl+c at prompt: exit cleanly

Built-in REPL commands:
- `/new` — create new session
- `/sessions` — list recent sessions
- `/session <id>` — switch to session
- `/context` — display current session context (one line per message, long content truncated with `...(+N chars)`)
- `/compact` — force compaction
- `/quit` — exit

`/context` output format — shows what the LLM actually sees:
```
[user] write hello world to test.go
[assistant] I'll create that file for you.
[assistant/tool_call] write {"file_path":"/tmp/test.go"...(+48 chars)
[user/tool_result] File written successfully.
[assistant] Done. I created test.go with a hel...(+120 chars)
```
Each line: `[role/part_type]` + first 60 chars of content + `...(+N chars)` if truncated. Summary messages are tagged `[summary]`.

This is a minimal readline-style REPL, not the full TUI (Step 7). It provides multi-turn conversation before the TUI exists.

**Verify:** Manual test: launch `nous`, type prompts, verify multi-turn conversation works with session continuity. Ctrl+c during a run stops it without exiting.

---

## Step 3: Fetch Tool

HTTP fetch that converts HTML to markdown for LLM consumption. Required by the `researcher` subagent.

**Files:**
```
internal/agent/tools/fetch.go               # New: fetch tool
internal/agent/tools/descriptions/fetch.md  # New: tool description
internal/agent/tools/tool.go                # Modify: add to AllTools()
```

Fetch tool:
- Input: `{ "url": string, "prompt": string }`
- Fetches URL via `net/http` with a sensible user-agent and timeout (30s)
- Converts HTML to markdown using `html-to-markdown` library (or simple tag stripping for MVP)
- Truncates content to ~100K chars
- If `prompt` is provided, returns the content with the prompt prepended so the agent can extract specific info
- Returns markdown content as tool result

**New dependency:** `go get github.com/JohannesKaufmann/html-to-markdown/v2` (or simpler alternative)

**Verify:** Unit test with a local HTTP test server returning HTML, verify markdown output.

---

## Step 4: Subagent Execution — Task Tool

The `armory` tool lets the primary agent spawn subagents. Each subagent gets its own session, runs with a restricted tool set, and returns a summary result.

**Files:**
```
internal/agent/tools/armory.go                # New: armory tool
internal/agent/tools/descriptions/armory.md   # New: tool description
internal/agent/tools/tool.go                # Modify: add to AllTools(), extend ToolContext
internal/agent/agent.go                     # Modify: add explorer, researcher agents
internal/agent/runner.go                    # Modify: accept agent override, tool filter
internal/agent/prompt.go                    # Modify: add explorer/researcher prompts
internal/agent/templates/explorer.md        # New: explorer system prompt
internal/agent/templates/researcher.md      # New: researcher system prompt
```

### ToolContext Extension

The armory tool needs access to the runner's dependencies to spawn subagents:

```go
type ToolContext struct {
    SessionID  string
    WorkDir    string
    Depth      int // current spawn depth (0 = primary agent)
    SpawnAgent func(ctx context.Context, agentName, prompt, taskID string) (string, error)
}
```

`SpawnAgent` is a closure wired in the runner that:
1. Checks `Depth < MaxDepth` (default 2) — returns error if exceeded
2. If `taskID` is provided, resumes the existing child session; otherwise creates a new one
3. Looks up the agent config by name
4. Creates a new child session (parent_id set to current session)
5. Builds a tool list filtered by the agent's allowed tools
6. Creates a new Runner with the filtered tools, `Depth` incremented by 1
7. Calls `runner.Run(ctx, childSess, prompt)`
8. Returns the child session ID + final assistant text response as the task result

### Task Tool

```go
// Input: { "agent": string, "prompt": string, "task_id": string (optional) }
// Output: task_id + the subagent's final text response
```

- `agent` defaults to `"explorer"` if not specified
- `task_id` is optional — when provided, resumes the existing subagent session instead of creating a new one. This lets the parent ask follow-up questions to a subagent that already has context.
- The tool blocks until the subagent run completes
- Output format includes the session ID for resumption:
  ```
  task_id: {child_session_id}

  <task_result>
  {final text response}
  </task_result>
  ```
- Subagent output is truncated if too long
- If the subagent errors or hits MaxSteps, return the error as an error result

### New Agents

```go
"explorer": {
    Name:        "explorer",
    Description: "Fast read-only codebase search",
    Mode:        AgentModeSubagent,
    MaxSteps:    25,
    Tools:       []string{"glob", "grep", "read", "ls"},
},
"researcher": {
    Name:        "researcher",
    Description: "Web research and document analysis",
    Mode:        AgentModeSubagent,
    MaxSteps:    15,
    Tools:       []string{"fetch", "read", "grep", "glob"},
},
```

Add a `Tools []string` field to `AgentInfo` — when non-nil, the runner filters the tool list to only these tools. Subagents can spawn further subagents if `armory` is in their tool list — depth is tracked and capped by `MaxDepth`.

### Runner Changes

```go
const DefaultMaxDepth = 2 // primary (0) + subagents (1)

func NewRunner(p provider.Provider, cfg *config.Config, sessions *session.Service,
    toolList []tools.Tool, agent AgentInfo, depth int, log *slog.Logger) *Runner
```

The runner now takes an `AgentInfo` and `depth` at construction. Primary agent starts at depth 0. Each `SpawnAgent` call increments depth. If `depth >= MaxDepth`, the armory tool returns an error instead of spawning.

**Verify:** Integration test: prompt that says "search for X in the codebase" triggers a armory tool call with the explorer agent, which uses glob/grep/read and returns results.

---

## Step 5: Skills System

Skills are contextual knowledge documents loaded on demand via the `skill` tool.

**Files:**
```
internal/skill/skill.go                     # New: Skill struct, discovery, loading
internal/skill/discovery.go                 # New: scan directories for SKILL.md files
internal/agent/tools/skill.go               # New: skill tool
internal/agent/tools/descriptions/skill.md  # New: tool description
internal/agent/tools/tool.go                # Modify: add to AllTools()
internal/agent/prompt.go                    # Modify: inject available skill list into system prompt
```

### Skill Model

```go
type Skill struct {
    Name        string   // from frontmatter
    Description string   // from frontmatter
    Content     string   // full markdown body
    Path        string   // source file path
    Files       []string // companion files in same directory
}
```

### Discovery

Scan three locations in precedence order (highest first):
1. `{workdir}/.nous/skills/**/SKILL.md` — project-scoped
2. `~/.nous/skills/**/SKILL.md` — user-scoped
3. `skills/**/SKILL.md` in nous repo — bundled

Parse frontmatter (`name`, `description`) from each SKILL.md. If duplicate names, highest-precedence wins.

### Skill Tool

```go
// Input: { "name": string }
// Output: skill markdown content
```

Returns the full markdown body. The agent sees available skills (name + description) listed in the system prompt and decides when to load one.

### System Prompt Injection

Append to system prompt:
```
<available_skills>
- backtest-review: Review a backtest result and suggest improvements
- strategy-template: Template for new trading strategy development
</available_skills>
```

### ToolContext Extension

```go
type ToolContext struct {
    // ... existing fields ...
    Skills []skill.Skill  // available skills for the skill tool
}
```

**Verify:** Create a test SKILL.md in a temp dir, verify discovery finds it, skill tool returns content, system prompt lists it.

---

## Step 6: Permission System

Replace Phase 1's auto-approve with an interactive approval flow. In REPL/TUI mode, prompt the user before executing tools. In `nous run` mode, auto-approve (current behavior).

**Files:**
```
internal/permission/permission.go           # New: permission service
internal/agent/runner.go                    # Modify: check permissions before tool execution
internal/agent/tools/tool.go                # Modify: add risk level to Tool interface
```

### Permission Model

```go
type Decision int
const (
    Allow Decision = iota
    Deny
    Ask  // prompt user
)

type Service struct {
    autoApprove bool
    askFunc     func(toolName string, input json.RawMessage) (bool, error) // UI callback
    rules       []Rule
}

type Rule struct {
    Tool    string // tool name or "*"
    Action  Decision
}
```

### Default Rules

- `read`, `glob`, `grep`, `ls` → Allow (read-only, safe)
- `bash`, `write`, `edit` → Ask (modifies filesystem)
- `fetch` → Allow (read-only, network)
- `armory` → Allow (spawns subagent which has its own permissions)
- `skill` → Allow (read-only)

### Runner Integration

Before executing a tool call, the runner calls `permission.Check(toolName, input)`. If the decision is `Ask`, it calls the `askFunc` callback which blocks until the user responds. In REPL mode, this prints a prompt to stderr and reads y/n. In `nous run` mode, `askFunc` is nil and `autoApprove` is true.

### Session-Level Memory

Once a user approves a tool+pattern combination, remember it for the session so they don't get asked again for the same operation.

**Verify:** Unit test: verify read tools auto-approve, write tools trigger ask. Integration test in REPL: verify prompt appears and blocks.

---

## Step 7: TUI (Bubbletea)

Full terminal UI replacing the simple REPL from Step 2.

**Files:**
```
internal/ui/app.go                          # New: main Bubbletea model, Init/Update/View
internal/ui/chat.go                         # New: chat message list component
internal/ui/input.go                        # New: multi-line text input component
internal/ui/sidebar.go                      # New: session list sidebar
internal/ui/status.go                       # New: status bar (model, session, tokens)
internal/ui/permission.go                   # New: tool approval prompt component
internal/ui/theme.go                        # New: Lipgloss styles
internal/cmd/chat.go                        # Modify: launch TUI instead of REPL
```

**New dependencies:** `go get github.com/charmbracelet/bubbletea/v2 github.com/charmbracelet/lipgloss/v2`

### Layout

```
┌─────────────────────────────────────────────────┐
│ Sessions │ Chat                                  │
│          │                                       │
│ > coding │ User: write hello world to test.go    │
│   debug  │                                       │
│   research│ Assistant: I'll create that file.     │
│          │ [write] test.go ✓                      │
│          │                                       │
│          │ Done. Created test.go with hello world │
│          │                                       │
│          ├───────────────────────────────────────│
│          │ > type your message...                 │
├──────────┴───────────────────────────────────────│
│ claude-opus-4-6 | session: abc123 | 12K tokens   │
└─────────────────────────────────────────────────┘
```

### Components

**App model** — top-level Bubbletea model. Owns the runner, session service, and child components. Routes key events and runner state changes.

**Chat view** — scrollable message list. Renders user messages, assistant text (streamed), tool calls (name + status), tool results (collapsed by default). Markdown rendering via Glamour or simple formatting.

**Input** — multi-line text editor. Enter submits (shift+enter for newline). Disabled while agent is running.

**Sidebar** — session list. Up/down to select, enter to switch. Shows title, date, message count.

**Status bar** — current model, session ID, cumulative token count.

**Permission prompt** — overlay that appears when a tool needs approval. Shows tool name and input summary. y/n to approve/deny. Remembers per-session.

### Event Flow

```
User types message → App.Update
    → Disable input
    → Start runner.Run() in goroutine
    → Runner streams events via channel:
        TextDelta    → append to chat view, trigger View()
        ToolStart    → add tool call indicator to chat
        ToolDone     → update tool call status
        NeedApproval → show permission prompt, block runner
    → Run complete → enable input
```

The runner communicates with the TUI via a channel of UI events (not pubsub — direct typed channel for the single-consumer TUI).

### Key Bindings

- `Enter` — submit message
- `Shift+Enter` — newline in input
- `Ctrl+C` — stop current run (if running) or quit (if idle)
- `Ctrl+N` — new session
- `Ctrl+L` — clear screen
- `Tab` — toggle sidebar focus
- `Esc` — cancel permission prompt (deny)

**Verify:** Manual testing — launch TUI, verify streaming display, tool call rendering, session switching, permission prompts, ctrl+c interruption.

---

## Dependency Graph

```
Step 1: Runner cancellation ───────────────────────┐
Step 2: Interactive REPL ◄──── Step 1              │
Step 3: Fetch tool (independent) ──────────────────┤
Step 4: Subagents ◄──────── Steps 1, 3            │
Step 5: Skills (independent) ──────────────────────┤
Step 6: Permissions ◄──────── Step 2               │
                                                    ▼
Step 7: TUI ◄─────────────── Steps 2, 4, 5, 6
```

Parallelizable: Steps 3 + 5 are independent and can be built alongside anything. Steps 1 + 2 are prerequisites for the rest.

---

## What Phase 2 Does NOT Include

- Gateway daemon / WebSocket server — Phase 3
- Telegram bot — Phase 3
- Memory / RAG integration — Phase 3
- Workflows / multi-agent orchestration — Phase 3
- Cron jobs — Phase 3
- Coordinator (shared dependency hub) — Phase 3 (runners are wired directly for now)
- Message queuing (queue prompts while agent is busy) — Phase 3 (TUI disables input instead)

## Key Design Decisions

1. **REPL before TUI.** Step 2 builds a minimal readline REPL so multi-turn conversation works immediately. The TUI (Step 7) replaces it but both share the same runner wiring.
2. **Subagents get their own sessions.** Child sessions with `parent_id` linking. Isolated context, independent compaction. Parent gets a summary result via the armory tool.
3. **Runner takes AgentInfo at construction.** This lets subagent runners use different configs (restricted tools, MaxSteps, different model) without subclassing.
4. **SpawnAgent as a closure on ToolContext.** Avoids the armory tool needing direct access to the session service or provider. The runner wires the closure with its own dependencies.
5. **Permissions are callback-based.** The permission service calls an `askFunc` that the REPL/TUI provides. `nous run` sets `autoApprove: true`. Clean separation between policy and UI.
6. **TUI events via direct channel, not pubsub.** Single consumer (the TUI), typed events, no need for the broadcast semantics of pubsub. Simpler and faster.
7. **Skills use frontmatter, not config.** Skills are self-describing via their SKILL.md frontmatter. No central registry to maintain.
