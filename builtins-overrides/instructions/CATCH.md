**Summary**
- Begins the catch-body of a `TRYC* ... CATCH ... ENDCATCH` construct.

**Tags**
- error-handling

**Syntax**
```text
CATCH
    <catch body>
ENDCATCH
```

- Header line: `CATCH`
- Terminator line: `ENDCATCH`

**Arguments**
- None.

**Semantics**
- When reached **sequentially** (i.e. the `TRYC*` succeeded and returned normally), `CATCH` jumps to the matching `ENDCATCH` marker, skipping the catch body.
- When entered by a failed `TRYC*` instruction, execution jumps to the `CATCH` marker and (due to the engine’s advance-first model) begins executing at the first line of the catch body.

**Errors & validation**
- `CATCH` without a matching open `TRYC*` is a load-time error (the line is marked as error).

**Examples**
```erabasic
TRYCCALL OPTIONAL_HOOK
CATCH
    PRINTL hook missing
ENDCATCH
```

**Progress state**
- complete
