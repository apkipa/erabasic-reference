**Summary**
- Parses a string as FORM / formatted text and returns the expanded result without printing it.

**Tags**
- text

**Syntax**
- `STRFORM(formatSource)`

**Signatures / argument rules**
- `STRFORM(formatSource)` → `string`

**Arguments**
- `formatSource` (string): runtime string to parse as FORM / formatted text.

**Semantics**
- Parses `formatSource` using the same FORM/formatted-string expansion model used by `PRINTFORM`-family text.
- Evaluates embedded substitutions against current runtime state and returns the expanded string.
- No output line is emitted; only the resulting string is returned.
- Parsing stops at the first newline in `formatSource`, matching end-of-line FORM scanning.
- If `formatSource` contains no FORM constructs, the returned string is the same text up to that first newline.

**Errors & validation**
- Runtime error if `formatSource` is not valid FORM/formatted text.
- Runtime error if expansion of an embedded substitution fails.

**Examples**
- `STRFORM("X={1+1}")` → `"X=2"`

**Progress state**
- complete
