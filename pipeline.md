# Load/Preprocess/Parse Pipeline (Emuera EvilMask)

This document is a **source-of-truth** description of how this engine loads EraBasic and related data files, and the exact high-level ordering of preprocessing steps.

It is written so that an implementer can reproduce compatible behavior without needing to read the engine source code, while still offering optional fact-check references.

## Directory layout (runtime roots)

At runtime, the engine sets these directories relative to `ExeDir`:

- `ExeDir/`
  - `csv/` (`Program.CsvDir`)
  - `erb/` (`Program.ErbDir`)
  - `debug/` (`Program.DebugDir`)
  - `dat/` (`Program.DatDir`)
  - `resources/` (`Program.ContentDir`)
  - `sound/` (`Program.SoundDir`)
  - `font/` (`Program.FontDir`)

The interpreter-relevant directories are mainly `csv/` and `erb/`.

## Top-level initialization order

This is the actual order in which files/config are loaded before scripts are executed:

Host-boundary note: steps (1)–(4) span an early preload stage and a later runtime-initialization stage. The observable order below is the compatibility-relevant order.

1) **Load config files**, then apply them.
2) **Load JSON settings** from `ExeDir/setting.json`.
3) **Load language/UI resources** (out of scope for a headless interpreter).
4) **Preload file contents** into an in-memory cache.
   - This eagerly reads `*.erb/*.erh/*.erd/*.csv/*.als` under those directories recursively.
   - This does **not** decide “what gets executed” (enumeration rules still decide that), but later file readers do read from this cache.
5) **Load sprites/resources** from `resources/**/*.csv` (and referenced image files) into the sprite dictionary.
6) **Load `_Replace.csv`** (optional; controlled by config; skipped in analysis mode).
7) **Load `_Rename.csv`** (optional; controlled by config).
8) **Load `GAMEBASE.CSV`** (required).
9) **Load all other main CSV data** (including `VariableSize.CSV` and name tables like `ABL.CSV`, etc.).
10) Initialize variable/evaluation subsystems.
11) **Load plugins** (optional; out of scope for a minimal interpreter, but it happens before script parsing in this engine).
12) **Load header files** `*.ERH` (with rename processing enabled).
13) Enable macro expansion (only if ERH defined macros).
14) **Load script files** `*.ERB` (with rename processing enabled only if configured).
15) Parse/build the script and run syntax checks.

The rest of this document breaks down the interpreter-relevant parts of those steps.

## Config load order and layering

Config is layered in this order (later wins):

1) `csv/_default.config` (fallback: `csv/default.config`)
2) `ExeDir/emuera.config`
3) `csv/_fixed.config` (fallback: `csv/fixed.config`) — values successfully parsed from this file become “fixed” (immutable at runtime).

Important: after loading, the engine writes `emuera.config` when that file does not exist, and can also rewrite it when its config-update check decides the stored file metadata is stale.

JSON settings are loaded afterwards from `ExeDir/setting.json`. If it doesn’t exist, a default JSON is written.

## `_Replace.csv` (replace settings) load point

If enabled by config (and not in analysis mode), the engine reads `csv/_Replace.csv` and applies it to the dedicated replace-item set documented in `config-items.md` section 7, not to arbitrary config keys.

Those items are a mix of UI strings/chars and script-visible runtime knobs (for example replace item `DrawLineString`, replace item `MoneyLabel`/replace item `MoneyFirst`, replace item `TimeupLabel`, replace item `MaxShopItem`, and several built-in default-value tables).

Separately, the line-continuation joiner string is taken from the normal config item `ReplaceContinuationBR` and used when concatenating `{ ... }` blocks (see “Line reading”).

## `_Rename.csv` load point

If enabled by config, the engine reads `csv/_Rename.csv` and builds a mapping of the form:

`[[pattern]]` → `replacement`

If config item `UseRenameFile` = `YES` but `csv/_Rename.csv` does not exist, this engine prints an error message and continues with an empty rename dictionary. Missing `_Rename.csv` is therefore a soft host-side error, not a startup abort.

That mapping is used by the line reader for ERB, and also for ERH (ERH forces rename enabled). If `[[...]]` remains in an enabled line after rename processing, later tokenization will treat it as an error.

Rename processing does **not** apply to the main CSV tables loaded for constants and variable names (they use a reader with rename disabled).

## CSV loading order (interpreter-relevant subset)

