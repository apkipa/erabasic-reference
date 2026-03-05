# EraBasic Built-ins Reference (Emuera / EvilMask)

Generated on `2026-03-05`.

This file is **user-facing**: it contains only human-written documentation overrides.
Undocumented built-ins are listed but contain only a `(TODO)` placeholder.

For engine-extracted skeletons, validation structures, and file/line references, see:
- `erabasic-reference/appendix/tooling/builtins-reference-engine.md` (writer/debug dump; not user-facing)

# Conventions used by this reference

Unless an entry explicitly says otherwise, interpret this reference using the conventions below.

## Evaluation order (default)

- Arguments are evaluated left-to-right.
- Each argument (and any subscripts inside it) is evaluated once.
- If an entry describes a different evaluation rule, that entry overrides this default.

## Optional arguments and defaults

- Whether an argument can be omitted is defined by an entry’s `Syntax` (instructions) or `Signatures` (methods).
- Optional arguments can be omitted by leaving an empty argument slot (e.g. `FUNC(a, , c)`); in that case the argument value is treated as “omitted” for the purpose of default substitution.
- Default values/behaviors for omitted arguments are documented inline under that entry’s `Arguments` (e.g. “optional, default `0`”).
- Omitted arguments are not the same as passing an empty string; if empty-string behavior matters for compatibility, the entry documents it explicitly.

## Output skipping / skipped execution

- Some instructions are skipped entirely when output skipping is active (e.g. `SKIPDISP` / skip-print mode).
- When an instruction is **skipped**, it is not executed: arguments are not evaluated and there are no side effects.
- Note: the engine may still parse/compile the line’s arguments before the skip check; skips only suppress execution-time evaluation and side effects.

## Range notation

- This reference avoids `a..b` range notation, because inclusive/exclusive bounds are easy to misread.
- Ranges are written using explicit inequalities (e.g. `0 <= i < n`) or half-open interval notation (e.g. `[startIndex, lastIndex)`).

## Terminology: errors vs rejection

- **Error**: the engine reports an error (typically aborting the current execution).
- **Reject** (input/choice contexts): the engine ignores the input and continues waiting; side effects such as `RESULT*` writes happen only as documented for the accepting path.

# Expression functions as statements

Some expression functions are also accepted as standalone statements (without `=` assignment).
In statement form, the engine evaluates the function and writes the return value to:
- `RESULT` for integer-returning functions
- `RESULTS` for string-returning functions

# Instructions

## SET (instruction)

**Summary**
- Describes **assignment statements** (`=`, `'=` and compound forms) and their observable behavior.
- Covers scalar assignment, compound assignment (`+=`, `-=`, etc.), `++/--`, and comma-list assignment into arrays.

**Tags**
- variables

**Syntax**
- Scalar assignment (int): `<intVarTerm> = <int expr>`
- Scalar assignment (string, formatted): `<strVarTerm> = <FORM string>` (subject to `SystemIgnoreStringSet`)
- Scalar assignment (string, expression): `<strVarTerm> '= <string expr>`
- Compound assignment (examples): `<intVarTerm> += <int expr>`, `<intVarTerm> <<= <int expr>`, `<strVarTerm> += <string expr>`, `<strVarTerm> *= <int expr>`
- Post-inc/dec: `<intVarTerm>++` / `<intVarTerm>--` (no RHS allowed)
- Pre-inc/dec: `++<intVarTerm>` / `--<intVarTerm>` (no RHS allowed)
- Comma-list assignment (int, only with `=`): `<intVarTerm> = v1, v2, v3, ...`
- Comma-list assignment (string, only with `'=`): `<strVarTerm> '= s1, s2, s3, ...`
- Compatibility quirk: `<varTerm> == <expr>` is accepted as assignment with a warning, and is treated as `<varTerm> = <expr>`.

**Arguments**
- LHS must be a **single variable term** (not an arbitrary expression), and must not be `CONST`.
- RHS is parsed in one of multiple modes depending on operator and LHS type:
  - int LHS: RHS is parsed as normal expressions.
  - string LHS with `=`: RHS is scanned as a formatted string until end-of-line.
  - string LHS with `'=` / `+=` / `*=`: RHS is parsed as normal expressions.

- Omitted arguments / defaults:
  - For `++/--`, the implicit delta is `+1` / `-1`.

**Semantics**
- There is no `SET` keyword in EraBasic source; this entry documents the language’s assignment syntax.
- Assignment operator recognition:
  - The engine recognizes: `=`, `'=`; `++`, `--`; and compound forms `+=`, `-=`, `*=`, `/=`, `%=`, `<<=`, `>>=`, `|=`, `&=`, `^=`.
- Allowed operators depend on LHS type:
  - int LHS: all the above operators are accepted by the assignment builder.
  - string LHS: only `=`, `'=` (string-expression assignment), `+=`, `*=` are accepted; other compound operators are rejected as invalid.
- If the RHS is a single value:
  - `=` assigns that value.
  - For compound assignment operators, the resulting value is the same as `LHS = (LHS <op> RHS)` (using the operator implied by the compound form).
- Index evaluation and side effects (important compatibility detail):
  - For `++`, `--`, `+= <const int>`, `-= <const int>`: the LHS variable term (including indices/subscripts) is evaluated once.
  - For other compound assignments: the LHS variable term is evaluated twice (once to read the old value, and once to write the new value), so any side effects in indices can run twice.
- If the RHS is a comma list:
  - This is only allowed for `=` on integer variables, and only allowed for `'=` on string variables.
  - Evaluates each element and writes a batch of consecutive elements starting at the LHS element (for multidimensional arrays, the list advances the last dimension only).
  - If any RHS element is omitted, it is an error.
- For string `=` assignment, the RHS is treated as FORM/formatted text (not a normal expression) and then compiled to a string expression internally.
  - After the operator, the parser skips **ASCII spaces only** (not tabs) before scanning the FORM string.

**Errors & validation**
- Parse-time errors:
  - If the line does not contain a recognized assignment operator, it becomes an invalid line at load/parse time.
- Errors if LHS cannot be read as a single variable term, if LHS is const, or if operator is incompatible with the LHS type.
- Errors if assigning string→int or int→string in contexts that disallow it.
- If `SystemIgnoreStringSet` is enabled, string `=` assignment is rejected (scripts must use `'=` or other operations).
  - Note: this check happens when the assignment line’s argument is parsed (by default: when the line is first reached at runtime).

**Examples**
- `A = 10`
- `A += 1`
- `A <<= 2`
- `++A`
- `S = "Hello, %NAME%!"`
- `S '= TOSTR(A)`
- `ARR:0 = 1, 2, 3, 4`

## PRINT (instruction)

**Summary**
- Prints a **raw literal string** (the remainder of the source line) into the console output buffer.
- This entry also documents **common PRINT-family semantics** (suffix letters, buffering, `K`/`D`, `C`/`LC`).

**Tags**
- io

**Syntax**
- `PRINT`
- `PRINT <raw text>`
- `PRINT;<raw text>`

**Arguments**
- `<raw text>` (optional, default `""`): raw text, not an expression.
- `<raw text>` is taken as the raw character sequence after the instruction delimiter.
- The parser consumes exactly one delimiter character after the keyword:
  - a single space / tab
  - or a full-width space if `SystemAllowFullSpace` is enabled
  - or a semicolon `;`
- Because only *one* delimiter character is consumed:
  - `PRINT X` prints `X` (the one space was consumed as delimiter).
  - `PRINT  X` prints `" X"` (the second space remains in the argument).
  - `PRINT;X` prints `X` (no leading whitespace in the argument).

**Semantics**
- Output is appended to the engine’s **print buffer** (it is not necessarily flushed to the UI immediately).
- If output skipping is active (`SKIPDISP`):
  - These instructions are skipped before execution by the interpreter.
  - Arguments are not evaluated and there are no side effects.
- Argument/evaluation modes by base variant (before suffix letters):
  - `PRINT*` (raw): uses the raw literal remainder-of-line (not an expression).
  - `PRINTS*`: evaluates one string expression.
  - `PRINTV*`: evaluates a comma-separated list of expressions; each element must be either integer or string; results are concatenated with no separator (left-to-right).
  - `PRINTFORM*`: parses its argument as a FORM/formatted string at load/parse time, then evaluates it at runtime.
  - `PRINTFORMS*`: evaluates one string expression to obtain a format-string source, then parses and evaluates it as a FORM string at runtime (see below).
- Suffix letters and their meaning (parser order is important):
  - `C` / `LC` (cell output): after building the output string, outputs a fixed-width cell:
    - `...C` uses right alignment, `...LC` uses left alignment.
    - This is **not** the same as the newline suffix `L`; for example, `PRINTLC` means “left-aligned cell”, not “PRINTL + C”.
    - Cell formatting rules are defined by the console implementation; see `PRINTC` / `PRINTLC`.
    - Cell variants do not use the `...L / ...W / ...N` newline/wait handling; they only append a cell to the buffer.
  - `K` (kana conversion): applies kana conversion as configured by `FORCEKANA`.
  - `D` (ignore SETCOLOR color): ignores `SETCOLOR`’s *color* for this output (font name/style still apply).
  - `L` (newline): after printing, flushes the current buffer and appends a newline.
  - `W` (wait): like `L`, then waits for a key.
  - `N` (wait without ending the logical line): prints without ending the logical line, then flushes and waits like `W`.
    - The *next* flushed output will be merged onto the same logical line.
- FORM-at-runtime behavior (`PRINTFORMS*`):
  - Evaluates the string expression to `src`.
  - Normalizes escapes (the same escape-handling used by FORM strings).
  - Parses `src` as a FORM string up to end-of-line, then evaluates it and prints the result.
- `PRINT` itself:
  - Uses the raw literal argument as the output string.
  - Treats the output as ending a logical line (even though it does not insert a newline by itself).

**Errors & validation**
- None for `PRINT` itself (argument is optional and not parsed as an expression).

**Examples**
- `PRINT Hello`
- `PRINT;Hello`
- `PRINT  (leading space is preserved)`

## PRINTL (instruction)

**Summary**
- `PRINTL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTL [<raw text>]`
- `PRINTL;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- After printing, flushes and appends a newline.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTL ...`

## PRINTW (instruction)

**Summary**
- `PRINTW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTW [<raw text>]`
- `PRINTW;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- After printing, flushes and appends a newline, then waits for a key.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTW ...`

## PRINTV (instruction)

**Summary**
- `PRINTV` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTV <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

