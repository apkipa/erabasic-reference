**Summary**
- Toggles bitmap-cache rendering for subsequently created output lines.

**Tags**
- ui
- graphics

**Syntax**
- `BITMAP_CACHE_ENABLE(enable)`

**Signatures / argument rules**
- `BITMAP_CACHE_ENABLE(enable)` → `long`

**Arguments**
- `enable` (int): non-zero enables bitmap-cache mode for future lines; `0` disables it.

**Semantics**
- Sets the console's persistent `bitmapCacheEnabledForNextLine` flag.
- Each future printed line copies that flag when the line object is created.
- Existing already-created lines are not retroactively changed.
- The setting remains in effect for subsequent lines until another call changes it.
- Returns `0`.

**Errors & validation**
- None beyond normal integer-argument evaluation.

**Examples**
- `BITMAP_CACHE_ENABLE(1)`

**Progress state**
- complete
