# Plugins (EvilMask / Emuera)

This document specifies the **observable compatibility contract** of the plugin system used by this engine build.
Its goal is to let a reader reimplement compatible plugin loading and `CALLSHARP` interop **without needing to read engine source code**.

## Scope

This document specifies:

- how plugin DLLs are discovered and when they are loaded,
- when startup is blocked by the `pluginsAware.txt` security gate,
- the required public contract types that a loadable plugin must provide,
- how plugin methods are registered and looked up, and
- how `CALLSHARP` passes values to plugins and writes values back.

This document specifies the public helper surface exposed through `PluginManager` / `PluginAPICharContext` to the level needed for compatible reimplementation of the plugin API.
Where a helper delegates to another already-specified subsystem (for example button behavior, variable indexing, or HTML output), this document references that existing contract rather than restating the entire subsystem here.

## Runtime root and plugin paths

All plugin-system paths in this document are resolved relative to the game's **runtime root**.
This is the same root that contains `erb/`, `csv/`, `dat/`, `resources/`, and other game folders.
In packaged builds that route game data through a `Data/` subdirectory, or in launches that explicitly choose a different game root, this runtime root can differ from the OS-level executable directory.

Plugin-related paths are:

- `Plugins/` — optional plugin DLL directory.
- `pluginsAware.txt` — optional acknowledgement file at the runtime root.

## Discovery and load timing

Plugin loading happens during engine initialization **before ERH and ERB are loaded**.

Discovery rules:

1. If the runtime root does **not** contain a `Plugins/` directory, plugin loading is skipped entirely.
2. Otherwise, the engine enumerates files matching `Plugins/*.dll`.
3. Enumeration is **top-level only**; the engine does **not** recurse into subdirectories under `Plugins/`.
4. Enumeration order is **not specified** by the language contract; do not rely on any particular order when multiple plugin DLLs are present.

Compatibility notes:

- The engine clears its plugin-method registry before loading the current contents of `Plugins/`.
- A reimplementation should treat plugin loading as part of startup, not as a late or on-demand feature.

## Security gate: `pluginsAware.txt`

The plugin system includes a startup security gate.

- A DLL under `Plugins/` only triggers this gate if it actually contains a type named `PluginManifest`.
- If such a DLL is found and `pluginsAware.txt` is **missing** from the runtime root, startup aborts with an error.
- DLLs that do **not** contain a `PluginManifest` type are ignored and do **not** by themselves trigger the gate.

Practical consequence:

- A loadable managed DLL under `Plugins/` that does not expose a `PluginManifest` type is ignored as a plugin.
- This does **not** mean every arbitrary file in `Plugins/` is harmless: DLL load failures, type-enumeration failures, or missing managed dependencies can abort startup before the loader reaches the “ignore” case.
- Shipping one or more actual plugins requires `pluginsAware.txt`.

## Required public contract types

The following source-level definitions are part of the **public plugin contract**.
A source-compatible plugin should be implementable against these definitions.

### `IPluginMethod`

```csharp
namespace MinorShift.Emuera.Runtime.Utils.PluginSystem
{
    public interface IPluginMethod
    {
        public abstract string Name { get; }
        public abstract string Description { get; }
        public abstract void Execute(PluginMethodParameter[] args);
    }
}
```

Contract notes:

- `Name` is the dispatch key used by `CALLSHARP`.
- `Description` is informational; it does not affect dispatch.
- `Execute(...)` is invoked synchronously when the plugin method is called.

### `PluginManifestAbstract`

```csharp
namespace MinorShift.Emuera.Runtime.Utils.PluginSystem
{
    public abstract class PluginManifestAbstract
    {
        public abstract string PluginName { get; }
        public abstract string PluginDescription { get; }
        public abstract string PluginVersion { get; }
        public abstract string PluginAuthor { get; }

        public List<IPluginMethod> GetPluginMethods() => methods;
        protected List<IPluginMethod> methods = [];
    }
}
```

Contract notes:

- A plugin manifest exposes its ERB-callable methods by populating `methods`.
- Registration order follows the list order returned by `GetPluginMethods()`.

### `PluginMethodParameter`

```csharp
namespace MinorShift.Emuera.Runtime.Utils.PluginSystem
{
    public class PluginMethodParameter
    {
        public bool isString;
        public string strValue;
        public long intValue;

        public PluginMethodParameter(string initialValue) { isString = true; strValue = initialValue; }
        public PluginMethodParameter(long initialValue) { isString = false; intValue = initialValue; }
    }
}
```

