**Summary**
- Enumerates files under a relative directory using a wildcard pattern.

**Tags**
- files

**Syntax**
- `ENUMFILES(dir [, pattern [, recursive [, output]]])`

**Signatures / argument rules**
- `ENUMFILES(dir)` → `long`
- `ENUMFILES(dir, pattern)` → `long`
- `ENUMFILES(dir, pattern, recursive)` → `long`
- `ENUMFILES(dir, pattern, recursive, output)` → `long`

**Arguments**
- `dir` (string): directory path relative to the executable directory.
- `pattern` (optional, string; default `"*"`): filesystem wildcard pattern.
- `recursive` (optional, int; default `0`): non-zero enables recursive enumeration.
- `output` (optional, 1D string-array variable reference; default `RESULTS:*`): destination for copied relative paths.

**Semantics**
- Resolves `dir` using the same safe relative-path normalization used by `EXISTFILE`.
- Returns `-1` if normalization fails or the resolved directory does not exist.
- Enumerates files using the host filesystem's wildcard matching rules.
- If `recursive == 0`, searches only the top directory.
- If `recursive != 0`, searches all subdirectories.
- Every returned path is converted back to a path relative to the executable directory.
- Output destination:
  - if `output` is omitted, copied paths go to `RESULTS:*`,
  - otherwise they go to the provided 1D string array.
- Return value is the number of paths actually copied.
  - This is `min(foundCount, destinationLength)`, not the total number of matches when truncation occurs.
- The destination is not cleared beyond the copied prefix.
- Returns `-1` if enumeration throws.

**Errors & validation**
- Argument type/count errors are rejected by the engine's function-method argument checker.

**Examples**
- `count = ENUMFILES("csv", "*.csv", 1)`

**Progress state**
- complete
