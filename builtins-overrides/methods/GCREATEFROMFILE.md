**Summary**
- Creates a graphics surface by loading an image file.

**Tags**
- graphics
- ui
- files

**Syntax**
- `GCREATEFROMFILE(<graphicsId>, <filename>)`
- `GCREATEFROMFILE(<graphicsId>, <filename>, <isRelative>)`

**Signatures / argument rules**
- `int GCREATEFROMFILE(int graphicsId, string filename)`
- `int GCREATEFROMFILE(int graphicsId, string filename, int isRelative)`

**Arguments**
- `<graphicsId>` (int): destination graphics-surface ID.
- `<filename>` (string): image path text.
- `<isRelative>` (optional, int; default `0`): path-base mode for non-rooted paths.
  - `0`: resolve non-rooted paths relative to `ContentDir`.
  - non-zero: use the given non-rooted path text as-is.

**Semantics**
- Loads an image file and creates the graphics surface at `<graphicsId>` from that image.
- Format handling:
  - `.webp` is handled explicitly through the engine's WebP loader.
  - other extensions are delegated to the host bitmap loader.
- Success/failure boundary:
  - if that graphics ID already refers to a created graphics surface, returns `0` and does nothing,
  - if the file does not exist, is not loadable as an image, or exceeds the graphics engine's maximum supported image size, returns `0`,
  - otherwise creates the graphics surface from the loaded image and returns `1`.
- Absolute paths are used directly.
- Layer boundary:
  - this does not itself print anything or modify the normal output model.

**Errors & validation**
- Runtime error if the host is using the `WINAPI` text-drawing mode; this method is GDI+-only.
- Runtime error if `<graphicsId> < 0` or `<graphicsId> > 2147483647`.
- Other load failures are reported by returning `0` rather than by a detailed script-visible error code.

**Examples**
```erabasic
R = GCREATEFROMFILE(GID, "face.png")
R = GCREATEFROMFILE(GID, "mods\face.png", 1)
```

**Progress state**
- complete
