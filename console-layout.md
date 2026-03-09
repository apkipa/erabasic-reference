# Console Layout Primitives and Shared Wrapping Rules

This document specifies the shared **row-formation/layout backend** used after an output frontend has already produced display nodes.

It covers:

- width measurement,
- grouping nodes into button/nonbutton regions,
- converting those regions into display rows,
- automatic wrapping vs no-wrap modes,
- character-level splitting inside dividable text nodes,
- custom-width subdivision used by HTML `<div>` content,
- and line-level alignment.

This backend is shared by both ordinary print-buffer output and HTML output.

This document does **not** redefine:

- output-state layering, temporary lines, history/readback, or redraw timing; those live in [`output-flow.md`](output-flow.md),
- HTML syntax, tags, or attribute validation; those live in [`html-output.md`](html-output.md),
- per-built-in producer quirks such as `PRINTC` cell formatting or `DRAWLINE` pattern expansion; those live in [`builtins-reference.md`](builtins-reference.md).

## 1) Shared layout pipeline

### 1.1 Internal layout objects

The shared backend uses three main object layers:

- **display node** (`AConsoleDisplayNode`):
  - the smallest measured/drawn unit,
  - examples: styled text, inline image, shape, space.
- **button/nonbutton region** (`ConsoleButtonString`):
  - an ordered list of display nodes that share one clickable/non-clickable region boundary,
  - may carry an integer or string input value,
  - is also the unit used by button-generation/input matching.
- **display row** (`ConsoleDisplayLine`):
  - an ordered list of button/nonbutton regions that occupy one retained visible row.

This document is about the transition from display nodes / button regions into display rows.

### 1.2 Frontend entry points

Two different frontends feed this same layout backend:

- **Ordinary output / print buffer**:
  - plain `PRINT*`-style output appends text/nodes into the print buffer,
  - button markup embedded in ordinary output is first split into button/nonbutton regions,
  - flush then turns those regions into one or more display rows.
- **HTML output**:
  - the HTML parser first turns tags/text into display nodes and button regions,
  - it then uses the same row-formation backend to produce display rows.

So HTML and non-HTML output do **not** share the same syntax layer, but they do share the same measurement / row-formation / alignment backend once the frontend has produced display nodes and button regions.

### 1.3 Explicit break sources before row formation

The shared row builder consumes explicit row-break markers, but different frontends create those markers differently:

- ordinary plain output handles a literal LF (`'\n'`) before the shared row builder and flushes the current logical line at that point,
- HTML converts `<br>` and literal LF inside the HTML string into explicit display-row breaks inside the parsed stream.

So the shared backend does **not** own all newline syntax by itself; it consumes already-decided break points from its frontends.

## 2) Width measurement

### 2.1 Text nodes

Styled text nodes use the shared `StringMeasure` helper.

Observable rules:

- measurement uses the node's current font,
- empty strings measure as width `0`,
- text width depends on the host text-drawing mode.

Host text-drawing modes:

- `TEXTRENDERER` mode:
  - uses `TextRenderer.MeasureText(..., NoPadding | NoPrefix)`,
  - width is taken directly from that host result.
- `GRAPHICS` mode:
  - uses `Graphics.MeasureCharacterRanges(...)`,
  - tabs are first expanded to eight spaces,
  - width is then rounded through the engine's `fontDisplaySize` grid rather than using the raw floating-point width directly.

This is the main shared width-measurement primitive used by ordinary text layout, HTML text layout, and helpers such as width-fitted draw-line expansion.

### 2.2 Non-text nodes

Non-text nodes still participate in the same row builder, but they do not all measure like plain text.

Shared rules:

- inline images, spaces, and drawable shapes carry their own width logic,
- percent-based widths are interpreted against the current font size,
- some nodes can extend above or below the normal line box while still consuming horizontal width in the same row.

Fallback rule:

- if an image/shape node cannot be drawn and falls back to literal tag text, that fallback text is still measured under the shared width system before row formation continues.

### 2.3 Dividable vs individable nodes

Each display node declares whether it can be split across rows.

Shared rule:

- ordinary styled text is dividable,
- images, spaces, and shape nodes are not,
- so character-level row splitting only happens inside text nodes.

### 2.4 Subpixel carry and locked starting positions

Width placement keeps a running fractional remainder (`XsubPixel`) across consecutive nodes/regions.

Observable consequences:

- a node's integer pixel width can depend on the subpixel remainder carried in from the previous node,
- the remainder is propagated left-to-right through a row during width setup.

Some frontends can also lock a region's starting X before alignment (notably HTML `pos`-style placement constraints).

Shared rule:

- a locked region keeps its own starting X during the initial left-to-right placement pass,
- when such a lock is encountered, the shared backend resets the carried subpixel remainder at that boundary.

## 3) Row-formation modes

### 3.1 Normal wrapping mode

The ordinary row builder consumes an ordered list of button/nonbutton regions and produces one or more display rows.

Shared width budget:

- default row width is the derived runtime value `DrawableWidth` (see [`config-items.md`](config-items.md)),
- HTML subdivision can override that with a custom row width for `<div>` content.

### 3.2 Single-line mode

The shared backend also exposes a single-line materialization mode.

Observable rule:

- it still measures widths and assigns positions,
- but it does **not** perform automatic wrapping into additional rows,
- so all content is forced into one display row.

This mode is what some host/system/temporary-line producers rely on when they want one retained row rather than ordinary wrapping behavior.

### 3.3 No-wrap HTML mode

HTML `<nobr>` also disables automatic wrapping, but at the HTML frontend layer rather than by using a different syntax family.