Contract notes:

- `isString` records whether the incoming ERB argument was converted as a string or an integer.
- The plugin may mutate `strValue` and/or `intValue` before returning.
- The engine does **not** automatically keep the two value fields in sync for you.

## Plugin manifest discovery and admission rules

For each discovered `Plugins/*.dll` file, the engine applies these rules:

1. Load the DLL as a .NET assembly.
2. Search that assembly's defined types for a type whose **type name** is exactly `PluginManifest`.
   - Namespace does not matter.
3. If no such type exists, ignore that DLL and continue.
4. If such a type exists, require `pluginsAware.txt` at the runtime root.
5. Instantiate the `PluginManifest` type using a **parameterless constructor**.
6. Treat the resulting object as `PluginManifestAbstract`.
7. Obtain its `IPluginMethod` list via `GetPluginMethods()`.
8. Register each method into the global plugin-method registry.

Important edge cases:

- If a DLL contains **multiple** types named `PluginManifest`, the chosen one is not a stable compatibility guarantee; provide exactly one.
- If the selected `PluginManifest` type cannot be constructed with no arguments, startup fails.
- If manifest construction itself throws an exception, startup fails.
- If the selected `PluginManifest` type does not actually satisfy the `PluginManifestAbstract` contract, startup fails.
- If DLL loading or type enumeration fails, startup fails.

## Method registration and lookup

Methods are registered globally by their `Name`.

Lookup case-sensitivity follows config item `IgnoreCase`:

- If `IgnoreCase = true`, the registry is case-insensitive.
- Otherwise, method names are matched case-sensitively.

Observable consequences:

- In case-insensitive mode, names that differ only by case are treated as the **same** plugin method name.
- If two methods register the same effective name, registration fails and startup aborts.
- Name collisions are global across **all** loaded plugin DLLs, not only within one manifest.
- Leading/trailing spaces are a poor choice for method-name uniqueness, because the ERB-side `CALLSHARP` parser trims the method-name token before lookup.

## ERB interop: `CALLSHARP`

`CALLSHARP` is the ERB-side entry point for invoking registered plugin methods.
See the `CALLSHARP` built-ins entry for source syntax and parser details.
This section focuses only on the plugin-facing execution contract.

### Method selection

- `CALLSHARP` selects a registered plugin method by name.
- If the method name does not resolve during load/validation, the engine emits a warning.
- Executing a `CALLSHARP` line whose target method was not successfully bound results in runtime failure.

### Argument conversion

Before the plugin method is invoked, each ERB argument is converted into one `PluginMethodParameter`:

- If the ERB expression is a **string expression**, the plugin receives `new PluginMethodParameter(stringValue)`.
- Otherwise, the plugin receives `new PluginMethodParameter(intValue)`.

Practical consequence:

- Plugins receive only two scalar value shapes from ERB: string or integer.
- ERB-side variable identity is **not** passed directly; what the plugin sees is a temporary parameter object.

### Write-back after `Execute`

After `Execute(...)` returns, the engine performs a write-back step for each original ERB argument position:

- If the original ERB argument was **not** a variable term, nothing is written back.
- If the original ERB argument was a **string variable term**, the engine writes back `args[i].strValue`.
- If the original ERB argument was an **integer variable term**, the engine writes back `args[i].intValue`.

Important compatibility detail:

- Write-back depends on the **ERB variable kind**, not on `args[i].isString`.
- A plugin that wants to behave like a generic `out`/`ref` helper should update **both** `strValue` and `intValue` unless it knows exactly which kind of ERB variable will be passed.

### Plugin exceptions

- If the plugin method throws an exception, the call fails at runtime.
- The engine does not define a plugin-specific recovery layer for `CALLSHARP`; plugin exceptions are not converted into an ERB-level “soft reject” contract.

## Public host helper entry points

Plugins run **in-process** with the engine.
They are not sandboxed by the plugin system.

The main helper entry point is `PluginManager`:

