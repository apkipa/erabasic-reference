**Summary**
- Like `TRYJUMP`, but supports a `CATCH ... ENDCATCH` block for the “not found” case.

**Tags**
- calls

**Syntax**
```text
TRYCJUMP <target>
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
- Same as `JUMP`.

**Semantics**
- If the target function exists: behaves like `JUMP` (tail-call-like); the current function is discarded, so it does not return to reach `CATCH`.
- If the function does not exist: jumps to the `CATCH` marker (entering the catch body).

**Errors & validation**
- Still errors for invalid argument binding/type conversion when a function is found.

**Examples**
```erabasic
TRYCJUMP OPTIONAL_PHASE
CATCH
    PRINTL "phase missing"
ENDCATCH
```

**Progress state**
- complete
