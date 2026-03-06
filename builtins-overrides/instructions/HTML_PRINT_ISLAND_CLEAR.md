**Summary**
- Clears all rows currently retained in the `HTML_PRINT_ISLAND` layer.

**Tags**
- io

**Syntax**
- `HTML_PRINT_ISLAND_CLEAR`

**Arguments**
- None.

**Semantics**
- Clears the retained island-layer state immediately.
- This affects only the island layer:
  - the normal output model is unchanged,
  - the pending print buffer is unchanged.
- This instruction is not skipped by output skipping; it always clears the island layer when executed.
- Repaint timing:
  - like `HTML_PRINT_ISLAND`, clearing changes stored state immediately,
  - but it does not itself force an immediate repaint,
  - so the disappearance becomes visible on the next repaint allowed/forced by the redraw schedule.

**Errors & validation**
- None.

**Examples**
```erabasic
HTML_PRINT_ISLAND_CLEAR
```

**Progress state**
- complete
