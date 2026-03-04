**Summary**
- Splits an HTML string into a sequence of raw tags and raw text segments.

**Tags**
- string

**Syntax**
- `HTML_TAGSPLIT <html>(, <outParts>, <outCount>)`

**Arguments**
- `<html>`: string expression.
- `<outParts>` (optional): a changeable 1D **non-character** string array variable.
  - Default: `RESULTS`.
- `<outCount>` (optional): a changeable integer variable.
  - Default: `RESULT`.

- Omitted arguments / defaults:
  - If `<outParts>` is omitted, the split parts are written to `RESULTS`.
  - If `<outCount>` is omitted, the split count is written to `RESULT`.

**Semantics**
- Interprets `<html>` as an HTML string and splits it by scanning for `<...>` regions:
  - Each tag-like region from `<` through the next `>` (inclusive) is emitted as a single part.
  - Text between such regions is emitted as-is as a single part.
- The splitter does **not** validate tag relationships or supported tag names; it only performs lexical splitting.
  - For example, it will emit `</font>` as a tag part even if no `<font>` was previously seen.
- On success:
  - Writes the total part count to `<outCount>`.
  - Writes parts to `<outParts>:i` for `0 <= i < min(partCount, len(<outParts>))`.
  - If `partCount` exceeds the destination array length, excess parts are not written.
- On failure (e.g. a `<` is found but no matching `>` exists later in the string):
  - Writes `-1` to `<outCount>`.
  - Does not modify `<outParts>`.

**Errors & validation**
- Argument type/count errors follow the normal expression argument rules.

**Examples**
```erabasic
HTML_TAGSPLIT "<p align='right'>A<!--c-->B</p>"
PRINTFORML RESULT = {RESULT}
PRINTFORML RESULTS:0 = %RESULTS:0%
PRINTFORML RESULTS:1 = %RESULTS:1%
```

**Progress state**
- complete
