# Line-Start Special Cases (engine-accurate)

This document summarizes the **line-initial** (first non-whitespace) patterns that are treated specially by this Emuera codebase.

It is intended as an implementer’s checklist: if you parse EraBasic “as a normal statement language” without these special cases, you will not match Emuera behavior.

## 0) “First non-whitespace” is not purely lexical

Many loaders first skip leading whitespace and executable-comment prefixes before deciding what a line “starts with”.

That routine:

- skips ASCII space and tab
- skips full-width space (`U+3000`) only when `SystemAllowFullSpace=YES`
- treats `;` as “skip-to-end-of-line comment”, **except** for the three executable prefixes defined in section 1

So in many contexts, the “first character” is really: “the first character after whitespace and, if applicable, executable-comment-prefix stripping (`;!;`, `;#;`, `;^;`)”.

## 1) Executable comment prefixes: `;!;`, `;#;`, `;^;`

When a loader uses `SkipWhiteSpace`, a line that begins with `;` is normally treated as a comment (skipped to end-of-line).

But these prefixes are *not* treated as comments: they are **stripped**, and the rest of the line continues to be parsed as code/text:

- `;!;` — always treated as executable in this engine.
- `;#;` — treated as executable only when the engine is in debug mode; otherwise it behaves like a normal comment line.
- `;^;` — treated as executable in this engine (historically an EMEE-only extension, but it is recognized here unconditionally).

Important scope detail:

- These prefixes affect any loader that uses `EraStreamReader.ReadEnabledLine(...)` (ERB/ERH and many CSV-like readers).
- They do **not** apply to config loaders that read raw lines and only treat a literal leading `;` as a comment (`*.config`, `_Replace.csv`, `_Rename.csv`).

## 2) Continuation blocks: `{` … `}` (line reader)

`EraStreamReader.ReadEnabledLine(disabled=false)` treats a line whose first non-whitespace character is `{` as the start of a **line concatenation block**, but only when the whole trimmed line equals `{`.

It then concatenates subsequent physical lines until it finds a closing line whose trimmed content equals `}`.

Notes:

- A stray `}` outside of a continuation block is an error at line-reading time.
- Continuation is disabled when the reader is called with `disabled=true` (used while skipping preprocessor-disabled regions).

This is not “syntax” in the ERB grammar; it happens before parsing proper. See `lexical.md` and `pipeline.md`.

## 3) ERB bracket preprocessor: `[` … `]`

In ERB loading only, if the first non-whitespace character is `[` and the *next* character is not `[` (so it’s not `[[...]]` rename syntax), the line is treated as a **preprocessor directive** and handled before script parsing.

Supported directives in this engine:

- `[SKIPSTART]` / `[SKIPEND]`
- `[IF_DEBUG]` / `[IF_NDEBUG]`
- `[IF MACRO]` / `[ELSEIF MACRO]` / `[ELSE]` / `[ENDIF]`

These directives are parsed as identifiers (no expressions; no quoting), and (in this implementation) are case-sensitive.

## 4) ERB “sharp lines”: `#...` after a function label

In ERB:

- If a line starts with `#` and the **previous logical line** was a function label (`@...`), it is parsed as a function attribute/metadata line (examples: `#LOCALSIZE`, `#DIM`, `#FUNCTIONS`, etc.).
- Otherwise, a `#` line is invalid in that position (warned and ignored as metadata; the engine does not treat it as a statement).

In ERH:

- Every enabled line must start with `#` (ERH is a header language, not a general statement language).

## 5) Label lines: `@...` and `$...`

In ERB loading:

- `@NAME ...` begins a **function label** (function definition).
- `$NAME` defines a **local jump label** within the current function.

These are parsed by a dedicated label-line routine, not the normal instruction parser.

## 6) Prefix `++X` / `--X` statement special-case

When parsing a normal ERB statement line (not a label, not `#`, not a preprocessor directive), the statement parser has a dedicated line-initial special case:

- If the first character is `+` or `-`, the engine attempts to interpret the line as a **prefix increment/decrement statement** (`++X` / `--X`).
- If the line starts with `+`/`-` but is not actually `++`/`--`, the line is rejected as an invalid line (it is not treated as a general “expression statement”).

This is an engine parsing rule, not a general EraBasic grammar rule.

