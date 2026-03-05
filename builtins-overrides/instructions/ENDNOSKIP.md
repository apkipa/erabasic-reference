**Summary**
- Ends a `NOSKIP ... ENDNOSKIP` block.

**Tags**
- skip-mode

**Syntax**
- `ENDNOSKIP`

**Arguments**
- None.

**Semantics**
- Structural marker paired with `NOSKIP`.
- See `NOSKIP` for the block’s runtime behavior (temporary disabling and restoration of output skipping).

**Errors & validation**
- `ENDNOSKIP` without a matching open `NOSKIP` is a load-time error (the line is marked as error).

**Examples**
- (See `NOSKIP`.)

**Progress state**
- complete