The engine loads CSV in two phases:

1) `GAMEBASE.CSV`
2) A “constant/name table” loader that:
   - reads `VariableSize.CSV` first (to decide array sizes and “forbidden” arrays)
   - allocates name arrays based on decided sizes
   - loads name tables such as `ABL.CSV`, `TALENT.CSV`, `PALAM.CSV`, etc.
   - optionally loads aliases from `*.als` files next to those tables
   - builds name → index lookup dictionaries used by “string indexing” (`ABL:Skill`, etc.)
   - loads character templates from `CHARA*.CSV` and builds `RELATION` reverse lookup (names/callnames/nicknames/masternames)

This matters for language compatibility because the script expression/indexing grammar allows “name indexing” that depends on these dictionaries.

### CSV folder / subfolder rules (what is actually discovered)

Most CSV tables are loaded by exact filename from `csv/` (top directory only), for example:

- `csv/GAMEBASE.CSV` (required)
- `csv/VariableSize.CSV`
- `csv/ABL.CSV`, `csv/TALENT.CSV`, `csv/PALAM.CSV`, ... (many fixed names)

So config item `SearchSubdirectory` does **not** change the set of loaded files for those tables.

Two loaders *do* enumerate patterns:

- `CHARA*.CSV` discovery:
  - `SearchSubdirectory=YES` enables recursive discovery under `csv/`
  - config item `SortWithFilename` = `YES` sorts directory and file names
  - extension matching is filesystem-dependent (typical Windows is effectively case-insensitive; case-sensitive filesystems may require uppercase `.CSV`)
- `VarExt*.csv` (save-extension settings) discovery:
  - it is always recursive regardless of `SearchSubdirectory`
  - the engine does not explicitly sort the returned list (ordering is filesystem/runtime-dependent)
  - on case-sensitive filesystems, the lowercase `*.csv` pattern may fail to match uppercase `.CSV`

## ERH loading (headers) vs ERB loading (scripts)

### Header files (`*.ERH`)

ERH file discovery rules:

- if `SearchSubdirectory=YES`, it searches all subdirectories recursively
- if `SortWithFilename=YES`, it sorts both directory names and file names using the runtime's normal string sort
- it filters out accidental long-extension glob matches (so patterns like `*.ERB*` are not picked up)

Case-sensitivity note:

- Whether `.erh` is found by `"*.ERH"` depends on the filesystem. Typical Windows deployments behave case-insensitively; case-sensitive filesystems may require uppercase extensions for discovery.

ERH is parsed **before ERB**. In this engine, ERH is allowed to contain:

- `#DEFINE` macros
- `#DIM/#DIMS` global variable declarations (processed in a second pass)

Anything else in ERH is treated as an error.

Rename processing is always enabled for ERH line reading (even if rename is “off” for ERB in config).

### Script files (`*.ERB`) and load ordering

ERB file discovery uses the normal ERB glob, but with a special ordering rule:

1) Any directory whose path matches `*#*` is loaded first (recursively if subdirectory search is enabled).
2) Then the remaining ERB files are loaded.

Within a directory, the file list is sorted only when `SortWithFilename=YES`; otherwise the engine keeps the raw filesystem enumeration order.

More precisely:

- `SearchSubdirectory` controls recursion
- `SortWithFilename` controls sorting of both directory and file names using the runtime's normal string sort
- file matches are filtered to extensions of length ≤ 4 (to avoid accidental `*.ERB*` matches)

Case-sensitivity note:

- Whether `.erb` is found by `"*.ERB"` depends on the filesystem. Typical Windows deployments behave case-insensitively; case-sensitive filesystems may require uppercase extensions for discovery.

Important ordering detail (engine quirk):

- The `*#*` directory list itself is **not** sorted by `SortWithFilename` before iteration. If multiple `*#*` directories exist, their relative order can therefore depend on filesystem enumeration order.
- Within each chosen directory, ERB files follow the same sorted/unsorted rule stated in this section for ordinary ERB discovery.
- The engine then scans the remaining ERB files under `erb/` and skips files already loaded from the `*#*` phase.

This ordering affects:

- which function labels are considered “first defined”
- warnings for normal function overloading
- the order of multi-defined event functions

### Macro expansion enable point

Macro expansion is disabled during early init and during ERH parsing.

After ERH has been loaded, macro expansion is enabled only if at least one macro was defined.

