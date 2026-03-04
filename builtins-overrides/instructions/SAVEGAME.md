**Summary**
- Opens the engine’s interactive **save UI** (system-driven save).

**Tags**
- save-system

**Syntax**
- `SAVEGAME`

**Arguments**
- None.

**Semantics**
- Requires that the current system state allows saving; otherwise raises an error.
- Saves the current process state for later restoration, then transitions into the system save flow.
- The system save flow (high-level behavior):
  - Displays save slots with indices `0 <= slot < Config.SaveDataNos` in pages of 20.
  - Uses `100` as the “back/cancel” input.
  - After selecting a slot:
    - If it already contains data, prompts for overwrite confirmation.
    - Initializes `SAVEDATA_TEXT` with the current timestamp (`yyyy/MM/dd HH:mm:ss `).
    - Calls `@SAVEINFO` (if it exists), which can append to `SAVEDATA_TEXT` (commonly via `PUTFORM`).
    - Saves the current state to the selected slot (as `save{slot:00}.sav` under `Config.SavDir`) using `SAVEDATA_TEXT` as the slot description text.
  - Returns to the previous system state after completion or cancellation.
- See also: `save-files.md` (directories, partitions, and on-disk formats)

**Errors & validation**
- Error if saving is not allowed in the current system state.
- If the underlying file write fails, the UI prints an error and waits for a key.

**Examples**
- `SAVEGAME`

**Progress state**
- complete
