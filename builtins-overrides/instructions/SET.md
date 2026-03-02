**Summary**
- Internal pseudo-instruction used by the engine to represent **assignment statements**; scripts do not write a `SET` keyword.
- Implements scalar assignment, compound assignment (`+=`, `-=`, etc.), `++/--`, and comma-list assignment into arrays.

**Syntax**
- Scalar assignment (int): `<intVarTerm> = <int expr>`
- Scalar assignment (string, formatted): `<strVarTerm> = <FORM string>` (subject to `SystemIgnoreStringSet`)
- Scalar assignment (string, expression): `<strVarTerm> '= <string expr>`
- Compound assignment (examples): `<intVarTerm> += <int expr>`, `<strVarTerm> += <string expr>`, `<strVarTerm> *= <int expr>`
- Inc/dec: `<intVarTerm>++` / `<intVarTerm>--` (no RHS allowed)
- Comma-list assignment (only with plain `=` / `'=`): `<varTerm> = v1, v2, v3, ...`

**Arguments**
- LHS must be a **single variable term** (not an arbitrary expression), and must not be `CONST`.
- RHS is parsed in one of multiple modes depending on operator and LHS type:
  - int LHS: RHS is parsed as normal expressions.
  - string LHS with `=`: RHS is scanned as a formatted string until end-of-line.
  - string LHS with `'=` / `+=` / `*=`: RHS is parsed as normal expressions.

**Defaults / optional arguments**
- For `++/--`, the implicit delta is `+1` / `-1`.

**Semantics**
- If the RHS is a single value:
  - `=` assigns that value.
  - `+=` / `-=` / `*=` etc. are reduced as `LHS = LHS <op> RHS` using the engine’s operator reducers.
- If the RHS is a comma list (only for plain assignment operators):
  - Evaluates each element and writes a batch of consecutive elements via the variable term’s `SetValue(long[]/string[])` overload.
  - If any RHS element is omitted, it is an error.
- For string `=` assignment, the RHS is treated as FORM/formatted text (not a normal expression) and then compiled to a string expression internally.

**Errors & validation**
- Errors if LHS cannot be read as a single variable term, if LHS is const, or if operator is incompatible with the LHS type.
- Errors if assigning string→int or int→string in contexts that disallow it.
- If `SystemIgnoreStringSet` is enabled, string `=` assignment is rejected (scripts must use `'=` or other operations).

**Examples**
- `A = 10`
- `A += 1`
- `S = "Hello, %NAME%!"`
- `S '= TOSTR(A)`
- `ARR:0 = 1, 2, 3, 4`
