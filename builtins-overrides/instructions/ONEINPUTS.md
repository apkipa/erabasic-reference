**Summary**
- Like `INPUTS`, but requests a “one input” string entry (UI-side restriction).

**Syntax**
- `ONEINPUTS`
- `ONEINPUTS <defaultFormString>`
- `ONEINPUTS <defaultFormString>, <mouse> [, <canSkip>]`

**Arguments**
- Same as `INPUTS`.

**Defaults / optional arguments**
- Same as `INPUTS`.

**Semantics**
- Like `INPUTS` (including `MesSkip` behavior and mouse side channels), but sets `OneInput = true` on the input request.
- Implementation detail: the UI input handler may truncate the entered string to at most one character.

**Errors & validation**
- Same as `INPUTS`.

**Examples**
- `ONEINPUTS`
- `ONEINPUTS A`

**Progress state**
- complete
