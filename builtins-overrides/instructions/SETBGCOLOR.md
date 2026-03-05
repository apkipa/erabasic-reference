**Summary**
- Sets the current background color.

**Tags**
- ui

**Syntax**
- `SETBGCOLOR rgb`
- `SETBGCOLOR r, g, b`

**Arguments**
- `rgb` (int): packed `0xRRGGBB` value. Only the low 24 bits are used.
- `r`, `g`, `b` (int): color components.
  - Must satisfy `0 <= component <= 255`.

**Semantics**
- Same argument handling as `SETCOLOR`, but applies to the background color instead of the text color.
- Does not print output.

**Errors & validation**
- Parse-time warning + rejection if you pass exactly 2 arguments.
- Runtime error in the three-argument form if any component is `< 0` or `> 255`.

**Examples**
- `SETBGCOLOR 0x000000`    ; black background
- `SETBGCOLOR 0, 0, 0`     ; black background

**Progress state**
- complete

