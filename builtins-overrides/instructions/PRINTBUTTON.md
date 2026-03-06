**Summary**
- Appends a clickable button region to the current output.

**Tags**
- io

**Syntax**
- `PRINTBUTTON <text>, <buttonValue>`

**Arguments**
- `<text>` (string expression): label shown in the output.
- `<buttonValue>` (int or string expression): value associated with the button.
  - Integer values are accepted by integer button waits (`BINPUT` / `ONEBINPUT`).
  - String values are accepted by string button waits (`BINPUTS` / `ONEBINPUTS`).

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output).
- Uses the current text style for output (and honors `SETCOLOR` color).
- Evaluates `<text>` to a string, then removes any newline characters (`'\n'`) from it.
- If the resulting label is empty, this instruction produces no output segment (no button is created).
- Appends one button region to the pending print buffer:
  - if `<buttonValue>` is an integer, the button’s input value is that integer,
  - if `<buttonValue>` is a string, the button’s input value is that string.
- This instruction does **not** add a newline and does not flush by itself.
- Selectability lifecycle:
  - after the containing output becomes retained, the button can be shown by the normal output model,
  - later button waits only accept buttons in the current active selectable generation,
  - so an older retained button may remain visible but no longer be selectable.
- Output/readback boundary:
  - `GETDISPLAYLINE` later sees only the rendered label text,
  - `HTML_GETPRINTEDSTR` / `HTML_POPPRINTINGSTR` preserve button structure as `<button ...>` markup.

**Errors & validation**
- Argument type/count errors follow the normal expression argument rules.

**Examples**
```erabasic
PRINTS "Are you sure? "
PRINTBUTTON "[0] Yes", 0
PRINTS "  "
PRINTBUTTON "[1] No", 1
INPUT
```

```erabasic
PRINTL Enter your name:
PRINTBUTTON "[Alice]", "Alice"
PRINTBUTTON " [Bob]", "Bob"
INPUTS
```

**Progress state**
- complete
