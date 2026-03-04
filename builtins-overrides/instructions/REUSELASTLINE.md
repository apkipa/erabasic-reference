**Summary**
- Prints a **temporary single line** that is intended to be overwritten by the next printed line.

**Tags**
- io

**Syntax**
- `REUSELASTLINE`
- `REUSELASTLINE <formString>`

**Arguments**
- `<formString>` (optional): FORM/formatted string (parsed like `PRINTFORM*`) used as the temporary line’s content.

- Omitted arguments / defaults:
  - If omitted, the argument is treated as the empty string.

**Semantics**
- Evaluates `<formString>` to a string and prints it as a temporary line.
- A “temporary line” has a special overwrite behavior:
  - When the engine later adds a new display line, if the current last display line is temporary, it is deleted first; the new line then takes its place.
  - As a result, repeated `REUSELASTLINE` calls typically “update” a single line (useful for progress/timer displays).
- If the resulting string is empty, the current console implementation prints nothing (and therefore does not overwrite an existing line).

**Errors & validation**
- None.

**Examples**
- `REUSELASTLINE Now loading...`
- `REUSELASTLINE %TIME%`

**Progress state**
- complete
