**Summary**
- Forces a script error with a caller-provided message.

**Tags**
- debug

**Syntax**
- `THROW`
- `THROW <formedString>`

**Arguments**
- `<formedString>` (optional, string; default `""`): error message text.
  - This uses formed-string parsing, so `{...}` / `%%...%%` interpolation is available.

**Semantics**
- Evaluates `<formedString>` and immediately raises a script error.
- The resulting text is shown as the `THROW` message in the engine’s error report.
- No later statements in the current run are executed unless outer error-handling flow intercepts the error.

**Errors & validation**
- `THROW` always raises a script error after evaluating its message.
- Additional parse / evaluation errors can occur while forming `<formedString>`.

**Examples**
- `THROW Unexpected state: {TARGET}`
- `THROW`

**Progress state**
- complete