```csharp
public class PluginManager
{
    public static PluginManager GetInstance();

    public void ExecuteLine(string line);
    public void Print(string text);
    public void PrintError(string text);
    public void PrintC(string text, bool aligmentRight = false);
    public void PrintPlain(string text);
    public void PrintPlainWithSingleLine(string text);
    public void PrintSingleLine(string text);
    public void PrintSystemLine(string text);
    public void PrintTemporaryLine(string text);
    public void PrintButton(string text, long id);
    public void PrintButtonC(string text, long id, bool aligmentRight = false);
    public void PrintBar(string text = "", bool isConst = true);
    public void PrintHtml(string htmlText, bool toBuffer = false);
    public void PrintImage(string resourceName, int width, int height, int y, string buttonResourceName = null, string mapResourceName = null);
    public void PrintNewLine();
    public void FlushConsole(bool force = false);
    public void DebugPrint(string text);

    public void ClearDisplay();
    public void SetBgColor(Color color);
    public void SetFont(string fontName);
    public Point GetMousePosition();
    public void WaitInput(bool oneInput = true, int timelimit = -1);
    public void ReadAnyKey();
    public void Await(int time);
    public void ForceStopTimer();
    public void Quit(bool force = false);

    public long[] GetCharacterIDs();
    public long GetIntVar(string name, int index = 0);
    public string GetStrVar(string name, int index = 0);
    public void SetIntVar(string name, long val, int index = 0);
    public void SetStrVar(string name, string val, int index = 0);
    public void SetCharVar(string name, long charId, string key, long value);
    public void SetCharVar(string name, long charId, long key, long value);
    public long GetCharVar(string name, long charId, long key);
    public long GetCharVar(string name, long charId, string key);

    public System.Data.DataTable GetDataTable(string name);
    public static PluginAPICharContext CreateCharContext(long charId);
    public IEnumerable<string> GetStackTrace();

    public void LoadPlugins();
    public IPluginMethod GetMethod(string name);
    public bool HasMethod(string name);
}
```

### `PluginManager` helper behavior

These helper methods operate on the **live runtime state**. They do not expose a detached snapshot.
Each wrapper or helper call reads and writes the current engine state at the time of that call.

`GetInstance()` returns the process-global plugin manager singleton shared by all plugin methods running in the same engine process.

Compatibility-relevant notes:

- `ExecuteLine(string line)` executes one parsed instruction line through the interpreter. It should be treated as a low-level escape hatch, not as a full script runner.
- `GetIntVar` / `GetStrVar` and `SetIntVar` / `SetStrVar` are convenience helpers for one-index global-variable access. They do not by themselves cover arbitrary multidimensional variables, character-data variables, or local stack variables.
- `SetCharVar(name, charId, string key, value)` and `GetCharVar(name, charId, string key)` are not generic string-key accessors for arbitrary character variables. The `key` string is resolved through the host's `CFLAG`-style keyword dictionary, not through arbitrary field-name lookup.
- `CreateCharContext(long charId)` returns a helper object permanently bound to that `charId`; the resulting wrapper methods implicitly prepend that character index on each access.
- Plugin DLL loading depends on normal managed assembly resolution. If a plugin DLL or one of its managed dependencies cannot be loaded or its types cannot be enumerated, startup fails.

### Output and UI helper groups

The output-facing helpers are thin host calls; they do not reparse ERB source unless explicitly stated.

