**Summary**
- Begins an `IF ... ENDIF` block. Chooses the first true clause among `IF` / `ELSEIF` / `ELSE` and executes that clause body.

**Syntax**
- `IF <int expr>`
- `IF <int expr>`
  - `...`
  - `ELSEIF <int expr>`
  - `...`
  - `ELSE`
  - `...`
  - `ENDIF`

**Arguments**
- `<int expr>`: evaluated as integer; zero = false, non-zero = true.

**Defaults / optional arguments**
- If the expression is omitted, it defaults to `0` (false) and emits a load-time warning.

**Semantics**
- The loader builds an ordered clause list (`IF` header, then each `ELSEIF`, and optional `ELSE`) and links every clause header to the matching `ENDIF`.
- At runtime, the `IF` header evaluates its own condition and then each `ELSEIF` in order:
  - If a condition is true, the engine jumps to that clause header as a **marker**.
  - Because Emuera’s execution loop advances to `NextLine` before executing, jumping to a clause header causes the next executed line to be the **first line of that clause body**, not the header itself.
- If no condition matches:
  - If there is an `ELSE`, the engine jumps to the `ELSE` header marker (and thus executes the `ELSE` body).
  - Otherwise it jumps to the `ENDIF` marker (skipping the whole block).

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
