# EraBasic Built-ins Reference (Emuera / EvilMask)

Generated on `2026-03-03`.

This file is **user-facing**: it contains only human-written documentation overrides.
Undocumented built-ins are listed but contain only a `(TODO)` placeholder.

For engine-extracted skeletons, validation structures, and file/line references, see:
- `erabasic-reference/appendix/tooling/builtins-reference-engine.md` (writer/debug dump; not user-facing)

# Expression functions as statements

Some expression functions are also accepted as standalone statements (without `=` assignment).
In statement form, the engine evaluates the function and writes the return value to:
- `RESULT` for integer-returning functions
- `RESULTS` for string-returning functions

# Instructions

## SET (instruction)

**Summary**
- Internal pseudo-instruction used by the engine to represent **assignment statements** (produced by parsing assignment syntax).
- Implements scalar assignment, compound assignment (`+=`, `-=`, etc.), `++/--`, and comma-list assignment into arrays.

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

**Defaults / optional arguments**
- For `++/--`, the implicit delta is `+1` / `-1`.

**Semantics**
- How “SET” appears:
  - This is not a script-level keyword; an assignment line is parsed into an `InstructionLine` whose function is internally `SET` and whose `AssignOperator` encodes the operator.
  - If a script tries to write a literal `SET ...` instruction, it is not parsed as an assignment line and will fail argument parsing (implementation detail).
- Assignment operator recognition (parser-level):
  - The engine recognizes: `=`, `'=`; `++`, `--`; and compound forms `+=`, `-=`, `*=`, `/=`, `%=`, `<<=`, `>>=`, `|=`, `&=`, `^=`.
- Allowed operators depend on LHS type:
  - int LHS: all the above operators are accepted by the assignment builder.
  - string LHS: only `=`, `'=` (string-expression assignment), `+=`, `*=` are accepted; other compound operators are rejected as invalid.
- If the RHS is a single value:
  - `=` assigns that value.
  - For compound assignment operators, the builder lowers the statement into either:
    - an in-place delta update (`ChangeValue`) only for the `+= <const>` / `-= <const>` / `++` / `--` cases, or
    - a read-then-write expression of the form `LHS = (LHS <op> RHS)` for all other cases (via the engine’s operator reducers).
- Index evaluation and side effects (important compatibility detail):
  - In the `ChangeValue` path (`+= <const>`, `-= <const>`, `++`, `--`), the variable term’s indices are evaluated once.
  - In the general read-then-write path (`LHS = (LHS <op> RHS)`), the variable term is evaluated once for the read and again for the write; if indices contain expressions with side effects, they may run twice (engine behavior).
- If the RHS is a comma list:
  - This is only allowed for `=` on integer variables, and only allowed for `'=` on string variables.
  - Evaluates each element and writes a batch of consecutive elements via the variable term’s `SetValue(long[]/string[])` overload (for multidimensional arrays, the list advances the last dimension).
  - If any RHS element is omitted, it is an error.
- For string `=` assignment, the RHS is treated as FORM/formatted text (not a normal expression) and then compiled to a string expression internally.
  - Implementation detail: after the operator, the engine skips **ASCII spaces only** (not tabs) before scanning the FORM string.
  - Implementation detail: the FORM scanner is invoked in a “trimmed” mode to approximate EraMaker behavior.

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
- See also: `PRINTV` (variadic expressions), `PRINTS` (string expression), `PRINTFORM` (FORM scanned at load-time), `PRINTFORMS` (FORM scanned at runtime).
- This entry also documents **common PRINT-family semantics** (suffix letters, buffering, `K`/`D`, `C`/`LC`).

**Syntax**
- `PRINT`
- `PRINT <raw text>`
- `PRINT;<raw text>`

**Arguments**
- `<raw text>` is **not an expression**. It is taken as the raw character sequence after the instruction delimiter.
- The parser consumes exactly one delimiter character after the keyword:
  - a single space / tab
  - or a full-width space if `SystemAllowFullSpace` is enabled
  - or a semicolon `;`
- Because only *one* delimiter character is consumed:
  - `PRINT X` prints `X` (the one space was consumed as delimiter).
  - `PRINT  X` prints `" X"` (the second space remains in the argument).
  - `PRINT;X` prints `X` (no leading whitespace in the argument).

**Defaults / optional arguments**
- If omitted, the argument is treated as the empty string.

**Semantics**
- Output is appended to the engine’s **print buffer** (it is not necessarily flushed to the UI immediately).
- Implementation detail: if `SkipPrint` is enabled, `PRINT*` does nothing (no output, no newline, no wait).
- Common behavior across the PRINT family:
  - `...L` variants: after output, flush and append a newline (`Console.NewLine()`).
  - `...W` variants: like `...L`, then wait for a key (`Console.ReadAnyKey()`).
  - `...N` variants: wait for a key **without ending the logical output line** (implementation detail: prints with `lineEnd=false` before flushing).
  - `...K` variants: apply kana conversion to the produced string, as configured by `FORCEKANA` (`ConvertStringType`).
  - `...D` variants: ignore `SETCOLOR`’s *color* for this output (still respects font style and font name).
  - `...C` / `...LC` variants: output a fixed-width *cell* using `Config.PrintCLength`; width is measured in **Shift-JIS byte count** (implementation detail; current console implementation hardcodes Shift-JIS for this measurement).
- `PRINT` itself:
  - Uses the raw literal argument as the output string.
  - Treats the output as ending a logical line (`lineEnd=true`) even though it does not insert a newline by itself.

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

**Syntax**
- `PRINTL [<raw text>]`
- `PRINTL;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).

**Defaults / optional arguments**
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

**Syntax**
- `PRINTW [<raw text>]`
- `PRINTW;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).

**Defaults / optional arguments**
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

**Syntax**
- `PRINTV <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

**Defaults / optional arguments**
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

**Syntax**
- `PRINTVL <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

**Defaults / optional arguments**
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

**Syntax**
- `PRINTVW <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

**Defaults / optional arguments**
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

**Syntax**
- `PRINTS <string expr>`

**Arguments**
- A single string expression (must be present).

**Defaults / optional arguments**
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

**Syntax**
- `PRINTSL <string expr>`

**Arguments**
- A single string expression (must be present).

**Defaults / optional arguments**
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

**Syntax**
- `PRINTSW <string expr>`

**Arguments**
- A single string expression (must be present).

**Defaults / optional arguments**
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

**Syntax**
- `PRINTFORM [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

**Defaults / optional arguments**
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

**Syntax**
- `PRINTFORML [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

**Defaults / optional arguments**
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

**Syntax**
- `PRINTFORMW [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

**Defaults / optional arguments**
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

**Syntax**
- `PRINTFORMS <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

**Defaults / optional arguments**
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

**Syntax**
- `PRINTFORMSL <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

**Defaults / optional arguments**
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

**Syntax**
- `PRINTFORMSW <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

**Defaults / optional arguments**
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

**Syntax**
- `PRINTK [<raw text>]`
- `PRINTK;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).

**Defaults / optional arguments**
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

**Syntax**
- `PRINTKL [<raw text>]`
- `PRINTKL;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).

**Defaults / optional arguments**
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

**Syntax**
- `PRINTKW [<raw text>]`
- `PRINTKW;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).

**Defaults / optional arguments**
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

**Syntax**
- `PRINTVK <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

**Defaults / optional arguments**
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

**Syntax**
- `PRINTVKL <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

**Defaults / optional arguments**
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

**Syntax**
- `PRINTVKW <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

**Defaults / optional arguments**
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

**Syntax**
- `PRINTSK <string expr>`

**Arguments**
- A single string expression (must be present).

**Defaults / optional arguments**
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

**Syntax**
- `PRINTSKL <string expr>`

**Arguments**
- A single string expression (must be present).

**Defaults / optional arguments**
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

**Syntax**
- `PRINTSKW <string expr>`

**Arguments**
- A single string expression (must be present).

**Defaults / optional arguments**
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

**Syntax**
- `PRINTFORMK [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

**Defaults / optional arguments**
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

**Syntax**
- `PRINTFORMKL [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

**Defaults / optional arguments**
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

**Syntax**
- `PRINTFORMKW [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

**Defaults / optional arguments**
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

**Syntax**
- `PRINTFORMSK <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

**Defaults / optional arguments**
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

**Syntax**
- `PRINTFORMSKL <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

**Defaults / optional arguments**
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

**Syntax**
- `PRINTFORMSKW <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

**Defaults / optional arguments**
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

**Syntax**
- `PRINTD [<raw text>]`
- `PRINTD;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).

**Defaults / optional arguments**
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

**Syntax**
- `PRINTDL [<raw text>]`
- `PRINTDL;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).

**Defaults / optional arguments**
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

**Syntax**
- `PRINTDW [<raw text>]`
- `PRINTDW;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).

**Defaults / optional arguments**
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

**Syntax**
- `PRINTVD <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

**Defaults / optional arguments**
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

**Syntax**
- `PRINTVDL <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

**Defaults / optional arguments**
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

