**Summary**
- Like `BINPUT`, but uses “one input” mode (`OneInput = true`) for submitted UI text.

**Tags**
- io

**Syntax**
- `ONEBINPUT [<default> [, <mouse> [, <canSkip> [, ... ]]]]`

**Arguments**
- `<default>` (optional, int expression): used only when the submitted text is empty (not used for invalid integer text).
- `<mouse>` (optional, int; default `0`): controls the extra mouse side-channel mode.
  - Clicking a selectable button can still satisfy `ONEBINPUT` by itself; when `<mouse> != 0`, the same extra mouse side channels as `INPUT` are also written.
- `<canSkip>` (optional, int): presence enables the `MesSkip` fast path; its numeric value is ignored (not evaluated).
- Extra arguments after `<canSkip>` are accepted by the argument parser but ignored by the runtime.

**Semantics**
- Same button-matching and default rules as `BINPUT`.
- Clicking a selectable integer button can satisfy this wait by itself; when `<mouse> != 0`, the same extra mouse side channels as `BINPUT` / `INPUT` are also written.
- Exact one-input rule:
  - One-input truncation is applied per submitted segment; see `input-flow.md` for the shared submission/segmentation model.
  - Each submitted segment is normally truncated to its first character.
  - Exception: if the segment is accepted through the mouse-click completion path and config option `AllowLongInputByMouse` is enabled (see `config-items.md`), that mouse-submitted text is not truncated.
  - This truncation applies only to submitted UI text. Defaults accepted via empty input or the `MesSkip` no-wait path are used as-is by `ONEBINPUT` itself.

**Errors & validation**
- Same as `BINPUT`.

**Examples**
```erabasic
PRINTBUTTON "0", 0
PRINTBUTTON "1", 1
PRINTL ""
ONEBINPUT
```

**Progress state**
- complete
