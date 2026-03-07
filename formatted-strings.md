# Formatted Strings (FORM): `%...%`, `{...}`, `@"..."`, triple symbols, and `\@...\@`

This document specifies Emuera’s **formatted-string (FORM)** system as implemented by this codebase.

FORM is used in two closely related ways:

1) **FORM strings** parsed directly from instruction arguments (not expression-lexed first), such as `PRINTFORM`-family arguments and some “FORM-capable” string arguments.
2) **Formatted-string terms inside string expressions**, produced by the expression lexer for:
   - `@"...FORM..."` (a formatted-string literal), and
   - `\@ cond ? left [# right] \@` (a string-ternary literal form that also tokenizes as a formatted-string term).

FORM parsing is **not** the same as double-quoted string literal parsing:

- FORM has its own escape rules (see §4).
- FORM recognizes interpolation placeholders `%...%` and `{...}` (see §2).
- Triple-symbol recognition in FORM (for sequences like `***`) is controlled by `SystemIgnoreTripleSymbol` (see §3).

## 0) Data model (what FORM produces)

The formatted-string analyzer produces a token (`StrFormWord`) that represents:

- an array of literal segments `strs` with length `subwords.Length + 1` (indices `0 <= i <= subwords.Length`)
- an array of placeholders/subwords `subwords` (indices `0 <= i < subwords.Length`)

Evaluation concatenates them in order:

`strs[0] + eval(subwords[0]) + strs[1] + eval(subwords[1]) + ... + strs[n]`.

During later “restructure”/constant-folding, a `StrFormWord` can collapse to:

- a constant string (`SingleStrTerm`) if it contains no subwords, or if all subwords fold into constants, or
- the single embedded string expression term itself, if the FORM consists of exactly one subword and no surrounding literals.

## 1) Where FORM is recognized

### 1.1 In expression lexing

When lexing an ordinary expression:

- `@"...` starts a formatted-string literal. The lexer reads FORM content until the next `"` and emits one `StrFormWord` token.
- `\@` starts a string-ternary literal form. The lexer parses the ternary structure and emits one `StrFormWord` token containing a `YenAtSubWord`.

In expression contexts, a backslash (`\\`) is otherwise not a normal token: a `\\` that is **not** followed by `@` is a lexing error.

### 1.2 In FORM-capable instruction arguments

Some instruction argument builders read FORM directly from the raw character stream using the formatted-string analyzer (not the normal expression lexer). Practically, you will see three termination modes:

- parse until end-of-line (full FORM argument)
- parse until `,` (FORM argument lists)
- parse until the first of `(` `[` `,` `;` (used for `CALLFORM`-style “function name” fields), with trimming enabled

## 2) Interpolation placeholders: `%...%` and `{...}`

FORM recognizes two placeholder forms in its character stream:

### 2.1 `% ... %` (string operand)

Syntax (conceptual):

- `%` *placeholder-body* `%`

The placeholder body is lexed as an **expression token stream** until the closing `%` at nesting depth 0.

Compilation rules:

- The first item inside `%...%` is the **operand**. It must be a **string-valued expression**.
- Optional extension fields may follow, separated by commas inside the placeholder:
  - `, width` where `width` is an integer expression
  - `, LEFT|RIGHT` where the token must be an identifier equal to `LEFT` or `RIGHT` (case-insensitive per config)

Semantics:

- If `width` is omitted: result is just the operand string.
- If `width` is present:
  - Default alignment is `RIGHT` (pad left).
  - If `LEFT` is specified, it pads right.
  - If the computed padding width is smaller than the string’s length, the string is returned unchanged.

Width measurement is **language-dependent** (§5.1).

### 2.2 `{ ... }` (numeric operand)

Syntax (conceptual):

- `{` *placeholder-body* `}`

The placeholder body is lexed as an expression token stream until the closing `}` at nesting depth 0.

Compilation rules:

- The first item inside `{...}` is the **operand**. It must be an **integer-valued expression**.
- Optional extension fields are the same shape as `%...%`:
  - `, width` (integer expression)
  - `, LEFT|RIGHT`

Semantics:

- The operand is converted to decimal text using `.ToString()`.
- If `width` is present, padding uses normal string character count (not `useLanguage` byte-count logic).

### 2.3 Errors for `%...%` and `{...}`

The engine reports errors at parse/compile time for:

- missing closing `%` / `}` for a placeholder
- an empty placeholder body (e.g. `%%` or `{}`)
- operand type mismatch (`%...%` requires string; `{...}` requires integer)
- `, LEFT|RIGHT` present but the third field is not an identifier
- third field is an identifier but not `LEFT` or `RIGHT`
- extra tokens after the optional third field inside the placeholder

## 3) Triple symbols (`***`, `+++`, `===`, `///`, `$$$`)

