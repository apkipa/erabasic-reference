**Summary**
- Like `INPUT`, but requests a “one input” integer entry (UI-side restriction).

**Tags**
- io

**Syntax**
- `ONEINPUT`
- `ONEINPUT <default>`
- `ONEINPUT <default>, <mouse>, <canSkip> [, <extra>]`

**Arguments**
- Same as `INPUT`.

**Semantics**
- Like `INPUT` (including `MesSkip` behavior and mouse side channels), but sets `OneInput = true` on the input request.
- Exact one-input rule:
  - One-input truncation is applied per submitted segment; see `input-flow.md` for the shared submission/segmentation model.
  - Each submitted segment is normally truncated to its first character.
  - Exception: if the segment is accepted through the mouse-click completion path and config option `AllowLongInputByMouse` is enabled (see `config-items.md`), that mouse-submitted text is not truncated.
  - This truncation applies only to submitted UI text. Defaults accepted via empty input or the `MesSkip` no-wait path are used as-is by `ONEINPUT` itself.

**Errors & validation**
- Same as `INPUT`.

**Examples**
- `ONEINPUT`
- `ONEINPUT 0`

**Progress state**
- complete
