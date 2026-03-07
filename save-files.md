# Save System and On-Disk Formats (engine-accurate)

This document specifies Emuera’s save/load mechanism at two levels:

1) **Script-visible behavior and persistence partitions** (what is saved where).
2) **On-disk file formats** for the engine’s save files (byte/field-level).

It is written for the Emuera engine in this workspace (EvilMask/Emuera) and aims to be reimplementable.

Cross-refs to engine code are optional and only for fact-check.

## 1) Directories and filenames

### 1.1 Base directories

In this codebase, the engine’s base directory (sometimes called `ExeDir`) contains these important subfolders:

- `csv/` — CSV data
- `erb/` — ERB scripts
- `dat/` — auxiliary binary save files for `SAVEVAR/SAVECHARA`
- `sav/` — optional folder for normal save slots / global save (config-dependent)

### 1.2 `SavDir` (where `save*.sav` and `global.sav` live)

The engine computes `SavDir` from config:

- If `UseSaveFolder=YES`: `SavDir = <ExeDir>/sav/`
- If `UseSaveFolder=NO`:  `SavDir = <ExeDir>/`

If `UseSaveFolder=YES` and `<ExeDir>/sav/` does not exist, the engine may create it and (optionally) move existing `save*.sav` and `global.sav` from `<ExeDir>/` into it (user-prompted in the UI).

### 1.3 Normal save slots (`.sav`)

- Global save file: `SavDir/global.sav`
- Normal slot save files: `SavDir/save{N}.sav`

The engine uses the formatting pattern `save{index:00}.sav`:

- `0` → `save00.sav`
- `7` → `save07.sav`
- `42` → `save42.sav`
- `100` → `save100.sav` (the `:00` means “at least two digits”, not “exactly two digits”)

### 1.4 `SAVEVAR/LOADVAR` and `SAVECHARA/LOADCHARA` (`.dat`)

These instructions store files under the `dat/` folder (not `SavDir`):

- Variable bundle: `dat/var_{name}.dat`
- Character bundle: `dat/chara_{name}.dat`

The `name` part must be non-empty and must not contain any OS-invalid filename characters (engine uses `Path.GetInvalidFileNameChars()`).

In this codebase, some call sites format the `{name}` portion from an integer slot/index using the numeric formatting pattern `{index:00}` (two digits minimum), producing filenames like `var_00.dat` and `chara_07.dat`.

The engine also provides an enumeration helper that lists `dat/var_*.dat` or `dat/chara_*.dat` with a wildcard pattern and extracts the `{name}` portion by stripping the prefix and the `.dat` extension.

## 2) Persistence partitions (what gets saved where)

This engine’s persistence model is not “everything is always saved”. Instead, variables are partitioned into multiple buckets, and different save/load actions touch different buckets.

The declaration keywords `SAVEDATA`, `GLOBAL`, and `CHARADATA` (for user-defined variables) participate in this partitioning; see `variables.md` for the storage model and reset boundaries.

At a high level:

- **Normal save slot** (`saveN.sav`, via `SAVEDATA/LOADDATA` and the save UI):
  - saves all characters plus “normal savedata” variables
  - does not persist `GLOBAL/GLOBALS` unless explicitly included by separate global-save logic
- **Global save** (`global.sav`, via `SAVEGLOBAL/LOADGLOBAL`):
  - saves only the engine’s global buckets (not normal savedata)
- **Variable bundle** (`var_{name}.dat`, via `SAVEVAR/LOADVAR`):
  - (not implemented in this engine build) would save only the explicitly named variables (a curated list chosen by the script)
- **Character bundle** (`chara_{name}.dat`, via `SAVECHARA/LOADCHARA`):
  - saves only the explicitly selected characters

### 2.1 Save summary text (“saveText” / `SAVEDATA_TEXT`)

Both the binary and legacy text formats contain a single string field that acts as the save slot’s **summary text** (shown in save/load UIs and also exposed to scripts via various built-ins).

In this codebase, the engine produces that text through two main paths:

- `SAVEDATA <slot>, <text>` writes `<text>` as the summary text for that slot (the engine rejects embedded newlines).
- The save UI flow calls `@SAVEINFO` and uses `PUTFORM` to append printable text into the internal variable `SAVEDATA_TEXT`, then writes `SAVEDATA_TEXT` as the summary text for the selected slot.

