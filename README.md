# EraBasic Language Reference (EvilMask / Emuera)

This is a compact, English-language reference for the EraBasic (ERB) language as implemented by the Emuera engine in this workspace.

This folder is intended to be **self-contained**: you should be able to read and use it without needing to open other documentation files in this repository.

## Contents

This reference has two “layers”:

- **Spec-facing**: rules you need for a compatible implementation.
- **Implementation-oriented notes**: how this specific engine is wired internally (helpful, but not always normative).

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

### Spec-facing (statements, flow, and functions)

- [`grammar.md`](grammar.md) — statement-level grammar (EBNF + matching rules)
- [`control-flow.md`](control-flow.md) — `IF/SIF`, loops, `SELECTCASE`, notes and links
- [`functions.md`](functions.md) — `CALL/RETURN`, arguments (`ARG/ARGS`), expression functions (`#FUNCTION/#FUNCTIONS`)
- [`argument-parsing-modes.md`](argument-parsing-modes.md) — how built-ins parse arguments (raw vs expression vs FORM) and how `;` behaves
- [`line-start-special-cases.md`](line-start-special-cases.md) — engine line-start dispatch rules (`;!;`, `{...}`, `[...]`, `@/$/#`, prefix `++/--`)
- [`preprocessor-and-macros.md`](preprocessor-and-macros.md) — `#DEFINE`, `[IF ...]`, `[SKIPSTART]`, debug-only lines

### Built-ins (engine truth)

- [`builtins-reference.md`](builtins-reference.md) — full built-in instruction + expression-function catalog (engine-extracted, no tables)
- [`builtins-overrides/`](builtins-overrides/) — manual entry overrides used to “realize” entries beyond the engine-extracted skeletons
- [`builtins-overrides/builtins-progress.md`](builtins-overrides/builtins-progress.md) — writing progress tracker for `builtins-reference.md` (manual overrides vs skeleton)

### Built-ins (appendix / tooling)

- [`appendix/tooling/builtins-engine.md`](appendix/tooling/builtins-engine.md) — built-in instruction/method name catalogs extracted from engine source
- [`appendix/tooling/builtins-engine-metadata.md`](appendix/tooling/builtins-engine-metadata.md) — built-in instruction metadata extracted from engine source (argument builders, flags, block pairing)
- [`appendix/tooling/builtins.md`](appendix/tooling/builtins.md) — doc-derived built-in command/function quick index (for fact-check)
- [`appendix/tooling/builtins-signatures.md`](appendix/tooling/builtins-signatures.md) — doc-derived built-in signatures (erbapi blocks, offline lookup / fact-check)

### Implementation-oriented notes (engine-specific)

- [`runtime-model.md`](runtime-model.md) — core runtime execution model (stack, events, scopes)
- [`pipeline.md`](pipeline.md) — exact load/preprocess/parse ordering (engine source of truth)
- [`source-position-mapping.md`](source-position-mapping.md) — how Emuera maps warnings/errors to file/line (implementation detail)
- [`appendix/implementation/builtins-core-implementation-notes.md`](appendix/implementation/builtins-core-implementation-notes.md) — readable, implementation-oriented notes for core control-flow/call/return (and the instruction keyword catalog)

### Data and config (tightly coupled to language use)

- [`data-files.md`](data-files.md) — config/CSV/rename/ERD formats tied to the language
- [`config-items.md`](config-items.md) — config key catalog (types, defaults, key spellings)

### Project meta

- [`errors-and-warnings.md`](errors-and-warnings.md) — warning levels, filtering, and error vs warning mechanics
- [`coverage.md`](coverage.md) — coverage plan for a reimplementable core spec
- [`sources.md`](sources.md) — where this reference was derived from (optional)

## Terminology

- **ERB**: script files (EraBasic).
- **ERH**: header files, processed before ERB, used for global `#DIM/#DIMS` and `#DEFINE`.
- **FORM syntax**: the `%...%` and `{...}` interpolation used by `PRINTFORM`-family commands and some string contexts.
- **`\@...\@` (string-ternary literal)**: a conditional string construct used inside FORM and also as a standalone string-expression token.
