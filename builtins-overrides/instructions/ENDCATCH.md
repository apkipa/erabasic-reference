**Summary**
- Ends a `CATCH ... ENDCATCH` block.

**Syntax**
- `ENDCATCH`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- Marker-only instruction (no runtime effect). The loader links it to the matching `CATCH` so that `CATCH` can skip the catch body on the success path.

**Errors & validation**
- `ENDCATCH` without a matching open `CATCH` produces a load-time warning.

**Examples**
- `ENDCATCH`
