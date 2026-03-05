**Summary**
- Reports whether the script runner is currently in “skip output” mode.

**Tags**
- runtime

**Syntax**
- `ISSKIP()`

**Signatures / argument rules**
- `ISSKIP()` → `long`

**Arguments**
- (none)

**Semantics**
- Returns `1` if skip-print mode is active, otherwise returns `0`.

**Errors & validation**
- (none)

**Examples**
- `if ISSKIP() == 0: PRINTFORML "not skipping"`

**Progress state**
- complete

