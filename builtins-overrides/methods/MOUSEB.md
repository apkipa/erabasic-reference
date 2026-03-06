**Summary**
- Returns the input value of the currently pointed normal-output button, as a string.

**Tags**
- ui
- input

**Syntax**
- `MOUSEB()`

**Signatures / argument rules**
- Signature: `string MOUSEB()`.

**Arguments**
- None.

**Semantics**
- Recomputes the current hover state from the actual mouse position, then inspects the currently pointed **normal-output button**.
- If the pointed output object is a button:
  - string button → returns its string input,
  - integer button → returns its integer input converted to decimal text.
- Returns `""` if:
  - no normal-output button is currently pointed,
  - the pointed object is not a button.
- Boundary note:
  - this follows the normal output-button hover model,
  - it does **not** expose CBG button-map values,
  - see `cbg-layer.md` for the separate CBG hit-map/value path.

**Errors & validation**
- None.

**Examples**
- `S = MOUSEB()`

**Progress state**
- complete
