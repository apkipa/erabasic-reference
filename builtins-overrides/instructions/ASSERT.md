**Summary**
- Debug-only assertion that raises a script error when its condition is false.

**Tags**
- debug

**Syntax**
- `ASSERT <bool>`

**Arguments**
- `<bool>` (int): treated as false when it evaluates to `0`, true otherwise.

**Semantics**
- In debug mode, evaluates `<bool>`.
- If the result is non-zero, `ASSERT` does nothing.
- If the result is `0`, `ASSERT` raises a script error and stops normal script execution.
- Outside debug mode, `ASSERT` is a complete no-op: the argument is not even parsed or validated.

**Errors & validation**
- In debug mode, parse / argument-validation errors are handled normally.
- In debug mode, runtime error if `<bool>` evaluates to `0`.
- Outside debug mode, `ASSERT` never raises argument-parsing errors because the argument is skipped entirely.

**Examples**
- `ASSERT TARGET >= 0`

**Progress state**
- complete
