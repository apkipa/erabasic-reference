**Summary**
- Removes CBG entries whose `zDepth` lies within an inclusive range.

**Tags**
- ui
- graphics

**Syntax**
- `CBGREMOVERANGE(<zMin>, <zMax>)`

**Signatures / argument rules**
- Signature: `int CBGREMOVERANGE(int zMin, int zMax)`.
- Both arguments are evaluated as integer expressions, then converted to 32-bit signed integers by truncation.

**Arguments**
- `<zMin>` (int): inclusive lower bound of the removal range after 32-bit conversion.
- `<zMax>` (int): inclusive upper bound of the removal range after 32-bit conversion.

**Semantics**
- Removes every current CBG entry whose `zDepth` satisfies `zMin <= zDepth <= zMax`.
- The reserved internal depth-`0` dummy entry is never removed.
- If `zMin > zMax`, nothing is removed.
- This operation does **not** clear the current CBG button-hit map.
- Observable consequence:
  - removed CBG images/button sprites disappear,
  - but the hit map and current CBG selection machinery remain installed unless changed separately.
- Layer boundary:
  - this affects only the CBG/background layer,
  - it does not modify the normal output model, pending print buffer, or HTML-island layer.
- Return value: always returns `1`.

**Errors & validation**
- No explicit range validation is performed after the 32-bit conversion.

**Examples**
- `R = CBGREMOVERANGE(10, 20)`

**Progress state**
- complete