This is a real phase boundary: if `UseMacro` is enabled, tokenization performs macro expansion; if it is disabled, the same tokenization call does not.

## ERB parse/build passes (function-level validation and linking)

After all enabled ERB files are read, the engine performs additional parsing/validation passes that are critical for compatibility.

High-level phases:

1) **Read ERB into a linked list of “logical lines”** (per file).
2) **Parse function label signatures** (user-defined function argument declarations).
3) **Per function**: run three validation/linking passes:
   - argument parsing and method-safe checks
   - structural block matching (“nest check”)
   - jump/call target linking (`JumpTo` wiring)
4) **Whole-program checks**: “function never called” warnings and optional suppression of uncalled functions.

### 1) ERB load: build `LogicalLine` objects

For each enabled ERB line, the loader classifies it by its first non-whitespace character:

- `[` (but not `[[`) → ERB preprocessor directive (handled immediately; does not become a `LogicalLine`)
- `#` → sharp directive, but only inside the current function's post-label sharp block (zero or more consecutive `#...` lines immediately after `@...`, before the first non-`#` logical line)
- `@` / `$` → label line (`FunctionLabelLine` / `GotoLabelLine`)
- otherwise → statement line (`InstructionLine` or `InvalidLine`)

This step does **not** fully parse instruction arguments in the general case. Most instruction lines store a raw “argument slice” and are parsed later (either during load-time validation, or lazily at runtime).

Certain parse failures clear the loader's coarse “load succeeded?” flag even though the loader continues to read the rest of the files:

- invalid function labels (`InvalidLabelLine`)
- invalid statement lines (`InvalidLine`)
- invalid `#...` attribute lines (sharp-line parse failure)

This flag is later used by the startup gate controlled by config item `CompatiErrorLine` (see `errors-and-warnings.md`).

### 2) Function label signature parsing

After label collection, the loader parses function label signatures (the optional `@NAME(...)` / `@NAME, ...` parameter declarations) and builds per-label metadata used by later passes and runtime call binding.

### 3) Per-function three-pass validation/linking

For each function label, the loader performs:

#### Pass 1/3: argument parsing + “method-safe” enforcement

The loader iterates `InstructionLine`s in the function and:

- If the function is a user-defined expression function (`#FUNCTION/#FUNCTIONS`), rejects any instruction not marked as method-safe by marking that line as an error line.
- Parses instruction arguments on load when any of these holds:
  - `NeedReduceArgumentOnLoad=YES`, or
  - analysis mode, or
  - the instruction family always forces load-time argument parsing.

This pass is where many “this line will crash if executed” issues become explicit error-line traps.

#### Pass 2/3: structural block matching (“nest check”)

The loader validates block structure and “syntax blocks” using a nesting stack:

- pairs/matches: `IF..ENDIF`, `SELECTCASE..ENDSELECT`, `REPEAT..REND`, `FOR..NEXT`, `WHILE..WEND`, `DO..LOOP`, `TRYC*..CATCH..ENDCATCH`, `TRY*LIST..ENDFUNC`
- validates restricted regions like `PRINTDATA`/`STRDATA`/`DATALIST` bodies (only specific child lines allowed)
- validates that `$` labels do not appear inside `PRINTDATA*`, `STRDATA`, `DATALIST`, or `TRYCALLLIST` / `TRYJUMPLIST` / `TRYGOTOLIST` bodies (they become error lines)
- wires some per-line jump anchors (e.g. `BREAK`/`CONTINUE` target the nearest enclosing loop marker)

Missing/extra closers and invalid nesting are reported through the warning system; many of those warnings also mark the offending marker line(s) as error lines. The exact warning-vs-error-line split depends on the loader path.

#### Pass 3/3: `JumpTo` wiring and load-time name resolution

The loader calls each instruction’s `SetJumpTo(...)` hook to:

- wire jump targets between marker lines (e.g. `IF` → selected `ELSEIF/ELSE/ENDIF`, `WHILE` ↔ `WEND`, etc.)
- resolve and link constant call/jump targets where applicable:
  - If a call/jump/goto target is a compile-time constant, the engine may resolve it at load time and cache the result on the line.
  - If such a target cannot be resolved and the instruction is not a `TRY*` form, the loader marks the line as an error line.
  - If the target is not constant (e.g. `CALLFORM`, or any other computed-name call), the loader records that dynamic call resolution is needed; resolution is deferred to runtime.

