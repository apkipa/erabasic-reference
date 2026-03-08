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

**Progress state**
- complete
