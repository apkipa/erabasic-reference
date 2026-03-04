# `builtins-overrides/`

This folder contains **manual, human-written** upgrade snippets for entries in the user-facing built-ins reference:

- `erabasic-reference/builtins-reference.md`

The generator (`erabasic-reference/tools/generate_builtins_reference.py`) produces two documents:

- `erabasic-reference/builtins-reference.md` — user-facing (overrides only; no engine debug info)
- `erabasic-reference/appendix/tooling/builtins-reference-engine.md` — writer/debug engine dump (engine-extracted skeletons + refs)

It also generates a progress tracker at:

- `builtins-progress.md` — manual override coverage for `builtins-reference.md`

## File layout

- `instructions/<NAME>.md` — overrides for instruction entries (`## NAME (instruction)`).
- `methods/<NAME>.md` — overrides for expression function entries (`## NAME (expression function)`).

## Snippet format

Each override file is parsed as a set of sections.
Use the exact section titles below (bold Markdown lines):

- `**Summary**`
- `**Tags**` (optional; user-facing)
- `**Progress state**` (optional; internal tooling only)
- `**Syntax**`
- `**Arguments**`
- `**Signatures / argument rules**` (methods only)
- `**Semantics**`
- `**Errors & validation**`
- `**Examples**`

Inside each section, write normal Markdown (typically `-` bullet lines).

Notes:
- `builtins-reference.md` is intentionally strict: it does **not** show engine-extracted skeletons. Missing sections remain `(TODO)`.
- `builtins-reference-engine.md` contains the engine-extracted skeletons and file/line references for fact-checking.
- The generator **fails by default** if any validation issues are found (missing docs, unknown section titles, etc.). Use `--no-fail` to override.

Argument defaults and “omitted argument” behavior should be documented inline under `**Arguments**` (for example:
`- start (optional, default 0): ...`), not in a standalone section.

### `Tags` (optional; user-facing)

If present, add one or more bullets, for example:

- `**Tags**`
- `- control-flow`
- `- text`
- `- save-system`

The generator will use tags to build a user-facing index file (`builtins-index.md`).

### `Progress state` (optional)

`builtins-progress.md` is intentionally conservative:
- Any entry without a manual override is `⛔ none`.
- Any entry with a manual override is `🟡 partial` unless explicitly marked complete.

To mark an entry as complete, add:

- `**Progress state**`
- `- complete`

## Authoring rules

Default authoring rules for this reference live in `erabasic-reference/agents.md`.
