# Emuera Configuration Catalog (language-adjacent)

This document catalogs the config items implemented by this engine (EvilMask/Emuera).
It also defines a small set of shared config-adjacent derived runtime values; those are not config keys and are not accepted by the config loader.
It is part of the self-contained EraBasic reference in `erabasic-reference/`.

Elsewhere in this reference, cite a config item by its canonical config-item name (for example `BackColor`), not by implementation-facing accessor spellings such as `Config.BackColor`.

If you only need the *file formats and load order*, read `data-files.md` first; this document focuses on the *actual keys* and their defaults.

## 1) Key matching rules (what names are accepted)

When reading a `KEY:VALUE` line, the engine uppercases the `KEY` and matches it against known items.

- **Main config** (`default.config`, `emuera.config`, `fixed.config`): matches if `KEY` equals any of:
  - the config code name (implementation detail: `AConfigItem.Name`)
  - the Japanese UI label (`AConfigItem.Text`, uppercased)
  - the English UI label (`AConfigItem.EngText`, uppercased)
- **Debug config** (`debug.config`): matches only by code name or Japanese UI label (English label is *not* accepted by the loader).
- **Replace items** (`_Replace.csv`): matches only by code name or Japanese UI label (English label is *not* accepted by the loader).

Compatibility note: `SaveConfig()` writes config keys as UI labels (JP by default, EN if `EnglishConfigOutput=YES`).
For **debug config**, this creates an engine quirk: if `EnglishConfigOutput=YES`, `debug.config` is saved with English labels but the loader does not recognize them.

## 2) Value parsing rules (recap)

Values are parsed by the item’s declared type:

- `bool`: accepts numeric `0/1`, `YES/NO`, `TRUE/FALSE` (case-insensitive); also accepts Japanese `前/後` for one specific replace key.
- `int` / `long`
- `string`: trimmed. **Exception:** `EditorArgument` is assigned from the raw substring after the first `:` without trimming. Example: `SomeKey:   abc  ` parses as `"abc"`, while `EditorArgument:   /A /B  ` parses as `"   /A /B  "`.
- `char`: must be a single character
- `Color`: `R,G,B` integers (each component satisfies `0 <= component <= 255`)
- enums: parsed by enum name (case-insensitive)
- `List<long>`: `/`-separated integers
- `List<string>`: comma-separated strings (each trimmed)

## 3) Loader quirks that affect parsing/compatibility

- `TextEditor`: because values may contain `:`, the loader re-joins split tokens so the full path survives.
- `EditorArgument`: set directly from the substring after the first `:`; it is not trimmed. (Also: `:` inside the value is not supported by the current loader.)
- `CompatiDRAWLINE`: deprecated key; if present, it is treated as `CompatiLinefeedAs1739` when loading config.
- Analysis mode: when `Program.AnalysisMode` is enabled, `MaxLog` is forced to `10000` during config load.

## 4) High-impact items for a compatible interpreter (selected)

This section calls out config that directly changes script parsing or core runtime semantics.
The full table in this section still lists *all* config items (including UI-only ones).