- Omitted arguments / defaults:
  - None (missing arguments are an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTV ...`

## PRINTVL (instruction)

**Summary**
- `PRINTVL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTVL <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

- Omitted arguments / defaults:
  - None (missing arguments are an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- After printing, flushes and appends a newline.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTVL ...`

## PRINTVW (instruction)

**Summary**
- `PRINTVW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTVW <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

- Omitted arguments / defaults:
  - None (missing arguments are an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- After printing, flushes and appends a newline, then waits for a key.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTVW ...`

## PRINTS (instruction)

**Summary**
- `PRINTS` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTS <string expr>`

**Arguments**
- A single string expression (must be present).

- Omitted arguments / defaults:
  - None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTS ...`

## PRINTSL (instruction)

**Summary**
- `PRINTSL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTSL <string expr>`

**Arguments**
- A single string expression (must be present).

- Omitted arguments / defaults:
  - None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- After printing, flushes and appends a newline.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSL ...`

## PRINTSW (instruction)

**Summary**
- `PRINTSW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTSW <string expr>`

**Arguments**
- A single string expression (must be present).

- Omitted arguments / defaults:
  - None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- After printing, flushes and appends a newline, then waits for a key.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSW ...`

## PRINTFORM (instruction)

**Summary**
- `PRINTFORM` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORM [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORM ...`

## PRINTFORML (instruction)

**Summary**
- `PRINTFORML` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORML [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- After printing, flushes and appends a newline.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORML ...`

## PRINTFORMW (instruction)

**Summary**
- `PRINTFORMW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORMW [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- After printing, flushes and appends a newline, then waits for a key.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMW ...`

## PRINTFORMS (instruction)

**Summary**
- `PRINTFORMS` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORMS <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

- Omitted arguments / defaults:
  - None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMS ...`

## PRINTFORMSL (instruction)

**Summary**
- `PRINTFORMSL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORMSL <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

- Omitted arguments / defaults:
  - None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- After printing, flushes and appends a newline.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMSL ...`

## PRINTFORMSW (instruction)

**Summary**
- `PRINTFORMSW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORMSW <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

- Omitted arguments / defaults:
  - None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- After printing, flushes and appends a newline, then waits for a key.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMSW ...`

## PRINTK (instruction)

**Summary**
- `PRINTK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTK [<raw text>]`
- `PRINTK;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Applies kana conversion (`FORCEKANA` state) before printing.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTK ...`

## PRINTKL (instruction)

**Summary**
- `PRINTKL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTKL [<raw text>]`
- `PRINTKL;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Applies kana conversion (`FORCEKANA` state) before printing.
- After printing, flushes and appends a newline.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTKL ...`

## PRINTKW (instruction)

**Summary**
- `PRINTKW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTKW [<raw text>]`
- `PRINTKW;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Applies kana conversion (`FORCEKANA` state) before printing.
- After printing, flushes and appends a newline, then waits for a key.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTKW ...`

## PRINTVK (instruction)

**Summary**
- `PRINTVK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTVK <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

- Omitted arguments / defaults:
  - None (missing arguments are an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- Applies kana conversion (`FORCEKANA` state) before printing.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTVK ...`

## PRINTVKL (instruction)

**Summary**
- `PRINTVKL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTVKL <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

- Omitted arguments / defaults:
  - None (missing arguments are an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- Applies kana conversion (`FORCEKANA` state) before printing.
- After printing, flushes and appends a newline.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTVKL ...`

## PRINTVKW (instruction)

**Summary**
- `PRINTVKW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTVKW <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

- Omitted arguments / defaults:
  - None (missing arguments are an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- Applies kana conversion (`FORCEKANA` state) before printing.
- After printing, flushes and appends a newline, then waits for a key.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTVKW ...`

## PRINTSK (instruction)

**Summary**
- `PRINTSK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTSK <string expr>`

**Arguments**
- A single string expression (must be present).

- Omitted arguments / defaults:
  - None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- Applies kana conversion (`FORCEKANA` state) before printing.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSK ...`

## PRINTSKL (instruction)

**Summary**
- `PRINTSKL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTSKL <string expr>`

**Arguments**
- A single string expression (must be present).

- Omitted arguments / defaults:
  - None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- Applies kana conversion (`FORCEKANA` state) before printing.
- After printing, flushes and appends a newline.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSKL ...`

## PRINTSKW (instruction)

**Summary**
- `PRINTSKW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTSKW <string expr>`

**Arguments**
- A single string expression (must be present).

- Omitted arguments / defaults:
  - None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- Applies kana conversion (`FORCEKANA` state) before printing.
- After printing, flushes and appends a newline, then waits for a key.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSKW ...`

## PRINTFORMK (instruction)

**Summary**
- `PRINTFORMK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORMK [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Applies kana conversion (`FORCEKANA` state) before printing.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMK ...`

## PRINTFORMKL (instruction)

**Summary**
- `PRINTFORMKL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORMKL [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Applies kana conversion (`FORCEKANA` state) before printing.
- After printing, flushes and appends a newline.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMKL ...`

## PRINTFORMKW (instruction)

**Summary**
- `PRINTFORMKW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORMKW [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Applies kana conversion (`FORCEKANA` state) before printing.
- After printing, flushes and appends a newline, then waits for a key.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMKW ...`

## PRINTFORMSK (instruction)

**Summary**
- `PRINTFORMSK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORMSK <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

- Omitted arguments / defaults:
  - None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- Applies kana conversion (`FORCEKANA` state) before printing.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMSK ...`

## PRINTFORMSKL (instruction)

**Summary**
- `PRINTFORMSKL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORMSKL <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

- Omitted arguments / defaults:
  - None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- Applies kana conversion (`FORCEKANA` state) before printing.
- After printing, flushes and appends a newline.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMSKL ...`

## PRINTFORMSKW (instruction)

**Summary**
- `PRINTFORMSKW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORMSKW <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

- Omitted arguments / defaults:
  - None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- Applies kana conversion (`FORCEKANA` state) before printing.
- After printing, flushes and appends a newline, then waits for a key.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMSKW ...`

## PRINTD (instruction)

**Summary**
- `PRINTD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTD [<raw text>]`
- `PRINTD;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTD ...`

## PRINTDL (instruction)

**Summary**
- `PRINTDL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTDL [<raw text>]`
- `PRINTDL;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- After printing, flushes and appends a newline.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTDL ...`

## PRINTDW (instruction)

**Summary**
- `PRINTDW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTDW [<raw text>]`
- `PRINTDW;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- After printing, flushes and appends a newline, then waits for a key.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTDW ...`

## PRINTVD (instruction)

**Summary**
- `PRINTVD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTVD <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

- Omitted arguments / defaults:
  - None (missing arguments are an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTVD ...`

## PRINTVDL (instruction)

**Summary**
- `PRINTVDL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTVDL <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

- Omitted arguments / defaults:
  - None (missing arguments are an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- After printing, flushes and appends a newline.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTVDL ...`

## PRINTVDW (instruction)

**Summary**
- `PRINTVDW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTVDW <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

- Omitted arguments / defaults:
  - None (missing arguments are an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- After printing, flushes and appends a newline, then waits for a key.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTVDW ...`

## PRINTSD (instruction)

**Summary**
- `PRINTSD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTSD <string expr>`

**Arguments**
- A single string expression (must be present).

- Omitted arguments / defaults:
  - None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSD ...`

## PRINTSDL (instruction)

**Summary**
- `PRINTSDL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTSDL <string expr>`

**Arguments**
- A single string expression (must be present).

- Omitted arguments / defaults:
  - None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- After printing, flushes and appends a newline.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSDL ...`

## PRINTSDW (instruction)

**Summary**
- `PRINTSDW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTSDW <string expr>`

**Arguments**
- A single string expression (must be present).

- Omitted arguments / defaults:
  - None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- After printing, flushes and appends a newline, then waits for a key.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSDW ...`

## PRINTFORMD (instruction)

**Summary**
- `PRINTFORMD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORMD [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMD ...`

## PRINTFORMDL (instruction)

**Summary**
- `PRINTFORMDL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORMDL [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- After printing, flushes and appends a newline.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMDL ...`

## PRINTFORMDW (instruction)

**Summary**
- `PRINTFORMDW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORMDW [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- After printing, flushes and appends a newline, then waits for a key.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMDW ...`

## PRINTFORMSD (instruction)

**Summary**
- `PRINTFORMSD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORMSD <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

- Omitted arguments / defaults:
  - None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMSD ...`

## PRINTFORMSDL (instruction)

**Summary**
- `PRINTFORMSDL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORMSDL <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

- Omitted arguments / defaults:
  - None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- After printing, flushes and appends a newline.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMSDL ...`

## PRINTFORMSDW (instruction)

**Summary**
- `PRINTFORMSDW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORMSDW <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

- Omitted arguments / defaults:
  - None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- After printing, flushes and appends a newline, then waits for a key.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMSDW ...`

## PRINTSINGLE (instruction)

**Summary**
- `PRINTSINGLE` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTSINGLE [<raw text>]`
- `PRINTSINGLE;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).

- Omitted arguments / defaults:
  - Omitted argument is treated as the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLE ...`

## PRINTSINGLEV (instruction)

**Summary**
- `PRINTSINGLEV` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTSINGLEV <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

- Omitted arguments / defaults:
  - None (missing arguments are an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLEV ...`

## PRINTSINGLES (instruction)

**Summary**
- `PRINTSINGLES` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTSINGLES <string expr>`

**Arguments**
- A single string expression (must be present).

- Omitted arguments / defaults:
  - None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLES ...`

## PRINTSINGLEFORM (instruction)

**Summary**
- `PRINTSINGLEFORM` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTSINGLEFORM [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

- Omitted arguments / defaults:
  - Omitted argument is treated as the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLEFORM ...`

## PRINTSINGLEFORMS (instruction)

**Summary**
- `PRINTSINGLEFORMS` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTSINGLEFORMS <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

- Omitted arguments / defaults:
  - None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLEFORMS ...`

## PRINTSINGLEK (instruction)

**Summary**
- `PRINTSINGLEK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTSINGLEK [<raw text>]`
- `PRINTSINGLEK;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).

- Omitted arguments / defaults:
  - Omitted argument is treated as the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.
- Applies kana conversion (`FORCEKANA` state) before printing.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLEK ...`

## PRINTSINGLEVK (instruction)

**Summary**
- `PRINTSINGLEVK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTSINGLEVK <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

- Omitted arguments / defaults:
  - None (missing arguments are an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.
- Applies kana conversion (`FORCEKANA` state) before printing.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLEVK ...`

## PRINTSINGLESK (instruction)

**Summary**
- `PRINTSINGLESK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTSINGLESK <string expr>`

**Arguments**
- A single string expression (must be present).

- Omitted arguments / defaults:
  - None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.
- Applies kana conversion (`FORCEKANA` state) before printing.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLESK ...`

## PRINTSINGLEFORMK (instruction)

**Summary**
- `PRINTSINGLEFORMK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTSINGLEFORMK [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

- Omitted arguments / defaults:
  - Omitted argument is treated as the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.
- Applies kana conversion (`FORCEKANA` state) before printing.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLEFORMK ...`

## PRINTSINGLEFORMSK (instruction)

**Summary**
- `PRINTSINGLEFORMSK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTSINGLEFORMSK <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

- Omitted arguments / defaults:
  - None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.
- Applies kana conversion (`FORCEKANA` state) before printing.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLEFORMSK ...`

## PRINTSINGLED (instruction)

**Summary**
- `PRINTSINGLED` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTSINGLED [<raw text>]`
- `PRINTSINGLED;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).

- Omitted arguments / defaults:
  - Omitted argument is treated as the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLED ...`

## PRINTSINGLEVD (instruction)

**Summary**
- `PRINTSINGLEVD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTSINGLEVD <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

- Omitted arguments / defaults:
  - None (missing arguments are an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLEVD ...`

## PRINTSINGLESD (instruction)

**Summary**
- `PRINTSINGLESD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTSINGLESD <string expr>`

**Arguments**
- A single string expression (must be present).

- Omitted arguments / defaults:
  - None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLESD ...`

## PRINTSINGLEFORMD (instruction)

**Summary**
- `PRINTSINGLEFORMD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTSINGLEFORMD [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

- Omitted arguments / defaults:
  - Omitted argument is treated as the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLEFORMD ...`

## PRINTSINGLEFORMSD (instruction)

**Summary**
- `PRINTSINGLEFORMSD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTSINGLEFORMSD <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

- Omitted arguments / defaults:
  - None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLEFORMSD ...`

## PRINTC (instruction)

**Summary**
- `PRINTC` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTC [<raw text>]`
- `PRINTC;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).
- Output is converted to a fixed-width “cell” string (see below).

- Omitted arguments / defaults:
  - Omitted argument is treated as the empty string, and therefore produces no output.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Writes one fixed-width cell; does not append a newline and does not flush immediately.
- Cell formatting (right-aligned cell; observable behavior):
  - Measures string length in **Shift-JIS byte count** (hardcoded; code page 932).
  - Let `n = PrintCLength`.
  - Computes a target pixel width by measuring `n` spaces using the default font.
  - Creates a font using the current text style (font name + style) and the default font size for measurement/rendering.
    - If font creation fails, returns `str` unchanged.
  - If `len < n`, left-pads spaces to reach exactly `n` bytes.
  - It then measures the padded string’s pixel width using the created font; while the width is greater than the target width and the first character is a space, it removes one leading space and re-measures.
  - If `len >= n`, it does not add padding and does not truncate (overlong strings are kept as-is).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTC ...`

## PRINTLC (instruction)

**Summary**
- `PRINTLC` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTLC [<raw text>]`
- `PRINTLC;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).
- Output is converted to a fixed-width “cell” string (see below).

- Omitted arguments / defaults:
  - Omitted argument is treated as the empty string, and therefore produces no output.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Writes one fixed-width cell; does not append a newline and does not flush immediately.
- Cell formatting (left-aligned cell; observable behavior):
  - Measures string length in **Shift-JIS byte count** (hardcoded; code page 932).
  - Let `n = PrintCLength`.
  - Computes a target pixel width by measuring `n` spaces using the default font.
  - Creates a font using the current text style (font name + style) and the default font size for measurement/rendering.
    - If font creation fails, returns `str` unchanged.
  - If `len < n + 1`, right-pads spaces to reach exactly `n + 1` bytes.
  - It then measures the padded string’s pixel width using the created font; while the width is greater than the target width and the last character is a space, it removes one trailing space and re-measures.
  - If `len >= n + 1`, it does not add padding and does not truncate (overlong strings are kept as-is).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTLC ...`

## PRINTFORMC (instruction)

**Summary**
- `PRINTFORMC` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORMC [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).
- Output is padded/truncated to a fixed-width cell (`PrintCLength`) using Shift-JIS byte count.

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMC ...`

## PRINTFORMLC (instruction)

**Summary**
- `PRINTFORMLC` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORMLC [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).
- Output is padded/truncated to a fixed-width cell (`PrintCLength`) using Shift-JIS byte count.

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMLC ...`

## PRINTCK (instruction)

**Summary**
- `PRINTCK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTCK [<raw text>]`
- `PRINTCK;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).
- Output is padded/truncated to a fixed-width cell (`PrintCLength`) using Shift-JIS byte count.

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns.
- Applies kana conversion (`FORCEKANA` state) before writing the cell.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTCK ...`

## PRINTLCK (instruction)

**Summary**
- `PRINTLCK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTLCK [<raw text>]`
- `PRINTLCK;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).
- Output is padded/truncated to a fixed-width cell (`PrintCLength`) using Shift-JIS byte count.

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns.
- Applies kana conversion (`FORCEKANA` state) before writing the cell.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTLCK ...`

## PRINTFORMCK (instruction)

**Summary**
- `PRINTFORMCK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORMCK [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).
- Output is padded/truncated to a fixed-width cell (`PrintCLength`) using Shift-JIS byte count.

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns.
- Applies kana conversion (`FORCEKANA` state) before writing the cell.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMCK ...`

## PRINTFORMLCK (instruction)

**Summary**
- `PRINTFORMLCK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORMLCK [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).
- Output is padded/truncated to a fixed-width cell (`PrintCLength`) using Shift-JIS byte count.

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns.
- Applies kana conversion (`FORCEKANA` state) before writing the cell.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMLCK ...`

## PRINTCD (instruction)

**Summary**
- `PRINTCD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTCD [<raw text>]`
- `PRINTCD;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).
- Output is padded/truncated to a fixed-width cell (`PrintCLength`) using Shift-JIS byte count.

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTCD ...`

## PRINTLCD (instruction)

**Summary**
- `PRINTLCD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTLCD [<raw text>]`
- `PRINTLCD;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).
- Output is padded/truncated to a fixed-width cell (`PrintCLength`) using Shift-JIS byte count.

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTLCD ...`

## PRINTFORMCD (instruction)

**Summary**
- `PRINTFORMCD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORMCD [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).
- Output is padded/truncated to a fixed-width cell (`PrintCLength`) using Shift-JIS byte count.

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMCD ...`

## PRINTFORMLCD (instruction)

**Summary**
- `PRINTFORMLCD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORMLCD [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).
- Output is padded/truncated to a fixed-width cell (`PrintCLength`) using Shift-JIS byte count.

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMLCD ...`

## PRINTDATA (instruction)

**Summary**
- Begins a **PRINTDATA block** that contains `DATA` / `DATAFORM` (and optional `DATALIST` groups).
- At runtime, the engine picks one choice uniformly at random, prints it, then jumps to `ENDDATA`.

**Tags**
- io
- data-blocks

**Syntax**
- `PRINTDATA [<intVarTerm>]`
- Block form:
  - `PRINTDATA [<intVarTerm>]`
    - `DATA <raw text>` / `DATAFORM <FORM string>` (one or more choices)
    - optionally, `DATALIST` ... `ENDLIST` groups to make a multi-line choice
  - `ENDDATA`

**Arguments**
- Optional `<intVarTerm>`: a changeable int variable term that receives the 0-based chosen index.

- Omitted arguments / defaults:
  - If `<intVarTerm>` is omitted, the chosen index is not stored anywhere.

**Semantics**
- Load-time structure rules (enforced by the loader):
  - `PRINTDATA*` must be closed by a matching `ENDDATA`.
  - `DATA` / `DATAFORM` must appear inside `PRINTDATA*`, `STRDATA`, or inside a `DATALIST` that is itself inside one of those blocks.
  - Nested `PRINTDATA*` blocks are a load-time error (the line is marked as error).
  - `STRDATA` cannot be nested inside `PRINTDATA*` and vice versa (load-time error).
  - The block body only permits `DATA` / `DATAFORM` / `DATALIST` / `ENDLIST` / `ENDDATA`; any other instruction (and any label definition) inside is a load-time error.
- Runtime behavior:
  - If output skipping is active (via `SKIPDISP`), `PRINTDATA*` is skipped entirely (no selection, no assignment to `<intVarTerm>`, and no jump to `ENDDATA`), so control flows through the block lines normally.
  - If there are no `DATA` choices, nothing is printed and the engine jumps to `ENDDATA`.
  - Otherwise:
    - Choose `choice` uniformly such that `0 <= choice < count` (using the engine RNG).
    - If `<intVarTerm>` is present, assign it the chosen index.
    - Print the selected `DATA` entry:
      - A single `DATA`/`DATAFORM` line prints as one line.
      - A `DATALIST` entry prints each contained `DATA`/`DATAFORM` line separated by newlines.
    - If the keyword has `...L`/`...W` behavior, append a newline (and optionally wait for a key).
    - Jump to the `ENDDATA` line, skipping over the block body.

**Errors & validation**
- Load-time structure errors (the line is marked as error) are produced for missing `ENDDATA`, `DATA` outside a block, `ENDLIST` without `DATALIST`, invalid instructions inside the block, etc.
- Non-fatal loader warnings also exist (e.g. empty choice lists), but the block still loads.
- The optional `<intVarTerm>` must be a changeable int variable term.

**Examples**
```erabasic
PRINTDATA CHOICE
  DATA First option
  DATA Second option
ENDDATA
```

```erabasic
PRINTDATA
  DATALIST
    DATA Line 1
    DATAFORM Line 2: %TOSTR(RAND:100)%
  ENDLIST
ENDDATA
```

## PRINTDATAL (instruction)

**Summary**
- `PRINTDATAL` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Tags**
- io
- data-blocks

**Syntax**
- `PRINTDATAL [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

- Omitted arguments / defaults:
  - Same as `PRINTDATA`.

**Semantics**
- Same as `PRINTDATA`, with these differences:
  - (No kana conversion flag.)
  - (Honors `SETCOLOR` color.)
  - Appends a newline after printing (`...L`).
  - (No automatic wait suffix.)

**Errors & validation**
- Same as `PRINTDATA`.

**Examples**
- `PRINTDATAL CHOICE` ... `ENDDATA`

## PRINTDATAW (instruction)

**Summary**
- `PRINTDATAW` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Tags**
- io
- data-blocks

**Syntax**
- `PRINTDATAW [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

- Omitted arguments / defaults:
  - Same as `PRINTDATA`.

**Semantics**
- Same as `PRINTDATA`, with these differences:
  - (No kana conversion flag.)
  - (Honors `SETCOLOR` color.)
  - (No automatic newline suffix.)
  - Appends a newline and waits for a key (`...W`).

**Errors & validation**
- Same as `PRINTDATA`.

**Examples**
- `PRINTDATAW CHOICE` ... `ENDDATA`

## PRINTDATAK (instruction)

**Summary**
- `PRINTDATAK` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Tags**
- io
- data-blocks

**Syntax**
- `PRINTDATAK [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

- Omitted arguments / defaults:
  - Same as `PRINTDATA`.

**Semantics**
- Same as `PRINTDATA`, with these differences:
  - Applies kana conversion (`...K`) before printing.
  - (Honors `SETCOLOR` color.)
  - (No automatic newline suffix.)
  - (No automatic wait suffix.)

**Errors & validation**
- Same as `PRINTDATA`.

**Examples**
- `PRINTDATAK CHOICE` ... `ENDDATA`

## PRINTDATAKL (instruction)

**Summary**
- `PRINTDATAKL` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Tags**
- io
- data-blocks

**Syntax**
- `PRINTDATAKL [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

- Omitted arguments / defaults:
  - Same as `PRINTDATA`.

**Semantics**
- Same as `PRINTDATA`, with these differences:
  - Applies kana conversion (`...K`) before printing.
  - (Honors `SETCOLOR` color.)
  - Appends a newline after printing (`...L`).
  - (No automatic wait suffix.)

**Errors & validation**
- Same as `PRINTDATA`.

**Examples**
- `PRINTDATAKL CHOICE` ... `ENDDATA`

## PRINTDATAKW (instruction)

**Summary**
- `PRINTDATAKW` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Tags**
- io
- data-blocks

**Syntax**
- `PRINTDATAKW [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

- Omitted arguments / defaults:
  - Same as `PRINTDATA`.

**Semantics**
- Same as `PRINTDATA`, with these differences:
  - Applies kana conversion (`...K`) before printing.
  - (Honors `SETCOLOR` color.)
  - (No automatic newline suffix.)
  - Appends a newline and waits for a key (`...W`).

**Errors & validation**
- Same as `PRINTDATA`.

**Examples**
- `PRINTDATAKW CHOICE` ... `ENDDATA`

## PRINTDATAD (instruction)

**Summary**
- `PRINTDATAD` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Tags**
- io
- data-blocks

**Syntax**
- `PRINTDATAD [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

- Omitted arguments / defaults:
  - Same as `PRINTDATA`.

**Semantics**
- Same as `PRINTDATA`, with these differences:
  - (No kana conversion flag.)
  - Ignores `SETCOLOR`’s color (`...D`) for this output.
  - (No automatic newline suffix.)
  - (No automatic wait suffix.)

**Errors & validation**
- Same as `PRINTDATA`.

**Examples**
- `PRINTDATAD CHOICE` ... `ENDDATA`

## PRINTDATADL (instruction)

**Summary**
- `PRINTDATADL` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Tags**
- io
- data-blocks

**Syntax**
- `PRINTDATADL [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

- Omitted arguments / defaults:
  - Same as `PRINTDATA`.

**Semantics**
- Same as `PRINTDATA`, with these differences:
  - (No kana conversion flag.)
  - Ignores `SETCOLOR`’s color (`...D`) for this output.
  - Appends a newline after printing (`...L`).
  - (No automatic wait suffix.)

**Errors & validation**
- Same as `PRINTDATA`.

**Examples**
- `PRINTDATADL CHOICE` ... `ENDDATA`

## PRINTDATADW (instruction)

**Summary**
- `PRINTDATADW` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Tags**
- io
- data-blocks

**Syntax**
- `PRINTDATADW [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

- Omitted arguments / defaults:
  - Same as `PRINTDATA`.

**Semantics**
- Same as `PRINTDATA`, with these differences:
  - (No kana conversion flag.)
  - Ignores `SETCOLOR`’s color (`...D`) for this output.
  - (No automatic newline suffix.)
  - Appends a newline and waits for a key (`...W`).

**Errors & validation**
- Same as `PRINTDATA`.

**Examples**
- `PRINTDATADW CHOICE` ... `ENDDATA`

## PRINTBUTTON (instruction)

**Summary**
- Prints a clickable button with a script-provided input value.
- Unlike automatic button conversion (e.g. `[0] ...` inside normal `PRINT` output), this instruction forces the output segment to be a button.

**Tags**
- io

**Syntax**
- `PRINTBUTTON <text>, <buttonValue>`

**Arguments**
- `<text>`: string expression (button label).
- `<buttonValue>`: expression whose runtime type is either:
  - integer (button produces that integer as input), or
  - string (button produces that string as input; useful with `INPUTS`).

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output).
- Uses the current text style for output (and honors `SETCOLOR` color).
- Evaluates `<text>` to a string, then removes any newline characters (`'\n'`) from it.
- If the resulting label is empty, this instruction produces no output segment (no button is created).
- Appends one button segment to the print buffer:
  - If `<buttonValue>` is an integer, the button produces that integer when clicked.
  - If `<buttonValue>` is a string, the button produces that string when clicked.
- This instruction does **not** add a newline and does not flush by itself (it behaves like other non-`...L` print-family commands).

**Errors & validation**
- Argument type/count errors follow the normal expression argument rules.

**Examples**
```erabasic
PRINTS "Are you sure? "
PRINTBUTTON "[0] Yes", 0
PRINTS "  "
PRINTBUTTON "[1] No", 1
INPUT
```

```erabasic
PRINTL Enter your name:
PRINTBUTTON "[Alice]", "Alice"
PRINTBUTTON " [Bob]", "Bob"
INPUTS
```

## PRINTBUTTONC (instruction)

**Summary**
- Like `PRINTBUTTON`, but formats the label as a fixed-width `PRINTC`-style cell aligned to the right.

**Tags**
- io

**Syntax**
- `PRINTBUTTONC <text>, <buttonValue>`

**Arguments**
- Same as `PRINTBUTTON`.

**Semantics**
- Same as `PRINTBUTTON`, with these differences:
  - The label still has all `'\n'` characters removed (same as `PRINTBUTTON`).
  - Before creating the button segment, the label is formatted as a `PRINTC`-style fixed-width cell, aligned to the right (same cell formatting rules as `PRINTC`).

**Errors & validation**
- Same as `PRINTBUTTON`.

**Examples**
```erabasic
PRINTBUTTONC "[0] OK", 0
PRINTBUTTONC "[1] Cancel", 1
INPUT
```

## PRINTBUTTONLC (instruction)

**Summary**
- Like `PRINTBUTTON`, but formats the label as a fixed-width `PRINTC`-style cell aligned to the left.

**Tags**
- io

**Syntax**
- `PRINTBUTTONLC <text>, <buttonValue>`

**Arguments**
- Same as `PRINTBUTTON`.

**Semantics**
- Same as `PRINTBUTTONC`, except the label cell is aligned to the left:
  - Uses the same fixed-width cell formatting rules as `PRINTLC`.

**Errors & validation**
- Same as `PRINTBUTTON`.

**Examples**
```erabasic
PRINTBUTTONLC "[0] OK", 0
PRINTBUTTONLC "[1] Cancel", 1
INPUT
```

## PRINTPLAIN (instruction)

**Summary**
- Outputs a raw string argument as plain text, without automatic button conversion.

**Tags**
- io

**Syntax**
- `PRINTPLAIN`
- `PRINTPLAIN <raw text>`

**Arguments**
- `<raw text>`: the literal remainder of the line (not a string expression).

- Omitted arguments / defaults:
  - If omitted, the argument is treated as the empty string; empty output produces no output segment.

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output).
- Appends the raw string to the print buffer as a “plain” segment:
  - It is **not** scanned for numeric button patterns like `[0]`.
  - It still uses the current style (`SETCOLOR`, font style, etc.).
- Does not add a newline and does not flush by itself.

**Errors & validation**
- None.

**Examples**
```erabasic
; This will NOT become a clickable button:
PRINTPLAIN [0] Save
PRINTL
```

## PRINTPLAINFORM (instruction)

**Summary**
- Like `PRINTPLAIN`, but reads its argument as a FORM/formatted string.

**Tags**
- io

**Syntax**
- `PRINTPLAINFORM`
- `PRINTPLAINFORM <FORM string>`

**Arguments**
- `<FORM string>`: a FORM argument scanned by the FORM analyzer (supports `%...%` and `{...}` placeholders).

- Omitted arguments / defaults:
  - If omitted, the argument is treated as the empty string; empty output produces no output segment.

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output).
- Evaluates the FORM argument to a string, then appends it as a “plain” segment (no automatic button conversion).
- Does not add a newline and does not flush by itself.

**Errors & validation**
- FORM parsing errors follow the engine’s normal FORM rules.

**Examples**
```erabasic
PRINTPLAINFORM HP: {HP}/{MAXHP}  [0] Not a button
PRINTL
```

## PRINT_ABL (instruction)

**Summary**
- Prints a one-line summary of a character’s non-zero abilities (`ABL`), then ends the line.

**Tags**
- io
- characters

**Syntax**
- `PRINT_ABL`
- `PRINT_ABL <charaIndex>`

**Arguments**
- `charaIndex` (optional, int; default `0` with a warning if omitted): index into the current character list.

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output).
- Validates `charaIndex` at runtime; out-of-range raises an error.
- Builds a summary string `s` as follows:
  - Let `abl[]` be the target character’s `ABL` 1D array.
  - Let `names[]` be the constant CSV name list `ABLNAME`.
  - For `i` such that `0 <= i < abl.Length`:
    - If `i >= names.Length`: stop the loop (`break`).
    - If `abl[i] == 0`: continue.
    - If `names[i]` is null/empty: continue (engine uses `string.IsNullOrEmpty`).
    - Append: `names[i] + "LV" + abl[i] + " "` (note the trailing space).
  - `s` is the concatenation of all appended parts; it may be the empty string.
- Prints `s`, then ends the line.
  - If `s` is empty, this still outputs a blank line.

**Errors & validation**
- Runtime error if `charaIndex` is out of range (`charaIndex < 0` or `charaIndex >= CHARANUM`).

**Examples**
```erabasic
PRINT_ABL TARGET
```

## PRINT_TALENT (instruction)

**Summary**
- Prints a one-line summary of a character’s enabled talents (`TALENT`), then ends the line.

**Tags**
- io
- characters

**Syntax**
- `PRINT_TALENT`
- `PRINT_TALENT <charaIndex>`

**Arguments**
- `charaIndex` (optional, int; default `0` with a warning if omitted): index into the current character list.

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output).
- Validates `charaIndex` at runtime; out-of-range raises an error.
- Builds a summary string `s` as follows:
  - Let `talent[]` be the target character’s `TALENT` 1D array.
  - Let `names[]` be the constant CSV name list `TALENTNAME`.
  - For `i` such that `0 <= i < talent.Length`:
    - If `i >= names.Length`: stop the loop (`break`).
    - If `talent[i] == 0`: continue.
    - If `names[i]` is null/empty: continue (engine uses `string.IsNullOrEmpty`).
    - Append: `"[" + names[i] + "]"` (no spaces are added by the engine).
  - `s` is the concatenation of all appended parts; it may be the empty string.
- Prints `s`, then ends the line.
  - If `s` is empty, this still outputs a blank line.

**Errors & validation**
- Runtime error if `charaIndex` is out of range.

**Examples**
```erabasic
PRINT_TALENT TARGET
```

## PRINT_MARK (instruction)

**Summary**
- Prints a one-line summary of a character’s non-zero marks (`MARK`), then ends the line.

**Tags**
- io
- characters

**Syntax**
- `PRINT_MARK`
- `PRINT_MARK <charaIndex>`

**Arguments**
- `charaIndex` (optional, int; default `0` with a warning if omitted): index into the current character list.

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output).
- Validates `charaIndex` at runtime; out-of-range raises an error.
- Builds a summary string `s` as follows:
  - Let `mark[]` be the target character’s `MARK` 1D array.
  - Let `names[]` be the constant CSV name list `MARKNAME`.
  - For `i` such that `0 <= i < mark.Length`:
    - If `i >= names.Length`: stop the loop (`break`).
    - If `mark[i] == 0`: continue.
    - If `names[i]` is null/empty: continue (engine uses `string.IsNullOrEmpty`).
    - Append: `names[i] + "LV" + mark[i] + " "` (note the trailing space).
  - `s` is the concatenation of all appended parts; it may be the empty string.
- Prints `s`, then ends the line.
  - If `s` is empty, this still outputs a blank line.

**Errors & validation**
- Runtime error if `charaIndex` is out of range.

**Examples**
```erabasic
PRINT_MARK TARGET
```

## PRINT_EXP (instruction)

**Summary**
- Prints a one-line summary of a character’s non-zero experiences (`EXP`), then ends the line.

**Tags**
- io
- characters

**Syntax**
- `PRINT_EXP`
- `PRINT_EXP <charaIndex>`

**Arguments**
- `charaIndex` (optional, int; default `0` with a warning if omitted): index into the current character list.

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output).
- Validates `charaIndex` at runtime; out-of-range raises an error.
- Builds a summary string `s` as follows:
  - Let `exp[]` be the target character’s `EXP` 1D array.
  - Let `names[]` be the constant CSV name list `EXPNAME`.
  - For `i` such that `0 <= i < exp.Length`:
    - If `i >= names.Length`: stop the loop (`break`).
    - If `exp[i] == 0`: continue.
    - If `names[i]` is null/empty: continue (engine uses `string.IsNullOrEmpty`).
    - Append: `names[i] + exp[i] + " "` (note the trailing space).
  - `s` is the concatenation of all appended parts; it may be the empty string.
- Prints `s`, then ends the line.
  - If `s` is empty, this still outputs a blank line.

**Errors & validation**
- Runtime error if `charaIndex` is out of range.

**Examples**
```erabasic
PRINT_EXP TARGET
```

## PRINT_PALAM (instruction)

**Summary**
- Prints a multi-column view of a character’s parameters (`PALAM`) using `PRINTC`-style cells.

**Tags**
- io
- characters

**Syntax**
- `PRINT_PALAM`
- `PRINT_PALAM <charaIndex>`

**Arguments**
- `charaIndex` (optional, int; default `0` with a warning if omitted): index into the current character list.

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output).
- Validates `charaIndex` at runtime; out-of-range raises an error.
- For each parameter code `i` such that `0 <= i < 100`, it computes a cell string `s` and prints it if present:
  - Let `param = PALAM[charaIndex, i]`.
  - Let `name = PALAMNAME[i]` (treat `null` as `""`).
  - If `param == 0` and `name == ""`: omit this cell (no output).
  - Otherwise:
    - Let `paramlv = PALAMLV` (global array).
    - Choose the bar fill character `c` and its threshold `border`:
      - Start with `c = '-'` and `border = paramlv[1]`.
      - If `param >= border`: set `c = '='`, `border = paramlv[2]`.
      - If `param >= border`: set `c = '>'`, `border = paramlv[3]`.
      - If `param >= border`: set `c = '*'`, `border = paramlv[4]`.
    - Build a 10-character bar string `bar`:
      - If `border <= 0` or `border <= param`: bar fill is 10 copies of `c`.
      - Else if `param <= 0`: bar fill is 10 copies of `'.'`.
      - Else:
        - Compute `filled = floor(param * 10 / border)` using integer division (integer overflow wraps).
        - Bar fill is `filled` copies of `c` followed by `10 - filled` copies of `'.'`.
    - Build the final cell string:
      - `name + "[" + barFill + "]" + paramText`
      - where `paramText` is `param` formatted as a decimal integer right-aligned in width 6 (equivalent to C# interpolated `{param,6}` under `CultureInfo.InvariantCulture`).
- Each produced cell string is printed via `PRINTC`-style output with right alignment.
- Keeps a per-line cell counter:
  - After each printed cell, `count += 1`.
  - If `PrintCPerLine > 0` and `count % PrintCPerLine == 0`, it flushes pending output.
- After finishing the loop, it flushes pending output and refreshes the display.
- This instruction does not automatically append a trailing newline.

**Errors & validation**
- Runtime error if `charaIndex` is out of range.

**Examples**
```erabasic
PRINT_PALAM TARGET
```

## PRINT_ITEM (instruction)

**Summary**
- Prints a one-line summary of currently owned items (`ITEM`), then ends the line.

**Tags**
- io

**Syntax**
- `PRINT_ITEM`

**Arguments**
- None.

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output).
- Builds a Japanese summary string `s` as follows:
  - Let `count[]` be the integer array `ITEM`.
  - Let `names[]` be the string array `ITEMNAME`.
  - Let `length = min(count.Length, names.Length)`.
  - Start with `s = "所持アイテム："`.
  - For each `i` such that `0 <= i < length`:
    - If `count[i] == 0`: continue.
    - If `names[i] != null`: append `names[i]` (note: unlike some other lists, empty string is not filtered out here).
    - Append: `"(" + count[i] + ") "` (note the trailing space).
  - If no `i` satisfied `count[i] != 0`, append `"なし"`.
- Prints `s`, then ends the line.

**Errors & validation**
- None specific to this instruction.

**Examples**
- `PRINT_ITEM`

## PRINT_SHOPITEM (instruction)

**Summary**
- Prints a grid of items currently for sale in the shop (based on `ITEMSALES`), including their indices and prices.

**Tags**
- io

**Syntax**
- `PRINT_SHOPITEM`

**Arguments**
- None.

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output).
- Let:
  - `sales = ITEMSALES` (numeric array)
  - `names = ITEMNAME` (CSV name list; string array)
  - `prices = ITEMPRICE` (numeric array)
- Iterates `i` such that `0 <= i < length`, where:
  - `length = min(sales.Length, names.Length)`, then
  - if `length > prices.Length`, `length = prices.Length`.
- An item is considered “for sale” iff:
  - `sales[i] != 0`, and
  - `names[i] != null`.
- For each `i` that is for sale:
  - Let `name = names[i]` (engine also guards against null by treating it as `""`, but the sale predicate rejects null names).
  - Let `price = prices[i]`.
  - Format the cell text as:
    - If `MoneyFirst` is true: `[{i}] {name}({MoneyLabel}{price})`
    - Otherwise: `[{i}] {name}({price}{MoneyLabel})`
  - Prints the cell using `PRINTC`-style formatting with left alignment.
  - Increments a per-line cell counter and flushes every `PrintCPerLine` cells when `PrintCPerLine > 0`.
- After finishing the loop, it flushes pending output and refreshes the display.
- This instruction does not automatically append a trailing newline.

**Errors & validation**
- None specific to this instruction.

**Examples**
- `PRINT_SHOPITEM`

## DRAWLINE (instruction)

**Summary**
- Draws a horizontal line across the console using the configured `DRAWLINE` pattern.

**Tags**
- io

**Syntax**
- `DRAWLINE`

**Arguments**
- None.

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output).
- The engine prints a precomputed “draw line” string and then ends the line.
- Pattern source:
  - The base pattern comes from config `DrawLineString` (default `"-"`).
- The engine precomputes an expanded line string from `DrawLineString` on initialization.
- Expansion algorithm:
  - Uses the UI’s drawable width (in pixels) as the target, and measures display width using the default font metrics.
  - Builds a string by repeating the pattern string until its measured display width is at least the target width.
  - Then trims one character at a time from the end until the measured width is at most the target width.
  - Returns the resulting string.
- Rendering:
  - The line is printed using regular style regardless of the current font style.
  - The engine then ends the line (flushes the buffer and refreshes the display).
- Important: `DRAWLINE` does not automatically flush existing buffered output *before* printing the line. If you need the line to start at the left edge, end the current logical line first (e.g. `PRINTL`) before calling `DRAWLINE`.

**Errors & validation**
- None (arguments are not accepted).

**Examples**
```erabasic
DRAWLINE
PRINTL Header
DRAWLINE
```

## BAR (instruction)

**Summary**
- Prints a bracketed bar-graph string representing the ratio `value / maxValue`.

**Tags**
- io

**Syntax**
- `BAR value, maxValue, length`

**Arguments**
- `value`: int expression (numerator).
- `maxValue`: int expression (denominator); must evaluate to `> 0`.
- `length`: int expression (bar width); must satisfy `1 <= length <= 99`.

**Semantics**
- Computes `filled = clamp(value * length / maxValue, 0, length)` using 64-bit integer arithmetic (integer overflow wraps).
- Produces and prints:
  - `[` + (`BarChar1` repeated `filled`) + (`BarChar2` repeated `length - filled`) + `]`
- `BarChar1` / `BarChar2` are configurable:
  - `BarChar1` default `*`
  - `BarChar2` default `.`
- Does **not** append a newline; use `BARL` if you want a newline.
- If output skipping is active (via `SKIPDISP`), this instruction is skipped.

**Errors & validation**
- Runtime errors if:
  - `maxValue <= 0`
  - `length <= 0`
  - `length >= 100`

**Examples**
```erabasic
BAR 2, 10, 20
PRINTL (2/10)
```

## BARL (instruction)

**Summary**
- Like `BAR`, but appends a newline after printing the bar.

**Tags**
- io

**Syntax**
- `BARL value, maxValue, length`

**Arguments**
- Same as `BAR`.

**Semantics**
- Prints the same bar string as `BAR value, maxValue, length`.
- Appends a newline after printing.
- If output skipping is active (via `SKIPDISP`), this instruction is skipped.

**Errors & validation**
- Same as `BAR`.

**Examples**
```erabasic
BARL 114, 514, 81
```

## TIMES (instruction)

**Summary**
- Multiplies a changeable integer variable by a real-number literal and stores the truncated result back.

**Tags**
- math

**Syntax**
- `TIMES intVarTerm, realLiteral`

**Arguments**
- `intVarTerm`: a changeable integer variable term (must not be `CONST`).
- `realLiteral`: a real-number **literal** parsed as `double` (not an expression).

**Semantics**
- Reads `intVarTerm`’s current value, multiplies it by `realLiteral`, then stores `(long)product` back into `intVarTerm`.
  - The cast truncates toward zero (`125.9` → `125`, `-1.9` → `-1`).
- Calculation mode depends on config `TimesNotRigorousCalculation`:
  - If enabled: uses `double` math.
  - Otherwise: uses `decimal` math (with a fallback conversion path for overflow) to reduce rounding differences.
- The assignment is performed in an `unchecked` context (overflow does not raise an error).

**Errors & validation**
- Load/parse-time validation rejects:
  - non-variable first argument
  - string variables
  - `CONST` variables
- If `realLiteral` is not a valid real number literal, the engine warns and treats it as `0.0`.

**Examples**
```erabasic
#DIM X
X = 100
TIMES X, 1.25
PRINTFORML {X}  ; 125
```

## WAIT (instruction)

**Summary**
- Waits for the user to press Enter (or click, depending on the UI), then continues.

**Tags**
- io

**Syntax**
- `WAIT`

**Arguments**
- None.

**Semantics**
- Enters a UI wait state for an Enter-style key/click.
- Does not assign `RESULT`/`RESULTS`.
- Skipped when output skipping is active (via `SKIPDISP`).

**Errors & validation**
- None.

**Examples**
- `WAIT`

## INPUT (instruction)

**Summary**
- Requests an integer input from the user and stores it into `RESULT` (with mouse-related side channels in some cases).

**Tags**
- io

**Syntax**
- `INPUT [<default> [, <mouse> [, <canSkip> [, <extra>]]]]`

**Arguments**
- `<default>` (optional, int): used only when the submitted text is empty (not used for invalid integer text).
- `<mouse>` (optional, int; default `0`): if non-zero, enables mouse-based input (e.g. selecting buttons can fill the input).
  - `0`: accepted value is written to `RESULT`.
  - Note: mouse mode does not change where the accepted integer is stored on the normal wait path (it is still stored into `RESULT`).
- `<canSkip>` (optional, int): presence enables the `MesSkip` fast path; its numeric value is ignored (not evaluated).
- `<extra>` (optional, int): accepted by the argument parser but ignored by the runtime (not read/evaluated).

**Semantics**
- Enters an integer-input UI wait.
- Timed-wait note: `INPUT` itself does not start a timed wait; timed waits are provided by `TINPUT` / `TINPUTS` (and the shared console input layer may suppress “empty input uses default” while a timed wait is running).
- On successful completion:
  - Writes the accepted integer to `RESULT`.
  - Echoes the accepted input text to output.
    - If the user submits an empty input and a default is used, the echoed text is the default’s decimal string form (e.g. `10`).
- Empty / invalid input handling:
  - If there is no default and the user submits an empty input, the input is rejected and the engine stays in the wait state.
  - If the submitted text is not a valid integer, the input is rejected and the engine stays in the wait state.
  - On a rejected input, no `RESULT*` variables are assigned and the rejected text is not echoed.
- `MesSkip` integration:
  - If `<canSkip>` is present and `MesSkip` is currently true, the engine does not wait and instead accepts the default immediately.
  - In that no-wait path:
    - `<mouse>` must be present (it is read to choose the output slot).
    - `<default>` must be present; otherwise the engine throws a runtime error.
    - The accepted value is written to:
      - `RESULT` if `<mouse> == 0`
      - `RESULT_ARRAY[1]` if `<mouse> != 0`
    - The input string is not echoed (because the UI wait is skipped entirely).
- Mouse-enabled input side channels (UI behavior):
  - If mouse input is enabled and the user completes input via a mouse click, the UI also writes metadata into:
    - `RESULT_ARRAY[1]`: mouse button (`1`=left, `2`=right, `3`=middle).
    - `RESULT_ARRAY[2]`: a modifier-key bitfield (Shift=`2^16`, Ctrl=`2^17`, Alt=`2^18`).
    - `RESULTS_ARRAY[1]`: the clicked button’s string (if any).
    - `RESULT_ARRAY[3]`: mapped “button color” (see below).
  - These side channels are only written on the UI click completion path (not on keyboard-only completion, and not in the `MesSkip` no-wait path).

#### Mapped “button color” (`RESULT:3`) from `<img srcm='...'>`

When a click completes mouse-enabled input, the UI computes `RESULT:3` as follows:

- If the clicked button contains at least one HTML `<img ...>` segment, take the **last** `<img ...>` in that button.
- If that `<img>` has a `srcm` mapping sprite that exists and is loaded:
  - Convert the click position to a pixel coordinate in the mapping sprite by scaling within the rendered image rectangle:
    - Let `drawnWidthPx` / `drawnHeightPx` be the (positive) rendered size of that `<img>` segment.
    - Let `localX` / `localY` be the click position inside that rendered rectangle, in pixels.
    - Let `mapWidthPx` / `mapHeightPx` be the mapping sprite’s base size, in pixels.
    - The sampled mapping coordinate uses integer division (floor):
      - `mapX = localX * mapWidthPx / drawnWidthPx`
      - `mapY = localY * mapHeightPx / drawnHeightPx`
  - Sample the mapping sprite pixel color at `(mapX, mapY)`.
  - Store `RESULT:3 = (color.ToArgb() & 0x00FFFFFF)` (24-bit RGB).
- Otherwise, store `RESULT:3 = 0`.

Compatibility notes:

- The mapping color uses the mapping sprite’s base size (the size defined by `resources/**/*.csv`), not the drawn size.
- If the click is exactly on the image rectangle boundary, the mapping color is treated as `0` (the hit-test uses strict `>`/`<`).
- Some other UI wait types (not `INPUT` itself) may write a mapping color to `RESULT:6` instead of `RESULT:3` (e.g. the “primitive mouse/key” wait used by `INPUTMOUSEKEY`).
- When output skipping is enabled, the engine normally skips `INPUT`.
  - Exception: if output skipping was enabled by `SKIPDISP`, reaching `INPUT` is a runtime error.

**Errors & validation**
- Argument-type errors are raised if a provided argument is not an `int` expression (including `<canSkip>` and `<extra>`).
- Integer parsing is equivalent to `.NET` `Int64.TryParse` on the submitted text.
  - If parsing fails, the engine stays in the wait state.

**Examples**
- `INPUT`
- `INPUT 0`
- `INPUT 10, 1, 1` (default=10, mouse input enabled, skip can auto-accept default)

## INPUTS (instruction)

**Summary**
- Requests a string input from the user and stores it into `RESULTS` (with mouse-related side channels in some cases).

**Tags**
- io

**Syntax**
- `INPUTS`
- `INPUTS <defaultFormString>`
- `INPUTS <defaultFormString>, <mouse> [, <canSkip>]`

**Arguments**
- `<defaultFormString>` (optional): a FORM/formatted string expression used as the default string.
- `<mouse>` (optional): integer expression; if non-zero, enables mouse-based input.
- `<canSkip>` (optional): integer expression; if present, allows `MesSkip` to auto-accept the default without waiting.

- Omitted arguments / defaults:
  - If `<defaultFormString>` is omitted, there is no default value.

**Semantics**
- Enters a string-input UI wait.
- If `<defaultFormString>` is provided, it is evaluated to a string and used as the default when the input is empty and the request is not running a timer.
- On successful completion:
  - Stores the string into `RESULTS`.
  - Echoes the accepted input text to output (UI behavior).
    - If the user submits an empty input and a default is used, the echoed text is that default string.
- Empty input handling:
  - If there is no default and the user submits an empty input, the accepted value is `""` (empty string).
- `MesSkip` integration:
  - If `<canSkip>` is present and `MesSkip` is currently true, the engine does not wait and instead accepts the default immediately.
  - In that no-wait path, the engine assigns the default to:
    - `RESULTS` if `<mouse> == 0`
    - `RESULTS_ARRAY[1]` if `<mouse> != 0`
  - In that no-wait path, the input string is not echoed (because the UI wait is skipped entirely).
- Note: if `<canSkip>` is present, `<mouse>` must also be present (it is read in the `MesSkip` no-wait path).
- Note: if `<canSkip>` is present and `MesSkip` is true at runtime, `<defaultFormString>` must be present.
  - If it is omitted, the engine throws a runtime error when taking the `MesSkip` no-wait path.
- Mouse-enabled input side channels: see `INPUT` (the same UI-side `RESULT_ARRAY[...]` / `RESULTS_ARRAY[...]` behaviors apply).
- Skip-print interaction is the same as `INPUT` (print-family skip rule + `SKIPDISP` input error case).

**Errors & validation**
- Argument parsing errors follow the underlying builder rules for `INPUTS`.
- Argument parsing quirks:
  - After the first comma, non-integer expressions are ignored with a warning.
  - Supplying `<canSkip>` may still emit a “too many arguments” warning, but the value is accepted and used by the runtime.

**Examples**
- `INPUTS`
- `INPUTS Default`
- `INPUTS Hello, %NAME%!, 1, 1`

## TINPUT (instruction)

**Summary**
- Timed integer input: like `INPUT`, but with a time limit and timeout message.

**Tags**
- io

**Syntax**
- `TINPUT <timeMs>, <default> [, <displayTime> [, <timeoutMessage> [, <mouse> [, <canSkip>]]]]`

**Arguments**
- `<timeMs>`: integer expression; time limit in milliseconds.
- `<default>`: integer expression; default value used on timeout (and also on empty input when the request is not running a timer).
- `<displayTime>` (optional, int; default `1`): if non-zero, displays remaining time (UI behavior).
- `<timeoutMessage>` (optional, string; default `TimeupLabel`): message used on timeout.
- `<mouse>` (optional): integer expression; enables mouse input when equal to `1`.
- `<canSkip>` (optional): integer expression; if present, allows `MesSkip` to auto-accept the default without waiting.

**Semantics**
- Enters an integer-input UI wait with a timer of `<timeMs>` milliseconds (a default is always present for timed input).
- Timeout behavior:
  - When the timer expires, the engine runs the input completion path with an empty input string; this causes the default to be accepted.
  - A timeout message is displayed (either by updating the last “remaining time” line, or by printing a single line, depending on `<displayTime>`).
- `MesSkip` integration:
  - If `<canSkip>` is present and `MesSkip` is currently true, the engine does not wait and instead accepts the default immediately.
  - In that no-wait path, the engine assigns the default to:
    - `RESULT` if `<mouse> == 0`
    - `RESULT_ARRAY[1]` if `<mouse> != 0`
  - In that no-wait path, the input string is not echoed (because the UI wait is skipped entirely).
- Mouse-enabled input side channels: see `INPUT` (the same UI-side `RESULT_ARRAY[...]` / `RESULTS_ARRAY[...]` behaviors apply).
- Output skipping interaction is the same as `INPUT`.

**Errors & validation**
- Argument parsing/type-checking errors are engine errors.

**Examples**
- `TINPUT 5000, 0`
- `TINPUT 10000, 1, 1, Time up!, 1, 1`

## TINPUTS (instruction)

**Summary**
- Timed string input: like `INPUTS`, but with a time limit and timeout message.

**Tags**
- io

**Syntax**
- `TINPUTS <timeMs>, <default> [, <displayTime> [, <timeoutMessage> [, <mouse> [, <canSkip>]]]]`

**Arguments**
- `<timeMs>`: integer expression; time limit in milliseconds.
- `<default>`: string expression; default value used on timeout (and also on empty input when the request is not running a timer).
- `<displayTime>` (optional, int; default `1`): if non-zero, displays remaining time.
- `<timeoutMessage>` (optional, string; default `TimeupLabel`): timeout message.
- `<mouse>` (optional): integer expression; enables mouse input when equal to `1`.
- `<canSkip>` (optional): integer expression; if present, allows `MesSkip` to auto-accept the default without waiting.

**Semantics**
- Same model as `TINPUT`, but stores into `RESULTS` (string) rather than `RESULT` (int).
- `MesSkip` integration:
  - If `<canSkip>` is present and `MesSkip` is currently true, the engine does not wait and instead accepts the default immediately.
  - In that no-wait path, the engine assigns the default to:
    - `RESULTS` if `<mouse> == 0`
    - `RESULTS_ARRAY[1]` if `<mouse> != 0`
  - In that no-wait path, the input string is not echoed (because the UI wait is skipped entirely).
- Mouse-enabled input side channels: see `INPUT` (the same UI-side `RESULT_ARRAY[...]` / `RESULTS_ARRAY[...]` behaviors apply).

**Errors & validation**
- Argument parsing/type-checking errors are engine errors.

**Examples**
- `TINPUTS 5000, "DEFAULT"`
- `TINPUTS 3000, NAME, 1, Time up!`

## TONEINPUT (instruction)

**Summary**
- Like `TINPUT`, but uses the “one input” mode (`OneInput = true`).

**Tags**
- io

**Syntax**
- Same as `TINPUT`.

**Arguments**
- Same as `TINPUT`.

- Omitted arguments / defaults:
  - Same as `TINPUT`.

**Semantics**
- Same as `TINPUT`, but with “one input” mode enabled:
  - If the entered text has length > 1, it is truncated to the first character.
  - Exception: if `AllowLongInputByMouse` is enabled and the input was produced by mouse selection, truncation does not occur.

**Errors & validation**
- Same as `TINPUT`.

**Examples**
- `TONEINPUT 5000, 0`

## TONEINPUTS (instruction)

**Summary**
- Like `TINPUTS`, but uses the “one input” mode (`OneInput = true`).

**Tags**
- io

**Syntax**
- Same as `TINPUTS`.

**Arguments**
- Same as `TINPUTS`.

- Omitted arguments / defaults:
  - Same as `TINPUTS`.

**Semantics**
- Same as `TINPUTS`, but with “one input” mode enabled:
  - If the entered text has length > 1, it is truncated to the first character.
  - Exception: if `AllowLongInputByMouse` is enabled and the input was produced by mouse selection, truncation does not occur.

**Errors & validation**
- Same as `TINPUTS`.

**Examples**
- `TONEINPUTS 5000, "A"`

## TWAIT (instruction)

**Summary**
- Timed wait: waits for a limited time (and optionally disallows user input), then continues.

**Tags**
- io

**Syntax**
- `TWAIT <timeMs>, <mode>`

**Arguments**
- `<timeMs>`: integer expression; time limit in milliseconds.
- `<mode>`: integer expression:
  - `0`: wait for Enter/click, but time out after `<timeMs>`.
  - non-zero: disallow input and simply wait `<timeMs>` (or be affected by macro/skip behavior).

**Semantics**
- If `<mode> == 0`: waits for Enter/click, but times out after `<timeMs>`.
- If `<mode> != 0`: disallows input and simply waits `<timeMs>` (but can still be affected by macro/skip behavior).
- When the time limit elapses, execution continues automatically.
- Does not assign `RESULT`/`RESULTS`.
- Skipped when output skipping is active (via `SKIPDISP`).

**Errors & validation**
- Argument type errors follow the normal integer-expression argument rules.

**Examples**
- `TWAIT 3000, 0` (wait up to 3 seconds for Enter)
- `TWAIT 1000, 1` (wait 1 second with no input)

## WAITANYKEY (instruction)

**Summary**
- Like `WAIT`, but accepts **any key** input (not only Enter) to continue.

**Tags**
- io

**Syntax**
- `WAITANYKEY`

**Arguments**
- None.

**Semantics**
- Enters a UI wait state for any-key input.
- Does not assign `RESULT`/`RESULTS`.
- Skipped when output skipping is active (via `SKIPDISP`).

**Errors & validation**
- None.

**Examples**
- `WAITANYKEY`

## FORCEWAIT (instruction)

**Summary**
- Like `WAIT`, but stops “message skip” from auto-advancing past the wait.

**Tags**
- io

**Syntax**
- `FORCEWAIT`

**Arguments**
- None.

**Semantics**
- Waits for Enter/click, and stops “message skip” from auto-advancing past the wait.
- Does not assign `RESULT`/`RESULTS`.
- Skipped when output skipping is active (via `SKIPDISP`).

**Errors & validation**
- None.

**Examples**
- `FORCEWAIT`

## ONEINPUT (instruction)

**Summary**
- Like `INPUT`, but requests a “one input” integer entry (UI-side restriction).

**Tags**
- io

**Syntax**
- `ONEINPUT`
- `ONEINPUT <default>`
- `ONEINPUT <default>, <mouse>, <canSkip> [, <extra>]`

**Arguments**
- Same as `INPUT`.

- Omitted arguments / defaults:
  - Same as `INPUT`.

**Semantics**
- Like `INPUT` (including `MesSkip` behavior and mouse side channels), but sets `OneInput = true` on the input request.
- Implementation-oriented notes:
  - In the UI input handler, `OneInput` truncates the entered text to at most one character in many cases, so it typically behaves like “read a single digit/character then parse”.
  - Depending on configuration, mouse-provided input may bypass this truncation.

**Errors & validation**
- Same as `INPUT`.

**Examples**
- `ONEINPUT`
- `ONEINPUT 0`

## ONEINPUTS (instruction)

**Summary**
- Like `INPUTS`, but requests a “one input” string entry (UI-side restriction).

**Tags**
- io

**Syntax**
- `ONEINPUTS`
- `ONEINPUTS <defaultFormString>`
- `ONEINPUTS <defaultFormString>, <mouse> [, <canSkip>]`

**Arguments**
- Same as `INPUTS`.

- Omitted arguments / defaults:
  - Same as `INPUTS`.

**Semantics**
- Like `INPUTS` (including `MesSkip` behavior and mouse side channels), but with “one input” mode enabled:
  - If the entered text has length > 1, it is truncated to the first character.
  - Exception: if `AllowLongInputByMouse` is enabled and the input was produced by mouse selection, truncation does not occur.

**Errors & validation**
- Same as `INPUTS`.

**Examples**
- `ONEINPUTS`
- `ONEINPUTS A`

## CLEARLINE (instruction)

**Summary**
- Deletes the last *N logical output lines* from the console display/log.

**Tags**
- io

**Syntax**
- `CLEARLINE <n>`

**Arguments**
- `<n>`: integer expression.
  - The evaluated value is converted to a 32-bit signed integer by truncation (i.e. low 32 bits interpreted as signed).

**Semantics**
- Evaluates `<n>` and deletes the last `n` logical output lines from the console display/log.
- The deletion count is in **logical lines**, not raw display lines:
  - One logical line can occupy multiple display lines (e.g. word wrapping).
  - Deletion walks backward from the end of the display list and counts only entries marked as “logical line” boundaries; all associated display lines are removed.
- If `n <= 0`, nothing is deleted.
- After deleting, the display is refreshed.

**Errors & validation**
- No explicit validation in the instruction.
- No error is raised for negative or overflowed values (after the 32-bit conversion).

**Examples**
- `CLEARLINE 1`
- `CLEARLINE 10`

## REUSELASTLINE (instruction)

**Summary**
- Prints a **temporary single line** that is intended to be overwritten by the next printed line.

**Tags**
- io

**Syntax**
- `REUSELASTLINE`
- `REUSELASTLINE <formString>`

**Arguments**
- `<formString>` (optional): FORM/formatted string (parsed like `PRINTFORM*`) used as the temporary line’s content.

- Omitted arguments / defaults:
  - If omitted, the argument is treated as the empty string.

**Semantics**
- Evaluates `<formString>` to a string and prints it as a temporary line.
- A “temporary line” has a special overwrite behavior:
  - When the engine later adds a new display line, if the current last display line is temporary, it is deleted first; the new line then takes its place.
  - As a result, repeated `REUSELASTLINE` calls typically “update” a single line (useful for progress/timer displays).
- If the resulting string is empty, the current console implementation prints nothing (and therefore does not overwrite an existing line).

**Errors & validation**
- None.

**Examples**
- `REUSELASTLINE Now loading...`
- `REUSELASTLINE %TIME%`

## UPCHECK (instruction)

**Summary**
- Applies the `UP`/`DOWN` delta arrays to `PALAM` for the current `TARGET` character, and prints each applied change.

**Tags**
- characters
- io

**Syntax**
- `UPCHECK`

**Arguments**
- None.

**Semantics**
- Reads:
  - global arrays `UP` and `DOWN`
  - the current `TARGET` character index
  - the target character’s `PALAM` array
  - parameter names from `PALAMNAME`
- If `TARGET` is out of range (`TARGET < 0` or `TARGET >= CHARANUM`):
  - no parameter changes are applied, and nothing is printed
  - it still clears `UP` and `DOWN` to `0` (see below).
- Otherwise, it computes the loop bound `length` as follows (note the ordering):
  - Start with `length = PALAM.Length`.
  - If `PALAM.Length > UP.Length`, set `length = UP.Length`.
  - If `PALAM.Length > DOWN.Length`, set `length = DOWN.Length`.
- For each parameter index `i` such that `0 <= i < length`:
  - Negative and zero deltas are ignored: if `UP[i] <= 0` and `DOWN[i] <= 0`, this index is skipped (no change, no output).
  - Otherwise:
    - Let `old = PALAM[i]`.
    - Apply the change in an `unchecked` context: `PALAM[i] = old + UP[i] - DOWN[i]`.
    - If output is not being skipped, prints one line (and ends the line) in this exact format:
      - `PALAMNAME[i] + " " + old + ("+" + UP[i] if UP[i] > 0) + ("-" + DOWN[i] if DOWN[i] > 0) + "=" + PALAM[i]`
      - Notes:
        - There are no parentheses around `+...` / `-...`.
        - If `PALAMNAME[i]` is `null`, it is treated as `""` (so the line starts with a space).
        - Each printed change ends the line immediately (i.e. it is printed as its own line).
- After finishing, clears **all elements** of `UP` and `DOWN` to `0`.
- If output skipping is active (via `SKIPDISP`), changes are still applied and `UP`/`DOWN` are still cleared, but nothing is printed.

**Errors & validation**
- None specific to this instruction.

**Examples**
```erabasic
UP:0 = 123
UP:1 = 456
UPCHECK
```

## CUPCHECK (instruction)

**Summary**
- Like `UPCHECK`, but applies `CUP`/`CDOWN` to `PALAM` for a specified character index.

**Tags**
- characters
- io

**Syntax**
- `CUPCHECK [charaIndex]`

**Arguments**
- `charaIndex` (optional, int; default `0` with a warning if omitted): the character index to apply changes to.

**Semantics**
- Reads the target character’s per-character arrays:
  - `CUP` and `CDOWN`
  - and that character’s `PALAM`
- If `charaIndex` is out of range, returns immediately:
  - no changes are applied, nothing is printed
  - `CUP`/`CDOWN` are **not** cleared.
- Otherwise, it computes the loop bound `length` as follows (note the ordering):
  - Start with `length = PALAM.Length`.
  - If `PALAM.Length > CUP.Length`, set `length = CUP.Length`.
  - If `PALAM.Length > CDOWN.Length`, set `length = CDOWN.Length`.
- For each parameter index `i` such that `0 <= i < length`:
  - Negative and zero deltas are ignored: if `CUP[i] <= 0` and `CDOWN[i] <= 0`, this index is skipped.
  - Otherwise:
    - Let `old = PALAM[i]`.
    - Apply the change in an `unchecked` context: `PALAM[i] = old + CUP[i] - CDOWN[i]`.
    - If output is not being skipped, prints one line (and ends the line) in the same format as `UPCHECK`, but using `CUP`/`CDOWN`:
      - `PALAMNAME[i] + " " + old + ("+" + CUP[i] if CUP[i] > 0) + ("-" + CDOWN[i] if CDOWN[i] > 0) + "=" + PALAM[i]`
      - Each printed change ends the line immediately (i.e. it is printed as its own line).
- After finishing, clears **all elements** of that character’s `CUP` and `CDOWN` arrays to `0`.
- If output skipping is active (via `SKIPDISP`), changes are still applied and `CUP`/`CDOWN` are still cleared, but nothing is printed.

**Errors & validation**
- None specific to this instruction (out-of-range just returns).

**Examples**
```erabasic
CUP:TARGET:0 = 10
CUPCHECK TARGET
```

## ADDCHARA (instruction)

**Summary**
- Adds one or more characters to the current character list using character templates loaded from CSV.

**Tags**
- characters

**Syntax**
- `ADDCHARA charaNo`
- `ADDCHARA charaNo1, charaNo2, ...`

**Arguments**
- Each `charaNo`: int expression selecting a character template.

**Semantics**
- Requires at least one argument; multiple arguments are accepted but the engine emits a parse-time warning for multi-argument uses.
- For each `charaNo` (evaluated left-to-right), the engine immediately appends one character to the current character list using the character template identified by that number.
- `CHARANUM` increases by 1 for each successfully added character.
- If a later argument fails (e.g. undefined template), earlier additions remain (no rollback).
- This instruction does not print anything and does not automatically change `TARGET`/`MASTER`/`ASSI`.

**Errors & validation**
- Runtime error if any `charaNo` does not resolve to a known character template.

**Examples**
```erabasic
ADDCHARA 3, 5, 6
PRINTFORML {CHARANUM}
```

## ADDSPCHARA (instruction)

**Summary**
- Adds one or more “SP characters” using the SP-character template path.

**Tags**
- characters

**Syntax**
- `ADDSPCHARA charaNo`
- `ADDSPCHARA charaNo1, charaNo2, ...`

**Arguments**
- Each `charaNo`: int expression selecting a character template.

**Semantics**
- Requires the `CompatiSPChara` config option to be enabled; otherwise this instruction errors before evaluating any arguments.
- Requires at least one argument; multiple arguments are accepted but the engine emits a parse-time warning for multi-argument uses.
- For each `charaNo` (evaluated left-to-right), immediately appends one character using the SP template lookup path.
- `CHARANUM` increases by 1 for each successfully added character.
- If a later argument fails (e.g. undefined template), earlier additions remain (no rollback).
- This instruction does not print anything and does not automatically change `TARGET`/`MASTER`/`ASSI`.

**Errors & validation**
- Runtime error if `CompatiSPChara` is disabled.
- Runtime error if any `charaNo` does not resolve to a known character template.

**Examples**
```erabasic
ADDSPCHARA 10
```

## ADDDEFCHARA (instruction)

**Summary**
- Performs the engine’s “default character initialization” step used at game start.

**Tags**
- characters
- system

**Syntax**
- `ADDDEFCHARA`

**Arguments**
- None.

**Semantics**
- Intended for use in `@SYSTEM_TITLE`.
- When executed, the engine adds:
  - the character template for CSV number `0`, and then
  - the initial character specified by `gamebase.csv` (`GameBaseData.DefaultCharacter`) if it is `> 0`.
- This uses “CSV number” lookup (engine template lookup by CSV slot), which is distinct from `ADDCHARA 0` (template lookup by character `NO`).
- If a referenced CSV template does not exist, the engine falls back to adding a “pseudo character” (like `ADDVOIDCHARA`).

**Errors & validation**
- Runtime error if executed outside `@SYSTEM_TITLE` (unless executed in a debug-only context where no parent label is attached).

**Examples**
```erabasic
@SYSTEM_TITLE
ADDDEFCHARA
```

## ADDVOIDCHARA (instruction)

**Summary**
- Adds a “pseudo character” that is not loaded from CSV.

**Tags**
- characters

**Syntax**
- `ADDVOIDCHARA`

**Arguments**
- None.

**Semantics**
- Appends a new character record created from the engine’s pseudo-character template.
- The new character’s variables start from the language defaults (`0` for numeric cells, `""` for string reads).
- This instruction does not print anything and does not automatically change `TARGET`/`MASTER`/`ASSI`.

**Errors & validation**
- None specific to this instruction.

**Examples**
```erabasic
ADDVOIDCHARA
TARGET = CHARANUM - 1
```

## DELCHARA (instruction)

**Summary**
- Deletes one or more characters from the current character list by character index.

**Tags**
- characters

**Syntax**
- `DELCHARA charaIndex`
- `DELCHARA charaIndex1, charaIndex2, ...`

**Arguments**
- Each `charaIndex`: int expression selecting an existing character index.

**Semantics**
- Requires at least one argument; multiple arguments are accepted but a parse-time warning is emitted for multi-argument uses.
- Evaluates all `charaIndex` arguments first (left-to-right), storing the integer results in an array.
- Deletion behavior depends on argument count:
  - If exactly one index was provided: deletes that character immediately by index.
  - If multiple indices were provided: deletes all referenced characters as a set.
    - Each index is resolved against the character list as it existed before any removals in this call.
    - The engine rejects duplicate deletions by identity (two indices that resolve to the same character object cause an error).
    - If an error occurs while processing a multi-delete list, some earlier listed characters may already have been deleted (no rollback).
- Deleting characters shifts indices of later characters; after deletion, valid indices are always a dense range `0 <= i < CHARANUM`.
- The engine does not automatically rebind `TARGET`/`MASTER`/`ASSI` after deletion.

**Errors & validation**
- Runtime error if any `charaIndex` is out of range.
- When deleting multiple characters, runtime error if the same character is specified more than once (duplicate deletion).

**Examples**
```erabasic
DELCHARA 2
DELCHARA 1, 3
```

## PUTFORM (instruction)

**Summary**
- Appends a formatted string to the save-description buffer (`SAVEDATA_TEXT`).

**Tags**
- io

**Syntax**
- `PUTFORM`
- `PUTFORM <formString>`

**Arguments**
- `<formString>` (optional): FORM/formatted string.

- Omitted arguments / defaults:
  - If omitted, the argument is treated as the empty string.

**Semantics**
- Evaluates `<formString>` to a string.
- Appends it to the internal save-description buffer:
  - If `SAVEDATA_TEXT` is non-null, `SAVEDATA_TEXT += <string>`.
  - Otherwise, `SAVEDATA_TEXT = <string>`.
- Does not print to the console.
- Typically used by the save-info generation path (e.g. `@SAVEINFO`) to build `SAVEDATA_TEXT`.

**Errors & validation**
- None.

**Examples**
- `PUTFORM %PLAYERNAME% - Day %DAY%`

## QUIT (instruction)

**Summary**
- Ends the current run by requesting the console to quit.

**Tags**
- system

**Syntax**
- `QUIT`

**Arguments**
- None.

**Semantics**
- Requests the engine to quit the game.
- Script execution stops immediately.
- UI shutdown is performed by the console/UI host after the quit request is posted.

**Errors & validation**
- None.

**Examples**
- `QUIT`

## BEGIN (instruction)

**Summary**
- Requests a transition into one of the engine’s **system phases** (e.g. `SHOP`, `TRAIN`, `TITLE`) after the current call stack unwinds.

**Tags**
- system

**Syntax**
- `BEGIN <keyword>`

**Arguments**
- `<keyword>`: raw string (the entire remainder of the source line after the instruction delimiter).
  - Must match one of the supported keywords exactly (see below).
  - The current engine compares this string literally (no automatic trim or case-folding).

**Semantics**
- Recognized keywords (engine-defined):
  - `SHOP`, `TRAIN`, `AFTERTRAIN`, `ABLUP`, `TURNEND`, `FIRST`, `TITLE`
- On execution:
  - Validates `<keyword>` by matching it against the list above; otherwise raises an error.
  - Requests a transition into that system phase after the current call stack unwinds.
  - Immediately performs some keyword-specific side effects:
    - `SHOP` and `FIRST` unload temporary loaded image resources.
  - Ends the current function immediately (as if returning) and continues unwinding until reaching the top-level.
  - After reaching the top-level, enters the requested system phase, clears the call stack, and continues execution in that phase.
  - Resets output style to defaults.

**Errors & validation**
- If `<keyword>` is not recognized, raises a runtime error (“invalid BEGIN argument”).

**Examples**
- `BEGIN TITLE`
- `BEGIN SHOP`

## SAVEGAME (instruction)

**Summary**
- Opens the engine’s interactive **save UI** (system-driven save).

**Tags**
- save-system

**Syntax**
- `SAVEGAME`

**Arguments**
- None.

**Semantics**
- Requires that the current system state allows saving; otherwise raises an error.
- Saves the current process state for later restoration, then transitions into the system save flow.
- The system save flow (high-level behavior):
  - Displays save slots with indices `0 <= slot < SaveDataNos` in pages of 20.
  - Uses `100` as the “back/cancel” input.
  - After selecting a slot:
    - If it already contains data, prompts for overwrite confirmation.
    - Initializes `SAVEDATA_TEXT` with the current timestamp (`yyyy/MM/dd HH:mm:ss `).
    - Calls `@SAVEINFO` (if it exists), which can append to `SAVEDATA_TEXT` (commonly via `PUTFORM`).
    - Saves the current state to the selected slot (as `save{slot:00}.sav` under `SavDir`) using `SAVEDATA_TEXT` as the slot description text.
  - Returns to the previous system state after completion or cancellation.
- See also: `save-files.md` (directories, partitions, and on-disk formats)

**Errors & validation**
- Error if saving is not allowed in the current system state.
- If the underlying file write fails, the UI prints an error and waits for a key.

**Examples**
- `SAVEGAME`

## LOADGAME (instruction)

**Summary**
- Opens the engine’s interactive **load UI** (system-driven load).

**Tags**
- save-system

**Syntax**
- `LOADGAME`

**Arguments**
- None.

**Semantics**
- Requires that the current system state allows saving/loading (same gate as `SAVEGAME`), otherwise raises an error.
- Saves the current process state for later restoration, then transitions into the system load flow.
- The system load flow (high-level behavior):
  - Displays save slots with indices `0 <= slot < SaveDataNos` in pages of 20.
  - Includes a special autosave entry `99` when applicable.
  - Uses `100` as the “back/cancel” input.
  - After selecting a valid slot:
    - Loads the slot file (as `save{slot:00}.sav` under `SavDir`).
    - Discards the previous saved process state.
    - Enters the same post-load system hook sequence as `LOADDATA`:
      - `SYSTEM_LOADEND` (if present)
      - `EVENTLOAD` (if present)
      - then returns to normal system flow (typically as if `BEGIN SHOP` occurred, unless `EVENTLOAD` performed a `BEGIN`).
- See also: `save-files.md` (directories, partitions, and on-disk formats)

**Errors & validation**
- Error if load is not allowed in the current system state.
- Selecting an empty slot prints a “no data” message and reopens the load prompt.
- If loading fails unexpectedly after selection, the engine throws an internal execution error.

**Examples**
- `LOADGAME`

## SAVEDATA (instruction)

**Summary**
- Saves the current game state to a numbered save slot file (script-controlled save).

**Tags**
- save-system

**Syntax**
- `SAVEDATA <slot>, <saveText>`

**Arguments**
- `<slot>`: integer expression. Must be in `[0, 2147483647]` (32-bit signed non-negative).
- `<saveText>`: string expression; saved into the file and shown by the built-in save/load UI.
  - Must not contain a newline (`'\n'`).

**Semantics**
- Evaluates `<slot>` and `<saveText>`.
- Writes a save file under `SavDir`:
  - Path is `save{slot:00}.sav` (e.g. slot `0` -> `save00.sav`).
- Save format:
  - If `SystemSaveInBinary` is enabled, writes Emuera’s binary save format with file type `Normal`.
  - Otherwise, writes the legacy text save format.
  - The save always includes:
    - game unique code and script version checks
    - the `<saveText>` string
    - the current character list and variable data
    - Emuera-private extension blocks (if applicable)
- If saving fails unexpectedly (I/O error, etc.), the engine prints an error message but does not throw.
- See also: `save-files.md` (directories, partitions, and on-disk formats)

**Errors & validation**
- Errors if `<slot>` is negative or larger than `int.MaxValue`.
- Error if `<saveText>` contains `'\n'`.

**Examples**
- `SAVEDATA 0, "Start of day 1"`
- `SAVEDATA 12, SAVEDATA_TEXT`

## LOADDATA (instruction)

**Summary**
- Loads a numbered save slot file (script-controlled load), resets the call stack, and then runs the engine’s post-load system hooks.

**Tags**
- save-system

**Syntax**
- `LOADDATA <slot>`

**Arguments**
- `<slot>`: integer expression. Must be in `[0, 2147483647]` (32-bit signed non-negative).
  - If omitted, the argument parser supplies `0` (with a warning); this effectively loads slot `0`.

- Omitted arguments / defaults:
  - None (but see omitted-argument behavior above).

**Semantics**
- Validates the target save file; if the file is missing/corrupt/mismatched, raises a runtime error.
- Loads the save slot and replaces the current saveable state (characters and variables) with the loaded contents.
- Sets the pseudo variables:
  - `LASTLOAD_NO` to the loaded slot number
  - `LASTLOAD_TEXT` to the saved `<saveText>`
  - `LASTLOAD_VERSION` to the save file’s recorded script version
- Clears the EraBasic call stack, discarding the current call context.
- Runs post-load system hooks (if they exist), in this order:
  - `SYSTEM_LOADEND`
  - `EVENTLOAD`
- If `EVENTLOAD` returns normally without performing a `BEGIN`, execution proceeds as if `BEGIN SHOP` occurred.
- See also: `save-files.md` (directories, partitions, and on-disk formats).

**Errors & validation**
- Errors if `<slot>` is negative or larger than `int.MaxValue`.
- Error if the target save file is missing/corrupt/mismatched.
- If loading fails unexpectedly after validation, a runtime error is raised.

**Examples**
- `LOADDATA 0`

## DELDATA (instruction)

**Summary**
- Deletes a numbered save slot file (`saveXX.sav`) if it exists.

**Tags**
- save-system

**Syntax**
- `DELDATA <slot>`

**Arguments**
- `<slot>` (optional, int; default `0` with a warning if omitted): save slot index. Must be in `[0, 2147483647]` (32-bit signed non-negative).

**Semantics**
- Computes the save file path under `SavDir` as `save{slot:00}.sav`.
- If the file does not exist, does nothing.
- If the file exists:
  - If it has the read-only attribute, raises an error.
  - Otherwise deletes it.
- See also: `save-files.md` (directories, partitions, and on-disk formats)

**Errors & validation**
- Errors if `<slot>` is negative or larger than `int.MaxValue`.
- Error if the file exists and is read-only.

**Examples**
- `DELDATA 3`

## SAVEGLOBAL (instruction)

**Summary**
- Saves global variables to `global.sav`.

**Tags**
- save-system

**Syntax**
- `SAVEGLOBAL`

**Arguments**
- None.

**Semantics**
- Writes the global save file under `SavDir`:
  - Path is `global.sav`.
- Save format:
  - If `SystemSaveInBinary` is enabled, writes Emuera’s binary save format with file type `Global`.
  - Otherwise, writes the legacy text save format.
  - Emuera-private global extension blocks may also be written.
- If a system-level I/O exception occurs during saving, the engine raises a runtime error.
- See also: `save-files.md` (directories, partitions, and on-disk formats)

**Errors & validation**
- Errors if the save directory cannot be created or the file cannot be written.

**Examples**
- `SAVEGLOBAL`

## LOADGLOBAL (instruction)

**Summary**
- Loads global variables from `global.sav` and reports success via `RESULT`.

**Tags**
- save-system

**Syntax**
- `LOADGLOBAL`

**Arguments**
- None.

**Semantics**
- Attempts to load `global.sav` under `SavDir`.
- On success:
  - Loads the global variable data from the file (format depends on file type).
  - Sets `RESULT = 1`.
- On failure:
  - Sets `RESULT = 0`.
- Before attempting to read, the loader removes certain Emuera-private global extension data; if loading then fails, this removal may still have occurred.
- See also: `save-files.md` (directories, partitions, and on-disk formats)

**Errors & validation**
- No explicit errors are raised for load failures; failures are reported via `RESULT`.

**Examples**
- `LOADGLOBAL`

## RESETDATA (instruction)

**Summary**
- Resets the current game/runtime variable state (excluding global variables).

**Tags**
- save-system

**Syntax**
- `RESETDATA`

**Arguments**
- None.

**Semantics**
- Resets non-global variables to their default values (global variables are not reset).
- Disposes and clears the character list.
- Removes Emuera-private save-related extension data (e.g. XML/maps/data-table extensions).
- Resets output style to defaults.
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- None.

**Examples**
- `RESETDATA`

## RESETGLOBAL (instruction)

**Summary**
- Resets global variables to their default values.

**Tags**
- save-system

**Syntax**
- `RESETGLOBAL`

**Arguments**
- None.

**Semantics**
- Resets global variables to their default values.
- Removes Emuera-private global/static extension data (e.g. XML/maps global/static extensions).
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- None.

**Examples**
- `RESETGLOBAL`

## SIF (instruction)

**Summary**
- “Single-line IF”: conditionally skips the **next logical line only**.

**Tags**
- control-flow

**Syntax**
- `SIF <int expr>`
  - `<next logical line>`

**Arguments**
- `<int expr>`: evaluated as integer; zero = false, non-zero = true.

- Omitted arguments / defaults:
  - If the expression is omitted, it defaults to `0` (false) and emits a load-time warning.

**Semantics**
- If the condition is true (non-zero), execution continues normally.
- If the condition is false (zero), the engine advances the program counter one extra time (skipping exactly one logical line).
- Load-time validation enforces an inherent limitation of this “skip the next line” model:
  - If the following line is a **partial instruction** (structural marker / block delimiter; e.g. `IF`, `ELSE`, `CASE`, loop markers), the engine warns because skipping marker lines breaks block structure.
  - If the following line is a `$label` line, the engine warns.
  - If there is no following executable line (EOF / next `@label`), the engine warns.
  - If there is at least one physically empty line between `SIF` and the next logical line, the engine warns.

**Errors & validation**
- Some invalid “next line” situations are treated as load-time errors (the `SIF` line is marked as error and cannot run safely), including:
  - no following logical line (EOF / next `@label`)
  - following line is a function label line (`@...`) or a null terminator line
  - following instruction line is a **partial instruction** (structural marker / block delimiter)
  - following line is a `$label` line
- The engine may also warn if there are physically empty line(s) between `SIF` and the next logical line.

**Examples**
- `SIF A == 0`
- `PRINTL "A is non-zero"`

## IF (instruction)

**Summary**
- Begins an `IF ... ENDIF` block. Chooses the first true clause among `IF` / `ELSEIF` / `ELSE` and executes that clause body.

**Tags**
- control-flow

**Syntax**
- `IF <int expr>`
  - `...`
  - `ELSEIF <int expr>`
  - `...`
  - `ELSE`
  - `...`
  - `ENDIF`

**Arguments**
- `<int expr>`: evaluated as integer; zero = false, non-zero = true.

- Omitted arguments / defaults:
  - If the expression is omitted, it defaults to `0` (false) and emits a load-time warning.

**Semantics**
- Evaluates its own condition and then each `ELSEIF` condition in order.
- If a condition is true, that clause’s body is selected and executed.
- If no condition matches:
  - If there is an `ELSE`, the `ELSE` body is executed.
  - Otherwise, the whole block is skipped.
- After any selected clause body finishes, the rest of the `IF` block is skipped and execution continues after the matching `ENDIF`.
- Jump behavior note (affects unstructured entry such as `GOTO` into blocks): when control transfers to an `IF`/`ELSEIF`/`ELSE` line as a jump target, execution begins at the **next** logical line (the clause body), not on the marker line itself. See `control-flow.md`.

**Errors & validation**
- `ELSE` / `ELSEIF` without a matching open `IF`, or `ENDIF` without a matching open `IF`, are load-time errors (the line is marked as error).
- `ELSEIF` after an `ELSE` produces a load-time warning.

**Examples**
- `IF FLAG`
- `  PRINTL "yes"`
- `ELSE`
- `  PRINTL "no"`
- `ENDIF`

## ELSE (instruction)

**Summary**
- Final clause header inside an `IF ... ENDIF` block.

**Tags**
- control-flow

**Syntax**
- `ELSE`

**Arguments**
- None.

**Semantics**
- When reached **sequentially**, `ELSE` unconditionally jumps to the matching `ENDIF` marker, skipping the rest of the block.
- When selected by the `IF` header, the engine jumps to the `ELSE` line as a **marker** and begins executing at the next line (the `ELSE` body).

**Errors & validation**
- Invalid placement (outside `IF`) is a load-time error (the line is marked as error).
- `ELSEIF` or `ELSE` after an `ELSE` produces a load-time warning.

**Examples**
- `ELSE`

## ELSEIF (instruction)

**Summary**
- Clause header inside an `IF ... ENDIF` block.

**Tags**
- control-flow

**Syntax**
- `ELSEIF <int expr>`

**Arguments**
- `<int expr>` is evaluated by the `IF` header’s clause-selection logic (not by the `ELSEIF` instruction itself).

**Semantics**
- When reached **sequentially** (i.e., a previous clause already executed and control fell through), `ELSEIF` unconditionally jumps to the matching `ENDIF` marker, skipping the rest of the block.
- When entered as the selected clause, the engine jumps to the `ELSEIF` line as a **marker** and begins executing at the next line (the clause body); the `ELSEIF` instruction itself is not executed in that path.

**Errors & validation**
- Invalid placement (outside `IF`) is a load-time error (the line is marked as error).

**Examples**
- `ELSEIF A > 10`

## ENDIF (instruction)

**Summary**
- Ends an `IF ... ENDIF` block.

**Tags**
- control-flow

**Syntax**
- `ENDIF`

**Arguments**
- None.

**Semantics**
- Marker-only instruction (no runtime effect). The loader uses it to close the `IF` nesting and to set jump targets for `IF`/`ELSEIF`/`ELSE`.

**Errors & validation**
- `ENDIF` without a matching open `IF` is a load-time error (the line is marked as error).

**Examples**
- `ENDIF`

## SELECTCASE (instruction)

**Summary**
- Begins a `SELECTCASE ... ENDSELECT` multi-branch block that compares a single selector expression against one or more `CASE` conditions.

**Tags**
- control-flow

**Syntax**
- `SELECTCASE <expr>`
  - `CASE <caseExpr> (, <caseExpr> ... )`
  - `...`
  - `CASEELSE`
  - `...`
  - `ENDSELECT`

**Arguments**
- `<expr>`: selector expression; may be int or string.

**Semantics**
- The loader gathers all `CASE` / `CASEELSE` headers into an ordered list and links them to the matching `ENDSELECT`.
- At runtime:
  - Evaluates the selector once to either `long` or `string`.
  - Scans each `CASE` in order; the first `CASE` that matches becomes the chosen clause.
  - If no `CASE` matches and a `CASEELSE` exists, chooses `CASEELSE`.
  - Otherwise jumps to the `ENDSELECT` marker (skipping the whole block).
- When a clause is chosen, the engine jumps to that `CASE`/`CASEELSE` header as a **marker** and begins executing at the next line (the clause body).

**Errors & validation**
- Missing selector expression is a load-time error (the `SELECTCASE` line is marked as error).
- `CASE` expressions whose type does not match the selector type are load-time errors (the `CASE` line is marked as error and is skipped by the runtime selector scan).
- Mis-nesting / unexpected `CASE` / unexpected `ENDSELECT` are load-time errors (the line is marked as error).

**Examples**
- `SELECTCASE A`
- `CASE 0`
- `  PRINTL "zero"`
- `CASE 1 TO 9`
- `  PRINTL "small"`
- `CASEELSE`
- `  PRINTL "other"`
- `ENDSELECT`

## CASE (instruction)

**Summary**
- Clause header inside a `SELECTCASE ... ENDSELECT` block.

**Tags**
- control-flow

**Syntax**
- `CASE <caseExpr> (, <caseExpr> ... )`

**Arguments**
- Each `<caseExpr>` is one of:
  - Normal: `<expr>` (matches by equality against the selector).
  - Range: `<expr> TO <expr>` (inclusive range).
  - “IS form”: `IS <binaryOp> <expr>` (e.g. `IS >= 10`), using the engine’s binary-operator semantics.

**Semantics**
- When reached **sequentially** (fall-through after another case body), `CASE` unconditionally jumps to the matching `ENDSELECT` marker, skipping the rest of the block.
- When entered as the selected clause, the engine jumps to the `CASE` header as a **marker** and begins executing at the next line (the clause body).
- Matching rules (engine details):
  - Normal: `selector == expr` (strings use .NET `==` on `string`).
  - Range:
    - int: `left <= selector && selector <= right`
    - string: uses `string.Compare(left, selector, SCExpression)` and `string.Compare(selector, right, SCExpression)` (where `SCExpression` is the engine’s configured string-comparison mode for expressions).
  - `IS <op> <expr>`: evaluates `(selector <op> expr)` using the engine’s binary operator reducer.

**Errors & validation**
- Invalid placement (outside `SELECTCASE`) is a load-time error (the line is marked as error).
- An empty `CASE` condition list is a load-time error (argument parsing fails and the line is marked as error).
- A `TO` range requires both sides to have the same operand type (otherwise: load-time error).

**Examples**
- `CASE 5`
- `CASE 1 TO 10`
- `CASE IS >= 100`

## CASEELSE (instruction)

**Summary**
- Default clause header inside a `SELECTCASE ... ENDSELECT` block.

**Tags**
- control-flow

**Syntax**
- `CASEELSE`

**Arguments**
- None.

**Semantics**
- Chosen only if no earlier `CASE` matches.
- When reached **sequentially** (fall-through after another case body), `CASEELSE` unconditionally jumps to the matching `ENDSELECT` marker.
- When selected, the engine jumps to the `CASEELSE` header as a **marker** and begins executing at the next line (the clause body).

**Errors & validation**
- Invalid placement (outside `SELECTCASE`) is a load-time error (the line is marked as error).
- `CASE` after `CASEELSE` produces a load-time warning.

**Examples**
- `CASEELSE`

## ENDSELECT (instruction)

**Summary**
- Ends a `SELECTCASE ... ENDSELECT` block.

**Tags**
- control-flow

**Syntax**
- `ENDSELECT`

**Arguments**
- None.

**Semantics**
- Marker-only instruction (no runtime effect). The loader uses it to close `SELECTCASE` nesting and to set jump targets for `SELECTCASE`/`CASE`/`CASEELSE`.

**Errors & validation**
- `ENDSELECT` without a matching open `SELECTCASE` is a load-time error (the line is marked as error).

**Examples**
- `ENDSELECT`

## REPEAT (instruction)

**Summary**
- Begins a `REPEAT ... REND` counted loop using the built-in variable `COUNT` as the loop counter.

**Tags**
- control-flow

**Syntax**
- `REPEAT <countExpr>`
  - `...`
  - `REND`

**Arguments**
- `<countExpr>`: int expression giving the number of iterations.

- Omitted arguments / defaults:
  - If omitted, the count defaults to `0` (and emits a warning when the line’s argument is parsed; by default: when the `REPEAT` line is first reached at runtime).

**Semantics**
- `REPEAT` is implemented as a FOR-like loop over `COUNT:0`:
  - Initializes `COUNT:0` to `0`.
  - Uses `end = <countExpr>` and `step = 1`.
  - The loop continues while `COUNT:0 < end`.
- `COUNT:0` is incremented by `1` at `REND` time (and also by `BREAK`/`CONTINUE` for era-maker compatibility).
- Jump behavior note: control transfers between `REPEAT` and `REND` are done via their marker lines, and entering a marker line as a jump target begins execution at the following logical line:
  - Jumping to `REPEAT` re-enters at the first line of the body.
  - Jumping to `REND` exits to the first line after `REND`.

**Errors & validation**
- If the system variable `COUNT` is forbidden by the current variable-scope configuration, `REPEAT` raises an error when its argument is parsed (typically: first execution of the `REPEAT` line).
- If a constant count is `<= 0`, the engine emits a warning when the line’s argument is parsed.
- Nested `REPEAT` is warned about by the loader (not necessarily a hard error).

**Examples**
- `REPEAT 10`
- `  PRINTV COUNT`
- `REND`

## REND (instruction)

**Summary**
- Ends a `REPEAT ... REND` loop.

**Tags**
- control-flow

**Syntax**
- `REND`

**Arguments**
- None.

**Semantics**
- Increments the loop counter and decides whether to continue:
  - If more iterations remain, jumps back to the matching `REPEAT` marker (and thus continues at the first body line).
  - Otherwise falls through to the next line after `REND`.
- Engine quirk: if the loop counter state is missing (e.g. due to invalid jumps into/out of the loop), `REND` exits the loop instead of throwing.

**Errors & validation**
- `REND` without a matching open `REPEAT` is a load-time error (the line is marked as error).

**Examples**
- `REND`

## FOR (instruction)

**Summary**
- Begins a `FOR ... NEXT` counted loop over a mutable integer variable term.

**Tags**
- control-flow

**Syntax**
- `FOR <intVarTerm>, <start>, <end> [, <step>]`
  - `...`
  - `NEXT`

**Arguments**
- `<intVarTerm>`: changeable integer variable term (must not be character-data).
- `<start>` (optional, int; default `0`): initial counter value.
- `<end>`: int expression.
- `<step>` (optional, int; default `1`): increment applied at `NEXT` time.

**Semantics**
- Initializes the counter variable to `<start>`, then loops while:
  - `step > 0`: `<counter> < <end>`
  - `step < 0`: `<counter> > <end>`
- The counter variable is incremented by `step` at `NEXT` time (and also by `BREAK`/`CONTINUE` for era-maker compatibility).

**Errors & validation**
- Errors if `<intVarTerm>` is not a changeable variable term, or if it is character-data.
- `NEXT` without a matching open `FOR` is a load-time error (the `NEXT` line is marked as error).

**Examples**
- `FOR I, 0, 10`
- `  PRINTV I`
- `NEXT`

## NEXT (instruction)

**Summary**
- Ends a `FOR ... NEXT` loop.

**Tags**
- control-flow

**Syntax**
- `NEXT`

**Arguments**
- None.

**Semantics**
- Like `REND`, but paired with `FOR`.
- Increments the loop counter by `step`, then:
  - If more iterations remain, jumps back to the matching `FOR` marker (and continues at the first body line).
  - Otherwise falls through to the next line after `NEXT`.

**Errors & validation**
- `NEXT` without a matching open `FOR` is a load-time error (the line is marked as error).

**Examples**
- `NEXT`

## WHILE (instruction)

**Summary**
- Begins a `WHILE ... WEND` loop.

**Tags**
- control-flow

**Syntax**
- `WHILE <int expr>`
  - `...`
  - `WEND`

**Arguments**
- `<int expr>`: loop condition (0 = false, non-zero = true).

- Omitted arguments / defaults:
  - If omitted, the condition defaults to `0` (false) and emits a warning when the line’s argument is parsed (by default: when the `WHILE` line is first reached at runtime).

**Semantics**
- At `WHILE`, evaluates the condition:
  - If true, enters the body (next line).
  - If false, jumps to the matching `WEND` marker (exiting the loop).
- At `WEND`, the engine re-evaluates the `WHILE` condition and loops again if it is still true.

**Errors & validation**
- `WEND` without a matching open `WHILE` is a load-time error (the `WEND` line is marked as error).

**Examples**
- `WHILE I < 10`
- `  I += 1`
- `WEND`

## WEND (instruction)

**Summary**
- Ends a `WHILE ... WEND` loop.

**Tags**
- control-flow

**Syntax**
- `WEND`

**Arguments**
- None.

**Semantics**
- Re-evaluates the matching `WHILE` condition:
  - If true, jumps back to the `WHILE` marker (and continues at the first body line).
  - If false, falls through to the next line after `WEND`.

**Errors & validation**
- `WEND` without a matching open `WHILE` is a load-time error (the line is marked as error).

**Examples**
- `WEND`

## DO (instruction)

**Summary**
- Begins a `DO ... LOOP` loop.

**Tags**
- control-flow

**Syntax**
- `DO`
  - `...`
  - `LOOP <int expr>`

**Arguments**
- None.

**Semantics**
- Marker-only instruction (no runtime effect).
- The loader links the `DO` marker with its matching `LOOP` condition line.

**Errors & validation**
- `LOOP` without a matching open `DO` is a load-time error (the `LOOP` line is marked as error).

**Examples**
- `DO`
- `  I += 1`
- `LOOP I < 10`

## LOOP (instruction)

**Summary**
- Ends a `DO ... LOOP` loop and provides the loop condition.

**Tags**
- control-flow

**Syntax**
- `LOOP <int expr>`

**Arguments**
- `<int expr>`: loop condition (0 = false, non-zero = true).

- Omitted arguments / defaults:
  - If omitted, the condition defaults to `0` (false) and emits a load-time warning.

**Semantics**
- Evaluates the condition:
  - If true, jumps back to the matching `DO` marker (and continues at the first body line).
  - If false, falls through to the next line after `LOOP`.

**Errors & validation**
- `LOOP` without a matching open `DO` is a load-time error (the line is marked as error).

**Examples**
- `LOOP I < 10`

## CONTINUE (instruction)

**Summary**
- Skips to the next iteration of the nearest enclosing loop (`REPEAT`, `FOR`, `WHILE`, or `DO`).

**Tags**
- control-flow

**Syntax**
- `CONTINUE`

**Arguments**
- None.

**Semantics**
- The loader links `CONTINUE` to the nearest enclosing loop start marker.
- `REPEAT`/`FOR`: increments the loop counter by `step`, then either:
  - jumps back to the loop start marker (continue), or
  - jumps to the end marker (exit) if no iterations remain.
- `WHILE`: re-evaluates the condition and either continues or exits.
- `DO`: evaluates the matching `LOOP` condition and either continues or exits.

**Errors & validation**
- `CONTINUE` outside any loop is a load-time error (the line is marked as error).

**Examples**
- `CONTINUE`

## BREAK (instruction)

**Summary**
- Exits the nearest enclosing loop (`REPEAT`, `FOR`, `WHILE`, or `DO`).

**Tags**
- control-flow

**Syntax**
- `BREAK`

**Arguments**
- None.

**Semantics**
- The loader links `BREAK` to the nearest enclosing loop start marker.
- At runtime, `BREAK` jumps to that loop’s end marker (so execution continues after the loop).
- For `REPEAT`/`FOR`, the engine also increments the loop counter once on `BREAK` (era-maker compatibility quirk).

**Errors & validation**
- `BREAK` outside any loop is a load-time error (the line is marked as error).

**Examples**
- `BREAK`

## RETURN (instruction)

**Summary**
- Returns from the current function. Also assigns the integer `RESULT` array (`RESULT:0`, `RESULT:1`, ...) from the provided values.

**Tags**
- calls

**Syntax**
- `RETURN`
- `RETURN <int expr1> [, <int expr2>, <int expr3>, ... ]`

**Arguments**
- Each argument is evaluated as an integer and stored into `RESULT:<index>`.

- Omitted arguments / defaults:
  - With no arguments: sets `RESULT:0` to `0` and returns `0`.

**Semantics**
- Evaluates all provided integer expressions (left-to-right), stores them into the `RESULT` integer array starting at index 0, then returns from the function.
- The return value used by the call stack is `RESULT:0` after the assignment.
- The engine does not clear unused `RESULT:<index>` slots; old values past the written prefix may remain.
- Load-time diagnostics (non-fatal): the engine may emit compatibility warnings when `RETURN` is used with a non-constant expression/variable, or with multiple values.

**Errors & validation**
- Errors if any argument cannot be evaluated as an integer.

**Examples**
- `RETURN`
- `RETURN 0`
- `RETURN 1, 2, 3`

## RETURNFORM (instruction)

**Summary**
- Returns from the current function like `RETURN`, but parses its values from a FORM/formatted string.

**Tags**
- calls

**Syntax**
- `RETURNFORM <formString>`

**Arguments**
- `<formString>` is evaluated to a string `s`, then `s` is re-lexed as one or more **comma-separated integer expressions**.

- Omitted arguments / defaults:
  - If `s` is empty, the engine behaves like `RETURN 0`.

**Semantics**
- Evaluates the formatted string to a string `s`.
- Parses `s` as `expr1, expr2, ...` using the engine’s expression lexer/parser.
- Parsing detail: after each comma, the engine skips ASCII spaces (not tabs) before reading the next expression.
- Stores the resulting integer values into `RESULT:0`, `RESULT:1`, ... and returns.

**Errors & validation**
- Errors if any parsed expression is not a valid integer expression.

**Examples**
- `RETURNFORM 1, 2, %A%`

## RETURNF (instruction)

**Summary**
- Returns from a user-defined expression function (`#FUNCTION/#FUNCTIONS`) with an optional return value.

**Tags**
- calls

**Syntax**
- `RETURNF`
- `RETURNF <expr>`

**Arguments**
- `<expr>` may be int or string, but should match the function’s declared return type.

- Omitted arguments / defaults:
  - With no argument: returns the engine’s “null” method value (a null internal return term; typically treated as `0` / empty depending on context).

**Semantics**
- Sets the method return value for the current expression-function call and exits the method body.
- Load-time validation:
  - `RETURNF` outside a `#FUNCTION/#FUNCTIONS` body is a load-time error (the line is marked as error).
  - A return-type mismatch (`RETURNF` returns string from an int method, or int from a string method) is a load-time error.

**Errors & validation**
- Argument parsing errors follow normal expression parsing rules.

**Examples**
- `RETURNF 0`
- `RETURNF "OK"`

## STRLEN (instruction)

**Summary**
- Sets `RESULT` to the engine’s **language/encoding length** of a raw string argument.

**Tags**
- text

**Syntax**
- `STRLEN <rawString>`

**Arguments**
- `<rawString>`: the literal remainder of the line (not a normal string expression).

- Omitted arguments / defaults:
  - If omitted, the string defaults to `""`.

**Semantics**
- Computes length via the engine’s language-aware length counter and assigns it to `RESULT`:
  - For ASCII-only strings: equals `str.Length`.
  - Otherwise: equals the current configured encoding’s `GetByteCount(str)` (often Shift-JIS in typical setups).
- For normal expression-style string evaluation (quotes, `%...%`, `{...}`), use `STRLENFORM` instead.

**Errors & validation**
- None (apart from abnormal evaluation errors; the raw-string form is constant).

**Examples**
- `STRLEN ABC` sets `RESULT` to the byte length of `ABC` under the current encoding.

## STRLENFORM (instruction)

**Summary**
- Sets `RESULT` to the engine’s **language/encoding length** of a FORM/formatted string.

**Tags**
- text

**Syntax**
- `STRLENFORM <formString>`

**Arguments**
- `<formString>`: FORM/formatted string expression (supports `%...%` and `{...}`).

- Omitted arguments / defaults:
  - If omitted, the string defaults to `""`.

**Semantics**
- Evaluates the formatted string to a string value, then computes its language/encoding length (see `STRLEN` for details).
- Assigns the result to `RESULT`.

**Errors & validation**
- Errors if the formatted string evaluation fails.

**Examples**
- `STRLENFORM NAME=%NAME%` sets `RESULT` to the length of the expanded string.

## STRLENU (instruction)

**Summary**
- Sets `RESULT` to the Unicode code-unit length (`string.Length`) of a raw string argument.

**Tags**
- text

**Syntax**
- `STRLENU <rawString>`

**Arguments**
- `<rawString>`: the literal remainder of the line (not a normal string expression).

- Omitted arguments / defaults:
  - If omitted, the string defaults to `""`.

**Semantics**
- Computes length as `str.Length` and assigns it to `RESULT`.

**Errors & validation**
- None (apart from abnormal evaluation errors; the raw-string form is constant).

**Examples**
- `STRLENU ABC` sets `RESULT` to `3`.

## STRLENFORMU (instruction)

**Summary**
- Sets `RESULT` to the Unicode code-unit length (`string.Length`) of a FORM/formatted string.

**Tags**
- text

**Syntax**
- `STRLENFORMU <formString>`

**Arguments**
- `<formString>`: FORM/formatted string expression.

- Omitted arguments / defaults:
  - If omitted, the string defaults to `""`.

**Semantics**
- Evaluates the formatted string to a string value, then assigns `str.Length` to `RESULT`.

**Errors & validation**
- Errors if the formatted string evaluation fails.

**Examples**
- `STRLENFORMU NAME=%NAME%` sets `RESULT` to the character length of the expanded string.

## SWAPCHARA (instruction)
**Summary**
- (TODO: not yet documented)

## COPYCHARA (instruction)
**Summary**
- (TODO: not yet documented)

## ADDCOPYCHARA (instruction)

**Summary**
- Adds one or more new characters by copying an existing character’s data.

**Tags**
- characters

**Syntax**
- `ADDCOPYCHARA charaIndex`
- `ADDCOPYCHARA charaIndex1, charaIndex2, ...`

**Arguments**
- Each `charaIndex`: int expression selecting an existing character index to copy from.

**Semantics**
- Requires at least one argument; multiple arguments are accepted but the engine emits a parse-time warning for multi-argument uses.
- For each `charaIndex` (evaluated and executed left-to-right), the engine:
  - Validates the source index is in range; otherwise errors.
  - Appends a new pseudo character.
  - Copies all character data from the source character into the newly appended last character.
- `CHARANUM` increases by 1 for each successfully created copy.
- This instruction does not print anything and does not automatically change `TARGET`/`MASTER`/`ASSI`.

**Errors & validation**
- Runtime error if any `charaIndex` is out of range.

**Examples**
```erabasic
ADDCOPYCHARA 0
```

## SPLIT (instruction)
**Summary**
- (TODO: not yet documented)

## SETCOLOR (instruction)
**Summary**
- (TODO: not yet documented)

## SETCOLORBYNAME (instruction)
**Summary**
- (TODO: not yet documented)

## RESETCOLOR (instruction)
**Summary**
- (TODO: not yet documented)

## SETBGCOLOR (instruction)
**Summary**
- (TODO: not yet documented)

## SETBGIMAGE (instruction)
**Summary**
- (TODO: not yet documented)

## SETBGCOLORBYNAME (instruction)
**Summary**
- (TODO: not yet documented)

## RESETBGCOLOR (instruction)
**Summary**
- (TODO: not yet documented)

## CLEARBGIMAGE (instruction)
**Summary**
- (TODO: not yet documented)

## REMOVEBGIMAGE (instruction)
**Summary**
- (TODO: not yet documented)

## FONTBOLD (instruction)
**Summary**
- (TODO: not yet documented)

## FONTITALIC (instruction)
**Summary**
- (TODO: not yet documented)

## FONTREGULAR (instruction)
**Summary**
- (TODO: not yet documented)

## SORTCHARA (instruction)

**Summary**
- Reorders the engine’s character list (`0 .. CHARANUM-1`) by a key taken from a character-data variable.
- Observable behavior: keeps `MASTER` fixed at its numeric position for this instruction.

**Tags**
- characters

**Syntax**
- `SORTCHARA`
- `SORTCHARA FORWARD | BACK`
- `SORTCHARA <charaVarTerm> [ , FORWARD | BACK ]`

**Arguments**
- `<charaVarTerm>`: a variable term whose identifier is a character-data variable.
- Order: `FORWARD` = ascending, `BACK` = descending.
- If the key variable is an array, the element indices are taken from the variable term’s subscripts after the character selector.

- Omitted arguments / defaults:
  - If no args: uses key `NO` and ascending.

**Semantics**
- Computes a sort key for each character via the engine’s key setter; null strings are treated as empty string.
- Stable sort: ties are broken by original order.
- After sorting, `TARGET`/`ASSI` are updated to keep pointing at the same character objects; `MASTER` is kept at its fixed index.

**Errors & validation**
- Parse-time error if `<charaVarTerm>` is not a character-data variable term.
- Runtime error if selected element indices are out of range for the variable.

**Examples**
- `SORTCHARA NO`
- `SORTCHARA CFLAG:3, BACK`
- `SORTCHARA NAME, FORWARD`

## FONTSTYLE (instruction)
**Summary**
- (TODO: not yet documented)

## ALIGNMENT (instruction)
**Summary**
- (TODO: not yet documented)

## CUSTOMDRAWLINE (instruction)
**Summary**
- (TODO: not yet documented)

## DRAWLINEFORM (instruction)
**Summary**
- (TODO: not yet documented)

## CLEARTEXTBOX (instruction)
**Summary**
- (TODO: not yet documented)

## SETFONT (instruction)
**Summary**
- (TODO: not yet documented)

## SWAP (instruction)

**Summary**
- Swaps the values of two **changeable variables** (integer or string).

**Tags**
- variables

**Syntax**
- `SWAP <var1>, <var2>`

**Arguments**
- `<var1>`: a changeable variable term (must not be `CONST`).
- `<var2>`: a changeable variable term (same type as `<var1>`).

**Semantics**
- The engine first **fixes** both variable terms’ indices (important when indices contain expressions like `RAND`):
  - Each variable’s indices are evaluated once to create a “fixed variable term”.
  - All subsequent reads/writes in this instruction use those fixed indices.
- Type check:
  - If the two variables’ runtime operand types differ (integer vs string), the instruction errors.
- Swap:
  - For integer variables, swaps the two `long` values.
  - For string variables, swaps the two `string` values.

**Errors & validation**
- Argument parsing fails if either argument is not a changeable variable term.
- Errors if the two variables do not have the same type, or if a variable has an unknown/unsupported type.

**Examples**
- `SWAP A, B`
- `SWAP NAME:TARGET, NICKNAME:TARGET`

## RANDOMIZE (instruction)

**Summary**
- Seeds the legacy RNG with a specified integer seed.

**Tags**
- random

**Syntax**
- `RANDOMIZE`
- `RANDOMIZE <seed>`

**Arguments**
- `<seed>` (optional): integer expression. If omitted, the seed defaults to `0`.

- Omitted arguments / defaults:
  - `<seed>` defaults to `0`.

**Semantics**
- If `UseNewRandom` is enabled in JSON config:
  - Emits a warning and does nothing.
- Otherwise:
  - Re-seeds the legacy RNG with `<seed>` truncated to 32 bits (i.e. low 32 bits used as an unsigned seed).
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- None (besides normal integer-expression evaluation errors).

**Examples**
- `RANDOMIZE 0`
- `RANDOMIZE 12345`

## DUMPRAND (instruction)

**Summary**
- Dumps the engine’s legacy RNG state into the `RANDDATA` variable.

**Tags**
- random

**Syntax**
- `DUMPRAND`

**Arguments**
- None.

**Semantics**
- If `UseNewRandom` is enabled in JSON config:
  - Emits a warning and does nothing.
- Otherwise:
  - Writes the legacy RNG state into `RANDDATA`.
  - `RANDDATA` must have length 625; otherwise a runtime error is raised.
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- None.

**Examples**
- `DUMPRAND`

## INITRAND (instruction)

**Summary**
- Initializes the engine’s legacy RNG state from the `RANDDATA` variable.

**Tags**
- random

**Syntax**
- `INITRAND`

**Arguments**
- None.

**Semantics**
- If `UseNewRandom` is enabled in JSON config:
  - Emits a warning and does nothing.
- Otherwise:
  - Loads the legacy RNG state from `RANDDATA`.
  - `RANDDATA` must have length 625; otherwise a runtime error is raised.
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- None.

**Examples**
- `INITRAND`

## REDRAW (instruction)
**Summary**
- (TODO: not yet documented)

## CALLTRAIN (instruction)
**Summary**
- (TODO: not yet documented)

## STOPCALLTRAIN (instruction)
**Summary**
- (TODO: not yet documented)

## DOTRAIN (instruction)
**Summary**
- (TODO: not yet documented)

## DATA (instruction)

**Summary**
- Declares one printable choice inside a surrounding `PRINTDATA*` / `STRDATA` / `DATALIST` block.
- `DATA` lines are *not* intended to execute as standalone statements; they are consumed by the loader into the surrounding block’s data list.

**Tags**
- data-blocks

**Syntax**
- `DATA [<raw text>]`
- `DATA;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).
  - Parsing detail: as with most instructions, Emuera consumes exactly one delimiter character after the keyword (space/tab/full-width-space if enabled, or `;`). The remainder of the line becomes the raw text.

- Omitted arguments / defaults:
  - Omitted argument is treated as empty string.

**Semantics**
- At load time, the loader attaches `DATA` lines to the nearest surrounding block (`PRINTDATA*`, `STRDATA`, or `DATALIST`).
- At runtime, `PRINTDATA*` / `STRDATA` evaluate the stored `DATA` line as a string and print/concatenate it when selected.

**Errors & validation**
- Using `DATA` outside a valid surrounding block is a load-time error (the line is marked as error) and it will not participate in any `PRINTDATA*` / `STRDATA` selection.

**Examples**
```erabasic
PRINTDATA
  DATA Hello
  DATA;World
ENDDATA
```

## DATAFORM (instruction)

**Summary**
- Like `DATA`, but the text is a FORM/formatted string (scanned at load time).

**Tags**
- data-blocks

**Syntax**
- `DATAFORM [<FORM string>]`

**Arguments**
- Optional FORM/formatted string scanned to end-of-line.

- Omitted arguments / defaults:
  - Omitted argument is treated as empty string.

**Semantics**
- Stored into the surrounding `PRINTDATA*` / `STRDATA` / `DATALIST` data list at load time.
- When selected, evaluated to a string at runtime and printed/concatenated.
  - The FORM string is scanned at load time and stored as an expression that is evaluated later (so it can still depend on runtime variables).

**Errors & validation**
- Must appear inside a valid surrounding block; otherwise it is a load-time error (the line is marked as error).

**Examples**
```erabasic
PRINTDATA
  DATAFORM Hello, %NAME%!
ENDDATA
```

## ENDDATA (instruction)

**Summary**
- Closes a `PRINTDATA*` or `STRDATA` block.

**Tags**
- data-blocks

**Syntax**
- `ENDDATA`

**Arguments**
- None.

- Omitted arguments / defaults:
  - N/A.

**Semantics**
- Load-time only structural marker. At runtime it does nothing.
- The loader wires `PRINTDATA*` / `STRDATA` to jump here after printing/selection.

**Errors & validation**
- `ENDDATA` without an open `PRINTDATA*` / `STRDATA` is a load-time error (the line is marked as error).
- Closing a block while a `DATALIST` is still open is a load-time error.

**Examples**
- (See `PRINTDATA`.)

## DATALIST (instruction)

**Summary**
- Starts a **multi-line** choice list inside a surrounding `PRINTDATA*` or `STRDATA` block.
- Each `DATA` / `DATAFORM` inside the list becomes a separate output line when this choice is selected.

**Tags**
- data-blocks

**Syntax**
- `DATALIST`
  - `DATA ...` / `DATAFORM ...` (one or more)
- `ENDLIST`

**Arguments**
- None.

- Omitted arguments / defaults:
  - N/A.

**Semantics**
- At load time, the loader accumulates contained `DATA` / `DATAFORM` lines into a single list entry and attaches it to the surrounding `PRINTDATA*` / `STRDATA` block.

**Errors & validation**
- `DATALIST` must appear inside `PRINTDATA*` or `STRDATA`; otherwise it is a load-time error (the line is marked as error).
- Missing `ENDLIST` produces a load-time error at end of file/load.
- An empty list produces a non-fatal loader warning, but still creates an empty choice entry.

**Examples**
```erabasic
PRINTDATA
  DATALIST
    DATA Line 1
    DATA Line 2
  ENDLIST
ENDDATA
```

## ENDLIST (instruction)

**Summary**
- Closes a `DATALIST` block.

**Tags**
- data-blocks

**Syntax**
- `ENDLIST`

**Arguments**
- None.

- Omitted arguments / defaults:
  - N/A.

**Semantics**
- Load-time only structural marker. At runtime it does nothing.

**Errors & validation**
- `ENDLIST` without an open `DATALIST` is a load-time error (the line is marked as error).

**Examples**
- (See `DATALIST`.)

## STRDATA (instruction)

**Summary**
- Like `PRINTDATA`, but instead of printing, it selects a `DATA`/`DATAFORM` choice and concatenates it into a destination string variable.

**Tags**
- data-blocks

**Syntax**
- `STRDATA [<strVarTerm>]` ... `ENDDATA`

**Arguments**
- Optional `<strVarTerm>`: changeable string variable term to receive the result.
- If omitted, defaults to `RESULTS`.

- Omitted arguments / defaults:
  - Destination defaults to `RESULTS` when omitted.

**Semantics**
- Shares the same block structure as `PRINTDATA` (`DATA`, `DATAFORM`, `DATALIST`, `ENDDATA`).
- Selects one entry uniformly at random.
- Concatenates the selected lines with `\n` between them (for `DATALIST` multi-line entries).
- Stores the result into the destination variable and jumps to `ENDDATA`.
- If the block contains no `DATA`/`DATAFORM` choices at all, it simply jumps to `ENDDATA` and does **not** assign anything to the destination variable (it remains unchanged).

**Errors & validation**
- The destination must be a changeable string variable term.
- Same structural diagnostics as `PRINTDATA`.

**Examples**
```erabasic
STRDATA
  DATA Hello
  DATA World
ENDDATA
PRINTFORML RESULTS
```

## SETBIT (instruction)
**Summary**
- (TODO: not yet documented)

## CLEARBIT (instruction)
**Summary**
- (TODO: not yet documented)

## INVERTBIT (instruction)
**Summary**
- (TODO: not yet documented)

## DELALLCHARA (instruction)
**Summary**
- (TODO: not yet documented)

## PICKUPCHARA (instruction)
**Summary**
- (TODO: not yet documented)

## VARSET (instruction)
**Summary**
- (TODO: not yet documented)

## CVARSET (instruction)
**Summary**
- (TODO: not yet documented)

## RESET_STAIN (instruction)
**Summary**
- (TODO: not yet documented)

## FORCEKANA (instruction)
**Summary**
- (TODO: not yet documented)

## SKIPDISP (instruction)

**Summary**
- Enables/disables the engine’s “skip output” mode, which causes most print/wait/input built-ins to be skipped.
- Also sets `RESULT` to indicate whether skip mode is currently enabled.

**Tags**
- skip-mode

**Syntax**
- `SKIPDISP <int expr>`

**Arguments**
- `<int expr>`: `0` disables skip mode; non-zero enables skip mode.

**Semantics**
- Evaluates `<int expr>` to `v`.
- If `v != 0`, enables output skipping; otherwise disables it.
- Sets `RESULT` to:
  - `1` when output skipping is enabled
  - `0` when output skipping is disabled
- While output skipping is enabled, the script runner skips most output-producing instructions (print/wait/input families).
- Special case (runtime error): if output skipping was enabled by `SKIPDISP`, then encountering an input instruction (e.g. `INPUT*`) raises an error rather than being silently skipped.

**Errors & validation**
- Argument type errors follow the normal integer-expression argument rules.
- Runtime error if an input instruction is reached while output skipping is active due to `SKIPDISP`.

**Examples**
- `SKIPDISP 1` (enable skip)
- `SKIPDISP 0` (disable skip)

## NOSKIP (instruction)

**Summary**
- Begins a `NOSKIP ... ENDNOSKIP` block that temporarily disables output skipping within the block body.
- Intended to force some output/wait behavior to run even if `SKIPDISP` is currently skipping print-family instructions.

**Tags**
- skip-mode

**Syntax**
- `NOSKIP`
  - `...`
- `ENDNOSKIP`

**Arguments**
- None.

**Semantics**
- This is a structural block (`NOSKIP` pairs with `ENDNOSKIP`).
- At runtime when `NOSKIP` is executed:
  - If the matching `ENDNOSKIP` was not linked by the loader, the engine throws an error.
  - Remembers whether output skipping is currently enabled.
  - If output skipping is currently enabled, disables it for the duration of the block.
- At runtime when `ENDNOSKIP` is executed:
  - If output skipping was enabled at block entry, re-enables it (restoring skip mode).
  - If output skipping was disabled at block entry, does nothing (so if you enabled skip inside the block manually, it remains enabled).

**Errors & validation**
- Load-time structure errors (the line is marked as error):
  - Nested `NOSKIP` is not allowed.
  - `ENDNOSKIP` without a matching open `NOSKIP` is an error.
  - Missing `ENDNOSKIP` at end of file/load is an error.
- Runtime error if the loader failed to link the matching `ENDNOSKIP` (should not happen in a successfully loaded script).

**Examples**
```erabasic
SKIPDISP 1

NOSKIP
  PRINTL This line still prints even during SKIPDISP.
ENDNOSKIP
```

## ENDNOSKIP (instruction)

**Summary**
- Ends a `NOSKIP ... ENDNOSKIP` block.

**Tags**
- skip-mode

**Syntax**
- `ENDNOSKIP`

**Arguments**
- None.

**Semantics**
- Structural marker paired with `NOSKIP`.
- See `NOSKIP` for the block’s runtime behavior (temporary disabling and restoration of output skipping).

**Errors & validation**
- `ENDNOSKIP` without a matching open `NOSKIP` is a load-time error (the line is marked as error).

**Examples**
- (See `NOSKIP`.)

## ARRAYSHIFT (instruction)

**Summary**
- Shifts elements in a mutable 1D array variable by a signed offset and fills new slots with a default value.

**Tags**
- arrays

**Syntax**
- `ARRAYSHIFT <arrayVar>, <shift>, <default> [, <start> [, <count>]]`

**Arguments**
- `<arrayVar>`: changeable 1D array variable term.
- `<shift>`: int expression.
- `<default>`: expression of the same scalar type as the array element type.
- `<start>`: int expression (default `0`).
- `<count>`: int expression (default “to end”; engine uses a sentinel).

- Omitted arguments / defaults:
  - `<start>` defaults to `0`.
  - `<count>` omitted means “to the end”.

**Semantics**
- Operates on the segment `[start, start+count)` (or `[start, end)` if count omitted).
- If `shift == 0`, does nothing.
- If shifting removes all overlap, fills the whole segment with `<default>`.
- If `start + count` exceeds array length, the engine clamps `count` to fit.

**Errors & validation**
- Errors if `<arrayVar>` is not 1D, if `start < 0`, if `count < 0` (when provided), or if `start >= arrayLength`.

**Examples**
- `ARRAYSHIFT SOME_INT_ARRAY, 1, 0`
- `ARRAYSHIFT SOME_STR_ARRAY, -2, "", 10`

## ARRAYREMOVE (instruction)

**Summary**
- Removes a slice of elements from a mutable 1D array by shifting later elements left and filling the tail with default values.

**Tags**
- arrays

**Syntax**
- `ARRAYREMOVE <arrayVar>, <start>, <count>`

**Arguments**
- `<arrayVar>`: changeable 1D array variable term.
- `<start>`: integer expression; start index (0-based).
- `<count>`: integer expression; number of elements to remove.

**Semantics**
- Works only on 1D arrays (int or string).
- Removes elements in the conceptual range `[start, start+count)`:
  - Elements after the removed segment are shifted left into the gap.
  - The remaining tail is filled with defaults:
    - int arrays: `0`
    - string arrays: `null` internally (typically observed as empty string in many contexts)
- Special case: if `<count> <= 0`, the engine treats it as “remove to the end” (it effectively clears the suffix starting at `<start>`).
- If `<start> + <count>` exceeds the array length, it behaves like removing to the end.

**Errors & validation**
- Runtime errors:
  - `<start> < 0`
  - `<start> >= array length`
  - `<arrayVar>` is not a 1D array

**Examples**
- `ARRAYREMOVE A, 0, 1` (drop first element)
- `ARRAYREMOVE A, 10, -1` (clear suffix from index 10)

## ARRAYSORT (instruction)

**Summary**
- Sorts a mutable 1D array in ascending or descending order, optionally within a subrange.

**Tags**
- arrays

**Syntax**
- Minimal form:
  - `ARRAYSORT <arrayVar>`
- With explicit order (required for subrange arguments):
  - `ARRAYSORT <arrayVar>, FORWARD|BACK [, <start> [, <count>]]`

**Arguments**
- `<arrayVar>`: changeable 1D array variable term (int or string).
- `FORWARD|BACK`:
  - `FORWARD`: ascending
  - `BACK`: descending
- `<start>` (optional): integer expression; default `0`.
- `<count>` (optional): integer expression; if omitted, sorts to end.

- Omitted arguments / defaults:
  - If `FORWARD|BACK` is omitted, order defaults to ascending and the engine does not accept `<start>/<count>` (parsing quirk).
  - `<start>` defaults to `0` when `FORWARD|BACK` is present but no subrange is provided.
  - `<count>` omitted means “to the end”.

**Semantics**
- Sorts the specified region of the array:
  - The runtime treats `count <= 0` as “to the end” (but an explicitly provided `count == 0` is handled as a no-op in the instruction dispatcher).
- Parsing rule:
  - `<start>` and `<count>` are only accepted when the `FORWARD|BACK` token is present.

**Errors & validation**
- Parse-time errors if:
  - `<arrayVar>` is not a changeable 1D array variable term
  - the order token is present but not `FORWARD` or `BACK`
  - `<start>/<count>` are provided but are not integers
- Runtime errors if:
  - `<start> < 0`
  - `<start> >= array length`
  - `<start> + <count>` exceeds array length (when `<count>` is provided and positive)

**Examples**
- `ARRAYSORT A`
- `ARRAYSORT A, BACK`
- `ARRAYSORT A, FORWARD, 10, 20` (sort subrange)

## ARRAYCOPY (instruction)

**Summary**
- Copies elements from one array variable to another array variable of the same element type and dimension.

**Tags**
- arrays

**Syntax**
- `ARRAYCOPY <srcVarNameExpr>, <dstVarNameExpr>`

**Arguments**
- `<srcVarNameExpr>`: string expression whose value is a variable name.
- `<dstVarNameExpr>`: string expression whose value is a variable name.

**Semantics**
- Resolves both variable names to variable tokens (early when literal, otherwise at runtime).
- Requires both to be arrays (1D/2D/3D), non-character-data; destination must be non-const.
- Copies element-wise:
  - If array sizes differ, only the overlapping region is copied (per dimension); there is no error for size mismatch.
  - Elements outside the copied region in the destination are left unchanged.

**Errors & validation**
- Errors if a name does not resolve to a variable, if either is not an array, if either is character-data, if destination is const, or if dimension/type mismatch.

**Examples**
- `ARRAYCOPY "ABL", "ABL_BAK"`
- `ARRAYCOPY "ITEM", SAVETO`

## SKIPLOG (instruction)

**Summary**
- Sets the console’s “message skip” flag (`MesSkip`), which affects UI-side input handling and macro/skip behavior.
- This is **not** the same mechanism as `SKIPDISP` (which skips print-family instructions in the script runner).

**Tags**
- skip-mode

**Syntax**
- `SKIPLOG <int expr>`

**Arguments**
- `<int expr>`: `0` clears message-skip; non-zero enables message-skip.

**Semantics**
- Evaluates `<int expr>` to `v`.
- Sets the message-skip flag `MesSkip` to `(v != 0)`.
- Implementation-oriented effect (UI-side):
  - When `MesSkip` is true, the input loop may automatically advance through waits that do not require a value, unless the current wait request explicitly stops message skip.
  - Some input instructions (`INPUT*`/`TINPUT*`) have a `canSkip` option that uses `MesSkip` to auto-accept their default value without waiting.

**Errors & validation**
- Argument type errors follow the normal integer-expression argument rules.

**Examples**
- `SKIPLOG 1`
- `SKIPLOG 0`

## JUMP (instruction)

**Summary**
- Jumps into another non-event function (`@NAME`) like `CALL`, but does not return to the current function.

**Tags**
- calls

**Syntax**
- `JUMP <functionName> [, <arg1>, <arg2>, ... ]`
- `JUMP <functionName>(<arg1>, <arg2>, ... )`

**Arguments**
- Same as `CALL`.

- Omitted arguments / defaults:
  - Same as `CALL`.

**Semantics**
- Enters the target function.
- When the target function returns, the engine immediately returns again, effectively discarding the current function’s return address (tail-call-like behavior).

**Errors & validation**
- Same as `CALL`.

**Examples**
- `JUMP NEXT_PHASE`

## CALL (instruction)

**Summary**
- Calls a non-event script function (`@NAME`) and returns to the next line after the `CALL` when the callee returns.

**Tags**
- calls

**Syntax**
- `CALL <functionName> [, <arg1>, <arg2>, ... ]`
- `CALL <functionName>(<arg1>, <arg2>, ... )`
- Optional (currently unused) bracket segment may appear after the function name:
  - `CALL <functionName>[<subName1>, <subName2>, ...](...)`

**Arguments**
- `<functionName>`: a raw string token read up to `(` / `[` / `,` / `;` and then trimmed.
- This is **not** a string literal. Quotes are treated as ordinary characters.
- Backslash escapes are processed (e.g. `\\n`, `\\t`, `\\s`).
- `<argN>`: expressions passed to the callee and bound to its `ARG`/`ARGS`-based parameters and/or `#FUNCTION` parameter declarations.

- Omitted arguments / defaults:
  - If the callee declares more parameters than provided arguments, omitted arguments are handled by the engine’s user-function argument binder (defaults and config gates apply).

**Semantics**
- Resolves the target label to a non-event function.
  - If `CompatiCallEvent` is enabled, an event function name is also callable via `CALL` (compatibility behavior: it calls only the first-defined function, ignoring event priority/single flags).
- Evaluates arguments, binds them to the callee’s declared formals (including `REF` behavior), then enters the callee.
- When the callee executes `RETURN` (or reaches end-of-function), control returns to the statement after the `CALL`.
- Load-time behavior: if `<functionName>` is a compile-time constant, the loader tries to resolve the callee and may emit early diagnostics (e.g. unknown function, argument binding issues).

**Errors & validation**
- If `<functionName>` is a constant string:
  - Non-`TRY*` variants: an unknown function is a load-time error (the line is marked as error).
  - `TRY*` variants: an unknown function is allowed (the line is not marked as error).
- Errors if the function exists but is not callable by `CALL`:
  - event function name when `CompatiCallEvent` is disabled
  - user-defined expression function (`#FUNCTION/#FUNCTIONS`)
- Errors if argument binding fails (too many args, omitted required args, type conversion not permitted, invalid `REF` binding, etc.).

**Examples**
- `CALL TRAIN_MAIN, TARGET`
- `CALL SHOP_MAIN()`

## TRYJUMP (instruction)

**Summary**
- Like `JUMP`, but if the target function does not exist the instruction **does not error** and simply falls through to the next line.

**Tags**
- calls

**Syntax**
- `TRYJUMP <functionName> [, <arg1>, <arg2>, ... ]`
- `TRYJUMP <functionName>(<arg1>, <arg2>, ... )`

**Arguments**
- Same as `JUMP`.

- Omitted arguments / defaults:
  - Same as `JUMP`.

**Semantics**
- If the target function exists: behaves like `JUMP`.
- If the target function does not exist: does nothing (continues at the next line after `TRYJUMP`).

**Errors & validation**
- Still errors for invalid argument binding/type conversion when a function is found.

**Examples**
- `TRYJUMP OPTIONAL_PHASE`

## TRYCALL (instruction)

**Summary**
- Like `CALL`, but if the target function does not exist the instruction **does not error** and simply falls through to the next line.

**Tags**
- calls

**Syntax**
- `TRYCALL <functionName> [, <arg1>, <arg2>, ... ]`
- `TRYCALL <functionName>(<arg1>, <arg2>, ... )`

**Arguments**
- Same as `CALL`.

- Omitted arguments / defaults:
  - Same as `CALL`.

**Semantics**
- If the target function exists: behaves like `CALL`.
- If the target function does not exist: does nothing (continues at the next line after `TRYCALL`).

**Errors & validation**
- Still errors for invalid argument binding/type conversion when a function is found.

**Examples**
- `TRYCALL OPTIONAL_HOOK`

## JUMPFORM (instruction)

**Summary**
- Like `JUMP`, but the function name is a formatted (FORM) string expression evaluated at runtime.

**Tags**
- calls

**Syntax**
- `JUMPFORM <formString> [, <arg1>, <arg2>, ... ]`
- `JUMPFORM <formString>(<arg1>, <arg2>, ... )`

**Arguments**
- Same as `CALLFORM`.

- Omitted arguments / defaults:
  - Same as `CALLFORM`.

**Semantics**
- Same as `JUMP`, with a runtime-evaluated function name.

**Errors & validation**
- Same as `JUMP`, but errors may occur at runtime if the evaluated function name varies.

**Examples**
- `JUMPFORM "EVENT_%COUNT%"`

## CALLFORM (instruction)

**Summary**
- Like `CALL`, but the function name is a formatted (FORM) string expression evaluated at runtime.

**Tags**
- calls

**Syntax**
- `CALLFORM <formString> [, <arg1>, <arg2>, ... ]`
- `CALLFORM <formString>(<arg1>, <arg2>, ... )`

**Arguments**
- `<formString>`: FORM/formatted string; the evaluated result is used as the function name.
  - If this FORM expression constant-folds to a constant string, the engine treats it like `CALL` for load-time resolution.
- `<argN>`: same as `CALL`.

- Omitted arguments / defaults:
  - Same as `CALL`.

**Semantics**
- Evaluates the function name string, resolves it to a non-event function, binds arguments, and enters the callee.

**Errors & validation**
- Same as `CALL`, but errors may occur at runtime if the evaluated function name varies.

**Examples**
- `CALLFORM "TRAIN_%TARGET%", TARGET`

## TRYJUMPFORM (instruction)

**Summary**
- Like `JUMPFORM`, but if the evaluated function name does not resolve to a function the instruction **does not error** and simply falls through.

**Tags**
- calls

**Syntax**
- `TRYJUMPFORM <formString> [, <arg1>, <arg2>, ... ]`
- `TRYJUMPFORM <formString>(<arg1>, <arg2>, ... )`

**Arguments**
- Same as `JUMPFORM`.

- Omitted arguments / defaults:
  - Same as `JUMPFORM`.

**Semantics**
- If the target function exists: behaves like `JUMPFORM`.
- If not: does nothing (continues at the next line after `TRYJUMPFORM`).

**Errors & validation**
- Still errors for invalid argument binding/type conversion when a function is found.

**Examples**
- `TRYJUMPFORM "OPTIONAL_%COUNT%"`

## TRYCALLFORM (instruction)

**Summary**
- Like `CALLFORM`, but if the evaluated function name does not resolve to a function the instruction **does not error** and simply falls through.

**Tags**
- calls

**Syntax**
- `TRYCALLFORM <formString> [, <arg1>, <arg2>, ... ]`
- `TRYCALLFORM <formString>(<arg1>, <arg2>, ... )`

**Arguments**
- Same as `CALLFORM`.

- Omitted arguments / defaults:
  - Same as `CALLFORM`.

**Semantics**
- If the target function exists: behaves like `CALLFORM`.
- If not: does nothing (continues at the next line after `TRYCALLFORM`).

**Errors & validation**
- Still errors for invalid argument binding/type conversion when a function is found.

**Examples**
- `TRYCALLFORM "HOOK_%TARGET%"`

## TRYCJUMP (instruction)

**Summary**
- Like `TRYJUMP`, but supports a `CATCH ... ENDCATCH` block for the “not found” case.

**Tags**
- calls

**Syntax**
- `TRYCJUMP <functionName> [, <arg1>, ... ]`
- `CATCH`
  - `<catch body>`
  - `ENDCATCH`

**Arguments**
- Same as `JUMP`.

- Omitted arguments / defaults:
  - Same as `JUMP`.

**Semantics**
- If the target function exists: behaves like `JUMP` (tail-call-like); the current function is discarded, so it does not return to reach `CATCH`.
- If the function does not exist: jumps to the `CATCH` marker (entering the catch body).

**Errors & validation**
- Still errors for invalid argument binding/type conversion when a function is found.

**Examples**
- `TRYCJUMP OPTIONAL_PHASE`
- `CATCH`
- `  PRINTL "phase missing"`
- `ENDCATCH`

## TRYCCALL (instruction)

**Summary**
- Like `TRYCALL`, but supports a `CATCH ... ENDCATCH` block for the “not found” case.

**Tags**
- calls

**Syntax**
- `TRYCCALL <functionName> [, <arg1>, ... ]`
- `CATCH`
  - `<catch body>`
  - `ENDCATCH`

**Arguments**
- Same as `CALL`.

- Omitted arguments / defaults:
  - Same as `CALL`.

**Semantics**
- If the target function exists: behaves like `CALL`, then control returns and reaches `CATCH` sequentially; `CATCH` skips the catch body.
- If the function does not exist: jumps to the `CATCH` marker (so execution begins at the first line of the catch body).

**Errors & validation**
- Still errors for invalid argument binding/type conversion when a function is found.
- Mis-nesting (`CATCH` without `TRYC*`, `ENDCATCH` without `CATCH`) is a load-time error (the line is marked as error).

**Examples**
- `TRYCCALL OPTIONAL_HOOK`
- `CATCH`
- `  PRINTL "hook missing"`
- `ENDCATCH`

## TRYCJUMPFORM (instruction)

**Summary**
- Like `TRYJUMPFORM`, but supports a `CATCH ... ENDCATCH` block for the “not found” case.

**Tags**
- calls

**Syntax**
- `TRYCJUMPFORM <formString> [, <arg1>, ... ]`
- `CATCH`
  - `<catch body>`
  - `ENDCATCH`

**Arguments**
- Same as `JUMPFORM`.

- Omitted arguments / defaults:
  - Same as `JUMPFORM`.

**Semantics**
- Same as `TRYCJUMP`, but with a runtime-evaluated function name.

**Errors & validation**
- Same as `TRYCJUMP`.

**Examples**
- `TRYCJUMPFORM "OPTIONAL_%COUNT%"`
- `CATCH`
- `  PRINTL "missing"`
- `ENDCATCH`

## TRYCCALLFORM (instruction)

**Summary**
- Like `TRYCALLFORM`, but supports a `CATCH ... ENDCATCH` block for the “not found” case.

**Tags**
- calls

**Syntax**
- `TRYCCALLFORM <formString> [, <arg1>, ... ]`
- `CATCH`
  - `<catch body>`
  - `ENDCATCH`

**Arguments**
- Same as `CALLFORM`.

- Omitted arguments / defaults:
  - Same as `CALLFORM`.

**Semantics**
- Same as `TRYCCALL`, but with a runtime-evaluated function name.

**Errors & validation**
- Same as `TRYCCALL`.

**Examples**
- `TRYCCALLFORM "HOOK_%TARGET%"`
- `CATCH`
- `  PRINTL "hook missing"`
- `ENDCATCH`

## CALLEVENT (instruction)
**Summary**
- (TODO: not yet documented)

## CALLF (instruction)

**Summary**
- Calls an expression function (built-in method or user-defined `#FUNCTION/#FUNCTIONS`) by name and evaluates it as a statement.

**Tags**
- calls

**Syntax**
- `CALLF <methodName> [, <arg1>, <arg2>, ... ]`
- `CALLF <methodName>(<arg1>, <arg2>, ... )`

**Arguments**
- `<methodName>`: a raw string token read up to `(` / `[` / `,` / `;` and then trimmed.
- `<argN>`: expressions passed to the method.

- Omitted arguments / defaults:
  - Depends on the called method’s own signature rules (omission/variadics/etc.).

**Semantics**
- Resolves `<methodName>` to an expression function and evaluates it with the provided arguments.
- The return value is computed but not assigned to `RESULT/RESULTS` by this instruction (use statement-form method calls or assignment if you need the value).

**Errors & validation**
- If `<methodName>` is a constant string: unknown methods are a load-time error (the line is marked as error).
- Errors if the method exists but argument checking fails.

**Examples**
- `CALLF MYFUNC, 1, 2`

## CALLFORMF (instruction)

**Summary**
- Like `CALLF`, but the method name is a formatted (FORM) string expression evaluated at runtime.

**Tags**
- calls

**Syntax**
- `CALLFORMF <formString> [, <arg1>, <arg2>, ... ]`
- `CALLFORMF <formString>(<arg1>, <arg2>, ... )`

**Arguments**
- `<formString>`: FORM/formatted string; the evaluated result is used as the method name.
- `<argN>`: expressions passed to the method.

- Omitted arguments / defaults:
  - Depends on the called method’s own signature rules.

**Semantics**
- Resolves the evaluated name to an expression function and evaluates it.
- The return value is computed but not assigned to `RESULT/RESULTS` by this instruction.

**Errors & validation**
- Errors if the method does not exist or if argument checking fails.

**Examples**
- `CALLFORMF "FUNC_%X%", A, B`

## CALLSHARP (instruction)
**Summary**
- (TODO: not yet documented)

## RESTART (instruction)
**Summary**
- (TODO: not yet documented)

## GOTO (instruction)

**Summary**
- Jumps to a local `$label` within the current function.

**Tags**
- calls

**Syntax**
- `GOTO <labelName>`

**Arguments**
- `<labelName>`: a raw string token; used to resolve a `$label` relative to the current function.

**Semantics**
- If the label exists, jumps to the `$label` marker; execution continues at the line after the `$label`.
- The parser accepts `(...)` / comma forms, but `GOTO` does not use argument lists; only the label name matters.

**Errors & validation**
- If the label name is a constant string and the label is missing:
  - Non-`TRY*` variants: load-time error (the line is marked as error).
  - `TRY*` variants: allowed; the instruction becomes a no-op at runtime.
- If the label name is computed at runtime (e.g. `GOTOFORM`) and the label is missing:
  - Non-`TRY*` variants: runtime error.
  - `TRY*` variants: no-op (or enters `CATCH` for `TRYC*` variants).
- Invalid label definitions are errors even for `TRY*` variants.

**Examples**
- `GOTO LOOP_START`

## TRYGOTO (instruction)

**Summary**
- Like `GOTO`, but if the target `$label` does not exist the instruction **does not error** and simply falls through.

**Tags**
- calls

**Syntax**
- `TRYGOTO <labelName>`

**Arguments**
- Same as `GOTO`.

**Semantics**
- If the `$label` exists: behaves like `GOTO`.
- If not: does nothing (continues at the next line after `TRYGOTO`).

**Errors & validation**
- Still errors if the label exists but is invalid.

**Examples**
- `TRYGOTO OPTIONAL_LABEL`

## GOTOFORM (instruction)

**Summary**
- Like `GOTO`, but the label name is a formatted (FORM) string expression evaluated at runtime.

**Tags**
- calls

**Syntax**
- `GOTOFORM <formString>`

**Arguments**
- `<formString>`: FORM/formatted string; the evaluated result is used as the `$label` name.

**Semantics**
- Evaluates the label name and jumps if it resolves to a `$label` in the current function.

**Errors & validation**
- Same as `GOTO`, but errors may occur at runtime if the evaluated label name varies.

**Examples**
- `GOTOFORM "CASE_%RESULT%"`

## TRYGOTOFORM (instruction)

**Summary**
- Like `GOTOFORM`, but if the evaluated `$label` name does not exist the instruction **does not error** and simply falls through.

**Tags**
- calls

**Syntax**
- `TRYGOTOFORM <formString>`

**Arguments**
- Same as `GOTOFORM`.

**Semantics**
- If the `$label` exists: behaves like `GOTOFORM`.
- If not: does nothing (continues at the next line after `TRYGOTOFORM`).

**Errors & validation**
- Still errors if the label exists but is invalid.

**Examples**
- `TRYGOTOFORM "LABEL_%RESULT%"`

## TRYCGOTO (instruction)

**Summary**
- Like `TRYGOTO`, but supports a `CATCH ... ENDCATCH` block for the “not found” case.

**Tags**
- calls

**Syntax**
- `TRYCGOTO <labelName>`
- `CATCH`
  - `<catch body>`
  - `ENDCATCH`

**Arguments**
- Same as `GOTO`.

**Semantics**
- If the `$label` exists: behaves like `GOTO` (jumps to the label). Whether the `CATCH` line is ever reached depends on subsequent control flow.
- If the `$label` does not exist: jumps to the `CATCH` marker (entering the catch body).

**Errors & validation**
- Mis-nesting (`CATCH` without `TRYC*`, `ENDCATCH` without `CATCH`) is a load-time error (the line is marked as error).

**Examples**
- `TRYCGOTO OPTIONAL_LABEL`
- `CATCH`
- `  PRINTL "label missing"`
- `ENDCATCH`

## TRYCGOTOFORM (instruction)

**Summary**
- Like `TRYGOTOFORM`, but supports a `CATCH ... ENDCATCH` block for the “not found” case.

**Tags**
- calls

**Syntax**
- `TRYCGOTOFORM <formString>`
- `CATCH`
  - `<catch body>`
  - `ENDCATCH`

**Arguments**
- Same as `GOTOFORM`.

**Semantics**
- Same as `TRYCGOTO`, but with a runtime-evaluated label name.

**Errors & validation**
- Same as `TRYCGOTO`.

**Examples**
- `TRYCGOTOFORM "LABEL_%RESULT%"`
- `CATCH`
- `  PRINTL "label missing"`
- `ENDCATCH`

## CATCH (instruction)

**Summary**
- Begins the catch-body of a `TRYC* ... CATCH ... ENDCATCH` construct.

**Tags**
- error-handling

**Syntax**
- `CATCH`
  - `<catch body>`
  - `ENDCATCH`

**Arguments**
- None.

**Semantics**
- When reached **sequentially** (i.e. the `TRYC*` succeeded and returned normally), `CATCH` jumps to the matching `ENDCATCH` marker, skipping the catch body.
- When entered by a failed `TRYC*` instruction, execution jumps to the `CATCH` marker and (due to the engine’s advance-first model) begins executing at the first line of the catch body.

**Errors & validation**
- `CATCH` without a matching open `TRYC*` is a load-time error (the line is marked as error).

**Examples**
- `CATCH`
- `  PRINTL "not found"`
- `ENDCATCH`

## ENDCATCH (instruction)

**Summary**
- Ends a `CATCH ... ENDCATCH` block.

**Tags**
- error-handling

**Syntax**
- `ENDCATCH`

**Arguments**
- None.

**Semantics**
- Marker-only instruction (no runtime effect). The loader links it to the matching `CATCH` so that `CATCH` can skip the catch body on the success path.

**Errors & validation**
- `ENDCATCH` without a matching open `CATCH` is a load-time error (the line is marked as error).

**Examples**
- `ENDCATCH`

## TRYCALLLIST (instruction)

**Summary**
- Tries a list of candidate non-event functions and `CALL`s the first one that exists; otherwise skips the block.

**Tags**
- calls

**Syntax**
- `TRYCALLLIST`
  - `FUNC <formString> [, <arg1>, <arg2>, ... ]`
  - `FUNC <formString>(<arg1>, <arg2>, ... )`
  - `...`
  - `ENDFUNC`

**Arguments**
- None on `TRYCALLLIST` itself.
- Each `FUNC` item provides:
  - a candidate function name as a **FORM/formatted string expression** (evaluated to a string at runtime)
  - optional call arguments (expressions)

**Semantics**
- Structural notes:
  - The lines between `TRYCALLLIST` and `ENDFUNC` are **list items**, not a normal executable block body.
  - Emuera stores the `FUNC` lines into an internal `callList` during load, and executes only `TRYCALLLIST` at runtime.
- Runtime algorithm:
  - For each `FUNC` item in source order:
    - Evaluate the candidate name to a string.
    - If no non-event `@function` with that name exists, try the next item.
    - Otherwise, bind arguments and enter that function (like `CALL`).
      - When the callee returns, execution resumes at the `ENDFUNC` line (then continues after it).
  - If no candidate matches, jump directly to the `ENDFUNC` line (then continue after it).
- `FUNC` syntax matches `CALLFORM`: candidate name is a FORM string; arguments are normal expressions.

**Errors & validation**
- Load-time structure errors (the line is marked as error):
  - `TRYCALLLIST` cannot be nested inside another `TRY*LIST` block.
  - Only `FUNC` and `ENDFUNC` are allowed between `TRYCALLLIST` and `ENDFUNC`; any other instruction (and any label definition) is an error.
  - `FUNC`/`ENDFUNC` outside a matching `TRY*LIST ... ENDFUNC` block is an error.
- Runtime errors:
  - If a candidate name resolves to an event function (and `CompatiCallEvent` is not applicable here), it errors rather than trying the next item.
  - If a candidate function exists but is a user-defined expression function (`#FUNCTION/#FUNCTIONS`), it errors.
  - If argument binding fails (too many args, omitted required args, type conversion not permitted, invalid `REF` binding, etc.), it errors (it does **not** “try the next one”).

**Examples**
- `TRYCALLLIST`
- `  FUNC HOOK_%TARGET%, TARGET`
- `  FUNC HOOK_DEFAULT`
- `ENDFUNC`

## TRYJUMPLIST (instruction)

**Summary**
- Like `TRYCALLLIST`, but performs a `JUMP` into the first existing candidate.

**Tags**
- calls

**Syntax**
- `TRYJUMPLIST`
  - `FUNC <formString> [, <arg1>, ... ]`
  - `...`
  - `ENDFUNC`

**Arguments**
- Same as `TRYCALLLIST`.

**Semantics**
- Same selection rules as `TRYCALLLIST`.
- If a candidate function is found:
  - Enters it as a `JUMP` (tail-call behavior): when the callee returns, the current function also returns (the engine unwinds the call stack until a non-`JUMP` frame).
  - As a consequence, control does **not** return to the `ENDFUNC` line on success.
- If no candidate is found, jumps to the `ENDFUNC` line (then continues after it).

**Errors & validation**
- Same as `TRYCALLLIST`.

**Examples**
- `TRYJUMPLIST`
- `  FUNC PHASE_%COUNT%`
- `  FUNC PHASE_DEFAULT`
- `ENDFUNC`

## TRYGOTOLIST (instruction)

**Summary**
- Tries a list of candidate `$label` targets and jumps to the first one that exists; otherwise jumps to `ENDFUNC` (end of the list).

**Tags**
- calls

**Syntax**
- `TRYGOTOLIST`
  - `FUNC <formString>`
  - `FUNC <formString>`
  - `...`
  - `ENDFUNC`

**Arguments**
- Each `FUNC` item provides a label name as a **FORM/formatted string expression** (evaluated to a string at runtime).

**Semantics**
- Structural notes:
  - The lines between `TRYGOTOLIST` and `ENDFUNC` are list items, not a normal executable block body (same model as `TRYCALLLIST`).
- Runtime algorithm:
  - For each `FUNC` item in source order:
    - Evaluate the candidate name to a string.
    - Resolve it as a `$label` inside the **current function**.
    - If it exists, jump to it and stop searching.
  - If no candidate exists, jump to the `ENDFUNC` line (then continue after it).

**Errors & validation**
- Load-time structure errors (the line is marked as error) follow `TRYCALLLIST`.
- Additional load-time restriction: in a `TRYGOTOLIST` block, each `FUNC` item must be a plain candidate name only:
  - no `[...]` subname segment
  - no argument list (neither `(... )` nor `, ...`)

**Examples**
- `TRYGOTOLIST`
- `  FUNC LABEL_%RESULT%`
- `  FUNC LABEL_DEFAULT`
- `ENDFUNC`

## FUNC (instruction)

**Summary**
- List-item line inside `TRYCALLLIST` / `TRYJUMPLIST` / `TRYGOTOLIST` blocks.

**Tags**
- functions

**Syntax**
- Inside `TRYCALLLIST` / `TRYJUMPLIST`:
  - `FUNC <formString> [, <arg1>, <arg2>, ... ]`
  - `FUNC <formString>(<arg1>, <arg2>, ... )`
- Inside `TRYGOTOLIST`:
  - `FUNC <formString>`

**Arguments**
- `<formString>`: a FORM/formatted string expression evaluated to a function name or label name.
- `<argN>`: optional call arguments (not allowed for `TRYGOTOLIST`).

**Semantics**
- Not executed as a standalone statement.
- During load, Emuera collects `FUNC` lines into the surrounding `TRY*LIST` instruction’s internal `callList`.
- At runtime, the surrounding `TRY*LIST` evaluates these items in order (see `TRYCALLLIST` / `TRYJUMPLIST` / `TRYGOTOLIST`).
- Argument parsing is the same as `CALLFORM`: candidate name is a FORM string; call arguments are normal expressions.
- In `TRYCALLLIST` / `TRYJUMPLIST`, the optional `[...]` subname segment is parsed and stored, but it is not used when selecting/calling the function.

**Errors & validation**
- `FUNC` must appear only inside `TRY*LIST ... ENDFUNC`; otherwise it is a load-time error (the line is marked as error).

**Examples**
- `FUNC HOOK_%TARGET%, TARGET`

## ENDFUNC (instruction)

**Summary**
- Ends a `TRY*LIST ... ENDFUNC` block.

**Tags**
- functions

**Syntax**
- `ENDFUNC`

**Arguments**
- None.

**Semantics**
- Marker-only instruction (no runtime effect). The surrounding `TRY*LIST` uses it as the jump target when no candidate succeeds.

**Errors & validation**
- `ENDFUNC` without a matching open `TRY*LIST` is a load-time error (the line is marked as error).

**Examples**
- `ENDFUNC`

## DEBUGPRINT (instruction)
**Summary**
- (TODO: not yet documented)

## DEBUGPRINTL (instruction)
**Summary**
- (TODO: not yet documented)

## DEBUGPRINTFORM (instruction)
**Summary**
- (TODO: not yet documented)

## DEBUGPRINTFORML (instruction)
**Summary**
- (TODO: not yet documented)

## DEBUGCLEAR (instruction)
**Summary**
- (TODO: not yet documented)

## ASSERT (instruction)
**Summary**
- (TODO: not yet documented)

## THROW (instruction)
**Summary**
- (TODO: not yet documented)

## SAVEVAR (instruction)

**Summary**
- Declared but **not implemented** in this engine build (always errors).

**Tags**
- save-system

**Syntax**
- `SAVEVAR <name>, <saveText>, <var1> [, <var2> ...]`

**Arguments**
- `<name>`: string expression; intended file name component.
- `<saveText>`: string expression; intended description text.
- `<var*>`: one or more changeable non-character variable terms (arrays are allowed; several variable categories are rejected).

**Semantics**
- The current engine implementation throws a “not implemented” error at runtime.
- See also: `save-files.md` (directories, partitions, and on-disk formats)

**Errors & validation**
- Always errors at runtime.

**Examples**
- `SAVEVAR "vars", "checkpoint", A, B, C`

## LOADVAR (instruction)

**Summary**
- Declared but **not implemented** in this engine build (always errors).

**Tags**
- save-system

**Syntax**
- `LOADVAR <name>`

**Arguments**
- `<name>`: string expression; intended file name component.

**Semantics**
- The current engine implementation throws a “not implemented” error at runtime.
- See also: `save-files.md` (directories, partitions, and on-disk formats)

**Errors & validation**
- Always errors at runtime.

**Examples**
- `LOADVAR "vars"`

## SAVECHARA (instruction)

**Summary**
- Saves one or more characters into a `dat/chara_<name>.dat` file (binary only).

**Tags**
- characters
- save-system

**Syntax**
- `SAVECHARA <name>, <saveText>, <charaNo1> [, <charaNo2> ...]`

**Arguments**
- `<name>`: string expression; the file name component.
- `<saveText>`: string expression stored in the file as a description.
- `<charaNo*>`: one or more integer expressions; character indices to save (0-based).

**Semantics**
- Writes a binary file under `Program.DatDir`:
  - Path is `chara_<name>.dat`.
- File format:
  - Binary save format with file type `CharVar`.
  - Includes game unique code and script version checks, `<saveText>`, and the serialized character data.
- Validates the character list:
  - All indices must be within `[0, CHARANUM-1]`.
  - Duplicate indices are rejected.
- See also: `save-files.md` (directories, partitions, and on-disk formats)

**Errors & validation**
- Argument parsing requires at least 3 arguments.
- Errors if any character index is negative, too large, out of range, or duplicated.
- File name validity is ultimately enforced by the OS; invalid names can cause runtime errors.

**Examples**
- `SAVECHARA "party", "Before boss", MASTER, TARGET`

## LOADCHARA (instruction)

**Summary**
- Loads characters from `dat/chara_<name>.dat` and appends them to the current character list.

**Tags**
- characters
- save-system

**Syntax**
- `LOADCHARA <name>`

**Arguments**
- `<name>`: string expression; the file name component.

**Semantics**
- Reads `Program.DatDir/chara_<name>.dat`.
- If the file exists and passes validation (file type, unique code, version):
  - Deserializes the characters and appends them to the current character list.
  - Sets `RESULT = 1`.
- Otherwise:
  - Does nothing and sets `RESULT = 0`.
- See also: `save-files.md` (directories, partitions, and on-disk formats)

**Errors & validation**
- No explicit errors are raised for “file not found” / “invalid file”; failures are reported via `RESULT`.

**Examples**
- `LOADCHARA "party"`

## REF (instruction)
**Summary**
- (TODO: not yet documented)

## REFBYNAME (instruction)
**Summary**
- (TODO: not yet documented)

## HTML_PRINT (instruction)

**Summary**
- Prints an HTML string (Emuera’s HTML-like mini language) as console output.

**Tags**
- io

**Syntax**
- `HTML_PRINT <html>(, <toBuffer>)`

**Arguments**
- `<html>`: string expression interpreted as an HTML string (see `html-output.md`).
- `<toBuffer>` (optional): integer expression.
  - `0` (default): print as a complete logical output line (implicit line end).
  - non-zero: append the HTML output into the current print buffer (no implicit line end).

- Omitted arguments / defaults:
  - `<toBuffer>` defaults to `0`.

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output and no evaluation).
- Evaluates `<html>` to a string.
  - If it is null/empty, no output is produced.
- Interprets the string as an HTML string and renders it according to `html-output.md` (tags, entities, comments, wrapping rules).
- If `<toBuffer> = 0` (or omitted):
  - Any pending print buffer content is flushed first (as with other “line-ending” print operations).
  - The HTML is rendered into one logical output line (it may still occupy multiple display lines due to `<br>` or wrapping).
- If `<toBuffer> != 0`:
  - The HTML is converted to output segments and appended into the current print buffer.
  - `<br>` (and literal `'\n'` inside the HTML string) insert display line breaks, but no final line end is implied.
- The output is not affected by non-HTML text style commands like `ALIGNMENT`, `SETFONT`, `SETCOLOR`, or `FONTSTYLE`; use HTML tags (`<p>`, `<font>`, `<b>`, etc.) instead.

**Errors & validation**
- Argument type/count errors follow the normal expression argument rules.
- Invalid HTML strings raise runtime errors (unsupported tags, invalid attributes, invalid character references, tag structure violations), except where a tag explicitly specifies a fallback-to-text behavior (e.g. unresolved `<img>` resources).

**Examples**
```erabasic
; Prints one logical line (with HTML styling)
HTML_PRINT "<p align='center'><b>Hello</b> <font color='red'>world</font></p>"
```

```erabasic
; Appends into the current print buffer (no implicit newline)
HTML_PRINT "<b>HP:</b> 10", 1
PRINTL ""
```

## HTML_TAGSPLIT (instruction)

**Summary**
- Splits an HTML string into a sequence of raw tags and raw text segments.

**Tags**
- string

**Syntax**
- `HTML_TAGSPLIT <html>(, <outParts>, <outCount>)`

**Arguments**
- `<html>`: string expression.
- `<outParts>` (optional): a changeable 1D **non-character** string array variable.
  - Default: `RESULTS`.
- `<outCount>` (optional): a changeable integer variable.
  - Default: `RESULT`.

- Omitted arguments / defaults:
  - If `<outParts>` is omitted, the split parts are written to `RESULTS`.
  - If `<outCount>` is omitted, the split count is written to `RESULT`.

**Semantics**
- Interprets `<html>` as an HTML string and splits it by scanning for `<...>` regions:
  - Each tag-like region from `<` through the next `>` (inclusive) is emitted as a single part.
  - Text between such regions is emitted as-is as a single part.
- The splitter does **not** validate tag relationships or supported tag names; it only performs lexical splitting.
  - For example, it will emit `</font>` as a tag part even if no `<font>` was previously seen.
- On success:
  - Writes the total part count to `<outCount>`.
  - Writes parts to `<outParts>:i` for `0 <= i < min(partCount, len(<outParts>))`.
  - If `partCount` exceeds the destination array length, excess parts are not written.
- On failure (e.g. a `<` is found but no matching `>` exists later in the string):
  - Writes `-1` to `<outCount>`.
  - Does not modify `<outParts>`.

**Errors & validation**
- Argument type/count errors follow the normal expression argument rules.

**Examples**
```erabasic
HTML_TAGSPLIT "<p align='right'>A<!--c-->B</p>"
PRINTFORML RESULT = {RESULT}
PRINTFORML RESULTS:0 = %RESULTS:0%
PRINTFORML RESULTS:1 = %RESULTS:1%
```

## PRINT_IMG (instruction)
**Summary**
- (TODO: not yet documented)

## PRINT_RECT (instruction)
**Summary**
- (TODO: not yet documented)

## PRINT_SPACE (instruction)
**Summary**
- (TODO: not yet documented)

## TOOLTIP_SETCOLOR (instruction)
**Summary**
- (TODO: not yet documented)

## TOOLTIP_SETDELAY (instruction)
**Summary**
- (TODO: not yet documented)

## TOOLTIP_SETDURATION (instruction)
**Summary**
- (TODO: not yet documented)

## INPUTMOUSEKEY (instruction)
**Summary**
- (TODO: not yet documented)

## AWAIT (instruction)
**Summary**
- (TODO: not yet documented)

## VARSIZE (instruction)
**Summary**
- (TODO: not yet documented)

## GETTIME (instruction)

**Summary**
- Writes the current local date/time into `RESULT` (as a packed integer) and `RESULTS` (as a formatted string).

**Tags**
- time

**Syntax**
- `GETTIME`

**Arguments**
- None.

**Semantics**
- Reads the current local time (`DateTime.Now`) and assigns:
  - `RESULT`: an integer of the form `yyyymmddHHMMSSmmm` (milliseconds included).
  - `RESULTS`: a string of the form `yyyy/MM/dd HH:mm:ss` (no milliseconds).
- Does not print output.

**Errors & validation**
- None.

**Examples**
- `GETTIME`

## POWER (instruction)

**Summary**
- Computes an integer power using `Math.Pow` and stores the result into a destination integer variable.

**Tags**
- math

**Syntax**
- `POWER <dest>, <x>, <y>`

**Arguments**
- `<dest>`: changeable integer variable term (destination).
- `<x>`: integer expression (base).
- `<y>`: integer expression (exponent).

**Semantics**
- Evaluates `<x>` and `<y>` as integers, converts them to `double`, then computes `pow = Math.Pow(x, y)`.
- Validates the computed `pow`:
  - If `pow` is NaN → error.
  - If `pow` is infinite → error.
  - If `pow >= long.MaxValue` or `pow <= long.MinValue` → error.
- Stores `(long)pow` into `<dest>` (C# cast truncation toward zero for non-integer results).

**Errors & validation**
- Argument parsing fails if `<dest>` is not a changeable integer variable term.
- Runtime errors for NaN/infinite/overflow results as described above.

**Examples**
- `POWER A, 2, 10` (sets `A` to `1024`)
- `POWER A, 2, -1` (sets `A` to `0` due to truncation of `0.5`)

## PRINTCPERLINE (instruction)
**Summary**
- (TODO: not yet documented)

## SAVENOS (instruction)
**Summary**
- (TODO: not yet documented)

## ENCODETOUNI (instruction)
**Summary**
- (TODO: not yet documented)

## PLAYSOUND (instruction)
**Summary**
- (TODO: not yet documented)

## STOPSOUND (instruction)
**Summary**
- (TODO: not yet documented)

## PLAYBGM (instruction)
**Summary**
- (TODO: not yet documented)

## STOPBGM (instruction)
**Summary**
- (TODO: not yet documented)

## SETSOUNDVOLUME (instruction)
**Summary**
- (TODO: not yet documented)

## SETBGMVOLUME (instruction)
**Summary**
- (TODO: not yet documented)

## TRYCALLF (instruction)
**Summary**
- (TODO: not yet documented)

## TRYCALLFORMF (instruction)
**Summary**
- (TODO: not yet documented)

## UPDATECHECK (instruction)
**Summary**
- (TODO: not yet documented)

## QUIT_AND_RESTART (instruction)
**Summary**
- (TODO: not yet documented)

## FORCE_QUIT (instruction)
**Summary**
- (TODO: not yet documented)

## FORCE_QUIT_AND_RESTART (instruction)
**Summary**
- (TODO: not yet documented)

## FORCE_BEGIN (instruction)

**Summary**
- A “forced” variant of `BEGIN`.

**Tags**
- system

**Syntax**
- `FORCE_BEGIN <keyword>`

**Arguments**
- Same as `BEGIN`.

**Semantics**
- Same as `BEGIN` in the current engine implementation.

**Errors & validation**
- Same as `BEGIN`.

**Examples**
- `FORCE_BEGIN TITLE`

## INPUTANY (instruction)
**Summary**
- (TODO: not yet documented)

## TOOLTIP_SETFONT (instruction)
**Summary**
- (TODO: not yet documented)

## TOOLTIP_SETFONTSIZE (instruction)
**Summary**
- (TODO: not yet documented)

## TOOLTIP_CUSTOM (instruction)
**Summary**
- (TODO: not yet documented)

## TOOLTIP_FORMAT (instruction)
**Summary**
- (TODO: not yet documented)

## TOOLTIP_IMG (instruction)
**Summary**
- (TODO: not yet documented)

## BINPUT (instruction)
**Summary**
- (TODO: not yet documented)

## BINPUTS (instruction)
**Summary**
- (TODO: not yet documented)

## ONEBINPUT (instruction)
**Summary**
- (TODO: not yet documented)

## ONEBINPUTS (instruction)
**Summary**
- (TODO: not yet documented)

## DT_COLUMN_OPTIONS (instruction)
**Summary**
- (TODO: not yet documented)

## VARI (instruction)
**Summary**
- (TODO: not yet documented)

## VARS (instruction)
**Summary**
- (TODO: not yet documented)

## HTML_PRINT_ISLAND (instruction)

**Summary**
- Prints an HTML string into the “HTML island” layer, which is not tied to the normal scrollback/logical line list.

**Tags**
- io

**Syntax**
- `HTML_PRINT_ISLAND <html>(, <ignored>)`

**Arguments**
- `<html>`: string expression interpreted as an HTML string (see `html-output.md`).
- `<ignored>` (optional): integer expression. Accepted by the argument parser but ignored by this instruction.

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output and no evaluation).
- Evaluates `<html>` to a string and appends the rendered HTML output into a separate “island” layer.
- The island layer is not counted by `LINECOUNT` and is not removed by `CLEARLINE`.
- The island layer is drawn independently of the normal log:
  - It does not scroll with the log.
  - It is drawn from the top of the window, with each appended “logical line” placed on successive rows.
- Note: `<div ...>...</div>` sub-areas are not rendered in the island layer.
- Use `HTML_PRINT_ISLAND_CLEAR` to clear the island layer.

**Errors & validation**
- Argument type/count errors follow the normal expression argument rules.
- Invalid HTML strings raise runtime errors (same HTML mini-language as `HTML_PRINT`).

**Examples**
```erabasic
HTML_PRINT_ISLAND "<div width='300px' height='30px' color='#202020'><font color='white'>Status</font></div>"
```

## HTML_PRINT_ISLAND_CLEAR (instruction)

**Summary**
- Clears all content previously added by `HTML_PRINT_ISLAND`.

**Tags**
- io

**Syntax**
- `HTML_PRINT_ISLAND_CLEAR`

**Arguments**
- None.

**Semantics**
- Clears the “HTML island” layer immediately.
- This instruction is not skipped by output skipping; it always clears the island layer.

**Errors & validation**
- None.

**Examples**
```erabasic
HTML_PRINT_ISLAND_CLEAR
```

## PRINTN (instruction)

**Summary**
- `PRINTN` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTN [<raw text>]`
- `PRINTN;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Waits for a key **without** ending the logical output line (see `PRINT`).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTN ...`

## PRINTVN (instruction)

**Summary**
- `PRINTVN` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTVN <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

- Omitted arguments / defaults:
  - None (missing arguments are an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- Waits for a key **without** ending the logical output line (see `PRINT`).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTVN ...`

## PRINTSN (instruction)

**Summary**
- `PRINTSN` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTSN <string expr>`

**Arguments**
- A single string expression (must be present).

- Omitted arguments / defaults:
  - None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- Waits for a key **without** ending the logical output line (see `PRINT`).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSN ...`

## PRINTFORMN (instruction)

**Summary**
- `PRINTFORMN` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORMN [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

- Omitted arguments / defaults:
  - Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Waits for a key **without** ending the logical output line (see `PRINT`).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMN ...`

## PRINTFORMSN (instruction)

**Summary**
- `PRINTFORMSN` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Tags**
- io

**Syntax**
- `PRINTFORMSN <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

- Omitted arguments / defaults:
  - None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- Waits for a key **without** ending the logical output line (see `PRINT`).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMSN ...`

# Expression functions (methods)

## GETCHARA (expression function)
**Summary**
- (TODO: not yet documented)

## GETSPCHARA (expression function)
**Summary**
- (TODO: not yet documented)

## CSVNAME (expression function)
**Summary**
- (TODO: not yet documented)

## CSVCALLNAME (expression function)
**Summary**
- (TODO: not yet documented)

## CSVNICKNAME (expression function)
**Summary**
- (TODO: not yet documented)

## CSVMASTERNAME (expression function)
**Summary**
- (TODO: not yet documented)

## CSVCSTR (expression function)
**Summary**
- (TODO: not yet documented)

## CSVBASE (expression function)
**Summary**
- (TODO: not yet documented)

## CSVABL (expression function)
**Summary**
- (TODO: not yet documented)

## CSVMARK (expression function)
**Summary**
- (TODO: not yet documented)

## CSVEXP (expression function)
**Summary**
- (TODO: not yet documented)

## CSVRELATION (expression function)
**Summary**
- (TODO: not yet documented)

## CSVTALENT (expression function)
**Summary**
- (TODO: not yet documented)

## CSVCFLAG (expression function)
**Summary**
- (TODO: not yet documented)

## CSVEQUIP (expression function)
**Summary**
- (TODO: not yet documented)

## CSVJUEL (expression function)
**Summary**
- (TODO: not yet documented)

## FINDCHARA (expression function)

**Summary**
- Returns the first chara index (role index) in the current character list whose character-data cell equals a target value.

**Tags**
- characters

**Syntax**
- `FINDCHARA(charaVarTerm, value [, startIndex [, lastIndex]])`

**Signatures / argument rules**
- `FINDCHARA(charaVarTerm, value)` → `long`
- `FINDCHARA(charaVarTerm, value, startIndex)` → `long`
- `FINDCHARA(charaVarTerm, value, startIndex, lastIndex)` → `long`

**Arguments**
- `charaVarTerm` (character-data variable term): selects a character-data variable (scalar or array).
  - If it is an array, its subscripts (written after the chara selector) select which per-chara cell is compared.
  - If it is an array, those subscript expressions are evaluated once to select the element(s) to compare.
- The chara selector part of `charaVarTerm` does not affect the search: the function always compares against the scanned chara index `i`.
- `value` (int|string; must match the selected cell type): scalar value to match.
- `startIndex` (optional, int; default `0`): inclusive start chara index.
- `lastIndex` (optional, int; default `CHARANUM`): exclusive end chara index.

**Semantics**
- Reads the current `CHARANUM` and searches forward in the half-open range `[startIndex, lastIndex)`.
- For each chara index `i` in the range, compares the selected per-chara cell against `value` using direct equality:
  - string cell: `==` (ordinal string equality in .NET)
  - int cell: `==`
- Returns the first matching index `i`, or `-1` if:
  - no match is found, or
  - `startIndex >= lastIndex`.

**Errors & validation**
- Errors if `charaVarTerm` is not a character-data variable term, or if `value`’s type does not match the cell type.
- Runtime errors if the range is invalid:
  - `startIndex < 0` or `startIndex >= CHARANUM`
  - `lastIndex < 0` or `lastIndex > CHARANUM`
- Note: `startIndex >= lastIndex` is not an error; it returns `-1`.

**Examples**
- `idx = FINDCHARA(NAME, "Alice")`
- `idx = FINDCHARA(CFLAG:3, 1, 10)`

## FINDLASTCHARA (expression function)

**Summary**
- Like `FINDCHARA`, but searches backward and returns the last matching chara index (role index) in the range.

**Tags**
- characters

**Syntax**
- `FINDLASTCHARA(charaVarTerm, value [, startIndex [, lastIndex]])`

**Signatures / argument rules**
- `FINDLASTCHARA(charaVarTerm, value)` → `long`
- `FINDLASTCHARA(charaVarTerm, value, startIndex)` → `long`
- `FINDLASTCHARA(charaVarTerm, value, startIndex, lastIndex)` → `long`

**Arguments**
- `charaVarTerm` (character-data variable term): selects a character-data variable (scalar or array).
  - If it is an array, its subscripts (written after the chara selector) select which per-chara cell is compared.
  - If it is an array, those subscript expressions are evaluated once to select the element(s) to compare.
- The chara selector part of `charaVarTerm` does not affect the search: the function always compares against the scanned chara index `i`.
- `value` (int|string; must match the selected cell type): scalar value to match.
- `startIndex` (optional, int; default `0`): inclusive start chara index.
- `lastIndex` (optional, int; default `CHARANUM`): exclusive end chara index.

**Semantics**
- Reads the current `CHARANUM` and searches backward in the half-open range `[startIndex, lastIndex)`.
- The search order is: `lastIndex - 1`, `lastIndex - 2`, ..., down to `startIndex`.
- For each chara index `i` in the range, compares the selected per-chara cell against `value` using direct equality:
  - string cell: `==` (ordinal string equality in .NET)
  - int cell: `==`
- Returns the first match encountered in that reverse scan (i.e. the “last” match in the range), or `-1` if:
  - no match is found, or
  - `startIndex >= lastIndex`.

**Errors & validation**
- Errors if `charaVarTerm` is not a character-data variable term, or if `value`’s type does not match the cell type.
- Runtime errors if the range is invalid:
  - `startIndex < 0` or `startIndex >= CHARANUM`
  - `lastIndex < 0` or `lastIndex > CHARANUM`
- Note: `startIndex >= lastIndex` is not an error; it returns `-1`.

**Examples**
- `idx = FINDLASTCHARA(NAME, "Alice")`
- `idx = FINDLASTCHARA(CFLAG:3, 1, 10)`

## EXISTCSV (expression function)
**Summary**
- (TODO: not yet documented)

## VARSIZE (expression function)
**Summary**
- (TODO: not yet documented)

## CHKFONT (expression function)
**Summary**
- (TODO: not yet documented)

## CHKDATA (expression function)
**Summary**
- (TODO: not yet documented)

## ISSKIP (expression function)
**Summary**
- (TODO: not yet documented)

## MOUSESKIP (expression function)
**Summary**
- (TODO: not yet documented)

## MESSKIP (expression function)
**Summary**
- (TODO: not yet documented)

## GETCOLOR (expression function)
**Summary**
- (TODO: not yet documented)

## GETDEFCOLOR (expression function)
**Summary**
- (TODO: not yet documented)

## GETFOCUSCOLOR (expression function)
**Summary**
- (TODO: not yet documented)

## GETBGCOLOR (expression function)
**Summary**
- (TODO: not yet documented)

## GETDEFBGCOLOR (expression function)
**Summary**
- (TODO: not yet documented)

## GETSTYLE (expression function)
**Summary**
- (TODO: not yet documented)

## GETFONT (expression function)
**Summary**
- (TODO: not yet documented)

## BARSTR (expression function)

**Summary**
- Returns the same bar string that `BAR`/`BARL` would print with the same arguments.

**Tags**
- io

**Syntax**
- `BARSTR(value, maxValue, length)`

**Signatures / argument rules**
- `BARSTR(value, maxValue, length)` → `string`

**Arguments**
- `value`: int expression (numerator).
- `maxValue`: int expression (denominator); must evaluate to `> 0`.
- `length`: int expression (bar width); must satisfy `1 <= length <= 99`.

**Semantics**
- Produces:
  - `[` + (`BarChar1` repeated `filled`) + (`BarChar2` repeated `length - filled`) + `]`
  - where `filled = clamp(value * length / maxValue, 0, length)`.
- `BarChar1` / `BarChar2` are configurable (defaults: `*` and `.`).
- As a standalone statement (method-as-statement form), the returned string is written to `RESULTS`.

**Errors & validation**
- Runtime errors if:
  - `maxValue <= 0`
  - `length <= 0`
  - `length >= 100`

**Examples**
```erabasic
S '= BARSTR(HP, MAXHP, 20)
PRINTFORML %S%
```

## CURRENTALIGN (expression function)
**Summary**
- (TODO: not yet documented)

## CURRENTREDRAW (expression function)
**Summary**
- (TODO: not yet documented)

## COLOR_FROMNAME (expression function)
**Summary**
- (TODO: not yet documented)

## COLOR_FROMRGB (expression function)
**Summary**
- (TODO: not yet documented)

## CHKCHARADATA (expression function)
**Summary**
- (TODO: not yet documented)

## FIND_CHARADATA (expression function)
**Summary**
- (TODO: not yet documented)

## MONEYSTR (expression function)
**Summary**
- (TODO: not yet documented)

## PRINTCPERLINE (expression function)
**Summary**
- (TODO: not yet documented)

## PRINTCLENGTH (expression function)
**Summary**
- (TODO: not yet documented)

## SAVENOS (expression function)
**Summary**
- (TODO: not yet documented)

## GETTIME (expression function)
**Summary**
- (TODO: not yet documented)

## GETTIMES (expression function)
**Summary**
- (TODO: not yet documented)

## GETMILLISECOND (expression function)
**Summary**
- (TODO: not yet documented)

## GETSECOND (expression function)
**Summary**
- (TODO: not yet documented)

## RAND (expression function)
**Summary**
- (TODO: not yet documented)

## MIN (expression function)
**Summary**
- (TODO: not yet documented)

## MAX (expression function)
**Summary**
- (TODO: not yet documented)

## ABS (expression function)
**Summary**
- (TODO: not yet documented)

## POWER (expression function)
**Summary**
- (TODO: not yet documented)

## SQRT (expression function)
**Summary**
- (TODO: not yet documented)

## CBRT (expression function)
**Summary**
- (TODO: not yet documented)

## LOG (expression function)
**Summary**
- (TODO: not yet documented)

## LOG10 (expression function)
**Summary**
- (TODO: not yet documented)

## EXPONENT (expression function)
**Summary**
- (TODO: not yet documented)

## SIGN (expression function)
**Summary**
- (TODO: not yet documented)

## LIMIT (expression function)
**Summary**
- (TODO: not yet documented)

## SUMARRAY (expression function)
**Summary**
- (TODO: not yet documented)

## SUMCARRAY (expression function)
**Summary**
- (TODO: not yet documented)

## MATCH (expression function)
**Summary**
- (TODO: not yet documented)

## CMATCH (expression function)
**Summary**
- (TODO: not yet documented)

## GROUPMATCH (expression function)
**Summary**
- (TODO: not yet documented)

## NOSAMES (expression function)
**Summary**
- (TODO: not yet documented)

## ALLSAMES (expression function)
**Summary**
- (TODO: not yet documented)

## MAXARRAY (expression function)
**Summary**
- (TODO: not yet documented)

## MAXCARRAY (expression function)
**Summary**
- (TODO: not yet documented)

## MINARRAY (expression function)
**Summary**
- (TODO: not yet documented)

## MINCARRAY (expression function)
**Summary**
- (TODO: not yet documented)

## GETBIT (expression function)
**Summary**
- (TODO: not yet documented)

## GETNUM (expression function)
**Summary**
- (TODO: not yet documented)

## GETPALAMLV (expression function)
**Summary**
- (TODO: not yet documented)

## GETEXPLV (expression function)
**Summary**
- (TODO: not yet documented)

## FINDELEMENT (expression function)
**Summary**
- (TODO: not yet documented)

## FINDLASTELEMENT (expression function)
**Summary**
- (TODO: not yet documented)

## INRANGE (expression function)
**Summary**
- (TODO: not yet documented)

## INRANGEARRAY (expression function)
**Summary**
- (TODO: not yet documented)

## INRANGECARRAY (expression function)
**Summary**
- (TODO: not yet documented)

## GETNUMB (expression function)
**Summary**
- (TODO: not yet documented)

## ARRAYMSORT (expression function)
**Summary**
- (TODO: not yet documented)

## STRLENS (expression function)
**Summary**
- (TODO: not yet documented)

## STRLENSU (expression function)
**Summary**
- (TODO: not yet documented)

## SUBSTRING (expression function)

**Summary**
- Returns a substring where `start`/`length` are measured in the engine’s “language length” units (the same unit returned by `STRLEN`).

**Tags**
- text

**Syntax**
- `SUBSTRING(str [, start [, length]])`

**Signatures / argument rules**
- `SUBSTRING(str)` → `string`
- `SUBSTRING(str, start)` → `string`
- `SUBSTRING(str, start, length)` → `string`

**Arguments**
- `str` (string): input string.
- `start` (optional, int; default `0`): language-length offset; see Semantics.
- `length` (optional, int; default `-1`): language-length count (`<0` means “to end”).

**Semantics**
- Let `total = STRLEN(str)` (the engine’s “language length” of `str`).
- `start` and `length` are measured in this same unit.
- Special cases:
  - If `start >= total` or `length == 0`: returns `""`.
  - If `length < 0` or `length > total`: `length` is treated as `total` (effectively “to end”).
  - If `start <= 0` and `length == total`: returns `str` unchanged.
- Start position selection (character-boundary rounding):
  - If `start <= 0`, the substring starts at the first character.
  - If `start > 0`, the engine advances from the beginning, accumulating the per-character byte count under the current language encoding until the accumulated count becomes `>= start`; the substring then starts at the *next* character position reached by that scan.
  - This means `start` values that fall “inside” a multi-byte character effectively round up to the next character boundary (the multi-byte character is skipped).
- Length selection (character-boundary rounding):
  - Starting from the chosen start character, the engine appends characters while accumulating the per-character byte count under the current language encoding until the accumulated count becomes `>= length`, or until end-of-string.
  - This means the returned substring may exceed `length` in bytes if the last included character is multi-byte.

**Errors & validation**
- Argument type/count errors are rejected by the engine’s function-method argument checker.

**Examples**
- `SUBSTRING("ABCDE", 1, 2)` → `"BC"` (ASCII)

## SUBSTRINGU (expression function)
**Summary**
- (TODO: not yet documented)

## STRFIND (expression function)
**Summary**
- (TODO: not yet documented)

## STRFINDU (expression function)
**Summary**
- (TODO: not yet documented)

## STRCOUNT (expression function)
**Summary**
- (TODO: not yet documented)

## TOSTR (expression function)

**Summary**
- Converts an integer to a string, optionally using a .NET numeric format string.

**Tags**
- text

**Syntax**
- `TOSTR(i [, format])`

**Signatures / argument rules**
- `TOSTR(i)` → `string`
- `TOSTR(i, format)` → `string`

**Arguments**
- `i`: int expression.
- `format` (optional): string expression passed to `Int64.ToString(format)`.

- Omitted arguments / defaults:
  - If `format` is omitted or `null`: uses the default `i.ToString()` formatting.

**Semantics**
- If `format` is omitted or null: returns `i.ToString()`.
- Otherwise: returns `i.ToString(format)`.

**Errors & validation**
- Argument type/count errors are rejected by the engine’s function-method argument checker.
- If `format` is present but not a valid `.NET` numeric format string, raises a runtime error for invalid format (engine reports the error at argument position 2).

**Examples**
- `TOSTR(42)` → `"42"`
- `TOSTR(42, "D5")` → `"00042"`

## TOINT (expression function)

**Summary**
- Parses a string into an integer using the engine’s numeric-literal reader.
- Returns `0` for many invalid inputs, but some invalid numeric-literal forms raise an error (see Errors & validation).

**Tags**
- text

**Syntax**
- `TOINT(str)`

**Signatures / argument rules**
- `TOINT(str)` → `long`

**Arguments**
- `str`: string expression.

**Semantics**
- Returns `0` if `str` is `null` or `""`.
- Rejects any string containing at least one multi-byte character under the engine’s configured language encoding:
  - If `LangByteCount(str) > str.Length`, returns `0`.
- Rejects strings that do not start with:
  - a digit, or
  - `+`/`-` followed by a digit.
- Parses the leading integer literal using the engine’s integer-literal reader (the same routine used by the lexer/parser):
  - recognizes `0x...` / `0X...` (hex) and `0b...` / `0B...` (binary)
  - recognizes exponent suffixes `e`/`E` (base-10) and `p`/`P` (base-2) with a (signed) integer exponent
    - Exponent digits are parsed using the same digit set as the main literal (so the accepted exponent digit set depends on the literal’s base).
- After the integer literal:
  - If end-of-string: return the parsed value.
  - If the next character is `.`: the remainder must be digits only; this fractional part is validated but ignored.
  - Otherwise: return `0`.

**Errors & validation**
- Argument type/count errors are rejected by the engine’s function-method argument checker.
- Even though many invalid strings return `0`, the underlying integer-literal reader can raise runtime errors for some inputs, including (non-exhaustive):
  - out-of-range / overflow while parsing the integer literal
  - invalid binary digit in a `0b...` literal (e.g. `0b2`)
  - malformed exponent forms (e.g. `1e` without exponent digits)

**Examples**
- `TOINT("123")` → `123`
- `TOINT("123.45")` → `123`
- `TOINT("0x10")` → `16`
- `TOINT("abc")` → `0`

## TOUPPER (expression function)

**Summary**
- Converts a string to uppercase.

**Tags**
- text

**Syntax**
- `TOUPPER(str)`

**Signatures / argument rules**
- `TOUPPER(str)` → `string`

**Arguments**
- `str`: string expression.

**Semantics**
- If `str` is null/empty: returns `""`.
- Otherwise: returns `str.ToUpper()` using the process `CurrentCulture`.
  - In this engine, `CurrentCulture` is set to `InvariantCulture` at startup, so behavior is invariant-culture uppercasing.

**Errors & validation**
- None (apart from normal evaluation errors for `str`).

**Examples**
- `TOUPPER("Abc")` → `"ABC"`

## TOLOWER (expression function)

**Summary**
- Converts a string to lowercase.

**Tags**
- text

**Syntax**
- `TOLOWER(str)`

**Signatures / argument rules**
- `TOLOWER(str)` → `string`

**Arguments**
- `str`: string expression.

**Semantics**
- If `str` is null/empty: returns `""`.
- Otherwise: returns `str.ToLower()` using the process `CurrentCulture`.
  - In this engine, `CurrentCulture` is set to `InvariantCulture` at startup, so behavior is invariant-culture lowercasing.

**Errors & validation**
- None (apart from normal evaluation errors for `str`).

**Examples**
- `TOLOWER("Abc")` → `"abc"`

## TOHALF (expression function)

**Summary**
- Converts full-width characters to half-width (narrow) form using the engine’s configured language encoding (`useLanguage`).

**Tags**
- text

**Syntax**
- `TOHALF(str)`

**Signatures / argument rules**
- `TOHALF(str)` → `string`

**Arguments**
- `str`: string expression.

**Semantics**
- If `str` is null/empty: returns `""`.
- Otherwise: uses VisualBasic `Strings.StrConv(..., Narrow, <code page>)`, where `<code page>` is the engine’s current language code page (derived from `useLanguage`).

**Errors & validation**
- Argument type/count errors are rejected by the engine’s function-method argument checker.
- Any runtime exceptions from the underlying `.NET` conversion routine propagate as engine errors.

**Examples**
- `TOHALF("ＡＢＣ")` → `"ABC"`

## TOFULL (expression function)

**Summary**
- Converts half-width characters to full-width (wide) form using the engine’s configured language encoding (`useLanguage`).

**Tags**
- text

**Syntax**
- `TOFULL(str)`

**Signatures / argument rules**
- `TOFULL(str)` → `string`

**Arguments**
- `str`: string expression.

**Semantics**
- If `str` is null/empty: returns `""`.
- Otherwise: uses VisualBasic `Strings.StrConv(..., Wide, <code page>)`, where `<code page>` is the engine’s current language code page (derived from `useLanguage`).

**Errors & validation**
- Argument type/count errors are rejected by the engine’s function-method argument checker.
- Any runtime exceptions from the underlying `.NET` conversion routine propagate as engine errors.

**Examples**
- `TOFULL("ABC")` → `"ＡＢＣ"`

## LINEISEMPTY (expression function)
**Summary**
- (TODO: not yet documented)

## REPLACE (expression function)
**Summary**
- (TODO: not yet documented)

## UNICODE (expression function)
**Summary**
- (TODO: not yet documented)

## UNICODEBYTE (expression function)
**Summary**
- (TODO: not yet documented)

## CONVERT (expression function)
**Summary**
- (TODO: not yet documented)

## ISNUMERIC (expression function)
**Summary**
- (TODO: not yet documented)

## ESCAPE (expression function)
**Summary**
- (TODO: not yet documented)

## ENCODETOUNI (expression function)
**Summary**
- (TODO: not yet documented)

## CHARATU (expression function)
**Summary**
- (TODO: not yet documented)

## GETLINESTR (expression function)
**Summary**
- (TODO: not yet documented)

## STRFORM (expression function)
**Summary**
- (TODO: not yet documented)

## STRJOIN (expression function)
**Summary**
- (TODO: not yet documented)

## GETCONFIG (expression function)
**Summary**
- (TODO: not yet documented)

## GETCONFIGS (expression function)
**Summary**
- (TODO: not yet documented)

## HTML_GETPRINTEDSTR (expression function)

**Summary**
- Returns the HTML-formatted representation of a previously displayed **logical output line**.

**Tags**
- io

**Syntax**
- `HTML_GETPRINTEDSTR(<lineNo>)`

**Signatures / argument rules**
- Signature: `string HTML_GETPRINTEDSTR(int lineNo = 0)`.
- `<lineNo>` is evaluated as an integer expression.

**Arguments**
- `<lineNo>` (optional): integer expression. Defaults to `0`.
  - `0` = the most recent logical output line.
  - `1` = the second most recent logical output line.
  - And so on.

- Omitted arguments / defaults:
  - `<lineNo>` defaults to `0`.

**Semantics**
- Interprets `<lineNo>` as a non-negative index into the current display log’s **logical lines**, counted from the end:
  - `HTML_GETPRINTEDSTR(0)` returns the most recently produced logical output line.
- Returns `""` if the requested line does not exist.
- The returned HTML is a normalized representation of the displayed line:
  - It always wraps the line in `<p align='...'><nobr> ... </nobr></p>`.
  - It uses `<br>` between display-wrapped lines within the same logical line.
  - Button segments are represented with `<button ...>` / `<nonbutton ...>` tags (including `title` and `pos` when present).
  - Inline images and shapes are represented by their tag-like alt text (e.g. `<img ...>` / `<shape ...>`).
  - `<div ...>` sub-area elements are omitted.
- This function does not modify the display.

**Errors & validation**
- If `<lineNo> < 0`, this is a runtime error.

**Examples**
```erabasic
PRINTL "Hello"
PRINTL "World"

; Gets the most recent logical line (the "World" line)
S = HTML_GETPRINTEDSTR(0)
```

## HTML_POPPRINTINGSTR (expression function)

**Summary**
- Returns (and clears) the current pending print buffer as an HTML string.

**Tags**
- io

**Syntax**
- `HTML_POPPRINTINGSTR()`

**Signatures / argument rules**
- Signature: `string HTML_POPPRINTINGSTR()`.

**Arguments**
- None.

**Semantics**
- If the engine output is disabled or the print buffer is empty, returns `""`.
- Otherwise:
  - Flushes the current print buffer into display-line structures **without displaying them**.
  - Clears the print buffer.
  - Converts the flushed content to an HTML string and returns it.
- The returned HTML:
  - uses `<br>` between display-wrapped lines within the flushed buffer
  - does **not** include `<p ...>` or `<nobr>` wrappers (so it does not reflect `ALIGNMENT`).
  - omits `<div ...>` sub-area elements

**Errors & validation**
- None.

**Examples**
```erabasic
PRINT "A"
PRINT "B"
S = HTML_POPPRINTINGSTR()
; At this point, the pending buffer is cleared and nothing was displayed.
```

## HTML_TOPLAINTEXT (expression function)

**Summary**
- Converts an HTML string to plain text by removing tags and expanding character references.

**Tags**
- string

**Syntax**
- `HTML_TOPLAINTEXT(html)`

**Signatures / argument rules**
- Signature: `string HTML_TOPLAINTEXT(string html)`.

**Arguments**
- `html`: string expression interpreted as an HTML string.

**Semantics**
- Removes all tag-like regions of the form `<...>` (including button tags and comments).
- Then expands character references in the remaining text (e.g. `&amp;` → `&`, `&#x41;` → `A`).

**Errors & validation**
- Malformed character references in the remaining text are runtime errors (e.g. an `&...` sequence missing a terminating `;`).
- Unsupported numeric character reference values (outside `0 <= codePoint <= 0xFFFF`) are runtime errors.

**Examples**
```erabasic
PRINTFORMW %HTML_TOPLAINTEXT("<b>AAA</b><i><b>BBB</b></i><s>CCC</s>")%
; prints: AAABBBCCC
```

## HTML_ESCAPE (expression function)

**Summary**
- Escapes a plain-text string for use in HTML strings.

**Tags**
- string

**Syntax**
- `HTML_ESCAPE(text)`

**Signatures / argument rules**
- Signature: `string HTML_ESCAPE(string text)`.

**Arguments**
- `text`: string expression.

**Semantics**
- Replaces:
  - `&` → `&amp;`
  - `>` → `&gt;`
  - `<` → `&lt;`
  - `"` → `&quot;`
  - `'` → `&apos;`
- All other characters are unchanged.

**Errors & validation**
- None.

**Examples**
```erabasic
PRINTFORMW %HTML_ESCAPE("A&B<C>D'E")%
; prints: A&amp;B&lt;C&gt;D&apos;E
```

## SPRITECREATED (expression function)
**Summary**
- (TODO: not yet documented)

## SPRITEWIDTH (expression function)
**Summary**
- (TODO: not yet documented)

## SPRITEHEIGHT (expression function)
**Summary**
- (TODO: not yet documented)

## SPRITEMOVE (expression function)
**Summary**
- (TODO: not yet documented)

## SPRITESETPOS (expression function)
**Summary**
- (TODO: not yet documented)

## SPRITEPOSX (expression function)
**Summary**
- (TODO: not yet documented)

## SPRITEPOSY (expression function)
**Summary**
- (TODO: not yet documented)

## CLIENTWIDTH (expression function)
**Summary**
- (TODO: not yet documented)

## CLIENTHEIGHT (expression function)
**Summary**
- (TODO: not yet documented)

## GETKEY (expression function)
**Summary**
- (TODO: not yet documented)

## GETKEYTRIGGERED (expression function)
**Summary**
- (TODO: not yet documented)

## MOUSEX (expression function)
**Summary**
- (TODO: not yet documented)

## MOUSEY (expression function)
**Summary**
- (TODO: not yet documented)

## MOUSEB (expression function)
**Summary**
- (TODO: not yet documented)

## ISACTIVE (expression function)
**Summary**
- (TODO: not yet documented)

## SAVETEXT (expression function)
**Summary**
- (TODO: not yet documented)

## LOADTEXT (expression function)
**Summary**
- (TODO: not yet documented)

## GCREATED (expression function)
**Summary**
- (TODO: not yet documented)

## GWIDTH (expression function)
**Summary**
- (TODO: not yet documented)

## GHEIGHT (expression function)
**Summary**
- (TODO: not yet documented)

## GGETCOLOR (expression function)
**Summary**
- (TODO: not yet documented)

## SPRITEGETCOLOR (expression function)
**Summary**
- (TODO: not yet documented)

## GCREATE (expression function)
**Summary**
- (TODO: not yet documented)

## GCREATEFROMFILE (expression function)
**Summary**
- (TODO: not yet documented)

## GDISPOSE (expression function)
**Summary**
- (TODO: not yet documented)

## GCLEAR (expression function)
**Summary**
- (TODO: not yet documented)

## GFILLRECTANGLE (expression function)
**Summary**
- (TODO: not yet documented)

## GDRAWSPRITE (expression function)
**Summary**
- (TODO: not yet documented)

## GSETCOLOR (expression function)
**Summary**
- (TODO: not yet documented)

## GDRAWG (expression function)
**Summary**
- (TODO: not yet documented)

## GDRAWGWITHMASK (expression function)
**Summary**
- (TODO: not yet documented)

## GSETBRUSH (expression function)
**Summary**
- (TODO: not yet documented)

## GSETFONT (expression function)
**Summary**
- (TODO: not yet documented)

## GSETPEN (expression function)
**Summary**
- (TODO: not yet documented)

## SPRITECREATE (expression function)
**Summary**
- (TODO: not yet documented)

## SPRITEDISPOSE (expression function)
**Summary**
- (TODO: not yet documented)

## CBGSETG (expression function)
**Summary**
- (TODO: not yet documented)

## CBGSETSPRITE (expression function)
**Summary**
- (TODO: not yet documented)

## CBGCLEAR (expression function)
**Summary**
- (TODO: not yet documented)

## CBGCLEARBUTTON (expression function)
**Summary**
- (TODO: not yet documented)

## CBGREMOVERANGE (expression function)
**Summary**
- (TODO: not yet documented)

## CBGREMOVEBMAP (expression function)
**Summary**
- (TODO: not yet documented)

## CBGSETBMAPG (expression function)
**Summary**
- (TODO: not yet documented)

## CBGSETBUTTONSPRITE (expression function)
**Summary**
- (TODO: not yet documented)

## GSAVE (expression function)
**Summary**
- (TODO: not yet documented)

## GLOAD (expression function)
**Summary**
- (TODO: not yet documented)

## SPRITEANIMECREATE (expression function)
**Summary**
- (TODO: not yet documented)

## SPRITEANIMEADDFRAME (expression function)
**Summary**
- (TODO: not yet documented)

## SETANIMETIMER (expression function)
**Summary**
- (TODO: not yet documented)

## OUTPUTLOG (expression function)
**Summary**
- (TODO: not yet documented)

## HTML_STRINGLEN (expression function)

**Summary**
- Measures the display width of an HTML string (using the same layout rules as `HTML_PRINT`).

**Tags**
- io

**Syntax**
- `HTML_STRINGLEN(html(, returnPixel))`

**Signatures / argument rules**
- Signature: `int HTML_STRINGLEN(string html, int returnPixel = 0)`.
- `returnPixel` is treated as “false” only when it is exactly `0`; any non-zero value selects pixel return.

**Arguments**
- `html`: string expression interpreted as an HTML string.
- `returnPixel` (optional): integer expression.
  - `0` (default): return in half-width character units.
  - non-zero: return in pixels.

- Omitted arguments / defaults:
  - `returnPixel` defaults to `0`.

**Semantics**
- Computes the rendered output for `html` using the same rules as `HTML_PRINT`.
- Measures the width of the **first display line** only (if `html` contains `<br>` or wraps, later lines do not affect the return value).
- If `returnPixel != 0`, returns the width in pixels.
- If `returnPixel = 0` (or omitted), converts pixel width to half-width character units using the configured font size:
  - Let `fontSizePx = FontSize` (see `config-items.md`).
  - Let `widthPx` be the measured pixel width (non-negative).
  - Returns the smallest integer `n` such that `n * fontSizePx / 2 >= widthPx`.
- Unless the HTML string is wrapped in `<nobr>...</nobr>`, the measured width does not exceed the drawable width (content is wrapped).

**Errors & validation**
- Invalid HTML strings raise runtime errors (same HTML mini-language as `HTML_PRINT`).

**Examples**
```erabasic
PRINTFORML {HTML_STRINGLEN("<b>B</b>")}
PRINTFORML {HTML_STRINGLEN("<b>B</b>", 1)}
```

## HTML_SUBSTRING (expression function)

**Summary**
- Splits an HTML string into a prefix that fits within a given display width and the remaining suffix.

**Tags**
- io

**Syntax**
- `HTML_SUBSTRING(html, width)`

**Signatures / argument rules**
- Signature: `string HTML_SUBSTRING(string html, int width)`.
- Also writes results into `RESULTS` (see semantics).

**Arguments**
- `html`: string expression interpreted as an HTML string.
- `width`: integer expression, in half-width character units.

**Semantics**
- Returns the first part (the prefix) as an HTML string.
- Writes the split results into `RESULTS`:
  - `RESULTS:0` = returned prefix
  - `RESULTS:1` = remaining suffix (may be `""`)
  - Other `RESULTS:*` entries are not cleared.
- Interprets `width` in “half-width character units”. One unit corresponds to half the configured font size in pixels:
  - `pixelBudget = width * FontSize / 2`
- Expands character references in `html` first, then performs the split.
  - This means that sequences like `&lt;b&gt;` may become `<b>` tags after expansion and affect the split.
- If the expanded HTML contains a `<br>` tag, it forces the split at that point:
  - The prefix ends before the `<br>`.
  - The suffix starts after the `<br>`.
  - The `<br>` tag itself is not included in either result.
- Compatibility notes:
  - The special handling of `<br>`, `<img ...>`, and `<shape ...>` is case-sensitive (`br`/`img`/`shape` in lowercase). For example, `<BR>` is not treated as a forced split point.
  - Literal newline characters (`'\n'`) are not treated as forced split points by this function (unlike `HTML_PRINT` rendering).
- Treats `<img ...>` and `<shape ...>` as indivisible units when splitting:
  - If the current line already has content and the next figure would exceed the width budget, the figure is left for the suffix.
- Produces output HTML that keeps basic style tag balance across the split boundary (so the prefix and suffix remain renderable HTML strings in this mini language).

**Errors & validation**
- Invalid HTML strings (including invalid character references) may raise runtime errors.

**Examples**
```erabasic
PRINTSL HTML_SUBSTRING("AB<b>CD</b>EFG", 4)
PRINTSL RESULTS:1
```

## HTML_STRINGLINES (expression function)

**Summary**
- Returns how many lines an HTML string would occupy when repeatedly split by a given width (using `HTML_SUBSTRING`).

**Tags**
- io

**Syntax**
- `HTML_STRINGLINES(html, width)`

**Signatures / argument rules**
- Signature: `int HTML_STRINGLINES(string html, int width)`.

**Arguments**
- `html`: string expression interpreted as an HTML string.
- `width`: integer expression, in half-width character units.

**Semantics**
- If `html` is null/empty, returns `0`.
- Otherwise, repeatedly applies the same splitting rules as `HTML_SUBSTRING(html, width)`:
  - Each split consumes the prefix as one line.
  - The remainder becomes the next input.
- Returns the number of iterations until the remainder becomes empty.
- Compatibility notes:
  - This function inherits all parsing/splitting quirks from `HTML_SUBSTRING`, including case-sensitive special handling of `<br>`, `<img ...>`, and `<shape ...>`.

**Errors & validation**
- Invalid HTML strings (including invalid character references) may raise runtime errors.

**Examples**
```erabasic
PRINTVL HTML_STRINGLINES("AB<b>CD</b>", 4)
```

## EXISTFILE (expression function)
**Summary**
- (TODO: not yet documented)

## EXISTVAR (expression function)
**Summary**
- (TODO: not yet documented)

## ISDEFINED (expression function)
**Summary**
- (TODO: not yet documented)

## ENUMFUNCBEGINSWITH (expression function)
**Summary**
- (TODO: not yet documented)

## ENUMFUNCENDSWITH (expression function)
**Summary**
- (TODO: not yet documented)

## ENUMFUNCWITH (expression function)
**Summary**
- (TODO: not yet documented)

## ENUMVARBEGINSWITH (expression function)
**Summary**
- (TODO: not yet documented)

## ENUMVARENDSWITH (expression function)
**Summary**
- (TODO: not yet documented)

## ENUMVARWITH (expression function)
**Summary**
- (TODO: not yet documented)

## ENUMMACROBEGINSWITH (expression function)
**Summary**
- (TODO: not yet documented)

## ENUMMACROENDSWITH (expression function)
**Summary**
- (TODO: not yet documented)

## ENUMMACROWITH (expression function)
**Summary**
- (TODO: not yet documented)

## ENUMFILES (expression function)
**Summary**
- (TODO: not yet documented)

## GETVAR (expression function)
**Summary**
- (TODO: not yet documented)

## GETVARS (expression function)
**Summary**
- (TODO: not yet documented)

## SETVAR (expression function)
**Summary**
- (TODO: not yet documented)

## VARSETEX (expression function)
**Summary**
- (TODO: not yet documented)

## ARRAYMSORTEX (expression function)
**Summary**
- (TODO: not yet documented)

## REGEXPMATCH (expression function)
**Summary**
- (TODO: not yet documented)

## XML_DOCUMENT (expression function)
**Summary**
- (TODO: not yet documented)

## XML_RELEASE (expression function)
**Summary**
- (TODO: not yet documented)

## XML_GET (expression function)
**Summary**
- (TODO: not yet documented)

## XML_GET_BYNAME (expression function)
**Summary**
- (TODO: not yet documented)

## XML_SET (expression function)
**Summary**
- (TODO: not yet documented)

## XML_SET_BYNAME (expression function)
**Summary**
- (TODO: not yet documented)

## XML_EXIST (expression function)
**Summary**
- (TODO: not yet documented)

## XML_TOSTR (expression function)
**Summary**
- (TODO: not yet documented)

## XML_ADDNODE (expression function)
**Summary**
- (TODO: not yet documented)

## XML_ADDNODE_BYNAME (expression function)
**Summary**
- (TODO: not yet documented)

## XML_REMOVENODE (expression function)
**Summary**
- (TODO: not yet documented)

## XML_REMOVENODE_BYNAME (expression function)
**Summary**
- (TODO: not yet documented)

## XML_REPLACE (expression function)
**Summary**
- (TODO: not yet documented)

## XML_REPLACE_BYNAME (expression function)
**Summary**
- (TODO: not yet documented)

## XML_ADDATTRIBUTE (expression function)
**Summary**
- (TODO: not yet documented)

## XML_ADDATTRIBUTE_BYNAME (expression function)
**Summary**
- (TODO: not yet documented)

## XML_REMOVEATTRIBUTE (expression function)
**Summary**
- (TODO: not yet documented)

## XML_REMOVEATTRIBUTE_BYNAME (expression function)
**Summary**
- (TODO: not yet documented)

## MAP_CREATE (expression function)
**Summary**
- (TODO: not yet documented)

## MAP_EXIST (expression function)
**Summary**
- (TODO: not yet documented)

## MAP_RELEASE (expression function)
**Summary**
- (TODO: not yet documented)

## MAP_GET (expression function)
**Summary**
- (TODO: not yet documented)

## MAP_CLEAR (expression function)
**Summary**
- (TODO: not yet documented)

## MAP_SIZE (expression function)
**Summary**
- (TODO: not yet documented)

## MAP_HAS (expression function)
**Summary**
- (TODO: not yet documented)

## MAP_SET (expression function)
**Summary**
- (TODO: not yet documented)

## MAP_REMOVE (expression function)
**Summary**
- (TODO: not yet documented)

## MAP_GETKEYS (expression function)
**Summary**
- (TODO: not yet documented)

## MAP_TOXML (expression function)
**Summary**
- (TODO: not yet documented)

## MAP_FROMXML (expression function)
**Summary**
- (TODO: not yet documented)

## DT_CREATE (expression function)
**Summary**
- (TODO: not yet documented)

## DT_EXIST (expression function)
**Summary**
- (TODO: not yet documented)

## DT_RELEASE (expression function)
**Summary**
- (TODO: not yet documented)

## DT_NOCASE (expression function)
**Summary**
- (TODO: not yet documented)

## DT_CLEAR (expression function)
**Summary**
- (TODO: not yet documented)

## DT_COLUMN_ADD (expression function)
**Summary**
- (TODO: not yet documented)

## DT_COLUMN_NAMES (expression function)
**Summary**
- (TODO: not yet documented)

## DT_COLUMN_EXIST (expression function)
**Summary**
- (TODO: not yet documented)

## DT_COLUMN_REMOVE (expression function)
**Summary**
- (TODO: not yet documented)

## DT_COLUMN_LENGTH (expression function)
**Summary**
- (TODO: not yet documented)

## DT_ROW_ADD (expression function)
**Summary**
- (TODO: not yet documented)

## DT_ROW_SET (expression function)
**Summary**
- (TODO: not yet documented)

## DT_ROW_REMOVE (expression function)
**Summary**
- (TODO: not yet documented)

## DT_ROW_LENGTH (expression function)
**Summary**
- (TODO: not yet documented)

## DT_CELL_GET (expression function)
**Summary**
- (TODO: not yet documented)

## DT_CELL_ISNULL (expression function)
**Summary**
- (TODO: not yet documented)

## DT_CELL_GETS (expression function)
**Summary**
- (TODO: not yet documented)

## DT_CELL_SET (expression function)
**Summary**
- (TODO: not yet documented)

## DT_SELECT (expression function)
**Summary**
- (TODO: not yet documented)

## DT_TOXML (expression function)
**Summary**
- (TODO: not yet documented)

## DT_FROMXML (expression function)
**Summary**
- (TODO: not yet documented)

## MOVETEXTBOX (expression function)
**Summary**
- (TODO: not yet documented)

## RESUMETEXTBOX (expression function)
**Summary**
- (TODO: not yet documented)

## EXISTSOUND (expression function)
**Summary**
- (TODO: not yet documented)

## EXISTFUNCTION (expression function)
**Summary**
- (TODO: not yet documented)

## GDRAWGWITHROTATE (expression function)
**Summary**
- (TODO: not yet documented)

## GDRAWTEXT (expression function)
**Summary**
- (TODO: not yet documented)

## GGETFONT (expression function)
**Summary**
- (TODO: not yet documented)

## GGETFONTSIZE (expression function)
**Summary**
- (TODO: not yet documented)

## GGETFONTSTYLE (expression function)
**Summary**
- (TODO: not yet documented)

## GGETTEXTSIZE (expression function)
**Summary**
- (TODO: not yet documented)

## GGETBRUSH (expression function)
**Summary**
- (TODO: not yet documented)

## GGETPEN (expression function)
**Summary**
- (TODO: not yet documented)

## GGETPENWIDTH (expression function)
**Summary**
- (TODO: not yet documented)

## GETMEMORYUSAGE (expression function)
**Summary**
- (TODO: not yet documented)

## CLEARMEMORY (expression function)
**Summary**
- (TODO: not yet documented)

## GETTEXTBOX (expression function)
**Summary**
- (TODO: not yet documented)

## SETTEXTBOX (expression function)
**Summary**
- (TODO: not yet documented)

## ERDNAME (expression function)
**Summary**
- (TODO: not yet documented)

## SPRITEDISPOSEALL (expression function)
**Summary**
- (TODO: not yet documented)

## GDRAWLINE (expression function)
**Summary**
- (TODO: not yet documented)

## GETDISPLAYLINE (expression function)
**Summary**
- (TODO: not yet documented)

## GDASHSTYLE (expression function)
**Summary**
- (TODO: not yet documented)

## GETDOINGFUNCTION (expression function)
**Summary**
- (TODO: not yet documented)

## FLOWINPUT (expression function)
**Summary**
- (TODO: not yet documented)

## FLOWINPUTS (expression function)
**Summary**
- (TODO: not yet documented)

## GETMETH (expression function)
**Summary**
- (TODO: not yet documented)

## GETMETHS (expression function)
**Summary**
- (TODO: not yet documented)

## EXISTMETH (expression function)
**Summary**
- (TODO: not yet documented)

## BITMAP_CACHE_ENABLE (expression function)
**Summary**
- (TODO: not yet documented)

## HOTKEY_STATE (expression function)
**Summary**
- (TODO: not yet documented)

## HOTKEY_STATE_INIT (expression function)
**Summary**
- (TODO: not yet documented)
