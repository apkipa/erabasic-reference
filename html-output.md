# HTML Output and HTML Strings (Emuera EvilMask)

This engine supports an **HTML-like mini language** for UI output and measurement. It is used by:

- `HTML_PRINT`, `HTML_PRINT_ISLAND`
- `HTML_TAGSPLIT`
- HTML helper functions such as `HTML_ESCAPE`, `HTML_TOPLAINTEXT`, `HTML_STRINGLEN`, `HTML_SUBSTRING`, `HTML_STRINGLINES`
- “HTML export” helpers such as `HTML_GETPRINTEDSTR` / `HTML_POPPRINTINGSTR`

This is **not** a web browser HTML implementation. Only the tags and behaviors described here are supported.

## 1) What is an “HTML string” in this engine?

An HTML string is a normal EraBasic string whose content is interpreted as:

- plain text, plus
- tags of the form `<tagName ...>` / `</tagName>`, plus
- comments `<!-- ... -->`, plus
- character references such as `&amp;` and `&#x41;`.

Tag names and attribute names are **case-insensitive**.

Plain text segments are rendered after expanding character references (e.g. `&amp;` becomes `&`).

## 2) Character references (escaping / unescaping)

### 2.1 Supported references

These character references are recognized:

- `&amp;` → `&`
- `&gt;` → `>`
- `&lt;` → `<`
- `&quot;` → `"`
- `&apos;` → `'`
- `&nbsp;` → space (`' '`)
- `&#nn;` → Unicode code point `nn` in base 10
- `&#xnn;` → Unicode code point `nn` in base 16

Numeric code points must satisfy `0 <= codePoint <= 0xFFFF`. Values outside that range are errors.

### 2.2 `HTML_ESCAPE` contract

`HTML_ESCAPE(text)` escapes the five characters:

- `&` → `&amp;`
- `>` → `&gt;`
- `<` → `&lt;`
- `"` → `&quot;`
- `'` → `&apos;`

No other characters are changed.

## 3) Comments

HTML comments have the form:

`<!-- comment -->`

In `HTML_PRINT` rendering, comments are ignored (they produce no output).

If a `<!--` start marker appears but a matching `-->` is not found, it is a runtime error.

## 4) Tag syntax and attribute syntax

### 4.1 Tag syntax

- Start tag: `<tagName ...>`
- End tag: `</tagName>`

Self-closing syntax (`<tag />`) is not used by this engine; use `<br>` for line breaks.

### 4.2 Attribute syntax

Attributes are written as assignments inside the tag:

`name='value'` or `name="value"`

Attribute values must be quoted (either quote style is accepted).

For most tags, attribute values are **unescaped** (character references are expanded) before they are interpreted (e.g. `title='A&amp;B'` means the tooltip text is `A&B`).

Exception:

- `<clearbutton notooltip='...'>` interprets `true|false` directly and does not expand character references in that value.

### 4.3 Errors

HTML parsing is strict:

- Unsupported tags are runtime errors.
- Unsupported attributes or invalid attribute values are runtime errors.
  - Some tags additionally define fallback behaviors (for example, `<img>` / `<shape>` can render as literal text when the referenced resource/shape is not drawable).
- Unclosed tags at end of string are runtime errors, except that `</p>`, `</nobr>`, and `</clearbutton>` may be omitted.
- Malformed character references are runtime errors.

## 5) Rendering model: logical lines, display lines, wrapping

### 5.1 Logical line vs display lines

One call to `HTML_PRINT` (without buffering) produces **one logical output line**.

Within that logical line, the engine may produce multiple **display lines** due to:

- explicit line breaks (`<br>` or literal `'\n'` in the HTML string), and/or
- automatic wrapping when content exceeds the drawable width.

Commands such as `CLEARLINE` and the `LINECOUNT` variable count/delete **logical lines**, not individual display lines.

### 5.2 `<br>` and newline characters

- `<br>` inserts an explicit display line break.
- A literal newline character `'\n'` inside an HTML string is treated the same as `<br>`.

### 5.3 `<nobr>` (no automatic wrapping)

`<nobr> ... </nobr>` disables automatic wrapping:

- the content is still allowed to contain explicit breaks (`<br>` / `'\n'`),
- but it is not wrapped just because it exceeds the drawable width.

Because the console does not scroll horizontally, any content that would extend past the right edge is not visible.

`<nobr>` must appear before any text in the HTML string. If `<p ...>` is also used, the order must be `<p ...><nobr> ...`.

`</nobr>` must appear at the end (after the last text). The closing tag may be omitted.

## 6) Supported tags (and their contracts)

### 6.1 Paragraph alignment: `<p align='...'>`

`<p align='left|center|right'> ... </p>`

- `align` is required and must be one of `left`, `center`, `right` (case-insensitive).
- No other `<p>` attributes are supported.
- `<p ...>` must appear at the beginning of the HTML string (before any text).
- If `<nobr>` is also used, the order must be `<p ...><nobr> ...`.
- `</p>` must appear at the end (after the last text); it may be omitted.

