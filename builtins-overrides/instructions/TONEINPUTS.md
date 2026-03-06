**Summary**
- Like `TINPUTS`, but uses the “one input” mode (`OneInput = true`).

**Tags**
- io

**Syntax**
- Same as `TINPUTS`.

**Arguments**
- Same as `TINPUTS`.

**Semantics**
- Same as `TINPUTS`, but with “one input” mode enabled.
- The same ordinary normal-output-button click path still exists here: clicking a selectable **normal-output button** can submit one string even when the extra mouse side-channel mode was not requested.
- When `<mouse> != 0`, the same extra mouse side channels as `TINPUTS` / `INPUTS` are also written.
- Exact one-input rule:
  - One-input truncation is applied per submitted segment; see `input-flow.md` for the shared submission/segmentation model.
  - Each submitted segment is normally truncated to its first character.
  - Exception: if the segment is accepted through the mouse-click completion path and config option `AllowLongInputByMouse` is enabled (see `config-items.md`), that mouse-submitted text is not truncated.
  - This truncation applies only to submitted UI text. Defaults accepted via empty input or the `MesSkip` no-wait path are used as-is by `TONEINPUTS` itself.

**Errors & validation**
- Same as `TINPUTS`.

**Examples**
- `TONEINPUTS 5000, "A"`

**Progress state**
- complete
