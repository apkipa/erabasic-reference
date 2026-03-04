**Summary**
- Prints a clickable button with a script-provided input value.
- Unlike automatic button conversion (e.g. `[0] ...` inside normal `PRINT` output), this instruction forces the output segment to be a button.

**Tags**
- io

**Syntax**
- `PRINTBUTTON <text>, <buttonValue>`

**Arguments**
- `<text>`: string expression (button label).
- `<buttonValue>`: expression whose runtime type is either:
  - integer (button produces that integer as input), or
  - string (button produces that string as input; useful with `INPUTS`).

**Semantics**
- If output skipping is active (`SKIPDISP` / `skipPrint`), this instruction is skipped (no output).
- Uses the current text style for output (and honors `SETCOLOR` color).
- Evaluates `<text>` to a string, then removes any newline characters (`'\n'`) from it.
- If the resulting label is empty, this instruction produces no output segment (no button is created).
- Appends one button segment to the print buffer:
  - If `<buttonValue>` is an integer, the button produces that integer when clicked.
  - If `<buttonValue>` is a string, the button produces that string when clicked.
- This instruction does **not** add a newline and does not flush by itself (it behaves like other non-`...L` print-family commands).

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
