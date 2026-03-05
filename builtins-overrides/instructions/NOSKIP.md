**Summary**
- Begins a `NOSKIP ... ENDNOSKIP` block that temporarily disables output skipping within the block body.
- Intended to force some output/wait behavior to run even if `SKIPDISP` is currently skipping print-family instructions.

**Tags**
- skip-mode

**Syntax**
- `NOSKIP`
  - `...`
- `ENDNOSKIP`

**Arguments**
- None.

**Semantics**
- This is a structural block (`NOSKIP` pairs with `ENDNOSKIP`).
- At runtime when `NOSKIP` is executed:
  - If the matching `ENDNOSKIP` was not linked by the loader, the engine throws an error.
  - Remembers whether output skipping is currently enabled.
  - If output skipping is currently enabled, disables it for the duration of the block.
- At runtime when `ENDNOSKIP` is executed:
  - If output skipping was enabled at block entry, re-enables it (restoring skip mode).
  - If output skipping was disabled at block entry, does nothing (so if you enabled skip inside the block manually, it remains enabled).

**Errors & validation**
- Load-time structure errors (the line is marked as error):
  - Nested `NOSKIP` is not allowed.
  - `ENDNOSKIP` without a matching open `NOSKIP` is an error.
  - Missing `ENDNOSKIP` at end of file/load is an error.
- Runtime error if the loader failed to link the matching `ENDNOSKIP` (should not happen in a successfully loaded script).

**Examples**
```erabasic
SKIPDISP 1

NOSKIP
  PRINTL This line still prints even during SKIPDISP.
ENDNOSKIP
```

**Progress state**
- complete
