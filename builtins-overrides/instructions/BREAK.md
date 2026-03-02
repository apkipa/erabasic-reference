**Summary**
- Exits the nearest enclosing loop (`REPEAT`, `FOR`, `WHILE`, or `DO`).

**Syntax**
- `BREAK`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- The loader links `BREAK` to the nearest enclosing loop start marker.
- At runtime, `BREAK` jumps to that loop’s end marker (so execution continues after the loop).
- For `REPEAT`/`FOR`, the engine also increments the loop counter once on `BREAK` (era-maker compatibility quirk).

**Errors & validation**
- `BREAK` outside any loop produces a load-time warning.

**Examples**
- `BREAK`
