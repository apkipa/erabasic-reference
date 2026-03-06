# Plugins (EvilMask / Emuera)

This engine supports loading external .NET DLL plugins and exposing their functionality to ERB via the built-in instruction `CALLSHARP`.

## What plugins can (and cannot) extend

- Plugins can register **named methods** that ERB can invoke using `CALLSHARP`.
- Plugins do **not** dynamically add new ERB instruction keywords or new expression-function names to the parser. (The ERB-facing entry point is still the built-in `CALLSHARP` instruction.)

## Discovery and load timing

- On startup, the engine scans the game directory’s `Plugins/` folder and loads all `*.dll` files found there.
- Plugins are loaded during engine initialization, before ERH/ERB compilation begins.

## Security gate: `pluginsAware.txt`

If the game distribution contains any plugin DLLs, the engine requires a `pluginsAware.txt` file at the game root (the executable directory). If it is missing, the engine aborts startup with an error message intended to warn the user about the security implications of running third-party code.

## Plugin manifest and method registration

Each plugin DLL must provide a type named `PluginManifest` (any namespace) that:

- is instantiable via a parameterless constructor, and
- derives from the engine’s `PluginManifestAbstract` base class, and
- populates its `methods` list with objects implementing `IPluginMethod`.

At load time, the engine:

1. Finds the `PluginManifest` type in each DLL.
2. Instantiates it.
3. Collects `IPluginMethod` objects returned by `GetPluginMethods()`.
4. Registers each method by its `Name`.

Method-name case sensitivity follows the engine’s `IgnoreCase` configuration:

- If `IgnoreCase = true`, method lookup is case-insensitive.
- Otherwise, method lookup is case-sensitive.

## Calling a plugin method from ERB: `CALLSHARP`

`CALLSHARP` invokes a registered plugin method by name and passes ERB argument values to it.

- Arguments are evaluated first, and each argument is passed as either a string value or an integer value (depending on whether the ERB expression is a string expression).
- After the plugin method returns, any arguments that were variable terms are written back from the plugin’s corresponding argument slot (out/ref-like behavior).

See the `CALLSHARP` entry in `builtins-reference.md` for the ERB-level contract and edge cases.

## Writing a compatible plugin (C#)

This section describes the minimum contract a plugin DLL must satisfy to be loadable and callable by this engine build.

### Source of truth (API excerpts)

This engine’s plugin API is defined by types inside the engine assembly (namespace `MinorShift.Emuera.Runtime.Utils.PluginSystem`).

The following excerpts are included here so plugin authors can implement against the exact contract without having to dig through engine source:

From `emuera.em/Emuera/Runtime/Utils/PluginSystem/IPluginMethod.cs`:

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

From `emuera.em/Emuera/Runtime/Utils/PluginSystem/BasePluginManifest.cs`:

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

From `emuera.em/Emuera/Runtime/Utils/PluginSystem/PluginMethodParameter.cs`:

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

### Packaging and placement

- Build a `.dll` and place it under the game’s `Plugins/` directory.
- The engine loads `Plugins/*.dll` on startup. If any DLLs are present, `pluginsAware.txt` must exist at the game root (executable directory) or the engine aborts startup (security gate).

### End-to-end minimal example

This is the smallest complete example of a plugin that can be loaded by the engine and invoked from ERB.

**Game folder layout**

```
<GameRoot>/
  Emuera.exe
  pluginsAware.txt
  Plugins/
    ExamplePlugin.dll
```

**Plugin project**

`ExamplePlugin.csproj` (reference the engine assembly and target a compatible framework):

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net10.0-windows</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>disable</Nullable>
  </PropertyGroup>

  <ItemGroup>
    <Reference Include="Emuera">
      <HintPath>path/to/Emuera.exe</HintPath>
    </Reference>
  </ItemGroup>
</Project>
```

`PluginManifest.cs` (the required `PluginManifest` type name):

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
        methods.Add(new AddOne());
    }
}
```

`Echo.cs` (prints all arguments):

