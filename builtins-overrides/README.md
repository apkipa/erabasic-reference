# `builtins-overrides/`

This folder contains **manual, human-written** upgrade snippets for entries in `builtins-reference.md`.

The generator (`erabasic-reference/tools/generate_builtins_reference.py`) merges these snippets into the generated document.

It also generates a progress tracker at:

- `builtins-progress.md` — manual override coverage for `builtins-reference.md`

## File layout

- `instructions/<NAME>.md` — overrides for instruction entries (`## NAME (instruction)`).
- `methods/<NAME>.md` — overrides for expression function entries (`## NAME (expression function)`).

## Snippet format

Each override file is parsed as a set of sections.
Use the exact section titles below (bold Markdown lines):

- `**Summary**`
- `**Syntax**` (instructions only)
- `**Arguments**`
- `**Defaults / optional arguments**` (instructions only)
- `**Signatures / argument rules**` (methods only)
- `**Semantics**`
- `**Errors & validation**`
- `**Examples**`

Inside each section, write normal Markdown (typically `-` bullet lines).

Notes:
- You do **not** need to include `Metadata` or `Engine references`; those are generated automatically.
- If a section is omitted, the generator falls back to the engine-extracted skeleton for that section (when available), or leaves it as `(TODO)`.
