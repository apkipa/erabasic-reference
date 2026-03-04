**Summary**
- Exits the nearest enclosing loop (`REPEAT`, `FOR`, `WHILE`, or `DO`).

**Tags**
- control-flow

**Syntax**
- `BREAK`

**Arguments**
- None.

**Semantics**
- The loader links `BREAK` to the nearest enclosing loop start marker.
- At runtime, `BREAK` jumps to that loop’s end marker (so execution continues after the loop).
- For `REPEAT`/`FOR`, the engine also increments the loop counter once on `BREAK` (era-maker compatibility quirk).

**Errors & validation**
- `BREAK` outside any loop is a load-time error (the line is marked as error).

**Examples**
- `BREAK`

**Progress state**
- complete