Shared consequence:

- once the HTML frontend has enabled `nobr`, the same shared row builder simply stops creating extra wrapped rows for width overflow.

## 4) Automatic wrapping and region splitting

### 4.1 Width setup before wrapping

Before row splitting begins, the backend performs a width/position pre-pass over the region list:

- each region computes its width from its child nodes,
- each region receives an initial left-to-right `PointX`,
- explicit break markers reset the running X position to `0`.

This pre-pass establishes the candidate row positions used by later fit checks.

### 4.2 Basic fit rule

For each region in order:

- if it is an explicit break marker, the current row ends immediately,
- otherwise, if its right edge is within the current row width budget, it stays on the current row,
- otherwise the backend must either:
  - split the region, or
  - move the whole region to the next row.

### 4.3 When a region is split vs moved whole

The shared split policy depends on the current row state and compatibility flags.

Important shared rules:

- if config item `ButtonWrap` is disabled, the backend is willing to split a region when a valid split point exists,
- if the current row is empty, an oversized region is also split when possible,
- if `ButtonWrap` is enabled and the current row already has content, clickable buttons normally move whole to the next row instead of splitting,
- non-button regions still split under that same situation unless compatibility config item `CompatiLinefeedAs1739` suppresses that behavior.

If no valid split point exists:

- the region is moved whole to the next row when possible,
- but if the current row is already empty, the oversized region remains whole and can overflow that row.

So the shared backend is **not** a strict "every visible row always fits inside the width budget" engine. Some rows can overflow when wrapping is disabled or when the first oversized region cannot be split.

### 4.4 Character-level split search

When the backend tries to split a region:

- it walks the region's child nodes until it finds the first width-overflowing dividable text node,
- it then finds the largest prefix of that text node that still fits inside the remaining width budget,
- this search is done by binary search over character count,
- the fitting prefix stays on the current row and the remainder becomes a new region on the following row.

Shared limitation:

- splitting is purely character-count based inside the text node,
- there is no separate word-boundary or hyphenation algorithm.

### 4.5 Repositioning after a row break

Whenever the backend ends a row and continues with remaining regions:

- the remaining regions are re-laid out from X = `0` for the new row,
- fit checking then continues against that new row state.

This is why a region that did not fit at the tail of one row can fit normally once reconsidered at the beginning of the next row.

### 4.6 Logical-row flag vs wrapped continuation rows

The row builder also marks whether a produced display row begins a logical output line.

Shared rules:

- the first produced row from a normal flush is the logical-line start,
- later wrapped rows from the same flush are continuation rows,
- HTML subdivision used for `<div>` content marks its produced rows as continuation rows rather than standalone logical-line starts.

The logical-line consequences of those flags are defined in [`output-flow.md`](output-flow.md); this document only defines how the rows are formed.

## 5) Alignment

### 5.1 Alignment is a second pass

After row formation, each produced display row goes through a line-level alignment pass.

Shared rule:

- alignment shifts the already-built row horizontally as a whole,
- it does **not** rerun width measurement or row splitting.

### 5.2 Width basis for alignment

The alignment pass first computes the row width as:

- the sum of the widths of all button/nonbutton regions in that display row.

The target width used for alignment is:

- the derived runtime value `DrawableWidth` in the normal case,
- or the custom subdivision width for HTML `<div>` content.

### 5.3 Left / center / right behavior

Shared behaviors:

- `CENTER`: move the row so its center matches the center of the target width,
- `RIGHT`: move the row so its right edge matches the target width,
- `LEFT`: keep the row at the ordinary left edge.

Special left-alignment rule:

- the first logical row keeps its existing precomputed X positions,
- wrapped continuation rows are normalized back to X = `0`.

This matters because some frontends can inject locked/relative X positions before the alignment pass.

### 5.4 Interaction with locked positions

Locked positions are honored during the initial left-to-right placement pass.

After that:

- any later line-level alignment shift moves the whole row together,
- so locked positions are not an absolute "ignore alignment forever" mechanism; they are part of the row before the final row shift is applied.

## 6) Visibility and clipping consequences

The shared backend does **not** insert ellipses, shrink-to-fit transformations, or synthetic continuation markers.

Observable consequences:

- if wrapping is disabled, content can extend past the right edge,
- if the first oversized region cannot be split, that row can also extend past the width budget,
- the host draw path then clips output to the visible client area rather than turning that overflow into extra wrapped rows.

So "not wrapped" and "not fully visible" are distinct states:

- the retained row still contains the full logical content,
- but only the visible clipped portion is painted on screen.

## 7) Frontend-specific boundaries

The shared backend stops at the row-formation/alignment layer.

The following remain frontend- or producer-specific topics:

- plain-text syntax that decides when a `PRINT*` call emits LF-driven line ends,
- HTML tag parsing, `<br>`, `<nobr>`, `<div>`, and tag validation,
- `PRINTC`/`PRINTLC` fixed-cell formatting,
- `DRAWLINE`/`GETLINESTR` string expansion before ordinary row formation,
- temporary-line creation and replacement timing,
- readback APIs and logical-line counters.

## 8) Related documents

- [`output-flow.md`](output-flow.md) — output-state layers, temporary lines, redraw, history/readback
- [`html-output.md`](html-output.md) — HTML syntax and HTML-specific switches that feed this backend
- [`builtins-reference.md`](builtins-reference.md) — producer/readback built-ins that rely on this backend
- [`input-flow.md`](input-flow.md) — how button regions produced here are later consumed by waits
