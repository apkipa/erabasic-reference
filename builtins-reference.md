# EraBasic Built-ins Reference (Emuera / EvilMask)

Generated on `2026-03-06`.

> [!WARNING]
> This file is generated. Do **not** edit `builtins-reference.md` by hand.
> Make persistent content changes in `erabasic-reference/builtins-overrides/**` or the generator/tooling inputs, then regenerate this file.

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
- `<raw text>` (optional, default `""`): raw text, not an expression.

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
- `<raw text>` (optional, default `""`): raw text, not an expression.

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
- `<raw text>` (optional, default `""`): raw text, not an expression.

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
- `<raw text>` (optional, default `""`): raw text, not an expression.

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
- `<raw text>` (optional, default `""`): raw text, not an expression.

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
- `<raw text>` (optional, default `""`): raw text, not an expression.

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
- `<raw text>` (optional, default `""`): raw text, not an expression.

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
- `<raw text>` (optional, default `""`): raw text, not an expression.

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
- `<raw text>` (optional, default `""`): raw text, not an expression.

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
- `<raw text>` (optional, default `""`): raw text, not an expression.

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
- `<raw text>` (optional, default `""`): raw text, not an expression.

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
- `<raw text>` (optional, default `""`): raw text, not an expression.
- If the resulting text is empty, nothing is appended.
- Output is converted to a fixed-width “cell” string (see below).

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
- `<raw text>` (optional, default `""`): raw text, not an expression.
- If the resulting text is empty, nothing is appended.
- Output is converted to a fixed-width “cell” string (see below).

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
- `<raw text>` (optional, default `""`): raw text, not an expression.
- Output is padded/truncated to a fixed-width cell (`PrintCLength`) using Shift-JIS byte count.

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
- `<raw text>` (optional, default `""`): raw text, not an expression.
- Output is padded/truncated to a fixed-width cell (`PrintCLength`) using Shift-JIS byte count.

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
- `<raw text>` (optional, default `""`): raw text, not an expression.
- Output is padded/truncated to a fixed-width cell (`PrintCLength`) using Shift-JIS byte count.

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
- `<raw text>` (optional, default `""`): raw text, not an expression.
- Output is padded/truncated to a fixed-width cell (`PrintCLength`) using Shift-JIS byte count.

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
- `<text>` (string): button label.
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
- See also: `input-flow.md` (shared wait-state lifecycle and `MesSkip` auto-advance model).
- Does not assign `RESULT`/`RESULTS`.
- Skipped when output skipping is active (via `SKIPDISP`).

**Errors & validation**
- None.

**Examples**
- `WAIT`

## INPUT (instruction)

**Summary**
- Requests an integer input from the user and stores it into `RESULT`; when `<mouse> != 0` and completion occurs via a mouse click, the UI also writes mouse-side-channel metadata.

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
- See also: `input-flow.md` (shared submission paths, segment draining/discard rules, and `MesSkip` interaction).
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
- Other input waits can use a different `RESULT:*` payload layout; `INPUTMOUSEKEY`, for example, does not reuse `INPUT`'s `RESULT:3` button-color slot.
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
- Requests a string input from the user and stores it into `RESULTS`; when `<mouse> != 0` and completion occurs via a mouse click, the UI also writes mouse-side-channel metadata.

**Tags**
- io

**Syntax**
- `INPUTS`
- `INPUTS <defaultFormString>`
- `INPUTS <defaultFormString>, <mouse> [, <canSkip>]`

**Arguments**
- `<defaultFormString>` (optional): FORM/formatted string expression used as the default string. If omitted, there is no default.
- `<mouse>` (optional, int; default `0`): if non-zero, enables mouse-based input.
- `<canSkip>` (optional, any): presence enables the `MesSkip` fast path; its value is ignored (not evaluated).

**Semantics**
- Enters a string-input UI wait.
- See also: `input-flow.md` (shared submission paths, segment draining/discard rules, and `MesSkip` interaction).
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
- Output skipping interaction is the same as `INPUT`.

**Errors & validation**
- Argument parsing errors follow the underlying builder rules for `INPUTS`.
- Argument parsing quirks:
  - After the first comma, the engine tries to parse `<mouse>` as an `int` expression.
    - If it is omitted or not an integer expression, the engine warns and ignores the entire tail (mouse input is disabled; `canSkip` is not enabled).
  - Supplying `<canSkip>` may still emit a “too many arguments” warning, but its presence is accepted and used by the runtime.

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
- `<timeMs>` (int): time limit in milliseconds.
- `<default>` (int): default value used on timeout (and also on empty input when the request is not running a timer).
- `<displayTime>` (optional, int; default `1`): if non-zero, displays remaining time (UI behavior).
- `<timeoutMessage>` (optional, string; default `TimeupLabel`): message used on timeout.
- `<mouse>` (optional, int; default `0`): enables mouse input when equal to `1`.
- `<canSkip>` (optional, int): if present, allows `MesSkip` to auto-accept the default without waiting (the value is not evaluated).

**Semantics**
- Enters an integer-input UI wait with a timer of `<timeMs>` milliseconds (a default is always present for timed input).
- See also: `input-flow.md` (shared submission paths, timed completion model, segment draining/discard rules, and `MesSkip` interaction).
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
- `<timeMs>` (int): time limit in milliseconds.
- `<default>` (string): default value used on timeout (and also on empty input when the request is not running a timer).
- `<displayTime>` (optional, int; default `1`): if non-zero, displays remaining time.
- `<timeoutMessage>` (optional, string; default `TimeupLabel`): timeout message.
- `<mouse>` (optional, int; default `0`): enables mouse input when equal to `1`.
- `<canSkip>` (optional, int): if present, allows `MesSkip` to auto-accept the default without waiting (the value is not evaluated).

**Semantics**
- Same model as `TINPUT`, but stores into `RESULTS` (string) rather than `RESULT` (int).
- See also: `input-flow.md` (shared submission paths, timed completion model, segment draining/discard rules, and `MesSkip` interaction).
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

**Semantics**
- Same as `TINPUT`, but with “one input” mode enabled:
  - One-input truncation is applied per submitted segment; see `input-flow.md` for the shared submission/segmentation model.
  - Each submitted segment is normally truncated to its first character.
  - Exception: if the segment is accepted through the mouse-click completion path and config option `AllowLongInputByMouse` is enabled (see `config-items.md`), that mouse-submitted text is not truncated.
  - This truncation applies only to submitted UI text. Defaults accepted via empty input or the `MesSkip` no-wait path are used as-is by `TONEINPUT` itself.

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

**Semantics**
- Same as `TINPUTS`, but with “one input” mode enabled:
  - One-input truncation is applied per submitted segment; see `input-flow.md` for the shared submission/segmentation model.
  - Each submitted segment is normally truncated to its first character.
  - Exception: if the segment is accepted through the mouse-click completion path and config option `AllowLongInputByMouse` is enabled (see `config-items.md`), that mouse-submitted text is not truncated.
  - This truncation applies only to submitted UI text. Defaults accepted via empty input or the `MesSkip` no-wait path are used as-is by `TONEINPUTS` itself.

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
- `<timeMs>` (int): time limit in milliseconds.
- `<mode>` (int):
  - `0`: wait for Enter/click, but time out after `<timeMs>`.
  - non-zero: disallow input and simply wait `<timeMs>` (or be affected by macro/skip behavior).

**Semantics**
- If `<mode> == 0`: waits for Enter/click, but times out after `<timeMs>`.
- See also: `input-flow.md` (shared wait-state lifecycle, timed completion model, and `MesSkip` auto-advance behavior).
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
- See also: `input-flow.md` (shared wait-state lifecycle and `MesSkip` auto-advance model).
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
- See also: `input-flow.md` (shared wait-state lifecycle and `MesSkip` auto-advance model).
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

**Semantics**
- Like `INPUT` (including `MesSkip` behavior and mouse side channels), but sets `OneInput = true` on the input request.
- Exact one-input rule:
  - One-input truncation is applied per submitted segment; see `input-flow.md` for the shared submission/segmentation model.
  - Each submitted segment is normally truncated to its first character.
  - Exception: if the segment is accepted through the mouse-click completion path and config option `AllowLongInputByMouse` is enabled (see `config-items.md`), that mouse-submitted text is not truncated.
  - This truncation applies only to submitted UI text. Defaults accepted via empty input or the `MesSkip` no-wait path are used as-is by `ONEINPUT` itself.

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

**Semantics**
- Like `INPUTS` (including `MesSkip` behavior and mouse side channels), but with “one input” mode enabled:
  - One-input truncation is applied per submitted segment; see `input-flow.md` for the shared submission/segmentation model.
  - Each submitted segment is normally truncated to its first character.
  - Exception: if the segment is accepted through the mouse-click completion path and config option `AllowLongInputByMouse` is enabled (see `config-items.md`), that mouse-submitted text is not truncated.
  - This truncation applies only to submitted UI text. Defaults accepted via empty input or the `MesSkip` no-wait path are used as-is by `ONEINPUTS` itself.

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
- `<n>` (int): number of logical output lines to delete.
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

**Semantics**
- Evaluates `<formString>` to a string.
- Appends it to the save-description buffer:
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
      - if `EVENTLOAD` returns normally without performing a `BEGIN`, the engine enters the SHOP main loop fallback: it proceeds to `@SHOW_SHOP` / command input without calling `@EVENTSHOP` and without performing the SHOP-entry autosave.
- See also: `save-files.md` (directories, partitions, and on-disk formats)

**Errors & validation**
- Error if load is not allowed in the current system state.
- Selecting an empty slot prints a “no data” message and reopens the load prompt.
- If loading fails unexpectedly after selection, raises a runtime error.

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
- `<slot>` (int): save slot number. Must satisfy `0 <= slot <= 2147483647` (32-bit signed non-negative).
- `<saveText>` (string): saved into the file and shown by the built-in save/load UI.
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
- `LOADDATA [<slot>]`

**Arguments**
- `<slot>` (optional, int; default `0` with a warning if omitted): save slot index. Must be in `[0, 2147483647]` (32-bit signed non-negative).

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
- If `EVENTLOAD` returns normally without performing a `BEGIN`, the engine enters the SHOP main loop fallback: it proceeds to `@SHOW_SHOP` / command input without calling `@EVENTSHOP` and without performing the SHOP-entry autosave.
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
- `SIF [<int expr>]`
  - `<next logical line>`

**Arguments**
- `<int expr>` (optional, int; default `0` with a warning if omitted): condition (`0` = false, non-zero = true).

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
- `IF [<int expr>]`
  - `...`
  - `ELSEIF <int expr>`
  - `...`
  - `ELSE`
  - `...`
  - `ENDIF`

**Arguments**
- `<int expr>` (optional, int; default `0` with a warning if omitted): condition (`0` = false, non-zero = true).

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
- `REPEAT [<countExpr>]`
  - `...`
  - `REND`

**Arguments**
- `<countExpr>` (optional, int; default `0` with a warning if omitted): number of iterations.

**Semantics**
- `REPEAT` is implemented as a FOR-like loop over `COUNT:0`:
  - Initializes `COUNT:0` to `0`.
  - Uses `end = <countExpr>` and `step = 1`.
  - The loop continues while `COUNT:0 < end`.
- If `end <= 0`, the loop body is skipped.
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
- `<end>` (int): loop bound (exclusive).
- `<step>` (optional, int; default `1`): increment applied at `NEXT` time.

**Semantics**
- Initializes the counter variable to `<start>`, then loops while:
  - `step > 0`: `<counter> < <end>`
  - `step < 0`: `<counter> > <end>`
- If `step == 0`, the loop body executes zero times (execution jumps directly to `NEXT`).
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
- `WHILE [<int expr>]`
  - `...`
  - `WEND`

**Arguments**
- `<int expr>` (optional, int; default `0` with a warning if omitted): loop condition (`0` = false, non-zero = true).

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
- `LOOP [<int expr>]`

**Arguments**
- `<int expr>` (optional, int; default `0` with a warning if omitted): loop condition (`0` = false, non-zero = true).

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
- `<valueN>` (optional, int): each value is stored into `RESULT:<index>`.

**Semantics**
- Evaluates all provided integer expressions (left-to-right), stores them into the `RESULT` integer array starting at index 0, then returns from the function.
- The return value used by the call stack is `RESULT:0` after the assignment.
- If no values are provided, behaves like `RETURN 0` (sets `RESULT:0` to `0` and returns `0`).
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

**Semantics**
- Evaluates the formatted string to a string `s`.
- Parses `s` as `expr1, expr2, ...` using the engine’s expression lexer/parser.
- Parsing detail: after each comma, the engine skips ASCII spaces (not tabs) before reading the next expression.
- Stores the resulting integer values into `RESULT:0`, `RESULT:1`, ... and returns.
- If `s` is empty, behaves like `RETURN 0`.

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
- `<expr>` (optional): expression whose type should match the function’s declared return type.

**Semantics**
- Sets the method return value for the current expression-function call and exits the method body.
- If `<expr>` is omitted:
  - int-returning method: returns `0`
  - string-returning method: returns `""`
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
- `STRLEN [<rawString>]`

**Arguments**
- `<rawString>` (optional, default `""`): literal remainder of the line (not a normal string expression).

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
- `STRLENFORM [<formString>]`

**Arguments**
- `<formString>` (optional, default `""`): FORM/formatted string expression (supports `%...%` and `{...}`).

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
- `STRLENU [<rawString>]`

**Arguments**
- `<rawString>` (optional, default `""`): literal remainder of the line (not a normal string expression).

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
- `STRLENFORMU [<formString>]`

**Arguments**
- `<formString>` (optional, default `""`): FORM/formatted string expression.

**Semantics**
- Evaluates the formatted string to a string value, then assigns `str.Length` to `RESULT`.

**Errors & validation**
- Errors if the formatted string evaluation fails.

**Examples**
- `STRLENFORMU NAME=%NAME%` sets `RESULT` to the character length of the expanded string.

## SWAPCHARA (instruction)

**Summary**
- Swaps two entries in the engine’s current character list.

**Tags**
- characters

**Syntax**
- `SWAPCHARA x, y`

**Arguments**
- `x` (int): character index.
- `y` (int): character index.

**Semantics**
- If `x == y`, no-op.
- Otherwise, swaps the character objects at indices `x` and `y` in the current character list.
- Does not adjust `TARGET` / `ASSI` / `MASTER`:
  - they remain numeric indices, so after the swap they may refer to different character objects than before.
- Does not print output.

**Errors & validation**
- Runtime error if `x` or `y` is out of range (`x < 0`, `y < 0`, or `>= CHARANUM`).

**Examples**
- `SWAPCHARA 1, 2`

## COPYCHARA (instruction)

**Summary**
- Copies all character data from one character to another (overwrite).

**Tags**
- characters

**Syntax**
- `COPYCHARA fromIndex, toIndex`

**Arguments**
- `fromIndex` (int): source character index.
- `toIndex` (int): destination character index.

**Semantics**
- Copies the entire character-data record from `fromIndex` into `toIndex`.
  - This overwrites all character variables for `toIndex`, including `NO`/`NAME`/etc and character arrays.
- Does not change the character list length and does not move character indices.
- Does not print output.

**Errors & validation**
- Runtime error if `fromIndex` is out of range.
- Runtime error if `toIndex` is out of range.

**Examples**
- `COPYCHARA 0, 1`

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
- Splits a string by a separator string and writes the resulting parts into a string array.

**Tags**
- text

**Syntax**
- `SPLIT <text>, <separator>, <outParts> [, <outCount>]`

**Arguments**
- `<text>` (string): string expression to split.
- `<separator>` (string): string expression used as the separator (not a set of characters).
- `<outParts>` (variable term): changeable array variable term to receive the parts.
  - Must be a **string** array variable (1D/2D/3D; character-data arrays are accepted but behave specially).
  - Any indices written in `<outParts>` are ignored for this instruction.
- `<outCount>` (optional, variable term; default `RESULT`): changeable integer variable term to receive the number of split parts.

**Semantics**
- Computes `parts = text.Split(new[] { separator }, StringSplitOptions.None)` (equivalent .NET behavior).
- Writes `parts.Length` into `<outCount>`.
- Writes a prefix of `parts` into `<outParts>`:
  - If `parts.Length > length0`, only the first `length0` parts are written, where `length0` is the destination array’s **first** dimension length.
  - Otherwise, all parts are written.
- Destination addressing rules:
  - 1D array: writes `outParts[i]` starting at `i = 0`.
  - 2D array: writes `outParts[0, i]` starting at `i = 0`.
  - 3D array: writes `outParts[0, 0, i]` starting at `i = 0`.
  - character-data string arrays: always write into character index `0` using the same “fixed earlier indices = 0” rule (e.g. `CVAR[0, i]`).
- Does not clear elements outside the written prefix.

**Errors & validation**
- Argument parsing fails if `<outParts>` is not a changeable array variable term.
- Argument parsing fails if `<outCount>` is provided but is not a changeable integer variable term.
- Runtime error if `<outParts>` is not a string array variable.

**Examples**
```erabasic
#DIM PARTS, 10
SPLIT "a,b,c", ",", PARTS
; RESULT == 3
; PARTS:0 == "a"
; PARTS:1 == "b"
; PARTS:2 == "c"
```

## SETCOLOR (instruction)

**Summary**
- Sets the current foreground (text) color.

**Tags**
- ui

**Syntax**
- `SETCOLOR rgb`
- `SETCOLOR r, g, b`

