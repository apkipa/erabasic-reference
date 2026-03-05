# EraBasic Built-ins Reference — Engine Dump (Emuera / EvilMask)

Generated from engine source on `2026-03-05`.

This file is **not user-facing**.
It exists for doc authors and fact-checking, and includes engine-extracted skeletons, validation structures, and file/line references.

User-facing built-ins documentation lives in:
- `erabasic-reference/builtins-reference.md`

This document is intentionally **no-table** and uses a per-entry template:
- Summary / Syntax / Arguments / Defaults / Semantics / Errors / Examples / Engine refs

Important:
- The generator can reliably extract hooks (argument builders, flags, code entry points).
- Deeper semantic structure often requires manual analysis; “engine-extracted key operations” are a starting point, not a full spec.

# Expression functions as statements (METHOD-dispatch)

In this engine, **expression functions** (the `# Expression functions (methods)` section below) are also registered as **instruction keywords** when there is no name conflict with an existing instruction keyword.
This allows writing method names as standalone statements (without `=` assignment).

Statement form (best-effort description):
- A line whose keyword matches an expression function name is executed by a shared internal instruction (`METHOD_Instruction`).
- The argument text is parsed as comma-separated expressions (parentheses are allowed but not required).
- The engine validates argument types/count using the method’s own argument checker.
- The method is evaluated; if it returns:
  - `long`: assigns `RESULT` (integer).
  - `string`: assigns `RESULTS` (string).

Examples:
- `TOSTR 42` sets `RESULTS` to `"42"`.
- `FINDCHARA NAME, "Alice"` sets `RESULT` to the found index (or `-1`).

# Argument specs (FunctionArgType)

Each instruction registered with an `Arg spec` references one of the `FunctionArgType` values below.
The entries here are generated from `ArgumentParser.Initialize()` and (best-effort) builder-class constructors.

How to interpret argument parsing (important):
- The `Arg spec` / builder largely determines whether the argument region is parsed as raw text vs expressions vs FORM, and whether `;` starts an inline comment or is literal.
- This document intentionally does not repeat the parsing rules per instruction. See `argument-parsing-modes.md` for the normative, self-contained parsing-mode definitions and examples.

## Argument spec: BIT_ARG

- Builder: `BIT_ARG_ArgumentBuilder()`
- Hint (translated, best-effort): <changeable int variable term>,<int>*n (SP_SETが使えないため新設)
- Hint (raw comment): `<可変数値変数>,<数値>*n (SP_SETが使えないため新設)`
- Type pattern: `[typeof(long), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `2`.
- Variadic (`argAny`): `true`.

## Argument spec: CASE

- Builder: `CASE_ArgumentBuilder()`
- Hint (translated, best-effort): <CASE条件式>(, <CASE条件式>...)
- Hint (raw comment): `<CASE条件式>(, <CASE条件式>...)`

## Argument spec: EXPRESSION

- Builder: `EXPRESSION_ArgumentBuilder(false)`
- Hint (translated, best-effort): <式>, variable type unconstrained
- Hint (raw comment): `<式>、変数の型は不問`
- Type pattern: `[typeof(void)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

## Argument spec: EXPRESSION_NULLABLE

- Builder: `EXPRESSION_ArgumentBuilder(true)`
- Hint (translated, best-effort): <式>, variable type unconstrained
- Hint (raw comment): `<式>、変数の型は不問`
- Type pattern: `[typeof(void)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

## Argument spec: FORM_STR

- Builder: `FORM_STR_ArgumentBuilder(false)`
- Hint (translated, best-effort): FORM string型。
- Hint (raw comment): `書式付文字列型。`

## Argument spec: FORM_STR_ANY

- Builder: `FORM_STR_ANY_ArgumentBuilder()`
- Hint (translated, best-effort): 1つ以上のFORMstringをvariadic
- Hint (raw comment): `1つ以上のFORM文字列を任意数`

## Argument spec: FORM_STR_NULLABLE

- Builder: `FORM_STR_ArgumentBuilder(true)`
- Hint (translated, best-effort): FORM string型。optional
- Hint (raw comment): `書式付文字列型。省略可能`

## Argument spec: INT_ANY

- Builder: `INT_ANY_ArgumentBuilder()`
- Hint (translated, best-effort): 1つ以上のintをvariadic
- Hint (raw comment): `1つ以上の数値を任意数`
- Type pattern: `[typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.
- Variadic (`argAny`): `true`.

## Argument spec: INT_EXPRESSION

- Builder: `INT_EXPRESSION_ArgumentBuilder(false)`
- Hint (translated, best-effort): int expression。optional
- Hint (raw comment): `数式型。省略可能`
- Type pattern: `[typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

## Argument spec: INT_EXPRESSION_NULLABLE

- Builder: `INT_EXPRESSION_ArgumentBuilder(true)`
- Hint (translated, best-effort): int expression
- Hint (raw comment): `数式型`
- Type pattern: `[typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

## Argument spec: METHOD

- Builder: `METHOD_ArgumentBuilder()`
- Hint (translated, best-effort): 式中関数。
- Hint (raw comment): `式中関数。`

## Argument spec: SP_BAR

- Builder: `SP_BAR_ArgumentBuilder()`
- Hint (translated, best-effort): <int>,<int>,<int>
- Hint (raw comment): `<数値>,<数値>,<数値>`
- Type pattern: `[typeof(long), typeof(long), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).

## Argument spec: SP_BUTTON

- Builder: `SP_BUTTON_ArgumentBuilder()`
- Hint (translated, best-effort): <string expr>,<int expr>
- Hint (raw comment): `<文字列式>,<数式>`
- Type pattern: `[typeof(string), typeof(void)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).

## Argument spec: SP_CALL

- Builder: `SP_CALL_ArgumentBuilder(false, false)`
- Hint (translated, best-effort): <string>,<引数>,... //引数はoptional
- Hint (raw comment): `<文字列>,<引数>,... //引数は省略可能`

## Argument spec: SP_CALLCSHARP

- Builder: `SP_CALLSHARP_ArgumentBuilder()`

## Argument spec: SP_CALLF

- Builder: `SP_CALL_ArgumentBuilder(true, false)`

## Argument spec: SP_CALLFORM

- Builder: `SP_CALL_ArgumentBuilder(false, true)`
- Hint (translated, best-effort): <FORM string>,<引数>,... //引数はoptional
- Hint (raw comment): `<書式付文字列>,<引数>,... //引数は省略可能`

## Argument spec: SP_CALLFORMF

- Builder: `SP_CALL_ArgumentBuilder(true, true)`
- Hint (translated, best-effort): <FORM string>,<引数>,... //引数はoptional
- Hint (raw comment): `<書式付文字列>,<引数>,... //引数は省略可能`

## Argument spec: SP_COLOR

- Builder: `SP_COLOR_ArgumentBuilder()`
- Type pattern: `[typeof(long), typeof(long), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `1`.

## Argument spec: SP_CONTROL_ARRAY

- Builder: `SP_CONTROL_ARRAY_ArgumentBuilder()`
- Hint (translated, best-effort): <changeable variable term>,<int>,<int>
- Hint (raw comment): `<可変変数>,<数値>,<数値>`
- Type pattern: `[typeof(void), typeof(long), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).

## Argument spec: SP_COPYCHARA

- Builder: `SP_SWAP_ArgumentBuilder(true)`
- Hint (translated, best-effort): <int>(, <int)第二引数省略可
- Hint (raw comment): `<数値>(, <数値)第二引数省略可`
- Type pattern: `[typeof(long), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `1`.

## Argument spec: SP_COPY_ARRAY

- Builder: `SP_COPY_ARRAY_Arguments()`
- Hint (translated, best-effort): <string expr>,<string expr>
- Hint (raw comment): `<文字列式>,<文字列式>`
- Custom parser (builder class not indexed by this generator).

## Argument spec: SP_CVAR_SET

- Builder: `SP_CVAR_SET_ArgumentBuilder()`
- Hint (translated, best-effort): <changeable variable term>,<式>,<int expr or string expr or null>(,<range start>, <range end>)
- Hint (raw comment): `<可変変数>,<式>,<数式 or 文字列式 or null>(,<範囲初値>, <範囲終値>)`
- Type pattern: `[typeof(void), typeof(void), typeof(void), typeof(long), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `1`.

## Argument spec: SP_DT_COLUMN_OPTIONS

- Builder: `SP_DT_COLUMN_OPTIONS_ArgumentBuilder()`
- Type pattern: `null;// new Type[] { typeof(string), typeof(string), typeof(Int64), typeof(Int64), typeof(Int64) }` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).

## Argument spec: SP_FOR_NEXT

- Builder: `SP_FOR_NEXT_ArgumentBuilder()`
- Hint (translated, best-effort): <changeable int variable term>,<int>,<int>,<int> //引数はoptional
- Hint (raw comment): `<可変数値変数>,<数値>,<数値>,<数値> //引数は省略可能`
- Type pattern: `[typeof(long), null, typeof(long), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `3`.

## Argument spec: SP_GETINT

- Builder: `SP_GETINT_ArgumentBuilder()`
- Hint (translated, best-effort): <changeable int variable term>(今までこれがないことに驚いた)
- Hint (raw comment): `<可変数値変数>(今までこれがないことに驚いた)`
- Type pattern: `[typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

## Argument spec: SP_HTMLSPLIT

- Builder: `SP_HTMLSPLIT_ArgumentBuilder()`
- Type pattern: `[typeof(string), typeof(string), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `1`.

## Argument spec: SP_HTML_PRINT

- Builder: `SP_HTML_PRINT_ArgumentBuilder()`
- Type pattern: `null;// new Type[] { typeof(string), typeof(string), typeof(Int64), typeof(Int64), typeof(Int64) }` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).

## Argument spec: SP_INPUT

- Builder: `SP_INPUT_ArgumentBuilder()`
- Hint (translated, best-effort): (<int>) //引数はオプションでないのがデフォ, INT_EXPRESSION_NULLABLEとは処理が違う
- Hint (raw comment): `(<数値>) //引数はオプションでないのがデフォ、INT_EXPRESSION_NULLABLEとは処理が違う`
- Type pattern: `[typeof(long), typeof(long), typeof(long), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

## Argument spec: SP_INPUTS

- Builder: `SP_INPUTS_ArgumentBuilder()`
- Hint (translated, best-effort): (<FORMstring>) //引数はオプションでないのがデフォ, STR_EXPRESSION_NULLABLEとは処理が違う
- Hint (raw comment): `(<FORM文字列>) //引数はオプションでないのがデフォ、STR_EXPRESSION_NULLABLEとは処理が違う`
- Type pattern: `[typeof(string)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

## Argument spec: SP_POWER

- Builder: `SP_POWER_ArgumentBuilder()`
- Hint (translated, best-effort): <changeable int variable term>,<int>,<int>
- Hint (raw comment): `<可変数値変数>,<数値>,<数値>`
- Type pattern: `[typeof(long), typeof(long), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).

## Argument spec: SP_PRINTV

- Builder: `SP_PRINTV_ArgumentBuilder()`
- Hint (translated, best-effort): 複数int expression。'～～,string可
- Hint (raw comment): `複数数式型。'～～,文字列可`

## Argument spec: SP_PRINT_IMG

- Builder: `SP_PRINT_IMG_ArgumentBuilder()`
- Type pattern: `null;// new Type[] { typeof(string), typeof(string), typeof(Int64), typeof(Int64), typeof(Int64) }` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `1`.

## Argument spec: SP_PRINT_RECT

- Builder: `SP_PRINT_SHAPE_ArgumentBuilder(4)`
- Type pattern: `[typeof(long), typeof(long), typeof(long), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `1`.

## Argument spec: SP_PRINT_SPACE

- Builder: `SP_PRINT_SHAPE_ArgumentBuilder(1)`
- Type pattern: `[typeof(long), typeof(long), typeof(long), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `1`.

## Argument spec: SP_REF

- Builder: `SP_REF_ArgumentBuilder(false)`
- Type pattern: `[typeof(void), typeof(void)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `2`.

## Argument spec: SP_REFBYNAME

- Builder: `SP_REF_ArgumentBuilder(true)`
- Type pattern: `[typeof(void), typeof(void)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `2`.

## Argument spec: SP_SAVECHARA

- Builder: `SP_SAVECHARA_ArgumentBuilder()`
- Hint (translated, best-effort): <int>, <string expr>, <int>(, <int>...)第二引数省略可
- Hint (raw comment): `<数値>, <文字列式>, <数値>（, <数値>...）第二引数省略可`
- Type pattern: `[typeof(string), typeof(string), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `3`.
- Variadic (`argAny`): `true`.

## Argument spec: SP_SAVEDATA

- Builder: `SP_SAVEDATA_ArgumentBuilder()`
- Hint (translated, best-effort): <int>,<string expr>
- Hint (raw comment): `<数値>,<文字列式>`
- Type pattern: `[typeof(long), typeof(string)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).

## Argument spec: SP_SAVEVAR

- Builder: `SP_SAVEVAR_ArgumentBuilder()`
- Hint (translated, best-effort): <int>,<string expr>, <variable term>(, <variable term>...)
- Hint (raw comment): `<数値>,<文字列式>, <変数>（, <変数>...）`
- Type pattern: `[typeof(string), typeof(string), typeof(void)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `3`.
- Variadic (`argAny`): `true`.

## Argument spec: SP_SET

- Builder: `SP_SET_ArgumentBuilder()`
- Hint (translated, best-effort): changeable int variable term / int expression。
- Hint (raw comment): `可変数値変数・数式型。`

## Argument spec: SP_SETS

- Builder: `SP_SET_ArgumentBuilder()`
- Hint (translated, best-effort): changeable string variable term / 単純又は複合string型。
- Hint (raw comment): `可変文字列変数・単純又は複合文字列型。`

## Argument spec: SP_SHIFT_ARRAY

- Builder: `SP_SHIFT_ARRAY_ArgumentBuilder()`
- Hint (translated, best-effort): <changeable variable term>,<int>,<intorstring>(,<int>,<int>)
- Hint (raw comment): `<可変変数>,<数値>,<数値or文字列>(,<数値>,<数値>)`
- Type pattern: `[typeof(void), typeof(long), typeof(void), typeof(long), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `3`.

## Argument spec: SP_SORTARRAY

- Builder: `SP_SORT_ARRAY_ArgumentBuilder()`
- Hint (translated, best-effort): <対象variable term>, (<sort order>, <range start>, <range end>)
- Hint (raw comment): `<対象変数>, (<ソート順序>, <範囲初値>, <範囲終値>)`

## Argument spec: SP_SORTCHARA

- Builder: `SP_SORTCHARA_ArgumentBuilder()`
- Hint (translated, best-effort): <キャラクタvariable term>,<sort order>(両方optional)
- Hint (raw comment): `<キャラクタ変数>,<ソート順序>(両方省略可能)`

## Argument spec: SP_SPLIT

- Builder: `SP_SPLIT_ArgumentBuilder()`
- Hint (translated, best-effort): <string expr>, <string expr>, <可変文字variable term>
- Hint (raw comment): `<文字列式>, <文字列式>, <可変文字変数>`
- Type pattern: `[typeof(string), typeof(string), typeof(string), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `3`.

## Argument spec: SP_SWAP

- Builder: `SP_SWAP_ArgumentBuilder(false)`
- Hint (translated, best-effort): <int>,<int>
- Hint (raw comment): `<数値>,<数値>`
- Type pattern: `[typeof(long), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `1`.

## Argument spec: SP_SWAPVAR

- Builder: `SP_SWAPVAR_ArgumentBuilder()`
- Hint (translated, best-effort): <changeable variable term>,<changeable variable term>(同型のみ)
- Hint (raw comment): `<可変変数>,<可変変数>(同型のみ)`
- Type pattern: `[typeof(void), typeof(void)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).

## Argument spec: SP_TIMES

- Builder: `SP_TIMES_ArgumentBuilder()`
- Hint (translated, best-effort): <int variable term>,<実数定数>
- Hint (raw comment): `<数値型変数>,<実数定数>`

## Argument spec: SP_TINPUT

- Builder: `SP_TINPUT_ArgumentBuilder()`
- Hint (translated, best-effort): <int>,<int>(,<int>,<string>)
- Hint (raw comment): `<数値>,<数値>(,<数値>,<文字列>)`

## Argument spec: SP_TINPUTS

- Builder: `SP_TINPUTS_ArgumentBuilder()`
- Hint (translated, best-effort): <int>,<string expr>(,<int>,<string>)
- Hint (raw comment): `<数値>,<文字列式>(,<数値>,<文字列>)`

## Argument spec: SP_VAR

- Builder: `SP_VAR_ArgumentBuilder()`
- Hint (translated, best-effort): <variable term>
- Hint (raw comment): `<変数>`

## Argument spec: SP_VAR_SET

- Builder: `SP_VAR_SET_ArgumentBuilder()`
- Hint (translated, best-effort): <changeable variable term>,<int expr or string expr or null>(,<range start>, <range end>)
- Hint (raw comment): `<可変変数>,<数式 or 文字列式 or null>(,<範囲初値>, <範囲終値>)`
- Type pattern: `[typeof(void), typeof(void), typeof(long), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `1`.

## Argument spec: STR

- Builder: `STR_ArgumentBuilder(false)`
- Hint (translated, best-effort): raw string
- Hint (raw comment): `単純文字列型`

## Argument spec: STR_EXPRESSION

- Builder: `STR_EXPRESSION_ArgumentBuilder(false)`
- Hint (translated, best-effort): string expression
- Hint (raw comment): `文字列式型`
- Type pattern: `[typeof(string)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

## Argument spec: STR_EXPRESSION_NULLABLE

- Builder: `STR_EXPRESSION_ArgumentBuilder(true)`
- Type pattern: `[typeof(string)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

## Argument spec: STR_NULLABLE

- Builder: `STR_ArgumentBuilder(true)`
- Hint (translated, best-effort): raw string, optional
- Hint (raw comment): `単純文字列型、省略可能`

## Argument spec: VAR_INT

- Builder: `VAR_INT_ArgumentBuilder()`
- Hint (translated, best-effort): <changeable int variable term> //引数は省略可
- Hint (raw comment): `<可変数値変数> //引数は省略可`
- Type pattern: `[typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

## Argument spec: VAR_STR

- Builder: `VAR_STR_ArgumentBuilder()`
- Hint (translated, best-effort): <changeable int variable term> //引数は省略可
- Hint (raw comment): `<可変数値変数> //引数は省略可`
- Type pattern: `[typeof(string)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

## Argument spec: VOID

- Builder: `VOID_ArgumentBuilder()`
- Hint (translated, best-effort): no arguments
- Hint (raw comment): `引数なし`

# Instructions

Total (engine-registered keywords, incl. internal `SET`): `303`.

## SET (instruction)
**Summary**
- Describes **assignment statements** (`=`, `'=` and compound forms) and their observable behavior.
- Covers scalar assignment, compound assignment (`+=`, `-=`, etc.), `++/--`, and comma-list assignment into arrays.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new SET_Instruction()`
- Note: Internal pseudo-instruction used for assignment parsing (not a normal keyword).

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
- (TODO)

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

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Internal: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs` (`setFunc` / `SETFunction`)

## PRINT (instruction)
**Summary**
- Prints a **raw literal string** (the remainder of the source line) into the console output buffer.
- This entry also documents **common PRINT-family semantics** (suffix letters, buffering, `K`/`D`, `C`/`LC`).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

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

**Defaults / optional arguments**
- (TODO)

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
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- None for `PRINT` itself (argument is optional and not parsed as an expression).

**Examples**
- `PRINT Hello`
- `PRINT;Hello`
- `PRINT  (leading space is preserved)`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTL (instruction)
**Summary**
- `PRINTL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTL [<raw text>]`
- `PRINTL;<raw text>`

**Arguments**
- `<raw text>` (optional, default `""`): raw text, not an expression.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- After printing, flushes and appends a newline.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTL ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTW (instruction)
**Summary**
- `PRINTW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTW [<raw text>]`
- `PRINTW;<raw text>`

**Arguments**
- `<raw text>` (optional, default `""`): raw text, not an expression.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- After printing, flushes and appends a newline, then waits for a key.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTW ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTV (instruction)
**Summary**
- `PRINTV` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTV <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTV ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTVL (instruction)
**Summary**
- `PRINTVL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTVL <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- After printing, flushes and appends a newline.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTVL ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTVW (instruction)
**Summary**
- `PRINTVW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTVW <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- After printing, flushes and appends a newline, then waits for a key.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTVW ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTS (instruction)
**Summary**
- `PRINTS` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTS <string expr>`

**Arguments**
- A single string expression (must be present).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTS ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTSL (instruction)
**Summary**
- `PRINTSL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTSL <string expr>`

**Arguments**
- A single string expression (must be present).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- After printing, flushes and appends a newline.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSL ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTSW (instruction)
**Summary**
- `PRINTSW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTSW <string expr>`

**Arguments**
- A single string expression (must be present).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- After printing, flushes and appends a newline, then waits for a key.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSW ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTFORM (instruction)
**Summary**
- `PRINTFORM` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTFORM [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORM ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTFORML (instruction)
**Summary**
- `PRINTFORML` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTFORML [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- After printing, flushes and appends a newline.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORML ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTFORMW (instruction)
**Summary**
- `PRINTFORMW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTFORMW [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- After printing, flushes and appends a newline, then waits for a key.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMW ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTFORMS (instruction)
**Summary**
- `PRINTFORMS` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTFORMS <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMS ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTFORMSL (instruction)
**Summary**
- `PRINTFORMSL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTFORMSL <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- After printing, flushes and appends a newline.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMSL ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTFORMSW (instruction)
**Summary**
- `PRINTFORMSW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTFORMSW <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- After printing, flushes and appends a newline, then waits for a key.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMSW ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTK (instruction)
**Summary**
- `PRINTK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTK [<raw text>]`
- `PRINTK;<raw text>`

**Arguments**
- `<raw text>` (optional, default `""`): raw text, not an expression.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Applies kana conversion (`FORCEKANA` state) before printing.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTK ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTKL (instruction)
**Summary**
- `PRINTKL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTKL [<raw text>]`
- `PRINTKL;<raw text>`

**Arguments**
- `<raw text>` (optional, default `""`): raw text, not an expression.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Applies kana conversion (`FORCEKANA` state) before printing.
- After printing, flushes and appends a newline.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTKL ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTKW (instruction)
**Summary**
- `PRINTKW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTKW [<raw text>]`
- `PRINTKW;<raw text>`

**Arguments**
- `<raw text>` (optional, default `""`): raw text, not an expression.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Applies kana conversion (`FORCEKANA` state) before printing.
- After printing, flushes and appends a newline, then waits for a key.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTKW ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTVK (instruction)
**Summary**
- `PRINTVK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTVK <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- Applies kana conversion (`FORCEKANA` state) before printing.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTVK ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTVKL (instruction)
**Summary**
- `PRINTVKL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTVKL <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- Applies kana conversion (`FORCEKANA` state) before printing.
- After printing, flushes and appends a newline.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTVKL ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTVKW (instruction)
**Summary**
- `PRINTVKW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTVKW <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- Applies kana conversion (`FORCEKANA` state) before printing.
- After printing, flushes and appends a newline, then waits for a key.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTVKW ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTSK (instruction)
**Summary**
- `PRINTSK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTSK <string expr>`

**Arguments**
- A single string expression (must be present).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- Applies kana conversion (`FORCEKANA` state) before printing.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSK ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTSKL (instruction)
**Summary**
- `PRINTSKL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTSKL <string expr>`

**Arguments**
- A single string expression (must be present).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- Applies kana conversion (`FORCEKANA` state) before printing.
- After printing, flushes and appends a newline.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSKL ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTSKW (instruction)
**Summary**
- `PRINTSKW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTSKW <string expr>`

**Arguments**
- A single string expression (must be present).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- Applies kana conversion (`FORCEKANA` state) before printing.
- After printing, flushes and appends a newline, then waits for a key.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSKW ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTFORMK (instruction)
**Summary**
- `PRINTFORMK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTFORMK [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Applies kana conversion (`FORCEKANA` state) before printing.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMK ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTFORMKL (instruction)
**Summary**
- `PRINTFORMKL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTFORMKL [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Applies kana conversion (`FORCEKANA` state) before printing.
- After printing, flushes and appends a newline.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMKL ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTFORMKW (instruction)
**Summary**
- `PRINTFORMKW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTFORMKW [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Applies kana conversion (`FORCEKANA` state) before printing.
- After printing, flushes and appends a newline, then waits for a key.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMKW ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTFORMSK (instruction)
**Summary**
- `PRINTFORMSK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTFORMSK <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- Applies kana conversion (`FORCEKANA` state) before printing.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMSK ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTFORMSKL (instruction)
**Summary**
- `PRINTFORMSKL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTFORMSKL <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- Applies kana conversion (`FORCEKANA` state) before printing.
- After printing, flushes and appends a newline.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMSKL ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTFORMSKW (instruction)
**Summary**
- `PRINTFORMSKW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTFORMSKW <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- Applies kana conversion (`FORCEKANA` state) before printing.
- After printing, flushes and appends a newline, then waits for a key.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMSKW ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTD (instruction)
**Summary**
- `PRINTD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTD [<raw text>]`
- `PRINTD;<raw text>`

**Arguments**
- `<raw text>` (optional, default `""`): raw text, not an expression.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTD ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTDL (instruction)
**Summary**
- `PRINTDL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTDL [<raw text>]`
- `PRINTDL;<raw text>`

**Arguments**
- `<raw text>` (optional, default `""`): raw text, not an expression.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- After printing, flushes and appends a newline.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTDL ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTDW (instruction)
**Summary**
- `PRINTDW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTDW [<raw text>]`
- `PRINTDW;<raw text>`

**Arguments**
- `<raw text>` (optional, default `""`): raw text, not an expression.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- After printing, flushes and appends a newline, then waits for a key.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTDW ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTVD (instruction)
**Summary**
- `PRINTVD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTVD <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTVD ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTVDL (instruction)
**Summary**
- `PRINTVDL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTVDL <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- After printing, flushes and appends a newline.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTVDL ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTVDW (instruction)
**Summary**
- `PRINTVDW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTVDW <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- After printing, flushes and appends a newline, then waits for a key.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTVDW ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTSD (instruction)
**Summary**
- `PRINTSD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTSD <string expr>`

**Arguments**
- A single string expression (must be present).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSD ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTSDL (instruction)
**Summary**
- `PRINTSDL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTSDL <string expr>`

**Arguments**
- A single string expression (must be present).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- After printing, flushes and appends a newline.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSDL ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTSDW (instruction)
**Summary**
- `PRINTSDW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTSDW <string expr>`

**Arguments**
- A single string expression (must be present).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- After printing, flushes and appends a newline, then waits for a key.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSDW ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTFORMD (instruction)
**Summary**
- `PRINTFORMD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTFORMD [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMD ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTFORMDL (instruction)
**Summary**
- `PRINTFORMDL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTFORMDL [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- After printing, flushes and appends a newline.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMDL ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTFORMDW (instruction)
**Summary**
- `PRINTFORMDW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTFORMDW [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- After printing, flushes and appends a newline, then waits for a key.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMDW ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTFORMSD (instruction)
**Summary**
- `PRINTFORMSD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTFORMSD <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMSD ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTFORMSDL (instruction)
**Summary**
- `PRINTFORMSDL` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTFORMSDL <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- After printing, flushes and appends a newline.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMSDL ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTFORMSDW (instruction)
**Summary**
- `PRINTFORMSDW` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTFORMSDW <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- After printing, flushes and appends a newline, then waits for a key.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMSDW ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTSINGLE (instruction)
**Summary**
- `PRINTSINGLE` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTSINGLE [<raw text>]`
- `PRINTSINGLE;<raw text>`

**Arguments**
- `<raw text>` (optional, default `""`): raw text, not an expression.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLE ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTSINGLEV (instruction)
**Summary**
- `PRINTSINGLEV` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTSINGLEV <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLEV ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTSINGLES (instruction)
**Summary**
- `PRINTSINGLES` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTSINGLES <string expr>`

**Arguments**
- A single string expression (must be present).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLES ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTSINGLEFORM (instruction)
**Summary**
- `PRINTSINGLEFORM` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTSINGLEFORM [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLEFORM ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTSINGLEFORMS (instruction)
**Summary**
- `PRINTSINGLEFORMS` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTSINGLEFORMS <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLEFORMS ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTSINGLEK (instruction)
**Summary**
- `PRINTSINGLEK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTSINGLEK [<raw text>]`
- `PRINTSINGLEK;<raw text>`

**Arguments**
- `<raw text>` (optional, default `""`): raw text, not an expression.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.
- Applies kana conversion (`FORCEKANA` state) before printing.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLEK ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTSINGLEVK (instruction)
**Summary**
- `PRINTSINGLEVK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTSINGLEVK <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.
- Applies kana conversion (`FORCEKANA` state) before printing.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLEVK ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTSINGLESK (instruction)
**Summary**
- `PRINTSINGLESK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTSINGLESK <string expr>`

**Arguments**
- A single string expression (must be present).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.
- Applies kana conversion (`FORCEKANA` state) before printing.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLESK ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTSINGLEFORMK (instruction)
**Summary**
- `PRINTSINGLEFORMK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTSINGLEFORMK [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.
- Applies kana conversion (`FORCEKANA` state) before printing.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLEFORMK ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTSINGLEFORMSK (instruction)
**Summary**
- `PRINTSINGLEFORMSK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTSINGLEFORMSK <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.
- Applies kana conversion (`FORCEKANA` state) before printing.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLEFORMSK ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTSINGLED (instruction)
**Summary**
- `PRINTSINGLED` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTSINGLED [<raw text>]`
- `PRINTSINGLED;<raw text>`

**Arguments**
- `<raw text>` (optional, default `""`): raw text, not an expression.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLED ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTSINGLEVD (instruction)
**Summary**
- `PRINTSINGLEVD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTSINGLEVD <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLEVD ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTSINGLESD (instruction)
**Summary**
- `PRINTSINGLESD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTSINGLESD <string expr>`

**Arguments**
- A single string expression (must be present).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLESD ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTSINGLEFORMD (instruction)
**Summary**
- `PRINTSINGLEFORMD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTSINGLEFORMD [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLEFORMD ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTSINGLEFORMSD (instruction)
**Summary**
- `PRINTSINGLEFORMSD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTSINGLEFORMSD <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- If the produced output string is empty, this instruction does nothing.
- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.
- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSINGLEFORMSD ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTC (instruction)
**Summary**
- `PRINTC` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTC [<raw text>]`
- `PRINTC;<raw text>`

**Arguments**
- `<raw text>` (optional, default `""`): raw text, not an expression.
- If the resulting text is empty, nothing is appended.
- Output is converted to a fixed-width “cell” string (see below).

**Defaults / optional arguments**
- (TODO)

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
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTC ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTLC (instruction)
**Summary**
- `PRINTLC` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTLC [<raw text>]`
- `PRINTLC;<raw text>`

**Arguments**
- `<raw text>` (optional, default `""`): raw text, not an expression.
- If the resulting text is empty, nothing is appended.
- Output is converted to a fixed-width “cell” string (see below).

**Defaults / optional arguments**
- (TODO)

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
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTLC ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTFORMC (instruction)
**Summary**
- `PRINTFORMC` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTFORMC [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).
- Output is padded/truncated to a fixed-width cell (`PrintCLength`) using Shift-JIS byte count.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMC ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTFORMLC (instruction)
**Summary**
- `PRINTFORMLC` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTFORMLC [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).
- Output is padded/truncated to a fixed-width cell (`PrintCLength`) using Shift-JIS byte count.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMLC ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTCK (instruction)
**Summary**
- `PRINTCK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTCK [<raw text>]`
- `PRINTCK;<raw text>`

**Arguments**
- `<raw text>` (optional, default `""`): raw text, not an expression.
- Output is padded/truncated to a fixed-width cell (`PrintCLength`) using Shift-JIS byte count.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns.
- Applies kana conversion (`FORCEKANA` state) before writing the cell.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTCK ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTLCK (instruction)
**Summary**
- `PRINTLCK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTLCK [<raw text>]`
- `PRINTLCK;<raw text>`

**Arguments**
- `<raw text>` (optional, default `""`): raw text, not an expression.
- Output is padded/truncated to a fixed-width cell (`PrintCLength`) using Shift-JIS byte count.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns.
- Applies kana conversion (`FORCEKANA` state) before writing the cell.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTLCK ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTFORMCK (instruction)
**Summary**
- `PRINTFORMCK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTFORMCK [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).
- Output is padded/truncated to a fixed-width cell (`PrintCLength`) using Shift-JIS byte count.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns.
- Applies kana conversion (`FORCEKANA` state) before writing the cell.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMCK ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTFORMLCK (instruction)
**Summary**
- `PRINTFORMLCK` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTFORMLCK [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).
- Output is padded/truncated to a fixed-width cell (`PrintCLength`) using Shift-JIS byte count.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns.
- Applies kana conversion (`FORCEKANA` state) before writing the cell.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMLCK ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTCD (instruction)
**Summary**
- `PRINTCD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTCD [<raw text>]`
- `PRINTCD;<raw text>`

**Arguments**
- `<raw text>` (optional, default `""`): raw text, not an expression.
- Output is padded/truncated to a fixed-width cell (`PrintCLength`) using Shift-JIS byte count.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTCD ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTLCD (instruction)
**Summary**
- `PRINTLCD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTLCD [<raw text>]`
- `PRINTLCD;<raw text>`

**Arguments**
- `<raw text>` (optional, default `""`): raw text, not an expression.
- Output is padded/truncated to a fixed-width cell (`PrintCLength`) using Shift-JIS byte count.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTLCD ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTFORMCD (instruction)
**Summary**
- `PRINTFORMCD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTFORMCD [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).
- Output is padded/truncated to a fixed-width cell (`PrintCLength`) using Shift-JIS byte count.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMCD ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTFORMLCD (instruction)
**Summary**
- `PRINTFORMLCD` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`

**Syntax**
- `PRINTFORMLCD [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).
- Output is padded/truncated to a fixed-width cell (`PrintCLength`) using Shift-JIS byte count.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Writes a fixed-width cell; does not append a newline and does not flush immediately.
- Alignment: `...C` right-aligns; `...LC` left-aligns.
- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMLCD ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTDATA (instruction)
**Summary**
- Begins a **PRINTDATA block** that contains `DATA` / `DATAFORM` (and optional `DATALIST` groups).
- At runtime, the engine picks one choice uniformly at random, prints it, then jumps to `ENDDATA`.

**Metadata**
- Arg spec: `VAR_INT` (see #argument-spec-var_int) (inferred from `PRINT_DATA_Instruction` ArgBuilder assignment)
- Implementor (registration): `new PRINT_DATA_Instruction("<keyword>")`
- Structural match end: `ENDDATA`

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
- Optional/default behavior is builder-specific; see engine refs.

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
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED | IS_PRINT | IS_PRINTDATA | PARTIAL`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `state.JumpTo(func.JumpTo)`
  - `int choice = (int)exm.VEvaluator.GetNextRand(count)`
  - `state.CurrentLine = selectedLine`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.Print(str)`
  - `exm.Console.NewLine()`
  - `exm.Console.ReadAnyKey()`
  - `exm.Console.UseSetColorStyle = true`

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

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VAR_INT`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:224 (`PRINT_DATA_Instruction`)

## PRINTDATAL (instruction)
**Summary**
- `PRINTDATAL` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Metadata**
- Arg spec: `VAR_INT` (see #argument-spec-var_int) (inferred from `PRINT_DATA_Instruction` ArgBuilder assignment)
- Implementor (registration): `new PRINT_DATA_Instruction("<keyword>")`
- Structural match end: `ENDDATA`

**Syntax**
- `PRINTDATAL [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Same as `PRINTDATA`, with these differences:
  - (No kana conversion flag.)
  - (Honors `SETCOLOR` color.)
  - Appends a newline after printing (`...L`).
  - (No automatic wait suffix.)
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED | IS_PRINT | IS_PRINTDATA | PARTIAL`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `state.JumpTo(func.JumpTo)`
  - `int choice = (int)exm.VEvaluator.GetNextRand(count)`
  - `state.CurrentLine = selectedLine`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.Print(str)`
  - `exm.Console.NewLine()`
  - `exm.Console.ReadAnyKey()`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Same as `PRINTDATA`.

**Examples**
- `PRINTDATAL CHOICE` ... `ENDDATA`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VAR_INT`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:224 (`PRINT_DATA_Instruction`)

## PRINTDATAW (instruction)
**Summary**
- `PRINTDATAW` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Metadata**
- Arg spec: `VAR_INT` (see #argument-spec-var_int) (inferred from `PRINT_DATA_Instruction` ArgBuilder assignment)
- Implementor (registration): `new PRINT_DATA_Instruction("<keyword>")`
- Structural match end: `ENDDATA`

**Syntax**
- `PRINTDATAW [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Same as `PRINTDATA`, with these differences:
  - (No kana conversion flag.)
  - (Honors `SETCOLOR` color.)
  - (No automatic newline suffix.)
  - Appends a newline and waits for a key (`...W`).
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED | IS_PRINT | IS_PRINTDATA | PARTIAL`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `state.JumpTo(func.JumpTo)`
  - `int choice = (int)exm.VEvaluator.GetNextRand(count)`
  - `state.CurrentLine = selectedLine`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.Print(str)`
  - `exm.Console.NewLine()`
  - `exm.Console.ReadAnyKey()`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Same as `PRINTDATA`.

**Examples**
- `PRINTDATAW CHOICE` ... `ENDDATA`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VAR_INT`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:224 (`PRINT_DATA_Instruction`)

## PRINTDATAK (instruction)
**Summary**
- `PRINTDATAK` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Metadata**
- Arg spec: `VAR_INT` (see #argument-spec-var_int) (inferred from `PRINT_DATA_Instruction` ArgBuilder assignment)
- Implementor (registration): `new PRINT_DATA_Instruction("<keyword>")`
- Structural match end: `ENDDATA`

**Syntax**
- `PRINTDATAK [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Same as `PRINTDATA`, with these differences:
  - Applies kana conversion (`...K`) before printing.
  - (Honors `SETCOLOR` color.)
  - (No automatic newline suffix.)
  - (No automatic wait suffix.)
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED | IS_PRINT | IS_PRINTDATA | PARTIAL`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `state.JumpTo(func.JumpTo)`
  - `int choice = (int)exm.VEvaluator.GetNextRand(count)`
  - `state.CurrentLine = selectedLine`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.Print(str)`
  - `exm.Console.NewLine()`
  - `exm.Console.ReadAnyKey()`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Same as `PRINTDATA`.

**Examples**
- `PRINTDATAK CHOICE` ... `ENDDATA`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VAR_INT`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:224 (`PRINT_DATA_Instruction`)

## PRINTDATAKL (instruction)
**Summary**
- `PRINTDATAKL` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Metadata**
- Arg spec: `VAR_INT` (see #argument-spec-var_int) (inferred from `PRINT_DATA_Instruction` ArgBuilder assignment)
- Implementor (registration): `new PRINT_DATA_Instruction("<keyword>")`
- Structural match end: `ENDDATA`

**Syntax**
- `PRINTDATAKL [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Same as `PRINTDATA`, with these differences:
  - Applies kana conversion (`...K`) before printing.
  - (Honors `SETCOLOR` color.)
  - Appends a newline after printing (`...L`).
  - (No automatic wait suffix.)
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED | IS_PRINT | IS_PRINTDATA | PARTIAL`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `state.JumpTo(func.JumpTo)`
  - `int choice = (int)exm.VEvaluator.GetNextRand(count)`
  - `state.CurrentLine = selectedLine`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.Print(str)`
  - `exm.Console.NewLine()`
  - `exm.Console.ReadAnyKey()`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Same as `PRINTDATA`.

**Examples**
- `PRINTDATAKL CHOICE` ... `ENDDATA`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VAR_INT`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:224 (`PRINT_DATA_Instruction`)

## PRINTDATAKW (instruction)
**Summary**
- `PRINTDATAKW` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Metadata**
- Arg spec: `VAR_INT` (see #argument-spec-var_int) (inferred from `PRINT_DATA_Instruction` ArgBuilder assignment)
- Implementor (registration): `new PRINT_DATA_Instruction("<keyword>")`
- Structural match end: `ENDDATA`

**Syntax**
- `PRINTDATAKW [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Same as `PRINTDATA`, with these differences:
  - Applies kana conversion (`...K`) before printing.
  - (Honors `SETCOLOR` color.)
  - (No automatic newline suffix.)
  - Appends a newline and waits for a key (`...W`).
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED | IS_PRINT | IS_PRINTDATA | PARTIAL`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `state.JumpTo(func.JumpTo)`
  - `int choice = (int)exm.VEvaluator.GetNextRand(count)`
  - `state.CurrentLine = selectedLine`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.Print(str)`
  - `exm.Console.NewLine()`
  - `exm.Console.ReadAnyKey()`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Same as `PRINTDATA`.

**Examples**
- `PRINTDATAKW CHOICE` ... `ENDDATA`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VAR_INT`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:224 (`PRINT_DATA_Instruction`)

## PRINTDATAD (instruction)
**Summary**
- `PRINTDATAD` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Metadata**
- Arg spec: `VAR_INT` (see #argument-spec-var_int) (inferred from `PRINT_DATA_Instruction` ArgBuilder assignment)
- Implementor (registration): `new PRINT_DATA_Instruction("<keyword>")`
- Structural match end: `ENDDATA`

**Syntax**
- `PRINTDATAD [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Same as `PRINTDATA`, with these differences:
  - (No kana conversion flag.)
  - Ignores `SETCOLOR`’s color (`...D`) for this output.
  - (No automatic newline suffix.)
  - (No automatic wait suffix.)
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED | IS_PRINT | IS_PRINTDATA | PARTIAL`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `state.JumpTo(func.JumpTo)`
  - `int choice = (int)exm.VEvaluator.GetNextRand(count)`
  - `state.CurrentLine = selectedLine`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.Print(str)`
  - `exm.Console.NewLine()`
  - `exm.Console.ReadAnyKey()`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Same as `PRINTDATA`.

**Examples**
- `PRINTDATAD CHOICE` ... `ENDDATA`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VAR_INT`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:224 (`PRINT_DATA_Instruction`)

## PRINTDATADL (instruction)
**Summary**
- `PRINTDATADL` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Metadata**
- Arg spec: `VAR_INT` (see #argument-spec-var_int) (inferred from `PRINT_DATA_Instruction` ArgBuilder assignment)
- Implementor (registration): `new PRINT_DATA_Instruction("<keyword>")`
- Structural match end: `ENDDATA`

**Syntax**
- `PRINTDATADL [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Same as `PRINTDATA`, with these differences:
  - (No kana conversion flag.)
  - Ignores `SETCOLOR`’s color (`...D`) for this output.
  - Appends a newline after printing (`...L`).
  - (No automatic wait suffix.)
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED | IS_PRINT | IS_PRINTDATA | PARTIAL`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `state.JumpTo(func.JumpTo)`
  - `int choice = (int)exm.VEvaluator.GetNextRand(count)`
  - `state.CurrentLine = selectedLine`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.Print(str)`
  - `exm.Console.NewLine()`
  - `exm.Console.ReadAnyKey()`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Same as `PRINTDATA`.

**Examples**
- `PRINTDATADL CHOICE` ... `ENDDATA`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VAR_INT`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:224 (`PRINT_DATA_Instruction`)

## PRINTDATADW (instruction)
**Summary**
- `PRINTDATADW` is a `PRINTDATA`-family block instruction.
- See `PRINTDATA` for the full block model and structure rules.

**Metadata**
- Arg spec: `VAR_INT` (see #argument-spec-var_int) (inferred from `PRINT_DATA_Instruction` ArgBuilder assignment)
- Implementor (registration): `new PRINT_DATA_Instruction("<keyword>")`
- Structural match end: `ENDDATA`

**Syntax**
- `PRINTDATADW [<intVarTerm>]` ... `ENDDATA`

**Arguments**
- Same as `PRINTDATA`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Same as `PRINTDATA`, with these differences:
  - (No kana conversion flag.)
  - Ignores `SETCOLOR`’s color (`...D`) for this output.
  - (No automatic newline suffix.)
  - Appends a newline and waits for a key (`...W`).
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED | IS_PRINT | IS_PRINTDATA | PARTIAL`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `state.JumpTo(func.JumpTo)`
  - `int choice = (int)exm.VEvaluator.GetNextRand(count)`
  - `state.CurrentLine = selectedLine`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.Print(str)`
  - `exm.Console.NewLine()`
  - `exm.Console.ReadAnyKey()`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Same as `PRINTDATA`.

**Examples**
- `PRINTDATADW CHOICE` ... `ENDDATA`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VAR_INT`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:224 (`PRINT_DATA_Instruction`)

## PRINTBUTTON (instruction)
**Summary**
- Prints a clickable button with a script-provided input value.
- Unlike automatic button conversion (e.g. `[0] ...` inside normal `PRINT` output), this instruction forces the output segment to be a button.

**Metadata**
- Arg spec: `SP_BUTTON` (see #argument-spec-sp_button)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- `PRINTBUTTON <text>, <buttonValue>`

**Arguments**
- `<text>` (string): button label.
- `<buttonValue>`: expression whose runtime type is either:
  - integer (button produces that integer as input), or
  - string (button produces that string as input; useful with `INPUTS`).

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output).
- Uses the current text style for output (and honors `SETCOLOR` color).
- Evaluates `<text>` to a string, then removes any newline characters (`'\n'`) from it.
- If the resulting label is empty, this instruction produces no output segment (no button is created).
- Appends one button segment to the print buffer:
  - If `<buttonValue>` is an integer, the button produces that integer when clicked.
  - If `<buttonValue>` is a string, the button produces that string when clicked.
- This instruction does **not** add a newline and does not flush by itself (it behaves like other non-`...L` print-family commands).
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = true`
  - `exm.Console.PrintButton(str, bArg.ButtonWord.GetIntValue(exm))`
  - `exm.Console.PrintButton(str, bArg.ButtonWord.GetStrValue(exm))`

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

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_BUTTON`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:111 (case `PRINTBUTTON`)

## PRINTBUTTONC (instruction)
**Summary**
- Like `PRINTBUTTON`, but formats the label as a fixed-width `PRINTC`-style cell aligned to the right.

**Metadata**
- Arg spec: `SP_BUTTON` (see #argument-spec-sp_button)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- `PRINTBUTTONC <text>, <buttonValue>`

**Arguments**
- Same as `PRINTBUTTON`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Same as `PRINTBUTTON`, with these differences:
  - The label still has all `'\n'` characters removed (same as `PRINTBUTTON`).
  - Before creating the button segment, the label is formatted as a `PRINTC`-style fixed-width cell, aligned to the right (same cell formatting rules as `PRINTC`).
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = true`
  - `exm.Console.PrintButtonC(str, bArg.ButtonWord.GetIntValue(exm), isRight)`
  - `exm.Console.PrintButtonC(str, bArg.ButtonWord.GetStrValue(exm), isRight)`

**Errors & validation**
- Same as `PRINTBUTTON`.

**Examples**
```erabasic
PRINTBUTTONC "[0] OK", 0
PRINTBUTTONC "[1] Cancel", 1
INPUT
```

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_BUTTON`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:127 (case `PRINTBUTTONC`)

## PRINTBUTTONLC (instruction)
**Summary**
- Like `PRINTBUTTON`, but formats the label as a fixed-width `PRINTC`-style cell aligned to the left.

**Metadata**
- Arg spec: `SP_BUTTON` (see #argument-spec-sp_button)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- `PRINTBUTTONLC <text>, <buttonValue>`

**Arguments**
- Same as `PRINTBUTTON`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Same as `PRINTBUTTONC`, except the label cell is aligned to the left:
  - Uses the same fixed-width cell formatting rules as `PRINTLC`.
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = true`
  - `exm.Console.PrintButtonC(str, bArg.ButtonWord.GetIntValue(exm), isRight)`
  - `exm.Console.PrintButtonC(str, bArg.ButtonWord.GetStrValue(exm), isRight)`

**Errors & validation**
- Same as `PRINTBUTTON`.

**Examples**
```erabasic
PRINTBUTTONLC "[0] OK", 0
PRINTBUTTONLC "[1] Cancel", 1
INPUT
```

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_BUTTON`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:128 (case `PRINTBUTTONLC`)

## PRINTPLAIN (instruction)
**Summary**
- Outputs a raw string argument as plain text, without automatic button conversion.

**Metadata**
- Arg spec: `STR_NULLABLE` (see #argument-spec-str_nullable)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- `PRINTPLAIN`
- `PRINTPLAIN <raw text>`

**Arguments**
- `<raw text>`: the literal remainder of the line (not a string expression).

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output).
- Appends the raw string to the print buffer as a “plain” segment:
  - It is **not** scanned for numeric button patterns like `[0]`.
  - It still uses the current style (`SETCOLOR`, font style, etc.).
- Does not add a newline and does not flush by itself.
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = true`
  - `exm.Console.PrintPlain(term.GetStrValue(exm))`

**Errors & validation**
- None.

**Examples**
```erabasic
; This will NOT become a clickable button:
PRINTPLAIN [0] Save
PRINTL
```

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.STR_NULLABLE`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:145 (case `PRINTPLAIN`)

## PRINTPLAINFORM (instruction)
**Summary**
- Like `PRINTPLAIN`, but reads its argument as a FORM/formatted string.

**Metadata**
- Arg spec: `FORM_STR_NULLABLE` (see #argument-spec-form_str_nullable)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- `PRINTPLAINFORM`
- `PRINTPLAINFORM <FORM string>`

**Arguments**
- `<FORM string>`: a FORM argument scanned by the FORM analyzer (supports `%...%` and `{...}` placeholders).

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output).
- Evaluates the FORM argument to a string, then appends it as a “plain” segment (no automatic button conversion).
- Does not add a newline and does not flush by itself.
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = true`
  - `exm.Console.PrintPlain(term.GetStrValue(exm))`

**Errors & validation**
- FORM parsing errors follow the engine’s normal FORM rules.

**Examples**
```erabasic
PRINTPLAINFORM HP: {HP}/{MAXHP}  [0] Not a button
PRINTL
```

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.FORM_STR_NULLABLE`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:146 (case `PRINTPLAINFORM`)

## PRINT_ABL (instruction)
**Summary**
- Prints a one-line summary of a character’s non-zero abilities (`ABL`), then ends the line.

**Metadata**
- Arg spec: `INT_EXPRESSION` (see #argument-spec-int_expression)
- Flags (registration): `METHOD_SAFE`

**Syntax**
- `PRINT_ABL`
- `PRINT_ABL <charaIndex>`

**Arguments**
- `charaIndex` (optional, int; default `0` with a warning if omitted): index into the current character list.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

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
- Engine-extracted notes (key operations):
  - `exm.Console.Print(vEvaluator.GetCharacterDataString(target, func.FunctionCode))`
  - `exm.Console.NewLine()`

**Errors & validation**
- Runtime error if `charaIndex` is out of range (`charaIndex < 0` or `charaIndex >= CHARANUM`).

**Examples**
```erabasic
PRINT_ABL TARGET
```

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:176 (case `PRINT_ABL`)

## PRINT_TALENT (instruction)
**Summary**
- Prints a one-line summary of a character’s enabled talents (`TALENT`), then ends the line.

**Metadata**
- Arg spec: `INT_EXPRESSION` (see #argument-spec-int_expression)
- Flags (registration): `METHOD_SAFE`

**Syntax**
- `PRINT_TALENT`
- `PRINT_TALENT <charaIndex>`

**Arguments**
- `charaIndex` (optional, int; default `0` with a warning if omitted): index into the current character list.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

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
- Engine-extracted notes (key operations):
  - `exm.Console.Print(vEvaluator.GetCharacterDataString(target, func.FunctionCode))`
  - `exm.Console.NewLine()`

**Errors & validation**
- Runtime error if `charaIndex` is out of range.

**Examples**
```erabasic
PRINT_TALENT TARGET
```

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:177 (case `PRINT_TALENT`)

## PRINT_MARK (instruction)
**Summary**
- Prints a one-line summary of a character’s non-zero marks (`MARK`), then ends the line.

**Metadata**
- Arg spec: `INT_EXPRESSION` (see #argument-spec-int_expression)
- Flags (registration): `METHOD_SAFE`

**Syntax**
- `PRINT_MARK`
- `PRINT_MARK <charaIndex>`

**Arguments**
- `charaIndex` (optional, int; default `0` with a warning if omitted): index into the current character list.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

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
- Engine-extracted notes (key operations):
  - `exm.Console.Print(vEvaluator.GetCharacterDataString(target, func.FunctionCode))`
  - `exm.Console.NewLine()`

**Errors & validation**
- Runtime error if `charaIndex` is out of range.

**Examples**
```erabasic
PRINT_MARK TARGET
```

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:178 (case `PRINT_MARK`)

## PRINT_EXP (instruction)
**Summary**
- Prints a one-line summary of a character’s non-zero experiences (`EXP`), then ends the line.

**Metadata**
- Arg spec: `INT_EXPRESSION` (see #argument-spec-int_expression)
- Flags (registration): `METHOD_SAFE`

**Syntax**
- `PRINT_EXP`
- `PRINT_EXP <charaIndex>`

**Arguments**
- `charaIndex` (optional, int; default `0` with a warning if omitted): index into the current character list.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

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
- Engine-extracted notes (key operations):
  - `exm.Console.Print(vEvaluator.GetCharacterDataString(target, func.FunctionCode))`
  - `exm.Console.NewLine()`

**Errors & validation**
- Runtime error if `charaIndex` is out of range.

**Examples**
```erabasic
PRINT_EXP TARGET
```

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:179 (case `PRINT_EXP`)

## PRINT_PALAM (instruction)
**Summary**
- Prints a multi-column view of a character’s parameters (`PALAM`) using `PRINTC`-style cells.

**Metadata**
- Arg spec: `INT_EXPRESSION` (see #argument-spec-int_expression)
- Flags (registration): `METHOD_SAFE`

**Syntax**
- `PRINT_PALAM`
- `PRINT_PALAM <charaIndex>`

**Arguments**
- `charaIndex` (optional, int; default `0` with a warning if omitted): index into the current character list.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

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
- Engine-extracted notes (key operations):
  - `string printStr = vEvaluator.GetCharacterParamString(target, i)`
  - `exm.Console.PrintC(printStr, true)`
  - `exm.Console.PrintFlush(false)`
  - `exm.Console.RefreshStrings(false)`

**Errors & validation**
- Runtime error if `charaIndex` is out of range.

**Examples**
```erabasic
PRINT_PALAM TARGET
```

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:189 (case `PRINT_PALAM`)

## PRINT_ITEM (instruction)
**Summary**
- Prints a one-line summary of currently owned items (`ITEM`), then ends the line.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void)
- Flags (registration): `METHOD_SAFE`

**Syntax**
- `PRINT_ITEM`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

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
- Engine-extracted notes (key operations):
  - `exm.Console.Print(vEvaluator.GetHavingItemsString())`
  - `exm.Console.NewLine()`

**Errors & validation**
- None specific to this instruction.

**Examples**
- `PRINT_ITEM`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:212 (case `PRINT_ITEM`)

## PRINT_SHOPITEM (instruction)
**Summary**
- Prints a grid of items currently for sale in the shop (based on `ITEMSALES`), including their indices and prices.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void)
- Flags (registration): `METHOD_SAFE`

**Syntax**
- `PRINT_SHOPITEM`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

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
- Engine-extracted notes (key operations):
  - `int length = Math.Min(vEvaluator.ITEMSALES.Length, vEvaluator.ITEMNAME.Length)`
  - `if (length > vEvaluator.ITEMPRICE.Length)`
  - `length = vEvaluator.ITEMPRICE.Length`
  - `if (vEvaluator.ItemSales(i))`
  - `string printStr = vEvaluator.ITEMNAME[i]`
  - `long price = vEvaluator.ITEMPRICE[i]`
  - `exm.Console.PrintC(string.Format("[{2}] {0}({3}{1})", printStr, price, i, Config.MoneyLabel), false)`
  - `exm.Console.PrintC(string.Format("[{2}] {0}({1}{3})", printStr, price, i, Config.MoneyLabel), false)`
  - `exm.Console.PrintFlush(false)`
  - `exm.Console.RefreshStrings(false)`

**Errors & validation**
- None specific to this instruction.

**Examples**
- `PRINT_SHOPITEM`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:218 (case `PRINT_SHOPITEM`)

## DRAWLINE (instruction)
**Summary**
- Draws a horizontal line across the console using the configured `DRAWLINE` pattern.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void)
- Flags (registration): `METHOD_SAFE`

**Syntax**
- `DRAWLINE`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

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
- Engine-extracted notes (key operations):
  - `exm.Console.PrintBar()`
  - `exm.Console.NewLine()`

**Errors & validation**
- None (arguments are not accepted).

**Examples**
```erabasic
DRAWLINE
PRINTL Header
DRAWLINE
```

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:156 (case `DRAWLINE`)

## BAR (instruction)
**Summary**
- Prints a bracketed bar-graph string representing the ratio `value / maxValue`.

**Metadata**
- Arg spec: `SP_BAR` (see #argument-spec-sp_bar) (inferred from `BAR_Instruction` ArgBuilder assignment)
- Implementor (registration): `new BAR_Instruction(false)`

**Syntax**
- `BAR value, maxValue, length`

**Arguments**
- `value`: int expression (numerator).
- `maxValue`: int expression (denominator); must evaluate to `> 0`.
- `length`: int expression (bar width); must satisfy `1 <= length <= 99`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Computes `filled = clamp(value * length / maxValue, 0, length)` using 64-bit integer arithmetic (integer overflow wraps).
- Produces and prints:
  - `[` + (`BarChar1` repeated `filled`) + (`BarChar2` repeated `length - filled`) + `]`
- `BarChar1` / `BarChar2` are configurable:
  - `BarChar1` default `*`
  - `BarChar2` default `.`
- Does **not** append a newline; use `BARL` if you want a newline.
- If output skipping is active (via `SKIPDISP`), this instruction is skipped.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT | METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.Console.Print(ExpressionMediator.CreateBar(var, max, length))`
  - `exm.Console.NewLine()`

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

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_BAR`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1340 (`BAR_Instruction`)

## BARL (instruction)
**Summary**
- Like `BAR`, but appends a newline after printing the bar.

**Metadata**
- Arg spec: `SP_BAR` (see #argument-spec-sp_bar) (inferred from `BAR_Instruction` ArgBuilder assignment)
- Implementor (registration): `new BAR_Instruction(true)`

**Syntax**
- `BARL value, maxValue, length`

**Arguments**
- Same as `BAR`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Prints the same bar string as `BAR value, maxValue, length`.
- Appends a newline after printing.
- If output skipping is active (via `SKIPDISP`), this instruction is skipped.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT | METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.Console.Print(ExpressionMediator.CreateBar(var, max, length))`
  - `exm.Console.NewLine()`

**Errors & validation**
- Same as `BAR`.

**Examples**
```erabasic
BARL 114, 514, 81
```

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_BAR`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1340 (`BAR_Instruction`)

## TIMES (instruction)
**Summary**
- Multiplies a changeable integer variable by a real-number literal and stores the truncated result back.

**Metadata**
- Arg spec: `SP_TIMES` (see #argument-spec-sp_times) (inferred from `TIMES_Instruction` ArgBuilder assignment)
- Implementor (registration): `new TIMES_Instruction()`

**Syntax**
- `TIMES intVarTerm, realLiteral`

**Arguments**
- `intVarTerm`: a changeable integer variable term (must not be `CONST`).
- `realLiteral`: a real-number **literal** parsed as `double` (not an expression).

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Reads `intVarTerm`’s current value, multiplies it by `realLiteral`, then stores `(long)product` back into `intVarTerm`.
  - The cast truncates toward zero (`125.9` → `125`, `-1.9` → `-1`).
- Calculation mode depends on config `TimesNotRigorousCalculation`:
  - If enabled: uses `double` math.
  - Otherwise: uses `decimal` math (with a fallback conversion path for overflow) to reduce rounding differences.
- The assignment is performed in an `unchecked` context (overflow does not raise an error).
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE`

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

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_TIMES`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1362 (`TIMES_Instruction`)

## WAIT (instruction)
**Summary**
- Waits for the user to press Enter (or click, depending on the UI), then continues.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `WAIT_Instruction` ArgBuilder assignment)
- Implementor (registration): `new WAIT_Instruction(false)`

**Syntax**
- `WAIT`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Enters a UI wait state for an Enter-style key/click.
- Does not assign `RESULT`/`RESULTS`.
- Skipped when output skipping is active (via `SKIPDISP`).
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.ReadAnyKey(false, true)`
  - `exm.Console.ReadAnyKey()`

**Errors & validation**
- None.

**Examples**
- `WAIT`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:749 (`WAIT_Instruction`)

## INPUT (instruction)
**Summary**
- Requests an integer input from the user and stores it into `RESULT` (with mouse-related side channels in some cases).

**Metadata**
- Arg spec: `SP_INPUT` (see #argument-spec-sp_input) (inferred from `INPUT_Instruction` ArgBuilder assignment)
- Implementor (registration): `new INPUT_Instruction()`

**Syntax**
- `INPUT [<default> [, <mouse> [, <canSkip> [, <extra>]]]]`

**Arguments**
- `<default>` (optional, int): used only when the submitted text is empty (not used for invalid integer text).
- `<mouse>` (optional, int; default `0`): if non-zero, enables mouse-based input (e.g. selecting buttons can fill the input).
  - `0`: accepted value is written to `RESULT`.
  - Note: mouse mode does not change where the accepted integer is stored on the normal wait path (it is still stored into `RESULT`).
- `<canSkip>` (optional, int): presence enables the `MesSkip` fast path; its numeric value is ignored (not evaluated).
- `<extra>` (optional, int): accepted by the argument parser but ignored by the runtime (not read/evaluated).

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

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
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT | IS_INPUT`
- Engine-extracted notes (key operations):
  - `exm.Console.Window.ApplyTextBoxChanges()`
  - `exm.Console.WaitInput(req)`

**Errors & validation**
- Argument-type errors are raised if a provided argument is not an `int` expression (including `<canSkip>` and `<extra>`).
- Integer parsing is equivalent to `.NET` `Int64.TryParse` on the submitted text.
  - If parsing fails, the engine stays in the wait state.

**Examples**
- `INPUT`
- `INPUT 0`
- `INPUT 10, 1, 1` (default=10, mouse input enabled, skip can auto-accept default)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_INPUT`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:805 (`INPUT_Instruction`)

## INPUTS (instruction)
**Summary**
- Requests a string input from the user and stores it into `RESULTS` (with mouse-related side channels in some cases).

**Metadata**
- Arg spec: `SP_INPUTS` (see #argument-spec-sp_inputs) (inferred from `INPUTS_Instruction` ArgBuilder assignment)
- Implementor (registration): `new INPUTS_Instruction()`

**Syntax**
- `INPUTS`
- `INPUTS <defaultFormString>`
- `INPUTS <defaultFormString>, <mouse> [, <canSkip>]`

**Arguments**
- `<defaultFormString>` (optional): FORM/formatted string expression used as the default string. If omitted, there is no default.
- `<mouse>` (optional, int; default `0`): if non-zero, enables mouse-based input.
- `<canSkip>` (optional, any): presence enables the `MesSkip` fast path; its value is ignored (not evaluated).

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

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
- Output skipping interaction is the same as `INPUT`.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT | IS_INPUT`
- Engine-extracted notes (key operations):
  - `exm.Console.Window.ApplyTextBoxChanges()`
  - `exm.Console.WaitInput(req)`

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

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_INPUTS`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:861 (`INPUTS_Instruction`)

## TINPUT (instruction)
**Summary**
- Timed integer input: like `INPUT`, but with a time limit and timeout message.

**Metadata**
- Arg spec: `SP_TINPUT` (see #argument-spec-sp_tinput) (inferred from `TINPUT_Instruction` ArgBuilder assignment)
- Implementor (registration): `new TINPUT_Instruction(false)`

**Syntax**
- `TINPUT <timeMs>, <default> [, <displayTime> [, <timeoutMessage> [, <mouse> [, <canSkip>]]]]`

**Arguments**
- `<timeMs>` (int): time limit in milliseconds.
- `<default>` (int): default value used on timeout (and also on empty input when the request is not running a timer).
- `<displayTime>` (optional, int; default `1`): if non-zero, displays remaining time (UI behavior).
- `<timeoutMessage>` (optional, string; default `TimeupLabel`): message used on timeout.
- `<mouse>` (optional, int; default `0`): enables mouse input when equal to `1`.
- `<canSkip>` (optional, int): if present, allows `MesSkip` to auto-accept the default without waiting (the value is not evaluated).

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

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
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT | IS_INPUT | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.Console.WaitInput(req)`

**Errors & validation**
- Argument parsing/type-checking errors are engine errors.

**Examples**
- `TINPUT 5000, 0`
- `TINPUT 10000, 1, 1, Time up!, 1, 1`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_TINPUT`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1045 (`TINPUT_Instruction`)

## TINPUTS (instruction)
**Summary**
- Timed string input: like `INPUTS`, but with a time limit and timeout message.

**Metadata**
- Arg spec: `SP_TINPUTS` (see #argument-spec-sp_tinputs) (inferred from `TINPUTS_Instruction` ArgBuilder assignment)
- Implementor (registration): `new TINPUTS_Instruction(false)`

**Syntax**
- `TINPUTS <timeMs>, <default> [, <displayTime> [, <timeoutMessage> [, <mouse> [, <canSkip>]]]]`

**Arguments**
- `<timeMs>` (int): time limit in milliseconds.
- `<default>` (string): default value used on timeout (and also on empty input when the request is not running a timer).
- `<displayTime>` (optional, int; default `1`): if non-zero, displays remaining time.
- `<timeoutMessage>` (optional, string; default `TimeupLabel`): timeout message.
- `<mouse>` (optional, int; default `0`): enables mouse input when equal to `1`.
- `<canSkip>` (optional, int): if present, allows `MesSkip` to auto-accept the default without waiting (the value is not evaluated).

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Same model as `TINPUT`, but stores into `RESULTS` (string) rather than `RESULT` (int).
- `MesSkip` integration:
  - If `<canSkip>` is present and `MesSkip` is currently true, the engine does not wait and instead accepts the default immediately.
  - In that no-wait path, the engine assigns the default to:
    - `RESULTS` if `<mouse> == 0`
    - `RESULTS_ARRAY[1]` if `<mouse> != 0`
  - In that no-wait path, the input string is not echoed (because the UI wait is skipped entirely).
- Mouse-enabled input side channels: see `INPUT` (the same UI-side `RESULT_ARRAY[...]` / `RESULTS_ARRAY[...]` behaviors apply).
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT | IS_INPUT | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.Console.WaitInput(req)`

**Errors & validation**
- Argument parsing/type-checking errors are engine errors.

**Examples**
- `TINPUTS 5000, "DEFAULT"`
- `TINPUTS 3000, NAME, 1, Time up!`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_TINPUTS`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1102 (`TINPUTS_Instruction`)

## TONEINPUT (instruction)
**Summary**
- Like `TINPUT`, but uses the “one input” mode (`OneInput = true`).

**Metadata**
- Arg spec: `SP_TINPUT` (see #argument-spec-sp_tinput) (inferred from `TINPUT_Instruction` ArgBuilder assignment)
- Implementor (registration): `new TINPUT_Instruction(true)`

**Syntax**
- Same as `TINPUT`.

**Arguments**
- Same as `TINPUT`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Same as `TINPUT`, but with “one input” mode enabled:
  - If the entered text has length > 1, it is truncated to the first character.
  - Exception: if `AllowLongInputByMouse` is enabled and the input was produced by mouse selection, truncation does not occur.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT | IS_INPUT | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.Console.WaitInput(req)`

**Errors & validation**
- Same as `TINPUT`.

**Examples**
- `TONEINPUT 5000, 0`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_TINPUT`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1045 (`TINPUT_Instruction`)

## TONEINPUTS (instruction)
**Summary**
- Like `TINPUTS`, but uses the “one input” mode (`OneInput = true`).

**Metadata**
- Arg spec: `SP_TINPUTS` (see #argument-spec-sp_tinputs) (inferred from `TINPUTS_Instruction` ArgBuilder assignment)
- Implementor (registration): `new TINPUTS_Instruction(true)`

**Syntax**
- Same as `TINPUTS`.

**Arguments**
- Same as `TINPUTS`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Same as `TINPUTS`, but with “one input” mode enabled:
  - If the entered text has length > 1, it is truncated to the first character.
  - Exception: if `AllowLongInputByMouse` is enabled and the input was produced by mouse selection, truncation does not occur.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT | IS_INPUT | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.Console.WaitInput(req)`

**Errors & validation**
- Same as `TINPUTS`.

**Examples**
- `TONEINPUTS 5000, "A"`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_TINPUTS`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1102 (`TINPUTS_Instruction`)

## TWAIT (instruction)
**Summary**
- Timed wait: waits for a limited time (and optionally disallows user input), then continues.

**Metadata**
- Arg spec: `SP_SWAP` (see #argument-spec-sp_swap) (inferred from `TWAIT_Instruction` ArgBuilder assignment)
- Implementor (registration): `new TWAIT_Instruction()`

**Syntax**
- `TWAIT <timeMs>, <mode>`

**Arguments**
- `<timeMs>` (int): time limit in milliseconds.
- `<mode>` (int):
  - `0`: wait for Enter/click, but time out after `<timeMs>`.
  - non-zero: disallow input and simply wait `<timeMs>` (or be affected by macro/skip behavior).

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- If `<mode> == 0`: waits for Enter/click, but times out after `<timeMs>`.
- If `<mode> != 0`: disallows input and simply waits `<timeMs>` (but can still be affected by macro/skip behavior).
- When the time limit elapses, execution continues automatically.
- Does not assign `RESULT`/`RESULTS`.
- Skipped when output skipping is active (via `SKIPDISP`).
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.Console.ReadAnyKey()`
  - `exm.Console.WaitInput(req)`

**Errors & validation**
- Argument type errors follow the normal integer-expression argument rules.

**Examples**
- `TWAIT 3000, 0` (wait up to 3 seconds for Enter)
- `TWAIT 1000, 1` (wait 1 second with no input)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_SWAP`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:780 (`TWAIT_Instruction`)

## WAITANYKEY (instruction)
**Summary**
- Like `WAIT`, but accepts **any key** input (not only Enter) to continue.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `WAITANYKEY_Instruction` ArgBuilder assignment)
- Implementor (registration): `new WAITANYKEY_Instruction()`

**Syntax**
- `WAITANYKEY`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Enters a UI wait state for any-key input.
- Does not assign `RESULT`/`RESULTS`.
- Skipped when output skipping is active (via `SKIPDISP`).
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.ReadAnyKey(true, false)`

**Errors & validation**
- None.

**Examples**
- `WAITANYKEY`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:767 (`WAITANYKEY_Instruction`)

## FORCEWAIT (instruction)
**Summary**
- Like `WAIT`, but stops “message skip” from auto-advancing past the wait.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `WAIT_Instruction` ArgBuilder assignment)
- Implementor (registration): `new WAIT_Instruction(true)`

**Syntax**
- `FORCEWAIT`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Waits for Enter/click, and stops “message skip” from auto-advancing past the wait.
- Does not assign `RESULT`/`RESULTS`.
- Skipped when output skipping is active (via `SKIPDISP`).
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.ReadAnyKey(false, true)`
  - `exm.Console.ReadAnyKey()`

**Errors & validation**
- None.

**Examples**
- `FORCEWAIT`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:749 (`WAIT_Instruction`)

## ONEINPUT (instruction)
**Summary**
- Like `INPUT`, but requests a “one input” integer entry (UI-side restriction).

**Metadata**
- Arg spec: `SP_INPUT` (see #argument-spec-sp_input) (inferred from `ONEINPUT_Instruction` ArgBuilder assignment)
- Implementor (registration): `new ONEINPUT_Instruction()`

**Syntax**
- `ONEINPUT`
- `ONEINPUT <default>`
- `ONEINPUT <default>, <mouse>, <canSkip> [, <extra>]`

**Arguments**
- Same as `INPUT`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Like `INPUT` (including `MesSkip` behavior and mouse side channels), but sets `OneInput = true` on the input request.
- Implementation-oriented notes:
  - In the UI input handler, `OneInput` truncates the entered text to at most one character in many cases, so it typically behaves like “read a single digit/character then parse”.
  - Depending on configuration, mouse-provided input may bypass this truncation.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT | IS_INPUT | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.Console.WaitInput(req)`

**Errors & validation**
- Same as `INPUT`.

**Examples**
- `ONEINPUT`
- `ONEINPUT 0`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_INPUT`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:917 (`ONEINPUT_Instruction`)

## ONEINPUTS (instruction)
**Summary**
- Like `INPUTS`, but requests a “one input” string entry (UI-side restriction).

**Metadata**
- Arg spec: `SP_INPUTS` (see #argument-spec-sp_inputs) (inferred from `ONEINPUTS_Instruction` ArgBuilder assignment)
- Implementor (registration): `new ONEINPUTS_Instruction()`

**Syntax**
- `ONEINPUTS`
- `ONEINPUTS <defaultFormString>`
- `ONEINPUTS <defaultFormString>, <mouse> [, <canSkip>]`

**Arguments**
- Same as `INPUTS`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Like `INPUTS` (including `MesSkip` behavior and mouse side channels), but with “one input” mode enabled:
  - If the entered text has length > 1, it is truncated to the first character.
  - Exception: if `AllowLongInputByMouse` is enabled and the input was produced by mouse selection, truncation does not occur.
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT | IS_INPUT | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.Console.WaitInput(req)`

**Errors & validation**
- Same as `INPUTS`.

**Examples**
- `ONEINPUTS`
- `ONEINPUTS A`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_INPUTS`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:982 (`ONEINPUTS_Instruction`)

## CLEARLINE (instruction)
**Summary**
- Deletes the last *N logical output lines* from the console display/log.

**Metadata**
- Arg spec: `INT_EXPRESSION` (see #argument-spec-int_expression) (inferred from `CLEARLINE_Instruction` ArgBuilder assignment)
- Implementor (registration): `new CLEARLINE_Instruction()`

**Syntax**
- `CLEARLINE <n>`

**Arguments**
- `<n>` (int): number of logical output lines to delete.
  - The evaluated value is converted to a 32-bit signed integer by truncation (i.e. low 32 bits interpreted as signed).

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Evaluates `<n>` and deletes the last `n` logical output lines from the console display/log.
- The deletion count is in **logical lines**, not raw display lines:
  - One logical line can occupy multiple display lines (e.g. word wrapping).
  - Deletion walks backward from the end of the display list and counts only entries marked as “logical line” boundaries; all associated display lines are removed.
- If `n <= 0`, nothing is deleted.
- After deleting, the display is refreshed.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED | IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.deleteLine(delNum)`
  - `exm.Console.RefreshStrings(false)`

**Errors & validation**
- No explicit validation in the instruction.
- No error is raised for negative or overflowed values (after the 32-bit conversion).

**Examples**
- `CLEARLINE 1`
- `CLEARLINE 10`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:675 (`CLEARLINE_Instruction`)

## REUSELASTLINE (instruction)
**Summary**
- Prints a **temporary single line** that is intended to be overwritten by the next printed line.

**Metadata**
- Arg spec: `FORM_STR_NULLABLE` (see #argument-spec-form_str_nullable) (inferred from `REUSELASTLINE_Instruction` ArgBuilder assignment)
- Implementor (registration): `new REUSELASTLINE_Instruction()`

**Syntax**
- `REUSELASTLINE`
- `REUSELASTLINE <formString>`

**Arguments**
- `<formString>` (optional): FORM/formatted string (parsed like `PRINTFORM*`) used as the temporary line’s content.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Evaluates `<formString>` to a string and prints it as a temporary line.
- A “temporary line” has a special overwrite behavior:
  - When the engine later adds a new display line, if the current last display line is temporary, it is deleted first; the new line then takes its place.
  - As a result, repeated `REUSELASTLINE` calls typically “update” a single line (useful for progress/timer displays).
- If the resulting string is empty, the current console implementation prints nothing (and therefore does not overwrite an existing line).
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED | IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.PrintTemporaryLine(str)`

**Errors & validation**
- None.

**Examples**
- `REUSELASTLINE Now loading...`
- `REUSELASTLINE %TIME%`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.FORM_STR_NULLABLE`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:660 (`REUSELASTLINE_Instruction`)

## UPCHECK (instruction)
**Summary**
- Applies the `UP`/`DOWN` delta arrays to `PALAM` for the current `TARGET` character, and prints each applied change.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void)
- Flags (registration): `METHOD_SAFE`

**Syntax**
- `UPCHECK`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

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
- Engine-extracted notes (key operations):
  - `vEvaluator.UpdateInUpcheck(exm.Console, skipPrint)`

**Errors & validation**
- None specific to this instruction.

**Examples**
```erabasic
UP:0 = 123
UP:1 = 456
UPCHECK
```

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:248 (case `UPCHECK`)

## CUPCHECK (instruction)
**Summary**
- Like `UPCHECK`, but applies `CUP`/`CDOWN` to `PALAM` for a specified character index.

**Metadata**
- Arg spec: `INT_EXPRESSION` (see #argument-spec-int_expression)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- `CUPCHECK [charaIndex]`

**Arguments**
- `charaIndex` (optional, int; default `0` with a warning if omitted): the character index to apply changes to.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

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
- Engine-extracted notes (key operations):
  - `vEvaluator.CUpdateInUpcheck(exm.Console, target, skipPrint)`

**Errors & validation**
- None specific to this instruction (out-of-range just returns).

**Examples**
```erabasic
CUP:TARGET:0 = 10
CUPCHECK TARGET
```

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:251 (case `CUPCHECK`)

## ADDCHARA (instruction)
**Summary**
- Adds one or more characters to the current character list using character templates loaded from CSV.

**Metadata**
- Arg spec: `INT_ANY` (see #argument-spec-int_any) (inferred from `ADDCHARA_Instruction` ArgBuilder assignment)
- Implementor (registration): `new ADDCHARA_Instruction(false, false)`

**Syntax**
- `ADDCHARA charaNo`
- `ADDCHARA charaNo1, charaNo2, ...`

**Arguments**
- Each `charaNo`: int expression selecting a character template.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Requires at least one argument; multiple arguments are accepted but the engine emits a parse-time warning for multi-argument uses.
- For each `charaNo` (evaluated left-to-right), the engine immediately appends one character to the current character list using the character template identified by that number.
- `CHARANUM` increases by 1 for each successfully added character.
- If a later argument fails (e.g. undefined template), earlier additions remain (no rollback).
- This instruction does not print anything and does not automatically change `TARGET`/`MASTER`/`ASSI`.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE`
- Engine-extracted notes (key operations):
  - `exm.VEvaluator.AddCharacter_UseSp(integer, isSp)`
  - `exm.VEvaluator.AddCharacter(integer)`
  - `exm.VEvaluator.DelCharacter(charaNoList[0])`
  - `exm.VEvaluator.DelCharacter(charaNoList)`

**Errors & validation**
- Runtime error if any `charaNo` does not resolve to a known character template.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.SPCharaConfigIsOff.Text)`

**Examples**
```erabasic
ADDCHARA 3, 5, 6
PRINTFORML {CHARANUM}
```

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_ANY`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1399 (`ADDCHARA_Instruction`)

## ADDSPCHARA (instruction)
**Summary**
- Adds one or more “SP characters” using the SP-character template path.

**Metadata**
- Arg spec: `INT_ANY` (see #argument-spec-int_any) (inferred from `ADDCHARA_Instruction` ArgBuilder assignment)
- Implementor (registration): `new ADDCHARA_Instruction(true, false)`

**Syntax**
- `ADDSPCHARA charaNo`
- `ADDSPCHARA charaNo1, charaNo2, ...`

**Arguments**
- Each `charaNo`: int expression selecting a character template.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Requires the `CompatiSPChara` config option to be enabled; otherwise this instruction errors before evaluating any arguments.
- Requires at least one argument; multiple arguments are accepted but the engine emits a parse-time warning for multi-argument uses.
- For each `charaNo` (evaluated left-to-right), immediately appends one character using the SP template lookup path.
- `CHARANUM` increases by 1 for each successfully added character.
- If a later argument fails (e.g. undefined template), earlier additions remain (no rollback).
- This instruction does not print anything and does not automatically change `TARGET`/`MASTER`/`ASSI`.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE`
- Engine-extracted notes (key operations):
  - `exm.VEvaluator.AddCharacter_UseSp(integer, isSp)`
  - `exm.VEvaluator.AddCharacter(integer)`
  - `exm.VEvaluator.DelCharacter(charaNoList[0])`
  - `exm.VEvaluator.DelCharacter(charaNoList)`

**Errors & validation**
- Runtime error if `CompatiSPChara` is disabled.
- Runtime error if any `charaNo` does not resolve to a known character template.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.SPCharaConfigIsOff.Text)`

**Examples**
```erabasic
ADDSPCHARA 10
```

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_ANY`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1399 (`ADDCHARA_Instruction`)

## ADDDEFCHARA (instruction)
**Summary**
- Performs the engine’s “default character initialization” step used at game start.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- `ADDDEFCHARA`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Intended for use in `@SYSTEM_TITLE`.
- When executed, the engine adds:
  - the character template for CSV number `0`, and then
  - the initial character specified by `gamebase.csv` (`GameBaseData.DefaultCharacter`) if it is `> 0`.
- This uses “CSV number” lookup (engine template lookup by CSV slot), which is distinct from `ADDCHARA 0` (template lookup by character `NO`).
- If a referenced CSV template does not exist, the engine falls back to adding a “pseudo character” (like `ADDVOIDCHARA`).
- Engine-extracted notes (key operations):
  - `vEvaluator.AddCharacterFromCsvNo(0)`
  - `vEvaluator.AddCharacterFromCsvNo(GlobalStatic.GameBaseData.DefaultCharacter)`

**Errors & validation**
- Runtime error if executed outside `@SYSTEM_TITLE` (unless executed in a debug-only context where no parent label is attached).
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.CanNotUseOutsideSystemtitle.Text)`

**Examples**
```erabasic
@SYSTEM_TITLE
ADDDEFCHARA
```

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:279 (case `ADDDEFCHARA`)

## ADDVOIDCHARA (instruction)
**Summary**
- Adds a “pseudo character” that is not loaded from CSV.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `ADDVOIDCHARA_Instruction` ArgBuilder assignment)
- Implementor (registration): `new ADDVOIDCHARA_Instruction()`

**Syntax**
- `ADDVOIDCHARA`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Appends a new character record created from the engine’s pseudo-character template.
- The new character’s variables start from the language defaults (`0` for numeric cells, `""` for string reads).
- This instruction does not print anything and does not automatically change `TARGET`/`MASTER`/`ASSI`.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.VEvaluator.AddPseudoCharacter()`

**Errors & validation**
- None specific to this instruction.

**Examples**
```erabasic
ADDVOIDCHARA
TARGET = CHARANUM - 1
```

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1445 (`ADDVOIDCHARA_Instruction`)

## DELCHARA (instruction)
**Summary**
- Deletes one or more characters from the current character list by character index.

**Metadata**
- Arg spec: `INT_ANY` (see #argument-spec-int_any) (inferred from `ADDCHARA_Instruction` ArgBuilder assignment)
- Implementor (registration): `new ADDCHARA_Instruction(false, true)`

**Syntax**
- `DELCHARA charaIndex`
- `DELCHARA charaIndex1, charaIndex2, ...`

**Arguments**
- Each `charaIndex`: int expression selecting an existing character index.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

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
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE`
- Engine-extracted notes (key operations):
  - `exm.VEvaluator.AddCharacter_UseSp(integer, isSp)`
  - `exm.VEvaluator.AddCharacter(integer)`
  - `exm.VEvaluator.DelCharacter(charaNoList[0])`
  - `exm.VEvaluator.DelCharacter(charaNoList)`

**Errors & validation**
- Runtime error if any `charaIndex` is out of range.
- When deleting multiple characters, runtime error if the same character is specified more than once (duplicate deletion).
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.SPCharaConfigIsOff.Text)`

**Examples**
```erabasic
DELCHARA 2
DELCHARA 1, 3
```

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_ANY`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1399 (`ADDCHARA_Instruction`)

## PUTFORM (instruction)
**Summary**
- Appends a formatted string to the save-description buffer (`SAVEDATA_TEXT`).

**Metadata**
- Arg spec: `FORM_STR_NULLABLE` (see #argument-spec-form_str_nullable)
- Flags (registration): `METHOD_SAFE`

**Syntax**
- `PUTFORM`
- `PUTFORM <formString>`

**Arguments**
- `<formString>` (optional): FORM/formatted string.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Evaluates `<formString>` to a string.
- Appends it to the save-description buffer:
  - If `SAVEDATA_TEXT` is non-null, `SAVEDATA_TEXT += <string>`.
  - Otherwise, `SAVEDATA_TEXT = <string>`.
- Does not print to the console.
- Typically used by the save-info generation path (e.g. `@SAVEINFO`) to build `SAVEDATA_TEXT`.
- Engine-extracted notes (key operations):
  - `if (vEvaluator.SAVEDATA_TEXT != null)`
  - `vEvaluator.SAVEDATA_TEXT += str`
  - `vEvaluator.SAVEDATA_TEXT = str`

**Errors & validation**
- None.

**Examples**
- `PUTFORM %PLAYERNAME% - Day %DAY%`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.FORM_STR_NULLABLE`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:289 (case `PUTFORM`)

## QUIT (instruction)
**Summary**
- Ends the current run by requesting the console to quit.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void)

**Syntax**
- `QUIT`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Requests the engine to quit the game.
- Script execution stops immediately.
- UI shutdown is performed by the console/UI host after the quit request is posted.
- Engine-extracted notes (key operations):
  - `exm.Console.Quit()`

**Errors & validation**
- None.

**Examples**
- `QUIT`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:299 (case `QUIT`)

## BEGIN (instruction)
**Summary**
- Requests a transition into one of the engine’s **system phases** (e.g. `SHOP`, `TRAIN`, `TITLE`) after the current call stack unwinds.

**Metadata**
- Arg spec: `STR` (see #argument-spec-str) (inferred from `BEGIN_Instruction` ArgBuilder assignment)
- Implementor (registration): `new BEGIN_Instruction()`

**Syntax**
- `BEGIN <keyword>`

**Arguments**
- `<keyword>`: raw string (the entire remainder of the source line after the instruction delimiter).
  - Must match one of the supported keywords exactly (see below).
  - The current engine compares this string literally (no automatic trim or case-folding).

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

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
- Engine-extracted notes (base flags from class):
  - `flag = FLOW_CONTROL`
- Engine-extracted notes (key operations):
  - `state.SetBegin(keyword, true)`
  - `state.Return(0)`
  - `exm.Console.ResetStyle()`

**Errors & validation**
- If `<keyword>` is not recognized, raises a runtime error (“invalid BEGIN argument”).

**Examples**
- `BEGIN TITLE`
- `BEGIN SHOP`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.STR`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3021 (`BEGIN_Instruction`)

## SAVEGAME (instruction)
**Summary**
- Opens the engine’s interactive **save UI** (system-driven save).

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `SAVELOADGAME_Instruction` ArgBuilder assignment)
- Implementor (registration): `new SAVELOADGAME_Instruction(true)`

**Syntax**
- `SAVEGAME`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

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
- Engine-extracted notes (base flags from class):
  - `flag = FLOW_CONTROL`
- Engine-extracted notes (key operations):
  - `if ((state.SystemState & SystemStateCode.__CAN_SAVE__) != SystemStateCode.__CAN_SAVE__)`
  - `string funcName = state.Scope`

**Errors & validation**
- Error if saving is not allowed in the current system state.
- If the underlying file write fails, the UI prints an error and waits for a key.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.CanNotUseInstruction.Text, funcName, "SAVEGAME/LOADGAME"))`

**Examples**
- `SAVEGAME`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3058 (`SAVELOADGAME_Instruction`)

## LOADGAME (instruction)
**Summary**
- Opens the engine’s interactive **load UI** (system-driven load).

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `SAVELOADGAME_Instruction` ArgBuilder assignment)
- Implementor (registration): `new SAVELOADGAME_Instruction(false)`

**Syntax**
- `LOADGAME`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

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
- Engine-extracted notes (base flags from class):
  - `flag = FLOW_CONTROL`
- Engine-extracted notes (key operations):
  - `if ((state.SystemState & SystemStateCode.__CAN_SAVE__) != SystemStateCode.__CAN_SAVE__)`
  - `string funcName = state.Scope`

**Errors & validation**
- Error if load is not allowed in the current system state.
- Selecting an empty slot prints a “no data” message and reopens the load prompt.
- If loading fails unexpectedly after selection, raises a runtime error.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.CanNotUseInstruction.Text, funcName, "SAVEGAME/LOADGAME"))`

**Examples**
- `LOADGAME`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3058 (`SAVELOADGAME_Instruction`)

## SAVEDATA (instruction)
**Summary**
- Saves the current game state to a numbered save slot file (script-controlled save).

**Metadata**
- Arg spec: `SP_SAVEDATA` (see #argument-spec-sp_savedata)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- `SAVEDATA <slot>, <saveText>`

**Arguments**
- `<slot>` (int): save slot number. Must satisfy `0 <= slot <= 2147483647` (32-bit signed non-negative).
- `<saveText>` (string): saved into the file and shown by the built-in save/load UI.
  - Must not contain a newline (`'\n'`).

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

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
- Engine-extracted notes (key operations):
  - `if (!vEvaluator.SaveTo((int)target, savemes))`
  - `console.PrintError(trerror.UnexpectedErrorInSavedata.Text)`

**Errors & validation**
- Errors if `<slot>` is negative or larger than `int.MaxValue`.
- Error if `<saveText>` contains `'\n'`.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.SavedataArgIsNegative.Text, target.ToString()))`
  - `throw new CodeEE(string.Format(trerror.TooLargeSavedataArg.Text, target.ToString()))`
  - `throw new CodeEE(trerror.SavetextContainNewLineCharacter.Text)`

**Examples**
- `SAVEDATA 0, "Start of day 1"`
- `SAVEDATA 12, SAVEDATA_TEXT`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_SAVEDATA`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:323 (case `SAVEDATA`)

## LOADDATA (instruction)
**Summary**
- Loads a numbered save slot file (script-controlled load), resets the call stack, and then runs the engine’s post-load system hooks.

**Metadata**
- Arg spec: `INT_EXPRESSION` (see #argument-spec-int_expression)
- Flags (registration): `EXTENDED`, `FLOW_CONTROL`

**Syntax**
- `LOADDATA [<slot>]`

**Arguments**
- `<slot>` (optional, int; default `0` with a warning if omitted): save slot index. Must be in `[0, 2147483647]` (32-bit signed non-negative).

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

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
- Engine-extracted notes (key operations):
  - `EraDataResult result = vEvaluator.CheckData((int)target, EraSaveFileType.Normal)`
  - `if (!vEvaluator.LoadFrom((int)target))`
  - `state.ClearFunctionList()`
  - `state.SystemState = SystemStateCode.LoadData_DataLoaded`

**Errors & validation**
- Errors if `<slot>` is negative or larger than `int.MaxValue`.
- Error if the target save file is missing/corrupt/mismatched.
- If loading fails unexpectedly after validation, a runtime error is raised.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.LoaddataArgIsNegative.Text, target.ToString()))`
  - `throw new CodeEE(string.Format(trerror.TooLargeLoaddataArg.Text, target.ToString()))`
  - `throw new CodeEE(trerror.LoadCorruptedData.Text)`
  - `throw new ExeEE(trerror.UnexpectedErrorInLoaddata.Text)`

**Examples**
- `LOADDATA 0`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:810 (case `LOADDATA`)

## DELDATA (instruction)
**Summary**
- Deletes a numbered save slot file (`saveXX.sav`) if it exists.

**Metadata**
- Arg spec: `INT_EXPRESSION` (see #argument-spec-int_expression) (inferred from `DELDATA_Instruction` ArgBuilder assignment)
- Implementor (registration): `new DELDATA_Instruction()`

**Syntax**
- `DELDATA <slot>`

**Arguments**
- `<slot>` (optional, int; default `0` with a warning if omitted): save slot index. Must be in `[0, 2147483647]` (32-bit signed non-negative).

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Computes the save file path under `SavDir` as `save{slot:00}.sav`.
- If the file does not exist, does nothing.
- If the file exists:
  - If it has the read-only attribute, raises an error.
  - Otherwise deletes it.
- See also: `save-files.md` (directories, partitions, and on-disk formats)
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `VariableEvaluator.DelData(target32)`

**Errors & validation**
- Errors if `<slot>` is negative or larger than `int.MaxValue`.
- Error if the file exists and is read-only.

**Examples**
- `DELDATA 3`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1995 (`DELDATA_Instruction`)

## SAVEGLOBAL (instruction)
**Summary**
- Saves global variables to `global.sav`.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `SAVEGLOBAL_Instruction` ArgBuilder assignment)
- Implementor (registration): `new SAVEGLOBAL_Instruction()`

**Syntax**
- `SAVEGLOBAL`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Writes the global save file under `SavDir`:
  - Path is `global.sav`.
- Save format:
  - If `SystemSaveInBinary` is enabled, writes Emuera’s binary save format with file type `Global`.
  - Otherwise, writes the legacy text save format.
  - Emuera-private global extension blocks may also be written.
- If a system-level I/O exception occurs during saving, the engine raises a runtime error.
- See also: `save-files.md` (directories, partitions, and on-disk formats)
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.VEvaluator.SaveGlobal()`

**Errors & validation**
- Errors if the save directory cannot be created or the file cannot be written.

**Examples**
- `SAVEGLOBAL`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1832 (`SAVEGLOBAL_Instruction`)

## LOADGLOBAL (instruction)
**Summary**
- Loads global variables from `global.sav` and reports success via `RESULT`.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `LOADGLOBAL_Instruction` ArgBuilder assignment)
- Implementor (registration): `new LOADGLOBAL_Instruction()`

**Syntax**
- `LOADGLOBAL`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Attempts to load `global.sav` under `SavDir`.
- On success:
  - Loads the global variable data from the file (format depends on file type).
  - Sets `RESULT = 1`.
- On failure:
  - Sets `RESULT = 0`.
- Before attempting to read, the loader removes certain Emuera-private global extension data; if loading then fails, this removal may still have occurred.
- See also: `save-files.md` (directories, partitions, and on-disk formats)
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `if (exm.VEvaluator.LoadGlobal())`
  - `exm.VEvaluator.RESULT = 1`
  - `exm.VEvaluator.RESULT = 0`

**Errors & validation**
- No explicit errors are raised for load failures; failures are reported via `RESULT`.

**Examples**
- `LOADGLOBAL`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1846 (`LOADGLOBAL_Instruction`)

## RESETDATA (instruction)
**Summary**
- Resets the current game/runtime variable state (excluding global variables).

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `RESETDATA_Instruction` ArgBuilder assignment)
- Implementor (registration): `new RESETDATA_Instruction()`

**Syntax**
- `RESETDATA`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Resets non-global variables to their default values (global variables are not reset).
- Disposes and clears the character list.
- Removes Emuera-private save-related extension data (e.g. XML/maps/data-table extensions).
- Resets output style to defaults.
- Does not assign `RESULT`/`RESULTS`.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.VEvaluator.ResetData()`
  - `exm.Console.ResetStyle()`

**Errors & validation**
- None.

**Examples**
- `RESETDATA`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1863 (`RESETDATA_Instruction`)

## RESETGLOBAL (instruction)
**Summary**
- Resets global variables to their default values.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `RESETGLOBAL_Instruction` ArgBuilder assignment)
- Implementor (registration): `new RESETGLOBAL_Instruction()`

**Syntax**
- `RESETGLOBAL`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Resets global variables to their default values.
- Removes Emuera-private global/static extension data (e.g. XML/maps global/static extensions).
- Does not assign `RESULT`/`RESULTS`.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.VEvaluator.ResetGlobalData()`

**Errors & validation**
- None.

**Examples**
- `RESETGLOBAL`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1878 (`RESETGLOBAL_Instruction`)

## SIF (instruction)
**Summary**
- “Single-line IF”: conditionally skips the **next logical line only**.

**Metadata**
- Arg spec: `INT_EXPRESSION` (see #argument-spec-int_expression) (inferred from `SIF_Instruction` ArgBuilder assignment)
- Implementor (registration): `new SIF_Instruction()`

**Syntax**
- `SIF [<int expr>]`
  - `<next logical line>`

**Arguments**
- `<int expr>` (optional, int; default `0` with a warning if omitted): condition (`0` = false, non-zero = true).

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- If the condition is true (non-zero), execution continues normally.
- If the condition is false (zero), the engine advances the program counter one extra time (skipping exactly one logical line).
- Load-time validation enforces an inherent limitation of this “skip the next line” model:
  - If the following line is a **partial instruction** (structural marker / block delimiter; e.g. `IF`, `ELSE`, `CASE`, loop markers), the engine warns because skipping marker lines breaks block structure.
  - If the following line is a `$label` line, the engine warns.
  - If there is no following executable line (EOF / next `@label`), the engine warns.
  - If there is at least one physically empty line between `SIF` and the next logical line, the engine warns.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | FLOW_CONTROL | PARTIAL | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `state.ShiftNextLine();//偽なら一行とばす。順に来たときと同じ扱いにする`

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

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3129 (`SIF_Instruction`)

## IF (instruction)
**Summary**
- Begins an `IF ... ENDIF` block. Chooses the first true clause among `IF` / `ELSEIF` / `ELSE` and executes that clause body.

**Metadata**
- Arg spec: `INT_EXPRESSION` (see #argument-spec-int_expression) (inferred from `IF_Instruction` ArgBuilder assignment)
- Implementor (registration): `new IF_Instruction()`
- Structural match end: `ENDIF`

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

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Evaluates its own condition and then each `ELSEIF` condition in order.
- If a condition is true, that clause’s body is selected and executed.
- If no condition matches:
  - If there is an `ELSE`, the `ELSE` body is executed.
  - Otherwise, the whole block is skipped.
- After any selected clause body finishes, the rest of the `IF` block is skipped and execution continues after the matching `ENDIF`.
- Jump behavior note (affects unstructured entry such as `GOTO` into blocks): when control transfers to an `IF`/`ELSEIF`/`ELSE` line as a jump target, execution begins at the **next** logical line (the clause body), not on the marker line itself. See `control-flow.md`.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | FLOW_CONTROL | PARTIAL | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `state.CurrentLine = line`
  - `state.JumpTo(ifJumpto)`

**Errors & validation**
- `ELSE` / `ELSEIF` without a matching open `IF`, or `ENDIF` without a matching open `IF`, are load-time errors (the line is marked as error).
- `ELSEIF` after an `ELSE` produces a load-time warning.

**Examples**
- `IF FLAG`
- `  PRINTL "yes"`
- `ELSE`
- `  PRINTL "no"`
- `ENDIF`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3200 (`IF_Instruction`)

## ELSE (instruction)
**Summary**
- Final clause header inside an `IF ... ENDIF` block.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new ELSEIF_Instruction(FunctionArgType.VOID)`

**Syntax**
- `ELSE`

**Arguments**
- None.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- When reached **sequentially**, `ELSE` unconditionally jumps to the matching `ENDIF` marker, skipping the rest of the block.
- When selected by the `IF` header, the engine jumps to the `ELSE` line as a **marker** and begins executing at the next line (the `ELSE` body).
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | FLOW_CONTROL | PARTIAL | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `state.JumpTo(func.JumpTo)`

**Errors & validation**
- Invalid placement (outside `IF`) is a load-time error (the line is marked as error).
- `ELSEIF` or `ELSE` after an `ELSE` produces a load-time warning.

**Examples**
- `ELSE`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3171 (`ELSEIF_Instruction`)

## ELSEIF (instruction)
**Summary**
- Clause header inside an `IF ... ENDIF` block.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new ELSEIF_Instruction(FunctionArgType.INT_EXPRESSION)`

**Syntax**
- `ELSEIF <int expr>`

**Arguments**
- `<int expr>` is evaluated by the `IF` header’s clause-selection logic (not by the `ELSEIF` instruction itself).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- When reached **sequentially** (i.e., a previous clause already executed and control fell through), `ELSEIF` unconditionally jumps to the matching `ENDIF` marker, skipping the rest of the block.
- When entered as the selected clause, the engine jumps to the `ELSEIF` line as a **marker** and begins executing at the next line (the clause body); the `ELSEIF` instruction itself is not executed in that path.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | FLOW_CONTROL | PARTIAL | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `state.JumpTo(func.JumpTo)`

**Errors & validation**
- Invalid placement (outside `IF`) is a load-time error (the line is marked as error).

**Examples**
- `ELSEIF A > 10`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3171 (`ELSEIF_Instruction`)

## ENDIF (instruction)
**Summary**
- Ends an `IF ... ENDIF` block.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `ENDIF_Instruction` ArgBuilder assignment)
- Implementor (registration): `new ENDIF_Instruction()`
- Additional flags (registration): `METHOD_SAFE`

**Syntax**
- `ENDIF`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Marker-only instruction (no runtime effect). The loader uses it to close the `IF` nesting and to set jump targets for `IF`/`ELSEIF`/`ELSE`.
- Engine-extracted notes (base flags from class):
  - `flag = FLOW_CONTROL | PARTIAL | FORCE_SETARG`

**Errors & validation**
- `ENDIF` without a matching open `IF` is a load-time error (the line is marked as error).

**Examples**
- `ENDIF`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3188 (`ENDIF_Instruction`)

## SELECTCASE (instruction)
**Summary**
- Begins a `SELECTCASE ... ENDSELECT` multi-branch block that compares a single selector expression against one or more `CASE` conditions.

**Metadata**
- Arg spec: `EXPRESSION` (see #argument-spec-expression) (inferred from `SELECTCASE_Instruction` ArgBuilder assignment)
- Implementor (registration): `new SELECTCASE_Instruction()`
- Structural match end: `ENDSELECT`

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
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- The loader gathers all `CASE` / `CASEELSE` headers into an ordered list and links them to the matching `ENDSELECT`.
- At runtime:
  - Evaluates the selector once to either `long` or `string`.
  - Scans each `CASE` in order; the first `CASE` that matches becomes the chosen clause.
  - If no `CASE` matches and a `CASEELSE` exists, chooses `CASEELSE`.
  - Otherwise jumps to the `ENDSELECT` marker (skipping the whole block).
- When a clause is chosen, the engine jumps to that `CASE`/`CASEELSE` header as a **marker** and begins executing at the next line (the clause body).
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED | FLOW_CONTROL | PARTIAL | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `state.CurrentLine = line`
  - `state.JumpTo(caseJumpto)`

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

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3255 (`SELECTCASE_Instruction`)

## CASE (instruction)
**Summary**
- Clause header inside a `SELECTCASE ... ENDSELECT` block.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new ELSEIF_Instruction(FunctionArgType.CASE)`
- Additional flags (registration): `EXTENDED`

**Syntax**
- `CASE <caseExpr> (, <caseExpr> ... )`

**Arguments**
- Each `<caseExpr>` is one of:
  - Normal: `<expr>` (matches by equality against the selector).
  - Range: `<expr> TO <expr>` (inclusive range).
  - “IS form”: `IS <binaryOp> <expr>` (e.g. `IS >= 10`), using the engine’s binary-operator semantics.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- When reached **sequentially** (fall-through after another case body), `CASE` unconditionally jumps to the matching `ENDSELECT` marker, skipping the rest of the block.
- When entered as the selected clause, the engine jumps to the `CASE` header as a **marker** and begins executing at the next line (the clause body).
- Matching rules (engine details):
  - Normal: `selector == expr` (strings use .NET `==` on `string`).
  - Range:
    - int: `left <= selector && selector <= right`
    - string: uses `string.Compare(left, selector, SCExpression)` and `string.Compare(selector, right, SCExpression)` (where `SCExpression` is the engine’s configured string-comparison mode for expressions).
  - `IS <op> <expr>`: evaluates `(selector <op> expr)` using the engine’s binary operator reducer.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | FLOW_CONTROL | PARTIAL | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `state.JumpTo(func.JumpTo)`

**Errors & validation**
- Invalid placement (outside `SELECTCASE`) is a load-time error (the line is marked as error).
- An empty `CASE` condition list is a load-time error (argument parsing fails and the line is marked as error).
- A `TO` range requires both sides to have the same operand type (otherwise: load-time error).

**Examples**
- `CASE 5`
- `CASE 1 TO 10`
- `CASE IS >= 100`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3171 (`ELSEIF_Instruction`)

## CASEELSE (instruction)
**Summary**
- Default clause header inside a `SELECTCASE ... ENDSELECT` block.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new ELSEIF_Instruction(FunctionArgType.VOID)`
- Additional flags (registration): `EXTENDED`

**Syntax**
- `CASEELSE`

**Arguments**
- None.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Chosen only if no earlier `CASE` matches.
- When reached **sequentially** (fall-through after another case body), `CASEELSE` unconditionally jumps to the matching `ENDSELECT` marker.
- When selected, the engine jumps to the `CASEELSE` header as a **marker** and begins executing at the next line (the clause body).
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | FLOW_CONTROL | PARTIAL | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `state.JumpTo(func.JumpTo)`

**Errors & validation**
- Invalid placement (outside `SELECTCASE`) is a load-time error (the line is marked as error).
- `CASE` after `CASEELSE` produces a load-time warning.

**Examples**
- `CASEELSE`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3171 (`ELSEIF_Instruction`)

## ENDSELECT (instruction)
**Summary**
- Ends a `SELECTCASE ... ENDSELECT` block.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `ENDIF_Instruction` ArgBuilder assignment)
- Implementor (registration): `new ENDIF_Instruction()`
- Additional flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- `ENDSELECT`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Marker-only instruction (no runtime effect). The loader uses it to close `SELECTCASE` nesting and to set jump targets for `SELECTCASE`/`CASE`/`CASEELSE`.
- Engine-extracted notes (base flags from class):
  - `flag = FLOW_CONTROL | PARTIAL | FORCE_SETARG`

**Errors & validation**
- `ENDSELECT` without a matching open `SELECTCASE` is a load-time error (the line is marked as error).

**Examples**
- `ENDSELECT`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3188 (`ENDIF_Instruction`)

## REPEAT (instruction)
**Summary**
- Begins a `REPEAT ... REND` counted loop using the built-in variable `COUNT` as the loop counter.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new REPEAT_Instruction(false)`
- Structural match end: `REND`

**Syntax**
- `REPEAT [<countExpr>]`
  - `...`
  - `REND`

**Arguments**
- `<countExpr>` (optional, int; default `0` with a warning if omitted): number of iterations.

**Defaults / optional arguments**
- (TODO)

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
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | FLOW_CONTROL | PARTIAL`
- Engine-extracted notes (key operations):
  - `state.JumpTo(func.JumpTo)`

**Errors & validation**
- If the system variable `COUNT` is forbidden by the current variable-scope configuration, `REPEAT` raises an error when its argument is parsed (typically: first execution of the `REPEAT` line).
- If a constant count is `<= 0`, the engine emits a warning when the line’s argument is parsed.
- Nested `REPEAT` is warned about by the loader (not necessarily a hard error).

**Examples**
- `REPEAT 10`
- `  PRINTV COUNT`
- `REND`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3082 (`REPEAT_Instruction`)

## REND (instruction)
**Summary**
- Ends a `REPEAT ... REND` loop.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `REND_Instruction` ArgBuilder assignment)
- Implementor (registration): `new REND_Instruction()`
- Structural parent: `REPEAT`

**Syntax**
- `REND`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Increments the loop counter and decides whether to continue:
  - If more iterations remain, jumps back to the matching `REPEAT` marker (and thus continues at the first body line).
  - Otherwise falls through to the next line after `REND`.
- Engine quirk: if the loop counter state is missing (e.g. due to invalid jumps into/out of the loop), `REND` exits the loop instead of throwing.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | FLOW_CONTROL | PARTIAL`
- Engine-extracted notes (key operations):
  - `state.JumpTo(jumpTo.JumpTo)`
  - `state.JumpTo(func.JumpTo)`

**Errors & validation**
- `REND` without a matching open `REPEAT` is a load-time error (the line is marked as error).

**Examples**
- `REND`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3505 (`REND_Instruction`)

## FOR (instruction)
**Summary**
- Begins a `FOR ... NEXT` counted loop over a mutable integer variable term.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new REPEAT_Instruction(true)`
- Additional flags (registration): `EXTENDED`
- Structural match end: `NEXT`

**Syntax**
- `FOR <intVarTerm>, <start>, <end> [, <step>]`
  - `...`
  - `NEXT`

**Arguments**
- `<intVarTerm>`: changeable integer variable term (must not be character-data).
- `<start>` (optional, int; default `0`): initial counter value.
- `<end>` (int): loop bound (exclusive).
- `<step>` (optional, int; default `1`): increment applied at `NEXT` time.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Initializes the counter variable to `<start>`, then loops while:
  - `step > 0`: `<counter> < <end>`
  - `step < 0`: `<counter> > <end>`
- If `step == 0`, the loop body executes zero times (execution jumps directly to `NEXT`).
- The counter variable is incremented by `step` at `NEXT` time (and also by `BREAK`/`CONTINUE` for era-maker compatibility).
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | FLOW_CONTROL | PARTIAL`
- Engine-extracted notes (key operations):
  - `state.JumpTo(func.JumpTo)`

**Errors & validation**
- Errors if `<intVarTerm>` is not a changeable variable term, or if it is character-data.
- `NEXT` without a matching open `FOR` is a load-time error (the `NEXT` line is marked as error).

**Examples**
- `FOR I, 0, 10`
- `  PRINTV I`
- `NEXT`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3082 (`REPEAT_Instruction`)

## NEXT (instruction)
**Summary**
- Ends a `FOR ... NEXT` loop.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `REND_Instruction` ArgBuilder assignment)
- Implementor (registration): `new REND_Instruction()`
- Additional flags (registration): `EXTENDED`
- Structural parent: `FOR`

**Syntax**
- `NEXT`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Like `REND`, but paired with `FOR`.
- Increments the loop counter by `step`, then:
  - If more iterations remain, jumps back to the matching `FOR` marker (and continues at the first body line).
  - Otherwise falls through to the next line after `NEXT`.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | FLOW_CONTROL | PARTIAL`
- Engine-extracted notes (key operations):
  - `state.JumpTo(jumpTo.JumpTo)`
  - `state.JumpTo(func.JumpTo)`

**Errors & validation**
- `NEXT` without a matching open `FOR` is a load-time error (the line is marked as error).

**Examples**
- `NEXT`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3505 (`REND_Instruction`)

## WHILE (instruction)
**Summary**
- Begins a `WHILE ... WEND` loop.

**Metadata**
- Arg spec: `INT_EXPRESSION` (see #argument-spec-int_expression) (inferred from `WHILE_Instruction` ArgBuilder assignment)
- Implementor (registration): `new WHILE_Instruction()`
- Structural match end: `WEND`

**Syntax**
- `WHILE [<int expr>]`
  - `...`
  - `WEND`

**Arguments**
- `<int expr>` (optional, int; default `0` with a warning if omitted): loop condition (`0` = false, non-zero = true).

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- At `WHILE`, evaluates the condition:
  - If true, enters the body (next line).
  - If false, jumps to the matching `WEND` marker (exiting the loop).
- At `WEND`, the engine re-evaluates the `WHILE` condition and loops again if it is still true.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED | FLOW_CONTROL | PARTIAL`
- Engine-extracted notes (key operations):
  - `state.JumpTo(func.JumpTo)`

**Errors & validation**
- `WEND` without a matching open `WHILE` is a load-time error (the `WEND` line is marked as error).

**Examples**
- `WHILE I < 10`
- `  I += 1`
- `WEND`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3113 (`WHILE_Instruction`)

## WEND (instruction)
**Summary**
- Ends a `WHILE ... WEND` loop.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `WEND_Instruction` ArgBuilder assignment)
- Implementor (registration): `new WEND_Instruction()`
- Structural parent: `WHILE`

**Syntax**
- `WEND`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Re-evaluates the matching `WHILE` condition:
  - If true, jumps back to the `WHILE` marker (and continues at the first body line).
  - If false, falls through to the next line after `WEND`.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED | FLOW_CONTROL | PARTIAL`
- Engine-extracted notes (key operations):
  - `state.JumpTo(func.JumpTo)`

**Errors & validation**
- `WEND` without a matching open `WHILE` is a load-time error (the line is marked as error).

**Examples**
- `WEND`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3533 (`WEND_Instruction`)

## DO (instruction)
**Summary**
- Begins a `DO ... LOOP` loop.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `ENDIF_Instruction` ArgBuilder assignment)
- Implementor (registration): `new ENDIF_Instruction()`
- Additional flags (registration): `METHOD_SAFE`, `EXTENDED`
- Structural match end: `LOOP`

**Syntax**
- `DO`
  - `...`
  - `LOOP <int expr>`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Marker-only instruction (no runtime effect).
- The loader links the `DO` marker with its matching `LOOP` condition line.
- Engine-extracted notes (base flags from class):
  - `flag = FLOW_CONTROL | PARTIAL | FORCE_SETARG`

**Errors & validation**
- `LOOP` without a matching open `DO` is a load-time error (the `LOOP` line is marked as error).

**Examples**
- `DO`
- `  I += 1`
- `LOOP I < 10`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3188 (`ENDIF_Instruction`)

## LOOP (instruction)
**Summary**
- Ends a `DO ... LOOP` loop and provides the loop condition.

**Metadata**
- Arg spec: `INT_EXPRESSION` (see #argument-spec-int_expression) (inferred from `LOOP_Instruction` ArgBuilder assignment)
- Implementor (registration): `new LOOP_Instruction()`
- Structural parent: `DO`

**Syntax**
- `LOOP [<int expr>]`

**Arguments**
- `<int expr>` (optional, int; default `0` with a warning if omitted): loop condition (`0` = false, non-zero = true).

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Evaluates the condition:
  - If true, jumps back to the matching `DO` marker (and continues at the first body line).
  - If false, falls through to the next line after `LOOP`.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED | FLOW_CONTROL | PARTIAL | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `state.JumpTo(func.JumpTo)`

**Errors & validation**
- `LOOP` without a matching open `DO` is a load-time error (the line is marked as error).

**Examples**
- `LOOP I < 10`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3548 (`LOOP_Instruction`)

## CONTINUE (instruction)
**Summary**
- Skips to the next iteration of the nearest enclosing loop (`REPEAT`, `FOR`, `WHILE`, or `DO`).

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `CONTINUE_Instruction` ArgBuilder assignment)
- Implementor (registration): `new CONTINUE_Instruction()`

**Syntax**
- `CONTINUE`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- The loader links `CONTINUE` to the nearest enclosing loop start marker.
- `REPEAT`/`FOR`: increments the loop counter by `step`, then either:
  - jumps back to the loop start marker (continue), or
  - jumps to the end marker (exit) if no iterations remain.
- `WHILE`: re-evaluates the condition and either continues or exits.
- `DO`: evaluates the matching `LOOP` condition and either continues or exits.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | FLOW_CONTROL`
- Engine-extracted notes (key operations):
  - `state.JumpTo(jumpTo.JumpTo)`
  - `state.JumpTo(func.JumpTo)`
  - `state.JumpTo(jumpTo);//DO`
  - `state.JumpTo(tFunc);//LOOP`

**Errors & validation**
- `CONTINUE` outside any loop is a load-time error (the line is marked as error).
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(tFunc.ErrMes, tFunc.Position)`
  - `throw new ExeEE(trerror.AbnormalContinue.Text)`

**Examples**
- `CONTINUE`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3449 (`CONTINUE_Instruction`)

## BREAK (instruction)
**Summary**
- Exits the nearest enclosing loop (`REPEAT`, `FOR`, `WHILE`, or `DO`).

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `BREAK_Instruction` ArgBuilder assignment)
- Implementor (registration): `new BREAK_Instruction()`

**Syntax**
- `BREAK`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- The loader links `BREAK` to the nearest enclosing loop start marker.
- At runtime, `BREAK` jumps to that loop’s end marker (so execution continues after the loop).
- For `REPEAT`/`FOR`, the engine also increments the loop counter once on `BREAK` (era-maker compatibility quirk).
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | FLOW_CONTROL`
- Engine-extracted notes (key operations):
  - `state.JumpTo(iLine)`

**Errors & validation**
- `BREAK` outside any loop is a load-time error (the line is marked as error).

**Examples**
- `BREAK`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3424 (`BREAK_Instruction`)

## RETURN (instruction)
**Summary**
- Returns from the current function. Also assigns the integer `RESULT` array (`RESULT:0`, `RESULT:1`, ...) from the provided values.

**Metadata**
- Arg spec: `INT_ANY` (see #argument-spec-int_any) (inferred from `RETURN_Instruction` ArgBuilder assignment)
- Implementor (registration): `new RETURN_Instruction()`

**Syntax**
- `RETURN`
- `RETURN <int expr1> [, <int expr2>, <int expr3>, ... ]`

**Arguments**
- `<valueN>` (optional, int): each value is stored into `RESULT:<index>`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Evaluates all provided integer expressions (left-to-right), stores them into the `RESULT` integer array starting at index 0, then returns from the function.
- The return value used by the call stack is `RESULT:0` after the assignment.
- If no values are provided, behaves like `RETURN 0` (sets `RESULT:0` to `0` and returns `0`).
- The engine does not clear unused `RESULT:<index>` slots; old values past the written prefix may remain.
- Load-time diagnostics (non-fatal): the engine may emit compatibility warnings when `RETURN` is used with a non-constant expression/variable, or with multiple values.
- Engine-extracted notes (base flags from class):
  - `flag = FLOW_CONTROL`
- Engine-extracted notes (key operations):
  - `exm.VEvaluator.RESULT = 0`
  - `state.Return(0)`
  - `exm.VEvaluator.SetResultX(termList)`
  - `state.Return(exm.VEvaluator.RESULT)`

**Errors & validation**
- Errors if any argument cannot be evaluated as an integer.

**Examples**
- `RETURN`
- `RETURN 0`
- `RETURN 1, 2, 3`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_ANY`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3367 (`RETURN_Instruction`)

## RETURNFORM (instruction)
**Summary**
- Returns from the current function like `RETURN`, but parses its values from a FORM/formatted string.

**Metadata**
- Arg spec: `FORM_STR` (see #argument-spec-form_str) (inferred from `RETURNFORM_Instruction` ArgBuilder assignment)
- Implementor (registration): `new RETURNFORM_Instruction()`

**Syntax**
- `RETURNFORM <formString>`

**Arguments**
- `<formString>` is evaluated to a string `s`, then `s` is re-lexed as one or more **comma-separated integer expressions**.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Evaluates the formatted string to a string `s`.
- Parses `s` as `expr1, expr2, ...` using the engine’s expression lexer/parser.
- Parsing detail: after each comma, the engine skips ASCII spaces (not tabs) before reading the next expression.
- Stores the resulting integer values into `RESULT:0`, `RESULT:1`, ... and returns.
- If `s` is empty, behaves like `RETURN 0`.
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED | FLOW_CONTROL`
- Engine-extracted notes (key operations):
  - `exm.VEvaluator.SetResultX(termList)`
  - `state.Return(exm.VEvaluator.RESULT)`
  - `if (state.ScriptEnd)`

**Errors & validation**
- Errors if any parsed expression is not a valid integer expression.

**Examples**
- `RETURNFORM 1, 2, %A%`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.FORM_STR`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3324 (`RETURNFORM_Instruction`)

## RETURNF (instruction)
**Summary**
- Returns from a user-defined expression function (`#FUNCTION/#FUNCTIONS`) with an optional return value.

**Metadata**
- Arg spec: `EXPRESSION_NULLABLE` (see #argument-spec-expression_nullable) (inferred from `RETURNF_Instruction` ArgBuilder assignment)
- Implementor (registration): `new RETURNF_Instruction()`

**Syntax**
- `RETURNF`
- `RETURNF <expr>`

**Arguments**
- `<expr>` (optional): expression whose type should match the function’s declared return type.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Sets the method return value for the current expression-function call and exits the method body.
- If `<expr>` is omitted:
  - int-returning method: returns `0`
  - string-returning method: returns `""`
- Load-time validation:
  - `RETURNF` outside a `#FUNCTION/#FUNCTIONS` body is a load-time error (the line is marked as error).
  - A return-type mismatch (`RETURNF` returns string from an int method, or int from a string method) is a load-time error.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED | FLOW_CONTROL`
- Engine-extracted notes (key operations):
  - `state.ReturnF(ret)`

**Errors & validation**
- Argument parsing errors follow normal expression parsing rules.

**Examples**
- `RETURNF 0`
- `RETURNF "OK"`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.EXPRESSION_NULLABLE`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3564 (`RETURNF_Instruction`)

## STRLEN (instruction)
**Summary**
- Sets `RESULT` to the engine’s **language/encoding length** of a raw string argument.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new STRLEN_Instruction(false, false)`

**Syntax**
- `STRLEN [<rawString>]`

**Arguments**
- `<rawString>` (optional, default `""`): literal remainder of the line (not a normal string expression).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Computes length via the engine’s language-aware length counter and assigns it to `RESULT`:
  - For ASCII-only strings: equals `str.Length`.
  - Otherwise: equals the current configured encoding’s `GetByteCount(str)` (often Shift-JIS in typical setups).
- For normal expression-style string evaluation (quotes, `%...%`, `{...}`), use `STRLENFORM` instead.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.VEvaluator.RESULT = str.Length`
  - `exm.VEvaluator.RESULT = LangManager.GetStrlenLang(str)`

**Errors & validation**
- None (apart from abnormal evaluation errors; the raw-string form is constant).

**Examples**
- `STRLEN ABC` sets `RESULT` to the byte length of `ABC` under the current encoding.

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:691 (`STRLEN_Instruction`)

## STRLENFORM (instruction)
**Summary**
- Sets `RESULT` to the engine’s **language/encoding length** of a FORM/formatted string.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new STRLEN_Instruction(true, false)`

**Syntax**
- `STRLENFORM [<formString>]`

**Arguments**
- `<formString>` (optional, default `""`): FORM/formatted string expression (supports `%...%` and `{...}`).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Evaluates the formatted string to a string value, then computes its language/encoding length (see `STRLEN` for details).
- Assigns the result to `RESULT`.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.VEvaluator.RESULT = str.Length`
  - `exm.VEvaluator.RESULT = LangManager.GetStrlenLang(str)`

**Errors & validation**
- Errors if the formatted string evaluation fails.

**Examples**
- `STRLENFORM NAME=%NAME%` sets `RESULT` to the length of the expanded string.

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:691 (`STRLEN_Instruction`)

## STRLENU (instruction)
**Summary**
- Sets `RESULT` to the Unicode code-unit length (`string.Length`) of a raw string argument.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new STRLEN_Instruction(false, true)`

**Syntax**
- `STRLENU [<rawString>]`

**Arguments**
- `<rawString>` (optional, default `""`): literal remainder of the line (not a normal string expression).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Computes length as `str.Length` and assigns it to `RESULT`.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.VEvaluator.RESULT = str.Length`
  - `exm.VEvaluator.RESULT = LangManager.GetStrlenLang(str)`

**Errors & validation**
- None (apart from abnormal evaluation errors; the raw-string form is constant).

**Examples**
- `STRLENU ABC` sets `RESULT` to `3`.

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:691 (`STRLEN_Instruction`)

## STRLENFORMU (instruction)
**Summary**
- Sets `RESULT` to the Unicode code-unit length (`string.Length`) of a FORM/formatted string.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new STRLEN_Instruction(true, true)`

**Syntax**
- `STRLENFORMU [<formString>]`

**Arguments**
- `<formString>` (optional, default `""`): FORM/formatted string expression.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Evaluates the formatted string to a string value, then assigns `str.Length` to `RESULT`.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.VEvaluator.RESULT = str.Length`
  - `exm.VEvaluator.RESULT = LangManager.GetStrlenLang(str)`

**Errors & validation**
- Errors if the formatted string evaluation fails.

**Examples**
- `STRLENFORMU NAME=%NAME%` sets `RESULT` to the character length of the expanded string.

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:691 (`STRLEN_Instruction`)

## SWAPCHARA (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `SP_SWAP` (see #argument-spec-sp_swap) (inferred from `SWAPCHARA_Instruction` ArgBuilder assignment)
- Implementor (registration): `new SWAPCHARA_Instruction()`

**Syntax**
- Hint (translated, best-effort): <int>,<int>
- Hint (raw comment): `<数値>,<数値>`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `SP_SWAP_ArgumentBuilder(false)`
- Type pattern: `[typeof(long), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `1`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.VEvaluator.SwapChara(x, y)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_SWAP`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1459 (`SWAPCHARA_Instruction`)

## COPYCHARA (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `SP_SWAP` (see #argument-spec-sp_swap) (inferred from `COPYCHARA_Instruction` ArgBuilder assignment)
- Implementor (registration): `new COPYCHARA_Instruction()`

**Syntax**
- Hint (translated, best-effort): <int>,<int>
- Hint (raw comment): `<数値>,<数値>`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `SP_SWAP_ArgumentBuilder(false)`
- Type pattern: `[typeof(long), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `1`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.VEvaluator.CopyChara(x, y)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_SWAP`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1475 (`COPYCHARA_Instruction`)

## ADDCOPYCHARA (instruction)
**Summary**
- Adds one or more new characters by copying an existing character’s data.

**Metadata**
- Arg spec: `INT_ANY` (see #argument-spec-int_any) (inferred from `ADDCOPYCHARA_Instruction` ArgBuilder assignment)
- Implementor (registration): `new ADDCOPYCHARA_Instruction()`

**Syntax**
- `ADDCOPYCHARA charaIndex`
- `ADDCOPYCHARA charaIndex1, charaIndex2, ...`

**Arguments**
- Each `charaIndex`: int expression selecting an existing character index to copy from.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Requires at least one argument; multiple arguments are accepted but the engine emits a parse-time warning for multi-argument uses.
- For each `charaIndex` (evaluated and executed left-to-right), the engine:
  - Validates the source index is in range; otherwise errors.
  - Appends a new pseudo character.
  - Copies all character data from the source character into the newly appended last character.
- `CHARANUM` increases by 1 for each successfully created copy.
- This instruction does not print anything and does not automatically change `TARGET`/`MASTER`/`ASSI`.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE`
- Engine-extracted notes (key operations):
  - `exm.VEvaluator.AddCopyChara(int64Term.GetIntValue(exm))`

**Errors & validation**
- Runtime error if any `charaIndex` is out of range.

**Examples**
```erabasic
ADDCOPYCHARA 0
```

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_ANY`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1492 (`ADDCOPYCHARA_Instruction`)

## SPLIT (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `SP_SPLIT` (see #argument-spec-sp_split)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- Hint (translated, best-effort): <string expr>, <string expr>, <可変文字variable term>
- Hint (raw comment): `<文字列式>, <文字列式>, <可変文字変数>`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `SP_SPLIT_ArgumentBuilder()`
- Type pattern: `[typeof(string), typeof(string), typeof(string), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `3`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_SPLIT`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:537 (case `SPLIT`)

## SETCOLOR (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `SP_COLOR` (see #argument-spec-sp_color)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `SP_COLOR_ArgumentBuilder()`
- Type pattern: `[typeof(long), typeof(long), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `1`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (key operations):
  - `exm.Console.SetStringStyle(c)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.SetcolorArgLessThan0.Text)`
  - `throw new CodeEE(trerror.SetcolorArgOver255.Text)`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_COLOR`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:396 (case `SETCOLOR`)

## SETCOLORBYNAME (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `STR` (see #argument-spec-str)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- Hint (translated, best-effort): raw string
- Hint (raw comment): `単純文字列型`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `STR_ArgumentBuilder(false)`

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (key operations):
  - `exm.Console.SetStringStyle(c)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.TransparentUnsupported.Text)`
  - `throw new CodeEE(string.Format(trerror.InvalidColorName.Text, colorName))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.STR`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:423 (case `SETCOLORBYNAME`)

## RESETCOLOR (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `RESETCOLOR_Instruction` ArgBuilder assignment)
- Implementor (registration): `new RESETCOLOR_Instruction()`

**Syntax**
- Hint (translated, best-effort): no arguments
- Hint (raw comment): `引数なし`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `VOID_ArgumentBuilder()`

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.Console.SetStringStyle(Config.ForeColor)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1533 (`RESETCOLOR_Instruction`)

## SETBGCOLOR (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `SP_COLOR` (see #argument-spec-sp_color)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `SP_COLOR_ArgumentBuilder()`
- Type pattern: `[typeof(long), typeof(long), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `1`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (key operations):
  - `exm.Console.SetBgColor(c)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.SetcolorArgLessThan0.Text)`
  - `throw new CodeEE(trerror.SetcolorArgOver255.Text)`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_COLOR`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:436 (case `SETBGCOLOR`)

## SETBGIMAGE (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `FORM_STR_ANY` (see #argument-spec-form_str_any) (inferred from `SETBGIMAGE_Instruction` ArgBuilder assignment)
- Implementor (registration): `new SETBGIMAGE_Instruction()`

**Syntax**
- Hint (translated, best-effort): 1つ以上のFORMstringをvariadic
- Hint (raw comment): `1つ以上のFORM文字列を任意数`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `FORM_STR_ANY_ArgumentBuilder()`

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.Console.AddBackgroundImage(bgName, bgDepth, opacity)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.FORM_STR_ANY`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1561 (`SETBGIMAGE_Instruction`)

## SETBGCOLORBYNAME (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `STR` (see #argument-spec-str)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- Hint (translated, best-effort): raw string
- Hint (raw comment): `単純文字列型`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `STR_ArgumentBuilder(false)`

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (key operations):
  - `exm.Console.SetBgColor(c)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.TransparentUnsupported.Text)`
  - `throw new CodeEE(string.Format(trerror.InvalidColorName.Text, colorName))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.STR`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:470 (case `SETBGCOLORBYNAME`)

## RESETBGCOLOR (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `RESETBGCOLOR_Instruction` ArgBuilder assignment)
- Implementor (registration): `new RESETBGCOLOR_Instruction()`

**Syntax**
- Hint (translated, best-effort): no arguments
- Hint (raw comment): `引数なし`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `VOID_ArgumentBuilder()`

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.Console.SetBgColor(Config.BackColor)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1547 (`RESETBGCOLOR_Instruction`)

## CLEARBGIMAGE (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `CLEARBGIMAGE_Instruction` ArgBuilder assignment)
- Implementor (registration): `new CLEARBGIMAGE_Instruction()`

**Syntax**
- Hint (translated, best-effort): no arguments
- Hint (raw comment): `引数なし`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `VOID_ArgumentBuilder()`

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.Console.ClearBackgroundImage()`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1603 (`CLEARBGIMAGE_Instruction`)

## REMOVEBGIMAGE (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `FORM_STR_ANY` (see #argument-spec-form_str_any) (inferred from `REMOVEBGIMAGE_Instruction` ArgBuilder assignment)
- Implementor (registration): `new REMOVEBGIMAGE_Instruction()`

**Syntax**
- Hint (translated, best-effort): 1つ以上のFORMstringをvariadic
- Hint (raw comment): `1つ以上のFORM文字列を任意数`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `FORM_STR_ANY_ArgumentBuilder()`

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.Console.RemoveBackground(bgName)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.FORM_STR_ANY`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1587 (`REMOVEBGIMAGE_Instruction`)

## FONTBOLD (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `FONTBOLD_Instruction` ArgBuilder assignment)
- Implementor (registration): `new FONTBOLD_Instruction()`

**Syntax**
- Hint (translated, best-effort): no arguments
- Hint (raw comment): `引数なし`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `VOID_ArgumentBuilder()`

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.Console.SetStringStyle(exm.Console.StringStyle.FontStyle | FontStyle.Bold)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1617 (`FONTBOLD_Instruction`)

## FONTITALIC (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `FONTITALIC_Instruction` ArgBuilder assignment)
- Implementor (registration): `new FONTITALIC_Instruction()`

**Syntax**
- Hint (translated, best-effort): no arguments
- Hint (raw comment): `引数なし`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `VOID_ArgumentBuilder()`

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.Console.SetStringStyle(exm.Console.StringStyle.FontStyle | FontStyle.Italic)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1632 (`FONTITALIC_Instruction`)

## FONTREGULAR (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `FONTREGULAR_Instruction` ArgBuilder assignment)
- Implementor (registration): `new FONTREGULAR_Instruction()`

**Syntax**
- Hint (translated, best-effort): no arguments
- Hint (raw comment): `引数なし`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `VOID_ArgumentBuilder()`

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.Console.SetStringStyle(FontStyle.Regular)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1647 (`FONTREGULAR_Instruction`)

## SORTCHARA (instruction)
**Summary**
- Reorders the engine’s character list (`0 .. CHARANUM-1`) by a key taken from a character-data variable.
- Observable behavior: keeps `MASTER` fixed at its numeric position for this instruction.

**Metadata**
- Arg spec: `SP_SORTCHARA` (see #argument-spec-sp_sortchara) (inferred from `SORTCHARA_Instruction` ArgBuilder assignment)
- Implementor (registration): `new SORTCHARA_Instruction()`

**Syntax**
- `SORTCHARA`
- `SORTCHARA FORWARD | BACK`
- `SORTCHARA <charaVarTerm> [ , FORWARD | BACK ]`

**Arguments**
- `<charaVarTerm>`: a variable term whose identifier is a character-data variable.
- Order: `FORWARD` = ascending, `BACK` = descending.
- If the key variable is an array, the element indices are taken from the variable term’s subscripts after the character selector.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Computes a sort key for each character via the engine’s key setter; null strings are treated as empty string.
- Stable sort: ties are broken by original order.
- After sorting, `TARGET`/`ASSI` are updated to keep pointing at the same character objects; `MASTER` is kept at its fixed index.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.VEvaluator.SortChara(sortKey.Identifier, elem, spSortArg.SortOrder, true)`

**Errors & validation**
- Parse-time error if `<charaVarTerm>` is not a character-data variable term.
- Runtime error if selected element indices are out of range for the variable.

**Examples**
- `SORTCHARA NO`
- `SORTCHARA CFLAG:3, BACK`
- `SORTCHARA NAME, FORWARD`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_SORTCHARA`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1508 (`SORTCHARA_Instruction`)

## FONTSTYLE (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `INT_EXPRESSION_NULLABLE` (see #argument-spec-int_expression_nullable)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- Hint (translated, best-effort): int expression
- Hint (raw comment): `数式型`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `INT_EXPRESSION_ArgumentBuilder(true)`
- Type pattern: `[typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (key operations):
  - `exm.Console.SetStringStyle(fs)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION_NULLABLE`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:483 (case `FONTSTYLE`)

## ALIGNMENT (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `STR` (see #argument-spec-str)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- Hint (translated, best-effort): raw string
- Hint (raw comment): `単純文字列型`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `STR_ArgumentBuilder(false)`

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (key operations):
  - `exm.Console.Alignment = DisplayLineAlignment.LEFT`
  - `exm.Console.Alignment = DisplayLineAlignment.CENTER`
  - `exm.Console.Alignment = DisplayLineAlignment.RIGHT`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.InvalidAlignment.Text, str))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.STR`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:508 (case `ALIGNMENT`)

## CUSTOMDRAWLINE (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new CUSTOMDRAWLINE_Instruction()`

**Syntax**
- (TODO)

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.Console.NewLine()`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:506 (`CUSTOMDRAWLINE_Instruction`)

## DRAWLINEFORM (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `FORM_STR` (see #argument-spec-form_str)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- Hint (translated, best-effort): FORM string型。
- Hint (raw comment): `書式付文字列型。`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `FORM_STR_ArgumentBuilder(false)`

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (key operations):
  - `exm.Console.printCustomBar(str, false)`
  - `exm.Console.NewLine()`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.FORM_STR`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:163 (case `DRAWLINEFORM`)

## CLEARTEXTBOX (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- Hint (translated, best-effort): no arguments
- Hint (raw comment): `引数なし`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `VOID_ArgumentBuilder()`

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (key operations):
  - `console.ClearText()`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:753 (case `CLEARTEXTBOX`)

## SETFONT (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `STR_EXPRESSION_NULLABLE` (see #argument-spec-str_expression_nullable)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `STR_EXPRESSION_ArgumentBuilder(true)`
- Type pattern: `[typeof(string)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (key operations):
  - `exm.Console.SetFont(str)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.STR_EXPRESSION_NULLABLE`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:501 (case `SETFONT`)

## SWAP (instruction)
**Summary**
- Swaps the values of two **changeable variables** (integer or string).

**Metadata**
- Arg spec: `SP_SWAPVAR` (see #argument-spec-sp_swapvar)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- `SWAP <var1>, <var2>`

**Arguments**
- `<var1>`: a changeable variable term (must not be `CONST`).
- `<var2>`: a changeable variable term (same type as `<var1>`).

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

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
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.VarsTypeDifferent.Text)`
  - `throw new CodeEE(trerror.UnknownVarType.Text)`

**Examples**
- `SWAP A, B`
- `SWAP NAME:TARGET, NICKNAME:TARGET`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_SWAPVAR`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:356 (case `SWAP`)

## RANDOMIZE (instruction)
**Summary**
- Seeds the legacy RNG with a specified integer seed.

**Metadata**
- Arg spec: `INT_EXPRESSION_NULLABLE` (see #argument-spec-int_expression_nullable) (inferred from `RANDOMIZE_Instruction` ArgBuilder assignment)
- Implementor (registration): `new RANDOMIZE_Instruction()`

**Syntax**
- `RANDOMIZE`
- `RANDOMIZE <seed>`

**Arguments**
- `<seed>` (optional): int. If omitted, the seed defaults to `0`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- If `UseNewRandom` is enabled in JSON config:
  - Emits a warning and does nothing.
- Otherwise:
  - Re-seeds the legacy RNG with `<seed>` truncated to 32 bits (i.e. low 32 bits used as an unsigned seed).
- Does not assign `RESULT`/`RESULTS`.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.VEvaluator.Randomize(iValue)`

**Errors & validation**
- None (besides normal integer-expression evaluation errors).

**Examples**
- `RANDOMIZE 0`
- `RANDOMIZE 12345`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION_NULLABLE`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1761 (`RANDOMIZE_Instruction`)

## DUMPRAND (instruction)
**Summary**
- Dumps the engine’s legacy RNG state into the `RANDDATA` variable.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `DUMPRAND_Instruction` ArgBuilder assignment)
- Implementor (registration): `new DUMPRAND_Instruction()`

**Syntax**
- `DUMPRAND`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- If `UseNewRandom` is enabled in JSON config:
  - Emits a warning and does nothing.
- Otherwise:
  - Writes the legacy RNG state into `RANDDATA`.
  - `RANDDATA` must have length 625; otherwise a runtime error is raised.
- Does not assign `RESULT`/`RESULTS`.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.VEvaluator.DumpRanddata()`

**Errors & validation**
- None.

**Examples**
- `DUMPRAND`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1809 (`DUMPRAND_Instruction`)

## INITRAND (instruction)
**Summary**
- Initializes the engine’s legacy RNG state from the `RANDDATA` variable.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `INITRAND_Instruction` ArgBuilder assignment)
- Implementor (registration): `new INITRAND_Instruction()`

**Syntax**
- `INITRAND`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- If `UseNewRandom` is enabled in JSON config:
  - Emits a warning and does nothing.
- Otherwise:
  - Loads the legacy RNG state from `RANDDATA`.
  - `RANDDATA` must have length 625; otherwise a runtime error is raised.
- Does not assign `RESULT`/`RESULTS`.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.VEvaluator.InitRanddata()`

**Errors & validation**
- None.

**Examples**
- `INITRAND`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1787 (`INITRAND_Instruction`)

## REDRAW (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `INT_EXPRESSION` (see #argument-spec-int_expression)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- Hint (translated, best-effort): int expression。optional
- Hint (raw comment): `数式型。省略可能`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `INT_EXPRESSION_ArgumentBuilder(false)`
- Type pattern: `[typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (key operations):
  - `exm.Console.SetRedraw(iValue)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:520 (case `REDRAW`)

## CALLTRAIN (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `INT_EXPRESSION` (see #argument-spec-int_expression)
- Flags (registration): `EXTENDED`, `FLOW_CONTROL`

**Syntax**
- Hint (translated, best-effort): int expression。optional
- Hint (raw comment): `数式型。省略可能`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `INT_EXPRESSION_ArgumentBuilder(false)`
- Type pattern: `[typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:878 (case `CALLTRAIN`)

## STOPCALLTRAIN (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void)
- Flags (registration): `EXTENDED`, `FLOW_CONTROL`

**Syntax**
- Hint (translated, best-effort): no arguments
- Hint (raw comment): `引数なし`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `VOID_ArgumentBuilder()`

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:885 (case `STOPCALLTRAIN`)

## DOTRAIN (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `INT_EXPRESSION` (see #argument-spec-int_expression)
- Flags (registration): `EXTENDED`, `FLOW_CONTROL`

**Syntax**
- Hint (translated, best-effort): int expression。optional
- Hint (raw comment): `数式型。省略可能`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `INT_EXPRESSION_ArgumentBuilder(false)`
- Type pattern: `[typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (key operations):
  - `switch (state.SystemState)`
  - `exm.Console.PrintSystemLine(state.SystemState.ToString())`
  - `state.SystemState = SystemStateCode.Train_DoTrain`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.CanNotUseDotrainHere.Text)`
  - `throw new CodeEE(trerror.DotrainArgLessThan0.Text)`
  - `throw new CodeEE(trerror.DotrainArgOverTrainnameArray.Text)`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:894 (case `DOTRAIN`)

## DATA (instruction)
**Summary**
- Declares one printable choice inside a surrounding `PRINTDATA*` / `STRDATA` / `DATALIST` block.
- `DATA` lines are *not* intended to execute as standalone statements; they are consumed by the loader into the surrounding block’s data list.

**Metadata**
- Arg spec: `STR_NULLABLE` (see #argument-spec-str_nullable)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`, `PARTIAL`, `PARTIAL`

**Syntax**
- `DATA [<raw text>]`
- `DATA;<raw text>`

**Arguments**
- `<raw text>` (optional, default `""`): raw text, not an expression.
  - Parsing detail: as with most instructions, Emuera consumes exactly one delimiter character after the keyword (space/tab/full-width-space if enabled, or `;`). The remainder of the line becomes the raw text.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

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

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.STR_NULLABLE`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`

## DATAFORM (instruction)
**Summary**
- Like `DATA`, but the text is a FORM/formatted string (scanned at load time).

**Metadata**
- Arg spec: `FORM_STR_NULLABLE` (see #argument-spec-form_str_nullable)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`, `PARTIAL`

**Syntax**
- `DATAFORM [<FORM string>]`

**Arguments**
- Optional FORM/formatted string scanned to end-of-line.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

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

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.FORM_STR_NULLABLE`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`

## ENDDATA (instruction)
**Summary**
- Closes a `PRINTDATA*` or `STRDATA` block.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `DO_NOTHING_Instruction` ArgBuilder assignment)
- Implementor (registration): `new DO_NOTHING_Instruction()`

**Syntax**
- `ENDDATA`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Load-time only structural marker. At runtime it does nothing.
- The loader wires `PRINTDATA*` / `STRDATA` to jump here after printing/selection.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED | PARTIAL`

**Errors & validation**
- `ENDDATA` without an open `PRINTDATA*` / `STRDATA` is a load-time error (the line is marked as error).
- Closing a block while a `DATALIST` is still open is a load-time error.

**Examples**
- (See `PRINTDATA`.)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:2016 (`DO_NOTHING_Instruction`)

## DATALIST (instruction)
**Summary**
- Starts a **multi-line** choice list inside a surrounding `PRINTDATA*` or `STRDATA` block.
- Each `DATA` / `DATAFORM` inside the list becomes a separate output line when this choice is selected.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`, `PARTIAL`
- Structural match end: `ENDLIST`

**Syntax**
- `DATALIST`
  - `DATA ...` / `DATAFORM ...` (one or more)
- `ENDLIST`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

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

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`

## ENDLIST (instruction)
**Summary**
- Closes a `DATALIST` block.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`, `PARTIAL`

**Syntax**
- `ENDLIST`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Load-time only structural marker. At runtime it does nothing.

**Errors & validation**
- `ENDLIST` without an open `DATALIST` is a load-time error (the line is marked as error).

**Examples**
- (See `DATALIST`.)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`

## STRDATA (instruction)
**Summary**
- Like `PRINTDATA`, but instead of printing, it selects a `DATA`/`DATAFORM` choice and concatenates it into a destination string variable.

**Metadata**
- Arg spec: `VAR_STR` (see #argument-spec-var_str)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`, `PARTIAL`
- Structural match end: `ENDDATA`

**Syntax**
- `STRDATA [<strVarTerm>]` ... `ENDDATA`

**Arguments**
- `<strVarTerm>` (optional; default `RESULTS`): changeable string variable term to receive the result.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Shares the same block structure as `PRINTDATA` (`DATA`, `DATAFORM`, `DATALIST`, `ENDDATA`).
- Selects one entry uniformly at random.
- Concatenates the selected lines with `\n` between them (for `DATALIST` multi-line entries).
- Stores the result into the destination variable and jumps to `ENDDATA`.
- If the block contains no `DATA`/`DATAFORM` choices at all, it simply jumps to `ENDDATA` and does **not** assign anything to the destination variable (it remains unchanged).
- Engine-extracted notes (key operations):
  - `state.JumpTo(func.JumpTo)`
  - `int choice = (int)exm.VEvaluator.GetNextRand(count)`
  - `state.CurrentLine = selectedLine`

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

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VAR_STR`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:756 (case `STRDATA`)

## SETBIT (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `BIT_ARG` (see #argument-spec-bit_arg) (inferred from `SETBIT_Instruction` ArgBuilder assignment)
- Implementor (registration): `new SETBIT_Instruction(1)`

**Syntax**
- Hint (translated, best-effort): <changeable int variable term>,<int>*n (SP_SETが使えないため新設)
- Hint (raw comment): `<可変数値変数>,<数値>*n (SP_SETが使えないため新設)`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `BIT_ARG_ArgumentBuilder()`
- Type pattern: `[typeof(long), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `2`.
- Variadic (`argAny`): `true`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.ArgIsOoRBit.Text, "2"))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.BIT_ARG`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:717 (`SETBIT_Instruction`)

## CLEARBIT (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `BIT_ARG` (see #argument-spec-bit_arg) (inferred from `SETBIT_Instruction` ArgBuilder assignment)
- Implementor (registration): `new SETBIT_Instruction(0)`

**Syntax**
- Hint (translated, best-effort): <changeable int variable term>,<int>*n (SP_SETが使えないため新設)
- Hint (raw comment): `<可変数値変数>,<数値>*n (SP_SETが使えないため新設)`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `BIT_ARG_ArgumentBuilder()`
- Type pattern: `[typeof(long), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `2`.
- Variadic (`argAny`): `true`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.ArgIsOoRBit.Text, "2"))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.BIT_ARG`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:717 (`SETBIT_Instruction`)

## INVERTBIT (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `BIT_ARG` (see #argument-spec-bit_arg) (inferred from `SETBIT_Instruction` ArgBuilder assignment)
- Implementor (registration): `new SETBIT_Instruction(-1)`

**Syntax**
- Hint (translated, best-effort): <changeable int variable term>,<int>*n (SP_SETが使えないため新設)
- Hint (raw comment): `<可変数値変数>,<数値>*n (SP_SETが使えないため新設)`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `BIT_ARG_ArgumentBuilder()`
- Type pattern: `[typeof(long), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `2`.
- Variadic (`argAny`): `true`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.ArgIsOoRBit.Text, "2"))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.BIT_ARG`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:717 (`SETBIT_Instruction`)

## DELALLCHARA (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- Hint (translated, best-effort): no arguments
- Hint (raw comment): `引数なし`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `VOID_ArgumentBuilder()`

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (key operations):
  - `vEvaluator.DelAllCharacter()`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:258 (case `DELALLCHARA`)

## PICKUPCHARA (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `INT_ANY` (see #argument-spec-int_any)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- Hint (translated, best-effort): 1つ以上のintをvariadic
- Hint (raw comment): `1つ以上の数値を任意数`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `INT_ANY_ArgumentBuilder()`
- Type pattern: `[typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.
- Variadic (`argAny`): `true`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (key operations):
  - `long charaNum = vEvaluator.CHARANUM`
  - `vEvaluator.PickUpChara(NoList)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.OoRPickupcharaArg.Text, (i + 1).ToString(), NoList[i].ToString()))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_ANY`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:263 (case `PICKUPCHARA`)

## VARSET (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `SP_VAR_SET` (see #argument-spec-sp_var_set) (inferred from `VARSET_Instruction` ArgBuilder assignment)
- Implementor (registration): `new VARSET_Instruction()`

**Syntax**
- Hint (translated, best-effort): <changeable variable term>,<int expr or string expr or null>(,<range start>, <range end>)
- Hint (raw comment): `<可変変数>,<数式 or 文字列式 or null>(,<範囲初値>, <範囲終値>)`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `SP_VAR_SET_ArgumentBuilder()`
- Type pattern: `[typeof(void), typeof(void), typeof(long), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `1`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `VariableEvaluator.SetValueAll(p, src, start, end)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_VAR_SET`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1663 (`VARSET_Instruction`)

## CVARSET (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `SP_CVAR_SET` (see #argument-spec-sp_cvar_set) (inferred from `CVARSET_Instruction` ArgBuilder assignment)
- Implementor (registration): `new CVARSET_Instruction()`

**Syntax**
- Hint (translated, best-effort): <changeable variable term>,<式>,<int expr or string expr or null>(,<range start>, <range end>)
- Hint (raw comment): `<可変変数>,<式>,<数式 or 文字列式 or null>(,<範囲初値>, <範囲終値>)`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `SP_CVAR_SET_ArgumentBuilder()`
- Type pattern: `[typeof(void), typeof(void), typeof(void), typeof(long), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `1`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `int charaNum = (int)exm.VEvaluator.CHARANUM`
  - `exm.VEvaluator.SetValueAllEachChara(p, index, src, start, end)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.OoRCvarsetArg.Text, "4", start.ToString()))`
  - `throw new CodeEE(string.Format(trerror.OoRCvarsetArg.Text, "5", start.ToString()))`
  - `throw new CodeEE(string.Format(trerror.CvarsetArgIsNotCharaVar.Text, p.Identifier.Name))`
  - `throw new CodeEE(string.Format(trerror.NotDefinedKey.Text, p.Identifier.Name, singleStrTerm.Str))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_CVAR_SET`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1705 (`CVARSET_Instruction`)

## RESET_STAIN (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `INT_EXPRESSION` (see #argument-spec-int_expression)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- Hint (translated, best-effort): int expression。optional
- Hint (raw comment): `数式型。省略可能`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `INT_EXPRESSION_ArgumentBuilder(false)`
- Type pattern: `[typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (key operations):
  - `vEvaluator.SetDefaultStain(iValue)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:528 (case `RESET_STAIN`)

## FORCEKANA (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `INT_EXPRESSION` (see #argument-spec-int_expression)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- Hint (translated, best-effort): int expression。optional
- Hint (raw comment): `数式型。省略可能`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `INT_EXPRESSION_ArgumentBuilder(false)`
- Type pattern: `[typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (key operations):
  - `exm.ForceKana(iValue)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:566 (case `FORCEKANA`)

## SKIPDISP (instruction)
**Summary**
- Enables/disables the engine’s “skip output” mode, which causes most print/wait/input built-ins to be skipped.
- Also sets `RESULT` to indicate whether skip mode is currently enabled.

**Metadata**
- Arg spec: `INT_EXPRESSION` (see #argument-spec-int_expression)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- `SKIPDISP <int expr>`

**Arguments**
- `<int expr>`: `0` disables skip mode; non-zero enables skip mode.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Evaluates `<int expr>` to `v`.
- If `v != 0`, enables output skipping; otherwise disables it.
- Sets `RESULT` to:
  - `1` when output skipping is enabled
  - `0` when output skipping is disabled
- While output skipping is enabled, the script runner skips most output-producing instructions (print/wait/input families).
- Special case (runtime error): if output skipping was enabled by `SKIPDISP`, then encountering an input instruction (e.g. `INPUT*`) raises an error rather than being silently skipped.
- Engine-extracted notes (key operations):
  - `vEvaluator.RESULT = skipPrint ? 1L : 0L`

**Errors & validation**
- Argument type errors follow the normal integer-expression argument rules.
- Runtime error if an input instruction is reached while output skipping is active due to `SKIPDISP`.

**Examples**
- `SKIPDISP 1` (enable skip)
- `SKIPDISP 0` (disable skip)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:573 (case `SKIPDISP`)

## NOSKIP (instruction)
**Summary**
- Begins a `NOSKIP ... ENDNOSKIP` block that temporarily disables output skipping within the block body.
- Intended to force some output/wait behavior to run even if `SKIPDISP` is currently skipping print-family instructions.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`, `PARTIAL`
- Structural match end: `ENDNOSKIP`

**Syntax**
- `NOSKIP`
  - `...`
- `ENDNOSKIP`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

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
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.MissingEndnoskip.Text)`

**Examples**
```erabasic
SKIPDISP 1

NOSKIP
  PRINTL This line still prints even during SKIPDISP.
ENDNOSKIP
```

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:581 (case `NOSKIP`)

## ENDNOSKIP (instruction)
**Summary**
- Ends a `NOSKIP ... ENDNOSKIP` block.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`, `PARTIAL`

**Syntax**
- `ENDNOSKIP`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Structural marker paired with `NOSKIP`.
- See `NOSKIP` for the block’s runtime behavior (temporary disabling and restoration of output skipping).

**Errors & validation**
- `ENDNOSKIP` without a matching open `NOSKIP` is a load-time error (the line is marked as error).
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.MissingNoskip.Text, "ENDNOSKIP"))`

**Examples**
- (See `NOSKIP`.)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:590 (case `ENDNOSKIP`)

## ARRAYSHIFT (instruction)
**Summary**
- Shifts elements in a mutable 1D array variable by an offset (can be negative) and fills new slots with a default value.

**Metadata**
- Arg spec: `SP_SHIFT_ARRAY` (see #argument-spec-sp_shift_array)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- `ARRAYSHIFT <arrayVar>, <shift>, <default> [, <start> [, <count>]]`

**Arguments**
- `<arrayVar>`: changeable 1D array variable term.
- `<shift>` (int): shift offset (can be negative). `0` is a no-op.
- `<default>`: expression of the same scalar type as the array element type.
- `<start>` (optional, int; default `0`): start index of the shifted segment.
- `<count>` (optional, int; default “to end”): number of elements in the segment. If explicitly `0`, this is a no-op.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Operates on the segment `[start, start+count)` (or `[start, end)` if count omitted).
- If `shift == 0`, does nothing.
- If shifting removes all overlap, fills the whole segment with `<default>`.
- If `start + count` exceeds array length, the engine clamps `count` to fit.
- Engine-extracted notes (key operations):
  - `VariableEvaluator.ShiftArray(dest, shift, def, start, num)`
  - `VariableEvaluator.ShiftArray(dest, shift, defs, start, num)`

**Errors & validation**
- Errors if `<arrayVar>` is not 1D, if `start < 0`, if `count < 0` (when provided), or if `start >= arrayLength`.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.IsUsableOnly1DVar.Text, "ARRAYSHIFT"))`
  - `throw new CodeEE(string.Format(trerror.ArgIsNegative.Text, "ARRAYSHIFT", "4", start.ToString()))`
  - `throw new CodeEE(string.Format(trerror.ArgIsNegative.Text, "ARRAYSHIFT", "5", num.ToString()))`

**Examples**
- `ARRAYSHIFT SOME_INT_ARRAY, 1, 0`
- `ARRAYSHIFT SOME_STR_ARRAY, -2, "", 10`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_SHIFT_ARRAY`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:612 (case `ARRAYSHIFT`)

## ARRAYREMOVE (instruction)
**Summary**
- Removes a slice of elements from a mutable 1D array by shifting later elements left and filling the tail with default values.

**Metadata**
- Arg spec: `SP_CONTROL_ARRAY` (see #argument-spec-sp_control_array)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- `ARRAYREMOVE <arrayVar>, <start>, <count>`

**Arguments**
- `<arrayVar>`: changeable 1D array variable term.
- `<start>` (int): start index (0-based).
- `<count>` (int): number of elements to remove.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Works only on 1D arrays (int or string).
- Removes elements in the conceptual range `[start, start+count)`:
  - Elements after the removed segment are shifted left into the gap.
  - The remaining tail is filled with defaults:
    - int arrays: `0`
    - string arrays: `null` internally (typically observed as empty string in many contexts)
- Special case: if `<count> <= 0`, the engine treats it as “remove to the end” (it effectively clears the suffix starting at `<start>`).
- If `<start> + <count>` exceeds the array length, it behaves like removing to the end.
- Engine-extracted notes (key operations):
  - `VariableEvaluator.RemoveArray(p, start, num)`

**Errors & validation**
- Runtime errors:
  - `<start> < 0`
  - `<start> >= array length`
  - `<arrayVar>` is not a 1D array
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.IsUsableOnly1DVar.Text, "ARRAYREMOVE"))`
  - `throw new CodeEE(string.Format(trerror.ArgIsNegative.Text, "ARRAYREMOVE", "2", start.ToString()))`

**Examples**
- `ARRAYREMOVE A, 0, 1` (drop first element)
- `ARRAYREMOVE A, 10, -1` (clear suffix from index 10)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_CONTROL_ARRAY`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:647 (case `ARRAYREMOVE`)

## ARRAYSORT (instruction)
**Summary**
- Sorts a mutable 1D array in ascending or descending order, optionally within a subrange.

**Metadata**
- Arg spec: `SP_SORTARRAY` (see #argument-spec-sp_sortarray)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- `ARRAYSORT <arrayVar> [, FORWARD|BACK [, <start> [, <count>]]]`

**Arguments**
- `<arrayVar>`: changeable 1D array variable term (int or string).
- `FORWARD|BACK` (optional; default `FORWARD`):
  - `FORWARD`: ascending
  - `BACK`: descending
- `<start>` (optional, int; default `0`): subrange start index (only parsed when `FORWARD|BACK` is present).
- `<count>` (optional, int; default “to end”): subrange length (only parsed when `FORWARD|BACK` is present). If explicitly `0`, this is a no-op.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Order defaults to ascending.
- Sorts the specified region of the array:
  - If `<count>` is omitted: sorts to end.
  - If `<count>` is provided and `<= 0`: `0` is a no-op; `<0` is an error.
- Parsing quirk:
  - `<start>` and `<count>` are only parsed when the `FORWARD|BACK` token is present.
  - If the token after the first comma is not `FORWARD` or `BACK`:
    - identifier → parse-time error
    - non-identifier (e.g. a number) → ignored (sorts the whole array with default order)
- Engine-extracted notes (key operations):
  - `VariableEvaluator.SortArray(p, arrayArg.Order, start, num)`

**Errors & validation**
- Parse-time errors if `<arrayVar>` is not a changeable 1D array variable term, or if the order token is present but not `FORWARD` or `BACK`.
- Runtime errors if:
  - `<start> < 0`
  - `<start> >= array length`
  - `<start> + <count>` exceeds array length (when `<count>` is provided and positive)
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.IsUsableOnly1DVar.Text, "ARRAYSORT"))`
  - `throw new CodeEE(string.Format(trerror.ArgIsNegative.Text, "ARRAYSORT", "3", start.ToString()))`
  - `throw new CodeEE(string.Format(trerror.ArgIsNegative.Text, "ARRAYSORT", "4", start.ToString()))`

**Examples**
- `ARRAYSORT A`
- `ARRAYSORT A, BACK`
- `ARRAYSORT A, FORWARD, 10, 20` (sort subrange)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_SORTARRAY`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:664 (case `ARRAYSORT`)

## ARRAYCOPY (instruction)
**Summary**
- Copies elements from one array variable to another array variable of the same element type and dimension.

**Metadata**
- Arg spec: `SP_COPY_ARRAY` (see #argument-spec-sp_copy_array)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- `ARRAYCOPY <srcVarNameExpr>, <dstVarNameExpr>`

**Arguments**
- `<srcVarNameExpr>` (string): expression whose value is a variable name.
- `<dstVarNameExpr>` (string): expression whose value is a variable name.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Resolves both variable names to variable tokens (early when literal, otherwise at runtime).
- Requires both to be arrays (1D/2D/3D), non-character-data; destination must be non-const.
- Copies element-wise:
  - If array sizes differ, only the overlapping region is copied (per dimension); there is no error for size mismatch.
  - Elements outside the copied region in the destination are left unchanged.
- Engine-extracted notes (key operations):
  - `VariableEvaluator.CopyArray(vars[0], vars[1])`

**Errors & validation**
- Errors if a name does not resolve to a variable, if either is not an array, if either is character-data, if destination is const, or if dimension/type mismatch.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.NotVariableName.Text, "ARRAYCOPY", "1", names[0]))`
  - `throw new CodeEE(string.Format(trerror.ArraycopyArgIsNotArray.Text, "1", names[0]))`
  - `throw new CodeEE(string.Format(trerror.ArraycopyArgIsCharaVar.Text, "1", names[0]))`
  - `throw new CodeEE(string.Format(trerror.NotVariableName.Text, "ARRAYCOPY", "2", names[1]))`
  - `throw new CodeEE(string.Format(trerror.ArraycopyArgIsNotArray.Text, "2", names[1]))`
  - `throw new CodeEE(string.Format(trerror.ArraycopyArgIsCharaVar.Text, "2", names[1]))`
  - `throw new CodeEE(string.Format(trerror.ArraycopyArgIsConst.Text, "2", names[1]))`
  - `throw new CodeEE(trerror.DifferentArraycopyArgsDim.Text)`
  - `throw new CodeEE(trerror.DifferentArraycopyArgsType.Text)`

**Examples**
- `ARRAYCOPY "ABL", "ABL_BAK"`
- `ARRAYCOPY "ITEM", SAVETO`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_COPY_ARRAY`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:687 (case `ARRAYCOPY`)

## SKIPLOG (instruction)
**Summary**
- Sets the console’s “message skip” flag (`MesSkip`), which affects UI-side input handling and macro/skip behavior.
- This is **not** the same mechanism as `SKIPDISP` (which skips print-family instructions in the script runner).

**Metadata**
- Arg spec: `INT_EXPRESSION` (see #argument-spec-int_expression)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- `SKIPLOG <int expr>`

**Arguments**
- `<int expr>`: `0` clears message-skip; non-zero enables message-skip.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Evaluates `<int expr>` to `v`.
- Sets the message-skip flag `MesSkip` to `(v != 0)`.
- Implementation-oriented effect (UI-side):
  - When `MesSkip` is true, the input loop may automatically advance through waits that do not require a value, unless the current wait request explicitly stops message skip.
  - Some input instructions (`INPUT*`/`TINPUT*`) have a `canSkip` option that uses `MesSkip` to auto-accept their default value without waiting.
- Engine-extracted notes (key operations):
  - `console.MesSkip = iValue != 0`

**Errors & validation**
- Argument type errors follow the normal integer-expression argument rules.

**Examples**
- `SKIPLOG 1`
- `SKIPLOG 0`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:784 (case `SKIPLOG`)

## JUMP (instruction)
**Summary**
- Jumps into another non-event function (`@NAME`) like `CALL`, but does not return to the current function.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new CALL_Instruction(false, true, false, false)`

**Syntax**
- `JUMP <functionName> [, <arg1>, <arg2>, ... ]`
- `JUMP <functionName>(<arg1>, <arg2>, ... )`

**Arguments**
- Same as `CALL`.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Enters the target function.
- When the target function returns, the engine immediately returns again, effectively discarding the current function’s return address (tail-call-like behavior).
- Engine-extracted notes (base flags from class):
  - `flag = FLOW_CONTROL | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `state.JumpTo(func.JumpToEndCatch)`
  - `state.IntoFunction(call, arg, exm)`

**Errors & validation**
- Same as `CALL`.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.NotDefinedFunc.Text, labelName))`
  - `throw new CodeEE(errMes)`

**Examples**
- `JUMP NEXT_PHASE`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3607 (`CALL_Instruction`)

## CALL (instruction)
**Summary**
- Calls a non-event script function (`@NAME`) and returns to the next line after the `CALL` when the callee returns.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new CALL_Instruction(false, false, false, false)`

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
- (TODO)

**Semantics**
- Resolves the target label to a non-event function.
  - If `CompatiCallEvent` is enabled, an event function name is also callable via `CALL` (compatibility behavior: it calls only the first-defined function, ignoring event priority/single flags).
- Evaluates arguments, binds them to the callee’s declared formals (including `REF` behavior), then enters the callee.
- When the callee executes `RETURN` (or reaches end-of-function), control returns to the statement after the `CALL`.
- Load-time behavior: if `<functionName>` is a compile-time constant, the loader tries to resolve the callee and may emit early diagnostics (e.g. unknown function, argument binding issues).
- Engine-extracted notes (base flags from class):
  - `flag = FLOW_CONTROL | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `state.JumpTo(func.JumpToEndCatch)`
  - `state.IntoFunction(call, arg, exm)`

**Errors & validation**
- If `<functionName>` is a constant string:
  - Non-`TRY*` variants: an unknown function is a load-time error (the line is marked as error).
  - `TRY*` variants: an unknown function is allowed (the line is not marked as error).
- Errors if the function exists but is not callable by `CALL`:
  - event function name when `CompatiCallEvent` is disabled
  - user-defined expression function (`#FUNCTION/#FUNCTIONS`)
- Errors if argument binding fails (too many args, omitted required args, type conversion not permitted, invalid `REF` binding, etc.).
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.NotDefinedFunc.Text, labelName))`
  - `throw new CodeEE(errMes)`

**Examples**
- `CALL TRAIN_MAIN, TARGET`
- `CALL SHOP_MAIN()`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3607 (`CALL_Instruction`)

## TRYJUMP (instruction)
**Summary**
- Like `JUMP`, but if the target function does not exist the instruction **does not error** and simply falls through to the next line.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new CALL_Instruction(false, true, true, false)`
- Additional flags (registration): `EXTENDED`

**Syntax**
- `TRYJUMP <functionName> [, <arg1>, <arg2>, ... ]`
- `TRYJUMP <functionName>(<arg1>, <arg2>, ... )`

**Arguments**
- Same as `JUMP`.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- If the target function exists: behaves like `JUMP`.
- If the target function does not exist: does nothing (continues at the next line after `TRYJUMP`).
- Engine-extracted notes (base flags from class):
  - `flag = FLOW_CONTROL | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `state.JumpTo(func.JumpToEndCatch)`
  - `state.IntoFunction(call, arg, exm)`

**Errors & validation**
- Still errors for invalid argument binding/type conversion when a function is found.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.NotDefinedFunc.Text, labelName))`
  - `throw new CodeEE(errMes)`

**Examples**
- `TRYJUMP OPTIONAL_PHASE`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3607 (`CALL_Instruction`)

## TRYCALL (instruction)
**Summary**
- Like `CALL`, but if the target function does not exist the instruction **does not error** and simply falls through to the next line.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new CALL_Instruction(false, false, true, false)`
- Additional flags (registration): `EXTENDED`

**Syntax**
- `TRYCALL <functionName> [, <arg1>, <arg2>, ... ]`
- `TRYCALL <functionName>(<arg1>, <arg2>, ... )`

**Arguments**
- Same as `CALL`.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- If the target function exists: behaves like `CALL`.
- If the target function does not exist: does nothing (continues at the next line after `TRYCALL`).
- Engine-extracted notes (base flags from class):
  - `flag = FLOW_CONTROL | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `state.JumpTo(func.JumpToEndCatch)`
  - `state.IntoFunction(call, arg, exm)`

**Errors & validation**
- Still errors for invalid argument binding/type conversion when a function is found.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.NotDefinedFunc.Text, labelName))`
  - `throw new CodeEE(errMes)`

**Examples**
- `TRYCALL OPTIONAL_HOOK`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3607 (`CALL_Instruction`)

## JUMPFORM (instruction)
**Summary**
- Like `JUMP`, but the function name is a formatted (FORM) string expression evaluated at runtime.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new CALL_Instruction(true, true, false, false)`
- Additional flags (registration): `EXTENDED`

**Syntax**
- `JUMPFORM <formString> [, <arg1>, <arg2>, ... ]`
- `JUMPFORM <formString>(<arg1>, <arg2>, ... )`

**Arguments**
- Same as `CALLFORM`.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Same as `JUMP`, with a runtime-evaluated function name.
- Engine-extracted notes (base flags from class):
  - `flag = FLOW_CONTROL | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `state.JumpTo(func.JumpToEndCatch)`
  - `state.IntoFunction(call, arg, exm)`

**Errors & validation**
- Same as `JUMP`, but errors may occur at runtime if the evaluated function name varies.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.NotDefinedFunc.Text, labelName))`
  - `throw new CodeEE(errMes)`

**Examples**
- `JUMPFORM "EVENT_%COUNT%"`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3607 (`CALL_Instruction`)

## CALLFORM (instruction)
**Summary**
- Like `CALL`, but the function name is a formatted (FORM) string expression evaluated at runtime.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new CALL_Instruction(true, false, false, false)`
- Additional flags (registration): `EXTENDED`

**Syntax**
- `CALLFORM <formString> [, <arg1>, <arg2>, ... ]`
- `CALLFORM <formString>(<arg1>, <arg2>, ... )`

**Arguments**
- `<formString>`: FORM/formatted string; the evaluated result is used as the function name.
  - If this FORM expression constant-folds to a constant string, the engine treats it like `CALL` for load-time resolution.
- `<argN>`: same as `CALL`.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Evaluates the function name string, resolves it to a non-event function, binds arguments, and enters the callee.
- Engine-extracted notes (base flags from class):
  - `flag = FLOW_CONTROL | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `state.JumpTo(func.JumpToEndCatch)`
  - `state.IntoFunction(call, arg, exm)`

**Errors & validation**
- Same as `CALL`, but errors may occur at runtime if the evaluated function name varies.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.NotDefinedFunc.Text, labelName))`
  - `throw new CodeEE(errMes)`

**Examples**
- `CALLFORM "TRAIN_%TARGET%", TARGET`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3607 (`CALL_Instruction`)

## TRYJUMPFORM (instruction)
**Summary**
- Like `JUMPFORM`, but if the evaluated function name does not resolve to a function the instruction **does not error** and simply falls through.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new CALL_Instruction(true, true, true, false)`
- Additional flags (registration): `EXTENDED`

**Syntax**
- `TRYJUMPFORM <formString> [, <arg1>, <arg2>, ... ]`
- `TRYJUMPFORM <formString>(<arg1>, <arg2>, ... )`

**Arguments**
- Same as `JUMPFORM`.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- If the target function exists: behaves like `JUMPFORM`.
- If not: does nothing (continues at the next line after `TRYJUMPFORM`).
- Engine-extracted notes (base flags from class):
  - `flag = FLOW_CONTROL | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `state.JumpTo(func.JumpToEndCatch)`
  - `state.IntoFunction(call, arg, exm)`

**Errors & validation**
- Still errors for invalid argument binding/type conversion when a function is found.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.NotDefinedFunc.Text, labelName))`
  - `throw new CodeEE(errMes)`

**Examples**
- `TRYJUMPFORM "OPTIONAL_%COUNT%"`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3607 (`CALL_Instruction`)

## TRYCALLFORM (instruction)
**Summary**
- Like `CALLFORM`, but if the evaluated function name does not resolve to a function the instruction **does not error** and simply falls through.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new CALL_Instruction(true, false, true, false)`
- Additional flags (registration): `EXTENDED`

**Syntax**
- `TRYCALLFORM <formString> [, <arg1>, <arg2>, ... ]`
- `TRYCALLFORM <formString>(<arg1>, <arg2>, ... )`

**Arguments**
- Same as `CALLFORM`.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- If the target function exists: behaves like `CALLFORM`.
- If not: does nothing (continues at the next line after `TRYCALLFORM`).
- Engine-extracted notes (base flags from class):
  - `flag = FLOW_CONTROL | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `state.JumpTo(func.JumpToEndCatch)`
  - `state.IntoFunction(call, arg, exm)`

**Errors & validation**
- Still errors for invalid argument binding/type conversion when a function is found.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.NotDefinedFunc.Text, labelName))`
  - `throw new CodeEE(errMes)`

**Examples**
- `TRYCALLFORM "HOOK_%TARGET%"`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3607 (`CALL_Instruction`)

## TRYCJUMP (instruction)
**Summary**
- Like `TRYJUMP`, but supports a `CATCH ... ENDCATCH` block for the “not found” case.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new CALL_Instruction(false, true, true, true)`
- Additional flags (registration): `EXTENDED`
- Structural match end: `CATCH`

**Syntax**
- `TRYCJUMP <functionName> [, <arg1>, ... ]`
- `CATCH`
  - `<catch body>`
  - `ENDCATCH`

**Arguments**
- Same as `JUMP`.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- If the target function exists: behaves like `JUMP` (tail-call-like); the current function is discarded, so it does not return to reach `CATCH`.
- If the function does not exist: jumps to the `CATCH` marker (entering the catch body).
- Engine-extracted notes (base flags from class):
  - `flag = FLOW_CONTROL | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `state.JumpTo(func.JumpToEndCatch)`
  - `state.IntoFunction(call, arg, exm)`

**Errors & validation**
- Still errors for invalid argument binding/type conversion when a function is found.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.NotDefinedFunc.Text, labelName))`
  - `throw new CodeEE(errMes)`

**Examples**
- `TRYCJUMP OPTIONAL_PHASE`
- `CATCH`
- `  PRINTL "phase missing"`
- `ENDCATCH`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3607 (`CALL_Instruction`)

## TRYCCALL (instruction)
**Summary**
- Like `TRYCALL`, but supports a `CATCH ... ENDCATCH` block for the “not found” case.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new CALL_Instruction(false, false, true, true)`
- Additional flags (registration): `EXTENDED`
- Structural match end: `CATCH`

**Syntax**
- `TRYCCALL <functionName> [, <arg1>, ... ]`
- `CATCH`
  - `<catch body>`
  - `ENDCATCH`

**Arguments**
- Same as `CALL`.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- If the target function exists: behaves like `CALL`, then control returns and reaches `CATCH` sequentially; `CATCH` skips the catch body.
- If the function does not exist: jumps to the `CATCH` marker (so execution begins at the first line of the catch body).
- Engine-extracted notes (base flags from class):
  - `flag = FLOW_CONTROL | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `state.JumpTo(func.JumpToEndCatch)`
  - `state.IntoFunction(call, arg, exm)`

**Errors & validation**
- Still errors for invalid argument binding/type conversion when a function is found.
- Mis-nesting (`CATCH` without `TRYC*`, `ENDCATCH` without `CATCH`) is a load-time error (the line is marked as error).
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.NotDefinedFunc.Text, labelName))`
  - `throw new CodeEE(errMes)`

**Examples**
- `TRYCCALL OPTIONAL_HOOK`
- `CATCH`
- `  PRINTL "hook missing"`
- `ENDCATCH`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3607 (`CALL_Instruction`)

## TRYCJUMPFORM (instruction)
**Summary**
- Like `TRYJUMPFORM`, but supports a `CATCH ... ENDCATCH` block for the “not found” case.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new CALL_Instruction(true, true, true, true)`
- Additional flags (registration): `EXTENDED`
- Structural match end: `CATCH`

**Syntax**
- `TRYCJUMPFORM <formString> [, <arg1>, ... ]`
- `CATCH`
  - `<catch body>`
  - `ENDCATCH`

**Arguments**
- Same as `JUMPFORM`.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Same as `TRYCJUMP`, but with a runtime-evaluated function name.
- Engine-extracted notes (base flags from class):
  - `flag = FLOW_CONTROL | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `state.JumpTo(func.JumpToEndCatch)`
  - `state.IntoFunction(call, arg, exm)`

**Errors & validation**
- Same as `TRYCJUMP`.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.NotDefinedFunc.Text, labelName))`
  - `throw new CodeEE(errMes)`

**Examples**
- `TRYCJUMPFORM "OPTIONAL_%COUNT%"`
- `CATCH`
- `  PRINTL "missing"`
- `ENDCATCH`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3607 (`CALL_Instruction`)

## TRYCCALLFORM (instruction)
**Summary**
- Like `TRYCALLFORM`, but supports a `CATCH ... ENDCATCH` block for the “not found” case.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new CALL_Instruction(true, false, true, true)`
- Additional flags (registration): `EXTENDED`
- Structural match end: `CATCH`

**Syntax**
- `TRYCCALLFORM <formString> [, <arg1>, ... ]`
- `CATCH`
  - `<catch body>`
  - `ENDCATCH`

**Arguments**
- Same as `CALLFORM`.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Same as `TRYCCALL`, but with a runtime-evaluated function name.
- Engine-extracted notes (base flags from class):
  - `flag = FLOW_CONTROL | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `state.JumpTo(func.JumpToEndCatch)`
  - `state.IntoFunction(call, arg, exm)`

**Errors & validation**
- Same as `TRYCCALL`.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.NotDefinedFunc.Text, labelName))`
  - `throw new CodeEE(errMes)`

**Examples**
- `TRYCCALLFORM "HOOK_%TARGET%"`
- `CATCH`
- `  PRINTL "hook missing"`
- `ENDCATCH`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3607 (`CALL_Instruction`)

## CALLEVENT (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `STR` (see #argument-spec-str) (inferred from `CALLEVENT_Instruction` ArgBuilder assignment)
- Implementor (registration): `new CALLEVENT_Instruction()`

**Syntax**
- Hint (translated, best-effort): raw string
- Hint (raw comment): `単純文字列型`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `STR_ArgumentBuilder(false)`

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = FLOW_CONTROL | EXTENDED`
- Engine-extracted notes (key operations):
  - `state.IntoFunction(call, null, null)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.STR`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3702 (`CALLEVENT_Instruction`)

## CALLF (instruction)
**Summary**
- Calls an expression function (built-in method or user-defined `#FUNCTION/#FUNCTIONS`) by name and evaluates it as a statement.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new CALLF_Instruction(false)`

**Syntax**
- `CALLF <methodName> [, <arg1>, <arg2>, ... ]`
- `CALLF <methodName>(<arg1>, <arg2>, ... )`

**Arguments**
- `<methodName>`: a raw string token read up to `(` / `[` / `,` / `;` and then trimmed.
- `<argN>`: expressions passed to the method.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Resolves `<methodName>` to an expression function and evaluates it with the provided arguments.
- The return value is computed but not assigned to `RESULT/RESULTS` by this instruction (use statement-form method calls or assignment if you need the value).
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED | METHOD_SAFE | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `if ((!func.Argument.IsConst) || exm.Console.RunERBFromMemory)`

**Errors & validation**
- If `<methodName>` is a constant string: unknown methods are a load-time error (the line is marked as error).
- Errors if the method exists but argument checking fails.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.NotDefinedUserFunc.Text, labelName))`

**Examples**
- `CALLF MYFUNC, 1, 2`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1152 (`CALLF_Instruction`)

## CALLFORMF (instruction)
**Summary**
- Like `CALLF`, but the method name is a formatted (FORM) string expression evaluated at runtime.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new CALLF_Instruction(true)`

**Syntax**
- `CALLFORMF <formString> [, <arg1>, <arg2>, ... ]`
- `CALLFORMF <formString>(<arg1>, <arg2>, ... )`

**Arguments**
- `<formString>`: FORM/formatted string; the evaluated result is used as the method name.
- `<argN>`: expressions passed to the method.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Resolves the evaluated name to an expression function and evaluates it.
- The return value is computed but not assigned to `RESULT/RESULTS` by this instruction.
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED | METHOD_SAFE | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `if ((!func.Argument.IsConst) || exm.Console.RunERBFromMemory)`

**Errors & validation**
- Errors if the method does not exist or if argument checking fails.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.NotDefinedUserFunc.Text, labelName))`

**Examples**
- `CALLFORMF "FUNC_%X%", A, B`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1152 (`CALLF_Instruction`)

## CALLSHARP (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `SP_CALLCSHARP` (see #argument-spec-sp_callcsharp) (inferred from `CALLSHARP_Instruction` ArgBuilder assignment)
- Implementor (registration): `new CALLSHARP_Instruction()`

**Syntax**
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `SP_CALLSHARP_ArgumentBuilder()`

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED | METHOD_SAFE | FORCE_SETARG`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_CALLCSHARP`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1211 (`CALLSHARP_Instruction`)

## RESTART (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `RESTART_Instruction` ArgBuilder assignment)
- Implementor (registration): `new RESTART_Instruction()`

**Syntax**
- Hint (translated, best-effort): no arguments
- Hint (raw comment): `引数なし`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `VOID_ArgumentBuilder()`

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | FLOW_CONTROL | EXTENDED`
- Engine-extracted notes (key operations):
  - `state.JumpTo(func.ParentLabelLine)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3411 (`RESTART_Instruction`)

## GOTO (instruction)
**Summary**
- Jumps to a local `$label` within the current function.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new GOTO_Instruction(false, false, false)`

**Syntax**
- `GOTO <labelName>`

**Arguments**
- `<labelName>`: a raw string token; used to resolve a `$label` relative to the current function.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- If the label exists, jumps to the `$label` marker; execution continues at the line after the `$label`.
- Compatibility parsing: after `<labelName>`, the engine also accepts an optional “call-like tail”:
  - `GOTO <labelName>(...)`
  - `GOTO <labelName>, ...`
  - These extra parts are parsed for compatibility but ignored by `GOTO`:
    - Only `<labelName>` is used to resolve the `$label`.
    - The ignored expressions are not evaluated and have no side effects (they only need to be syntactically valid).
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | FLOW_CONTROL | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `jumpto = state.CurrentCalled.CallLabel(GlobalStatic.Process, label)`
  - `state.JumpTo(func.JumpToEndCatch)`
  - `state.JumpTo(jumpto)`

**Errors & validation**
- If the label name is a constant string and the label is missing:
  - Non-`TRY*` variants: load-time error (the line is marked as error).
  - `TRY*` variants: allowed; the instruction becomes a no-op at runtime.
- If the label name is computed at runtime (e.g. `GOTOFORM`) and the label is missing:
  - Non-`TRY*` variants: runtime error.
  - `TRY*` variants: no-op (or enters `CATCH` for `TRYC*` variants).
- Invalid label definitions are errors even for `TRY*` variants.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.NotDefinedLabelName.Text, label))`
  - `throw new CodeEE(string.Format(trerror.InvalidLabelName.Text, label))`

**Examples**
- `GOTO LOOP_START`
- `GOTO LOOP_START(1, 2)` (equivalent to `GOTO LOOP_START`)
- `GOTO LOOP_START, 1, 2` (equivalent to `GOTO LOOP_START`)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3730 (`GOTO_Instruction`)

## TRYGOTO (instruction)
**Summary**
- Like `GOTO`, but if the target `$label` does not exist the instruction **does not error** and simply falls through.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new GOTO_Instruction(false, true, false)`
- Additional flags (registration): `EXTENDED`

**Syntax**
- `TRYGOTO <labelName>`

**Arguments**
- Same as `GOTO`.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- If the `$label` exists: behaves like `GOTO`.
- If not: does nothing (continues at the next line after `TRYGOTO`).
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | FLOW_CONTROL | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `jumpto = state.CurrentCalled.CallLabel(GlobalStatic.Process, label)`
  - `state.JumpTo(func.JumpToEndCatch)`
  - `state.JumpTo(jumpto)`

**Errors & validation**
- Still errors if the label exists but is invalid.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.NotDefinedLabelName.Text, label))`
  - `throw new CodeEE(string.Format(trerror.InvalidLabelName.Text, label))`

**Examples**
- `TRYGOTO OPTIONAL_LABEL`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3730 (`GOTO_Instruction`)

## GOTOFORM (instruction)
**Summary**
- Like `GOTO`, but the label name is a formatted (FORM) string expression evaluated at runtime.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new GOTO_Instruction(true, false, false)`
- Additional flags (registration): `EXTENDED`

**Syntax**
- `GOTOFORM <formString>`

**Arguments**
- `<formString>`: FORM/formatted string; the evaluated result is used as the `$label` name.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Evaluates the label name and jumps if it resolves to a `$label` in the current function.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | FLOW_CONTROL | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `jumpto = state.CurrentCalled.CallLabel(GlobalStatic.Process, label)`
  - `state.JumpTo(func.JumpToEndCatch)`
  - `state.JumpTo(jumpto)`

**Errors & validation**
- Same as `GOTO`, but errors may occur at runtime if the evaluated label name varies.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.NotDefinedLabelName.Text, label))`
  - `throw new CodeEE(string.Format(trerror.InvalidLabelName.Text, label))`

**Examples**
- `GOTOFORM "CASE_%RESULT%"`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3730 (`GOTO_Instruction`)

## TRYGOTOFORM (instruction)
**Summary**
- Like `GOTOFORM`, but if the evaluated `$label` name does not exist the instruction **does not error** and simply falls through.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new GOTO_Instruction(true, true, false)`
- Additional flags (registration): `EXTENDED`

**Syntax**
- `TRYGOTOFORM <formString>`

**Arguments**
- Same as `GOTOFORM`.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- If the `$label` exists: behaves like `GOTOFORM`.
- If not: does nothing (continues at the next line after `TRYGOTOFORM`).
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | FLOW_CONTROL | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `jumpto = state.CurrentCalled.CallLabel(GlobalStatic.Process, label)`
  - `state.JumpTo(func.JumpToEndCatch)`
  - `state.JumpTo(jumpto)`

**Errors & validation**
- Still errors if the label exists but is invalid.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.NotDefinedLabelName.Text, label))`
  - `throw new CodeEE(string.Format(trerror.InvalidLabelName.Text, label))`

**Examples**
- `TRYGOTOFORM "LABEL_%RESULT%"`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3730 (`GOTO_Instruction`)

## TRYCGOTO (instruction)
**Summary**
- Like `TRYGOTO`, but supports a `CATCH ... ENDCATCH` block for the “not found” case.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new GOTO_Instruction(false, true, true)`
- Additional flags (registration): `EXTENDED`
- Structural match end: `CATCH`

**Syntax**
- `TRYCGOTO <labelName>`
- `CATCH`
  - `<catch body>`
  - `ENDCATCH`

**Arguments**
- Same as `GOTO`.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- If the `$label` exists: behaves like `GOTO` (jumps to the label). Whether the `CATCH` line is ever reached depends on subsequent control flow.
- If the `$label` does not exist: jumps to the `CATCH` marker (entering the catch body).
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | FLOW_CONTROL | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `jumpto = state.CurrentCalled.CallLabel(GlobalStatic.Process, label)`
  - `state.JumpTo(func.JumpToEndCatch)`
  - `state.JumpTo(jumpto)`

**Errors & validation**
- Mis-nesting (`CATCH` without `TRYC*`, `ENDCATCH` without `CATCH`) is a load-time error (the line is marked as error).
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.NotDefinedLabelName.Text, label))`
  - `throw new CodeEE(string.Format(trerror.InvalidLabelName.Text, label))`

**Examples**
- `TRYCGOTO OPTIONAL_LABEL`
- `CATCH`
- `  PRINTL "label missing"`
- `ENDCATCH`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3730 (`GOTO_Instruction`)

## TRYCGOTOFORM (instruction)
**Summary**
- Like `TRYGOTOFORM`, but supports a `CATCH ... ENDCATCH` block for the “not found” case.

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new GOTO_Instruction(true, true, true)`
- Additional flags (registration): `EXTENDED`
- Structural match end: `CATCH`

**Syntax**
- `TRYCGOTOFORM <formString>`
- `CATCH`
  - `<catch body>`
  - `ENDCATCH`

**Arguments**
- Same as `GOTOFORM`.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Same as `TRYCGOTO`, but with a runtime-evaluated label name.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | FLOW_CONTROL | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `jumpto = state.CurrentCalled.CallLabel(GlobalStatic.Process, label)`
  - `state.JumpTo(func.JumpToEndCatch)`
  - `state.JumpTo(jumpto)`

**Errors & validation**
- Same as `TRYCGOTO`.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.NotDefinedLabelName.Text, label))`
  - `throw new CodeEE(string.Format(trerror.InvalidLabelName.Text, label))`

**Examples**
- `TRYCGOTOFORM "LABEL_%RESULT%"`
- `CATCH`
- `  PRINTL "label missing"`
- `ENDCATCH`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3730 (`GOTO_Instruction`)

## CATCH (instruction)
**Summary**
- Begins the catch-body of a `TRYC* ... CATCH ... ENDCATCH` construct.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `CATCH_Instruction` ArgBuilder assignment)
- Implementor (registration): `new CATCH_Instruction()`
- Structural match end: `ENDCATCH`

**Syntax**
- `CATCH`
  - `<catch body>`
  - `ENDCATCH`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- When reached **sequentially** (i.e. the `TRYC*` succeeded and returned normally), `CATCH` jumps to the matching `ENDCATCH` marker, skipping the catch body.
- When entered by a failed `TRYC*` instruction, execution jumps to the `CATCH` marker and (due to the engine’s advance-first model) begins executing at the first line of the catch body.
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED | FLOW_CONTROL | PARTIAL`
- Engine-extracted notes (key operations):
  - `state.JumpTo(func.JumpToEndCatch)`

**Errors & validation**
- `CATCH` without a matching open `TRYC*` is a load-time error (the line is marked as error).

**Examples**
- `CATCH`
- `  PRINTL "not found"`
- `ENDCATCH`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3397 (`CATCH_Instruction`)

## ENDCATCH (instruction)
**Summary**
- Ends a `CATCH ... ENDCATCH` block.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `ENDIF_Instruction` ArgBuilder assignment)
- Implementor (registration): `new ENDIF_Instruction()`
- Additional flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- `ENDCATCH`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Marker-only instruction (no runtime effect). The loader links it to the matching `CATCH` so that `CATCH` can skip the catch body on the success path.
- Engine-extracted notes (base flags from class):
  - `flag = FLOW_CONTROL | PARTIAL | FORCE_SETARG`

**Errors & validation**
- `ENDCATCH` without a matching open `CATCH` is a load-time error (the line is marked as error).

**Examples**
- `ENDCATCH`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3188 (`ENDIF_Instruction`)

## TRYCALLLIST (instruction)
**Summary**
- Tries a list of candidate non-event functions and `CALL`s the first one that exists; otherwise skips the block.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void)
- Flags (registration): `EXTENDED`, `FLOW_CONTROL`, `PARTIAL`, `IS_TRY`
- Structural match end: `ENDFUNC`

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
- Optional/default behavior is builder-specific; see engine refs.

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
- Engine-extracted notes (key operations):
  - `state.IntoFunction(callto, args, exm)`
  - `state.JumpTo(func.JumpTo)`

**Errors & validation**
- Load-time structure errors (the line is marked as error):
  - `TRYCALLLIST` cannot be nested inside another `TRY*LIST` block.
  - Only `FUNC` and `ENDFUNC` are allowed between `TRYCALLLIST` and `ENDFUNC`; any other instruction (and any label definition) is an error.
  - `FUNC`/`ENDFUNC` outside a matching `TRY*LIST ... ENDFUNC` block is an error.
- Runtime errors:
  - If a candidate name resolves to an event function (and `CompatiCallEvent` is not applicable here), it errors rather than trying the next item.
  - If a candidate function exists but is a user-defined expression function (`#FUNCTION/#FUNCTIONS`), it errors.
  - If argument binding fails (too many args, omitted required args, type conversion not permitted, invalid `REF` binding, etc.), it errors (it does **not** “try the next one”).
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(errMes)`

**Examples**
- `TRYCALLLIST`
- `  FUNC HOOK_%TARGET%, TARGET`
- `  FUNC HOOK_DEFAULT`
- `ENDFUNC`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:830 (case `TRYCALLLIST`)

## TRYJUMPLIST (instruction)
**Summary**
- Like `TRYCALLLIST`, but performs a `JUMP` into the first existing candidate.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void)
- Flags (registration): `EXTENDED`, `FLOW_CONTROL`, `PARTIAL`, `IS_JUMP`, `IS_TRY`
- Structural match end: `ENDFUNC`

**Syntax**
- `TRYJUMPLIST`
  - `FUNC <formString> [, <arg1>, ... ]`
  - `...`
  - `ENDFUNC`

**Arguments**
- Same as `TRYCALLLIST`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Same selection rules as `TRYCALLLIST`.
- If a candidate function is found:
  - Enters it as a `JUMP` (tail-call behavior): when the callee returns, the current function also returns (the engine unwinds the call stack until a non-`JUMP` frame).
  - As a consequence, control does **not** return to the `ENDFUNC` line on success.
- If no candidate is found, jumps to the `ENDFUNC` line (then continues after it).
- Engine-extracted notes (key operations):
  - `state.IntoFunction(callto, args, exm)`
  - `state.JumpTo(func.JumpTo)`

**Errors & validation**
- Same as `TRYCALLLIST`.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(errMes)`

**Examples**
- `TRYJUMPLIST`
- `  FUNC PHASE_%COUNT%`
- `  FUNC PHASE_DEFAULT`
- `ENDFUNC`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:831 (case `TRYJUMPLIST`)

## TRYGOTOLIST (instruction)
**Summary**
- Tries a list of candidate `$label` targets and jumps to the first one that exists; otherwise jumps to `ENDFUNC` (end of the list).

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void)
- Flags (registration): `EXTENDED`, `FLOW_CONTROL`, `PARTIAL`, `IS_TRY`
- Structural match end: `ENDFUNC`

**Syntax**
- `TRYGOTOLIST`
  - `FUNC <formString>`
  - `FUNC <formString>`
  - `...`
  - `ENDFUNC`

**Arguments**
- Each `FUNC` item provides a label name as a **FORM/formatted string expression** (evaluated to a string at runtime).

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Structural notes:
  - The lines between `TRYGOTOLIST` and `ENDFUNC` are list items, not a normal executable block body (same model as `TRYCALLLIST`).
- Runtime algorithm:
  - For each `FUNC` item in source order:
    - Evaluate the candidate name to a string.
    - Resolve it as a `$label` inside the **current function**.
    - If it exists, jump to it and stop searching.
  - If no candidate exists, jump to the `ENDFUNC` line (then continue after it).
- Engine-extracted notes (key operations):
  - `jumpto = state.CurrentCalled.CallLabel(this, funcName)`
  - `state.JumpTo(func.JumpTo)`
  - `state.JumpTo(jumpto)`

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

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:859 (case `TRYGOTOLIST`)

## FUNC (instruction)
**Summary**
- List-item line inside `TRYCALLLIST` / `TRYJUMPLIST` / `TRYGOTOLIST` blocks.

**Metadata**
- Arg spec: `SP_CALLFORM` (see #argument-spec-sp_callform)
- Flags (registration): `EXTENDED`, `FLOW_CONTROL`, `PARTIAL`, `FORCE_SETARG`

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
- Optional/default behavior is builder-specific; see engine refs.

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

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_CALLFORM`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`

## ENDFUNC (instruction)
**Summary**
- Ends a `TRY*LIST ... ENDFUNC` block.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `ENDIF_Instruction` ArgBuilder assignment)
- Implementor (registration): `new ENDIF_Instruction()`
- Additional flags (registration): `EXTENDED`

**Syntax**
- `ENDFUNC`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Marker-only instruction (no runtime effect). The surrounding `TRY*LIST` uses it as the jump target when no candidate succeeds.
- Engine-extracted notes (base flags from class):
  - `flag = FLOW_CONTROL | PARTIAL | FORCE_SETARG`

**Errors & validation**
- `ENDFUNC` without a matching open `TRY*LIST` is a load-time error (the line is marked as error).

**Examples**
- `ENDFUNC`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3188 (`ENDIF_Instruction`)

## DEBUGPRINT (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new DEBUGPRINT_Instruction(false, false)`

**Syntax**
- (TODO)

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED | DEBUG_FUNC`
- Engine-extracted notes (key operations):
  - `exm.Console.DebugPrint(str)`
  - `exm.Console.DebugNewLine()`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:540 (`DEBUGPRINT_Instruction`)

## DEBUGPRINTL (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new DEBUGPRINT_Instruction(false, true)`

**Syntax**
- (TODO)

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED | DEBUG_FUNC`
- Engine-extracted notes (key operations):
  - `exm.Console.DebugPrint(str)`
  - `exm.Console.DebugNewLine()`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:540 (`DEBUGPRINT_Instruction`)

## DEBUGPRINTFORM (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new DEBUGPRINT_Instruction(true, false)`

**Syntax**
- (TODO)

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED | DEBUG_FUNC`
- Engine-extracted notes (key operations):
  - `exm.Console.DebugPrint(str)`
  - `exm.Console.DebugNewLine()`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:540 (`DEBUGPRINT_Instruction`)

## DEBUGPRINTFORML (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new DEBUGPRINT_Instruction(true, true)`

**Syntax**
- (TODO)

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED | DEBUG_FUNC`
- Engine-extracted notes (key operations):
  - `exm.Console.DebugPrint(str)`
  - `exm.Console.DebugNewLine()`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:540 (`DEBUGPRINT_Instruction`)

## DEBUGCLEAR (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `DEBUGCLEAR_Instruction` ArgBuilder assignment)
- Implementor (registration): `new DEBUGCLEAR_Instruction()`

**Syntax**
- Hint (translated, best-effort): no arguments
- Hint (raw comment): `引数なし`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `VOID_ArgumentBuilder()`

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED | DEBUG_FUNC`
- Engine-extracted notes (key operations):
  - `exm.Console.DebugClear()`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:565 (`DEBUGCLEAR_Instruction`)

## ASSERT (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `INT_EXPRESSION` (see #argument-spec-int_expression)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`, `DEBUG_FUNC`

**Syntax**
- Hint (translated, best-effort): int expression。optional
- Hint (raw comment): `数式型。省略可能`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `INT_EXPRESSION_ArgumentBuilder(false)`
- Type pattern: `[typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.AssertArgIs0.Text)`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:747 (case `ASSERT`)

## THROW (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `FORM_STR_NULLABLE` (see #argument-spec-form_str_nullable)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- Hint (translated, best-effort): FORM string型。optional
- Hint (raw comment): `書式付文字列型。省略可能`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `FORM_STR_ArgumentBuilder(true)`

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(((ExpressionArgument)func.Argument).Term.GetStrValue(exm))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.FORM_STR_NULLABLE`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:751 (case `THROW`)

## SAVEVAR (instruction)
**Summary**
- Declared but **not implemented** in this engine build (always errors).

**Metadata**
- Arg spec: `SP_SAVEVAR` (see #argument-spec-sp_savevar) (inferred from `SAVEVAR_Instruction` ArgBuilder assignment)
- Implementor (registration): `new SAVEVAR_Instruction()`

**Syntax**
- `SAVEVAR <name>, <saveText>, <var1> [, <var2> ...]`

**Arguments**
- `<name>` (string): intended file name component.
- `<saveText>` (string): intended description text.
- `<var*>`: one or more changeable non-character variable terms (arrays are allowed; several variable categories are rejected).

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- The current engine implementation throws a “not implemented” error at runtime.
- See also: `save-files.md` (directories, partitions, and on-disk formats)
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`

**Errors & validation**
- Always errors at runtime.
- Engine-extracted notes (throws/errors):
  - `throw new NotImplCodeEE()`

**Examples**
- `SAVEVAR "vars", "checkpoint", A, B, C`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_SAVEVAR`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1955 (`SAVEVAR_Instruction`)

## LOADVAR (instruction)
**Summary**
- Declared but **not implemented** in this engine build (always errors).

**Metadata**
- Arg spec: `STR_EXPRESSION` (see #argument-spec-str_expression) (inferred from `LOADVAR_Instruction` ArgBuilder assignment)
- Implementor (registration): `new LOADVAR_Instruction()`

**Syntax**
- `LOADVAR <name>`

**Arguments**
- `<name>` (string): intended file name component.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- The current engine implementation throws a “not implemented” error at runtime.
- See also: `save-files.md` (directories, partitions, and on-disk formats)
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`

**Errors & validation**
- Always errors at runtime.
- Engine-extracted notes (throws/errors):
  - `throw new NotImplCodeEE()`

**Examples**
- `LOADVAR "vars"`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.STR_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1973 (`LOADVAR_Instruction`)

## SAVECHARA (instruction)
**Summary**
- Saves one or more characters into a `dat/chara_<name>.dat` file (binary only).

**Metadata**
- Arg spec: `SP_SAVECHARA` (see #argument-spec-sp_savechara) (inferred from `SAVECHARA_Instruction` ArgBuilder assignment)
- Implementor (registration): `new SAVECHARA_Instruction()`

**Syntax**
- `SAVECHARA <name>, <saveText>, <charaNo1> [, <charaNo2> ...]`

**Arguments**
- `<name>` (string): the file name component.
- `<saveText>` (string): stored in the file as a description.
- `<charaNo*>`: one or more integer expressions; character indices to save (0-based).

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

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
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `int charanum = (int)exm.VEvaluator.CHARANUM`
  - `exm.VEvaluator.SaveChara(datFilename, savMes, savCharaList)`

**Errors & validation**
- Argument parsing requires at least 3 arguments.
- Errors if any character index is negative, too large, out of range, or duplicated.
- File name validity is ultimately enforced by the OS; invalid names can cause runtime errors.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.OoRSavecharaArg.Text, (i + 3).ToString()))`
  - `throw new CodeEE(string.Format(trerror.DuplicateCharaNo.Text, savCharaList[i].ToString()))`

**Examples**
- `SAVECHARA "party", "Before boss", MASTER, TARGET`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_SAVECHARA`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1902 (`SAVECHARA_Instruction`)

## LOADCHARA (instruction)
**Summary**
- Loads characters from `dat/chara_<name>.dat` and appends them to the current character list.

**Metadata**
- Arg spec: `STR_EXPRESSION` (see #argument-spec-str_expression) (inferred from `LOADCHARA_Instruction` ArgBuilder assignment)
- Implementor (registration): `new LOADCHARA_Instruction()`

**Syntax**
- `LOADCHARA <name>`

**Arguments**
- `<name>` (string): the file name component.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Reads `Program.DatDir/chara_<name>.dat`.
- If the file exists and passes validation (file type, unique code, version):
  - Deserializes the characters and appends them to the current character list.
  - Sets `RESULT = 1`.
- Otherwise:
  - Does nothing and sets `RESULT = 0`.
- See also: `save-files.md` (directories, partitions, and on-disk formats)
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.VEvaluator.LoadChara(datFilename)`

**Errors & validation**
- No explicit errors are raised for “file not found” / “invalid file”; failures are reported via `RESULT`.

**Examples**
- `LOADCHARA "party"`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.STR_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1934 (`LOADCHARA_Instruction`)

## REF (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new REF_Instruction(false)`

**Syntax**
- (TODO)

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.VEvaluator.RESULT = 0`
  - `exm.VEvaluator.RESULT = 1`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new NotImplCodeEE()`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:2031 (`REF_Instruction`)

## REFBYNAME (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new REF_Instruction(true)`

**Syntax**
- (TODO)

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.VEvaluator.RESULT = 0`
  - `exm.VEvaluator.RESULT = 1`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new NotImplCodeEE()`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:2031 (`REF_Instruction`)

## HTML_PRINT (instruction)
**Summary**
- Prints an HTML string (Emuera’s HTML-like mini language) as console output.

**Metadata**
- Arg spec: `SP_HTML_PRINT` (see #argument-spec-sp_html_print) (inferred from `HTML_PRINT_Instruction` ArgBuilder assignment)
- Implementor (registration): `new HTML_PRINT_Instruction()`

**Syntax**
- `HTML_PRINT <html> [, <toBuffer>]`

**Arguments**
- `<html>` (string): HTML string (see `html-output.md`).
- `<toBuffer>` (optional, int; default `0`)
  - `0` (default): print as a complete logical output line (implicit line end).
  - non-zero: append the HTML output into the current print buffer (no implicit line end).

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

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
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED | METHOD_SAFE`
- Engine-extracted notes (key operations):
  - `if (arg.IsConst) exm.Console.PrintHtml(arg.ConstStr, arg.ConstInt != 0)`
  - `else exm.Console.PrintHtml(arg.Str.GetStrValue(exm), arg.Opt == null ? false : arg.Opt.GetIntValue(exm) != 0)`

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

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_HTML_PRINT`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:311 (`HTML_PRINT_Instruction`)

## HTML_TAGSPLIT (instruction)
**Summary**
- Splits an HTML string into a sequence of raw tags and raw text segments.

**Metadata**
- Arg spec: `SP_HTMLSPLIT` (see #argument-spec-sp_htmlsplit) (inferred from `HTML_TAGSPLIT_Instruction` ArgBuilder assignment)
- Implementor (registration): `new HTML_TAGSPLIT_Instruction()`

**Syntax**
- `HTML_TAGSPLIT <html> [, <outParts> [, <outCount>]]`

**Arguments**
- `<html>` (string): HTML string.
- `<outParts>` (optional; default `RESULTS`): changeable 1D **non-character** string array variable to receive parts.
- `<outCount>` (optional; default `RESULT`): changeable integer variable to receive the part count.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

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
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED | METHOD_SAFE`

**Errors & validation**
- Argument type/count errors follow the normal expression argument rules.

**Examples**
```erabasic
HTML_TAGSPLIT "<p align='right'>A<!--c-->B</p>"
PRINTFORML RESULT = {RESULT}
PRINTFORML RESULTS:0 = %RESULTS:0%
PRINTFORML RESULTS:1 = %RESULTS:1%
```

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_HTMLSPLIT`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:338 (`HTML_TAGSPLIT_Instruction`)

## PRINT_IMG (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `SP_PRINT_IMG` (see #argument-spec-sp_print_img) (inferred from `PRINT_IMG_Instruction` ArgBuilder assignment)
- Implementor (registration): `new PRINT_IMG_Instruction()`

**Syntax**
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `SP_PRINT_IMG_ArgumentBuilder()`
- Type pattern: `null;// new Type[] { typeof(string), typeof(string), typeof(Int64), typeof(Int64), typeof(Int64) }` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `1`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED | METHOD_SAFE`
- Engine-extracted notes (key operations):
  - `exm.Console.PrintImg(`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.InvalidArg.Text)`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_PRINT_IMG`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:401 (`PRINT_IMG_Instruction`)

## PRINT_RECT (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `SP_PRINT_RECT` (see #argument-spec-sp_print_rect) (inferred from `PRINT_RECT_Instruction` ArgBuilder assignment)
- Implementor (registration): `new PRINT_RECT_Instruction()`

**Syntax**
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `SP_PRINT_SHAPE_ArgumentBuilder(4)`
- Type pattern: `[typeof(long), typeof(long), typeof(long), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `1`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED | METHOD_SAFE`
- Engine-extracted notes (key operations):
  - `exm.Console.PrintShape("rect", param)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.InvalidArg.Text)`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_PRINT_RECT`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:440 (`PRINT_RECT_Instruction`)

## PRINT_SPACE (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `SP_PRINT_SPACE` (see #argument-spec-sp_print_space) (inferred from `PRINT_SPACE_Instruction` ArgBuilder assignment)
- Implementor (registration): `new PRINT_SPACE_Instruction()`

**Syntax**
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `SP_PRINT_SHAPE_ArgumentBuilder(1)`
- Type pattern: `[typeof(long), typeof(long), typeof(long), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `1`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED | METHOD_SAFE`
- Engine-extracted notes (key operations):
  - `exm.Console.PrintShape("space", param)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.InvalidArg.Text)`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_PRINT_SPACE`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:473 (`PRINT_SPACE_Instruction`)

## TOOLTIP_SETCOLOR (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `SP_SWAP` (see #argument-spec-sp_swap) (inferred from `TOOLTIP_SETCOLOR_Instruction` ArgBuilder assignment)
- Implementor (registration): `new TOOLTIP_SETCOLOR_Instruction()`

**Syntax**
- Hint (translated, best-effort): <int>,<int>
- Hint (raw comment): `<数値>,<数値>`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `SP_SWAP_ArgumentBuilder(false)`
- Type pattern: `[typeof(long), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `1`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.Console.SetToolTipColor(fc, bc)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.ArgIsOoRColorCode.Text, "1"))`
  - `throw new CodeEE(string.Format(trerror.ArgIsOoRColorCode.Text, "2"))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_SWAP`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:2112 (`TOOLTIP_SETCOLOR_Instruction`)

## TOOLTIP_SETDELAY (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `INT_EXPRESSION` (see #argument-spec-int_expression) (inferred from `TOOLTIP_SETDELAY_Instruction` ArgBuilder assignment)
- Implementor (registration): `new TOOLTIP_SETDELAY_Instruction()`

**Syntax**
- Hint (translated, best-effort): int expression。optional
- Hint (raw comment): `数式型。省略可能`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `INT_EXPRESSION_ArgumentBuilder(false)`
- Type pattern: `[typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.Console.SetToolTipDelay((int)delay)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.ArgIsOoR.Text)`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:2135 (`TOOLTIP_SETDELAY_Instruction`)

## TOOLTIP_SETDURATION (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `INT_EXPRESSION` (see #argument-spec-int_expression) (inferred from `TOOLTIP_SETDURATION_Instruction` ArgBuilder assignment)
- Implementor (registration): `new TOOLTIP_SETDURATION_Instruction()`

**Syntax**
- Hint (translated, best-effort): int expression。optional
- Hint (raw comment): `数式型。省略可能`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `INT_EXPRESSION_ArgumentBuilder(false)`
- Type pattern: `[typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.Console.SetToolTipDuration((int)duration)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.ArgIsOoR.Text)`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:2157 (`TOOLTIP_SETDURATION_Instruction`)

## INPUTMOUSEKEY (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new INPUTMOUSEKEY_Instruction()`

**Syntax**
- (TODO)

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.Console.WaitInput(req)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:2181 (`INPUTMOUSEKEY_Instruction`)

## AWAIT (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `EXPRESSION_NULLABLE` (see #argument-spec-expression_nullable) (inferred from `AWAIT_Instruction` ArgBuilder assignment)
- Implementor (registration): `new AWAIT_Instruction()`

**Syntax**
- Hint (translated, best-effort): <式>, variable type unconstrained
- Hint (raw comment): `<式>、変数の型は不問`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `EXPRESSION_ArgumentBuilder(true)`
- Type pattern: `[typeof(void)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.Console.Await((int)waittime)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.AwaitArgIsNegative.Text, waittime.ToString()))`
  - `throw new CodeEE(string.Format(trerror.AwaitArgIsOver10Seconds.Text, waittime.ToString()))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.EXPRESSION_NULLABLE`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:2661 (`AWAIT_Instruction`)

## VARSIZE (instruction)
**Summary**
- Writes the size of an array variable into `RESULT` / `RESULT:1` / `RESULT:2`.

**Metadata**
- Arg spec: `SP_VAR` (see #argument-spec-sp_var)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- `VARSIZE <arrayVarName>`

**Arguments**
- `<arrayVarName>`: an identifier token naming an array variable (not an expression).
  - Must be a 1D/2D/3D array variable (character-data arrays are allowed).
  - `RAND` is rejected (even though it is 1D).
  - Compatibility parsing: any extra characters after the identifier are ignored (with a warning). For example, `VARSIZE ABL:TARGET:0` is treated like `VARSIZE ABL`.
    - The ignored tail is not parsed as expressions and is not evaluated (so it has no side effects).

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Resolves `<arrayVarName>` to a variable token.
- Writes array lengths into `RESULT_ARRAY`:
  - 1D array: `RESULT = length0`
  - 2D array: `RESULT = length0`, `RESULT:1 = length1`
  - 3D array: `RESULT = length0`, `RESULT:1 = length1`, `RESULT:2 = length2`
- Does not clear other `RESULT:*` slots.
- Engine-extracted notes (key operations):
  - `vEvaluator.VarSize(varID)`

**Errors & validation**
- Errors if `<arrayVarName>` is missing, is not a variable identifier, is not an array variable, or is `RAND`.

**Examples**
- `VARSIZE ABL` (writes the `ABL` dimensions to `RESULT*`)
- `VARSIZE ITEM` (writes the `ITEM` length to `RESULT`)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_VAR`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:316 (case `VARSIZE`)

## GETTIME (instruction)
**Summary**
- Writes the current local date/time into `RESULT` (as a packed integer) and `RESULTS` (as a formatted string).

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- `GETTIME`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Reads the current local time (`DateTime.Now`) and assigns:
  - `RESULT`: an integer of the form `yyyymmddHHMMSSmmm` (milliseconds included).
  - `RESULTS`: a string of the form `yyyy/MM/dd HH:mm:ss` (no milliseconds).
- Does not print output.
- Engine-extracted notes (key operations):
  - `vEvaluator.RESULT = date;//17桁。2京くらい。`
  - `vEvaluator.RESULTS = DateTime.Now.ToString("yyyy/MM/dd HH:mm:ss")`

**Errors & validation**
- None.

**Examples**
- `GETTIME`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:383 (case `GETTIME`)

## POWER (instruction)
**Summary**
- Computes an integer power using `Math.Pow` and stores the result into a destination integer variable.

**Metadata**
- Arg spec: `SP_POWER` (see #argument-spec-sp_power)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- `POWER <dest>, <x>, <y>`

**Arguments**
- `<dest>`: changeable integer variable term (destination).
- `<x>` (int): base.
- `<y>` (int): exponent.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

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
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.PowerResultNonNumeric.Text)`
  - `throw new CodeEE(trerror.PowerResultInfinite.Text)`
  - `throw new CodeEE(string.Format(trerror.PowerResultOverflow.Text, pow.ToString()))`

**Examples**
- `POWER A, 2, 10` (sets `A` to `1024`)
- `POWER A, 2, -1` (sets `A` to `0` due to truncation of `0.5`)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_POWER`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:341 (case `POWER`)

## PRINTCPERLINE (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `SP_GETINT` (see #argument-spec-sp_getint)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- Hint (translated, best-effort): <changeable int variable term>(今までこれがないことに驚いた)
- Hint (raw comment): `<可変数値変数>(今までこれがないことに驚いた)`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `SP_GETINT_ArgumentBuilder()`
- Type pattern: `[typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_GETINT`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:554 (case `PRINTCPERLINE`)

## SAVENOS (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `SP_GETINT` (see #argument-spec-sp_getint)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- Hint (translated, best-effort): <changeable int variable term>(今までこれがないことに驚いた)
- Hint (raw comment): `<可変数値変数>(今までこれがないことに驚いた)`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `SP_GETINT_ArgumentBuilder()`
- Type pattern: `[typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_GETINT`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:560 (case `SAVENOS`)

## ENCODETOUNI (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `FORM_STR_NULLABLE` (see #argument-spec-form_str_nullable)
- Flags (registration): `METHOD_SAFE`, `EXTENDED`

**Syntax**
- Hint (translated, best-effort): FORM string型。optional
- Hint (raw comment): `書式付文字列型。省略可能`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `FORM_STR_ArgumentBuilder(true)`

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (key operations):
  - `int length = vEvaluator.RESULT_ARRAY.Length`
  - `vEvaluator.SetEncodingResult(ary)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.tooLongEncodetouniArg.Text, target.Length, length - 1))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.FORM_STR_NULLABLE`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:727 (case `ENCODETOUNI`)

## PLAYSOUND (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `SP_HTML_PRINT` (see #argument-spec-sp_html_print) (inferred from `PLAYSOUND_Instruction` ArgBuilder assignment)
- Implementor (registration): `new PLAYSOUND_Instruction()`

**Syntax**
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `SP_HTML_PRINT_ArgumentBuilder()`
- Type pattern: `null;// new Type[] { typeof(string), typeof(string), typeof(Int64), typeof(Int64), typeof(Int64) }` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.ImcompatibleSoundFile.Text)`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_HTML_PRINT`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:2691 (`PLAYSOUND_Instruction`)

## STOPSOUND (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `STOPSOUND_Instruction` ArgBuilder assignment)
- Implementor (registration): `new STOPSOUND_Instruction()`

**Syntax**
- Hint (translated, best-effort): no arguments
- Hint (raw comment): `引数なし`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `VOID_ArgumentBuilder()`

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:2736 (`STOPSOUND_Instruction`)

## PLAYBGM (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `STR_EXPRESSION` (see #argument-spec-str_expression) (inferred from `PLAYBGM_Instruction` ArgBuilder assignment)
- Implementor (registration): `new PLAYBGM_Instruction()`

**Syntax**
- Hint (translated, best-effort): string expression
- Hint (raw comment): `文字列式型`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `STR_EXPRESSION_ArgumentBuilder(false)`
- Type pattern: `[typeof(string)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.ImcompatibleSoundFile.Text)`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.STR_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:2755 (`PLAYBGM_Instruction`)

## STOPBGM (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `STOPBGM_Instruction` ArgBuilder assignment)
- Implementor (registration): `new STOPBGM_Instruction()`

**Syntax**
- Hint (translated, best-effort): no arguments
- Hint (raw comment): `引数なし`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `VOID_ArgumentBuilder()`

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:2785 (`STOPBGM_Instruction`)

## SETSOUNDVOLUME (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `INT_EXPRESSION` (see #argument-spec-int_expression) (inferred from `SETSOUNDVOLUME_Instruction` ArgBuilder assignment)
- Implementor (registration): `new SETSOUNDVOLUME_Instruction()`

**Syntax**
- Hint (translated, best-effort): int expression。optional
- Hint (raw comment): `数式型。省略可能`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `INT_EXPRESSION_ArgumentBuilder(false)`
- Type pattern: `[typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:2798 (`SETSOUNDVOLUME_Instruction`)

## SETBGMVOLUME (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `INT_EXPRESSION` (see #argument-spec-int_expression) (inferred from `SETBGMVOLUME_Instruction` ArgBuilder assignment)
- Implementor (registration): `new SETBGMVOLUME_Instruction()`

**Syntax**
- Hint (translated, best-effort): int expression。optional
- Hint (raw comment): `数式型。省略可能`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `INT_EXPRESSION_ArgumentBuilder(false)`
- Type pattern: `[typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:2817 (`SETBGMVOLUME_Instruction`)

## TRYCALLF (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new TRYCALLF_Instruction(false)`

**Syntax**
- (TODO)

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED | METHOD_SAFE | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `if ((!func.Argument.IsConst) || exm.Console.RunERBFromMemory)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1283 (`TRYCALLF_Instruction`)

## TRYCALLFORMF (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new TRYCALLF_Instruction(true)`

**Syntax**
- (TODO)

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED | METHOD_SAFE | FORCE_SETARG`
- Engine-extracted notes (key operations):
  - `if ((!func.Argument.IsConst) || exm.Console.RunERBFromMemory)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:1283 (`TRYCALLF_Instruction`)

## UPDATECHECK (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `UPDATECHECK_Instruction` ArgBuilder assignment)
- Implementor (registration): `new UPDATECHECK_Instruction()`

**Syntax**
- Hint (translated, best-effort): no arguments
- Hint (raw comment): `引数なし`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `VOID_ArgumentBuilder()`

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = METHOD_SAFE | EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.VEvaluator.RESULT = 4`
  - `exm.VEvaluator.RESULT = 5`
  - `exm.VEvaluator.RESULT = 3`
  - `exm.VEvaluator.RESULT = 2`
  - `exm.VEvaluator.RESULT = 1`
  - `exm.VEvaluator.RESULT = 0`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:2832 (`UPDATECHECK_Instruction`)

## QUIT_AND_RESTART (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void)

**Syntax**
- Hint (translated, best-effort): no arguments
- Hint (raw comment): `引数なし`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `VOID_ArgumentBuilder()`

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (key operations):
  - `exm.Console.Quit()`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:303 (case `QUIT_AND_RESTART`)

## FORCE_QUIT (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void)

**Syntax**
- Hint (translated, best-effort): no arguments
- Hint (raw comment): `引数なし`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `VOID_ArgumentBuilder()`

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (key operations):
  - `exm.Console.ForceQuit()`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:307 (case `FORCE_QUIT`)

## FORCE_QUIT_AND_RESTART (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void)

**Syntax**
- Hint (translated, best-effort): no arguments
- Hint (raw comment): `引数なし`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `VOID_ArgumentBuilder()`

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (key operations):
  - `exm.Console.ForceQuit()`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`:310 (case `FORCE_QUIT_AND_RESTART`)

## FORCE_BEGIN (instruction)
**Summary**
- A “forced” variant of `BEGIN`.

**Metadata**
- Arg spec: `STR` (see #argument-spec-str) (inferred from `FORCE_BEGIN_Instruction` ArgBuilder assignment)
- Implementor (registration): `new FORCE_BEGIN_Instruction()`

**Syntax**
- `FORCE_BEGIN <keyword>`

**Arguments**
- Same as `BEGIN`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Same as `BEGIN` in the current engine implementation.
- Engine-extracted notes (base flags from class):
  - `flag = FLOW_CONTROL`
- Engine-extracted notes (key operations):
  - `state.SetBegin(keyword, true)`
  - `state.Return(0)`
  - `exm.Console.ResetStyle()`

**Errors & validation**
- Same as `BEGIN`.

**Examples**
- `FORCE_BEGIN TITLE`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.STR`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:3040 (`FORCE_BEGIN_Instruction`)

## INPUTANY (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `INPUTANY_Instruction` ArgBuilder assignment)
- Implementor (registration): `new INPUTANY_Instruction()`

**Syntax**
- Hint (translated, best-effort): no arguments
- Hint (raw comment): `引数なし`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `VOID_ArgumentBuilder()`

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.Console.WaitInput(req)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:2207 (`INPUTANY_Instruction`)

## TOOLTIP_SETFONT (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `STR_EXPRESSION` (see #argument-spec-str_expression) (inferred from `TOOLTIP_SETFONT_Instruction` ArgBuilder assignment)
- Implementor (registration): `new TOOLTIP_SETFONT_Instruction()`

**Syntax**
- Hint (translated, best-effort): string expression
- Hint (raw comment): `文字列式型`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `STR_EXPRESSION_ArgumentBuilder(false)`
- Type pattern: `[typeof(string)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.Console.SetToolTipFontName(fn.Term.GetStrValue(exm))`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.STR_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:2932 (`TOOLTIP_SETFONT_Instruction`)

## TOOLTIP_SETFONTSIZE (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `INT_EXPRESSION` (see #argument-spec-int_expression) (inferred from `TOOLTIP_SETFONTSIZE_Instruction` ArgBuilder assignment)
- Implementor (registration): `new TOOLTIP_SETFONTSIZE_Instruction()`

**Syntax**
- Hint (translated, best-effort): int expression。optional
- Hint (raw comment): `数式型。省略可能`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `INT_EXPRESSION_ArgumentBuilder(false)`
- Type pattern: `[typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.Console.SetToolTipFontSize(fs.Term.GetIntValue(exm))`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:2948 (`TOOLTIP_SETFONTSIZE_Instruction`)

## TOOLTIP_CUSTOM (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `INT_EXPRESSION` (see #argument-spec-int_expression) (inferred from `TOOLTIP_CUSTOM_Instruction` ArgBuilder assignment)
- Implementor (registration): `new TOOLTIP_CUSTOM_Instruction()`

**Syntax**
- Hint (translated, best-effort): int expression。optional
- Hint (raw comment): `数式型。省略可能`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `INT_EXPRESSION_ArgumentBuilder(false)`
- Type pattern: `[typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.Console.CustomToolTip(false)`
  - `exm.Console.CustomToolTip(true)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:2964 (`TOOLTIP_CUSTOM_Instruction`)

## TOOLTIP_FORMAT (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `INT_EXPRESSION` (see #argument-spec-int_expression) (inferred from `TOOLTIP_FORMAT_Instruction` ArgBuilder assignment)
- Implementor (registration): `new TOOLTIP_FORMAT_Instruction()`

**Syntax**
- Hint (translated, best-effort): int expression。optional
- Hint (raw comment): `数式型。省略可能`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `INT_EXPRESSION_ArgumentBuilder(false)`
- Type pattern: `[typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.Console.SetToolTipFormat(i.Term.GetIntValue(exm))`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:2983 (`TOOLTIP_FORMAT_Instruction`)

## TOOLTIP_IMG (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `INT_EXPRESSION` (see #argument-spec-int_expression) (inferred from `TOOLTIP_IMG_Instruction` ArgBuilder assignment)
- Implementor (registration): `new TOOLTIP_IMG_Instruction()`

**Syntax**
- Hint (translated, best-effort): int expression。optional
- Hint (raw comment): `数式型。省略可能`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `INT_EXPRESSION_ArgumentBuilder(false)`
- Type pattern: `[typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED`
- Engine-extracted notes (key operations):
  - `exm.Console.SetToolTipImg(i.Term.GetIntValue(exm) != 0)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.INT_EXPRESSION`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:2999 (`TOOLTIP_IMG_Instruction`)

## BINPUT (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `SP_INPUT` (see #argument-spec-sp_input) (inferred from `BINPUT_Instruction` ArgBuilder assignment)
- Implementor (registration): `new BINPUT_Instruction()`

**Syntax**
- Hint (translated, best-effort): (<int>) //引数はオプションでないのがデフォ, INT_EXPRESSION_NULLABLEとは処理が違う
- Hint (raw comment): `(<数値>) //引数はオプションでないのがデフォ、INT_EXPRESSION_NULLABLEとは処理が違う`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `SP_INPUT_ArgumentBuilder()`
- Type pattern: `[typeof(long), typeof(long), typeof(long), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT | IS_INPUT`
- Engine-extracted notes (key operations):
  - `if (!exm.Console.PrintBuffer.IsEmpty)`
  - `exm.Console.NewLine()`
  - `exm.Console.RefreshStrings(true)`
  - `exm.Console.Window.ApplyTextBoxChanges()`
  - `foreach (ConsoleDisplayLine line in Enumerable.Reverse(exm.Console.DisplayLineList).ToList())`
  - `if (button.Generation != 0 && button.Generation != exm.Console.LastButtonGeneration)`
  - `foreach (var value in exm.Console.EscapedParts)`
  - `exm.Console.WaitInput(req)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.NothingButtonBinput.Text, "BINPUT"))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_INPUT`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:2227 (`BINPUT_Instruction`)

## BINPUTS (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `SP_INPUTS` (see #argument-spec-sp_inputs) (inferred from `BINPUTS_Instruction` ArgBuilder assignment)
- Implementor (registration): `new BINPUTS_Instruction()`

**Syntax**
- Hint (translated, best-effort): (<FORMstring>) //引数はオプションでないのがデフォ, STR_EXPRESSION_NULLABLEとは処理が違う
- Hint (raw comment): `(<FORM文字列>) //引数はオプションでないのがデフォ、STR_EXPRESSION_NULLABLEとは処理が違う`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `SP_INPUTS_ArgumentBuilder()`
- Type pattern: `[typeof(string)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT | IS_INPUT`
- Engine-extracted notes (key operations):
  - `if (!exm.Console.PrintBuffer.IsEmpty)`
  - `exm.Console.NewLine()`
  - `exm.Console.RefreshStrings(true)`
  - `exm.Console.Window.ApplyTextBoxChanges()`
  - `foreach (ConsoleDisplayLine line in Enumerable.Reverse(exm.Console.DisplayLineList).ToList())`
  - `if (button.Generation != 0 && button.Generation != exm.Console.LastButtonGeneration)`
  - `foreach (var value in exm.Console.EscapedParts)`
  - `exm.Console.WaitInput(req)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.NothingButtonBinput.Text, "BINPUTS"))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_INPUTS`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:2317 (`BINPUTS_Instruction`)

## ONEBINPUT (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `SP_INPUT` (see #argument-spec-sp_input) (inferred from `ONEBINPUT_Instruction` ArgBuilder assignment)
- Implementor (registration): `new ONEBINPUT_Instruction()`

**Syntax**
- Hint (translated, best-effort): (<int>) //引数はオプションでないのがデフォ, INT_EXPRESSION_NULLABLEとは処理が違う
- Hint (raw comment): `(<数値>) //引数はオプションでないのがデフォ、INT_EXPRESSION_NULLABLEとは処理が違う`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `SP_INPUT_ArgumentBuilder()`
- Type pattern: `[typeof(long), typeof(long), typeof(long), typeof(long)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT | IS_INPUT`
- Engine-extracted notes (key operations):
  - `if (!exm.Console.PrintBuffer.IsEmpty)`
  - `exm.Console.NewLine()`
  - `exm.Console.RefreshStrings(true)`
  - `exm.Console.Window.ApplyTextBoxChanges()`
  - `foreach (ConsoleDisplayLine line in Enumerable.Reverse(exm.Console.DisplayLineList).ToList())`
  - `if (button.Generation != 0 && button.Generation != exm.Console.LastButtonGeneration)`
  - `foreach (var value in exm.Console.EscapedParts)`
  - `exm.Console.WaitInput(req)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.NothingButtonBinput.Text, "ONEBINPUT"))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_INPUT`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:2423 (`ONEBINPUT_Instruction`)

## ONEBINPUTS (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `SP_INPUTS` (see #argument-spec-sp_inputs) (inferred from `ONEBINPUTS_Instruction` ArgBuilder assignment)
- Implementor (registration): `new ONEBINPUTS_Instruction()`

**Syntax**
- Hint (translated, best-effort): (<FORMstring>) //引数はオプションでないのがデフォ, STR_EXPRESSION_NULLABLEとは処理が違う
- Hint (raw comment): `(<FORM文字列>) //引数はオプションでないのがデフォ、STR_EXPRESSION_NULLABLEとは処理が違う`
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `SP_INPUTS_ArgumentBuilder()`
- Type pattern: `[typeof(string)]` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).
- Minimum args: `0`.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT | IS_INPUT`
- Engine-extracted notes (key operations):
  - `if (!exm.Console.PrintBuffer.IsEmpty)`
  - `exm.Console.NewLine()`
  - `exm.Console.RefreshStrings(true)`
  - `exm.Console.Window.ApplyTextBoxChanges()`
  - `foreach (ConsoleDisplayLine line in Enumerable.Reverse(exm.Console.DisplayLineList).ToList())`
  - `if (button.Generation != 0 && button.Generation != exm.Console.LastButtonGeneration)`
  - `foreach (var value in exm.Console.EscapedParts)`
  - `exm.Console.WaitInput(req)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.NothingButtonBinput.Text, "ONEBINPUTS"))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_INPUTS`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:2513 (`ONEBINPUTS_Instruction`)

## DT_COLUMN_OPTIONS (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: `SP_DT_COLUMN_OPTIONS` (see #argument-spec-sp_dt_column_options) (inferred from `DT_COLUMN_OPTIONS_Instruction` ArgBuilder assignment)
- Implementor (registration): `new DT_COLUMN_OPTIONS_Instruction()`

**Syntax**
- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).

**Arguments**
- Builder: `SP_DT_COLUMN_OPTIONS_ArgumentBuilder()`
- Type pattern: `null;// new Type[] { typeof(string), typeof(string), typeof(Int64), typeof(Int64), typeof(Int64) }` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED | METHOD_SAFE`
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataDataTables`
  - `if (!dict.ContainsKey(key)) exm.VEvaluator.RESULT = -1`
  - `if (!dt.Columns.Contains(cName)) exm.VEvaluator.RESULT = 0`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.DTInvalidDataType.Text, "DT_COLUMN_OPTIONS", key, cName))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_DT_COLUMN_OPTIONS`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:2619 (`DT_COLUMN_OPTIONS_Instruction`)

## VARI (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new VARI_Instruction()`
- Note: Config-gated: `JSONConfig.Data.UseScopedVariableInstruction`

**Syntax**
- (TODO)

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:33 (`VARI_Instruction`)

## VARS (instruction)
**Summary**
- (TODO)

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new VARS_Instruction()`
- Note: Config-gated: `JSONConfig.Data.UseScopedVariableInstruction`

**Syntax**
- (TODO)

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:57 (`VARS_Instruction`)

## HTML_PRINT_ISLAND (instruction)
**Summary**
- Prints an HTML string into the “HTML island” layer, which is not tied to the normal scrollback/logical line list.

**Metadata**
- Arg spec: `SP_HTML_PRINT` (see #argument-spec-sp_html_print) (inferred from `HTML_PRINT_ISLAND_Instruction` ArgBuilder assignment)
- Implementor (registration): `new HTML_PRINT_ISLAND_Instruction()`
- Note: Config-gated: `JSONConfig.Data.UseScopedVariableInstruction`

**Syntax**
- `HTML_PRINT_ISLAND <html>(, <ignored>)`

**Arguments**
- `<html>` (string): HTML string (see `html-output.md`).
- `<ignored>` (optional, int): compatibility-only argument.
  - If provided, it must be a valid `int` expression (it is parsed and type-checked).
  - The value is ignored by `HTML_PRINT_ISLAND` and is not evaluated during execution.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output and no evaluation).
- Evaluates `<html>` to a string and appends the rendered HTML output into a separate “island” layer.
- The island layer is not counted by `LINECOUNT` and is not removed by `CLEARLINE`.
- The island layer is drawn independently of the normal log:
  - It does not scroll with the log.
  - It is drawn from the top of the window, with each appended “logical line” placed on successive rows.
- Note: `<div ...>...</div>` sub-areas are not rendered in the island layer.
- Use `HTML_PRINT_ISLAND_CLEAR` to clear the island layer.
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED | METHOD_SAFE`
- Engine-extracted notes (key operations):
  - `exm.Console.PrintHTMLIsland(str)`

**Errors & validation**
- Argument type/count errors follow the normal expression argument rules.
- Invalid HTML strings raise runtime errors (same HTML mini-language as `HTML_PRINT`).

**Examples**
```erabasic
HTML_PRINT_ISLAND "<div width='300px' height='30px' color='#202020'><font color='white'>Status</font></div>"
```

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.SP_HTML_PRINT`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:365 (`HTML_PRINT_ISLAND_Instruction`)

## HTML_PRINT_ISLAND_CLEAR (instruction)
**Summary**
- Clears all content previously added by `HTML_PRINT_ISLAND`.

**Metadata**
- Arg spec: `VOID` (see #argument-spec-void) (inferred from `HTML_PRINT_ISLAND_CLEAR_Instruction` ArgBuilder assignment)
- Implementor (registration): `new HTML_PRINT_ISLAND_CLEAR_Instruction()`
- Note: Config-gated: `JSONConfig.Data.UseScopedVariableInstruction`

**Syntax**
- `HTML_PRINT_ISLAND_CLEAR`

**Arguments**
- None.

**Defaults / optional arguments**
- Optional/default behavior is builder-specific; see engine refs.

**Semantics**
- Clears the “HTML island” layer immediately.
- This instruction is not skipped by output skipping; it always clears the island layer.
- Engine-extracted notes (base flags from class):
  - `flag = EXTENDED | METHOD_SAFE`
- Engine-extracted notes (key operations):
  - `exm.Console.ClearHTMLIsland()`

**Errors & validation**
- None.

**Examples**
```erabasic
HTML_PRINT_ISLAND_CLEAR
```

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Arg builder mapping: `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (search `FunctionArgType.VOID`)
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:387 (`HTML_PRINT_ISLAND_CLEAR_Instruction`)

## PRINTN (instruction)
**Summary**
- `PRINTN` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`
- Note: Config-gated: `JSONConfig.Data.UseScopedVariableInstruction`

**Syntax**
- `PRINTN [<raw text>]`
- `PRINTN;<raw text>`

**Arguments**
- `<raw text>` (optional, default `""`): raw text, not an expression.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Waits for a key **without** ending the logical output line (see `PRINT`).
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTN ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTVN (instruction)
**Summary**
- `PRINTVN` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`
- Note: Config-gated: `JSONConfig.Data.UseScopedVariableInstruction`

**Syntax**
- `PRINTVN <expr1> [, <expr2> ...]`

**Arguments**
- One or more comma-separated expressions (each may be int or string).
- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Concatenates all arguments into a single output string, then prints it.
- Waits for a key **without** ending the logical output line (see `PRINT`).
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTVN ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTSN (instruction)
**Summary**
- `PRINTSN` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`
- Note: Config-gated: `JSONConfig.Data.UseScopedVariableInstruction`

**Syntax**
- `PRINTSN <string expr>`

**Arguments**
- A single string expression (must be present).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression and prints the result.
- Waits for a key **without** ending the logical output line (see `PRINT`).
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTSN ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTFORMN (instruction)
**Summary**
- `PRINTFORMN` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`
- Note: Config-gated: `JSONConfig.Data.UseScopedVariableInstruction`

**Syntax**
- `PRINTFORMN [<FORM string>]`

**Arguments**
- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).
- The argument is optional for the `...FORM...` PRINT family (missing means empty string).

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- The formatted string is scanned at load/parse time and evaluated at runtime.
- Waits for a key **without** ending the logical output line (see `PRINT`).
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMN ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

## PRINTFORMSN (instruction)
**Summary**
- `PRINTFORMSN` is a PRINT-family variant.
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).

**Metadata**
- Arg spec: (instruction-defined)
- Implementor (registration): `new PRINT_Instruction("<keyword>")`
- Note: Config-gated: `JSONConfig.Data.UseScopedVariableInstruction`

**Syntax**
- `PRINTFORMSN <string expr>`

**Arguments**
- A string expression (must be present).
- The resulting string is then treated as a FORM/formatted string **at runtime**.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics).
- Evaluates the string expression to produce a format-string source.
- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.
- Waits for a key **without** ending the logical output line (see `PRINT`).
- Engine-extracted notes (base flags from class):
  - `flag = IS_PRINT`
- Engine-extracted notes (key operations):
  - `exm.Console.UseUserStyle = true`
  - `exm.Console.UseSetColorStyle = !func.Function.IsPrintDFunction()`
  - `str = exm.ConvertStringType(str)`
  - `exm.Console.PrintC(str, true)`
  - `exm.Console.PrintC(str, false)`
  - `exm.OutputToConsole(str, func.Function, isLineEnd)`
  - `exm.Console.UseSetColorStyle = true`

**Errors & validation**
- Argument parsing/type-checking errors follow the underlying argument mode for this variant.

**Examples**
- `PRINTFORMSN ...`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Execution: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`:83 (`PRINT_Instruction`)

# Expression functions (methods)

## How to read method argument rules

Method entries describe argument checking using one of two engine models:
- `argumentTypeArray = [typeof(...), ...]`: fixed arity and fixed operand types (`long` vs `string`).
- `argumentTypeArrayEx`: a list of `ArgTypeList` signature options used for refs/arrays/variadics/optional args.

For `argumentTypeArrayEx` entries:
- Each `ArgTypeList:` line is one **signature option** (an overload-like alternative). Any one option may match; the engine accepts the first one that passes all checks.
- `OmitStart = k` is a **0-based index** controlling omission/`null`:
  - Argument count must satisfy `k <= argc <= len(ArgTypes)` (unless variadic). If `OmitStart = -1`, then `argc` must equal `len(ArgTypes)` (unless variadic).
  - Trailing arguments may be omitted by passing fewer than `len(ArgTypes)` arguments (method supplies defaults in its implementation, typically by checking `arguments.Count`).
  - A blank argument inside the call (e.g. `FUNC(a,,c)` or `FUNC(a,)`) becomes `null`. `null` is rejected for positions `< OmitStart`, and may also be rejected at/after `OmitStart` when the rule includes `DisallowVoid`.
- Common `ArgType` flags you may see:
  - `Ref*`: argument must be a variable term (by-reference-like), not an arbitrary expression.
  - `AllowConstRef`: allows referencing `CONST` variables where otherwise refs reject them.
  - `CharacterData`: requires a character-data variable term (chara var).
  - `Variadic*`: variable-length tail; when `MatchVariadicGroup=true`, the tail repeats in fixed-size groups.
  - `SameAsFirst`: enforces operand-type equality with argument 1 for that position.
  - `DisallowVoid`: forbids omission/`null` for that position even when `OmitStart` would allow it.

Total (method names in `FunctionMethodCreator`): `266`.

## GETCHARA (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetcharaMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.Int }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return exm.VEvaluator.GetChara(integer)`
  - `long chara = exm.VEvaluator.GetChara_UseSp(integer, false)`
  - `return exm.VEvaluator.GetChara_UseSp(integer, true)`
  - `return exm.VEvaluator.GetChara_UseSp(integer, false)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1992 (class `GetcharaMethod`)

## GETSPCHARA (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetspcharaMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return exm.VEvaluator.GetChara_UseSp(integer, true)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.SPCharacterFeatureDisabled.Text)`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2046 (class `GetspcharaMethod`)

## CSVNAME (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new CsvStrDataMethod(CharacterStrData.NAME)`
- Return type: `string`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.Int }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return exm.VEvaluator.GetCharacterStrfromCSVData(x, charaStr, y != 0, 0)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.SPCharacterFeatureDisabled.Text)`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2064 (class `CsvStrDataMethod`)

## CSVCALLNAME (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new CsvStrDataMethod(CharacterStrData.CALLNAME)`
- Return type: `string`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.Int }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return exm.VEvaluator.GetCharacterStrfromCSVData(x, charaStr, y != 0, 0)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.SPCharacterFeatureDisabled.Text)`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2064 (class `CsvStrDataMethod`)

## CSVNICKNAME (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new CsvStrDataMethod(CharacterStrData.NICKNAME)`
- Return type: `string`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.Int }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return exm.VEvaluator.GetCharacterStrfromCSVData(x, charaStr, y != 0, 0)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.SPCharacterFeatureDisabled.Text)`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2064 (class `CsvStrDataMethod`)

## CSVMASTERNAME (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new CsvStrDataMethod(CharacterStrData.MASTERNAME)`
- Return type: `string`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.Int }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return exm.VEvaluator.GetCharacterStrfromCSVData(x, charaStr, y != 0, 0)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.SPCharacterFeatureDisabled.Text)`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2064 (class `CsvStrDataMethod`)

## CSVCSTR (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new CsvcstrMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.Int, ArgType.Int }; OmitStart = 2.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return exm.VEvaluator.GetCharacterStrfromCSVData(x, CharacterStrData.CSTR, z != 0, y)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.SPCharacterFeatureDisabled.Text)`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2114 (class `CsvcstrMethod`)

## CSVBASE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new CsvDataMethod(CharacterIntData.BASE)`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.Int, ArgType.Int }; OmitStart = 2.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return exm.VEvaluator.GetCharacterIntfromCSVData(x, charaInt, z != 0, y)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.SPCharacterFeatureDisabled.Text)`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2157 (class `CsvDataMethod`)

## CSVABL (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new CsvDataMethod(CharacterIntData.ABL)`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.Int, ArgType.Int }; OmitStart = 2.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return exm.VEvaluator.GetCharacterIntfromCSVData(x, charaInt, z != 0, y)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.SPCharacterFeatureDisabled.Text)`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2157 (class `CsvDataMethod`)

## CSVMARK (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new CsvDataMethod(CharacterIntData.MARK)`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.Int, ArgType.Int }; OmitStart = 2.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return exm.VEvaluator.GetCharacterIntfromCSVData(x, charaInt, z != 0, y)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.SPCharacterFeatureDisabled.Text)`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2157 (class `CsvDataMethod`)

## CSVEXP (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new CsvDataMethod(CharacterIntData.EXP)`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.Int, ArgType.Int }; OmitStart = 2.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return exm.VEvaluator.GetCharacterIntfromCSVData(x, charaInt, z != 0, y)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.SPCharacterFeatureDisabled.Text)`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2157 (class `CsvDataMethod`)

## CSVRELATION (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new CsvDataMethod(CharacterIntData.RELATION)`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.Int, ArgType.Int }; OmitStart = 2.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return exm.VEvaluator.GetCharacterIntfromCSVData(x, charaInt, z != 0, y)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.SPCharacterFeatureDisabled.Text)`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2157 (class `CsvDataMethod`)

## CSVTALENT (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new CsvDataMethod(CharacterIntData.TALENT)`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.Int, ArgType.Int }; OmitStart = 2.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return exm.VEvaluator.GetCharacterIntfromCSVData(x, charaInt, z != 0, y)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.SPCharacterFeatureDisabled.Text)`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2157 (class `CsvDataMethod`)

## CSVCFLAG (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new CsvDataMethod(CharacterIntData.CFLAG)`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.Int, ArgType.Int }; OmitStart = 2.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return exm.VEvaluator.GetCharacterIntfromCSVData(x, charaInt, z != 0, y)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.SPCharacterFeatureDisabled.Text)`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2157 (class `CsvDataMethod`)

## CSVEQUIP (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new CsvDataMethod(CharacterIntData.EQUIP)`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.Int, ArgType.Int }; OmitStart = 2.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return exm.VEvaluator.GetCharacterIntfromCSVData(x, charaInt, z != 0, y)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.SPCharacterFeatureDisabled.Text)`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2157 (class `CsvDataMethod`)

## CSVJUEL (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new CsvDataMethod(CharacterIntData.JUEL)`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.Int, ArgType.Int }; OmitStart = 2.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return exm.VEvaluator.GetCharacterIntfromCSVData(x, charaInt, z != 0, y)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.SPCharacterFeatureDisabled.Text)`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2157 (class `CsvDataMethod`)

## FINDCHARA (expression function)
**Summary**
- Returns the first chara index (role index) in the current character list whose character-data cell equals a target value.

**Metadata**
- Implementor: `new FindcharaMethod(false)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

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

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Reads the current `CHARANUM` and searches forward in the half-open range `[startIndex, lastIndex)`.
- For each chara index `i` in the range, compares the selected per-chara cell against `value` using direct equality:
  - string cell: `==` (ordinal string equality in .NET)
  - int cell: `==`
- Returns the first matching index `i`, or `-1` if:
  - no match is found, or
  - `startIndex >= lastIndex`.
- Engine-extracted notes (key operations):
  - `long lastindex = exm.VEvaluator.CHARANUM`
  - `if (startindex < 0 || startindex >= exm.VEvaluator.CHARANUM)`
  - `if (lastindex < 0 || lastindex > exm.VEvaluator.CHARANUM)`
  - `ret = VariableEvaluator.FindChara(varID, elem, word, startindex, lastindex, isLast)`

**Errors & validation**
- Errors if `charaVarTerm` is not a character-data variable term, or if `value`’s type does not match the cell type.
- Runtime errors if the range is invalid:
  - `startIndex < 0` or `startIndex >= CHARANUM`
  - `lastIndex < 0` or `lastIndex > CHARANUM`
- Note: `startIndex >= lastIndex` is not an error; it returns `-1`.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.CharacterIndexOutOfRange.Text, Name, 3, startindex))`
  - `throw new CodeEE(string.Format(trerror.CharacterIndexOutOfRange.Text, Name, 4, lastindex))`

**Examples**
- `idx = FINDCHARA(NAME, "Alice")`
- `idx = FINDCHARA(CFLAG:3, 1, 10)`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2212 (class `FindcharaMethod`)

## FINDLASTCHARA (expression function)
**Summary**
- Like `FINDCHARA`, but searches backward and returns the last matching chara index (role index) in the range.

**Metadata**
- Implementor: `new FindcharaMethod(true)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

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

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Reads the current `CHARANUM` and searches backward in the half-open range `[startIndex, lastIndex)`.
- The search order is: `lastIndex - 1`, `lastIndex - 2`, ..., down to `startIndex`.
- For each chara index `i` in the range, compares the selected per-chara cell against `value` using direct equality:
  - string cell: `==` (ordinal string equality in .NET)
  - int cell: `==`
- Returns the first match encountered in that reverse scan (i.e. the “last” match in the range), or `-1` if:
  - no match is found, or
  - `startIndex >= lastIndex`.
- Engine-extracted notes (key operations):
  - `long lastindex = exm.VEvaluator.CHARANUM`
  - `if (startindex < 0 || startindex >= exm.VEvaluator.CHARANUM)`
  - `if (lastindex < 0 || lastindex > exm.VEvaluator.CHARANUM)`
  - `ret = VariableEvaluator.FindChara(varID, elem, word, startindex, lastindex, isLast)`

**Errors & validation**
- Errors if `charaVarTerm` is not a character-data variable term, or if `value`’s type does not match the cell type.
- Runtime errors if the range is invalid:
  - `startIndex < 0` or `startIndex >= CHARANUM`
  - `lastIndex < 0` or `lastIndex > CHARANUM`
- Note: `startIndex >= lastIndex` is not an error; it returns `-1`.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.CharacterIndexOutOfRange.Text, Name, 3, startindex))`
  - `throw new CodeEE(string.Format(trerror.CharacterIndexOutOfRange.Text, Name, 4, lastindex))`

**Examples**
- `idx = FINDLASTCHARA(NAME, "Alice")`
- `idx = FINDLASTCHARA(CFLAG:3, 1, 10)`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2212 (class `FindcharaMethod`)

## EXISTCSV (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new ExistCsvMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.Int }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return exm.VEvaluator.ExistCsv(no, isSp)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.SPCharacterFeatureDisabled.Text)`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2292 (class `ExistCsvMethod`)

## VARSIZE (expression function)
**Summary**
- Returns the length of an array variable’s dimension.

**Metadata**
- Implementor: `new VarsizeMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

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

**Defaults / optional arguments**
- (TODO)

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
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.NotVariableName.Text, Name, 1, arguments[0].GetStrValue(exm)))`

**Examples**
- `n = VARSIZE("ITEM")` (length of `ITEM`)
- `w = VARSIZE("CFLAG", 1)` (first dimension when `VarsizeDimConfig` is enabled)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2333 (class `VarsizeMethod`)

## CHKFONT (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new CheckfontMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true;//起動中に変わることもそうそうないはず……`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2399 (class `CheckfontMethod`)

## CHKDATA (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new CheckdataMethod(EraSaveFileType.Normal)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `EraDataResult result = exm.VEvaluator.CheckData((int)target, type)`
  - `exm.VEvaluator.RESULTS = result.DataMes`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.ArgIsNegative.Text, Name, 1, target))`
  - `throw new CodeEE(string.Format(trerror.ArgIsTooLarge.Text, Name, 1, target))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2435 (class `CheckdataMethod`)

## ISSKIP (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new IsSkipMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return exm.Process.SkipPrint ? 1L : 0L`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2529 (class `IsSkipMethod`)

## MOUSESKIP (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new MesSkipMethod(true)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: custom check (no `argumentTypeArray`/`argumentTypeArrayEx` assignment detected).

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2543 (class `MesSkipMethod`)

## MESSKIP (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new MesSkipMethod(false)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: custom check (no `argumentTypeArray`/`argumentTypeArrayEx` assignment detected).

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2543 (class `MesSkipMethod`)

## GETCOLOR (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetColorMethod(false)`
- Return type: `long`
- Constant folding (`CanRestructure`): `isDef`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2571 (class `GetColorMethod`)

## GETDEFCOLOR (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetColorMethod(true)`
- Return type: `long`
- Constant folding (`CanRestructure`): `isDef`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2571 (class `GetColorMethod`)

## GETFOCUSCOLOR (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetFocusColorMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2589 (class `GetFocusColorMethod`)

## GETBGCOLOR (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetBGColorMethod(false)`
- Return type: `long`
- Constant folding (`CanRestructure`): `isDef`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2603 (class `GetBGColorMethod`)

## GETDEFBGCOLOR (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetBGColorMethod(true)`
- Return type: `long`
- Constant folding (`CanRestructure`): `isDef`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2603 (class `GetBGColorMethod`)

## GETSTYLE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetStyleMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2621 (class `GetStyleMethod`)

## GETFONT (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetFontMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2646 (class `GetFontMethod`)

## BARSTR (expression function)
**Summary**
- Returns the same bar string that `BAR`/`BARL` would print with the same arguments.

**Metadata**
- Implementor: `new BarStringMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- `BARSTR(value, maxValue, length)`

**Signatures / argument rules**
- `BARSTR(value, maxValue, length)` → `string`

**Arguments**
- `value`: int expression (numerator).
- `maxValue`: int expression (denominator); must evaluate to `> 0`.
- `length`: int expression (bar width); must satisfy `1 <= length <= 99`.

**Defaults / optional arguments**
- (TODO)

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

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2660 (class `BarStringMethod`)

## CURRENTALIGN (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new CurrentAlignMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `if (exm.Console.Alignment == DisplayLineAlignment.LEFT)`
  - `else if (exm.Console.Alignment == DisplayLineAlignment.CENTER)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2677 (class `CurrentAlignMethod`)

## CURRENTREDRAW (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new CurrentRedrawMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return (exm.Console.Redraw == GameView.ConsoleRedraw.None) ? 0L : 1L`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2696 (class `CurrentRedrawMethod`)

## COLOR_FROMNAME (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new ColorFromNameMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(trerror.TransparentUnsupported.Text)`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2710 (class `ColorFromNameMethod`)

## COLOR_FROMRGB (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new ColorFromRGBMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long), typeof(long), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.ArgIsOutOfRange.Text, Name, 1, r, 0, 255))`
  - `throw new CodeEE(string.Format(trerror.ArgIsOutOfRange.Text, Name, 2, g, 0, 255))`
  - `throw new CodeEE(string.Format(trerror.ArgIsOutOfRange.Text, Name, 3, b, 0, 255))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2737 (class `ColorFromRGBMethod`)

## CHKCHARADATA (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new CheckdataStrMethod(EraSaveFileType.CharVar)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `EraDataResult result = exm.VEvaluator.CheckData(datFilename, type)`
  - `exm.VEvaluator.RESULTS = result.DataMes`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2464 (class `CheckdataStrMethod`)

## FIND_CHARADATA (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new FindFilesMethod(EraSaveFileType.CharVar)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String }; OmitStart = 0.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `List<string> filepathes = VariableEvaluator.GetDatFiles(type == EraSaveFileType.CharVar, pattern)`
  - `string[] results = exm.VEvaluator.VariableData.DataStringArray[(int)(VariableCode.RESULTS & VariableCode.__LOWERCASE__)]`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2487 (class `FindFilesMethod`)

## MONEYSTR (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new MoneyStrMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.String }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.InvalidFormat.Text, Name, 2))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2794 (class `MoneyStrMethod`)

## PRINTCPERLINE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetPrintCPerLineMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2840 (class `GetPrintCPerLineMethod`)

## PRINTCLENGTH (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new PrintCLengthMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2854 (class `PrintCLengthMethod`)

## SAVENOS (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetSaveNosMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2868 (class `GetSaveNosMethod`)

## GETTIME (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GettimeMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2882 (class `GettimeMethod`)

## GETTIMES (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GettimesMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2903 (class `GettimesMethod`)

## GETMILLISECOND (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetmsMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2917 (class `GetmsMethod`)

## GETSECOND (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetSecondMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2932 (class `GetSecondMethod`)

## RAND (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new RandMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.Int }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return exm.VEvaluator.GetNextRand(max - min) + min`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.NegativeMaximum.Text, Name, max))`
  - `throw new CodeEE(string.Format(trerror.MaximumLowerThanMinimum.Text, Name, max))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:2950 (class `RandMethod`)

## MIN (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new MaxMethod(false)`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.VariadicInt }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3009 (class `MaxMethod`)

## MAX (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new MaxMethod(true)`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.VariadicInt }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3009 (class `MaxMethod`)

## ABS (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new AbsMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.MinInt64CanNotApplyABS.Text, Name, long.MinValue))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3067 (class `AbsMethod`)

## POWER (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new PowerMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.ResultIsNaN.Text, Name))`
  - `throw new CodeEE(string.Format(trerror.ResultIsInfinity.Text, Name))`
  - `throw new CodeEE(string.Format(trerror.ResultIsOutOfTheRangeOfInt64.Text, Name, pow))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3085 (class `PowerMethod`)

## SQRT (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new SqrtMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.ArgIsNegative.Text, Name, 1, ret))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3111 (class `SqrtMethod`)

## CBRT (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new CbrtMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.ArgIsNegative.Text, Name, 1, ret))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3129 (class `CbrtMethod`)

## LOG (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new LogMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.ArgIsNotMoreThan0.Text, Name, 1, ret))`
  - `throw new CodeEE(string.Format(trerror.ResultIsNaN.Text, Name))`
  - `throw new CodeEE(string.Format(trerror.ResultIsInfinity.Text, Name))`
  - `throw new CodeEE(string.Format(trerror.ResultIsOutOfTheRangeOfInt64.Text, Name, dret))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3147 (class `LogMethod`)

## LOG10 (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new LogMethod(10.0d)`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.ArgIsNotMoreThan0.Text, Name, 1, ret))`
  - `throw new CodeEE(string.Format(trerror.ResultIsNaN.Text, Name))`
  - `throw new CodeEE(string.Format(trerror.ResultIsInfinity.Text, Name))`
  - `throw new CodeEE(string.Format(trerror.ResultIsOutOfTheRangeOfInt64.Text, Name, dret))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3147 (class `LogMethod`)

## EXPONENT (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new ExpMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.ResultIsNaN.Text, Name))`
  - `throw new CodeEE(string.Format(trerror.ResultIsInfinity.Text, Name))`
  - `throw new CodeEE(string.Format(trerror.ResultIsOutOfTheRangeOfInt64.Text, Name, dret))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3191 (class `ExpMethod`)

## SIGN (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new SignMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3217 (class `SignMethod`)

## LIMIT (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetLimitMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long), typeof(long), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3233 (class `GetLimitMethod`)

## SUMARRAY (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new SumArrayMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.RefIntArray, ArgType.Int, ArgType.Int }; OmitStart = 1.
- ArgTypeList: ArgTypes = { ArgType.CharacterData | ArgType.RefIntArray | ArgType.AllowConstRef, ArgType.Int, ArgType.Int }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `long index2 = (arguments.Count == 3 && arguments[2] != null) ? arguments[2].GetIntValue(exm) : (isCharaRange ? exm.VEvaluator.CHARANUM : varTerm.GetLastLength())`
  - `return VariableEvaluator.GetArraySum(p, index1, index2)`
  - `long charaNum = exm.VEvaluator.CHARANUM`
  - `return VariableEvaluator.GetArraySumChara(p, index1, index2)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.CharacterRangeInvalid.Text, Name, index1, index2))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3259 (class `SumArrayMethod`)

## SUMCARRAY (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new SumArrayMethod(true)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.RefIntArray, ArgType.Int, ArgType.Int }; OmitStart = 1.
- ArgTypeList: ArgTypes = { ArgType.CharacterData | ArgType.RefIntArray | ArgType.AllowConstRef, ArgType.Int, ArgType.Int }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `long index2 = (arguments.Count == 3 && arguments[2] != null) ? arguments[2].GetIntValue(exm) : (isCharaRange ? exm.VEvaluator.CHARANUM : varTerm.GetLastLength())`
  - `return VariableEvaluator.GetArraySum(p, index1, index2)`
  - `long charaNum = exm.VEvaluator.CHARANUM`
  - `return VariableEvaluator.GetArraySumChara(p, index1, index2)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.CharacterRangeInvalid.Text, Name, index1, index2))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3259 (class `SumArrayMethod`)

## MATCH (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new MatchMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.RefAny1D | ArgType.AllowConstRef, ArgType.SameAsFirst, ArgType.Int, ArgType.Int }; OmitStart = 2.
- ArgTypeList: ArgTypes = { ArgType.CharacterData | ArgType.RefAny1D | ArgType.AllowConstRef | ArgType.Any, ArgType.SameAsFirst, ArgType.Int, ArgType.Int }; OmitStart = 2.
- ArgTypeList: ArgTypes = { ArgType.Any, ArgType.SameAsFirst, ArgType.Int, ArgType.Int }; OmitStart = 2.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `long end = (arguments.Count > 3 && arguments[3] != null) ? arguments[3].GetIntValue(exm) : (isCharaRange ? exm.VEvaluator.CHARANUM : varTerm.GetLength())`
  - `return VariableEvaluator.GetMatch(p, targetValue, start, end)`
  - `return VariableEvaluator.GetMatch(p, targetStr, start, end)`
  - `long charaNum = exm.VEvaluator.CHARANUM`
  - `return VariableEvaluator.GetMatchChara(p, targetValue, start, end)`
  - `return VariableEvaluator.GetMatchChara(p, targetStr, start, end)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.CharacterRangeInvalid.Text, Name, start, end))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3332 (class `MatchMethod`)

## CMATCH (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new MatchMethod(true)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.RefAny1D | ArgType.AllowConstRef, ArgType.SameAsFirst, ArgType.Int, ArgType.Int }; OmitStart = 2.
- ArgTypeList: ArgTypes = { ArgType.CharacterData | ArgType.RefAny1D | ArgType.AllowConstRef | ArgType.Any, ArgType.SameAsFirst, ArgType.Int, ArgType.Int }; OmitStart = 2.
- ArgTypeList: ArgTypes = { ArgType.Any, ArgType.SameAsFirst, ArgType.Int, ArgType.Int }; OmitStart = 2.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `long end = (arguments.Count > 3 && arguments[3] != null) ? arguments[3].GetIntValue(exm) : (isCharaRange ? exm.VEvaluator.CHARANUM : varTerm.GetLength())`
  - `return VariableEvaluator.GetMatch(p, targetValue, start, end)`
  - `return VariableEvaluator.GetMatch(p, targetStr, start, end)`
  - `long charaNum = exm.VEvaluator.CHARANUM`
  - `return VariableEvaluator.GetMatchChara(p, targetValue, start, end)`
  - `return VariableEvaluator.GetMatchChara(p, targetStr, start, end)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.CharacterRangeInvalid.Text, Name, start, end))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3332 (class `MatchMethod`)

## GROUPMATCH (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GroupMatchMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Any, ArgType.VariadicSameAsFirst }.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3439 (class `GroupMatchMethod`)

## NOSAMES (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new NosamesMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Any, ArgType.VariadicSameAsFirst }.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3491 (class `NosamesMethod`)

## ALLSAMES (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new AllsamesMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Any, ArgType.VariadicSameAsFirst }.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3546 (class `AllsamesMethod`)

## MAXARRAY (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new MaxArrayMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.RefInt1D | ArgType.AllowConstRef, ArgType.Int, ArgType.Int }; OmitStart = 1.
- ArgTypeList: ArgTypes = { ArgType.CharacterData | ArgType.RefInt1D | ArgType.AllowConstRef, ArgType.Int, ArgType.Int }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `long end = (arguments.Count > 2 && arguments[2] != null) ? arguments[2].GetIntValue(exm) : (isCharaRange ? exm.VEvaluator.CHARANUM : vTerm.GetLength())`
  - `return VariableEvaluator.GetMaxArray(p, start, end, isMax)`
  - `long charaNum = exm.VEvaluator.CHARANUM`
  - `return VariableEvaluator.GetMaxArrayChara(p, start, end, isMax)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.CharacterRangeInvalid.Text, funcName, start, end))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3597 (class `MaxArrayMethod`)

## MAXCARRAY (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new MaxArrayMethod(true)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.RefInt1D | ArgType.AllowConstRef, ArgType.Int, ArgType.Int }; OmitStart = 1.
- ArgTypeList: ArgTypes = { ArgType.CharacterData | ArgType.RefInt1D | ArgType.AllowConstRef, ArgType.Int, ArgType.Int }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `long end = (arguments.Count > 2 && arguments[2] != null) ? arguments[2].GetIntValue(exm) : (isCharaRange ? exm.VEvaluator.CHARANUM : vTerm.GetLength())`
  - `return VariableEvaluator.GetMaxArray(p, start, end, isMax)`
  - `long charaNum = exm.VEvaluator.CHARANUM`
  - `return VariableEvaluator.GetMaxArrayChara(p, start, end, isMax)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.CharacterRangeInvalid.Text, funcName, start, end))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3597 (class `MaxArrayMethod`)

## MINARRAY (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new MaxArrayMethod(false, false)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.RefInt1D | ArgType.AllowConstRef, ArgType.Int, ArgType.Int }; OmitStart = 1.
- ArgTypeList: ArgTypes = { ArgType.CharacterData | ArgType.RefInt1D | ArgType.AllowConstRef, ArgType.Int, ArgType.Int }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `long end = (arguments.Count > 2 && arguments[2] != null) ? arguments[2].GetIntValue(exm) : (isCharaRange ? exm.VEvaluator.CHARANUM : vTerm.GetLength())`
  - `return VariableEvaluator.GetMaxArray(p, start, end, isMax)`
  - `long charaNum = exm.VEvaluator.CHARANUM`
  - `return VariableEvaluator.GetMaxArrayChara(p, start, end, isMax)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.CharacterRangeInvalid.Text, funcName, start, end))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3597 (class `MaxArrayMethod`)

## MINCARRAY (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new MaxArrayMethod(true, false)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.RefInt1D | ArgType.AllowConstRef, ArgType.Int, ArgType.Int }; OmitStart = 1.
- ArgTypeList: ArgTypes = { ArgType.CharacterData | ArgType.RefInt1D | ArgType.AllowConstRef, ArgType.Int, ArgType.Int }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `long end = (arguments.Count > 2 && arguments[2] != null) ? arguments[2].GetIntValue(exm) : (isCharaRange ? exm.VEvaluator.CHARANUM : vTerm.GetLength())`
  - `return VariableEvaluator.GetMaxArray(p, start, end, isMax)`
  - `long charaNum = exm.VEvaluator.CHARANUM`
  - `return VariableEvaluator.GetMaxArrayChara(p, start, end, isMax)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.CharacterRangeInvalid.Text, funcName, start, end))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3597 (class `MaxArrayMethod`)

## GETBIT (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetbitMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.ArgIsOutOfRange.Text, Name, 2, m, 0, 63))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3691 (class `GetbitMethod`)

## GETNUM (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetnumMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.RefAny | ArgType.AllowConstRef, ArgType.String, ArgType.Int }; OmitStart = 2.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `if (exm.VEvaluator.Constant.TryKeywordToInteger(out int ret, varCode, key, -1, varname))`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3724 (class `GetnumMethod`)

## GETPALAMLV (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetPalamLVMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return exm.VEvaluator.getPalamLv(value, maxLv)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3819 (class `GetPalamLVMethod`)

## GETEXPLV (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetExpLVMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return exm.VEvaluator.getExpLv(value, maxLv)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3845 (class `GetExpLVMethod`)

## FINDELEMENT (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new FindElementMethod(false)`
- Return type: `long`
- Constant folding (`CanRestructure`): `true; //すべて定数項ならできるはず`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.RefAny1D | ArgType.AllowConstRef, ArgType.SameAsFirst, ArgType.Int, ArgType.Int, ArgType.Int }; OmitStart = 2.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return VariableEvaluator.FindElement(p, targetValue, start, end, isExact, isLast)`
  - `return VariableEvaluator.FindElement(p, targetString, start, end, isExact, isLast)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.InvalidRegexArg.Text, Name, 2, e.Message))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3871 (class `FindElementMethod`)

## FINDLASTELEMENT (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new FindElementMethod(true)`
- Return type: `long`
- Constant folding (`CanRestructure`): `true; //すべて定数項ならできるはず`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.RefAny1D | ArgType.AllowConstRef, ArgType.SameAsFirst, ArgType.Int, ArgType.Int, ArgType.Int }; OmitStart = 2.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return VariableEvaluator.FindElement(p, targetValue, start, end, isExact, isLast)`
  - `return VariableEvaluator.FindElement(p, targetString, start, end, isExact, isLast)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.InvalidRegexArg.Text, Name, 2, e.Message))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3871 (class `FindElementMethod`)

## INRANGE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new InRangeMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long), typeof(long), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3968 (class `InRangeMethod`)

## INRANGEARRAY (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new InRangeArrayMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.RefInt1D | ArgType.AllowConstRef, ArgType.Int, ArgType.Int, ArgType.Int, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.CharacterData | ArgType.RefInt1D | ArgType.AllowConstRef, ArgType.Int, ArgType.Int, ArgType.Int, ArgType.Int }; OmitStart = 3.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `long end = (arguments.Count > 4 && arguments[4] != null) ? arguments[4].GetIntValue(exm) : (isCharaRange ? exm.VEvaluator.CHARANUM : varTerm.GetLength())`
  - `return VariableEvaluator.GetInRangeArray(p, min, max, start, end)`
  - `long charaNum = exm.VEvaluator.CHARANUM`
  - `return VariableEvaluator.GetInRangeArrayChara(p, min, max, start, end)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.CharacterRangeInvalid.Text, Name, start, end))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3985 (class `InRangeArrayMethod`)

## INRANGECARRAY (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new InRangeArrayMethod(true)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.RefInt1D | ArgType.AllowConstRef, ArgType.Int, ArgType.Int, ArgType.Int, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.CharacterData | ArgType.RefInt1D | ArgType.AllowConstRef, ArgType.Int, ArgType.Int, ArgType.Int, ArgType.Int }; OmitStart = 3.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `long end = (arguments.Count > 4 && arguments[4] != null) ? arguments[4].GetIntValue(exm) : (isCharaRange ? exm.VEvaluator.CHARANUM : varTerm.GetLength())`
  - `return VariableEvaluator.GetInRangeArray(p, min, max, start, end)`
  - `long charaNum = exm.VEvaluator.CHARANUM`
  - `return VariableEvaluator.GetInRangeArrayChara(p, min, max, start, end)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.CharacterRangeInvalid.Text, Name, start, end))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3985 (class `InRangeArrayMethod`)

## GETNUMB (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetnumBMethod()`
- Return type: `Int64`
- Constant folding (`CanRestructure`): `true`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: custom check (no `argumentTypeArray`/`argumentTypeArrayEx` assignment detected).

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `if (exm.VEvaluator.Constant.TryKeywordToInteger(out int ret, var.Code, key, -1, arguments[0].GetStrValue(exm)))`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE("GETNUMBの1番目の引数(\"" + arguments[0].GetStrValue(exm) + "\")が変数名ではありません")`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:3777 (class `GetnumBMethod`)

## ARRAYMSORT (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new ArrayMultiSortMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.RefAny1D, ArgType.RefAnyArray | ArgType.Variadic }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `else { throw new ExeEE(trerror.AbnormalArray.Text); }`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:4067 (class `ArrayMultiSortMethod`)

## STRLENS (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new StrlenMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:4227 (class `StrlenMethod`)

## STRLENSU (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new StrlenuMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:4242 (class `StrlenuMethod`)

## SUBSTRING (expression function)
**Summary**
- Returns a substring where `start`/`length` are measured in the engine’s “language length” units (the same unit returned by `STRLEN`).

**Metadata**
- Implementor: `new SubstringMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `true`

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

**Defaults / optional arguments**
- (TODO)

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

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:4257 (class `SubstringMethod`)

## SUBSTRINGU (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new SubstringuMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:4302 (class `SubstringuMethod`)

## STRFIND (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new StrfindMethod(false)`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.Int }; OmitStart = 2.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:4360 (class `StrfindMethod`)

## STRFINDU (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new StrfindMethod(true)`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.Int }; OmitStart = 2.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:4360 (class `StrfindMethod`)

## STRCOUNT (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new StrCountMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string), typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.InvalidRegexArg.Text, Name, 2, e.Message))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:4424 (class `StrCountMethod`)

## TOSTR (expression function)
**Summary**
- Converts an integer to a string, optionally using a .NET numeric format string.

**Metadata**
- Implementor: `new ToStrMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- `TOSTR(i [, format])`

**Signatures / argument rules**
- `TOSTR(i)` → `string`
- `TOSTR(i, format)` → `string`

**Arguments**
- `i`: int.
- `format` (optional): string expression passed to `Int64.ToString(format)`. If omitted or `null`, uses default formatting.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- If `format` is omitted or null: returns `i.ToString()`.
- Otherwise: returns `i.ToString(format)`.

**Errors & validation**
- Argument type/count errors are rejected by the engine’s function-method argument checker.
- If `format` is present but not a valid `.NET` numeric format string, raises a runtime error for invalid format (engine reports the error at argument position 2).
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.InvalidFormat.Text, Name, 2))`

**Examples**
- `TOSTR(42)` → `"42"`
- `TOSTR(42, "D5")` → `"00042"`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:4448 (class `ToStrMethod`)

## TOINT (expression function)
**Summary**
- Parses a string into an integer using the engine’s numeric-literal reader.
- Returns `0` for many invalid inputs, but some invalid numeric-literal forms raise an error (see Errors & validation).

**Metadata**
- Implementor: `new ToIntMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- `TOINT(str)`

**Signatures / argument rules**
- `TOINT(str)` → `long`

**Arguments**
- `str`: string expression.

**Defaults / optional arguments**
- (TODO)

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

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:4495 (class `ToIntMethod`)

## TOUPPER (expression function)
**Summary**
- Converts a string to uppercase.

**Metadata**
- Implementor: `new StrChangeStyleMethod(StrFormType.Upper)`
- Return type: `string`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- `TOUPPER(str)`

**Signatures / argument rules**
- `TOUPPER(str)` → `string`

**Arguments**
- `str`: string expression.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- If `str` is null/empty: returns `""`.
- Otherwise: returns `str.ToUpper()` using the process `CurrentCulture`.
  - In this engine, `CurrentCulture` is set to `InvariantCulture` at startup, so behavior is invariant-culture uppercasing.

**Errors & validation**
- None (apart from normal evaluation errors for `str`).

**Examples**
- `TOUPPER("Abc")` → `"ABC"`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:4546 (class `StrChangeStyleMethod`)

## TOLOWER (expression function)
**Summary**
- Converts a string to lowercase.

**Metadata**
- Implementor: `new StrChangeStyleMethod(StrFormType.Lower)`
- Return type: `string`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- `TOLOWER(str)`

**Signatures / argument rules**
- `TOLOWER(str)` → `string`

**Arguments**
- `str`: string expression.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- If `str` is null/empty: returns `""`.
- Otherwise: returns `str.ToLower()` using the process `CurrentCulture`.
  - In this engine, `CurrentCulture` is set to `InvariantCulture` at startup, so behavior is invariant-culture lowercasing.

**Errors & validation**
- None (apart from normal evaluation errors for `str`).

**Examples**
- `TOLOWER("Abc")` → `"abc"`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:4546 (class `StrChangeStyleMethod`)

## TOHALF (expression function)
**Summary**
- Converts full-width characters to half-width (narrow) form using the engine’s configured language encoding (`useLanguage`).

**Metadata**
- Implementor: `new StrChangeStyleMethod(StrFormType.Half)`
- Return type: `string`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- `TOHALF(str)`

**Signatures / argument rules**
- `TOHALF(str)` → `string`

**Arguments**
- `str`: string expression.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- If `str` is null/empty: returns `""`.
- Otherwise: uses VisualBasic `Strings.StrConv(..., Narrow, <code page>)`, where `<code page>` is the engine’s current language code page (derived from `useLanguage`).

**Errors & validation**
- Argument type/count errors are rejected by the engine’s function-method argument checker.
- Any runtime exceptions from the underlying `.NET` conversion routine propagate as engine errors.

**Examples**
- `TOHALF("ＡＢＣ")` → `"ABC"`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:4546 (class `StrChangeStyleMethod`)

## TOFULL (expression function)
**Summary**
- Converts half-width characters to full-width (wide) form using the engine’s configured language encoding (`useLanguage`).

**Metadata**
- Implementor: `new StrChangeStyleMethod(StrFormType.Full)`
- Return type: `string`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- `TOFULL(str)`

**Signatures / argument rules**
- `TOFULL(str)` → `string`

**Arguments**
- `str`: string expression.

**Defaults / optional arguments**
- (TODO)

**Semantics**
- If `str` is null/empty: returns `""`.
- Otherwise: uses VisualBasic `Strings.StrConv(..., Wide, <code page>)`, where `<code page>` is the engine’s current language code page (derived from `useLanguage`).

**Errors & validation**
- Argument type/count errors are rejected by the engine’s function-method argument checker.
- Any runtime exceptions from the underlying `.NET` conversion routine propagate as engine errors.

**Examples**
- `TOFULL("ABC")` → `"ＡＢＣ"`

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:4546 (class `StrChangeStyleMethod`)

## LINEISEMPTY (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new LineIsEmptyMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:4583 (class `LineIsEmptyMethod`)

## REPLACE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new ReplaceMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.String, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.RefString1D | ArgType.AllowConstRef, ArgType.Int }.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.InvalidRegexArg.Text, Name, 2, e.Message))`
  - `throw new CodeEE(string.Format(trerror.ArgIsNotNDStrArray.Text, Name, 3, 1))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:4598 (class `ReplaceMethod`)

## UNICODE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new UnicodeMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.ArgIsOutOfRange.Text, Name, 1, i, 0, 0xFFFF))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:4679 (class `UnicodeMethod`)

## UNICODEBYTE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new UnicodeByteMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:4715 (class `UnicodeByteMethod`)

## CONVERT (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new ConvertIntMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.ArgShouldBeSpecificValue.Text, Name, 2, "2, 8, 10, 16"))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:4735 (class `ConvertIntMethod`)

## ISNUMERIC (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new IsNumericMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:4753 (class `IsNumericMethod`)

## ESCAPE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new EscapeMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:4794 (class `EscapeMethod`)

## ENCODETOUNI (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new EncodeToUniMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.Int }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.ArgIsNegative.Text, Name, 2, position))`
  - `throw new CodeEE(string.Format(trerror.EncodeToUni2ndArgError.Text, Name, position, baseStr))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:4808 (class `EncodeToUniMethod`)

## CHARATU (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new CharAtMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:4850 (class `CharAtMethod`)

## GETLINESTR (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetLineStrMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return exm.Console.getStBar(str)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.ArgIsEmptyString.Text, Name, 1))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:4868 (class `GetLineStrMethod`)

## STRFORM (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new StrFormMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.InvalidFormString.Text, Name, str, e.Message))`
  - `throw new CodeEE(string.Format(trerror.UnexectedFormStringErr.Text, Name, str))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:4886 (class `StrFormMethod`)

## STRJOIN (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new JoinMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.RefAnyArray | ArgType.AllowConstRef, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return VariableEvaluator.GetJoinedStr(p, delimiter, index1, index2)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.ArgIsNegative.Text, Name, 4, index2))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:4943 (class `JoinMethod`)

## GETCONFIG (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetConfigMethod(true)`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.ArgIsEmptyString.Text, Name, 1))`
  - `throw new CodeEE(errMes)`
  - `throw new ExeEE(funcname + "関数:不正な呼び出し")`
  - `throw new CodeEE(string.Format(trerror.InvalidType.Text, Name, "GETCONFIGS"))`
  - `throw new CodeEE(string.Format(trerror.InvalidType.Text, Name, "GETCONFIG"))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5014 (class `GetConfigMethod`)

## GETCONFIGS (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetConfigMethod(false)`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.ArgIsEmptyString.Text, Name, 1))`
  - `throw new CodeEE(errMes)`
  - `throw new ExeEE(funcname + "関数:不正な呼び出し")`
  - `throw new CodeEE(string.Format(trerror.InvalidType.Text, Name, "GETCONFIGS"))`
  - `throw new CodeEE(string.Format(trerror.InvalidType.Text, Name, "GETCONFIG"))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5014 (class `GetConfigMethod`)

## HTML_GETPRINTEDSTR (expression function)
**Summary**
- Returns the HTML-formatted representation of a previously displayed **logical output line**.

**Metadata**
- Implementor: `new HtmlGetPrintedStrMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `false`

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

**Defaults / optional arguments**
- (TODO)

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
- Engine-extracted notes (key operations):
  - `ConsoleDisplayLine[] dispLines = exm.Console.GetDisplayLines(lineNo)`

**Errors & validation**
- If `<lineNo> < 0`, this is a runtime error.
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.ArgIsNegative.Text, Name, 1, lineNo))`

**Examples**
```erabasic
PRINTL "Hello"
PRINTL "World"

; Gets the most recent logical line (the "World" line)
S = HTML_GETPRINTEDSTR(0)
```

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5070 (class `HtmlGetPrintedStrMethod`)

## HTML_POPPRINTINGSTR (expression function)
**Summary**
- Returns (and clears) the current pending print buffer as an HTML string.

**Metadata**
- Implementor: `new HtmlPopPrintingStrMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- `HTML_POPPRINTINGSTR()`

**Signatures / argument rules**
- Signature: `string HTML_POPPRINTINGSTR()`.

**Arguments**
- None.

**Defaults / optional arguments**
- (TODO)

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
- Engine-extracted notes (key operations):
  - `ConsoleDisplayLine[] dispLines = exm.Console.PopDisplayingLines()`

**Errors & validation**
- None.

**Examples**
```erabasic
PRINT "A"
PRINT "B"
S = HTML_POPPRINTINGSTR()
; At this point, the pending buffer is cleared and nothing was displayed.
```

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5108 (class `HtmlPopPrintingStrMethod`)

## HTML_TOPLAINTEXT (expression function)
**Summary**
- Converts an HTML string to plain text by removing tags and expanding character references.

**Metadata**
- Implementor: `new HtmlToPlainTextMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- `HTML_TOPLAINTEXT(html)`

**Signatures / argument rules**
- Signature: `string HTML_TOPLAINTEXT(string html)`.

**Arguments**
- `html`: string expression interpreted as an HTML string.

**Defaults / optional arguments**
- (TODO)

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

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5126 (class `HtmlToPlainTextMethod`)

## HTML_ESCAPE (expression function)
**Summary**
- Escapes a plain-text string for use in HTML strings.

**Metadata**
- Implementor: `new HtmlEscapeMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- `HTML_ESCAPE(text)`

**Signatures / argument rules**
- Signature: `string HTML_ESCAPE(string text)`.

**Arguments**
- `text`: string expression.

**Defaults / optional arguments**
- (TODO)

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

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5139 (class `HtmlEscapeMethod`)

## SPRITECREATED (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new SpriteStateMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new ExeEE("SpriteStateMethod:" + Name + ":異常な分岐")`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5829 (class `SpriteStateMethod`)

## SPRITEWIDTH (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new SpriteStateMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new ExeEE("SpriteStateMethod:" + Name + ":異常な分岐")`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5829 (class `SpriteStateMethod`)

## SPRITEHEIGHT (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new SpriteStateMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new ExeEE("SpriteStateMethod:" + Name + ":異常な分岐")`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5829 (class `SpriteStateMethod`)

## SPRITEMOVE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new SpriteSetPosMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string), typeof(long), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new ExeEE("SpriteStateMethod:" + Name + ":異常な分岐")`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5860 (class `SpriteSetPosMethod`)

## SPRITESETPOS (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new SpriteSetPosMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string), typeof(long), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new ExeEE("SpriteStateMethod:" + Name + ":異常な分岐")`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5860 (class `SpriteSetPosMethod`)

## SPRITEPOSX (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new SpriteStateMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new ExeEE("SpriteStateMethod:" + Name + ":異常な分岐")`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5829 (class `SpriteStateMethod`)

## SPRITEPOSY (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new SpriteStateMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new ExeEE("SpriteStateMethod:" + Name + ":異常な分岐")`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5829 (class `SpriteStateMethod`)

## CLIENTWIDTH (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new ClientSizeMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return exm.Console.ClientWidth`
  - `return exm.Console.ClientHeight`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new ExeEE("ClientSize:" + Name + ":異常な分岐")`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5915 (class `ClientSizeMethod`)

## CLIENTHEIGHT (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new ClientSizeMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return exm.Console.ClientWidth`
  - `return exm.Console.ClientHeight`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new ExeEE("ClientSize:" + Name + ":異常な分岐")`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5915 (class `ClientSizeMethod`)

## GETKEY (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetKeyStateMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `if (!exm.Console.IsActive)//アクティブでないならスルー`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new ExeEE("異常な分岐")`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:6783 (class `GetKeyStateMethod`)

## GETKEYTRIGGERED (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetKeyStateMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `if (!exm.Console.IsActive)//アクティブでないならスルー`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new ExeEE("異常な分岐")`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:6783 (class `GetKeyStateMethod`)

## MOUSEX (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new MousePosMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `case "MOUSEX": return exm.Console.GetMousePosition().X`
  - `case "MOUSEY": return exm.Console.GetMousePosition().Y`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new ExeEE("異常な名前")`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:6810 (class `MousePosMethod`)

## MOUSEY (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new MousePosMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `case "MOUSEX": return exm.Console.GetMousePosition().X`
  - `case "MOUSEY": return exm.Console.GetMousePosition().Y`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new ExeEE("異常な名前")`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:6810 (class `MousePosMethod`)

## MOUSEB (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new MouseButtonMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `bool b = exm.Console.AlwaysRefresh`
  - `Point point = exm.Console.Window.MainPicBox.PointToClient(Control.MousePosition)`
  - `exm.Console.AlwaysRefresh = true`
  - `if (exm.Console.Window.MainPicBox.ClientRectangle.Contains(point))`
  - `exm.Console.MoveMouse(point)`
  - `exm.Console.AlwaysRefresh = b`
  - `if (exm.Console.PointingSring != null)`
  - `if (!exm.Console.PointingSring.IsButton)`
  - `if (exm.Console.PointingSring.IsInteger)`
  - `return exm.Console.PointingSring.Input.ToString()`
  - `return exm.Console.PointingSring.Inputs`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:6829 (class `MouseButtonMethod`)

## ISACTIVE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new IsActiveMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return exm.Console.IsActive ? 1 : 0`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:6861 (class `IsActiveMethod`)

## SAVETEXT (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new SaveTextMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.Any, ArgType.Int, ArgType.Int }; OmitStart = 2.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:6897 (class `SaveTextMethod`)

## LOADTEXT (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new LoadTextMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Any, ArgType.Int, ArgType.Int }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:7006 (class `LoadTextMethod`)

## GCREATED (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GraphicsStateMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`
  - `throw new ExeEE("GraphicsState:" + Name + ":異常な分岐")`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5304 (class `GraphicsStateMethod`)

## GWIDTH (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GraphicsStateMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`
  - `throw new ExeEE("GraphicsState:" + Name + ":異常な分岐")`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5304 (class `GraphicsStateMethod`)

## GHEIGHT (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GraphicsStateMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`
  - `throw new ExeEE("GraphicsState:" + Name + ":異常な分岐")`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5304 (class `GraphicsStateMethod`)

## GGETCOLOR (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GraphicsGetColorMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long), typeof(long), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5372 (class `GraphicsGetColorMethod`)

## SPRITEGETCOLOR (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new SpriteGetColorMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string), typeof(long), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5888 (class `SpriteGetColorMethod`)

## GCREATE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GraphicsCreateMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long), typeof(long), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`
  - `throw new CodeEE(string.Format(trerror.GParamIsNegative.Text, Name, "Width", width))`
  - `throw new CodeEE(string.Format(trerror.GParamTooLarge.Text, Name, "Width", AbstractImage.MAX_IMAGESIZE, width))`
  - `throw new CodeEE(string.Format(trerror.GParamIsNegative.Text, Name, "Height", height))`
  - `throw new CodeEE(string.Format(trerror.GParamTooLarge.Text, Name, "Height", AbstractImage.MAX_IMAGESIZE, height))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5936 (class `GraphicsCreateMethod`)

## GCREATEFROMFILE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GraphicsCreateFromFileMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.String, ArgType.Int }; OmitStart = 2.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5974 (class `GraphicsCreateFromFileMethod`)

## GDISPOSE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GraphicsDisposeMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:6037 (class `GraphicsDisposeMethod`)

## GCLEAR (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GraphicsClearMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.Int }.
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.Int, ArgType.Int, ArgType.Int, ArgType.Int, ArgType.Int }.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:6171 (class `GraphicsClearMethod`)

## GFILLRECTANGLE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GraphicsFillRectangleMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long), typeof(long), typeof(long), typeof(long), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:6220 (class `GraphicsFillRectangleMethod`)

## GDRAWSPRITE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GraphicsDrawSpriteMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.String }.
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.String, ArgType.Int, ArgType.Int }.
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.String, ArgType.Int, ArgType.Int, ArgType.Int, ArgType.Int, ArgType.RefInt2D | ArgType.AllowConstRef }; OmitStart = 6.
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.String, ArgType.Int, ArgType.Int, ArgType.Int, ArgType.Int, ArgType.RefInt3D | ArgType.AllowConstRef }; OmitStart = 6.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:6367 (class `GraphicsDrawSpriteMethod`)

## GSETCOLOR (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GraphicsSetColorMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long), typeof(long), typeof(long), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5398 (class `GraphicsSetColorMethod`)

## GDRAWG (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GraphicsDrawGMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.Int, ArgType.Int, ArgType.Int, ArgType.Int, ArgType.Int, ArgType.Int, ArgType.Int, ArgType.Int, ArgType.Int, ArgType.RefInt2D | ArgType.AllowConstRef }; OmitStart = 10.
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.Int, ArgType.Int, ArgType.Int, ArgType.Int, ArgType.Int, ArgType.Int, ArgType.Int, ArgType.Int, ArgType.Int, ArgType.RefInt3D | ArgType.AllowConstRef }; OmitStart = 10.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:6246 (class `GraphicsDrawGMethod`)

## GDRAWGWITHMASK (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GraphicsDrawGWithMaskMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long), typeof(long), typeof(long), typeof(long), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:6325 (class `GraphicsDrawGWithMaskMethod`)

## GSETBRUSH (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GraphicsSetBrushMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5423 (class `GraphicsSetBrushMethod`)

## GSETFONT (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GraphicsSetFontMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 2.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5446 (class `GraphicsSetFontMethod`)

## GSETPEN (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GraphicsSetPenMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long), typeof(long), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5517 (class `GraphicsSetPenMethod`)

## SPRITECREATE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new SpriteCreateMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.Int }.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.Int, ArgType.Int, ArgType.Int, ArgType.Int, ArgType.Int }.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`
  - `throw new CodeEE(string.Format(trerror.ImgRefOutOfRange.Text, Name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:6061 (class `SpriteCreateMethod`)

## SPRITEDISPOSE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new SpriteDisposeMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:6134 (class `SpriteDisposeMethod`)

## CBGSETG (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new CBGSetGraphicsMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long), typeof(long), typeof(long), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `exm.Console.CBG_SetGraphics(g, p.X, p.Y, (int)z64)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`
  - `throw new CodeEE(string.Format(trerror.ArgIsOutOfRangeExcept.Text, Name, 4, z64, int.MinValue, int.MaxValue, 0))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:6633 (class `CBGSetGraphicsMethod`)

## CBGSETSPRITE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new CBGSetCIMGMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string), typeof(long), typeof(long), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `if (!exm.Console.CBG_SetImage(img, p.X, p.Y, (int)z64))`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.ArgIsOutOfRangeExcept.Text, Name, 4, z64, int.MinValue, int.MaxValue, 0))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:6690 (class `CBGSetCIMGMethod`)

## CBGCLEAR (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new CBGClearMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `exm.Console.CBG_Clear()`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:6552 (class `CBGClearMethod`)

## CBGCLEARBUTTON (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new CBGClearButtonMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `exm.Console.CBG_ClearButton()`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:6595 (class `CBGClearButtonMethod`)

## CBGREMOVERANGE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new CBGRemoveRangeMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `exm.Console.CBG_ClearRange((int)x64, (int)y64)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:6572 (class `CBGRemoveRangeMethod`)

## CBGREMOVEBMAP (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new CBGRemoveBMapMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `exm.Console.CBG_ClearBMap()`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:6614 (class `CBGRemoveBMapMethod`)

## CBGSETBMAPG (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new CBGSetBMapGMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `exm.Console.CBG_SetButtonMap(g)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:6664 (class `CBGSetBMapGMethod`)

## CBGSETBUTTONSPRITE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new CBGSETButtonSpriteMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int, ArgType.Int, ArgType.String }; OmitStart = 6.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `if (!exm.Console.CBG_SetButtonImage((int)b64, imgN, imgB, p.X, p.Y, (int)z64, tooltip))`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`
  - `throw new CodeEE(string.Format(trerror.ArgIsOutOfRangeExcept.Text, Name, 6, z64, int.MinValue, int.MaxValue, 0))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:6722 (class `CBGSETButtonSpriteMethod`)

## GSAVE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GraphicsSaveMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:7104 (class `GraphicsSaveMethod`)

## GLOAD (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GraphicsLoadMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:7141 (class `GraphicsLoadMethod`)

## SPRITEANIMECREATE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new SpriteAnimeCreateMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string), typeof(long), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`
  - `throw new CodeEE(string.Format(trerror.GParamIsNegative.Text, Name, "Width", pos.X))`
  - `throw new CodeEE(string.Format(trerror.GParamTooLarge.Text, Name, "Width", AbstractImage.MAX_IMAGESIZE, pos.X))`
  - `throw new CodeEE(string.Format(trerror.GParamIsNegative.Text, Name, "Height", pos.Y))`
  - `throw new CodeEE(string.Format(trerror.GParamTooLarge.Text, Name, "Height", AbstractImage.MAX_IMAGESIZE, pos.Y))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:6466 (class `SpriteAnimeCreateMethod`)

## SPRITEANIMEADDFRAME (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new SpriteAnimeAddFrameMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string), typeof(long), typeof(long), typeof(long), typeof(long), typeof(long), typeof(long), typeof(long), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:6508 (class `SpriteAnimeAddFrameMethod`)

## SETANIMETIMER (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new SetAnimeTimerMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `exm.Console.setRedrawTimer((int)i64)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.ArgIsOutOfRange.Text, Name, 1, i64, int.MinValue, int.MaxValue))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:6875 (class `SetAnimeTimerMethod`)

## OUTPUTLOG (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new OutputlogMethod()`
- Return type: `Int64`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.Int }; OmitStart = 0.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `exm.Console.OutputLog(filename, hideInfo)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:7627 (class `OutputlogMethod`)

## HTML_STRINGLEN (expression function)
**Summary**
- Measures the display width of an HTML string (using the same layout rules as `HTML_PRINT`).

**Metadata**
- Implementor: `new HtmlStringLenMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

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

**Defaults / optional arguments**
- (TODO)

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

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:31 (class `HtmlStringLenMethod`)

## HTML_SUBSTRING (expression function)
**Summary**
- Splits an HTML string into a prefix that fits within a given display width and the remaining suffix.

**Metadata**
- Implementor: `new HtmlSubStringMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- `HTML_SUBSTRING(html, width)`

**Signatures / argument rules**
- Signature: `string HTML_SUBSTRING(string html, int width)`.
- Also writes results into `RESULTS` (see semantics).

**Arguments**
- `html`: string expression interpreted as an HTML string.
- `width`: integer expression, in half-width character units.

**Defaults / optional arguments**
- (TODO)

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

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:647 (class `HtmlSubStringMethod`)

## HTML_STRINGLINES (expression function)
**Summary**
- Returns how many lines an HTML string would occupy when repeatedly split by a given width (using `HTML_SUBSTRING`).

**Metadata**
- Implementor: `new HtmlStringLinesMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- `HTML_STRINGLINES(html, width)`

**Signatures / argument rules**
- Signature: `int HTML_STRINGLINES(string html, int width)`.

**Arguments**
- `html`: string expression interpreted as an HTML string.
- `width`: integer expression, in half-width character units.

**Defaults / optional arguments**
- (TODO)

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

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:666 (class `HtmlStringLinesMethod`)

## EXISTFILE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new ExistFileMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1255 (class `ExistFileMethod`)

## EXISTVAR (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new ExistVarMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:322 (class `ExistVarMethod`)

## ISDEFINED (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new IsDefinedMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:137 (class `IsDefinedMethod`)

## ENUMFUNCBEGINSWITH (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new EnumNameMethod(EnumNameMethod.EType.Function, EnumNameMethod.EAction.BeginsWith)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.RefString1D }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `output = exm.VEvaluator.RESULTS_ARRAY`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:151 (class `EnumNameMethod`)

## ENUMFUNCENDSWITH (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new EnumNameMethod(EnumNameMethod.EType.Function, EnumNameMethod.EAction.EndsWith)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.RefString1D }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `output = exm.VEvaluator.RESULTS_ARRAY`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:151 (class `EnumNameMethod`)

## ENUMFUNCWITH (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new EnumNameMethod(EnumNameMethod.EType.Function, EnumNameMethod.EAction.With)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.RefString1D }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `output = exm.VEvaluator.RESULTS_ARRAY`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:151 (class `EnumNameMethod`)

## ENUMVARBEGINSWITH (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new EnumNameMethod(EnumNameMethod.EType.Variable, EnumNameMethod.EAction.BeginsWith)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.RefString1D }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `output = exm.VEvaluator.RESULTS_ARRAY`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:151 (class `EnumNameMethod`)

## ENUMVARENDSWITH (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new EnumNameMethod(EnumNameMethod.EType.Variable, EnumNameMethod.EAction.EndsWith)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.RefString1D }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `output = exm.VEvaluator.RESULTS_ARRAY`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:151 (class `EnumNameMethod`)

## ENUMVARWITH (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new EnumNameMethod(EnumNameMethod.EType.Variable, EnumNameMethod.EAction.With)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.RefString1D }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `output = exm.VEvaluator.RESULTS_ARRAY`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:151 (class `EnumNameMethod`)

## ENUMMACROBEGINSWITH (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new EnumNameMethod(EnumNameMethod.EType.Macro, EnumNameMethod.EAction.BeginsWith)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.RefString1D }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `output = exm.VEvaluator.RESULTS_ARRAY`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:151 (class `EnumNameMethod`)

## ENUMMACROENDSWITH (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new EnumNameMethod(EnumNameMethod.EType.Macro, EnumNameMethod.EAction.EndsWith)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.RefString1D }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `output = exm.VEvaluator.RESULTS_ARRAY`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:151 (class `EnumNameMethod`)

## ENUMMACROWITH (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new EnumNameMethod(EnumNameMethod.EType.Macro, EnumNameMethod.EAction.With)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.RefString1D }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `output = exm.VEvaluator.RESULTS_ARRAY`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:151 (class `EnumNameMethod`)

## ENUMFILES (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new EnumFilesMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.Int, ArgType.RefString1D }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `output = exm.VEvaluator.RESULTS_ARRAY`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:223 (class `EnumFilesMethod`)

## GETVAR (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetVarMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.IsNotVar.Text, name))`
  - `throw new CodeEE(string.Format(trerror.IsNotInt.Text, name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:265 (class `GetVarMethod`)

## GETVARS (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetVarsMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.IsNotVar.Text, name))`
  - `throw new CodeEE(string.Format(trerror.IsNotStr.Text, name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:294 (class `GetVarsMethod`)

## SETVAR (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new SetVarMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.Any }.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.IsNotVar.Text, name))`
  - `throw new CodeEE(string.Format(trerror.IsNotInt.Text, name))`
  - `throw new CodeEE(string.Format(trerror.IsNotStr.Text, name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:503 (class `SetVarMethod`)

## VARSETEX (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new VarSetExMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.Any, ArgType.Int, ArgType.Int, ArgType.Int }; OmitStart = 2.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.IsNotVar.Text, name))`
  - `throw new CodeEE(string.Format(trerror.SetStrToInt.Text, name))`
  - `throw new CodeEE(string.Format(trerror.SetIntToStr.Text, name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:541 (class `VarSetExMethod`)

## ARRAYMSORTEX (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new ArrayMultiSortExMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.RefString1D, ArgType.Int, ArgType.Int | ArgType.DisallowVoid }; OmitStart = 2.
- ArgTypeList: ArgTypes = { ArgType.RefInt1D, ArgType.RefString1D, ArgType.Int, ArgType.Int | ArgType.DisallowVoid }; OmitStart = 2.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(err)`
  - `else { throw new ExeEE(trerror.AbnormalArray.Text); }`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:347 (class `ArrayMultiSortExMethod`)

## REGEXPMATCH (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new RegexpMatchMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.Int }; OmitStart = 2.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.RefInt, ArgType.RefString1D }.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `exm.VEvaluator.RESULT_ARRAY[1] = reg.GetGroupNumbers().Length`
  - `if (ret > 0) Output(matches, reg, exm.VEvaluator.RESULTS_ARRAY)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.InvalidRegexArg.Text, Name, 2, e.Message))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:689 (class `RegexpMatchMethod`)

## XML_DOCUMENT (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new XmlDocumentMethod(XmlDocumentMethod.Operation.Create)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Any, ArgType.String }.
- ArgTypeList: ArgTypes = { ArgType.Any }.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var xmlDict = exm.VEvaluator.VariableData.DataXmlDocument`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.XmlGetError.Text, xml, e.Message))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:739 (class `XmlDocumentMethod`)

## XML_RELEASE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new XmlDocumentMethod(XmlDocumentMethod.Operation.Release)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Any, ArgType.String }.
- ArgTypeList: ArgTypes = { ArgType.Any }.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var xmlDict = exm.VEvaluator.VariableData.DataXmlDocument`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.XmlGetError.Text, xml, e.Message))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:739 (class `XmlDocumentMethod`)

## XML_GET (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new XmlGetMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Any, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 2.
- ArgTypeList: ArgTypes = { ArgType.Any, ArgType.String, ArgType.RefString1D, ArgType.Int }; OmitStart = 3.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataXmlDocument`
  - `for (int i = 0; i < Math.Min(nodes.Count, exm.VEvaluator.RESULTS_ARRAY.Length); i++)`
  - `OutPutNode(nodes[i], exm.VEvaluator.RESULTS_ARRAY, i, outputStyle)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.XmlGetError.Text, xml, e.Message))`
  - `throw new CodeEE(string.Format(trerror.XmlGetPathError.Text, path, e.Message))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:54 (class `XmlGetMethod`)

## XML_GET_BYNAME (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new XmlGetMethod(true)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Any, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 2.
- ArgTypeList: ArgTypes = { ArgType.Any, ArgType.String, ArgType.RefString1D, ArgType.Int }; OmitStart = 3.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataXmlDocument`
  - `for (int i = 0; i < Math.Min(nodes.Count, exm.VEvaluator.RESULTS_ARRAY.Length); i++)`
  - `OutPutNode(nodes[i], exm.VEvaluator.RESULTS_ARRAY, i, outputStyle)`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.XmlGetError.Text, xml, e.Message))`
  - `throw new CodeEE(string.Format(trerror.XmlGetPathError.Text, path, e.Message))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:54 (class `XmlGetMethod`)

## XML_SET (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new XmlSetMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.RefString, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataXmlDocument`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.XmlParseError.Text, Name, xml, e.Message))`
  - `throw new CodeEE(string.Format(trerror.XmlXPathParseError.Text, Name, path, e.Message))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:791 (class `XmlSetMethod`)

## XML_SET_BYNAME (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new XmlSetMethod(true)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.RefString, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataXmlDocument`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.XmlParseError.Text, Name, xml, e.Message))`
  - `throw new CodeEE(string.Format(trerror.XmlXPathParseError.Text, Name, path, e.Message))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:791 (class `XmlSetMethod`)

## XML_EXIST (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new XmlDocumentMethod(XmlDocumentMethod.Operation.Check)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Any, ArgType.String }.
- ArgTypeList: ArgTypes = { ArgType.Any }.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var xmlDict = exm.VEvaluator.VariableData.DataXmlDocument`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.XmlGetError.Text, xml, e.Message))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:739 (class `XmlDocumentMethod`)

## XML_TOSTR (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new XmlToStrMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Any }.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var xmlDict = exm.VEvaluator.VariableData.DataXmlDocument`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:875 (class `XmlToStrMethod`)

## XML_ADDNODE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new XmlAddNodeMethod(XmlAddNodeMethod.Operation.Node)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.RefString, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.String, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.RefString, ArgType.String, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataXmlDocument`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.XmlParseError.Text, Name, xml, e.Message))`
  - `throw new CodeEE(string.Format(trerror.XmlXPathParseError.Text, Name, path, e.Message))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:893 (class `XmlAddNodeMethod`)

## XML_ADDNODE_BYNAME (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new XmlAddNodeMethod(XmlAddNodeMethod.Operation.Node, true)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.RefString, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.String, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.RefString, ArgType.String, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataXmlDocument`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.XmlParseError.Text, Name, xml, e.Message))`
  - `throw new CodeEE(string.Format(trerror.XmlXPathParseError.Text, Name, path, e.Message))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:893 (class `XmlAddNodeMethod`)

## XML_REMOVENODE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new XmlRemoveNodeMethod(XmlRemoveNodeMethod.Operation.Node)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.String, ArgType.Int }; OmitStart = 2.
- ArgTypeList: ArgTypes = { ArgType.RefString, ArgType.String, ArgType.Int }; OmitStart = 2.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.Int }; OmitStart = 2.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataXmlDocument`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.XmlParseError.Text, Name, xml, e.Message))`
  - `throw new CodeEE(string.Format(trerror.XmlXPathParseError.Text, Name, path, e.Message))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1048 (class `XmlRemoveNodeMethod`)

## XML_REMOVENODE_BYNAME (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new XmlRemoveNodeMethod(XmlRemoveNodeMethod.Operation.Node, true)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.String, ArgType.Int }; OmitStart = 2.
- ArgTypeList: ArgTypes = { ArgType.RefString, ArgType.String, ArgType.Int }; OmitStart = 2.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.Int }; OmitStart = 2.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataXmlDocument`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.XmlParseError.Text, Name, xml, e.Message))`
  - `throw new CodeEE(string.Format(trerror.XmlXPathParseError.Text, Name, path, e.Message))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1048 (class `XmlRemoveNodeMethod`)

## XML_REPLACE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new XmlReplaceMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Any, ArgType.String }.
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.String, ArgType.String, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.RefString, ArgType.String, ArgType.String, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.String, ArgType.Int }; OmitStart = 3.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataXmlDocument`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.XmlParseError.Text, Name, xml, e.Message))`
  - `throw new CodeEE(string.Format(trerror.XmlXPathParseError.Text, Name, path, e.Message))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1146 (class `XmlReplaceMethod`)

## XML_REPLACE_BYNAME (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new XmlReplaceMethod(true)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Any, ArgType.String }.
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.String, ArgType.String, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.RefString, ArgType.String, ArgType.String, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.String, ArgType.Int }; OmitStart = 3.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataXmlDocument`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.XmlParseError.Text, Name, xml, e.Message))`
  - `throw new CodeEE(string.Format(trerror.XmlXPathParseError.Text, Name, path, e.Message))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1146 (class `XmlReplaceMethod`)

## XML_ADDATTRIBUTE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new XmlAddNodeMethod(XmlAddNodeMethod.Operation.Attribute)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.RefString, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.String, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.RefString, ArgType.String, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataXmlDocument`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.XmlParseError.Text, Name, xml, e.Message))`
  - `throw new CodeEE(string.Format(trerror.XmlXPathParseError.Text, Name, path, e.Message))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:893 (class `XmlAddNodeMethod`)

## XML_ADDATTRIBUTE_BYNAME (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new XmlAddNodeMethod(XmlAddNodeMethod.Operation.Attribute, true)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.RefString, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.String, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.RefString, ArgType.String, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataXmlDocument`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.XmlParseError.Text, Name, xml, e.Message))`
  - `throw new CodeEE(string.Format(trerror.XmlXPathParseError.Text, Name, path, e.Message))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:893 (class `XmlAddNodeMethod`)

## XML_REMOVEATTRIBUTE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new XmlRemoveNodeMethod(XmlRemoveNodeMethod.Operation.Attribute)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.String, ArgType.Int }; OmitStart = 2.
- ArgTypeList: ArgTypes = { ArgType.RefString, ArgType.String, ArgType.Int }; OmitStart = 2.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.Int }; OmitStart = 2.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataXmlDocument`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.XmlParseError.Text, Name, xml, e.Message))`
  - `throw new CodeEE(string.Format(trerror.XmlXPathParseError.Text, Name, path, e.Message))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1048 (class `XmlRemoveNodeMethod`)

## XML_REMOVEATTRIBUTE_BYNAME (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new XmlRemoveNodeMethod(XmlRemoveNodeMethod.Operation.Attribute, true)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.String, ArgType.Int }; OmitStart = 2.
- ArgTypeList: ArgTypes = { ArgType.RefString, ArgType.String, ArgType.Int }; OmitStart = 2.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.Int }; OmitStart = 2.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataXmlDocument`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.XmlParseError.Text, Name, xml, e.Message))`
  - `throw new CodeEE(string.Format(trerror.XmlXPathParseError.Text, Name, path, e.Message))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1048 (class `XmlRemoveNodeMethod`)

## MAP_CREATE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new MapManagementMethod(MapManagementMethod.Operation.Create)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataStringMaps`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1780 (class `MapManagementMethod`)

## MAP_EXIST (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new MapManagementMethod(MapManagementMethod.Operation.Check)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataStringMaps`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1780 (class `MapManagementMethod`)

## MAP_RELEASE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new MapManagementMethod(MapManagementMethod.Operation.Release)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataStringMaps`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1780 (class `MapManagementMethod`)

## MAP_GET (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new MapGetStrMethod(MapGetStrMethod.Operation.Get)`
- Return type: `string`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: multiple `argumentTypeArray` assignments detected (name/branch dependent).
- `argumentTypeArray = [typeof(string), typeof(string)]`.
- `argumentTypeArray = [typeof(string)]`.
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.Int }; OmitStart = 1.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.RefString1D, ArgType.Int }.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataStringMaps`
  - `array = exm.VEvaluator.RESULTS_ARRAY`
  - `exm.VEvaluator.RESULT = sMap.Keys.Count`
  - `return arguments.Count == 2 ? exm.VEvaluator.RESULTS : ""`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1847 (class `MapGetStrMethod`)

## MAP_CLEAR (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new MapDataOperationMethod(MapDataOperationMethod.Operation.Clear)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: multiple `argumentTypeArray` assignments detected (name/branch dependent).
- `argumentTypeArray = [typeof(string), typeof(string), typeof(string)]`.
- `argumentTypeArray = [typeof(string), typeof(string)]`.
- `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataStringMaps`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1806 (class `MapDataOperationMethod`)

## MAP_SIZE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new MapDataOperationMethod(MapDataOperationMethod.Operation.Size)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: multiple `argumentTypeArray` assignments detected (name/branch dependent).
- `argumentTypeArray = [typeof(string), typeof(string), typeof(string)]`.
- `argumentTypeArray = [typeof(string), typeof(string)]`.
- `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataStringMaps`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1806 (class `MapDataOperationMethod`)

## MAP_HAS (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new MapDataOperationMethod(MapDataOperationMethod.Operation.Has)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: multiple `argumentTypeArray` assignments detected (name/branch dependent).
- `argumentTypeArray = [typeof(string), typeof(string), typeof(string)]`.
- `argumentTypeArray = [typeof(string), typeof(string)]`.
- `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataStringMaps`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1806 (class `MapDataOperationMethod`)

## MAP_SET (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new MapDataOperationMethod(MapDataOperationMethod.Operation.Set)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: multiple `argumentTypeArray` assignments detected (name/branch dependent).
- `argumentTypeArray = [typeof(string), typeof(string), typeof(string)]`.
- `argumentTypeArray = [typeof(string), typeof(string)]`.
- `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataStringMaps`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1806 (class `MapDataOperationMethod`)

## MAP_REMOVE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new MapDataOperationMethod(MapDataOperationMethod.Operation.Remove)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: multiple `argumentTypeArray` assignments detected (name/branch dependent).
- `argumentTypeArray = [typeof(string), typeof(string), typeof(string)]`.
- `argumentTypeArray = [typeof(string), typeof(string)]`.
- `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataStringMaps`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1806 (class `MapDataOperationMethod`)

## MAP_GETKEYS (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new MapGetStrMethod(MapGetStrMethod.Operation.GetKeys)`
- Return type: `string`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: multiple `argumentTypeArray` assignments detected (name/branch dependent).
- `argumentTypeArray = [typeof(string), typeof(string)]`.
- `argumentTypeArray = [typeof(string)]`.
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.Int }; OmitStart = 1.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.RefString1D, ArgType.Int }.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataStringMaps`
  - `array = exm.VEvaluator.RESULTS_ARRAY`
  - `exm.VEvaluator.RESULT = sMap.Keys.Count`
  - `return arguments.Count == 2 ? exm.VEvaluator.RESULTS : ""`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1847 (class `MapGetStrMethod`)

## MAP_TOXML (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new MapGetStrMethod(MapGetStrMethod.Operation.ToXml)`
- Return type: `string`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: multiple `argumentTypeArray` assignments detected (name/branch dependent).
- `argumentTypeArray = [typeof(string), typeof(string)]`.
- `argumentTypeArray = [typeof(string)]`.
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.Int }; OmitStart = 1.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.RefString1D, ArgType.Int }.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataStringMaps`
  - `array = exm.VEvaluator.RESULTS_ARRAY`
  - `exm.VEvaluator.RESULT = sMap.Keys.Count`
  - `return arguments.Count == 2 ? exm.VEvaluator.RESULTS : ""`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1847 (class `MapGetStrMethod`)

## MAP_FROMXML (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new MapFromXmlMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string), typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataStringMaps`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.XmlParseError.Text, Name, xml, e.Message))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1930 (class `MapFromXmlMethod`)

## DT_CREATE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new DataTableManagementMethod(DataTableManagementMethod.Operation.Create)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: multiple `argumentTypeArray` assignments detected (name/branch dependent).
- `argumentTypeArray = [typeof(string), typeof(long)]`.
- `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataDataTables`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1270 (class `DataTableManagementMethod`)

## DT_EXIST (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new DataTableManagementMethod(DataTableManagementMethod.Operation.Check)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: multiple `argumentTypeArray` assignments detected (name/branch dependent).
- `argumentTypeArray = [typeof(string), typeof(long)]`.
- `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataDataTables`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1270 (class `DataTableManagementMethod`)

## DT_RELEASE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new DataTableManagementMethod(DataTableManagementMethod.Operation.Release)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: multiple `argumentTypeArray` assignments detected (name/branch dependent).
- `argumentTypeArray = [typeof(string), typeof(long)]`.
- `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataDataTables`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1270 (class `DataTableManagementMethod`)

## DT_NOCASE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new DataTableManagementMethod(DataTableManagementMethod.Operation.Case)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: multiple `argumentTypeArray` assignments detected (name/branch dependent).
- `argumentTypeArray = [typeof(string), typeof(long)]`.
- `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataDataTables`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1270 (class `DataTableManagementMethod`)

## DT_CLEAR (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new DataTableManagementMethod(DataTableManagementMethod.Operation.Clear)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: multiple `argumentTypeArray` assignments detected (name/branch dependent).
- `argumentTypeArray = [typeof(string), typeof(long)]`.
- `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataDataTables`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1270 (class `DataTableManagementMethod`)

## DT_COLUMN_ADD (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new DataTableColumnManagementMethod(DataTableColumnManagementMethod.Operation.Create)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string), typeof(string)]`.
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.Any, ArgType.Int }; OmitStart = 2.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.RefString1D }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataDataTables`
  - `else output = exm.VEvaluator.RESULTS_ARRAY`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.UnsupportedType.Text, Name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1325 (class `DataTableColumnManagementMethod`)

## DT_COLUMN_NAMES (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new DataTableColumnManagementMethod(DataTableColumnManagementMethod.Operation.Names)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string), typeof(string)]`.
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.Any, ArgType.Int }; OmitStart = 2.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.RefString1D }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataDataTables`
  - `else output = exm.VEvaluator.RESULTS_ARRAY`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.UnsupportedType.Text, Name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1325 (class `DataTableColumnManagementMethod`)

## DT_COLUMN_EXIST (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new DataTableColumnManagementMethod(DataTableColumnManagementMethod.Operation.Check)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string), typeof(string)]`.
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.Any, ArgType.Int }; OmitStart = 2.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.RefString1D }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataDataTables`
  - `else output = exm.VEvaluator.RESULTS_ARRAY`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.UnsupportedType.Text, Name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1325 (class `DataTableColumnManagementMethod`)

## DT_COLUMN_REMOVE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new DataTableColumnManagementMethod(DataTableColumnManagementMethod.Operation.Remove)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string), typeof(string)]`.
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.Any, ArgType.Int }; OmitStart = 2.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.RefString1D }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataDataTables`
  - `else output = exm.VEvaluator.RESULTS_ARRAY`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.UnsupportedType.Text, Name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1325 (class `DataTableColumnManagementMethod`)

## DT_COLUMN_LENGTH (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new DataTableLengthMethod(DataTableLengthMethod.Operation.Column)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataDataTables`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1512 (class `DataTableLengthMethod`)

## DT_ROW_ADD (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new DataTableRowSetMethod(DataTableRowSetMethod.Operation.Add)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.VariadicString, ArgType.VariadicAny }; OmitStart = 1; MatchVariadicGroup = true.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.RefString1D, ArgType.RefAny1D, ArgType.Int }.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.Int, ArgType.VariadicString, ArgType.VariadicAny }; MatchVariadicGroup = true.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.Int, ArgType.RefString1D, ArgType.RefAny1D, ArgType.Int }.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataDataTables`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.DTCanNotEditIdColumn.Text, Name, key))`
  - `throw new CodeEE(string.Format(trerror.DTLackOfNamedColumn.Text, Name, key, name))`
  - `throw new CodeEE(string.Format(trerror.DTInvalidDataType.Text, Name, key, name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1393 (class `DataTableRowSetMethod`)

## DT_ROW_SET (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new DataTableRowSetMethod(DataTableRowSetMethod.Operation.Set)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.VariadicString, ArgType.VariadicAny }; OmitStart = 1; MatchVariadicGroup = true.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.RefString1D, ArgType.RefAny1D, ArgType.Int }.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.Int, ArgType.VariadicString, ArgType.VariadicAny }; MatchVariadicGroup = true.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.Int, ArgType.RefString1D, ArgType.RefAny1D, ArgType.Int }.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataDataTables`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.DTCanNotEditIdColumn.Text, Name, key))`
  - `throw new CodeEE(string.Format(trerror.DTLackOfNamedColumn.Text, Name, key, name))`
  - `throw new CodeEE(string.Format(trerror.DTInvalidDataType.Text, Name, key, name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1393 (class `DataTableRowSetMethod`)

## DT_ROW_REMOVE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new DataTableRowRemoveMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.Int }.
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.RefInt1D, ArgType.Int }.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataDataTables`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1531 (class `DataTableRowRemoveMethod`)

## DT_ROW_LENGTH (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new DataTableLengthMethod(DataTableLengthMethod.Operation.Row)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataDataTables`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1512 (class `DataTableLengthMethod`)

## DT_CELL_GET (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new DataTableCellGetMethod(DataTableCellGetMethod.Operation.Get)`
- Return type: (see engine implementation)
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.Int, ArgType.String, ArgType.Int }; OmitStart = 3.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataDataTables`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1569 (class `DataTableCellGetMethod`)

## DT_CELL_ISNULL (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new DataTableCellGetMethod(DataTableCellGetMethod.Operation.IsNull)`
- Return type: (see engine implementation)
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.Int, ArgType.String, ArgType.Int }; OmitStart = 3.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataDataTables`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1569 (class `DataTableCellGetMethod`)

## DT_CELL_GETS (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new DataTableCellGetMethod(DataTableCellGetMethod.Operation.Gets)`
- Return type: (see engine implementation)
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.Int, ArgType.String, ArgType.Int }; OmitStart = 3.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataDataTables`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1569 (class `DataTableCellGetMethod`)

## DT_CELL_SET (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new DataTableCellSetMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.Int, ArgType.String, ArgType.Any, ArgType.Int }; OmitStart = 3.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataDataTables`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1637 (class `DataTableCellSetMethod`)

## DT_SELECT (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new DataTableSelectMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.String, ArgType.RefInt1D }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataDataTables`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1679 (class `DataTableSelectMethod`)

## DT_TOXML (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new DataTableToXmlMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.RefString }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataDataTables`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1715 (class `DataTableToXmlMethod`)

## DT_FROMXML (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new DataTableFromXmlMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string), typeof(string), typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `var dict = exm.VEvaluator.VariableData.DataDataTables`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1745 (class `DataTableFromXmlMethod`)

## MOVETEXTBOX (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new MoveTextBoxMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long), typeof(long), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `if (resume) exm.Console.Window.ResetTextBoxPos()`
  - `else exm.Console.Window.SetTextBoxPos(`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1969 (class `MoveTextBoxMethod`)

## RESUMETEXTBOX (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new MoveTextBoxMethod(true)`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long), typeof(long), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `if (resume) exm.Console.Window.ResetTextBoxPos()`
  - `else exm.Console.Window.SetTextBoxPos(`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:1969 (class `MoveTextBoxMethod`)

## EXISTSOUND (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new ExistSoundMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:7196 (class `ExistSoundMethod`)

## EXISTFUNCTION (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new ExistFunctionMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.Int }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:7217 (class `ExistFunctionMethod`)

## GDRAWGWITHROTATE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GraphicsDrawGWithRotateMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.Int, ArgType.Int, ArgType.Int, ArgType.Int }; OmitStart = 3.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5737 (class `GraphicsDrawGWithRotateMethod`)

## GDRAWTEXT (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GraphicsDrawStringMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 2.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `long[] resultArray = exm.VEvaluator.RESULT_ARRAY`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5567 (class `GraphicsDrawStringMethod`)

## GGETFONT (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GraphicsStateStrMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`
  - `throw new ExeEE("GraphicsState:" + Name + ":Abnormal branching")`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5346 (class `GraphicsStateStrMethod`)

## GGETFONTSIZE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GraphicsStateMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`
  - `throw new ExeEE("GraphicsState:" + Name + ":異常な分岐")`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5304 (class `GraphicsStateMethod`)

## GGETFONTSTYLE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GraphicsStateMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`
  - `throw new ExeEE("GraphicsState:" + Name + ":異常な分岐")`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5304 (class `GraphicsStateMethod`)

## GGETTEXTSIZE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GraphicsGetTextSizeMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.Int, ArgType.Int }; OmitStart = 3.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `long[] resultArray = exm.VEvaluator.RESULT_ARRAY`

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5640 (class `GraphicsGetTextSizeMethod`)

## GGETBRUSH (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GraphicsStateMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`
  - `throw new ExeEE("GraphicsState:" + Name + ":異常な分岐")`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5304 (class `GraphicsStateMethod`)

## GGETPEN (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GraphicsStateMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`
  - `throw new ExeEE("GraphicsState:" + Name + ":異常な分岐")`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5304 (class `GraphicsStateMethod`)

## GGETPENWIDTH (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GraphicsStateMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`
  - `throw new ExeEE("GraphicsState:" + Name + ":異常な分岐")`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5304 (class `GraphicsStateMethod`)

## GETMEMORYUSAGE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetUsingMemoryMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:7276 (class `GetUsingMemoryMethod`)

## CLEARMEMORY (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new ClearMemoryMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:7294 (class `ClearMemoryMethod`)

## GETTEXTBOX (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetTextBoxMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `return exm.Console.Window.TextBox.Text`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:7317 (class `GetTextBoxMethod`)

## SETTEXTBOX (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new ChangeTextBoxMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(string)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `exm.Console.Window.ChangeTextBox(arguments[0].GetStrValue(exm))`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:7330 (class `ChangeTextBoxMethod`)

## ERDNAME (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new ErdNameMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `true`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.RefAny | ArgType.AllowConstRef, ArgType.Int, ArgType.Int }; OmitStart = 2.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `if (exm.VEvaluator.Constant.TryIntegerToKeyword(out string ret, value, varname))`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:7346 (class `ErdNameMethod`)

## SPRITEDISPOSEALL (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new SpriteDisposeAllMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:6153 (class `SpriteDisposeAllMethod`)

## GDRAWLINE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GraphicsDrawLineMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long), typeof(long), typeof(long), typeof(long), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5806 (class `GraphicsDrawLineMethod`)

## GETDISPLAYLINE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetDisplayLineMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int }.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `if (num < 0 || num >= exm.Console.DisplayLineList.Count)`
  - `return exm.Console.DisplayLineList[(int)num].ToString()`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:7380 (class `GetDisplayLineMethod`)

## GDASHSTYLE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GraphicsSetDashStyleMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`
- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = [typeof(long), typeof(long), typeof(long)]`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.GDIPlusOnly.Text, Name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:5543 (class `GraphicsSetDashStyleMethod`)

## GETDOINGFUNCTION (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetDoingFunctionMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArray = []`.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `LogicalLine line = exm.Process.GetScaningLine()`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:7404 (class `GetDoingFunctionMethod`)

## FLOWINPUT (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new FlowInputMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.Int, ArgType.Int, ArgType.Int }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `exm.Process.flowinputDef = arguments[0].GetIntValue(exm)`
  - `exm.Process.flowinput = arguments[1].GetIntValue(exm) != 0 ? true : false`
  - `exm.Process.flowinputCanSkip = arguments[2].GetIntValue(exm) != 0 ? true : false`
  - `exm.Process.flowinputForceSkip = arguments[3].GetIntValue(exm) != 0 ? true : false`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:7422 (class `FlowInputMethod`)

## FLOWINPUTS (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new FlowInputsMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.String }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- Engine-extracted notes (key operations):
  - `exm.Process.flowinputString = arguments[0].GetIntValue(exm) != 0 ? true : false`
  - `exm.Process.flowinputDefString = arguments[1].GetStrValue(exm)`

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:7445 (class `FlowInputsMethod`)

## GETMETH (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetMethMethod()`
- Return type: `Int64`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.Int, ArgType.VariadicAny }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.NotDefinedUserFunc.Text, name))`
  - `throw new CodeEE(string.Format(trerror.IsNotInt.Text, name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:7467 (class `GetMethMethod`)

## GETMETHS (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new GetMethsMethod()`
- Return type: `string`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.String, ArgType.String, ArgType.VariadicAny }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- Engine-extracted notes (throws/errors):
  - `throw new CodeEE(string.Format(trerror.NotDefinedUserFunc.Text, name))`
  - `throw new CodeEE(string.Format(trerror.IsNotStr.Text, name))`

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:7498 (class `GetMethsMethod`)

## EXISTMETH (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new ExistMethMethod()`
- Return type: `Int64`
- Constant folding (`CanRestructure`): `true`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: custom check (no `argumentTypeArray`/`argumentTypeArrayEx` assignment detected).

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:7528 (class `ExistMethMethod`)

## BITMAP_CACHE_ENABLE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new BitmapCacheEnableMethod()`
- Return type: `long`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:7567 (class `BitmapCacheEnableMethod`)

## HOTKEY_STATE (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new HotkeyStateMethod()`
- Return type: `Int64`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int, ArgType.Int }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:7588 (class `HotkeyStateMethod`)

## HOTKEY_STATE_INIT (expression function)
**Summary**
- (TODO)

**Metadata**
- Implementor: `new HotkeyStateInitMethod()`
- Return type: `Int64`
- Constant folding (`CanRestructure`): `false`

**Syntax**
- (TODO)

**Signatures / argument rules**
- Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).
- ArgTypeList: ArgTypes = { ArgType.Int }; OmitStart = 1.

**Arguments**
- (TODO)

**Defaults / optional arguments**
- (TODO)

**Semantics**
- (TODO)

**Errors & validation**
- (TODO)

**Examples**
- (TODO)

**Engine references (fact-check)**
- Registration: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs` (dictionary `methodList`)
- Implementation: `emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs`:7608 (class `HotkeyStateInitMethod`)
