**Summary**
- Opens the engine’s interactive **load UI** (system-driven load).

**Syntax**
- `LOADGAME`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- Requires that the current system state allows saving/loading (same gate as `SAVEGAME`), otherwise raises an error.
- Saves the current process state for later restoration, then transitions into the system load flow.
- The system load flow (high-level behavior):
  - Displays save slots `0..Config.SaveDataNos-1` in pages of 20.
  - Includes a special autosave entry `99` when applicable (implementation detail).
  - Uses `100` as the “back/cancel” input.
  - After selecting a valid slot:
    - Loads the slot file (as `save{slot:00}.sav` under `Config.SavDir`).
    - Discards the previous saved process state.
    - Enters the same post-load system hook sequence as `LOADDATA`:
      - `SYSTEM_LOADEND` (if present)
      - `EVENTLOAD` (if present)
      - then returns to normal system flow (typically as if `BEGIN SHOP` occurred, unless `EVENTLOAD` performed a `BEGIN`).
- See also: `save-files.md` (directories, partitions, and on-disk formats)

**Errors & validation**
- Error if load is not allowed in the current system state.
- Selecting an empty slot prints a “no data” message and reopens the load prompt.
- If loading fails unexpectedly after selection, the engine throws an internal execution error.

**Examples**
- `LOADGAME`

**Progress state**
- complete