**Arguments**
- `rgb` (int): packed `0xRRGGBB` value. Only the low 24 bits are used.
- `r`, `g`, `b` (int): color components.
  - Must satisfy `0 <= component <= 255`.

**Semantics**
- One-argument form (`rgb`):
  - Extracts components:
    - `r = (rgb & 0xFF0000) >> 16`
    - `g = (rgb & 0x00FF00) >> 8`
    - `b = (rgb & 0x0000FF)`
  - Sets the current text color to `(r, g, b)`.
- Three-argument form (`r, g, b`):
  - Validates that each component is within `0..255`.
  - Sets the current text color to `(r, g, b)`.
- Does not print output.

**Errors & validation**
- Parse-time warning + rejection if you pass exactly 2 arguments.
- Runtime error in the three-argument form if any component is `< 0` or `> 255`.

**Examples**
- `SETCOLOR 0xFF0000`      ; red
- `SETCOLOR 255, 0, 0`     ; red

## SETCOLORBYNAME (instruction)

**Summary**
- Sets the current foreground (text) color by a named color.

**Tags**
- ui

**Syntax**
- `SETCOLORBYNAME <name>`

**Arguments**
- `<name>` (raw string): a color name recognized by `System.Drawing.Color.FromName`.
  - This is a raw string argument, not a string expression.

**Semantics**
- Resolves `<name>` via `Color.FromName(name)` and sets the current text color to the resolved RGB.
- Does not print output.

**Errors & validation**
- Parse-time error if `<name>` is not a valid color name.
- Parse-time error if `<name>` is `"transparent"` (case-insensitive).

**Examples**
- `SETCOLORBYNAME Red`

## RESETCOLOR (instruction)

**Summary**
- Resets the current text color to the configured default foreground color.

**Tags**
- ui

**Syntax**
- `RESETCOLOR`

**Arguments**
- None.

**Semantics**
- Sets the current text color to the configured default (`ForeColor`).
- Does not print output.

**Errors & validation**
- (none)

**Examples**
- `RESETCOLOR`

## SETBGCOLOR (instruction)

**Summary**
- Sets the current background color.

**Tags**
- ui

**Syntax**
- `SETBGCOLOR rgb`
- `SETBGCOLOR r, g, b`

**Arguments**
- `rgb` (int): packed `0xRRGGBB` value. Only the low 24 bits are used.
- `r`, `g`, `b` (int): color components.
  - Must satisfy `0 <= component <= 255`.

**Semantics**
- Same argument handling as `SETCOLOR`, but applies to the background color instead of the text color.
- Does not print output.

**Errors & validation**
- Parse-time warning + rejection if you pass exactly 2 arguments.
- Runtime error in the three-argument form if any component is `< 0` or `> 255`.

**Examples**
- `SETBGCOLOR 0x000000`    ; black background
- `SETBGCOLOR 0, 0, 0`     ; black background

## SETBGIMAGE (instruction)

**Summary**
- Adds a sprite-backed background image layer to the console.

**Tags**
- ui
- resources

**Syntax**
- `SETBGIMAGE <spriteName> [, <depth> [, <opacityByte> ]]`

**Arguments**
- `<spriteName>` (string): formatted string expression naming a sprite.
  - Sprite lookup is case-insensitive (the engine uppercases before lookup).
  - Only file-backed sprites loaded from `resources/**/*.csv` are accepted; other sprite kinds are ignored.
- `<depth>` (optional, string; default `0`): formatted string expression parsed by `Int64.Parse`.
- `<opacityByte>` (optional, string; default `255`): formatted string expression parsed by `Int64.Parse`, then converted to opacity as `value / 255.0`.
  - Not clamped.

**Semantics**
- Resolves `<spriteName>` to a sprite:
  - If the sprite does not exist or is not a file-backed sprite, the instruction is a no-op.
  - Otherwise, it appends a new background entry `(depth, sprite, opacity)` to the background list.
- The background list is sorted by `depth` descending (larger depth first).
- The engine bakes a composite background image from the list:
  - Each sprite is scaled to **cover** the client area while preserving aspect ratio.
  - If horizontal padding is needed, it is centered; vertical alignment is top-aligned (extra height is cropped at the bottom).
  - Each layer is alpha-multiplied by `opacity`.
- Does not print output.

**Errors & validation**
- Runtime error if `<depth>` or `<opacityByte>` cannot be parsed by `Int64.Parse`.

**Examples**
- `SETBGIMAGE TITLE_BG`
- `SETBGIMAGE TITLE_BG, 10, 128`  ; 50% opacity

## SETBGCOLORBYNAME (instruction)

**Summary**
- Sets the current background color by a named color.

**Tags**
- ui

**Syntax**
- `SETBGCOLORBYNAME <name>`

**Arguments**
- `<name>` (raw string): a color name recognized by `System.Drawing.Color.FromName`.
  - This is a raw string argument, not a string expression.

**Semantics**
- Resolves `<name>` via `Color.FromName(name)` and sets the background color to the resolved RGB.
- Does not print output.

**Errors & validation**
- Parse-time error if `<name>` is not a valid color name.
- Parse-time error if `<name>` is `"transparent"` (case-insensitive).

**Examples**
- `SETBGCOLORBYNAME Black`

## RESETBGCOLOR (instruction)

**Summary**
- Resets the current background color to the configured default background color.

**Tags**
- ui

**Syntax**
- `RESETBGCOLOR`

**Arguments**
- None.

**Semantics**
- Sets the current background color to the configured default (`BackColor`).
- Does not print output.

**Errors & validation**
- (none)

**Examples**
- `RESETBGCOLOR`

## CLEARBGIMAGE (instruction)

**Summary**
- Removes all background image layers.

**Tags**
- ui

**Syntax**
- `CLEARBGIMAGE`

**Arguments**
- None.

**Semantics**
- Clears the background image list and re-bakes the composite background.
- Does not print output.

**Errors & validation**
- (none)

**Examples**
- `CLEARBGIMAGE`

## REMOVEBGIMAGE (instruction)

**Summary**
- Removes one background image layer by sprite name.

**Tags**
- ui
- resources

**Syntax**
- `REMOVEBGIMAGE <spriteName>`

**Arguments**
- `<spriteName>` (string): formatted string expression.
  - Matching is **case-sensitive** against the stored sprite name (which is uppercased during resource loading).

**Semantics**
- Removes the first background entry whose sprite name equals `<spriteName>`, then re-bakes the composite background.
- Does not print output.

**Errors & validation**
- Runtime error if no matching background entry exists.

**Examples**
- `REMOVEBGIMAGE TITLE_BG`

## FONTBOLD (instruction)

**Summary**
- Enables bold font style for subsequent output (Windows only).

**Tags**
- ui

**Syntax**
- `FONTBOLD`

**Arguments**
- None.

**Semantics**
- If running on Windows:
  - Sets the current font style to `(currentStyle | Bold)`.
- If not running on Windows:
  - No-op.

**Errors & validation**
- (none)

**Examples**
- `FONTBOLD`

## FONTITALIC (instruction)

**Summary**
- Enables italic font style for subsequent output (Windows only).

**Tags**
- ui

**Syntax**
- `FONTITALIC`

**Arguments**
- None.

**Semantics**
- If running on Windows:
  - Sets the current font style to `(currentStyle | Italic)`.
- If not running on Windows:
  - No-op.

**Errors & validation**
- (none)

**Examples**
- `FONTITALIC`

## FONTREGULAR (instruction)

**Summary**
- Resets the font style to regular (clears bold/italic/etc) for subsequent output (Windows only).

**Tags**
- ui

**Syntax**
- `FONTREGULAR`

**Arguments**
- None.

**Semantics**
- If running on Windows:
  - Sets the current font style to `Regular` (clears all style flags).
- If not running on Windows:
  - No-op.

**Errors & validation**
- (none)

**Examples**
- `FONTREGULAR`

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
  - Any written chara selector in `<charaVarTerm>` is ignored and not evaluated (the sort always scans `i = 0 .. CHARANUM-1`).

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
- Sets the current font style flags (bold/italic/strikeout/underline) for subsequent text output.

**Tags**
- ui

**Syntax**
- `FONTSTYLE`
- `FONTSTYLE <flags>`

**Arguments**
- `<flags>` (optional, int; default `0`): style bit flags.
  - `1`: bold
  - `2`: italic
  - `4`: strikeout
  - `8`: underline
  - Other bits are ignored.

**Semantics**
- Computes the style as `Regular` plus any flags present in `<flags>`, then sets it as the current text style.
- Does not change the font face (see `SETFONT`).

**Errors & validation**
- (none)

**Examples**
- `FONTSTYLE 3` (bold + italic)
- `FONTSTYLE` (reset to regular)

## ALIGNMENT (instruction)

**Summary**
- Sets the horizontal alignment (left/center/right) used when the engine lays out subsequent printed lines.

**Tags**
- ui

**Syntax**
- `ALIGNMENT LEFT`
- `ALIGNMENT CENTER`
- `ALIGNMENT RIGHT`

**Arguments**
- Alignment keyword: raw token compared using the engine’s `IgnoreCase` setting.
  - This is not a string expression/literal.

**Semantics**
- Sets the current alignment for subsequent lines.

**Errors & validation**
- Runtime error if the keyword is not one of `LEFT`, `CENTER`, `RIGHT`.

**Examples**
- `ALIGNMENT CENTER`

## CUSTOMDRAWLINE (instruction)

**Summary**
- Draws a horizontal rule by repeating a raw pattern string across the drawable width, then prints a newline.

**Tags**
- ui

**Syntax**
- `CUSTOMDRAWLINE <pattern>`

**Arguments**
- `<pattern>` (raw text): the remainder of the line after the keyword.
  - This is not an expression.

**Semantics**
- Skipped when output skipping is active (via `SKIPDISP`).
- Expands `<pattern>` to a full-width bar using the engine’s “custom bar” algorithm:
  - Measure is based on rendered display width (using the configured default font and `DrawableWidth`).
  - Repeats `<pattern>` until the measured width reaches/exceeds `DrawableWidth`, then removes characters from the end until it fits.
- Prints the expanded bar with font style forced to `Regular`, then prints a newline.

**Errors & validation**
- Load-time error if `<pattern>` is omitted.

**Examples**
- `CUSTOMDRAWLINE -`
- `CUSTOMDRAWLINE =*=`

## DRAWLINEFORM (instruction)

**Summary**
- Draws a horizontal rule by repeating a runtime string expression across the drawable width, then prints a newline.

**Tags**
- ui

**Syntax**
- `DRAWLINEFORM <pattern>`

**Arguments**
- `<pattern>` (string expression): pattern to repeat.

**Semantics**
- Skipped when output skipping is active (via `SKIPDISP`).
- Evaluates `<pattern>` to a string `s`.
  - If `s` is non-empty, expands it to a full-width bar using the same algorithm as `CUSTOMDRAWLINE` (repeat until it reaches `DrawableWidth`, then trim to fit).
- Prints the expanded bar with font style forced to `Regular`, then prints a newline.

**Errors & validation**
- Runtime error if `<pattern>` evaluates to `""` (empty).

**Examples**
- `DRAWLINEFORM "-" + STRFORM("%02d", RAND:100)`

## CLEARTEXTBOX (instruction)

**Summary**
- Clears the main output text box (removes all currently displayed lines).

**Tags**
- ui

**Syntax**
- `CLEARTEXTBOX`

**Arguments**
- None.

**Semantics**
- Clears the UI’s main output area.
- This instruction still executes even when output skipping is active.

**Errors & validation**
- (none)

**Examples**
- `CLEARTEXTBOX`

## SETFONT (instruction)

**Summary**
- Sets the current font face name used for subsequent text output.

**Tags**
- ui

**Syntax**
- `SETFONT`
- `SETFONT <fontName>`

**Arguments**
- `<fontName>` (optional, string expression; default `""`): font face name.

**Semantics**
- If `<fontName>` is non-empty, sets the current font face name to that value.
- If `<fontName>` is empty (including when omitted), resets the current font face name to the configured default font.

**Errors & validation**
- (none)

**Examples**
- `SETFONT "MS Gothic"`
- `SETFONT` (reset to default)

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
- `<seed>` (optional): int. If omitted, the seed defaults to `0`.

**Semantics**
- The legacy RNG used here is SFMT with the MT19937 parameter set.
- If `UseNewRandom` is enabled in JSON config:
  - Emits a warning and does nothing.
  - The new-mode RNG used by `RAND` remains the host `.NET System.Random` instance.
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
- The legacy RNG used here is SFMT with the MT19937 parameter set.
- If `UseNewRandom` is enabled in JSON config:
  - Emits a warning and does nothing.
- Otherwise:
  - Writes the legacy RNG state into `RANDDATA`.
  - `RANDDATA` must have length `625`.
  - Layout: elements `0..623` receive the 624 state words; element `624` receives the current index.
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- Runtime error if `RANDDATA` does not have length `625`.

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
- The legacy RNG used here is SFMT with the MT19937 parameter set.
- If `UseNewRandom` is enabled in JSON config:
  - Emits a warning and does nothing.
- Otherwise:
  - Loads the legacy RNG state from `RANDDATA`.
  - `RANDDATA` must have length `625`.
  - Layout: elements `0..623` are the 624 state words; element `624` is the current index.
  - On load, elements `0..623` are interpreted as unsigned 32-bit values.
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- Runtime error if `RANDDATA` does not have length `625`.

**Examples**
- `INITRAND`

## REDRAW (instruction)

**Summary**
- Controls the console redraw mode and optionally forces an immediate redraw.

**Tags**
- ui

**Syntax**
- `REDRAW <flags>`

**Arguments**
- `<flags>` (int expression): redraw flags.
  - Bit `0`:
    - `0`: disable automatic redraw (`Redraw = None`)
    - `1`: enable normal redraw (`Redraw = Normal`)
  - Bit `1`:
    - if set, forces an immediate redraw once (`RefreshStrings(true)`).
  - Other bits are ignored.

**Semantics**
- Updates the console’s redraw mode according to `<flags>`.

**Errors & validation**
- (none)

**Examples**
- `REDRAW 0` (stop automatic redraw)
- `REDRAW 3` (enable redraw + force immediate refresh)

## CALLTRAIN (instruction)

**Summary**
- Enables “continuous train command execution” using the commands pre-populated in `SELECTCOM`.

**Tags**
- system

**Syntax**
- `CALLTRAIN <count>`

**Arguments**
- `<count>` (int expression): number of commands to take from `SELECTCOM`.

**Semantics**
- Reads the current `SELECTCOM` array and enqueues `SELECTCOM[1] .. SELECTCOM[count]` (inclusive) as a command list.
- While this mode is active, the train loop consumes the queued commands automatically instead of waiting for user input.
- When the queued command list is exhausted, the engine exits the mode and (if present) calls `@CALLTRAINEND`.

**Errors & validation**
- Runtime error if `<count> >= length(SELECTCOM)`.
- `<count> <= 0` is not explicitly rejected by the engine, but results in an empty queue and is not useful (avoid).

**Examples**
- `CALLTRAIN 3` (use `SELECTCOM[1]`, `SELECTCOM[2]`, `SELECTCOM[3]`)

## STOPCALLTRAIN (instruction)

**Summary**
- Stops “continuous train command execution” mode (started by `CALLTRAIN`) and clears any remaining queued commands.

**Tags**
- system

**Syntax**
- `STOPCALLTRAIN`

**Arguments**
- None.

**Semantics**
- If continuous-train mode is active:
  - Clears the queued command list.
  - Calls `@CALLTRAINEND` if it exists.
- If not active, no-op.

**Errors & validation**
- (none)

**Examples**
- `STOPCALLTRAIN`

## DOTRAIN (instruction)

**Summary**
- Immediately executes a specific train command (by `TRAINNAME` index) within the train system phase.

**Tags**
- system

**Syntax**
- `DOTRAIN <trainIndex>`

**Arguments**
- `<trainIndex>` (int expression): index into `TRAINNAME` (from `train.csv`).

**Semantics**
- Valid only in specific train-phase internal states (e.g. during `@EVENTTRAIN`, `@SHOW_STATUS`, `@SHOW_USERCOM`, or `@EVENTCOMEND` processing).
- Sets `SELECTCOM = <trainIndex>` and advances the train system state to execute that command as if it was selected.

**Errors & validation**
- Runtime error if executed outside the allowed train-phase states.
- Runtime error if `<trainIndex> < 0` or `<trainIndex> >= length(TRAINNAME)`.

**Examples**
- `DOTRAIN 5`

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
- `<raw text>` (optional, default `""`): raw text, not an expression.
  - Parsing detail: as with most instructions, Emuera consumes exactly one delimiter character after the keyword (space/tab/full-width-space if enabled, or `;`). The remainder of the line becomes the raw text.

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
- `<strVarTerm>` (optional; default `RESULTS`): changeable string variable term to receive the result.

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
- Shifts elements in a mutable 1D array variable by an offset (can be negative) and fills new slots with a default value.

**Tags**
- arrays

**Syntax**
- `ARRAYSHIFT <arrayVar>, <shift>, <default> [, <start> [, <count>]]`

**Arguments**
- `<arrayVar>`: changeable 1D array variable term.
- `<shift>` (int): shift offset (can be negative). `0` is a no-op.
- `<default>`: expression of the same scalar type as the array element type.
- `<start>` (optional, int; default `0`): start index of the shifted segment.
- `<count>` (optional, int; default “to end”): number of elements in the segment. If explicitly `0`, this is a no-op.

