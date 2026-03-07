**Summary**
- Begins a `WHILE ... WEND` loop.

**Tags**
- control-flow

**Syntax**
```text
WHILE [<condition>]
    ...
WEND
```

- Header line: `WHILE [<condition>]`
- Terminator line: `WEND`

**Arguments**
- `<condition>` (optional, int; default `0`; omission emits a warning): loop condition (`0` = false, non-zero = true).

**Semantics**
- At `WHILE`, evaluates the condition:
  - If true, enters the body (next line).
  - If false, jumps to the matching `WEND` marker (exiting the loop).
- At `WEND`, the engine re-evaluates the `WHILE` condition and loops again if it is still true.

**Errors & validation**
- `WEND` without a matching open `WHILE` is a load-time error (the `WEND` line is marked as error).

**Examples**
```erabasic
WHILE I < 10
    I += 1
WEND
```

**Progress state**
- complete
