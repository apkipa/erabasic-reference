# Expressions (numeric, string, operators, FORM)

EraBasic has:

- **Numeric expressions** (evaluate to `Int64` / `long`)
- **String expressions** (evaluate to `string`)

Many commands accept a **raw/simple string argument** rather than a string expression. This affects:

- whether `%...%` / `{...}` is treated as formatting (FORM) or as literal text
- whether `;` starts a comment or is treated as part of the string

## Type system and “required type” contexts (engine-accurate)

The expression evaluator is strictly typed:

- Numeric expressions have type `long` (`Int64`).
- String expressions have type `string`.
- There is **no array value type** in the expression system. Arrays exist as *variable storage*; expressions can read/write **array elements**, but cannot produce “an array value” (no array literals, no array return values, no passing arrays as expression values).
- There is no general implicit conversion between numeric and string expression types.

“Boolean” values are numeric:

- Conditions are `long` values where `0` is false and any non-zero is true.
- Comparisons (`== != < > <= >=`) return `0` or `1`.
- Logical operators (`&& || !& !| ^^` and unary `!`) return `0` or `1`.
- Bitwise operators (`& | ^ ~ << >>`) return numeric bitwise results (not restricted to `0/1`).

### Contexts that require numeric (`long`) expressions

In core language constructs, these positions require `long` (string is a type error):

- Control-flow conditions: `IF`, `ELSEIF`, `SIF`, `WHILE`, `LOOP` (the `LOOP <cond>` part of `DO ... LOOP <cond>`).
- Numeric ternary condition and branches: `cond ? a # b` requires `cond`, `a`, and `b` to all be numeric.
- Most numeric-only operands such as shift counts and arithmetic operands (unless an operator explicitly supports strings; see below).

If a context requires numeric, the engine throws an “expression result is not numeric” error when given a string.

### Contexts that require string (`string`) expressions

- String ternary: `\@cond ? a # b\@` requires numeric `cond` and string branches `a` and `b`.
- String assignment with `'=` requires a string expression on the RHS.

### The only “mixed-type” operator

The binary `*` operator also supports string repetition:

- `string * long` and `long * string` → `string`
- The multiplier must satisfy `0 <= n < 10000`.

Invalid mixes (engine rejects these):

- `string + long` or `long + string`
- comparing `string` with `long`

### Config-controlled conversion (user-function arguments only)

One notable conversion path exists for user-defined function argument binding:

- Passing `long` to a `string` formal parameter is rejected unless `CompatiFuncArgAutoConvert=YES`, in which case the engine wraps it as `TOSTR(long, ...)`.
- Passing `string` to a `long` formal parameter is always rejected.

### More required-type contexts (beyond plain expressions)

These rules are enforced around expression evaluation by the loader and/or runtime:

- **Indexing (`VAR:...`)**: index positions are numeric.
  - Some built-in variables accept *string keys* in specific index positions (CSV-name indexing); in those positions a string is converted to an integer index via name tables.
  - This is not a general “string index” feature. See `variables.md` and `string-key-indexing.md`.
- **`SELECTCASE` typing**:
  - integer `SELECTCASE` → each `CASE` condition expression must be integer
  - string `SELECTCASE` → each `CASE` condition expression (including `IS ...` and `... TO ...` bounds) must be string
  - mixed int/string cases are errors
  - string comparisons are ordinal and case-sensitive (not affected by `IgnoreCase`)
  See `control-flow.md` for the full `CASE` forms (`IS` / `TO`) and selection semantics.
- **Assignments**:
  - numeric variables: RHS must be numeric expressions
  - string variables:
    - `'=`, `+=`, `*=` parse the RHS as a normal expression (type depends on operator)
    - `=` parses the RHS as a formatted string (FORM) token stream rather than a string expression
  See “Assignment” below and `formatted-strings.md`.

## Arrays and indexing in expressions (what “array support” really means)

EraBasic has many array variables (including multi-dimensional and per-character arrays), but Emuera’s expression language itself remains **scalar**:

- An expression evaluates to exactly one `long` or one `string`.
- “Using an array in an expression” means **reading/writing one array cell** via a variable term with `:` indices (e.g. `ABL:0`, `CFLAG:TARGET:1`).
- Built-ins that “take an array” (e.g. `ARRAYSHIFT`) are not taking an array *value*; they take a **variable term** whose identifier refers to an array variable, and the instruction’s implementation operates on the variable’s underlying storage.

### Variable terms and `:` indices

