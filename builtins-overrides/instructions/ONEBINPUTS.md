**Summary**
- Like `BINPUTS`, but uses “one input” mode (`OneInput = true`) for submitted UI text.

**Tags**
- io

**Syntax**
- `ONEBINPUTS [<default> [, <mouse> [, <canSkip>]]]`

**Arguments**
- `<default>` (optional, string): default string used only when the submitted text is empty.
- `<mouse>` (optional, int; default `0`): controls the extra mouse side-channel mode.
  - Clicking a selectable button also satisfies `ONEBINPUTS` by itself; when `<mouse> != 0`, the same extra mouse side channels as `INPUTS` are also written.
- `<canSkip>` (optional, int): presence enables the `MesSkip` fast path; its numeric value is ignored (not evaluated).

**Semantics**
- Same button-matching and default rules as `BINPUTS`.
- Clicking a selectable button can satisfy this wait by itself; when `<mouse> != 0`, the same extra mouse side channels as `BINPUTS` / `INPUTS` are also written.
- Exact one-input rule:
  - One-input truncation is applied per submitted segment; see `input-flow.md` for the shared submission/segmentation model.
  - Each submitted segment is normally truncated to its first character.
  - Exception: if the segment is accepted through the mouse-click completion path and config option `AllowLongInputByMouse` is enabled (see `config-items.md`), that mouse-submitted text is not truncated.
  - This truncation applies only to submitted UI text. Defaults accepted via empty input or the `MesSkip` no-wait path are used as-is by `ONEBINPUTS` itself.

**Errors & validation**
- Same as `BINPUTS`.

**Examples**
```erabasic
PRINTBUTTONS "A", "A"
PRINTBUTTONS "B", "B"
PRINTL ""
ONEBINPUTS
```

**Progress state**
- complete
