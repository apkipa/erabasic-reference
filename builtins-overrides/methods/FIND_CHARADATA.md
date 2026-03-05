**Summary**
- Lists character-variable save files matching a wildcard pattern.

**Tags**
- save-files

**Syntax**
- `FIND_CHARADATA([pattern])`

**Signatures / argument rules**
- `FIND_CHARADATA()` → `long`
- `FIND_CHARADATA(pattern)` → `long`

**Arguments**
- `pattern` (optional, string; default `*`): wildcard pattern applied to the `<name>` part of `chara_<name>.dat`.

**Semantics**
- Searches the engine’s data directory for files matching `chara_<pattern>.dat`.
- Extracts each match’s `<name>` (the part after `chara_` and before the `.dat` extension).
- Writes the extracted names into the `RESULTS` string array starting at `RESULTS:0`:
  - If there are more matches than the `RESULTS` array length, only the first `length(RESULTS)` names are written.
  - If there are fewer matches than the `RESULTS` array length, entries past the written prefix are left unchanged.
- Returns the total number of matches found (including any not written due to truncation).

**Errors & validation**
- (none)

**Examples**
- `n = FIND_CHARADATA()`               ; list all `chara_*.dat`
- `n = FIND_CHARADATA("foo*")`         ; list `chara_foo*.dat`
- `first = RESULTS:0`

**Progress state**
- complete

