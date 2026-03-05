**Summary**
- Begins a `FOR ... NEXT` counted loop over a mutable integer variable term.

**Tags**
- control-flow

**Syntax**
- `FOR <intVarTerm>, <start>, <end> [, <step>]`
  - `...`
  - `NEXT`

**Arguments**
- `<intVarTerm>`: changeable integer variable term (must not be character-data).
- `<start>` (optional, int; default `0`): initial counter value.
- `<end>` (int): loop bound (exclusive).
- `<step>` (optional, int; default `1`): increment applied at `NEXT` time.

**Semantics**
- Initializes the counter variable to `<start>`, then loops while:
  - `step > 0`: `<counter> < <end>`
  - `step < 0`: `<counter> > <end>`
- If `step == 0`, the loop body executes zero times (execution jumps directly to `NEXT`).
- The counter variable is incremented by `step` at `NEXT` time (and also by `BREAK`/`CONTINUE` for era-maker compatibility).

**Errors & validation**
- Errors if `<intVarTerm>` is not a changeable variable term, or if it is character-data.
- `NEXT` without a matching open `FOR` is a load-time error (the `NEXT` line is marked as error).

**Examples**
- `FOR I, 0, 10`
- `  PRINTV I`
- `NEXT`

**Progress state**
- complete
