**Summary**
- Begins an `IF ... ENDIF` block. Chooses the first true clause among `IF` / `ELSEIF` / `ELSE` and executes that clause body.

**Tags**
- control-flow

**Syntax**
- `IF <int expr>`
  - `...`
  - `ELSEIF <int expr>`
  - `...`
  - `ELSE`
  - `...`
  - `ENDIF`

**Arguments**
- `<int expr>`: evaluated as integer; zero = false, non-zero = true.

- Omitted arguments / defaults:
  - If the expression is omitted, it defaults to `0` (false) and emits a load-time warning.

**Semantics**
- Evaluates its own condition and then each `ELSEIF` condition in order.
- If a condition is true, that clause’s body is selected and executed.
- If no condition matches:
  - If there is an `ELSE`, the `ELSE` body is executed.
  - Otherwise, the whole block is skipped.
- After any selected clause body finishes, the rest of the `IF` block is skipped and execution continues after the matching `ENDIF`.
- Jump behavior note (affects unstructured entry such as `GOTO` into blocks): when control transfers to an `IF`/`ELSEIF`/`ELSE` line as a jump target, execution begins at the **next** logical line (the clause body), not on the marker line itself. See `control-flow.md`.

**Errors & validation**
- `ELSE` / `ELSEIF` without a matching open `IF`, or `ENDIF` without a matching open `IF`, are load-time errors (the line is marked as error).
- `ELSEIF` after an `ELSE` produces a load-time warning.

**Examples**
- `IF FLAG`
- `  PRINTL "yes"`
- `ELSE`
- `  PRINTL "no"`
- `ENDIF`

**Progress state**
- complete
