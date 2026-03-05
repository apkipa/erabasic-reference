**Summary**
- Opens the engine’s interactive **load UI** (system-driven load).

**Tags**
- save-system

**Syntax**
- `LOADGAME`

**Arguments**
- None.

**Semantics**
- Requires that the current system state allows saving/loading (same gate as `SAVEGAME`), otherwise raises an error.
- Saves the current process state for later restoration, then transitions into the system load flow.
- The system load flow (high-level behavior):
  - Displays save slots with indices `0 <= slot < SaveDataNos` in pages of 20.
  - Includes a special autosave entry `99` when applicable.
  - Uses `100` as the “back/cancel” input.
  - After selecting a valid slot:
    - Loads the slot file (as `save{slot:00}.sav` under `SavDir`).
    - Discards the previous saved process state.
    - Enters the same post-load system hook sequence as `LOADDATA`:
      - `SYSTEM_LOADEND` (if present)
      - `EVENTLOAD` (if present)
      - then returns to normal system flow (typically as if `BEGIN SHOP` occurred, unless `EVENTLOAD` performed a `BEGIN`).
- See also: `save-files.md` (directories, partitions, and on-disk formats)

**Errors & validation**
- Error if load is not allowed in the current system state.
- Selecting an empty slot prints a “no data” message and reopens the load prompt.
- If loading fails unexpectedly after selection, raises a runtime error.

**Examples**
- `LOADGAME`

**Progress state**
- complete
