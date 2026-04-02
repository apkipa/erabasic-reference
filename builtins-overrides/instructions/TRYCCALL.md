**Summary**
- Like `TRYCALL`, but supports a `CATCH ... ENDCATCH` block for the “not found” case.

**Tags**
- calls

**Syntax**
```text
TRYCCALL <target>
CATCH
    <catch body>
ENDCATCH
```

- `<target>` can be:
  - `functionName`
  - `functionName()`
  - `functionName, <arg1> [, <arg2> ... ]`
  - `functionName(<arg1> [, <arg2> ... ])`
  - `functionName[<subName1>, <subName2>, ...]`
  - `functionName[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`

> **Note:** The bracketed `[...]` segment is accepted for backward compatibility, but is currently unused.

**Arguments**
- Same as `CALL`.

**Semantics**
- If the target function exists: behaves like `CALL`, then control returns and reaches `CATCH` sequentially; `CATCH` skips the catch body.
- If the function does not exist: jumps to the `CATCH` marker (so execution begins at the first line of the catch body).

**Errors & validation**
- Still errors for invalid argument binding/type conversion when a function is found.
- Mis-nesting (`CATCH` without `TRYC*`, `ENDCATCH` without `CATCH`) is a load-time error (the line is marked as error).

**Examples**
```erabasic
TRYCCALL OPTIONAL_HOOK
CATCH
    PRINTL hook missing
ENDCATCH
```

**Progress state**
- complete
