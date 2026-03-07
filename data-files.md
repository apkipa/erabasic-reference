# Data and Config Files (language-adjacent)

This engine’s “language” is not only ERB syntax: it is tightly coupled to configuration and CSV-driven tables that affect parsing, variable sizes, and name-based indexing.

This document specifies the file formats and behaviors that a compatible interpreter needs to reproduce.

## 0) Text decoding and line splitting (all text files)

Emuera treats most of its inputs as “line-based text files” (ERB/ERH/ERD/CSV/ALS/config).

### 0.1 Encoding detection

The engine chooses a decoding as follows:

1) If the file starts with a UTF-8 BOM (`EF BB BF`), decode as UTF-8 (BOM-aware).
2) Otherwise, attempt to read the file as UTF-8 **strictly** (invalid byte sequences cause failure).
   - If .NET detects some other BOM encoding during this attempt (e.g. UTF-16 with BOM), that detected encoding is used instead of UTF-8.
3) If strict UTF-8 reading fails, fall back to Shift-JIS (code page 932), also with strict decoder fallbacks.

This means:

- UTF-8 without BOM is accepted if it is valid UTF-8.
- Shift-JIS is the “default legacy” fallback when UTF-8 decoding fails.
- Files with “broken” byte sequences that are invalid in both UTF-8 and Shift-JIS do not decode successfully.
- This shared section defines only the decode decision itself; the higher-level loader then decides whether that becomes a warning-and-skip, a printed load-failure, or an abort of that load path.

### 0.2 Line splitting

Most loaders ultimately use `.NET File.ReadAllLines(...)` (directly or via the preload cache):

- Line terminators are not preserved; each returned string is a line without `\r` / `\n`.
- Empty lines are represented as empty strings; whether they are skipped is decided by the specific loader.

## 0.3 File locations and subfolder discovery (overview)

Emuera’s loaders are a mix of “open an exact filename in `csv/`” and “enumerate a pattern”.

- **Exact-path CSVs (top directory only):** most tables are opened by exact name in `csv/` (examples: `GAMEBASE.CSV`, `VariableSize.CSV`, `ABL.CSV`, ...). Placing these in subfolders does not work in this codebase.
- **Pattern-enumerated CSVs:**
  - `CHARA*.CSV` uses `Config.GetFiles(csvDir, "CHARA*.CSV")`, so `SearchSubdirectory` / `SortWithFilename` affect whether it searches subfolders and how it orders results.
  - `VarExt*.csv` (save-extension settings) is enumerated with `SearchOption.AllDirectories` unconditionally and is not explicitly sorted.

For the full runtime load order and ordering quirks, see `pipeline.md`.

## 1) Config files (`*.config`)

### 1.1 Files and load order

The engine layers configuration from three files (later wins):

1) `csv/_default.config` (fallback: `csv/default.config`)
2) `ExeDir/emuera.config`
3) `csv/_fixed.config` (fallback: `csv/fixed.config`) — when a value is successfully parsed from this file, it becomes **fixed** (immutable).

### 1.2 Syntax

Each non-empty, non-comment line is:

    KEY:VALUE

Rules:

- Lines starting with `;` are comments and ignored.
- The key is the substring before the first `:`.
- The value is the substring after the first `:`. `TextEditor` has extra loader logic so later `:` characters are preserved in the path; `EditorArgument` has its own raw-substring handling (see `config-items.md`).
- Unknown keys are ignored.

Important: the engine uppercases the parsed `KEY` and matches it against known items. For main config items, it accepts multiple key spellings (config code name, JP label, EN label). For the exact accepted key set and defaults, see `config-items.md`.

### 1.3 Value parsing (core types)

Depending on the config key, values are parsed as:

- **bool**: accepts `YES/NO`, `TRUE/FALSE`, and similar “on/off” spellings (case-insensitive).
- **int/long**
- **string**
- **Color**: `R,G,B`
- **enum**: parsed by enum name (case-insensitive)
- **List<string>**: comma-separated list
- **List<long>**: `/`-separated list (each element must parse as long)

