# Output Flow and Visible-Line Semantics

This document specifies the shared **host-side output contract** used by normal `PRINT*` output, HTML output, button presentation, output skipping, redraw scheduling, and output readback helpers.

It is written as a shared contract for the `PRINT*` family, `HTML_PRINT*`, `PRINTBUTTON*`, `REUSELASTLINE`, `CLEARLINE`, `SKIPDISP`, `REDRAW`, `CURRENTREDRAW`, `GETDISPLAYLINE`, `HTML_GETPRINTEDSTR`, and `HTML_POPPRINTINGSTR` families.

## 1) Scope and non-goals

This topic defines the **observable output-state model**:

- what lives in the pending print buffer,
- what becomes part of the current normal-output **display-line array**,
- how visible display lines are grouped into **logical output lines**,
- how temporary lines differ from ordinary normal lines,
- how button regions exist as output objects before later input consumes them,
- how the separate HTML-island layer accumulates and is cleared,
- which output-readback APIs read which layer,
- how host-generated system/warning/error lines join the same normal output model,
- and how redraw scheduling affects paint timing without redefining output state.

This topic does **not** redefine:

- HTML tag grammar or attribute validity rules; those live in [`html-output.md`](html-output.md),
- wait-state lifecycle or input acceptance rules; those live in [`input-flow.md`](input-flow.md),
- per-built-in argument syntax beyond the shared model documented here; detailed signatures still live in [`builtins-reference.md`](builtins-reference.md).

This topic deliberately covers only the **normal output** and **HTML-island** models. The separate `CBG` graphics/hit-map layer is specified in [`cbg-layer.md`](cbg-layer.md). Even when `CBG` visually appears above or below ordinary text, it is not part of the retained output history described here.

`GETLINESTR` is **not** part of this model. It is a `DRAWLINE` helper that expands a pattern string to the current drawable width; see its own built-in entry.

## 2) Output state layers

The observable output model has six relevant layers/states.

### 2.1 Pending print buffer

The **pending print buffer** is the current not-yet-materialized normal output being assembled by buffered output instructions.

Shared properties:

- Appending to the pending print buffer does **not** immediately create an entry in the normal display-line array.
- Multiple buffered output instructions can contribute segments to the same future logical line.
- The pending print buffer may contain plain text, HTML-derived styled segments, images/shapes, and button/nonbutton regions.
- `HTML_POPPRINTINGSTR()` reads and clears this layer directly.
- `GETDISPLAYLINE` and `HTML_GETPRINTEDSTR` do **not** read this layer.

### 2.2 Normal display-line array

The normal output area stores an ordered array of **display lines**.

Shared properties:

- Each entry corresponds to one currently retained rendered row in the normal output area.
- `GETDISPLAYLINE(i)` indexes this array directly.
- Wrapped rows and explicit line breaks occupy separate display-line entries.
- Temporary lines, while they remain present, also occupy entries in this array.
- Host-generated system/warning/error lines also occupy entries in this array.
- The separate HTML-island layer is **not** part of this array.

### 2.3 Logical output lines

A **logical output line** is one or more consecutive normal display-line entries treated as one line-oriented unit.

Line-oriented APIs and operations such as `LINECOUNT`, `CLEARLINE`, and `HTML_GETPRINTEDSTR` use this model.

Observable consequences:

- One logical line can occupy multiple visible display-line entries.
- `CLEARLINE 1` removes the most recent logical line, including all of its wrapped/display-broken rows.
- `HTML_GETPRINTEDSTR(0)` returns the most recent retained logical line, not merely the last retained row.
- `GETDISPLAYLINE` and `HTML_GETPRINTEDSTR` therefore do **not** count/index the same thing.

### 2.4 Temporary trailing-line state

A **temporary line** is a currently retained normal logical line with overwrite-on-next-normal-visible-line behavior.

Shared properties:

- `REUSELASTLINE` creates a temporary line.
- While retained, a temporary line participates in the normal output model: line-oriented APIs still see/count it.
- The next operation that appends a new normal visible display line first removes the trailing temporary line, then appends the new line(s).
- Merely appending more content to the pending print buffer does **not** remove the trailing temporary line, because no new normal visible line has been appended yet.

### 2.5 HTML-island layer

`HTML_PRINT_ISLAND*` writes to a separate retained layer.

Shared properties:

- It is painted on screen, but it is not part of the normal display-line array or logical-line grouping.
- It is not counted by `LINECOUNT` and is not removed by `CLEARLINE`.
- `GETDISPLAYLINE`, `HTML_GETPRINTEDSTR`, and `HTML_POPPRINTINGSTR` do not read it.
- `HTML_PRINT_ISLAND_CLEAR` clears it without touching the normal output model.

### 2.6 Paint schedule vs stored output state

The engine distinguishes **stored output state** from **immediate repaint timing**.

Shared properties:

- Normal display-line state, pending-buffer state, and island-layer state can change even if the window is not repainted immediately.
- `REDRAW` controls normal repaint scheduling, not whether output state exists.
- The output-readback APIs read stored state, not “only what has already been physically repainted on screen”.

## 3) Producing normal output

### 3.1 Buffered appenders

**Buffered appenders** add segments to the pending print buffer without immediately appending normal display lines.

Examples include:

- plain buffered `PRINT*` variants,
- `PRINTBUTTON*`,
- `HTML_PRINT(<html>, nonZero)`,
- inline image/shape appenders that explicitly say they append to the current print buffer.

Shared rule:

- A buffered append does not yet affect `GETDISPLAYLINE`, `HTML_GETPRINTEDSTR`, or `LINECOUNT`.

### 3.2 Materializing the pending print buffer

When the engine **flushes** the pending print buffer into the normal output model:

- buffered content is converted into one or more normal display-line entries,
- those display-line entries are attached to the current logical line or start a new one according to the pending line-end state,
- if the current trailing normal line is temporary, that temporary line is removed before the new normal display-line entries are appended.

This is the core shared transition from pending buffered output into retained normal output.

### 3.3 Line end vs visible flush-without-line-end

Do not confuse these two transitions:

- **line end**: the current logical line is finalized,
- **visible flush without line end**: buffered content becomes retained normal output, but the same logical line remains open for later appended content.

Examples:

- `PRINTL`-style output both materializes and ends the logical line.
- `PRINTN`-style output materializes and waits, but the next later flush still merges into the same logical line.

### 3.4 Operations that materialize pending content first

Some operations need previously buffered content to become retained normal output before they perform their own visible-state transition.

Shared rule:

- `HTML_PRINT(..., 0)`, `REUSELASTLINE`, host-generated system lines, warning/error lines, and waits that require the current output to be visible first all force this kind of “materialize pending content first” behavior.
- In the wait case, the wait itself does not create a new retained output line; the shared observable effect is simply that pending buffered content has already become visible retained normal output by the time the console is sitting in that wait.

### 3.5 Producers that append to already-buffered content

Other producers do **not** force a separate fresh line before they append their own content.

Compatibility implication:

- `DRAWLINE` / `DRAWLINEFORM` append their line string to the current pending print buffer and then end the line.
- Therefore, if buffered text already exists, the resulting committed output is the combined buffered text plus the draw-line string.

## 4) Host-generated normal lines

Not all retained normal output originates from script `PRINT*` instructions.

The host also appends **system-generated normal lines**, including:

- host/system informational lines,
- warning/error lines,
- some loader/parser/runtime diagnostic lines.

Shared properties:

- These lines join the same normal display-line array and logical-line grouping used by script output.
- `GETDISPLAYLINE`, `HTML_GETPRINTEDSTR`, `LINECOUNT`, and `CLEARLINE` can therefore observe/affect them the same way they observe/affect script-generated normal lines.
- They are not part of the HTML-island layer.
- They are ordinary retained normal lines, not temporary lines, unless a separate temporary-line mechanism is explicitly used.

## 5) Temporary lines

### 5.1 Core rule

`REUSELASTLINE` creates a retained **temporary line**.

Observable contract:

- It is not pending buffered text; it becomes part of the normal output model immediately.
- While retained, it occupies a normal logical-line slot for line-oriented APIs.
- The next later append of a normal visible display line removes it first.

### 5.2 Empty temporary writes do nothing

If `REUSELASTLINE` produces an empty string, it does not append a new temporary line.

Observable consequence:

- an already-retained trailing temporary line is left untouched rather than being cleared by an empty `REUSELASTLINE` call.

### 5.3 Why temporary lines matter outside `REUSELASTLINE`

Temporary lines are not just cosmetic. They are also part of the host-flow contract.

Shared rule:

