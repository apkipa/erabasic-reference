**Summary**
- Polls a Windows virtual-key code and returns a one-shot trigger-style result.

**Tags**
- input

**Syntax**
- `GETKEYTRIGGERED(keyCode)`

**Signatures / argument rules**
- `GETKEYTRIGGERED(keyCode)` → `long`

**Arguments**
- `keyCode` (int): Windows virtual-key code.

**Semantics**
- If the game window is not active, returns `0`.
- If `keyCode < 0` or `keyCode > 255`, returns `0`.
- Otherwise polls Win32 `GetKeyState(keyCode)`.
- Returns `1` exactly when both conditions hold:
  - the key is currently down (`GetKeyState(keyCode) < 0`), and
  - the newly observed low-order/toggle-bit-derived snapshot for this `keyCode` differs from the previously remembered snapshot.
- Otherwise returns `0`.
- First-poll behavior:
  - the remembered snapshot starts empty,
  - so a key already down on the first observed poll for that `keyCode` returns `1`.
- Poll side effect shared with `GETKEY`:
  - each call updates the same remembered per-key snapshot used by future trigger checks,
  - so polling either `GETKEY(keyCode)` or `GETKEYTRIGGERED(keyCode)` can affect later `GETKEYTRIGGERED(keyCode)` results.

**Errors & validation**
- None.

**Examples**
- `IF GETKEYTRIGGERED(13) != 0`

**Progress state**
- complete
