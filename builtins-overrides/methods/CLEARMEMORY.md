**Summary**
- Forces a garbage collection and returns the change in process working-set size.

**Tags**
- runtime

**Syntax**
- `CLEARMEMORY()`

**Signatures / argument rules**
- `CLEARMEMORY()` → `long`

**Arguments**
- None.

**Semantics**
- Measures the current process working set.
- Runs `GC.Collect()`.
- Measures the working set again.
- Returns `before - after` in bytes.
- A positive value means the working set became smaller.
- A negative value is possible if the working set becomes larger instead.

**Errors & validation**
- None.

**Examples**
- `freed = CLEARMEMORY()`

**Progress state**
- complete