- `Print`, `PrintError`, `PrintC`, `PrintPlain`, `PrintPlainWithSingleLine`, `PrintSingleLine`, `PrintSystemLine`, `PrintTemporaryLine`, `PrintButton`, `PrintButtonC`, `PrintHtml`, `PrintImage`, `PrintNewLine`, `FlushConsole`, and `DebugPrint` write directly to the host console/UI layer.
- `ExecuteLine(string line)` is the main exception: it reparses and executes the supplied ERB instruction line.
- `ClearDisplay()` clears the current display-line collection and related transient display state; it is a destructive screen-clear operation, not merely a print-buffer reset.
- `PrintBar()` with no text argument emits the host's standard separator/bar output. `PrintBar(text, isConst)` with a non-empty `text` emits a custom bar string instead.
- `PrintC(text, alignmentRight)` formats `text` into the host's fixed-width PRINTC-style cell layout before appending it to the print buffer. That cell formatting follows the same hardcoded Shift-JIS byte-count rule as script-side `PRINTC` (code page 932, not derived runtime value `LanguageCodePage`). `PrintButtonC` applies the same cell formatting before appending a button.
- `PrintButton` appends a clickable/button entry with the supplied label and numeric id. `PrintButtonC` differs only by applying that same PRINTC-style cell formatting to the label first. Their button behavior follows the same host button model used by normal script-side button output.
- `Print(text)` appends to the print buffer rather than forcing immediate display. If `text` contains `\n`, the host emits a line break at each split point and continues printing the remaining segments.
- `PrintPlain(text)` appends plain text to the print buffer without the raw-PRINT parser step that ERB `PRINT` uses.
- `PrintPlainWithSingleLine(text)` is an observable API quirk in this build: it routes through a low-level helper that creates a single-line display object, but the plugin-facing wrapper does not insert that returned line into the display list itself. Do not assume it behaves like `PrintSingleLine`.
- `PrintImage(...)` treats `width`, `height`, and `y` as pixel-valued integers when forwarding them to the host image renderer.
- `PrintHtml(htmlText, toBuffer: false)` renders HTML-like content directly into display output. `PrintHtml(htmlText, toBuffer: true)` appends the generated content to the current print buffer instead of immediately emitting standalone display lines. The HTML fragment semantics themselves follow the same HTML-output rules used elsewhere in this reference.
- `PrintSingleLine(text)` flushes the current buffer and emits one standard display line.
- `PrintTemporaryLine(text)` uses the host's temporary-single-line path rather than a persistent standard line.
- `PrintSystemLine(text)` flushes first, disables user-style output, and emits one system-style line. In this build that style-mode switch is stateful until later host/script output re-enables user-style mode.
- `PrintError(text)` flushes first, disables user-style output, and emits one error display line. In debug mode it also mirrors the text to the debug log. Like `PrintSystemLine`, it leaves the host in non-user-style mode until something later re-enables it.
- `FlushConsole(force: false)` flushes the current print buffer if it is non-empty. With `force: true`, it forces a flush even when the print buffer is empty.
- `PrintNewLine()` forces a flush/newline boundary in the host console.
- `SetFont(fontName)` changes the current user-style font name. Passing `null` or an empty string resets the font name to the host default font setting.
- `SetBgColor(color)` requests a host background-color change for the console surface.
- `DebugPrint(text)` writes only to the debug log path and does nothing when debug mode is disabled.

### Input, timing, and process-control helpers

- `WaitInput(oneInput, timelimit)` enters the host's wait-for-input state using an `InputRequest` built from those two values.
  - `oneInput` controls the request's single-input mode.
  - `timelimit > 0` enables the host timer path for that wait request.
- `WaitInput(...)` does **not** configure a typed ERB input mode such as integer/string/button input.
  - In this engine it behaves as a host-side pause/wait request rather than a typed `INPUT*` equivalent.
  - When the wait later completes, the accepted input is echoed to output, but no typed value is dispatched into the script input handlers through this helper alone.
- `ReadAnyKey()` is a misleading name in this engine: the plugin-exposed zero-argument form waits for Enter or a click, not for an arbitrary keyboard key.
- `Await(time)` enters the host sleep/wait state, processes pending UI events, and sleeps for `time` milliseconds when `time > 0`.
- `Quit(force: false)` requests normal host shutdown. `Quit(force: true)` uses the host's force-quit path instead.
- `ForceStopTimer()` stops the host-side input timer mechanism if one is active.
- `GetMousePosition()` returns the current host mouse position in UI coordinates.

### Runtime-data helpers

- `GetCharacterIDs()` returns the current character list as an array of character `NO` values in the host's current character-list order.
- `GetDataTable(name)` returns the live `DataTable` stored under `name`; it does not clone the table before returning it.
- `GetStackTrace()` returns ERB-side call-stack entries as strings in the form `filename:line@label`.
  - The first element is the current executing line.
  - Later elements follow the return-address chain outward.
  - Frames without a source position are skipped.
- `LoadPlugins()` clears the current plugin-method registry and reruns this topic's plugin discovery/admission sequence. It is the host's plugin-loader entry point. In the normal engine startup path, that initialization has already happened before ordinary plugin code runs.
- `GetMethod(name)` and `HasMethod(name)` consult the plugin registry using the same case-sensitivity rules as plugin registration.
  - `HasMethod(name)` is the existence probe.
  - `GetMethod(name)` assumes the method exists; if it does not, the lookup fails rather than returning a sentinel/null object.

### Public wrapper class contracts

The helper API exposes these public wrapper classes:

