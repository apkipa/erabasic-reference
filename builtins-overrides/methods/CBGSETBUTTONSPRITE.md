**Summary**
- Adds one CBG button sprite entry, optionally with a hover/selected sprite and tooltip text.

**Tags**
- ui
- graphics

**Syntax**
- `CBGSETBUTTONSPRITE(<buttonValue>, <normalSprite>, <hoverSprite>, <x>, <y>, <zDepth>)`
- `CBGSETBUTTONSPRITE(<buttonValue>, <normalSprite>, <hoverSprite>, <x>, <y>, <zDepth>, <tooltip>)`

**Signatures / argument rules**
- Signature: `int CBGSETBUTTONSPRITE(int buttonValue, string normalSprite, string hoverSprite, int x, int y, int zDepth, string tooltip = omitted)`.

**Arguments**
- `<buttonValue>` (int): logical CBG button value associated with this sprite.
- `<normalSprite>` (string): sprite name used in the normal state. This call shape does not allow omission; an empty string is still a supplied value.
- `<hoverSprite>` (string): sprite name used while this button value is currently selected by the CBG hit map. This call shape does not allow omission; an empty string is still a supplied value.
- `<x>`, `<y>` (int): CBG placement coordinates.
- `<zDepth>` (int): CBG depth; must be a 32-bit signed integer and must not be `0`.
- `<tooltip>` (optional, string): tooltip text associated with this button sprite.

**Semantics**
- Adds one CBG button sprite entry to the client-background layer.
- The entry is associated with `<buttonValue>`.
- The registered entry holds **live references** to the normal/hover sprite objects rather than copied snapshots.
  - Later mutation/disposal of those same sprite objects changes later CBG rendering for this entry.
- When the current CBG hit map selects that same button value, the runtime draws the hover/selected sprite in place of the normal sprite for this entry.
- If multiple CBG button sprites share the same `<buttonValue>`, they all participate by value rather than by unique object identity.
- Tooltip boundary:
  - the optional tooltip text is stored on the CBG button sprite entry,
  - when this button value is the currently selected CBG value, that tooltip can be surfaced by the host UI,
  - but the standard host tooltip path only does so for selected values greater than `0`, so `buttonValue = 0` still participates in selection/hover-sprite switching without surfacing tooltip text through that standard path.
- Sprite-existence boundary:
  - missing/uncreated sprite names do **not** make the call fail by themselves,
  - the entry is still registered,
  - but an uncreated/missing sprite simply does not draw,
  - an explicit empty string behaves the same way as any other failing lookup here,
  - so if the hover sprite is missing/uncreated, the entry can become invisible while selected.
- Layer boundary:
  - this affects only the CBG/background-button layer,
  - it does not modify the normal output model, pending print buffer, or HTML-island layer.
- Return value:
  - returns `0` if `<buttonValue>` is outside `0 .. 0xFFFFFF`,
  - otherwise returns `1` after registering the entry.

**Errors & validation**
- Runtime error if the host is using the `WINAPI` text-drawing mode; this method is GDI+-only.
- Runtime error if `<x>` or `<y>` is outside the 32-bit signed integer range.
- Runtime error if `<zDepth>` is outside the 32-bit signed integer range or equals `0`.

**Examples**
```erabasic
R = CBGSETBUTTONSPRITE(0x0000FF, "BTN_N", "BTN_H", 100, 40, 10)
R = CBGSETBUTTONSPRITE(0x0000FF, "BTN_N", "BTN_H", 100, 40, 10, "Open")
```

**Progress state**
- complete
