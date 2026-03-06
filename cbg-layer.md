# CBG Layer, Depth, and Hit Testing

`CBG` means **client background**.
Despite that name, it is **not** merely a fixed background that always sits behind normal `PRINT*` output.
It is a separate host/UI graphics layer with its own visual entries, its own button-hit map, and a defined depth relationship to ordinary output.

This document specifies the shared observable contract behind the `CBG*` built-ins.
Per-built-in signatures and argument validation remain in `builtins-reference.md`.

## 1) Scope and state model

The host maintains three distinct pieces of `CBG` state:

- a list of **visual CBG entries**,
- one optional **CBG button-hit map**,
- one current **selected CBG button value** derived from the current mouse position and that hit map.

Visual CBG entries come in two public kinds:

- ordinary CBG images (`CBGSETG`, `CBGSETSPRITE`),
- CBG button sprites (`CBGSETBUTTONSPRITE`).

Each visual entry has at least:

- a placement coordinate `x, y`,
- a nonzero `zDepth`,
- visible image content,
- and, for button sprites, an associated logical `buttonValue` plus optional tooltip text.

The hit map is separate state installed by `CBGSETBMAPG`.
It is **not** automatically derived from the visible CBG images or sprites.

Both the visual-entry list and the hit map store **live references** to underlying sprite/graphics objects rather than copied pixel snapshots.
Observable consequence:

- later mutation of a referenced `G` surface or sprite object changes later CBG rendering/hit-testing,
- removing a CBG entry or hit map breaks that reference,
- but it does **not** dispose the underlying externally managed graphics/sprite resource.

## 2) Coordinate system

`CBG` placement and `CBG` hit-testing use the same client-area coordinate system:

- `x` increases to the right from the client area's left edge,
- `y` increases upward from the client area's bottom edge.

For visual placement, `y` refers to the placed image's **bottom edge** in client coordinates.
So a sprite placed at `y = 0` sits with its bottom edge on the client area's bottom edge.

The CBG button-hit map uses the same logical client coordinates, but samples the underlying bitmap in its own usual top-origin pixel space.
A compatible implementation should therefore convert between the two coordinate conventions when reading the hit-map bitmap.

## 3) Depth model and paint order

### 3.1 Ordinary output occupies depth `0`

Ordinary retained output (`PRINT*`, retained button regions, host-generated normal lines, etc.) behaves as the `depth = 0` layer for CBG composition purposes.

This means `CBG` depth is defined **relative to normal output**, not in a completely separate compositor.

### 3.2 Positive depth goes under normal output

If a CBG entry has `zDepth > 0`, it is drawn **before** ordinary depth-`0` output and therefore appears **under** ordinary text/buttons.

Example:

```erabasic
CBGSETSPRITE("BG", 0, 0, 10)
PRINTFORML "text"
```

The sprite behaves like a background under the printed text.

### 3.3 Negative depth can overdraw normal output

If a CBG entry has `zDepth < 0`, it is drawn **after** ordinary depth-`0` output and therefore can appear **over** ordinary text/buttons.

Example:

```erabasic
PRINTFORML "text"
CBGSETSPRITE("OVERLAY", 0, 0, -10)
```

The sprite can visually cover the printed text.

So the statement “CBG is always below `PRINT*` output” is incorrect.
It depends on the sign of `zDepth`.

### 3.4 `zDepth == 0` is reserved

The public `CBG` setters reject `zDepth == 0`.
Depth `0` is reserved for the ordinary output layer itself.

### 3.5 Equal-depth tie order is not a separate public contract

`CBG` entries are ordered by `zDepth`.
The public contract does not expose a separate user-facing tie-break rule for multiple different entries with the same `zDepth`.

For compatibility-sensitive content, do not rely on a specific overlap order among different entries that share the same depth.

## 4) Hit-testing model

### 4.1 The hit map is independent of visible sprites

`CBGSETBMAPG` installs one graphics surface as the current **CBG button-hit map**.
Mouse-facing CBG selection uses that map, not the visible bounds of `CBGSETBUTTONSPRITE` entries.

Therefore:

- a visible CBG button sprite does not become clickable by itself,
- an opaque hit-map pixel can select a CBG button value even if no visible sprite is present there,
- replacing/removing visual entries does not automatically replace/remove the hit map.

### 4.2 Pixel rule

At a given mouse position, the host samples the hit-map pixel at the corresponding point.

- If the point lies outside the hit-map bitmap, there is no selected CBG button value.
- If the pixel alpha is exactly `255`, the selected CBG button value becomes that pixel's low 24-bit RGB value.
- Otherwise, there is no selected CBG button value.

In other words, transparency in the hit map is binary for selection purposes:

- `A == 255` means “active”,
- every other alpha value means “inactive”.

### 4.3 CBG hit-testing takes pointer-selection precedence

When the current mouse position hits an active CBG-map pixel, the host treats that as the current pointer-side CBG selection **before** it tries to select ordinary output buttons at that point.

Observable consequence:

- an opaque CBG-map pixel at a point suppresses ordinary normal-output button hover selection at that point,
- this precedence is about the pointer-selection path, not about visual paint order.

So a `CBG` entry may be visually under text while the CBG hit map at the same point still captures the pointer-side selection.

This pointer-side CBG selection is also broader than ordinary output-button selection:

- it is updated before the host applies the usual ordinary-button wait-state/generation gating,
- it can therefore remain active even when ordinary output buttons are not currently selectable,
- and it clears the host's current ordinary button-hover/selection state at that point.

