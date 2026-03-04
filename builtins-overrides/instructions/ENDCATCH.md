**Summary**
- Ends a `CATCH ... ENDCATCH` block.

**Tags**
- error-handling

**Syntax**
- `ENDCATCH`

**Arguments**
- None.

**Semantics**
- Marker-only instruction (no runtime effect). The loader links it to the matching `CATCH` so that `CATCH` can skip the catch body on the success path.

**Errors & validation**
- `ENDCATCH` without a matching open `CATCH` is a load-time error (the line is marked as error).

**Examples**
- `ENDCATCH`

**Progress state**
- complete
