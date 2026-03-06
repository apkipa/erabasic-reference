# Errors and Warnings (core model)

This document describes the engine’s core **diagnostic model**: how it reports warnings vs errors during config load, script load/parse, and runtime execution.

It is not a full list of messages; it defines the *mechanics* you need for compatible behavior.

Terminology used in this reference:

- **Warning**: a diagnostic message recorded during config/script loading or analysis. Warnings do not necessarily stop loading.
- **Error line**: a parsed line object that is marked as invalid for execution (`line.IsError == true`) and will throw if reached at runtime.
- **Invalid line**: a line that could not be parsed into a meaningful statement object; it is represented by a distinct `InvalidLine`/`InvalidLabelLine` object and is always an error line.
- **Exception error**: a thrown exception (`CodeEE`, `ExeEE`, etc.) that aborts the current load phase or current runtime execution step, depending on where it is caught.

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

Important engine behavior (affects compatibility):

- When the engine is running ERB “from memory” (`console.RunERBFromMemory == true`), most warnings are not added to the global warning list (so they will not be printed by `FlushWarningList`).
  - This does not prevent line objects from being marked as error lines (see §3); it only affects warning output.

## 3) Parse-time line errors vs non-errors

Some parsing paths treat a malformed line as “this line is invalid” rather than “the entire load must abort”.

Mechanically:

- Certain parsers call a warning function with `isError=true`, which marks the parsed `LogicalLine` as an error line and attaches `ErrMes`.
- The loader can continue reading subsequent lines even if some lines are marked as errors.

This is one reason “warnings” with level `2` often behave like “soft errors”.

Compatibility-critical nuance:

- Marking a line as an error line (`isError=true`) happens **before** warning filtering (`DisplayWarningLevel`) and before back-compat suppression (`WarnBackCompatibility`).
  - Even if the warning message is suppressed, the line may still be non-executable and will throw if reached.

### 3.1 “Invalid line” vs “error line”

The engine uses multiple representations for “bad” lines:

- **Invalid line objects** (`InvalidLine`, `InvalidLabelLine`):
  - represent lines that could not be parsed at all (or function labels that are structurally invalid)
  - are always error lines (`IsError == true`)
  - typically cause the loader to report “cannot interpret” issues; whether startup still proceeds is determined later by the loader flag / `CompatiErrorLine` behavior described in §7
- **Normal line objects marked as error lines**:
  - represent lines that were parsed into a statement object, but were later determined to be invalid (for example, disallowed instructions in a `#FUNCTION` body, or unresolved constructs under specific config rules)
  - behave like runtime traps: if execution reaches the line, the interpreter throws `CodeEE(line.ErrMes)`

### 3.2 Instruction-line argument errors (`func.IsError`)

Instruction lines have two different “error bits”:

- `line.IsError` on the `LogicalLine` itself (set by parsers/validators; throws immediately when reached)
- `func.IsError` on an `InstructionLine`’s parsed argument object (set when argument parsing fails)

At runtime, if an `InstructionLine` has not had its arguments parsed yet, the engine parses them lazily.
If that lazy argument parse sets `func.IsError`, the engine throws a `CodeEE(func.ErrMes)` when the line is reached.

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

## 7) Startup behavior and `CompatiErrorLine` (engine behavior)

This engine has two different “load succeeded?” signals:

1) A loader return flag (`noError` in the main `Process`) that is set to `false` when the loader encounters *certain* hard parse failures during the ERB load phase (notably invalid label lines, invalid non-label lines, and some invalid `#...` attribute lines).
2) The presence of error lines (`line.IsError == true`) created during later validation passes.

At the “begin title” boundary, this codebase checks only the loader flag:

- If `noError == false` and `CompatiErrorLine == NO`, the engine stops at title with an error prompt (“cannot interpret”).
- If `CompatiErrorLine == YES`, the engine proceeds into normal execution even when `noError == false`.

Important limitation:

- `CompatiErrorLine` does not guarantee that scripts with error lines are safe to run. If execution reaches an error line, the interpreter still throws `CodeEE`.

## Fact-check cross-refs (optional)

- Warning collection/filtering/levels: `emuera.em/Emuera/Runtime/Script/Data/ParserMediator.cs`
- Config key definition: `emuera.em/Emuera/Runtime/Config/ConfigData.cs` (`DisplayWarningLevel`)
