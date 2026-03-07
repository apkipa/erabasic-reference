**Summary**
- Writes the configured `SaveDataNos` value into an integer variable.

**Tags**
- config

**Syntax**
- `SAVENOS [<dest>]`

**Arguments**
- `<dest>` (optional, changeable integer variable term; default `RESULT`): receives the value.

**Semantics**
- Assigns the configuration value `SaveDataNos` to `<dest>`.
- Does not print output.

**Errors & validation**
- Argument parsing fails if `<dest>` is provided but is not a changeable integer variable term.

**Examples**
- `SAVENOS`        ; writes into `RESULT`
- `SAVENOS X`      ; writes into `X`

**Progress state**
- complete

