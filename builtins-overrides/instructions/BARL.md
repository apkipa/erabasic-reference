**Summary**
- Like `BAR`, but appends a newline after printing the bar.

**Tags**
- io

**Syntax**
- `BARL value, maxValue, length`

**Arguments**
- Same as `BAR`.

**Semantics**
- Prints the same bar string as `BAR value, maxValue, length`.
- Appends a newline after printing.
- If output skipping is active (`SKIPDISP` / `skipPrint`), this instruction is skipped like other print-family instructions.

**Errors & validation**
- Same as `BAR`.

**Examples**
```erabasic
BARL 114, 514, 81
```

**Progress state**
- complete
