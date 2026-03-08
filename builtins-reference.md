# EraBasic Built-ins Reference (Emuera / EvilMask)

Generated on `2026-03-08`.

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

- **Error**: the engine reports an error. This is distinct from rejection; the exact aftermath is documented per topic/built-in where relevant.
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
- RHS parsing mode is determined by the operator and LHS type:
  - int LHS: RHS is parsed as normal expressions.
  - string LHS with `=`: RHS is scanned as a formatted string until end-of-line.
  - string LHS with `'=` / `+=` / `*=`: RHS is parsed as normal expressions.

**Semantics**
- There is no `SET` keyword in EraBasic source; this entry documents the language’s assignment syntax.
- Assignment operator recognition:
  - The engine recognizes: `=`, `'=`; `++`, `--`; and compound forms `+=`, `-=`, `*=`, `/=`, `%=`, `<<=`, `>>=`, `|=`, `&=`, `^=`.
- Allowed operators depend on LHS type:
  - int LHS: accepts `=`, `++`, `--`, and the integer compound operators `+=`, `-=`, `*=`, `/=`, `%=`, `<<=`, `>>=`, `|=`, `&=`, `^=`. The string-assignment operator `'=` is rejected.
  - string LHS: accepts `=` (FORM assignment), `'=` (string-expression assignment), `+=` (string concatenation), and `*=` (string repetition). Other compound operators are rejected as invalid.
- If the RHS is a single value:
  - `=` assigns that value.
  - For compound assignment operators, the resulting value is the same as `LHS = (LHS <op> RHS)` (using the operator implied by the compound form).
- String-typed operator constraints:
  - `strVar '= expr` requires each RHS expression to be string-typed.
  - `strVar += expr` requires the RHS expression to be string-typed.
  - `strVar *= expr` requires the RHS expression to be int-typed.
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
- Errors if LHS cannot be read as a single variable term, if LHS is const, or if operator is incompatible with the LHS type (for example, `intVar '= expr`).
- Errors if assigning string→int or int→string in contexts that disallow it (for example, `intVar = "x"`, `strVar '= 1`, `strVar += 1`, or `strVar *= "x"`).
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
- `<raw text>` (optional, raw text; default `""`): not an expression.
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
- Output is appended to the engine’s **pending print buffer**; see `output-flow.md` for the shared layer model.
- Appending buffered `PRINT*` output does **not** immediately create a visible display-line entry.
- If output skipping is active (`SKIPDISP`):
  - these instructions are skipped before execution by the interpreter,
  - arguments are not evaluated and there are no side effects.
- Argument/evaluation modes by base variant (before suffix letters):
  - `PRINT*` (raw): uses the raw literal remainder-of-line (not an expression).
  - `PRINTS*`: evaluates one string expression.
  - `PRINTV*`: evaluates a comma-separated list of expressions; each element must be either integer or string; results are concatenated with no separator (left-to-right).
  - `PRINTFORM*`: parses its argument as a FORM/formatted string at load/parse time, then evaluates it at runtime.
  - `PRINTFORMS*`: evaluates one string expression to obtain a format-string source, then parses and evaluates it as a FORM string at runtime (see below).
- Suffix letters and their meaning (parser order is important):
  - `C` / `LC` (cell output): after building the output string, outputs a fixed-width cell.
    - `...C` uses right alignment, `...LC` uses left alignment.
    - This is **not** the same as the newline suffix `L`; for example, `PRINTLC` means “left-aligned cell”, not “PRINTL + C”.
    - Cell formatting rules are defined by the console implementation; see `PRINTC` / `PRINTLC`.
    - Cell variants do not use the `...L / ...W / ...N` newline/wait handling; they only append a cell to the buffer.
  - `K` (kana conversion): applies kana conversion as configured by `FORCEKANA`.
  - `D` (ignore `SETCOLOR` color): ignores `SETCOLOR`’s *color* for this output (font name/style still apply).
  - `L` (line end): after printing, flushes the current buffer as visible output and ends the logical line.
  - `W` (line end + wait): like `L`, then waits for a key.
  - `N` (flush + wait without line end): flushes current buffered content to visible output, then waits **without** ending the logical line.
    - the next later flush is merged into the same logical line.
- FORM-at-runtime behavior (`PRINTFORMS*`):
  - evaluates the string expression to `src`,
  - normalizes escapes using the FORM escape rules,
  - parses `src` as a FORM string up to end-of-line,
  - evaluates it and prints the result.
- `PRINT` itself:
  - uses the raw literal argument as the output string,
  - appends it with `lineEnd = true`, so when the buffer is later flushed it belongs to a logical line that ends at that point.
- Buffer/temporary-line boundary:
  - appending `PRINT*` content to the pending print buffer does not by itself remove a trailing temporary line,
  - the temporary line is only replaced when later visible output is actually appended.

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
- `PRINTL`
- `PRINTL <raw text>`
- `PRINTL;<raw text>`

**Arguments**
- `<raw text>` (optional, raw text; default `""`): not an expression.

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
- `PRINTW`
- `PRINTW <raw text>`
- `PRINTW;<raw text>`

**Arguments**
- `<raw text>` (optional, raw text; default `""`): not an expression.

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
- `PRINTV <value1> [, <value2> ...]`

**Arguments**
- `<valueN>` (expression): each occurrence must evaluate to an int or string; ints are converted with `ToString` and concatenated with no separator.

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
- `PRINTVL <value1> [, <value2> ...]`

**Arguments**
- `<valueN>` (expression): each occurrence must evaluate to an int or string; ints are converted with `ToString` and concatenated with no separator.

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
- `PRINTVW <value1> [, <value2> ...]`

**Arguments**
- `<valueN>` (expression): each occurrence must evaluate to an int or string; ints are converted with `ToString` and concatenated with no separator.

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
- `PRINTS <text>`

**Arguments**
- `<text>` (string): text to print.

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
- `PRINTSL <text>`

**Arguments**
- `<text>` (string): text to print.

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
- `PRINTSW <text>`

**Arguments**
- `<text>` (string): text to print.

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
- `PRINTFORM [<formString>]`

**Arguments**
- `<formString>` (optional, FORM/formatted string; default `""`): scanned to end-of-line.

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
- `PRINTFORML [<formString>]`

**Arguments**
- `<formString>` (optional, FORM/formatted string; default `""`): scanned to end-of-line.

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
- `PRINTFORMW [<formString>]`

**Arguments**
- `<formString>` (optional, FORM/formatted string; default `""`): scanned to end-of-line.

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
- `PRINTFORMS <formatSource>`

**Arguments**
- `<formatSource>` (string): evaluated to a string, then parsed as a FORM/formatted string at runtime.

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
- `PRINTFORMSL <formatSource>`

**Arguments**
- `<formatSource>` (string): evaluated to a string, then parsed as a FORM/formatted string at runtime.

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
- `PRINTFORMSW <formatSource>`

**Arguments**
- `<formatSource>` (string): evaluated to a string, then parsed as a FORM/formatted string at runtime.

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
- `PRINTK`
- `PRINTK <raw text>`
- `PRINTK;<raw text>`

**Arguments**
- `<raw text>` (optional, raw text; default `""`): not an expression.

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
- `PRINTKL`
- `PRINTKL <raw text>`
- `PRINTKL;<raw text>`

**Arguments**
- `<raw text>` (optional, raw text; default `""`): not an expression.

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
- `PRINTKW`
- `PRINTKW <raw text>`
- `PRINTKW;<raw text>`

**Arguments**
- `<raw text>` (optional, raw text; default `""`): not an expression.

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
- `PRINTVK <value1> [, <value2> ...]`

**Arguments**
- `<valueN>` (expression): each occurrence must evaluate to an int or string; ints are converted with `ToString` and concatenated with no separator.

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
- `PRINTVKL <value1> [, <value2> ...]`

**Arguments**
- `<valueN>` (expression): each occurrence must evaluate to an int or string; ints are converted with `ToString` and concatenated with no separator.

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
- `PRINTVKW <value1> [, <value2> ...]`

**Arguments**
- `<valueN>` (expression): each occurrence must evaluate to an int or string; ints are converted with `ToString` and concatenated with no separator.

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
- `PRINTSK <text>`

**Arguments**
- `<text>` (string): text to print.

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
- `PRINTSKL <text>`

**Arguments**
- `<text>` (string): text to print.

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
- `PRINTSKW <text>`

**Arguments**
- `<text>` (string): text to print.

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
- `PRINTFORMK [<formString>]`

**Arguments**
- `<formString>` (optional, FORM/formatted string; default `""`): scanned to end-of-line.

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
- `PRINTFORMKL [<formString>]`

**Arguments**
- `<formString>` (optional, FORM/formatted string; default `""`): scanned to end-of-line.

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
- `PRINTFORMKW [<formString>]`

**Arguments**
- `<formString>` (optional, FORM/formatted string; default `""`): scanned to end-of-line.

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
- `PRINTFORMSK <formatSource>`

**Arguments**
- `<formatSource>` (string): evaluated to a string, then parsed as a FORM/formatted string at runtime.

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
- `PRINTFORMSKL <formatSource>`

**Arguments**
- `<formatSource>` (string): evaluated to a string, then parsed as a FORM/formatted string at runtime.

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
- `PRINTFORMSKW <formatSource>`

**Arguments**
- `<formatSource>` (string): evaluated to a string, then parsed as a FORM/formatted string at runtime.

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
- `PRINTD`
- `PRINTD <raw text>`
- `PRINTD;<raw text>`

**Arguments**
- `<raw text>` (optional, raw text; default `""`): not an expression.

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
- `PRINTDL`
- `PRINTDL <raw text>`
- `PRINTDL;<raw text>`

**Arguments**
- `<raw text>` (optional, raw text; default `""`): not an expression.

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
- `PRINTDW`
- `PRINTDW <raw text>`
- `PRINTDW;<raw text>`

**Arguments**
- `<raw text>` (optional, raw text; default `""`): not an expression.

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
- `PRINTVD <value1> [, <value2> ...]`

**Arguments**
- `<valueN>` (expression): each occurrence must evaluate to an int or string; ints are converted with `ToString` and concatenated with no separator.

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
- `PRINTVDL <value1> [, <value2> ...]`

**Arguments**
- `<valueN>` (expression): each occurrence must evaluate to an int or string; ints are converted with `ToString` and concatenated with no separator.

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
- `PRINTVDW <value1> [, <value2> ...]`

**Arguments**
- `<valueN>` (expression): each occurrence must evaluate to an int or string; ints are converted with `ToString` and concatenated with no separator.

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
- `PRINTSD <text>`

**Arguments**
- `<text>` (string): text to print.

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
- `PRINTSDL <text>`

**Arguments**
- `<text>` (string): text to print.

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
- `PRINTSDW <text>`

**Arguments**
- `<text>` (string): text to print.

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
- `PRINTFORMD [<formString>]`

**Arguments**
- `<formString>` (optional, FORM/formatted string; default `""`): scanned to end-of-line.

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
- `PRINTFORMDL [<formString>]`

**Arguments**
- `<formString>` (optional, FORM/formatted string; default `""`): scanned to end-of-line.

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
- `PRINTFORMDW [<formString>]`

**Arguments**
- `<formString>` (optional, FORM/formatted string; default `""`): scanned to end-of-line.

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
- `PRINTFORMSD <formatSource>`

**Arguments**
- `<formatSource>` (string): evaluated to a string, then parsed as a FORM/formatted string at runtime.

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
- `PRINTFORMSDL <formatSource>`

**Arguments**
- `<formatSource>` (string): evaluated to a string, then parsed as a FORM/formatted string at runtime.

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
- `PRINTFORMSDW <formatSource>`

**Arguments**
- `<formatSource>` (string): evaluated to a string, then parsed as a FORM/formatted string at runtime.

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
- `PRINTSINGLE`
- `PRINTSINGLE <raw text>`
- `PRINTSINGLE;<raw text>`

**Arguments**
- `<raw text>` (optional, raw text; default `""`): not an expression.

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
- `PRINTSINGLEV <value1> [, <value2> ...]`

**Arguments**
- `<valueN>` (expression): each occurrence must evaluate to an int or string; ints are converted with `ToString` and concatenated with no separator.

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
- `PRINTSINGLES <text>`

**Arguments**
- `<text>` (string): text to print.

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
- `PRINTSINGLEFORM [<formString>]`

**Arguments**
- `<formString>` (optional, FORM/formatted string; default `""`): scanned to end-of-line.

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
- `PRINTSINGLEFORMS <formatSource>`

**Arguments**
- `<formatSource>` (string): evaluated to a string, then parsed as a FORM/formatted string at runtime.

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
- `PRINTSINGLEK`
- `PRINTSINGLEK <raw text>`
- `PRINTSINGLEK;<raw text>`

**Arguments**
- `<raw text>` (optional, raw text; default `""`): not an expression.

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
- `PRINTSINGLEVK <value1> [, <value2> ...]`

**Arguments**
- `<valueN>` (expression): each occurrence must evaluate to an int or string; ints are converted with `ToString` and concatenated with no separator.

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
- `PRINTSINGLESK <text>`

**Arguments**
- `<text>` (string): text to print.

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
- `PRINTSINGLEFORMK [<formString>]`

**Arguments**
- `<formString>` (optional, FORM/formatted string; default `""`): scanned to end-of-line.

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
- `PRINTSINGLEFORMSK <formatSource>`

**Arguments**
- `<formatSource>` (string): evaluated to a string, then parsed as a FORM/formatted string at runtime.

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
- `PRINTSINGLED`
- `PRINTSINGLED <raw text>`
- `PRINTSINGLED;<raw text>`

**Arguments**
- `<raw text>` (optional, raw text; default `""`): not an expression.

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
- `PRINTSINGLEVD <value1> [, <value2> ...]`

**Arguments**
- `<valueN>` (expression): each occurrence must evaluate to an int or string; ints are converted with `ToString` and concatenated with no separator.

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
- `PRINTSINGLESD <text>`

**Arguments**
- `<text>` (string): text to print.

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
- `PRINTSINGLEFORMD [<formString>]`

**Arguments**
- `<formString>` (optional, FORM/formatted string; default `""`): scanned to end-of-line.

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
- `PRINTSINGLEFORMSD <formatSource>`

**Arguments**
- `<formatSource>` (string): evaluated to a string, then parsed as a FORM/formatted string at runtime.

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
- `PRINTC`
- `PRINTC <raw text>`
- `PRINTC;<raw text>`

**Arguments**
- `<raw text>` (optional, raw text; default `""`): not an expression.
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
- `PRINTLC`
- `PRINTLC <raw text>`
- `PRINTLC;<raw text>`

**Arguments**
- `<raw text>` (optional, raw text; default `""`): not an expression.
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
- `PRINTFORMC [<formString>]`

**Arguments**
- `<formString>` (optional, FORM/formatted string; default `""`): scanned to end-of-line.

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
- `PRINTFORMLC [<formString>]`

**Arguments**
- `<formString>` (optional, FORM/formatted string; default `""`): scanned to end-of-line.

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
- `PRINTCK`
- `PRINTCK <raw text>`
- `PRINTCK;<raw text>`

**Arguments**
- `<raw text>` (optional, raw text; default `""`): not an expression.
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
- `PRINTLCK`
- `PRINTLCK <raw text>`
- `PRINTLCK;<raw text>`

**Arguments**
- `<raw text>` (optional, raw text; default `""`): not an expression.
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
- `PRINTFORMCK [<formString>]`

**Arguments**
- `<formString>` (optional, FORM/formatted string; default `""`): scanned to end-of-line.

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
- `PRINTFORMLCK [<formString>]`

**Arguments**
- `<formString>` (optional, FORM/formatted string; default `""`): scanned to end-of-line.

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
- `PRINTCD`
- `PRINTCD <raw text>`
- `PRINTCD;<raw text>`

**Arguments**
- `<raw text>` (optional, raw text; default `""`): not an expression.
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
- `PRINTLCD`
- `PRINTLCD <raw text>`
- `PRINTLCD;<raw text>`

**Arguments**
- `<raw text>` (optional, raw text; default `""`): not an expression.
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
- `PRINTFORMCD [<formString>]`

**Arguments**
- `<formString>` (optional, FORM/formatted string; default `""`): scanned to end-of-line.

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
- `PRINTFORMLCD [<formString>]`

**Arguments**
- `<formString>` (optional, FORM/formatted string; default `""`): scanned to end-of-line.

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
```text
PRINTDATA [<intVarTerm>]
    DATA <raw text> | DATAFORM <formString>
    ...
    [DATALIST
        DATA <raw text> | DATAFORM <formString>
        ...
    ENDLIST]
ENDDATA
```

- Header line: `PRINTDATA [<intVarTerm>]`
- Body entries may be single-line `DATA` / `DATAFORM` choices or nested `DATALIST ... ENDLIST` multi-line choices.
- Terminator line: `ENDDATA`

**Arguments**
- `<intVarTerm>` (optional, changeable int variable term): receives the 0-based chosen index.

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
```text
PRINTDATAL [<intVarTerm>]
    ...
ENDDATA
```

- Header line: `PRINTDATAL [<intVarTerm>]`
- Body / terminator structure is the same as `PRINTDATA`.

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
```erabasic
PRINTDATAL CHOICE
    DATA First option
    DATA Second option
ENDDATA
```

## PRINTDATAW (instruction)

**Summary**
- `PRINTDATAW` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Tags**
- io
- data-blocks

**Syntax**
```text
PRINTDATAW [<intVarTerm>]
    ...
ENDDATA
```

- Header line: `PRINTDATAW [<intVarTerm>]`
- Body / terminator structure is the same as `PRINTDATA`.

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
```erabasic
PRINTDATAW CHOICE
    DATA First option
    DATA Second option
ENDDATA
```

## PRINTDATAK (instruction)

**Summary**
- `PRINTDATAK` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Tags**
- io
- data-blocks

**Syntax**
```text
PRINTDATAK [<intVarTerm>]
    ...
ENDDATA
```

- Header line: `PRINTDATAK [<intVarTerm>]`
- Body / terminator structure is the same as `PRINTDATA`.

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
```erabasic
PRINTDATAK CHOICE
    DATA First option
    DATA Second option
ENDDATA
```

## PRINTDATAKL (instruction)

**Summary**
- `PRINTDATAKL` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Tags**
- io
- data-blocks

**Syntax**
```text
PRINTDATAKL [<intVarTerm>]
    ...
ENDDATA
```

- Header line: `PRINTDATAKL [<intVarTerm>]`
- Body / terminator structure is the same as `PRINTDATA`.

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
```erabasic
PRINTDATAKL CHOICE
    DATA First option
    DATA Second option
ENDDATA
```

## PRINTDATAKW (instruction)

**Summary**
- `PRINTDATAKW` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Tags**
- io
- data-blocks

**Syntax**
```text
PRINTDATAKW [<intVarTerm>]
    ...
ENDDATA
```

- Header line: `PRINTDATAKW [<intVarTerm>]`
- Body / terminator structure is the same as `PRINTDATA`.

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
```erabasic
PRINTDATAKW CHOICE
    DATA First option
    DATA Second option
ENDDATA
```

## PRINTDATAD (instruction)

**Summary**
- `PRINTDATAD` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Tags**
- io
- data-blocks

**Syntax**
```text
PRINTDATAD [<intVarTerm>]
    ...
ENDDATA
```

- Header line: `PRINTDATAD [<intVarTerm>]`
- Body / terminator structure is the same as `PRINTDATA`.

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
```erabasic
PRINTDATAD CHOICE
    DATA First option
    DATA Second option
ENDDATA
```

## PRINTDATADL (instruction)

**Summary**
- `PRINTDATADL` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Tags**
- io
- data-blocks

**Syntax**
```text
PRINTDATADL [<intVarTerm>]
    ...
ENDDATA
```

- Header line: `PRINTDATADL [<intVarTerm>]`
- Body / terminator structure is the same as `PRINTDATA`.

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
```erabasic
PRINTDATADL CHOICE
    DATA First option
    DATA Second option
ENDDATA
```

## PRINTDATADW (instruction)

**Summary**
- `PRINTDATADW` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Tags**
- io
- data-blocks

**Syntax**
```text
PRINTDATADW [<intVarTerm>]
    ...
ENDDATA
```

- Header line: `PRINTDATADW [<intVarTerm>]`
- Body / terminator structure is the same as `PRINTDATA`.

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
```erabasic
PRINTDATADW CHOICE
    DATA First option
    DATA Second option
ENDDATA
```

## PRINTBUTTON (instruction)

**Summary**
- Appends a clickable button region to the current output.

**Tags**
- io

**Syntax**
- `PRINTBUTTON <text>, <buttonValue>`

**Arguments**
- `<text>` (string): label shown in the output.
- `<buttonValue>` (int or string): value associated with the button.
  - Integer values are accepted by integer button waits (`BINPUT` / `ONEBINPUT`).
  - String values are accepted by string button waits (`BINPUTS` / `ONEBINPUTS`).

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output).
- Uses the current text style for output (and honors `SETCOLOR` color).
- Evaluates `<text>` to a string, then removes any newline characters (`'\n'`) from it.
- If the resulting label is empty, this instruction produces no output segment (no button is created).
- Appends one button region to the pending print buffer:
  - if `<buttonValue>` is an integer, the button’s input value is that integer,
  - if `<buttonValue>` is a string, the button’s input value is that string.
- This instruction does **not** add a newline and does not flush by itself.
- Selectability lifecycle:
  - after the containing output becomes retained, the button can be shown by the normal output model,
  - later button waits only accept buttons in the current active selectable generation,
  - so an older retained button may remain visible but no longer be selectable.
- Output/readback boundary:
  - `GETDISPLAYLINE` later sees only the rendered label text,
  - `HTML_GETPRINTEDSTR` / `HTML_POPPRINTINGSTR` preserve button structure as `<button ...>` markup.

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
- `<raw text>` (optional, raw text; default `""`): the literal remainder of the line; not an expression.

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
- `PRINTPLAINFORM <formString>`

**Arguments**
- `<formString>` (optional, FORM/formatted string; default `""`): scanned by the FORM analyzer (supports `%...%` and `{...}` placeholders).

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
- `charaIndex` (optional, int; default `0`; omission emits a warning): index into the current character list.

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
- `charaIndex` (optional, int; default `0`; omission emits a warning): index into the current character list.

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
- `charaIndex` (optional, int; default `0`; omission emits a warning): index into the current character list.

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
- `charaIndex` (optional, int; default `0`; omission emits a warning): index into the current character list.

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
- `charaIndex` (optional, int; default `0`; omission emits a warning): index into the current character list.

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
- Builds a summary string `s` as follows:
  - Let `count[]` be the integer array `ITEM`.
  - Let `names[]` be the string array `ITEMNAME`.
  - Let `length = min(count.Length, names.Length)`.
  - Start with `s = "所持アイテム："` (the engine's fixed Japanese prefix meaning “owned items:”).
  - For each `i` such that `0 <= i < length`:
    - If `count[i] == 0`: continue.
    - If `names[i] != null`: append `names[i]` (note: unlike some other lists, empty string is not filtered out here).
    - Append: `"(" + count[i] + ") "` (note the trailing space).
  - If no `i` satisfied `count[i] != 0`, append `"なし"` (the engine's fixed Japanese word meaning “none”).
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
- The engine appends the precomputed default draw-line string to the current pending print buffer and then ends the line.
- Pattern source:
  - the base pattern comes from config `DrawLineString` (default `"-"`),
  - the runtime precomputes a width-fitted expanded string from that pattern during initialization.
- Width-fitting rule:
  - repeat the pattern until the measured display width reaches or exceeds the current drawable width,
  - then trim one character at a time from the end until the measured width is less than or equal to the drawable width.
- Rendering:
  - the line text is printed using regular font style regardless of the current font style,
  - the instruction then ends the line and refreshes the display.
- Important boundary behavior:
  - `DRAWLINE` does **not** automatically flush earlier buffered output before appending the line string,
  - so if buffered text already exists, the draw-line string is appended to that same pending line and the combined result is what gets committed when the line is ended.
- Related helpers:
  - `GETLINESTR(pattern)` exposes the same width-fitting algorithm for an arbitrary pattern string,
  - `DRAWLINEFORM` uses the same expansion rule for its runtime string argument.

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
- `value` (int): numerator.
- `maxValue` (int): denominator; must evaluate to `> 0`.
- `length` (int): bar width; must satisfy `1 <= length <= 99`.

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
- `intVarTerm` (changeable integer variable term): target variable; must not be `CONST`.
- `realLiteral` (real-number literal): parsed as `double`; not an expression.

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
- Waits for a confirmation event, then continues.

**Tags**
- io

**Syntax**
- `WAIT`

**Arguments**
- None.

**Semantics**
- Observable visibility rule: by the time the instruction has put the console into its wait state, any pending print-buffer content from the current execution pass has already been materialized to retained normal output, so the current output is visible to the user.
- Then enters an Enter-style confirmation wait. On this host, that wait can be satisfied by Enter and by the same left/right-click UI path used for ordinary `WAIT` continuation.
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
- `<mouse>` (optional, int; default `0`): controls the extra mouse side-channel mode.
  - Clicking a selectable **normal-output button** also submits its value as `INPUT` even when this argument is omitted or `0`.
  - If non-zero, the UI additionally writes the mouse side-channel metadata described below.
  - `0`: accepted integer values on the normal completion path are written to `RESULT`.
- `<canSkip>` (optional, int): presence enables the `MesSkip` fast path; its numeric value is ignored (not evaluated).
- `<extra>` (optional, int): accepted by the argument parser but ignored by the runtime (not read/evaluated).

**Semantics**
- Enters an integer-input UI wait.
- Like other non-primitive value waits, clicking a selectable **normal-output button** can submit one input value on the mouse-click completion path.
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
- Mouse side channels (UI behavior when `<mouse> != 0`):
  - If the instruction requested mouse side-channel mode and the user completes input via a mouse click, the UI also writes metadata into:
    - `RESULT_ARRAY[1]`: mouse button (`1`=left, `2`=right, `3`=middle).
    - `RESULT_ARRAY[2]`: a modifier-key bitfield (Shift=`2^16`, Ctrl=`2^17`, Alt=`2^18`).
    - `RESULTS_ARRAY[1]`: the clicked button’s string (if any).
    - `RESULT_ARRAY[3]`: mapped “button color” (see below).
  - These side channels are only written on the UI click completion path (not on keyboard-only completion, and not in the `MesSkip` no-wait path).

#### Mapped “button color” (`RESULT:3`) from `<img srcm='...'>`

When a click completes input **and** `<mouse> != 0`, the UI computes `RESULT:3` as follows:

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
- `<defaultFormString>` (optional, FORM/formatted string): its evaluated result is used as the default string. If omitted, there is no default.
- `<mouse>` (optional, int; default `0`): controls the extra mouse side-channel mode.
  - Clicking a selectable **normal-output button** also submits its string as `INPUTS` even when this argument is omitted or `0`.
- `<canSkip>` (optional, any): presence enables the `MesSkip` fast path; its value is ignored (not evaluated).

**Semantics**
- Enters a string-input UI wait.
- Like other non-primitive value waits, clicking a selectable **normal-output button** can submit one input string on the mouse-click completion path.
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
- Mouse side channels when `<mouse> != 0`: see `INPUT` (the same UI-side `RESULT_ARRAY[...]` / `RESULTS_ARRAY[...]` behaviors apply).
- Output skipping interaction is the same as `INPUT`.

**Errors & validation**
- Argument parsing errors follow the underlying builder rules for `INPUTS`.
- Argument parsing quirks:
  - After the first comma, the engine parses `<mouse>` as an `int` expression.
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
- `<mouse>` (optional, int; default `0`): controls the extra mouse side-channel mode.
  - Clicking a selectable **normal-output button** also submits its value as `TINPUT` even when this argument is `0` or omitted.
- `<canSkip>` (optional, int): if present, allows `MesSkip` to auto-accept the default without waiting (the value is not evaluated).

**Semantics**
- Enters an integer-input UI wait with a timer of `<timeMs>` milliseconds (a default is always present for timed input).
- Like other non-primitive value waits, clicking a selectable **normal-output button** can submit one input value on the mouse-click completion path.
- See also: `input-flow.md` (shared submission paths, timed completion model, segment draining/discard rules, and `MesSkip` interaction).
- Timeout behavior:
  - When the timer expires, the engine runs the input completion path with an empty input string; this causes the default to be accepted.
  - If `<displayTime> != 0`, the timeout message updates the current “remaining time” line.
  - If `<displayTime> == 0`, the timeout message is printed as a single line.
- `MesSkip` integration:
  - If `<canSkip>` is present and `MesSkip` is currently true, the engine does not wait and instead accepts the default immediately.
  - In that no-wait path, the engine assigns the default to:
    - `RESULT` if `<mouse> == 0`
    - `RESULT_ARRAY[1]` if `<mouse> != 0`
  - In that no-wait path, the input string is not echoed (because the UI wait is skipped entirely).
- Mouse side channels when `<mouse> != 0`: see `INPUT` (the same UI-side `RESULT_ARRAY[...]` / `RESULTS_ARRAY[...]` behaviors apply).
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
- `<mouse>` (optional, int; default `0`): controls the extra mouse side-channel mode.
  - Clicking a selectable **normal-output button** also submits its string as `TINPUTS` even when this argument is `0` or omitted.
- `<canSkip>` (optional, int): if present, allows `MesSkip` to auto-accept the default without waiting (the value is not evaluated).

**Semantics**
- Same model as `TINPUT`, but stores into `RESULTS` (string) rather than `RESULT` (int).
- Like other non-primitive value waits, clicking a selectable **normal-output button** can submit one input string on the mouse-click completion path.
- See also: `input-flow.md` (shared submission paths, timed completion model, segment draining/discard rules, and `MesSkip` interaction).
- `MesSkip` integration:
  - If `<canSkip>` is present and `MesSkip` is currently true, the engine does not wait and instead accepts the default immediately.
  - In that no-wait path, the engine assigns the default to:
    - `RESULTS` if `<mouse> == 0`
    - `RESULTS_ARRAY[1]` if `<mouse> != 0`
  - In that no-wait path, the input string is not echoed (because the UI wait is skipped entirely).
- Mouse side channels when `<mouse> != 0`: see `INPUT` (the same UI-side `RESULT_ARRAY[...]` / `RESULTS_ARRAY[...]` behaviors apply).

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
- Same as `TINPUT`, but with “one input” mode enabled.
- The same ordinary normal-output-button click path still exists here: clicking a selectable **normal-output button** can submit one value even when the extra mouse side-channel mode was not requested.
- When `<mouse> != 0`, the same extra mouse side channels as `TINPUT` / `INPUT` are also written.
- Exact one-input rule:
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
- Same as `TINPUTS`, but with “one input” mode enabled.
- The same ordinary normal-output-button click path still exists here: clicking a selectable **normal-output button** can submit one string even when the extra mouse side-channel mode was not requested.
- When `<mouse> != 0`, the same extra mouse side channels as `TINPUTS` / `INPUTS` are also written.
- Exact one-input rule:
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
- Observable visibility rule: by the time the instruction has put the console into its timed wait state, any pending print-buffer content from the current execution pass has already been materialized to retained normal output, so the current output is visible to the user.
- See also: `input-flow.md` (shared wait-state lifecycle, timed completion model, and `MesSkip` auto-advance behavior).
- If `<mode> == 0`: enters the same Enter/click confirmation wait surface as `WAIT`, but with a time limit.
- If `<mode> != 0`: enters a no-input timed wait. Ordinary textbox/button submission does not satisfy it; execution continues only when the time limit expires or when skip/macro-driven continuation bypasses the wait under the shared non-value-wait rules.
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
- Observable visibility rule: by the time the instruction has put the console into its wait state, any pending print-buffer content from the current execution pass has already been materialized to retained normal output, so the current output is visible to the user.
- Then enters an any-key confirmation wait. On this host, mouse left/right click can also satisfy that wait through the same UI continuation path.
- See also: `input-flow.md` (shared wait-state lifecycle and `MesSkip` auto-advance model).
- Does not assign `RESULT`/`RESULTS`.
- Skipped when output skipping is active (via `SKIPDISP`).

**Errors & validation**
- None.

**Examples**
- `WAITANYKEY`

## FORCEWAIT (instruction)

**Summary**
- Like `WAIT`, but stops `MesSkip` from auto-advancing past the wait.

**Tags**
- io

**Syntax**
- `FORCEWAIT`

**Arguments**
- None.

**Semantics**
- Observable visibility rule: by the time the instruction has put the console into its wait state, any pending print-buffer content from the current execution pass has already been materialized to retained normal output, so the current output is visible to the user.
- Then waits for Enter/click, and stops `MesSkip` from auto-advancing past the wait.
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
- Like `INPUT`, but sets `OneInput = true` on the input request.
- The same ordinary normal-output-button click path still exists here: clicking a selectable **normal-output button** can submit one value even when the extra mouse side-channel mode was not requested.
- When `<mouse> != 0`, the same extra mouse side channels as `INPUT` are also written.
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
- Like `INPUTS`, but with “one input” mode enabled.
- The same ordinary normal-output-button click path still exists here: clicking a selectable **normal-output button** can submit one string even when the extra mouse side-channel mode was not requested.
- When `<mouse> != 0`, the same extra mouse side channels as `INPUTS` are also written.
- Exact one-input rule:
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
- Deletes the last *N logical output lines* from the current visible normal output area.

**Tags**
- io

**Syntax**
- `CLEARLINE <n>`

**Arguments**
- `<n>` (int): number of logical output lines to delete.
  - The evaluated value is converted to a 32-bit signed integer by truncation (low 32 bits interpreted as signed).

**Semantics**
- Evaluates `<n>` and deletes the last `n` logical lines from the current visible normal output area.
- The deletion count is in **logical lines**, not visible display rows:
  - one logical line can occupy multiple visible display rows,
  - deleting one logical line removes all of its visible rows.
- If the current trailing visible line is temporary and it falls within the deleted suffix, it is deleted like any other currently visible logical line.
- If `n <= 0`, nothing is deleted.
- Layer boundary:
  - this affects only the current visible normal output area,
  - it does not clear or flush the pending print buffer,
  - it does not affect the separate `HTML_PRINT_ISLAND` layer.
- After deleting, the display is refreshed.

**Errors & validation**
- No explicit validation in the instruction.
- No error is raised for negative or overflowed values after the 32-bit conversion.

**Examples**
- `CLEARLINE 1`
- `CLEARLINE 10`

## REUSELASTLINE (instruction)

**Summary**
- Prints a **temporary single line** that is overwritten by the next later visible normal line append.

**Tags**
- io

**Syntax**
- `REUSELASTLINE`
- `REUSELASTLINE <formString>`

**Arguments**
- `<formString>` (optional, FORM/formatted string): parsed like `PRINTFORM*` and used as the temporary line’s content.

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output).
- If ordinary buffered output is currently pending, that buffered content is flushed first as normal visible output.
- Evaluates `<formString>` to a string and, if the result is non-empty, appends it as a **temporary visible line**.
- Temporary-line behavior:
  - while it remains visible, it occupies a normal visible logical-line slot,
  - the next operation that appends a new normal visible display line removes the trailing temporary line first,
  - repeated `REUSELASTLINE` calls therefore replace one another instead of accumulating.
- If the resulting string is empty, this instruction prints nothing.
  - In that empty-result case, it does not clear or replace an already-visible temporary line.

**Errors & validation**
- None.

**Examples**
```erabasic
REUSELASTLINE "Now loading..."
REUSELASTLINE %TIME%
```

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
- `charaIndex` (optional, int; default `0`; omission emits a warning): the character index to apply changes to.

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
- Each `charaNo` (int): selects a character template.

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
- Each `charaNo` (int): selects a character template.

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
- Each `charaIndex` (int): selects an existing character index.

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
- `<formString>` (optional, FORM/formatted string): its evaluated result is appended to the save-description buffer.

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
- `<keyword>` (raw string): the entire remainder of the source line after the instruction delimiter.
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
- `<slot>` (optional, int; default `0`; omission emits a warning): save slot index. Must be in `[0, 2147483647]` (32-bit signed non-negative).

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
- `DELDATA [<slot>]`

**Arguments**
- `<slot>` (optional, int; default `0`; omission emits a warning): save slot index. Must be in `[0, 2147483647]` (32-bit signed non-negative).

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
- `SIF [<condition>]`
  - `<next logical line>`

**Arguments**
- `<condition>` (optional, int; default `0`; omission emits a warning): condition (`0` = false, non-zero = true).

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
```text
IF [<condition>]
    ...
[ELSEIF <condition>
    ...]
[ELSE
    ...]
ENDIF
```

- Header line: `IF [<condition>]`
- Clause header lines inside the block may include `ELSEIF <condition>` and `ELSE`.
- Terminator line: `ENDIF`

**Arguments**
- `<condition>` (optional, int; default `0`; omission emits a warning): condition (`0` = false, non-zero = true).

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
```erabasic
IF FLAG
    PRINTL "yes"
ELSE
    PRINTL "no"
ENDIF
```

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
- `ELSEIF <condition>`

**Arguments**
- `<condition>` (int): evaluated by the surrounding `IF` header’s clause-selection logic, not by standalone `ELSEIF` execution.

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
```text
SELECTCASE <expr>
    CASE <caseExpr> [, <caseExpr> ...]
        ...
    ...
    [CASEELSE
        ...]
ENDSELECT
```

- Header line: `SELECTCASE <expr>`
- Clause header lines inside the block are `CASE <caseExpr> [, <caseExpr> ...]`; an optional final `CASEELSE` may appear.
- Terminator line: `ENDSELECT`

**Arguments**
- `<expr>` (int|string): selector expression.

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
```erabasic
SELECTCASE A
CASE 0
    PRINTL "zero"
CASE 1 TO 9
    PRINTL "small"
CASEELSE
    PRINTL "other"
ENDSELECT
```

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
```text
REPEAT [<countExpr>]
    ...
REND
```

- Header line: `REPEAT [<countExpr>]`
- Terminator line: `REND`

**Arguments**
- `<countExpr>` (optional, int; default `0`; omission emits a warning): number of iterations.

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
- If the system variable `COUNT` is forbidden by the current variable-scope configuration, `REPEAT` raises an error when execution reaches the `REPEAT` line and its argument is parsed.
- If a constant count is `<= 0`, the engine emits a warning when the line’s argument is parsed.
- Nested `REPEAT` is warned about by the loader (not necessarily a hard error).

**Examples**
```erabasic
REPEAT 10
    PRINTV COUNT
REND
```

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
```erabasic
REPEAT 10
    PRINTV COUNT
REND
```

## FOR (instruction)

**Summary**
- Begins a `FOR ... NEXT` counted loop over a mutable integer variable term.

**Tags**
- control-flow

**Syntax**
```text
FOR <intVarTerm>, [<start>], <end> [, <step>]
    ...
NEXT
```

- Header line: `FOR <intVarTerm>, [<start>], <end> [, <step>]`
- Terminator line: `NEXT`

**Arguments**
- `<intVarTerm>` (changeable integer variable term): loop counter; must not be character-data.
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
```erabasic
FOR I, 0, 10
    PRINTV I
NEXT
```

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
```erabasic
FOR I, 0, 10
    PRINTV I
NEXT
```

## WHILE (instruction)

**Summary**
- Begins a `WHILE ... WEND` loop.

**Tags**
- control-flow

**Syntax**
```text
WHILE [<condition>]
    ...
WEND
```

- Header line: `WHILE [<condition>]`
- Terminator line: `WEND`

**Arguments**
- `<condition>` (optional, int; default `0`; omission emits a warning): loop condition (`0` = false, non-zero = true).

**Semantics**
- At `WHILE`, evaluates the condition:
  - If true, enters the body (next line).
  - If false, jumps to the matching `WEND` marker (exiting the loop).
- At `WEND`, the engine re-evaluates the `WHILE` condition and loops again if it is still true.

**Errors & validation**
- `WEND` without a matching open `WHILE` is a load-time error (the `WEND` line is marked as error).

**Examples**
```erabasic
WHILE I < 10
    I += 1
WEND
```

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
```erabasic
WHILE I < 10
    I += 1
WEND
```

## DO (instruction)

**Summary**
- Begins a `DO ... LOOP` loop.

**Tags**
- control-flow

**Syntax**
```text
DO
    ...
LOOP <condition>
```

- Header line: `DO`
- Terminator line: `LOOP <condition>`

**Arguments**
- None.

**Semantics**
- Marker-only instruction (no runtime effect).
- The loader links the `DO` marker with its matching `LOOP` condition line.

**Errors & validation**
- `LOOP` without a matching open `DO` is a load-time error (the `LOOP` line is marked as error).

**Examples**
```erabasic
DO
    I += 1
LOOP I < 10
```

## LOOP (instruction)

**Summary**
- Ends a `DO ... LOOP` loop and provides the loop condition.

**Tags**
- control-flow

**Syntax**
- `LOOP [<condition>]`

**Arguments**
- `<condition>` (optional, int; default `0`; omission emits a warning): loop condition (`0` = false, non-zero = true).

**Semantics**
- Evaluates the condition:
  - If true, jumps back to the matching `DO` marker (and continues at the first body line).
  - If false, falls through to the next line after `LOOP`.

**Errors & validation**
- `LOOP` without a matching open `DO` is a load-time error (the line is marked as error).

**Examples**
```erabasic
DO
    I += 1
LOOP I < 10
```

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
- `RETURN <value1> [, <value2>, <value3>, ... ]`

**Arguments**
- `<valueN>` (optional, int): each occurrence is stored into `RESULT:<index>`.

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
- `<expr>` (optional, expression): its value should match the function’s declared return type.

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
- `<rawString>` (optional, default `""`): literal remainder of the line (not a normal string).

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
- `<formString>` (optional, FORM/formatted string; default `""`): its evaluated result is measured; supports `%...%` and `{...}`.

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
- `<rawString>` (optional, default `""`): literal remainder of the line (not a normal string).

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
- `<formString>` (optional, FORM/formatted string; default `""`): its evaluated result is measured.

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
- Each `charaIndex` (int): selects an existing character index to copy from.

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
- `<outParts>` (changeable string array variable term): receives the parts.
  - Must be a **string** array variable (1D/2D/3D; character-data arrays are accepted but behave specially).
  - Any indices written in `<outParts>` are ignored for this instruction.
- `<outCount>` (optional, changeable integer variable term; default `RESULT`): receives the number of split parts.

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
  - Validates that each component is within `0 <= component <= 255`.
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
- `<spriteName>` (FORM/formatted string): its evaluated result names a sprite.
  - Sprite lookup is case-insensitive (the engine uppercases before lookup).
  - Only file-backed sprites loaded from `resources/**/*.csv` are accepted; other sprite kinds are ignored.
- `<depth>` (optional, FORM/formatted string; default `0`): its evaluated result is parsed by `Int64.Parse`.
- `<opacityByte>` (optional, FORM/formatted string; default `255`): its evaluated result is parsed by `Int64.Parse`, then converted to opacity as `value / 255.0`.
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
- `<spriteName>` (FORM/formatted string): its evaluated result selects the sprite name to remove.
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
- Reorders the engine’s character list (`0 <= i < CHARANUM`) by a key taken from a character-data variable.
- Observable behavior: keeps `MASTER` fixed at its numeric position for this instruction.

**Tags**
- characters

**Syntax**
- `SORTCHARA`
- `SORTCHARA <charaVarTerm> [ , FORWARD | BACK ]`
- `SORTCHARA FORWARD | BACK`

**Arguments**
- `<charaVarTerm>` (optional, character-data variable term; default `NO`): sort key.
- `FORWARD | BACK` (optional, keyword; default `FORWARD`): sort order.
- If the key variable is an array, the element indices are taken from the variable term’s subscripts after the character selector.
  - Any written chara selector in `<charaVarTerm>` is ignored and not evaluated (the sort always scans `0 <= i < CHARANUM`).

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
- `<pattern>` (string): pattern to repeat.

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
- `<fontName>` (optional, string; default `""`): font face name.

**Semantics**
- Non-empty `<fontName>` sets the current font face name.
- Empty `<fontName>` resets it to the configured default font.

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
- `<var1>` (changeable variable term): first swap target; must not be `CONST`.
- `<var2>` (changeable variable term): second swap target; must have the same type as `<var1>`.

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
- `<seed>` (optional, int; default `0`): seed value.

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
  - Layout: elements `0` through `623` receive the 624 state words; element `624` receives the current index.
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
  - Layout: elements `0` through `623` are the 624 state words; element `624` is the current index.
  - On load, elements `0` through `623` are interpreted as unsigned 32-bit values.
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- Runtime error if `RANDDATA` does not have length `625`.

**Examples**
- `INITRAND`

## REDRAW (instruction)

**Summary**
- Controls automatic repaint scheduling for the output window and can optionally force an immediate repaint.

**Tags**
- ui

**Syntax**
- `REDRAW <flags>`

**Arguments**
- `<flags>` (int): redraw flags.
  - Bit `0`:
    - `0`: disable non-forced automatic redraw (`Redraw = None`)
    - `1`: enable normal redraw (`Redraw = Normal`)
  - Bit `1`:
    - if set, forces an immediate repaint once.
  - Other bits are ignored.

**Semantics**
- Updates the console redraw mode according to bit `0`.
- If bit `1` is set, immediately repaints the current stored output state once.
- This instruction affects **paint timing**, not stored output state:
  - pending buffered output, retained normal output, and the retained HTML-island layer are not erased or rebuilt by changing redraw mode,
  - getters such as `GETDISPLAYLINE` / `HTML_GETPRINTEDSTR` still read the current stored state even if redraw is off.
- With redraw disabled:
  - non-forced repaint work is suppressed while the window is at the live bottom,
  - forced repaints still show the current stored state,
  - backlog-mode repainting is still allowed.
- The repaint applies to the whole output surface, including both the normal output area and the retained HTML-island layer.

**Errors & validation**
- None.

**Examples**
- `REDRAW 0` (stop non-forced automatic redraw)
- `REDRAW 3` (enable redraw and force an immediate repaint)

## CALLTRAIN (instruction)

**Summary**
- Enables “continuous train command execution” using the commands pre-populated in `SELECTCOM`.

**Tags**
- system

**Syntax**
- `CALLTRAIN <count>`

**Arguments**
- `<count>` (int): number of commands to take from `SELECTCOM`.

**Semantics**
- Reads the current `SELECTCOM` array and enqueues `SELECTCOM[1]` through `SELECTCOM[count]` (inclusive) as a command list.
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
- `<trainIndex>` (int): index into `TRAINNAME` (from `train.csv`).

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
- `DATA`
- `DATA <raw text>`
- `DATA;<raw text>`

**Arguments**
- `<raw text>` (optional, raw text; default `""`): not an expression.
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
- `DATAFORM [<formString>]`

**Arguments**
- `<formString>` (optional, FORM/formatted string; default `""`): scanned to end-of-line.

**Semantics**
- Stored into the surrounding `PRINTDATA*` / `STRDATA` / `DATALIST` data list at load time.
- When selected, evaluated to a string at runtime and printed/concatenated.
  - The FORM string is scanned at load time and stored as an expression that is evaluated later, so runtime variables inside it are read when the entry is selected.

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
```text
DATALIST
    DATA <raw text> | DATAFORM <formString>
    ...
ENDLIST
```

- Header line: `DATALIST`
- Item lines: `DATA <raw text>` / `DATAFORM <formString>`
- Terminator line: `ENDLIST`

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
```text
STRDATA [<strVarTerm>]
    DATA <raw text> | DATAFORM <formString>
    ...
    [DATALIST
        DATA <raw text> | DATAFORM <formString>
        ...
    ENDLIST]
ENDDATA
```

- Header line: `STRDATA [<strVarTerm>]`
- Body / terminator structure is the same as `PRINTDATA`.

**Arguments**
- `<strVarTerm>` (optional, changeable string variable term; default `RESULTS`): receives the result.

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
- Sets one or more bits in a writable integer variable.

**Tags**
- math

**Syntax**
- `SETBIT <integerVariable>, <bit1> [, <bit2> ... ]`

**Arguments**
- `<integerVariable>` (writable int variable): target variable.
- `<bitN>` (int): bit position; each value must satisfy `0 <= bit <= 63`.

**Semantics**
- Evaluates the bit arguments left-to-right.
- For each evaluated bit `b`, immediately updates `<integerVariable>` with `value |= (1 << b)`.
- The variable is reread before each step, so later bit expressions observe earlier mutations if they read the same variable.
- Duplicate bit positions are allowed; the same bit may be processed more than once in one call.

**Errors & validation**
- Parse / argument-validation error if `<integerVariable>` is missing, is not a writable int variable, or no bit argument is supplied.
- Parse / argument-validation error if a constant `<bitN>` is outside `0 <= bit <= 63`.
- Runtime error if an evaluated `<bitN>` is outside `0 <= bit <= 63`.
- If a later bit errors at runtime, earlier bit changes remain.

**Examples**
- `SETBIT FLAG, 0`
- `SETBIT FLAGS, 1, 3, 5`

## CLEARBIT (instruction)

**Summary**
- Clears one or more bits in a writable integer variable.

**Tags**
- math

**Syntax**
- `CLEARBIT <integerVariable>, <bit1> [, <bit2> ... ]`

**Arguments**
- `<integerVariable>` (writable int variable): target variable.
- `<bitN>` (int): bit position; each value must satisfy `0 <= bit <= 63`.

**Semantics**
- Evaluates the bit arguments left-to-right.
- For each evaluated bit `b`, immediately updates `<integerVariable>` with `value &= ~(1 << b)`.
- The variable is reread before each step, so later bit expressions observe earlier mutations if they read the same variable.
- Duplicate bit positions are allowed; the same bit may be processed more than once in one call.

**Errors & validation**
- Parse / argument-validation error if `<integerVariable>` is missing, is not a writable int variable, or no bit argument is supplied.
- Parse / argument-validation error if a constant `<bitN>` is outside `0 <= bit <= 63`.
- Runtime error if an evaluated `<bitN>` is outside `0 <= bit <= 63`.
- If a later bit errors at runtime, earlier bit changes remain.

**Examples**
- `CLEARBIT FLAG, 0`
- `CLEARBIT FLAGS, 1, 3, 5`

## INVERTBIT (instruction)

**Summary**
- Toggles one or more bits in a writable integer variable.

**Tags**
- math

**Syntax**
- `INVERTBIT <integerVariable>, <bit1> [, <bit2> ... ]`

**Arguments**
- `<integerVariable>` (writable int variable): target variable.
- `<bitN>` (int): bit position; each value must satisfy `0 <= bit <= 63`.

**Semantics**
- Evaluates the bit arguments left-to-right.
- For each evaluated bit `b`, immediately updates `<integerVariable>` with `value ^= (1 << b)`.
- The variable is reread before each step, so later bit expressions observe earlier mutations if they read the same variable.
- Duplicate bit positions are allowed; the same bit may be processed more than once in one call.

**Errors & validation**
- Parse / argument-validation error if `<integerVariable>` is missing, is not a writable int variable, or no bit argument is supplied.
- Parse / argument-validation error if a constant `<bitN>` is outside `0 <= bit <= 63`.
- Runtime error if an evaluated `<bitN>` is outside `0 <= bit <= 63`.
- If a later bit errors at runtime, earlier bit changes remain.

**Examples**
- `INVERTBIT FLAG, 0`
- `INVERTBIT FLAGS, 1, 3, 5`

## DELALLCHARA (instruction)

**Summary**
- Deletes every currently registered character.

**Tags**
- characters

**Syntax**
- `DELALLCHARA`

**Arguments**
- None.

**Semantics**
- Removes all characters from the current character list.
- After completion, `CHARANUM` becomes `0`.
- The instruction is safe when the list is already empty.
- It does **not** automatically rewrite `MASTER`, `TARGET`, or `ASSI`; scripts that rely on those variables must reset or re-check them afterward.

**Errors & validation**
- None.

**Examples**
- `DELALLCHARA`

## PICKUPCHARA (instruction)

**Summary**
- Keeps only the selected registered characters, reorders them to match the selection order, and deletes the rest.

**Tags**
- characters

**Syntax**
- `PICKUPCHARA <charaID> [, <charaID> ... ]`

**Arguments**
- `<charaID>` (int): selects a currently registered character index.

**Semantics**
- Evaluates all arguments left-to-right.
- For ordinary expressions, each value must be a valid current character index.
- If an argument is the variable `MASTER`, `TARGET`, or `ASSI`, a negative value is ignored instead of rejected.
- After evaluation, the engine removes duplicate non-negative selections while preserving first-appearance order.
- The selected characters are moved to the front of the character list in that deduplicated order, and all remaining characters are deleted.
- `MASTER`, `TARGET`, and `ASSI` are then rebound to the new indices of their old characters if those characters survived; otherwise they become `-1`.

**Errors & validation**
- Parse / argument-validation error if no argument is supplied.
- Runtime error if an ordinary argument is outside the current character range.
- `MASTER`, `TARGET`, and `ASSI` participate with their current numeric values. Their negative case is ignored; other invalid values are not guaranteed to succeed.

**Examples**
- `PICKUPCHARA MASTER, TARGET`
- `PICKUPCHARA 3, 1, 3`

## VARSET (instruction)

**Summary**
- Fills a writable variable block with one repeated value.

**Tags**
- variables

**Syntax**
- `VARSET <variableName>`
- `VARSET <variableName>, <value>`
- `VARSET <variableName>, <value>, <startIndex>, <endIndex>`

**Arguments**
- `<variableName>` (writable variable): target storage block.
  - The target may name a whole array/block or a character-data target with explicit or implicit character selection.
- `<value>` (optional; default `0` / `""`): replacement value.
  - Omission uses `0` for int targets and `""` for string targets.
- `<startIndex>` / `<endIndex>` (optional, int): range bounds for 1D fill targets.
  - For 1D targets, omission means `startIndex = 0` and `endIndex = length`.
  - `endIndex` is exclusive, so `VARSET A, 7, 2, 5` fills `A:2`, `A:3`, and `A:4`.

**Semantics**
- `VARSET` fills the storage block designated by `<variableName>`.
- For 1D targets, it fills the half-open range `[startIndex, endIndex)`.
- If `startIndex > endIndex`, the engine swaps them before filling.
- For targets whose remaining payload is not a 1D block, the whole addressed block is filled and the range arguments are not used.
- If `<variableName>` is character-data and omits the character selector, the usual implicit-target rules still apply. For example, `VARSET CSTR, ""` affects only the current implicit target character.

**Errors & validation**
- Parse / argument-validation error if `<variableName>` is missing, is not a writable variable, is const, or `<value>` has the wrong type.
- Runtime error if a 1D range bound is outside `0 <= index <= length`.

**Examples**
- `VARSET FLAG, 0`
- `VARSET STR, "あああ", 0, 10`
- `VARSET CFLAG:MASTER:0, 0`

## CVARSET (instruction)

**Summary**
- Fills one character-variable element across a range of registered characters.

**Tags**
- variables

**Syntax**
- `CVARSET <characterVariable>`
- `CVARSET <characterVariable>, <index>, <value>`
- `CVARSET <characterVariable>, <index>, <value>, <startID>, <endID>`

**Arguments**
- `<characterVariable>` (writable character-data variable): target variable.
  - 2D character-data variables are not accepted.
- `<index>` (optional; default `0`): element selector used when `<characterVariable>` has a per-character 1D payload.
  - May be an int index or a string key accepted by that variable.
  - If the target has no such 1D payload, this argument is ignored.
- `<value>` (optional; default `0` / `""`): replacement value.
  - Omission uses `0` for int targets and `""` for string targets.
- `<startID>` / `<endID>` (optional, int): registered-character range.
  - Omission means `startID = 0` and `endID = CHARANUM`.
  - `endID` is exclusive, so `CVARSET CFLAG, 10, 123, 1, 4` affects character indices `1`, `2`, and `3`.

**Semantics**
- Applies the assignment to each registered character index in the half-open range `[startID, endID)`.
- If `startID > endID`, the engine swaps them before filling.
- If `<characterVariable>` has a 1D per-character payload, `<index>` selects which element is written for each character.
- If `<characterVariable>` does not have a 1D per-character payload, `<index>` does not change which field is written.
- If `CHARANUM == 0`, the instruction has no effect.

**Errors & validation**
- Parse / argument-validation error if `<characterVariable>` is missing, is not a writable character-data variable, is 2D character-data, or `<value>` has the wrong type.
- Runtime error if `startID` or `endID` is outside `0 <= id <= CHARANUM`.
- Runtime error if a string `<index>` does not name a defined key for that variable.

**Examples**
- `CVARSET CFLAG, 10, 123`
- `CVARSET CSTR, 0, "", 0, CHARANUM`

## RESET_STAIN (instruction)

**Summary**
- Resets one character’s `STAIN` array to the engine’s configured default stain table.

**Tags**
- characters

**Syntax**
- `RESET_STAIN <charaID>`

**Arguments**
- `<charaID>` (int): selects an existing registered character.

**Semantics**
- Replaces the target character’s entire `STAIN` array with the configured default stain values.
- The default table is the same one used for newly initialized stain state (including `_Replace.csv`-driven defaults when enabled; see `config-items.md`).
- If the target `STAIN` array is longer than the configured default table, the remaining tail elements are set to `0`.
- If the target `STAIN` array is shorter than the configured default table, only the leading portion that fits is copied.

**Errors & validation**
- Runtime error if `<charaID>` is outside the current registered-character range.

**Examples**
- `RESET_STAIN TARGET`

## FORCEKANA (instruction)

**Summary**
- Sets the kana-conversion mode used by output operations that explicitly request kana conversion.

**Tags**
- text

**Syntax**
- `FORCEKANA <mode>`

**Arguments**
- `<mode>` (int): conversion mode.
  - `0`: no conversion
  - `1`: hiragana -> katakana
  - `2`: full-width katakana -> hiragana
  - `3`: katakana -> hiragana, and half-width katakana are widened first

**Semantics**
- Updates the persistent kana-conversion state used by print paths that request kana conversion (the `...K` / `K` output family; see the relevant print built-ins and `output-flow.md`).
- The mode remains in effect until another `FORCEKANA` changes it.
- It does not retroactively modify text that has already been buffered or printed.

**Errors & validation**
- Runtime error if `<mode>` is outside `0 <= mode <= 3`.

**Examples**
- `FORCEKANA 1`
- `FORCEKANA 0`

## SKIPDISP (instruction)

**Summary**
- Enables/disables the engine’s “skip output” mode, which causes most print/wait/input built-ins to be skipped.
- Also sets `RESULT` to indicate whether skip mode is currently enabled.

**Tags**
- skip-mode

**Syntax**
- `SKIPDISP <enabled>`

**Arguments**
- `<enabled>` (int): `0` disables skip mode; non-zero enables skip mode.

**Semantics**
- Evaluates `<enabled>` to `v`.
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
```text
NOSKIP
    ...
ENDNOSKIP
```

- Header line: `NOSKIP`
- Terminator line: `ENDNOSKIP`

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
- `<arrayVar>` (changeable 1D array variable term): target array.
- `<shift>` (int): shift offset (can be negative). `0` is a no-op.
- `<default>` (same scalar type as the array element type): fill value for newly exposed slots.
- `<start>` (optional, int; default `0`): start index of the shifted segment.
- `<count>` (optional, int; default remaining length to array end): number of elements in the segment. If explicitly `0`, this is a no-op.

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
- `<arrayVar>` (changeable 1D array variable term): target array.
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
    - string arrays: `null` internally; ordinary script-side reads observe this as `""`.
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
- `<arrayVar>` (changeable 1D array variable term): target array; must be int or string.
- `FORWARD|BACK` (optional; default `FORWARD`):
  - `FORWARD`: ascending
  - `BACK`: descending
- `<start>` (optional, int; default `0`): subrange start index (only parsed when `FORWARD|BACK` is present).
- `<count>` (optional, int; default remaining length to array end): subrange length (only parsed when `FORWARD|BACK` is present). If explicitly `0`, this is a no-op.

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
- `<srcVarNameExpr>` (string): its value names the source array variable.
- `<dstVarNameExpr>` (string): its value names the destination array variable.

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
- `SKIPLOG <enabled>`

**Arguments**
- `<enabled>` (int): `0` clears message-skip; non-zero enables message-skip.

**Semantics**
- Evaluates `<enabled>` to `v`.
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
- `JUMP <functionName>`
- `JUMP <functionName>()`
- `JUMP <functionName>, <arg1> [, <arg2> ... ]`
- `JUMP <functionName>(<arg1> [, <arg2> ... ])`
- `JUMP <functionName>[<subName1>, <subName2>, ...]`
- `JUMP <functionName>[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`
- The bracket segment is accepted for compatibility, but is currently unused.

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
- `CALL <functionName>`
- `CALL <functionName>()`
- `CALL <functionName>, <arg1> [, <arg2> ... ]`
- `CALL <functionName>(<arg1> [, <arg2> ... ])`
- `CALL <functionName>[<subName1>, <subName2>, ...]`
- `CALL <functionName>[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`
- The bracket segment is accepted for compatibility, but is currently unused.

**Arguments**
- `<functionName>` (raw string token): read up to `(` / `[` / `,` / `;` and then trimmed.
  - This is **not** a string literal. Quotes are treated as ordinary characters.
  - Backslash escapes are processed (e.g. `\n`, `\t`, `\s`).
- `<argN>` (optional, expression): each occurrence is evaluated, passed to the callee, and bound to its `ARG`/`ARGS`-based parameters and/or `#FUNCTION` parameter declarations.
- `<subNameN>` (optional): values parsed from the bracket segment after `<functionName>`.
  - The current engine accepts and stores them, but they do not affect target resolution or call behavior.

**Semantics**
- Resolves the target label to a non-event function.
  - If `CompatiCallEvent` is enabled, an event function name is also callable via `CALL` (compatibility behavior: it calls only the first-defined function, ignoring event priority/single flags).
- Evaluates arguments, binds them to the callee’s declared formals (including `REF` behavior), then enters the callee.
- When the callee executes `RETURN` (or reaches end-of-function), control returns to the statement after the `CALL`.
- Load-time behavior: if `<functionName>` is a compile-time constant, the loader resolves the callee during load and may emit early diagnostics (e.g. unknown function, argument binding issues).

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
- `TRYJUMP <functionName>`
- `TRYJUMP <functionName>()`
- `TRYJUMP <functionName>, <arg1> [, <arg2> ... ]`
- `TRYJUMP <functionName>(<arg1> [, <arg2> ... ])`
- `TRYJUMP <functionName>[<subName1>, <subName2>, ...]`
- `TRYJUMP <functionName>[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`
- The bracket segment is accepted for compatibility, but is currently unused.

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
- `TRYCALL <functionName>`
- `TRYCALL <functionName>()`
- `TRYCALL <functionName>, <arg1> [, <arg2> ... ]`
- `TRYCALL <functionName>(<arg1> [, <arg2> ... ])`
- `TRYCALL <functionName>[<subName1>, <subName2>, ...]`
- `TRYCALL <functionName>[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`
- The bracket segment is accepted for compatibility, but is currently unused.

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
- `JUMPFORM <formString>`
- `JUMPFORM <formString>()`
- `JUMPFORM <formString>, <arg1> [, <arg2> ... ]`
- `JUMPFORM <formString>(<arg1> [, <arg2> ... ])`
- `JUMPFORM <formString>[<subName1>, <subName2>, ...]`
- `JUMPFORM <formString>[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`
- The bracket segment is accepted for compatibility, but is currently unused.

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
- `CALLFORM <formString>`
- `CALLFORM <formString>()`
- `CALLFORM <formString>, <arg1> [, <arg2> ... ]`
- `CALLFORM <formString>(<arg1> [, <arg2> ... ])`
- `CALLFORM <formString>[<subName1>, <subName2>, ...]`
- `CALLFORM <formString>[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`
- The bracket segment is accepted for compatibility, but is currently unused.

**Arguments**
- `<formString>` (FORM/formatted string): its evaluated result is used as the function name.
  - If this FORM expression constant-folds to a constant string, the engine treats it like `CALL` for load-time resolution.
- `<argN>` (optional, expression): each occurrence is evaluated and passed like `CALL`.
- `<subNameN>` (optional): values parsed from the bracket segment after `<formString>`.
  - The current engine accepts and stores them, but they do not affect target resolution or call behavior.

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
- `TRYJUMPFORM <formString>`
- `TRYJUMPFORM <formString>()`
- `TRYJUMPFORM <formString>, <arg1> [, <arg2> ... ]`
- `TRYJUMPFORM <formString>(<arg1> [, <arg2> ... ])`
- `TRYJUMPFORM <formString>[<subName1>, <subName2>, ...]`
- `TRYJUMPFORM <formString>[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`
- The bracket segment is accepted for compatibility, but is currently unused.

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
- `TRYCALLFORM <formString>`
- `TRYCALLFORM <formString>()`
- `TRYCALLFORM <formString>, <arg1> [, <arg2> ... ]`
- `TRYCALLFORM <formString>(<arg1> [, <arg2> ... ])`
- `TRYCALLFORM <formString>[<subName1>, <subName2>, ...]`
- `TRYCALLFORM <formString>[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`
- The bracket segment is accepted for compatibility, but is currently unused.

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
```text
TRYCJUMP <target>
CATCH
    <catch body>
ENDCATCH
```

- `<target>` can be:
  - `functionName`
  - `functionName()`
  - `functionName, <arg1> [, <arg2> ... ]`
  - `functionName(<arg1> [, <arg2> ... ])`
  - `functionName[<subName1>, <subName2>, ...]`
  - `functionName[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`

> **Note:** The bracketed `[...]` segment is accepted for backward compatibility, but is currently unused.

**Arguments**
- Same as `JUMP`.

**Semantics**
- If the target function exists: behaves like `JUMP` (tail-call-like); the current function is discarded, so it does not return to reach `CATCH`.
- If the function does not exist: jumps to the `CATCH` marker (entering the catch body).

**Errors & validation**
- Still errors for invalid argument binding/type conversion when a function is found.

**Examples**
```erabasic
TRYCJUMP OPTIONAL_PHASE
CATCH
    PRINTL "phase missing"
ENDCATCH
```

## TRYCCALL (instruction)

**Summary**
- Like `TRYCALL`, but supports a `CATCH ... ENDCATCH` block for the “not found” case.

**Tags**
- calls

**Syntax**
```text
TRYCCALL <target>
CATCH
    <catch body>
ENDCATCH
```

- `<target>` can be:
  - `functionName`
  - `functionName()`
  - `functionName, <arg1> [, <arg2> ... ]`
  - `functionName(<arg1> [, <arg2> ... ])`
  - `functionName[<subName1>, <subName2>, ...]`
  - `functionName[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`

> **Note:** The bracketed `[...]` segment is accepted for backward compatibility, but is currently unused.

**Arguments**
- Same as `CALL`.

**Semantics**
- If the target function exists: behaves like `CALL`, then control returns and reaches `CATCH` sequentially; `CATCH` skips the catch body.
- If the function does not exist: jumps to the `CATCH` marker (so execution begins at the first line of the catch body).

**Errors & validation**
- Still errors for invalid argument binding/type conversion when a function is found.
- Mis-nesting (`CATCH` without `TRYC*`, `ENDCATCH` without `CATCH`) is a load-time error (the line is marked as error).

**Examples**
```erabasic
TRYCCALL OPTIONAL_HOOK
CATCH
    PRINTL "hook missing"
ENDCATCH
```

## TRYCJUMPFORM (instruction)

**Summary**
- Like `TRYJUMPFORM`, but supports a `CATCH ... ENDCATCH` block for the “not found” case.

**Tags**
- calls

**Syntax**
```text
TRYCJUMPFORM <target>
CATCH
    <catch body>
ENDCATCH
```

- `<target>` can be:
  - `<formString>`
  - `<formString>()`
  - `<formString>, <arg1> [, <arg2> ... ]`
  - `<formString>(<arg1> [, <arg2> ... ])`
  - `<formString>[<subName1>, <subName2>, ...]`
  - `<formString>[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`

> **Note:** The bracketed `[...]` segment is accepted for backward compatibility, but is currently unused.

**Arguments**
- Same as `JUMPFORM`.

**Semantics**
- Same as `TRYCJUMP`, but with a runtime-evaluated function name.

**Errors & validation**
- Same as `TRYCJUMP`.

**Examples**
```erabasic
TRYCJUMPFORM "OPTIONAL_%COUNT%"
CATCH
    PRINTL "missing"
ENDCATCH
```

## TRYCCALLFORM (instruction)

**Summary**
- Like `TRYCALLFORM`, but supports a `CATCH ... ENDCATCH` block for the “not found” case.

**Tags**
- calls

**Syntax**
```text
TRYCCALLFORM <target>
CATCH
    <catch body>
ENDCATCH
```

- `<target>` can be:
  - `<formString>`
  - `<formString>()`
  - `<formString>, <arg1> [, <arg2> ... ]`
  - `<formString>(<arg1> [, <arg2> ... ])`
  - `<formString>[<subName1>, <subName2>, ...]`
  - `<formString>[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`

> **Note:** The bracketed `[...]` segment is accepted for backward compatibility, but is currently unused.

**Arguments**
- Same as `CALLFORM`.

**Semantics**
- Same as `TRYCCALL`, but with a runtime-evaluated function name.

**Errors & validation**
- Same as `TRYCCALL`.

**Examples**
```erabasic
TRYCCALLFORM "HOOK_%TARGET%"
CATCH
    PRINTL "hook missing"
ENDCATCH
```

## CALLEVENT (instruction)

**Summary**
- Invokes an event function by event-dispatch semantics rather than by ordinary `CALL` semantics.

**Tags**
- calls

**Syntax**
- `CALLEVENT <eventFunction>`

**Arguments**
- `<eventFunction>` (raw event-function name): target event name.
  - This is not a string expression and no arguments can be passed through `CALLEVENT`.

**Semantics**
- Resolves `<eventFunction>` as an event-function name.
- If the name exists as an event function, `CALLEVENT` runs the same grouped event-dispatch sequence described in `runtime-model.md`:
  - group 0: `#ONLY`
  - group 1: `#PRI`
  - group 2: normal
  - group 3: `#LATER`
- `#SINGLE` / `#ONLY` affect progression exactly as in ordinary event dispatch.
- If no event function with that name exists and no non-event function with that name exists, the instruction is a silent no-op.

**Errors & validation**
- Runtime error if `<eventFunction>` names a non-event function instead of an event function.
- Runtime error if any event call is already active on the call stack; event calls cannot nest.
- Load-time warning if a `CALLEVENT` line is written inside an event function body, because such execution would always violate the non-nesting rule.

**Examples**
- `CALLEVENT EVENTLOAD`

## CALLF (instruction)

**Summary**
- Calls an expression function (built-in method or user-defined `#FUNCTION/#FUNCTIONS`) by name and evaluates it as a statement.

**Tags**
- calls

**Syntax**
- `CALLF <methodName>`
- `CALLF <methodName>()`
- `CALLF <methodName>, <arg1> [, <arg2> ... ]`
- `CALLF <methodName>(<arg1> [, <arg2> ... ])`
- `CALLF <methodName>[<subName1>, <subName2>, ...]`
- `CALLF <methodName>[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`
- The bracket segment is accepted for compatibility, but is currently unused.

**Arguments**
- `<methodName>` (raw string token): read up to `(` / `[` / `,` / `;` and then trimmed.
- `<argN>` (optional, expression): each occurrence is evaluated and passed to the method.
- `<subNameN>` (optional): values parsed from the bracket segment after `<methodName>`.
  - The current engine accepts and stores them, but they do not affect method resolution or call behavior.

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
- `CALLFORMF <formString>`
- `CALLFORMF <formString>()`
- `CALLFORMF <formString>, <arg1> [, <arg2> ... ]`
- `CALLFORMF <formString>(<arg1> [, <arg2> ... ])`
- `CALLFORMF <formString>[<subName1>, <subName2>, ...]`
- `CALLFORMF <formString>[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`
- The bracket segment is accepted for compatibility, but is currently unused.

**Arguments**
- `<formString>` (FORM/formatted string): its evaluated result is used as the method name.
- `<argN>` (optional, expression): each occurrence is evaluated and passed to the method.
- `<subNameN>` (optional): values parsed from the bracket segment after `<formString>`.
  - The current engine accepts and stores them, but they do not affect method resolution or call behavior.

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
- `CALLSHARP <methodName>()`
- `CALLSHARP <methodName>, <arg1> [, <arg2> ... ]`
- `CALLSHARP <methodName>(<arg1> [, <arg2> ... ])`
- `CALLSHARP <methodName>[<subName1>, <subName2>, ...]`
- `CALLSHARP <methodName>[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`

**Arguments**
- `<methodName>` (raw string token): matched against the registered plugin method name.
- `<argN>` (optional, expression): each occurrence is evaluated and passed to the plugin as either a string or an integer.
- `<subNameN>` (optional): values parsed from the bracket segment accepted by the parser for compatibility.
  - The current implementation accepts and stores them, but they do not affect plugin-method lookup or invocation.

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
- Jumps back to the start of the currently executing function label without leaving the current call frame.

**Tags**
- flow

**Syntax**
- `RESTART`

**Arguments**
- None.

**Semantics**
- Restarts the current function label from its beginning.
- The current call frame is preserved: arguments, `LOCAL/LOCALS`, private variables, and other per-call state stay in the same call instance.
- In particular, `DYNAMIC` private variables are **not** reinitialized just because `RESTART` occurs.
- If the restarted function eventually returns, it returns to the original caller of the current function, not to the line after `RESTART`.
- Inside an event dispatch, `RESTART` restarts the current event handler label only; it does not restart the whole event-group sequence.

**Errors & validation**
- None.

**Examples**
- `RESTART`

## GOTO (instruction)

**Summary**
- Jumps to a local `$label` within the current function.

**Tags**
- calls

**Syntax**
- `GOTO <labelName>`

**Arguments**
- `<labelName>` (raw string token): used to resolve a `$label` relative to the current function.

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
- `<formString>` (FORM/formatted string): its evaluated result is used as the `$label` name.

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
```text
TRYCGOTO <labelName>
CATCH
    <catch body>
ENDCATCH
```

- Header line: `TRYCGOTO <labelName>`

**Arguments**
- Same as `GOTO`.

**Semantics**
- If the `$label` exists: behaves like `GOTO` (jumps to the label). Whether the `CATCH` line is ever reached depends on subsequent control flow.
- If the `$label` does not exist: jumps to the `CATCH` marker (entering the catch body).

**Errors & validation**
- Mis-nesting (`CATCH` without `TRYC*`, `ENDCATCH` without `CATCH`) is a load-time error (the line is marked as error).

**Examples**
```erabasic
TRYCGOTO OPTIONAL_LABEL
CATCH
    PRINTL "label missing"
ENDCATCH
```

## TRYCGOTOFORM (instruction)

**Summary**
- Like `TRYGOTOFORM`, but supports a `CATCH ... ENDCATCH` block for the “not found” case.

**Tags**
- calls

**Syntax**
```text
TRYCGOTOFORM <formString>
CATCH
    <catch body>
ENDCATCH
```

- Header line: `TRYCGOTOFORM <formString>`

**Arguments**
- Same as `GOTOFORM`.

**Semantics**
- Same as `TRYCGOTO`, but with a runtime-evaluated label name.

**Errors & validation**
- Same as `TRYCGOTO`.

**Examples**
```erabasic
TRYCGOTOFORM "LABEL_%RESULT%"
CATCH
    PRINTL "label missing"
ENDCATCH
```

## CATCH (instruction)

**Summary**
- Begins the catch-body of a `TRYC* ... CATCH ... ENDCATCH` construct.

**Tags**
- error-handling

**Syntax**
```text
CATCH
    <catch body>
ENDCATCH
```

- Header line: `CATCH`
- Terminator line: `ENDCATCH`

**Arguments**
- None.

**Semantics**
- When reached **sequentially** (i.e. the `TRYC*` succeeded and returned normally), `CATCH` jumps to the matching `ENDCATCH` marker, skipping the catch body.
- When entered by a failed `TRYC*` instruction, execution jumps to the `CATCH` marker and (due to the engine’s advance-first model) begins executing at the first line of the catch body.

**Errors & validation**
- `CATCH` without a matching open `TRYC*` is a load-time error (the line is marked as error).

**Examples**
```erabasic
TRYCCALL OPTIONAL_HOOK
CATCH
    PRINTL "hook missing"
ENDCATCH
```

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
```text
TRYCALLLIST
    FUNC ...
    ...
ENDFUNC
```

- Header line: `TRYCALLLIST`
- Item lines: `FUNC ...` (see `FUNC` for item syntax)
- Terminator line: `ENDFUNC`

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
- `FUNC` item syntax is documented in `FUNC`; candidate name is a FORM string, arguments are normal expressions, and any bracket subname segment is currently ignored here.

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
```erabasic
TRYCALLLIST
    FUNC HOOK_%TARGET%, TARGET
    FUNC HOOK_DEFAULT
ENDFUNC
```

## TRYJUMPLIST (instruction)

**Summary**
- Like `TRYCALLLIST`, but performs a `JUMP` into the first existing candidate.

**Tags**
- calls

**Syntax**
```text
TRYJUMPLIST
    FUNC ...
    ...
ENDFUNC
```

- Header line: `TRYJUMPLIST`
- Item lines: `FUNC ...` (see `FUNC` for item syntax)
- Terminator line: `ENDFUNC`

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
```erabasic
TRYJUMPLIST
    FUNC PHASE_%COUNT%
    FUNC PHASE_DEFAULT
ENDFUNC
```

## TRYGOTOLIST (instruction)

**Summary**
- Tries a list of candidate `$label` targets and jumps to the first one that exists; otherwise jumps to `ENDFUNC` (end of the list).

**Tags**
- calls

**Syntax**
```text
TRYGOTOLIST
    FUNC <formString>
    ...
ENDFUNC
```

- Header line: `TRYGOTOLIST`
- Item lines: `FUNC <formString>` (see `FUNC`; this variant forbids subnames and arguments)
- Terminator line: `ENDFUNC`

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
```erabasic
TRYGOTOLIST
    FUNC LABEL_%RESULT%
    FUNC LABEL_DEFAULT
ENDFUNC
```

## FUNC (instruction)

**Summary**
- List-item line inside `TRYCALLLIST` / `TRYJUMPLIST` / `TRYGOTOLIST` blocks.

**Tags**
- functions

**Syntax**
- Inside `TRYCALLLIST` / `TRYJUMPLIST`:
  - `FUNC <formString>`
  - `FUNC <formString>()`
  - `FUNC <formString>, <arg1> [, <arg2> ... ]`
  - `FUNC <formString>(<arg1> [, <arg2> ... ])`
  - `FUNC <formString>[<subName1>, <subName2>, ...]`
  - `FUNC <formString>[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`
  - The bracket segment is accepted for compatibility, but is currently unused by `TRYCALLLIST` / `TRYJUMPLIST`.
- Inside `TRYGOTOLIST`:
  - `FUNC <formString>`

**Arguments**
- `<formString>` (FORM/formatted string): evaluated to a function name or label name.
- `<argN>` (optional, expression): call argument; not allowed for `TRYGOTOLIST`.
- `<subNameN>` (optional): only for `TRYCALLLIST` / `TRYJUMPLIST`; parsed from the bracket segment after `<formString>` and currently ignored.

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
- Appends raw literal text to the separate debug-output buffer.

**Tags**
- debug
- io

**Syntax**
- `DEBUGPRINT`
- `DEBUGPRINT <raw text>`
- `DEBUGPRINT;<raw text>`

**Arguments**
- `<raw text>` (optional, raw text; default `""`): not an expression.

**Semantics**
- Appends the raw literal text to the host's **debug-output buffer**, not to the normal output model.
- Layer boundary:
  - this does not add normal display lines,
  - `GETDISPLAYLINE`, `HTML_GETPRINTEDSTR`, `HTML_POPPRINTINGSTR`, `LINECOUNT`, and `OUTPUTLOG` do not read it.
- If debug mode is disabled, the instruction still executes but produces no visible effect.
- This instruction is **not** skipped by output skipping (`SKIPDISP`).
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- None.

**Examples**
- `DEBUGPRINT trace=`

## DEBUGPRINTL (instruction)

**Summary**
- Like `DEBUGPRINT`, but also appends a newline to the debug-output buffer.

**Tags**
- debug
- io

**Syntax**
- `DEBUGPRINTL`
- `DEBUGPRINTL <raw text>`
- `DEBUGPRINTL;<raw text>`

**Arguments**
- `<raw text>` (optional, raw text; default `""`): not an expression.

**Semantics**
- Same destination and isolation rules as `DEBUGPRINT`: it writes only to the separate debug-output buffer, not to the normal output model.
- After appending the raw literal text, appends one newline to the debug-output buffer.
- If debug mode is disabled, the instruction still executes but produces no visible effect.
- This instruction is **not** skipped by output skipping (`SKIPDISP`).
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- None.

**Examples**
- `DEBUGPRINTL init ok`

## DEBUGPRINTFORM (instruction)

**Summary**
- Appends a FORM/formatted string result to the separate debug-output buffer.

**Tags**
- debug
- io

**Syntax**
- `DEBUGPRINTFORM`
- `DEBUGPRINTFORM <formString>`

**Arguments**
- `<formString>` (optional, FORM/formatted string; default `""`): parsed like `PRINTFORM*`.

**Semantics**
- Evaluates `<formString>` using the normal FORM/formatted-string rules, then appends the resulting string to the host's separate debug-output buffer.
- Layer boundary:
  - this does not add normal display lines,
  - `GETDISPLAYLINE`, `HTML_GETPRINTEDSTR`, `HTML_POPPRINTINGSTR`, `LINECOUNT`, and `OUTPUTLOG` do not read it.
- If debug mode is disabled, the formatted string is still parsed/evaluated, but the resulting text is not shown anywhere visible.
- This instruction is **not** skipped by output skipping (`SKIPDISP`).
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- FORM parsing/evaluation errors follow the normal `PRINTFORM*` rules.

**Examples**
```erabasic
DEBUGPRINTFORM "X={VALUE}"
```

## DEBUGPRINTFORML (instruction)

**Summary**
- Like `DEBUGPRINTFORM`, but also appends a newline to the debug-output buffer.

**Tags**
- debug
- io

**Syntax**
- `DEBUGPRINTFORML`
- `DEBUGPRINTFORML <formString>`

**Arguments**
- `<formString>` (optional, FORM/formatted string; default `""`): parsed like `PRINTFORM*`.

**Semantics**
- Evaluates `<formString>` using the normal FORM/formatted-string rules, appends the resulting string to the separate debug-output buffer, then appends one newline there.
- It does not affect the normal output model or any normal output readback helper.
- If debug mode is disabled, the formatted string is still parsed/evaluated, but the resulting text is not shown anywhere visible.
- This instruction is **not** skipped by output skipping (`SKIPDISP`).
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- FORM parsing/evaluation errors follow the normal `PRINTFORM*` rules.

**Examples**
```erabasic
DEBUGPRINTFORML "phase={PHASE}"
```

## DEBUGCLEAR (instruction)

**Summary**
- Clears the separate debug-output buffer.

**Tags**
- debug
- io

**Syntax**
- `DEBUGCLEAR`

**Arguments**
- None.

**Semantics**
- Clears the host's debug-output buffer.
- This does not affect the normal output model, the pending print buffer, or the HTML-island layer.
- This instruction is **not** skipped by output skipping (`SKIPDISP`).
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- None.

**Examples**
- `DEBUGCLEAR`

## ASSERT (instruction)

**Summary**
- Debug-only assertion that raises a script error when its condition is false.

**Tags**
- debug

**Syntax**
- `ASSERT <bool>`

**Arguments**
- `<bool>` (int): treated as false when it evaluates to `0`, true otherwise.

**Semantics**
- In debug mode, evaluates `<bool>`.
- If the result is non-zero, `ASSERT` does nothing.
- If the result is `0`, `ASSERT` raises a script error and stops normal script execution.
- Outside debug mode, `ASSERT` is a complete no-op: the argument is not even parsed or validated.

**Errors & validation**
- In debug mode, parse / argument-validation errors are handled normally.
- In debug mode, runtime error if `<bool>` evaluates to `0`.
- Outside debug mode, `ASSERT` never raises argument-parsing errors because the argument is skipped entirely.

**Examples**
- `ASSERT TARGET >= 0`

## THROW (instruction)

**Summary**
- Forces a script error with a caller-provided message.

**Tags**
- debug

**Syntax**
- `THROW`
- `THROW <formedString>`

**Arguments**
- `<formedString>` (optional, string; default `""`): error message text.
  - This uses formed-string parsing, so `{...}` / `%%...%%` interpolation is available.

**Semantics**
- Evaluates `<formedString>` and immediately raises a script error.
- The resulting text is shown as the `THROW` message in the engine’s error report.
- No later statements in the current run are executed unless outer error-handling flow intercepts the error.

**Errors & validation**
- `THROW` always raises a script error after evaluating its message.
- Additional parse / evaluation errors can occur while forming `<formedString>`.

**Examples**
- `THROW Unexpected state: {TARGET}`
- `THROW`

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
- `<var*>` (one or more changeable non-character variable terms): arrays are allowed; several variable categories are rejected.

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
- `<charaNo*>` (one or more int values): character indices to save (0-based).

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
- `<refTarget>` (identifier token): intended to be a `REF` variable name; see `variables.md`.
- `<sourceName>` (identifier token): names the source variable to bind to.

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
- `<refTarget>` (identifier token): intended to be a `REF` variable name; see `variables.md`.
- `<sourceName>` (string): evaluates to a variable name string.

**Semantics**
- The current engine implementation throws a “not implemented” error at runtime.
- In this build, `REF` variables are still used by user-defined function argument binding (pass-by-reference); see `variables.md`.

**Errors & validation**
- Always errors at runtime.

**Examples**
- `REFBYNAME X, "A"`

## HTML_PRINT (instruction)

**Summary**
- Prints an HTML string (Emuera’s HTML-like mini language) into the normal output model.

**Tags**
- io

**Syntax**
- `HTML_PRINT <html> [, <toBuffer>]`

**Arguments**
- `<html>` (string): HTML string (see `html-output.md`).
- `<toBuffer>` (optional, int; default `0`)
  - `0` (default): append directly to the visible normal output area as one logical line.
  - non-zero: append the parsed HTML segments to the pending print buffer (no immediate visible line append).

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output and no evaluation).
- Evaluates `<html>` to a string.
  - If it is null/empty, no output is produced.
- Interprets the string as HTML according to `html-output.md`.
- If `<toBuffer> = 0` (or omitted):
  - any pending print-buffer content is flushed first as normal visible output,
  - the HTML output is then appended directly to the visible normal output area,
  - the entire `HTML_PRINT` call constitutes one logical line, even if it occupies multiple visible display rows because of `<br>` or wrapping.
- If `<toBuffer> != 0`:
  - the HTML output is converted to output segments and appended to the pending print buffer,
  - `<br>` (and literal `\n` inside the HTML string) create internal display-row breaks for the future flush,
  - but no visible line is appended yet and no final logical-line end is implied.
- Style boundary:
  - non-HTML text style commands such as `ALIGNMENT`, `SETFONT`, `SETCOLOR`, or `FONTSTYLE` do not style the HTML output,
  - use HTML tags (`<p>`, `<font>`, `<b>`, etc.) instead.
- Layer boundary:
  - `HTML_PRINT(..., 0)` affects the normal visible output area,
  - `HTML_PRINT(..., nonZero)` affects only the pending print buffer until some later flush/line-end operation.

**Errors & validation**
- Argument type/count errors follow the normal expression argument rules.
- Invalid HTML strings raise runtime errors (unsupported tags, invalid attributes, invalid character references, or invalid tag structure), except where a tag explicitly defines fallback-to-text behavior.

**Examples**
```erabasic
HTML_PRINT "<p align='center'><b>Hello</b> <font color='red'>world</font></p>"
```

```erabasic
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
- `<outParts>` (optional, changeable 1D non-character string array variable term; default `RESULTS`): receives the split parts.
- `<outCount>` (optional, changeable integer variable term; default `RESULT`): receives the part count.

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
- `<src>` (string): main sprite name.
- `<srcb>` (optional, string; default `""`): sprite name used when the region is selected/focused.
- `<srcm>` (optional, string; default `""`): mapping-sprite name used by mouse-input mapping color side channels (see `html-output.md` and `INPUT`).
- `<width>` / `<height>` / `<ypos>` (optional, int): mixed numeric attributes.
  - Numeric arguments are positional: `width`, then `height`, then `ypos`.
  - Each numeric argument may be followed by a `px` suffix token to indicate pixels (e.g. `80px`).
  - Without `px`, the value is interpreted as a percentage of the current font size (in pixels): `valuePx = value * FontSize / 100`.

**Semantics**
- Skipped when output skipping is active (via `SKIPDISP`).
- Appends an image part to the current print buffer (no implicit newline).
- Argument parsing is two-phase:
  - First, `PRINT_IMG` reads up to three leading string slots: `src`, then `srcb`, then `srcm`.
  - Once the first numeric argument appears, the parse switches to numeric mode, and all remaining arguments must also be numeric.
- To supply `srcm` while leaving `srcb` absent, pass an empty string placeholder for `srcb`.
- Empty `srcb` / `srcm` omit the corresponding HTML attribute.
- The image part is equivalent to emitting an HTML `<img ...>` tag and letting the HTML renderer handle it:
  - `src=<src>`
  - `srcb=<srcb>` only when `srcb` is non-empty
  - `srcm=<srcm>` only when `srcm` is non-empty
  - `width=<width>`, `height=<height>`, `ypos=<ypos>` only when the numeric value is non-zero
- See `html-output.md` (“Inline images: `<img ...>`”) for rendering rules:
  - If `height` is omitted or `0`, it defaults to the current font size (pixels).
  - If `width` is omitted or `0`, the original aspect ratio is preserved.
  - Negative `width` / `height` values flip the image horizontally/vertically.
  - If the sprite cannot be resolved, the tag is rendered as literal text.

**Errors & validation**
- Parse-time error if `<src>` is omitted.
- Parse-time error if a string argument appears after numeric arguments have started.
- Parse-time error if more than 3 numeric arguments are provided.

**Examples**
- `PRINT_IMG "FACE_001"`
- `PRINT_IMG "FACE_001", 80px` (explicit pixel width)
- `PRINT_IMG "FACE_001", "", "FACE_001_MAP"` (set `srcm` while leaving `srcb` absent)
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
- `<width>` (int): rectangle width in mixed units; must satisfy `width > 0`.
- `<x>` (int): 4-argument form only; rectangle X offset in mixed units and must satisfy `x >= 0`.
- `<y>` (int): 4-argument form only; rectangle Y offset in mixed units; negative values are allowed.
- `<height>` (int): 4-argument form only; rectangle height in mixed units and must satisfy `height > 0`.
- Mixed-unit rule:
  - A numeric argument may be followed by a `px` suffix token to indicate pixels (for example `30px`).
  - Without `px`, the value is interpreted as a percentage of the current font size in pixels: `valuePx = value * FontSize / 100`.
- 1-argument form defaults:
  - `x = 0`
  - `y = 0`
  - `height = FontSize` (pixels)

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
- `<width>` (int): space width in mixed units.
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
- `<foreColor>` (int): RGB color `0x000000 <= color <= 0xFFFFFF`.
- `<backColor>` (int): RGB color `0x000000 <= color <= 0xFFFFFF`.

**Semantics**
- Updates the UI tooltip colors for subsequent tooltips.
- This instruction executes even when output skipping is active.

**Errors & validation**
- Runtime error if either color is outside `0 <= color <= 0xFFFFFF`.

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
- `<delayMs>` (int): delay in milliseconds.
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
- `<durationMs>` (int): duration in milliseconds.
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
- Waits for a primitive mouse/key event (mouse down, wheel, key press, or timeout) and reports it via `RESULT` / `RESULT:*`; on the mouse-down path it may also write `RESULTS` when a selected string ordinary-output button is involved.

**Tags**
- io

**Syntax**
- `INPUTMOUSEKEY`
- `INPUTMOUSEKEY <timeMs>`

**Arguments**
- `<timeMs>` (optional, int): time limit in milliseconds.
  - If `timeMs > 0`, enables a timeout.
  - If omitted or `timeMs <= 0`, no timeout is used.

**Semantics**
- Enters a wait state for *primitive* input events (not text box submission).
- See also: `input-flow.md` (how primitive waits differ from textbox-segmentation waits) and `cbg-layer.md` (why `RESULT:4` is a separate CBG hit-map channel rather than an ordinary output-button value).
- This instruction is **not** skipped by output skipping (`SKIPDISP`) because it is not a print-skip instruction.
- When an event occurs, the engine resumes script execution and assigns `RESULT_ARRAY[0]` through `RESULT_ARRAY[5]` (i.e. `RESULT` and `RESULT:1` through `RESULT:5`) as follows.

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
  - `RESULT:4`: current CBG button-hit-map value (24-bit RGB), or `-1` when no opaque CBG-map pixel is available at the click position.
  - `RESULT:5`: if an **integer ordinary output button** is currently selected, its button value; otherwise `0`.
  - Additionally, if a **string ordinary output button** is currently selected, the engine assigns `RESULTS = <button string>` (and `RESULT:5 = 0`).
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
  - `RESULT:1` through `RESULT:5` are set to `0`.

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
- `<timeMs>` (optional, int; default `0`): sleep duration in milliseconds after processing pending UI events. Must satisfy `0 <= timeMs <= 10000`.

**Semantics**
- Forces a repaint, sets an internal “sleep” state, processes UI events, and then:
  - if `timeMs > 0`, sleeps for `timeMs` milliseconds,
  - otherwise returns immediately after event processing.
- This is a redraw/UI-yield primitive, not a normal input wait and not a normal output producer.
- It does not assign `RESULT`/`RESULTS`.
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
- `<arrayVarName>` (identifier token): names an array variable; not an expression.
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
- `<dest>` (changeable integer variable term): destination.
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
- `<dest>` (optional, changeable integer variable term; default `RESULT`): receives the value.

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
- `<dest>` (optional, changeable integer variable term; default `RESULT`): receives the value.

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
- `<filename>` (string): file name or relative path under the sound directory.
- `<repeat>` (optional, int; default `1`): number of times to repeat the sound.
  - Values `< 1` are clamped to `1`.

**Semantics**
- Resolves the path by concatenating the engine’s sound directory with `<filename>`, then normalizing to an absolute path.
- If the file does not exist, no-op.
- Otherwise, starts playback on a “sound effect slot”:
  - There are 10 slots (`0 <= slot <= 9`).
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
- Stops playback of all sound effect slots (`0 <= slot <= 9`).
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
- `<filename>` (string): file name or relative path under the sound directory.

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
- `<volume>` (int): volume level, clamped to `0 <= volume <= 100`.

**Semantics**
- Applies the volume to all 10 sound effect slots (`0 <= slot <= 9`).
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
- `<volume>` (int): volume level, clamped to `0 <= volume <= 100`.

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
- `TRYCALLF <methodName>`
- `TRYCALLF <methodName>()`
- `TRYCALLF <methodName>, <arg1> [, <arg2> ... ]`
- `TRYCALLF <methodName>(<arg1> [, <arg2> ... ])`
- `TRYCALLF <methodName>[<subName1>, <subName2>, ...]`
- `TRYCALLF <methodName>[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`
- The bracket segment is accepted for compatibility, but is currently unused.

**Arguments**
- `<methodName>` (raw string token): read up to `(` / `[` / `,` / `;` and then trimmed.
  - This is **not** a string literal or string.
  - Quotes are treated as ordinary characters.
  - Backslash escapes are processed (e.g. `\n`, `\t`, `\s`).
- `<argN>` (optional, expression): each occurrence is evaluated and passed to the target method.
- `<subNameN>` (optional): values parsed from the bracket segment after `<methodName>`.
  - The current engine accepts and stores them, but they do not affect method resolution or call behavior.

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
- `TRYCALLFORMF <formString>`
- `TRYCALLFORMF <formString>()`
- `TRYCALLFORMF <formString>, <arg1> [, <arg2> ... ]`
- `TRYCALLFORMF <formString>(<arg1> [, <arg2> ... ])`
- `TRYCALLFORMF <formString>[<subName1>, <subName2>, ...]`
- `TRYCALLFORMF <formString>[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`
- The bracket segment is accepted for compatibility, but is currently unused.

**Arguments**
- `<formString>` (FORM/formatted string): its evaluated result is used as the method name.
- `<argN>` (optional, expression): each occurrence is evaluated and passed to the target method.
- `<subNameN>` (optional): values parsed from the bracket segment after `<formString>`.
  - The current engine accepts and stores them, but they do not affect method resolution or call behavior.

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
- The UI host performs the actual restart after the quit request is posted; scripts have no further control over that timing.

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
- Waits for a text input, then stores it in `RESULT` if it parses as a signed 64-bit integer; otherwise stores it in `RESULTS`.

**Tags**
- io

**Syntax**
- `INPUTANY`

**Arguments**
- None.

**Semantics**
- Enters an input wait (`InputType = AnyValue`).
- Like other non-primitive value waits, clicking a selectable **normal-output button** can submit one value/text on the mouse-click completion path.
- See also: `input-flow.md` (shared submission paths, segment draining/discard rules, and `MesSkip` interaction).
- On completion:
  - If the submitted text parses as a signed 64-bit integer, assigns it to `RESULT`.
  - Otherwise assigns the submitted text to `RESULTS`.
  - This same rule is used when the submitted text came from a clicked normal-output button.
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
- `<fontName>` (string): font family name.

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
- `<size>` (int): font size value passed to the UI font constructor.

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
- `<enabled>` (int): `0` disables custom tooltips; non-zero enables.

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
- `<flags>` (int): bitmask passed through as `.NET` `TextFormatFlags`.

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
- `<enabled>` (int): `0` disables; non-zero enables.

**Semantics**
- When enabled and tooltips are custom-drawn (`TOOLTIP_CUSTOM 1`):
  - If the tooltip text can be parsed as an integer `i`, the engine uses graphics resource `G:i` as the primary tooltip content.
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
- `<default>` (optional, int): used only when the submitted text is empty (not used for invalid integer text).
- `<mouse>` (optional, int; default `0`): controls the extra mouse side-channel mode.
  - Clicking a selectable button also satisfies `BINPUT` by itself; when `<mouse> != 0`, the same extra mouse side channels as `INPUT` are also written.
- `<canSkip>` (optional, int): presence enables the `MesSkip` fast path; its numeric value is ignored (not evaluated).
- Extra arguments after `<canSkip>` are accepted by the argument parser but ignored by the runtime.

**Semantics**
- Ensures the current output is drawn before waiting (flushes any pending buffer and forces a refresh).
- See also: `input-flow.md` (shared submission paths, segment draining/discard rules, and `MesSkip` interaction).
- Selectable-button scope:
  - only buttons in the current active button generation are eligible for typed/button matching,
  - older retained buttons may remain visible in output but are not accepted once the active generation has advanced.
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
- Mouse side channels when `<mouse> != 0`:
  - When the input is completed via a mouse click, the same UI-side `RESULT_ARRAY[...]` / `RESULTS_ARRAY[...]` side channels as `INPUT` are written (see `INPUT`).
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
- `<default>` (optional, string): default string used only when the submitted text is empty.
- `<mouse>` (optional, int; default `0`): controls the extra mouse side-channel mode.
  - Clicking a selectable button also satisfies `BINPUTS` by itself; when `<mouse> != 0`, the same extra mouse side channels as `INPUTS` are also written.
- `<canSkip>` (optional, int): presence enables the `MesSkip` fast path; its numeric value is ignored (not evaluated).

**Semantics**
- Ensures the current output is drawn before waiting (flushes any pending buffer and forces a refresh).
- See also: `input-flow.md` (shared submission paths, segment draining/discard rules, and `MesSkip` interaction).
- Selectable-button scope:
  - only buttons in the current active button generation are eligible for typed/button matching,
  - older retained buttons may remain visible in output but are not accepted once the active generation has advanced.
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
- Mouse side channels when `<mouse> != 0`:
  - When the input is completed via a mouse click, the same UI-side `RESULT_ARRAY[...]` / `RESULTS_ARRAY[...]` side channels as `INPUTS` are written (see `INPUT`).
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
- `<default>` (optional, int): used only when the submitted text is empty (not used for invalid integer text).
- `<mouse>` (optional, int; default `0`): controls the extra mouse side-channel mode.
  - Clicking a selectable button also satisfies `ONEBINPUT` by itself; when `<mouse> != 0`, the same extra mouse side channels as `INPUT` are also written.
- `<canSkip>` (optional, int): presence enables the `MesSkip` fast path; its numeric value is ignored (not evaluated).
- Extra arguments after `<canSkip>` are accepted by the argument parser but ignored by the runtime.

**Semantics**
- Same button-matching and default rules as `BINPUT`.
- Clicking a selectable integer button can satisfy this wait by itself; when `<mouse> != 0`, the same extra mouse side channels as `BINPUT` / `INPUT` are also written.
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
- `<default>` (optional, string): default string used only when the submitted text is empty.
- `<mouse>` (optional, int; default `0`): controls the extra mouse side-channel mode.
  - Clicking a selectable button also satisfies `ONEBINPUTS` by itself; when `<mouse> != 0`, the same extra mouse side channels as `INPUTS` are also written.
- `<canSkip>` (optional, int): presence enables the `MesSkip` fast path; its numeric value is ignored (not evaluated).

**Semantics**
- Same button-matching and default rules as `BINPUTS`.
- Clicking a selectable button can satisfy this wait by itself; when `<mouse> != 0`, the same extra mouse side channels as `BINPUTS` / `INPUTS` are also written.
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
- Updates option metadata for an existing data-table column.

**Tags**
- data

**Syntax**
- `DT_COLUMN_OPTIONS <dataTableName>, <columnName>, DEFAULT, <optionValue>`
- `DT_COLUMN_OPTIONS <dataTableName>, <columnName>, DEFAULT, <optionValue>, DEFAULT, <optionValue>, ...`

**Arguments**
- `<dataTableName>` (string): data-table name.
- `<columnName>` (string): column name.
- `DEFAULT` (option keyword): matched case-insensitively.
- `<optionValue>` (same type as the column): default value to store for that option.
  - String columns require a string value.
  - Numeric columns require an int value.

**Semantics**
- Requires an existing data table and an existing column.
- Currently the only supported option keyword is `DEFAULT`.
- `DEFAULT` changes the column’s default value used for future row/cell operations that consult the column default.
- If a numeric column uses a narrower integer type than the script value type, the stored default is converted with the same clamping rules as other data-table numeric writes.
- Repeated option pairs are processed left-to-right; a later `DEFAULT` overrides an earlier one.

**Errors & validation**
- Parse / argument-validation error if the first two arguments are missing, if an option keyword has no following value, or if an unknown option keyword is used.
- Runtime error if the named table or column does not exist.
- Runtime error if `<optionValue>` has the wrong type for the column.

**Examples**
- `DT_COLUMN_OPTIONS "SHOP", "PRICE", DEFAULT, 0`
- `DT_COLUMN_OPTIONS "SHOP", "NAME", DEFAULT, "(none)"`

## VARI (instruction)

**Summary**
- Declares a function-private dynamic int variable through the scoped-variable instruction extension.

**Tags**
- variables

**Syntax**
- `VARI <name>`
- `VARI <name> = <intValue>`
- `VARI <name>, <size1>`
- `VARI <name>, <size1>, <size2>`
- `VARI <name>, <size1>, <size2>, <size3>`

**Arguments**
- `<name>` (string): private variable name declared in the containing function.
- `<intValue>` (optional, int): scalar initializer.
- `<size1>` (optional, int literal): first array size.
- `<size2>` (optional, int literal): second array size.
- `<size3>` (optional, int literal): third array size.
  - `VARI` supports 1D / 2D / 3D declarations.

**Semantics**
- Available only when `UseScopedVariableInstruction` is enabled; see `data-files.md` and `grammar.md`.
- At load time, `VARI` declares a function-private dynamic int variable in the containing function’s private-variable namespace.
- Name visibility is function-wide after load; other lines in the same function can resolve the variable name regardless of the declaration’s textual position.
- Executing the `VARI` line reinitializes that variable for the current call:
  - scalar form resets it, then applies `<intValue>` if present
  - array form allocates a fresh zero-filled array of the declared size
- Re-executing the same `VARI` line during one call resets the variable again.
- On function return, the current call’s storage is discarded like other dynamic private variables.
- Array declarations do not have element initializers; if `= ...` text is present in an array form, it does not supply array contents.

**Errors & validation**
- Not available unless `UseScopedVariableInstruction` is enabled.
- Parse / load error if an array size is not an integer literal or if more than 3 dimensions are requested.
- Other name-validity rules follow ordinary function-private variable rules; see `variables.md`.

**Examples**
- `VARI ANSWER = 42`
- `VARI BUFFER, 16`

## VARS (instruction)

**Summary**
- Declares a function-private dynamic string variable through the scoped-variable instruction extension.

**Tags**
- variables

**Syntax**
- `VARS <name>`
- `VARS <name> = "<literal>"`
- `VARS <name>, <size1>`
- `VARS <name>, <size1>, <size2>`
- `VARS <name>, <size1>, <size2>, <size3>`

**Arguments**
- `<name>` (string): private variable name declared in the containing function.
- `"<literal>"` (optional, double-quoted string literal): scalar initializer.
  - This is not a general string expression.
- `<size1>` (optional, int literal): first array size.
- `<size2>` (optional, int literal): second array size.
- `<size3>` (optional, int literal): third array size.
  - `VARS` supports 1D / 2D / 3D declarations.

**Semantics**
- Available only when `UseScopedVariableInstruction` is enabled; see `data-files.md` and `grammar.md`.
- At load time, `VARS` declares a function-private dynamic string variable in the containing function’s private-variable namespace.
- Name visibility is function-wide after load; other lines in the same function can resolve the variable name regardless of the declaration’s textual position.
- Executing the `VARS` line reinitializes that variable for the current call:
  - scalar form resets it, then applies the literal initializer if present
  - array form allocates a fresh empty-string-filled array of the declared size
- Re-executing the same `VARS` line during one call resets the variable again.
- On function return, the current call’s storage is discarded like other dynamic private variables.
- Array declarations do not have element initializers; if `= ...` text is present in an array form, it does not supply array contents.

**Errors & validation**
- Not available unless `UseScopedVariableInstruction` is enabled.
- Parse / load error if an array size is not an integer literal, if more than 3 dimensions are requested, or if the scalar initializer is not written as a double-quoted literal.
- Other name-validity rules follow ordinary function-private variable rules; see `variables.md`.

**Examples**
- `VARS QUESTION = "生命、宇宙、そして万物についての究極の疑問の答え"`
- `VARS BUFFER, 8`

## HTML_PRINT_ISLAND (instruction)

**Summary**
- Appends HTML-rendered rows into the separate `HTML_PRINT_ISLAND` layer rather than the normal output/log model.

**Tags**
- io

**Syntax**
- `HTML_PRINT_ISLAND <html>`
- `HTML_PRINT_ISLAND <html>, <ignored>`

**Arguments**
- `<html>` (string): HTML string (see `html-output.md`).
- `<ignored>` (optional, int): compatibility-only argument.
  - If provided, it must parse/type-check as an `int` expression.
  - Its value is ignored at runtime.

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output and no evaluation).
- Evaluates `<html>` to a string and parses it with the same HTML mini-language used by `HTML_PRINT`.
- Appends the resulting display rows to the retained `HTML_PRINT_ISLAND` layer in order.
  - `<br>` and literal `\n` create separate appended island rows.
  - Automatic wrapping can also create additional appended island rows.
- Layer boundary:
  - the island layer is not part of the normal display-line array,
  - it is not counted by `LINECOUNT`,
  - it is not removed by `CLEARLINE`,
  - it is not returned by `GETDISPLAYLINE` or `HTML_GETPRINTEDSTR`.
- Painting model:
  - island rows are painted from the top of the window downward,
  - they do not scroll together with the normal backlog.
- Repaint timing:
  - this instruction updates island-layer state immediately,
  - but it does not itself force an immediate repaint,
  - so the changed island content becomes visible on the next repaint allowed/forced by the redraw schedule.
- `<div ...>` sub-area elements are not rendered in the island layer.
- Use `HTML_PRINT_ISLAND_CLEAR` to clear the island layer.

**Errors & validation**
- Argument type/count errors follow the normal expression argument rules.
- Invalid HTML strings raise runtime errors (same HTML mini-language as `HTML_PRINT`).

**Examples**
```erabasic
HTML_PRINT_ISLAND "<font color='white'>Status</font><br>HP: 10"
```

## HTML_PRINT_ISLAND_CLEAR (instruction)

**Summary**
- Clears all rows currently retained in the `HTML_PRINT_ISLAND` layer.

**Tags**
- io

**Syntax**
- `HTML_PRINT_ISLAND_CLEAR`

**Arguments**
- None.

**Semantics**
- Clears the retained island-layer state immediately.
- This affects only the island layer:
  - the normal output model is unchanged,
  - the pending print buffer is unchanged.
- This instruction is not skipped by output skipping; it always clears the island layer when executed.
- Repaint timing:
  - like `HTML_PRINT_ISLAND`, clearing changes stored state immediately,
  - but it does not itself force an immediate repaint,
  - so the disappearance becomes visible on the next repaint allowed/forced by the redraw schedule.

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
- `PRINTN`
- `PRINTN <raw text>`
- `PRINTN;<raw text>`

**Arguments**
- `<raw text>` (optional, raw text; default `""`): not an expression.

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- `PRINTN` appends its text to the pending print buffer, then materializes the current buffered content to retained normal output, then waits for a key **without** ending the logical line.
- Observable consequence:
  - the current content becomes part of retained normal output before the wait,
  - but the next later flush is still merged into that same logical line rather than starting a new one.
- If output skipping is active (via `SKIPDISP`), this instruction is skipped before execution.

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
- `PRINTVN <value1> [, <value2> ...]`

**Arguments**
- `<valueN>` (expression): each occurrence must evaluate to an int or string; ints are converted with `ToString` and concatenated with no separator.

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
- `PRINTSN <text>`

**Arguments**
- `<text>` (string): text to print.

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
- `PRINTFORMN [<formString>]`

**Arguments**
- `<formString>` (optional, FORM/formatted string; default `""`): scanned to end-of-line.

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
- `PRINTFORMSN <formatSource>`

**Arguments**
- `<formatSource>` (string): evaluated to a string, then parsed as a FORM/formatted string at runtime.

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
- Returns the first registered character index in the current character list whose `NO` matches the requested character number.

**Tags**
- characters

**Syntax**
- `GETCHARA(charaNo [, spFlag])`

**Signatures / argument rules**
- `GETCHARA(charaNo)` → `long`
- `GETCHARA(charaNo, spFlag)` → `long`

**Arguments**
- `charaNo` (int): character `NO` to search for in the current registered character list.
- `spFlag` (optional, int; default `0`): legacy SP-character compatibility argument.

**Semantics**
- Scans the current registered character list in ascending character-index order and returns the first matching character index.
- If `CompatiSPChara=NO`:
  - `spFlag` is accepted but ignored,
  - the search matches any registered character whose `NO` equals `charaNo`.
- If `CompatiSPChara=YES`:
  - omitted / `0`: searches only non-SP registered characters,
  - non-zero: first searches non-SP registered characters; if no match is found, retries against SP registered characters.
- Returns `-1` if no matching registered character is found.

**Errors & validation**
- No special validation beyond normal integer-argument evaluation.

**Examples**
- `idx = GETCHARA(100)`
- `IF GETCHARA(100) != -1`

## GETSPCHARA (expression function)

**Summary**
- Returns the first registered SP-character index in the current character list whose `NO` matches the requested character number.

**Tags**
- characters

**Syntax**
- `GETSPCHARA(charaNo)`

**Signatures / argument rules**
- `GETSPCHARA(charaNo)` → `long`

**Arguments**
- `charaNo` (int): character `NO` to search for among currently registered SP characters.

**Semantics**
- Scans the current registered character list in ascending character-index order.
- A match requires both:
  - `NO == charaNo`, and
  - the character is currently flagged as SP (`CFLAG:0 != 0`).
- Returns the first matching registered character index, or `-1` if none exists.

**Errors & validation**
- Runtime error if `CompatiSPChara=NO`.

**Examples**
- `idx = GETSPCHARA(100)`

## CSVNAME (expression function)

**Summary**
- Returns the CSV-defined `NAME` string for a character template `NO`.

**Tags**
- characters
- csv

**Syntax**
- `CSVNAME(charaNo [, spFlag])`

**Signatures / argument rules**
- `CSVNAME(charaNo)` → `string`
- `CSVNAME(charaNo, spFlag)` → `string`

**Arguments**
- `charaNo` (int): character template `NO` to read from the CSV-backed character-template database.
- `spFlag` (optional, int; default `0`): legacy SP-character compatibility argument.
  - `0`: ordinary call shape.
  - non-zero: accepted only when `CompatiSPChara=YES`.

**Semantics**
- Looks up a character template by `NO` and returns its CSV-defined `NAME` string.
- If that field is absent or `null` in the template, returns `""`.
- Compatibility quirk:
  - `spFlag != 0` is accepted only when `CompatiSPChara=YES`,
  - but this build does not expose a separate stable public selector for duplicate normal/SP templates that share the same `NO`; do not rely on `spFlag` alone to disambiguate duplicate template definitions.

**Errors & validation**
- Runtime error if `charaNo` does not resolve to a character template.
- Runtime error if `spFlag != 0` while `CompatiSPChara=NO`.

**Examples**
- `s = CSVNAME(0)`

## CSVCALLNAME (expression function)

**Summary**
- Returns the CSV-defined `CALLNAME` string for a character template `NO`.

**Tags**
- characters
- csv

**Syntax**
- `CSVCALLNAME(charaNo [, spFlag])`

**Signatures / argument rules**
- `CSVCALLNAME(charaNo)` → `string`
- `CSVCALLNAME(charaNo, spFlag)` → `string`

**Arguments**
- `charaNo` (int): character template `NO` to read from the CSV-backed character-template database.
- `spFlag` (optional, int; default `0`): legacy SP-character compatibility argument.
  - `0`: ordinary call shape.
  - non-zero: accepted only when `CompatiSPChara=YES`.

**Semantics**
- Looks up a character template by `NO` and returns its CSV-defined `CALLNAME` string.
- If that field is absent or `null` in the template, returns `""`.
- Compatibility quirk:
  - `spFlag != 0` is accepted only when `CompatiSPChara=YES`,
  - but this build does not expose a separate stable public selector for duplicate normal/SP templates that share the same `NO`; do not rely on `spFlag` alone to disambiguate duplicate template definitions.

**Errors & validation**
- Runtime error if `charaNo` does not resolve to a character template.
- Runtime error if `spFlag != 0` while `CompatiSPChara=NO`.

**Examples**
- `s = CSVCALLNAME(0)`

## CSVNICKNAME (expression function)

**Summary**
- Returns the CSV-defined `NICKNAME` string for a character template `NO`.

**Tags**
- characters
- csv

**Syntax**
- `CSVNICKNAME(charaNo [, spFlag])`

**Signatures / argument rules**
- `CSVNICKNAME(charaNo)` → `string`
- `CSVNICKNAME(charaNo, spFlag)` → `string`

**Arguments**
- `charaNo` (int): character template `NO` to read from the CSV-backed character-template database.
- `spFlag` (optional, int; default `0`): legacy SP-character compatibility argument.
  - `0`: ordinary call shape.
  - non-zero: accepted only when `CompatiSPChara=YES`.

**Semantics**
- Looks up a character template by `NO` and returns its CSV-defined `NICKNAME` string.
- If that field is absent or `null` in the template, returns `""`.
- Compatibility quirk:
  - `spFlag != 0` is accepted only when `CompatiSPChara=YES`,
  - but this build does not expose a separate stable public selector for duplicate normal/SP templates that share the same `NO`; do not rely on `spFlag` alone to disambiguate duplicate template definitions.

**Errors & validation**
- Runtime error if `charaNo` does not resolve to a character template.
- Runtime error if `spFlag != 0` while `CompatiSPChara=NO`.

**Examples**
- `s = CSVNICKNAME(0)`

## CSVMASTERNAME (expression function)

**Summary**
- Returns the CSV-defined `MASTERNAME` string for a character template `NO`.

**Tags**
- characters
- csv

**Syntax**
- `CSVMASTERNAME(charaNo [, spFlag])`

**Signatures / argument rules**
- `CSVMASTERNAME(charaNo)` → `string`
- `CSVMASTERNAME(charaNo, spFlag)` → `string`

**Arguments**
- `charaNo` (int): character template `NO` to read from the CSV-backed character-template database.
- `spFlag` (optional, int; default `0`): legacy SP-character compatibility argument.
  - `0`: ordinary call shape.
  - non-zero: accepted only when `CompatiSPChara=YES`.

**Semantics**
- Looks up a character template by `NO` and returns its CSV-defined `MASTERNAME` string.
- If that field is absent or `null` in the template, returns `""`.
- Compatibility quirk:
  - `spFlag != 0` is accepted only when `CompatiSPChara=YES`,
  - but this build does not expose a separate stable public selector for duplicate normal/SP templates that share the same `NO`; do not rely on `spFlag` alone to disambiguate duplicate template definitions.

**Errors & validation**
- Runtime error if `charaNo` does not resolve to a character template.
- Runtime error if `spFlag != 0` while `CompatiSPChara=NO`.

**Examples**
- `s = CSVMASTERNAME(0)`

## CSVCSTR (expression function)

**Summary**
- Returns a CSV-defined `CSTR` string entry for a character template `NO`.

**Tags**
- characters
- csv

**Syntax**
- `CSVCSTR(charaNo, index [, spFlag])`

**Signatures / argument rules**
- `CSVCSTR(charaNo, index)` → `string`
- `CSVCSTR(charaNo, index, spFlag)` → `string`

**Arguments**
- `charaNo` (int): character template `NO` to read.
- `index` (int): `CSTR` element index to read.
- `spFlag` (optional, int; default `0`): legacy SP-character compatibility argument.
  - `0`: ordinary call shape.
  - non-zero: accepted only when `CompatiSPChara=YES`.

**Semantics**
- Looks up a character template by `NO` and returns its `CSTR[index]` entry.
- If the template has no `CSTR` table, returns `""`.
- If the template has a `CSTR` table and `index` is in range but no explicit entry is defined at that slot, returns `""`.
- Compatibility quirk:
  - `spFlag != 0` is accepted only when `CompatiSPChara=YES`,
  - but this build does not expose a separate stable public selector for duplicate normal/SP templates that share the same `NO`; do not rely on `spFlag` alone to disambiguate duplicate template definitions.

**Errors & validation**
- Runtime error if `charaNo` does not resolve to a character template.
- Runtime error if `index` is outside the readable `CSTR` range for that template.
- Runtime error if `spFlag != 0` while `CompatiSPChara=NO`.

**Examples**
- `s = CSVCSTR(0, 2)`

## CSVBASE (expression function)

**Summary**
- Returns the CSV-defined `BASE` integer entry for a character template `NO`.

**Tags**
- characters
- csv

**Syntax**
- `CSVBASE(charaNo, index [, spFlag])`

**Signatures / argument rules**
- `CSVBASE(charaNo, index)` → `long`
- `CSVBASE(charaNo, index, spFlag)` → `long`

**Arguments**
- `charaNo` (int): character template `NO` to read.
- `index` (int): `BASE` table index to read.
- `spFlag` (optional, int; default `0`): legacy SP-character compatibility argument.
  - `0`: ordinary call shape.
  - non-zero: accepted only when `CompatiSPChara=YES`.

**Semantics**
- Looks up a character template by `NO` and returns its `BASE[index]` entry.
- If `index` is in range but no explicit entry is defined at that slot, returns `0`.
- `CSVBASE` reads the template table directly; when a live character is created, the same template entries are copied into both runtime `BASE` and `MAXBASE`.
- Compatibility quirk:
  - `spFlag != 0` is accepted only when `CompatiSPChara=YES`,
  - but this build does not expose a separate stable public selector for duplicate normal/SP templates that share the same `NO`; do not rely on `spFlag` alone to disambiguate duplicate template definitions.

**Errors & validation**
- Runtime error if `charaNo` does not resolve to a character template.
- Runtime error if `index` is outside the readable `BASE` range for that template.
- Runtime error if `spFlag != 0` while `CompatiSPChara=NO`.

**Examples**
- `n = CSVBASE(0, 0)`

## CSVABL (expression function)

**Summary**
- Returns the CSV-defined `ABL` integer entry for a character template `NO`.

**Tags**
- characters
- csv

**Syntax**
- `CSVABL(charaNo, index [, spFlag])`

**Signatures / argument rules**
- `CSVABL(charaNo, index)` → `long`
- `CSVABL(charaNo, index, spFlag)` → `long`

**Arguments**
- `charaNo` (int): character template `NO` to read.
- `index` (int): `ABL` table index to read.
- `spFlag` (optional, int; default `0`): legacy SP-character compatibility argument.
  - `0`: ordinary call shape.
  - non-zero: accepted only when `CompatiSPChara=YES`.

**Semantics**
- Looks up a character template by `NO` and returns its `ABL[index]` entry.
- If `index` is in range but no explicit entry is defined at that slot, returns `0`.
- Compatibility quirk:
  - `spFlag != 0` is accepted only when `CompatiSPChara=YES`,
  - but this build does not expose a separate stable public selector for duplicate normal/SP templates that share the same `NO`; do not rely on `spFlag` alone to disambiguate duplicate template definitions.

**Errors & validation**
- Runtime error if `charaNo` does not resolve to a character template.
- Runtime error if `index` is outside the readable `ABL` range for that template.
- Runtime error if `spFlag != 0` while `CompatiSPChara=NO`.

**Examples**
- `n = CSVABL(0, 0)`

## CSVMARK (expression function)

**Summary**
- Returns the CSV-defined `MARK` integer entry for a character template `NO`.

**Tags**
- characters
- csv

**Syntax**
- `CSVMARK(charaNo, index [, spFlag])`

**Signatures / argument rules**
- `CSVMARK(charaNo, index)` → `long`
- `CSVMARK(charaNo, index, spFlag)` → `long`

**Arguments**
- `charaNo` (int): character template `NO` to read.
- `index` (int): `MARK` table index to read.
- `spFlag` (optional, int; default `0`): legacy SP-character compatibility argument.
  - `0`: ordinary call shape.
  - non-zero: accepted only when `CompatiSPChara=YES`.

**Semantics**
- Looks up a character template by `NO` and returns its `MARK[index]` entry.
- If `index` is in range but no explicit entry is defined at that slot, returns `0`.
- Compatibility quirk:
  - `spFlag != 0` is accepted only when `CompatiSPChara=YES`,
  - but this build does not expose a separate stable public selector for duplicate normal/SP templates that share the same `NO`; do not rely on `spFlag` alone to disambiguate duplicate template definitions.

**Errors & validation**
- Runtime error if `charaNo` does not resolve to a character template.
- Runtime error if `index` is outside the readable `MARK` range for that template.
- Runtime error if `spFlag != 0` while `CompatiSPChara=NO`.

**Examples**
- `n = CSVMARK(0, 0)`

## CSVEXP (expression function)

**Summary**
- Returns the CSV-defined `EXP` integer entry for a character template `NO`.

**Tags**
- characters
- csv

**Syntax**
- `CSVEXP(charaNo, index [, spFlag])`

**Signatures / argument rules**
- `CSVEXP(charaNo, index)` → `long`
- `CSVEXP(charaNo, index, spFlag)` → `long`

**Arguments**
- `charaNo` (int): character template `NO` to read.
- `index` (int): `EXP` table index to read.
- `spFlag` (optional, int; default `0`): legacy SP-character compatibility argument.
  - `0`: ordinary call shape.
  - non-zero: accepted only when `CompatiSPChara=YES`.

**Semantics**
- Looks up a character template by `NO` and returns its `EXP[index]` entry.
- If `index` is in range but no explicit entry is defined at that slot, returns `0`.
- Compatibility quirk:
  - `spFlag != 0` is accepted only when `CompatiSPChara=YES`,
  - but this build does not expose a separate stable public selector for duplicate normal/SP templates that share the same `NO`; do not rely on `spFlag` alone to disambiguate duplicate template definitions.

**Errors & validation**
- Runtime error if `charaNo` does not resolve to a character template.
- Runtime error if `index` is outside the readable `EXP` range for that template.
- Runtime error if `spFlag != 0` while `CompatiSPChara=NO`.

**Examples**
- `n = CSVEXP(0, 0)`

## CSVRELATION (expression function)

**Summary**
- Returns the CSV-defined `RELATION` integer entry for a character template `NO`.

**Tags**
- characters
- csv

**Syntax**
- `CSVRELATION(charaNo, index [, spFlag])`

**Signatures / argument rules**
- `CSVRELATION(charaNo, index)` → `long`
- `CSVRELATION(charaNo, index, spFlag)` → `long`

**Arguments**
- `charaNo` (int): character template `NO` to read.
- `index` (int): `RELATION` table index to read.
- `spFlag` (optional, int; default `0`): legacy SP-character compatibility argument.
  - `0`: ordinary call shape.
  - non-zero: accepted only when `CompatiSPChara=YES`.

**Semantics**
- Looks up a character template by `NO` and returns its `RELATION[index]` entry.
- If `index` is in range but no explicit entry is defined at that slot, returns `0`.
- For `CSVRELATION`, an undefined slot returns `0`; the runtime default relation value used for live characters is **not** substituted here.
- Compatibility quirk:
  - `spFlag != 0` is accepted only when `CompatiSPChara=YES`,
  - but this build does not expose a separate stable public selector for duplicate normal/SP templates that share the same `NO`; do not rely on `spFlag` alone to disambiguate duplicate template definitions.

**Errors & validation**
- Runtime error if `charaNo` does not resolve to a character template.
- Runtime error if `index` is outside the readable `RELATION` range for that template.
- Runtime error if `spFlag != 0` while `CompatiSPChara=NO`.

**Examples**
- `n = CSVRELATION(0, 0)`

## CSVTALENT (expression function)

**Summary**
- Returns the CSV-defined `TALENT` integer entry for a character template `NO`.

**Tags**
- characters
- csv

**Syntax**
- `CSVTALENT(charaNo, index [, spFlag])`

**Signatures / argument rules**
- `CSVTALENT(charaNo, index)` → `long`
- `CSVTALENT(charaNo, index, spFlag)` → `long`

**Arguments**
- `charaNo` (int): character template `NO` to read.
- `index` (int): `TALENT` table index to read.
- `spFlag` (optional, int; default `0`): legacy SP-character compatibility argument.
  - `0`: ordinary call shape.
  - non-zero: accepted only when `CompatiSPChara=YES`.

**Semantics**
- Looks up a character template by `NO` and returns its `TALENT[index]` entry.
- If `index` is in range but no explicit entry is defined at that slot, returns `0`.
- Compatibility quirk:
  - `spFlag != 0` is accepted only when `CompatiSPChara=YES`,
  - but this build does not expose a separate stable public selector for duplicate normal/SP templates that share the same `NO`; do not rely on `spFlag` alone to disambiguate duplicate template definitions.

**Errors & validation**
- Runtime error if `charaNo` does not resolve to a character template.
- Runtime error if `index` is outside the readable `TALENT` range for that template.
- Runtime error if `spFlag != 0` while `CompatiSPChara=NO`.

**Examples**
- `n = CSVTALENT(0, 0)`

## CSVCFLAG (expression function)

**Summary**
- Returns the CSV-defined `CFLAG` integer entry for a character template `NO`.

**Tags**
- characters
- csv

**Syntax**
- `CSVCFLAG(charaNo, index [, spFlag])`

**Signatures / argument rules**
- `CSVCFLAG(charaNo, index)` → `long`
- `CSVCFLAG(charaNo, index, spFlag)` → `long`

**Arguments**
- `charaNo` (int): character template `NO` to read.
- `index` (int): `CFLAG` table index to read.
- `spFlag` (optional, int; default `0`): legacy SP-character compatibility argument.
  - `0`: ordinary call shape.
  - non-zero: accepted only when `CompatiSPChara=YES`.

**Semantics**
- Looks up a character template by `NO` and returns its `CFLAG[index]` entry.
- If `index` is in range but no explicit entry is defined at that slot, returns `0`.
- Compatibility quirk:
  - `spFlag != 0` is accepted only when `CompatiSPChara=YES`,
  - but this build does not expose a separate stable public selector for duplicate normal/SP templates that share the same `NO`; do not rely on `spFlag` alone to disambiguate duplicate template definitions.

**Errors & validation**
- Runtime error if `charaNo` does not resolve to a character template.
- Runtime error if `index` is outside the readable `CFLAG` range for that template.
- Runtime error if `spFlag != 0` while `CompatiSPChara=NO`.

**Examples**
- `n = CSVCFLAG(0, 0)`

## CSVEQUIP (expression function)

**Summary**
- Returns the CSV-defined `EQUIP` integer entry for a character template `NO`.

**Tags**
- characters
- csv

**Syntax**
- `CSVEQUIP(charaNo, index [, spFlag])`

**Signatures / argument rules**
- `CSVEQUIP(charaNo, index)` → `long`
- `CSVEQUIP(charaNo, index, spFlag)` → `long`

**Arguments**
- `charaNo` (int): character template `NO` to read.
- `index` (int): `EQUIP` table index to read.
- `spFlag` (optional, int; default `0`): legacy SP-character compatibility argument.
  - `0`: ordinary call shape.
  - non-zero: accepted only when `CompatiSPChara=YES`.

**Semantics**
- Looks up a character template by `NO` and returns its `EQUIP[index]` entry.
- If `index` is in range but no explicit entry is defined at that slot, returns `0`.
- Compatibility quirk:
  - `spFlag != 0` is accepted only when `CompatiSPChara=YES`,
  - but this build does not expose a separate stable public selector for duplicate normal/SP templates that share the same `NO`; do not rely on `spFlag` alone to disambiguate duplicate template definitions.

**Errors & validation**
- Runtime error if `charaNo` does not resolve to a character template.
- Runtime error if `index` is outside the readable `EQUIP` range for that template.
- Runtime error if `spFlag != 0` while `CompatiSPChara=NO`.

**Examples**
- `n = CSVEQUIP(0, 0)`

## CSVJUEL (expression function)

**Summary**
- Returns the CSV-defined `JUEL` integer entry for a character template `NO`.

**Tags**
- characters
- csv

**Syntax**
- `CSVJUEL(charaNo, index [, spFlag])`

**Signatures / argument rules**
- `CSVJUEL(charaNo, index)` → `long`
- `CSVJUEL(charaNo, index, spFlag)` → `long`

**Arguments**
- `charaNo` (int): character template `NO` to read.
- `index` (int): `JUEL` table index to read.
- `spFlag` (optional, int; default `0`): legacy SP-character compatibility argument.
  - `0`: ordinary call shape.
  - non-zero: accepted only when `CompatiSPChara=YES`.

**Semantics**
- Looks up a character template by `NO` and returns its `JUEL[index]` entry.
- If `index` is in range but no explicit entry is defined at that slot, returns `0`.
- Compatibility quirk:
  - `spFlag != 0` is accepted only when `CompatiSPChara=YES`,
  - but this build does not expose a separate stable public selector for duplicate normal/SP templates that share the same `NO`; do not rely on `spFlag` alone to disambiguate duplicate template definitions.

**Errors & validation**
- Runtime error if `charaNo` does not resolve to a character template.
- Runtime error if `index` is outside the readable `JUEL` range for that template.
- Runtime error if `spFlag != 0` while `CompatiSPChara=NO`.

**Examples**
- `n = CSVJUEL(0, 0)`

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
- The chara selector part of `charaVarTerm` (written selector only): does not affect the search; the function always compares against the scanned chara index `i`.
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
- The chara selector part of `charaVarTerm` (written selector only): does not affect the search; the function always compares against the scanned chara index `i`.
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
- `isSp` (optional, int; default `0`): legacy SP-character compatibility argument.
  - `0`: ordinary call shape.
  - non-zero: accepted only when `CompatiSPChara=YES`.

**Semantics**
- Returns `1` if a character template exists for `charaNo`, otherwise returns `0`.
- Compatibility quirk:
  - `isSp != 0` is accepted only when `CompatiSPChara=YES`,
  - but this build does not expose a separate stable public selector for duplicate normal/SP templates that share the same `NO`; do not rely on `isSp` alone to disambiguate duplicate template definitions.

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
- `value` (int): numerator.
- `maxValue` (int): denominator; must evaluate to `> 0`.
- `length` (int): bar width; must satisfy `1 <= length <= 99`.

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
- Reports whether non-forced automatic redraw is currently enabled.

**Tags**
- ui

**Syntax**
- `CURRENTREDRAW()`

**Signatures / argument rules**
- `CURRENTREDRAW()` → `long`

**Arguments**
- None.

**Semantics**
- Returns `0` if redraw mode is currently off (`REDRAW` bit `0` disabled).
- Returns `1` if redraw mode is currently on.
- This reflects only the persistent redraw mode flag.
  - It does not report whether a one-shot forced repaint just happened.
  - It does not report whether stored output state exists; redraw mode and stored output state are separate concerns.

**Errors & validation**
- None.

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
- Runtime error if any component is outside `0 <= component <= 255`.

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
- `format` (optional, string; default `""`): numeric format string passed to `Int64.ToString(format)`.

**Semantics**
- Formats `money`:
  - if `format` is omitted or `""`: uses default numeric formatting (`money.ToString()`)
  - otherwise: uses `money.ToString(format)`
- Then attaches the currency label (`MoneyLabel`):
  - `MoneyFirst = true`: `MoneyLabel + formatted`
  - `MoneyFirst = false`: `formatted + MoneyLabel`

**Errors & validation**
- Runtime error if `format` is not a valid `Int64.ToString` format string.

**Examples**
- `MONEYSTR(123)` → `"$123"` if `MoneyLabel="$"` and `MoneyFirst=true`.
- `MONEYSTR(123, "D6")` → `"$000123"` under the same config.

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
- `RAND(<min>, <max>)`
- `RAND(<max>)`

**Signatures / argument rules**
- `RAND(max)` → `long`
- `RAND(min, max)` → `long`

**Arguments**
- `min` (int): inclusive lower bound in the two-argument form.
- `max` (int): exclusive upper bound.

**Semantics**
- `RAND(max)` is shorthand for `RAND(0, max)`.
- Returns a random integer `r` such that `min <= r < max`.
- RNG engine selection depends on JSON `UseNewRandom`:
  - `UseNewRandom=NO` (legacy mode): uses the legacy SFMT generator with the MT19937 parameter set. The returned value is computed as `min + (nextUInt64 % (max - min))`. This is deterministic for a given seed/state, but it is not perfectly unbiased when `(max - min)` does not divide `2^64`.
  - `UseNewRandom=YES` (new mode): uses a host `.NET System.Random` instance and its `NextInt64(max - min)` behavior, then adds `min`. `RANDOMIZE`, `INITRAND`, and `DUMPRAND` do not control this mode.
- In new mode, the host `System.Random` instance is created when the runtime creates its variable-evaluator state; scripts have no built-in way to reseed or snapshot it.

**Errors & validation**
- Parse/argument-validation error if called with no arguments (`RAND()`).
- Runtime error if `max <= min` after argument evaluation.
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
- `endIndex` (optional, int; default current length of the summed dimension): exclusive end index in the summed dimension.

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
- `endIndex` (optional, int; default current array length): exclusive end index.

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
- `endIndex` (optional, int; default current array length): end index.

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
- `endIndex` (optional, int; default current array length): end index.

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
- Maps a CSV/alias/ERD key name to its integer index for a variable family or user-defined variable.

**Tags**
- string-key
- erd

**Syntax**
- `GETNUM(varTerm, key [, dimension])`

**Signatures / argument rules**
- `GETNUM(varTerm, key)` → `long`
- `GETNUM(varTerm, key, dimension)` → `long`

**Arguments**
- `varTerm` (variable term): selects the variable family or user-defined variable name whose key dictionary should be queried.
  - This function uses the variable identity, not the current cell value.
  - Any written `:` subscripts do not participate in the lookup itself.
- `key` (string): key name to resolve.
- `dimension` (optional, int): ERD dimension selector for user-defined variables.
  - Omitted: ERD fallback uses the base variable name.
  - Supplied `n`: ERD fallback uses the dictionary named `name@n`.

**Semantics**
- First checks the built-in CSV-name / alias dictionary associated with `varTerm`'s variable family.
- If no built-in match is found, it checks ERD data for the selected variable name (or `name@dimension`) when such ERD data exists.
- Returns the mapped integer index on success; otherwise returns `-1`.
- `key = ""` also returns `-1`.
- `dimension` only affects the ERD fallback path; it does not change built-in CSV-name lookup.
- `GETNUM(NAME, key)` / `GETNUM(CALLNAME, key)` are allowed even though those families do not accept string-key syntax in ordinary variable-argument positions.

**Errors & validation**
- Parse/type error if `varTerm` is not a variable term or `key` is not string-typed.
- No runtime error is raised merely because the selected variable family has no key dictionary; that case returns `-1`.

**Examples**
- `n = GETNUM(ABL, "技巧")`
- `charaNo = GETNUM(CALLNAME, "霊夢")`

## GETPALAMLV (expression function)

**Summary**
- Converts a raw value into a level number by comparing it against the current `PALAMLV` threshold table.

**Tags**
- numeric

**Syntax**
- `GETPALAMLV(value, maxLv)`

**Signatures / argument rules**
- `GETPALAMLV(value, maxLv)` → `long`

**Arguments**
- `value` (int): value to compare against the current `PALAMLV` thresholds.
- `maxLv` (int): maximum level boundary to inspect.

**Semantics**
- Reads the current runtime `PALAMLV` array, not a baked copy.
- For each `i` with `0 <= i < maxLv`, compares `value` against `PALAMLV:i+1`.
- Returns the first `i` such that `value < PALAMLV:i+1`.
- If no such `i` exists, returns `maxLv`.
- Therefore the result is effectively “how many leading level boundaries are less than or equal to `value`”, capped at `maxLv`.
- No clamping is applied to `maxLv`:
  - if `maxLv <= 0`, the loop is skipped and the function returns `maxLv` as-is,
  - if `maxLv` is larger than the readable `PALAMLV` boundary range, the function fails when it reads past the table.

**Errors & validation**
- No special validation beyond normal integer-argument evaluation.
- Runtime failure if `maxLv` makes the function read beyond the current `PALAMLV` array.

**Examples**
- `lv = GETPALAMLV(PALAM:0, 5)`

## GETEXPLV (expression function)

**Summary**
- Converts a raw value into a level number by comparing it against the current `EXPLV` threshold table.

**Tags**
- numeric

**Syntax**
- `GETEXPLV(value, maxLv)`

**Signatures / argument rules**
- `GETEXPLV(value, maxLv)` → `long`

**Arguments**
- `value` (int): value to compare against the current `EXPLV` thresholds.
- `maxLv` (int): maximum level boundary to inspect.

**Semantics**
- Reads the current runtime `EXPLV` array, not a baked copy.
- For each `i` with `0 <= i < maxLv`, compares `value` against `EXPLV:i+1`.
- Returns the first `i` such that `value < EXPLV:i+1`.
- If no such `i` exists, returns `maxLv`.
- Therefore the result is effectively “how many leading level boundaries are less than or equal to `value`”, capped at `maxLv`.
- No clamping is applied to `maxLv`:
  - if `maxLv <= 0`, the loop is skipped and the function returns `maxLv` as-is,
  - if `maxLv` is larger than the readable `EXPLV` boundary range, the function fails when it reads past the table.

**Errors & validation**
- No special validation beyond normal integer-argument evaluation.
- Runtime failure if `maxLv` makes the function read beyond the current `EXPLV` array.

**Examples**
- `lv = GETEXPLV(PALAM:0, 5)`

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
- `endIndex` (optional, int; default current array length): exclusive end index.
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
- `i = FINDELEMENT(S, "^Alice$", 0, 100, 1)`

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
- `i = FINDLASTELEMENT(S, "Alice", 0, 100, 1)`  ; exact regex match

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
- `endIndex` (optional, int; default current array length): exclusive end index.

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
- Like `GETNUM`, but takes the variable name as a string instead of a variable term.

**Tags**
- string-key
- erd

**Syntax**
- `GETNUMB(varName, key)`

**Signatures / argument rules**
- `GETNUMB(varName, key)` → `long`

**Arguments**
- `varName` (string): variable name to resolve at runtime (for example `"ABL"`, `"CALLNAME"`, or a user-defined variable name).
- `key` (string): key name to resolve.

**Semantics**
- Resolves `varName` to a variable token at runtime.
- Then performs the same lookup model as `GETNUM`:
  - built-in CSV-name / alias dictionary first,
  - ERD fallback second (using only the base variable name, because this function has no `dimension` argument).
- Returns the mapped integer index on success; otherwise returns `-1`.
- `key = ""` also returns `-1`.

**Errors & validation**
- Runtime error if `varName` does not resolve to a variable name in the current runtime.
- No runtime error is raised merely because the resolved variable family has no key dictionary; that case returns `-1`.

**Examples**
- `n = GETNUMB("ABL", "技巧")`

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
- `keyArray` (non-character 1D array variable term): sort key array; int or string; must not be `CONST` or a calculated/pseudo variable.
- `arrayN` (one or more non-character array variable terms): arrays permuted to follow the key order; each may be 1D/2D/3D and int or string; must not be `CONST` or calculated.
  - Any subscripts written in these variable terms are ignored; the function operates on the underlying array storage.

**Semantics**
- Builds a permutation by scanning `keyArray` from index `0` and collecting a prefix of entries:
  - int key array: stops at the first `0`
  - string key array: stops at the first `null` or empty string
- Sorts that collected prefix in ascending order by key:
  - int keys: numeric ascending
  - string keys: `string.CompareTo` ordering (current culture)
- Applies the resulting permutation to each argument array (including `keyArray` itself):
  - 1D arrays: permutes elements `0 <= i < n`
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
- Returns the length of a string in the engine's language-length unit (the same unit used by `STRLEN`, `SUBSTRING`, and `STRFIND`).

**Tags**
- text

**Syntax**
- `STRLENS(str)`

**Signatures / argument rules**
- `STRLENS(str)` → `long`

**Arguments**
- `str` (string): input string.

**Semantics**
- Returns the same count that command-form `STRLEN` would write to `RESULT`.
- The count is measured under the engine's configured language encoding:
  - ASCII-only text counts as `str.Length`.
  - Non-ASCII text counts by encoded byte length.
- This is **not** Unicode-scalar counting; the result depends on the active language encoding.

**Errors & validation**
- None.

**Examples**
- `STRLENS("ABC")` → `3`

## STRLENSU (expression function)

**Summary**
- Returns the length of a string in UTF-16 code units.

**Tags**
- text

**Syntax**
- `STRLENSU(str)`

**Signatures / argument rules**
- `STRLENSU(str)` → `long`

**Arguments**
- `str` (string): input string.

**Semantics**
- Returns the same count that command-form `STRLENU` would write to `RESULT`.
- Equivalent to `.NET` `string.Length`.
- BMP characters count as `1`.
- Supplementary characters count as `2` because they occupy a UTF-16 surrogate pair.

**Errors & validation**
- None.

**Examples**
- `STRLENSU("ABC")` → `3`

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
- Returns a substring where `start` and `length` are measured in UTF-16 code units.

**Tags**
- text

**Syntax**
- `SUBSTRINGU(str [, start [, length]])`

**Signatures / argument rules**
- `SUBSTRINGU(str)` → `string`
- `SUBSTRINGU(str, start)` → `string`
- `SUBSTRINGU(str, start, length)` → `string`

**Arguments**
- `str` (string): input string.
- `start` (optional, int; default `0`): UTF-16 code-unit start index.
- `length` (optional, int; default `-1`): UTF-16 code-unit count; `< 0` means "to end".

**Semantics**
- Indexing/counting uses the same unit as `STRLENSU` (`.NET` `string.Length`).
- Normalization rules:
  - If `start >= str.Length` or `length == 0`, returns `""`.
  - If `length < 0` or `length > str.Length`, `length` is first replaced with `str.Length`.
  - If `start <= 0`, the effective start becomes `0`.
  - If `start + length > str.Length`, `length` is clamped to the remaining suffix length.
- After normalization, returns `.NET` `str.Substring(start, length)`.
- Because indexing is by UTF-16 code unit, a supplementary character occupies two positions and can be split by `start`/`length`.

**Errors & validation**
- Argument type/count errors are rejected by the engine's function-method argument checker.

**Examples**
- `SUBSTRINGU("ABCDE", 1, 2)` → `"BC"`

## STRFIND (expression function)

**Summary**
- Searches a string and returns the first match position in the engine's language-length unit.

**Tags**
- text

**Syntax**
- `STRFIND(target, word [, start])`

**Signatures / argument rules**
- `STRFIND(target, word)` → `long`
- `STRFIND(target, word, start)` → `long`

**Arguments**
- `target` (string): string to search.
- `word` (string): substring to find.
- `start` (optional, int; default `0`): search start position in the same unit as `STRLENS`.

**Semantics**
- Uses ordinal, case-sensitive substring search.
- `start` is interpreted in the same language-length unit returned by `STRLENS`.
- Effective start-position rules:
  - If `start <= 0`, search begins at the start of `target`.
  - If `start` falls inside a multi-byte character, the effective start moves to the following character boundary.
  - If the effective start is at or past the end of `target`, returns `-1`.
- Returns the first match position in the same language-length unit.
- Returns `-1` if no match is found.
- If `word == ""`, returns the effective start position when that position is still inside the string; otherwise returns `-1`.

**Errors & validation**
- None.

**Examples**
- `STRFIND("abcdeabced", "a", 3)` → `5`

## STRFINDU (expression function)

**Summary**
- Searches a string and returns the first match position in UTF-16 code units.

**Tags**
- text

**Syntax**
- `STRFINDU(target, word [, start])`

**Signatures / argument rules**
- `STRFINDU(target, word)` → `long`
- `STRFINDU(target, word, start)` → `long`

**Arguments**
- `target` (string): string to search.
- `word` (string): substring to find.
- `start` (optional, int; default `0`): UTF-16 code-unit start position.

**Semantics**
- Uses ordinal, case-sensitive substring search.
- `start` is interpreted in the same unit as `STRLENSU` (`.NET` `string.Length`).
- If `start < 0` or `start >= target.Length`, returns `-1`.
- Otherwise returns the first matching UTF-16 code-unit index, or `-1` if no match is found.
- If `word == ""`, returns `start` when `0 <= start < target.Length`; otherwise returns `-1`.
- Because indexing is by UTF-16 code unit, a supplementary character occupies two positions and can be split by `start`.

**Errors & validation**
- None.

**Examples**
- `STRFINDU("abcdeabced", "a", 3)` → `5`

## STRCOUNT (expression function)

**Summary**
- Counts regex matches in a string.

**Tags**
- text

**Syntax**
- `STRCOUNT(str, pattern)`

**Signatures / argument rules**
- `STRCOUNT(str, pattern)` → `long`

**Arguments**
- `str` (string): target string.
- `pattern` (string): regular-expression pattern.

**Semantics**
- Compiles `pattern` as a `.NET` regular expression with default options.
- Returns `Regex.Matches(str, pattern).Count`.
- Matching is regex-based, not plain-substring-based.
- Counted matches are the normal non-overlapping matches returned by `.NET` regex enumeration.
- Use `ESCAPE(pattern)` first if you want to search for a literal string via regex APIs.

**Errors & validation**
- Runtime error if `pattern` is not a valid regular expression.

**Examples**
- `STRCOUNT("aaaa", "aa")` → `2`

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
- `i` (int): value to format.
- `format` (optional, string; default `""`): numeric format string passed to `Int64.ToString(format)`.

**Semantics**
- Empty `format` uses default formatting.
- Otherwise returns `i.ToString(format)`.

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
- `str` (string): input string to parse.

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
- Even though many invalid strings return `0`, inputs that reach the integer-literal reader can raise runtime errors; for example:
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
- `str` (string): input string.

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
- `str` (string): input string.

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
- `str` (string): input string.

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
- `str` (string): input string.

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
- Returns whether the current in-progress output line is still empty.

**Tags**
- io

**Syntax**
- `LINEISEMPTY()`

**Signatures / argument rules**
- `LINEISEMPTY()` → `long`

**Arguments**
- None.

**Semantics**
- Returns `1` if the current printable line buffer has no content yet.
- Returns `0` once the current line has any visible/button content pending on it.
- Equivalent observable test: at that point in execution, would a bare `PRINTL` emit only an empty line?
- Only the current in-progress line matters; already flushed earlier lines do not affect the result.

**Errors & validation**
- None.

**Examples**
- `IF LINEISEMPTY() != 0`

## REPLACE (expression function)

**Summary**
- Replaces text in a string using regex mode, literal mode, or sequential array-driven regex replacement.

**Tags**
- text

**Syntax**
- `REPLACE(base, pattern, replaceArg [, mode])`
- `REPLACE(base, pattern, replaceArg, 1)`

**Signatures / argument rules**
- `REPLACE(base, pattern, replacement)` → `string`
- `REPLACE(base, pattern, replacement, mode)` → `string`
- `REPLACE(base, pattern, replacements, 1)` → `string`

**Arguments**
- `base` (string): input string.
- `pattern` (string): regex pattern unless `mode == 2`.
- `replaceArg` (string or non-const 1D string-array variable reference): mode-dependent third argument.
- `mode` (optional, int; default `0`): replacement mode selector.
  - `0`: regex replace using a string third argument
  - `1`: regex replace using successive string-array elements
  - `2`: literal `.NET` `string.Replace`
  - all values other than `1` and `2`: same behavior as `0`

**Semantics**
- Regex modes (`mode` omitted / `0` / all values other than `1` and `2`):
  - Compiles `pattern` as a `.NET` regular expression.
  - Treats `replaceArg` as a string and returns `Regex.Replace(base, pattern, replaceArg)`.
  - The replacement text follows normal `.NET` regex-replacement syntax (for example `$1` for capture groups).
- Sequential array mode (`mode == 1`):
  - Compiles `pattern` as a `.NET` regular expression.
  - Requires `replaceArg` to be a non-const 1D string-array variable reference.
  - For the `k`-th match (0-based), if `k < length(replaceArg)`, the replacement text is `replaceArg[k]`.
  - If `k >= length(replaceArg)`, the replacement text is `""`.
- Literal mode (`mode == 2`):
  - Treats `replaceArg` as a string.
  - Performs plain `.NET` `base.Replace(pattern, replaceArg)`.
  - `pattern` is treated as literal text, not a regex.

**Errors & validation**
- Runtime error if `pattern` is not a valid regular expression in regex modes.
- Runtime error if `mode == 1` but `replaceArg` is not a non-const 1D string-array variable reference.
- In literal mode, an empty `pattern` is rejected by the underlying string-replacement routine.

**Examples**
- `REPLACE("12億3456万7890円", "[^0-9]", "")` → `"1234567890"`
- `REPLACE("A-B-C", "-", ARR, 1)` with `ARR = ["x", "y"]` → `"AxByC"`
- `REPLACE("a.b.c", ".", "-", 2)` → `"a-b-c"`

## UNICODE (expression function)

**Summary**
- Returns a one-code-unit string for a BMP Unicode value.

**Tags**
- text

**Syntax**
- `UNICODE(code)`

**Signatures / argument rules**
- `UNICODE(code)` → `string`

**Arguments**
- `code` (int): Unicode value to convert.

**Semantics**
- Accepts only `0 <= code <= 0xFFFF`.
- On success, returns a string containing exactly one UTF-16 code unit.
- No surrogate-pair composition is performed:
  - supplementary scalar values above `0xFFFF` are rejected,
  - values satisfying `0xD800 <= code <= 0xDFFF` are returned as single code units.
- Control-code handling:
  - `LF` (`0x000A`) and `CR` (`0x000D`) are allowed,
  - other control values satisfying `0x0000 <= code <= 0x001E` and values satisfying `0x007F <= code <= 0x009F` cause a warning and return `""`.

**Errors & validation**
- Runtime error if `code` is outside `0 <= code <= 0xFFFF`.

**Examples**
- `UNICODE(0x2661)` → `"♡"`

## UNICODEBYTE (expression function)

**Summary**
- Despite the name, returns the first UTF-32 code value of the string as an integer.

**Tags**
- text

**Syntax**
- `UNICODEBYTE(str)`

**Signatures / argument rules**
- `UNICODEBYTE(str)` → `long`

**Arguments**
- `str` (string): source string.

**Semantics**
- Encodes `str` as UTF-32 and returns the first encoded code value.
- Only the first encoded code point matters; the remainder of the string is ignored.
- If the string begins with a supplementary character, the returned value can be greater than `0xFFFF`.
- This is a code-value query, not a raw-byte dump API.

**Errors & validation**
- Runtime error if `str == ""`.
- Any failure in the underlying UTF-32 conversion propagates as a runtime error.

**Examples**
- `UNICODEBYTE("A")` → `65`

## CONVERT (expression function)

**Summary**
- Converts an integer to its string form in base `2`, `8`, `10`, or `16`.

**Tags**
- text

**Syntax**
- `CONVERT(value, toBase)`

**Signatures / argument rules**
- `CONVERT(value, toBase)` → `string`

**Arguments**
- `value` (int): value to format.
- `toBase` (int): output base.

**Semantics**
- Accepts only `2`, `8`, `10`, or `16` for `toBase`.
- Equivalent to `.NET` `Convert.ToString(value, toBase)`.
- For hexadecimal output, alphabetic digits follow the external `.NET` behavior (`a`-`f`).

**Errors & validation**
- Runtime error if `toBase` is any value other than `2`, `8`, `10`, or `16`.

**Examples**
- `CONVERT(255, 16)` → `"ff"`

## ISNUMERIC (expression function)

**Summary**
- Returns whether a string is accepted by the engine's numeric-literal predicate.

**Tags**
- text

**Syntax**
- `ISNUMERIC(str)`

**Signatures / argument rules**
- `ISNUMERIC(str)` → `long`

**Arguments**
- `str` (string): string to test.

**Semantics**
- Returns `0` immediately if `str` contains any multi-byte character under the current language encoding.
- Returns `0` if `str` does not start with:
  - a digit, or
  - `+` / `-` followed by a digit.
- Otherwise checks the engine's integer-literal family, plus an optional trailing `.` followed only by decimal digits.
- Accepted integer-literal features include:
  - `0x` / `0X` hexadecimal prefixes,
  - `0b` / `0B` binary prefixes,
  - `e` / `E` and `p` / `P` exponent markers.
- Compatibility quirks:
  - base prefixes are recognized only when the string itself starts with `0`; a leading sign prevents `0x` / `0b` recognition,
  - after an exponent marker, this predicate requires the next character to be a digit, so signed exponents are **not** accepted here.
- Returns `1` for accepted text and `0` for most rejected text.

**Errors & validation**
- Some exponent forms can still raise a runtime error instead of returning `0` if exponent evaluation overflows the 64-bit signed range.

**Examples**
- `ISNUMERIC("123")` → `1`
- `ISNUMERIC("12a")` → `0`

## ESCAPE (expression function)

**Summary**
- Escapes a string so it can be used as literal text inside regex-based built-ins.

**Tags**
- text

**Syntax**
- `ESCAPE(str)`

**Signatures / argument rules**
- `ESCAPE(str)` → `string`

**Arguments**
- `str` (string): input text.

**Semantics**
- Equivalent to `.NET` `Regex.Escape(str)`.
- Escapes regex metacharacters so the result matches the original text literally when passed to regex-based built-ins such as `REPLACE` or `STRCOUNT`.

**Errors & validation**
- None.

**Examples**
- `ESCAPE("a+b")` → `"a\+b"`

## ENCODETOUNI (expression function)

**Summary**
- Returns the Unicode scalar value at a UTF-16 position in a string.

**Tags**
- text

**Syntax**
- `ENCODETOUNI(str [, position])`

**Signatures / argument rules**
- `ENCODETOUNI(str)` → `long`
- `ENCODETOUNI(str, position)` → `long`

**Arguments**
- `str` (string): source string.
- `position` (optional, int; default `0`): UTF-16 code-unit index.

**Semantics**
- If `str == ""`, returns `-1` immediately, even if `position` is supplied.
- Otherwise returns `.NET` `char.ConvertToUtf32(str, position)`.
- `position` counts UTF-16 code units, not Unicode scalar values.
- If a supplementary character begins at `position`, the returned value can be greater than `0xFFFF`.
- If `position` points at the second half of a surrogate pair, or at another invalid UTF-16 sequence, conversion fails with a runtime error.

**Errors & validation**
- Runtime error if `str != ""` and `position < 0`.
- Runtime error if `str != ""` and `position >= str.Length`.
- Runtime error if UTF-16 to scalar conversion fails at the requested position.

**Examples**
- `ENCODETOUNI("A")` → `65`

## CHARATU (expression function)

**Summary**
- Returns the single UTF-16 code unit at a given string position.

**Tags**
- text

**Syntax**
- `CHARATU(str, position)`

**Signatures / argument rules**
- `CHARATU(str, position)` → `string`

**Arguments**
- `str` (string): source string.
- `position` (int): UTF-16 code-unit index.

**Semantics**
- If `position < 0` or `position >= str.Length`, returns `""`.
- Otherwise returns `.NET` `str[position].ToString()`.
- Indexing is by UTF-16 code unit, not Unicode scalar value.
- A supplementary character therefore occupies two positions and is **not** returned as one combined character here.

**Errors & validation**
- None.

**Examples**
- `CHARATU("ABC", 1)` → `"B"`

## GETLINESTR (expression function)

**Summary**
- Expands a pattern string to the current drawable width using the same width-fitting rule used by `DRAWLINE`-style output.

**Tags**
- io
- string

**Syntax**
- `GETLINESTR(<pattern>)`

**Signatures / argument rules**
- Signature: `string GETLINESTR(string pattern)`.
- `<pattern>` is evaluated as a string expression.

**Arguments**
- `<pattern>` (string): the pattern string to expand.

**Semantics**
- Evaluates `<pattern>` to a string.
- Returns the width-fitted line string that the runtime would use for a dynamic `DRAWLINE`-style expansion of that pattern:
  - repeat the pattern until the measured display width reaches or exceeds the current drawable width,
  - then trim one character at a time from the end until the measured width is less than or equal to the drawable width.
- The result depends on the current host layout metrics (drawable width and font measurement), so its character count is **not** a stable “one visible line = N characters” value.
- This helper does not print anything and does not modify output state.
- Contract relation:
  - it matches the runtime width-expansion rule used by non-constant `DRAWLINEFORM`,
  - and it matches the already-expanded string produced for `CUSTOMDRAWLINE` / `DRAWLINE`-style line patterns.

**Errors & validation**
- Runtime error if `<pattern>` evaluates to `""`.

**Examples**
```erabasic
S = GETLINESTR("-=")
PRINTL S
```

## STRFORM (expression function)

**Summary**
- Parses a string as FORM / formatted text and returns the expanded result without printing it.

**Tags**
- text

**Syntax**
- `STRFORM(formatSource)`

**Signatures / argument rules**
- `STRFORM(formatSource)` → `string`

**Arguments**
- `formatSource` (string): runtime string to parse as FORM / formatted text.

**Semantics**
- Parses `formatSource` using the same FORM/formatted-string expansion model used by `PRINTFORM`-family text.
- Evaluates embedded substitutions against current runtime state and returns the expanded string.
- No output line is emitted; only the resulting string is returned.
- Parsing stops at the first newline in `formatSource`, matching end-of-line FORM scanning.
- If `formatSource` contains no FORM constructs, the returned string is the same text up to that first newline.

**Errors & validation**
- Runtime error if `formatSource` is not valid FORM/formatted text.
- Runtime error if expansion of an embedded substitution fails.

**Examples**
- `STRFORM("X={1+1}")` → `"X=2"`

## STRJOIN (expression function)

**Summary**
- Joins a slice of an array into one string.

**Tags**
- text

**Syntax**
- `STRJOIN(arrayRef [, delimiter [, start [, count]]])`

**Signatures / argument rules**
- `STRJOIN(arrayRef)` → `string`
- `STRJOIN(arrayRef, delimiter)` → `string`
- `STRJOIN(arrayRef, delimiter, start)` → `string`
- `STRJOIN(arrayRef, delimiter, start, count)` → `string`

**Arguments**
- `arrayRef` (array variable reference): source array to join. May be an int or string array.
- `delimiter` (optional, string; default `","`): separator inserted between items.
- `start` (optional, int; default `0`): first index in the joined slice.
- `count` (optional, int): number of items to join. If omitted, defaults to `lastDimensionLength - start`.

**Semantics**
- `arrayRef` must be an array variable reference, not an array-valued expression.
- Works with 1D, 2D, and 3D arrays:
  - for 1D arrays, joins along that only dimension,
  - for 2D/3D arrays, joins along the **last** dimension while keeping earlier indices fixed by `arrayRef`.
- Omitted `delimiter` uses `","`; explicit `""` is distinct and joins without a separator.
- Omitted `count` is computed as `lastDimensionLength - start` before range validation.
  - If that computed value is negative, the call fails with the normal negative-`count` error.
- Range rules after defaults:
  - `count < 0` is an error,
  - `start` and `start + count` must both satisfy `0 <= value <= lastDimensionLength`.
- Return construction:
  - string-array elements are concatenated as stored,
  - int-array elements are converted with normal decimal `ToString()` before joining.
- If `count == 0`, returns `""`.

**Errors & validation**
- Runtime error if `arrayRef` is not an array variable reference.
- Runtime error if `count < 0`.
- Runtime error if the selected slice is outside the last-dimension bounds.

**Examples**
- If `ARR = ["a", "b", "c"]`, `STRJOIN(ARR, "|", 1, 2)` → `"b|c"`

## GETCONFIG (expression function)

**Summary**
- Looks up a config-like item by name and returns its value in integer form.

**Tags**
- config

**Syntax**
- `GETCONFIG(key)`

**Signatures / argument rules**
- `GETCONFIG(key)` → `long`

**Arguments**
- `key` (string): case-insensitive lookup key.

**Semantics**
- Lookup order is fixed:
  - first config items,
  - then replace items,
  - then debug items.
- Matching is case-insensitive.
- Accepted keys:
  - config items: symbolic name, primary display label, or English display label,
  - replace/debug items: symbolic name or primary display label.
- `GETCONFIG` succeeds only when the resolved item materializes as an integer-like value.
- Integer materialization rules include:
  - booleans → `1` / `0`,
  - colors → `0xRRGGBB`,
  - ordinary integer/long values → that integer,
  - textual values equal to `YES` / `NO` → `1` / `0`,
  - other textual values that parse as decimal integers → that integer.
- If the resolved item materializes as a string-like value, use `GETCONFIGS` instead.

**Errors & validation**
- Runtime error if `key == ""`.
- Runtime error if no matching config/replace/debug item exists.
- Runtime error if the matched item is not available in integer form; the engine tells the caller to use `GETCONFIGS`.

**Examples**
- `size = GETCONFIG("FONTSIZE")`

## GETCONFIGS (expression function)

**Summary**
- Looks up a config-like item by name and returns its value in string form.

**Tags**
- config

**Syntax**
- `GETCONFIGS(key)`

**Signatures / argument rules**
- `GETCONFIGS(key)` → `string`

**Arguments**
- `key` (string): case-insensitive lookup key.

**Semantics**
- Lookup order is fixed:
  - first config items,
  - then replace items,
  - then debug items.
- Matching is case-insensitive.
- Accepted keys:
  - config items: symbolic name, primary display label, or English display label,
  - replace/debug items: symbolic name or primary display label.
- `GETCONFIGS` succeeds only when the resolved item materializes as a string-like value.
- String materialization rules include:
  - ordinary string values → that string,
  - `char` values → a one-character string,
  - `TextDrawingMode` values → the enum-name string,
  - other items whose textual form is neither `YES`/`NO` nor a decimal integer → that textual form.
- If the resolved item materializes as an integer-like value, use `GETCONFIG` instead.

**Errors & validation**
- Runtime error if `key == ""`.
- Runtime error if no matching config/replace/debug item exists.
- Runtime error if the matched item is not available in string form; the engine tells the caller to use `GETCONFIG`.

**Examples**
- `font = GETCONFIGS("FONTNAME")`

## HTML_GETPRINTEDSTR (expression function)

**Summary**
- Returns the HTML-formatted representation of one currently visible **logical output line** in the normal output area.

**Tags**
- io

**Syntax**
- `HTML_GETPRINTEDSTR()`
- `HTML_GETPRINTEDSTR(<lineNo>)`

**Signatures / argument rules**
- Signature: `string HTML_GETPRINTEDSTR(int lineNo = 0)`.
- `<lineNo>` is evaluated as an integer expression.

**Arguments**
- `<lineNo>` (optional, int; default `0`): zero-based index from the newest visible logical line backward.
  - `0` = the most recent currently visible logical output line.
  - `1` = the second most recent currently visible logical output line.
  - Larger values continue counting backward through the currently visible logical lines.

**Semantics**
- Interprets `<lineNo>` as a non-negative index into the current visible **logical-line** history of the normal output area.
- Returns `""` if the requested logical line does not exist.
- The returned HTML is a normalized representation of that visible logical line:
  - it always wraps the line in `<p align='...'><nobr> ... </nobr></p>`,
  - it uses `<br>` between display rows that belong to the same logical line,
  - button segments are represented with `<button ...>` / `<nonbutton ...>` tags (including `title` and `pos` when present),
  - inline images and shapes are represented by their tag-like alt text (for example `<img ...>` / `<shape ...>`),
  - `<div ...>` sub-area elements are omitted.
- This function does not modify the display.
- Layer boundary:
  - pending buffered output is not included,
  - the `HTML_PRINT_ISLAND` layer is not included,
  - while a temporary line remains visible, it can be returned here like any other visible logical line.

**Errors & validation**
- Runtime error if `<lineNo> < 0`.

**Examples**
```erabasic
PRINTL "Hello"
PRINTL "World"
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
- If output is disabled or the pending print buffer is empty, returns `""`.
- Otherwise:
  - converts the current pending print buffer into the same internal display-line structures that normal flushing would use,
  - clears the pending print buffer,
  - returns the converted content as HTML,
  - does **not** append that content to the visible normal output area.
- The returned HTML:
  - preserves structured button/nonbutton regions,
  - uses `<br>` between internal display-row breaks within the flushed buffer,
  - does **not** include outer `<p ...>` / `<nobr>` wrappers, so `ALIGNMENT` is not reflected,
  - omits `<div ...>` sub-area elements.
- Layer boundary:
  - this reads the pending print buffer,
  - it does not read committed visible history,
  - it does not read the `HTML_PRINT_ISLAND` layer.

**Errors & validation**
- None.

**Examples**
```erabasic
PRINT "A"
PRINTBUTTON "[B]", "B"
S = HTML_POPPRINTINGSTR()
; The buffer is now cleared and nothing was added to visible output.
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
- `html` (string): HTML string.

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
- `text` (string): input text.

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
- Returns whether a created sprite currently exists under the given name.

**Tags**
- graphics
- ui
- resources

**Syntax**
- `SPRITECREATED(<spriteName>)`

**Signatures / argument rules**
- Signature: `int SPRITECREATED(string spriteName)`.

**Arguments**
- `<spriteName>` (string): sprite name.

**Semantics**
- Returns `1` if a created sprite exists under `<spriteName>`.
- Returns `0` otherwise.
- Name matching is effectively case-insensitive for lookup/use.

**Errors & validation**
- None.

**Examples**
- `R = SPRITECREATED("ICON")`

## SPRITEWIDTH (expression function)

**Summary**
- Returns the base width of a created sprite.

**Tags**
- graphics
- ui
- resources

**Syntax**
- `SPRITEWIDTH(<spriteName>)`

**Signatures / argument rules**
- Signature: `int SPRITEWIDTH(string spriteName)`.

**Arguments**
- `<spriteName>` (string): sprite name.

**Semantics**
- Returns the sprite's base width.
- If no created sprite exists under that name, returns `0`.
- Name matching is effectively case-insensitive for lookup/use.

**Errors & validation**
- None.

**Examples**
- `W = SPRITEWIDTH("ICON")`

## SPRITEHEIGHT (expression function)

**Summary**
- Returns the base height of a created sprite.

**Tags**
- graphics
- ui
- resources

**Syntax**
- `SPRITEHEIGHT(<spriteName>)`

**Signatures / argument rules**
- Signature: `int SPRITEHEIGHT(string spriteName)`.

**Arguments**
- `<spriteName>` (string): sprite name.

**Semantics**
- Returns the sprite's base height.
- If no created sprite exists under that name, returns `0`.
- Name matching is effectively case-insensitive for lookup/use.

**Errors & validation**
- None.

**Examples**
- `H = SPRITEHEIGHT("ICON")`

## SPRITEMOVE (expression function)

**Summary**
- Offsets the base position of a created sprite by a relative amount.

**Tags**
- graphics
- ui
- resources

**Syntax**
- `SPRITEMOVE(<spriteName>, <dx>, <dy>)`

**Signatures / argument rules**
- Signature: `int SPRITEMOVE(string spriteName, int dx, int dy)`.

**Arguments**
- `<spriteName>` (string): sprite name.
- `<dx>`, `<dy>` (int): relative offset.

**Semantics**
- If a created sprite exists under `<spriteName>`, offsets its current base position by `(<dx>, <dy>)` and returns `1`.
- If no created sprite exists under that name, returns `0` and does nothing.
- Name matching is effectively case-insensitive for lookup/use.
- Layer boundary:
  - this changes later rendering of that sprite,
  - but does not itself print anything or modify the normal output model.

**Errors & validation**
- Runtime error if `<dx>` or `<dy>` is outside the 32-bit signed integer range.

**Examples**
```erabasic
R = SPRITEMOVE("ICON", 8, -4)
```

## SPRITESETPOS (expression function)

**Summary**
- Sets the base position of a created sprite.

**Tags**
- graphics
- ui
- resources

**Syntax**
- `SPRITESETPOS(<spriteName>, <x>, <y>)`

**Signatures / argument rules**
- Signature: `int SPRITESETPOS(string spriteName, int x, int y)`.

**Arguments**
- `<spriteName>` (string): sprite name.
- `<x>`, `<y>` (int): new base position.

**Semantics**
- If a created sprite exists under `<spriteName>`, sets its base position to exactly `(<x>, <y>)` and returns `1`.
- If no created sprite exists under that name, returns `0` and does nothing.
- Name matching is effectively case-insensitive for lookup/use.
- Layer boundary:
  - this changes later rendering of that sprite,
  - but does not itself print anything or modify the normal output model.

**Errors & validation**
- Runtime error if `<x>` or `<y>` is outside the 32-bit signed integer range.

**Examples**
```erabasic
R = SPRITESETPOS("ICON", 100, 50)
```

## SPRITEPOSX (expression function)

**Summary**
- Returns the current base X position of a created sprite.

**Tags**
- graphics
- ui
- resources

**Syntax**
- `SPRITEPOSX(<spriteName>)`

**Signatures / argument rules**
- Signature: `int SPRITEPOSX(string spriteName)`.

**Arguments**
- `<spriteName>` (string): sprite name.

**Semantics**
- Returns the sprite's current base X position.
- If no created sprite exists under that name, returns `0`.
- Name matching is effectively case-insensitive for lookup/use.

**Errors & validation**
- None.

**Examples**
- `X = SPRITEPOSX("ICON")`

## SPRITEPOSY (expression function)

**Summary**
- Returns the current base Y position of a created sprite.

**Tags**
- graphics
- ui
- resources

**Syntax**
- `SPRITEPOSY(<spriteName>)`

**Signatures / argument rules**
- Signature: `int SPRITEPOSY(string spriteName)`.

**Arguments**
- `<spriteName>` (string): sprite name.

**Semantics**
- Returns the sprite's current base Y position.
- If no created sprite exists under that name, returns `0`.
- Name matching is effectively case-insensitive for lookup/use.

**Errors & validation**
- None.

**Examples**
- `Y = SPRITEPOSY("ICON")`

## CLIENTWIDTH (expression function)

**Summary**
- Returns the current width of the game client's drawable picture-box area, in pixels.

**Tags**
- ui

**Syntax**
- `CLIENTWIDTH()`

**Signatures / argument rules**
- `CLIENTWIDTH()` → `long`

**Arguments**
- None.

**Semantics**
- Returns the live width of the current main client drawing surface in pixels.
- This is a runtime UI measurement, not a saved config value.
- The result can change while the program is running if the window/client area is resized.

**Errors & validation**
- None.

**Examples**
- `w = CLIENTWIDTH()`

## CLIENTHEIGHT (expression function)

**Summary**
- Returns the current height of the game client's drawable picture-box area, in pixels.

**Tags**
- ui

**Syntax**
- `CLIENTHEIGHT()`

**Signatures / argument rules**
- `CLIENTHEIGHT()` → `long`

**Arguments**
- None.

**Semantics**
- Returns the live height of the current main client drawing surface in pixels.
- This is a runtime UI measurement, not a saved config value.
- The result can change while the program is running if the window/client area is resized.

**Errors & validation**
- None.

**Examples**
- `h = CLIENTHEIGHT()`

## GETKEY (expression function)

**Summary**
- Polls a Windows virtual-key code and returns whether it is currently down.

**Tags**
- input

**Syntax**
- `GETKEY(keyCode)`

**Signatures / argument rules**
- `GETKEY(keyCode)` → `long`

**Arguments**
- `keyCode` (int): Windows virtual-key code.

**Semantics**
- If the game window is not active, returns `0`.
- If `keyCode < 0` or `keyCode > 255`, returns `0`.
- Otherwise polls Win32 `GetKeyState(keyCode)`.
- Returns `1` if the polled state is currently down (`GetKeyState(keyCode) < 0`), otherwise `0`.
- Poll side effect shared with `GETKEYTRIGGERED`:
  - each call updates the engine's remembered per-key trigger snapshot for that same `keyCode`,
  - so calling `GETKEY` can affect the next `GETKEYTRIGGERED(keyCode)` result.

**Errors & validation**
- None.

**Examples**
- `IF GETKEY(13) != 0`

## GETKEYTRIGGERED (expression function)

**Summary**
- Polls a Windows virtual-key code and returns a one-shot trigger-style result.

**Tags**
- input

**Syntax**
- `GETKEYTRIGGERED(keyCode)`

**Signatures / argument rules**
- `GETKEYTRIGGERED(keyCode)` → `long`

**Arguments**
- `keyCode` (int): Windows virtual-key code.

**Semantics**
- If the game window is not active, returns `0`.
- If `keyCode < 0` or `keyCode > 255`, returns `0`.
- Otherwise polls Win32 `GetKeyState(keyCode)`.
- Returns `1` exactly when both conditions hold:
  - the key is currently down (`GetKeyState(keyCode) < 0`), and
  - the newly observed low-order/toggle-bit-derived snapshot for this `keyCode` differs from the previously remembered snapshot.
- Otherwise returns `0`.
- First-poll behavior:
  - the remembered snapshot starts empty,
  - so a key already down on the first observed poll for that `keyCode` returns `1`.
- Poll side effect shared with `GETKEY`:
  - each call updates the same remembered per-key snapshot used by future trigger checks,
  - so polling either `GETKEY(keyCode)` or `GETKEYTRIGGERED(keyCode)` can affect later `GETKEYTRIGGERED(keyCode)` results.

**Errors & validation**
- None.

**Examples**
- `IF GETKEYTRIGGERED(13) != 0`

## MOUSEX (expression function)

**Summary**
- Returns the current mouse X coordinate in the engine's client-coordinate system.

**Tags**
- ui
- input

**Syntax**
- `MOUSEX()`

**Signatures / argument rules**
- Signature: `int MOUSEX()`.

**Arguments**
- None.

**Semantics**
- Returns the current mouse X coordinate relative to the client area.
- If the main window does not currently exist, returns `0`.
- Coordinate convention:
  - this uses the same client-coordinate conversion used by the engine's mouse event pipeline,
  - X is measured from the left edge.

**Errors & validation**
- None.

**Examples**
- `X = MOUSEX()`

## MOUSEY (expression function)

**Summary**
- Returns the current mouse Y coordinate in the engine's client-coordinate system.

**Tags**
- ui
- input

**Syntax**
- `MOUSEY()`

**Signatures / argument rules**
- Signature: `int MOUSEY()`.

**Arguments**
- None.

**Semantics**
- Returns the current mouse Y coordinate in the engine's converted client-coordinate system.
- If the main window does not currently exist, returns `0`.
- Coordinate convention:
  - this is **not** the raw top-left-based window Y,
  - it uses the engine's shared conversion `clientY - clientHeight`,
  - so values inside the client area are non-positive, and larger on-screen Y values map to larger (less negative) results; the bottom edge is the position closest to `0`.

**Errors & validation**
- None.

**Examples**
- `Y = MOUSEY()`

## MOUSEB (expression function)

**Summary**
- Returns the input value of the currently pointed normal-output button, as a string.

**Tags**
- ui
- input

**Syntax**
- `MOUSEB()`

**Signatures / argument rules**
- Signature: `string MOUSEB()`.

**Arguments**
- None.

**Semantics**
- Recomputes the current hover state from the actual mouse position, then inspects the currently pointed **normal-output button**.
- If the pointed output object is a button:
  - string button → returns its string input,
  - integer button → returns its integer input converted to decimal text.
- Returns `""` if:
  - no normal-output button is currently pointed,
  - the pointed object is not a button.
- Boundary note:
  - this follows the normal output-button hover model,
  - it does **not** expose CBG button-map values,
  - see `cbg-layer.md` for the separate CBG hit-map/value path.

**Errors & validation**
- None.

**Examples**
- `S = MOUSEB()`

## ISACTIVE (expression function)

**Summary**
- Returns whether the game window is currently active.

**Tags**
- ui

**Syntax**
- `ISACTIVE()`

**Signatures / argument rules**
- `ISACTIVE()` → `long`

**Arguments**
- None.

**Semantics**
- Returns `1` if the game window is active.
- Returns `0` if it is inactive.
- This is the same window-activity state that also gates APIs such as `GETKEY*`.

**Errors & validation**
- None.

**Examples**
- `active = ISACTIVE()`

## SAVETEXT (expression function)

**Summary**
- Saves a string either to a numbered text-save slot or to an explicit relative path.

**Tags**
- files
- io

**Syntax**
- `SAVETEXT(text, target [, forceSavdir [, forceUTF8]])`

**Signatures / argument rules**
- `SAVETEXT(text, fileNo)` → `long`
- `SAVETEXT(text, fileNo, forceSavdir)` → `long`
- `SAVETEXT(text, fileNo, forceSavdir, forceUTF8)` → `long`
- `SAVETEXT(text, relativePath)` → `long`
- `SAVETEXT(text, relativePath, forceSavdir)` → `long`
- `SAVETEXT(text, relativePath, forceSavdir, forceUTF8)` → `long`

**Arguments**
- `text` (string): content to write.
- `target` (int or string): numbered save slot or explicit relative path.
- `forceSavdir` (optional, int; default `0`): in numeric-slot mode, non-zero forces the dedicated save-folder path; in explicit-path mode, ignored.
- `forceUTF8` (optional, int; default `0`): legacy compatibility argument with no observable effect in this build.

**Semantics**
- Numeric-slot mode (`target` is int):
  - If `target < 0` or `target > 2147483647`, returns `0`.
  - Resolves the destination filename as `txt{target:00}.txt` in the normal save-text directory, or the forced save-text directory when `forceSavdir != 0`.
  - Creates the chosen destination directory if needed.
- Explicit-path mode (`target` is string):
  - Applies the same safe relative-path normalization used by `EXISTFILE`.
  - If normalization fails, returns `0`.
  - If the path's extension is missing or not present in config item `ValidExtension`, rewrites the extension to `.txt`.
  - Creates any missing parent directories under the resolved path.
  - `forceSavdir` is ignored.
- Writing behavior shared by both modes:
  - writes the exact string content without newline normalization or automatic extra terminators,
  - writes using the runtime save-text encoding; in this build that encoding is UTF-8 with BOM,
  - returns `1` on success and `0` on any failure.

**Errors & validation**
- None; failure paths return `0`.

**Examples**
- `SAVETEXT("hello", 2)`
- `SAVETEXT("hello", "notes/memo.txt")`

## LOADTEXT (expression function)

**Summary**
- Loads text either from a numbered text-save slot or from an explicit relative path.

**Tags**
- files
- io

**Syntax**
- `LOADTEXT(source [, forceSavdir [, forceUTF8]])`

**Signatures / argument rules**
- `LOADTEXT(fileNo)` → `string`
- `LOADTEXT(fileNo, forceSavdir)` → `string`
- `LOADTEXT(fileNo, forceSavdir, forceUTF8)` → `string`
- `LOADTEXT(relativePath)` → `string`
- `LOADTEXT(relativePath, forceSavdir)` → `string`
- `LOADTEXT(relativePath, forceSavdir, forceUTF8)` → `string`

**Arguments**
- `source` (int or string): numbered save slot or explicit relative path.
- `forceSavdir` (optional, int; default `0`): in numeric-slot mode, non-zero forces the dedicated save-folder path; in explicit-path mode, ignored.
- `forceUTF8` (optional, int; default `0`): legacy compatibility argument with no observable effect in this build.

**Semantics**
- Numeric-slot mode (`source` is int):
  - If `source < 0` or `source > 2147483647`, returns `""`.
  - Resolves the source filename as `txt{source:00}.txt` in the normal save-text directory, or the forced save-text directory when `forceSavdir != 0`.
- Explicit-path mode (`source` is string):
  - Applies the same safe relative-path normalization used by `EXISTFILE`.
  - If normalization fails, returns `""`.
  - The path must already have an extension present in config item `ValidExtension`; otherwise returns `""`.
  - `forceSavdir` is ignored.
- Reading behavior shared by both modes:
  - if the resolved file does not exist, returns `""`,
  - reads the entire file,
  - detects encoding as UTF-8 with BOM / UTF-8 when valid, otherwise falls back to Shift-JIS,
  - removes every `
` character from the loaded text before returning it,
  - returns `""` on any failure.

**Errors & validation**
- None; failure paths return `""`.

**Examples**
- `text = LOADTEXT(2)`
- `text = LOADTEXT("notes/memo.txt")`

## GCREATED (expression function)

**Summary**
- Returns whether a graphics surface currently exists at the given graphics ID.

**Tags**
- graphics
- ui

**Syntax**
- `GCREATED(<graphicsId>)`

**Signatures / argument rules**
- Signature: `int GCREATED(int graphicsId)`.

**Arguments**
- `<graphicsId>` (int): graphics-surface ID.

**Semantics**
- Returns `1` if the referenced graphics surface is currently created.
- Returns `0` otherwise.

**Errors & validation**
- Runtime error if the host is using the `WINAPI` text-drawing mode; this method is GDI+-only.
- Runtime error if `<graphicsId> < 0` or `<graphicsId> > 2147483647`.

**Examples**
- `R = GCREATED(GID)`

## GWIDTH (expression function)

**Summary**
- Returns the width of a created graphics surface.

**Tags**
- graphics
- ui

**Syntax**
- `GWIDTH(<graphicsId>)`

**Signatures / argument rules**
- Signature: `int GWIDTH(int graphicsId)`.

**Arguments**
- `<graphicsId>` (int): graphics-surface ID.

**Semantics**
- Returns the width of the referenced graphics surface.
- If the graphics surface is not currently created, returns `0`.

**Errors & validation**
- Runtime error if the host is using the `WINAPI` text-drawing mode; this method is GDI+-only.
- Runtime error if `<graphicsId> < 0` or `<graphicsId> > 2147483647`.

**Examples**
- `W = GWIDTH(GID)`

## GHEIGHT (expression function)

**Summary**
- Returns the height of a created graphics surface.

**Tags**
- graphics
- ui

**Syntax**
- `GHEIGHT(<graphicsId>)`

**Signatures / argument rules**
- Signature: `int GHEIGHT(int graphicsId)`.

**Arguments**
- `<graphicsId>` (int): graphics-surface ID.

**Semantics**
- Returns the height of the referenced graphics surface.
- If the graphics surface is not currently created, returns `0`.

**Errors & validation**
- Runtime error if the host is using the `WINAPI` text-drawing mode; this method is GDI+-only.
- Runtime error if `<graphicsId> < 0` or `<graphicsId> > 2147483647`.

**Examples**
- `H = GHEIGHT(GID)`

## GGETCOLOR (expression function)

**Summary**
- Reads a single pixel from a graphics surface as unsigned ARGB.

**Tags**
- graphics

**Syntax**
- `GGETCOLOR(gID, x, y)`

**Signatures / argument rules**
- `GGETCOLOR(gID, x, y)` → `long`

**Arguments**
- `gID` (int): graphics id.
- `x` (int): pixel x coordinate.
- `y` (int): pixel y coordinate.

**Semantics**
- Returns the pixel color as `0xAARRGGBB` in the range `0 <= value <= 0xFFFFFFFF`.
- If the target graphics does not exist or has already been disposed, returns `-1`.
- If `x < 0`, `x >= width`, or `y >= height`, returns `-1`.
- Bounds-check bug: negative `y` is not rejected by the wrapper; it falls through to the pixel API instead of returning `-1` cleanly.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error when the negative-`y` bug path reaches the underlying pixel API.

**Examples**
- `color = GGETCOLOR(0, 10, 20)`

## SPRITEGETCOLOR (expression function)

**Summary**
- Returns the ARGB color of one pixel in a sprite.

**Tags**
- graphics
- ui
- resources

**Syntax**
- `SPRITEGETCOLOR(<spriteName>, <x>, <y>)`

**Signatures / argument rules**
- Signature: `int SPRITEGETCOLOR(string spriteName, int x, int y)`.

**Arguments**
- `<spriteName>` (string): sprite name.
- `<x>`, `<y>` (int): pixel coordinates in the sprite's base size.

**Semantics**
- If the sprite exists and the point lies inside `0 <= x < width`, `0 <= y < height`, returns that pixel's ARGB value as an unsigned 32-bit pattern carried in an integer return value.
- Returns `-1` if:
  - the sprite does not exist,
  - the sprite is not created,
  - the point is outside the sprite bounds.
- Name matching is effectively case-insensitive for lookup/use.

**Errors & validation**
- Runtime error if `<x>` or `<y>` is outside the 32-bit signed integer range.

**Examples**
```erabasic
C = SPRITEGETCOLOR("ICON", 0, 0)
```

## GCREATE (expression function)

**Summary**
- Creates a graphics surface with the given size at an existing graphics ID handle.

**Tags**
- graphics
- ui

**Syntax**
- `GCREATE(<graphicsId>, <width>, <height>)`

**Signatures / argument rules**
- Signature: `int GCREATE(int graphicsId, int width, int height)`.

**Arguments**
- `<graphicsId>` (int): graphics-surface ID.
- `<width>` (int): surface width.
- `<height>` (int): surface height.

**Semantics**
- Creates a new graphics surface at `<graphicsId>`.
- Success/failure boundary:
  - if that graphics ID already refers to a created graphics surface, returns `0` and does nothing,
  - otherwise creates the surface and returns `1`.
- The created surface is initially blank and becomes available to later `G*` drawing operations.
- Layer boundary:
  - this does not itself print anything or modify the normal output model.

**Errors & validation**
- Runtime error if the host is using the `WINAPI` text-drawing mode; this method is GDI+-only.
- Runtime error if `<graphicsId> < 0` or `<graphicsId> > 2147483647`.
- Runtime error if `<width> <= 0` or `<height> <= 0`.
- Runtime error if `<width>` or `<height>` exceeds the graphics engine's maximum supported image size.

**Examples**
```erabasic
R = GCREATE(GID, 640, 480)
```

## GCREATEFROMFILE (expression function)

**Summary**
- Creates a graphics surface by loading an image file.

**Tags**
- graphics
- ui
- files

**Syntax**
- `GCREATEFROMFILE(<graphicsId>, <filename>)`
- `GCREATEFROMFILE(<graphicsId>, <filename>, <isRelative>)`

**Signatures / argument rules**
- `int GCREATEFROMFILE(int graphicsId, string filename)`
- `int GCREATEFROMFILE(int graphicsId, string filename, int isRelative)`

**Arguments**
- `<graphicsId>` (int): destination graphics-surface ID.
- `<filename>` (string): image path text.
- `<isRelative>` (optional, int; default `0`): path-base mode for non-rooted paths.
  - `0`: resolve non-rooted paths relative to `ContentDir`.
  - non-zero: use the given non-rooted path text as-is.

**Semantics**
- Loads an image file and creates the graphics surface at `<graphicsId>` from that image.
- Success/failure boundary:
  - if that graphics ID already refers to a created graphics surface, returns `0` and does nothing,
  - if the file does not exist, is not loadable as an image, or exceeds the graphics engine's maximum supported image size, returns `0`,
  - otherwise creates the graphics surface from the loaded image and returns `1`.
- Absolute paths are used directly.
- Layer boundary:
  - this does not itself print anything or modify the normal output model.

**Errors & validation**
- Runtime error if the host is using the `WINAPI` text-drawing mode; this method is GDI+-only.
- Runtime error if `<graphicsId> < 0` or `<graphicsId> > 2147483647`.
- Other load failures are reported by returning `0` rather than by a detailed script-visible error code.

**Examples**
```erabasic
R = GCREATEFROMFILE(GID, "face.png")
R = GCREATEFROMFILE(GID, "mods\face.png", 1)
```

## GDISPOSE (expression function)

**Summary**
- Disposes a created graphics surface.

**Tags**
- graphics
- ui

**Syntax**
- `GDISPOSE(<graphicsId>)`

**Signatures / argument rules**
- Signature: `int GDISPOSE(int graphicsId)`.

**Arguments**
- `<graphicsId>` (int): graphics-surface ID.

**Semantics**
- Disposes the graphics surface currently stored at `<graphicsId>`.
- Success/failure boundary:
  - if the graphics surface is not currently created, returns `0`,
  - otherwise disposes it and returns `1`.
- After disposal, the handle may still exist conceptually, but it no longer has a created bitmap/surface.
- Layer boundary:
  - this does not itself print anything or modify the normal output model.

**Errors & validation**
- Runtime error if the host is using the `WINAPI` text-drawing mode; this method is GDI+-only.
- Runtime error if `<graphicsId> < 0` or `<graphicsId> > 2147483647`.

**Examples**
```erabasic
R = GDISPOSE(GID)
```

## GCLEAR (expression function)

**Summary**
- Clears an entire graphics surface, or a clipped rectangle of it, to one color.

**Tags**
- graphics

**Syntax**
- `GCLEAR(gID, cARGB)`
- `GCLEAR(gID, cARGB, x, y, width, height)`

**Signatures / argument rules**
- `GCLEAR(gID, cARGB)` → `long`
- `GCLEAR(gID, cARGB, x, y, width, height)` → `long`

**Arguments**
- `gID` (int): graphics id.
- `cARGB` (int): color in `0xAARRGGBB` form.
- `x` (optional, int): clip-rectangle x coordinate for the six-argument form.
- `y` (optional, int): clip-rectangle y coordinate for the six-argument form.
- `width` (optional, int): clip-rectangle width for the six-argument form.
- `height` (optional, int): clip-rectangle height for the six-argument form.

**Semantics**
- If the target graphics does not exist or has already been disposed, returns `0`.
- Two-argument form clears the entire surface.
- Six-argument form sets a clip rectangle and clears only that clipped region.
- Unlike the rectangle-reading helpers used by other graphics built-ins, the six-argument form performs no wrapper-side range validation on `x`, `y`, `width`, or `height`; each is simply cast to 32-bit integer and passed on.
- On success returns `1`.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error if `cARGB` is outside `0 <= value <= 0xFFFFFFFF`.

**Examples**
- `GCLEAR 0, 0xFFFFFFFF`

## GFILLRECTANGLE (expression function)

**Summary**
- Fills a rectangle on a graphics surface using the current brush.

**Tags**
- graphics

**Syntax**
- `GFILLRECTANGLE(gID, x, y, width, height)`

**Signatures / argument rules**
- `GFILLRECTANGLE(gID, x, y, width, height)` → `long`

**Arguments**
- `gID` (int): graphics id.
- `x` (int): rectangle x coordinate.
- `y` (int): rectangle y coordinate.
- `width` (int): rectangle width.
- `height` (int): rectangle height.

**Semantics**
- If the target graphics does not exist or has already been disposed, returns `0`.
- If no brush has been set with `GSETBRUSH`, fills with `Config.BackColor`.
- Rectangle parsing rejects `width == 0` and `height == 0`, but negative sizes are still forwarded as-is.
- On success returns `1`.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error if any rectangle component is outside signed 32-bit range, or if `width` or `height` is `0`.

**Examples**
- `GFILLRECTANGLE 0, 10, 20, 100, 50`

## GDRAWSPRITE (expression function)

**Summary**
- Draws a sprite resource onto a graphics surface, optionally through a color matrix.

**Tags**
- graphics
- sprites

**Syntax**
- `GDRAWSPRITE(destID, spriteName)`
- `GDRAWSPRITE(destID, spriteName, destX, destY)`
- `GDRAWSPRITE(destID, spriteName, destX, destY, destWidth, destHeight)`
- `GDRAWSPRITE(destID, spriteName, destX, destY, destWidth, destHeight, colorMatrix)`

**Signatures / argument rules**
- `GDRAWSPRITE(destID, spriteName)` → `long`
- `GDRAWSPRITE(destID, spriteName, destX, destY)` → `long`
- `GDRAWSPRITE(destID, spriteName, destX, destY, destWidth, destHeight)` → `long`
- `GDRAWSPRITE(destID, spriteName, destX, destY, destWidth, destHeight, colorMatrix)` → `long`

**Arguments**
- `destID` (int): destination graphics id.
- `spriteName` (string): sprite resource name; lookup is case-insensitive.
- `destX` (optional, int): destination x coordinate.
- `destY` (optional, int): destination y coordinate.
- `destWidth` (optional, int): destination width.
- `destHeight` (optional, int): destination height.
- `colorMatrix` (optional, int 2D/3D array): 5×5 matrix source; values are divided by `256` before being passed to the color-matrix API.

**Semantics**
- If the destination graphics does not exist or has already been disposed, returns `0`.
- If the named sprite does not exist or is not created, returns `0`.
- Two-argument form draws the sprite at `(0, 0)` using the sprite's base destination size.
- Four-argument form draws at `(destX, destY)` using the sprite's base destination size.
- Six-argument form draws into the supplied destination rectangle.
- Seven-argument form behaves like the six-argument form and additionally applies the supplied color matrix.
- Rectangle parsing rejects `width == 0` and `height == 0`, but negative sizes are still forwarded as-is.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `destID` is negative or exceeds 32-bit range.
- Runtime error if any rectangle component is outside signed 32-bit range, or if any rectangle width/height is `0`.
- Runtime error if the referenced color-matrix window does not contain a full 5×5 block.

**Examples**
- `GDRAWSPRITE 0, "ICON", 10, 20`

## GSETCOLOR (expression function)

**Summary**
- Writes a single pixel on a graphics surface.

**Tags**
- graphics

**Syntax**
- `GSETCOLOR(gID, cARGB, x, y)`

**Signatures / argument rules**
- `GSETCOLOR(gID, cARGB, x, y)` → `long`

**Arguments**
- `gID` (int): graphics id.
- `cARGB` (int): color in `0xAARRGGBB` form.
- `x` (int): pixel x coordinate.
- `y` (int): pixel y coordinate.

**Semantics**
- If the target graphics does not exist or has already been disposed, returns `0`.
- If `x < 0`, `x >= width`, or `y >= height`, returns `0`.
- On success writes the pixel and returns `1`.
- Bounds-check bug: negative `y` is not rejected by the wrapper; it falls through to the pixel API instead of returning `0` cleanly.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error if `cARGB` is outside `0 <= value <= 0xFFFFFFFF`.
- Runtime error when the negative-`y` bug path reaches the underlying pixel API.

**Examples**
- `GSETCOLOR 0, 0xFF00FF00, 10, 20`

## GDRAWG (expression function)

**Summary**
- Draws one graphics surface onto another, optionally through a color matrix.

**Tags**
- graphics

**Syntax**
- `GDRAWG(destID, srcID, destX, destY, destWidth, destHeight, srcX, srcY, srcWidth, srcHeight)`
- `GDRAWG(destID, srcID, destX, destY, destWidth, destHeight, srcX, srcY, srcWidth, srcHeight, colorMatrix)`

**Signatures / argument rules**
- `GDRAWG(destID, srcID, destX, destY, destWidth, destHeight, srcX, srcY, srcWidth, srcHeight)` → `long`
- `GDRAWG(destID, srcID, destX, destY, destWidth, destHeight, srcX, srcY, srcWidth, srcHeight, colorMatrix)` → `long`

**Arguments**
- `destID` (int): destination graphics id.
- `srcID` (int): source graphics id.
- `destX` (int): destination rectangle x coordinate.
- `destY` (int): destination rectangle y coordinate.
- `destWidth` (int): destination rectangle width.
- `destHeight` (int): destination rectangle height.
- `srcX` (int): source rectangle x coordinate.
- `srcY` (int): source rectangle y coordinate.
- `srcWidth` (int): source rectangle width.
- `srcHeight` (int): source rectangle height.
- `colorMatrix` (optional, int 2D/3D array): 5×5 matrix source; values are divided by `256` before being passed to the color-matrix API.

**Semantics**
- If either graphics surface does not exist or has already been disposed, returns `0`.
- Otherwise draws the selected source rectangle into the selected destination rectangle and returns `1`.
- Source and destination may be the same graphics surface.
- Rectangle parsing rejects `width == 0` and `height == 0`, but negative sizes are still forwarded as-is.
- Color-matrix lookup rules: for 2D arrays, reads a 5×5 block starting at the referenced indices; for 3D arrays, fixes the first index and reads a 5×5 block from the second / third indices.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if any graphics id is negative or exceeds 32-bit range.
- Runtime error if any rectangle component is outside signed 32-bit range, or if any rectangle width/height is `0`.
- Runtime error if the referenced color-matrix window does not contain a full 5×5 block.

**Examples**
- `GDRAWG 0, 1, 0, 0, 100, 100, 0, 0, 100, 100`

## GDRAWGWITHMASK (expression function)

**Summary**
- Draws one graphics surface onto another using a mask surface as per-pixel opacity.

**Tags**
- graphics

**Syntax**
- `GDRAWGWITHMASK(destID, srcID, maskID, destX, destY)`

**Signatures / argument rules**
- `GDRAWGWITHMASK(destID, srcID, maskID, destX, destY)` → `long`

**Arguments**
- `destID` (int): destination graphics id.
- `srcID` (int): source graphics id.
- `maskID` (int): mask graphics id.
- `destX` (int): destination x coordinate.
- `destY` (int): destination y coordinate.

**Semantics**
- If any of the three graphics surfaces does not exist or has already been disposed, returns `0`.
- If `src` and `mask` sizes differ, returns `0`.
- If `destX + srcWidth > destWidth` or `destY + srcHeight > destHeight`, returns `0`.
- Otherwise uses the blue channel of the mask image as source opacity, composites onto the destination, and returns `1`.
- Negative destination coordinates are not pre-rejected by the wrapper; they fall through to the compositor path instead of producing a clean bounds failure.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if any graphics id is negative or exceeds 32-bit range.
- Runtime error if `destX` or `destY` is outside signed 32-bit range.
- Runtime error when the negative-coordinate path reaches the underlying compositor with invalid indices.

**Examples**
- `GDRAWGWITHMASK 0, 1, 2, 10, 20`

## GSETBRUSH (expression function)

**Summary**
- Sets the current fill brush of a graphics surface to a solid color.

**Tags**
- graphics

**Syntax**
- `GSETBRUSH(gID, cARGB)`

**Signatures / argument rules**
- `GSETBRUSH(gID, cARGB)` → `long`

**Arguments**
- `gID` (int): graphics id.
- `cARGB` (int): color in `0xAARRGGBB` form.

**Semantics**
- If the target graphics does not exist or has already been disposed, returns `0`.
- On success replaces the current brush with a `SolidBrush` of the requested color and returns `1`.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error if `cARGB` is outside `0 <= value <= 0xFFFFFFFF`.

**Examples**
- `GSETBRUSH 0, 0xFF112233`

## GSETFONT (expression function)

**Summary**
- Sets the font used by `GDRAWTEXT` on a graphics surface.

**Tags**
- graphics
- text

**Syntax**
- `GSETFONT(gID, fontName, fontSize [, fontStyle])`

**Signatures / argument rules**
- `GSETFONT(gID, fontName, fontSize)` → `long`
- `GSETFONT(gID, fontName, fontSize, fontStyle)` → `long`

**Arguments**
- `gID` (int): graphics id.
- `fontName` (string): font family name.
- `fontSize` (int): pixel size.
- `fontStyle` (optional, int; default `0`): bitmask `1=bold`, `2=italic`, `4=strikeout`, `8=underline`.

**Semantics**
- If the target graphics does not exist or has already been disposed, returns `0`.
- Tries loaded private font families first, then normal font lookup by name.
- On success stores both the font object and the requested style bitmask, and returns `1`.
- The stored font remains attached to that graphics surface until disposal or the next `GSETFONT`.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Returns `0` if font creation fails.

**Examples**
- `GSETFONT 0, "Arial", 48, 1`

## GSETPEN (expression function)

**Summary**
- Sets the current outline pen of a graphics surface.

**Tags**
- graphics

**Syntax**
- `GSETPEN(gID, cARGB, width)`

**Signatures / argument rules**
- `GSETPEN(gID, cARGB, width)` → `long`

**Arguments**
- `gID` (int): graphics id.
- `cARGB` (int): color in `0xAARRGGBB` form.
- `width` (int): pen width.

**Semantics**
- If the target graphics does not exist or has already been disposed, returns `0`.
- On success replaces the current pen, preserving the previous dash style / dash cap if a pen was already present.
- No wrapper-side validation is performed on `width`; it is passed directly to the pen constructor.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error if `cARGB` is outside `0 <= value <= 0xFFFFFFFF`.
- Runtime error if the underlying pen constructor rejects `width`.

**Examples**
- `GSETPEN 0, 0xFFFF0000, 3`

## SPRITECREATE (expression function)

**Summary**
- Creates or replaces a sprite name by referencing a whole graphics surface or a rectangle crop from it.

**Tags**
- graphics
- ui
- resources

**Syntax**
- `SPRITECREATE(<spriteName>, <graphicsId>)`
- `SPRITECREATE(<spriteName>, <graphicsId>, <x>, <y>, <width>, <height>)`

**Signatures / argument rules**
- `int SPRITECREATE(string spriteName, int graphicsId)`
- `int SPRITECREATE(string spriteName, int graphicsId, int x, int y, int width, int height)`

**Arguments**
- `<spriteName>` (string): sprite name to create/update.
- `<graphicsId>` (int): source graphics-surface ID.
- `<x>`, `<y>`, `<width>`, `<height>` (optional, ints): source rectangle within the graphics surface.

**Semantics**
- Creates a sprite named `<spriteName>` from the source graphics surface.
- Two-argument form:
  - uses the entire source graphics surface.
- Six-argument form:
  - uses the specified source rectangle.
- Success/failure boundary:
  - if a created sprite already exists under `<spriteName>`, returns `0` and leaves it unchanged,
  - if the source graphics surface is not created, returns `0`,
  - otherwise creates/replaces the sprite and returns `1`.
- Rectangle boundary in the six-argument form:
  - the rectangle may extend outside the source bounds,
  - but it must still intersect the source graphics area somewhere,
  - otherwise the call raises a runtime error.
- Name matching is effectively case-insensitive for lookup/use.
- Layer boundary:
  - creating a sprite does not itself draw it or modify the normal output model.

**Errors & validation**
- Runtime error if `<graphicsId> < 0` or `<graphicsId> > 2147483647`.
- Runtime error if any rectangle coordinate/dimension argument is outside the 32-bit signed integer range.
- Runtime error if the six-argument source rectangle does not intersect the source graphics area.

**Examples**
```erabasic
R = SPRITECREATE("ICON", GID)
R = SPRITECREATE("ICON_CROP", GID, 10, 20, 64, 64)
```

## SPRITEDISPOSE (expression function)

**Summary**
- Disposes one sprite by name.

**Tags**
- graphics
- ui
- resources

**Syntax**
- `SPRITEDISPOSE(<spriteName>)`

**Signatures / argument rules**
- Signature: `int SPRITEDISPOSE(string spriteName)`.

**Arguments**
- `<spriteName>` (string): sprite name.

**Semantics**
- If a created sprite exists under `<spriteName>`, disposes it and returns `1`.
- If no created sprite exists under that name, returns `0`.
- Name matching is effectively case-insensitive for lookup/use.
- Layer boundary:
  - disposing a sprite does not itself modify the normal output model,
  - but later rendering that depended on that sprite may stop drawing it.

**Errors & validation**
- None beyond normal string-expression evaluation.

**Examples**
```erabasic
R = SPRITEDISPOSE("ICON")
```

## CBGSETG (expression function)

**Summary**
- Adds a graphics surface to the CBG layer at a given position and depth.

**Tags**
- ui
- graphics

**Syntax**
- `CBGSETG(<graphicsId>, <x>, <y>, <zDepth>)`

**Signatures / argument rules**
- Signature: `int CBGSETG(int graphicsId, int x, int y, int zDepth)`.

**Arguments**
- `<graphicsId>` (int): graphics-surface ID.
- `<x>`, `<y>` (int): CBG placement coordinates.
- `<zDepth>` (int): CBG depth; must be a 32-bit signed integer and must not be `0`.

**Semantics**
- Wraps the referenced graphics surface as a CBG image entry and adds it to the client-background layer at `(<x>, <y>, zDepth)`.
- The registered entry holds a **live reference** to that graphics surface rather than a copied pixel snapshot.
  - Later drawing/mutation of the same `G` surface changes later CBG rendering for this entry.
  - Removing the CBG entry breaks that reference, but does **not** dispose the underlying graphics surface.
- Layer boundary:
  - this affects only the CBG/background layer,
  - it does not modify the normal output model, pending print buffer, or HTML-island layer.
- Success/failure boundary:
  - if the referenced graphics surface is not created or has no bitmap, returns `0` and does not add an entry,
  - otherwise returns `1` after adding the entry.

**Errors & validation**
- Runtime error if the host is using the `WINAPI` text-drawing mode; this method is GDI+-only.
- Runtime error if `<graphicsId> < 0` or `<graphicsId> > 2147483647`.
- Runtime error if `<x>` or `<y>` is outside the 32-bit signed integer range.
- Runtime error if `<zDepth>` is outside the 32-bit signed integer range or equals `0`.

**Examples**
```erabasic
R = CBGSETG(GID, 0, 0, 10)
```

## CBGSETSPRITE (expression function)

**Summary**
- Adds an existing sprite to the CBG layer at a given position and depth.

**Tags**
- ui
- graphics
- resources

**Syntax**
- `CBGSETSPRITE(<spriteName>, <x>, <y>, <zDepth>)`

**Signatures / argument rules**
- Signature: `int CBGSETSPRITE(string spriteName, int x, int y, int zDepth)`.

**Arguments**
- `<spriteName>` (string): sprite name to look up and place on the CBG layer. This call shape does not allow omission; an empty string is still a supplied value.
- `<x>`, `<y>` (int): CBG placement coordinates.
- `<zDepth>` (int): CBG depth; must be a 32-bit signed integer and must not be `0`.

**Semantics**
- Looks up `<spriteName>` in the sprite table and, if it exists and is created, adds that sprite to the client-background layer at `(<x>, <y>, zDepth)`.
- If `<spriteName>` is `""`, the same lookup path is used against that supplied empty name; in the current implementation this returns `0`.
- The registered entry holds a **live reference** to that sprite object rather than a copied snapshot.
  - Later mutation/disposal of that same sprite object changes later CBG rendering for this entry.
- Host-mode quirk:
  - unlike `CBGSETG` / `CBGSETBMAPG` / `CBGSETBUTTONSPRITE`, this call does **not** raise a GDI+-only error in `WINAPI` text-drawing mode,
  - but on this host the ordinary CBG paint path is not active in that mode, so the stored entry normally has no visible CBG effect there.
- Layer boundary:
  - this affects only the CBG/background layer,
  - it does not modify the normal output model, pending print buffer, or HTML-island layer.
- Success/failure boundary:
  - if the sprite does not exist or is not created, returns `0` and does not add an entry,
  - otherwise returns `1` after adding the entry.

**Errors & validation**
- Runtime error if `<x>` or `<y>` is outside the 32-bit signed integer range.
- Runtime error if `<zDepth>` is outside the 32-bit signed integer range or equals `0`.

**Examples**
```erabasic
R = CBGSETSPRITE("BG_ICON", 32, 16, 10)
```

## CBGCLEAR (expression function)

**Summary**
- Clears the entire CBG layer and also clears the current CBG button-hit map.

**Tags**
- ui
- graphics

**Syntax**
- `CBGCLEAR()`

**Signatures / argument rules**
- Signature: `int CBGCLEAR()`.

**Arguments**
- None.

**Semantics**
- Removes all currently registered CBG entries from the client-background layer, including ordinary CBG images and CBG button sprites.
- Also clears the current CBG button-hit map and resets current CBG button selection state.
- Resource-ownership boundary:
  - this clears only the CBG-side registrations/references,
  - it does **not** dispose the underlying named sprite objects or graphics surfaces that had been referenced there.
- Layer boundary:
  - this affects only the CBG/background layer,
  - it does not modify the normal output model, pending print buffer, or HTML-island layer.
- Return value: always returns `1`.

**Errors & validation**
- None.

**Examples**
- `R = CBGCLEAR()`

## CBGCLEARBUTTON (expression function)

**Summary**
- Removes all CBG button sprites and also clears the current CBG button-hit map.

**Tags**
- ui
- graphics

**Syntax**
- `CBGCLEARBUTTON()`

**Signatures / argument rules**
- Signature: `int CBGCLEARBUTTON()`.

**Arguments**
- None.

**Semantics**
- Removes every currently registered **CBG button sprite** from the client-background (`CBG`) layer.
- Also clears the current CBG button-hit map and resets current CBG button selection state.
- Resource-ownership boundary:
  - this removes only the CBG-side button registrations/references,
  - it does **not** dispose the underlying named sprite objects that had been referenced there.
- Layer boundary:
  - this affects only the CBG/background-button layer,
  - it does not modify the normal output model, pending print buffer, or HTML-island layer.
- Observable consequence:
  - any CBG buttons disappear,
  - CBG mouse hit-testing no longer finds those buttons.
- Return value: always returns `1`.

**Errors & validation**
- None.

**Examples**
- `R = CBGCLEARBUTTON()`

## CBGREMOVERANGE (expression function)

**Summary**
- Removes CBG entries whose `zDepth` lies within an inclusive range.

**Tags**
- ui
- graphics

**Syntax**
- `CBGREMOVERANGE(<zMin>, <zMax>)`

**Signatures / argument rules**
- Signature: `int CBGREMOVERANGE(int zMin, int zMax)`.
- Both arguments are evaluated as integer expressions, then converted to 32-bit signed integers by truncation.

**Arguments**
- `<zMin>` (int): inclusive lower bound of the removal range after 32-bit conversion.
- `<zMax>` (int): inclusive upper bound of the removal range after 32-bit conversion.

**Semantics**
- Removes every current CBG entry whose `zDepth` satisfies `zMin <= zDepth <= zMax`.
- The reserved internal depth-`0` dummy entry is never removed.
- If `zMin > zMax`, nothing is removed.
- This operation does **not** clear the current CBG button-hit map.
- Observable consequence:
  - removed CBG images/button sprites disappear,
  - but the hit map and current CBG selection machinery remain installed unless changed separately,
  - and removing an entry severs only the CBG-side reference; it does **not** dispose the underlying sprite/graphics resource.
- Layer boundary:
  - this affects only the CBG/background layer,
  - it does not modify the normal output model, pending print buffer, or HTML-island layer.
- Return value: always returns `1`.

**Errors & validation**
- No explicit range validation is performed after the 32-bit conversion.

**Examples**
- `R = CBGREMOVERANGE(10, 20)`

## CBGREMOVEBMAP (expression function)

**Summary**
- Clears the current CBG button-hit map without removing the CBG button sprites themselves.

**Tags**
- ui
- graphics

**Syntax**
- `CBGREMOVEBMAP()`

**Signatures / argument rules**
- Signature: `int CBGREMOVEBMAP()`.

**Arguments**
- None.

**Semantics**
- Clears the current CBG button-hit map and resets current CBG button selection state.
- It does **not** remove existing CBG button sprites from the visual CBG layer.
- Observable consequence:
  - previously placed CBG button sprites can remain visible,
  - but CBG hit-testing/hover selection no longer finds them until a new button-hit map is installed.
- Layer boundary:
  - this affects only the CBG/background-button interaction state,
  - it does not modify the normal output model, pending print buffer, or HTML-island layer.
- Return value: always returns `1`.

**Errors & validation**
- None.

**Examples**
- `R = CBGREMOVEBMAP()`

## CBGSETBMAPG (expression function)

**Summary**
- Installs a graphics surface as the current CBG button-hit map.

**Tags**
- ui
- graphics

**Syntax**
- `CBGSETBMAPG(<graphicsId>)`

**Signatures / argument rules**
- Signature: `int CBGSETBMAPG(int graphicsId)`.
- `<graphicsId>` is evaluated as an integer expression.

**Arguments**
- `<graphicsId>` (int): graphics-surface ID used as the CBG hit-test map.

**Semantics**
- Selects one graphics surface as the current **CBG button-hit map**.
- The installed hit map is a **live reference** to that graphics surface, not a copied bitmap snapshot.
  - Later drawing/mutation of the same `G` surface changes later CBG hit-testing results.
  - Clearing/replacing the hit map breaks that reference, but does **not** dispose the underlying graphics surface.
- The map is used for CBG mouse hit-testing by reading the pixel under the mouse:
  - if the pixel alpha is `255`, its low 24-bit RGB value becomes the selected CBG button value,
  - otherwise no CBG button is considered selected at that point.
- Layer boundary:
  - this does not add/remove normal output,
  - it only changes CBG-side hit-testing state.
- Success/failure boundary:
  - if the referenced graphics surface is not created (or has no bitmap), the method returns `0` and leaves the current hit map unchanged,
  - otherwise the method returns `1`.
- Compatibility quirk:
  - the public return value does **not** report whether the installed map is actually different from the previous one,
  - so re-setting the same already-installed map still returns `1`.
- Selection-reset boundary:
  - installing a **different** graphics object as the hit map resets current CBG hover/selection state,
  - but re-setting the same already-installed graphics object leaves the existing hit map and current selection state unchanged even though the public return value is still `1`.

**Errors & validation**
- Runtime error if the host is using the `WINAPI` text-drawing mode; this method is GDI+-only.
- Runtime error if `<graphicsId> < 0` or `<graphicsId> > 2147483647`.

**Examples**
```erabasic
R = CBGSETBMAPG(GID)
```

## CBGSETBUTTONSPRITE (expression function)

**Summary**
- Adds one CBG button sprite entry, optionally with a hover/selected sprite and tooltip text.

**Tags**
- ui
- graphics

**Syntax**
- `CBGSETBUTTONSPRITE(<buttonValue>, <normalSprite>, <hoverSprite>, <x>, <y>, <zDepth>)`
- `CBGSETBUTTONSPRITE(<buttonValue>, <normalSprite>, <hoverSprite>, <x>, <y>, <zDepth>, <tooltip>)`

**Signatures / argument rules**
- Signature: `int CBGSETBUTTONSPRITE(int buttonValue, string normalSprite, string hoverSprite, int x, int y, int zDepth, string tooltip = omitted)`.

**Arguments**
- `<buttonValue>` (int): logical CBG button value associated with this sprite.
- `<normalSprite>` (string): sprite name used in the normal state. This call shape does not allow omission; an empty string is still a supplied value.
- `<hoverSprite>` (string): sprite name used while this button value is currently selected by the CBG hit map. This call shape does not allow omission; an empty string is still a supplied value.
- `<x>`, `<y>` (int): CBG placement coordinates.
- `<zDepth>` (int): CBG depth; must be a 32-bit signed integer and must not be `0`.
- `<tooltip>` (optional, string): tooltip text associated with this button sprite.

**Semantics**
- Adds one CBG button sprite entry to the client-background layer.
- The entry is associated with `<buttonValue>`.
- The registered entry holds **live references** to the normal/hover sprite objects rather than copied snapshots.
  - Later mutation/disposal of those same sprite objects changes later CBG rendering for this entry.
- When the current CBG hit map selects that same button value, the runtime draws the hover/selected sprite in place of the normal sprite for this entry.
- If multiple CBG button sprites share the same `<buttonValue>`, they all participate by value rather than by unique object identity.
- Tooltip boundary:
  - the optional tooltip text is stored on the CBG button sprite entry,
  - when this button value is the currently selected CBG value, that tooltip can be surfaced by the host UI,
  - but the standard host tooltip path only does so for selected values greater than `0`, so `buttonValue = 0` still participates in selection/hover-sprite switching without surfacing tooltip text through that standard path.
- Sprite-existence boundary:
  - missing/uncreated sprite names do **not** make the call fail by themselves,
  - the entry is still registered,
  - but an uncreated/missing sprite simply does not draw,
  - an explicit empty string behaves the same way as any other failing lookup here,
  - so if the hover sprite is missing/uncreated, the entry can become invisible while selected.
- Layer boundary:
  - this affects only the CBG/background-button layer,
  - it does not modify the normal output model, pending print buffer, or HTML-island layer.
- Return value:
  - returns `0` if `<buttonValue>` is outside `0 <= value <= 0xFFFFFF`,
  - otherwise returns `1` after registering the entry.

**Errors & validation**
- Runtime error if the host is using the `WINAPI` text-drawing mode; this method is GDI+-only.
- Runtime error if `<x>` or `<y>` is outside the 32-bit signed integer range.
- Runtime error if `<zDepth>` is outside the 32-bit signed integer range or equals `0`.

**Examples**
```erabasic
R = CBGSETBUTTONSPRITE(0x0000FF, "BTN_N", "BTN_H", 100, 40, 10)
R = CBGSETBUTTONSPRITE(0x0000FF, "BTN_N", "BTN_H", 100, 40, 10, "Open")
```

## GSAVE (expression function)

**Summary**
- Saves a created graphics surface to the save directory as a PNG file.

**Tags**
- graphics
- files

**Syntax**
- `GSAVE(gID, fileNo)`

**Signatures / argument rules**
- `GSAVE(gID, fileNo)` → `long`

**Arguments**
- `gID` (int): graphics id.
- `fileNo` (int): save slot number.

**Semantics**
- If the graphics surface does not exist or has already been disposed, returns `0`.
- If `fileNo` is outside `0 <= value <= 2147483647`, returns `0`.
- Otherwise writes the bitmap to `sav/img{fileNo:0000}.png`, creating the save directory if needed, and returns `1` on success.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Returns `0` on file-system or image-save failure.

**Examples**
- `GSAVE 0, 12`

## GLOAD (expression function)

**Summary**
- Loads a saved PNG slot into a not-yet-created graphics surface.

**Tags**
- graphics
- files

**Syntax**
- `GLOAD(gID, fileNo)`

**Signatures / argument rules**
- `GLOAD(gID, fileNo)` → `long`

**Arguments**
- `gID` (int): graphics id.
- `fileNo` (int): save slot number.

**Semantics**
- If the target graphics surface already exists, returns `0` without overwriting it.
- If `fileNo` is outside `0 <= value <= 2147483647`, returns `0`.
- Loads from `sav/img{fileNo:0000}.png`.
- If the file does not exist, cannot be decoded, or exceeds the engine image-size limit, returns `0`.
- On success creates the graphics surface from that image and returns `1`.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Non-`CodeEE` load failures collapse to return value `0`.

**Examples**
- `GLOAD 0, 12`

## SPRITEANIMECREATE (expression function)

**Summary**
- Creates an empty animated sprite resource.

**Tags**
- graphics
- sprites

**Syntax**
- `SPRITEANIMECREATE(spriteName, width, height)`

**Signatures / argument rules**
- `SPRITEANIMECREATE(spriteName, width, height)` → `long`

**Arguments**
- `spriteName` (string): sprite resource name; lookup is case-insensitive.
- `width` (int): animation canvas width.
- `height` (int): animation canvas height.

**Semantics**
- If `spriteName == ""`, returns `0`.
- If a sprite with that name already exists and is created, returns `0`.
- Otherwise creates an empty animated sprite canvas of the requested size and returns `1`.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `width <= 0` or `height <= 0`.
- Runtime error if `width` or `height` exceeds the engine image-size limit.

**Examples**
- `SPRITEANIMECREATE "WALK", 64, 64`

## SPRITEANIMEADDFRAME (expression function)

**Summary**
- Adds one frame to an animated sprite from a rectangle inside a graphics surface.

**Tags**
- graphics
- sprites

**Syntax**
- `SPRITEANIMEADDFRAME(spriteName, gID, x, y, width, height, offsetX, offsetY, delay)`

**Signatures / argument rules**
- `SPRITEANIMEADDFRAME(spriteName, gID, x, y, width, height, offsetX, offsetY, delay)` → `long`

**Arguments**
- `spriteName` (string): target animated-sprite name; lookup is case-insensitive.
- `gID` (int): source graphics id.
- `x` (int): source-rectangle x coordinate.
- `y` (int): source-rectangle y coordinate.
- `width` (int): source-rectangle width.
- `height` (int): source-rectangle height.
- `offsetX` (int): destination offset inside the animation canvas.
- `offsetY` (int): destination offset inside the animation canvas.
- `delay` (int): frame duration in milliseconds.

**Semantics**
- If `spriteName == ""`, returns `0`.
- If no sprite exists with that name, returns `0`.
- If the sprite name resolves to a non-animation sprite, current build follows a null-path bug and errors instead of cleanly returning `0`.
- If the source graphics does not exist or has already been disposed, returns `0`.
- The source rectangle must have positive size and lie fully inside the source graphics; otherwise the function returns `0`.
- If `delay <= 0` or `delay > 2147483647`, returns `0`.
- On success appends a frame and returns `1`.
- Offset clipping quirk: the offset is not rejected when it places the frame partly or wholly outside the animation canvas. The frame is clipped to that canvas and may become visually empty while still consuming its delay time.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error if any point/rectangle coordinate is outside signed 32-bit range, or if `width` or `height` is `0`.

**Examples**
- `SPRITEANIMEADDFRAME "WALK", 0, 0, 0, 32, 32, 16, 16, 100`

## SETANIMETIMER (expression function)

**Summary**
- Configures the redraw timer used for animated sprites during ordinary waits.

**Tags**
- graphics
- sprites

**Syntax**
- `SETANIMETIMER(time)`

**Signatures / argument rules**
- `SETANIMETIMER(time)` → `long`

**Arguments**
- `time` (int): requested redraw interval in milliseconds.

**Semantics**
- Accepts only `time >= -2147483648` and `time <= 32767` in this build.
- If `time <= 0`, disables the redraw timer.
- If `1 <= time < 10`, enables the timer with an actual interval of `10` milliseconds.
- If `time >= 10`, enables the timer with that interval.
- Returns `1`.

**Errors & validation**
- Runtime error if `time < -2147483648` or `time > 32767`.

**Examples**
- `SETANIMETIMER 16`

## OUTPUTLOG (expression function)

**Summary**
- Writes the current retained normal output log to a UTF-8-with-BOM text file under the executable-root directory.

**Tags**
- io
- files

**Syntax**
- `OUTPUTLOG()`
- `OUTPUTLOG(<filename>)`
- `OUTPUTLOG(<filename>, <hideInfo>)`

**Signatures / argument rules**
- Signature: `int OUTPUTLOG(string filename = "", int hideInfo = 0)`.
- `<hideInfo>` is treated as “hide headers” only when it is exactly `1`.

**Arguments**
- `<filename>` (optional, string; default `""`): output path text.
  - If omitted or `""`, the file name is `emuera.log` in the executable-root directory.
  - Otherwise the engine prepends the executable-root directory to the given text as a raw relative-path string.
- `<hideInfo>` (optional, int; default `0`): whether to suppress the environment/title header block.
  - `1`: hide the header block.
  - any other value: include the header block.

**Semantics**
- Exports the current retained **normal output** to a text file encoded as UTF-8 with BOM.
- Log source boundary:
  - it reads only the currently retained normal display-line log,
  - pending buffered output is **not** flushed first and is therefore not included,
  - the separate `HTML_PRINT_ISLAND` layer is not included,
  - debug-output-buffer content is not included.
- Output text is plain text:
  - HTML/button markup is stripped,
  - one retained display row becomes one output file line.
- If `<hideInfo> != 1`, the file begins with environment/title/log header text before the retained output lines.
- Path restriction model:
  - output is restricted to the executable-root directory tree,
  - if the effective path text contains `../`, the call is rejected,
  - if the effective path is judged outside the executable-root tree, the call is rejected.
- On successful file creation while the window exists, the host appends a normal **system line** announcing the created log file.
  - That announcement happens **after** the file has already been written, so the just-written file does not contain its own success message.
  - Because that success path uses the normal system-line path, any pending print buffer may become visible on screen at that point even though it was not included in the file.
- Return value:
  - returns `1` after the method call completes,
  - this return value does **not** distinguish success from failure.
  - Failure is instead signaled by host dialog/error UI and by the absence of the success system line.

**Errors & validation**
- Invalid path destinations are rejected by host error UI.
- File-write failures are rejected by host error UI.
- No exception-style success/failure code is exposed through the return value.

**Examples**
```erabasic
R = OUTPUTLOG()
R = OUTPUTLOG("logs\\scene.txt", 1)
```

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
- `html` (string): HTML string.
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
- `html` (string): HTML string.
- `width` (int): width in half-width character units.

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
- `html` (string): HTML string.
- `width` (int): width in half-width character units.

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
- Tests whether a file exists under the executable directory using the engine's safe relative-path normalization.

**Tags**
- files

**Syntax**
- `EXISTFILE(relativePath)`

**Signatures / argument rules**
- `EXISTFILE(relativePath)` → `long`

**Arguments**
- `relativePath` (string): file path relative to the executable directory.

**Semantics**
- Normalizes the supplied path before checking:
  - `/` is converted to `\`,
  - literal parent-directory segments `..\` are stripped,
  - rooted / absolute paths are rejected.
- The resulting relative path is resolved under the executable directory.
- Returns `1` if the resolved path exists and is a file.
- Returns `0` if normalization fails or the resolved file does not exist.
- This API does **not** apply the `LOADTEXT` / `SAVETEXT` extension allow-list.

**Errors & validation**
- None.

**Examples**
- `EXISTFILE("csv/VariableSize.csv")` → `1` when that file exists

## EXISTVAR (expression function)

**Summary**
- Tests whether a bare variable name resolves, and returns a bitmask describing its declared shape/type.

**Tags**
- reflection

**Syntax**
- `EXISTVAR(name)`

**Signatures / argument rules**
- `EXISTVAR(name)` → `long`

**Arguments**
- `name` (string): bare variable name.

**Semantics**
- Resolves `name` as a variable token, not as a full variable-term expression.
  - Subscripted strings such as `A:0` are not parsed here.
- Scope lookup follows the runtime's normal variable-token rules:
  - current private variable first,
  - then local variable,
  - then global/system variable.
- Returns `0` if no variable token is found.
- Otherwise returns a bitmask with these flags:
  - `1`: integer-typed
  - `2`: string-typed
  - `4`: const
  - `8`: 2D array
  - `16`: 3D array
- No flag distinguishes scalar from 1D array.
- No flag distinguishes ordinary variables from character-data variables.

**Errors & validation**
- Some names can still raise runtime errors instead of returning `0` when normal variable-token lookup would reject them, for example prohibited variables or local/private lookups with no valid current function context.

**Examples**
- `mask = EXISTVAR("TARGET")`

## ISDEFINED (expression function)

**Summary**
- Tests whether a macro is currently defined.

**Tags**
- reflection

**Syntax**
- `ISDEFINED(name)`

**Signatures / argument rules**
- `ISDEFINED(name)` → `long`

**Arguments**
- `name` (string): macro name.

**Semantics**
- Returns `1` if a macro with that name exists in the current macro table.
- Returns `0` otherwise.
- This function checks macros only. It does not test variables, labels, or methods.
- Name matching follows the runtime's normal macro-lookup rules.

**Errors & validation**
- None.

**Examples**
- `ISDEFINED("MY_MACRO")`

## ENUMFUNCBEGINSWITH (expression function)

**Summary**
        - Enumerates user-defined non-event label/method names from loaded scripts whose names begins with the given keyword.

        **Tags**
        - reflection

        **Syntax**
        - `ENUMFUNCBEGINSWITH(keyword [, output])`

        **Signatures / argument rules**
        - `ENUMFUNCBEGINSWITH(keyword)` → `long`
        - `ENUMFUNCBEGINSWITH(keyword, output)` → `long`

        **Arguments**
        - `keyword` (string): case-insensitive match key.
        - `output` (optional, 1D string-array variable reference; default `RESULTS:*`): destination for copied names.

        **Semantics**
        - Matching is case-insensitive.
        - If `keyword == ""`, returns `0` and writes nothing.
        - Function enumeration uses the current non-event script label table.
- Built-in expression functions are not included.
        - Match rule:
          - `ENUMFUNCBEGINSWITH` selects names whose uppercase form begins with `keyword`'s uppercase form.
        - Output destination:
          - if `output` is omitted, matched names are copied into `RESULTS:*`,
          - otherwise they are copied into the provided 1D string array.
        - Return value is the number of names actually copied.
          - This is `min(matchCount, destinationLength)`, not the total number of matches when truncation occurs.
        - The destination is **not** cleared beyond the copied prefix.
        - Matched names are emitted in the engine's current enumeration order; this implementation does not sort them.

        **Errors & validation**
        - Argument type/count errors are rejected by the engine's function-method argument checker.

        **Examples**
        - `ENUMFUNCBEGINSWITH("TEST")`

        **Progress state**
        - complete

**Syntax**
- (TODO)

**Signatures / argument rules**
- (TODO)

**Arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

## ENUMFUNCENDSWITH (expression function)

**Summary**
        - Enumerates user-defined non-event label/method names from loaded scripts whose names ends with the given keyword.

        **Tags**
        - reflection

        **Syntax**
        - `ENUMFUNCENDSWITH(keyword [, output])`

        **Signatures / argument rules**
        - `ENUMFUNCENDSWITH(keyword)` → `long`
        - `ENUMFUNCENDSWITH(keyword, output)` → `long`

        **Arguments**
        - `keyword` (string): case-insensitive match key.
        - `output` (optional, 1D string-array variable reference; default `RESULTS:*`): destination for copied names.

        **Semantics**
        - Matching is case-insensitive.
        - If `keyword == ""`, returns `0` and writes nothing.
        - Function enumeration uses the current non-event script label table.
- Built-in expression functions are not included.
        - Match rule:
          - `ENUMFUNCENDSWITH` selects names whose uppercase form ends with `keyword`'s uppercase form.
        - Output destination:
          - if `output` is omitted, matched names are copied into `RESULTS:*`,
          - otherwise they are copied into the provided 1D string array.
        - Return value is the number of names actually copied.
          - This is `min(matchCount, destinationLength)`, not the total number of matches when truncation occurs.
        - The destination is **not** cleared beyond the copied prefix.
        - Matched names are emitted in the engine's current enumeration order; this implementation does not sort them.

        **Errors & validation**
        - Argument type/count errors are rejected by the engine's function-method argument checker.

        **Examples**
        - `ENUMFUNCENDSWITH("TEST")`

        **Progress state**
        - complete

**Syntax**
- (TODO)

**Signatures / argument rules**
- (TODO)

**Arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

## ENUMFUNCWITH (expression function)

**Summary**
        - Enumerates user-defined non-event label/method names from loaded scripts whose names contains the given keyword.

        **Tags**
        - reflection

        **Syntax**
        - `ENUMFUNCWITH(keyword [, output])`

        **Signatures / argument rules**
        - `ENUMFUNCWITH(keyword)` → `long`
        - `ENUMFUNCWITH(keyword, output)` → `long`

        **Arguments**
        - `keyword` (string): case-insensitive match key.
        - `output` (optional, 1D string-array variable reference; default `RESULTS:*`): destination for copied names.

        **Semantics**
        - Matching is case-insensitive.
        - If `keyword == ""`, returns `0` and writes nothing.
        - Function enumeration uses the current non-event script label table.
- Built-in expression functions are not included.
        - Match rule:
          - `ENUMFUNCWITH` selects names whose uppercase form contains `keyword`'s uppercase form.
        - Output destination:
          - if `output` is omitted, matched names are copied into `RESULTS:*`,
          - otherwise they are copied into the provided 1D string array.
        - Return value is the number of names actually copied.
          - This is `min(matchCount, destinationLength)`, not the total number of matches when truncation occurs.
        - The destination is **not** cleared beyond the copied prefix.
        - Matched names are emitted in the engine's current enumeration order; this implementation does not sort them.

        **Errors & validation**
        - Argument type/count errors are rejected by the engine's function-method argument checker.

        **Examples**
        - `ENUMFUNCWITH("TEST")`

        **Progress state**
        - complete

**Syntax**
- (TODO)

**Signatures / argument rules**
- (TODO)

**Arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

## ENUMVARBEGINSWITH (expression function)

**Summary**
        - Enumerates global/system variable names whose names begins with the given keyword.

        **Tags**
        - reflection

        **Syntax**
        - `ENUMVARBEGINSWITH(keyword [, output])`

        **Signatures / argument rules**
        - `ENUMVARBEGINSWITH(keyword)` → `long`
        - `ENUMVARBEGINSWITH(keyword, output)` → `long`

        **Arguments**
        - `keyword` (string): case-insensitive match key.
        - `output` (optional, 1D string-array variable reference; default `RESULTS:*`): destination for copied names.

        **Semantics**
        - Matching is case-insensitive.
        - If `keyword == ""`, returns `0` and writes nothing.
        - Variable enumeration uses the global/system variable table.
- Local variables and private variables are not included.
        - Match rule:
          - `ENUMVARBEGINSWITH` selects names whose uppercase form begins with `keyword`'s uppercase form.
        - Output destination:
          - if `output` is omitted, matched names are copied into `RESULTS:*`,
          - otherwise they are copied into the provided 1D string array.
        - Return value is the number of names actually copied.
          - This is `min(matchCount, destinationLength)`, not the total number of matches when truncation occurs.
        - The destination is **not** cleared beyond the copied prefix.
        - Matched names are emitted in the engine's current enumeration order; this implementation does not sort them.

        **Errors & validation**
        - Argument type/count errors are rejected by the engine's function-method argument checker.

        **Examples**
        - `ENUMVARBEGINSWITH("TEST")`

        **Progress state**
        - complete

**Syntax**
- (TODO)

**Signatures / argument rules**
- (TODO)

**Arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

## ENUMVARENDSWITH (expression function)

**Summary**
        - Enumerates global/system variable names whose names ends with the given keyword.

        **Tags**
        - reflection

        **Syntax**
        - `ENUMVARENDSWITH(keyword [, output])`

        **Signatures / argument rules**
        - `ENUMVARENDSWITH(keyword)` → `long`
        - `ENUMVARENDSWITH(keyword, output)` → `long`

        **Arguments**
        - `keyword` (string): case-insensitive match key.
        - `output` (optional, 1D string-array variable reference; default `RESULTS:*`): destination for copied names.

        **Semantics**
        - Matching is case-insensitive.
        - If `keyword == ""`, returns `0` and writes nothing.
        - Variable enumeration uses the global/system variable table.
- Local variables and private variables are not included.
        - Match rule:
          - `ENUMVARENDSWITH` selects names whose uppercase form ends with `keyword`'s uppercase form.
        - Output destination:
          - if `output` is omitted, matched names are copied into `RESULTS:*`,
          - otherwise they are copied into the provided 1D string array.
        - Return value is the number of names actually copied.
          - This is `min(matchCount, destinationLength)`, not the total number of matches when truncation occurs.
        - The destination is **not** cleared beyond the copied prefix.
        - Matched names are emitted in the engine's current enumeration order; this implementation does not sort them.

        **Errors & validation**
        - Argument type/count errors are rejected by the engine's function-method argument checker.

        **Examples**
        - `ENUMVARENDSWITH("TEST")`

        **Progress state**
        - complete

**Syntax**
- (TODO)

**Signatures / argument rules**
- (TODO)

**Arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

## ENUMVARWITH (expression function)

**Summary**
        - Enumerates global/system variable names whose names contains the given keyword.

        **Tags**
        - reflection

        **Syntax**
        - `ENUMVARWITH(keyword [, output])`

        **Signatures / argument rules**
        - `ENUMVARWITH(keyword)` → `long`
        - `ENUMVARWITH(keyword, output)` → `long`

        **Arguments**
        - `keyword` (string): case-insensitive match key.
        - `output` (optional, 1D string-array variable reference; default `RESULTS:*`): destination for copied names.

        **Semantics**
        - Matching is case-insensitive.
        - If `keyword == ""`, returns `0` and writes nothing.
        - Variable enumeration uses the global/system variable table.
- Local variables and private variables are not included.
        - Match rule:
          - `ENUMVARWITH` selects names whose uppercase form contains `keyword`'s uppercase form.
        - Output destination:
          - if `output` is omitted, matched names are copied into `RESULTS:*`,
          - otherwise they are copied into the provided 1D string array.
        - Return value is the number of names actually copied.
          - This is `min(matchCount, destinationLength)`, not the total number of matches when truncation occurs.
        - The destination is **not** cleared beyond the copied prefix.
        - Matched names are emitted in the engine's current enumeration order; this implementation does not sort them.

        **Errors & validation**
        - Argument type/count errors are rejected by the engine's function-method argument checker.

        **Examples**
        - `ENUMVARWITH("TEST")`

        **Progress state**
        - complete

**Syntax**
- (TODO)

**Signatures / argument rules**
- (TODO)

**Arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

## ENUMMACROBEGINSWITH (expression function)

**Summary**
- Enumerates macro names whose names begins with the given keyword.

**Tags**
- reflection

**Syntax**
- `ENUMMACROBEGINSWITH(keyword [, output])`

**Signatures / argument rules**
- `ENUMMACROBEGINSWITH(keyword)` → `long`
- `ENUMMACROBEGINSWITH(keyword, output)` → `long`

**Arguments**
- `keyword` (string): case-insensitive match key.
- `output` (optional, 1D string-array variable reference; default `RESULTS:*`): destination for copied names.

**Semantics**
- Matching is case-insensitive.
- If `keyword == ""`, returns `0` and writes nothing.
- Macro enumeration uses the current macro table.
- Match rule:
  - `ENUMMACROBEGINSWITH` selects names whose uppercase form begins with `keyword`'s uppercase form.
- Output destination:
  - if `output` is omitted, matched names are copied into `RESULTS:*`,
  - otherwise they are copied into the provided 1D string array.
- Return value is the number of names actually copied.
  - This is `min(matchCount, destinationLength)`, not the total number of matches when truncation occurs.
- The destination is **not** cleared beyond the copied prefix.
- Matched names are emitted in the engine's current enumeration order; this implementation does not sort them.

**Errors & validation**
- Argument type/count errors are rejected by the engine's function-method argument checker.

**Examples**
- `ENUMMACROBEGINSWITH("TEST")`

## ENUMMACROENDSWITH (expression function)

**Summary**
- Enumerates macro names whose names ends with the given keyword.

**Tags**
- reflection

**Syntax**
- `ENUMMACROENDSWITH(keyword [, output])`

**Signatures / argument rules**
- `ENUMMACROENDSWITH(keyword)` → `long`
- `ENUMMACROENDSWITH(keyword, output)` → `long`

**Arguments**
- `keyword` (string): case-insensitive match key.
- `output` (optional, 1D string-array variable reference; default `RESULTS:*`): destination for copied names.

**Semantics**
- Matching is case-insensitive.
- If `keyword == ""`, returns `0` and writes nothing.
- Macro enumeration uses the current macro table.
- Match rule:
  - `ENUMMACROENDSWITH` selects names whose uppercase form ends with `keyword`'s uppercase form.
- Output destination:
  - if `output` is omitted, matched names are copied into `RESULTS:*`,
  - otherwise they are copied into the provided 1D string array.
- Return value is the number of names actually copied.
  - This is `min(matchCount, destinationLength)`, not the total number of matches when truncation occurs.
- The destination is **not** cleared beyond the copied prefix.
- Matched names are emitted in the engine's current enumeration order; this implementation does not sort them.

**Errors & validation**
- Argument type/count errors are rejected by the engine's function-method argument checker.

**Examples**
- `ENUMMACROENDSWITH("TEST")`

## ENUMMACROWITH (expression function)

**Summary**
- Enumerates macro names whose names contains the given keyword.

**Tags**
- reflection

**Syntax**
- `ENUMMACROWITH(keyword [, output])`

**Signatures / argument rules**
- `ENUMMACROWITH(keyword)` → `long`
- `ENUMMACROWITH(keyword, output)` → `long`

**Arguments**
- `keyword` (string): case-insensitive match key.
- `output` (optional, 1D string-array variable reference; default `RESULTS:*`): destination for copied names.

**Semantics**
- Matching is case-insensitive.
- If `keyword == ""`, returns `0` and writes nothing.
- Macro enumeration uses the current macro table.
- Match rule:
  - `ENUMMACROWITH` selects names whose uppercase form contains `keyword`'s uppercase form.
- Output destination:
  - if `output` is omitted, matched names are copied into `RESULTS:*`,
  - otherwise they are copied into the provided 1D string array.
- Return value is the number of names actually copied.
  - This is `min(matchCount, destinationLength)`, not the total number of matches when truncation occurs.
- The destination is **not** cleared beyond the copied prefix.
- Matched names are emitted in the engine's current enumeration order; this implementation does not sort them.

**Errors & validation**
- Argument type/count errors are rejected by the engine's function-method argument checker.

**Examples**
- `ENUMMACROWITH("TEST")`

## ENUMFILES (expression function)

**Summary**
- Enumerates files under a relative directory using a wildcard pattern.

**Tags**
- files

**Syntax**
- `ENUMFILES(dir [, pattern [, recursive [, output]]])`

**Signatures / argument rules**
- `ENUMFILES(dir)` → `long`
- `ENUMFILES(dir, pattern)` → `long`
- `ENUMFILES(dir, pattern, recursive)` → `long`
- `ENUMFILES(dir, pattern, recursive, output)` → `long`

**Arguments**
- `dir` (string): directory path relative to the executable directory.
- `pattern` (optional, string; default `"*"`): filesystem wildcard pattern.
- `recursive` (optional, int; default `0`): non-zero enables recursive enumeration.
- `output` (optional, 1D string-array variable reference; default `RESULTS:*`): destination for copied relative paths.

**Semantics**
- Resolves `dir` using the same safe relative-path normalization used by `EXISTFILE`.
- Returns `-1` if normalization fails or the resolved directory does not exist.
- Enumerates files using the host filesystem's wildcard matching rules.
- If `recursive == 0`, searches only the top directory.
- If `recursive != 0`, searches all subdirectories.
- Every returned path is converted back to a path relative to the executable directory.
- Output destination:
  - if `output` is omitted, copied paths go to `RESULTS:*`,
  - otherwise they go to the provided 1D string array.
- Return value is the number of paths actually copied.
  - This is `min(foundCount, destinationLength)`, not the total number of matches when truncation occurs.
- The destination is not cleared beyond the copied prefix.
- Returns `-1` if enumeration throws.

**Errors & validation**
- Argument type/count errors are rejected by the engine's function-method argument checker.

**Examples**
- `count = ENUMFILES("csv", "*.csv", 1)`

## GETVAR (expression function)

**Summary**
- Parses a string as an integer variable term and returns its current value.

**Tags**
- reflection

**Syntax**
- `GETVAR(varExpr)`

**Signatures / argument rules**
- `GETVAR(varExpr)` → `long`

**Arguments**
- `varExpr` (string): text that must parse to an integer variable term.

**Semantics**
- Re-parses `varExpr` at runtime using the normal expression parser.
- `varExpr` must reduce to a variable term.
- Constants are allowed.
- Array elements are allowed if `varExpr` includes valid subscripts.
- Scope-sensitive names (for example locals/private variables) follow the current runtime context exactly as if the same variable term had appeared directly in script code.

**Errors & validation**
- Runtime error if `varExpr` does not parse to a variable term.
- Runtime error if the resolved term is not integer-typed.
- Runtime error if normal variable evaluation of that term fails.

**Examples**
- `value = GETVAR("TARGET")`
- `value = GETVAR("ARRAY:3")`

## GETVARS (expression function)

**Summary**
- Parses a string as a string variable term and returns its current value.

**Tags**
- reflection

**Syntax**
- `GETVARS(varExpr)`

**Signatures / argument rules**
- `GETVARS(varExpr)` → `string`

**Arguments**
- `varExpr` (string): text that must parse to a string variable term.

**Semantics**
- Re-parses `varExpr` at runtime using the normal expression parser.
- `varExpr` must reduce to a variable term.
- Constants are allowed.
- Array elements are allowed if `varExpr` includes valid subscripts.
- Scope-sensitive names (for example locals/private variables) follow the current runtime context exactly as if the same variable term had appeared directly in script code.

**Errors & validation**
- Runtime error if `varExpr` does not parse to a variable term.
- Runtime error if the resolved term is not string-typed.
- Runtime error if normal variable evaluation of that term fails.

**Examples**
- `text = GETVARS("TARGETS")`
- `text = GETVARS("NAMES:3")`

## SETVAR (expression function)

**Summary**
- Parses a string as a writable variable term and assigns one value to it.

**Tags**
- reflection

**Syntax**
- `SETVAR(varExpr, value)`

**Signatures / argument rules**
- `SETVAR(varExpr, value)` → `long`

**Arguments**
- `varExpr` (string): text that must parse to a writable variable term.
- `value` (int|string): value to assign; its type must match the resolved variable type.

**Semantics**
- Re-parses `varExpr` at runtime using the normal expression parser.
- `varExpr` must reduce to a non-const variable term.
- The assignment target can be a scalar variable or one addressed array element.
- If the resolved target is string-typed, `value` must be string-typed.
- If the resolved target is integer-typed, `value` must be integer-typed.
- Returns `1` after a successful assignment.

**Errors & validation**
- Runtime error if `varExpr` does not parse to a writable variable term.
- Runtime error if the resolved target is const.
- Runtime error if `value` has the wrong type for the resolved target.
- Runtime error if normal target evaluation/assignment fails.

**Examples**
- `SETVAR("TARGET", 5)`
- `SETVAR("NAMES:3", "Alice")`

## VARSETEX (expression function)

**Summary**
- Parses a string as a variable term and bulk-writes a value across a last-dimension slice.

**Tags**
- reflection

**Syntax**
- `VARSETEX(varExpr, value [, setAllDims [, from [, to]]])`

**Signatures / argument rules**
- `VARSETEX(varExpr, value)` → `long`
- `VARSETEX(varExpr, value, setAllDims)` → `long`
- `VARSETEX(varExpr, value, setAllDims, from)` → `long`
- `VARSETEX(varExpr, value, setAllDims, from, to)` → `long`

**Arguments**
- `varExpr` (string): text that must parse to a writable variable term.
- `value` (int|string): fill value; its type must match the resolved variable type.
- `setAllDims` (optional, int; default `1`): for integer 2D/3D arrays, non-zero fills all leading-dimension slices; `0` fills only the currently addressed slice.
- `from` (optional, int; default `0`): inclusive start position on the last dimension.
- `to` (optional, int): exclusive end position on the last dimension.

**Semantics**
- Re-parses `varExpr` at runtime using the normal expression parser.
- `varExpr` must reduce to a non-const variable term.
- Type rule:
  - string targets require string `value`,
  - integer targets require integer `value`.
- Scalar-target quirk:
  - if `varExpr` resolves to a scalar variable rather than an array/slice, this function performs no write and still returns `1`.
- Range defaults:
  - omitted `from` defaults to `0`,
  - omitted `to` defaults to the last-dimension length for 1D arrays,
  - omitted `to` defaults to dimension-1 length for 2D arrays,
  - omitted `to` defaults to `0` for 3D arrays in this build.
- The effective loop start is floored by any already-specified last-dimension index embedded inside `varExpr`.
  - In other words, writes begin at `max(from, embeddedLastDimIndex)`.
- Write behavior by target kind:
  - 1D arrays: fills the selected `[from, to)` slice.
  - Integer 2D/3D arrays with `setAllDims != 0`: fills every leading-dimension slice over the selected last-dimension range.
  - Integer 2D/3D arrays with `setAllDims == 0`: fills only the currently addressed leading-dimension slice.
  - String 2D/3D arrays: `setAllDims` is ignored; only the currently addressed slice is filled.
- If the effective start is greater than or equal to `to`, no elements are written and the function still returns `1`.
- Returns `1` whenever the operation completes without a runtime error.

**Errors & validation**
- Runtime error if `varExpr` does not parse to a writable variable term.
- Runtime error if the resolved target is const.
- Runtime error if `value` has the wrong type for the resolved target.
- Runtime error if array access goes out of range during the write loop.

**Examples**
- `VARSETEX("ARR", -1, 0, 3, 5)`
- `VARSETEX("NAMES", "dog")`

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
  - 1D arrays: permutes elements `0 <= i < n`
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
- Counts regex matches and can optionally expose captured group values.

**Tags**
- text
- reflection

**Syntax**
- `REGEXPMATCH(str, pattern [, outputFlag])`
- `REGEXPMATCH(str, pattern, groupCount, matches)`

**Signatures / argument rules**
- `REGEXPMATCH(str, pattern)` → `long`
- `REGEXPMATCH(str, pattern, outputFlag)` → `long`
- `REGEXPMATCH(str, pattern, groupCount, matches)` → `long`

**Arguments**
- `str` (string): target string.
- `pattern` (string): regular-expression pattern.
- `outputFlag` (optional, int; default `0`): when non-zero, writes capture output into `RESULTS:*` and writes group count into `RESULT:1`.
- `groupCount` (ref int): destination for the number of regex groups.
- `matches` (ref 1D string array): destination for flattened group outputs.

**Semantics**
- Compiles `pattern` as a `.NET` regular expression with default options.
- Returns the number of matches in `str`.
- Group-count rule:
  - the reported group count is `.NET` `Regex.GetGroupNumbers().Length`,
  - this includes group `0` (the whole match).
- Output modes:
  - if `outputFlag != 0`, writes the group count to `RESULT:1` and writes flattened match/group values to `RESULTS:*`,
  - if `groupCount, matches` references are supplied, writes the group count to `groupCount` and flattened values to `matches`.
- Flattening order:
  - iterate matches in match order,
  - for each match, iterate groups in `.NET` `Regex.GetGroupNames()` order,
  - append each `match.Groups[name].Value`.
- Output truncation/retention:
  - flattened output stops when the destination string array is full,
  - any remaining output is discarded,
  - destination entries beyond the copied prefix are not cleared,
  - if there are no matches, the string destination is left unchanged.

**Errors & validation**
- Runtime error if `pattern` is not a valid regular expression.

**Examples**
- `count = REGEXPMATCH("Apple Banana Car", ".(.{2})\b")`

## XML_DOCUMENT (expression function)

**Summary**
- Creates a stored XML document under a key.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_DOCUMENT(xmlId, xmlContent)`

**Signatures / argument rules**
- `XML_DOCUMENT(xmlId, xmlContent)` → `long`

**Arguments**
- `xmlId` (int|string): storage key; integer values are converted to decimal strings.
- `xmlContent` (string): XML text to parse and store.

**Semantics**
- Uses the process-local stored-document table shared by the `XML_*` built-ins.
- If a document already exists for the resolved key, returns `0` and leaves that document unchanged.
- Otherwise parses `xmlContent`, stores the resulting document under the key, and returns `1`.

**Errors & validation**
- Runtime error if `xmlContent` is not well-formed XML.

**Examples**
- `XML_DOCUMENT("menu", "<root/>")`

## XML_RELEASE (expression function)

**Summary**
- Removes a stored XML document by key.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_RELEASE(xmlId)`

**Signatures / argument rules**
- `XML_RELEASE(xmlId)` → `long`

**Arguments**
- `xmlId` (int|string): storage key; integer values are converted to decimal strings.

**Semantics**
- If a document exists for the resolved key, it is removed and the function returns `1`.
- If no document exists for that key, the function returns `0`.

**Errors & validation**
- None.

**Examples**
- `XML_RELEASE(0)`

## XML_GET (expression function)

**Summary**
- Selects XML nodes and optionally copies their projected values to a string array.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_GET(xmlOrId, xpath [, doOutput [, outputType]])`
- `XML_GET(xmlOrId, xpath, outputArray [, outputType])`

**Signatures / argument rules**
- `XML_GET(xmlOrId, xpath)` → `long`
- `XML_GET(xmlOrId, xpath, doOutput)` → `long`
- `XML_GET(xmlOrId, xpath, doOutput, outputType)` → `long`
- `XML_GET(xmlOrId, xpath, ref outputArray)` → `long`
- `XML_GET(xmlOrId, xpath, ref outputArray, outputType)` → `long`

**Arguments**
- `xmlOrId` (int|string): integer values resolve a stored document by decimal-string key; string values in this non-`_BYNAME` form are parsed as raw XML text for this call.
- `xpath` (string): XPath expression evaluated against the selected document.
- `doOutput` (optional, int; default `0`): non-zero copies to `RESULTS`; `0` leaves outputs untouched.
- `outputType` (optional, int; default `0`): projection style.
- `outputArray` (string[]): destination array for copied values.

**Semantics**
- Selects nodes with `xpath` and returns the full match count.
- Output destination rules:
- if the third argument is omitted or is integer `0`, nothing is written,
- if the third argument is a non-zero integer, matched values are copied to `RESULTS` starting at index `0`,
- if the third argument is `ref outputArray`, matched values are copied there instead.
- `outputType` mapping:
- `1`: `InnerText`,
- `2`: `InnerXml`,
- `3`: `OuterXml`,
- `4`: `Name`,
- other values or omission: `Value`.
- Style `0`/default reads `XmlNode.Value`; for element nodes that is `null`, not the element's text content.
- Copies at most the destination length, does not clear untouched slots, and still returns the total match count rather than the copied count.

**Errors & validation**
- Returns `-1` if integer-key lookup is requested and no stored document exists for that key.
- Runtime error if raw-XML parsing fails.
- Runtime error if `xpath` is not a valid XPath expression.

**Examples**
- `XML_GET("<root><a>1</a></root>", "/root/a", 1, 1)`

## XML_GET_BYNAME (expression function)

**Summary**
- Selects nodes from a stored XML document and optionally copies their projected values to a string array.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_GET_BYNAME(xmlName, xpath [, doOutput [, outputType]])`
- `XML_GET_BYNAME(xmlName, xpath, outputArray [, outputType])`

**Signatures / argument rules**
- `XML_GET_BYNAME(xmlName, xpath)` → `long`
- `XML_GET_BYNAME(xmlName, xpath, doOutput)` → `long`
- `XML_GET_BYNAME(xmlName, xpath, doOutput, outputType)` → `long`
- `XML_GET_BYNAME(xmlName, xpath, ref outputArray)` → `long`
- `XML_GET_BYNAME(xmlName, xpath, ref outputArray, outputType)` → `long`

**Arguments**
- `xmlName` (int|string): stored-document key; string values are used directly, and integer values are also accepted here and converted to decimal strings.
- `xpath` (string): XPath expression evaluated against the stored document.
- `doOutput` (optional, int; default `0`): non-zero copies to `RESULTS`; `0` leaves outputs untouched.
- `outputType` (optional, int; default `0`): projection style.
- `outputArray` (string[]): destination array for copied values.

**Semantics**
- Same projection, copy-limit, and return-value rules as `XML_GET`.
- Unlike `XML_GET`, this form never parses raw XML from the first argument; it always performs stored-document lookup.
- Output destination rules:
- if the third argument is omitted or is integer `0`, nothing is written,
- if the third argument is a non-zero integer, matched values are copied to `RESULTS` starting at index `0`,
- if the third argument is `ref outputArray`, matched values are copied there instead.
- `outputType` mapping:
- `1`: `InnerText`,
- `2`: `InnerXml`,
- `3`: `OuterXml`,
- `4`: `Name`,
- other values or omission: `Value`.
- Style `0`/default reads `XmlNode.Value`; for element nodes that is `null`, not the element's text content.
- Copies at most the destination length, does not clear untouched slots, and still returns the total match count rather than the copied count.

**Errors & validation**
- Returns `-1` if no stored document exists for the resolved key.
- Runtime error if `xpath` is not a valid XPath expression.

**Examples**
- `XML_GET_BYNAME("menu", "/root/a", 1, 1)`

## XML_SET (expression function)

**Summary**
- Assigns a string to selected XML nodes.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_SET(xmlId, xpath, value [, setAllNodes [, outputType]])`
- `XML_SET(xmlVar, xpath, value [, setAllNodes [, outputType]])`

**Signatures / argument rules**
- `XML_SET(xmlId, xpath, value)` → `long`
- `XML_SET(xmlId, xpath, value, setAllNodes)` → `long`
- `XML_SET(xmlId, xpath, value, setAllNodes, outputType)` → `long`
- `XML_SET(ref xmlVar, xpath, value)` → `long`
- `XML_SET(ref xmlVar, xpath, value, setAllNodes)` → `long`
- `XML_SET(ref xmlVar, xpath, value, setAllNodes, outputType)` → `long`

**Arguments**
- `xmlId` (int): stored-document key, converted to a decimal string.
- `xpath` (string): XPath expression evaluated against the selected document.
- `value` (string): replacement text.
- `setAllNodes` (optional, int; default `0`): when multiple nodes match, non-zero updates all of them; `0` leaves them all unchanged.
- `outputType` (optional, int; default `0`): write mode; `0` = `Value`, `1` = `InnerText`, `2` = `InnerXml`; other values clamp to `0`.
- `xmlVar` (string variable): writable string variable containing raw XML.

**Semantics**
- Target resolution:
- `XML_SET(xmlId, ...)` mutates a stored document in place,
- `XML_SET(ref xmlVar, ...)` reparses the variable as XML, applies the mutation to that temporary document, and writes back `OuterXml` only when at least one node matches.
- Returns the full match count from `xpath`.
- If no nodes match, no mutation occurs and the function returns `0`.
- If exactly one node matches, that node is always updated.
- If more than one node matches and `setAllNodes == 0`, no node is updated even though the match count is still returned.
- If more than one node matches and `setAllNodes != 0`, every matched node is updated.
- Style `0` writes `XmlNode.Value`; on element nodes that follows .NET element-value rules and raises a runtime error instead of writing text.

**Errors & validation**
- Returns `-1` if stored-document lookup is requested and the key does not exist.
- Runtime error if `xmlVar` does not contain well-formed XML.
- Runtime error if `xpath` is not a valid XPath expression.
- Runtime error if the chosen write mode is invalid for the matched node type.

**Examples**
- `XML_SET(0, "/root/a/@id", "42")`

## XML_SET_BYNAME (expression function)

**Summary**
- Assigns a string to selected nodes in a stored XML document.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_SET_BYNAME(xmlName, xpath, value [, setAllNodes [, outputType]])`

**Signatures / argument rules**
- `XML_SET_BYNAME(xmlName, xpath, value)` → `long`
- `XML_SET_BYNAME(xmlName, xpath, value, setAllNodes)` → `long`
- `XML_SET_BYNAME(xmlName, xpath, value, setAllNodes, outputType)` → `long`

**Arguments**
- `xmlName` (string): stored-document key.
- `xpath` (string): XPath expression evaluated against the stored document.
- `value` (string): replacement text.
- `setAllNodes` (optional, int; default `0`): when multiple nodes match, non-zero updates all of them; `0` leaves them all unchanged.
- `outputType` (optional, int; default `0`): write mode; `0` = `Value`, `1` = `InnerText`, `2` = `InnerXml`; other values clamp to `0`.

**Semantics**
- Uses stored-document lookup only; raw XML text is not accepted in this form.
- Otherwise follows the same match-count, `setAllNodes`, and write-mode rules as `XML_SET`.

**Errors & validation**
- Returns `-1` if no stored document exists for `xmlName`.
- Runtime error if `xpath` is not a valid XPath expression.
- Runtime error if the chosen write mode is invalid for the matched node type.

**Examples**
- `XML_SET_BYNAME("menu", "/root/a/@id", "42")`

## XML_EXIST (expression function)

**Summary**
- Checks whether a stored XML document exists.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_EXIST(xmlId)`

**Signatures / argument rules**
- `XML_EXIST(xmlId)` → `long`

**Arguments**
- `xmlId` (int|string): storage key; integer values are converted to decimal strings.

**Semantics**
- Returns `1` if a stored document exists for the resolved key.
- Returns `0` otherwise.

**Errors & validation**
- None.

**Examples**
- `IF XML_EXIST("menu")`

## XML_TOSTR (expression function)

**Summary**
- Returns the serialized text of a stored XML document.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_TOSTR(xmlId)`

**Signatures / argument rules**
- `XML_TOSTR(xmlId)` → `string`

**Arguments**
- `xmlId` (int|string): storage key; integer values are converted to decimal strings.

**Semantics**
- If a stored document exists for the resolved key, returns its current `OuterXml`.
- If no stored document exists for that key, returns `""`.

**Errors & validation**
- None.

**Examples**
- `PRINTFORM %XML_TOSTR("menu")%`

## XML_ADDNODE (expression function)

**Summary**
- Inserts an XML element parsed from text at positions selected by XPath.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_ADDNODE(xmlId, xpath, childXml [, methodType [, setAllNodes]])`
- `XML_ADDNODE(xmlVar, xpath, childXml [, methodType [, setAllNodes]])`

**Signatures / argument rules**
- `XML_ADDNODE(xmlId, xpath, childXml)` → `long`
- `XML_ADDNODE(xmlId, xpath, childXml, methodType)` → `long`
- `XML_ADDNODE(xmlId, xpath, childXml, methodType, setAllNodes)` → `long`
- `XML_ADDNODE(ref xmlVar, xpath, childXml)` → `long`
- `XML_ADDNODE(ref xmlVar, xpath, childXml, methodType)` → `long`
- `XML_ADDNODE(ref xmlVar, xpath, childXml, methodType, setAllNodes)` → `long`

**Arguments**
- `xmlId` (int): stored-document key, converted to a decimal string.
- `xpath` (string): selects insertion targets.
- `childXml` (string): XML text whose document element becomes the inserted node.
- `methodType` (optional, int; default `0`): `0` append as child, `1` insert before the matched node, `2` insert after the matched node; other values clamp to `0`.
- `setAllNodes` (optional, int; default `0`): when multiple nodes match, non-zero performs insertion attempts for all of them; `0` leaves them all unchanged.
- `xmlVar` (string variable): writable string variable containing raw XML.

**Semantics**
- Target resolution matches `XML_SET`: stored-document lookup for `xmlId`, or parse / write-back behavior for `ref xmlVar`.
- Returns the full match count from `xpath`.
- If no nodes match, no mutation occurs and the function returns `0`.
- If exactly one node matches, insertion is attempted regardless of `setAllNodes`.
- If more than one node matches and `setAllNodes == 0`, no insertion occurs even though the match count is still returned.
- Multi-match quirk: the engine constructs one inserted node and reuses it for every successful insertion instead of cloning it. Each later successful insertion moves that same node again, so the final document contains the inserted node only at the last successful target.
- When operating on `ref xmlVar`, the variable is rewritten to `OuterXml` only if at least one node matched.

**Errors & validation**
- Returns `-1` if stored-document lookup is requested and the key does not exist.
- Runtime error if `xmlVar` or `childXml` is not well-formed XML.
- Runtime error if `xpath` is not a valid XPath expression.
- Single-target before/after insertion returns `0` if the matched node has no parent; other unsupported target kinds follow the underlying XML API failure path.

**Examples**
- `XML_ADDNODE(0, "/root/list", "<item/>")`

## XML_ADDNODE_BYNAME (expression function)

**Summary**
- Inserts an XML element parsed from text into a stored XML document.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_ADDNODE_BYNAME(xmlName, xpath, childXml [, methodType [, setAllNodes]])`

**Signatures / argument rules**
- `XML_ADDNODE_BYNAME(xmlName, xpath, childXml)` → `long`
- `XML_ADDNODE_BYNAME(xmlName, xpath, childXml, methodType)` → `long`
- `XML_ADDNODE_BYNAME(xmlName, xpath, childXml, methodType, setAllNodes)` → `long`

**Arguments**
- `xmlName` (string): stored-document key.
- `xpath` (string): selects insertion targets.
- `childXml` (string): XML text whose document element becomes the inserted node.
- `methodType` (optional, int; default `0`): `0` append as child, `1` insert before the matched node, `2` insert after the matched node; other values clamp to `0`.
- `setAllNodes` (optional, int; default `0`): when multiple nodes match, non-zero performs insertion attempts for all of them; `0` leaves them all unchanged.

**Semantics**
- Uses stored-document lookup only; raw XML text is not accepted in this form.
- Otherwise follows the same match-count, `methodType`, and multi-match node-reuse rules as `XML_ADDNODE`.

**Errors & validation**
- Returns `-1` if no stored document exists for `xmlName`.
- Runtime error if `childXml` is not well-formed XML.
- Runtime error if `xpath` is not a valid XPath expression.

**Examples**
- `XML_ADDNODE_BYNAME("menu", "/root/list", "<item/>")`

## XML_REMOVENODE (expression function)

**Summary**
- Removes nodes selected by XPath.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_REMOVENODE(xmlId, xpath [, setAllNodes])`
- `XML_REMOVENODE(xmlVar, xpath [, setAllNodes])`

**Signatures / argument rules**
- `XML_REMOVENODE(xmlId, xpath)` → `long`
- `XML_REMOVENODE(xmlId, xpath, setAllNodes)` → `long`
- `XML_REMOVENODE(ref xmlVar, xpath)` → `long`
- `XML_REMOVENODE(ref xmlVar, xpath, setAllNodes)` → `long`

**Arguments**
- `xmlId` (int): stored-document key, converted to a decimal string.
- `xpath` (string): selects removal targets.
- `setAllNodes` (optional, int; default `0`): when multiple nodes match, non-zero removes all of them; `0` leaves them all unchanged.
- `xmlVar` (string variable): writable string variable containing raw XML.

**Semantics**
- Target resolution matches `XML_SET`.
- Returns the full match count from `xpath`.
- If no nodes match, no mutation occurs and the function returns `0`.
- If exactly one node matches, removal is attempted regardless of `setAllNodes`.
- If more than one node matches and `setAllNodes == 0`, no node is removed even though the match count is still returned.
- If more than one node matches and `setAllNodes != 0`, removal is attempted for every matched node; per-node failures in that loop do not change the returned count.
- A document element can be removed; the resulting document then serializes as an empty string.
- When operating on `ref xmlVar`, the variable is rewritten to `OuterXml` only if at least one node matched.

**Errors & validation**
- Returns `-1` if stored-document lookup is requested and the key does not exist.
- Runtime error if `xmlVar` is not well-formed XML.
- Runtime error if `xpath` is not a valid XPath expression.
- Single-target removal returns `0` when the matched node cannot be removed because it has no parent.

**Examples**
- `XML_REMOVENODE(0, "/root/item", 1)`

## XML_REMOVENODE_BYNAME (expression function)

**Summary**
- Removes nodes selected by XPath from a stored XML document.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_REMOVENODE_BYNAME(xmlName, xpath [, setAllNodes])`

**Signatures / argument rules**
- `XML_REMOVENODE_BYNAME(xmlName, xpath)` → `long`
- `XML_REMOVENODE_BYNAME(xmlName, xpath, setAllNodes)` → `long`

**Arguments**
- `xmlName` (string): stored-document key.
- `xpath` (string): selects removal targets.
- `setAllNodes` (optional, int; default `0`): when multiple nodes match, non-zero removes all of them; `0` leaves them all unchanged.

**Semantics**
- Uses stored-document lookup only; raw XML text is not accepted in this form.
- Otherwise follows the same match-count, `setAllNodes`, and root-removal rules as `XML_REMOVENODE`.

**Errors & validation**
- Returns `-1` if no stored document exists for `xmlName`.
- Runtime error if `xpath` is not a valid XPath expression.

**Examples**
- `XML_REMOVENODE_BYNAME("menu", "/root/item", 1)`

## XML_REPLACE (expression function)

**Summary**
- Replaces either an entire stored XML document or selected nodes with a new XML element.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_REPLACE(xmlId, newXml)`
- `XML_REPLACE(xmlId, xpath, newXml [, setAllNodes])`
- `XML_REPLACE(xmlVar, xpath, newXml [, setAllNodes])`

**Signatures / argument rules**
- `XML_REPLACE(xmlId, newXml)` → `long`
- `XML_REPLACE(xmlId, xpath, newXml)` → `long`
- `XML_REPLACE(xmlId, xpath, newXml, setAllNodes)` → `long`
- `XML_REPLACE(ref xmlVar, xpath, newXml)` → `long`
- `XML_REPLACE(ref xmlVar, xpath, newXml, setAllNodes)` → `long`

**Arguments**
- `xmlId` (int|string): in the two-argument form this is always a stored-document key; integer values are converted to decimal strings.
- `newXml` (string): XML text whose document element becomes the replacement node, or the whole new stored document in the two-argument form.
- `xpath` (string): selects replacement targets.
- `setAllNodes` (optional, int; default `0`): when multiple nodes match, non-zero replaces all of them; `0` leaves them all unchanged.
- `xmlVar` (string variable): writable string variable containing raw XML for the three-/four-argument form.

**Semantics**
- Two-argument form: parses `newXml` and replaces the entire stored document for `xmlId`; raw XML variables are not accepted in this form.
- Three-/four-argument forms: target resolution matches `XML_SET`.
- Selected-node replacement returns the full match count from `xpath`.
- If no nodes match, no mutation occurs and the function returns `0`.
- If exactly one node matches, replacement is attempted regardless of `setAllNodes`.
- If more than one node matches and `setAllNodes == 0`, no node is replaced even though the match count is still returned.
- Multi-match quirk: the engine constructs one replacement node and reuses it for every successful replacement instead of cloning it. Each later successful replacement moves that same node again, so only the last successful replacement remains in the final document.
- When operating on `ref xmlVar`, the variable is rewritten to `OuterXml` only if at least one node matched.

**Errors & validation**
- Returns `-1` if stored-document lookup is requested and the key does not exist.
- Runtime error if `newXml` or `xmlVar` is not well-formed XML.
- Runtime error if `xpath` is not a valid XPath expression.
- Single-target replacement returns `0` when the matched node cannot be replaced because it has no parent.

**Examples**
- `XML_REPLACE(0, "/root/item", "<other/>", 1)`

## XML_REPLACE_BYNAME (expression function)

**Summary**
- Replaces selected nodes in a stored XML document with a new XML element.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_REPLACE_BYNAME(xmlName, xpath, newXml [, setAllNodes])`

**Signatures / argument rules**
- `XML_REPLACE_BYNAME(xmlName, xpath, newXml)` → `long`
- `XML_REPLACE_BYNAME(xmlName, xpath, newXml, setAllNodes)` → `long`

**Arguments**
- `xmlName` (string): stored-document key.
- `xpath` (string): selects replacement targets.
- `newXml` (string): XML text whose document element becomes the replacement node.
- `setAllNodes` (optional, int; default `0`): when multiple nodes match, non-zero replaces all of them; `0` leaves them all unchanged.

**Semantics**
- Uses stored-document lookup only; raw XML text is not accepted in this form.
- Otherwise follows the same match-count, `setAllNodes`, and multi-match node-reuse rules as the three-/four-argument form of `XML_REPLACE`.

**Errors & validation**
- Returns `-1` if no stored document exists for `xmlName`.
- Runtime error if `newXml` is not well-formed XML.
- Runtime error if `xpath` is not a valid XPath expression.

**Examples**
- `XML_REPLACE_BYNAME("menu", "/root/item", "<other/>", 1)`

## XML_ADDATTRIBUTE (expression function)

**Summary**
- Creates an XML attribute and inserts it at positions selected by XPath.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_ADDATTRIBUTE(xmlId, xpath, attrName [, attrValue [, methodType [, setAllNodes]]])`
- `XML_ADDATTRIBUTE(xmlVar, xpath, attrName [, attrValue [, methodType [, setAllNodes]]])`

**Signatures / argument rules**
- `XML_ADDATTRIBUTE(xmlId, xpath, attrName)` → `long`
- `XML_ADDATTRIBUTE(xmlId, xpath, attrName, attrValue)` → `long`
- `XML_ADDATTRIBUTE(xmlId, xpath, attrName, attrValue, methodType)` → `long`
- `XML_ADDATTRIBUTE(xmlId, xpath, attrName, attrValue, methodType, setAllNodes)` → `long`
- `XML_ADDATTRIBUTE(ref xmlVar, xpath, attrName)` → `long`
- `XML_ADDATTRIBUTE(ref xmlVar, xpath, attrName, attrValue)` → `long`
- `XML_ADDATTRIBUTE(ref xmlVar, xpath, attrName, attrValue, methodType)` → `long`
- `XML_ADDATTRIBUTE(ref xmlVar, xpath, attrName, attrValue, methodType, setAllNodes)` → `long`

**Arguments**
- `xmlId` (int): stored-document key, converted to a decimal string.
- `xpath` (string): selects insertion targets.
- `attrName` (string): attribute name to create.
- `attrValue` (optional, string; default `""`): attribute value.
- `methodType` (optional, int; default `0`): `0` append to the matched element, `1` insert before the matched attribute, `2` insert after the matched attribute; other values clamp to `0`.
- `setAllNodes` (optional, int; default `0`): when multiple nodes match, non-zero performs insertion attempts for all of them; `0` leaves them all unchanged.
- `xmlVar` (string variable): writable string variable containing raw XML.

**Semantics**
- Target resolution matches `XML_SET`.
- Returns the full match count from `xpath`.
- Method `0` is for matched element nodes. Methods `1` and `2` are for matched attribute nodes.
- If no nodes match, no mutation occurs and the function returns `0`.
- If exactly one node matches, insertion is attempted regardless of `setAllNodes`.
- If more than one node matches and `setAllNodes == 0`, no insertion occurs even though the match count is still returned.
- Multi-match quirk: the engine constructs one attribute object and reuses it for every successful insertion instead of cloning it. Each later successful insertion moves that same attribute again, so the final document retains that new attribute only at the last successful target.
- When operating on `ref xmlVar`, the variable is rewritten to `OuterXml` only if at least one node matched.

**Errors & validation**
- Returns `-1` if stored-document lookup is requested and the key does not exist.
- Runtime error if `xmlVar` is not well-formed XML.
- Runtime error if `xpath` is not a valid XPath expression.
- Method `0` on non-element targets and other unsupported target kinds follow the underlying XML API failure path.

**Examples**
- `XML_ADDATTRIBUTE(0, "/root/item", "id", "42")`

## XML_ADDATTRIBUTE_BYNAME (expression function)

**Summary**
- Creates an XML attribute and inserts it into a stored XML document.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_ADDATTRIBUTE_BYNAME(xmlName, xpath, attrName [, attrValue [, methodType [, setAllNodes]]])`

**Signatures / argument rules**
- `XML_ADDATTRIBUTE_BYNAME(xmlName, xpath, attrName)` → `long`
- `XML_ADDATTRIBUTE_BYNAME(xmlName, xpath, attrName, attrValue)` → `long`
- `XML_ADDATTRIBUTE_BYNAME(xmlName, xpath, attrName, attrValue, methodType)` → `long`
- `XML_ADDATTRIBUTE_BYNAME(xmlName, xpath, attrName, attrValue, methodType, setAllNodes)` → `long`

**Arguments**
- `xmlName` (string): stored-document key.
- `xpath` (string): selects insertion targets.
- `attrName` (string): attribute name to create.
- `attrValue` (optional, string; default `""`): attribute value.
- `methodType` (optional, int; default `0`): `0` append to the matched element, `1` insert before the matched attribute, `2` insert after the matched attribute; other values clamp to `0`.
- `setAllNodes` (optional, int; default `0`): when multiple nodes match, non-zero performs insertion attempts for all of them; `0` leaves them all unchanged.

**Semantics**
- Uses stored-document lookup only; raw XML text is not accepted in this form.
- Otherwise follows the same match-count, target-kind, and multi-match attribute-reuse rules as `XML_ADDATTRIBUTE`.

**Errors & validation**
- Returns `-1` if no stored document exists for `xmlName`.
- Runtime error if `xpath` is not a valid XPath expression.

**Examples**
- `XML_ADDATTRIBUTE_BYNAME("menu", "/root/item", "id", "42")`

## XML_REMOVEATTRIBUTE (expression function)

**Summary**
- Removes attributes selected by XPath.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_REMOVEATTRIBUTE(xmlId, xpath [, setAllNodes])`
- `XML_REMOVEATTRIBUTE(xmlVar, xpath [, setAllNodes])`

**Signatures / argument rules**
- `XML_REMOVEATTRIBUTE(xmlId, xpath)` → `long`
- `XML_REMOVEATTRIBUTE(xmlId, xpath, setAllNodes)` → `long`
- `XML_REMOVEATTRIBUTE(ref xmlVar, xpath)` → `long`
- `XML_REMOVEATTRIBUTE(ref xmlVar, xpath, setAllNodes)` → `long`

**Arguments**
- `xmlId` (int): stored-document key, converted to a decimal string.
- `xpath` (string): selects removal targets.
- `setAllNodes` (optional, int; default `0`): when multiple nodes match, non-zero removes all of them; `0` leaves them all unchanged.
- `xmlVar` (string variable): writable string variable containing raw XML.

**Semantics**
- Target resolution matches `XML_SET`.
- Returns the full match count from `xpath`.
- This form is for attribute nodes; a single non-attribute match returns `0` instead of removing anything.
- If no nodes match, no mutation occurs and the function returns `0`.
- If exactly one attribute matches, it is removed regardless of `setAllNodes`.
- If more than one node matches and `setAllNodes == 0`, no attribute is removed even though the match count is still returned.
- If more than one node matches and `setAllNodes != 0`, removal is attempted for every matched node; per-node failures in that loop do not change the returned count.
- When operating on `ref xmlVar`, the variable is rewritten to `OuterXml` only if at least one node matched.

**Errors & validation**
- Returns `-1` if stored-document lookup is requested and the key does not exist.
- Runtime error if `xmlVar` is not well-formed XML.
- Runtime error if `xpath` is not a valid XPath expression.

**Examples**
- `XML_REMOVEATTRIBUTE(0, "/root/item/@id", 1)`

## XML_REMOVEATTRIBUTE_BYNAME (expression function)

**Summary**
- Removes attributes selected by XPath from a stored XML document.

**Tags**
- xml
- data-structures

**Syntax**
- `XML_REMOVEATTRIBUTE_BYNAME(xmlName, xpath [, setAllNodes])`

**Signatures / argument rules**
- `XML_REMOVEATTRIBUTE_BYNAME(xmlName, xpath)` → `long`
- `XML_REMOVEATTRIBUTE_BYNAME(xmlName, xpath, setAllNodes)` → `long`

**Arguments**
- `xmlName` (string): stored-document key.
- `xpath` (string): selects removal targets.
- `setAllNodes` (optional, int; default `0`): when multiple nodes match, non-zero removes all of them; `0` leaves them all unchanged.

**Semantics**
- Uses stored-document lookup only; raw XML text is not accepted in this form.
- Otherwise follows the same match-count and target-kind rules as `XML_REMOVEATTRIBUTE`.

**Errors & validation**
- Returns `-1` if no stored document exists for `xmlName`.
- Runtime error if `xpath` is not a valid XPath expression.

**Examples**
- `XML_REMOVEATTRIBUTE_BYNAME("menu", "/root/item/@id", 1)`

## MAP_CREATE (expression function)

**Summary**
- Creates an empty named map.

**Tags**
- map
- data-structures

**Syntax**
- `MAP_CREATE(mapName)`

**Signatures / argument rules**
- `MAP_CREATE(mapName)` → `long`

**Arguments**
- `mapName` (string): map identifier.

**Semantics**
- If a map with that name already exists, returns `0` and leaves it unchanged.
- Otherwise creates an empty map and returns `1`.

**Errors & validation**
- None.

**Examples**
- `MAP_CREATE("session")`

## MAP_EXIST (expression function)

**Summary**
- Checks whether a named map exists.

**Tags**
- map
- data-structures

**Syntax**
- `MAP_EXIST(mapName)`

**Signatures / argument rules**
- `MAP_EXIST(mapName)` → `long`

**Arguments**
- `mapName` (string): map identifier.

**Semantics**
- Returns `1` if the map exists.
- Returns `0` otherwise.

**Errors & validation**
- None.

**Examples**
- `IF MAP_EXIST("session")`

## MAP_RELEASE (expression function)

**Summary**
- Deletes a named map.

**Tags**
- map
- data-structures

**Syntax**
- `MAP_RELEASE(mapName)`

**Signatures / argument rules**
- `MAP_RELEASE(mapName)` → `long`

**Arguments**
- `mapName` (string): map identifier.

**Semantics**
- If the map exists, it is removed.
- The function always returns `1`, even when the map was already absent.

**Errors & validation**
- None.

**Examples**
- `MAP_RELEASE("session")`

## MAP_GET (expression function)

**Summary**
- Returns the value stored for a key in a named map.

**Tags**
- map
- data-structures

**Syntax**
- `MAP_GET(mapName, key)`

**Signatures / argument rules**
- `MAP_GET(mapName, key)` → `string`

**Arguments**
- `mapName` (string): map identifier.
- `key` (string): lookup key.

**Semantics**
- If the map exists and contains `key`, returns the stored string value.
- If the map does not exist or the key is absent, returns `""`.

**Errors & validation**
- None.

**Examples**
- `PRINTFORM %MAP_GET("session", "token")%`

## MAP_CLEAR (expression function)

**Summary**
- Removes all entries from a named map.

**Tags**
- map
- data-structures

**Syntax**
- `MAP_CLEAR(mapName)`

**Signatures / argument rules**
- `MAP_CLEAR(mapName)` → `long`

**Arguments**
- `mapName` (string): map identifier.

**Semantics**
- If the map exists, clears every entry and returns `1`.
- If the map does not exist, returns `-1`.

**Errors & validation**
- None.

**Examples**
- `MAP_CLEAR("session")`

## MAP_SIZE (expression function)

**Summary**
- Returns the entry count of a named map.

**Tags**
- map
- data-structures

**Syntax**
- `MAP_SIZE(mapName)`

**Signatures / argument rules**
- `MAP_SIZE(mapName)` → `long`

**Arguments**
- `mapName` (string): map identifier.

**Semantics**
- If the map exists, returns its current entry count.
- If the map does not exist, returns `-1`.

**Errors & validation**
- None.

**Examples**
- `PRINTFORML {MAP_SIZE("session")}`

## MAP_HAS (expression function)

**Summary**
- Checks whether a named map contains a key.

**Tags**
- map
- data-structures

**Syntax**
- `MAP_HAS(mapName, key)`

**Signatures / argument rules**
- `MAP_HAS(mapName, key)` → `long`

**Arguments**
- `mapName` (string): map identifier.
- `key` (string): lookup key.

**Semantics**
- If the map does not exist, returns `-1`.
- Otherwise returns `1` when `key` exists, or `0` when it does not.

**Errors & validation**
- None.

**Examples**
- `IF MAP_HAS("session", "token")`

## MAP_SET (expression function)

**Summary**
- Adds or overwrites a key-value entry in a named map.

**Tags**
- map
- data-structures

**Syntax**
- `MAP_SET(mapName, key, value)`

**Signatures / argument rules**
- `MAP_SET(mapName, key, value)` → `long`

**Arguments**
- `mapName` (string): map identifier.
- `key` (string): entry key.
- `value` (string): stored value.

**Semantics**
- If the map does not exist, returns `-1`.
- Otherwise stores `value` under `key`, replacing any previous value, and returns `1`.

**Errors & validation**
- None.

**Examples**
- `MAP_SET("session", "token", "abc")`

## MAP_REMOVE (expression function)

**Summary**
- Deletes a key from a named map.

**Tags**
- map
- data-structures

**Syntax**
- `MAP_REMOVE(mapName, key)`

**Signatures / argument rules**
- `MAP_REMOVE(mapName, key)` → `long`

**Arguments**
- `mapName` (string): map identifier.
- `key` (string): entry key.

**Semantics**
- If the map does not exist, returns `-1`.
- Otherwise removes `key` if present and returns `1` either way.

**Errors & validation**
- None.

**Examples**
- `MAP_REMOVE("session", "token")`

## MAP_GETKEYS (expression function)

**Summary**
- Enumerates the keys stored in a named map.

**Tags**
- map
- data-structures

**Syntax**
- `MAP_GETKEYS(mapName)`
- `MAP_GETKEYS(mapName, doOutput)`
- `MAP_GETKEYS(mapName, outputArray, doOutput)`

**Signatures / argument rules**
- `MAP_GETKEYS(mapName)` → `string`
- `MAP_GETKEYS(mapName, doOutput)` → `string`
- `MAP_GETKEYS(mapName, outputArray, doOutput)` → `string`

**Arguments**
- `mapName` (string): map identifier.
- `doOutput` (optional, int; default `0`): non-zero enables array output in the two- and three-argument forms.
- `outputArray` (optional, string[]): destination array for copied keys.

**Semantics**
- If the map does not exist, returns `""` and does not write any outputs.
- One-argument form returns a comma-joined key list with no escaping. Keys containing commas therefore make the returned string ambiguous.
- Two-argument form with `doOutput == 0` returns `""` and writes nothing.
- Two-argument form with `doOutput != 0` copies keys to `RESULTS` starting at index `0`, sets `RESULT` to the total key count, and returns the scalar `RESULTS` value (`RESULTS:0`, meaning the first copied key or `""`).
- Three-argument form with `doOutput == 0` returns `""` and writes nothing.
- Three-argument form with `doOutput != 0` copies keys to `outputArray` starting at index `0`, sets `RESULT` to the total key count, and returns `""`.
- Copying stops at the destination length, untouched slots are not cleared, and the engine does not sort the keys before enumeration.

**Errors & validation**
- None.

**Examples**
- `MAP_GETKEYS("session", 1)`

## MAP_TOXML (expression function)

**Summary**
- Serializes a named map to XML-like text.

**Tags**
- map
- data-structures

**Syntax**
- `MAP_TOXML(mapName)`

**Signatures / argument rules**
- `MAP_TOXML(mapName)` → `string`

**Arguments**
- `mapName` (string): map identifier.

**Semantics**
- If the map does not exist, returns `""`.
- Otherwise returns text in the form `<map><p><k>...</k><v>...</v></p>...</map>` using the map's native enumeration order.
- Keys and values are inserted without XML escaping. Special characters such as `<`, `>`, or `&` therefore produce malformed or structurally changed output.

**Errors & validation**
- None.

**Examples**
- `data '= MAP_TOXML("session")`

## MAP_FROMXML (expression function)

**Summary**
- Imports key-value pairs from XML-like text into an existing named map.

**Tags**
- map
- data-structures

**Syntax**
- `MAP_FROMXML(mapName, xmlMap)`

**Signatures / argument rules**
- `MAP_FROMXML(mapName, xmlMap)` → `long`

**Arguments**
- `mapName` (string): map identifier.
- `xmlMap` (string): source text expected to contain `/map/p` entries.

**Semantics**
- If the map does not exist, returns `0`.
- Parses `xmlMap`, selects `/map/p`, and for each selected node requires exactly one `./k` child and exactly one `./v` child.
- Imported keys use `k.InnerText`; imported values use `v.InnerXml`.
- The map is not cleared first. Imported entries overwrite existing keys they mention and leave all other existing entries untouched.
- Returns `1` after successful parsing even if no usable pairs were imported.

**Errors & validation**
- Runtime error if `xmlMap` is not well-formed XML.

**Examples**
- `MAP_FROMXML("session", data)`

## DT_CREATE (expression function)

**Summary**
- Creates an empty named `DataTable` with an automatic primary-key column.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_CREATE(tableName)`

**Signatures / argument rules**
- `DT_CREATE(tableName)` → `long`

**Arguments**
- `tableName` (string): table identifier.

**Semantics**
- If a table with that name already exists, returns `0` and leaves it unchanged.
- Otherwise creates a new table with `CaseSensitive = true`, auto-adds an `id` column of type `int64`, marks it non-null / unique / primary-key, and returns `1`.

**Errors & validation**
- None.

**Examples**
- `DT_CREATE("db")`

## DT_EXIST (expression function)

**Summary**
- Checks whether a named `DataTable` exists.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_EXIST(tableName)`

**Signatures / argument rules**
- `DT_EXIST(tableName)` → `long`

**Arguments**
- `tableName` (string): table identifier.

**Semantics**
- Returns `1` if the table exists.
- Returns `0` otherwise.

**Errors & validation**
- None.

**Examples**
- `IF DT_EXIST("db")`

## DT_RELEASE (expression function)

**Summary**
- Deletes a named `DataTable`.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_RELEASE(tableName)`

**Signatures / argument rules**
- `DT_RELEASE(tableName)` → `long`

**Arguments**
- `tableName` (string): table identifier.

**Semantics**
- If the table exists, it is removed.
- The function always returns `1`, even when the table was already absent.

**Errors & validation**
- None.

**Examples**
- `DT_RELEASE("db")`

## DT_NOCASE (expression function)

**Summary**
- Toggles case-sensitive string comparison for a named `DataTable`.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_NOCASE(tableName, ignoreCase)`

**Signatures / argument rules**
- `DT_NOCASE(tableName, ignoreCase)` → `long`

**Arguments**
- `tableName` (string): table identifier.
- `ignoreCase` (int): non-zero makes the table case-insensitive; `0` restores case-sensitive comparison.

**Semantics**
- If the table does not exist, returns `-1`.
- Otherwise sets `CaseSensitive` to `false` when `ignoreCase != 0`, or to `true` when `ignoreCase == 0`, and returns `1`.

**Errors & validation**
- None.

**Examples**
- `DT_NOCASE("db", 1)`

## DT_CLEAR (expression function)

**Summary**
- Removes all rows from a named `DataTable` without changing its columns.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_CLEAR(tableName)`

**Signatures / argument rules**
- `DT_CLEAR(tableName)` → `long`

**Arguments**
- `tableName` (string): table identifier.

**Semantics**
- If the table does not exist, returns `-1`.
- Otherwise clears all rows, keeps the schema intact, and returns `1`.

**Errors & validation**
- None.

**Examples**
- `DT_CLEAR("db")`

## DT_COLUMN_ADD (expression function)

**Summary**
- Adds a column to a named `DataTable`.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_COLUMN_ADD(tableName, columnName [, type [, nullable]])`

**Signatures / argument rules**
- `DT_COLUMN_ADD(tableName, columnName)` → `long`
- `DT_COLUMN_ADD(tableName, columnName, type)` → `long`
- `DT_COLUMN_ADD(tableName, columnName, type, nullable)` → `long`

**Arguments**
- `tableName` (string): table identifier.
- `columnName` (string): column name.
- `type` (optional, int|string): column type; integer codes are `1=int8`, `2=int16`, `3=int32`, `4=int64`, `5=string`; string names must be the exact lowercase spellings `int8`, `int16`, `int32`, `int64`, or `string`.
- `nullable` (optional, int; default `1`): non-zero allows `NULL`; `0` disallows it.

**Semantics**
- If the table does not exist, returns `-1`.
- Column-name collisions are checked through `DataTable` column lookup, so case variants such as `id` and `ID` count as the same existing column.
- If the column already exists, returns `0`.
- If `type` is omitted, the new column uses `string` type.
- Otherwise creates the column and returns `1`.

**Errors & validation**
- Runtime error if `type` is present but not one of the supported integer codes or exact lowercase type names.

**Examples**
- `DT_COLUMN_ADD("db", "name")`

## DT_COLUMN_NAMES (expression function)

**Summary**
- Copies column names from a named `DataTable` to a string array.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_COLUMN_NAMES(tableName)`
- `DT_COLUMN_NAMES(tableName, outputArray)`

**Signatures / argument rules**
- `DT_COLUMN_NAMES(tableName)` → `long`
- `DT_COLUMN_NAMES(tableName, outputArray)` → `long`

**Arguments**
- `tableName` (string): table identifier.
- `outputArray` (optional, string[]): destination array; if omitted, `RESULTS` is used.

**Semantics**
- If the table does not exist, returns `-1`.
- Copies names in column order starting at destination index `0` and returns the full column count.
- The auto-created `id` column is included.
- No destination clearing is performed.

**Errors & validation**
- Runtime error if the destination array is shorter than the column count; this build does not clamp the copy length here.

**Examples**
- `DT_COLUMN_NAMES("db", names)`

## DT_COLUMN_EXIST (expression function)

**Summary**
- Checks whether a named `DataTable` contains a column and reports its type.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_COLUMN_EXIST(tableName, columnName)`

**Signatures / argument rules**
- `DT_COLUMN_EXIST(tableName, columnName)` → `long`

**Arguments**
- `tableName` (string): table identifier.
- `columnName` (string): column name.

**Semantics**
- If the table does not exist, returns `-1`.
- If the column does not exist, returns `0`.
- Otherwise returns the type code `1=int8`, `2=int16`, `3=int32`, `4=int64`, or `5=string`.

**Errors & validation**
- None.

**Examples**
- `PRINTFORML {DT_COLUMN_EXIST("db", "name")}`

## DT_COLUMN_REMOVE (expression function)

**Summary**
- Removes a column from a named `DataTable`.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_COLUMN_REMOVE(tableName, columnName)`

**Signatures / argument rules**
- `DT_COLUMN_REMOVE(tableName, columnName)` → `long`

**Arguments**
- `tableName` (string): table identifier.
- `columnName` (string): column name.

**Semantics**
- If the table does not exist, returns `-1`.
- If the column exists and its name is not `id` under case-insensitive comparison, removes it and returns `1`.
- If the column does not exist, or it resolves to the protected `id` column, returns `0`.

**Errors & validation**
- None.

**Examples**
- `DT_COLUMN_REMOVE("db", "age")`

## DT_COLUMN_LENGTH (expression function)

**Summary**
- Returns the column count of a named `DataTable`.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_COLUMN_LENGTH(tableName)`

**Signatures / argument rules**
- `DT_COLUMN_LENGTH(tableName)` → `long`

**Arguments**
- `tableName` (string): table identifier.

**Semantics**
- If the table does not exist, returns `-1`.
- Otherwise returns the current number of columns, including the auto-created `id` column.

**Errors & validation**
- None.

**Examples**
- `PRINTFORML {DT_COLUMN_LENGTH("db")}`

## DT_ROW_ADD (expression function)

**Summary**
- Adds a row to a named `DataTable` and returns its generated `id` value.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_ROW_ADD(tableName [, columnName, columnValue] ...)`
- `DT_ROW_ADD(tableName, columnNames, columnValues, count)`

**Signatures / argument rules**
- `DT_ROW_ADD(tableName)` → `long`
- `DT_ROW_ADD(tableName, columnName, columnValue [, columnName, columnValue] ...)` → `long`
- `DT_ROW_ADD(tableName, columnNames, columnValues, count)` → `long`

**Arguments**
- `tableName` (string): table identifier.
- `columnName` (optional, string): column name in the variadic pair form.
- `columnValue` (optional, int|string): value in the variadic pair form; its type must match the destination column type.
- `columnNames` (string[]): column names in the array form.
- `columnValues` (int[]|string[]): homogeneous value array in the array form; mixed string/integer array input is not supported.
- `count` (int): requested number of array-form assignments.

**Semantics**
- If the table does not exist, returns `-1`.
- Creates a new row, auto-generates its `id`, then applies assignments.
- Calling `DT_ROW_ADD(tableName)` with no assignments is valid and still creates a row.
- Array-form assignments use `min(count, len(columnNames), len(columnValues))`; if that effective count is `<= 0`, no assignments are performed and the row is still added.
- Integer writes to `int8` / `int16` / `int32` columns are clamped to the destination range.
- Column lookup follows `DataTable` rules and is case-insensitive in practice. Guard quirk: only the exact lowercase name `id` is blocked; case variants such as `ID` still resolve to the primary-key column and can overwrite it.
- If an error occurs during assignment, the new row is not added because insertion happens only after all assignments finish.

**Errors & validation**
- Runtime error if a named column does not exist.
- Runtime error if a supplied value type does not match the destination column type.

**Examples**
- `id = DT_ROW_ADD("db", "name", "Alice")`

## DT_ROW_SET (expression function)

**Summary**
- Edits an existing row in a named `DataTable` selected by `id`.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_ROW_SET(tableName, idValue [, columnName, columnValue] ...)`
- `DT_ROW_SET(tableName, idValue, columnNames, columnValues, count)`

**Signatures / argument rules**
- `DT_ROW_SET(tableName, idValue)` → `long`
- `DT_ROW_SET(tableName, idValue, columnName, columnValue [, columnName, columnValue] ...)` → `long`
- `DT_ROW_SET(tableName, idValue, columnNames, columnValues, count)` → `long`

**Arguments**
- `tableName` (string): table identifier.
- `idValue` (int): primary-key value of the row to edit.
- `columnName` (optional, string): column name in the variadic pair form.
- `columnValue` (optional, int|string): value in the variadic pair form; its type must match the destination column type.
- `columnNames` (string[]): column names in the array form.
- `columnValues` (int[]|string[]): homogeneous value array in the array form; mixed string/integer array input is not supported.
- `count` (int): requested number of array-form assignments.

**Semantics**
- If the table does not exist, returns `-1`.
- If no row exists with primary-key `idValue`, returns `-2`.
- Returns the number of assignments actually performed.
- Array-form assignments use `min(count, len(columnNames), len(columnValues))`; if that effective count is `<= 0`, returns `0` without changing the row.
- Integer writes to `int8` / `int16` / `int32` columns are clamped to the destination range.
- Column lookup follows `DataTable` rules and is case-insensitive in practice. Guard quirk: only the exact lowercase name `id` is blocked; case variants such as `ID` still resolve to the primary-key column and can overwrite it.
- Assignments are applied sequentially to the already-existing row, so earlier writes remain visible if a later write throws a runtime error.

**Errors & validation**
- Runtime error if a named column does not exist.
- Runtime error if a supplied value type does not match the destination column type.

**Examples**
- `DT_ROW_SET("db", id, "age", 18)`

## DT_ROW_REMOVE (expression function)

**Summary**
- Removes one or more rows from a named `DataTable` by `id`.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_ROW_REMOVE(tableName, idValue)`
- `DT_ROW_REMOVE(tableName, idValues, count)`

**Signatures / argument rules**
- `DT_ROW_REMOVE(tableName, idValue)` → `long`
- `DT_ROW_REMOVE(tableName, idValues, count)` → `long`

**Arguments**
- `tableName` (string): table identifier.
- `idValue` (int): single primary-key value to remove.
- `idValues` (int[]): source array of primary-key values in the bulk form.
- `count` (int): requested number of `idValues` elements to consider.

**Semantics**
- If the table does not exist, returns `-1`.
- Single-row form removes the row whose primary key equals `idValue`, returning `1` on success or `0` if that row does not exist.
- Array form uses `min(count, len(idValues))`; if that effective count is `<= 0`, returns `0`.
- Array form builds an `id IN (...)` selection from that prefix and removes every matching row, returning the number of removed rows.
- Duplicate ids in the input array do not produce duplicate removals because selection happens through a single `IN (...)` query.

**Errors & validation**
- Runtime error if the generated `id IN (...)` selection is rejected by the underlying `DataTable` expression engine.

**Examples**
- `DT_ROW_REMOVE("db", id)`

## DT_ROW_LENGTH (expression function)

**Summary**
- Returns the row count of a named `DataTable`.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_ROW_LENGTH(tableName)`

**Signatures / argument rules**
- `DT_ROW_LENGTH(tableName)` → `long`

**Arguments**
- `tableName` (string): table identifier.

**Semantics**
- If the table does not exist, returns `-1`.
- Otherwise returns the current row count.

**Errors & validation**
- None.

**Examples**
- `PRINTFORML {DT_ROW_LENGTH("db")}`

## DT_CELL_GET (expression function)

**Summary**
- Reads a cell as an integer from a named `DataTable`.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_CELL_GET(tableName, row, columnName [, asId])`

**Signatures / argument rules**
- `DT_CELL_GET(tableName, row, columnName)` → `long`
- `DT_CELL_GET(tableName, row, columnName, asId)` → `long`

**Arguments**
- `tableName` (string): table identifier.
- `row` (int): row index when `asId == 0`, or primary-key value when `asId != 0`.
- `columnName` (string): column name.
- `asId` (optional, int; default `0`): non-zero selects by `id`; `0` selects by zero-based row index.

**Semantics**
- If the table does not exist, returns `0`.
- If the selected row or column does not exist, returns `0`.
- If the selected cell is `NULL`, returns `0`.
- Otherwise converts the stored value with `Convert.ToInt64(...)` and returns the result.
- Column lookup follows `DataTable` rules and is case-insensitive in practice.

**Errors & validation**
- Runtime error if the stored value cannot be converted to `long`; for example, a non-numeric string cell read through `DT_CELL_GET` throws instead of returning `0`.

**Examples**
- `PRINTFORML {DT_CELL_GET("db", 0, "age")}`

## DT_CELL_ISNULL (expression function)

**Summary**
- Checks whether a selected cell is `NULL` in a named `DataTable`.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_CELL_ISNULL(tableName, row, columnName [, asId])`

**Signatures / argument rules**
- `DT_CELL_ISNULL(tableName, row, columnName)` → `long`
- `DT_CELL_ISNULL(tableName, row, columnName, asId)` → `long`

**Arguments**
- `tableName` (string): table identifier.
- `row` (int): row index when `asId == 0`, or primary-key value when `asId != 0`.
- `columnName` (string): column name.
- `asId` (optional, int; default `0`): non-zero selects by `id`; `0` selects by zero-based row index.

**Semantics**
- If the table does not exist, returns `-1`.
- If the selected row or column does not exist, returns `-2`.
- Otherwise returns `1` when the selected cell contains `NULL`, or `0` when it contains a value.
- Column lookup follows `DataTable` rules and is case-insensitive in practice.

**Errors & validation**
- None.

**Examples**
- `IF DT_CELL_ISNULL("db", id, "age", 1)`

## DT_CELL_GETS (expression function)

**Summary**
- Reads a cell as a string from a named `DataTable`.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_CELL_GETS(tableName, row, columnName [, asId])`

**Signatures / argument rules**
- `DT_CELL_GETS(tableName, row, columnName)` → `string`
- `DT_CELL_GETS(tableName, row, columnName, asId)` → `string`

**Arguments**
- `tableName` (string): table identifier.
- `row` (int): row index when `asId == 0`, or primary-key value when `asId != 0`.
- `columnName` (string): column name.
- `asId` (optional, int; default `0`): non-zero selects by `id`; `0` selects by zero-based row index.

**Semantics**
- If the table does not exist, returns `""`.
- If the selected row or column does not exist, returns `""`.
- If the selected cell is `NULL`, returns `""`.
- Otherwise returns `value.ToString()`.
- Numeric cells therefore come back as their decimal string form.
- Column lookup follows `DataTable` rules and is case-insensitive in practice.

**Errors & validation**
- None.

**Examples**
- `PRINTFORM %DT_CELL_GETS("db", 0, "name")%`

## DT_CELL_SET (expression function)

**Summary**
- Writes a value, or `NULL`, into a selected cell of a named `DataTable`.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_CELL_SET(tableName, row, columnName)`
- `DT_CELL_SET(tableName, row, columnName, value)`
- `DT_CELL_SET(tableName, row, columnName, value, asId)`

**Signatures / argument rules**
- `DT_CELL_SET(tableName, row, columnName)` → `long`
- `DT_CELL_SET(tableName, row, columnName, value)` → `long`
- `DT_CELL_SET(tableName, row, columnName, value, asId)` → `long`

**Arguments**
- `tableName` (string): table identifier.
- `row` (int): row index when `asId == 0`, or primary-key value when `asId != 0`.
- `columnName` (string): column name.
- `value` (optional, int|string): replacement value; omission writes `NULL`.
- `asId` (optional, int; default `0`): non-zero selects by `id`; `0` selects by zero-based row index. This slot is available only when `value` is present.

**Semantics**
- If the table does not exist, returns `-1`.
- If `columnName` resolves to `id` under case-insensitive comparison, returns `0` and refuses the write.
- If the selected row or column does not exist, returns `-3`.
- If `value` is omitted, writes `NULL` and returns `1`.
- If `value` is present but its type does not match the destination column type, returns `-2`.
- Integer writes to `int8` / `int16` / `int32` columns are clamped to the destination range.
- Column lookup follows `DataTable` rules and is case-insensitive in practice.

**Errors & validation**
- None beyond normal argument evaluation.

**Examples**
- `DT_CELL_SET("db", 0, "age", 18)`

## DT_SELECT (expression function)

**Summary**
- Runs a `DataTable.Select(...)` query and outputs matching row ids.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_SELECT(tableName [, filterExpression [, sortRule [, outputArray]]])`

**Signatures / argument rules**
- `DT_SELECT(tableName)` → `long`
- `DT_SELECT(tableName, filterExpression)` → `long`
- `DT_SELECT(tableName, filterExpression, sortRule)` → `long`
- `DT_SELECT(tableName, filterExpression, sortRule, outputArray)` → `long`

**Arguments**
- `tableName` (string): table identifier.
- `filterExpression` (optional, string): `DataTable.Select` filter expression; omission selects every row.
- `sortRule` (optional, string): `DataTable.Select` sort rule; omission leaves the default order unchanged.
- `outputArray` (optional, int[]): destination array for row ids; if omitted, `RESULT` is used instead.

**Semantics**
- If the table does not exist, returns `-1`.
- Delegates filtering and sorting directly to `DataTable.Select(...)`.
- The returned row ids are the values of the table's first column, which is the auto-created `id` primary key.
- If `outputArray` is omitted, copied ids go to `RESULT:1`, `RESULT:2`, ... and `RESULT:0` is set to the full match count.
- If `outputArray` is supplied, copied ids go to that array starting at index `0`; `RESULT` is not updated by this path.
- Copying is clamped to the destination length (`RESULT` loses one slot because index `0` stores the count). Untouched slots are not cleared.
- The function return value is always the full match count, not the copied count.
- Explicitly omitted middle arguments remain omitted; for example, supplying only `sortRule` requires an omitted `filterExpression` slot.

**Errors & validation**
- Runtime error if `filterExpression` or `sortRule` is rejected by the underlying `DataTable.Select` parser.

**Examples**
- `count = DT_SELECT("db", "age >= 18", "age ASC", ids)`

## DT_TOXML (expression function)

**Summary**
- Serializes a named `DataTable` to XML and also exposes its schema XML.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_TOXML(tableName)`
- `DT_TOXML(tableName, schemaOutput)`

**Signatures / argument rules**
- `DT_TOXML(tableName)` → `string`
- `DT_TOXML(tableName, schemaOutput)` → `string`

**Arguments**
- `tableName` (string): table identifier.
- `schemaOutput` (optional, string variable): destination for schema XML; if omitted, schema is written to `RESULTS:1`.

**Semantics**
- If the table does not exist, returns `""`.
- On success, returns the data XML produced by `DataTable.WriteXml(...)`.
- Also writes the schema XML produced by `DataTable.WriteXmlSchema(...)`.
- If `schemaOutput` is omitted, that schema string is written to `RESULTS:1`; `RESULTS:0` is not used for this function.

**Errors & validation**
- None.

**Examples**
- `data '= DT_TOXML("db", schema)`

## DT_FROMXML (expression function)

**Summary**
- Loads a named `DataTable` from schema XML plus data XML.

**Tags**
- datatable
- data-structures

**Syntax**
- `DT_FROMXML(tableName, schemaXml, dataXml)`

**Signatures / argument rules**
- `DT_FROMXML(tableName, schemaXml, dataXml)` → `long`

**Arguments**
- `tableName` (string): table identifier.
- `schemaXml` (string): schema XML consumed by `ReadXmlSchema(...)`.
- `dataXml` (string): data XML consumed by `ReadXml(...)`.

**Semantics**
- Builds a fresh `DataTable`, reads `schemaXml`, then reads `dataXml` into it.
- If both reads succeed, replaces the existing named table or creates a new one and returns `1`.
- If any step fails, returns `0` and leaves the previously stored table unchanged.

**Errors & validation**
- None; all load/parse failures collapse to return value `0`.

**Examples**
- `DT_FROMXML("db", schema, data)`

## MOVETEXTBOX (expression function)

**Summary**
- Schedules a custom textbox position/width for the next textbox-position apply point used by input waits.

**Tags**
- ui
- input

**Syntax**
- `MOVETEXTBOX(xOffset, yOffset, width)`

**Signatures / argument rules**
- `MOVETEXTBOX(xOffset, yOffset, width)` → `long`

**Arguments**
- `xOffset` (int): requested left offset.
- `yOffset` (int): requested bottom offset.
- `width` (int): requested textbox width.

**Semantics**
- Does not immediately move the textbox widget.
- Instead stores a pending textbox placement that is later applied when the host processes textbox-position changes for primitive input waits.
- Placement normalization:
  - `xOffset` is clamped so the textbox stays inside the client area with a minimum width allowance of `50`,
  - `yOffset` is interpreted from the bottom edge and clamped so the textbox stays fully visible,
  - `width` is clamped to at least `50` and at most the current host-allowed width.
- The pending position remains until it is applied or replaced.
- Returns `1`.

**Errors & validation**
- None beyond normal integer-argument evaluation.

**Examples**
- `MOVETEXTBOX(50, 30, 300)`

## RESUMETEXTBOX (expression function)

**Summary**
- Immediately restores the textbox to its original/default position.

**Tags**
- ui
- input

**Syntax**
- `RESUMETEXTBOX(dummyX, dummyY, dummyWidth)`

**Signatures / argument rules**
- `RESUMETEXTBOX(dummyX, dummyY, dummyWidth)` → `long`

**Arguments**
- `dummyX` (int): ignored.
- `dummyY` (int): ignored.
- `dummyWidth` (int): ignored.

**Semantics**
- Current-build quirk: the function is registered with a three-integer call shape, but ignores all three values.
- Restores the textbox position/size to the host's remembered original/default textbox placement immediately.
- Clears the pending custom textbox-position state.
- Returns `1`.

**Errors & validation**
- Argument type/count errors follow the current three-integer registration.

**Examples**
- `RESUMETEXTBOX(0, 0, 0)`

## EXISTSOUND (expression function)

**Summary**
- Tests whether a file exists under the runtime's `sound` path prefix.

**Tags**
- files
- audio

**Syntax**
- `EXISTSOUND(mediaFile)`

**Signatures / argument rules**
- `EXISTSOUND(mediaFile)` → `long`

**Arguments**
- `mediaFile` (string): path suffix appended to the `sound` directory prefix.

**Semantics**
- Resolves the path as `./sound/<mediaFile>` under the host's current working directory, then canonicalizes it with the platform's full-path resolver.
- Returns `1` if that resolved path exists as a file.
- Returns `0` otherwise.
- No safe-path normalization is applied here:
  - subdirectories are allowed,
  - parent-directory segments such as `..` are not stripped before full-path resolution.

**Errors & validation**
- None.

**Examples**
- `EXISTSOUND("bgm/theme.ogg")`

## EXISTFUNCTION (expression function)

**Summary**
- Tests whether a user-defined script function/method label exists, with optional case-insensitive search override.

**Tags**
- reflection

**Syntax**
- `EXISTFUNCTION(funcName [, ignoreCase])`

**Signatures / argument rules**
- `EXISTFUNCTION(funcName)` → `long`
- `EXISTFUNCTION(funcName, ignoreCase)` → `long`

**Arguments**
- `funcName` (string): target script function label name.
- `ignoreCase` (optional, int; default `0`): non-zero forces a case-insensitive name scan.

**Semantics**
- Searches only user-defined script labels in the current non-event callable label table.
- Built-in expression functions are not counted here.
- Return codes:
  - `0`: not found,
  - `1`: ordinary script function label,
  - `2`: numeric method label,
  - `3`: string method label.
- Name matching:
  - if `ignoreCase` is omitted or `0`, lookup follows the runtime's current string-comparison mode,
  - if `ignoreCase != 0`, the function performs an explicit case-insensitive scan regardless of the current string-comparison mode.

**Errors & validation**
- None.

**Examples**
- `kind = EXISTFUNCTION("SHOP")`
- `kind = EXISTFUNCTION("shop", 1)`

## GDRAWGWITHROTATE (expression function)

**Summary**
- Draws one graphics surface onto another with rotation.

**Tags**
- graphics

**Syntax**
- `GDRAWGWITHROTATE(destID, srcID, angle)`
- `GDRAWGWITHROTATE(destID, srcID, angle, centerX, centerY)`

**Signatures / argument rules**
- `GDRAWGWITHROTATE(destID, srcID, angle)` → `long`
- `GDRAWGWITHROTATE(destID, srcID, angle, centerX, centerY)` → `long`

**Arguments**
- `destID` (int): destination graphics id.
- `srcID` (int): source graphics id.
- `angle` (int): clockwise rotation angle in degrees.
- `centerX` (optional, int): rotation-center x coordinate.
- `centerY` (optional, int): rotation-center y coordinate.

**Semantics**
- If either graphics surface does not exist or has already been disposed, returns `0`.
- Three-argument form uses the source image center `(srcWidth / 2, srcHeight / 2)` as the rotation center.
- Five-argument form uses the supplied center coordinates.
- On success draws the rotated source and returns `1`.
- Current-build quirk: the destination graphics transform is not reset afterward, so later draw calls on the same graphics observe the accumulated transform.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if either graphics id is negative or exceeds 32-bit range.
- Runtime error if `centerX` or `centerY` is outside signed 32-bit range.

**Examples**
- `GDRAWGWITHROTATE 0, 1, 90`

## GDRAWTEXT (expression function)

**Summary**
- Draws a string onto a graphics surface and exposes measured size through `RESULT`.

**Tags**
- graphics
- text

**Syntax**
- `GDRAWTEXT(gID, text)`
- `GDRAWTEXT(gID, text, x, y)`

**Signatures / argument rules**
- `GDRAWTEXT(gID, text)` → `long`
- `GDRAWTEXT(gID, text, x, y)` → `long`

**Arguments**
- `gID` (int): graphics id.
- `text` (string): text to draw.
- `x` (optional, int; default `0`): draw x coordinate.
- `y` (optional, int; default `0`): draw y coordinate.

**Semantics**
- If the target graphics does not exist or has already been disposed, returns `0`.
- Two-argument form draws at `(0, 0)`.
- Four-argument form draws at `(x, y)`.
- Fill / outline behavior follows the current graphics state: the fill uses the current brush or `Config.ForeColor` when no brush is set, and the outline uses the current pen or `Config.ForeColor` when no pen is set.
- Font behavior follows the current graphics state: if no font has been set with `GSETFONT`, drawing uses `Config.FontName` at size `100` with the current console font style.
- On success returns `1`, stores measured width in `RESULT:1`, and stores measured height in `RESULT:2`. `RESULT:0` is not used by this function.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error if `x` or `y` is outside signed 32-bit range.

**Examples**
- `GDRAWTEXT 0, "Hello", 20, 30`

## GGETFONT (expression function)

**Summary**
- Returns the current font family name of a graphics surface.

**Tags**
- graphics
- text

**Syntax**
- `GGETFONT(gID)`

**Signatures / argument rules**
- `GGETFONT(gID)` → `string`

**Arguments**
- `gID` (int): graphics id.

**Semantics**
- If the target graphics does not exist or has already been disposed, returns `""`.
- Otherwise returns the stored font family name.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error if no font has been set yet.

**Examples**
- `PRINTFORM %GGETFONT(0)%`

## GGETFONTSIZE (expression function)

**Summary**
- Returns the current font size of a graphics surface.

**Tags**
- graphics
- text

**Syntax**
- `GGETFONTSIZE(gID)`

**Signatures / argument rules**
- `GGETFONTSIZE(gID)` → `long`

**Arguments**
- `gID` (int): graphics id.

**Semantics**
- If the target graphics does not exist or has already been disposed, returns `0`.
- Otherwise returns the stored font size as an integer.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error if no font has been set yet.

**Examples**
- `PRINTFORML {GGETFONTSIZE(0)}`

## GGETFONTSTYLE (expression function)

**Summary**
- Returns the current font-style bitmask of a graphics surface.

**Tags**
- graphics
- text

**Syntax**
- `GGETFONTSTYLE(gID)`

**Signatures / argument rules**
- `GGETFONTSTYLE(gID)` → `long`

**Arguments**
- `gID` (int): graphics id.

**Semantics**
- If the target graphics does not exist or has already been disposed, returns `0`.
- Otherwise returns the stored style bitmask using `1=bold`, `2=italic`, `4=strikeout`, `8=underline`.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error if no font has been set yet.

**Examples**
- `PRINTFORML {GGETFONTSTYLE(0)}`

## GGETTEXTSIZE (expression function)

**Summary**
- Measures text with an explicit font specification.

**Tags**
- graphics
- text

**Syntax**
- `GGETTEXTSIZE(text, fontName, fontSize [, fontStyle])`

**Signatures / argument rules**
- `GGETTEXTSIZE(text, fontName, fontSize)` → `long`
- `GGETTEXTSIZE(text, fontName, fontSize, fontStyle)` → `long`

**Arguments**
- `text` (string): text to measure.
- `fontName` (string): font family name.
- `fontSize` (int): pixel size.
- `fontStyle` (optional, int; default `0`): bitmask `1=bold`, `2=italic`, `4=strikeout`, `8=underline`.

**Semantics**
- Measures the string using the supplied font specification without drawing anything.
- Returns the measured width.
- Also stores the measured height in `RESULT:1`. Other `RESULT` slots are not written by this function.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if the underlying font creation or measurement path fails.

**Examples**
- `width = GGETTEXTSIZE("Hello", "Arial", 48, 1)`

## GGETBRUSH (expression function)

**Summary**
- Returns the current brush color of a graphics surface as unsigned ARGB.

**Tags**
- graphics

**Syntax**
- `GGETBRUSH(gID)`

**Signatures / argument rules**
- `GGETBRUSH(gID)` → `long`

**Arguments**
- `gID` (int): graphics id.

**Semantics**
- If the target graphics does not exist or has already been disposed, returns `0`.
- Otherwise returns the current brush color as `0xAARRGGBB` in the range `0 <= value <= 0xFFFFFFFF`.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error if no brush has been set yet.

**Examples**
- `PRINTFORML {GGETBRUSH(0)}`

## GGETPEN (expression function)

**Summary**
- Returns the current pen color of a graphics surface as unsigned ARGB.

**Tags**
- graphics

**Syntax**
- `GGETPEN(gID)`

**Signatures / argument rules**
- `GGETPEN(gID)` → `long`

**Arguments**
- `gID` (int): graphics id.

**Semantics**
- If the target graphics does not exist or has already been disposed, returns `0`.
- Otherwise returns the current pen color as `0xAARRGGBB` in the range `0 <= value <= 0xFFFFFFFF`.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error if no pen has been set yet.

**Examples**
- `PRINTFORML {GGETPEN(0)}`

## GGETPENWIDTH (expression function)

**Summary**
- Returns the current pen width of a graphics surface.

**Tags**
- graphics

**Syntax**
- `GGETPENWIDTH(gID)`

**Signatures / argument rules**
- `GGETPENWIDTH(gID)` → `long`

**Arguments**
- `gID` (int): graphics id.

**Semantics**
- If the target graphics does not exist or has already been disposed, returns `0`.
- Otherwise returns the current pen width truncated to `long`.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error if no pen has been set yet.

**Examples**
- `PRINTFORML {GGETPENWIDTH(0)}`

## GETMEMORYUSAGE (expression function)

**Summary**
- Returns the current process working-set size in bytes.

**Tags**
- runtime

**Syntax**
- `GETMEMORYUSAGE()`

**Signatures / argument rules**
- `GETMEMORYUSAGE()` → `long`

**Arguments**
- None.

**Semantics**
- Returns the current process `WorkingSet64` value.
- The unit is bytes.
- This is an operating-system working-set measurement, not a managed-heap-only measurement.

**Errors & validation**
- None.

**Examples**
- `bytes = GETMEMORYUSAGE()`

## CLEARMEMORY (expression function)

**Summary**
- Forces a garbage collection and returns the change in process working-set size.

**Tags**
- runtime

**Syntax**
- `CLEARMEMORY()`

**Signatures / argument rules**
- `CLEARMEMORY()` → `long`

**Arguments**
- None.

**Semantics**
- Measures the current process working set.
- Runs `GC.Collect()`.
- Measures the working set again.
- Returns `before - after` in bytes.
- A positive value means the working set became smaller.
- A negative value is possible if the working set becomes larger instead.

**Errors & validation**
- None.

**Examples**
- `freed = CLEARMEMORY()`

## GETTEXTBOX (expression function)

**Summary**
- Returns the current contents of the host textbox widget.

**Tags**
- ui
- input

**Syntax**
- `GETTEXTBOX()`

**Signatures / argument rules**
- `GETTEXTBOX()` → `string`

**Arguments**
- None.

**Semantics**
- Returns the textbox's current text exactly as stored by the host widget at call time.
- This does not wait for input.
- This reads the live widget state, not a saved snapshot.

**Errors & validation**
- None.

**Examples**
- `s = GETTEXTBOX()`

## SETTEXTBOX (expression function)

**Summary**
- Replaces the current contents of the host textbox widget.

**Tags**
- ui
- input

**Syntax**
- `SETTEXTBOX(text)`

**Signatures / argument rules**
- `SETTEXTBOX(text)` → `long`

**Arguments**
- `text` (string): replacement textbox content.

**Semantics**
- Immediately replaces the textbox widget's text with `text`.
- Returns `1`.

**Errors & validation**
- None.

**Examples**
- `SETTEXTBOX("search text")`

## ERDNAME (expression function)

**Summary**
- Reverse-maps an integer value back to an ERD key name for a user-defined variable.

**Tags**
- erd
- string-key

**Syntax**
- `ERDNAME(varTerm, value [, dimension])`

**Signatures / argument rules**
- `ERDNAME(varTerm, value)` → `string`
- `ERDNAME(varTerm, value, dimension)` → `string`

**Arguments**
- `varTerm` (variable term): selects the declared variable name whose ERD dictionary should be queried.
  - This function uses only the identifier name.
  - Any written `:` subscripts do not participate in the reverse lookup itself.
- `value` (int): integer value to reverse-map.
- `dimension` (optional, int): ERD dimension selector.
  - Omitted: uses the base ERD dictionary `name`.
  - Supplied `n`: uses the ERD dictionary `name@n`.

**Semantics**
- Performs reverse lookup against ERD dictionaries only.
- Built-in CSV-name / alias tables are not consulted.
- Returns the matching key string if the selected ERD dictionary contains an entry whose value equals `value`.
- Returns `""` if:
  - `value < 0`,
  - no matching ERD dictionary exists,
  - or no key in that dictionary maps to `value`.
- If multiple ERD keys share the same integer value, scripts should not rely on a stable public choice among them.

**Errors & validation**
- Parse/type error if `varTerm` is not a variable term.
- Otherwise, missing ERD data is not an error; it returns `""`.

**Examples**
```erabasic
S = ERDNAME(HOGE3D, 0, 1)
S = ERDNAME(HOGE3D, 1, 2)
```

## SPRITEDISPOSEALL (expression function)

**Summary**
- Disposes multiple sprites and returns how many were removed.

**Tags**
- graphics
- ui
- resources

**Syntax**
- `SPRITEDISPOSEALL(<includeCsvSprites>)`

**Signatures / argument rules**
- Signature: `int SPRITEDISPOSEALL(int includeCsvSprites)`.

**Arguments**
- `<includeCsvSprites>` (int): controls whether sprites loaded from content/resource CSVs are also disposed.
  - `0`: keep CSV/resource sprites.
  - non-zero: dispose all sprites, including CSV/resource sprites.

**Semantics**
- Disposes sprite entries in bulk.
- If `<includeCsvSprites> == 0`:
  - disposes only non-resource sprites,
  - preserves the sprites that come from the resource/content tables,
  - returns the number of sprites removed by that selective disposal.
- If `<includeCsvSprites> != 0`:
  - disposes all sprites,
  - returns the total number of sprites that were present before clearing.
- Layer boundary:
  - this does not itself print anything or modify the normal output model,
  - but later rendering that depended on disposed sprites may stop drawing them.

**Errors & validation**
- None beyond normal integer-expression evaluation.

**Examples**
```erabasic
R = SPRITEDISPOSEALL(0)
R = SPRITEDISPOSEALL(1)
```

## GDRAWLINE (expression function)

**Summary**
- Draws one straight line onto a graphics surface.

**Tags**
- graphics
- ui

**Syntax**
- `GDRAWLINE(<graphicsId>, <fromX>, <fromY>, <toX>, <toY>)`

**Signatures / argument rules**
- Signature: `int GDRAWLINE(int graphicsId, int fromX, int fromY, int toX, int toY)`.
- All five arguments are evaluated as integer expressions.

**Arguments**
- `<graphicsId>` (int): target graphics-surface ID.
- `<fromX>`, `<fromY>` (int): line start point.
- `<toX>`, `<toY>` (int): line end point.

**Semantics**
- Draws a straight line from `(<fromX>, <fromY>)` to `(<toX>, <toY>)` on the target graphics surface.
- This affects only that graphics surface; it does not itself print to the console or modify the normal output model.
- Drawing state:
  - if the target graphics surface currently has an explicit drawing pen/configuration, that pen is used,
  - otherwise the line is drawn with the host's default foreground-color pen.
- Return value:
  - returns `1` when the draw operation is performed,
  - returns `0` when the target graphics object exists only as an uncreated handle/surface and therefore no drawing occurs.

**Errors & validation**
- Runtime error if the host is using the `WINAPI` text-drawing mode; this method is GDI+-only.
- Runtime error if `<graphicsId> < 0` or `<graphicsId> > 2147483647`.
- Runtime error if any coordinate is outside the 32-bit signed integer range.

**Examples**
```erabasic
R = GDRAWLINE(GID, 0, 0, 100, 100)
```

## GETDISPLAYLINE (expression function)

**Summary**
- Returns the plain-text content of one currently visible **display line** in the normal output area.

**Tags**
- io

**Syntax**
- `GETDISPLAYLINE(<lineNumber>)`

**Signatures / argument rules**
- Signature: `string GETDISPLAYLINE(int lineNumber)`.
- `<lineNumber>` is evaluated as an integer expression.

**Arguments**
- `<lineNumber>` (int): zero-based index into the current visible display-line array of the normal output area.
  - `0` = the oldest currently visible display row.

**Semantics**
- Reads one entry from the current visible display-line array.
- This is a **display-row** getter, not a logical-line getter:
  - wrapped rows and explicit display breaks occupy separate indices,
  - one logical output line may therefore correspond to multiple `GETDISPLAYLINE` indices.
- Returns `""` if `<lineNumber> < 0` or if the requested visible row does not exist.
- Reads only the current visible normal output area:
  - pending buffered output is not included,
  - the separate `HTML_PRINT_ISLAND` layer is not included.
- The return value is plain text:
  - button metadata/clickability is flattened away,
  - inline images/shapes contribute their text/alt representation rather than structured HTML.
- Temporary lines are included while they remain visible.
- Because this getter reads the **current visible** display-line array, older rows that have already fallen out of the visible log are no longer accessible by index.

**Errors & validation**
- None.

**Examples**
```erabasic
PRINTL "AAA"
PRINTL "BBB"
S = GETDISPLAYLINE(0)
```

## GDASHSTYLE (expression function)

**Summary**
- Sets the dash style and dash cap of the current pen on a graphics surface.

**Tags**
- graphics

**Syntax**
- `GDASHSTYLE(gID, dashStyle, dashCap)`

**Signatures / argument rules**
- `GDASHSTYLE(gID, dashStyle, dashCap)` → `long`

**Arguments**
- `gID` (int): graphics id.
- `dashStyle` (int): numeric value written directly to `Pen.DashStyle`.
- `dashCap` (int): numeric value written directly to `Pen.DashCap`.

**Semantics**
- If the target graphics does not exist or has already been disposed, returns `0`.
- If no pen has been set yet, this function first creates one in `Config.ForeColor` with width `1`.
- Then writes the requested dash style / dash cap and returns `1`.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error if the underlying pen rejects the requested enum values.

**Examples**
- `GDASHSTYLE 0, 1, 3`

## GETDOINGFUNCTION (expression function)

**Summary**
- Returns the name of the currently executing parent label/function.

**Tags**
- runtime
- reflection

**Syntax**
- `GETDOINGFUNCTION()`

**Signatures / argument rules**
- `GETDOINGFUNCTION()` → `string`

**Arguments**
- None.

**Semantics**
- Returns the current scanning line's parent label name.
- Returns `""` if there is no active running function context, for example from a system-wait debug context.

**Errors & validation**
- None.

**Examples**
- `fn = GETDOINGFUNCTION()`

## FLOWINPUT (expression function)

**Summary**
- Updates persistent system-flow integer-input behavior flags and defaults.

**Tags**
- input
- system-flow

**Syntax**
- `FLOWINPUT(defaultValue [, allowMouseInput [, allowSkip [, forceSkip]]])`

**Signatures / argument rules**
- `FLOWINPUT(defaultValue)` → `long`
- `FLOWINPUT(defaultValue, allowMouseInput)` → `long`
- `FLOWINPUT(defaultValue, allowMouseInput, allowSkip)` → `long`
- `FLOWINPUT(defaultValue, allowMouseInput, allowSkip, forceSkip)` → `long`

**Arguments**
- `defaultValue` (int): stored default integer value for later system-flow waits.
- `allowMouseInput` (optional, int): when supplied, non-zero enables system-flow mouse/default handling; `0` disables it.
- `allowSkip` (optional, int): when supplied, non-zero enables skip-driven default resolution for later system-flow waits; `0` disables it.
- `forceSkip` (optional, int): when supplied, non-zero forces later system-flow waits to prefill the default result immediately; `0` disables it.

**Semantics**
- This function does not perform an input wait by itself.
- It mutates persistent process-level flags used later by system-flow waits such as title/shop/save/load flow input prompts.
- Field update rules:
  - `defaultValue` is always overwritten,
  - each later optional flag is overwritten only when that argument is supplied,
  - omitted later arguments leave their previous stored values unchanged.
- Future system-flow waits use these stored values as follows:
  - if `allowMouseInput != 0`, the wait request carries an integer default and enables system-flow mouse input,
  - if `allowSkip != 0` and message-skip is active, the default integer result is prefilled before the wait state is entered,
  - if `forceSkip != 0`, the default integer result is prefilled before the wait state is entered even without message-skip.
- These flags affect only system-flow waits built on the engine's dedicated system-input path, not ordinary script `INPUT*` statements.
- Returns `0`.

**Errors & validation**
- None beyond normal integer-argument evaluation.

**Examples**
- `FLOWINPUT(0, 1, 1, 0)`

## FLOWINPUTS (expression function)

**Summary**
- Updates persistent system-flow string-input mode and its stored default string.

**Tags**
- input
- system-flow

**Syntax**
- `FLOWINPUTS(enableStringMode [, defaultString])`

**Signatures / argument rules**
- `FLOWINPUTS(enableStringMode)` → `long`
- `FLOWINPUTS(enableStringMode, defaultString)` → `long`

**Arguments**
- `enableStringMode` (int): non-zero switches future system-flow waits to string-input mode; `0` switches them back to integer-input mode.
- `defaultString` (optional, string): stored default string for later system-flow waits.

**Semantics**
- This function does not perform an input wait by itself.
- It mutates persistent process-level state used later by system-flow waits.
- Field update rules:
  - `enableStringMode` is always overwritten,
  - `defaultString` is overwritten only when supplied,
  - omitted `defaultString` leaves the previous stored default string unchanged.
- When string mode is enabled, future system-flow waits request string input instead of integer input.
- The stored default string is injected into the actual wait request only when `FLOWINPUT`'s mouse/default mode is also enabled.
- These flags affect only system-flow waits built on the engine's dedicated system-input path, not ordinary script `INPUT*` statements.
- Returns `0`.

**Errors & validation**
- None beyond normal argument evaluation.

**Examples**
- `FLOWINPUTS(1, "")`

## GETMETH (expression function)

**Summary**
- Dynamically calls a user-defined numeric in-expression function by name.

**Tags**
- reflection

**Syntax**
- `GETMETH(name [, defaultValue [, args ...]])`

**Signatures / argument rules**
- `GETMETH(name)` → `long`
- `GETMETH(name, defaultValue)` → `long`
- `GETMETH(name, defaultValue [, args ...])` → `long`

**Arguments**
- `name` (string): target method name.
- `defaultValue` (optional, int): fallback return used only when no matching user-defined method is found.
- `args...` (optional, any): arguments forwarded to the resolved target method.

**Semantics**
- Resolves only user-defined in-expression functions/methods.
- Built-in expression functions are not searched here.
- `defaultValue` is a reserved fallback slot and is **not** forwarded to the target call.
  - To pass call arguments without a fallback, omit that slot explicitly.
- If no matching user-defined method is found:
  - returns `defaultValue` when it is present,
  - otherwise raises a runtime error.
- If a same-name script label exists but is not a method, this is an error, not a `not found` fallback case.
- If a matching method exists but the forwarded arguments are invalid, this is an error, not a fallback case.
- If a matching method exists but returns string type, this function raises a numeric-type mismatch error.

**Errors & validation**
- Runtime error when no method is found and `defaultValue` is omitted.
- Runtime error when the name resolves to a non-method script label.
- Runtime error when the resolved call fails argument validation.
- Runtime error when the resolved method is not integer-typed.

**Examples**
- `score = GETMETH("MYSCORE", 0, 1, 2)`

## GETMETHS (expression function)

**Summary**
- Dynamically calls a user-defined string in-expression function by name.

**Tags**
- reflection

**Syntax**
- `GETMETHS(name [, defaultValue [, args ...]])`

**Signatures / argument rules**
- `GETMETHS(name)` → `string`
- `GETMETHS(name, defaultValue)` → `string`
- `GETMETHS(name, defaultValue [, args ...])` → `string`

**Arguments**
- `name` (string): target method name.
- `defaultValue` (optional, string): fallback return used only when no matching user-defined method is found.
- `args...` (optional, any): arguments forwarded to the resolved target method.

**Semantics**
- Resolves only user-defined in-expression functions/methods.
- Built-in expression functions are not searched here.
- `defaultValue` is a reserved fallback slot and is **not** forwarded to the target call.
  - To pass call arguments without a fallback, omit that slot explicitly.
- If no matching user-defined method is found:
  - returns `defaultValue` when it is present,
  - otherwise raises a runtime error.
- If a same-name script label exists but is not a method, this is an error, not a `not found` fallback case.
- If a matching method exists but the forwarded arguments are invalid, this is an error, not a fallback case.
- If a matching method exists but returns integer type, this function raises a string-type mismatch error.

**Errors & validation**
- Runtime error when no method is found and `defaultValue` is omitted.
- Runtime error when the name resolves to a non-method script label.
- Runtime error when the resolved call fails argument validation.
- Runtime error when the resolved method is not string-typed.

**Examples**
- `name = GETMETHS("MYNAME", "", 1, 2)`

## EXISTMETH (expression function)

**Summary**
- Tests whether a user-defined in-expression function is callable with zero arguments.

**Tags**
- reflection

**Syntax**
- `EXISTMETH(name)`

**Signatures / argument rules**
- `EXISTMETH(name)` → `long`

**Arguments**
- `name` (string): target method name.

**Semantics**
- Resolves only user-defined in-expression functions/methods.
- Built-in expression functions are not searched here.
- Resolution is attempted with zero forwarded call arguments.
- Returns `0` if:
  - no matching user-defined method is found,
  - the same-name label is not a method,
  - or zero-argument resolution fails.
- Otherwise returns a bitmask describing the resolved zero-arg callable result type:
  - `1`: callable as integer,
  - `2`: callable as string,
  - `3`: supports both.

**Errors & validation**
- None; resolution failures collapse to `0`.

**Examples**
- `kind = EXISTMETH("MYSCORE")`

## BITMAP_CACHE_ENABLE (expression function)

**Summary**
- Toggles bitmap-cache rendering for subsequently created output lines.

**Tags**
- ui
- graphics

**Syntax**
- `BITMAP_CACHE_ENABLE(enable)`

**Signatures / argument rules**
- `BITMAP_CACHE_ENABLE(enable)` → `long`

**Arguments**
- `enable` (int): non-zero enables bitmap-cache mode for future lines; `0` disables it.

**Semantics**
- Sets the console's persistent `bitmapCacheEnabledForNextLine` flag.
- Each future printed line copies that flag when the line object is created.
- Existing already-created lines are not retroactively changed.
- The setting remains in effect for subsequent lines until another call changes it.
- Returns `0`.

**Errors & validation**
- None beyond normal integer-argument evaluation.

**Examples**
- `BITMAP_CACHE_ENABLE(1)`

## HOTKEY_STATE (expression function)

**Summary**
- Writes one entry in the host hotkey state array used by the optional hotkey subsystem.

**Tags**
- input
- host

**Syntax**
- `HOTKEY_STATE(index, value)`

**Signatures / argument rules**
- `HOTKEY_STATE(index, value)` → `long`

**Arguments**
- `index` (int): state-array index to update.
- `value` (int): new value to store.

**Semantics**
- Writes `state[index] = value` in the host hotkey state array.
- This affects only the optional host hotkey subsystem; by itself it does not enable hotkeys.
- Returns `0`.

**Errors & validation**
- Runtime error if the state array was not initialized first via `HOTKEY_STATE_INIT`.
- Runtime error if `index` is outside the allocated state-array bounds.

**Examples**
- `HOTKEY_STATE(2, 1)`

## HOTKEY_STATE_INIT (expression function)

**Summary**
- Allocates/reinitializes the host hotkey state array used by the optional hotkey subsystem.

**Tags**
- input
- host

**Syntax**
- `HOTKEY_STATE_INIT(size)`

**Signatures / argument rules**
- `HOTKEY_STATE_INIT(size)` → `long`

**Arguments**
- `size` (int): new state-array length.

**Semantics**
- Allocates a new hotkey state array of length `size`.
- Any previous hotkey state array contents are discarded.
- This prepares the array later used by `HOTKEY_STATE` and the optional hotkey subsystem.
- Returns `0`.

**Errors & validation**
- Runtime error if `size` is negative or otherwise invalid for array allocation.

**Examples**
- `HOTKEY_STATE_INIT(8)`
