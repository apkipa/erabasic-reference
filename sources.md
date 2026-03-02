# Sources

This reference was assembled by reading and cross-checking:

## Documentation repository (`emuera.em.doc`)

- `emuera.em.doc/docs/Emuera/expression.en.md`
- `emuera.em.doc/docs/Emuera/operand.en.md`
- `emuera.em.doc/docs/Emuera/function.en.md`
- `emuera.em.doc/docs/Emuera/variables.en.md`
- `emuera.em.doc/docs/Emuera/user_defined_variables.en.md`
- `emuera.em.doc/docs/Emuera/ERH.en.md`
- `emuera.em.doc/docs/Emuera/user_defined_in_expression_function.en.md`
- Built-in index: `emuera.em.doc/docs/Reference/README.en.md`
- Control-flow pages: `emuera.em.doc/docs/Reference/IF.en.md`, `emuera.em.doc/docs/Reference/SELECTCASE.en.md`, etc.
- EMEE extension: `emuera.em.doc/docs/EMEE/EMEE_Summary.en.md` (for `;^;`)

## Engine source repository (`emuera.em`)

- Lexer / whitespace / comment handling: `emuera.em/Emuera/Runtime/Script/Parser/LexicalAnalyzer.cs`
- Instruction line parsing and “consume exactly one separator char”: `emuera.em/Emuera/Runtime/Script/Parser/LogicalLineParser.cs` (`ParseLine`)
- FORM scanner, `%...%`/`{...}` placeholders, triple symbols, and `\@...\@`: `emuera.em/Emuera/Runtime/Script/Parser/LexicalAnalyzer.cs`, `emuera.em/Emuera/Runtime/Script/Data/StrForm.cs`, `emuera.em/Emuera/Runtime/Script/Statements/Expression/Term.cs`, `emuera.em/Emuera/Runtime/Utils/LangManager.cs`, `emuera.em/Emuera/Runtime/Utils/CharStream.cs`, `emuera.em/Emuera/Runtime/Script/Parser/SubWord.cs`
- Argument parsing modes (raw vs expression vs FORM): `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (`STR_ArgumentBuilder`, `FORM_STR_ArgumentBuilder`, `STR_EXPRESSION_ArgumentBuilder`), `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs` (`PRINT_Instruction`)
- `#...` function attributes parsing: `emuera.em/Emuera/Runtime/Script/Parser/LogicalLineParser.cs`
- Event attribute grouping (`#ONLY/#PRI/#LATER/#SINGLE`) and sizing reconciliation: `emuera.em/Emuera/Runtime/Script/Data/LabelDictionary.cs`
- Method-safe instruction restriction inside `#FUNCTION/#FUNCTIONS`: `emuera.em/Emuera/Runtime/Script/Loader/ErbLoader.cs` (`setArgument`), `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs` (`IsMethodSafe`)
- Load pipeline / file order: `emuera.em/Emuera/Runtime/Script/Process.cs`
- Preload cache population (required for `OpenOnCache(...)` readers): `emuera.em/Emuera/UI/Game/EmueraConsole.cs` (`Initialize`), `emuera.em/Emuera/Runtime/Utils/Preload.cs`
- Root directory + folder layout (`erb/`, `csv/`, `dat/`, `resources/`): `emuera.em/Emuera/Program.cs` (`SetDirPaths`, static initializer `Data/erb` check)
- ERB/ERH loaders and preprocessor directives: `emuera.em/Emuera/Runtime/Script/Loader/ErbLoader.cs`, `emuera.em/Emuera/Runtime/Script/Loader/ErhLoader.cs`
- `*#*`-directory-first ERB ordering and its (lack of) sorting: `emuera.em/Emuera/Runtime/Script/Loader/ErbLoader.cs` (`LoadErbDir`)
- Line reading, `[[...]]` rename replacement, and `{...}` continuation: `emuera.em/Emuera/Runtime/Utils/EraStreamReader.cs`
- Encoding detection and preload cache: `emuera.em/Emuera/Runtime/Utils/EncodingHandler.cs`, `emuera.em/Emuera/Runtime/Utils/Preload.cs`
- Config keys/defaults and parsing rules: `emuera.em/Emuera/Runtime/Config/ConfigData.cs`, `emuera.em/Emuera/Runtime/Config/ConfigItem.cs`, `emuera.em/Emuera/Runtime/Config/Config.cs`
- File enumeration rules (`SearchSubdirectory`, `SortWithFilename`, extension-length filter): `emuera.em/Emuera/Runtime/Config/Config.cs` (`GetFiles`)
- CSV + variable sizing + name tables + `CHARA*.CSV` discovery + `VarExt*.csv` discovery: `emuera.em/Emuera/Runtime/Script/Data/ConstantData.cs`
- `#DIM/#DIMS` parsing and keyword constraints: `emuera.em/Emuera/Runtime/Script/Data/UserDefinedVariable.cs`
- Variable `:` argument inference and string-key wrapping: `emuera.em/Emuera/Runtime/Script/Statements/Variable/VariableParser.cs`, `emuera.em/Emuera/Runtime/Script/Statements/Variable/VariableStrArgTerm.cs`
- Assignment parsing and operators (`=`, `'=`, `+=`, batch assignment lists): `emuera.em/Emuera/Runtime/Script/Parser/LexicalAnalyzer.cs` (`ReadAssignmentOperator`), `emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs` (`SP_SET_ArgumentBuilder`), `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs` (`SET_Instruction`)
- Batch assignment write semantics (last-dimension slice write): `emuera.em/Emuera/Runtime/Script/Statements/Variable/VariableTerm.cs` (`SetValue(long[]/string[], ...)`), `emuera.em/Emuera/Runtime/Script/Statements/Variable/VariableToken.cs` (`SetValue(values, arguments)` overrides)
- Expression parsing and CASE expressions: `emuera.em/Emuera/Runtime/Script/Statements/Expression/ExpressionParser.cs`, `emuera.em/Emuera/Runtime/Script/Statements/CaseExpression.cs`
- Control-flow instruction semantics: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`, `emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs`
- Script execution order and jump/return mechanics: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`, `emuera.em/Emuera/Runtime/Script/Process.State.cs`
- Operator set/precedence and type rules: `emuera.em/Emuera/Runtime/Script/Statements/Expression/OperatorCode.cs`, `emuera.em/Emuera/Runtime/Script/Statements/Expression/OperatorMethod.cs`
- Runtime call stack / event sequencing / method calls: `emuera.em/Emuera/Runtime/Script/Process.State.cs`, `emuera.em/Emuera/Runtime/Script/Process.CalledFunction.cs`, `emuera.em/Emuera/Runtime/Script/Process.cs`, `emuera.em/Emuera/Runtime/Script/Data/LabelDictionary.cs`
- Local variable stores (`LOCAL/LOCALS`, `ARG/ARGS`) and per-function sizing rules: `emuera.em/Emuera/Runtime/Script/Statements/Variable/VariableLocal.cs`
- Label validation and reserved-name collision rules: `emuera.em/Emuera/Runtime/Script/Data/IdentifierDictionary.cs`
- Warning collection/filtering: `emuera.em/Emuera/Runtime/Script/Data/ParserMediator.cs`
- ScriptPosition and error-location plumbing: `emuera.em/Emuera/Runtime/Utils/EmueraException.cs`, `emuera.em/Emuera/Runtime/Script/Process.cs`, `emuera.em/Emuera/Runtime/Script/Statements/LogicalLine.cs`
- Variable storage partitioning + reset behavior: `emuera.em/Emuera/Runtime/Script/Statements/Variable/VariableData.cs`, `emuera.em/Emuera/Runtime/Script/Statements/Variable/VariableEvaluator.cs`, `emuera.em/Emuera/Runtime/Script/Statements/Variable/CharacterData.cs`
