**Summary**
- Like `TINPUTS`, but uses the “one input” mode (`OneInput = true`).

**Tags**
- io

**Syntax**
- Same as `TINPUTS`.

**Arguments**
- Same as `TINPUTS`.

- Omitted arguments / defaults:
  - Same as `TINPUTS`.

**Semantics**
- Same as `TINPUTS`, but with “one input” mode enabled:
  - If the entered text has length > 1, it is truncated to the first character.
  - Exception: if `AllowLongInputByMouse` is enabled and the input was produced by mouse selection, truncation does not occur.

**Errors & validation**
- Same as `TINPUTS`.

**Examples**
- `TONEINPUTS 5000, "A"`

**Progress state**
- complete
