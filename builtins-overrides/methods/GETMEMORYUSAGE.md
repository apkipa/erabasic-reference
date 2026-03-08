**Summary**
- Returns the current process working-set size in bytes.

**Tags**
- runtime

**Syntax**
- `GETMEMORYUSAGE()`

**Signatures / argument rules**
- `GETMEMORYUSAGE()` → `long`

**Arguments**
- None.

**Semantics**
- Returns the current process `WorkingSet64` value.
- The unit is bytes.
- This is an operating-system working-set measurement, not a managed-heap-only measurement.

**Errors & validation**
- None.

**Examples**
- `bytes = GETMEMORYUSAGE()`

**Progress state**
- complete
