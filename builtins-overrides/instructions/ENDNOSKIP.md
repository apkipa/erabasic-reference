**Summary**
- Ends a `NOSKIP ... ENDNOSKIP` block.

**Syntax**
- `ENDNOSKIP`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- Structural marker paired with `NOSKIP`.
- Restores `skipPrint` to its saved value when the block was entered (see `NOSKIP`).

**Errors & validation**
- `ENDNOSKIP` without a matching open `NOSKIP` is a load-time error (the line is marked as error).

**Examples**
- (See `NOSKIP`.)

**Progress state**
- complete
