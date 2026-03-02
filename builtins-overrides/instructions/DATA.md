**Summary**
- Declares one printable choice inside a surrounding `PRINTDATA*` / `STRDATA` / `DATALIST` block.
- `DATA` lines are *not* intended to execute as standalone statements; they are consumed by the loader into the surrounding block’s data list.

**Syntax**
- `DATA [<raw text>]`
- `DATA;<raw text>`

**Arguments**
- Optional raw literal text (not an expression).

**Defaults / optional arguments**
- Omitted argument is treated as empty string.

**Semantics**
- At load time, the loader attaches `DATA` lines to the nearest surrounding block (`PRINTDATA*`, `STRDATA`, or `DATALIST`).
- At runtime, `PRINTDATA*` / `STRDATA` evaluate the stored `DATA` line as a string and print/concatenate it when selected.

**Errors & validation**
- Using `DATA` outside a valid surrounding block produces loader warnings/errors and the line will not participate in any `PRINTDATA*` / `STRDATA` selection.

**Examples**
```erabasic
PRINTDATA
  DATA Hello
  DATA;World
ENDDATA
```
