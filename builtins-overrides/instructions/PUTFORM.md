**Summary**
- Appends a formatted string to the save-description buffer (`SAVEDATA_TEXT`).

**Tags**
- io

**Syntax**
- `PUTFORM`
- `PUTFORM <formString>`

**Arguments**
- `<formString>` (optional): FORM/formatted string.

- Omitted arguments / defaults:
  - If omitted, the argument is treated as the empty string.

**Semantics**
- Evaluates `<formString>` to a string.
- Appends it to the internal save-description buffer:
  - If `SAVEDATA_TEXT` is non-null, `SAVEDATA_TEXT += <string>`.
  - Otherwise, `SAVEDATA_TEXT = <string>`.
- Does not print to the console.
- Typically used by the save-info generation path (e.g. `@SAVEINFO`) to build `SAVEDATA_TEXT`.

**Errors & validation**
- None.

**Examples**
- `PUTFORM %PLAYERNAME% - Day %DAY%`

**Progress state**
- complete
