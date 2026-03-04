**Summary**
- Like `PRINTBUTTON`, but formats the label as a fixed-width `PRINTC`-style cell aligned to the left.

**Tags**
- io

**Syntax**
- `PRINTBUTTONLC <text>, <buttonValue>`

**Arguments**
- Same as `PRINTBUTTON`.

**Semantics**
- Same as `PRINTBUTTONC`, except the label cell is aligned to the left:
  - Uses the same fixed-width cell formatting rules as `PRINTLC`.

**Errors & validation**
- Same as `PRINTBUTTON`.

**Examples**
```erabasic
PRINTBUTTONLC "[0] OK", 0
PRINTBUTTONLC "[1] Cancel", 1
INPUT
```

**Progress state**
- complete
