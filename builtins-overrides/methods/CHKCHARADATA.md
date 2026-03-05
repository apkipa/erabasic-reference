**Summary**
- Checks whether a character-variable save file exists and is loadable, and reports a short status message.

**Tags**
- save-files

**Syntax**
- `CHKCHARADATA(name)`

**Signatures / argument rules**
- `CHKCHARADATA(name)` → `long`

**Arguments**
- `name` (string): the save “name” suffix used to form the file name `chara_<name>.dat` under the engine’s data directory.

**Semantics**
- Checks the file `chara_<name>.dat` and returns a status code:
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
- (none)

**Examples**
- `state = CHKCHARADATA("00")`
- `msg = RESULTS:0`

**Progress state**
- complete