**Syntax**
- `PRINTVDW <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

**Defaults / optional arguments**
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

**Syntax**
- `PRINTSD <string expr>`

**Arguments**
- A single string expression (must be present).

**Defaults / optional arguments**
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

**Syntax**
- `PRINTSDL <string expr>`

**Arguments**
- A single string expression (must be present).

**Defaults / optional arguments**
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

**Syntax**
- `PRINTSDW <string expr>`

**Arguments**
- A single string expression (must be present).

**Defaults / optional arguments**
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

**Syntax**
- `PRINTFORMD [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

**Defaults / optional arguments**
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

**Syntax**
- `PRINTFORMDL [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

**Defaults / optional arguments**
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

**Syntax**
- `PRINTFORMDW [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

**Defaults / optional arguments**
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

**Syntax**
- `PRINTFORMSD <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

**Defaults / optional arguments**
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

**Syntax**
- `PRINTFORMSDL <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

**Defaults / optional arguments**
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

**Syntax**
- `PRINTFORMSDW <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

**Defaults / optional arguments**
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

**Syntax**
- `PRINTSINGLE [<raw text>]`
- `PRINTSINGLE;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).

**Defaults / optional arguments**
- Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Flushes any pending buffered output first, then prints as a **single display line** (`Console.PrintSingleLine`).
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLE ...`

## PRINTSINGLEV (instruction)

**Summary**
- `PRINTSINGLEV` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Syntax**
- `PRINTSINGLEV <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

**Defaults / optional arguments**
- None (missing arguments are an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- Flushes any pending buffered output first, then prints as a **single display line** (`Console.PrintSingleLine`).
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLEV ...`

## PRINTSINGLES (instruction)

**Summary**
- `PRINTSINGLES` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Syntax**
- `PRINTSINGLES <string expr>`

**Arguments**
- A single string expression (must be present).

**Defaults / optional arguments**
- None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- Flushes any pending buffered output first, then prints as a **single display line** (`Console.PrintSingleLine`).
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLES ...`

## PRINTSINGLEFORM (instruction)

**Summary**
- `PRINTSINGLEFORM` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Syntax**
- `PRINTSINGLEFORM [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

**Defaults / optional arguments**
- Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Flushes any pending buffered output first, then prints as a **single display line** (`Console.PrintSingleLine`).
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLEFORM ...`

## PRINTSINGLEFORMS (instruction)

**Summary**
- `PRINTSINGLEFORMS` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Syntax**
- `PRINTSINGLEFORMS <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

**Defaults / optional arguments**
- None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- Flushes any pending buffered output first, then prints as a **single display line** (`Console.PrintSingleLine`).
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLEFORMS ...`

## PRINTSINGLEK (instruction)

**Summary**
- `PRINTSINGLEK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Syntax**
- `PRINTSINGLEK [<raw text>]`
- `PRINTSINGLEK;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).

**Defaults / optional arguments**
- Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Flushes any pending buffered output first, then prints as a **single display line** (`Console.PrintSingleLine`).
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

**Syntax**
- `PRINTSINGLEVK <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

**Defaults / optional arguments**
- None (missing arguments are an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- Flushes any pending buffered output first, then prints as a **single display line** (`Console.PrintSingleLine`).
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

**Syntax**
- `PRINTSINGLESK <string expr>`

**Arguments**
- A single string expression (must be present).

**Defaults / optional arguments**
- None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- Flushes any pending buffered output first, then prints as a **single display line** (`Console.PrintSingleLine`).
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

**Syntax**
- `PRINTSINGLEFORMK [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

**Defaults / optional arguments**
- Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Flushes any pending buffered output first, then prints as a **single display line** (`Console.PrintSingleLine`).
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

**Syntax**
- `PRINTSINGLEFORMSK <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

**Defaults / optional arguments**
- None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- Flushes any pending buffered output first, then prints as a **single display line** (`Console.PrintSingleLine`).
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

**Syntax**
- `PRINTSINGLED [<raw text>]`
- `PRINTSINGLED;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).

**Defaults / optional arguments**
- Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Flushes any pending buffered output first, then prints as a **single display line** (`Console.PrintSingleLine`).
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

**Syntax**
- `PRINTSINGLEVD <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

**Defaults / optional arguments**
- None (missing arguments are an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- Flushes any pending buffered output first, then prints as a **single display line** (`Console.PrintSingleLine`).
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

**Syntax**
- `PRINTSINGLESD <string expr>`

**Arguments**
- A single string expression (must be present).

**Defaults / optional arguments**
- None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- Flushes any pending buffered output first, then prints as a **single display line** (`Console.PrintSingleLine`).
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

**Syntax**
- `PRINTSINGLEFORMD [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

**Defaults / optional arguments**
- Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Flushes any pending buffered output first, then prints as a **single display line** (`Console.PrintSingleLine`).
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

**Syntax**
- `PRINTSINGLEFORMSD <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

**Defaults / optional arguments**
- None (missing argument is an error).

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- Flushes any pending buffered output first, then prints as a **single display line** (`Console.PrintSingleLine`).
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

**Syntax**
- `PRINTC [<raw text>]`
- `PRINTC;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).
- Output is padded/truncated to a fixed-width cell (`Config.PrintCLength`) using Shift-JIS byte count (implementation detail).

**Defaults / optional arguments**
- Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns (implementation detail).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTC ...`

## PRINTLC (instruction)

**Summary**
- `PRINTLC` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Syntax**
- `PRINTLC [<raw text>]`
- `PRINTLC;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).
- Output is padded/truncated to a fixed-width cell (`Config.PrintCLength`) using Shift-JIS byte count (implementation detail).

**Defaults / optional arguments**
- Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns (implementation detail).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTLC ...`

## PRINTFORMC (instruction)

**Summary**
- `PRINTFORMC` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Syntax**
- `PRINTFORMC [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).
- Output is padded/truncated to a fixed-width cell (`Config.PrintCLength`) using Shift-JIS byte count (implementation detail).

**Defaults / optional arguments**
- Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns (implementation detail).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMC ...`

## PRINTFORMLC (instruction)

**Summary**
- `PRINTFORMLC` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Syntax**
- `PRINTFORMLC [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).
- Output is padded/truncated to a fixed-width cell (`Config.PrintCLength`) using Shift-JIS byte count (implementation detail).

**Defaults / optional arguments**
- Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns (implementation detail).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMLC ...`

## PRINTCK (instruction)

**Summary**
- `PRINTCK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Syntax**
- `PRINTCK [<raw text>]`
- `PRINTCK;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).
- Output is padded/truncated to a fixed-width cell (`Config.PrintCLength`) using Shift-JIS byte count (implementation detail).

**Defaults / optional arguments**
- Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns (implementation detail).
- Applies kana conversion (`FORCEKANA` state) before writing the cell.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTCK ...`

## PRINTLCK (instruction)

**Summary**
- `PRINTLCK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Syntax**
- `PRINTLCK [<raw text>]`
- `PRINTLCK;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).
- Output is padded/truncated to a fixed-width cell (`Config.PrintCLength`) using Shift-JIS byte count (implementation detail).

**Defaults / optional arguments**
- Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns (implementation detail).
- Applies kana conversion (`FORCEKANA` state) before writing the cell.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTLCK ...`

## PRINTFORMCK (instruction)

**Summary**
- `PRINTFORMCK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Syntax**
- `PRINTFORMCK [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).
- Output is padded/truncated to a fixed-width cell (`Config.PrintCLength`) using Shift-JIS byte count (implementation detail).

**Defaults / optional arguments**
- Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns (implementation detail).
- Applies kana conversion (`FORCEKANA` state) before writing the cell.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMCK ...`

## PRINTFORMLCK (instruction)

**Summary**
- `PRINTFORMLCK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Syntax**
- `PRINTFORMLCK [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).
- Output is padded/truncated to a fixed-width cell (`Config.PrintCLength`) using Shift-JIS byte count (implementation detail).

**Defaults / optional arguments**
- Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns (implementation detail).
- Applies kana conversion (`FORCEKANA` state) before writing the cell.

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMLCK ...`

## PRINTCD (instruction)

**Summary**
- `PRINTCD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Syntax**
- `PRINTCD [<raw text>]`
- `PRINTCD;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).
- Output is padded/truncated to a fixed-width cell (`Config.PrintCLength`) using Shift-JIS byte count (implementation detail).

**Defaults / optional arguments**
- Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns (implementation detail).
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTCD ...`

## PRINTLCD (instruction)

**Summary**
- `PRINTLCD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Syntax**
- `PRINTLCD [<raw text>]`
- `PRINTLCD;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).
- Output is padded/truncated to a fixed-width cell (`Config.PrintCLength`) using Shift-JIS byte count (implementation detail).

**Defaults / optional arguments**
- Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns (implementation detail).
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTLCD ...`

## PRINTFORMCD (instruction)

**Summary**
- `PRINTFORMCD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Syntax**
- `PRINTFORMCD [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).
- Output is padded/truncated to a fixed-width cell (`Config.PrintCLength`) using Shift-JIS byte count (implementation detail).

**Defaults / optional arguments**
- Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns (implementation detail).
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMCD ...`

## PRINTFORMLCD (instruction)

**Summary**
- `PRINTFORMLCD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Syntax**
- `PRINTFORMLCD [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).
- Output is padded/truncated to a fixed-width cell (`Config.PrintCLength`) using Shift-JIS byte count (implementation detail).

