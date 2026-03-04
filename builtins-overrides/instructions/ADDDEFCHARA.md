**Summary**
- Performs the engine’s “default character initialization” step used at game start.

**Tags**
- characters
- system

**Syntax**
- `ADDDEFCHARA`

**Arguments**
- None.

**Semantics**
- Intended for use in `@SYSTEM_TITLE`.
- When executed, the engine adds:
  - the character template for CSV number `0`, and then
  - the initial character specified by `gamebase.csv` (`GameBaseData.DefaultCharacter`) if it is `> 0`.
- This uses “CSV number” lookup (engine template lookup by CSV slot), which is distinct from `ADDCHARA 0` (template lookup by character `NO`).
- If a referenced CSV template does not exist, the engine falls back to adding a “pseudo character” (like `ADDVOIDCHARA`).

**Errors & validation**
- Runtime error if executed outside `@SYSTEM_TITLE` (unless executed in a debug-only context where no parent label is attached).

**Examples**
```erabasic
@SYSTEM_TITLE
ADDDEFCHARA
```

**Progress state**
- complete
