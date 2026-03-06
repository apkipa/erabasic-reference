**Summary**
- Clears the entire CBG layer and also clears the current CBG button-hit map.

**Tags**
- ui
- graphics

**Syntax**
- `CBGCLEAR()`

**Signatures / argument rules**
- Signature: `int CBGCLEAR()`.

**Arguments**
- None.

**Semantics**
- Removes all currently registered CBG entries from the client-background layer, including ordinary CBG images and CBG button sprites.
- Also clears the current CBG button-hit map and resets current CBG button selection state.
- Resource-ownership boundary:
  - this clears only the CBG-side registrations/references,
  - it does **not** dispose the underlying named sprite objects or graphics surfaces that had been referenced there.
- Layer boundary:
  - this affects only the CBG/background layer,
  - it does not modify the normal output model, pending print buffer, or HTML-island layer.
- Return value: always returns `1`.

**Errors & validation**
- None.

**Examples**
- `R = CBGCLEAR()`

**Progress state**
- complete