- Some system flows inspect whether the current trailing retained normal line is temporary.
- If it is temporary, those flows re-open the immediate prompt on the same screen instead of restarting the phase’s top-level redraw.

This coupling is documented in [`system-flow.md`](system-flow.md).

## 6) Button regions and selectable generations

### 6.1 Buttons exist first as output

`PRINTBUTTON*` does not itself wait for input. Its first job is to emit a **button region** into output.

A button region has two externally visible roles:

- a rendered label that appears in output,
- and, if selectable, an associated input value that later button waits may accept.

### 6.2 Buttons are attached to retained line content

A button region is part of the content of the buffered line or retained normal line(s) that contain it.

Observable consequences:

- it is displayed as part of those line(s),
- it survives until the containing buffered/retained line is removed, overwritten, or replaced,
- it is not stored in a completely separate hidden choice list detached from output.

### 6.3 Not every retained button stays selectable forever

The runtime groups buttons into **selectable generations**.

Shared rule:

- Later button waits accept only buttons in the current active generation for that wait.
- Older buttons can remain retained and visible in the output, but no longer be selectable by later typed/button waits.
- This is why later waits do not automatically keep reusing every older visible button still present in scrollback.

### 6.4 Output/readback differences

Not every readback API preserves the same amount of button structure.

Observable distinction:

- `GETDISPLAYLINE` returns plain text for one retained display row, so button metadata/clickability is flattened away.
- `HTML_GETPRINTEDSTR` and `HTML_POPPRINTINGSTR` preserve button structure as `<button ...>` / `<nonbutton ...>` markup.
- Typed `BINPUT*` acceptance checks for existence of a matching selectable button value in the active generation; it does not use rich readback APIs.

### 6.5 Duplicated labels or values

Duplicated labels and duplicated accepted values are allowed as output.

Observable consequence:

- typed/button-value acceptance is value-based: if at least one selectable button in the active generation matches the submitted value, the wait can accept it,
- the script cannot distinguish between multiple same-value buttons by typed submission alone,
- mouse completion still distinguishes by the clicked region and its side-channel data.

## 7) HTML-island model

### 7.1 Accumulation model

Each `HTML_PRINT_ISLAND` call parses its HTML string into one or more display-line objects and appends them to the island layer.

Observable consequences:

- multiple `HTML_PRINT_ISLAND` calls accumulate in insertion order,
- the island layer is not tied to normal logical-line history,
- clearing normal output does not remove earlier island content.

### 7.2 Line formation inside the island

Within one `HTML_PRINT_ISLAND` call:

- `<br>` and literal `\n` create separate island display rows,
- automatic wrapping can also create additional island display rows,
- the resulting rows are appended to the island layer in order.

### 7.3 Painting model

When the window is repainted, the island layer is drawn independently of the normal output log:

- painting starts from the top of the window,
- each retained island display row is drawn on the next row,
- the island layer does not scroll together with the normal output backlog.

### 7.4 State change vs immediate repaint

`HTML_PRINT_ISLAND` and `HTML_PRINT_ISLAND_CLEAR` mutate island-layer state immediately, but they do **not** themselves force an immediate repaint.

Observable consequence:

- with normal redraw scheduling, the changed island state becomes visible on the next repaint,
- with redraw suppressed, the changed state still exists and can appear once a later forced repaint happens.

### 7.5 Layer boundary

The island layer remains isolated from the normal output model:

- `LINECOUNT` and `CLEARLINE` ignore it,
- `GETDISPLAYLINE`, `HTML_GETPRINTEDSTR`, and `HTML_POPPRINTINGSTR` ignore it,
- host/system-generated normal lines do not enter it,
- `HTML_PRINT_ISLAND_CLEAR` clears only it.

## 8) Output skipping and redraw scheduling

### 8.1 `SKIPDISP` is a producer-side gate

`SKIPDISP` affects output-producing instructions before they execute.

Shared contract:

- If an instruction is skipped by the print-skip mechanism, it produces no output.
- Under the reference’s default evaluation rule, a skipped output instruction also performs no argument evaluation and has no side effects unless a built-in explicitly documents an exception.
- Reaching an input instruction while output skipping is active due to `SKIPDISP` is a runtime-error path, not a silent auto-accept path.

### 8.2 `REDRAW` affects paint timing, not stored state

`REDRAW` controls whether non-forced repaints happen automatically.