**Semantics**
- If `<arrayVar>` is a character-data 1D array, the shift is applied to the **per-character slice** selected by `<arrayVar>`’s chara selector.
  - Any element-index subscript written after the chara selector is ignored for this instruction, but it is still evaluated once when the instruction evaluates `<arrayVar>`’s indices.
  - To target a specific character explicitly, write both indices (the element index is a dummy), e.g. `CFLAG:chara:0`.
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
- `<start>` (int): start index (0-based).
- `<count>` (int): number of elements to remove.

**Semantics**
- Works only on 1D arrays (int or string).
- If `<arrayVar>` is a character-data 1D array, the removal is applied to the **per-character slice** selected by `<arrayVar>`’s chara selector.
  - Any element-index subscript written after the chara selector is ignored for this instruction, but it is still evaluated once when the instruction evaluates `<arrayVar>`’s indices.
  - To target a specific character explicitly, write both indices (the element index is a dummy), e.g. `CFLAG:chara:0`.
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
- `ARRAYSORT <arrayVar> [, FORWARD|BACK [, <start> [, <count>]]]`

**Arguments**
- `<arrayVar>`: changeable 1D array variable term (int or string).
- `FORWARD|BACK` (optional; default `FORWARD`):
  - `FORWARD`: ascending
  - `BACK`: descending
- `<start>` (optional, int; default `0`): subrange start index (only parsed when `FORWARD|BACK` is present).
- `<count>` (optional, int; default “to end”): subrange length (only parsed when `FORWARD|BACK` is present). If explicitly `0`, this is a no-op.

**Semantics**
- Order defaults to ascending.
- If `<arrayVar>` is a character-data 1D array, the sort is applied to the **per-character slice** selected by `<arrayVar>`’s chara selector.
  - Any element-index subscript written after the chara selector is ignored for this instruction, but it is still evaluated once when the instruction evaluates `<arrayVar>`’s indices.
  - To target a specific character explicitly, write both indices (the element index is a dummy), e.g. `CFLAG:chara:0`.
- Sorts the specified region of the array:
  - If `<count>` is omitted: sorts to end.
  - If `<count>` is provided and `<= 0`: `0` is a no-op; `<0` is an error.
- Parsing quirk:
  - `<start>` and `<count>` are only parsed when the `FORWARD|BACK` token is present.
  - If the token after the first comma is not `FORWARD` or `BACK`:
    - identifier → parse-time error
    - non-identifier (e.g. a number) → ignored (sorts the whole array with default order)

**Errors & validation**
- Parse-time errors if `<arrayVar>` is not a changeable 1D array variable term, or if the order token is present but not `FORWARD` or `BACK`.
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
- `<srcVarNameExpr>` (string): expression whose value is a variable name.
- `<dstVarNameExpr>` (string): expression whose value is a variable name.

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

**Semantics**
- Resolves the evaluated name to an expression function and evaluates it.
- The return value is computed but not assigned to `RESULT/RESULTS` by this instruction.

**Errors & validation**
- Errors if the method does not exist or if argument checking fails.

**Examples**
- `CALLFORMF "FUNC_%X%", A, B`

## CALLSHARP (instruction)

**Summary**
- Calls a C# plugin method (from `Plugins/*.dll`) by name.

**Tags**
- plugins

**Syntax**
- `CALLSHARP <methodName>`
- `CALLSHARP <methodName> [, <arg1>, <arg2>, ... ]`
- `CALLSHARP <methodName>(<arg1>, <arg2>, ... )`

**Arguments**
- `<methodName>`: raw string token; matched against the registered plugin method name.
- `<argN>`: expression; evaluated and passed to the plugin as either a string or an integer.

**Semantics**
- `CALLSHARP` resolves `<methodName>` to a plugin method registered by the plugin system and calls it.
- `<methodName>` is not an expression:
  - It is parsed as raw text up to the first `(`, `[`, `,`, or `;`, then trimmed.
  - Backslash escapes are processed while parsing the raw token (e.g. `\\s` = space, `\\t` = tab, and `\\,` can be used to include a comma in the name).
  - Quotation marks are not special here; `CALLSHARP "X"` looks for a method literally named `"X"`.
- Argument passing:
  - Each `<argN>` is evaluated before the plugin is invoked.
  - If `<argN>` is a string expression, the plugin receives a string value; otherwise it receives an integer value.
- Write-back (out/ref-like behavior):
  - After the plugin returns, any `<argN>` that is a variable term is assigned a new value from the plugin’s corresponding argument slot.
  - Non-variable arguments (constants, computed expressions, etc.) are not written back.
- Optional bracket segment:
  - The parser accepts `CALLSHARP <methodName>[...]` in the same “subname” shape as `CALL/CALLF`.
  - This bracket segment is ignored by `CALLSHARP`: it is parsed for compatibility, but not evaluated and not passed to the plugin.

**Errors & validation**
- If `<methodName>` is empty: load-time error.
- If `<methodName>` does not match any registered plugin method:
  - The engine emits a load-time warning.
  - Executing the instruction still fails at runtime (missing method binding).
- If an argument position is left empty (e.g. `CALLSHARP M, , 1`): runtime error.
- If the plugin throws an exception: runtime error.

Method-name case sensitivity follows the engine’s `IgnoreCase` configuration:
- If `IgnoreCase = true`, plugin methods are looked up case-insensitively.
- Otherwise, method names are case-sensitive.

See `plugins.md` for how plugins are discovered/loaded and how methods are registered.

**Examples**
- `CALLSHARP MyMethod`
- `CALLSHARP MyMethod, 123, "abc", X, S`
- `CALLSHARP MyMethod(X, S)` (equivalent argument parsing)

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
- Compatibility parsing: after `<labelName>`, the engine also accepts an optional “call-like tail”:
  - `GOTO <labelName>(...)`
  - `GOTO <labelName>, ...`
  - These extra parts are parsed for compatibility but ignored by `GOTO`:
    - Only `<labelName>` is used to resolve the `$label`.
    - The ignored expressions are not evaluated and have no side effects (they only need to be syntactically valid).

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
- `GOTO LOOP_START(1, 2)` (equivalent to `GOTO LOOP_START`)
- `GOTO LOOP_START, 1, 2` (equivalent to `GOTO LOOP_START`)

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
  - Emuera collects the `FUNC` lines into a list during load, and executes only `TRYCALLLIST` at runtime.
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
- During load, Emuera collects `FUNC` lines into a list owned by the surrounding `TRY*LIST` instruction.
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
- `<name>` (string): intended file name component.
- `<saveText>` (string): intended description text.
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
- `<name>` (string): intended file name component.

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
- `<name>` (string): the file name component.
- `<saveText>` (string): stored in the file as a description.
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
- `<name>` (string): the file name component.

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
- Declared but **not implemented** in this engine build (always errors).

**Tags**
- variables

**Syntax**
- `REF <refTarget>, <sourceName>`

**Arguments**
- `<refTarget>`: identifier token (intended to be a `REF` variable name; see `variables.md`).
- `<sourceName>`: identifier token naming the source variable to bind to.

**Semantics**
- The current engine implementation throws a “not implemented” error at runtime.
- In this build, `REF` variables are still used by user-defined function argument binding (pass-by-reference); see `variables.md`.

**Errors & validation**
- Always errors at runtime.

**Examples**
- `REF X, A`

## REFBYNAME (instruction)

**Summary**
- Declared but **not implemented** in this engine build (always errors).

**Tags**
- variables

**Syntax**
- `REFBYNAME <refTarget>, <sourceName>`

**Arguments**
- `<refTarget>`: identifier token (intended to be a `REF` variable name; see `variables.md`).
- `<sourceName>` (string expression): evaluates to a variable name string.

**Semantics**
- The current engine implementation throws a “not implemented” error at runtime.
- In this build, `REF` variables are still used by user-defined function argument binding (pass-by-reference); see `variables.md`.

**Errors & validation**
- Always errors at runtime.

**Examples**
- `REFBYNAME X, "A"`

## HTML_PRINT (instruction)

**Summary**
- Prints an HTML string (Emuera’s HTML-like mini language) as console output.

**Tags**
- io

**Syntax**
- `HTML_PRINT <html> [, <toBuffer>]`

**Arguments**
- `<html>` (string): HTML string (see `html-output.md`).
- `<toBuffer>` (optional, int; default `0`)
  - `0` (default): print as a complete logical output line (implicit line end).
  - non-zero: append the HTML output into the current print buffer (no implicit line end).

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
- `HTML_TAGSPLIT <html> [, <outParts> [, <outCount>]]`

**Arguments**
- `<html>` (string): HTML string.
- `<outParts>` (optional; default `RESULTS`): changeable 1D **non-character** string array variable to receive parts.
- `<outCount>` (optional; default `RESULT`): changeable integer variable to receive the part count.

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
- Appends an inline image part to the current output line (equivalent to an `<img ...>` element in the HTML output model).

**Tags**
- ui

**Syntax**
- `PRINT_IMG <src>`
- `PRINT_IMG <src>, <srcb>`
- `PRINT_IMG <src>, <srcb>, <srcm>`
- `PRINT_IMG <src>, <srcb>, <srcm>, <width> [, <height> [, <ypos>]]`
- `PRINT_IMG <src>, <width> [, <height> [, <ypos>]]`

**Arguments**
- `<src>` (string expression): sprite name.
- `<srcb>` (optional, string expression): sprite name used when the region is selected/focused.
  - If this evaluates to `""`, it is treated as omitted.
- `<srcm>` (optional, string expression): mapping-sprite name used by mouse-input mapping color side channels (see `html-output.md` and `INPUT`).
- `<width>` / `<height>` / `<ypos>` (optional, int expressions): mixed numeric attributes.
  - Each numeric argument may be followed by a `px` suffix token to indicate pixels (e.g. `80px`).
  - Without `px`, the value is interpreted as a percentage of the current font size (in pixels): `valuePx = value * FontSize / 100`.
  - Numeric argument order is `width`, then `height`, then `ypos`.

**Semantics**
- Skipped when output skipping is active (via `SKIPDISP`).
- Appends an image part to the current print buffer (no implicit newline).
- The image part is equivalent to emitting an HTML `<img ...>` tag and letting the HTML renderer handle it:
  - `src=<src>`, `srcb=<srcb>`, `srcm=<srcm>`
  - `width=<width>`, `height=<height>`, `ypos=<ypos>` (only included when the numeric value is non-zero)
- See `html-output.md` (“Inline images: `<img ...>`”) for rendering rules:
  - If `height` is omitted or `0`, it defaults to the current font size (pixels).
  - If `width` is omitted or `0`, the original aspect ratio is preserved.
  - Negative `width` / `height` values flip the image horizontally/vertically.
  - If the sprite cannot be resolved, the tag is rendered as literal text.

**Errors & validation**
- Argument parse-time errors if more than 3 numeric arguments are provided, or if string arguments appear after numeric arguments.

**Examples**
- `PRINT_IMG "FACE_001"`
- `PRINT_IMG "FACE_001", 80px` (explicit pixel width)
- `PRINT_IMG "FACE_001", 120, 120` (width/height as percent of font size)

## PRINT_RECT (instruction)

**Summary**
- Appends a filled rectangle shape part to the current output line (equivalent to a `<shape type='rect' ...>` element in the HTML output model).

**Tags**
- ui

**Syntax**
- `PRINT_RECT <width>`
- `PRINT_RECT <x>, <y>, <width>, <height>`

**Arguments**
- The numeric arguments are int expressions in mixed units:
  - A numeric argument may be followed by a `px` suffix token to indicate pixels (e.g. `30px`).
  - Without `px`, the value is interpreted as a percentage of the current font size (pixels): `valuePx = value * FontSize / 100`.
- 1-argument form:
  - `<width>`: rectangle width (must be `> 0`).
  - Height is the current font size (pixels), and the rectangle starts at `(x=0, y=0)` within the line box.
- 4-argument form:
  - `<x>, <y>, <width>, <height>` define the rectangle (must satisfy `x >= 0`, `width > 0`, `height > 0`; `y` may be negative).

**Semantics**
- Skipped when output skipping is active (via `SKIPDISP`).
- Appends a rectangle shape part to the current print buffer (no implicit newline).
- The shape uses the current output color as its fill color, and uses the current “button color” when selected/focused.
- The output part is equivalent to emitting an HTML `<shape type='rect' ...>` tag; see `html-output.md` (“Shapes: `<shape ...>`”) for details and the literal-text fallback behavior for invalid params.

**Errors & validation**
- Parse-time error if the number of arguments is not exactly `1` or `4`.
- If the rectangle is not drawable (unsupported parameter constraints), it is rendered as literal text (the string form of the `<shape ...>` tag).

**Examples**
- `PRINT_RECT 200` (width = 200% of font size)
- `PRINT_RECT 0px, -20px, 100px, 20px`

## PRINT_SPACE (instruction)

**Summary**
- Appends a non-drawing horizontal space part to the current output line (equivalent to a `<shape type='space' ...>` element in the HTML output model).

**Tags**
- ui

**Syntax**
- `PRINT_SPACE <width>`

**Arguments**
- `<width>` (int expression): space width in mixed units.
  - May be followed by a `px` suffix token to indicate pixels (e.g. `40px`).
  - Without `px`, the value is interpreted as a percentage of the current font size (pixels): `widthPx = width * FontSize / 100`.

**Semantics**
- Skipped when output skipping is active (via `SKIPDISP`).
- Appends a space shape part to the current print buffer (no implicit newline).
- Equivalent to emitting an HTML `<shape type='space' ...>` tag; see `html-output.md` (“Shapes: `<shape ...>`”).

**Errors & validation**
- (none)

**Examples**
- `PRINT_SPACE 100` (one “em”, i.e. 100% of font size)
- `PRINT_SPACE 12px`

## TOOLTIP_SETCOLOR (instruction)

**Summary**
- Sets the tooltip text and background colors.

**Tags**
- ui

**Syntax**
- `TOOLTIP_SETCOLOR <foreColor>, <backColor>`

**Arguments**
- `<foreColor>` (int expression): RGB color `0x000000 .. 0xFFFFFF`.
- `<backColor>` (int expression): RGB color `0x000000 .. 0xFFFFFF`.

**Semantics**
- Updates the UI tooltip colors for subsequent tooltips.
- This instruction executes even when output skipping is active.

**Errors & validation**
- Runtime error if either color is outside `0 .. 0xFFFFFF`.

**Examples**
- `TOOLTIP_SETCOLOR 0xFFFFFF, 0x000000`

## TOOLTIP_SETDELAY (instruction)

**Summary**
- Sets the tooltip initial delay (time between hover and tooltip popup).

**Tags**
- ui

**Syntax**
- `TOOLTIP_SETDELAY <delayMs>`

**Arguments**
- `<delayMs>` (int expression): delay in milliseconds.
  - Omitted argument is accepted with a warning and treated as `0`.

**Semantics**
- Sets the tooltip initial delay used by the engine’s tooltip popup logic.
- This instruction executes even when output skipping is active.

**Errors & validation**
- Runtime error if `<delayMs> < 0` or `<delayMs> > 2147483647`.

**Examples**
- `TOOLTIP_SETDELAY 500`

## TOOLTIP_SETDURATION (instruction)

**Summary**
- Sets the tooltip display duration.

**Tags**
- ui

**Syntax**
- `TOOLTIP_SETDURATION <durationMs>`

**Arguments**
- `<durationMs>` (int expression): duration in milliseconds.
  - Omitted argument is accepted with a warning and treated as `0`.

**Semantics**
- Sets how long tooltips stay visible after appearing.
  - `0` uses the UI toolkit’s default “no explicit duration” mode.
- Values greater than `32767` are clamped to `32767`.
- This instruction executes even when output skipping is active.

**Errors & validation**
- Runtime error if `<durationMs> < 0` or `<durationMs> > 2147483647`.

**Examples**
- `TOOLTIP_SETDURATION 2000`
- `TOOLTIP_SETDURATION 0` (use default/indefinite mode)

## INPUTMOUSEKEY (instruction)

**Summary**
- Waits for a primitive mouse/key event (mouse down, wheel, key press, or timeout) and reports it via `RESULT` / `RESULT:*` (and sometimes `RESULTS`).

**Tags**
- io

**Syntax**
- `INPUTMOUSEKEY`
- `INPUTMOUSEKEY <timeMs>`

**Arguments**
- `<timeMs>` (optional, int expression): time limit in milliseconds.
  - If `timeMs > 0`, enables a timeout.
  - If omitted or `timeMs <= 0`, no timeout is used.

**Semantics**
- Enters a wait state for *primitive* input events (not text box submission).
- See also: `input-flow.md` (how primitive waits differ from textbox-segmentation waits).
- This instruction is **not** skipped by output skipping (`SKIPDISP`) because it is not a print-skip instruction.
- When an event occurs, the engine resumes script execution and assigns `RESULT_ARRAY[0..5]` (i.e. `RESULT` and `RESULT:1..5`) as follows.

Event type (`RESULT`):

- `1`: mouse button down
- `2`: mouse wheel
- `3`: key press
- `4`: timeout (only possible when `timeMs > 0`)

Payload (`RESULT:*`), by event type:

- Mouse button down (`RESULT == 1`):
  - `RESULT:1`: mouse button bit flag (`MouseButtons` integer value).
    - Typical values: left=`1048576`, right=`2097152`, middle=`4194304`.
  - `RESULT:2`: mouse `x` in client pixels (origin at the left edge).
  - `RESULT:3`: mouse `y` in client pixels, using a bottom-origin coordinate: `y = rawY - ClientHeight`.
  - `RESULT:4`: current button-map/background-map hit value (24-bit RGB), or `-1` when no opaque map pixel is available at the click position.
  - `RESULT:5`: if an **integer** button is currently selected, its button value; otherwise `0`.
  - Additionally, if a **string** button is currently selected, the engine assigns `RESULTS = <button string>` (and `RESULT:5 = 0`).
  - No additional `RESULT:6` payload is assigned by this instruction.

- Mouse wheel (`RESULT == 2`):
  - `RESULT:1`: wheel delta.
  - `RESULT:2`: mouse `x` (same coordinate system as above).
  - `RESULT:3`: mouse `y` (same coordinate system as above).
  - `RESULT:4 = 0`, `RESULT:5 = 0`.

- Key press (`RESULT == 3`):
  - `RESULT:1`: key code (`Keys` integer value).
  - `RESULT:2`: key data (`Keys` integer value).
  - `RESULT:3 = 0`, `RESULT:4 = 0`, `RESULT:5 = 0`.

- Timeout (`RESULT == 4`):
  - `RESULT:1..5 = 0`.

**Errors & validation**
- (none)

**Examples**
```erabasic
INPUTMOUSEKEY 1000
PRINTFORML "type=" + RESULT + " x=" + RESULT:2 + " y=" + RESULT:3
```

## AWAIT (instruction)

**Summary**
- Processes pending UI events and optionally sleeps for a short time (used to yield to the UI / drive animations).

**Tags**
- ui

**Syntax**
- `AWAIT`
- `AWAIT <timeMs>`

**Arguments**
- `<timeMs>` (optional, int expression):
  - If omitted, `AWAIT` yields without sleeping.
  - Otherwise must satisfy `0 <= timeMs <= 10000`.

**Semantics**
- Forces a redraw, sets an internal “sleep” state, processes UI events, and then:
  - if `timeMs > 0`, sleeps for `timeMs` milliseconds
  - otherwise returns immediately after event processing
- Does not assign `RESULT`/`RESULTS`.
- This instruction is **not** skipped by output skipping (`SKIPDISP`) because it is not a print-skip instruction.

**Errors & validation**
- Runtime error if `timeMs < 0` or `timeMs > 10000`.

**Examples**
- `AWAIT`         ; yield to UI
- `AWAIT 16`      ; ~60 FPS pacing

## VARSIZE (instruction)

**Summary**
- Writes the size of an array variable into `RESULT` / `RESULT:1` / `RESULT:2`.

**Tags**
- variables

**Syntax**
- `VARSIZE <arrayVarName>`

**Arguments**
- `<arrayVarName>`: an identifier token naming an array variable (not an expression).
  - Must be a 1D/2D/3D array variable (character-data arrays are allowed).
  - `RAND` is rejected (even though it is 1D).
  - Compatibility parsing: any extra characters after the identifier are ignored (with a warning). For example, `VARSIZE ABL:TARGET:0` is treated like `VARSIZE ABL`.
    - The ignored tail is not parsed as expressions and is not evaluated (so it has no side effects).

**Semantics**
- Resolves `<arrayVarName>` to a variable token.
- Writes array lengths into `RESULT_ARRAY`:
  - 1D array: `RESULT = length0`
  - 2D array: `RESULT = length0`, `RESULT:1 = length1`
  - 3D array: `RESULT = length0`, `RESULT:1 = length1`, `RESULT:2 = length2`
- Does not clear other `RESULT:*` slots.

**Errors & validation**
- Errors if `<arrayVarName>` is missing, is not a variable identifier, is not an array variable, or is `RAND`.

**Examples**
- `VARSIZE ABL` (writes the `ABL` dimensions to `RESULT*`)
- `VARSIZE ITEM` (writes the `ITEM` length to `RESULT`)

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
- `<x>` (int): base.
- `<y>` (int): exponent.

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
- Writes the configured `PrintCPerLine` value into an integer variable.

**Tags**
- config

**Syntax**
- `PRINTCPERLINE [<dest>]`

**Arguments**
- `<dest>` (optional; default `RESULT`): changeable integer variable term to receive the value.

**Semantics**
- Assigns the configuration value `PrintCPerLine` to `<dest>`.
- Does not print output.

**Errors & validation**
- Argument parsing fails if `<dest>` is provided but is not a changeable integer variable term.

**Examples**
- `PRINTCPERLINE`        ; writes into `RESULT`
- `PRINTCPERLINE X`      ; writes into `X`

## SAVENOS (instruction)

**Summary**
- Writes the configured `SaveDataNos` value into an integer variable.

**Tags**
- config

**Syntax**
- `SAVENOS [<dest>]`

**Arguments**
- `<dest>` (optional; default `RESULT`): changeable integer variable term to receive the value.

**Semantics**
- Assigns the configuration value `SaveDataNos` to `<dest>`.
- Does not print output.

**Errors & validation**
- Argument parsing fails if `<dest>` is provided but is not a changeable integer variable term.

**Examples**
- `SAVENOS`        ; writes into `RESULT`
- `SAVENOS X`      ; writes into `X`

## ENCODETOUNI (instruction)

**Summary**
- Encodes a string into Unicode scalar values and writes them into `RESULT:*`.

**Tags**
- string

**Syntax**
- `ENCODETOUNI`
- `ENCODETOUNI <formString>`

**Arguments**
- `<formString>` (optional, FORM/formatted string; default `""`): the string to encode.

**Semantics**
- Evaluates `<formString>` to a string `s`.
- Let `cap = length(RESULT_ARRAY) - 1` (because `RESULT:0` stores the length).
  - If `len(s) > cap`, runtime error.
- Produces an integer sequence of length `len(s)` by applying the platform’s UTF-16 conversion at each string index:
  - For each index `i` in `0 <= i < len(s)`, compute `code[i] = ConvertToUtf32(s, i)`.
  - Note: this is done at every index; if `s` contains a surrogate pair, converting at the *second* (low-surrogate) index raises an error.
- Writes the result to `RESULT_ARRAY`:
  - `RESULT:0 = len(s)`
  - For `0 <= i < len(s)`: `RESULT:(i+1) = code[i]`
- Does not clear any `RESULT:*` slots beyond `RESULT:len(s)`.

**Errors & validation**
- Runtime error if `len(s) > length(RESULT_ARRAY) - 1`.
- Runtime error if the UTF-16 conversion fails at any index (e.g. low surrogate, invalid surrogate pair).

**Examples**
```erabasic
ENCODETOUNI "ABC"
; RESULT:0 = 3
; RESULT:1 = 65
; RESULT:2 = 66
; RESULT:3 = 67
```

## PLAYSOUND (instruction)

**Summary**
- Plays a one-shot sound effect file from the sound directory.

**Tags**
- io

**Syntax**
- `PLAYSOUND <filename> [, <repeat>]`

**Arguments**
- `<filename>` (string expression): file name or relative path under the sound directory.
- `<repeat>` (optional, int; default `1`): number of times to repeat the sound.
  - Values `< 1` are clamped to `1`.

**Semantics**
- Resolves the path by concatenating the engine’s sound directory with `<filename>`, then normalizing to an absolute path.
- If the file does not exist, no-op.
- Otherwise, starts playback on a “sound effect slot”:
  - There are 10 slots (`0..9`).
  - The engine prefers the first non-playing slot; if all are playing, it reuses slot `0`.
- Playback is independent from BGM (`PLAYBGM`).

**Errors & validation**
- Runtime error if the file exists but cannot be decoded/played by the audio backend.

**Examples**
- `PLAYSOUND "click.wav"`
- `PLAYSOUND "se\\hit.ogg", 3`

## STOPSOUND (instruction)

**Summary**
- Stops all currently playing sound effects (all 10 sound effect slots).

**Tags**
- io

**Syntax**
- `STOPSOUND`

**Arguments**
- None.

**Semantics**
- Stops playback of all sound effect slots (`0..9`).
- Does not affect BGM (`PLAYBGM`).

**Errors & validation**
- (none)

**Examples**
- `STOPSOUND`

## PLAYBGM (instruction)

**Summary**
- Starts looping background music (BGM) from the sound directory.

**Tags**
- io

**Syntax**
- `PLAYBGM <filename>`

**Arguments**
- `<filename>` (string expression): file name or relative path under the sound directory.

**Semantics**
- Resolves the path by concatenating the engine’s sound directory with `<filename>`, then normalizing to an absolute path.
- If the file does not exist, no-op (does not stop any currently playing BGM).
- Otherwise, starts playback on the BGM channel and repeats indefinitely.
  - Starting a new BGM replaces the previous BGM.

**Errors & validation**
- Runtime error if the file exists but cannot be decoded/played by the audio backend.

**Examples**
- `PLAYBGM "bgm\\theme.flac"`

## STOPBGM (instruction)

**Summary**
- Stops the currently playing BGM.

**Tags**
- io

**Syntax**
- `STOPBGM`

**Arguments**
- None.

**Semantics**
- Stops BGM playback.
- Does not affect sound effects (`PLAYSOUND`).

**Errors & validation**
- (none)

**Examples**
- `STOPBGM`

## SETSOUNDVOLUME (instruction)

**Summary**
- Sets the volume for sound effects (`PLAYSOUND`) across all sound effect slots.

**Tags**
- io

**Syntax**
- `SETSOUNDVOLUME <volume>`

**Arguments**
- `<volume>` (int expression): volume level, clamped to `0 .. 100`.

**Semantics**
- Applies the volume to all 10 sound effect slots (`0..9`).
- If a slot is currently playing, the change takes effect immediately.

**Errors & validation**
- (none)

**Examples**
- `SETSOUNDVOLUME 30`

## SETBGMVOLUME (instruction)

**Summary**
- Sets the volume for BGM (`PLAYBGM`).

**Tags**
- io

**Syntax**
- `SETBGMVOLUME <volume>`

**Arguments**
- `<volume>` (int expression): volume level, clamped to `0 .. 100`.

**Semantics**
- Applies the volume to the BGM channel.
- If BGM is currently playing, the change takes effect immediately.

**Errors & validation**
- (none)

**Examples**
- `SETBGMVOLUME 50`

## TRYCALLF (instruction)

**Summary**
- Tries to call a **user-defined** expression function (`#FUNCTION/#FUNCTIONS`) by name; if it cannot be resolved, does nothing.

**Tags**
- calls

**Syntax**
- `TRYCALLF <methodName> [, <arg1>, <arg2>, ... ]`
- `TRYCALLF <methodName>(<arg1>, <arg2>, ... )`
- Optional (currently unused) bracket segment may appear after the name:
  - `TRYCALLF <methodName>[<subName1>, <subName2>, ...](...)`

**Arguments**
- `<methodName>`: a raw string token read up to `(` / `[` / `,` / `;` and then trimmed.
  - This is **not** a string literal or string expression.
  - Quotes are treated as ordinary characters.
  - Backslash escapes are processed (e.g. `\\n`, `\\t`, `\\s`).
- `<argN>`: expressions passed to the target method.

**Semantics**
- Resolution scope:
  - Only **user-defined** expression functions are considered (built-in expression functions are not).
- Resolves `<methodName>` to a user-defined expression function with the provided argument list.
  - If no matching method is found (or it cannot be resolved at load time for the constant-name fast path), the instruction is a no-op.
  - Otherwise evaluates the method.
- The return value is computed but not assigned to `RESULT/RESULTS` by this instruction.

**Errors & validation**
- The “try” behavior only covers “cannot resolve to a callable user-defined expression function”.
- Errors if a name resolves to an incompatible kind of function (not an expression function) or if argument checking/conversion fails.

**Examples**
- `TRYCALLF HOOK_AFTER_PRINT, TARGET`

## TRYCALLFORMF (instruction)

**Summary**
- Like `TRYCALLF`, but the method name is a formatted (FORM) string expression evaluated at runtime.

**Tags**
- calls

**Syntax**
- `TRYCALLFORMF <formString> [, <arg1>, <arg2>, ... ]`
- `TRYCALLFORMF <formString>(<arg1>, <arg2>, ... )`

**Arguments**
- `<formString>`: FORM/formatted string; the evaluated result is used as the method name.
- `<argN>`: expressions passed to the target method.

**Semantics**
- Evaluates `<formString>` to a name string, then behaves like `TRYCALLF`.
- The return value is computed but not assigned to `RESULT/RESULTS` by this instruction.

**Errors & validation**
- Same as `TRYCALLF`.

**Examples**
- `TRYCALLFORMF "HOOK_%TARGET%", TARGET`

## UPDATECHECK (instruction)

**Summary**
- Checks a remote “update check” URL and reports whether a newer version is available.

**Tags**
- system

**Syntax**
- `UPDATECHECK`

**Arguments**
- None.

**Semantics**
- Writes a status code into `RESULT`:
  - `0`: remote version string equals the current version string (no update).
  - `1`: remote version differs; user chose “No” in the confirmation dialog.
  - `2`: remote version differs; user chose “Yes” and the engine attempted to open the provided link in the OS.
  - `3`: update check failed (URL missing/invalid response/network/IO error).
  - `4`: update check is forbidden by config (`ForbidUpdateCheck`).
  - `5`: no network is available.
- The update check source is `UpdateCheckURL` from the game base metadata.
  - If it is missing/empty, sets `RESULT = 3`.
- If network is available and the URL is present:
  - Fetches the URL and reads the first two lines:
    - line 1: remote version string
    - line 2: link URL
  - If either line is missing/empty, sets `RESULT = 3`.
  - If the remote version string differs from the current version string:
    - Shows a confirmation dialog containing the version and link.
    - If the user accepts, sets `RESULT = 2` and opens the link via the OS.
    - Otherwise sets `RESULT = 1`.

**Errors & validation**
- No runtime errors; failures are reported via `RESULT`.

**Examples**
- `UPDATECHECK`
- `PRINTFORML "updatecheck=" + RESULT`

## QUIT_AND_RESTART (instruction)

**Summary**
- Requests the console to quit and restart the application.

**Tags**
- system

**Syntax**
- `QUIT_AND_RESTART`

**Arguments**
- None.

**Semantics**
- Sets the engine’s “reboot on quit” flag, then requests quit (same as `QUIT` for script control flow).
- Script execution stops immediately.
- The actual restart is performed by the UI host after the quit request is posted (typically on the next user interaction in the quit state).

**Errors & validation**
- (none)

**Examples**
- `QUIT_AND_RESTART`

## FORCE_QUIT (instruction)

**Summary**
- A “forced quit” instruction in this engine build.

**Tags**
- system

**Syntax**
- `FORCE_QUIT`

**Arguments**
- None.

**Semantics**
- In the current engine implementation, this instruction does not request a normal quit by itself.
- It participates in the same “consecutive forced restart” guard used by `FORCE_QUIT_AND_RESTART`.

**Errors & validation**
- May raise a runtime error on the guard path (see `FORCE_QUIT_AND_RESTART`).

**Examples**
- `FORCE_QUIT`

## FORCE_QUIT_AND_RESTART (instruction)

**Summary**
- Forces an immediate application restart (without waiting for the normal quit UI flow).

**Tags**
- system

**Syntax**
- `FORCE_QUIT_AND_RESTART`

**Arguments**
- None.

**Semantics**
- Sets the engine’s “reboot” flag and triggers the UI host’s restart routine immediately.
- Guard behavior (to prevent continuous restart without an intervening input wait):
  - If this instruction is executed again without passing through an input-wait/quit/error state, the engine shows a confirmation dialog.
  - If the user accepts, the engine cancels restart and raises a runtime error instead.

**Errors & validation**
- May raise a runtime error on the guard path (see above).

**Examples**
- `FORCE_QUIT_AND_RESTART`

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
- Waits for a text input, then stores it as either an integer (`RESULT`) or a string (`RESULTS`) depending on whether it parses as a 64-bit integer.

**Tags**
- io

**Syntax**
- `INPUTANY`

**Arguments**
- None.

**Semantics**
- Enters an input wait (`InputType = AnyValue`).
- See also: `input-flow.md` (shared submission paths, segment draining/discard rules, and `MesSkip` interaction).
- On completion:
  - If the submitted text parses as a signed 64-bit integer, assigns it to `RESULT`.
  - Otherwise assigns the submitted text to `RESULTS`.
- Does **not** clear the “other” result:
  - If an integer is accepted, `RESULTS` remains unchanged.
  - If a string is accepted, `RESULT` remains unchanged.
- Empty input is accepted as a string `""` (which produces no visible echo because printing an empty string outputs nothing).
- This instruction is **not** skipped by output skipping (`SKIPDISP`) because it is not a print-skip instruction.

**Errors & validation**
- (none)

**Examples**
```erabasic
INPUTANY
IF RESULTS != ""
  PRINTFORML "string: " + RESULTS
ELSE
  PRINTFORML "int: " + RESULT
ENDIF
```

## TOOLTIP_SETFONT (instruction)

**Summary**
- Sets the font family name used when drawing tooltips (in custom-draw mode).

**Tags**
- ui

**Syntax**
- `TOOLTIP_SETFONT <fontName>`

**Arguments**
- `<fontName>` (string expression): font family name.

