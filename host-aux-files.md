# Host Auxiliary Files (`macro.txt`, `debug/*`, `time.log`)

This document records a small set of **host-side auxiliary files** that are observable in this engine build but are not part of ERB syntax itself.

These files matter mainly for compatibility with the shipped UI/runtime shell, not for a minimal headless EraBasic interpreter.

## 1) Runtime roots and directory creation

Relevant host-side paths are:

- `ExeDir/macro.txt`
- `ExeDir/debug/debug.config`
- `ExeDir/debug/watchlist.csv`
- `ExeDir/debug/console.log`
- `ExeDir/time.log`

The engine derives `debug/` as `ExeDir/debug/`.

- During startup, if `debug/` does not exist, the engine tries to create it.
- If that directory creation fails, startup aborts with a host-side error dialog before normal script execution.

## 2) Keyboard macro system (`macro.txt`)

The keyboard macro system is gated by config item `UseKeyMacro`.

### 2.1 Load/save timing

- During process initialization:
  - if config item `UseKeyMacro` is false, the macro file is ignored,
  - if analysis mode is enabled, the macro file is ignored,
  - otherwise, if `ExeDir/macro.txt` exists, it is loaded.
- If config item `DisplayReport` is enabled, loading `macro.txt` also emits the host system line “Loading macro.txt...” (localized through the language pack).
- On main-window close:
  - if config item `UseKeyMacro` is true, the engine calls the macro save path,
  - otherwise it does not save `macro.txt`.

### 2.2 In-memory model

The engine stores:

- 10 macro groups (`0 <= group < 10`)
- 12 function-key slots per group (`F1`..`F12`)

So the total macro slot count is `10 * 12 = 120`.

Each slot stores one string. Empty string means “no macro”.

The engine also stores one display name per group.

### 2.3 Keyboard behavior

When config item `UseKeyMacro` is enabled, the main window intercepts these key combinations:

- `F1`..`F12` with **no modifiers**:
  - replace the current input textbox contents with the stored macro text for the current group and that F-key slot,
  - move the caret to the end,
  - this happens even if the stored macro is empty (the input box becomes empty).
- `Shift+F1`..`Shift+F12`:
  - if the current input textbox is non-empty, store its current text into that slot of the current group,
  - if the input textbox is empty, do nothing.
- `Ctrl+0`..`Ctrl+9`:
  - switch the current macro group,
  - accept both the top-row digit keys and numpad digits,
  - show a temporary on-screen label with the group's display name.

If config item `UseKeyMacro` is disabled, these macro-specific key bindings are not active.

### 2.4 File format

`macro.txt` is a plain text file written line-by-line.

Write order:

1. 10 group-name lines
2. 120 macro-slot lines

Group-name lines use this exact prefix:

- `グループ{digit}:{groupName}`

Examples:

- `グループ0:...`
- `グループ9:...`

Macro-slot lines use the current localized slot-name prefix followed immediately by the macro text payload.

Important compatibility quirk:

- The group-header prefix is hardcoded Japanese `グループ`.
- The macro-slot prefixes are **not** hardcoded:
  - group `0` uses the current localized `MacroKeyF` pattern,
  - groups `1..9` use the current localized `GMacroKeyF` pattern.
- So the parseable `macro.txt` surface depends on the current language resources loaded into the host UI.

Examples of slot prefixes in the English language pack:

- `Macro Key F1:`
- `G2:Macro Key F5:`

Examples of slot prefixes in the default Japanese strings:

- `マクロキーF1:`
- `G2:マクロキーF5:`

### 2.5 Read rules

The load path uses the shared `EraStreamReader` text-file reader, so text decoding follows the normal rules from `data-files.md`.

Per-line behavior:

- empty lines are ignored
- lines whose first character is `;` are ignored
- a line starting with `グループ` can update one group's display name if all of these hold:
  - the line is at least 4 characters past the prefix,
  - the next character after `グループ` is a single digit `0`..`9`,
  - the next character after that digit is `:`
- otherwise, the loader scans all 120 current slot-name prefixes and, on the first `StartsWith(...)` match, stores the line suffix as that macro's text

Compatibility consequences:

- macro-slot parsing depends on the **current** localized slot-name strings, not on a stable machine-format prefix
- UI language changes do **not** all behave the same for macros:
  - if the language is changed through the config dialog, the host reloads language resources and then immediately resets all in-memory macro slot names, macro texts, and group names to the current-language defaults
  - if the language is changed through the main-window language menu, the host reloads language resources but does **not** rebuild the current in-memory macro arrays
- after a later restart under a different UI language, existing `macro.txt` lines using old localized slot prefixes may stop matching
- after a config-dialog language change, if the macro subsystem had already been marked dirty earlier in the same session, the normal close-time save path can overwrite `macro.txt` with the reset/default in-memory macro state
- group-name lines remain parseable across those UI-language changes because their `グループ` prefix is hardcoded

## 3) Debug auxiliary files under `debug/`

### 3.1 `debug/debug.config`

This is the debug-config persistence file for the debug-window config item set.

- Path: `ExeDir/debug/debug.config`
- Save path uses implementation property `Config.Encode`
- Load path uses `EraStreamReader`, so reading follows the normal text-file decode rules from `data-files.md`

The accepted keys and value parsing rules for the debug-config items themselves are already documented in `config-items.md`.

### 3.2 `debug/watchlist.csv`

This file stores the debug window's watched-expression list.

- Path: `ExeDir/debug/watchlist.csv`
- Written when the debug dialog saves its state (including on debug-dialog close)
- Also writable through the debug dialog's explicit “save watch list” action

Format:

- one watched expression per line
- empty watch entries are not written
- there is no CSV quoting/escaping despite the `.csv` extension

Encoding behavior:

- write uses implementation property `Config.Encode`
- read uses `new StreamReader(path, Config.Encode)` directly
- unlike most script/data text files, readback here does **not** use auto-detection

Load behavior:

- if the file does not exist, nothing is loaded
- non-empty lines become watch entries in order
- on read failure, the host shows a debug-window error dialog

### 3.3 `debug/console.log`

This file stores the current debug console text when the debug dialog saves its state.

- Path: `ExeDir/debug/console.log`
- Written on debug-dialog close through the shared debug save path
- It is overwritten, not appended
- Encoding uses implementation property `Config.Encode`

The current implementation does not document a corresponding automatic load path for `debug/console.log`; it is treated as an export/save artifact rather than as persistent session restore input.

## 4) Boot timing log (`time.log`)

Config item `DisplayReport` enables a boot-timing report path.

- Path: `ExeDir/time.log`
- Created/opened during console initialization when config item `DisplayReport` is true
- If the file is locked by another process, the engine emits a warning and continues without timing-log output

Content shape:

- the engine writes timing/status lines such as:
  - `Init:Start`
  - `File:Preload:Start`
  - `File:Preload:End ...ms`
  - `Init:End ...ms`

Encoding/path quirk:

- `time.log` is opened through `new StreamWriter(FileStream)` with no explicit encoding argument
- so it does **not** use implementation property `Config.Encode` or implementation property `Config.SaveEncode`

Overwrite/append quirk:

- the file is opened with `FileMode.OpenOrCreate`
- the writer starts at the beginning of the file
- there is no explicit truncate-before-write step in this path

So a compatible host shell that wants to mimic this behavior exactly should not assume “fresh truncate then write”.
