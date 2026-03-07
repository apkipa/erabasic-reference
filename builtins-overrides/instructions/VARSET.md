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

**Progress state**
- complete
