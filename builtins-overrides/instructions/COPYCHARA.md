**Summary**
- Copies all character data from one character to another (overwrite).

**Tags**
- characters

**Syntax**
- `COPYCHARA fromIndex, toIndex`

**Arguments**
- `fromIndex` (int): source character index.
- `toIndex` (int): destination character index.

**Semantics**
- Copies the entire character-data record from `fromIndex` into `toIndex`.
  - This overwrites all character variables for `toIndex`, including `NO`/`NAME`/etc and character arrays.
- Does not change the character list length and does not move character indices.
- Does not print output.

**Errors & validation**
- Runtime error if `fromIndex` is out of range.
- Runtime error if `toIndex` is out of range.

**Examples**
- `COPYCHARA 0, 1`

**Progress state**
- complete

