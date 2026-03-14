**Summary**
- Like `PRINTBUTTON`, but formats the label as a fixed-width `PRINTC`-style cell aligned to the right.

**Tags**
- io

**Syntax**
- `PRINTBUTTONC <text>, <buttonValue>`

**Arguments**
- Same as `PRINTBUTTON`.

**Semantics**
- Same as `PRINTBUTTON`, with these differences:
  - The label still has all `'\n'` characters removed (same as `PRINTBUTTON`).
  - Before creating the button segment, the label is formatted as a `PRINTC`-style fixed-width cell, aligned to the right.
  - That cell formatting uses hardcoded Shift-JIS byte count (code page 932), via the same `CreateTypeCString()` path as `PRINTC`; it does **not** use derived runtime value `LanguageCodePage`.

**Errors & validation**
- Same as `PRINTBUTTON`.

**Examples**
```erabasic
PRINTBUTTONC "[0] OK", 0
PRINTBUTTONC "[1] Cancel", 1
INPUT
```

**Progress state**
- complete
