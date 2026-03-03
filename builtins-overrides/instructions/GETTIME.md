**Summary**
- Writes the current local date/time into `RESULT` (as a packed integer) and `RESULTS` (as a formatted string).

**Syntax**
- `GETTIME`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- Reads the current local time (`DateTime.Now`) and assigns:
  - `RESULT`: an integer of the form `yyyymmddHHMMSSmmm` (milliseconds included).
  - `RESULTS`: a string of the form `yyyy/MM/dd HH:mm:ss` (no milliseconds).
- Does not print output.

**Errors & validation**
- None.

**Examples**
- `GETTIME`

**Progress state**
- complete

