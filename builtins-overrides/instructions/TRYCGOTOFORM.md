**Summary**
- Like `TRYGOTOFORM`, but supports a `CATCH ... ENDCATCH` block for the “not found” case.

**Tags**
- calls

**Syntax**
```text
TRYCGOTOFORM <formString>
CATCH
    <catch body>
ENDCATCH
```

- Header line: `TRYCGOTOFORM <formString>`

**Arguments**
- Same as `GOTOFORM`.

**Semantics**
- Same as `TRYCGOTO`, but with a runtime-evaluated label name.

**Errors & validation**
- Same as `TRYCGOTO`.

**Examples**
```erabasic
TRYCGOTOFORM "LABEL_%RESULT%"
CATCH
    PRINTL "label missing"
ENDCATCH
```

**Progress state**
- complete