### 4.4 Selection is by value, not object identity

The selected CBG state is a single integer button value, not a pointer to one unique sprite object.
If several CBG button sprites share the same `buttonValue`, they all observe the same selected/not-selected state.

For click reporting, `INPUTMOUSEKEY` samples the hit-map pixel directly at the click point.
So its `RESULT:4` channel does **not** depend on some prior hover update having already populated the current selected CBG value.

## 5) CBG button sprites and tooltip behavior

`CBGSETBUTTONSPRITE` adds visual entries associated with a logical `buttonValue`.
When the currently selected CBG value matches that `buttonValue`, those entries can switch from their normal sprite to their hover/selected sprite.

Observable rules:

- multiple button sprites may share one `buttonValue`,
- when that value is selected, all matching entries use their selected sprite path,
- this selection is driven by the hit map's sampled value, not by per-sprite rectangle testing,
- if a matching entry has no created hover sprite, that entry simply draws nothing while selected.

Tooltip handling is narrower than selection handling:

- the host can surface tooltip text from a matching selected CBG button sprite,
- but the standard tooltip path only does this for selected values greater than `0`.

So `buttonValue = 0` still participates in CBG selection and hover-sprite switching, but does **not** surface tooltip text through that standard host path.

If multiple matching selected entries carry tooltip text, the standard host tooltip path takes the **first** matching entry encountered in current CBG list order.
This effectively prefers higher `zDepth` entries first; same-depth tie order should still be treated as non-portable.
The host also replaces literal `<br>` substrings in that tooltip text with actual line breaks before showing it.

## 6) Clearing and removal boundaries

The `CBG` API surface intentionally separates visual-entry removal from hit-map removal.

- `CBGCLEAR()` removes all visual CBG entries and also clears the current hit map.
- `CBGCLEARBUTTON()` removes only CBG button sprites, then also clears the current hit map.
- `CBGREMOVERANGE(zMin, zMax)` removes only visual CBG entries whose `zDepth` lies in that inclusive range; it does **not** clear the hit map.
- `CBGREMOVEBMAP()` clears only the hit map and current CBG selection state; it does **not** remove visible CBG entries.

This separation is observable.
For example, button sprites can remain visible after `CBGREMOVEBMAP()`, but they will no longer participate in CBG hit-testing until a new hit map is installed.

## 7) Relationship to ordinary output and input

### 7.1 `CBG` is not part of the normal output model

`CBG` is not stored in the normal output buffer/history model documented in `output-flow.md`.
It is separate host/UI state.

Therefore:

- `GETDISPLAYLINE`, `HTML_GETPRINTEDSTR`, `HTML_POPPRINTINGSTR`, `LINECOUNT`, and `CLEARLINE` do not read/write CBG state,
- `CBG` does not become part of retained normal logical lines,
- `CBG` is also separate from the HTML-island layer.

Host-mode quirk:

- on this host, ordinary CBG painting is performed only on the non-`WINAPI` text-drawing path,
- so methods that do not themselves reject `WINAPI` can still mutate stored CBG state there without producing normal visible CBG painting.

### 7.2 `CBG` buttons are not ordinary output buttons

Ordinary output buttons are created by output content such as `PRINTBUTTON*` and participate in the value-submission path described in `input-flow.md`.
CBG buttons do **not** use that model.

Compatibility boundary:

- clicking a normal-output button can satisfy ordinary `INPUT` / `INPUTS` / `INPUTANY` / `BINPUT*` waits,
- a CBG hit-map selection does not by itself create such a normal-output button submission,
- `MOUSEB()` reports the currently pointed **ordinary output button** only; it does not return CBG button-map values.

### 7.3 `INPUTMOUSEKEY` reports separate channels

`INPUTMOUSEKEY` exposes CBG-map and normal-output-button information through different result channels.

- `RESULT:4` carries the current CBG hit-map value (or `-1` when no active CBG-map pixel exists at the click point).
- `RESULT:5` / `RESULTS` describe the currently selected ordinary output button, if any.

These channels should not be merged into one abstract “mouse button target”.
They represent different host-side subsystems.

## 8) Reimplementation checklist

A compatible implementation should preserve all of the following:

- `CBG` means a separate host/UI graphics layer, not ordinary output history.
- `zDepth > 0` places CBG under ordinary output; `zDepth < 0` can place it over ordinary output.
- `zDepth == 0` is rejected by the public CBG setters.
- CBG placement uses left-origin `x` and bottom-origin `y` client coordinates.
- One optional hit map drives CBG selection independently of visible sprite rectangles.
- Only hit-map pixels with alpha exactly `255` are active.
- The selected CBG state is a value, so multiple button sprites can share one selected state.
- Pointer-side CBG hit selection takes precedence over ordinary output-button hover selection at the same point.
- Removing visual CBG entries and removing the hit map are separate operations.
- `CBG` remains outside normal output readback/history APIs even when it visually overlaps ordinary text.

## 9) Related documents

- [`output-flow.md`](output-flow.md) — ordinary output state, retained lines, readback helpers, button generations
- [`input-flow.md`](input-flow.md) — ordinary wait completion paths and the distinction from CBG hit-map selection
- [`resources-and-sprites.md`](resources-and-sprites.md) — sprite loading/name resolution used by `CBGSETSPRITE` / `CBGSETBUTTONSPRITE`
- [`builtins-reference.md`](builtins-reference.md) — per-built-in signatures and validation rules
