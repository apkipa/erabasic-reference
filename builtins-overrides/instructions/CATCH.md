**Summary**
- Begins the catch-body of a `TRYC* ... CATCH ... ENDCATCH` construct.

**Syntax**
- `CATCH`
  - `<catch body>`
  - `ENDCATCH`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- When reached **sequentially** (i.e. the `TRYC*` succeeded and returned normally), `CATCH` jumps to the matching `ENDCATCH` marker, skipping the catch body.
- When entered by a failed `TRYC*` instruction, execution jumps to the `CATCH` marker and (due to the engine’s advance-first model) begins executing at the first line of the catch body.

**Errors & validation**
- `CATCH` without a matching open `TRYC*` produces a load-time warning.

**Examples**
- `CATCH`
- `  PRINTL "not found"`
- `ENDCATCH`
