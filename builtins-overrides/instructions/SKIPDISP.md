**Summary**
- Enables/disables Emuera’s “skip output” mode (`skipPrint`), which causes most print/wait/input built-ins to be skipped by the script runner.
- Also sets `RESULT` to indicate whether skip mode is currently enabled.

**Tags**
- skip-mode

**Syntax**
- `SKIPDISP <int expr>`

**Arguments**
- `<int expr>`: `0` disables skip mode; non-zero enables skip mode.

**Semantics**
- Evaluates `<int expr>` to `v`.
- Sets:
  - `skipPrint = (v != 0)`
  - `userDefinedSkip = (v != 0)` (used to distinguish “user requested skip” from internal engine skip states)
  - `RESULT = (skipPrint ? 1 : 0)`
- While `skipPrint` is true, the script execution loop *skips* any built-in instruction whose registration has the `IS_PRINT` flag (this includes `PRINT*`, `WAIT*`, `INPUT*`, etc.).
- Special case (runtime error): if `skipPrint` is true **and** `userDefinedSkip` is true, then encountering an `IS_INPUT` instruction causes a runtime error rather than silently skipping.

**Errors & validation**
- Argument type errors follow the normal integer-expression argument rules.
- Runtime error if an input instruction is reached while `skipPrint` is active due to `SKIPDISP`.

**Examples**
- `SKIPDISP 1` (enable skip)
- `SKIPDISP 0` (disable skip)

**Progress state**
- complete
