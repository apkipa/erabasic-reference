**Summary**
- Counts regex matches in a string.

**Tags**
- text

**Syntax**
- `STRCOUNT(str, pattern)`

**Signatures / argument rules**
- `STRCOUNT(str, pattern)` → `long`

**Arguments**
- `str` (string): target string.
- `pattern` (string): regular-expression pattern.

**Semantics**
- Compiles `pattern` as a `.NET` regular expression with default options.
- Returns `Regex.Matches(str, pattern).Count`.
- Matching is regex-based, not plain-substring-based.
- Counted matches are the normal non-overlapping matches returned by `.NET` regex enumeration.
- Use `ESCAPE(pattern)` first if you want to search for a literal string via regex APIs.

**Errors & validation**
- Runtime error if `pattern` is not a valid regular expression.

**Examples**
- `STRCOUNT("aaaa", "aa")` → `2`

**Progress state**
- complete