**Semantics**
- Stores the font name used by tooltip custom drawing (`TOOLTIP_CUSTOM 1`).
- This instruction executes even when output skipping is active.

**Errors & validation**
- (none)

**Examples**
- `TOOLTIP_SETFONT "MS Gothic"`

## TOOLTIP_SETFONTSIZE (instruction)

**Summary**
- Sets the font size (in points) used when drawing tooltips (in custom-draw mode).

**Tags**
- ui

**Syntax**
- `TOOLTIP_SETFONTSIZE <size>`

**Arguments**
- `<size>` (int expression): font size value passed to the UI font constructor.

**Semantics**
- Stores the tooltip font size used by tooltip custom drawing (`TOOLTIP_CUSTOM 1`).
- This instruction executes even when output skipping is active.

**Errors & validation**
- (none)

**Examples**
- `TOOLTIP_SETFONTSIZE 12`

## TOOLTIP_CUSTOM (instruction)

**Summary**
- Enables/disables owner-drawn (custom rendered) tooltips.

**Tags**
- ui

**Syntax**
- `TOOLTIP_CUSTOM <enabled>`

**Arguments**
- `<enabled>` (int expression): `0` disables custom tooltips; non-zero enables.

**Semantics**
- When enabled, tooltips are drawn via the engine’s custom draw logic, which supports:
  - custom font name/size (`TOOLTIP_SETFONT`, `TOOLTIP_SETFONTSIZE`)
  - custom text formatting flags (`TOOLTIP_FORMAT`)
  - optional image tooltips (`TOOLTIP_IMG`)
- This instruction executes even when output skipping is active.

**Errors & validation**
- (none)

**Examples**
- `TOOLTIP_CUSTOM 1`

## TOOLTIP_FORMAT (instruction)

**Summary**
- Sets the tooltip text rendering flags used by the UI text renderer (in custom-draw mode).

**Tags**
- ui

**Syntax**
- `TOOLTIP_FORMAT <flags>`

**Arguments**
- `<flags>` (int expression): bitmask passed through as `.NET` `TextFormatFlags`.

**Semantics**
- Updates the text format flags used when drawing tooltip text in custom-draw mode (`TOOLTIP_CUSTOM 1`).
- This instruction executes even when output skipping is active.

**Errors & validation**
- (none)

**Examples**
- `TOOLTIP_FORMAT 0`

## TOOLTIP_IMG (instruction)

**Summary**
- Enables/disables “image tooltip” interpretation in custom-draw tooltips.

**Tags**
- ui

**Syntax**
- `TOOLTIP_IMG <enabled>`

**Arguments**
- `<enabled>` (int expression): `0` disables; non-zero enables.

**Semantics**
- When enabled and tooltips are custom-drawn (`TOOLTIP_CUSTOM 1`):
  - If the tooltip text can be parsed as an integer `i`, the engine attempts to draw graphics resource `G:i` as the tooltip content.
  - If the graphics resource is not available, it falls back to drawing the tooltip text.
- This instruction executes even when output skipping is active.

**Errors & validation**
- (none)

**Examples**
- `TOOLTIP_CUSTOM 1`
- `TOOLTIP_IMG 1`

## BINPUT (instruction)

**Summary**
- Like `INPUT`, but only accepts an integer that matches a currently selectable **integer button** on screen.

**Tags**
- io

**Syntax**
- `BINPUT [<default> [, <mouse> [, <canSkip> [, ... ]]]]`

**Arguments**
- `<default>` (optional, int expression): used only when the submitted text is empty (not used for invalid integer text).
- `<mouse>` (optional, int; default `0`): if non-zero, enables mouse-based completion and the same mouse side channels as `INPUT`.
- `<canSkip>` (optional, int): presence enables the `MesSkip` fast path; its numeric value is ignored (not evaluated).
- Extra arguments after `<canSkip>` are accepted by the argument parser but ignored by the runtime.

**Semantics**
- Ensures the current output is drawn before waiting (flushes any pending buffer and forces a refresh).
- See also: `input-flow.md` (shared submission paths, segment draining/discard rules, and `MesSkip` interaction).
- If there is no selectable integer button available:
  - If `<default>` is omitted: runtime error.
  - Otherwise: immediately accepts `<default>` (writes it to `RESULT`) and returns without waiting.
- Waits for an integer input and accepts it **only if** it matches a selectable integer button value:
  - Accepted if there exists an integer button with `buttonValue == input` in the current selectable button generation.
  - Otherwise the input is rejected and the engine stays in the wait state.
- Default handling:
  - If the user submits empty input and `<default>` is present, the engine uses the default value *as the input*.
  - That default is still rejected if no matching integer button exists.
- On successful completion:
  - Assigns the accepted value to `RESULT`.
  - Echoes the accepted input text to output (UI behavior).
- `MesSkip` integration:
  - If `<canSkip>` is present and `MesSkip` is currently true, the engine does not wait and instead accepts the default immediately.
  - In that no-wait path:
    - `<default>` must be present; otherwise the engine throws a runtime error.
    - The accepted value is written to:
      - `RESULT` if `<mouse> == 0`
      - `RESULT_ARRAY[1]` if `<mouse> != 0`
    - The input string is not echoed.
- Mouse side channels:
  - When `<mouse> != 0` and the input is completed via a mouse click, the same UI-side `RESULT_ARRAY[...]` / `RESULTS_ARRAY[...]` side channels as `INPUT` are written (see `INPUT`).
- Output skipping (`SKIPDISP`):
  - Same interaction as `INPUT` (reaching input while output skipping is active due to `SKIPDISP` is a runtime error).

**Errors & validation**
- Runtime error if no selectable integer button exists and `<default>` is omitted.
- Argument parsing errors if provided arguments are not integer expressions.

**Examples**
```erabasic
PRINTBUTTON "A", 10
PRINTBUTTON "B", 20
PRINTL ""
BINPUT
PRINTFORML "picked=" + RESULT
```

## BINPUTS (instruction)

**Summary**
- Like `INPUTS`, but only accepts a string that matches a currently selectable **button** on screen.

**Tags**
- io

**Syntax**
- `BINPUTS [<default> [, <mouse> [, <canSkip>]]]`

**Arguments**
- `<default>` (optional, string expression): default string used only when the submitted text is empty.
- `<mouse>` (optional, int; default `0`): if non-zero, enables mouse-based completion and the same mouse side channels as `INPUTS`.
- `<canSkip>` (optional, int): presence enables the `MesSkip` fast path; its numeric value is ignored (not evaluated).

**Semantics**
- Ensures the current output is drawn before waiting (flushes any pending buffer and forces a refresh).
- See also: `input-flow.md` (shared submission paths, segment draining/discard rules, and `MesSkip` interaction).
- If there is no selectable button available:
  - If `<default>` is omitted: runtime error.
  - Otherwise: immediately accepts `<default>` (writes it to `RESULTS`) and returns without waiting.
- Waits for a string input and accepts it **only if** it matches a selectable button:
  - Accepted if there exists a button where either:
    - it is a string button and `buttonString == input`, or
    - it is an integer button and `buttonValue.ToString() == input`.
  - Otherwise the input is rejected and the engine stays in the wait state.
- Default handling:
  - If the user submits empty input and `<default>` is present, the engine uses the default string *as the input*.
  - That default is still rejected if no matching button exists.
- On successful completion:
  - Assigns the accepted string to `RESULTS`.
  - Echoes the accepted input text to output (UI behavior).
- `MesSkip` integration:
  - If `<canSkip>` is present and `MesSkip` is currently true, the engine does not wait and instead accepts the default immediately.
  - In that no-wait path:
    - `<default>` must be present; otherwise the engine throws a runtime error.
    - The accepted value is written to:
      - `RESULTS` if `<mouse> == 0`
      - `RESULTS_ARRAY[1]` if `<mouse> != 0`
    - The input string is not echoed.
- Mouse side channels:
  - When `<mouse> != 0` and the input is completed via a mouse click, the same UI-side `RESULT_ARRAY[...]` / `RESULTS_ARRAY[...]` side channels as `INPUTS` are written (see `INPUT`).
- Output skipping (`SKIPDISP`):
  - Same interaction as `INPUTS` (runtime error).

**Errors & validation**
- Runtime error if no selectable button exists and `<default>` is omitted.
- Argument parsing quirks:
  - The parser first reads `<default>` as a formatted-string expression up to the first comma.
  - After the first comma, if `<mouse>` is omitted or is not an integer expression, the engine warns and ignores the entire tail (mouse input is disabled; `canSkip` is not enabled).
  - Supplying both `<mouse>` and `<canSkip>` may still emit a “too many arguments” warning, but the `<canSkip>` presence is accepted and used by the runtime.

**Examples**
```erabasic
PRINTBUTTONS "Yes", "Y"
PRINTBUTTONS "No", "N"
PRINTL ""
BINPUTS
PRINTFORML "picked=" + RESULTS
```

## ONEBINPUT (instruction)

**Summary**
- Like `BINPUT`, but uses “one input” mode (`OneInput = true`) for submitted UI text.

**Tags**
- io

**Syntax**
- `ONEBINPUT [<default> [, <mouse> [, <canSkip> [, ... ]]]]`

**Arguments**
- Same argument model as `BINPUT`.

**Semantics**
- Same button-matching and default rules as `BINPUT`.
- Exact one-input rule:
  - One-input truncation is applied per submitted segment; see `input-flow.md` for the shared submission/segmentation model.
  - Each submitted segment is normally truncated to its first character.
  - Exception: if the segment is accepted through the mouse-click completion path and config option `AllowLongInputByMouse` is enabled (see `config-items.md`), that mouse-submitted text is not truncated.
  - This truncation applies only to submitted UI text. Defaults accepted via empty input or the `MesSkip` no-wait path are used as-is by `ONEBINPUT` itself.

**Errors & validation**
- Same as `BINPUT`.

**Examples**
```erabasic
PRINTBUTTON "0", 0
PRINTBUTTON "1", 1
PRINTL ""
ONEBINPUT
```

## ONEBINPUTS (instruction)

**Summary**
- Like `BINPUTS`, but uses “one input” mode (`OneInput = true`) for submitted UI text.

**Tags**
- io

**Syntax**
- `ONEBINPUTS [<default> [, <mouse> [, <canSkip>]]]`

**Arguments**
- Same argument model as `BINPUTS`.

**Semantics**
- Same button-matching and default rules as `BINPUTS`.
- Exact one-input rule:
  - One-input truncation is applied per submitted segment; see `input-flow.md` for the shared submission/segmentation model.
  - Each submitted segment is normally truncated to its first character.
  - Exception: if the segment is accepted through the mouse-click completion path and config option `AllowLongInputByMouse` is enabled (see `config-items.md`), that mouse-submitted text is not truncated.
  - This truncation applies only to submitted UI text. Defaults accepted via empty input or the `MesSkip` no-wait path are used as-is by `ONEBINPUTS` itself.

**Errors & validation**
- Same as `BINPUTS`.

**Examples**
```erabasic
PRINTBUTTONS "A", "A"
PRINTBUTTONS "B", "B"
PRINTL ""
ONEBINPUTS
```

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
- `<html>` (string): HTML string (see `html-output.md`).
- `<ignored>` (optional, int): compatibility-only argument.
  - If provided, it must be a valid `int` expression (it is parsed and type-checked).
  - The value is ignored by `HTML_PRINT_ISLAND` and is not evaluated during execution.

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
- `<raw text>` (optional, default `""`): raw text, not an expression.

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
  - The written chara selector is also not evaluated (no side effects from that expression).
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
  - The written chara selector is also not evaluated (no side effects from that expression).
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
- Tests whether a character template exists for a given character `NO` in the CSV-backed character database.

**Tags**
- characters

**Syntax**
- `EXISTCSV(charaNo [, isSp])`

**Signatures / argument rules**
- `EXISTCSV(charaNo)` → `long`
- `EXISTCSV(charaNo, isSp)` → `long`

**Arguments**
- `charaNo` (int): character template `NO` to look up.
- `isSp` (optional, int; default `0`): whether to look up in the SP-character template set.
  - `0`: normal character templates
  - non-zero: SP character templates

**Semantics**
- Returns `1` if a character template exists for `charaNo` in the selected template set, otherwise returns `0`.

**Errors & validation**
- Runtime error if `isSp != 0` while the compatibility option “use SP characters” is disabled (`CompatiSPChara = false`).

**Examples**
- `ok = EXISTCSV(100)`

## VARSIZE (expression function)

**Summary**
- Returns the length of an array variable’s dimension.

**Tags**
- variables

**Syntax**
- `VARSIZE(varName [, dim])`

**Signatures / argument rules**
- `VARSIZE(varName)` → `int`
- `VARSIZE(varName, dim)` → `int`

**Arguments**
- `varName` (string): variable name to resolve.
  - This is a variable **name**, not a variable term. Do not include `:` indices (for example, `"CFLAG:TARGET:0"` does not resolve as a variable name).
- `dim` (optional, int; default `0`): dimension selector.
  - Default behavior: `0` selects the first dimension (0-based).
  - If `VarsizeDimConfig` is enabled and `dim > 0`, the engine subtracts `1` before selecting the dimension (i.e. `1` selects the first dimension).

**Semantics**
- Resolves `varName` to a variable token using the normal variable-name lookup rules.
- Returns `GetLength(dim)` of that variable token.
  - For a 1D array, valid `dim` is `0`.
  - For a 2D array, valid `dim` is `0` or `1`.
  - For a 3D array, valid `dim` is `0`, `1`, or `2`.
- Reference variables (`REF`) are supported as long as they currently refer to an array; otherwise it errors.

**Errors & validation**
- Runtime error if `varName` does not resolve to a variable.
- Runtime error if the resolved variable is not an array variable.
- Runtime error if `dim` is out of range for that variable’s dimension count (including negative values).
- Runtime error if the resolved variable is a `REF` variable that is currently unbound.

**Examples**
- `n = VARSIZE("ITEM")` (length of `ITEM`)
- `w = VARSIZE("CFLAG", 1)` (first dimension when `VarsizeDimConfig` is enabled)

## CHKFONT (expression function)

**Summary**
- Tests whether a given font family name is available to the engine.

**Tags**
- ui

**Syntax**
- `CHKFONT(name)`

**Signatures / argument rules**
- `CHKFONT(name)` → `long`

**Arguments**
- `name` (string): font family name to look up.

**Semantics**
- Returns `1` if `name` exactly matches (`==`) the `.Name` of:
  - any system-installed font family, or
  - any font family loaded into the engine’s private font collection.
- Otherwise returns `0`.

**Errors & validation**
- (none)

**Examples**
- `ok = CHKFONT("Arial")`

## CHKDATA (expression function)

**Summary**
- Checks whether a numbered save file exists and is loadable, and reports a short status message.

**Tags**
- save-files

**Syntax**
- `CHKDATA(saveIndex)`

**Signatures / argument rules**
- `CHKDATA(saveIndex)` → `long`

**Arguments**
- `saveIndex` (int): save slot index used to form the file name `save<saveIndex>.sav` (with at least 2 digits) under the save directory.

**Semantics**
- Checks the save file and returns a status code:
  - `0`: OK (loadable)
  - `1`: file not found
  - `2`: different game
  - `3`: different version
  - `4`: other error (corrupt / read error / type mismatch)
- Also writes a message string to `RESULTS:0`:
  - for OK: the save message stored in the file
  - for not found: `"----"`
  - for errors: a human-readable error message

**Errors & validation**
- Runtime error if `saveIndex < 0` or `saveIndex > 2147483647`.

**Examples**
- `state = CHKDATA(0)`   ; checks `save00.sav`
- `msg = RESULTS:0`

## ISSKIP (expression function)

**Summary**
- Reports whether the script runner is currently in “skip output” mode.

**Tags**
- runtime

**Syntax**
- `ISSKIP()`

**Signatures / argument rules**
- `ISSKIP()` → `long`

**Arguments**
- (none)

**Semantics**
- Returns `1` if skip-print mode is active, otherwise returns `0`.

**Errors & validation**
- (none)

**Examples**
- `if ISSKIP() == 0: PRINTFORML "not skipping"`

## MOUSESKIP (expression function)

**Summary**
- Deprecated alias of `MESSKIP()`.

**Tags**
- ui

**Syntax**
- `MOUSESKIP()`

**Signatures / argument rules**
- `MOUSESKIP()` → `long`

**Arguments**
- (none)

**Semantics**
- Same return value as `MESSKIP()`.

**Errors & validation**
- Parse-time warning: calling `MOUSESKIP()` emits a deprecation warning recommending `MESSKIP()`.

**Examples**
- `skipping = MOUSESKIP()`

## MESSKIP (expression function)

**Summary**
- Reports whether message-skip mode is currently active in the UI.

**Tags**
- ui

**Syntax**
- `MESSKIP()`

**Signatures / argument rules**
- `MESSKIP()` → `long`

**Arguments**
- (none)

**Semantics**
- Returns `1` if message-skip mode is active, otherwise returns `0`.

**Errors & validation**
- (none)

**Examples**
- `skipping = MESSKIP()`

## GETCOLOR (expression function)

**Summary**
- Returns the current foreground text color as a 24-bit RGB integer.

**Tags**
- ui

**Syntax**
- `GETCOLOR()`

**Signatures / argument rules**
- `GETCOLOR()` → `long`

**Arguments**
- (none)

**Semantics**
- Returns the current text color as `0xRRGGBB`:
  - `ConsoleStringColor.ToArgb() & 0xFFFFFF`.