Shared contract:

- Turning redraw off does **not** erase pending-buffer, retained normal-output, or island-layer state.
- It suppresses non-forced repaint work while the window is at the live bottom, but forced repaints still show the current stored state.
- The output-readback APIs read stored state regardless of whether redraw is currently off.

## 9) Output readback helpers

### 9.1 `GETDISPLAYLINE`

`GETDISPLAYLINE(<lineNumber>)` reads the retained **normal display-line array**.

Shared properties:

- It indexes from the oldest currently retained normal display line.
- `0` means the first retained normal display row.
- It returns one retained display row, not one logical line.
- It returns plain text, not structured HTML.
- It excludes pending buffered output and the HTML-island layer.
- Temporary lines and host-generated normal lines are included while they remain retained.
- Once old rows fall out of the retained normal log, they are no longer accessible by index.

### 9.2 `HTML_GETPRINTEDSTR`

`HTML_GETPRINTEDSTR(<lineNo>)` reads the retained **normal logical-line** history.

Shared properties:

- It indexes logical lines from the newest retained logical line backward.
- `0` means the newest retained logical line.
- It returns grouped structured HTML for that logical line.
- It preserves button markup and uses `<br>` for display-row breaks within that logical line.
- It excludes pending buffered output and the HTML-island layer.
- Temporary lines and host-generated normal lines are included while they remain retained.
- Once older logical lines fall out of the retained normal log, they are no longer accessible here.

### 9.3 `HTML_POPPRINTINGSTR`

`HTML_POPPRINTINGSTR()` reads and clears the current **pending print buffer**.

Shared properties:

- It does not read retained normal history.
- It clears the pending print buffer.
- It does not append the exported content to the normal output area.
- It preserves structured HTML/button information from the pending buffer.
- It does not add outer paragraph/alignment wrappers.
- It does not read the HTML-island layer.

## 10) Relationship to system flow and input flow

### 10.1 System flow depends on output state

`system-flow.md` depends on this topic because some host loops inspect the current trailing retained normal line state.

Most importantly:

- “temporary trailing line” vs “ordinary trailing line” changes whether some flows re-open a prompt or restart a full redraw.

### 10.2 Input flow depends on output objects

`input-flow.md` depends on this topic because later waits consume objects created by output:

- button waits only accept values that match currently selectable button regions,
- mouse-driven completion can target clickable regions embedded in retained output,
- output/readback APIs and input acceptance must therefore agree on what counts as the current retained line content.

## 11) Reimplementation checklist

A compatible implementation should preserve all of the following observable distinctions.

- There is a real difference between pending buffered output, retained normal output, and the separate island layer.
- Retained normal output has both a display-line view and a logical-line view.
- `GETDISPLAYLINE` reads retained display rows; `HTML_GETPRINTEDSTR` reads retained logical lines; `HTML_POPPRINTINGSTR` reads pending buffered output.
- One logical line can occupy multiple retained display rows without becoming multiple logical-line entries.
- `REUSELASTLINE` creates overwrite-on-next-normal-line temporary output rather than ordinary buffered text.
- Merely appending to the pending print buffer does not remove a trailing temporary line.
- Host-generated system/warning/error lines enter the same retained normal output model as script output.
- Buttons are part of output objects before any later input wait consumes them.
- Older visible buttons can remain rendered while becoming unselectable after the active generation changes.
- Plain-text row getters flatten button metadata; HTML getters preserve it.
- The HTML-island layer accumulates independently, paints from the top, ignores normal line counters/getters, and is cleared only by island-specific clearing.
- `REDRAW` changes repaint scheduling rather than redefining stored output state.
- `SKIPDISP` is not merely “don’t draw”; it suppresses output-producing instructions at the producer side and still treats later input as an error boundary.

## 12) Related documents

- [`html-output.md`](html-output.md) — HTML mini-language, tags, attributes, wrapping-oriented rendering rules
- [`input-flow.md`](input-flow.md) — wait lifecycle, button acceptance, mouse completion paths, segmentation
- [`system-flow.md`](system-flow.md) — phase loops that inspect trailing temporary-line state
- [`builtins-reference.md`](builtins-reference.md) — per-built-in signatures and family-specific quirks
- [`cbg-layer.md`](cbg-layer.md) — separate CBG graphics/hit-map state excluded from normal output history
