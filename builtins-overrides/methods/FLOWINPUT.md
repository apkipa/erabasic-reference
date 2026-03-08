**Summary**
- Updates persistent system-flow integer-input behavior flags and defaults.

**Tags**
- input
- system-flow

**Syntax**
- `FLOWINPUT(defaultValue [, allowMouseInput [, allowSkip [, forceSkip]]])`

**Signatures / argument rules**
- `FLOWINPUT(defaultValue)` → `long`
- `FLOWINPUT(defaultValue, allowMouseInput)` → `long`
- `FLOWINPUT(defaultValue, allowMouseInput, allowSkip)` → `long`
- `FLOWINPUT(defaultValue, allowMouseInput, allowSkip, forceSkip)` → `long`

**Arguments**
- `defaultValue` (int): stored default integer value for later system-flow waits.
- `allowMouseInput` (optional, int): when supplied, non-zero enables system-flow mouse/default handling; `0` disables it.
- `allowSkip` (optional, int): when supplied, non-zero enables skip-driven default resolution for later system-flow waits; `0` disables it.
- `forceSkip` (optional, int): when supplied, non-zero forces later system-flow waits to prefill the default result immediately; `0` disables it.

**Semantics**
- This function does not perform an input wait by itself.
- It mutates persistent process-level flags used later by system-flow waits such as title/shop/save/load flow input prompts.
- Field update rules:
  - `defaultValue` is always overwritten,
  - each later optional flag is overwritten only when that argument is supplied,
  - omitted later arguments leave their previous stored values unchanged.
- Future system-flow waits use these stored values as follows:
  - if `allowMouseInput != 0`, the wait request carries an integer default and enables system-flow mouse input,
  - if `allowSkip != 0` and message-skip is active, the default integer result is prefilled before the wait state is entered,
  - if `forceSkip != 0`, the default integer result is prefilled before the wait state is entered even without message-skip.
- These flags affect only system-flow waits built on the engine's dedicated system-input path, not ordinary script `INPUT*` statements.
- Returns `0`.

**Errors & validation**
- None beyond normal integer-argument evaluation.

**Examples**
- `FLOWINPUT(0, 1, 1, 0)`

**Progress state**
- complete
