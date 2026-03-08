# Diagnostic Source Positions

This document describes how this engine attaches **file/line locations** to warnings and errors.

It is **not** part of the EraBasic language itself. A different engine could report locations differently while still being “language compatible”.

## 1) The location model

This engine stores locations as a `(Filename, LineNo)` pair:

- `Filename`: a string (often a path relative to `erb/` or `csv/`, but sometimes an absolute path)
- `LineNo`: a **1-based** line number

There is **no column / byte offset** tracking.

The stored line number is **1-based** even though the reader counter is 0-based. A reader-side value of `-1` therefore becomes a reported `LineNo` of `0`, which is used as a sentinel in a few EOF-style warnings.

## 2) “Physical lines” vs “logical lines”

- A **physical line** is a line in a file as read by `File.ReadAllLines()` / `StreamReader`.
- A **logical line** is what the script parser turns into a `LogicalLine` node (an executable instruction line, label line, etc.).

Most diagnostics are attached to a logical line’s `Position`, which is ultimately derived from a physical line number.

## 3) ERB loading (script files)

### 3.1 Position assignment

During ERB loading, each time the loader accepts the next enabled line, it snapshots the reader's current filename and line number and attaches that pair to the parsed label or statement line.

Important: the stored filename is the reader's display name, not necessarily the raw filesystem path. For ordinary directory loading it is usually a path relative to `erb/` (and uses `\` as a separator if the engine is searching subdirectories). For explicit file-list / analysis-style loads, diagnostics can instead show the supplied absolute path string directly.

### 3.2 Preprocessor directives do not create logical lines

Lines whose first non-whitespace character is `[` (and whose second character is not `[`) are treated as preprocessor directives (e.g. `[IF]`, `[SKIPSTART]`).

Those directive lines are consumed by the loader and **do not** become `LogicalLine` nodes; warnings about malformed directives are attached to the directive line’s `ScriptPosition`.

### 3.3 Line concatenation blocks (`{ ... }`) distort positions

The enabled-line reader can replace a `{ ... }` block with a **single logical input string** containing the concatenated content.

However, it does **not** preserve a per-inner-line mapping. When it finishes reading the block, its current line counter corresponds to the **last physical line it read**; for a normal completed block, that is the line containing `}`. That is the line number later attached to the resulting logical line.

Consequence:

- Diagnostics produced while parsing/executing a logical line originating from a `{ ... }` block report the `}` line number, not the line number where the meaningful content started.
- Errors thrown *inside* the line reader (e.g. malformed `{` line, unexpected `{` inside a block, malformed `}` line, EOF without `}`) report whatever physical line the reader was processing at that moment.

### 3.4 `_Rename.csv` replacement affects text, not locations

If rename processing is enabled (`UseRenameFile`), the enabled-line reader applies `[[...]]` replacement **before tokenization**, on each physical line it reads.

Locations still refer to the original script file and physical line number; there is no mapping back to which rename key produced which characters.

## 4) ERH loading (header files)

Header files are read similarly, but with two important location-related quirks:

- Rename processing is enabled unconditionally for ERH.
- ERH files are required to be `#...` directive lines; most failures are reported with that line’s position.

## 5) CSV/config/data file loaders

Many “language-adjacent” files produce warnings with `ScriptPosition` as well (configs, variable sizes, name tables, etc.).

Patterns used in this engine:

- **Config-like files** often read lines without applying the enabled-line filter first, then attach positions from the reader’s current line counter. Comment/blank lines are skipped *before* the diagnostic position is assigned, but the reported line number still reflects the physical file line number because the reader advances through every line.
- **CSV-like files** often use the enabled-line reader path (skip empty/whitespace-only lines after trimming leading whitespace).
- A few loaders track line numbers manually; at least one such implementation does **not** increment its counter on comment lines, which means the reported `LineNo` can differ from the physical line number in that file.

## 6) Runtime errors: which position is shown

At runtime, error reporting prefers:

1) an explicit position carried by the thrown runtime/script exception, else
2) the current logical line’s stored position

So a runtime error can be positioned either at the exact place where it was detected or at the current executing line.

## 7) “Scanning line” vs “current line” in warnings

During loading/parsing, some helpers emit warnings using a “currently scanning line” value instead of taking a `ScriptPosition` directly.

The warning path prefers a dedicated “currently scanning line” when one is available; otherwise it falls back to the process state's current/error line.

This affects which location is attached to certain warnings generated while parsing expressions or validating definitions.
