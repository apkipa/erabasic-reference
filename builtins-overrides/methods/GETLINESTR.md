**Summary**
- Expands a pattern string to the current drawable width using the same width-fitting rule used by `DRAWLINE`-style output.

**Tags**
- io
- string

**Syntax**
- `GETLINESTR(<pattern>)`

**Signatures / argument rules**
- Signature: `string GETLINESTR(string pattern)`.
- `<pattern>` is evaluated as a string expression.

**Arguments**
- `<pattern>` (string): the pattern string to expand.

**Semantics**
- Evaluates `<pattern>` to a string.
- Returns the width-fitted line string that the runtime would use for a dynamic `DRAWLINE`-style expansion of that pattern:
  - repeat the pattern until the measured display width reaches or exceeds the current drawable width,
  - then trim one character at a time from the end until the measured width is less than or equal to the drawable width.
- The result depends on the current host layout metrics (drawable width and font measurement), so its character count is **not** a stable “one visible line = N characters” value.
- This helper does not print anything and does not modify output state.
- Contract relation:
  - it matches the runtime width-expansion rule used by non-constant `DRAWLINEFORM`,
  - and it matches the already-expanded string produced for `CUSTOMDRAWLINE` / `DRAWLINE`-style line patterns.

**Errors & validation**
- Runtime error if `<pattern>` evaluates to `""`.

**Examples**
```erabasic
S = GETLINESTR("-=")
PRINTL S
```

**Progress state**
- complete
