**Summary**
- Timed wait: waits for a limited time (and optionally disallows user input), then continues.

**Syntax**
- `TWAIT <timeMs>, <mode>`

**Arguments**
- `<timeMs>`: integer expression; time limit in milliseconds.
- `<mode>`: integer expression:
  - `0`: wait for Enter/click, but time out after `<timeMs>`.
  - non-zero: disallow input and simply wait `<timeMs>` (or be affected by macro/skip behavior).

**Defaults / optional arguments**
- None.

**Semantics**
- Implementation detail: `TWAIT` first calls an Enter-style wait, then replaces it with a timed `WaitInput` request.
- Creates an `InputRequest` with:
  - `InputType = EnterKey` if `<mode> == 0`, otherwise `Void`
  - `Timelimit = <timeMs>`
- When the time limit elapses, execution continues automatically.
- Does not assign `RESULT`/`RESULTS`.
- Skipped when the script runner’s `skipPrint` mode is active (print-family skip rule).

**Errors & validation**
- Argument type errors follow the normal integer-expression argument rules.

**Examples**
- `TWAIT 3000, 0` (wait up to 3 seconds for Enter)
- `TWAIT 1000, 1` (wait 1 second with no input)

**Progress state**
- complete
