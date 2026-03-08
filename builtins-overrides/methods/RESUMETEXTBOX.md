**Summary**
- Immediately restores the textbox to its original/default position.

**Tags**
- ui
- input

**Syntax**
- `RESUMETEXTBOX(dummyX, dummyY, dummyWidth)`

**Signatures / argument rules**
- `RESUMETEXTBOX(dummyX, dummyY, dummyWidth)` → `long`

**Arguments**
- `dummyX` (int): ignored.
- `dummyY` (int): ignored.
- `dummyWidth` (int): ignored.

**Semantics**
- Current-build quirk: the function is registered with a three-integer call shape, but ignores all three values.
- Restores the textbox position/size to the host's remembered original/default textbox placement immediately.
- Clears the pending custom textbox-position state.
- Returns `1`.

**Errors & validation**
- Argument type/count errors follow the current three-integer registration.

**Examples**
- `RESUMETEXTBOX(0, 0, 0)`

**Progress state**
- complete
