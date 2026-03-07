**Summary**
- Fills one character-variable element across a range of registered characters.

**Tags**
- variables

**Syntax**
- `CVARSET <characterVariable>`
- `CVARSET <characterVariable>, <index>, <value>`
- `CVARSET <characterVariable>, <index>, <value>, <startID>, <endID>`

**Arguments**
- `<characterVariable>` (writable character-data variable): target variable.
  - 2D character-data variables are not accepted.
- `<index>` (optional; default `0`): element selector used when `<characterVariable>` has a per-character 1D payload.
  - May be an int index or a string key accepted by that variable.
  - If the target has no such 1D payload, this argument is ignored.
- `<value>` (optional; default `0` / `""`): replacement value.
  - Omission uses `0` for int targets and `""` for string targets.
- `<startID>` / `<endID>` (optional, int): registered-character range.
  - Omission means `startID = 0` and `endID = CHARANUM`.
  - `endID` is exclusive, so `CVARSET CFLAG, 10, 123, 1, 4` affects character indices `1`, `2`, and `3`.

**Semantics**
- Applies the assignment to each registered character index in the half-open range `[startID, endID)`.
- If `startID > endID`, the engine swaps them before filling.
- If `<characterVariable>` has a 1D per-character payload, `<index>` selects which element is written for each character.
- If `<characterVariable>` does not have a 1D per-character payload, `<index>` does not change which field is written.
- If `CHARANUM == 0`, the instruction has no effect.

**Errors & validation**
- Parse / argument-validation error if `<characterVariable>` is missing, is not a writable character-data variable, is 2D character-data, or `<value>` has the wrong type.
- Runtime error if `startID` or `endID` is outside `0 <= id <= CHARANUM`.
- Runtime error if a string `<index>` does not name a defined key for that variable.

**Examples**
- `CVARSET CFLAG, 10, 123`
- `CVARSET CSTR, 0, "", 0, CHARANUM`

**Progress state**
- complete
