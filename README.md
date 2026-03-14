# EraBasic Language Reference (EvilMask / Emuera)

This is a compact, English-language reference for the EraBasic (ERB) language as implemented by the Emuera engine in this workspace.

This reference was assembled and curated by **OpenAI GPT-5.2 (high)**.

This folder is intended to be **self-contained**: you should be able to read and use it without needing to open other documentation files in this repository.

## Contents

This reference has two “layers”:

- **Spec-facing**: rules you need for a compatible implementation.
- **Engine-behavior notes**: engine-specific behavior that helps match compatibility boundaries, even when it is not purely normative.

### Spec-facing (core language)

- [`lexical.md`](lexical.md) — tokens, comments, whitespace, literals, escapes
- [`program-structure.md`](program-structure.md) — files, functions (`@...`), blocks, events
- [`labels.md`](labels.md) — function labels (`@...`), local jump labels (`$...`), overloading, event grouping
- [`variables.md`](variables.md) — built-ins, arrays, `#DIM/#DIMS`, ERH globals, `REF`, `DYNAMIC`, `CONST`
- [`string-key-indexing.md`](string-key-indexing.md) — exact CSV/alias/ERD string-key → index mapping rules for `VAR:Key`

### Spec-facing (expressions and text)

- [`expressions.md`](expressions.md) — numeric vs string expressions, operators, FORM/format strings
- [`expression-grammar.md`](expression-grammar.md) — formal expression grammar (EBNF, precedence, tokenization quirks)
- [`formatted-strings.md`](formatted-strings.md) — FORM scanner + `%...%`/`{...}` placeholders, `@"..."`, triple symbols, `\@...\@`
- [`html-output.md`](html-output.md) — HTML-like output mini language (`HTML_PRINT`, HTML string helpers)

### Spec-facing (statements, flow, and functions)

- [`grammar.md`](grammar.md) — statement-level grammar (EBNF + matching rules)
- [`control-flow.md`](control-flow.md) — `IF/SIF`, loops, `SELECTCASE`, notes and links
- [`system-flow.md`](system-flow.md) — system phase state machine (TITLE/SHOP/TRAIN/ABLUP/…) and required `BEGIN` contracts
- [`input-flow.md`](input-flow.md) — host-side input request lifecycle, segmentation, submission paths, and wait-state consumption rules
- [`output-flow.md`](output-flow.md) — shared output-state model (logical lines, temporary lines, button regions, history/buffer APIs)
- [`console-layout.md`](console-layout.md) — shared width measurement, wrapping, splitting, and alignment backend used by plain-text and HTML output
- [`cbg-layer.md`](cbg-layer.md) — client-background (`CBG`) layer, depth ordering, hit-testing, and its boundary against normal output/buttons
- [`functions.md`](functions.md) — `CALL/RETURN`, arguments (`ARG/ARGS`), expression functions (`#FUNCTION/#FUNCTIONS`)
- [`argument-parsing-modes.md`](argument-parsing-modes.md) — how built-ins parse arguments (raw vs expression vs FORM) and how `;` behaves
- [`line-start-special-cases.md`](line-start-special-cases.md) — engine line-start dispatch rules (`;!;`, `{...}`, `[...]`, `@/$/#`, prefix `++/--`)
- [`preprocessor-and-macros.md`](preprocessor-and-macros.md) — `#DEFINE`, `[IF ...]`, `[SKIPSTART]`, debug-only lines

### Built-ins (engine truth)

- [`builtins-reference.md`](builtins-reference.md) — user-facing built-ins reference (manual overrides only; no engine debug info)
- [`builtins-index.md`](builtins-index.md) — user-facing built-ins index by tag (from `builtins-overrides/**`)
- [`builtins-overrides/`](builtins-overrides/) — manual entry overrides used to “realize” entries beyond the engine-extracted skeletons
- [`builtins-overrides/builtins-progress.md`](builtins-overrides/builtins-progress.md) — writing progress tracker for `builtins-reference.md` (manual overrides vs skeleton)

### Built-ins (appendix / tooling)

- [`appendix/README.md`](appendix/README.md) — what lives in `appendix/` and how to treat it
- [`appendix/tooling/builtins-engine.md`](appendix/tooling/builtins-engine.md) — built-in instruction/method name catalogs extracted from engine source
- [`appendix/tooling/builtins-engine-metadata.md`](appendix/tooling/builtins-engine-metadata.md) — built-in instruction metadata extracted from engine source (argument builders, flags, block pairing)
- [`appendix/tooling/builtins-reference-engine.md`](appendix/tooling/builtins-reference-engine.md) — engine-dump built-ins reference (skeletons + validation structures + file/line refs; not user-facing)
- [`appendix/tooling/builtins.md`](appendix/tooling/builtins.md) — doc-derived built-in command/function quick index (for fact-check)
- [`appendix/tooling/builtins-signatures.md`](appendix/tooling/builtins-signatures.md) — doc-derived built-in signatures (erbapi blocks, offline lookup / fact-check)

### Compatibility-critical engine behavior

- [`runtime-model.md`](runtime-model.md) — core runtime execution model (stack, events, scopes)
- [`plugins.md`](plugins.md) — plugin loading and `CALLSHARP` integration (public extension contract)
- [`pipeline.md`](pipeline.md) — exact load/preprocess/parse ordering (compatibility-critical)

### Implementation detail / diagnostics

- [`source-position-mapping.md`](source-position-mapping.md) — how Emuera maps warnings/errors to file/line (diagnostic behavior)
- [`host-aux-files.md`](host-aux-files.md) — keyboard macros, debug auxiliary files, and selected host-side log files
- [`appendix/implementation/builtins-core-implementation-notes.md`](appendix/implementation/builtins-core-implementation-notes.md) — legacy (kept for older links; content migrated into the main docs)

### Data and config (tightly coupled to language use)

- [`data-files.md`](data-files.md) — config/CSV/rename/ERD formats tied to the language
- [`config-items.md`](config-items.md) — main/debug/replace item catalog plus shared config-adjacent derived runtime values
- [`filesystem-paths.md`](filesystem-paths.md) — shared path-handling families used by filesystem/resource built-ins
- [`save-files.md`](save-files.md) — save directories, persistence partitions, and on-disk save formats (binary + legacy text)
- [`resources-and-sprites.md`](resources-and-sprites.md) — `resources/**/*.csv` sprite loading and sprite-name resolution used by UI/HTML output

### Project meta

- [`errors-and-warnings.md`](errors-and-warnings.md) — warning levels, filtering, and error vs warning mechanics
- [`coverage.md`](coverage.md) — coverage plan for a reimplementable typical-game spec
- [`sources.md`](sources.md) — where this reference was derived from (optional)
- [`AGENTS.md`](AGENTS.md) — default authoring rules for this reference

## Terminology

- **ERB**: script files (EraBasic).
- **ERH**: header files, processed before ERB, used for global `#DIM/#DIMS` and `#DEFINE`.
- **FORM syntax**: the `%...%` and `{...}` interpolation used by `PRINTFORM`-family commands and some string contexts.
- **`\@...\@` (string-ternary literal)**: a conditional string construct used inside FORM and also as a standalone string-expression token.

## Parameter notation

Unless a parameter is explicitly marked `optional`, read it as required.
If an entry says `optional, ...; default X`, omitting that argument is observably equivalent to supplying `X` unless the entry says otherwise.
