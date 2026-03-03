# Appendix

This folder contains **optional** supporting material for the EraBasic reference.

The main reference documents in the repository root are intended to be **self-contained** and sufficient for understanding the language as implemented by this Emuera codebase. Appendix documents are primarily for:

- implementation-oriented background (engine-specific wiring and quirks), and
- tooling outputs / indexes used for offline lookup and fact-checking.

Nothing in this folder should be treated as “more normative” than the spec-facing docs in the repository root.

## Important (maintenance rule)

This folder is intentionally treated as **generated/derived and/or legacy**:

- `tooling/` is **tooling-derived output** (indexes, metadata) and should generally be updated by regenerating it from sources, not by hand-editing.
- `implementation/` currently contains **legacy stubs** kept to avoid breaking older links.

If you add new reference content, **do not put it in `appendix/`**. Add it to the main reference in the repository root (or another clearly non-appendix location) so the core reference remains discoverable and stable.

## Subfolders

### `implementation/`

Legacy implementation notes and compatibility stubs.

- `implementation/builtins-core-implementation-notes.md` is currently a **legacy stub** kept for older links; the substantive content was migrated into `control-flow.md`, `runtime-model.md`, `functions.md`, and `labels.md`.

### `tooling/`

Tooling-derived indexes and metadata for the built-in instruction/method set.

These files exist to make it easy to audit and fact-check `builtins-reference.md` against engine/doc sources without having to grep the engine manually.

- `tooling/builtins-engine.md`
- `tooling/builtins-engine-metadata.md`
- `tooling/builtins.md`
- `tooling/builtins-signatures.md`