If parsing fails, the engine records a config warning.

### 1.4 Fixed config behavior

When reading `fixed.config` / `_fixed.config`, if a line’s value parses successfully, the corresponding item becomes fixed.

Fixed items:

- cannot be changed later by other config files
- cannot be changed by runtime UI/config editing

## 2) JSON settings (`setting.json`)

The engine also loads `ExeDir/setting.json`. If missing, it writes a default JSON file and then reads it.

Current fields include:

- `UseNewRandom`
- `UseScopedVariableInstruction`
- `UseButtonFocusBackgroundColor` (UI-related)

These flags can affect runtime semantics and warning behavior. In particular, `UseNewRandom` switches `RAND` from the legacy SFMT(MT19937)-based engine (with `RANDDATA` snapshot support) to a host `.NET System.Random` instance, and makes `RANDOMIZE`, `DUMPRAND`, and `INITRAND` warning-only no-ops.

## 3) `_Replace.csv` (replace settings)

If enabled by config, the engine reads `csv/_Replace.csv`.

### 3.1 Syntax

Each non-empty, non-comment line is:

    ITEM,VALUE
    ITEM:VALUE

Rules:

- Lines starting with `;` are comments and ignored.
- The first separator is either `,` or `:`.
- `ITEM` is trimmed.
- `VALUE` is the remainder of the line after the first separator (so it may contain additional commas/colons).

### 3.2 Replaceable item set and observable effects

`_Replace.csv` does **not** target arbitrary config keys. It only targets the dedicated replace-item set listed in `config-items.md`:

- currency/unit presentation: `MoneyLabel`, `MoneyFirst`
- loading/title/menu strings: `LoadLabel`, `TitleMenuString0`, `TitleMenuString1`
- rendering strings/chars: `DrawLineString`, `BarChar1`, `BarChar2`
- other host/script-visible text: `TimeupLabel`
- runtime limits/defaults: `MaxShopItem`, `ComAbleDefault`, `StainDefault`, `ExpLvDef`, `PalamLvDef`, `pbandDef`, `RelationDef`

This means `_Replace.csv` is not merely cosmetic. Some entries are observable from scripts or script-visible runtime state, for example:

- `DrawLineString` changes the string used for `DRAWLINE` output.
- `MoneyLabel` / `MoneyFirst` affect money-formatted output such as `MONEYSTR(...)` and shop displays.
- `TimeupLabel` is the default timeout message for timed input instructions when the script does not supply its own timeout text.
- `MaxShopItem` changes the accepted shop selection range.
- `ComAbleDefault`, `StainDefault`, `ExpLvDef`, `PalamLvDef`, `pbandDef`, `RelationDef` change engine-provided initial values for built-in runtime data.

Separately, the **line concatenation joiner** is controlled by a normal config value (`ReplaceContinuationBR`), not by `_Replace.csv`, and is used by the line reader:

- the engine removes all `"` characters from this config string and appends the result between concatenated lines
- default behavior approximates inserting a single ASCII space between lines

## 4) `_Rename.csv` (rename mapping for `[[...]]`)

If enabled by config, the engine reads `csv/_Rename.csv` and builds a dictionary used for rename replacement in ERB and ERH line reading. If `UseRenameFile=YES` but the file is missing, the host prints an error message and continues with an empty rename dictionary.

### 4.1 Syntax

