**Summary**
- Like `TINPUT`, but uses the “one input” mode (`OneInput = true`).

**Tags**
- io

**Syntax**
- Same as `TINPUT`.

**Arguments**
- Same as `TINPUT`.

- Omitted arguments / defaults:
  - Same as `TINPUT`.

**Semantics**
- Same as `TINPUT`, but with “one input” mode enabled:
  - If the entered text has length > 1, it is truncated to the first character.
  - Exception: if `AllowLongInputByMouse` is enabled and the input was produced by mouse selection, truncation does not occur.

**Errors & validation**
- Same as `TINPUT`.

**Examples**
- `TONEINPUT 5000, 0`

**Progress state**
- complete
