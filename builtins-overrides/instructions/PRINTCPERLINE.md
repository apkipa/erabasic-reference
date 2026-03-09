**Summary**
- Writes the value of config item `PrintCPerLine` into an integer variable.

**Tags**
- config

**Syntax**
- `PRINTCPERLINE [<dest>]`

**Arguments**
- `<dest>` (optional, changeable integer variable term; default `RESULT`): receives the value.

**Semantics**
- Assigns the value of config item `PrintCPerLine` to `<dest>`.
- Does not print output.

**Errors & validation**
- Argument parsing fails if `<dest>` is provided but is not a changeable integer variable term.

**Examples**
- `PRINTCPERLINE`        ; writes into `RESULT`
- `PRINTCPERLINE X`      ; writes into `X`

**Progress state**
- complete
