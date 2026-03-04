**Summary**
- “Single-line IF”: conditionally skips the **next logical line only**.

**Tags**
- control-flow

**Syntax**
- `SIF <int expr>`
  - `<next logical line>`

**Arguments**
- `<int expr>`: evaluated as integer; zero = false, non-zero = true.

- Omitted arguments / defaults:
  - If the expression is omitted, it defaults to `0` (false) and emits a load-time warning.

**Semantics**
- If the condition is true (non-zero), execution continues normally.
- If the condition is false (zero), the engine advances the program counter one extra time (skipping exactly one logical line).
- Load-time validation enforces an inherent limitation of this “skip the next line” model:
  - If the following line is a **partial instruction** (structural marker / block delimiter; e.g. `IF`, `ELSE`, `CASE`, loop markers), the engine warns because skipping marker lines breaks block structure.
  - If the following line is a `$label` line, the engine warns.
  - If there is no following executable line (EOF / next `@label`), the engine warns.
  - If there is at least one physically empty line between `SIF` and the next logical line, the engine warns.

**Errors & validation**
- Some invalid “next line” situations are treated as load-time errors (the `SIF` line is marked as error and cannot run safely), including:
  - no following logical line (EOF / next `@label`)
  - following line is a function label line (`@...`) or a null terminator line
  - following instruction line is a **partial instruction** (structural marker / block delimiter)
  - following line is a `$label` line
- The engine may also warn if there are physically empty line(s) between `SIF` and the next logical line.

**Examples**
- `SIF A == 0`
- `PRINTL "A is non-zero"`

**Progress state**
- complete
