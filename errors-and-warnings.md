# Errors and Warnings (core model)

This document describes the engine’s core **diagnostic model**: how it reports warnings vs errors during config load, script load/parse, and runtime execution.

It is not a full list of messages; it defines the *mechanics* you need for compatible behavior.

Terminology used in this reference:

- **Warning**: a diagnostic message recorded during config/script loading or analysis. Warnings do not necessarily stop loading.
- **Error line**: a parsed line object that is marked as invalid for execution and will throw if reached at runtime.
- **Invalid line**: a line that could not be parsed into a meaningful statement object; it is represented by a distinct `InvalidLine`/`InvalidLabelLine` object and is always an error line.
- **Exception error**: a thrown hard failure. At the boundary where it escapes, it aborts that current load phase or runtime execution step.

## 1) Warning levels and filtering

Warnings carry an integer **level**. The engine treats the numeric level as a severity category and filters output by config:

- Filtering uses config item `DisplayWarningLevel`.
- If a warning’s `level < DisplayWarningLevel` and the engine is not in analysis mode, the warning is suppressed.

The engine’s own severity note describes the intended meaning as:

- `0`: minor mistake
- `1`: ignorable line / non-fatal issue
- `2`: may be harmful if the line is executed; many parse-time “invalid line” reports use this level
- `3`: fatal

Back-compat warnings are additionally gated by config item `WarnBackCompatibility` (they can be suppressed even if the level passes).

## 2) How warnings are collected and printed

During config load and script load/parse, warnings are accumulated in a warning list (each warning has):

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

This is one reason many level-`2` parse warnings behave like “soft errors”: they may also mark the line itself as invalid.

Compatibility-critical nuance:

- Marking a line as an error line (`isError=true`) happens **before** warning filtering (`DisplayWarningLevel`) and before back-compat suppression (`WarnBackCompatibility`).
  - Even if the warning message is suppressed, the line may still be non-executable and will throw if reached.

### 3.1 “Invalid line” vs “error line”

The engine uses multiple representations for “bad” lines:

- **Invalid line objects** (`InvalidLine`, `InvalidLabelLine`):
  - represent lines that could not be parsed at all (or function labels that are structurally invalid)
  - are always error lines (`IsError == true`)
  - cause the loader to report “cannot interpret” issues; whether startup still proceeds is determined later by the loader flag / config item `CompatiErrorLine` behavior described in §7
- **Normal line objects marked as error lines**:
  - represent lines that were parsed into a statement object, but were later determined to be invalid (for example, disallowed instructions in a `#FUNCTION` body, or unresolved constructs under specific config rules)
  - behave like runtime traps: if execution reaches the line, the interpreter throws using that line's stored error message

### 3.2 Deferred argument-parse errors

Instruction lines have two separate failure states:

- the `LogicalLine` itself may already be marked as an error line by parsers/validators, in which case execution throws immediately when it reaches that line
- the line may still be structurally valid, but its instruction arguments may fail when they are first parsed

At runtime, if an `InstructionLine` has not had its arguments parsed yet, the engine parses them lazily. If that lazy argument parse fails, the engine throws at that point using the argument-parser error message.

## 4) Exceptions: when the engine throws instead of warning

The engine uses exceptions for hard failures. Common families include:

- one family for script/config/parse-time errors (often carrying a source position)
- one family for runtime execution errors
- specialized variants; for example, the ERH `#DIM/#DIMS` loader can catch an unresolved-identifier failure, retry after more declarations are known, and only later downgrade it to a warning if still unresolved

Whether an exception aborts loading depends on where it is caught:

- Some loaders catch script/config exceptions, emit a warning, and continue or skip the current unit. Examples include config / `_Replace.csv` loading and the ERH `#DIM/#DIMS` pass.
- Other exceptions propagate and abort the current load phase.

## 5) Analysis mode differences

In “analysis mode” (used for static analysis / indexing), the engine changes some behaviors:

- parser warnings bypass the normal `DisplayWarningLevel` suppression check
- unresolved function references in expression parsing can return `NullTerm(0)` instead of immediately throwing, so analysis can continue and record the missing name

If you aim for strict runtime compatibility, treat analysis mode as a separate “tooling” profile.

## 6) Where a warning/error “points” to

EraBasic itself does not define a standard source-location format, but Emuera does.

- Locations are stored as a `(Filename, LineNo)` pair (`ScriptPosition`) without any column.
- Some preprocessing steps (notably `{ ... }` line concatenation and `[[...]]` rename replacement) can make the reported line number differ from where the “meaningful” text appears in the original file.

For the engine-accurate behavior (including `{...}` blocks reporting the closing `}` line as their logical-line position), see:

- `source-position-mapping.md`

## 7) Startup behavior and `CompatiErrorLine` (engine behavior)

This engine has two different “load succeeded?” signals:

1) A coarse loader-success flag that is cleared when the ERB loader encounters an invalid label line, an invalid non-label line, or a `#...` line whose parser reports failure.
2) The presence of error lines created during later validation passes.

At the “begin title” boundary, this engine checks only the coarse loader flag:

- If that flag indicates failure and `CompatiErrorLine == NO`, the engine stops at title with an error prompt (“cannot interpret”).
- If `CompatiErrorLine == YES`, the engine proceeds into normal execution even when that flag indicates failure.

Important limitation:

- `CompatiErrorLine` does not guarantee that scripts with error lines are safe to run. If execution reaches an error line, the interpreter still throws.