```csharp
using MinorShift.Emuera.Runtime.Utils.PluginSystem;

public sealed class Echo : IPluginMethod
{
    public string Name => "ECHO";
    public string Description => "Prints args via PluginManager";

    public void Execute(PluginMethodParameter[] args)
    {
        var pm = PluginManager.GetInstance();
        for (int i = 0; i < args.Length; i++)
        {
            var text = args[i].isString ? args[i].strValue : args[i].intValue.ToString();
            pm.Print(text);
            pm.PrintNewLine();
        }
    }
}
```

`AddOne.cs` (demonstrates write-back: updates `args[0]`):

```csharp
using MinorShift.Emuera.Runtime.Utils.PluginSystem;

public sealed class AddOne : IPluginMethod
{
    public string Name => "ADDONE";
    public string Description => "args[0] += 1 (write-back demo)";

    public void Execute(PluginMethodParameter[] args)
    {
        if (args.Length < 1) return;

        long value;
        if (args[0].isString)
            value = long.Parse(args[0].strValue);
        else
            value = args[0].intValue;

        value += 1;

        // Set both fields so either kind of ERB variable can receive write-back.
        args[0].intValue = value;
        args[0].strValue = value.ToString();
    }
}
```

Build and deploy:

- `dotnet build -c Release`
- Copy the resulting `ExamplePlugin.dll` to `<GameRoot>/Plugins/`.
- Ensure `<GameRoot>/pluginsAware.txt` exists.

**ERB usage**

```erb
#DIM X
#DIMS S
X = 41
S = "41"

CALLSHARP ADDONE, X
CALLSHARP ADDONE, S
CALLSHARP ECHO, "X=", X, " S=", S

PRINTFORMS "X=%d S=%s", X, S
```

### Target framework and architecture

- The plugin must be built for a .NET target compatible with the engine build (this repository’s engine project targets `net10.0-windows`).
- If you distribute separate x86/x64 engine builds, ensure the plugin and its native dependencies are compatible with the bitness of the engine that will load it.

### Referencing the engine API assembly

To compile a plugin, reference the engine assembly that contains the plugin API types under the `MinorShift.Emuera.Runtime.Utils.PluginSystem` namespace.

