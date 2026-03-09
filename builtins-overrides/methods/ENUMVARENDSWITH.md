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