```csharp
public class GlobalInt1dWrapper
{
    public long this[string key] { get; set; }
    public long this[long key] { get; set; }
    public long Get(string key);
    public long Get(long key);
    public void Set(string key, long value);
    public void Set(long key, long value);
}

public class GlobalString1dWrapper
{
    public string this[string key] { get; set; }
    public string this[long key] { get; set; }
    public string Get(string key);
    public string Get(long key);
    public void Set(string key, string value);
    public void Set(long key, string value);
}

public class GlobalConstString1dWrapper
{
    public string this[string key] { get; }
    public string this[long key] { get; }
    public string Get(string key);
    public string Get(long key);
}

public class GlobalConstInt1dWrapper
{
    public long this[string key] { get; }
    public long this[long key] { get; }
    public long Get(string key);
    public long Get(long key);
}

public class CharInt1dWrapper
{
    public long this[string key] { get; set; }
    public long this[long key] { get; set; }
    public long Get(string key);
    public long Get(long key);
    public void Set(string key, long value);
    public void Set(long key, long value);
}

public class CharInt2dWrapper
{
    public long this[string keyA, string keyB] { get; set; }
    public long this[long keyA, string keyB] { get; set; }
    public long this[string keyA, long keyB] { get; set; }
    public long this[long keyA, long keyB] { get; set; }
    public long Get(string keyA, string keyB);
    public long Get(long keyA, string keyB);
    public long Get(string keyA, long keyB);
    public long Get(long keyA, long keyB);
    public void Set(string keyA, string keyB, long value);
    public void Set(long keyA, string keyB, long value);
    public void Set(string keyA, long keyB, long value);
    public void Set(long keyA, long keyB, long value);
}

public class CharUserdefinedInt1dWrapper
{
    public long this[string key] { get; set; }
    public long this[string key, long idx] { get; set; }
    public long Get(string key, long idx = 0);
    public void Set(string key, long value, long idx = 0);
}

public class CharStringWrapper
{
    public string Get();
    public void Set(string value);
}

public class CharString1dWrapper
{
    public string this[string key] { get; set; }
    public string this[long key] { get; set; }
    public string Get(string key);
    public string Get(long key);
    public void Set(string key, string value);
    public void Set(long key, string value);
}
```

Wrapper semantics:

- `Global*Wrapper` classes address one-dimensional global variables.
- `Char*Wrapper` classes address variables whose first implicit index is the bound `charId` from `PluginAPICharContext`.
- Numeric overloads (`long key`, `long keyA`, `long keyB`) use raw numeric indices.
- String-key overloads on all wrappers except `CharUserdefinedInt1dWrapper` resolve the string through the host's keyword dictionary for that wrapper's variable family, then use the resulting numeric index.
- `CharUserdefinedInt1dWrapper` uses its first string argument as the **user-defined variable name**, not as a name-table subscript. Its optional `idx` is the numeric secondary index, defaulting to `0`.
- For `CharUserdefinedInt1dWrapper`, variable-name matching follows the host's `IgnoreCase` mode.
- `CharStringWrapper` is the scalar-string special case: it has no indexers and simply gets/sets the bound character's single string slot.
- Const wrapper classes expose only getters; there is no public setter surface.
- Failed name lookup, failed string-key resolution, and out-of-range index access are runtime failures; these wrappers do not provide a `TryGet`-style sentinel API.

### Public wrapper-bearing fields

Public variable/helper fields exist on `PluginManager`.
Their exact names are part of the source-level API surface:

- integer wrappers: `DAY`, `MONEY`, `ITEM`, `FLAG`, `TFLAG`, `UP`, `PALAMLV`, `EXPLV`, `EJAC`, `DOWN`, `RESULT`, `COUNT`, `TARGET`, `ASSI`, `MASTER`, `NOITEM`, `LOSEBASE`, `SELECTCOM`, `ASSIPLAY`, `PREVCOM`, `TIME`, `ITEMSALES`, `PLAYER`, `NEXTCOM`, `PBAND`, `BOUGHT`, `GLOBAL`, `RANDDATA`
- string wrappers: `SAVESTR`, `TSTR`, `STR`, `RESULTS`, `GLOBALS`
- const integer wrappers: `NO`, `ITEMPRICE`
- const string wrappers: `ABLNAME`, `TALENTNAME`, `EXPNAME`, `MARKNAME`, `PALAMNAME`, `ITEMNAME`, `TRAINNAME`, `BASENAME`, `SOURCENAME`, `EXNAME`, `EQUIPNAME`, `TEQUIPNAME`, `FLAGNAME`, `TFLAGNAME`, `CFLAGNAME`, `TCVARNAME`, `CSTRNAME`, `STAINNAME`, `CDFLAGNAME1`, `CDFLAGNAME2`, `STRNAME`, `TSTRNAME`, `SAVESTRNAME`, `GLOBALNAME`, `GLOBALSNAME`

