**Summary**
- Counts regex matches and can optionally expose captured group values.

**Tags**
- text
- reflection

**Syntax**
- `REGEXPMATCH(str, pattern [, outputFlag])`
- `REGEXPMATCH(str, pattern, groupCount, matches)`

**Signatures / argument rules**
- `REGEXPMATCH(str, pattern)` → `long`
- `REGEXPMATCH(str, pattern, outputFlag)` → `long`
- `REGEXPMATCH(str, pattern, groupCount, matches)` → `long`

**Arguments**
- `str` (string): target string.
- `pattern` (string): regular-expression pattern.
- `outputFlag` (optional, int; default `0`): when non-zero, writes capture output into `RESULTS:*` and writes group count into `RESULT:1`.
- `groupCount` (ref int): destination for the number of regex groups.
- `matches` (ref 1D string array): destination for flattened group outputs.

**Semantics**
- Compiles `pattern` as a `.NET` regular expression with default options.
- Returns the number of matches in `str`.
- Group-count rule:
  - the reported group count is `.NET` `Regex.GetGroupNumbers().Length`,
  - this includes group `0` (the whole match).
- Output modes:
  - if `outputFlag != 0`, writes the group count to `RESULT:1` and writes flattened match/group values to `RESULTS:*`,
  - if `groupCount, matches` references are supplied, writes the group count to `groupCount` and flattened values to `matches`.
- Flattening order:
  - iterate matches in match order,
  - for each match, iterate groups in `.NET` `Regex.GetGroupNames()` order,
  - append each `match.Groups[name].Value`.
- Output truncation/retention:
  - flattened output stops when the destination string array is full,
  - any remaining output is discarded,
  - destination entries beyond the copied prefix are not cleared,
  - if there are no matches, the string destination is left unchanged.

**Errors & validation**
- Runtime error if `pattern` is not a valid regular expression.

**Examples**
- `count = REGEXPMATCH("Apple Banana Car", ".(.{2})\b")`

**Progress state**
- complete