### 2.2 Load-time clearing and merge behavior (engine behavior)

Load operations are not all “replace everything”. In this codebase:

- Normal slot load (`LOADDATA` / save UI load) is a full game-state load:
  - the engine resets variables to defaults, clears characters, then loads characters and savedata variables from the file.
  - for EM extension Map/XML/DT, it clears only the normal-slot extension partition before reading new values.
- Global load (`LOADGLOBAL`) loads only the global buckets:
  - it clears only the global-save EM extension partition before reading new values.
- Variable bundle load (`LOADVAR`) would be a **partial overwrite** (but is not implemented in this engine build):
  - it would load only the variables present in the `.dat` file and leave all other variables unchanged.
- Character bundle load (`LOADCHARA`) is an **append**:
  - it loads characters from the `.dat` file and appends them to the current character list (it does not replace existing characters).

Unknown keys in binary variable streams are ignored:

- if a variable name is unknown or not loadable into the current runtime’s variable tables, the engine reads and discards the corresponding value and continues.

### 2.3 EM extension persistence (Map / XML / DataTable)

This codebase has “extension” persistence for non-primitive data types:

- `Map` (string → string dictionary)
- `Xml` (`XmlDocument`)
- `DT` (`DataTable`)

These are stored in separate “key sets” configured by `VarExt*.csv` (see `data-files.md`):

- Normal-slot extension keys: `SAVE_MAPS`, `SAVE_XMLS`, `SAVE_DTS`
- Global-save extension keys: `GLOBAL_MAPS`, `GLOBAL_XMLS`, `GLOBAL_DTS`
- Reset-only extension keys: `STATIC_MAPS`, `STATIC_XMLS`, `STATIC_DTS`

On load/reset, the engine clears only the extension keys belonging to the corresponding partition before reading new values (see `variables.md` for the exact reset/load boundaries).

Important limitation (engine behavior):

- These EM extension values are persisted only via the **binary** save format in this codebase.
- The legacy text save format (`SystemSaveInBinary=NO`) does not serialize Map/XML/DT extension data.

## 3) Binary save format: EraBinaryData v1808

When `SystemSaveInBinary=YES`, normal-slot and global saves are written in the engine’s binary format (“EraBinaryData v1808”).

Regardless of `SystemSaveInBinary`, `SAVECHARA/LOADCHARA` use this binary format in this codebase.

`SAVEVAR/LOADVAR` are declared built-ins but are **not implemented** in this engine build (they throw `NotImplCodeEE` at runtime). The engine still defines a binary file type `Var` and contains internal save/load helpers for variable packs; this document specifies that format for completeness.

### 3.1 File header (magic, version, optional compression)

The file starts with a small header written with .NET `BinaryWriter` and read with `BinaryReader` (little-endian).

Header fields:

1) `u64 magic`:
   - uncompressed: `0x0A1A0A0D41524589`
   - compressed:   `0x0A50495A41524589` (ZipHeader)
2) `u32 formatVersion` = `1808`
3) `u32 dataCount` (currently `0` in this codebase)
4) `u32[dataCount] dataTable` (currently empty)

Payload:

- If `magic` is the uncompressed header, the remainder of the file is the raw payload.
- If `magic` is ZipHeader, the remainder of the file is a **GZip** stream that decompresses to the payload bytes.

When ZipHeader is used:

- It is controlled by `ZipSaveData`, but in this codebase compression is only enabled when **both** `SystemSaveInBinary=YES` and `ZipSaveData=YES`.
  (As a result, `SAVEVAR/SAVECHARA` binary `.dat` files are not compressed unless `SystemSaveInBinary` is also enabled.)

### 3.2 Primitive encodings used in the payload

All fixed-width integers (`Int16/Int32/Int64`, `UInt32/UInt64`) use little-endian byte order (standard .NET behavior).

#### 3.2.1 Strings

Strings are written using .NET `BinaryWriter.Write(string)` with `Encoding.Unicode` (UTF-16LE).

That encoding is **not** “write raw UTF-16 until NUL”. It is the .NET length-prefixed string format:

- a 7-bit encoded integer length prefix (byte count of the UTF-16LE payload), followed by
- the UTF-16LE bytes.

#### 3.2.2 Compressed integer (`m_WriteInt` / `m_ReadInt`)

Many values use a compact integer encoding:

- If `0 <= v <= 207` (`0xCF`), write a single byte equal to `v`.
- Else write a type marker byte, then the value in that width:
  - `0xD0` → Int16
  - `0xD1` → Int32
  - `0xD2` → Int64

### 3.3 Variable records (`EraSaveDataType`) and file types (`EraSaveFileType`)

The payload begins with a file-type byte:

```text
EraSaveFileType (byte)
  0x00 Normal
  0x01 Global
  0x02 Var
  0x03 CharVar
```

Most content is stored as a stream of **variable records**. Each record begins with a 1-byte `EraSaveDataType`:

```text
EraSaveDataType (byte)
  0x00 Int
  0x01 IntArray
  0x02 IntArray2D
  0x03 IntArray3D
  0x10 Str
  0x11 StrArray
  0x12 StrArray2D
  0x13 StrArray3D
  0x20 Map
  0x21 Xml
  0x22 DT
  0xFD Separator
  0xFE EOC
  0xFF EOF
```

Record layouts:

- `Int`:       `type(0x00)` + `key(string)` + `value(m_WriteInt)`
- `Str`:       `type(0x10)` + `key(string)` + `value(string)`
- `IntArray`:  `type(0x01)` + `key(string)` + `value(intArray1D)`
- `StrArray`:  `type(0x11)` + `key(string)` + `value(strArray1D)`
- `IntArray2D`: `type(0x02)` + `key(string)` + `value(intArray2D)`
- `StrArray2D`: `type(0x12)` + `key(string)` + `value(strArray2D)`
- `IntArray3D`: `type(0x03)` + `key(string)` + `value(intArray3D)`
- `StrArray3D`: `type(0x13)` + `key(string)` + `value(strArray3D)`

Extension records:

- `Map`: `type(0x20)` + `key(string)` + `count(i32)` + `count * (k(string), v(string))`
- `Xml`: `type(0x21)` + `key(string)` + `outerXml(string)`
- `DT`:  `type(0x22)` + `key(string)` + `schemaXml(string)` + `dataXml(string)`

Control markers:

- `Separator` (`0xFD`): used inside `CharacterData` records to switch from built-in chara vars to user-defined chara vars.
- `EOC` (`0xFE`): end of a single character record.
- `EOF` (`0xFF`): end of a variable-record stream.

### 3.4 Array encodings (Ebdb tokens)

Arrays are encoded as a length prefix plus a token stream. Tokens are single bytes:

```text
Ebdb tokens (byte)
  0xCF Byte     ; numeric literal where `0 <= value <= 207` (encoded directly as the byte value)
  0xD0 Int16
  0xD1 Int32
  0xD2 Int64
  0xD8 String

  0xE0 EoA1     ; end-of-row (2D) / end-of-row (3D)
  0xE1 EoA2     ; end-of-matrix (3D)

  0xF0 Zero     ; run of empty elements (0 or empty string)
  0xF1 ZeroA1   ; run of empty rows (2D) / empty rows inside a matrix (3D)
  0xF2 ZeroA2   ; run of empty matrices (3D)

  0xFF EoD      ; end-of-array data
```

Notes:

- “Empty” means `0` for integer arrays; and `null/""` for string arrays.
- The engine’s reader tolerates size mismatches:
  - if the saved array is larger than the in-memory array, the engine reads safely and copies only the overlap region;
  - if the saved array is smaller, missing elements are initialized to `0` / `null` (when overwriting is enabled).

#### 3.4.1 `intArray1D` (for `IntArray`)

```text
len0(i32)
tokenStream...
EoD(0xFF)
```

Token stream:

- `Zero(0xF0)` + `count(m_WriteInt)`: write `count` consecutive zeros.
- Otherwise, a single element value:
  - `b` where `0x00 <= b <= 0xCF` → value `b`
  - `Int16(0xD0)` + `i16`
  - `Int32(0xD1)` + `i32`
  - `Int64(0xD2)` + `i64`

#### 3.4.2 `strArray1D` (for `StrArray`)

```text
len0(i32)
tokenStream...
EoD(0xFF)
```

Token stream:

- `Zero(0xF0)` + `count(m_WriteInt)`: write `count` consecutive empty entries (`null` in memory).
- `String(0xD8)` + `s(string)`: write one non-empty entry.

#### 3.4.3 `intArray2D` / `strArray2D`

```text
len0(i32)
len1(i32)
tokenStream...
EoD(0xFF)
```

