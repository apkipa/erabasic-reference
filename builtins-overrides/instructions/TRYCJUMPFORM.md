**Summary**
- Like `TRYJUMPFORM`, but supports a `CATCH ... ENDCATCH` block for the “not found” case.

**Tags**
- calls

**Syntax**
- `TRYCJUMPFORM <formString> [, <arg1>, ... ]`
- `CATCH`
  - `<catch body>`
  - `ENDCATCH`

**Arguments**
- Same as `JUMPFORM`.

- Omitted arguments / defaults:
  - Same as `JUMPFORM`.

**Semantics**
- Same as `TRYCJUMP`, but with a runtime-evaluated function name.

**Errors & validation**
- Same as `TRYCJUMP`.

**Examples**
- `TRYCJUMPFORM "OPTIONAL_%COUNT%"`
- `CATCH`
- `  PRINTL "missing"`
- `ENDCATCH`

**Progress state**
- complete
