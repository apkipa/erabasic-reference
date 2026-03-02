# Errors and Warnings (core model)

This document describes the engine’s core **diagnostic model**: how it reports warnings vs errors during config load, script load/parse, and runtime execution.

It is not a full list of messages; it defines the *mechanics* you need for compatible behavior.

## 1) Warning levels and filtering

Warnings carry an integer **level**. The engine treats the numeric level as a severity category and filters output by config:

- Config key: `DisplayWarningLevel`
- If a warning’s `level < DisplayWarningLevel` and the engine is not in analysis mode, the warning is suppressed.

The engine’s internal comment describes the intended meaning as:

- `0`: minor mistake
- `1`: ignorable line / non-fatal issue
- `2`: may be harmful if the line is executed (often treated as “error-ish” during parsing)
- `3`: fatal

Some warnings are additionally gated by `WarnBackCompatibility` (back-compat warnings can be suppressed even if the level passes).

## 2) How warnings are collected and printed

During config load and script load/parse, warnings are accumulated in an internal list (each warning has):

- message text
- optional source position (`filename`, `line`)
- warning level
- optional stack trace text

Warnings are not always printed immediately; at several points the engine “flushes” the list and prints them to the console.

## 3) Parse-time line errors vs non-errors

Some parsing paths treat a malformed line as “this line is invalid” rather than “the entire load must abort”.

Mechanically:

- Certain parsers call a warning function with `isError=true`, which marks the parsed `LogicalLine` as an error line and attaches `ErrMes`.
- The loader can continue reading subsequent lines even if some lines are marked as errors.

This is one reason “warnings” with level `2` often behave like “soft errors”.

## 4) Exceptions: when the engine throws instead of warning

The engine uses exceptions for hard failures. Common families include:

- `CodeEE`: used for script/config/parse-time errors (often includes a source position)
- `ExeEE`: used for runtime execution errors
- specialized subclasses (e.g. identifier-not-found) that some loaders catch and treat specially

Whether an exception aborts loading depends on where it is caught:

- Some loaders catch `CodeEE`, emit a warning, and continue/skip the current unit.
- Other exceptions propagate and abort the current load phase.

## 5) Analysis mode differences

In “analysis mode” (used for static analysis / indexing), the engine relaxes some behaviors:

- some warnings are not filtered by `DisplayWarningLevel`
- some missing-identifier situations in expression parsing may produce placeholder/null terms instead of immediately throwing

If you aim for strict runtime compatibility, treat analysis mode as a separate “tooling” profile.

## 6) Where a warning/error “points” to

EraBasic itself does not define a standard source-location format, but Emuera does.

- Locations are stored as a `(Filename, LineNo)` pair (`ScriptPosition`) without any column.
- Some preprocessing steps (notably `{ ... }` line concatenation and `[[...]]` rename replacement) can make the reported line number differ from where the “meaningful” text appears in the original file.

For the engine-accurate behavior (including `{...}` blocks typically reporting the closing `}` line), see:

- `source-position-mapping.md`

## Fact-check cross-refs (optional)

- Warning collection/filtering/levels: `emuera.em/Emuera/Runtime/Script/Data/ParserMediator.cs`
- Config key definition: `emuera.em/Emuera/Runtime/Config/ConfigData.cs` (`DisplayWarningLevel`)