Variable terms have the shape:

- `NAME` (optionally `NAME@subName`) followed by up to 3 `:` arguments.
- Each `:` argument is an expression, but it is ultimately converted to a numeric index:
  - normally: numeric expression → numeric index
  - for specific CSV-backed variables/positions: string key → numeric index via name tables (this is targeted, not general “string indexing”)

### Omitted indices are not “the whole array”

Because variable parsing performs argument inference, “omitting indices” does **not** generally produce an “array reference”:

- For **non-character 1D arrays**, `NAME` is treated as `NAME:0` (except `RAND`, which can reject omission depending on config).
- For **character-data 1D arrays**, the value form expects two indices: `[chara, index]`. If `SystemNoTarget=NO`, a single written index is treated as the **element index** and the character defaults to `TARGET`.
- For **2D/3D arrays (character or not)**, omitting indices may parse to a special “no-arg variable term” that throws a “missing variable argument” error if evaluated as a value.

This matters for array-manipulating built-ins:

- Many such instructions only need to know *which underlying array storage* to operate on, and will ignore some indices.
- For example, Emuera’s `ARRAYSHIFT` operates on a **1D array storage**; for a per-character 1D array, the *character selector* index matters, but the *element index* is effectively a dummy.

### L-value vs r-value: where array-ness is visible

- In **r-value** contexts (most expressions), a variable term produces a scalar cell value (after index evaluation and bounds checks).
- In **l-value** contexts (assignment LHS, `++/--`, and built-ins that require a “changeable variable”), the parser still builds a variable term, but additional rules apply:
  - the term must be a variable (not a literal)
  - the variable must not be `CONST`
  - the instruction may impose extra constraints (e.g. “must be 1D array”, “must be numeric”, etc.)

Engine references (fact-check):

- Variable argument inference and “no-arg variable term”: `emuera.em/Emuera/Runtime/Script/Statements/Variable/VariableParser.cs`
- “No-arg term” throws on value access: `emuera.em/Emuera/Runtime/Script/Statements/Variable/VariableTerm.cs` (`VariableNoArgTerm`)

## Operators

### Core operator set

Numeric and string expressions share some operators, but not all combinations are valid (e.g., adding a number to a string is not allowed).

Highlights:

- Unary: `~` (bitwise NOT), `!` (logical NOT)
- Arithmetic: `+ - * / %`
- Shift: `<< >>`
- Comparison: `< > <= >= == !=`
- Logical/bitwise families:
  - bitwise: `& | ^`
  - logical (short-circuit): `&& || !& !|`
  - logical NAND/NOR: `!& !|`
  - logical XOR: `^^`
- Ternary:
  - numeric: `cond ? a # b`
  - string: `\@cond ? a # b\@` (if `#` is omitted, the engine warns and treats the else-branch as `""`)
- Increment/decrement statement operators: `++ --`

### Operator typing summary (practical)

- Unary `+ - ~` require numeric and return numeric.
- Unary `!` requires numeric and returns numeric (`0` or `1`).
- Arithmetic `+ - * / %`:
  - `long op long` → `long`
  - additionally for `*`: `string * long` / `long * string` → `string` (with `0 <= n < 10000`)
- Shifts `<< >>` require numeric operands and return numeric.
- Bitwise `& | ^` require numeric operands and return numeric.
- Comparisons:
  - `long cmp long` → `long` (`0`/`1`)
  - `string cmp string` → `long` (`0`/`1`)
- Logical operators (`&& || !& !| ^^`) require numeric operands and return `0`/`1`.

### `++` / `--` semantics (engine-accurate)

`++` and `--` are available both:

- as **statement forms** (a whole line), and
- as **expression operators** inside larger expressions.

They apply only to **integer** (numeric) variable terms and have side effects:

- Prefix `++X` / `--X` increments/decrements `X` and yields the **new** value.
- Postfix `X++` / `X--` increments/decrements `X` and yields the **old** value.

They are rejected if the operand is not a variable term or is a const variable.

### String operations supported by the engine

The engine supports several string operators:

- `+` — string concatenation (string + string)
- `*` — string repetition (string * integer), with a multiplier constraint `0 <= n < 10000`

Comparisons such as `==`, `!=`, `<`, `<=`, `>` and `>=` can compare strings to strings (lexicographic).

Implementation note: string comparisons are ordinal (byte/Unicode code-point order) and are not affected by `IgnoreCase`.

Invalid mixes (engine rejects these):

- comparing a number and a string
- using `+` to add/concatenate a number and a string