In typical distributions this is the main `Emuera` executable (an `.exe` is still a .NET assembly and can be referenced by a C# project), or a `Emuera.dll` if you distribute the engine as a library.

### Required entry point: `PluginManifest`

For each plugin DLL, the engine searches for a type whose **type name** is exactly `PluginManifest` (namespace does not matter). The type must:

- have a parameterless constructor, and
- derive from `MinorShift.Emuera.Runtime.Utils.PluginSystem.PluginManifestAbstract`.

The manifest provides the list of methods exposed to ERB via its `methods` list (returned by `GetPluginMethods()`).

Practical notes:

- If the DLL contains multiple `PluginManifest` types, the engine will pick one depending on reflection enumeration order; do not rely on this. Provide exactly one.
- If two methods register the same `Name` (after `IgnoreCase` normalization, if enabled), registration throws and plugin loading aborts. Avoid name collisions across plugins.

From `emuera.em/Emuera/Runtime/Utils/PluginSystem/PluginManager.cs` (plugin discovery + security gate, excerpt):

```csharp
if (!Directory.Exists(Path.Combine(Program.ExeDir, "Plugins")))
    return;
string[] plugins = Directory.GetFiles(Path.Combine(Program.ExeDir, "Plugins"), "*.dll");
bool pluginsAware = File.Exists(Program.ExeDir + "pluginsAware.txt");
...
if (!pluginsAware)
    throw new ExeEE("This game comes prepackaged with plugins. ... create file pluginsAware.txt ...");
...
Assembly DLL = Assembly.LoadFrom(pluginPath);
var manifestType = DLL.GetTypes().Where((v) => v.Name == "PluginManifest").FirstOrDefault();
...
PluginManifestAbstract manifest = (PluginManifestAbstract)Activator.CreateInstance(manifestType);
var methods = manifest.GetPluginMethods();
foreach (var method in methods)
    AddMethod(method);
```

### `CALLSHARP` parsing and binding (engine behavior)

`CALLSHARP` is the only ERB-facing entry point for plugins. In this build:

- The method name is parsed as a raw string token (not an expression and not a FORM string).
- If the method name is a constant and is found in the plugin registry, the engine binds it at load time.
- If the method name is not found, the engine emits a load-time warning but still leaves the call target unbound; at runtime, executing such a line fails (null call target).

From `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (method-name tokenization, excerpt):

```csharp
CharStream st = line.PopArgumentPrimitive();
string str = LexicalAnalyzer.ReadString(st, StrEndWith.LeftParenthesis_Bracket_Comma_Semicolon);
str = str.Trim([' ', '\t']);
funcname = new SingleStrTerm(str);
```

Practical implication: because the engine trims the parsed method name, plugin method `Name` values should not rely on leading/trailing spaces for uniqueness (scripts cannot spell them).

From `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs` (binding check, excerpt):

```csharp
if (!manager.HasMethod(arg.ConstStr))
{
    ParserMediator.Warn(string.Format(trerror.MethodNotFound.Text, arg.ConstStr), func, 2, true, false);
    return;
}
arg.CallFunc = manager.GetMethod(func.Argument.ConstStr);
```

From `emuera.em/Emuera/Runtime/Script/Parser/LexicalAnalyzer.cs` (escape handling inside raw-string parsing, excerpt):

```csharp
case '\\':
    st.ShiftNext();
    switch (st.Current)
    {
        case 's': buffer.Append(' '); break;
        case 'S': buffer.Append('　'); break;
        case 't': buffer.Append('\t'); break;
        case 'n': buffer.Append('\n'); break;
        default: buffer.Append(st.Current); break;
    }
    st.ShiftNext();
    continue;
```

### Exposed methods: `IPluginMethod`

Each exposed method must implement `MinorShift.Emuera.Runtime.Utils.PluginSystem.IPluginMethod`:

- `string Name { get; }` — the method name used by `CALLSHARP`.
- `string Description { get; }` — informational (not required for dispatch).
- `void Execute(PluginMethodParameter[] args)` — invoked by `CALLSHARP`.

Method-name lookup uses the engine’s `IgnoreCase` configuration:

- If `IgnoreCase = true`, method names are matched case-insensitively.
- Otherwise, they are case-sensitive.

### Argument values and write-back

`CALLSHARP` passes arguments as an array of `PluginMethodParameter`:

- For a string expression argument, the engine creates a parameter with `isString = true` and initializes `strValue`.
- For a non-string argument, the engine creates a parameter with `isString = false` and initializes `intValue`.

After `Execute` returns, `CALLSHARP` performs a write-back step:

- For each argument position whose original ERB argument is a **variable term**, the engine assigns a new value from `args[i]` back into that variable.
  - If the variable term is a string variable, it writes back `args[i].strValue`.
  - Otherwise it writes back `args[i].intValue`.

Implications for plugin authors:

- To implement “out/ref”-style outputs, mutate `args[i].strValue` / `args[i].intValue` in-place.
- `args[i].isString` reflects the original ERB expression type, but write-back depends on whether the ERB argument is a *string variable* or an *integer variable*. Avoid setting only one field when you don’t control which variable kind was passed.

From `emuera.em/Emuera/Runtime/Utils/PluginSystem/PluginMethodParameter.cs` (how ERB terms are converted to plugin args, excerpt):

```csharp
internal static PluginMethodParameter ConvertTerm(AExpression term, ExpressionMediator exm)
{
    if (term.IsString) return new PluginMethodParameter(term.GetStrValue(exm));
    else return new PluginMethodParameter(term.GetIntValue(exm));
}
```

From `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs` (argument conversion + write-back, excerpt):

```csharp
var pluginArgs = arg.RowArgs.Select((term) => PluginMethodParameterBuilder.ConvertTerm(term, exm)).ToArray();
arg.CallFunc.Execute(pluginArgs);
for (var i = 0; i < pluginArgs.Count(); ++i)
{
    var rowArg = arg.RowArgs[i];
    if (rowArg is VariableTerm)
    {
        var varTerm = (VariableTerm)rowArg;
        if (varTerm.IsString) varTerm.SetValue(pluginArgs[i].strValue, exm);
        else varTerm.SetValue(pluginArgs[i].intValue, exm);
    }
}
```

### Calling back into the engine

Plugins run in-process and can call engine APIs directly (they are not sandboxed).

- You can access the engine’s plugin API entry point via `PluginManager.GetInstance()`.
- `PluginManager` provides helper methods for common tasks (printing to the console, reading/setting variables, creating a character context wrapper, awaiting timers, etc.).
- As an escape hatch, `PluginManager.ExecuteLine(string line)` can execute a single ERB instruction line through the interpreter (intended for debugging/quick integration; prefer direct API calls where possible).

From `emuera.em/Emuera/Runtime/Utils/PluginSystem/PluginManager.cs` (selected public API surface, excerpt):

```csharp
public static PluginManager GetInstance()
{
	if (instance == null)
	{
		instance = new PluginManager();
	}

	return instance;
}

public void ExecuteLine(string line)
{
	var logicalLine = LogicalLineParser.ParseLine(line, null);
	InstructionLine func = (InstructionLine)logicalLine;
	ArgumentParser.SetArgumentTo(func);
	func.Function.Instruction.DoInstruction(expressionMediator, func, processState);
}

public void Print(string text)
{
	expressionMediator.Console.Print(text);
}
public void PrintError(string text)
{
	expressionMediator.Console.PrintError(text);
}
public void PrintC(string text, bool aligmentRight = false)
{
	expressionMediator.Console.PrintC(text, aligmentRight);
}
public void PrintPlain(string text)
{
	expressionMediator.Console.PrintPlain(text);
}
public void PrintSystemLine(string text)
{
	expressionMediator.Console.PrintSystemLine(text);
}
public void PrintButton(string text, long id)
{
	expressionMediator.Console.PrintButton(text, id);
}
public void PrintHtml(string htmlText, bool toBuffer = false)
{
	expressionMediator.Console.PrintHtml(htmlText, toBuffer);
}
public void PrintNewLine()
{
	expressionMediator.Console.NewLine();
}
public void FlushConsole(bool force = false)
{
	expressionMediator.Console.PrintFlush(force);
}

public void WaitInput(bool oneInput = true, int timelimit = -1)
{
	InputRequest request = new()
	{
		OneInput = oneInput,
		Timelimit = timelimit
	};
	expressionMediator.Console.WaitInput(request);
}
public void ReadAnyKey()
{
	expressionMediator.Console.ReadAnyKey();
}
public void Await(int time)
{
	expressionMediator.Console.Await(time);
}
public void ForceStopTimer()
{
	expressionMediator.Console.forceStopTimer();
}
public void Quit(bool force = false)
{
	if (force)
	{
		expressionMediator.Console.ForceQuit();
	}
	else
	{
		expressionMediator.Console.Quit();
	}
}

public long[] GetCharacterIDs()
{
	return expressionMediator.VEvaluator.VariableData.CharacterList.Select(v => v.NO).ToArray();
}
public long GetIntVar(string name, int index = 0)
{
	return expressionMediator.VEvaluator.VariableData.GetVarTokenDic()[name].GetIntValue(expressionMediator, [index]);
}
public string GetStrVar(string name, int index = 0)
{
	return expressionMediator.VEvaluator.VariableData.GetVarTokenDic()[name].GetStrValue(expressionMediator, [index]);
}
public void SetIntVar(string name, long val, int index = 0)
{
	expressionMediator.VEvaluator.VariableData.GetVarTokenDic()[name].SetValue(val, [index]);
}
public void SetStrVar(string name, string val, int index = 0)
{
	expressionMediator.VEvaluator.VariableData.GetVarTokenDic()[name].SetValue(val, [index]);
}

public void SetCharVar(string name, long charId, string key, long value)
{
	var variable = expressionMediator.VEvaluator.VariableData.GetVarTokenDic()[name];
	var errPos = "";
	var dict = expressionMediator.VEvaluator.Constant.GetKeywordDictionary(out errPos, VariableCode.CFLAG, 1, key);
	variable.SetValue(value, [charId, dict[key]]);
}
public void SetCharVar(string name, long charId, long key, long value)
{
	var variable = expressionMediator.VEvaluator.VariableData.GetVarTokenDic()[name];
	variable.SetValue(value, [charId, key]);
}
public long GetCharVar(string name, long charId, long key)
{
	var variable = expressionMediator.VEvaluator.VariableData.GetVarTokenDic()[name];
	return variable.GetIntValue(expressionMediator, [charId, key]);
}
public long GetCharVar(string name, long charId, string key)
{
	var variable = expressionMediator.VEvaluator.VariableData.GetVarTokenDic()[name];
	var errPos = "";
	var dict = expressionMediator.VEvaluator.Constant.GetKeywordDictionary(out errPos, VariableCode.CFLAG, 1, key);
	return variable.GetIntValue(expressionMediator, [charId, dict[key]]);
}

public System.Data.DataTable GetDataTable(string name)
{
	return expressionMediator.VEvaluator.VariableData.DataDataTables[name];
}
public static PluginAPICharContext CreateCharContext(long charId)
{
	return new PluginAPICharContext(charId);
}
```

From `emuera.em/Emuera/Runtime/Utils/PluginSystem/PluginManager.cs` (cached wrapper fields exposed on the singleton, excerpt):

```csharp
public GlobalInt1dWrapper DAY;
public GlobalInt1dWrapper MONEY;
public GlobalInt1dWrapper ITEM;
public GlobalInt1dWrapper FLAG;
public GlobalInt1dWrapper TFLAG;
public GlobalInt1dWrapper UP;
public GlobalInt1dWrapper PALAMLV;
public GlobalInt1dWrapper EXPLV;
public GlobalInt1dWrapper EJAC;
public GlobalInt1dWrapper DOWN;
public GlobalInt1dWrapper RESULT;
public GlobalInt1dWrapper COUNT;
public GlobalInt1dWrapper TARGET;
public GlobalInt1dWrapper ASSI;
public GlobalInt1dWrapper MASTER;
public GlobalInt1dWrapper NOITEM;
public GlobalInt1dWrapper LOSEBASE;
public GlobalInt1dWrapper SELECTCOM;
public GlobalInt1dWrapper ASSIPLAY;
public GlobalInt1dWrapper PREVCOM;
public GlobalInt1dWrapper TIME;
public GlobalInt1dWrapper ITEMSALES;
public GlobalInt1dWrapper PLAYER;
public GlobalInt1dWrapper NEXTCOM;
public GlobalInt1dWrapper PBAND;
public GlobalInt1dWrapper BOUGHT;

public GlobalInt1dWrapper GLOBAL;
public GlobalInt1dWrapper RANDDATA;

public GlobalString1dWrapper SAVESTR;
public GlobalString1dWrapper TSTR;
public GlobalString1dWrapper STR;
public GlobalString1dWrapper RESULTS;
public GlobalString1dWrapper GLOBALS;

public GlobalConstInt1dWrapper NO;
public GlobalConstInt1dWrapper ITEMPRICE;

public GlobalConstString1dWrapper ABLNAME;
public GlobalConstString1dWrapper TALENTNAME;
public GlobalConstString1dWrapper EXPNAME;
public GlobalConstString1dWrapper MARKNAME;
public GlobalConstString1dWrapper PALAMNAME;
public GlobalConstString1dWrapper ITEMNAME;
public GlobalConstString1dWrapper TRAINNAME;
public GlobalConstString1dWrapper BASENAME;
public GlobalConstString1dWrapper SOURCENAME;
public GlobalConstString1dWrapper EXNAME;
public GlobalConstString1dWrapper EQUIPNAME;
public GlobalConstString1dWrapper TEQUIPNAME;
public GlobalConstString1dWrapper FLAGNAME;
public GlobalConstString1dWrapper TFLAGNAME;
public GlobalConstString1dWrapper CFLAGNAME;
public GlobalConstString1dWrapper TCVARNAME;
public GlobalConstString1dWrapper CSTRNAME;
public GlobalConstString1dWrapper STAINNAME;

public GlobalConstString1dWrapper CDFLAGNAME1;
public GlobalConstString1dWrapper CDFLAGNAME2;
public GlobalConstString1dWrapper STRNAME;
public GlobalConstString1dWrapper TSTRNAME;
public GlobalConstString1dWrapper SAVESTRNAME;
public GlobalConstString1dWrapper GLOBALNAME;
public GlobalConstString1dWrapper GLOBALSNAME;
```

From `emuera.em/Emuera/Runtime/Utils/PluginSystem/VariableDataWrappers.cs` (indexer-based variable wrappers, excerpt):

```csharp
public class GlobalInt1dWrapper
{
    public long this[string key] { get => Get(key); set => Set(key, value); }
    public long this[long key] { get => Get(key); set => Set(key, value); }

    public long Get(string key) { ... } // string-key -> index via keyword dictionary
    public long Get(long key) => token.GetIntValue(exm, [key]);

    public void Set(string key, long value) { ... } // string-key -> index via keyword dictionary
    public void Set(long key, long value) => token.SetValue(value, [key]);
}

public class GlobalString1dWrapper
{
    public string this[string key] { get => Get(key); set => Set(key, value); }
    public string this[long key] { get => Get(key); set => Set(key, value); }
    public string Get(string key) { ... } // string-key -> index via keyword dictionary
    public string Get(long key) => token.GetStrValue(exm, [key]);
    public void Set(string key, string value) { ... } // string-key -> index via keyword dictionary
    public void Set(long key, string value) => token.SetValue(value, [key]);
}

public class CharInt1dWrapper
{
    public long this[string key] { get => Get(key); set => Set(key, value); }
    public long this[long key] { get => Get(key); set => Set(key, value); }

    public long Get(string key) { ... } // string-key -> index via keyword dictionary
    public long Get(long key) => token.GetIntValue(exm, [charId, key]);

    public void Set(string key, long value) { ... } // string-key -> index via keyword dictionary
    public void Set(long key, long value) => token.SetValue(value, [charId, key]);
}

public class CharInt2dWrapper
{
    public long this[long keyA, long keyB] { get => Get(keyA, keyB); set => Set(keyA, keyB, value); }
    public long Get(long keyA, long keyB) => token.GetIntValue(exm, [charId, keyA, keyB]);
    public void Set(long keyA, long keyB, long value) => token.SetValue(value, [charId, keyA, keyB]);
}

public class CharUserdefinedInt1dWrapper
{
    public long this[string key, long idx] { get => Get(key, idx); set => Set(key, value, idx); }
    public long Get(string key, long idx = 0) { ... } // optional IgnoreCase uppercasing
    public void Set(string key, long value, long idx = 0) { ... } // optional IgnoreCase uppercasing
}

public class CharStringWrapper
{
    public string Get() => token.GetStrValue(exm, [charId]);
    public void Set(string value) => token.SetValue(value, [charId]);
}

public class CharString1dWrapper
{
    public string this[long key] { get => Get(key); set => Set(key, value); }
    public string Get(long key) => token.GetStrValue(exm, [charId, key]);
    public void Set(long key, string value) => token.SetValue(value, [charId, key]);
}
```

From `emuera.em/Emuera/Runtime/Utils/PluginSystem/PluginAPICharContext.cs` (character context wrapper, excerpt):

```csharp
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

### Dependencies

Plugin DLLs are loaded with `Assembly.LoadFrom(...)`. If your plugin depends on additional managed DLLs, keep those dependencies in a location where the runtime can resolve them reliably (commonly alongside the engine executable or alongside the plugin DLL, depending on the host’s probing behavior). If a dependency cannot be resolved, plugin loading fails at startup.

## Troubleshooting and compatibility pitfalls

### API quirks and limitations (this build)

These are observable behaviors/limitations that matter if you want to be compatible with existing plugins written for this engine build.

#### Caching happens before ERH is loaded

During engine startup, plugins are loaded before ERH/ERB compilation begins. The plugin system also caches some variable-token references at that time.

Implication:

- `PluginAPICharContext.UserDefined` is built from the engine’s `UserDefinedCharaVarList` at cache time. Because ERH `#DIM/#DIMS` declarations are processed later, `UserDefined` may not include ERH-defined character variables in this build.

Workarounds:

- Prefer accessing built-in character variables through the fixed fields on `PluginAPICharContext` (e.g. `BASE`, `ABL`, `CFLAG`, ...), which are cached from built-ins.
- For user-defined character variables:
  - Use `PluginManager.SetCharVar/GetCharVar` if your variable is compatible with the two-index `[charId, key]` shape.
  - Otherwise, use `PluginManager.ExecuteLine(...)` as a last resort to run an ERB assignment that touches the desired variable term.

#### `SetCharVar/GetCharVar` string-key overload is not generic

`PluginManager.SetCharVar(name, charId, string key, value)` and `GetCharVar(name, charId, string key)` always resolve `key` via the engine’s keyword dictionary for `CFLAG` (regardless of `name`). This means the string-key overload is only compatible with variables whose second index uses the same keyword dictionary as `CFLAG`.

#### `GetIntVar/GetStrVar` are 1D helpers

`GetIntVar/GetStrVar` and `SetIntVar/SetStrVar` pass a single index (`[index]`) to the underlying variable token. They are convenient for 1D global variables but do not directly cover:

- multi-dimensional variables
- character-data variables (which require a `charId` index)
- local variables (`LOCAL/LOCALS/ARG/ARGS`)

### Plugin not loaded at all

- No `Plugins/` directory: the engine does not create it and simply skips plugin loading.
- DLL does not contain any type whose `.Name` is exactly `PluginManifest`: the engine silently ignores that DLL.

### Engine aborts on startup (plugins present)

Common causes:

- `pluginsAware.txt` missing at game root: startup aborts with a security warning error.
- Manifest type exists but is not instantiable (no parameterless constructor, throws in constructor) or does not derive from `PluginManifestAbstract`: startup aborts due to an exception during instantiation/cast.
- Two plugin methods register the same `Name` (after `IgnoreCase` normalization if enabled): startup aborts because registration uses `Dictionary.Add(...)` and throws on duplicate keys.
- A plugin’s managed dependency is missing or incompatible: the engine may abort while loading the assembly or enumerating types (`GetTypes()`), depending on when the runtime tries to resolve the dependency.

### `CALLSHARP` fails at runtime

- Method name mismatch:
  - `CALLSHARP` does not evaluate the method name; it is a raw token with backslash escapes and trimming.
  - Quoting is literal: `CALLSHARP "ECHO"` looks for a method named `"ECHO"` (including quotes).
  - If `IgnoreCase = true`, method lookup normalizes names using `ToUpper()`; avoid non-ASCII method names if you want predictable matching across locales.
- Method missing:
  - The engine warns at load time for constant method names but still executes the line later; because the call target is unbound, the runtime failure may surface as a null-reference-style error.
- Empty argument slots:
  - `CALLSHARP M, , 1` parses but leaves a missing argument term; execution fails when the engine tries to evaluate that argument.

### API coupling and binary compatibility

Plugins are compiled against the engine assembly that defines `MinorShift.Emuera.Runtime.Utils.PluginSystem.*`. In practice this means:

- A plugin binary is tightly coupled to the engine build it was compiled against (assembly identity + API surface).
- To run an existing plugin binary on a different host, that host must provide the expected assembly identity and the required public types/members with compatible behavior.
