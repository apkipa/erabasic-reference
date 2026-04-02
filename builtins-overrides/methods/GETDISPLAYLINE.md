**Summary**
- Returns the plain-text content of one currently visible **display line** in the normal output area.

**Tags**
- io

**Syntax**
- `GETDISPLAYLINE(<lineNumber>)`

**Signatures / argument rules**
- Signature: `string GETDISPLAYLINE(int lineNumber)`.
- `<lineNumber>` is evaluated as an integer expression.

**Arguments**
- `<lineNumber>` (int): zero-based index into the current visible display-line array of the normal output area.
  - `0` = the oldest currently visible display row.

**Semantics**
- Reads one entry from the current visible display-line array.
- This is a **display-row** getter, not a logical-line getter:
  - wrapped rows and explicit display breaks occupy separate indices,
  - one logical output line may therefore correspond to multiple `GETDISPLAYLINE` indices.
- Returns `""` if `<lineNumber> < 0` or if the requested visible row does not exist.
- Reads only the current visible normal output area:
  - pending buffered output is not included,
  - the separate `HTML_PRINT_ISLAND` layer is not included.
- The return value is plain text:
  - button metadata/clickability is flattened away,
  - inline images/shapes contribute their text/alt representation rather than structured HTML.
- Temporary lines are included while they remain visible.
- Because this getter reads the **current visible** display-line array, older rows that have already fallen out of the visible log are no longer accessible by index.

**Errors & validation**
- None.

**Examples**
```erabasic
PRINTL AAA
PRINTL BBB
S = GETDISPLAYLINE(0)
```

**Progress state**
- complete
