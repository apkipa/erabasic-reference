**Summary**
- Like `TRYJUMPFORM`, but supports a `CATCH ... ENDCATCH` block for the “not found” case.

**Tags**
- calls

**Syntax**
```text
TRYCJUMPFORM <target>
CATCH
    <catch body>
ENDCATCH
```

- `<target>` can be:
  - `<formString>`
  - `<formString>()`
  - `<formString>, <arg1> [, <arg2> ... ]`
  - `<formString>(<arg1> [, <arg2> ... ])`
  - `<formString>[<subName1>, <subName2>, ...]`
  - `<formString>[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`

> **Note:** The bracketed `[...]` segment is accepted for backward compatibility, but is currently unused.

**Arguments**
- Same as `JUMPFORM`.

**Semantics**
- Same as `TRYCJUMP`, but with a runtime-evaluated function name.

**Errors & validation**
- Same as `TRYCJUMP`.

**Examples**
```erabasic
TRYCJUMPFORM OPTIONAL_{COUNT}
CATCH
    PRINTL missing
ENDCATCH
```

**Progress state**
- complete
