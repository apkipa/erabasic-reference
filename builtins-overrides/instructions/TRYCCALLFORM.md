**Summary**
- Like `TRYCALLFORM`, but supports a `CATCH ... ENDCATCH` block for the “not found” case.

**Tags**
- calls

**Syntax**
```text
TRYCCALLFORM <target>
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
- Same as `CALLFORM`.

**Semantics**
- Same as `TRYCCALL`, but with a runtime-evaluated function name.

**Errors & validation**
- Same as `TRYCCALL`.

**Examples**
```erabasic
TRYCCALLFORM "HOOK_%TARGET%"
CATCH
    PRINTL "hook missing"
ENDCATCH
```

**Progress state**
- complete
