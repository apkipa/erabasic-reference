**Summary**
- Like `BINPUTS`, but uses “one input” mode (`OneInput = true`): typed text input is truncated to its first character.

**Tags**
- io

**Syntax**
- `ONEBINPUTS [<default> [, <mouse> [, <canSkip>]]]`

**Arguments**
- Same argument model as `BINPUTS`.

**Semantics**
- Same button-matching and default rules as `BINPUTS`.
- Additionally, when the user submits a non-empty input string:
  - The engine truncates the input to its first character before attempting to match it.
  - Exception: if the input is produced by mouse selection and config `AllowLongInputByMouse` is enabled, truncation does not occur.

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
