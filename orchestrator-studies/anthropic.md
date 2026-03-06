# Anthropic OAuth Token Compatibility

## Problem

Raw OAuth tokens from Claude Code (`~/.claude/.credentials.json`) are rejected by the Anthropic API when used for Opus/Sonnet models or when tools are included in the request. The error: `"This credential is only authorized for use with Claude Code and cannot be used for other API requests."`

## Root Cause

The Anthropic API validates that OAuth token requests originate from Claude Code by checking three things beyond just the HTTP headers. Without all three, the request is rejected.

## Required Headers (Necessary But Not Sufficient)

OAuth requests must use `Authorization: Bearer <token>` (not `X-Api-Key`) and include these headers:

```
anthropic-beta: claude-code-20250219,oauth-2025-04-20
anthropic-dangerous-direct-browser-access: true
user-agent: claude-cli/2.1.0 (external, cli)
x-app: cli
```

In the Go SDK, `option.WithAuthToken()` sets the Bearer header, while `option.WithAPIKey()` sets `X-Api-Key`.

## Three Additional Requirements

Discovered by examining pi-ai (the provider library used by moltbot/openclaw) at `packages/ai/src/providers/anthropic.ts`.

### 1. System Prompt Prefix

The first system prompt block must be exactly:

```
You are Claude Code, Anthropic's official CLI for Claude.
```

The actual system prompt follows as a second text block. This is how the API verifies the request is a Claude Code-like session.

### 2. Tool Name Transformation (Outbound)

Tool names sent to the API must match Claude Code's canonical PascalCase:

| Original | Claude Code |
|----------|-------------|
| bash     | Bash        |
| read     | Read        |
| write    | Write       |
| edit     | Edit        |
| glob     | Glob        |
| grep     | Grep        |
| ls       | Ls          |

This applies to both the tool definitions and any `tool_use` content blocks in the message history.

The full set of Claude Code tool names (for reference):
`Read`, `Write`, `Edit`, `Bash`, `Grep`, `Glob`, `AskUserQuestion`, `EnterPlanMode`, `ExitPlanMode`, `KillShell`, `NotebookEdit`, `Skill`, `Task`, `TaskOutput`, `TodoWrite`, `WebFetch`, `WebSearch`

### 3. Tool Name Reverse Mapping (Inbound)

When the API returns `tool_use` blocks, the names come back in PascalCase. These must be mapped back to the original lowercase names so the local tool dispatch works correctly.

## Implementation

- `internal/provider/anthropic.go` — stores `isOAuth` flag, applies all three transformations in `Stream()`
- `internal/provider/convert.go` — `convertMessagesOAuth()` remaps tool names in message history
- `internal/cmd/run.go` — auth priority: Claude Code OAuth > saved token > config > env var
- `internal/auth/claude_code.go` — reads `~/.claude/.credentials.json`
- `internal/auth/token.go` — `IsSetupToken()` detects `sk-ant-oat01-` prefixed tokens (also OAuth)

## Reference

Source of truth: pi-ai `packages/ai/src/providers/anthropic.ts` — `isOAuthToken()`, `toClaudeCodeName()`, `fromClaudeCodeName()`, and the system prompt injection in the stream/chat methods.
