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
  - One-input truncation is applied per submitted segment; see `input-flow.md` for the shared submission/segmentation model.
  - Each submitted segment is normally truncated to its first character.
  - Exception: if the segment is accepted through the mouse-click completion path and config option `AllowLongInputByMouse` is enabled (see `config-items.md`), that mouse-submitted text is not truncated.
  - This truncation applies only to submitted UI text. Defaults accepted via empty input or the `MesSkip` no-wait path are used as-is by `ONEINPUTS` itself.

**Errors & validation**
- Same as `INPUTS`.

**Examples**
- `ONEINPUTS`
- `ONEINPUTS A`

**Progress state**
- complete
