**Summary**
- Like `TRYCALLLIST`, but performs a `JUMP` into the first existing candidate.

**Tags**
- calls

**Syntax**
- `TRYJUMPLIST`
  - `FUNC <formString> [, <arg1>, ... ]`
  - `...`
  - `ENDFUNC`

**Arguments**
- Same as `TRYCALLLIST`.

**Semantics**
- Same selection rules as `TRYCALLLIST`.
- If a candidate function is found:
  - Enters it as a `JUMP` (tail-call behavior): when the callee returns, the current function also returns (the engine unwinds the call stack until a non-`JUMP` frame).
  - As a consequence, control does **not** return to the `ENDFUNC` line on success.
- If no candidate is found, jumps to the `ENDFUNC` line (then continues after it).

**Errors & validation**
- Same as `TRYCALLLIST`.

**Examples**
- `TRYJUMPLIST`
- `  FUNC PHASE_%COUNT%`
- `  FUNC PHASE_DEFAULT`
- `ENDFUNC`

**Progress state**
- complete
