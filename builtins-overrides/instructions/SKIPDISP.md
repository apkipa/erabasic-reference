**Summary**
- Enables/disables the engine’s “skip output” mode, which causes most print/wait/input built-ins to be skipped.
- Also sets `RESULT` to indicate whether skip mode is currently enabled.

**Tags**
- skip-mode

**Syntax**
- `SKIPDISP <int expr>`

**Arguments**
- `<int expr>`: `0` disables skip mode; non-zero enables skip mode.

**Semantics**
- Evaluates `<int expr>` to `v`.
- If `v != 0`, enables output skipping; otherwise disables it.
- Sets `RESULT` to:
  - `1` when output skipping is enabled
  - `0` when output skipping is disabled
- While output skipping is enabled, the script runner skips most output-producing instructions (print/wait/input families).
- Special case (runtime error): if output skipping was enabled by `SKIPDISP`, then encountering an input instruction (e.g. `INPUT*`) raises an error rather than being silently skipped.

**Errors & validation**
- Argument type errors follow the normal integer-expression argument rules.
- Runtime error if an input instruction is reached while output skipping is active due to `SKIPDISP`.

**Examples**
- `SKIPDISP 1` (enable skip)
- `SKIPDISP 0` (disable skip)

**Progress state**
- complete
