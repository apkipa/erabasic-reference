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

**Progress state**
- complete