**Defaults / optional arguments**
- Omitted argument prints the empty string.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns (implementation detail).
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMLCD ...`

## PRINTDATA (instruction)

**Summary**
- Begins a **PRINTDATA block** that contains `DATA` / `DATAFORM` (and optional `DATALIST` groups).
- At runtime, the engine picks one choice uniformly at random, prints it, then jumps to `ENDDATA`.

**Syntax**
- `PRINTDATA [<intVarTerm>]`
- Block form:
  - `PRINTDATA [<intVarTerm>]`
    - `DATA <raw text>` / `DATAFORM <FORM string>` (one or more choices)
    - optionally, `DATALIST` ... `ENDLIST` groups to make a multi-line choice
  - `ENDDATA`

**Arguments**
- Optional `<intVarTerm>`: a changeable int variable term that receives the 0-based chosen index.

**Defaults / optional arguments**
- If `<intVarTerm>` is omitted, the chosen index is not stored anywhere.

**Semantics**
- Load-time structure rules (enforced by the loader):
  - `PRINTDATA*` must be closed by a matching `ENDDATA`.
  - `DATA` / `DATAFORM` must appear inside `PRINTDATA*`, `STRDATA`, or inside a `DATALIST` that is itself inside one of those blocks.
  - Nested `PRINTDATA*` blocks are a load-time error (the line is marked as error).
  - `STRDATA` cannot be nested inside `PRINTDATA*` and vice versa (load-time error).
  - The block body only permits `DATA` / `DATAFORM` / `DATALIST` / `ENDLIST` / `ENDDATA`; any other instruction (and any label definition) inside is a load-time error.
- Runtime behavior:
  - Implementation detail: if `SkipPrint` is enabled, `PRINTDATA*` is skipped entirely (no selection, no assignment to `<intVarTerm>`, and no jump to `ENDDATA`), so control flows through the block lines normally.
  - If there are no `DATA` choices, nothing is printed and the engine jumps to `ENDDATA`.
  - Otherwise:
    - Choose `choice = RAND(0..count-1)` using the engine RNG.
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

**Syntax**
- `PRINTDATAL [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

**Defaults / optional arguments**
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

**Syntax**
- `PRINTDATAW [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

**Defaults / optional arguments**
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

**Syntax**
- `PRINTDATAK [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

**Defaults / optional arguments**
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

**Syntax**
- `PRINTDATAKL [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

**Defaults / optional arguments**
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

**Syntax**
- `PRINTDATAKW [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

**Defaults / optional arguments**
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

**Syntax**
- `PRINTDATAD [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

**Defaults / optional arguments**
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

**Syntax**
- `PRINTDATADL [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

**Defaults / optional arguments**
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

**Syntax**
- `PRINTDATADW [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

**Defaults / optional arguments**
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
- (TODO: not yet documented)

## PRINTBUTTONC (instruction)
**Summary**
- (TODO: not yet documented)

## PRINTBUTTONLC (instruction)
**Summary**
- (TODO: not yet documented)

## PRINTPLAIN (instruction)
**Summary**
- (TODO: not yet documented)

## PRINTPLAINFORM (instruction)
**Summary**
- (TODO: not yet documented)

## PRINT_ABL (instruction)
**Summary**
- (TODO: not yet documented)

## PRINT_TALENT (instruction)
**Summary**
- (TODO: not yet documented)

## PRINT_MARK (instruction)
**Summary**
- (TODO: not yet documented)

## PRINT_EXP (instruction)
**Summary**
- (TODO: not yet documented)

## PRINT_PALAM (instruction)
**Summary**
- (TODO: not yet documented)

## PRINT_ITEM (instruction)
**Summary**
- (TODO: not yet documented)

## PRINT_SHOPITEM (instruction)
**Summary**
- (TODO: not yet documented)

## DRAWLINE (instruction)
**Summary**
- (TODO: not yet documented)

## BAR (instruction)
**Summary**
- (TODO: not yet documented)

## BARL (instruction)
**Summary**
- (TODO: not yet documented)

## TIMES (instruction)
**Summary**
- (TODO: not yet documented)

## WAIT (instruction)

**Summary**
- Waits for the user to press Enter (or click, depending on the UI), then continues.

**Syntax**
- `WAIT`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- Enters a UI wait state for an Enter-style key/click (`InputType.EnterKey`).
- Does not assign `RESULT`/`RESULTS`.
- If the script runner’s `skipPrint` mode is active (e.g. via `SKIPDISP`), `WAIT` is skipped as part of the print-family skip rule.

**Errors & validation**
- None.

**Examples**
- `WAIT`

## INPUT (instruction)

**Summary**
- Requests an integer input from the user and stores it into `RESULT` (with mouse-related side channels in some cases).

**Syntax**
- `INPUT`
- `INPUT <default>`
- `INPUT <default>, <mouse>, <canSkip> [, <extra>]`

**Arguments**
- `<default>` (optional): integer expression for the default value.
- `<mouse>` (optional): integer expression; if non-zero, enables mouse-based input (implementation detail: selecting buttons can fill the input).
- `<canSkip>` (optional): integer expression; if present and non-zero, allows “message skip” (`MesSkip`) to auto-accept the default value without waiting.
- `<extra>` (optional): accepted by the current argument builder but ignored by the runtime implementation (implementation detail).

**Defaults / optional arguments**
- If `<default>` is omitted, there is no default value.

**Semantics**
- Enters an integer-input UI wait (`InputType.IntValue`).
- If `<default>` is provided, it becomes the default used when the input is empty and the request is not running a timer.
- On successful completion:
  - Stores the integer value into `RESULT`.
  - Echoes the entered text to output (UI behavior).
- `MesSkip` integration (implementation detail):
  - If `<canSkip>` is present and `MesSkip` is currently true, the engine does not wait and instead accepts the default immediately.
  - In that no-wait path, the engine assigns the default to:
    - `RESULT` if `<mouse> == 0`
    - `RESULT_ARRAY[1]` if `<mouse> != 0`
  - In that no-wait path, the input string is not echoed (because the UI wait is skipped entirely).
- Mouse-enabled input side channels (implementation detail; WinForms UI behavior):
  - If mouse input is enabled and the user completes input via a mouse interaction, the UI may also write metadata into:
    - `RESULT_ARRAY[1]`: mouse button (`1`=left, `2`=right, `3`=middle) in some click paths.
    - `RESULT_ARRAY[2]`: a modifier-key bitfield in some click paths (Shift=`2^16`, Ctrl=`2^17`, Alt=`2^18`).
    - `RESULTS_ARRAY[1]`: the clicked button’s string (if any) in some click paths.
    - `RESULT_ARRAY[3]`: a mapped “button color” value in some click paths.
- If the script runner’s `skipPrint` mode is active (e.g. via `SKIPDISP`), `INPUT` is treated as a print-family instruction:
  - In internal skip modes, it is skipped.
  - If skip was enabled by `SKIPDISP`, reaching `INPUT` is a runtime error.

**Errors & validation**
- Argument-type errors are raised if a non-integer argument is provided.
- If input cannot be parsed as an integer, the engine stays in the wait state (no value is stored).

**Examples**
- `INPUT`
- `INPUT 0`
- `INPUT 10, 1, 1` (default=10, mouse input enabled, skip can auto-accept default)

## INPUTS (instruction)

**Summary**
- Requests a string input from the user and stores it into `RESULTS` (with mouse-related side channels in some cases).

**Syntax**
- `INPUTS`
- `INPUTS <defaultFormString>`
- `INPUTS <defaultFormString>, <mouse> [, <canSkip>]`

**Arguments**
- `<defaultFormString>` (optional): a FORM/formatted string expression used as the default string.
- `<mouse>` (optional): integer expression; if non-zero, enables mouse-based input (implementation detail).
- `<canSkip>` (optional): integer expression; if present, allows `MesSkip` to auto-accept the default without waiting.

**Defaults / optional arguments**
- If `<defaultFormString>` is omitted, there is no default value.

**Semantics**
- Enters a string-input UI wait (`InputType.StrValue`).
- If `<defaultFormString>` is provided, it is evaluated to a string and used as the default when the input is empty and the request is not running a timer.
- On successful completion:
  - Stores the string into `RESULTS`.
  - Echoes the entered text to output (UI behavior).
- `MesSkip` integration (implementation detail):
  - If `<canSkip>` is present and `MesSkip` is currently true, the engine does not wait and instead accepts the default immediately.
  - In that no-wait path, the engine assigns the default to:
    - `RESULTS` if `<mouse> == 0`
    - `RESULTS_ARRAY[1]` if `<mouse> != 0`
  - In that no-wait path, the input string is not echoed (because the UI wait is skipped entirely).
- Mouse-enabled input side channels: see `INPUT` (the same UI-side `RESULT_ARRAY[...]` / `RESULTS_ARRAY[...]` behaviors apply).
- Skip-print interaction is the same as `INPUT` (print-family skip rule + `SKIPDISP` input error case).

**Errors & validation**
- Argument parsing errors follow the underlying builder rules for `INPUTS`.
- Implementation detail (current argument builder quirks):
  - After the first comma, non-integer expressions are ignored with a warning.
  - Supplying `<canSkip>` may still emit a “too many arguments” warning, but the value is accepted and used by the runtime.

**Examples**
- `INPUTS`
- `INPUTS Default`
- `INPUTS Hello, %NAME%!, 1, 1`

## TINPUT (instruction)

**Summary**
- Timed integer input: like `INPUT`, but with a time limit and timeout message.

**Syntax**
- `TINPUT <timeMs>, <default> [, <displayTime> [, <timeoutMessage> [, <mouse> [, <canSkip>]]]]`

**Arguments**
- `<timeMs>`: integer expression; time limit in milliseconds.
- `<default>`: integer expression; default value used on timeout (and also on empty input when the request is not running a timer).
- `<displayTime>` (optional): integer expression; if non-zero, displays remaining time (UI behavior). Default `1`.
- `<timeoutMessage>` (optional): string expression; message used on timeout. Default `Config.TimeupLabel`.
- `<mouse>` (optional): integer expression; enables mouse input when equal to `1` (implementation detail).
- `<canSkip>` (optional): integer expression; if present, allows `MesSkip` to auto-accept the default without waiting.

**Defaults / optional arguments**
- `<displayTime>` defaults to `1`.
- `<timeoutMessage>` defaults to `Config.TimeupLabel`.

**Semantics**
- Enters an integer-input UI wait with a timer:
  - `InputType = IntValue`
  - `Timelimit = <timeMs>`
  - default value is always present (`HasDefValue = true`)
- Timeout behavior:
  - When the timer expires, the engine runs the input completion path with an empty input string; this causes the default to be accepted.
  - A timeout message is displayed (either by updating the last “remaining time” line, or by printing a single line, depending on `<displayTime>`).
- `MesSkip` integration (implementation detail):
  - If `<canSkip>` is present and `MesSkip` is currently true, the engine does not wait and instead accepts the default immediately.
  - In that no-wait path, the engine assigns the default to:
    - `RESULT` if `<mouse> == 0`
    - `RESULT_ARRAY[1]` if `<mouse> != 0`
  - In that no-wait path, the input string is not echoed (because the UI wait is skipped entirely).
- Mouse-enabled input side channels: see `INPUT` (the same UI-side `RESULT_ARRAY[...]` / `RESULTS_ARRAY[...]` behaviors apply).
- Skip-print interaction is the same as `INPUT` (print-family skip rule + `SKIPDISP` input error case).

**Errors & validation**
- Argument type/count errors are rejected by the argument builder.

**Examples**
- `TINPUT 5000, 0`
- `TINPUT 10000, 1, 1, Time up!, 1, 1`

## TINPUTS (instruction)

**Summary**
- Timed string input: like `INPUTS`, but with a time limit and timeout message.

**Syntax**
- `TINPUTS <timeMs>, <default> [, <displayTime> [, <timeoutMessage> [, <mouse> [, <canSkip>]]]]`

**Arguments**
- `<timeMs>`: integer expression; time limit in milliseconds.
- `<default>`: string expression; default value used on timeout (and also on empty input when the request is not running a timer).
- `<displayTime>` (optional): integer expression; if non-zero, displays remaining time. Default `1`.
- `<timeoutMessage>` (optional): string expression; timeout message. Default `Config.TimeupLabel`.
- `<mouse>` (optional): integer expression; enables mouse input when equal to `1` (implementation detail).
- `<canSkip>` (optional): integer expression; if present, allows `MesSkip` to auto-accept the default without waiting.

**Defaults / optional arguments**
- `<displayTime>` defaults to `1`.
- `<timeoutMessage>` defaults to `Config.TimeupLabel`.

**Semantics**
- Same model as `TINPUT`, but stores into `RESULTS` (string) rather than `RESULT` (int).
- `MesSkip` integration (implementation detail):
  - If `<canSkip>` is present and `MesSkip` is currently true, the engine does not wait and instead accepts the default immediately.
  - In that no-wait path, the engine assigns the default to:
    - `RESULTS` if `<mouse> == 0`
    - `RESULTS_ARRAY[1]` if `<mouse> != 0`
  - In that no-wait path, the input string is not echoed (because the UI wait is skipped entirely).
- Mouse-enabled input side channels: see `INPUT` (the same UI-side `RESULT_ARRAY[...]` / `RESULTS_ARRAY[...]` behaviors apply).

**Errors & validation**
- Argument type/count errors are rejected by the argument builder.

**Examples**
- `TINPUTS 5000, "DEFAULT"`
- `TINPUTS 3000, NAME, 1, Time up!`

## TONEINPUT (instruction)

**Summary**
- Like `TINPUT`, but uses the “one input” mode (`OneInput = true`).

**Syntax**
- Same as `TINPUT`.

**Arguments**
- Same as `TINPUT`.

**Defaults / optional arguments**
- Same as `TINPUT`.

**Semantics**
- Same as `TINPUT`, but the UI may truncate the entered text to at most one character (implementation detail).

**Errors & validation**
- Same as `TINPUT`.

**Examples**
- `TONEINPUT 5000, 0`

## TONEINPUTS (instruction)

**Summary**
- Like `TINPUTS`, but uses the “one input” mode (`OneInput = true`).

**Syntax**
- Same as `TINPUTS`.

**Arguments**
- Same as `TINPUTS`.

**Defaults / optional arguments**
- Same as `TINPUTS`.

**Semantics**
- Same as `TINPUTS`, but the UI may truncate the entered text to at most one character (implementation detail).

**Errors & validation**
- Same as `TINPUTS`.

**Examples**
- `TONEINPUTS 5000, "A"`

## TWAIT (instruction)

**Summary**
- Timed wait: waits for a limited time (and optionally disallows user input), then continues.

**Syntax**
- `TWAIT <timeMs>, <mode>`

**Arguments**
- `<timeMs>`: integer expression; time limit in milliseconds.
- `<mode>`: integer expression:
  - `0`: wait for Enter/click, but time out after `<timeMs>`.
  - non-zero: disallow input and simply wait `<timeMs>` (or be affected by macro/skip behavior).

**Defaults / optional arguments**
- None.

**Semantics**
- Implementation detail: `TWAIT` first calls an Enter-style wait, then replaces it with a timed `WaitInput` request.
- Creates an `InputRequest` with:
  - `InputType = EnterKey` if `<mode> == 0`, otherwise `Void`
  - `Timelimit = <timeMs>`
- When the time limit elapses, execution continues automatically.
- Does not assign `RESULT`/`RESULTS`.
- Skipped when the script runner’s `skipPrint` mode is active (print-family skip rule).

**Errors & validation**
- Argument type errors follow the normal integer-expression argument rules.

**Examples**
- `TWAIT 3000, 0` (wait up to 3 seconds for Enter)
- `TWAIT 1000, 1` (wait 1 second with no input)

## WAITANYKEY (instruction)

**Summary**
- Like `WAIT`, but accepts **any key** input (not only Enter) to continue.

**Syntax**
- `WAITANYKEY`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- Enters a UI wait state for any-key input (`InputType.AnyKey`).
- Does not assign `RESULT`/`RESULTS`.
- Skipped when the script runner’s `skipPrint` mode is active (print-family skip rule).

**Errors & validation**
- None.

**Examples**
- `WAITANYKEY`

## FORCEWAIT (instruction)

**Summary**
- Like `WAIT`, but stops “message skip” from auto-advancing past the wait.

**Syntax**
- `FORCEWAIT`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- Enters an Enter-style UI wait (`InputType.EnterKey`) with `StopMesskip = true`.
  - Implementation detail: this prevents `MesSkip`-driven macro/skip logic from treating the wait as a no-op.
- Does not assign `RESULT`/`RESULTS`.
- Skipped when the script runner’s `skipPrint` mode is active (print-family skip rule).

**Errors & validation**
- None.

**Examples**
- `FORCEWAIT`

## ONEINPUT (instruction)

**Summary**
- Like `INPUT`, but requests a “one input” integer entry (UI-side restriction).

**Syntax**
- `ONEINPUT`
- `ONEINPUT <default>`
- `ONEINPUT <default>, <mouse>, <canSkip> [, <extra>]`

**Arguments**
- Same as `INPUT`.

**Defaults / optional arguments**
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

**Syntax**
- `ONEINPUTS`
- `ONEINPUTS <defaultFormString>`
- `ONEINPUTS <defaultFormString>, <mouse> [, <canSkip>]`

**Arguments**
- Same as `INPUTS`.

**Defaults / optional arguments**
- Same as `INPUTS`.

**Semantics**
- Like `INPUTS` (including `MesSkip` behavior and mouse side channels), but sets `OneInput = true` on the input request.
- Implementation detail: the UI input handler may truncate the entered string to at most one character.

**Errors & validation**
- Same as `INPUTS`.

**Examples**
- `ONEINPUTS`
- `ONEINPUTS A`

## CLEARLINE (instruction)

**Summary**
- Deletes the last *N logical output lines* from the console display/log.

**Syntax**
- `CLEARLINE <n>`

**Arguments**
- `<n>`: integer expression (cast to a 32-bit signed integer before use; out-of-range values are implementation-defined).

**Defaults / optional arguments**
- None.

**Semantics**
- Evaluates `<n>` and calls the console’s internal `deleteLine(<n>)`.
- The deletion count is in **logical lines**, not raw display lines:
  - One logical line can occupy multiple display lines (e.g. word wrapping).
  - Deletion walks backward from the end of the display list and counts only entries marked as “logical line” boundaries; all associated display lines are removed.
- After deleting, the console is refreshed (`RefreshStrings(false)`).

**Errors & validation**
- No explicit validation in the instruction.
- Engine behavior is only well-defined for small non-negative `<n>`; negative or overflowed values can lead to implementation-specific results.

**Examples**
- `CLEARLINE 1`
- `CLEARLINE 10`

## REUSELASTLINE (instruction)

**Summary**
- Prints a **temporary single line** that is intended to be overwritten by the next printed line.

**Syntax**
- `REUSELASTLINE`
- `REUSELASTLINE <formString>`

**Arguments**
- `<formString>` (optional): FORM/formatted string (parsed like `PRINTFORM*`) used as the temporary line’s content.

**Defaults / optional arguments**
- If omitted, the argument is treated as the empty string.

**Semantics**
- Evaluates `<formString>` to a string and calls `Console.PrintTemporaryLine(str)`.
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
- (TODO: not yet documented)

## CUPCHECK (instruction)
**Summary**
- (TODO: not yet documented)

## ADDCHARA (instruction)
**Summary**
- (TODO: not yet documented)

## ADDSPCHARA (instruction)
**Summary**
- (TODO: not yet documented)

## ADDDEFCHARA (instruction)
**Summary**
- (TODO: not yet documented)

## ADDVOIDCHARA (instruction)
**Summary**
- (TODO: not yet documented)

## DELCHARA (instruction)
**Summary**
- (TODO: not yet documented)

## PUTFORM (instruction)

**Summary**
- Appends a formatted string to the save-description buffer (`SAVEDATA_TEXT`).

**Syntax**
- `PUTFORM`
- `PUTFORM <formString>`

**Arguments**
- `<formString>` (optional): FORM/formatted string.

**Defaults / optional arguments**
- If omitted, the argument is treated as the empty string.

**Semantics**
- Evaluates `<formString>` to a string.
- Appends it to the internal save-description buffer:
  - If `SAVEDATA_TEXT` is non-null, `SAVEDATA_TEXT += <string>`.
  - Otherwise, `SAVEDATA_TEXT = <string>`.
- Does not print to the console.
- Intended for use by the save-info generation path (implementation detail).

**Errors & validation**
- None.

**Examples**
- `PUTFORM %PLAYERNAME% - Day %DAY%`

## QUIT (instruction)

**Summary**
- Ends the current run by requesting the console to quit.

**Syntax**
- `QUIT`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- Calls `Console.Quit()`, which sets the console state to `Quit`.
- Script execution stops because `Console.IsRunning` becomes false.
- UI shutdown is handled by the console’s event loop (implementation detail).

**Errors & validation**
- None.

**Examples**
- `QUIT`

## BEGIN (instruction)

**Summary**
- Requests a transition into one of the engine’s **system phases** (e.g. `SHOP`, `TRAIN`, `TITLE`) after the current call stack unwinds.

**Syntax**
- `BEGIN <keyword>`

**Arguments**
- `<keyword>`: raw string (the entire remainder of the source line after the instruction delimiter).
  - Must match one of the supported keywords exactly (see below).
  - The current engine compares this string literally (no automatic trim or case-folding).

**Defaults / optional arguments**
- None.

**Semantics**
- Recognized keywords (engine-defined):
  - `SHOP`, `TRAIN`, `AFTERTRAIN`, `ABLUP`, `TURNEND`, `FIRST`, `TITLE`
- On execution:
  - Validates `<keyword>` by matching it against the list above; otherwise raises an error.
  - Sets an internal “begin type” on the process state.
  - Immediately performs some keyword-specific side effects:
    - `SHOP` and `FIRST` unload temporary loaded image resources (implementation detail).
  - Calls `state.Return(0)`:
    - This starts unwinding the current EraBasic call stack.
    - When unwinding reaches the top-level (no return address), the engine performs the actual system-phase transition (`state.Begin()`), clears the function stack, and continues execution in the new system state.
  - Resets console style (`Console.ResetStyle()`).

**Errors & validation**
- If `<keyword>` is not recognized, raises a runtime error (“invalid BEGIN argument”).

**Examples**
- `BEGIN TITLE`
- `BEGIN SHOP`

## SAVEGAME (instruction)

**Summary**
- Opens the engine’s interactive **save UI** (system-driven save).

**Syntax**
- `SAVEGAME`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- Requires that the current system state allows saving (implementation detail: `SystemStateCode.__CAN_SAVE__`), otherwise raises an error.
- Saves the current process state for later restoration, then transitions into the system save flow.
- The system save flow (high-level behavior):
  - Displays save slots `0..Config.SaveDataNos-1` in pages of 20.
  - Uses `100` as the “back/cancel” input.
  - After selecting a slot:
    - If it already contains data, prompts for overwrite confirmation.
    - Initializes `SAVEDATA_TEXT` with the current timestamp (`yyyy/MM/dd HH:mm:ss `).
    - Calls `@SAVEINFO` (if it exists), which can append to `SAVEDATA_TEXT` (commonly via `PUTFORM`).
    - Saves the current state to the selected slot (as `save{slot:00}.sav` under `Config.SavDir`) using `SAVEDATA_TEXT` as the slot description text.
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

**Syntax**
- `LOADGAME`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- Requires that the current system state allows saving/loading (same gate as `SAVEGAME`), otherwise raises an error.
- Saves the current process state for later restoration, then transitions into the system load flow.
- The system load flow (high-level behavior):
  - Displays save slots `0..Config.SaveDataNos-1` in pages of 20.
  - Includes a special autosave entry `99` when applicable (implementation detail).
  - Uses `100` as the “back/cancel” input.
  - After selecting a valid slot:
    - Loads the slot file (as `save{slot:00}.sav` under `Config.SavDir`).
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

**Syntax**
- `SAVEDATA <slot>, <saveText>`

**Arguments**
- `<slot>`: integer expression. Must be in `[0, 2147483647]` (32-bit signed non-negative).
- `<saveText>`: string expression; saved into the file and shown by the built-in save/load UI.
  - Must not contain a newline (`'\n'`).

**Defaults / optional arguments**
- None.

**Semantics**
- Evaluates `<slot>` and `<saveText>`.
- Writes a save file under `Config.SavDir`:
  - Path is `save{slot:00}.sav` (e.g. slot `0` -> `save00.sav`).
- Save format (implementation detail):
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

**Syntax**
- `LOADDATA <slot>`

**Arguments**
- `<slot>`: integer expression. Must be in `[0, 2147483647]` (32-bit signed non-negative).
  - If omitted, the argument parser supplies `0` (with a warning); this effectively loads slot `0`.

**Defaults / optional arguments**
- None (but see omitted-argument behavior above).

**Semantics**
- Validates the target save file via `CheckData(slot, Normal)`; if the file is missing/corrupt/mismatched, raises an error.
- Loads the save file:
  - Resets variable state and reloads characters/variables from the file (implementation detail).
  - Sets the pseudo variables:
    - `LASTLOAD_NO` to the loaded slot number
    - `LASTLOAD_TEXT` to the saved `<saveText>`
    - `LASTLOAD_VERSION` to the save file’s recorded script version
- Clears the EraBasic function stack (`state.ClearFunctionList()`), discarding the current call context.
- Transfers control into the system “data loaded” phase:
  - Sets `SystemState = LoadData_DataLoaded`.
  - System processing then calls (if they exist):
    - `SYSTEM_LOADEND`
    - `EVENTLOAD`
  - If `EVENTLOAD` returns normally without performing a `BEGIN`, the engine proceeds as if `BEGIN SHOP` occurred (implementation detail).
- See also: `save-files.md` (directories, partitions, and on-disk formats)

**Errors & validation**
- Errors if `<slot>` is negative or larger than `int.MaxValue`.
- Error if the file is not considered valid by `CheckData(..., Normal)` (“corrupted save data” path).
- If loading fails after validation, the engine throws an internal execution error.

**Examples**
- `LOADDATA 0`

## DELDATA (instruction)

**Summary**
- Deletes a numbered save slot file (`saveXX.sav`) if it exists.

**Syntax**
- `DELDATA <slot>`

**Arguments**
- `<slot>`: integer expression. Must be in `[0, 2147483647]` (32-bit signed non-negative).
  - If omitted, the argument parser supplies `0` (with a warning); this deletes slot `0`.

**Defaults / optional arguments**
- None (but see omitted-argument behavior above).

**Semantics**
- Computes the save file path under `Config.SavDir` as `save{slot:00}.sav`.
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

**Syntax**
- `SAVEGLOBAL`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- Writes the global save file under `Config.SavDir`:
  - Path is `global.sav`.
- Save format (implementation detail):
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

**Syntax**
- `LOADGLOBAL`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- Attempts to load `global.sav` under `Config.SavDir`.
- On success:
  - Loads the global variable data from the file (format depends on file type).
  - Sets `RESULT = 1`.
- On failure:
  - Sets `RESULT = 0`.
- Implementation detail: before attempting to read, the loader removes certain Emuera-private global extension data; if loading then fails, this removal may still have occurred.
- See also: `save-files.md` (directories, partitions, and on-disk formats)

**Errors & validation**
- No explicit errors are raised for load failures; failures are reported via `RESULT`.

**Examples**
- `LOADGLOBAL`

## RESETDATA (instruction)

**Summary**
- Resets the current game/runtime variable state (excluding global variables).

**Syntax**
- `RESETDATA`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- Calls `VEvaluator.ResetData()`, which (high-level):
  - Clears local/default variable state.
  - Disposes and clears the character list.
  - Removes certain Emuera-private save-related data structures (implementation detail; e.g. XML/maps/DT savedata extensions).
  - Does **not** reset global variables.
- Resets console style (`Console.ResetStyle()`).
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- None.

**Examples**
- `RESETDATA`

## RESETGLOBAL (instruction)

**Summary**
- Resets global variables to their default values.

**Syntax**
- `RESETGLOBAL`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- Calls `VEvaluator.ResetGlobalData()`, which (high-level):
  - Resets global variables to default values.
  - Removes certain Emuera-private global/static data structures (implementation detail; e.g. XML/maps global/static extensions).
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- None.

**Examples**
- `RESETGLOBAL`

## SIF (instruction)

**Summary**
- “Single-line IF”: conditionally skips the **next logical line only**.

**Syntax**
- `SIF <int expr>`
  - `<next logical line>`

**Arguments**
- `<int expr>`: evaluated as integer; zero = false, non-zero = true.

**Defaults / optional arguments**
- If the expression is omitted, it defaults to `0` (false) and emits a load-time warning.

**Semantics**
- If the condition is true (non-zero), execution continues normally.
- If the condition is false (zero), the engine advances the program counter one extra time (skipping exactly one logical line).
- Load-time validation enforces an inherent limitation of this “skip the next line” model:
  - If the following line is a **partial instruction** (structural marker / block delimiter; e.g. `IF`, `ELSE`, `CASE`, loop markers), the engine warns because skipping marker lines breaks block structure.
  - If the following line is a `$label` line, the engine warns.
  - If there is no following executable line (EOF / next `@label`), the engine warns.
  - If there is at least one physically empty line between `SIF` and the next logical line, the engine warns (implementation detail: it compares source line numbers and reports “empty line(s) after SIF”).

**Errors & validation**
- Some invalid “next line” situations are treated as load-time errors (the `SIF` line is marked as error and cannot run safely), including:
  - no following logical line (EOF / next `@label`)
  - following line is a function label line (`@...`) or a null terminator line
  - following instruction line is a **partial instruction** (structural marker / block delimiter)
  - following line is a `$label` line
- The engine may also warn if there are physically empty line(s) between `SIF` and the next logical line (implementation detail).

**Examples**
- `SIF A == 0`
- `PRINTL "A is non-zero"`

## IF (instruction)

**Summary**
- Begins an `IF ... ENDIF` block. Chooses the first true clause among `IF` / `ELSEIF` / `ELSE` and executes that clause body.

**Syntax**
- `IF <int expr>`
- `IF <int expr>`
  - `...`
  - `ELSEIF <int expr>`
  - `...`
  - `ELSE`
  - `...`
  - `ENDIF`

**Arguments**
- `<int expr>`: evaluated as integer; zero = false, non-zero = true.

**Defaults / optional arguments**
- If the expression is omitted, it defaults to `0` (false) and emits a load-time warning.

**Semantics**
- The loader builds an ordered clause list (`IF` header, then each `ELSEIF`, and optional `ELSE`) and links every clause header to the matching `ENDIF`.
- At runtime, the `IF` header evaluates its own condition and then each `ELSEIF` in order:
  - If a condition is true, the engine jumps to that clause header as a **marker**.
  - Because Emuera’s execution loop advances to `NextLine` before executing, jumping to a clause header causes the next executed line to be the **first line of that clause body**, not the header itself.
- If no condition matches:
  - If there is an `ELSE`, the engine jumps to the `ELSE` header marker (and thus executes the `ELSE` body).
  - Otherwise it jumps to the `ENDIF` marker (skipping the whole block).

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

**Syntax**
- `ELSE`

**Arguments**
- None.

**Defaults / optional arguments**
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

**Syntax**
- `ELSEIF <int expr>`

**Arguments**
- `<int expr>` is evaluated by the `IF` header’s clause-selection logic (not by the `ELSEIF` instruction itself).

**Defaults / optional arguments**
- None.

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

**Syntax**
- `ENDIF`

**Arguments**
- None.

**Defaults / optional arguments**
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

**Syntax**
- `SELECTCASE <expr>`
  - `CASE <caseExpr> (, <caseExpr> ... )`
  - `...`
  - `CASEELSE`
  - `...`
  - `ENDSELECT`

**Arguments**
- `<expr>`: selector expression; may be int or string.

**Defaults / optional arguments**
- None.

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

**Syntax**
- `CASE <caseExpr> (, <caseExpr> ... )`

**Arguments**
- Each `<caseExpr>` is one of:
  - Normal: `<expr>` (matches by equality against the selector).
  - Range: `<expr> TO <expr>` (inclusive range).
  - “IS form”: `IS <binaryOp> <expr>` (e.g. `IS >= 10`), using the engine’s binary-operator semantics.

**Defaults / optional arguments**
- None.

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

**Syntax**
- `CASEELSE`

**Arguments**
- None.

**Defaults / optional arguments**
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

**Syntax**
- `ENDSELECT`

**Arguments**
- None.

**Defaults / optional arguments**
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

**Syntax**
- `REPEAT <countExpr>`
  - `...`
  - `REND`

**Arguments**
- `<countExpr>`: int expression giving the number of iterations.

**Defaults / optional arguments**
- If omitted, the count defaults to `0` (and emits a warning when the line’s argument is parsed; by default: when the `REPEAT` line is first reached at runtime).

**Semantics**
- `REPEAT` is implemented as a FOR-like loop over `COUNT:0`:
  - Initializes `COUNT:0` to `0`.
  - Uses `end = <countExpr>` and `step = 1`.
  - The loop continues while `COUNT:0 < end`.
- `COUNT:0` is incremented by `1` at `REND` time (and also by `BREAK`/`CONTINUE` for era-maker compatibility).
- Because the engine advances to `NextLine` before executing, jumps between `REPEAT` and `REND` are done via marker lines:
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

**Syntax**
- `REND`

**Arguments**
- None.

**Defaults / optional arguments**
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

**Syntax**
- `FOR <intVarTerm>, <start>, <end> [, <step>]`
- Start may be omitted by leaving an empty slot: `FOR <intVarTerm>, , <end> [, <step>]`
  - `...`
  - `NEXT`

**Arguments**
- `<intVarTerm>`: changeable integer variable term (must not be character-data).
- `<start>`: int expression (defaults to `0` if omitted via an empty argument).
- `<end>`: int expression.
- `<step>`: int expression (defaults to `1` if omitted).

**Defaults / optional arguments**
- `<start>` defaults to `0` when omitted as an empty argument.
- `<step>` defaults to `1` when omitted.

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

**Syntax**
- `NEXT`

**Arguments**
- None.

**Defaults / optional arguments**
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

**Syntax**
- `WHILE <int expr>`
  - `...`
  - `WEND`

**Arguments**
- `<int expr>`: loop condition (0 = false, non-zero = true).

**Defaults / optional arguments**
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

**Syntax**
- `WEND`

**Arguments**
- None.

**Defaults / optional arguments**
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

**Syntax**
- `DO`
  - `...`
  - `LOOP <int expr>`

**Arguments**
- None.

**Defaults / optional arguments**
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

**Syntax**
- `LOOP <int expr>`

**Arguments**
- `<int expr>`: loop condition (0 = false, non-zero = true).

**Defaults / optional arguments**
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

**Syntax**
- `CONTINUE`

**Arguments**
- None.

**Defaults / optional arguments**
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

**Syntax**
- `BREAK`

**Arguments**
- None.

**Defaults / optional arguments**
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

**Syntax**
- `RETURN`
- `RETURN <int expr1> [, <int expr2>, <int expr3>, ... ]`

**Arguments**
- Each argument is evaluated as an integer and stored into `RESULT:<index>`.

**Defaults / optional arguments**
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

**Syntax**
- `RETURNFORM <formString>`

**Arguments**
- `<formString>` is evaluated to a string `s`, then `s` is re-lexed as one or more **comma-separated integer expressions**.

**Defaults / optional arguments**
- If `s` is empty, the engine behaves like `RETURN 0`.

**Semantics**
- Evaluates the formatted string to a string `s`.
- Parses `s` as `expr1, expr2, ...` using the engine’s expression lexer/parser.
- Parsing detail: after each comma, the engine skips ASCII spaces (not tabs) before reading the next expression.
- Stores the resulting integer values into `RESULT:0..` and returns.

**Errors & validation**
- Errors if any parsed expression is not a valid integer expression.

**Examples**
- `RETURNFORM 1, 2, %A%`

## RETURNF (instruction)

**Summary**
- Returns from a user-defined expression function (`#FUNCTION/#FUNCTIONS`) with an optional return value.

**Syntax**
- `RETURNF`
- `RETURNF <expr>`

**Arguments**
- `<expr>` may be int or string, but should match the function’s declared return type.

**Defaults / optional arguments**
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

**Syntax**
- `STRLEN <rawString>`

**Arguments**
- `<rawString>`: the literal remainder of the line (not a normal string expression).

**Defaults / optional arguments**
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

**Syntax**
- `STRLENFORM <formString>`

**Arguments**
- `<formString>`: FORM/formatted string expression (supports `%...%` and `{...}`).

**Defaults / optional arguments**
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

**Syntax**
- `STRLENU <rawString>`

**Arguments**
- `<rawString>`: the literal remainder of the line (not a normal string expression).

**Defaults / optional arguments**
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

**Syntax**
- `STRLENFORMU <formString>`

**Arguments**
- `<formString>`: FORM/formatted string expression.

**Defaults / optional arguments**
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
- (TODO: not yet documented)

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
- Observable engine behavior: keeps `MASTER` fixed at its numeric position for this instruction.

**Syntax**
- `SORTCHARA`
- `SORTCHARA FORWARD | BACK`
- `SORTCHARA <charaVarTerm> [ , FORWARD | BACK ]`

**Arguments**
- `<charaVarTerm>`: a variable term whose identifier is a character-data variable.
- Order: `FORWARD` = ascending, `BACK` = descending.
- If the key variable is an array, the element indices are taken from the variable term’s subscripts after the character selector.

**Defaults / optional arguments**
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

**Syntax**
- `SWAP <var1>, <var2>`

**Arguments**
- `<var1>`: a changeable variable term (must not be `CONST`).
- `<var2>`: a changeable variable term (same type as `<var1>`).

**Defaults / optional arguments**
- None.

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
- Seeds the engine’s legacy RNG (Mersenne Twister) with a specified integer seed.

**Syntax**
- `RANDOMIZE`
- `RANDOMIZE <seed>`

**Arguments**
- `<seed>` (optional): integer expression. If omitted, the seed defaults to `0`.

**Defaults / optional arguments**
- `<seed>` defaults to `0`.

**Semantics**
- If `UseNewRandom` is enabled in JSON config:
  - Emits a warning and does nothing (implementation detail).
- Otherwise:
  - Replaces the engine’s legacy RNG instance with `new MTRandom(<seed>)`.
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- None (besides normal integer-expression evaluation errors).

**Examples**
- `RANDOMIZE 0`
- `RANDOMIZE 12345`

## DUMPRAND (instruction)

**Summary**
- Dumps the engine’s legacy RNG state into the `RANDDATA` variable.

**Syntax**
- `DUMPRAND`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- If `UseNewRandom` is enabled in JSON config:
  - Emits a warning and does nothing (implementation detail).
- Otherwise:
  - Writes the legacy RNG state into `RANDDATA` (via `MTRandom.GetRand(RANDDATA)`).
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- None.

**Examples**
- `DUMPRAND`

## INITRAND (instruction)

**Summary**
- Initializes the engine’s legacy RNG state from the `RANDDATA` variable.

**Syntax**
- `INITRAND`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- If `UseNewRandom` is enabled in JSON config:
  - Emits a warning and does nothing (implementation detail).
- Otherwise:
  - Loads the legacy RNG state from `RANDDATA` (via `MTRandom.SetRand(RANDDATA)`).
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

**Syntax**
- `DATA [<raw text>]`
- `DATA;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).
  - Parsing detail: as with most instructions, Emuera consumes exactly one delimiter character after the keyword (space/tab/full-width-space if enabled, or `;`). The remainder of the line becomes the raw text.

**Defaults / optional arguments**
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

**Syntax**
- `DATAFORM [<FORM string>]`

**Arguments**
- Optional FORM/formatted string scanned to end-of-line.

**Defaults / optional arguments**
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

**Syntax**
- `ENDDATA`

**Arguments**
- None.

**Defaults / optional arguments**
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

**Syntax**
- `DATALIST`
  - `DATA ...` / `DATAFORM ...` (one or more)
- `ENDLIST`

**Arguments**
- None.

**Defaults / optional arguments**
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

**Syntax**
- `ENDLIST`

**Arguments**
- None.

**Defaults / optional arguments**
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

**Syntax**
- `STRDATA [<strVarTerm>]` ... `ENDDATA`

**Arguments**
- Optional `<strVarTerm>`: changeable string variable term to receive the result.
- If omitted, defaults to `RESULTS` (engine behavior).

**Defaults / optional arguments**
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
- Enables/disables Emuera’s “skip output” mode (`skipPrint`), which causes most print/wait/input built-ins to be skipped by the script runner.
- Also sets `RESULT` to indicate whether skip mode is currently enabled.

**Syntax**
- `SKIPDISP <int expr>`

**Arguments**
- `<int expr>`: `0` disables skip mode; non-zero enables skip mode.

**Defaults / optional arguments**
- None.

**Semantics**
- Evaluates `<int expr>` to `v`.
- Sets:
  - `skipPrint = (v != 0)`
  - `userDefinedSkip = (v != 0)` (used to distinguish “user requested skip” from internal engine skip states)
  - `RESULT = (skipPrint ? 1 : 0)`
- While `skipPrint` is true, the script execution loop *skips* any built-in instruction whose registration has the `IS_PRINT` flag (this includes `PRINT*`, `WAIT*`, `INPUT*`, etc.).
- Special case (runtime error): if `skipPrint` is true **and** `userDefinedSkip` is true, then encountering an `IS_INPUT` instruction causes a runtime error rather than silently skipping.

**Errors & validation**
- Argument type errors follow the normal integer-expression argument rules.
- Runtime error if an input instruction is reached while `skipPrint` is active due to `SKIPDISP`.

**Examples**
- `SKIPDISP 1` (enable skip)
- `SKIPDISP 0` (disable skip)

## NOSKIP (instruction)

**Summary**
- Begins a `NOSKIP ... ENDNOSKIP` block that temporarily disables `skipPrint` within the block body.
- Intended to force some output/wait behavior to run even if `SKIPDISP` is currently skipping print-family instructions.

**Syntax**
- `NOSKIP`
  - `...`
- `ENDNOSKIP`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- This is a structural block (`NOSKIP` pairs with `ENDNOSKIP`).
- At runtime when `NOSKIP` is executed:
  - If the matching `ENDNOSKIP` was not linked by the loader, the engine throws an error.
  - Saves the current `skipPrint` into an internal slot (`saveSkip`).
  - If `skipPrint` is currently true, sets `skipPrint = false` for the duration of the block.
- At runtime when `ENDNOSKIP` is executed:
  - If `saveSkip` was true at the block entry, sets `skipPrint = true` (restoring skip mode).
  - If `saveSkip` was false, does nothing (so if you enabled skip inside the block manually, it remains enabled).

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

**Syntax**
- `ENDNOSKIP`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- Structural marker paired with `NOSKIP`.
- Restores `skipPrint` to its saved value when the block was entered (see `NOSKIP`).

**Errors & validation**
- `ENDNOSKIP` without a matching open `NOSKIP` is a load-time error (the line is marked as error).

**Examples**
- (See `NOSKIP`.)

## ARRAYSHIFT (instruction)

**Summary**
- Shifts elements in a mutable 1D array variable by a signed offset and fills new slots with a default value.

**Syntax**
- `ARRAYSHIFT <arrayVar>, <shift>, <default> [, <start> [, <count>]]`

**Arguments**
- `<arrayVar>`: changeable 1D array variable term.
- `<shift>`: int expression.
- `<default>`: expression of the same scalar type as the array element type.
- `<start>`: int expression (default `0`).
- `<count>`: int expression (default “to end”; engine uses a sentinel).

**Defaults / optional arguments**
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

**Syntax**
- `ARRAYREMOVE <arrayVar>, <start>, <count>`

**Arguments**
- `<arrayVar>`: changeable 1D array variable term.
- `<start>`: integer expression; start index (0-based).
- `<count>`: integer expression; number of elements to remove.

**Defaults / optional arguments**
- None.

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

**Defaults / optional arguments**
- If `FORWARD|BACK` is omitted, order defaults to ascending and the engine does not accept `<start>/<count>` (parsing quirk).
- `<start>` defaults to `0` when `FORWARD|BACK` is present but no subrange is provided.
- `<count>` omitted means “to the end”.

**Semantics**
- Sorts the specified region of the array:
  - The runtime treats `count <= 0` as “to the end” (but an explicitly provided `count == 0` is handled as a no-op in the instruction dispatcher).
- Implementation detail / parsing quirk:
  - The argument builder only parses `<start>` and `<count>` if the `FORWARD|BACK` token is present.

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

**Syntax**
- `ARRAYCOPY <srcVarNameExpr>, <dstVarNameExpr>`

**Arguments**
- `<srcVarNameExpr>`: string expression whose value is a variable name.
- `<dstVarNameExpr>`: string expression whose value is a variable name.

**Defaults / optional arguments**
- None.

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

**Syntax**
- `SKIPLOG <int expr>`

**Arguments**
- `<int expr>`: `0` clears message-skip; non-zero enables message-skip.

**Defaults / optional arguments**
- None.

**Semantics**
- Evaluates `<int expr>` to `v`.
- Sets `Console.MesSkip = (v != 0)`.
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

**Syntax**
- `JUMP <functionName> [, <arg1>, <arg2>, ... ]`
- `JUMP <functionName>(<arg1>, <arg2>, ... )`

**Arguments**
- Same as `CALL`.

**Defaults / optional arguments**
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

**Defaults / optional arguments**
- If the callee declares more parameters than provided arguments, omitted arguments are handled by the engine’s user-function argument binder (defaults and config gates apply).

**Semantics**
- Resolves the target label to a non-event function.
  - If `CompatiCallEvent` is enabled, an event function name is also callable via `CALL` (compatibility behavior: it calls only the first-defined function, ignoring event priority/single flags).
- Evaluates arguments, binds them to the callee’s declared formals (including `REF` behavior), then enters the callee.
- When the callee executes `RETURN` (or reaches end-of-function), control returns to the statement after the `CALL`.
- Engine implementation detail: if `<functionName>` is a compile-time constant, the loader tries to resolve the callee and pre-check argument binding during the load phase.

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

**Syntax**
- `TRYJUMP <functionName> [, <arg1>, <arg2>, ... ]`
- `TRYJUMP <functionName>(<arg1>, <arg2>, ... )`

**Arguments**
- Same as `JUMP`.

**Defaults / optional arguments**
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

**Syntax**
- `TRYCALL <functionName> [, <arg1>, <arg2>, ... ]`
- `TRYCALL <functionName>(<arg1>, <arg2>, ... )`

**Arguments**
- Same as `CALL`.

**Defaults / optional arguments**
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

**Syntax**
- `JUMPFORM <formString> [, <arg1>, <arg2>, ... ]`
- `JUMPFORM <formString>(<arg1>, <arg2>, ... )`

**Arguments**
- Same as `CALLFORM`.

**Defaults / optional arguments**
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

**Syntax**
- `CALLFORM <formString> [, <arg1>, <arg2>, ... ]`
- `CALLFORM <formString>(<arg1>, <arg2>, ... )`

**Arguments**
- `<formString>`: FORM/formatted string; the evaluated result is used as the function name.
  - If this FORM expression constant-folds to a constant string, the engine treats it like `CALL` for load-time resolution.
- `<argN>`: same as `CALL`.

**Defaults / optional arguments**
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

**Syntax**
- `TRYJUMPFORM <formString> [, <arg1>, <arg2>, ... ]`
- `TRYJUMPFORM <formString>(<arg1>, <arg2>, ... )`

**Arguments**
- Same as `JUMPFORM`.

**Defaults / optional arguments**
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

**Syntax**
- `TRYCALLFORM <formString> [, <arg1>, <arg2>, ... ]`
- `TRYCALLFORM <formString>(<arg1>, <arg2>, ... )`

**Arguments**
- Same as `CALLFORM`.

**Defaults / optional arguments**
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

**Syntax**
- `TRYCJUMP <functionName> [, <arg1>, ... ]`
- `CATCH`
  - `<catch body>`
  - `ENDCATCH`

**Arguments**
- Same as `JUMP`.

**Defaults / optional arguments**
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

**Syntax**
- `TRYCCALL <functionName> [, <arg1>, ... ]`
- `CATCH`
  - `<catch body>`
  - `ENDCATCH`

**Arguments**
- Same as `CALL`.

**Defaults / optional arguments**
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

**Syntax**
- `TRYCJUMPFORM <formString> [, <arg1>, ... ]`
- `CATCH`
  - `<catch body>`
  - `ENDCATCH`

**Arguments**
- Same as `JUMPFORM`.

**Defaults / optional arguments**
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

**Syntax**
- `TRYCCALLFORM <formString> [, <arg1>, ... ]`
- `CATCH`
  - `<catch body>`
  - `ENDCATCH`

**Arguments**
- Same as `CALLFORM`.

**Defaults / optional arguments**
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

**Syntax**
- `CALLF <methodName> [, <arg1>, <arg2>, ... ]`
- `CALLF <methodName>(<arg1>, <arg2>, ... )`

**Arguments**
- `<methodName>`: a raw string token read up to `(` / `[` / `,` / `;` and then trimmed.
- `<argN>`: expressions passed to the method.

**Defaults / optional arguments**
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

**Syntax**
- `CALLFORMF <formString> [, <arg1>, <arg2>, ... ]`
- `CALLFORMF <formString>(<arg1>, <arg2>, ... )`

**Arguments**
- `<formString>`: FORM/formatted string; the evaluated result is used as the method name.
- `<argN>`: expressions passed to the method.

**Defaults / optional arguments**
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

**Syntax**
- `GOTO <labelName>`

**Arguments**
- `<labelName>`: a raw string token; used to resolve a `$label` relative to the current function.

**Defaults / optional arguments**
- None.

**Semantics**
- If the label exists, jumps to the `$label` marker; execution continues at the line after the `$label`.
- The argument builder accepts `(...)` / comma forms, but `GOTO` does not use argument lists; only the label name matters.

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

**Syntax**
- `TRYGOTO <labelName>`

**Arguments**
- Same as `GOTO`.

**Defaults / optional arguments**
- None.

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

**Syntax**
- `GOTOFORM <formString>`

**Arguments**
- `<formString>`: FORM/formatted string; the evaluated result is used as the `$label` name.

**Defaults / optional arguments**
- None.

**Semantics**
- Evaluates the label name and jumps if it resolves to a `$label` in the current function.

**Errors & validation**
- Same as `GOTO`, but errors may occur at runtime if the evaluated label name varies.

**Examples**
- `GOTOFORM "CASE_%RESULT%"`

## TRYGOTOFORM (instruction)

**Summary**
- Like `GOTOFORM`, but if the evaluated `$label` name does not exist the instruction **does not error** and simply falls through.

**Syntax**
- `TRYGOTOFORM <formString>`

**Arguments**
- Same as `GOTOFORM`.

**Defaults / optional arguments**
- None.

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

**Syntax**
- `TRYCGOTO <labelName>`
- `CATCH`
  - `<catch body>`
  - `ENDCATCH`

**Arguments**
- Same as `GOTO`.

**Defaults / optional arguments**
- None.

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

**Syntax**
- `TRYCGOTOFORM <formString>`
- `CATCH`
  - `<catch body>`
  - `ENDCATCH`

**Arguments**
- Same as `GOTOFORM`.

**Defaults / optional arguments**
- None.

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

**Syntax**
- `CATCH`
  - `<catch body>`
  - `ENDCATCH`

**Arguments**
- None.

**Defaults / optional arguments**
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

**Syntax**
- `ENDCATCH`

**Arguments**
- None.

**Defaults / optional arguments**
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

**Defaults / optional arguments**
- None.

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
- Implementation detail: `FUNC` syntax is parsed using the same argument builder as `CALLFORM` (candidate name is a FORM string; arguments are normal expressions).

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

**Syntax**
- `TRYJUMPLIST`
  - `FUNC <formString> [, <arg1>, ... ]`
  - `...`
  - `ENDFUNC`

**Arguments**
- Same as `TRYCALLLIST`.

**Defaults / optional arguments**
- None.

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

**Syntax**
- `TRYGOTOLIST`
  - `FUNC <formString>`
  - `FUNC <formString>`
  - `...`
  - `ENDFUNC`

**Arguments**
- Each `FUNC` item provides a label name as a **FORM/formatted string expression** (evaluated to a string at runtime).

**Defaults / optional arguments**
- None.

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

**Syntax**
- Inside `TRYCALLLIST` / `TRYJUMPLIST`:
  - `FUNC <formString> [, <arg1>, <arg2>, ... ]`
  - `FUNC <formString>(<arg1>, <arg2>, ... )`
- Inside `TRYGOTOLIST`:
  - `FUNC <formString>`

**Arguments**
- `<formString>`: a FORM/formatted string expression evaluated to a function name or label name.
- `<argN>`: optional call arguments (not allowed for `TRYGOTOLIST`).

**Defaults / optional arguments**
- None.

**Semantics**
- Not executed as a standalone statement.
- During load, Emuera collects `FUNC` lines into the surrounding `TRY*LIST` instruction’s internal `callList`.
- At runtime, the surrounding `TRY*LIST` evaluates these items in order (see `TRYCALLLIST` / `TRYJUMPLIST` / `TRYGOTOLIST`).
- Implementation detail: `FUNC` is parsed using the same argument builder as `CALLFORM`.
- Implementation detail: in `TRYCALLLIST` / `TRYJUMPLIST`, the optional `[...]` subname segment is parsed and stored, but the current runtime implementation does not use it when selecting/calling the function.

**Errors & validation**
- `FUNC` must appear only inside `TRY*LIST ... ENDFUNC`; otherwise it is a load-time error (the line is marked as error).

**Examples**
- `FUNC HOOK_%TARGET%, TARGET`

## ENDFUNC (instruction)

**Summary**
- Ends a `TRY*LIST ... ENDFUNC` block.

**Syntax**
- `ENDFUNC`

**Arguments**
- None.

**Defaults / optional arguments**
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

**Syntax**
- `SAVEVAR <name>, <saveText>, <var1> [, <var2> ...]`

**Arguments**
- `<name>`: string expression; intended file name component.
- `<saveText>`: string expression; intended description text.
- `<var*>`: one or more changeable non-character variable terms (arrays are allowed; several variable categories are rejected).

**Defaults / optional arguments**
- None.

**Semantics**
- The current engine implementation throws a “not implemented” error at runtime.
- (Implementation note) The underlying variable evaluator contains binary save/load support for variable packs, but the instruction is disabled.
- See also: `save-files.md` (directories, partitions, and on-disk formats)

**Errors & validation**
- Always errors at runtime (`NotImplCodeEE`).

**Examples**
- `SAVEVAR "vars", "checkpoint", A, B, C`

## LOADVAR (instruction)

**Summary**
- Declared but **not implemented** in this engine build (always errors).

**Syntax**
- `LOADVAR <name>`

**Arguments**
- `<name>`: string expression; intended file name component.

**Defaults / optional arguments**
- None.

**Semantics**
- The current engine implementation throws a “not implemented” error at runtime.
- See also: `save-files.md` (directories, partitions, and on-disk formats)

**Errors & validation**
- Always errors at runtime (`NotImplCodeEE`).

**Examples**
- `LOADVAR "vars"`

## SAVECHARA (instruction)

**Summary**
- Saves one or more characters into a `dat/chara_<name>.dat` file (binary only).

**Syntax**
- `SAVECHARA <name>, <saveText>, <charaNo1> [, <charaNo2> ...]`

**Arguments**
- `<name>`: string expression; the file name component.
- `<saveText>`: string expression stored in the file as a description.
- `<charaNo*>`: one or more integer expressions; character indices to save (0-based).

**Defaults / optional arguments**
- None.

**Semantics**
- Writes a binary file under `Program.DatDir`:
  - Path is `chara_<name>.dat`.
- File format (implementation detail):
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

**Syntax**
- `LOADCHARA <name>`

**Arguments**
- `<name>`: string expression; the file name component.

**Defaults / optional arguments**
- None.

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
- (TODO: not yet documented)

## HTML_TAGSPLIT (instruction)
**Summary**
- (TODO: not yet documented)

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

**Syntax**
- `GETTIME`

**Arguments**
- None.

**Defaults / optional arguments**
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

**Syntax**
- `POWER <dest>, <x>, <y>`

**Arguments**
- `<dest>`: changeable integer variable term (destination).
- `<x>`: integer expression (base).
- `<y>`: integer expression (exponent).

**Defaults / optional arguments**
- None.

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

**Syntax**
- `FORCE_BEGIN <keyword>`

**Arguments**
- Same as `BEGIN`.

**Defaults / optional arguments**
- None.

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
- (TODO: not yet documented)

## HTML_PRINT_ISLAND_CLEAR (instruction)
**Summary**
- (TODO: not yet documented)

## PRINTN (instruction)

**Summary**
- `PRINTN` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Syntax**
- `PRINTN [<raw text>]`
- `PRINTN;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).

**Defaults / optional arguments**
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

**Syntax**
- `PRINTVN <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

**Defaults / optional arguments**
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

**Syntax**
- `PRINTSN <string expr>`

**Arguments**
- A single string expression (must be present).

**Defaults / optional arguments**
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

**Syntax**
- `PRINTFORMN [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

**Defaults / optional arguments**
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

**Syntax**
- `PRINTFORMSN <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

**Defaults / optional arguments**
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
- Returns the first character index in the current character list whose character-variable cell equals a target value.

**Syntax**
- `FINDCHARA(charaVarTerm, value [, startIndex [, lastIndex]])`
- Optional arguments can be omitted by leaving an empty argument slot (e.g. `FINDCHARA(NAME, "A", , 10)`).

**Signatures / argument rules**
- `FINDCHARA(charaVarTerm, value)` → `long`
- `FINDCHARA(charaVarTerm, value, startIndex)` → `long`
- `FINDCHARA(charaVarTerm, value, startIndex, lastIndex)` → `long`

**Arguments**
- `charaVarTerm`: character-data variable term.
  - Must evaluate to a variable term whose identifier is marked as “character data”.
  - If the variable is a 1D/2D array, the array subscripts on `charaVarTerm` select which per-character cell is compared.
- `value`: scalar value to match; must be the same scalar type as the selected cell (string vs int).
- `startIndex` (optional): int expression; inclusive start character index.
- `lastIndex` (optional): int expression; exclusive end character index.

**Defaults / optional arguments**
- If `startIndex` is omitted (or omitted as an empty slot): defaults to `0`.
- If `lastIndex` is omitted (or omitted as an empty slot): defaults to `CHARANUM` (the current total number of characters).

**Semantics**
- Reads the current `CHARANUM` and searches forward in the half-open range `[startIndex, lastIndex)`.
- For each character index `i` in the range, compares `charaVarTerm(i)` against `value` using direct equality:
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
- Like `FINDCHARA`, but searches backward and returns the last matching character index in the range.

**Syntax**
- `FINDLASTCHARA(charaVarTerm, value [, startIndex [, lastIndex]])`
- Optional arguments can be omitted by leaving an empty argument slot (e.g. `FINDLASTCHARA(NAME, "A", , 10)`).

**Signatures / argument rules**
- `FINDLASTCHARA(charaVarTerm, value)` → `long`
- `FINDLASTCHARA(charaVarTerm, value, startIndex)` → `long`
- `FINDLASTCHARA(charaVarTerm, value, startIndex, lastIndex)` → `long`

**Arguments**
- `charaVarTerm`: character-data variable term.
  - Must evaluate to a variable term whose identifier is marked as “character data”.
  - If the variable is a 1D/2D array, the array subscripts on `charaVarTerm` select which per-character cell is compared.
- `value`: scalar value to match; must be the same scalar type as the selected cell (string vs int).
- `startIndex` (optional): int expression; inclusive start character index.
- `lastIndex` (optional): int expression; exclusive end character index.

**Defaults / optional arguments**
- If `startIndex` is omitted (or omitted as an empty slot): defaults to `0`.
- If `lastIndex` is omitted (or omitted as an empty slot): defaults to `CHARANUM` (the current total number of characters).

**Semantics**
- Reads the current `CHARANUM` and searches backward in the half-open range `[startIndex, lastIndex)`.
- The search order is: `lastIndex - 1`, `lastIndex - 2`, ..., down to `startIndex`.
- For each character index `i` in the range, compares `charaVarTerm(i)` against `value` using direct equality:
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
- (TODO: not yet documented)

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
- Returns a substring where `start`/`length` are measured in the engine’s current language-encoding byte count (not Unicode code units).

**Syntax**
- `SUBSTRING(str [, start [, length]])`
- Optional arguments can be omitted by leaving an empty argument slot (e.g. `SUBSTRING(str, , 10)`).

**Signatures / argument rules**
- `SUBSTRING(str)` → `string`
- `SUBSTRING(str, start)` → `string`
- `SUBSTRING(str, start, length)` → `string`

**Arguments**
- `str`: string.
- `start` (optional): int (language-length offset; see Semantics).
- `length` (optional): int (language-length count; `<0` means “to end”).

**Defaults / optional arguments**
- If `start` is omitted (or omitted as an empty slot): defaults to `0`.
- If `length` is omitted (or omitted as an empty slot): defaults to `-1` (meaning “to end”).

**Semantics**
- The engine defines a “language length” for strings:
  - If `str` is ASCII-only: `total = str.Length`.
  - Otherwise: `total = ByteCount(str)` under the engine’s configured language encoding (see `useLanguage` / `Config.Language`).
- Special cases:
  - If `start >= total` or `length == 0`: returns `""`.
  - If `length < 0` or `length > total`: `length` is treated as `total` (effectively “to end”).
  - If `start <= 0` and `length == total`: returns `str` unchanged.
- Start position selection (character-boundary rounding):
  - If `start <= 0`, the substring starts at the first character.
  - If `start > 0`, the engine advances from the beginning, accumulating `ByteCount(char)` until the accumulated count becomes `>= start`; the substring then starts at the *next* character position reached by that scan.
  - This means `start` values that fall “inside” a multi-byte character effectively round up to the next character boundary (the multi-byte character is skipped).
- Length selection (character-boundary rounding):
  - Starting from the chosen start character, the engine appends characters while accumulating `ByteCount(char)` until the accumulated count becomes `>= length`, or until end-of-string.
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

**Syntax**
- `TOSTR(i [, format])`
- Optional arguments can be omitted by leaving an empty argument slot (e.g. `TOSTR(42, )`).

**Signatures / argument rules**
- `TOSTR(i)` → `string`
- `TOSTR(i, format)` → `string`

**Arguments**
- `i`: int expression.
- `format` (optional): string expression passed to `Int64.ToString(format)`.

**Defaults / optional arguments**
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

**Syntax**
- `TOINT(str)`

**Signatures / argument rules**
- `TOINT(str)` → `long`

**Arguments**
- `str`: string expression.

**Defaults / optional arguments**
- None.

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
    - Implementation detail: exponent digits are parsed by the same digit-reader used for the main literal (so the accepted exponent digit set depends on the literal’s base).
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

**Syntax**
- `TOUPPER(str)`

**Signatures / argument rules**
- `TOUPPER(str)` → `string`

**Arguments**
- `str`: string expression.

**Defaults / optional arguments**
- None.

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

**Syntax**
- `TOLOWER(str)`

**Signatures / argument rules**
- `TOLOWER(str)` → `string`

**Arguments**
- `str`: string expression.

**Defaults / optional arguments**
- None.

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
- Converts full-width characters to half-width (narrow) form using the engine’s configured language setting.

**Syntax**
- `TOHALF(str)`

**Signatures / argument rules**
- `TOHALF(str)` → `string`

**Arguments**
- `str`: string expression.

**Defaults / optional arguments**
- None.

**Semantics**
- If `str` is null/empty: returns `""`.
- Otherwise: uses VisualBasic `Strings.StrConv(..., Narrow, Config.Language)`.

**Errors & validation**
- Argument type/count errors are rejected by the engine’s function-method argument checker.
- Any runtime exceptions from the underlying `.NET` conversion routine propagate as engine errors.

**Examples**
- `TOHALF("ＡＢＣ")` → `"ABC"`

## TOFULL (expression function)

**Summary**
- Converts half-width characters to full-width (wide) form using the engine’s configured language setting.

**Syntax**
- `TOFULL(str)`

**Signatures / argument rules**
- `TOFULL(str)` → `string`

**Arguments**
- `str`: string expression.

**Defaults / optional arguments**
- None.

**Semantics**
- If `str` is null/empty: returns `""`.
- Otherwise: uses VisualBasic `Strings.StrConv(..., Wide, Config.Language)`.

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
- (TODO: not yet documented)

## HTML_POPPRINTINGSTR (expression function)
**Summary**
- (TODO: not yet documented)

## HTML_TOPLAINTEXT (expression function)
**Summary**
- (TODO: not yet documented)

## HTML_ESCAPE (expression function)
**Summary**
- (TODO: not yet documented)

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
- (TODO: not yet documented)

## HTML_SUBSTRING (expression function)
**Summary**
- (TODO: not yet documented)

## HTML_STRINGLINES (expression function)
**Summary**
- (TODO: not yet documented)

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