Each non-empty line that does **not** start with `;` is split by an “unescaped comma” regex: commas preceded by `\` are not separators.

Only lines that split into **exactly two fields** are used.

Let the two fields be:

- `A = tokens[0].Trim()`
- `B = tokens[1].Trim()`

Then the rename dictionary entry is:

    key   = "[[" + B + "]]"
    value = A

So `_Rename.csv` is written as:

    replacement,pattern

and the script uses:

    [[pattern]]

### 4.2 Application rules

- Replacement is applied **per line** before tokenization.
- Replacement uses a regex scan for substrings matching `[[...]]`.
- Replacement is not recursive: if the replacement text contains another `[[...]]`, it is not processed again in the same pass.
- If an enabled line still contains `[[...]]` after rename processing, later tokenization treats it as an error (“cannot rename key”).

Important compatibility quirk in this codebase:

- ERH line reading enables rename processing unconditionally (even if rename is “off” for ERB in config).
- Main CSV tables (name/constant CSVs) are read with rename disabled.

## 5) `VariableSize.CSV` (built-in array sizes and prohibitions)

`csv/VariableSize.CSV` is loaded early during constant/name-table loading. It affects:

- built-in array sizes (1D/2D/3D)
- “forbidden variables” (by specifying a negative size for certain arrays)
- coupling between certain variables and their `*NAME` name tables

### 5.1 Syntax

Each enabled line is split by comma:

    VARNAME,L1
    VARNAME,L1,L2
    VARNAME,L1,L2,L3

Rules:

- `VARNAME` is trimmed and resolved to a known built-in variable identifier.
- `L*` must parse as integers.
- Lines with fewer than 2 tokens are warned and ignored.

### 5.2 Forbidden arrays (negative sizes)

If `L1` is negative:

- if the variable is allowed to be forbidden, it becomes prohibited (internally treated as length `0`)
- if the variable is not allowed to be forbidden, the engine warns and ignores the prohibition

Note: `L1 == 0` is invalid and warned.

### 5.3 Size constraints (enforced)

The engine enforces several limits; key ones:

- 1D arrays:
  - local arrays must be at least 1
  - non-local arrays must be at least 100
  - length must be ≤ 1,000,000
- 2D/3D arrays:
  - each dimension must be ≥ 1 and ≤ 1,000,000
  - total element count must be ≤ 1,000,000

Violations are warned and ignored.

### 5.4 Coupling with name tables (`*NAME`)

Many variables have an associated name table variable (e.g. `ABL` and `ABLNAME`).

After reading `VariableSize.CSV`, the engine reconciles sizes so that:

- if only one side was changed, the other follows
- if both were changed inconsistently, the engine warns and chooses a max/adjusted value

Special cases include coupled families like `PALAM/JUEL/PALAMNAME` and `CDFLAG`/`CDFLAGNAME1`/`CDFLAGNAME2` which have extra constraints.

## 6) Name table CSVs (`ABL.CSV`, `TALENT.CSV`, etc.)

These CSV files define the “string indexing” keys used by expressions like:

    ABL:Skill
    TALENT:"Brave"

### 6.1 Syntax

Each enabled line is interpreted as:

    INDEX,NAME(,EXTRA...)

Rules:

- The line must contain at least one comma.
- `INDEX` must parse as an integer.
- `INDEX` must be within bounds of the target name array (as sized by `VariableSize.CSV` reconciliation).
- `NAME` is taken as the raw substring after the first comma (it is not fully CSV-escaped).
- Duplicate `INDEX` definitions warn and overwrite.

Some tables also parse a third field as a numeric value (example: `ITEM.CSV` can store an item price).

### 6.2 Alias files (`*.als`)

If a file named `<TableName>.als` exists next to a name table, it is loaded as aliases.

Syntax:

    INDEX,ALIAS

The engine stores `ALIAS → INDEX` mappings.

Important:

- Alias keys must be unique. Duplicate alias strings can raise an exception in the loader (treated as an unexpected error).
- Alias index bounds are not validated at load time.

## 7) ERD identifier files (`*.ERD`) for user-defined variables

When the `UseERD` config is enabled, the engine supports “CSV-like string keys” for **user-defined variables** declared via `#DIM/#DIMS` in ERH.

### 7.1 Discovery rules

At ERH load time, the engine gathers candidate identifier-definition files from:

- all `*.erd` files under `erb/` (all directories)
- all `*.csv` files directly under `csv/` (top-level only)

