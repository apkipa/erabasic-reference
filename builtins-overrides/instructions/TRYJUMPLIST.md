**Summary**
- Like `TRYCALLLIST`, but performs a `JUMP` into the first existing candidate.

**Syntax**
- `TRYJUMPLIST`
  - `FUNC <formString> [, <arg1>, ... ]`
  - `...`
  - `ENDFUNC`

**Arguments**
- Same as `TRYCALLLIST`.

**Defaults / optional arguments**
- None.

**Semantics**
- Same as `TRYCALLLIST`, but the chosen call behaves like `JUMP` (does not return to the current function).

**Errors & validation**
- Same as `TRYCALLLIST`.

**Examples**
- `TRYJUMPLIST`
- `  FUNC "PHASE_%COUNT%"`
- `  FUNC "PHASE_DEFAULT"`
- `ENDFUNC`
