**Summary**
- Clears the current CBG button-hit map without removing the CBG button sprites themselves.

**Tags**
- ui
- graphics

**Syntax**
- `CBGREMOVEBMAP()`

**Signatures / argument rules**
- Signature: `int CBGREMOVEBMAP()`.

**Arguments**
- None.

**Semantics**
- Clears the current CBG button-hit map and resets current CBG button selection state.
- It does **not** remove existing CBG button sprites from the visual CBG layer.
- Observable consequence:
  - previously placed CBG button sprites can remain visible,
  - but CBG hit-testing/hover selection no longer finds them until a new button-hit map is installed.
- Layer boundary:
  - this affects only the CBG/background-button interaction state,
  - it does not modify the normal output model, pending print buffer, or HTML-island layer.
- Return value: always returns `1`.

**Errors & validation**
- None.

**Examples**
- `R = CBGREMOVEBMAP()`

**Progress state**
- complete
