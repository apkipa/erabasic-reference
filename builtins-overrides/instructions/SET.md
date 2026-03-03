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

**Progress state**
- complete
