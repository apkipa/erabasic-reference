# Program Structure (files, functions, blocks)

## Folder layout (engine assumptions)

This Emuera codebase assumes a conventional “game root” directory containing `erb/` and `csv/`.

### Root directory selection

On startup, the engine selects `ExeDir` as:

- `AppContext.BaseDirectory`, but
- if a `Data/erb` directory exists under that base directory, it uses `AppContext.BaseDirectory/Data` instead.

So the selected root is always one of exactly two directories: the executable directory itself, or its `Data/` subdirectory when `Data/erb` exists.

### Expected subdirectories

Under `ExeDir`, the engine uses these directories (trailing path separator is normalized internally):

- `erb/` — ERB scripts (`*.ERB`) and headers (`*.ERH`)
- `csv/` — config layers and CSV tables (`*.CSV`, `*.ALS`, `_Rename.csv`, etc.)
- `dat/` — runtime data inputs/outputs tied to built-ins (not fully specified in this phase)
- `resources/` — engine resource files used by image/sprite/UI-facing features
- `debug/` — debug outputs/config
- `font/` — optional font files (`*.ttf`/`*.otf`) loaded recursively at startup
- `sound/` — audio files used by sound-related built-ins

Compatibility note (saves):

- The save directory is controlled by config (not just folder layout). When `UseSaveFolder=YES`, saves go under `ExeDir/sav/`; otherwise they are written directly under `ExeDir/`.

### Case sensitivity of directory names (important)

The engine hard-codes directory names such as `csv` and `erb` when building paths (see `Program.SetDirPaths`).

On typical Windows deployments this is not observable, but on case-sensitive filesystems you must match the exact directory names (`csv/`, `erb/`, etc.) or startup will fail to find them.

### Case sensitivity of file discovery (important)

Script/data file discovery uses filesystem globbing such as `Directory.GetFiles(dir, "*.ERB")`.

This means extension matching is **environment-dependent**:

- On Windows (the intended platform), discovery is effectively case-insensitive (`.erb` and `.ERB` are both found).
- On case-sensitive filesystems (typical Linux), `"*.ERB"` may match only `.ERB` files, not `.erb`.

If you need cross-platform behavior that matches typical Emuera deployments, treat extension matching as case-insensitive in your reimplementation.

### Subdirectory loading rules (ERH/ERB/CSV)

ERH (`*.ERH`) and ERB (`*.ERB`) discovery is controlled by config:

- `SearchSubdirectory` controls whether `erb/` is searched recursively.
- `SortWithFilename` controls whether directory and file names are sorted before loading (using the runtime’s string sort).

This codebase also applies a special ERB ordering rule: directories matching `*#*` are loaded first (see `pipeline.md` for the precise algorithm).

CSV discovery is *not* recursive except for the cases listed in the bullets that follow:

- Most CSV tables are loaded by exact filename from `csv/` (e.g. `GAMEBASE.CSV`, `VariableSize.CSV`, `ABL.CSV`, ...), so `SearchSubdirectory` does not affect those.
- Two notable exceptions:
  - `CHARA*.CSV` discovery uses `Config.GetFiles(csvDir, "CHARA*.CSV")`, so it is affected by `SearchSubdirectory` and `SortWithFilename` (and filesystem case-sensitivity of `"*.CSV"`).
  - `VarExt*.csv` discovery uses `Directory.GetFiles(csvDir, "VarExt*.csv", SearchOption.AllDirectories)` unconditionally (recursive regardless of `SearchSubdirectory`, and ordering is not explicitly sorted).

## File types

- `*.ERB`: script files. Contain function labels (`@...`) and statements.
- `*.ERH`: header files. Loaded before ERB; intended for:
  - Global-scope variable declarations via `#DIM/#DIMS`
  - Macro declarations via `#DEFINE`

Header file (ERH) rules in Emuera:

- All `*.ERH` files in the ERB folder are loaded.
- Loading order is: CSV files → `*.ERH` → `*.ERB`.
  - ERH effects therefore do **not** apply to CSV content.
- ERH files should contain only `#DIM`, `#DIMS`, and `#DEFINE` lines. Other content is considered invalid for headers.
- Some engine variants apply `_rename.csv`-style replacement to ERH, which can affect compatibility with other engines.

## Functions (labels)

Functions are declared by a label that starts with `@`:

    @SYSTEM_TITLE
        ; ...

Functions are invoked using `CALL`, `JUMP`, and related commands (see `functions.md` and the built-in reference).

For exact rules on what names are allowed, case-sensitivity, duplicate selection, event grouping, and `$` labels, see `labels.md`.

### Event functions vs normal functions

Some function names are treated specially by the engine as event entry points (e.g. `@SYSTEM_TITLE`, `@EVENTLOAD`, `@TITLE_LOADGAME`). Their presence can change startup/load flow.

Event functions may have multiple definitions; dispatch groups them by event name and attributes such as `#ONLY`, `#PRI`, and `#LATER`. For ordinary non-event functions, duplicate definitions do not create a dispatch group: the first definition is the primary one, and later ones only trigger duplicate-definition diagnostics/warnings as configured.

## Local jump labels (`$...`)

Lines beginning with `$NAME` define a local jump target. These labels are scoped to the surrounding function label and are used by jump-style built-ins (see `builtins*.md`).

Exact scoping and duplicate handling is specified in `labels.md`.

## Function attributes (`#...` under a label)

Some `#`-directives must appear immediately under a function label to affect that function.

Commonly documented:

- `#ONLY` — for event functions: if present, only that one definition runs.
- `#FUNCTION` / `#FUNCTIONS` — marks the function as an expression function (numeric / string).
- `#LOCALSIZE` / `#LOCALSSIZE` — sets the `LOCAL/LOCALS` array sizes for that function (ignored for event functions).
- `#DIM` / `#DIMS` — declares function-private variables.

Other engine-supported event attributes exist (e.g. `#PRI`, `#LATER`, `#SINGLE`)—these are parsed by the engine even if not always covered in high-level language tutorials.

## Blocks and “special block lines”

Some constructs are represented by block-like keyword lines. These lines should contain only the block keyword (no trailing commands/comments on the same line).

Notable examples:

- `[SKIPSTART]` … `[SKIPEND]` — skip lines in Emuera (useful for cross-engine compatibility).
- `[IF XXX]` … `[ELSEIF XXX]` … `[ELSE]` … `[ENDIF]` — conditional inclusion based on `#DEFINE`.
- `[IF_DEBUG]` … `[ENDIF]`, `[IF_NDEBUG]` … `[ENDIF]` — debug-mode conditional inclusion.

For details, see `preprocessor-and-macros.md`.
