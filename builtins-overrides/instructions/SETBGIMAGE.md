**Summary**
- Adds a sprite-backed background image layer to the console.

**Tags**
- ui
- resources

**Syntax**
- `SETBGIMAGE <spriteName> [, <depth> [, <opacityByte> ]]`

**Arguments**
- `<spriteName>` (FORM/formatted string): its evaluated result names a sprite.
  - Sprite lookup is case-insensitive (the engine uppercases before lookup).
  - Only file-backed sprites loaded from `resources/**/*.csv` are accepted; other sprite kinds are ignored.
- `<depth>` (optional, FORM/formatted string; default `0`): its evaluated result is parsed by `Int64.Parse`.
- `<opacityByte>` (optional, FORM/formatted string; default `255`): its evaluated result is parsed by `Int64.Parse`, then converted to opacity as `value / 255.0`.
  - Not clamped.

**Semantics**
- Resolves `<spriteName>` to a sprite:
  - If the sprite does not exist or is not a file-backed sprite, the instruction is a no-op.
  - Otherwise, it appends a new background entry `(depth, sprite, opacity)` to the background list.
- The background list is sorted by `depth` descending (larger depth first).
- The engine bakes a composite background image from the list:
  - Each sprite is scaled to **cover** the client area while preserving aspect ratio.
  - If horizontal padding is needed, it is centered; vertical alignment is top-aligned (extra height is cropped at the bottom).
  - Each layer is alpha-multiplied by `opacity`.
- Does not print output.

**Errors & validation**
- Runtime error if `<depth>` or `<opacityByte>` cannot be parsed by `Int64.Parse`.

**Examples**
- `SETBGIMAGE TITLE_BG`
- `SETBGIMAGE TITLE_BG, 10, 128`  ; 50% opacity

**Progress state**
- complete
