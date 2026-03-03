**Summary**
- Requests a transition into one of the engine’s **system phases** (e.g. `SHOP`, `TRAIN`, `TITLE`) after the current call stack unwinds.

**Syntax**
- `BEGIN <keyword>`

**Arguments**
- `<keyword>`: raw string (the entire remainder of the source line after the instruction delimiter).
  - Must match one of the supported keywords exactly (see below).
  - The current engine compares this string literally (no automatic trim or case-folding).

**Defaults / optional arguments**
- None.

**Semantics**
- Recognized keywords (engine-defined):
  - `SHOP`, `TRAIN`, `AFTERTRAIN`, `ABLUP`, `TURNEND`, `FIRST`, `TITLE`
- On execution:
  - Validates `<keyword>` by matching it against the list above; otherwise raises an error.
  - Sets an internal “begin type” on the process state.
  - Immediately performs some keyword-specific side effects:
    - `SHOP` and `FIRST` unload temporary loaded image resources (implementation detail).
  - Calls `state.Return(0)`:
    - This starts unwinding the current EraBasic call stack.
    - When unwinding reaches the top-level (no return address), the engine performs the actual system-phase transition (`state.Begin()`), clears the function stack, and continues execution in the new system state.
  - Resets console style (`Console.ResetStyle()`).

**Errors & validation**
- If `<keyword>` is not recognized, raises a runtime error (“invalid BEGIN argument”).

**Examples**
- `BEGIN TITLE`
- `BEGIN SHOP`

**Progress state**
- complete

