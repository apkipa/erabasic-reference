# Preprocessor and Macros (ERB/ERH)

This document covers two separate mechanisms that happen **before** normal statement execution:

1) **ERB bracket preprocessor directives**: `[IF ...]`, `[ELSE]`, `[ENDIF]`, `[SKIPSTART]`, etc.
2) **ERH `#DEFINE` macros** expanded by the expression lexer.

Both are implemented by engine code (not by script libraries) and are needed for strict compatibility.

## 1) ERB bracket preprocessor directives

Bracket preprocessor directives are recognized only in **ERB file loading**, and only when the line’s first non-whitespace character is `[` and the second character is **not** `[` (so `[[...]]` rename keys do not count as preprocessor directives).

### 1.1 Directive line syntax (exact scanning rules)

Given a line whose first non-whitespace is `[` and next char is not `[`, the loader parses:

- `[` (must be the first non-whitespace character)
- **directive keyword**: an identifier read as a maximal substring up to a delimiter (no whitespace allowed between `[` and the keyword)
- optional whitespace
- optional **single identifier argument** (same identifier scanning rules as elsewhere)
- optional whitespace
- `]` must appear immediately after the above (otherwise the line is warned as invalid)
- any remaining characters after `]` are ignored with a warning

Consequences:

- `[IF HOGE]` is valid.
- `[ IF HOGE]` is **not** valid (space after `[` makes the keyword empty).
- Only one “argument token” is supported: `[IF A B]` treats `B` as “extra” and warns/ignores it.

### 1.2 Supported directives and semantics

All directives below are **case-insensitive** under the engine’s configured comparison mode.

#### `[SKIPSTART] ... [SKIPEND]`

- `[SKIPSTART]` begins a “skip mode” that forces all non-preprocessor lines to be ignored.
- `[SKIPEND]` ends that skip mode.

Notes:

- Nested `[SKIPSTART]` is warned as a duplicate; skip mode remains active.
- While skip mode is active, the loader still recognizes and processes further preprocessor directives (so nesting inside skip blocks still affects preprocessor nesting state), but non-preprocessor lines are ignored.

#### `[IF_DEBUG] ... [ELSEIF] ... [ELSE] ... [ENDIF]`

- `[IF_DEBUG]` enables the first branch only when the engine is in debug mode.

#### `[IF_NDEBUG] ... [ELSEIF] ... [ELSE] ... [ENDIF]`

- `[IF_NDEBUG]` enables the first branch only when the engine is **not** in debug mode.

#### `[IF MACRO] ... [ELSEIF MACRO] ... [ELSE] ... [ENDIF]`

- `[IF X]` enables the first branch only when macro `X` is **defined** (existence check only).
- `[ELSEIF X]` enables its branch only if no previous branch in this IF-chain has been enabled, and `X` is defined.
- `[ELSE]` enables its branch only if no previous branch in this IF-chain has been enabled.

Important: `[IF X]` does **not** evaluate the macro expansion value; it only checks whether the name exists in the macro table.

### 1.3 Error/warning behavior and mismatches

The loader uses warnings for most preprocessor mistakes (and continues loading):

- missing required arguments (e.g. `[IF]` or `[ELSEIF]`) → warning, and the directive does not push/pop the preprocessor stack
- unexpected/mismatched end markers (e.g. `[ENDIF]` without an open IF, `[SKIPEND]` without `[SKIPSTART]`) → warning
- invalid bracket syntax (e.g. missing closing `]`) → warning

At end-of-file, if there are unmatched directives left in preprocessor nesting state, the loader emits **one** warning for the topmost missing end marker.

### 1.4 Interaction with line continuation blocks (`{...}`)

When a file is currently in a disabled preprocessor state (inside a skipped branch), the line reader is called in a mode that does **not** recognize `{` / `}` as line-continuation markers.

Practical effect:

- `{` / `}` lines inside skipped branches do not start/stop continuation blocks and do not produce continuation-related errors.

## 2) `#DEFINE` macros (declared in ERH, expanded by the lexer)

Macros are declared in **ERH** files and are expanded by the engine’s ordinary **expression lexer** as a post-processing step over the token list.

Example:

    #DEFINE FIVE 5

Then in an expression context:

    X = FIVE + FIVE

lexes as if it were:

    X = 5 + 5

### 2.1 Declaration model (this engine)

- `#DEFINE NAME ...replacement...` declares a macro named `NAME`.
- Empty macros are allowed: `#DEFINE NAME` defines `NAME` with an empty replacement.
- The engine checks macro names for collisions with reserved identifiers and emits warnings/errors accordingly.
- Name comparison follows the engine's normal identifier-comparison mode (config item `IgnoreCase`).
- If `NAME` is already present in the macro table, the redeclaration emits a level-2 warning, does not replace the earlier macro, and causes ERH loading to fail for startup purposes.

Function-like macros (`#DEFINE NAME(arg1,...) ...`) are recognized by older/other code paths, but **this engine rejects them in ERH** (declaring one is an error).

### 2.2 Expansion model (token-based, bounded)

Expansion happens after lexing, over the token sequence:

- The lexer scans left-to-right.
- When it sees an identifier token matching a macro name, it replaces that one identifier token with the macro’s replacement token sequence.
- Newly inserted tokens are immediately subject to further expansion as the scan continues.

There is a hard limit on total expansions per lexed unit:

- Maximum expansions: `100`
- If exceeded, the lexer throws an error (intended to catch self/circular references).

### 2.3 Where macros apply (and where they do not)

Macros apply wherever the engine uses the ordinary **expression lexer**, including:

- normal numeric/string expressions
- the expression bodies inside FORM placeholders `%...%` and `{...}`
- the condition part of `\@...\@` string-ternary constructs

Macros do **not** apply to:

- raw/simple string arguments parsed as plain text by specific instructions
- literal segments of FORM strings (outside `%...%` / `{...}`)
- ERB line-start classification itself (`@` / `$` label lines, post-label `#...` lines, and `[` preprocessor directives) because that classification happens before token-level macro expansion

### 2.4 Limitations and common pitfalls

- Macros do not turn text into statements: a macro replacement is still just expression tokens.
- In particular, a macro expansion cannot turn an ordinary ERB line into an `@LABEL`, `$LABEL`, `#...`, or `[...]` line-start structure.
- Even though macro declarations are tokenized with “assignment allowed” in ERH, using `=` inside a normal expression is still an error at expression-parse time.
- Because replacement is token-based (not raw text), you cannot rely on “spacing tricks” inside macro bodies; use parentheses explicitly to avoid precedence surprises.
