**Summary**
- Like `TRYCALLFORM`, but supports a `CATCH ... ENDCATCH` block for the “not found” case.

**Tags**
- calls

**Syntax**
- `TRYCCALLFORM <formString> [, <arg1>, ... ]`
- `CATCH`
  - `<catch body>`
  - `ENDCATCH`

**Arguments**
- Same as `CALLFORM`.

- Omitted arguments / defaults:
  - Same as `CALLFORM`.

**Semantics**
- Same as `TRYCCALL`, but with a runtime-evaluated function name.

**Errors & validation**
- Same as `TRYCCALL`.

**Examples**
- `TRYCCALLFORM "HOOK_%TARGET%"`
- `CATCH`
- `  PRINTL "hook missing"`
- `ENDCATCH`

**Progress state**
- complete
