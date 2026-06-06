# Review

Compare the **work done against its specification file** to confirm the implementation matches what was requested. Read the spec to understand the requirements, read the `git diff` to see what was built, and judge whether the diff satisfies each requirement and use case in the spec. Report any mismatches as issues with a severity. This is a **spec-conformance review, not a test** — whether the code runs, builds, or passes tests is the build step's job, not yours.

## Variables

spec_file: $ARGUMENTS — path to the spec (relative to repo root, e.g. `specs/feature-search-ui.md`). A bare filename is resolved under `specs/**`. If omitted, auto-discover (see Phases).

## Phases

Execute in order. If a gate fails, emit the exit format and stop.

| Phase | Action | Gate | Failure |
|---|---|---|---|
| Locate | Identify the spec: if `spec_file` is provided, use it (resolve a bare filename under `specs/**`); otherwise check the current branch (`git branch`) and look for a `specs/**/*.md` file in `git diff origin/main` that matches the work. Read it. | Can you point to one spec file that describes the intended work? | `EXIT_NO_SPEC` |
| Understand | Read the spec's Requirements/Fix Direction and every Use Case. Read `git diff origin/main` to see what was built. Then run `git status --porcelain` and read any **untracked** new files (`??`) — they are part of the work but absent from the diff. | Can you map each use case to the code that implements it (or confirm it's absent)? | `EXIT_NO_DIFF` |
| Assess | For each requirement and use case, decide: satisfied, partially satisfied, or missing. Flag anything in the diff that goes beyond the spec (scope creep) or contradicts it. | Have you judged every use case in the spec against the diff? | — |

### Failure Modes

| Exit Code | Meaning | Recommended Action |
|---|---|---|
| `EXIT_NO_SPEC` | No spec file provided or discoverable for this branch | Pass the spec path explicitly as the argument |
| `EXIT_NO_DIFF` | No changes to review — neither a diff against `origin/main` nor any untracked new files | Confirm the work exists on this branch (committed, staged, or at least saved) |

On gate failure, emit only:

```md
# Exit: {EXIT_CODE}

## What was tried
<spec path attempted, branch, what the diff showed>

## What's missing
<what information or access would unblock this>
```

## Severity Guidelines

Judge the impact of each mismatch on the spec's intent:

- `skippable` — diverges from the spec but is a non-blocking nit; the work is still releasable
- `tech_debt` — non-blocking, but leaves debt that should be addressed later (e.g. a use case met in a fragile or incomplete way)
- `blocker` — the implementation fails to satisfy a required use case, or contradicts the spec; must be fixed before release

## Constraints

- Conformance, not correctness-by-execution — you compare diff to spec; you do not run, build, or test the code
- Spec is the source of truth — a "better" implementation that ignores the spec is still a mismatch; report it
- Stay in scope — review only what the spec covers and what the diff changed
- Don't report nits that aren't traceable to a spec requirement — if the spec doesn't speak to it, it's not a review issue

## Codebase Scope

| Path | Contains |
|---|---|
| `README.md` | Project overview and architecture |
| `specs/**` | Spec files — the requirements you review against |
| `apps/listen/**` | Python: HTTP job listener (`main.py`) + Claude Code worker (`worker.py`) |
| `apps/mcp/**` | Python: MCP server + client (`src/agent_mcp/`) bridging agents to the device |
| `apps/drive/**` | Python: tmux terminal-automation CLI (`commands/`, `modules/`) |
| `apps/direct/**` | Python: direct job-sender CLI (`src/direct/`) |
| `apps/steer/Sources/steer/**` | Swift: macOS GUI automation CLI (click, type, OCR, windows, screen capture) |

Ignore all other paths (including `.venv/`, `.build/`, `__pycache__/`).

## Report

Emit this markdown on the success path. Omit `## Issues` when there are none.

```md
# Review: <spec name>

## Verdict
<`PASS` if there are no blocker issues, `FAIL` if any blocker exists>

## Summary
<2-4 sentences, standup-style: what was built and whether it matches the spec.>

## Use Case Coverage
<one line per spec use case: ✅ satisfied / ⚠️ partial / ❌ missing — with a brief note>

- **1. <use case name>** — ✅ <how the diff satisfies it, with file:line>
- **2. <use case name>** — ❌ <what's missing>

## Issues (if applicable)
<one entry per mismatch>

### 1. <short description>
- **Spec says:** <the requirement / use case being violated>
- **Diff does:** <what the implementation actually does, with file:line>
- **Severity:** `skippable` | `tech_debt` | `blocker`
- **Resolution:** <what would bring the diff in line with the spec>
```
