**Summary**
- Adds an existing sprite to the CBG layer at a given position and depth.

**Tags**
- ui
- graphics
- resources

**Syntax**
- `CBGSETSPRITE(<spriteName>, <x>, <y>, <zDepth>)`

**Signatures / argument rules**
- Signature: `int CBGSETSPRITE(string spriteName, int x, int y, int zDepth)`.

**Arguments**
- `<spriteName>` (required string): sprite name to look up and place on the CBG layer. This argument is required by the call shape; an empty string is still a supplied value, not an omitted argument.
- `<x>`, `<y>` (int): CBG placement coordinates.
- `<zDepth>` (int): CBG depth; must be a 32-bit signed integer and must not be `0`.

**Semantics**
- Looks up `<spriteName>` in the sprite table and, if it exists and is created, adds that sprite to the client-background layer at `(<x>, <y>, zDepth)`.
- If `<spriteName>` is `""`, lookup still runs normally against that supplied empty name; in practice that lookup fails, so the call returns `0`.
- The registered entry holds a **live reference** to that sprite object rather than a copied snapshot.
  - Later mutation/disposal of that same sprite object changes later CBG rendering for this entry.
- Host-mode quirk:
  - unlike `CBGSETG` / `CBGSETBMAPG` / `CBGSETBUTTONSPRITE`, this call does **not** raise a GDI+-only error in `WINAPI` text-drawing mode,
  - but on this host the ordinary CBG paint path is not active in that mode, so the stored entry normally has no visible CBG effect there.
- Layer boundary:
  - this affects only the CBG/background layer,
  - it does not modify the normal output model, pending print buffer, or HTML-island layer.
- Success/failure boundary:
  - if the sprite does not exist or is not created, returns `0` and does not add an entry,
  - otherwise returns `1` after adding the entry.

**Errors & validation**
- Runtime error if `<x>` or `<y>` is outside the 32-bit signed integer range.
- Runtime error if `<zDepth>` is outside the 32-bit signed integer range or equals `0`.

**Examples**
```erabasic
R = CBGSETSPRITE("BG_ICON", 32, 16, 10)
```

**Progress state**
- complete
