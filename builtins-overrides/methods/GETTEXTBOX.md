**Summary**
- Returns the current contents of the host textbox widget.

**Tags**
- ui
- input

**Syntax**
- `GETTEXTBOX()`

**Signatures / argument rules**
- `GETTEXTBOX()` → `string`

**Arguments**
- None.

**Semantics**
- Returns the textbox's current text exactly as stored by the host widget at call time.
- This does not wait for input.
- This reads the live widget state, not a saved snapshot.

**Errors & validation**
- None.

**Examples**
- `s = GETTEXTBOX()`

**Progress state**
- complete