When `SystemIgnoreTripleSymbol` is `false`, the formatted-string analyzer recognizes **three identical characters in a row** for the following leading characters:

- `***` `+++` `===` `///` `$$$`

Each expands as if it were a `%...%` placeholder for a specific built-in variable:

- `***` → `%NAME:TARGET%`
- `+++` → `%CALLNAME:MASTER%`
- `===` → `%CALLNAME:PLAYER%`
- `///` → `%NAME:ASSI%`
- `$$$` → `%CALLNAME:TARGET%`

If `SystemIgnoreTripleSymbol` is `true`, these sequences are treated as literal characters (no expansion).

## 4) FORM escapes inside literal segments

In literal segments (outside `%...%` / `{...}` bodies), FORM treats backslash as an escape introducer:

- `\s` → half-width space (`' '`)
- `\S` → full-width space (`'　'`)
- `\t` → tab (`'\t'`)
- `\n` → newline character (`'\n'`)
- `\` followed immediately by a newline: consumes the newline and produces **no** output (line-continuation)
- `\@` → starts a FORM string-ternary subword (see §6) *unless* the current termination mode treats `\@` as an end marker (see §6.2)
- Any other `\X`:
  - the backslash is discarded
  - `X` is appended literally

Notes:

- This escape system is distinct from double-quoted string literal escapes inside `%...%` / `{...}` expression bodies.
- To include a literal `\@` in FORM output, write `\\@` (first `\\` becomes a literal backslash; then `@` is literal because it is not preceded by a backslash).

## 5) Width and alignment semantics

### 5.1 `%...%` width uses `useLanguage` byte-count adjustment

For `%operand,width%`, padding uses the following effective logic:

- Let `s = operand` (a .NET `string`)
- Let `byteLen = LangManager.GetStrlenLang(s)`:
  - if `s` is ASCII-only, this is `s.Length`
  - otherwise, this is the configured legacy code-page byte count (set by `useLanguage`)
- The engine adjusts the requested `width` by subtracting `(byteLen - s.Length)` before calling `.PadLeft/.PadRight`.

This is intended to approximate “display width in the configured legacy encoding” while still using .NET’s character-count-based padding.

### 5.2 `{...}` width pads by character count

`{...}` uses `.PadLeft/.PadRight` directly on the decimal string, with no `useLanguage` adjustment.

### 5.3 Alignment default and flags

Inside both `%...%` and `{...}`:

- Default is `RIGHT` (pad left).
- `LEFT` sets left alignment (pad right).
- `RIGHT` is accepted but is the default (it does not set the “left” flag).

## 6) `\@...\@` string-ternary subword

FORM recognizes a conditional string construct introduced by `\@`:

Conceptual syntax:

`\@ cond ? left [ # right ] \@`

This appears in two places:

- as a subword inside a larger FORM string (`AnalyseFormattedString` sees `\@` and inserts a `YenAtSubWord`)
- as a standalone token in expression lexing (the lexer emits a `StrFormWord` whose only subword is this `YenAtSubWord`)

### 6.1 Condition parsing (`cond`)

`cond` is lexed as an **integer expression token stream** until `?` at nesting depth 0.

The condition is required: an empty condition is a parse/compile error.

### 6.2 Branch parsing (`left` / `right`) and terminators

`left` and `right` are parsed as nested FORM strings, but with special termination rules:

- `left` is parsed until `#` **or** until the closing `\@` is encountered.
- `right` is parsed until the closing `\@` is encountered.

Trimming:

- `left` and `right` are parsed with `trim=true`, which removes only half-width spaces and tabs:
  - from the start of the first literal segment, and
  - from the end of the last literal segment.

If `#` is omitted:

- the engine emits a warning
- `right` is treated as an empty string

### 6.3 Semantics

Evaluation returns:

- `left` if `cond != 0`
- otherwise `right`

## 7) Termination modes and trimming (scanner-level rules)

The formatted-string analyzer is called with:

- an **end marker set** (what terminates scanning)
- a `trim` flag (whether to trim the first/last literal segments)

Termination always occurs on end-of-line (`'\n'`) or end-of-string.

Additional termination depends on the caller:

- `DoubleQuotation`: stop before `"` (used for `@"..."`
- `Comma`: stop before `,` (used for “FORM list” arguments)
- `Sharp`: stop before `#` (used for the `left` branch of `\@...\@`)
- `YenAt`: stop before the closing `\@` (implemented as: seeing `\@` causes termination and leaves the stream positioned at the `@`)
- `LeftParenthesis_Bracket_Comma_Semicolon`: stop before any of `(` `[` `,` `;` (used for FORM-parsed “function name” fields)

Trimming (`trim=true`) removes only `' '` and `'\t'` from the start/end edges as described in §6.2.