Per-character helper access is exposed through `PluginAPICharContext`:

```csharp
public static PluginAPICharContext CreateCharContext(long charId);

public class PluginAPICharContext
{
    public CharUserdefinedInt1dWrapper UserDefined;

    public CharInt1dWrapper BASE;
    public CharInt1dWrapper MAXBASE;
    public CharInt1dWrapper ABL;
    public CharInt1dWrapper TALENT;
    public CharInt1dWrapper EXP;
    public CharInt1dWrapper MARK;
    public CharInt1dWrapper PALAM;
    public CharInt1dWrapper SOURCE;
    public CharInt1dWrapper EX;
    public CharInt1dWrapper CFLAG;
    public CharInt1dWrapper JUEL;
    public CharInt1dWrapper RELATION;
    public CharInt1dWrapper EQUIP;
    public CharInt1dWrapper TEQUIP;
    public CharInt1dWrapper STAIN;
    public CharInt1dWrapper GOTJUEL;
    public CharInt1dWrapper NOWEX;
    public CharInt1dWrapper DOWNBASE;
    public CharInt1dWrapper CUP;
    public CharInt1dWrapper CDOWN;
    public CharInt1dWrapper TCVAR;

    public CharStringWrapper NAME;
    public CharStringWrapper CALLNAME;
    public CharStringWrapper NICKNAME;
    public CharStringWrapper MASTERNAME;

    public CharString1dWrapper CSTR;
    public CharInt2dWrapper CDFLAG;
}
```

Public-surface note:

- Plugins obtain `PluginAPICharContext` instances through `CreateCharContext(long charId)`; construction is not a public plugin-side contract in this build.
- The public skeleton above intentionally omits non-contract setup machinery such as `CacheVariables(...)`.
- Those setup steps are not themselves part of the plugin-facing API contract; only their observable effects matter for compatibility.

Compatibility-relevant quirk:

- `PluginAPICharContext.UserDefined` is populated from the user-defined character-variable set known at plugin setup time. Because plugin setup happens before ERH declarations are loaded, character variables introduced later by ERH may be absent from this helper view.

## Minimal compatible plugin

A minimal loadable plugin must:

- compile to a `.dll`,
- be placed directly under `Plugins/`,
- expose exactly one usable `PluginManifest` type,
- derive that type from `PluginManifestAbstract`,
- provide a parameterless constructor,
- populate `methods` with one or more `IPluginMethod` objects, and
- be accompanied by `pluginsAware.txt` if it will actually be recognized as a plugin.

Minimal example:

```csharp
using MinorShift.Emuera.Runtime.Utils.PluginSystem;

public sealed class PluginManifest : PluginManifestAbstract
{
    public override string PluginName => "ExamplePlugin";
    public override string PluginDescription => "Minimal CALLSHARP demo";
    public override string PluginVersion => "1.0.0";
    public override string PluginAuthor => "Example";

    public PluginManifest()
    {
        methods.Add(new Echo());
    }
}

public sealed class Echo : IPluginMethod
{
    public string Name => "ECHO";
    public string Description => "Echoes arguments";

    public void Execute(PluginMethodParameter[] args)
    {
        var pm = PluginManager.GetInstance();
        foreach (var arg in args)
        {
            pm.Print(arg.isString ? arg.strValue : arg.intValue.ToString());
            pm.PrintNewLine();
        }
    }
}
```

One compatible ERB call site is:

```erb
CALLSHARP ECHO, "hello", 123
```

If you prefer not to depend on helper printing APIs, a plugin can also restrict itself to mutating `args` and returning.

## Compatibility checklist for reimplementation

A compatible reimplementation of this plugin system should, at minimum, preserve these observable behaviors:

- plugin loading happens before ERH/ERB compilation,
- `Plugins/` enumeration is top-level-only and not recursive,
- non-plugin DLLs under `Plugins/` are ignored,
- actual plugins require `pluginsAware.txt`,
- plugin admission is based on a type named exactly `PluginManifest`,
- plugin methods are registered globally by `IPluginMethod.Name`,
- case-sensitivity follows the engine's `IgnoreCase` mode,
- duplicate effective method names abort loading,
- `CALLSHARP` passes string/int scalar values via `PluginMethodParameter`, and
- post-call write-back affects only original ERB variable arguments, using `strValue` for string variables and `intValue` for integer variables.
