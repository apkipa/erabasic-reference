**Summary**
- Like `BINPUT`, but uses “one input” mode (`OneInput = true`): typed text input is truncated to its first character.

**Tags**
- io

**Syntax**
- `ONEBINPUT [<default> [, <mouse> [, <canSkip> [, ... ]]]]`

**Arguments**
- Same argument model as `BINPUT`.

**Semantics**
- Same button-matching and default rules as `BINPUT`.
- Additionally, when the user submits a non-empty input string:
  - The engine truncates the input to its first character before attempting to parse/match it.
  - Exception: if the input is produced by mouse selection and config `AllowLongInputByMouse` is enabled, truncation does not occur.

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