- `IgnoreCase`: controls the engine's identifier-comparison mode used throughout parsing and runtime lookup.
- `SearchSubdirectory`: controls whether certain file enumerations use recursive search (notably `*.ERH`, `*.ERB`, and `CHARA*.CSV`). Other enumerations may ignore this setting (e.g. `*.erd` and `VarExt*.csv` are always searched recursively in this engine).
- `SortWithFilename`: controls whether file and directory enumeration is lexicographically sorted; this also affects label “first-defined” ordering and event iteration order.
- `SystemAllowFullSpace`: when enabled, the lexer treats full-width space (U+3000) as whitespace in multiple places (notably when skipping whitespace/comments).
- `UseRenameFile`: enables `_Rename.csv` processing (affects `[[...]]` replacement during ERH/ERB line reading).
- `UseReplaceFile`: enables `_Replace.csv` processing for the dedicated replace-item set listed in section 7. That set covers currency/unit presentation, loading/title strings, `DRAWLINE`/`BAR` rendering strings, shop capacity, timeout text, and several runtime default-value tables (`COM_ABLE`, `STAIN`, `EXPLV`, `PALAMLV`, `PBAND`, `RELATION`).
- `ReplaceContinuationBR`: controls the string inserted when joining `{ ... }` continuation lines; the joiner is used after removing all `"` characters from this value.
- `UseERD`: enables ERD-based string-indexing for user-defined variables (`#DIM/#DIMS`).
- `SaveDataNos`: controls the count of normal save slots shown by `SAVEGAME` / `LOADGAME`. Runtime clamps it to `20 <= SaveDataNos <= 80`; the UI still paginates in fixed pages of 20.
- `MaxShopItem`: controls the default SHOP buy-range upper bound (`0 <= x < MaxShopItem`).
- `VarsizeDimConfig`: changes the `VARSIZE(var, dim)` dimension numbering (the engine decrements `dim` by 1 when enabled and `dim > 0`).
- `SystemNoTarget`: disables the engine’s auto-completion of omitted character-variable arguments (e.g. defaulting to `TARGET`).
- `SystemIgnoreStringSet`: changes whether string variables may be assigned via `=`; when enabled the engine warns and rejects certain string assignments.
- `CompatiFuncArgOptional` / `CompatiFuncArgAutoConvert`: change user-function argument binding (omitted args and implicit `TOSTR` insertion).
- `CompatiCallEvent`: allows `CALL` on event functions (compat toggle).
- `CompatiErrorLine`: if disabled, the engine exits after load when there were uninterpretable lines; if enabled it continues (important for strict acceptance criteria).
- `SystemIgnoreTripleSymbol`: disables triple-symbol expansion inside formatted strings (`FORM` parsing).
- `useLanguage`: affects byte-length based string operations via `LangManager` (string length/substr semantics depend on chosen legacy code page).

## 5) Main config items (emuera.config + default/fixed layers)