Token stream (row-major order):

- `ZeroA1(0xF1)` + `count(m_WriteInt)`: `count` consecutive **all-empty rows**.
- `EoA1(0xE0)`: end of current row (remaining entries in the row are implicitly empty).
- `Zero(0xF0)` + `count(m_WriteInt)`: `count` consecutive empty entries within the current row.
- For `intArray2D`: a numeric value token (as in 1D).
- For `strArray2D`: `String(0xD8)` + `s(string)`.

#### 3.4.4 `intArray3D` / `strArray3D`

```text
len0(i32)
len1(i32)
len2(i32)
tokenStream...
EoD(0xFF)
```

Token stream (x-major, then y, then z):

- `ZeroA2(0xF2)` + `count(m_WriteInt)`: `count` consecutive **all-empty matrices** along the x dimension.
- `EoA2(0xE1)`: end of current matrix (remaining rows are implicitly empty).
- `ZeroA1(0xF1)` + `count(m_WriteInt)`: `count` consecutive **all-empty rows** inside the current matrix.
- `EoA1(0xE0)`: end of current row (remaining z entries are implicitly empty).
- `Zero(0xF0)` + `count(m_WriteInt)`: `count` consecutive empty entries within the current row.
- For `intArray3D`: a numeric value token (as in 1D).
- For `strArray3D`: `String(0xD8)` + `s(string)`.

### 3.5 Payload layout by `EraSaveFileType`

After the file-type byte, all file types share this common prefix:

```text
scriptUniqueCode(i64)
scriptVersion(i64)
saveText(string)  ; may be ""
```

Then the remainder depends on `EraSaveFileType`.

#### 3.5.1 `Normal` (`saveN.sav`)

```text
Normal
uniqueCode, version, saveText
charaCount(i64)
charaCount * CharacterDataBinary
NonCharaVariablesBinary
EOF
OptionalEmExtensionVariablesBinary
EOF
```

`CharacterDataBinary` is a variable-record stream terminated by `EOC`, with an optional `Separator` splitting built-in chara vars and user-defined chara vars.

`NonCharaVariablesBinary` is a variable-record stream terminated by `EOF`.

In this codebase, an additional “EM extension” variable-record stream may follow (Map/XML/DT partition keys) and is also terminated by `EOF`.

Which variables are included (engine behavior):

- In `CharacterDataBinary`, the engine writes:
  - built-in character variables whose tokens are marked `IsSavedata=YES`, `IsCharacterData=YES`, `IsGlobal=NO`, and
  - user-defined character variables (`CHARADATA` variables) that are marked `SAVEDATA` (and not `GLOBAL`).
- In `NonCharaVariablesBinary`, the engine writes:
  - built-in non-character variables whose tokens are marked `IsSavedata=YES`, `IsCharacterData=NO`, `IsGlobal=NO`, and
  - user-defined non-global `SAVEDATA` variables (including “scalar” user variables, which are represented as 1D arrays of length 1 in this engine).

#### 3.5.2 `Global` (`global.sav`)

```text
Global
uniqueCode, version, saveText("")
GlobalVariablesBinary
EOF
OptionalEmGlobalExtensionVariablesBinary
EOF
```

Which variables are included (engine behavior):

- `GlobalVariablesBinary` includes built-in variables whose tokens are marked `IsSavedata=YES`, `IsCharacterData=NO`, `IsGlobal=YES`, plus user-defined ERH variables that are both `GLOBAL` and `SAVEDATA`.

#### 3.5.3 `Var` (`dat/var_{name}.dat`)

```text
Var
uniqueCode, version, saveText(user-provided)
SelectedVariablesBinary
EOF
```

This is a curated variable-record stream containing only the variables explicitly selected by the `SAVEVAR` call site. Unknown keys are safely skipped during load.

Engine note:

- In this engine build, the `SAVEVAR/LOADVAR` instructions always throw `NotImplCodeEE`, so this file type is not produced/consumed by EraBasic built-ins.

#### 3.5.4 `CharVar` (`dat/chara_{name}.dat`)

```text
CharVar
uniqueCode, version, saveText(user-provided)
charaCount(i64)
charaCount * CharacterDataBinary
EOF
```

## 4) Legacy text save format (EraDataStream)

When `SystemSaveInBinary=NO`, the engine writes `saveN.sav` and `global.sav` using a line-based legacy format. That format remains loadable even when binary saves are enabled, because the loader first checks for a valid EraBinaryData header and otherwise falls back to this text parser.

