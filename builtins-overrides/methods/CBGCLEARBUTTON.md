**Summary**
- Removes all CBG button sprites and also clears the current CBG button-hit map.

**Tags**
- ui
- graphics

**Syntax**
- `CBGCLEARBUTTON()`

**Signatures / argument rules**
- Signature: `int CBGCLEARBUTTON()`.

**Arguments**
- None.

**Semantics**
- Removes every currently registered **CBG button sprite** from the client-background (`CBG`) layer.
- Also clears the current CBG button-hit map and resets current CBG button selection state.
- Layer boundary:
  - this affects only the CBG/background-button layer,
  - it does not modify the normal output model, pending print buffer, or HTML-island layer.
- Observable consequence:
  - any CBG buttons disappear,
  - CBG mouse hit-testing no longer finds those buttons.
- Return value: always returns `1`.

**Errors & validation**
- None.

**Examples**
- `R = CBGCLEARBUTTON()`

**Progress state**
- complete
