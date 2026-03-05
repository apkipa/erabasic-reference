**Summary**
- Immediately executes a specific train command (by `TRAINNAME` index) within the train system phase.

**Tags**
- system

**Syntax**
- `DOTRAIN <trainIndex>`

**Arguments**
- `<trainIndex>` (int expression): index into `TRAINNAME` (from `train.csv`).

**Semantics**
- Valid only in specific train-phase internal states (e.g. during `@EVENTTRAIN`, `@SHOW_STATUS`, `@SHOW_USERCOM`, or `@EVENTCOMEND` processing).
- Sets `SELECTCOM = <trainIndex>` and advances the train system state to execute that command as if it was selected.

**Errors & validation**
- Runtime error if executed outside the allowed train-phase states.
- Runtime error if `<trainIndex> < 0` or `<trainIndex> >= length(TRAINNAME)`.

**Examples**
- `DOTRAIN 5`

**Progress state**
- complete
