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

**Progress state**
- complete
