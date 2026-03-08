**Summary**
- Configures the redraw timer used for animated sprites during ordinary waits.

**Tags**
- graphics
- sprites

**Syntax**
- `SETANIMETIMER(time)`

**Signatures / argument rules**
- `SETANIMETIMER(time)` → `long`

**Arguments**
- `time` (int): requested redraw interval in milliseconds.

**Semantics**
- Accepts only `time >= -2147483648` and `time <= 32767` in this build.
- If `time <= 0`, disables the redraw timer.
- If `1 <= time < 10`, enables the timer with an actual interval of `10` milliseconds.
- If `time >= 10`, enables the timer with that interval.
- Returns `1`.

**Errors & validation**
- Runtime error if `time < -2147483648` or `time > 32767`.

**Examples**
- `SETANIMETIMER 16`

**Progress state**
- complete
