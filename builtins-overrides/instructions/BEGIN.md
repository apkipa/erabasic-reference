**Summary**
- Requests a transition into one of the engine’s **system phases** (e.g. `SHOP`, `TRAIN`, `TITLE`) after the current call stack unwinds.

**Tags**
- system

**Syntax**
- `BEGIN <keyword>`

**Arguments**
- `<keyword>` (raw string): the entire remainder of the source line after the instruction delimiter.
  - Must match one of the supported keywords exactly (see below).
  - The current engine compares this string literally (no automatic trim or case-folding).

**Semantics**
- Recognized keywords (engine-defined):
  - `SHOP`, `TRAIN`, `AFTERTRAIN`, `ABLUP`, `TURNEND`, `FIRST`, `TITLE`
- On execution:
  - Validates `<keyword>` by matching it against the list above; otherwise raises an error.
  - Requests a transition into that system phase after the current call stack unwinds.
  - Immediately performs some keyword-specific side effects:
    - `SHOP` and `FIRST` unload temporary loaded image resources.
  - Ends the current function immediately (as if returning) and continues unwinding until reaching the top-level.
  - After reaching the top-level, enters the requested system phase, clears the call stack, and continues execution in that phase.
  - Resets output style to defaults.

**Errors & validation**
- If `<keyword>` is not recognized, raises a runtime error (“invalid BEGIN argument”).

**Examples**
- `BEGIN TITLE`
- `BEGIN SHOP`

**Progress state**
- complete