### 6.2 Line break: `<br>`

Inserts a display line break. `<br>` has no attributes.

### 6.3 Text style tags: `<b>`, `<i>`, `<u>`, `<s>`

These tags toggle styling for enclosed text:

- `<b>` bold
- `<i>` italic
- `<u>` underline
- `<s>` strikeout

They have no attributes.

Tag matching rules:

- Each style is tracked independently (it is **not** a strict nesting stack).
  - Example: `<b><i>X</b>Y</i>` is accepted.
- Opening a style that is already active is a runtime error (e.g. `<b><b>...`).
- Closing a style that is not currently active is a runtime error (e.g. `</u>` when underline is not active).
- All active styles must be closed by the end of the HTML string (otherwise it is a runtime error).

### 6.4 Font/color: `<font face='...' color='...' bcolor='...'>`

`<font ...> ... </font>` changes style for the enclosed region.

`<font>` requires at least one attribute.

Supported attributes:

- `face`: font family name.
- `color`: text color.
- `bcolor`: selection highlight color used for buttons.

`<font>` tags can be nested. When nested:

- Any attribute omitted in an inner `<font>` inherits the value from the nearest surrounding `<font>`.

Color formats:

- Hex form: `#RRGGBB` only (hex without the leading `#` is not accepted).
- Named colors: names recognized by the runtime’s color-name table (case-insensitive).
  - `Transparent` is rejected as a color name.

### 6.5 Buttons: `<button>` and `<nonbutton>`

`<button ...> ... </button>` marks the enclosed region as a (potentially clickable) button.

`<nonbutton ...> ... </nonbutton>` marks the enclosed region as non-clickable button-like text.

Buttons cannot be nested.

Supported attributes:

- `value` (button-only):
  - If present, the region becomes clickable and the button “input value” is the given string.
  - If omitted, the region is rendered as non-clickable (like `nonbutton`).
  - For `<nonbutton>`, specifying `value` is a runtime error.
- `title`:
  - Tooltip text shown when hovering the region.
- `pos`:
  - A horizontal position lock (integer), interpreted as a percentage of font size.
    - `posPx = pos * FontSize / 100`
  - It is permitted only when the overall layout uses `<nobr>` and alignment is `left`.

Button value interpretation:

- The `value` attribute is always a string in the HTML syntax.
- If it can be parsed as a signed 64-bit integer, the engine also treats it as an “integer button value” for input purposes (both forms are retained).

### 6.6 Disable buttonization region: `<clearbutton>`

`<clearbutton> ... </clearbutton>` disables clickability for enclosed button regions:

- If a `<button ...>` would normally be clickable, it becomes non-clickable in a `clearbutton` region.
- `title` and `pos` behavior remains available unless disabled by `notooltip`.

Supported attribute:

- `notooltip='true|false'` (default `false`)
  - When `true`, tooltip titles are suppressed inside the region.

`<clearbutton>` cannot be nested.

`</clearbutton>` may be omitted (in which case the effect applies until the end of the current HTML string / `<div>` content).

### 6.7 Inline images: `<img ...>`

`<img src='...' ...>`

Supported attributes:

- `src` (required): sprite name for the image (see `resources-and-sprites.md`).
- `srcb` (optional): sprite name shown when the region is selected/focused.
- `srcm` (optional): mapping-sprite name used by mouse-input “mapping color” side channels (see `INPUT`).
- `height` (optional): size in percent of font size, or pixels with `px` suffix.
  - If omitted or `0`, it defaults to the current font size in pixels.
  - Negative values flip vertically.
- `width` (optional): size in percent of font size, or pixels with `px` suffix.
  - If omitted or `0`, the original aspect ratio is preserved.
  - Negative values flip horizontally.
- `ypos` (optional): vertical offset in percent of font size, or pixels with `px` suffix.

If the image resource cannot be resolved, the tag is rendered as literal text (the string form of the `<img ...>` tag).

### 6.8 Shapes: `<shape ...>`

`<shape type='...' param='...' ...>`

Supported attributes:

- `type` (required): shape type name (case-insensitive).
  - Supported drawable types: `rect`, `space`.
  - Other values are accepted syntactically but result in a non-drawable shape (rendered as literal text).
- `param` (required): comma-separated integers (each may use `px` suffix).
  - Without `px`, each value is interpreted as a percentage of font size (in pixels).
  - For `type='rect'`:
    - 1 value: rectangle width (must be `> 0`).
    - 4 values: `x,y,width,height` (must satisfy `x >= 0`, `width > 0`, `height > 0`; `y` may be negative).
  - For `type='space'`: 1 value: space width (any integer).
- `color` (optional): shape color (same formats as `<font color=...>`).
- `bcolor` (optional): selected/focused color (same formats as `<font color=...>`).

