# Resources, Sprites, and Media Files (`resources/`, `sound/`) (Emuera EvilMask)

This engine loads image resources from `ExeDir/resources/` into a **sprite dictionary** that is used by:

- HTML output (`<img src='...'>`, `<img srcb='...'>`, `<img srcm='...'>`)
- `PRINT_IMG`
- sprite-related built-ins such as `SPRITEGETCOLOR`, `SPRITEWIDTH/HEIGHT`, `CBGSETSPRITE`, etc.

This document specifies the **observable contracts** needed to reimplement:

- sprite name resolution and the `resources/**/*.csv` loader,
- direct image loading used by `GCREATEFROMFILE`,
- and direct audio path resolution used by `PLAYSOUND`, `PLAYBGM`, and `EXISTSOUND`.

## 1) Load point and directory enumeration

During startup initialization, the engine loads resources before running scripts.

- Root directory: `ExeDir/resources/`
- CSV files enumerated: every `*.csv` file under `resources/` recursively.

## 2) CSV parsing model (no quoting)

Each `resources/**/*.csv` file is read as text using encoding auto-detection.

Each line is processed as follows:

- Trim leading/trailing whitespace.
- If the trimmed line is empty, ignore it.
- If the trimmed line starts with `;`, ignore it (comment).
- Split by literal comma `,` into tokens.
  - There is no CSV quoting/escaping.
  - Whitespace around tokens is ignored by per-field trimming where stated below.

## 3) Sprite name normalization and duplicate handling

Sprite name is taken from `tokens[0]`:

- `name = tokens[0].Trim()`.
- If `name` is empty, the line is ignored.
- The name is normalized to uppercase before lookup/insertion:
  - `normalizedName = name.ToUpper()` using the current culture (that is, not an invariant/ordinal ASCII-only fold).

If a sprite with the same normalized name already exists:

- The engine emits a warning.
- The new sprite definition is ignored (the earlier one remains in effect).

## 4) Sprite declaration lines

A non-comment line must have at least 2 tokens:

`name, arg2, ...`

If fewer than 2 tokens are present, the line is ignored.

### 4.1 Animation sprite declaration (`ANIME`)

If `arg2` equals `ANIME` (case-insensitive), the line declares an animation sprite:

`name, ANIME, width, height`

- `width` and `height` are required (must have at least 4 tokens total).
- Each must be a base-10 integer.
- Each must satisfy `1 <= value <= 8192`.

If any requirement is not met, the engine emits a warning and ignores the line.

After a successful `ANIME` declaration, subsequent lines with the same `name` can add frames under the frame-line rules in this section until another sprite declaration resets the “current animation sprite”.

### 4.2 Static sprite declaration (from an image file)

If `arg2` is not `ANIME`, it is interpreted as an image filename.

Validation:

- `arg2` must contain a dot `.` somewhere (an “extension-like” check).
  - If it does not, the engine emits a warning and ignores the line.

Path resolution:

- The image file path is resolved relative to the directory containing the CSV file:
  - `imagePath = <csvDirectory> + arg2`

Image load failure:

- If the image cannot be loaded, the engine emits a warning and ignores the line.

Large images:

- Images larger than `8192` in either dimension are allowed, but produce a warning.

Parameters:

`name, file, x, y, width, height, offsetX, offsetY, delayMs, destWidth, destHeight`

All parameters after `file` are optional.

- `x,y,width,height` (optional, 4 ints)
  - If all 4 parse successfully, they define a source rectangle inside the image.
  - `width` and `height` must be positive.
  - The rectangle must intersect the source image bounds (partial overlap is accepted).
- `offsetX,offsetY` (optional, 2 ints)
  - If both parse successfully, they define an offset for the sprite.
- `delayMs` (optional, 1 int)
  - If present and parseable, must be `> 0`.
- `destWidth,destHeight` (optional, 2 ints)
  - If both parse successfully, they define the sprite’s destination/base size.

Interpretation:

- If there is an active “current animation sprite” and `name` matches that animation sprite’s name:
  - The line is treated as an **animation frame addition** instead of a new sprite declaration.
  - On success, it modifies the animation sprite and does not create a new sprite name.
- Otherwise:
  - The line declares a new static sprite under `name`.

## 5) Sprite name lookup contract (used by HTML `<img>`)

Sprite lookup by name (e.g. `<img src='NAME'>`) behaves as:

- If the input name is null, lookup fails.
- Otherwise, the engine uppercases the name with the same current-culture `ToUpper()` rule and performs a dictionary lookup.
- Therefore ASCII names behave case-insensitively under this mapping, while non-ASCII names follow the current culture’s uppercase mapping.

If lookup fails, HTML `<img ...>` falls back to displaying the tag as literal text (see `html-output.md`).

## 6) Directory roots used by direct file-based image/audio built-ins

These built-ins do **not** all use the same path-base rule as sprite lookup.

- Sprite lookup (`<img src='...'>`, `PRINT_IMG`, sprite built-ins) uses the already-loaded sprite dictionary from `resources/**/*.csv`.
  - It does **not** resolve a filename at call time.
- `GCREATEFROMFILE` loads an image file directly.
  - If the path is rooted/absolute, it is used as-is.
  - If the path is non-rooted and `isRelative == 0`, the engine prepends `ExeDir/resources/`.
  - If the path is non-rooted and `isRelative != 0`, the engine uses the given path text as-is.
- `PLAYSOUND` and `PLAYBGM` load audio files directly.
  - They resolve the path as `Path.GetFullPath(ExeDir/sound/ + filename)`.
  - Missing files are ignored (no-op).
- `EXISTSOUND` is similar in purpose but **not** identical in path handling.
  - It resolves the path as `Path.GetFullPath("./sound/" + mediaFile)` under the current working directory.
  - It does not use the runtime's `Program.SoundDir` field.
  - It does not apply the safe relative-path normalization used by `EXISTFILE`.

Compatibility consequence:

- `PLAYSOUND` / `PLAYBGM` and `EXISTSOUND` usually point at the same `sound/` tree in ordinary launches, but they are not implemented through the same helper and should not be treated as byte-for-byte identical path-resolution APIs.

## 7) Supported image and audio format contract

### 7.1 Images

The common image-loading surface used by sprite CSV entries and `GCREATEFROMFILE` is:

- explicit `.webp` handling through the bundled native WebP loader,
- otherwise the host bitmap loader (`System.Drawing.Bitmap`) for other image extensions.

Observable contract:

- `.webp` is intentionally supported by this engine build.
- Other image formats follow whatever the host bitmap loader accepts.
- If `.webp` support is unavailable at runtime (for example native library load failure) or decoding fails, the load fails the same way as any other invalid image.

### 7.2 Audio

The common audio-loading surface used by `PLAYSOUND` and `PLAYBGM` is:

- direct `.wav` loading,
- direct `.ogg` loading,
- delegation of all other extensions to the host media backend.

Compatibility reading rule:

- `.wav` and `.ogg` are the stable audio formats this reference treats as portable script-visible compatibility surface.
- Other extensions may still work on some hosts, but that behavior is backend-dependent and is **not** promised as a stable cross-host contract here.

## 8) Shared failure model for common resource built-ins

- Sprite CSV image entries:
  - missing/unloadable images produce a warning and the sprite definition is ignored.
  - oversized images (`> 8192` in either dimension) are accepted with a warning.
- `GCREATEFROMFILE`:
  - returns `0` if the target graphics ID already exists, the file is missing, decoding fails, or the decoded image exceeds the graphics size limit.
  - raises a runtime error only for the GDI+-only / invalid-ID argument boundaries described in its built-in entry.
- `PLAYSOUND` / `PLAYBGM`:
  - missing files are ignored.
  - if the file exists but the audio backend cannot open/decode/play it, execution raises a runtime error.
- `EXISTSOUND`:
  - returns `1` only when the resolved path exists as a file.
  - otherwise returns `0`; it does not report richer failure detail.