Candidates are grouped by uppercase file base name:

- `HOGE.ERD` or `HOGE.CSV` defines keys for variable `HOGE` (1D)
- `HOGE@1.ERD`, `HOGE@2.ERD`, ... define keys per dimension for multi-dimensional variables

### 7.2 File format

ERD files use the same simple format as name tables:

    INDEX,NAME

When multiple ERD/CSV files are collected for the same key group, the engine merges them, but:

- if the same `NAME` is defined more than once across files, the engine errors

### 7.3 When they apply

After the engine creates a user-defined variable from ERH `#DIM/#DIMS`, it looks for matching ERD keys and loads them into a lookup dictionary for that variable name (or `name@dim` for multi-dimensional variables).

This enables expressions like:

    MYVAR:SomeKey

for user-defined variables, using the same “string indexing” mechanism as built-in CSV-backed variables.

## 8) `VarExt*.csv` (EM extension save partitions: Map / XML / DataTable)

This codebase implements additional persistent containers not present in classic EraMaker:

- `DataStringMaps`: `Dictionary<string, Dictionary<string, string>>`
- `DataXmlDocument`: `Dictionary<string, XmlDocument>`
- `DataDataTables`: `Dictionary<string, DataTable>`

These are keyed by an arbitrary **string key name** (e.g. `"FOO"`), and various built-in instructions manipulate them (semantics deferred).

`VarExt*.csv` defines which keys belong to which “persistence partition”:

- **save-slot partition**: cleared on normal reset/load; stored in normal save slots
- **global-save partition**: cleared on global reset/load; stored in the global save file
- **static partition**: cleared only on global reset; **not** stored in save files

### 8.1 Discovery rules

At constant-data load time, the engine enumerates:

- all files matching `VarExt*.csv` under `csv/` using `SearchOption.AllDirectories`

Ordering notes:

- The enumeration is not explicitly sorted in this codebase.
- The settings from all discovered files are merged (union of key sets).

### 8.2 File format and parsing

Each enabled line is split using a simple comma split:

    CATEGORY,key1,key2,key3,...

Rules:

- Lines with fewer than 2 tokens warn and are ignored.
- A line whose first token is empty warns and is ignored.
- `CATEGORY` is compared using `Config.StringComparison`: ordinal case-insensitive when `IgnoreCase=YES`, ordinal case-sensitive when `IgnoreCase=NO`.
- Each `keyN` is `Trim()`ed and added to a set.

Recognized categories:

- `GLOBAL_MAPS`, `SAVE_MAPS`, `STATIC_MAPS`
- `GLOBAL_XMLS`, `SAVE_XMLS`, `STATIC_XMLS`
- `GLOBAL_DTS`,  `SAVE_DTS`,  `STATIC_DTS`

Important: key matching is case-sensitive.

- The key sets are stored in normal `HashSet<string>` and are checked by exact string equality.
- The runtime dictionaries (`DataStringMaps` / `DataXmlDocument` / `DataDataTables`) also use case-sensitive keys by default.

### 8.3 Runtime effects (what is cleared, loaded, and saved)

Clearing boundaries (engine-accurate):

- Normal reset (`ResetData()`): clears only the **save-slot partition** keys.
- Global reset (`ResetGlobalData()`): clears the **global-save partition** keys and the **static partition** keys.
- Normal slot load (`LoadFrom(...)`): clears only the **save-slot partition** keys before reading the save file.
- Global load (`LoadGlobal()`): clears only the **global-save partition** keys before reading the global save file (static keys remain).

Save/load boundaries (binary save mode, engine-accurate):

- Normal save slots write only keys in `SAVE_*` sets.
- Global save writes only keys in `GLOBAL_*` sets.
- Static keys are never written to save files in this codebase.
- When reading, the engine accepts `Map`/`Xml`/`DT` records only if the key belongs to either a `SAVE_*` or a `GLOBAL_*` set (static keys are ignored at load time).