### Precedence (practical summary)

The engine’s effective precedence (high → low) can be approximated as:

1. unary `~ !`
2. `* / %`
3. `+ -`
4. `<< >>`
5. `< > <= >=`
6. `== !=`
7. `& | ^` (bitwise)
8. `&& || !& !| ^^` (logical family, with short-circuit where applicable)
9. ternary `? ... # ...`

If you are unsure, use parentheses.

## Assignment

### Numeric assignment

Uses `=` and compound assignments (`+=`, `-=`, etc.) where supported.

### String assignment: `=` vs `'=`

Emuera supports a distinct assignment operator for string expressions:

    STR '= "hello"
    STR '= TSTR:0 + " world"

Engine-accurate rule:

- For **string variables**, `=` does **not** parse a normal string expression. Instead, it parses the right-hand side as a *formatted string (FORM)* token stream (similar to `PRINTFORM` scanning).
- For **string-expression assignment**, you must use `'=`.

This is also required for “batch assignment” to string arrays when you want to assign multiple string elements at once, because the comma-separated list is a string-expression list in that context.

### String compound assignments

For string variables, these compound assignments are supported:

- `+=` — concatenation (string + string)
- `*=` — repetition (string * int)

They parse the RHS as a normal expression (like `'=`, not like `=`), and require exactly one RHS expression (no comma list).

### Config option: `SystemIgnoreStringSet`

If `SystemIgnoreStringSet=YES`, the engine rejects `STR = ...` (string `=` assignment) with a warning/error.

This does **not** prohibit `STR '= ...`, `STR += ...`, or `STR *= ...`.

## FORM syntax vs string expressions

### FORM (formatted/interpolated strings)

Many `PRINTFORM`-family commands use FORM syntax (interpolation):

- `%...%` — embed variables/expressions in output
- `{...}` — embed numeric expressions in output (often also supports width/alignment extensions in Emuera)

Emuera also supports width/alignment extensions in some FORM placeholders, for example:

- `{X,10}` — print `X` in a field of width 10
- `{X,10,LEFT}` — left-aligned
- `%STR:0,10%` — similar, for string output

Width calculations for `%...%` placeholders use `useLanguage`-dependent byte-count adjustments (typically treating many full-width characters as width 2 in common JP code pages). See `formatted-strings.md` for the exact algorithm.

### FORM in string-expression contexts: `@"..."`

In string expressions, using FORM syntax directly (e.g. `%VAR%`) can be an error. To embed FORM content inside a string expression, use the formatted-string literal form:

    PRINTS @"%STR:0%!"

In some cases, if the entire content is only a string-ternary `\@...\@`, `@"..."` can be omitted.

This `@"..."` form is an engine extension specifically meant for “FORM inside string expressions”.

For a strict, engine-accurate specification of FORM scanning, escapes, placeholder typing, width/alignment rules, triple symbols, and `\@...\@`, see:

- `formatted-strings.md`

## Notes on evaluation order

Evaluation is generally left-to-right.

Short-circuiting operators (engine-accurate):

- `&&`, `||`, `!&`, `!|` are short-circuiting (the right operand may not be evaluated).
- ternary `? ... # ...` is short-circuiting (the unchosen branch is not evaluated).
- `^^` (logical XOR) is **not** short-circuiting (both operands are evaluated).

Important: the engine performs expression “restructuring” during load/parse in many places (constant folding and normalization).
This can cause some errors (e.g. divide-by-zero in a fully constant subexpression) to surface at load time rather than at runtime.
For reimplementation, see `expression-grammar.md` and treat constant folding as part of the language-as-implemented.

In expression functions (`#FUNCTION/#FUNCTIONS`), avoid side effects in expressions anyway: optimizer/restructure steps can still move work across phases, and short-circuiting can skip calls.

## Formal grammar (recommended for reimplementation)

For a formal EBNF of expressions (including operator set and precedence as implemented), see:

- `expression-grammar.md`

## Fact-check cross-refs (optional)

- `emuera.em.doc/docs/Emuera/operand.en.md`
- `emuera.em.doc/docs/Emuera/expression.en.md`
- `emuera.em.doc/docs/Emuera/user_defined_in_expression_function.en.md`
- Implementation reference: `emuera.em/Emuera/Runtime/Script/Parser/LexicalAnalyzer.cs`
- Operator semantics and short-circuiting: `emuera.em/Emuera/Runtime/Script/Statements/Expression/OperatorMethod.cs`
