**Summary**
- Timed wait: waits for a limited time (and optionally disallows user input), then continues.

**Tags**
- io

**Syntax**
- `TWAIT <timeMs>, <mode>`

**Arguments**
- `<timeMs>`: integer expression; time limit in milliseconds.
- `<mode>`: integer expression:
  - `0`: wait for Enter/click, but time out after `<timeMs>`.
  - non-zero: disallow input and simply wait `<timeMs>` (or be affected by macro/skip behavior).

**Semantics**
- If `<mode> == 0`: waits for Enter/click, but times out after `<timeMs>`.
- If `<mode> != 0`: disallows input and simply waits `<timeMs>` (but can still be affected by macro/skip behavior).
- When the time limit elapses, execution continues automatically.
- Does not assign `RESULT`/`RESULTS`.
- Skipped when output skipping is active (via `SKIPDISP`).

**Errors & validation**
- Argument type errors follow the normal integer-expression argument rules.

**Examples**
- `TWAIT 3000, 0` (wait up to 3 seconds for Enter)
- `TWAIT 1000, 1` (wait 1 second with no input)

**Progress state**
- complete
