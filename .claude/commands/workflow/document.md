# Document Feature

Generate concise markdown documentation for implemented work by analyzing the code changes against the original specification. Creates a doc in `app_docs/` based on the `git diff` (and any new untracked files) plus the spec.

## Variables

spec_file: $ARGUMENTS — path to the spec (relative to repo root, e.g. `specs/feature-search-ui.md`). A bare filename is resolved under `specs/**`. Optional; if omitted, document from the diff alone.

## Instructions

### 1. Analyze Changes

- Run `git diff origin/main --stat` and `git diff origin/main --name-only` to see what changed.
- Run `git status --porcelain` and read any **untracked** new files (`??`) — they are part of the work but absent from the diff.
- For significant changes (>50 lines), run `git diff origin/main <file>` on specific files to understand the implementation.
- **Guard:** if there is no diff against `origin/main` *and* no untracked new files, there is nothing to document — stop and report `Nothing to document: no changes found on this branch.` Do not write a doc.

### 2. Read Specification (if provided)

- If `spec_file` is provided, read it to understand the original requirements and success criteria.
- Frame the documentation around what was requested versus what was built.

### 3. Generate Documentation

- Create a new file in `app_docs/` (create the directory if it doesn't exist).
- Filename: `feature-{descriptive-name}.md` — a short feature name (e.g. "job-stop", "ocr-store", "mcp-tunnel").
- Follow the Documentation Format below. Focus on what was built, how it works, how to use it, and any setup required.

### 4. Final Output

- Return exclusively the path to the documentation file created and nothing else.

## Documentation Format

```md
# <Feature Title>

**Date:** <current date>
**Specification:** <spec_file or "N/A">

## Overview

<2-3 sentence summary of what was built and why>

## What Was Built

<the main components/features implemented, based on the diff>

- <Component/feature 1>
- <Component/feature 2>

## Technical Implementation

### Files Changed

- `<file_path>`: <what was changed/added>
- `<file_path>`: <what was changed/added>

### Key Changes

<the most important technical changes in 3-5 bullet points>

## How to Use

<step-by-step instructions for using the new feature>

1. <Step 1>
2. <Step 2>

## Configuration

<any configuration options, environment variables, or settings — omit if none>

## Notes

<any additional context, limitations, or future considerations — omit if none>
```

## Report

- IMPORTANT: Return exclusively the path to the documentation file created and nothing else.
