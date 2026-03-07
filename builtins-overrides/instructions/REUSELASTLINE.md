**Summary**
- Prints a **temporary single line** that is overwritten by the next later visible normal line append.

**Tags**
- io

**Syntax**
- `REUSELASTLINE`
- `REUSELASTLINE <formString>`

**Arguments**
- `<formString>` (optional, FORM/formatted string): parsed like `PRINTFORM*` and used as the temporary line’s content.

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output).
- If ordinary buffered output is currently pending, that buffered content is flushed first as normal visible output.
- Evaluates `<formString>` to a string and, if the result is non-empty, appends it as a **temporary visible line**.
- Temporary-line behavior:
  - while it remains visible, it occupies a normal visible logical-line slot,
  - the next operation that appends a new normal visible display line removes the trailing temporary line first,
  - repeated `REUSELASTLINE` calls therefore replace one another instead of accumulating.
- If the resulting string is empty, this instruction prints nothing.
  - In that empty-result case, it does not clear or replace an already-visible temporary line.

**Errors & validation**
- None.

**Examples**
```erabasic
REUSELASTLINE "Now loading..."
REUSELASTLINE %TIME%
```

**Progress state**
- complete
