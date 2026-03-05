**Summary**
- Like `INPUTS`, but requests a “one input” string entry (UI-side restriction).

**Tags**
- io

**Syntax**
- `ONEINPUTS`
- `ONEINPUTS <defaultFormString>`
- `ONEINPUTS <defaultFormString>, <mouse> [, <canSkip>]`

**Arguments**
- Same as `INPUTS`.

**Semantics**
- Like `INPUTS` (including `MesSkip` behavior and mouse side channels), but with “one input” mode enabled:
  - If the entered text has length > 1, it is truncated to the first character.
  - Exception: if `AllowLongInputByMouse` is enabled and the input was produced by mouse selection, truncation does not occur.

**Errors & validation**
- Same as `INPUTS`.

**Examples**
- `ONEINPUTS`
- `ONEINPUTS A`

**Progress state**
- complete
