**Summary**
- Invokes an event function by event-dispatch semantics rather than by ordinary `CALL` semantics.

**Tags**
- calls

**Syntax**
- `CALLEVENT <eventFunction>`

**Arguments**
- `<eventFunction>` (raw event-function name): target event name.
  - This is not a string expression and no arguments can be passed through `CALLEVENT`.

**Semantics**
- Resolves `<eventFunction>` as an event-function name.
- If the name exists as an event function, `CALLEVENT` runs the same grouped event-dispatch sequence described in `runtime-model.md`:
  - group 0: `#ONLY`
  - group 1: `#PRI`
  - group 2: normal
  - group 3: `#LATER`
- `#SINGLE` / `#ONLY` affect progression exactly as in ordinary event dispatch.
- If no event function with that name exists and no non-event function with that name exists, the instruction is a silent no-op.

**Errors & validation**
- Runtime error if `<eventFunction>` names a non-event function instead of an event function.
- Runtime error if any event call is already active on the call stack; event calls cannot nest.
- Load-time warning if a `CALLEVENT` line is written inside an event function body, because such execution would always violate the non-nesting rule.

**Examples**
- `CALLEVENT EVENTLOAD`

**Progress state**
- complete