| Code | Type | Default | Config key (JP) | Config key (EN) |
|---|---|---|---|---|
| `IgnoreCase` | `bool` | `true` | `大文字小文字の違いを無視する` | `Ignore case` |
| `UseRenameFile` | `bool` | `false` | `_Rename.csvを利用する` | `Use _Rename.csv file` |
| `UseReplaceFile` | `bool` | `true` | `_Replace.csvを利用する` | `Use _Replace.csv file` |
| `UseMouse` | `bool` | `true` | `マウスを使用する` | `Use mouse` |
| `UseMenu` | `bool` | `true` | `メニューを使用する` | `Show menu` |
| `UseDebugCommand` | `bool` | `false` | `デバッグコマンドを使用する` | `Allow debug commands` |
| `AllowMultipleInstances` | `bool` | `true` | `多重起動を許可する` | `Allow multiple instances` |
| `AutoSave` | `bool` | `true` | `オートセーブを行なう` | `Make autosaves` |
| `UseKeyMacro` | `bool` | `true` | `キーボードマクロを使用する` | `Use keyboard macros` |
| `SizableWindow` | `bool` | `true` | `ウィンドウの高さを可変にする` | `Changeable window height` |
| `TextDrawingMode` | `TextDrawingMode` | `TextDrawingMode.TEXTRENDERER` | `描画インターフェース` | `Drawing interface` |
| `WindowX` | `int` | `760` | `ウィンドウ幅` | `Window width` |
| `WindowY` | `int` | `480` | `ウィンドウ高さ` | `Window height` |
| `WindowPosX` | `int` | `0` | `ウィンドウ位置X` | `Window X position` |
| `WindowPosY` | `int` | `0` | `ウィンドウ位置Y` | `Window Y position` |
| `SetWindowPos` | `bool` | `false` | `起動時のウィンドウ位置を指定する` | `Fixed window starting position` |
| `WindowMaximixed` | `bool` | `false` | `起動時にウィンドウを最大化する` | `Maximize window on startup` |
| `MaxLog` | `int` | `5000` | `履歴ログの行数` | `Max history log lines` |
| `PrintCPerLine` | `int` | `3` | `PRINTCを並べる数` | `Items per line for PRINTC` |
| `PrintCLength` | `int` | `25` | `PRINTCの文字数` | `Number of Item characters for PRINTC` |
| `FontName` | `string` | `"ＭＳ ゴシック"` | `フォント名` | `Font name` |
| `FontSize` | `int` | `18` | `フォントサイズ` | `Font size` |
| `LineHeight` | `int` | `19` | `一行の高さ` | `Line height` |
| `ForeColor` | `Color` | `192,192,192` | `文字色` | `Text color` |
| `BackColor` | `Color` | `0,0,0` | `背景色` | `Background color` |
| `FocusColor` | `Color` | `255,255,0` | `選択中文字色` | `Highlight color` |
| `LogColor` | `Color` | `192,192,192` | `履歴文字色` | `History log color` |
| `FPS` | `int` | `5` | `フレーム毎秒` | `FPS` |
| `SkipFrame` | `int` | `3` | `最大スキップフレーム数` | `Skip frames` |
| `ScrollHeight` | `int` | `1` | `スクロール行数` | `Lines per scroll` |
| `InfiniteLoopAlertTime` | `int` | `5000` | `無限ループ警告までのミリ秒数` | `Milliseconds for infinite loop warning` |
| `DisplayWarningLevel` | `int` | `1` | `表示する最低警告レベル` | `Minimum warning level` |
| `DisplayReport` | `bool` | `false` | `ロード時にレポートを表示する` | `Display loading report` |
| `ReduceArgumentOnLoad` | `ReduceArgumentOnLoadFlag` | `ReduceArgumentOnLoadFlag.NO` | `ロード時に引数を解析する` | `Reduce argument on load` |
| `IgnoreUncalledFunction` | `bool` | `true` | `呼び出されなかった関数を無視する` | `Ignore uncalled functions` |
| `FunctionNotFoundWarning` | `DisplayWarningFlag` | `DisplayWarningFlag.IGNORE` | `関数が見つからない警告の扱い` | `Function is not found warning` |
| `FunctionNotCalledWarning` | `DisplayWarningFlag` | `DisplayWarningFlag.IGNORE` | `関数が呼び出されなかった警告の扱い` | `Function not called warning` |
| `ChangeMasterNameIfDebug` | `bool` | `true` | `デバッグコマンドを使用した時にMASTERの名前を変更する` | `Change MASTER mame in debug` |
| `ButtonWrap` | `bool` | `false` | `ボタンの途中で行を折りかえさない` | `Button wrapping` |
| `SearchSubdirectory` | `bool` | `false` | `サブディレクトリを検索する` | `Search subfolders` |
| `SortWithFilename` | `bool` | `false` | `読み込み順をファイル名順にソートする` | `Sort filenames` |
| `LastKey` | `long` | `0` | `最終更新コード` | `Latest identify code` |
| `SaveDataNos` | `int` | `20` | `表示するセーブデータ数` | `Save data count per page` |
| `WarnBackCompatibility` | `bool` | `true` | `eramaker互換性に関する警告を表示する` | `Eramaker compatibility warning` |
| `AllowFunctionOverloading` | `bool` | `true` | `システム関数の上書きを許可する` | `Allow overriding system functions` |
| `WarnFunctionOverloading` | `bool` | `true` | `システム関数が上書きされたとき警告を表示する` | `System function override warning` |
| `TextEditor` | `string` | `"notepad"` | `関連づけるテキストエディタ` | `Text editor` |
| `EditorType` | `TextEditorType` | `TextEditorType.USER_SETTING` | `テキストエディタコマンドライン指定` | `Text editor command line setting` |
| `EditorArgument` | `string` | `""` | `エディタに渡す行指定引数` | `Text editor command line arguments` |
| `WarnNormalFunctionOverloading` | `bool` | `false` | `同名の非イベント関数が複数定義されたとき警告する` | `Duplicated functions warning` |
| `CompatiErrorLine` | `bool` | `false` | `解釈不可能な行があっても実行する` | `Execute error lines` |
| `CompatiCALLNAME` | `bool` | `false` | `CALLNAMEが空文字列の時にNAMEを代入する` | `Use NAME if CALLNAME is empty` |
| `UseSaveFolder` | `bool` | `false` | `セーブデータをsavフォルダ内に作成する` | `Use sav folder` |
| `CompatiRAND` | `bool` | `false` | `擬似変数RANDの仕様をeramakerに合わせる` | `Imitate behavior for RAND` |
| `CompatiDRAWLINE` | `bool` | `false` | `DRAWLINEを常に新しい行で行う` | `Always start DRAWLINE in a new line` |
| `CompatiFunctionNoignoreCase` | `bool` | `false` | `関数・属性については大文字小文字を無視しない` | `Do not ignore case for functions and attributes` |
| `SystemAllowFullSpace` | `bool` | `true` | `全角スペースをホワイトスペースに含める` | `Whitespace includes full-width space` |
| `CompatiLinefeedAs1739` | `bool` | `false` | `ver1739以前の非ボタン折り返しを再現する` | `Reproduce wrapping behavior like in pre ver1739` |
| `useLanguage` | `UseLanguage` | `UseLanguage.JAPANESE` | `内部で使用する東アジア言語` | `Default ANSI encoding` |
| `AllowLongInputByMouse` | `bool` | `false` | `ONEINPUT系命令でマウスによる2文字以上の入力を許可する` | `Allow long input by mouse for ONEINPUT` |
| `CompatiCallEvent` | `bool` | `false` | `イベント関数のCALLを許可する` | `Allow CALL on event functions` |
| `CompatiSPChara` | `bool` | `false` | `SPキャラを使用する` | `Allow SP characters` |
| `SystemSaveInBinary` | `bool` | `false` | `セーブデータをバイナリ形式で保存する` | `Use the binary format for saving data` |
| `CompatiFuncArgOptional` | `bool` | `false` | `ユーザー関数の全ての引数の省略を許可する` | `Allow arguments omission for user functions` |
| `CompatiFuncArgAutoConvert` | `bool` | `false` | `ユーザー関数の引数に自動的にTOSTRを補完する` | `Auto TOSTR conversion for user function arguments` |
| `SystemIgnoreTripleSymbol` | `bool` | `false` | `FORM中の三連記号を展開しない` | `Do not process triple symbols inside FORM` |
| `TimesNotRigorousCalculation` | `bool` | `false` | `TIMESの計算をeramakerにあわせる` | `Imitate behavior for TIMES` |
| `SystemNoTarget` | `bool` | `false` | `キャラクタ変数の引数を補完しない` | `Do not auto-complete arguments for character variables` |
| `SystemIgnoreStringSet` | `bool` | `false` | `文字列変数の代入に文字列式を強制する` | `String variable assignment on valid with string expression` |
| `ForbidUpdateCheck` | `bool` | `false` | `UPDATECHECKを許可しない` | `Disallow UPDATECHECK` |
| `UseERD` | `bool` | `true` | `ERD機能を利用する` | `Use ERD` |
| `VarsizeDimConfig` | `bool` | `false` | `VARSIZEの次元指定をERD機能に合わせる` | `Imitate ERD to VARSIZE dimension specification` |
| `CheckDuplicateIdentifier` | `bool` | `false` | `ERDで定義した識別子とローカル変数の重複を確認する` | `Check duplicate ERD identifier and private variablea` |
| `ReplaceContinuationBR` | `string` | `"\" \""` | `行連結の改行コードの置換文字列` | `String of replacing new line code inside continuation` |
| `ValidExtension` | `List<string>` | `["txt"]` | `LOADTEXTとSAVETEXTで使える拡張子` | `Valid extensions for LOADTEXT and SAVETEXT` |
| `ZipSaveData` | `bool` | `false` | `セーブデータを圧縮して保存する` | `Compress save data` |
| `EnglishConfigOutput` | `bool` | `false` | `CONFIGファイルの内容を英語で保存する` | `Output English items in the config file` |
| `EmueraLang` | `string` | `""` | `Emueraの表示言語` | `Emuera interface language` |
| `EmueraIcon` | `string` | `""` | `Emueraのアイコンのパス` | `Path to a custom window icon` |
| `CBUseClipboard` | `bool` | `false` | `表示したテキストをクリップボードにコピーする` | `Clipboard- Copy text to Clipboard during Game` |
| `CBIgnoreTags` | `bool` | `false` | `テキスト中の<>タグを無視する` | `Clipboard- ignore <> tags in text` |
| `CBReplaceTags` | `string` | `"."` | `<>を次の文で置き換える` | `Clipboard- Replace <> with this` |
| `CBNewLinesOnly` | `bool` | `true` | `新しい行のみコピーする` | `Clipboard- Show new lines only` |
| `CBClearBuffer` | `bool` | `false` | `画面のリフレッシュ時にクリップボードとバッファを消去する` | `Clipboard- Clear Buffer when game clears screen` |
| `CBTriggerLeftClick` | `bool` | `true` | `左クリックをトリガーにする` | `Clipboard- LeftClick Trigger` |
| `CBTriggerMiddleClick` | `bool` | `false` | `ホイールクリックをトリガーにする` | `Clipboard- MiddleClick Trigger` |
| `CBTriggerDoubleLeftClick` | `bool` | `false` | `ダブルクリックをトリガーにする` | `Clipboard- Double Left Click Trigger` |
| `CBTriggerAnyKeyWait` | `bool` | `false` | `WAITをトリガーにする` | `Clipboard- AnyKey Wait Trigger ` |
| `CBTriggerInputWait` | `bool` | `true` | `INPUTをトリガーにする` | `Clipboard- Wait for Input Trigger` |
| `CBMaxCB` | `int` | `25` | `クリップボードに貼り付ける行数` | `Clipboard- Length of Clipboard` |
| `CBBufferSize` | `int` | `300` | `総バッファサイズ` | `Clipboard- Buffer Size` |
| `CBScrollCount` | `int` | `5` | `スクロールの行数` | `Clipboard- Scrolled Lines per Key` |
| `CBMinTimer` | `int` | `800` | `クリップボードの更新間隔(ミリ秒)` | `Clipboard- min time between pastes` |
| `RikaiEnabled` | `bool` | `false` | `Rikaichanを使用する` | `Rikai- Enabled` |
| `RikaiFilename` | `string` | `"Emuera-Rikai-edict.txt-eucjp"` | `Rikaichanのファイルパス` | `Rikai- Dictionary Filename` |
| `RikaiColorBack` | `Color` | `0,0,139` | `ポップアップの背景色` | `Rikai- Back Color` |
| `RikaiColorText` | `Color` | `255,255,255` | `ポップアップの文字色` | `Rikai- Text Color` |
| `RikaiUseSeparateBoxes` | `bool` | `true` | `翻訳中の語句を強調表示する` | `Rikai- Use Separate Boxes` |
| `Ctrl_Z_Enabled` | `bool` | `false` | `Ctrl-Zで元に戻す機能を有効にする` | `Enable undo with ctrl-z` |

