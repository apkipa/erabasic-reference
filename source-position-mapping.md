# Diagnostic Source Positions (Emuera Implementation Detail)

This document describes how this Emuera codebase attaches **file/line locations** to warnings and errors.

It is **not** part of the EraBasic language itself. A different engine could report locations differently while still being “language compatible”.

## 1) The only location type: `ScriptPosition`

Emuera stores locations as a `(Filename, LineNo)` pair:

- `Filename`: a string (often a path relative to `erb/` or `csv/`, but sometimes an absolute path)
- `LineNo`: a **1-based** line number

There is **no column / byte offset** tracking.

Implementation note: `ScriptPosition(string srcFile, int srcLineNo)` stores `LineNo = srcLineNo + 1`, where `srcLineNo` is a **0-based** index in the reader. A `srcLineNo` of `-1` becomes `LineNo = 0` and is used as a sentinel in a few “end-of-file” warnings.

Fact-check cross-ref (optional): `emuera.em/Emuera/Runtime/Utils/EmueraException.cs` (`ScriptPosition`).

## 2) “Physical lines” vs “logical lines”

- A **physical line** is a line in a file as read by `File.ReadAllLines()` / `StreamReader`.
- A **logical line** is what the script parser turns into a `LogicalLine` node (an executable instruction line, label line, etc.).

Most diagnostics are attached to a logical line’s `Position`, which is ultimately derived from a physical line number.

Fact-check cross-ref (optional): `emuera.em/Emuera/Runtime/Script/Statements/LogicalLine.cs` (`scriptPosition`).

## 3) ERB loading (script files)

### 3.1 Position assignment

During ERB loading, each time the loader reads the next enabled line, it immediately creates:

    position = new ScriptPosition(eReader.Filename, eReader.LineNo)

and passes that position into the label parser or statement parser. The resulting `LogicalLine.Position` is that `position`.

Important: `eReader.Filename` is the “display name” passed into `EraStreamReader.OpenOnCache(path, name)`. For normal directory loading this is typically a path relative to `erb/` (and uses `\\` as a separator if the engine is searching subdirectories). In some modes it can be an absolute file path.

Fact-check cross-ref (optional): `emuera.em/Emuera/Runtime/Script/Loader/ErbLoader.cs` (`loadErb`).

### 3.2 Preprocessor directives do not create logical lines

Lines whose first non-whitespace character is `[` (and whose second character is not `[`) are treated as preprocessor directives (e.g. `[IF]`, `[SKIPSTART]`).

Those directive lines are consumed by the loader and **do not** become `LogicalLine` nodes; warnings about malformed directives are attached to the directive line’s `ScriptPosition`.

Fact-check cross-ref (optional): `emuera.em/Emuera/Runtime/Script/Loader/ErbLoader.cs` (`PPState`, directive scan).

### 3.3 Line concatenation blocks (`{ ... }`) distort positions

The line reader (`EraStreamReader.ReadEnabledLine`) can replace a `{ ... }` block with a **single returned `CharStream`** containing the concatenated content.

However, the reader does **not** preserve a per-inner-line mapping. When it finishes reading the block, its internal `LineNo` corresponds to the **last physical line it read** (typically the line containing `}`), and that is what the loader turns into `ScriptPosition`.

Consequence:

- Diagnostics produced while parsing/executing a logical line originating from a `{ ... }` block typically report the `}` line number, not the line number where the meaningful content started.
- Errors thrown *inside* the line reader (e.g. malformed `{` line, unexpected `{` inside a block, malformed `}` line, EOF without `}`) report whatever physical line the reader was processing at that moment.

Fact-check cross-ref (optional): `emuera.em/Emuera/Runtime/Utils/EraStreamReader.cs` (`ReadEnabledLine`).

### 3.4 `_Rename.csv` replacement affects text, not locations

If rename processing is enabled (`UseRenameFile`), `EraStreamReader.ReadEnabledLine` applies `[[...]]` replacement **before tokenization**, on each physical line it reads.

Locations still refer to the original script file and physical line number; there is no mapping back to which rename key produced which characters.

Fact-check cross-ref (optional): `emuera.em/Emuera/Runtime/Utils/EraStreamReader.cs` (rename regex + replacement).

## 4) ERH loading (header files)

Header files are read similarly, but with two important location-related quirks:

- Rename processing is enabled unconditionally for ERH (`new EraStreamReader(true)`).
- ERH files are required to be `#...` directive lines; most failures throw `CodeEE` with that line’s position.

Fact-check cross-ref (optional): `emuera.em/Emuera/Runtime/Script/Loader/ErhLoader.cs`.

## 5) CSV/config/data file loaders

Many “language-adjacent” files produce warnings with `ScriptPosition` as well (configs, variable sizes, name tables, etc.).

Patterns used in this codebase:

- **Config-like files** often use `EraStreamReader.ReadLine()` and then compute `ScriptPosition` from the reader’s `LineNo`. Comment/blank lines are skipped *before* `ScriptPosition` is assigned, but the reported `LineNo` still reflects the physical file line number because the reader increments through every line.
- **CSV-like files** often use `EraStreamReader.ReadEnabledLine()` (skip empty/whitespace-only lines after trimming leading whitespace).
- A few loaders track line numbers manually; at least one such implementation does **not** increment its counter on comment lines, which means the reported `LineNo` can differ from the physical line number in that file.

Fact-check cross-refs (optional):

- Config load: `emuera.em/Emuera/Runtime/Config/ConfigData.cs` (`loadConfig`)
- Variable sizes and name tables: `emuera.em/Emuera/Runtime/Script/Data/ConstantData.cs`
- Rename CSV manual line counter quirk: `emuera.em/Emuera/Runtime/Script/Data/ParserMediator.cs` (`LoadEraExRenameFile`)

## 6) Runtime errors: which position is shown

At runtime, error reporting prefers:

1) the `Position` stored in the thrown `EmueraException` (e.g. a `CodeEE` created with a `ScriptPosition`), else
2) the current logical line’s `Position` (the engine’s current instruction line)

So a runtime error can be positioned either at the exact place where it was detected (if the engine threw an exception with an explicit `ScriptPosition`) or at the current executing line.

Fact-check cross-ref (optional): `emuera.em/Emuera/Runtime/Script/Process.cs` (`handleException`).

## 7) “Scanning line” vs “current line” in warnings

During loading/parsing, some helpers emit warnings using a “currently scanning line” value instead of taking a `ScriptPosition` directly.

This codebase exposes a dedicated “currently scanning line” getter:

- if `Process.scaningLine` is non-null, it returns that
- otherwise it falls back to the process state’s current/error line

This affects which location is attached to certain warnings generated while parsing expressions or validating definitions.

Fact-check cross-ref (optional): `emuera.em/Emuera/Runtime/Script/Process.cs` (`GetScaningLine`).

