**Summary**
- “Single-line IF”: conditionally skips the **next logical line only**.

**Syntax**
- `SIF <int expr>`
  - `<next logical line>`

**Arguments**
- `<int expr>`: evaluated as integer; zero = false, non-zero = true.

**Defaults / optional arguments**
- If the expression is omitted, it defaults to `0` (false) and emits a load-time warning.

**Semantics**
- If the condition is true (non-zero), execution continues normally.
- If the condition is false (zero), the engine advances the program counter one extra time (skipping exactly one logical line).
- Load-time validation enforces an inherent limitation of this “skip the next line” model:
  - If the following line is a **structural marker / partial instruction** (e.g. `IF`, `ELSE`, `CASE`, loop markers), the engine warns because skipping marker lines breaks block structure.
  - If the following line is a `$label` line, the engine warns.
  - If there is no following executable line (EOF / next `@label`), the engine warns.

**Errors & validation**
- The engine issues warnings when `SIF` is followed by an invalid line kind; behavior may become engine-version-dependent if such warnings are ignored.

**Examples**
- `SIF A == 0`
- `PRINTL "A is non-zero"`