## 6) Debug config items (debug.config)

| Code | Type | Default | Config key (JP) | Config key (EN) |
|---|---|---|---|---|
| `DebugShowWindow` | `bool` | `true` | `起動時にデバッグウインドウを表示する` | `Show debug window on startup` |
| `DebugWindowTopMost` | `bool` | `true` | `デバッグウインドウを最前面に表示する` | `Debug window always on top` |
| `DebugWindowWidth` | `int` | `400` | `デバッグウィンドウ幅` | `Debug window width` |
| `DebugWindowHeight` | `int` | `300` | `デバッグウィンドウ高さ` | `Debug window height` |
| `DebugSetWindowPos` | `bool` | `false` | `デバッグウィンドウ位置を指定する` | `Fixed debug window starting position` |
| `DebugWindowPosX` | `int` | `0` | `デバッグウィンドウ位置X` | `Debug window X position` |
| `DebugWindowPosY` | `int` | `0` | `デバッグウィンドウ位置Y` | `Debug window Y position` |

## 7) Replace items (`csv/_Replace.csv`)

| Code | Type | Default | Config key (JP) | Config key (EN) |
|---|---|---|---|---|
| `MoneyLabel` | `string` | `"$"` | `お金の単位` | `Currency symbol` |
| `MoneyFirst` | `bool` | `true` | `単位の位置` | `Currency symbol position` |
| `LoadLabel` | `string` | `"Now Loading..."` | `起動時簡略表示` | `Loading message` |
| `MaxShopItem` | `int` | `100` | `販売アイテム数` | `Max shop item storage` |
| `DrawLineString` | `string` | `"-"` | `DRAWLINE文字` | `DRAWLINE character` |
| `BarChar1` | `char` | `'*'` | `BAR文字1` | `BAR character 1` |
| `BarChar2` | `char` | `'.'` | `BAR文字2` | `BAR character 2` |
| `TitleMenuString0` | `string` | `"最初からはじめる"` | `システムメニュー0` | `System menu 0` |
| `TitleMenuString1` | `string` | `"ロードしてはじめる"` | `システムメニュー1` | `System menu 1` |
| `ComAbleDefault` | `int` | `1` | `COM_ABLE初期値` | `Default COM_ABLE` |
| `StainDefault` | `List<long>` | `[0, 0, 2, 1, 8]` | `汚れの初期値` | `Default Stain` |
| `TimeupLabel` | `string` | `"時間切れ"` | `時間切れ表示` | `Time up message` |
| `ExpLvDef` | `List<long>` | `[0, 1, 4, 20, 50, 200]` | `EXPLVの初期値` | `Default EXPLV` |
| `PalamLvDef` | `List<long>` | `[0, 100, 500, 3000, 10000, 30000, 60000, 100000, 150000, 250000]` | `PALAMLVの初期値` | `Default PALAMLV` |
| `pbandDef` | `long` | `4` | `PBANDの初期値` | `Default PBAND` |
| `RelationDef` | `long` | `0` | `RELATIONの初期値` | `Default RELATION` |

