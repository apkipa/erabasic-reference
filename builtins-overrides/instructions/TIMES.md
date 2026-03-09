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
- Calculation mode depends on config item `TimesNotRigorousCalculation`:
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

**Progress state**
- complete
