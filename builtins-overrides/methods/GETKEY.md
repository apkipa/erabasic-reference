**Summary**
- Polls a Windows virtual-key code and returns whether it is currently down.

**Tags**
- input

**Syntax**
- `GETKEY(keyCode)`

**Signatures / argument rules**
- `GETKEY(keyCode)` → `long`

**Arguments**
- `keyCode` (int): Windows virtual-key code.

**Semantics**
- If the game window is not active, returns `0`.
- If `keyCode < 0` or `keyCode > 255`, returns `0`.
- Otherwise polls Win32 `GetKeyState(keyCode)`.
- Returns `1` if the polled state is currently down (`GetKeyState(keyCode) < 0`), otherwise `0`.
- Poll side effect shared with `GETKEYTRIGGERED`:
  - each call updates the engine's remembered per-key trigger snapshot for that same `keyCode`,
  - so calling `GETKEY` can affect the next `GETKEYTRIGGERED(keyCode)` result.

**Errors & validation**
- None.

**Examples**
- `IF GETKEY(13) != 0`

**Progress state**
- complete