## 8) Shared derived runtime values (config-adjacent, not config keys)

These entries are **not** config items:

- they have no standalone config default,
- the config loader does not accept them as keys,
- and other spec-facing docs should cite them as derived runtime values rather than as config items.

| Canonical spec term | Inputs | Implementation names |
|---|---|---|
| `shape position shift` | `TextDrawingMode`, `FontSize` | `DrawingParam_ShapePositionShift` |
| `drawable width` | `WindowX`, `shape position shift` | `DrawableWidth`, `Config.DrawableWidth` |

### 8.1 Shape position shift

- Kind: derived runtime value (not a config item; not accepted by the config loader).
- Definition:
  - The engine first rewrites unsupported config item `TextDrawingMode = WINAPI` to `TEXTRENDERER`.
  - Then `shape position shift = max(2, FontSize / 6)`, using integer division for `FontSize / 6`.
- Observable role:
  - This offset is subtracted from config item `WindowX` to compute the derived runtime value `drawable width`.
- Implementation mapping:
  - implementation property `DrawingParam_ShapePositionShift`.

### 8.2 Drawable width

- Kind: derived runtime value (not a config item; not accepted by the config loader).
- Definition:
  - `drawable width = WindowX - shape position shift`.
- Observable role:
  - This is the default row-width budget used by ordinary console wrapping/alignment and by width-fitted line helpers such as `DRAWLINE`, `CUSTOMDRAWLINE`, `DRAWLINEFORM`, and `GETLINESTR`.
- Implementation mapping:
  - implementation property `DrawableWidth`.
  - Some code paths expose the same value through implementation-facing accessor spelling `Config.DrawableWidth`; that accessor name is not a config item.