**Errors & validation**
- (none)

**Examples**
- `c = GETCOLOR()`

## GETDEFCOLOR (expression function)

**Summary**
- Returns the configured default foreground text color as a 24-bit RGB integer.

**Tags**
- ui
- config

**Syntax**
- `GETDEFCOLOR()`

**Signatures / argument rules**
- `GETDEFCOLOR()` → `long`

**Arguments**
- (none)

**Semantics**
- Returns the configured default text color (`ForeColor`) as `0xRRGGBB`:
  - `ForeColor.ToArgb() & 0xFFFFFF`.

**Errors & validation**
- (none)

**Examples**
- `c = GETDEFCOLOR()`

## GETFOCUSCOLOR (expression function)

**Summary**
- Returns the configured focus highlight color as a 24-bit RGB integer.

**Tags**
- ui
- config

**Syntax**
- `GETFOCUSCOLOR()`

**Signatures / argument rules**
- `GETFOCUSCOLOR()` → `long`

**Arguments**
- (none)

**Semantics**
- Returns the configured focus color (`FocusColor`) as `0xRRGGBB`:
  - `FocusColor.ToArgb() & 0xFFFFFF`.

**Errors & validation**
- (none)

**Examples**
- `c = GETFOCUSCOLOR()`

## GETBGCOLOR (expression function)

**Summary**
- Returns the current background color as a 24-bit RGB integer.

**Tags**
- ui

**Syntax**
- `GETBGCOLOR()`

**Signatures / argument rules**
- `GETBGCOLOR()` → `long`

**Arguments**
- (none)

**Semantics**
- Returns the current background color as `0xRRGGBB`:
  - `ConsoleBgColor.ToArgb() & 0xFFFFFF`.

**Errors & validation**
- (none)

**Examples**
- `c = GETBGCOLOR()`

## GETDEFBGCOLOR (expression function)

**Summary**
- Returns the configured default background color as a 24-bit RGB integer.

**Tags**
- ui
- config

**Syntax**
- `GETDEFBGCOLOR()`

**Signatures / argument rules**
- `GETDEFBGCOLOR()` → `long`

**Arguments**
- (none)

**Semantics**
- Returns the configured default background color (`BackColor`) as `0xRRGGBB`:
  - `BackColor.ToArgb() & 0xFFFFFF`.

**Errors & validation**
- (none)

**Examples**
- `c = GETDEFBGCOLOR()`

## GETSTYLE (expression function)

**Summary**
- Returns the current text style (bold/italic/strikeout/underline) as a bitmask.

**Tags**
- ui

**Syntax**
- `GETSTYLE()`

**Signatures / argument rules**
- `GETSTYLE()` → `long`

**Arguments**
- (none)

**Semantics**
- Returns a bitmask where:
  - bit `0` (`1`): bold
  - bit `1` (`2`): italic
  - bit `2` (`4`): strikeout
  - bit `3` (`8`): underline
- The return value is the OR of all currently enabled bits.

**Errors & validation**
- (none)

**Examples**
- `style = GETSTYLE()`

## GETFONT (expression function)

**Summary**
- Returns the current font name used for console output.

**Tags**
- ui

**Syntax**
- `GETFONT()`

**Signatures / argument rules**
- `GETFONT()` → `string`

**Arguments**
- (none)

**Semantics**
- Returns the current font name string.

**Errors & validation**
- (none)

**Examples**
- `font = GETFONT()`

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
- Returns the current line alignment mode of the console output.

**Tags**
- ui

**Syntax**
- `CURRENTALIGN()`

**Signatures / argument rules**
- `CURRENTALIGN()` → `string`

**Arguments**
- (none)

**Semantics**
- Returns one of:
  - `"LEFT"`
  - `"CENTER"`
  - `"RIGHT"`

**Errors & validation**
- (none)

**Examples**
- `align = CURRENTALIGN()`

## CURRENTREDRAW (expression function)

**Summary**
- Reports whether the console is currently in an auto-redraw mode.

**Tags**
- ui

**Syntax**
- `CURRENTREDRAW()`

**Signatures / argument rules**
- `CURRENTREDRAW()` → `long`

**Arguments**
- (none)

**Semantics**
- Returns `0` if redraw mode is off, otherwise returns `1`.

**Errors & validation**
- (none)

**Examples**
- `isRedrawing = CURRENTREDRAW()`

## COLOR_FROMNAME (expression function)

**Summary**
- Converts a named color to a 24-bit RGB integer.

**Tags**
- ui

**Syntax**
- `COLOR_FROMNAME(name)`

**Signatures / argument rules**
- `COLOR_FROMNAME(name)` → `long`

**Arguments**
- `name` (string): a color name recognized by `System.Drawing.Color.FromName`.

**Semantics**
- If `name` resolves to a non-transparent color, returns `0xRRGGBB` as an integer:
  - `(R << 16) + (G << 8) + B`.
- If `name` is not a valid color name, returns `-1`.

**Errors & validation**
- Runtime error if `name` is `"transparent"` (case-insensitive). This special name is treated as “unsupported”.

**Examples**
- `c = COLOR_FROMNAME("Red")` returns `0xFF0000`.
- `c = COLOR_FROMNAME("not_a_color")` returns `-1`.

## COLOR_FROMRGB (expression function)

**Summary**
- Builds a 24-bit RGB integer from separate color components.

**Tags**
- ui

**Syntax**
- `COLOR_FROMRGB(r, g, b)`

**Signatures / argument rules**
- `COLOR_FROMRGB(r, g, b)` → `long`

**Arguments**
- `r` (int): red component, must satisfy `0 <= r <= 255`.
- `g` (int): green component, must satisfy `0 <= g <= 255`.
- `b` (int): blue component, must satisfy `0 <= b <= 255`.

**Semantics**
- Returns `0xRRGGBB` as an integer:
  - `(r << 16) + (g << 8) + b`.

**Errors & validation**
- Runtime error if any component is outside `0..255`.

**Examples**
- `c = COLOR_FROMRGB(255, 0, 0)` returns `0xFF0000`.

## CHKCHARADATA (expression function)

**Summary**
- Checks whether a character-variable save file exists and is loadable, and reports a short status message.

**Tags**
- save-files

**Syntax**
- `CHKCHARADATA(name)`

**Signatures / argument rules**
- `CHKCHARADATA(name)` → `long`

**Arguments**
- `name` (string): the save “name” suffix used to form the file name `chara_<name>.dat` under the engine’s data directory.

**Semantics**
- Checks the file `chara_<name>.dat` and returns a status code:
  - `0`: OK (loadable)
  - `1`: file not found
  - `2`: different game
  - `3`: different version
  - `4`: other error (corrupt / read error / type mismatch)
- Also writes a message string to `RESULTS:0`:
  - for OK: the save message stored in the file
  - for not found: `"----"`
  - for errors: a human-readable error message

**Errors & validation**
- (none)

**Examples**
- `state = CHKCHARADATA("00")`
- `msg = RESULTS:0`

## FIND_CHARADATA (expression function)

**Summary**
- Lists character-variable save files matching a wildcard pattern.

**Tags**
- save-files

**Syntax**
- `FIND_CHARADATA([pattern])`

**Signatures / argument rules**
- `FIND_CHARADATA()` → `long`
- `FIND_CHARADATA(pattern)` → `long`

**Arguments**
- `pattern` (optional, string; default `*`): wildcard pattern applied to the `<name>` part of `chara_<name>.dat`.

**Semantics**
- Searches the engine’s data directory for files matching `chara_<pattern>.dat`.
- Extracts each match’s `<name>` (the part after `chara_` and before the `.dat` extension).
- Writes the extracted names into the `RESULTS` string array starting at `RESULTS:0`:
  - If there are more matches than the `RESULTS` array length, only the first `length(RESULTS)` names are written.
  - If there are fewer matches than the `RESULTS` array length, entries past the written prefix are left unchanged.
- Returns the total number of matches found (including any not written due to truncation).

**Errors & validation**
- (none)

**Examples**
- `n = FIND_CHARADATA()`               ; list all `chara_*.dat`
- `n = FIND_CHARADATA("foo*")`         ; list `chara_foo*.dat`
- `first = RESULTS:0`

## MONEYSTR (expression function)

**Summary**
- Formats an integer as a currency string using the engine’s configured currency label and placement.

**Tags**
- formatting

**Syntax**
- `MONEYSTR(money [, format])`

**Signatures / argument rules**
- `MONEYSTR(money)` → `string`
- `MONEYSTR(money, format)` → `string`

**Arguments**
- `money` (int)
- `format` (optional, string; default = no custom formatting): passed to `Int64.ToString(format)`.

**Semantics**
- Formats `money`:
  - if `format` is omitted: uses `money.ToString()`
  - otherwise: uses `money.ToString(format)`
- Then attaches the currency label (`MoneyLabel`) either as a prefix or suffix depending on `MoneyFirst`:
  - `MoneyFirst = true`: `MoneyLabel + formatted`
  - `MoneyFirst = false`: `formatted + MoneyLabel`

**Errors & validation**
- Runtime error if `format` is not a valid `Int64.ToString` format string.

**Examples**
- `MONEYSTR(123)` → `"$123"` if `MoneyLabel="$"` and `MoneyFirst=true`.
- `MONEYSTR(123, \"D6\")` → `"$000123"` under the same config.

## PRINTCPERLINE (expression function)

**Summary**
- Returns the configured “items per line” setting used by `PRINTC`.

**Tags**
- config

**Syntax**
- `PRINTCPERLINE()`

**Signatures / argument rules**
- `PRINTCPERLINE()` → `long`

**Arguments**
- (none)

**Semantics**
- Returns the configuration item `PrintCPerLine`.

**Errors & validation**
- (none)

**Examples**
- `n = PRINTCPERLINE()`

## PRINTCLENGTH (expression function)

**Summary**
- Returns the configured “item character length” setting used by `PRINTC`.

**Tags**
- config

**Syntax**
- `PRINTCLENGTH()`

**Signatures / argument rules**
- `PRINTCLENGTH()` → `long`

**Arguments**
- (none)

**Semantics**
- Returns the configuration item `PrintCLength`.

**Errors & validation**
- (none)

**Examples**
- `n = PRINTCLENGTH()`

## SAVENOS (expression function)

**Summary**
- Returns the configured number of save slots shown per page in the save UI.

**Tags**
- config

**Syntax**
- `SAVENOS()`

**Signatures / argument rules**
- `SAVENOS()` → `long`

**Arguments**
- (none)

**Semantics**
- Returns the configuration item `SaveDataNos`.

**Errors & validation**
- (none)

**Examples**
- `n = SAVENOS()`

## GETTIME (expression function)

**Summary**
- Returns a numeric timestamp encoding of the current local time.

**Tags**
- time

**Syntax**
- `GETTIME()`

**Signatures / argument rules**
- `GETTIME()` → `long`

**Arguments**
- (none)

**Semantics**
- Returns a base-10 integer encoding:
  - `YYYYMMDDHHMMSSmmm` (year, month, day, hour, minute, second, millisecond; local time).
- Components are combined as:
  - `(((((year * 100 + month) * 100 + day) * 100 + hour) * 100 + minute) * 100 + second) * 1000 + millisecond`.
- Note: the engine reads each component from `DateTime.Now` separately; if the system clock crosses a boundary while evaluating, different components may come from different instants.

**Errors & validation**
- (none)

**Examples**
- `GETTIME()` at `2026-03-05 09:07:02.004` returns `20260305090702004`.

## GETTIMES (expression function)

**Summary**
- Returns a formatted timestamp string for the current local time.

**Tags**
- time

**Syntax**
- `GETTIMES()`

**Signatures / argument rules**
- `GETTIMES()` → `string`

**Arguments**
- (none)

**Semantics**
- Returns `DateTime.Now.ToString("yyyy/MM/dd HH:mm:ss")` (local time).

**Errors & validation**
- (none)

**Examples**
- `GETTIMES()` might return `2026/03/05 09:07:02`.

## GETMILLISECOND (expression function)

**Summary**
- Returns the number of milliseconds elapsed since `0001-01-01 00:00:00` (local time).

**Tags**
- time

**Syntax**
- `GETMILLISECOND()`

**Signatures / argument rules**
- `GETMILLISECOND()` → `long`

**Arguments**
- (none)

**Semantics**
- Returns `DateTime.Now.Ticks / 10000` (ticks are 100-nanosecond units).

**Errors & validation**
- (none)

**Examples**
- `ms = GETMILLISECOND()`

## GETSECOND (expression function)

**Summary**
- Returns the number of seconds elapsed since `0001-01-01 00:00:00` (local time).

**Tags**
- time

**Syntax**
- `GETSECOND()`

**Signatures / argument rules**
- `GETSECOND()` → `long`

**Arguments**
- (none)

**Semantics**
- Returns `DateTime.Now.Ticks / 10000000` (ticks are 100-nanosecond units).

**Errors & validation**
- (none)

**Examples**
- `sec = GETSECOND()`

## RAND (expression function)

**Summary**
- Returns a random integer in a half-open range using the engine's current RNG mode.

**Tags**
- math

**Syntax**
- `RAND(max)`
- `RAND(min, max)`

**Signatures / argument rules**
- `RAND(max)` → `long`
- `RAND(min, max)` → `long`

**Arguments**
- `min` (optional, int; default `0`): inclusive lower bound.
- `max` (int): exclusive upper bound.

**Semantics**
- Returns a random integer `r` such that `min <= r < max`.
- RNG engine selection depends on JSON `UseNewRandom`:
  - `UseNewRandom=NO` (legacy mode): uses the legacy SFMT generator with the MT19937 parameter set. The returned value is computed as `min + (nextUInt64 % (max - min))`. This is deterministic for a given seed/state, but it is not perfectly unbiased when `(max - min)` does not divide `2^64`.
  - `UseNewRandom=YES` (new mode): uses a host `.NET System.Random` instance and its `NextInt64(max - min)` behavior, then adds `min`. `RANDOMIZE`, `INITRAND`, and `DUMPRAND` do not control this mode.
- In new mode, the host `System.Random` instance is created when the runtime creates its variable-evaluator state; scripts have no built-in way to reseed or snapshot it.

**Errors & validation**
- Runtime error if `max <= min`.
  - In particular, `RAND(0)` and `RAND(<negative>)` are errors.

**Examples**
- `RAND(10)` returns a value in `0 <= r < 10`.
- `RAND(5, 8)` returns `5`, `6`, or `7`.

## MIN (expression function)

**Summary**
- Returns the minimum of one or more integers.

**Tags**
- math

**Syntax**
- `MIN(x [, y ...])`

**Signatures / argument rules**
- `MIN(x [, y ...])` → `long`
  - Requires at least 1 argument.

**Arguments**
- `x` (int)
- `y...` (optional, int)

**Semantics**
- Returns the minimum value among all provided arguments.

**Errors & validation**
- (none)

**Examples**
- `MIN(1)` returns `1`.
- `MIN(1, 5, 2)` returns `1`.

## MAX (expression function)

**Summary**
- Returns the maximum of one or more integers.

**Tags**
- math

**Syntax**
- `MAX(x [, y ...])`

**Signatures / argument rules**
- `MAX(x [, y ...])` → `long`
  - Requires at least 1 argument.

**Arguments**
- `x` (int)
- `y...` (optional, int)

**Semantics**
- Returns the maximum value among all provided arguments.

**Errors & validation**
- (none)

**Examples**
- `MAX(1)` returns `1`.
- `MAX(1, 5, 2)` returns `5`.

## ABS (expression function)

**Summary**
- Returns the absolute value of an integer.

**Tags**
- math

**Syntax**
- `ABS(x)`

**Signatures / argument rules**
- `ABS(x)` → `long`

**Arguments**
- `x` (int)

**Semantics**
- Returns `Math.Abs(x)`.

**Errors & validation**
- Runtime error if `x == -9223372036854775808` (the minimum `Int64`), because `ABS(x)` would overflow.

**Examples**
- `ABS(-3)` returns `3`.
- `ABS(3)` returns `3`.

## POWER (expression function)

**Summary**
- Returns `x^y` (x to the power y), truncated to an integer.

**Tags**
- math

**Syntax**
- `POWER(x, y)`

**Signatures / argument rules**
- `POWER(x, y)` → `long`

**Arguments**
- `x` (int)
- `y` (int)

**Semantics**
- Computes `Math.Pow((double)x, (double)y)` and returns it truncated toward `0` as an integer.

**Errors & validation**
- Runtime error if the computed value is NaN, Infinity, or outside the `Int64` range.

**Examples**
- `POWER(2, 10)` returns `1024`.
- `POWER(2, -1)` returns `0`.

## SQRT (expression function)

**Summary**
- Returns the square root of an integer, truncated to an integer.

**Tags**
- math

**Syntax**
- `SQRT(x)`

**Signatures / argument rules**
- `SQRT(x)` → `long`

**Arguments**
- `x` (int): must be non-negative.

**Semantics**
- Computes `Math.Sqrt((double)x)` and returns it truncated toward `0` as an integer.

**Errors & validation**
- Runtime error if `x < 0`.

**Examples**
- `SQRT(0)` returns `0`.
- `SQRT(2)` returns `1`.
- `SQRT(4)` returns `2`.

## CBRT (expression function)

**Summary**
- Returns the cube root of an integer, truncated to an integer.

**Tags**
- math