The loader’s detection rule is:

- If the file begins with a valid EraBinaryData header (magic + version), it is treated as binary.
- Otherwise, the engine dispatches the file to this legacy text parser.

Engine quirk:

- If a file has the EraBinaryData magic but an **unknown binary version**, the binary reader creation fails and the engine still falls back to attempting text parsing instead of rejecting the file at the version check boundary. A compatible reimplementation should mirror that fallback attempt if “bit-for-bit compatibility” with Emuera’s error handling is desired.

### 4.1 Text encoding

- Write: `StreamWriter(..., Config.SaveEncode)` (default UTF-8 with BOM in this codebase).
- Read: `StreamReader(..., DetectEncoding(file))` (BOM-aware / heuristic).

### 4.2 Primitive encodings

- `ReadInt64()` reads one line and parses it as a decimal `Int64`.
- `ReadString()` reads one line as-is; a `null` internal string is written as an empty line.

#### 4.2.1 EraMaker-style arrays

1D arrays are written as a sequence of lines followed by a terminator line:

- terminator line: `__FINISHED`

For integer arrays (`long[]`):

- The writer emits elements with indices `0 <= i < k` up to the last non-zero element (`k` is computed as “last non-zero index + 1”).
- Then it writes `__FINISHED`.
- The reader reads until `__FINISHED`. Missing elements are set to `0`.

For string arrays (`string[]`):

- The writer emits elements up to the last non-empty element (non-null and non-empty).
- Then `__FINISHED`.
- Missing elements are set to `""`.

### 4.3 Normal save slot (`saveN.sav`) text layout

```text
line: scriptUniqueCode (decimal i64)
line: scriptVersion    (decimal i64)
line: saveText         (string; may be empty)
line: charaCount       (decimal i64)
charaCount * CharacterDataText
VariableDataText
__EMUERA_1808_STRAT__
charaCount * CharacterDataExtendedText
VariableDataExtendedText
```

`CharacterDataText` and `VariableDataText` are fixed-count dumps of built-in save variables:

- first: a fixed number of string scalars (1 line each)
- then: a fixed number of integer scalars (1 line each)
- then: a fixed number of integer arrays (EraMaker array blocks)
- then: a fixed number of string arrays (EraMaker array blocks)

The exact counts are engine constants (`__COUNT_SAVE_*` and `__COUNT_SAVE_CHARACTER_*`) and depend on the engine’s variable tables.

### 4.4 Global save (`global.sav`) text layout

```text
line: scriptUniqueCode (decimal i64)
line: scriptVersion    (decimal i64)
GLOBAL(int[])          ; EraMaker array block
GLOBALS(string[])      ; EraMaker array block
__EMUERA_1808_STRAT__
UserDefinedGlobalSavedataExtendedText
```

### 4.5 Emuera “extended” text blocks

After the `__EMUERA_..._STRAT__` marker, the engine uses a key/value extension format separated into sections by:

- section separator line: `__EMU_SEPARATOR__`

There are two families of extended encodings:

#### 4.5.1 Scalar dictionaries

A section consists of zero or more lines:

- `KEY:VALUE`

and ends at the `__EMU_SEPARATOR__` line.

The writer omits “default” values:

- numeric scalars: `0` is omitted
- string scalars: `""` is omitted

#### 4.5.2 Array dictionaries

For 1D arrays:

```text
KEY
valueLine0
valueLine1
...
__FINISHED
```

For 2D integer arrays (`long[,]`):

```text
KEY
row0Csv   ; comma-separated integers, trimmed to last non-zero; empty line = all zeros
row1Csv
...
__FINISHED
```

For 3D integer arrays (`long[,,]`):

```text
KEY
0{
row0Csv
row1Csv
...
}
1{
...
}
__FINISHED
```

String 2D/3D extended arrays are **not supported** by the engine’s legacy text reader in this codebase.

### 4.6 Backward-compatibility notes (text format)

The text reader recognizes multiple Emuera extension markers:

- `__EMUERA_STRAT__`
- `__EMUERA_1708_STRAT__`
- `__EMUERA_1729_STRAT__`
- `__EMUERA_1803_STRAT__`
- `__EMUERA_1808_STRAT__`

and uses the marker to decide which extended sections are present and supported.
