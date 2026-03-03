**Summary**
- Resets global variables to their default values.

**Syntax**
- `RESETGLOBAL`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- Calls `VEvaluator.ResetGlobalData()`, which (high-level):
  - Resets global variables to default values.
  - Removes certain Emuera-private global/static data structures (implementation detail; e.g. XML/maps global/static extensions).
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- None.

**Examples**
- `RESETGLOBAL`

**Progress state**
- complete

