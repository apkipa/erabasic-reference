**Summary**
- Checks whether a numbered save file exists and is loadable, and reports a short status message.

**Tags**
- save-files

**Syntax**
- `CHKDATA(saveIndex)`

**Signatures / argument rules**
- `CHKDATA(saveIndex)` → `long`

**Arguments**
- `saveIndex` (int): save slot index used to form the file name `save<saveIndex>.sav` (with at least 2 digits) under the save directory.

**Semantics**
- Checks the save file and returns a status code:
  - `0`: OK (loadable)
  - `1`: file not found
  - `2`: different game
  - `3`: different version
  - `4`: other error (corrupt / read error / type mismatch)
- Also writes a message string to `RESULTS:0`:
  - for OK: the save message stored in the file
  - for not found: `"----"`
  - for errors: a human-readable error message

**Errors & validation**
- Runtime error if `saveIndex < 0` or `saveIndex > 2147483647`.

**Examples**
- `state = CHKDATA(0)`   ; checks `save00.sav`
- `msg = RESULTS:0`

**Progress state**
- complete

