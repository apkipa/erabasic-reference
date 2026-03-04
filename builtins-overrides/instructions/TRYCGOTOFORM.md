**Summary**
- Like `TRYGOTOFORM`, but supports a `CATCH ... ENDCATCH` block for the “not found” case.

**Tags**
- calls

**Syntax**
- `TRYCGOTOFORM <formString>`
- `CATCH`
  - `<catch body>`
  - `ENDCATCH`

**Arguments**
- Same as `GOTOFORM`.

**Semantics**
- Same as `TRYCGOTO`, but with a runtime-evaluated label name.

**Errors & validation**
- Same as `TRYCGOTO`.

**Examples**
- `TRYCGOTOFORM "LABEL_%RESULT%"`
- `CATCH`
- `  PRINTL "label missing"`
- `ENDCATCH`

**Progress state**
- complete
