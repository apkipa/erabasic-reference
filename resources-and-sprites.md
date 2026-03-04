# Resources and Sprites (`resources/`) (Emuera EvilMask)

This engine loads image resources from `ExeDir/resources/` into a **sprite dictionary** that is used by:

- HTML output (`<img src='...'>`, `<img srcb='...'>`, `<img srcm='...'>`)
- `PRINT_IMG`
- sprite-related built-ins such as `SPRITEGETCOLOR`, `SPRITEWIDTH/HEIGHT`, `CBGSETSPRITE`, etc.

This document specifies the **observable contracts** needed to reimplement sprite name resolution and the `resources/**/*.csv` loader.

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
  - `normalizedName = name.ToUpper()` (culture-dependent).

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

After a successful `ANIME` declaration, subsequent lines with the same `name` can add frames (see below) until another sprite declaration resets the “current animation sprite”.

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
- Otherwise, the engine uppercases the name and performs a dictionary lookup.
- Lookup is effectively case-insensitive for typical ASCII names.

If lookup fails, HTML `<img ...>` falls back to displaying the tag as literal text (see `html-output.md`).