**Syntax**
- `CBRT(x)`

**Signatures / argument rules**
- `CBRT(x)` → `long`

**Arguments**
- `x` (int): must be non-negative.

**Semantics**
- Computes `Math.Pow((double)x, 1.0 / 3.0)` and returns it truncated toward `0` as an integer.

**Errors & validation**
- Runtime error if `x < 0`.

**Examples**
- `CBRT(0)` returns `0`.
- `CBRT(7)` returns `1`.
- `CBRT(8)` returns `2`.

## LOG (expression function)

**Summary**
- Returns the natural logarithm of an integer, truncated to an integer.

**Tags**
- math

**Syntax**
- `LOG(x)`

**Signatures / argument rules**
- `LOG(x)` → `long`

**Arguments**
- `x` (int): must be greater than `0`.

**Semantics**
- Computes `Math.Log((double)x)` (base *e*) and returns it truncated toward `0` as an integer.

**Errors & validation**
- Runtime error if `x <= 0`.
- Runtime error if the computed value is NaN, Infinity, or outside the `Int64` range.

**Examples**
- `LOG(1)` returns `0`.
- `LOG(2)` returns `0` (since `ln(2)` is between `0` and `1`).

## LOG10 (expression function)

**Summary**
- Returns the base-10 logarithm of an integer, truncated to an integer.

**Tags**
- math

**Syntax**
- `LOG10(x)`

**Signatures / argument rules**
- `LOG10(x)` → `long`

**Arguments**
- `x` (int): must be greater than `0`.

**Semantics**
- Computes `Math.Log10((double)x)` and returns it truncated toward `0` as an integer.

**Errors & validation**
- Runtime error if `x <= 0`.
- Runtime error if the computed value is NaN, Infinity, or outside the `Int64` range.

**Examples**
- `LOG10(1)` returns `0`.
- `LOG10(9)` returns `0`.
- `LOG10(10)` returns `1`.

## EXPONENT (expression function)

**Summary**
- Returns `e^x` (the exponential function), truncated to an integer.

**Tags**
- math

**Syntax**
- `EXPONENT(x)`

**Signatures / argument rules**
- `EXPONENT(x)` → `long`

**Arguments**
- `x` (int)

**Semantics**
- Computes `Math.Exp((double)x)` and returns it truncated toward `0` as an integer.

**Errors & validation**
- Runtime error if the computed value is NaN, Infinity, or outside the `Int64` range.

**Examples**
- `EXPONENT(0)` returns `1`.
- `EXPONENT(1)` returns `2`.
- `EXPONENT(-1)` returns `0`.

## SIGN (expression function)

**Summary**
- Returns the sign of an integer.

**Tags**
- math

**Syntax**
- `SIGN(x)`

**Signatures / argument rules**
- `SIGN(x)` → `long`

**Arguments**
- `x` (int)

**Semantics**
- Returns:
  - `-1` if `x < 0`
  - `0` if `x == 0`
  - `1` if `x > 0`

**Errors & validation**
- (none)

**Examples**
- `SIGN(-10)` returns `-1`.
- `SIGN(0)` returns `0`.
- `SIGN(10)` returns `1`.

## LIMIT (expression function)

**Summary**
- Clamps an integer value to a specified inclusive range.

**Tags**
- math

**Syntax**
- `LIMIT(value, min, max)`

**Signatures / argument rules**
- `LIMIT(value, min, max)` → `long`

**Arguments**
- `value` (int)
- `min` (int)
- `max` (int)

**Semantics**
- Returns:
  - `min` if `value < min`
  - `max` if `value > max`
  - otherwise `value`
- Note: `min` and `max` are used as written; they are not swapped if `min > max`.

**Errors & validation**
- (none)

**Examples**
- `LIMIT(5, 0, 10)` returns `5`.
- `LIMIT(-1, 0, 10)` returns `0`.
- `LIMIT(11, 0, 10)` returns `10`.

## SUMARRAY (expression function)

**Summary**
- Returns the sum of elements in an integer array over a specified index range.

**Tags**
- arrays

**Syntax**
- `SUMARRAY(arrayVarTerm [, startIndex [, endIndex]])`

**Signatures / argument rules**
- `SUMARRAY(arrayVarTerm)` → `long`
- `SUMARRAY(arrayVarTerm, startIndex)` → `long`
- `SUMARRAY(arrayVarTerm, startIndex, endIndex)` → `long`

**Arguments**
- `arrayVarTerm` (int array variable term): an integer array variable term (1D/2D/3D; character-data arrays are allowed).
  - The operation sums along the **last** dimension.
  - Any subscript written in the **last** slot of `arrayVarTerm` is ignored for addressing (but is still validated as an in-range index).
    - 1D: `A:x` → sums `A[i]` (the written `x` is ignored)
    - 2D: `A:x:y` → sums `A[x, i]` (the written `y` is ignored)
    - 3D: `A:x:y:z` → sums `A[x, y, i]` (the written `z` is ignored)
    - character-data 1D: `C:chara:x` → sums `C[chara, i]` (the written `x` is ignored)
    - character-data 2D: `C:chara:x:y` → sums `C[chara, x, i]` (the written `y` is ignored)
- `startIndex` (optional, int; default `0`): inclusive start index in the summed dimension.
- `endIndex` (optional, int; default = length of the summed dimension): exclusive end index in the summed dimension.

**Semantics**
- Returns `Σ arrayVarTerm[...]` over indices `i` with `startIndex <= i < endIndex` using the addressing rules above.
- If `startIndex >= endIndex`, returns `0`.

**Errors & validation**
- Parse-time error if `arrayVarTerm` is not a non-`CONST` integer array variable term.
- Runtime error if:
  - `startIndex < 0` or `endIndex < 0`
  - `startIndex > length` or `endIndex > length` (where `length` is the length of the summed dimension)
  - any fixed indices inside `arrayVarTerm` are out of range
  - the ignored “last-slot” subscript written in `arrayVarTerm` is out of range

**Examples**
- `total = SUMARRAY(A, 0, 10)`
- `total = SUMARRAY(B:2:0, 5, 8)`  ; sums `B[2,5] + B[2,6] + B[2,7]`
- `total = SUMARRAY(CFLAG, 0, 100)` ; sums `CFLAG[TARGET,i]` for `0 <= i < 100`

## SUMCARRAY (expression function)

**Summary**
- Returns the sum of a character-data integer variable over a specified character-index range.

**Tags**
- characters
- arrays

**Syntax**
- `SUMCARRAY(charaVarTerm [, startIndex [, endIndex]])`

**Signatures / argument rules**
- `SUMCARRAY(charaVarTerm)` → `long`
- `SUMCARRAY(charaVarTerm, startIndex)` → `long`
- `SUMCARRAY(charaVarTerm, startIndex, endIndex)` → `long`

**Arguments**
- `charaVarTerm` (character-data int array variable term): selects which per-character cell to read.
  - The function scans characters and treats the scanned index `i` as the effective character selector.
  - Any written chara selector in `charaVarTerm` does not affect which characters are scanned.
  - Subscripts written after the chara selector (if any) select which per-character cell is summed:
    - character 1D array: reads `V[i, index]`
    - character 2D array: reads `V[i, index1, 0]` (the second index is not used by this function and behaves as `0`)
- `startIndex` (optional, int; default `0`): inclusive start chara index.
- `endIndex` (optional, int; default `CHARANUM`): exclusive end chara index.

**Semantics**
- Returns `Σ charaVarTerm[i]` over character indices `i` with `startIndex <= i < endIndex` using the addressing rules above.
- If `startIndex >= endIndex`, returns `0`.

**Errors & validation**
- Parse-time error if `charaVarTerm` is not a character-data integer array variable term.
- Runtime error if:
  - `startIndex < 0` or `startIndex >= CHARANUM`
  - `endIndex < 0` or `endIndex > CHARANUM`
  - any “after-chara” subscripts inside `charaVarTerm` are out of range
  - any written chara selector inside `charaVarTerm` is out of range (even though it does not affect the scan)

**Examples**
- `sum = SUMCARRAY(CFLAG:3)`        ; sums `CFLAG[i,3]` for `0 <= i < CHARANUM`
- `sum = SUMCARRAY(TALENT:0, 0, 10)` ; sums `TALENT[i,0]` for `0 <= i < 10`

## MATCH (expression function)

**Summary**
- Counts how many elements in an array equal a target value.

**Tags**
- arrays

**Syntax**
- `MATCH(arrayVarTerm, value [, startIndex [, endIndex]])`

**Signatures / argument rules**
- `MATCH(arrayVarTerm, value)` → `long`
- `MATCH(arrayVarTerm, value, startIndex)` → `long`
- `MATCH(arrayVarTerm, value, startIndex, endIndex)` → `long`

**Arguments**
- `arrayVarTerm` (1D array variable term): a 1D variable term (int or string). Character-data 1D arrays are allowed (the chara selector chooses the character slice).
  - The written subscript of a 1D `arrayVarTerm` is ignored for addressing (but is still validated as an in-range index).
- `value` (int|string; must match the array element type): target value.
- `startIndex` (optional, int; default `0`): inclusive start index.
- `endIndex` (optional, int; default = array length): exclusive end index.

**Semantics**
- Counts indices `i` with `startIndex <= i < endIndex` where the element equals `value`.
- Equality:
  - int array: `==`
  - string array: `==` (ordinal string equality in .NET), with the following rule:
    - if `value` is `""`, then both `""` and `null` elements are counted as matches
- Returns the count (0 or greater).

**Errors & validation**
- Parse-time error if `arrayVarTerm` is not a 1D array variable term.
- Runtime error if:
  - `startIndex < 0` or `endIndex < 0`
  - `startIndex > length` or `endIndex > length`
  - the ignored written subscript in `arrayVarTerm` is out of range

**Examples**
- `n = MATCH(A, 0)`
- `n = MATCH(S, "", 0, 100)`
- `n = MATCH(CFLAG, 1, 0, 50)` ; counts in `CFLAG[TARGET,i]` for `0 <= i < 50`

## CMATCH (expression function)

**Summary**
- Counts how many characters in the current character list have a given character-data cell equal to a target value.

**Tags**
- characters

**Syntax**
- `CMATCH(charaVarTerm, value [, startIndex [, endIndex]])`

**Signatures / argument rules**
- `CMATCH(charaVarTerm, value)` → `long`
- `CMATCH(charaVarTerm, value, startIndex)` → `long`
- `CMATCH(charaVarTerm, value, startIndex, endIndex)` → `long`

**Arguments**
- `charaVarTerm` (character-data variable term): selects which per-character cell to compare.
  - The function scans characters and treats the scanned index `i` as the effective character selector.
  - Any written chara selector in `charaVarTerm` does not affect the scan.
  - Subscripts written after the chara selector (if any) select the per-character cell:
    - scalar character variable: compares `V[i]`
    - character 1D array: compares `V[i, index]`
    - character 2D array: compares `V[i, index1, index2]`
- `value` (int|string; must match the selected cell type): target value.
- `startIndex` (optional, int; default `0`): inclusive start chara index.
- `endIndex` (optional, int; default `CHARANUM`): exclusive end chara index.

**Semantics**
- Counts character indices `i` with `startIndex <= i < endIndex` where the selected cell equals `value`.
- Equality:
  - int cell: `==`
  - string cell: `==` (ordinal string equality in .NET), with the following rule:
    - if `value` is `""`, then both `""` and `null` cells are counted as matches
- Returns the count (0 or greater).

**Errors & validation**
- Error if `charaVarTerm` is not a character-data variable term.
- Runtime error if:
  - `startIndex < 0` or `startIndex >= CHARANUM`
  - `endIndex < 0` or `endIndex > CHARANUM`
  - any “after-chara” subscripts inside `charaVarTerm` are out of range
  - any written chara selector inside `charaVarTerm` is out of range (even though it does not affect the scan)

**Examples**
- `n = CMATCH(TALENT, 1)`
- `n = CMATCH(CFLAG:3, 0, 0, CHARANUM)`

## GROUPMATCH (expression function)

**Summary**
- Counts how many of the trailing arguments are equal to the first argument.

**Tags**
- math

**Syntax**
- `GROUPMATCH(base, value1 [, value2 ...])`

**Signatures / argument rules**
- `GROUPMATCH(base, value1 [, value2 ...])` → `long`
  - Requires at least 2 arguments.
  - All arguments must have the same type (int or string).

**Arguments**
- `base` (int|string)
- `valueN` (int|string): values to compare against `base`.

**Semantics**
- Returns the number of `valueN` that compare equal to `base` using `==`.
- The first argument `base` is not counted as a match against itself.

**Errors & validation**
- Parse-time error if any `valueN` has a different type from `base`.

**Examples**
- `GROUPMATCH(1, 1, 2, 1)` returns `2`.
- `GROUPMATCH("a", "a", "b")` returns `1`.

## NOSAMES (expression function)

**Summary**
- Tests whether all arguments are pairwise distinct.

**Tags**
- math

**Syntax**
- `NOSAMES(a, b [, c ...])`

**Signatures / argument rules**
- `NOSAMES(a, b [, c ...])` → `long`
  - Requires at least 2 arguments.
  - All arguments must have the same type (int or string).

**Arguments**
- `a` (int|string)
- `b` (int|string)
- `c...` (optional, int|string)

**Semantics**
- Returns `1` if no two arguments are equal (using `==`), otherwise returns `0`.

**Errors & validation**
- Parse-time error if the argument types do not match.

**Examples**
- `NOSAMES(1, 2, 3)` returns `1`.
- `NOSAMES(1, 2, 1)` returns `0`.

## ALLSAMES (expression function)

**Summary**
- Tests whether all arguments are equal to the first argument.

**Tags**
- math

**Syntax**
- `ALLSAMES(a, b [, c ...])`

**Signatures / argument rules**
- `ALLSAMES(a, b [, c ...])` → `long`
  - Requires at least 2 arguments.
  - All arguments must have the same type (int or string).

**Arguments**
- `a` (int|string)
- `b` (int|string)
- `c...` (optional, int|string)

**Semantics**
- Returns `1` if `a == b == c == ...`, otherwise returns `0`.

**Errors & validation**
- Parse-time error if the argument types do not match.

**Examples**
- `ALLSAMES(1, 1, 1)` returns `1`.
- `ALLSAMES(1, 1, 2)` returns `0`.

## MAXARRAY (expression function)

**Summary**
- Returns the maximum integer value in an array range.

**Tags**
- arrays

**Syntax**
- `MAXARRAY(arrayVarTerm [, startIndex [, endIndex]])`

**Signatures / argument rules**
- `MAXARRAY(arrayVarTerm)` → `long`
- `MAXARRAY(arrayVarTerm, startIndex)` → `long`
- `MAXARRAY(arrayVarTerm, startIndex, endIndex)` → `long`

**Arguments**
- `arrayVarTerm` (int 1D array variable term): a 1D integer array variable term. Character-data 1D arrays are allowed (the chara selector chooses the character slice).
  - The written subscript of a 1D `arrayVarTerm` is ignored for addressing (but is still validated as an in-range index).
- `startIndex` (optional, int; default `0`): start index.
- `endIndex` (optional, int; default = array length): end index.

**Semantics**
- Reads `ret = element[startIndex]`, then scans `i` from `startIndex + 1` while `i < endIndex`, and updates `ret = max(ret, element[i])`.
- If `endIndex <= startIndex`, returns `element[startIndex]` (the single element at `startIndex`).

**Errors & validation**
- Parse-time error if `arrayVarTerm` is not an integer 1D array variable term.
- Runtime error if:
  - `startIndex < 0` or `startIndex >= length`
  - `endIndex < 0` or `endIndex > length`
  - the ignored written subscript in `arrayVarTerm` is out of range

**Examples**
- `m = MAXARRAY(A)`
- `m = MAXARRAY(A, 10, 20)`
- `m = MAXARRAY(CFLAG, 0, 100)` ; max within `CFLAG[TARGET,i]` for `0 <= i < 100`

## MAXCARRAY (expression function)

**Summary**
- Returns the maximum integer value of a character-data cell over a character-index range.

**Tags**
- characters

**Syntax**
- `MAXCARRAY(charaVarTerm [, startIndex [, endIndex]])`

**Signatures / argument rules**
- `MAXCARRAY(charaVarTerm)` → `long`
- `MAXCARRAY(charaVarTerm, startIndex)` → `long`
- `MAXCARRAY(charaVarTerm, startIndex, endIndex)` → `long`

**Arguments**
- `charaVarTerm` (character-data int 1D array variable term): selects which per-character cell to read.
  - The function scans characters and treats the scanned index `i` as the effective character selector.
  - Any written chara selector in `charaVarTerm` does not affect the scan.
  - The subscript written after the chara selector selects the per-character cell: reads `V[i, index]`.
- `startIndex` (optional, int; default `0`): start chara index.
- `endIndex` (optional, int; default `CHARANUM`): end chara index.

**Semantics**
- Reads `ret = cell[startIndex]`, then scans `i` from `startIndex + 1` while `i < endIndex`, and updates `ret = max(ret, cell[i])`.
- If `endIndex <= startIndex`, returns `cell[startIndex]` (the single cell at `startIndex`).

**Errors & validation**
- Parse-time error if `charaVarTerm` is not a character-data integer 1D array variable term.
- Runtime error if:
  - `startIndex < 0` or `startIndex >= CHARANUM`
  - `endIndex < 0` or `endIndex > CHARANUM`
  - any “after-chara” subscripts inside `charaVarTerm` are out of range
  - any written chara selector inside `charaVarTerm` is out of range (even though it does not affect the scan)

