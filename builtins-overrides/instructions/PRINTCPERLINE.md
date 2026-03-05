**Summary**
- Writes the configured `PrintCPerLine` value into an integer variable.

**Tags**
- config

**Syntax**
- `PRINTCPERLINE [<dest>]`

**Arguments**
- `<dest>` (optional; default `RESULT`): changeable integer variable term to receive the value.

**Semantics**
- Assigns the configuration value `PrintCPerLine` to `<dest>`.
- Does not print output.

**Errors & validation**
- Argument parsing fails if `<dest>` is provided but is not a changeable integer variable term.

**Examples**
- `PRINTCPERLINE`        ; writes into `RESULT`
- `PRINTCPERLINE X`      ; writes into `X`

**Progress state**
- complete

