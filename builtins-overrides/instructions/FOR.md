**Summary**
- Begins a `FOR ... NEXT` counted loop over a mutable integer variable term.

**Tags**
- control-flow

**Syntax**
- `FOR <intVarTerm>, <start>, <end> [, <step>]`
- Start may be omitted by leaving an empty slot: `FOR <intVarTerm>, , <end> [, <step>]`
  - `...`
  - `NEXT`

**Arguments**
- `<intVarTerm>`: changeable integer variable term (must not be character-data).
- `<start>`: int expression (defaults to `0` if omitted via an empty argument).
- `<end>`: int expression.
- `<step>`: int expression (defaults to `1` if omitted).

- Omitted arguments / defaults:
  - `<start>` defaults to `0` when omitted as an empty argument.
  - `<step>` defaults to `1` when omitted.

**Semantics**
- Initializes the counter variable to `<start>`, then loops while:
  - `step > 0`: `<counter> < <end>`
  - `step < 0`: `<counter> > <end>`
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
