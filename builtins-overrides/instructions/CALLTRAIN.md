**Summary**
- Enables “continuous train command execution” using the commands pre-populated in `SELECTCOM`.

**Tags**
- system

**Syntax**
- `CALLTRAIN <count>`

**Arguments**
- `<count>` (int expression): number of commands to take from `SELECTCOM`.

**Semantics**
- Reads the current `SELECTCOM` array and enqueues `SELECTCOM[1] .. SELECTCOM[count]` (inclusive) as a command list.
- While this mode is active, the train loop consumes the queued commands automatically instead of waiting for user input.
- When the queued command list is exhausted, the engine exits the mode and (if present) calls `@CALLTRAINEND`.

**Errors & validation**
- Runtime error if `<count> >= length(SELECTCOM)`.
- `<count> <= 0` is not explicitly rejected by the engine, but results in an empty queue and is not useful (avoid).

**Examples**
- `CALLTRAIN 3` (use `SELECTCOM[1]`, `SELECTCOM[2]`, `SELECTCOM[3]`)

**Progress state**
- complete