Config interaction (important):

- config item `FunctionNotFoundWarning` affects whether “function not found” warnings are printed, but when this pass marks a line as an error line, that happens regardless of whether the warning is later suppressed by config (see `errors-and-warnings.md`).

### 4) Whole-program function reachability checks

After per-function parsing, the loader runs a “function never called” check unless some call/jump target remained dynamic during load:

- If any target must be resolved dynamically at runtime, the loader treats all functions as “potentially called” and parses them all.
- Otherwise, it warns for functions never reached via static call graph discovery, controlled by config item `FunctionNotCalledWarning`.

Optional hardening (default in this engine):

- If config item `IgnoreUncalledFunction` = `YES`, the loader does **not** parse uncalled functions, and instead plants a runtime trap at the function entry:
  - the first executable line after the label is marked as an error line (“this function should not be called”).
  - calling such a function at runtime therefore throws immediately on entry.

## Line reading (common behavior across config/ERH/ERB/CSV readers)

The core line reader:

- reads the file into a line array using encoding detection
- iterates lines, skipping:
  - empty lines
  - whitespace-only lines
  - lines that become empty after leading whitespace + comment stripping under the line-start rules in `line-start-special-cases.md`
- applies rename replacement (if enabled) **before** tokenization
- supports Emuera line concatenation blocks `{ ... }` unless “disabled” by the caller (used for ERB skip regions)

### Leading whitespace and comment stripping for “enabled line” detection

To decide whether a raw line is “empty”, the reader calls a lexer routine that:

- skips spaces/tabs (and, optionally, full-width spaces if allowed by config)
- treats `;` as a comment start and skips to end of line

If the stream is at end-of-string after that, the line is skipped.

Important: this skipping is only used for “is this line empty” and for brace detection. The returned line stream still contains the original content (except for rename replacement and concatenation).

### Rename replacement details (`[[...]]`)

When rename is enabled, the reader scans for non-overlapping matches of the regex:

    \[\[.*?\]\]

For each matched substring:

- if the rename dictionary contains that exact key, it replaces it with the mapped value
- otherwise it leaves it unchanged

Replacement is **not recursive**: if the replacement text contains another `[[...]]`, it is not processed again in the same pass.

### Line concatenation blocks (`{ ... }`)

When concatenation is enabled and the first non-whitespace character of the line is `{`:

- the line must trim to exactly `{` (otherwise it is an error)
- subsequent raw lines are appended into a single logical line until a closing `}` line is found
- the closing line must contain only `}` (plus whitespace) (otherwise it is an error)
- a joiner string is inserted between appended lines:
  - the engine takes the configured `ReplaceContinuationBR` string, removes all `"` characters, and appends the result
  - the default joiner behaves like a single ASCII space

Concatenation blocks are **not nestable**. Encountering another `{` inside a concatenation block is an error.

If EOF is reached before `}`, it is an error.

### Disabling concatenation in “disabled regions”

Some callers read lines with a `disabled=true` flag.

In this mode:

- brace concatenation is not recognized (so `{`/`}` will not be treated as concatenation markers)
- this exists to avoid false positives while skipping preprocessor-disabled ERB lines

Rename replacement still applies in disabled mode.

## ERB preprocessing blocks (`[ ... ]` lines)

When loading ERB, the loader treats a line as a preprocessor directive iff:

- the first non-whitespace character is `[` **and**
- the next character is not `[` (so `[[...]]` is not treated as a preprocessor line)

Preprocessor lines are parsed as:

    [TOKEN]
    [TOKEN ARG]

Where:

- `TOKEN` is read as an identifier (no macro expansion)
- `ARG` (if any) is read as a second identifier (no quoting, no expressions)
- the line must close with `]` immediately after `ARG` (whitespace after `]` still triggers a warning)
- any characters after `]` cause a warning and are ignored

These directives are case-sensitive in this implementation (`IF` is recognized, `if` is not).

The preprocessor system is *structural* and does not evaluate expressions. The only condition supported is “is a macro name defined”.

Supported directives:

- `[SKIPSTART]` / `[SKIPEND]`
- `[IF_DEBUG]` / `[IF_NDEBUG]`
- `[IF MACRO]` / `[ELSEIF MACRO]` / `[ELSE]` / `[ENDIF]`

Semantics are described in `preprocessor-and-macros.md`, and the exact state machine is in the engine source.
