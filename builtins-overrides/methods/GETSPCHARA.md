**Summary**
- Returns the first registered SP-character index in the current character list whose `NO` matches the requested character number.

**Tags**
- characters

**Syntax**
- `GETSPCHARA(charaNo)`

**Signatures / argument rules**
- `GETSPCHARA(charaNo)` → `long`

**Arguments**
- `charaNo` (int): character `NO` to search for among currently registered SP characters.

**Semantics**
- Scans the current registered character list in ascending character-index order.
- A match requires both:
  - `NO == charaNo`, and
  - the character is currently flagged as SP (`CFLAG:0 != 0`).
- Returns the first matching registered character index, or `-1` if none exists.

**Errors & validation**
- Runtime error if `CompatiSPChara=NO`.

**Examples**
- `idx = GETSPCHARA(100)`

**Progress state**
- complete
