# Load/Preprocess/Parse Pipeline (Emuera EvilMask)

This document is a **source-of-truth** description of how this codebase loads EraBasic and related data files, and the exact high-level ordering of preprocessing steps.

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

1) **Load config files** (`ConfigData.LoadConfig()`), then apply them (`Config.SetConfig()`).
2) **Load JSON settings** from `ExeDir/setting.json` (`JSONConfig.Load()`).
3) **Load language/UI resources** (out of scope for a headless interpreter).
4) **Preload file contents** into an in-memory cache (`Preload.Load(erbDir)` and `Preload.Load(csvDir)`).
   - This eagerly reads `*.erb/*.erh/*.erd/*.csv/*.als` under those directories recursively.
   - This does **not** decide “what gets executed” (enumeration rules still decide that), but later readers use `OpenOnCache(...)` and therefore depend on this cache.
5) **Load `_Replace.csv`** (optional; controlled by config; skipped in analysis mode).
6) **Load `_Rename.csv`** (optional; controlled by config).
7) **Load `GAMEBASE.CSV`** (required).
8) **Load all other main CSV data** (including `VariableSize.CSV` and name tables like `ABL.CSV`, etc.).
9) Initialize variable/evaluation subsystems.
10) **Load plugins** (optional; out of scope for a minimal interpreter, but it happens before script parsing in this engine).
11) **Load header files** `*.ERH` (with rename processing enabled).
12) Enable macro expansion (only if ERH defined macros).
13) **Load script files** `*.ERB` (with rename processing enabled only if configured).
14) Parse/build the script and run syntax checks.

The rest of this document breaks down the interpreter-relevant parts of those steps.

## Config load order and layering

Config is layered in this order (later wins):

1) `csv/_default.config` (fallback: `csv/default.config`)
2) `ExeDir/emuera.config`
3) `csv/_fixed.config` (fallback: `csv/fixed.config`) — values successfully parsed from this file become “fixed” (immutable at runtime).

Important: after loading, the engine may auto-write `emuera.config` if it does not exist, and may also update certain keys (e.g. update key) and save.

JSON settings are loaded afterwards from `ExeDir/setting.json`. If it doesn’t exist, a default JSON is written.

## `_Replace.csv` (replace settings) load point

If enabled by config (and not in analysis mode), the engine reads `csv/_Replace.csv` and applies it to configuration-derived “replace settings”.

One key language-adjacent effect: the line-continuation joiner string is taken from config (`ReplaceContinuationBR`) and used when concatenating `{ ... }` blocks (see “Line reading”).

## `_Rename.csv` load point

If enabled by config, the engine reads `csv/_Rename.csv` and builds a mapping of the form:

`[[pattern]]` → `replacement`

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

So `SearchSubdirectory` does **not** change the set of loaded files for those tables.

Two loaders *do* enumerate patterns:

- `CHARA*.CSV` is enumerated via `Config.GetFiles(csvDir, "CHARA*.CSV")`, so:
  - `SearchSubdirectory=YES` enables recursive discovery under `csv/`
  - `SortWithFilename=YES` sorts directory/file names (via `.NET Array.Sort(string[])` inside `Config.GetFiles`)
  - enumeration still relies on `Directory.GetFiles(dir, "CHARA*.CSV")`, so extension matching is filesystem-dependent (typical Windows is effectively case-insensitive; case-sensitive filesystems may require uppercase `.CSV`)
- `VarExt*.csv` (save-extension settings) is enumerated via `Directory.GetFiles(csvDir, "VarExt*.csv", SearchOption.AllDirectories)`:
  - it is always recursive regardless of `SearchSubdirectory`
  - the engine does not explicitly sort the returned list (ordering is filesystem/runtime-dependent)
  - on case-sensitive filesystems, the pattern uses lowercase `.csv`, so uppercase `.CSV` may not match

## ERH loading (headers) vs ERB loading (scripts)

### Header files (`*.ERH`)

ERH files are enumerated by `Config.GetFiles(erbDir, "*.ERH")`:

- if `SearchSubdirectory=YES`, it searches all subdirectories recursively
- if `SortWithFilename=YES`, it sorts both directory names and file names using `.NET Array.Sort(string[])` on full paths (string-ordering can be runtime/culture dependent)
- it filters out “weird glob matches” by requiring `Path.GetExtension(path).Length <= 4` (so patterns like `*.ERB*` are not accidentally picked up)

Case-sensitivity note:

- Enumeration ultimately relies on `Directory.GetFiles(dir, "*.ERH")`, so whether `.erh` is found by `"*.ERH"` depends on the filesystem. Typical Windows deployments behave case-insensitively; case-sensitive filesystems may require uppercase extensions for discovery.

ERH is parsed **before ERB**. In this engine, ERH is allowed to contain:

- `#DEFINE` macros
- `#DIM/#DIMS` global variable declarations (processed in a second pass)

Anything else in ERH is treated as an error.

Rename processing is always enabled for ERH line reading (even if rename is “off” for ERB in config).

### Script files (`*.ERB`) and load ordering

ERB files are enumerated by `Config.GetFiles(erbDir, "*.ERB")`, but with a special ordering rule:

1) Any directory whose path matches `*#*` is loaded first (recursively if subdirectory search is enabled).
2) Then the remaining ERB files are loaded.

Within a directory, the file list may be sorted depending on config.

More precisely, enumeration uses the same `Config.GetFiles(...)` routine:

- `SearchSubdirectory` controls recursion
- `SortWithFilename` controls sorting of both directory and file names (via `.NET Array.Sort(string[])` on full paths; ordering can be runtime/culture dependent)
- file matches are filtered to extensions of length ≤ 4 (to avoid accidental `*.ERB*` matches)

Case-sensitivity note:

- Enumeration ultimately relies on `Directory.GetFiles(dir, "*.ERB")`, so whether `.erb` is found by `"*.ERB"` depends on the filesystem. Typical Windows deployments behave case-insensitively; case-sensitive filesystems may require uppercase extensions for discovery.

Important ordering detail (engine quirk):

- The `*#*` directory list is obtained via `Directory.GetDirectories(erbDir, "*#*", ...)` and is **not** sorted by `SortWithFilename` before being iterated. If multiple `*#*` directories exist, their relative order can therefore depend on filesystem enumeration order.
- Within each chosen directory, the engine uses `Config.GetFiles(dir, erbDir, "*.ERB")` to enumerate ERBs (which *can* be sorted, depending on `SortWithFilename`).
- The engine then enumerates `Config.GetFiles(erbDir, "*.ERB")` for the “remaining” files and skips any absolute paths already loaded from the `*#*` phase.

This ordering affects:

- which function labels are considered “first defined”
- warnings for normal function overloading
- the order of multi-defined event functions

### Macro expansion enable point

Macro expansion is disabled during early init and during ERH parsing.

After ERH has been loaded, macro expansion is enabled only if at least one macro was defined.

This is a real phase boundary: the same tokenization call behaves differently depending on whether `UseMacro` is enabled.

## Line reading (common behavior across config/ERH/ERB/CSV readers)

The core line reader:

- reads the file into a line array using encoding detection
- iterates lines, skipping:
  - empty lines
  - whitespace-only lines
  - lines that become empty after leading whitespace + comment stripping (see below)
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
  - the engine takes `Config.ReplaceContinuationBR`, removes all `"` characters, and appends the result
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

## Fact-check cross-refs (optional)

- Initialization order: `emuera.em/Emuera/Runtime/Script/Process.cs`
- Preload cache load (required for `OpenOnCache(...)`): `emuera.em/Emuera/UI/Game/EmueraConsole.cs`, `emuera.em/Emuera/Runtime/Utils/Preload.cs`
- Directory paths: `emuera.em/Emuera/Program.cs`
- Line reader: `emuera.em/Emuera/Runtime/Utils/EraStreamReader.cs`
- ERB preprocessor state machine: `emuera.em/Emuera/Runtime/Script/Loader/ErbLoader.cs`
- Config loader: `emuera.em/Emuera/Runtime/Config/ConfigData.cs`, `emuera.em/Emuera/Runtime/Config/ConfigItem.cs`
- JSON settings: `emuera.em/Emuera/Runtime/Config/JSON/JSONConfig.cs`