If the shape is not drawable (unsupported `type` or invalid `param` shape), the tag is rendered as literal text (the string form of the `<shape ...>` tag).

### 6.9 Sub-areas: `<div ...>`

`<div ...> ... </div>` renders its enclosed HTML content into a rectangular sub-area.

Key properties:

- `<div>` cannot be nested.
- `</div>` is required.
- A `<div>` does **not** participate in inline flow width:
  - It does not “consume” horizontal space in the surrounding line.
  - It can overlap other content.
- Rendering limitations:
  - `<div>` is only rendered by the engine’s graphics drawing path. In WinAPI text drawing mode, `<div>` content is not drawn.
  - `<div>` is not rendered in the HTML island layer (even though it is still parsed/validated).
- Visibility note:
  - A `<div>` is rendered as an overlay element and is only drawn when it extends outside the normal line box (i.e. its vertical bounds exceed the standard line height). A `<div>` fully contained within the line box should be treated as non-drawn for compatibility.
- The `<div>` start tag must appear when there are no active style/font/button tags:
  - You must not have an unclosed `<font>`, `<button>/<nonbutton>`, or `<b>/<i>/<u>/<s>` at the point where `<div>` starts.
  - `<p>`, `<nobr>`, and `<clearbutton>` may still be active.

#### 6.9.1 Required attributes

- `width`: required.
- `height`: required.

Each is a signed integer, either:

- `Npx` = pixels, or
- `N` = percentage of font size (in pixels).

Negative `width` / `height` values are accepted, but are treated as their absolute values.

#### 6.9.2 Positioning attributes

- `xpos` (optional): x-offset of the sub-area.
- `ypos` (optional): y-offset of the sub-area.

Each uses the same numeric format as `width`/`height` (percent of font size, or `px`).

Shorthands:

- `size='width,height'` sets `width` and `height`.
- `rect='xpos,ypos,width,height'` sets `xpos`, `ypos`, `width`, and `height`.

Whitespace around comma-separated tokens is ignored.

#### 6.9.3 Depth (z-order)

- `depth` (optional): signed integer (default `0`).
- Rendering order is based on `depth`:
  - Higher `depth` is drawn earlier (behind).
  - Lower `depth` is drawn later (in front).
  - Regular inline content is treated as depth `0`.

#### 6.9.4 Background color

- `color` (optional): background color of the sub-area.
  - Same color formats as `<font color=...>`.

#### 6.9.5 Display mode

- `display` (optional): `relative` (default) or `absolute`.
  - `relative`: position is relative to the current output line’s origin and scrolls with the log.
  - `absolute`: position is relative to the window and does not scroll.
    - The origin is the bottom-left of the window.
    - Positive `ypos` moves upward.

#### 6.9.6 Box model: margin / padding / border / radius / bcolor

These attributes are all optional:

- `margin`
- `padding`
- `border` (border thickness)
- `radius` (outer-corner radius)

Each takes 1, 2, 3, or 4 comma-separated numbers, where each number uses the same numeric format as `width`/`height` (`N` percent-of-font-size, or `Npx`):

- 1 value: `all`
- 2 values: `topBottom, leftRight`
- 3 values: `top, leftRight, bottom`
- 4 values: `top, right, bottom, left`

`bcolor` (optional) specifies border colors. It takes 1, 2, 3, or 4 comma-separated color values in the same positional mapping as above, and each color uses the same format as `<font color=...>`.

If `border` is specified but `bcolor` is omitted, the border color defaults to the engine’s default text color.

#### 6.9.7 Layout of `<div>` contents

The enclosed HTML is laid out using the same HTML-string rules as `HTML_PRINT`, with a custom drawable width derived from the `<div>`’s `width`:

- The base width is `width` (converted to pixels).
- If any of `margin`, `border`, or `padding` is present, the left+right values are subtracted from the base width to get the content drawable width.

This content drawable width affects wrapping and alignment inside the `<div>`.

#### 6.9.8 Examples

```erabasic
; A small overlay box near the current position
HTML_PRINT "<div rect='-180px,-5px,80px,80px' color='#503030' depth='-1'><button value='3'>[3]</button></div>"
```

```erabasic
; A rounded panel with border (note: for <div>, `bcolor` means border color)
HTML_PRINT "<div rect='0,0,300px,80px' color='#202020' border='2px' bcolor='#808080' radius='8px' padding='8px'><font color='white'>Status</font></div>"
```

## 7) Related built-ins (high-level interaction)

For the built-in signatures and exact scripting contracts, see the individual built-in entries:

- `HTML_PRINT`, `HTML_PRINT_ISLAND`, `HTML_PRINT_ISLAND_CLEAR`
- `HTML_TAGSPLIT`
- `HTML_GETPRINTEDSTR`, `HTML_POPPRINTINGSTR`
- `HTML_ESCAPE`, `HTML_TOPLAINTEXT`
- `HTML_STRINGLEN`, `HTML_SUBSTRING`, `HTML_STRINGLINES`