**Examples**
- `m = MAXCARRAY(CFLAG:3)`
- `m = MAXCARRAY(CFLAG:3, 0, CHARANUM)`

## MINARRAY (expression function)

**Summary**
- Returns the minimum integer value in an array range.

**Tags**
- arrays

**Syntax**
- `MINARRAY(arrayVarTerm [, startIndex [, endIndex]])`

**Signatures / argument rules**
- `MINARRAY(arrayVarTerm)` → `long`
- `MINARRAY(arrayVarTerm, startIndex)` → `long`
- `MINARRAY(arrayVarTerm, startIndex, endIndex)` → `long`

**Arguments**
- `arrayVarTerm` (int 1D array variable term): a 1D integer array variable term. Character-data 1D arrays are allowed (the chara selector chooses the character slice).
  - The written subscript of a 1D `arrayVarTerm` is ignored for addressing (but is still validated as an in-range index).
- `startIndex` (optional, int; default `0`): start index.
- `endIndex` (optional, int; default = array length): end index.

**Semantics**
- Reads `ret = element[startIndex]`, then scans `i` from `startIndex + 1` while `i < endIndex`, and updates `ret = min(ret, element[i])`.
- If `endIndex <= startIndex`, returns `element[startIndex]` (the single element at `startIndex`).

**Errors & validation**
- Parse-time error if `arrayVarTerm` is not an integer 1D array variable term.
- Runtime error if:
  - `startIndex < 0` or `startIndex >= length`
  - `endIndex < 0` or `endIndex > length`
  - the ignored written subscript in `arrayVarTerm` is out of range

**Examples**
- `m = MINARRAY(A)`
- `m = MINARRAY(A, 10, 20)`

## MINCARRAY (expression function)

**Summary**
- Returns the minimum integer value of a character-data cell over a character-index range.

**Tags**
- characters

**Syntax**
- `MINCARRAY(charaVarTerm [, startIndex [, endIndex]])`

**Signatures / argument rules**
- `MINCARRAY(charaVarTerm)` → `long`
- `MINCARRAY(charaVarTerm, startIndex)` → `long`
- `MINCARRAY(charaVarTerm, startIndex, endIndex)` → `long`

**Arguments**
- `charaVarTerm` (character-data int 1D array variable term): selects which per-character cell to read.
  - The function scans characters and treats the scanned index `i` as the effective character selector.
  - Any written chara selector in `charaVarTerm` does not affect the scan.
  - The subscript written after the chara selector selects the per-character cell: reads `V[i, index]`.
- `startIndex` (optional, int; default `0`): start chara index.
- `endIndex` (optional, int; default `CHARANUM`): end chara index.

**Semantics**
- Reads `ret = cell[startIndex]`, then scans `i` from `startIndex + 1` while `i < endIndex`, and updates `ret = min(ret, cell[i])`.
- If `endIndex <= startIndex`, returns `cell[startIndex]` (the single cell at `startIndex`).

**Errors & validation**
- Parse-time error if `charaVarTerm` is not a character-data integer 1D array variable term.
- Runtime error if:
  - `startIndex < 0` or `startIndex >= CHARANUM`
  - `endIndex < 0` or `endIndex > CHARANUM`
  - any “after-chara” subscripts inside `charaVarTerm` are out of range
  - any written chara selector inside `charaVarTerm` is out of range (even though it does not affect the scan)

**Examples**
- `m = MINCARRAY(CFLAG:3)`

## GETBIT (expression function)

**Summary**
- Extracts a single bit from a 64-bit integer.

**Tags**
- math

**Syntax**
- `GETBIT(n, m)`

**Signatures / argument rules**
- `GETBIT(n, m)` → `long`

**Arguments**
- `n` (int): treated as a signed 64-bit value.
- `m` (int): bit position, must satisfy `0 <= m <= 63` (`0` = least-significant bit).

**Semantics**
- Returns `((n >> m) & 1)`.

**Errors & validation**
- Runtime error if `m < 0` or `m > 63`.

**Examples**
- `GETBIT(5, 0)` returns `1`.
- `GETBIT(5, 2)` returns `1`.
- `GETBIT(5, 1)` returns `0`.

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
- Searches a 1D array for a target and returns the first matching index.

**Tags**
- arrays

**Syntax**
- `FINDELEMENT(arrayVarTerm, target [, startIndex [, endIndex [, exact]]])`

**Signatures / argument rules**
- `FINDELEMENT(arrayVarTerm, target)` → `long`
- `FINDELEMENT(arrayVarTerm, target, startIndex)` → `long`
- `FINDELEMENT(arrayVarTerm, target, startIndex, endIndex)` → `long`
- `FINDELEMENT(arrayVarTerm, target, startIndex, endIndex, exact)` → `long`

**Arguments**
- `arrayVarTerm` (1D array variable term): a 1D variable term (int or string). Character-data 1D arrays are allowed (the chara selector chooses the character slice).
  - The written subscript of a 1D `arrayVarTerm` is ignored for addressing (but is still validated as an in-range index).
- `target`:
  - int array: int value to match
  - string array: a **regular expression pattern** (see “Semantics”)
- `startIndex` (optional, int; default `0`): inclusive start index.
- `endIndex` (optional, int; default = array length): exclusive end index.
- `exact` (optional, int; default `0`): only meaningful for string arrays.
  - `0`: regex partial match
  - non-zero: regex full-string match

**Semantics**
- If `startIndex >= endIndex`, returns `-1`.
- int array:
  - Returns the first index `i` with `startIndex <= i < endIndex` where `array[i] == target`, or `-1` if not found.
  - `exact` is accepted but has no effect.
- string array:
  - Compiles `target` as a .NET regular expression pattern.
  - Treats `null` array elements as `""` during matching.
  - If `exact != 0`, returns the first index whose string fully matches the regex.
  - Otherwise, returns the first index whose string contains a regex match.

**Errors & validation**
- Parse-time error if `arrayVarTerm` is not a 1D array variable term.
- Runtime error if:
  - `startIndex < 0` or `endIndex < 0`
  - `startIndex > length` or `endIndex > length`
  - the ignored written subscript in `arrayVarTerm` is out of range
  - the regex pattern is invalid (string array case)

**Examples**
- `i = FINDELEMENT(A, 0)`
- `i = FINDELEMENT(S, \"^Alice$\", 0, 100, 1)`

## FINDLASTELEMENT (expression function)

**Summary**
- Searches a 1D array for a target and returns the last matching index.

**Tags**
- arrays

**Syntax**
- `FINDLASTELEMENT(arrayVarTerm, target [, startIndex [, endIndex [, exact]]])`

**Signatures / argument rules**
- `FINDLASTELEMENT(arrayVarTerm, target)` → `long`
- `FINDLASTELEMENT(arrayVarTerm, target, startIndex)` → `long`
- `FINDLASTELEMENT(arrayVarTerm, target, startIndex, endIndex)` → `long`
- `FINDLASTELEMENT(arrayVarTerm, target, startIndex, endIndex, exact)` → `long`

**Arguments**
- Same as `FINDELEMENT`.

**Semantics**
- Same as `FINDELEMENT`, except it searches backward and returns the last matching index in `[startIndex, endIndex)`.

**Errors & validation**
- Same as `FINDELEMENT`.

**Examples**
- `i = FINDLASTELEMENT(A, 0)`
- `i = FINDLASTELEMENT(S, \"Alice\", 0, 100, 1)`  ; exact regex match

## INRANGE (expression function)

**Summary**
- Tests whether a value is within an inclusive numeric range.

**Tags**
- math

**Syntax**
- `INRANGE(value, min, max)`

**Signatures / argument rules**
- `INRANGE(value, min, max)` → `long`

**Arguments**
- `value` (int)
- `min` (int)
- `max` (int)

**Semantics**
- Returns `1` if `min <= value <= max`, otherwise returns `0`.

**Errors & validation**
- (none)

**Examples**
- `INRANGE(5, 0, 10)` returns `1`.
- `INRANGE(10, 0, 10)` returns `1`.
- `INRANGE(11, 0, 10)` returns `0`.

## INRANGEARRAY (expression function)

**Summary**
- Counts how many elements of an integer array are within a numeric range.

**Tags**
- arrays

**Syntax**
- `INRANGEARRAY(arrayVarTerm, min, max [, startIndex [, endIndex]])`

**Signatures / argument rules**
- `INRANGEARRAY(arrayVarTerm, min, max)` → `long`
- `INRANGEARRAY(arrayVarTerm, min, max, startIndex)` → `long`
- `INRANGEARRAY(arrayVarTerm, min, max, startIndex, endIndex)` → `long`

**Arguments**
- `arrayVarTerm` (int 1D array variable term): a 1D integer array variable term. Character-data 1D arrays are allowed (the chara selector chooses the character slice).
  - The written subscript of a 1D `arrayVarTerm` is ignored for addressing (but is still validated as an in-range index).
- `min` (int): inclusive lower bound.
- `max` (int): exclusive upper bound.
- `startIndex` (optional, int; default `0`): inclusive start index.
- `endIndex` (optional, int; default = array length): exclusive end index.

**Semantics**
- Returns how many indices `i` satisfy:
  - `startIndex <= i < endIndex`, and
  - `min <= array[i] < max`.
- If `startIndex >= endIndex`, returns `0`.

**Errors & validation**
- Parse-time error if `arrayVarTerm` is not an integer 1D array variable term.
- Runtime error if:
  - `startIndex < 0` or `endIndex < 0`
  - `startIndex > length` or `endIndex > length`
  - the ignored written subscript in `arrayVarTerm` is out of range

**Examples**
- `n = INRANGEARRAY(A, 0, 10)`       ; counts `0 <= A[i] < 10`
- `n = INRANGEARRAY(CFLAG, 1, 2)`   ; counts `CFLAG[TARGET,i] == 1`

## INRANGECARRAY (expression function)

**Summary**
- Counts how many characters have a character-data cell within a numeric range.

**Tags**
- characters

**Syntax**
- `INRANGECARRAY(charaVarTerm, min, max [, startIndex [, endIndex]])`

**Signatures / argument rules**
- `INRANGECARRAY(charaVarTerm, min, max)` → `long`
- `INRANGECARRAY(charaVarTerm, min, max, startIndex)` → `long`
- `INRANGECARRAY(charaVarTerm, min, max, startIndex, endIndex)` → `long`

**Arguments**
- `charaVarTerm` (character-data int 1D array variable term): selects which per-character cell to test.
  - The function scans characters and treats the scanned index `i` as the effective character selector.
  - Any written chara selector in `charaVarTerm` does not affect the scan.
  - The subscript written after the chara selector selects the per-character cell: reads `V[i, index]`.
- `min` (int): inclusive lower bound.
- `max` (int): exclusive upper bound.
- `startIndex` (optional, int; default `0`): inclusive start chara index.
- `endIndex` (optional, int; default `CHARANUM`): exclusive end chara index.

**Semantics**
- Returns how many character indices `i` satisfy:
  - `startIndex <= i < endIndex`, and
  - `min <= cell[i] < max`.
- If `startIndex >= endIndex`, returns `0`.

**Errors & validation**
- Parse-time error if `charaVarTerm` is not a character-data integer 1D array variable term.
- Runtime error if:
  - `startIndex < 0` or `startIndex >= CHARANUM`
  - `endIndex < 0` or `endIndex > CHARANUM`
  - any “after-chara” subscripts inside `charaVarTerm` are out of range
  - any written chara selector inside `charaVarTerm` is out of range (even though it does not affect the scan)

**Examples**
- `n = INRANGECARRAY(CFLAG:3, 1, 2)` ; counts `CFLAG[i,3] == 1`

## GETNUMB (expression function)
**Summary**
- (TODO: not yet documented)

## ARRAYMSORT (expression function)

**Summary**
- Sorts one or more array variables in-place using the first argument as the sort key array.

**Tags**
- arrays

**Syntax**
- `ARRAYMSORT(keyArray, array1 [, array2 ...])`

**Signatures / argument rules**
- `ARRAYMSORT(keyArray, array1 [, array2 ...])` → `long`

**Arguments**
- `keyArray` (array variable term): non-character 1D array variable term (int or string). Must not be `CONST` or a calculated/pseudo variable.
- `arrayN` (array variable term): one or more non-character array variable terms (1D/2D/3D; int or string). Must not be `CONST` or calculated.
  - Any subscripts written in these variable terms are ignored; the function operates on the underlying array storage.

**Semantics**
- Builds a permutation by scanning `keyArray` from index `0` and collecting a prefix of entries:
  - int key array: stops at the first `0`
  - string key array: stops at the first `null` or empty string
- Sorts that collected prefix in ascending order by key:
  - int keys: numeric ascending
  - string keys: `string.CompareTo` ordering (current culture)
- Applies the resulting permutation to each argument array (including `keyArray` itself):
  - 1D arrays: permutes elements `0 .. n-1`
  - 2D arrays: permutes rows by the first index (`[row, col]`)
  - 3D arrays: permutes slabs by the first index (`[i, j, k]`)
- If any argument array’s first dimension is shorter than `n`, the function returns `0`.
  - This function is not atomic: earlier arrays may already have been permuted before the failure is detected.
- Returns `1` on success.

**Errors & validation**
- Errors if:
  - `keyArray` is not a 1D array variable term
  - any `arrayN` is not an array variable term
  - any argument is a character-data variable
  - any argument is `CONST` or a calculated/pseudo variable

**Examples**
```erabasic
ARRAYMSORT(A, B, C)
```

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
- `i`: int.
- `format` (optional): string expression passed to `Int64.ToString(format)`. If omitted or `null`, uses default formatting.

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
- `<lineNo>` (optional, int; default `0`): index from the end of the logical-line log.
  - `0` = the most recent logical output line.
  - `1` = the second most recent logical output line.
  - And so on.

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
- `HTML_STRINGLEN(html [, returnPixel])`

**Signatures / argument rules**
- Signature: `int HTML_STRINGLEN(string html, int returnPixel = 0)`.
- `returnPixel` is treated as “false” only when it is exactly `0`; any non-zero value selects pixel return.

**Arguments**
- `html`: string expression interpreted as an HTML string.
- `returnPixel` (optional, int; default `0`)
  - `0` (default): return in half-width character units.
  - non-zero: return in pixels.

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
- Sorts one or more array variables in-place using a key array, with explicit control of sort order and the sorted prefix length.

**Tags**
- arrays

**Syntax**
- `ARRAYMSORTEX(keyArray, arrayNameList [, isAscending [, fixedLength]])`

**Signatures / argument rules**
- `ARRAYMSORTEX(keyArray, arrayNameList)` → `long`
- `ARRAYMSORTEX(keyArray, arrayNameList, isAscending)` → `long`
- `ARRAYMSORTEX(keyArray, arrayNameList, isAscending, fixedLength)` → `long`

**Arguments**
- `keyArray` (array variable term | string):
  - Either a non-character 1D array variable term (int or string), or a string that is parsed as a variable term expression.
  - Must not be `CONST`, calculated, or character-data.
- `arrayNameList` (string 1D array variable term): a string array whose elements are variable-term strings naming the arrays to permute.
  - Each element is parsed as a variable term expression at runtime.
  - Any subscripts written in those variable-term strings are ignored; the function operates on the underlying array storage.
- `isAscending` (optional, int; default `1`): sort order flag.
  - `0` = descending
  - non-zero = ascending
- `fixedLength` (optional, int; default `-1`): how many key entries to sort.
  - `-1`: sentinel-terminated mode (see Semantics)
  - `> 0`: sorts the first `min(fixedLength, length(keyArray))` entries
  - `0`: returns `0`

**Semantics**
- Resolves `keyArray` to a key list of length `n` (indexed by `0 <= i < n`):
  - int key array:
    - if `fixedLength == -1`: collects entries until the first `0`
    - else: collects exactly `min(fixedLength, length(keyArray))` entries (including `0` values)
  - string key array:
    - if `fixedLength == -1`: returns `0` if any inspected entry is `null` or empty
    - else: collects exactly `min(fixedLength, length(keyArray))` entries
- Sorts the collected key list using:
  - int keys: numeric ordering
  - string keys: `string.CompareTo` ordering (current culture)
  - direction is controlled by `isAscending`
- For each variable-term string in `arrayNameList`, resolves it to an array variable and applies the same permutation:
  - 1D arrays: permutes elements `0 .. n-1`
  - 2D arrays: permutes rows by the first index (`[row, col]`)
  - 3D arrays: permutes slabs by the first index (`[i, j, k]`)
- If any target array’s first dimension is shorter than `n`, the function returns `0`.
  - This function is not atomic: earlier arrays may already have been permuted before the failure is detected.
- Returns `1` on success.

**Errors & validation**
- Errors if:
  - `keyArray` cannot be resolved as a non-character, non-`CONST` array variable term
  - any array name in `arrayNameList` cannot be resolved to a non-character, non-`CONST` array variable term
  - any resolved array is not an array (dimension 0)
  - any resolved array is a calculated/pseudo variable

**Examples**
```erabasic
#DIM SORT_TARGETS, 3
SORT_TARGETS:0 = "A"
SORT_TARGETS:1 = "B"
SORT_TARGETS:2 = "C"
ARRAYMSORTEX(A, SORT_TARGETS, 1)
```

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
