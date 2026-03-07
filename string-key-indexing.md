# String-Key Indexing for Variables (`VAR:Key` / `VAR:"Key"` / `VAR:(expr)`)

Many EraBasic variables are indexed by `:` arguments. In this engine, some `:` arguments may be provided as **strings** (CSV names / aliases / ERD keys) and are resolved to integer indices.

This document specifies the exact parsing and resolution rules needed to reimplement “CSV name indexing” behavior.

## 1) Syntax forms that produce a string key

In a `:` argument position, a string key can appear as:

- a double-quoted string literal:
  - `ABL:"Skill"`
- a parenthesized string expression (dynamic key):
  - `ABL:(RESULTS:0)`
- a bare identifier that is interpreted as a key:
  - `ABL:Skill`

The last form is **context-sensitive** and only works when the identifier can be interpreted as a key (see §2).

## 2) Parsing: when does `ABL:Skill` become a string key?

The expression parser has a special “variable argument” mode for expressions that appear after `:` in a variable term.

In this mode, when it encounters an identifier token `IDENT`:

1) If `IDENT` resolves as a variable name, it is treated as a variable term (not a key).
2) Else if it resolves as a function reference, it is treated as that function reference term (and will later error if misused).
3) Else, if the variable being indexed has a known key table and `IDENT` is a defined key in that table, it is treated as the string literal key `"IDENT"`.
4) Otherwise it is an error (“cannot interpret identifier”).

Implications:

- Bare identifiers only become keys when they are **not** variable/function names and are known keys for that specific variable.
- Quoted keys (`"Skill"`) and parenthesized string expressions always produce a string value and do not rely on this special-case parsing.

## 3) Compilation: string arguments become numeric index terms

After the variable’s argument list is inferred/normalized (see `variables.md`), the engine converts each argument expression:

- if an argument expression is numeric (`long`), it stays numeric
- if an argument expression is string (`string`), it is wrapped into a special numeric term that resolves the string key to an integer at runtime

Practically, this means:

- string-key indexing is not a separate “string index type”; it compiles down to a numeric index.

## 4) Runtime resolution algorithm (engine-accurate)

At runtime, a string-key argument is resolved as follows:

1) Obtain a dictionary `dict: string -> int` for the variable code and the argument position being resolved:
   - `dict` is retrieved via `ConstantData.GetKeywordDictionary(out errPos, variableCode, argIndex, varNameForERD)`
2) Evaluate the key string `key = (stringExpr)`
3) If `key` is empty: error
4) If `dict` is `null`: error (ERD-specific error message may be used)
5) Look up `key` in `dict` (exact match):
   - if found, the result is the numeric index
   - if not found, error; if `errPos` is known, the error message references that CSV source (e.g. `abl.csv`)

### 4.1 Exact-match semantics (case sensitivity)

Key lookup uses .NET `Dictionary<string,int>` default semantics:

- keys are matched by exact string equality
- there is no automatic case-folding

Whether `ABL:Skill` works depends on whether the CSV/alias/ERD key is exactly `Skill` (not `SKILL`), unless the game’s data uses consistent casing.

### 4.2 Duplicate keys and aliases

For built-in CSV-backed tables, the reverse dictionaries are constructed as:

1) add each non-empty CSV “name” if the key is not already present
2) add each non-empty alias key if it is not already present

So the first occurrence wins; later duplicates are ignored.

## 5) Which variables accept string keys (built-in tables)

The engine’s `GetKeywordDictionary` defines, for each variable code:

- which dictionary is used (derived from which `csv/*.csv`)
- which argument position (`argIndex`, 0-based) is allowed to be a string key

`argIndex` is the index into the final parsed argument list (after character-variable argument inference).

### 5.1 Table: variable code → source → allowed `argIndex`

The following table is engine-accurate.

#### Character 1D variables (string key is typically the *second* argument, `argIndex = 1`)

- `ABL` → `abl.csv` → `argIndex = 1`
- `EXP` → `exp.csv` → `argIndex = 1`
- `TALENT` → `talent.csv` → `argIndex = 1`
- `PALAM`, `JUEL`, `GOTJUEL`, `CUP`, `CDOWN` → `palam.csv` → `argIndex = 1`
- `MARK` → `mark.csv` → `argIndex = 1`
- `SOURCE` → `source.csv` → `argIndex = 1`
- `EX`, `NOWEX` → `ex.csv` → `argIndex = 1`
- `EQUIP` → `equip.csv` → `argIndex = 1`
- `TEQUIP` → `tequip.csv` → `argIndex = 1`
- `CFLAG` → `cflag.csv` → `argIndex = 1`
- `TCVAR` → `tcvar.csv` → `argIndex = 1`
- `CSTR` → `cstr.csv` → `argIndex = 1`
- `STAIN` → `stain.csv` → `argIndex = 1`

#### Character scalar / other character variables

- `UP`, `DOWN` → `palam.csv` → `argIndex = 0` (this variable family uses a different indexing shape)
- `RELATION` → `chara*.csv` (character names/callnames/etc.) → `argIndex = 1`
- `NAME`, `CALLNAME` → `chara*.csv` dictionary exists but **string-key indexing is not allowed** in variable-argument positions

#### Non-character 1D variables (string key is typically the *first* argument, `argIndex = 0`)

- `TRAINNAME` → `train.csv` → `argIndex = 0`
- `ITEM`, `ITEMSALES`, `ITEMPRICE` → `Item.csv` → `argIndex = 0`
- `LOSEBASE` → `base.csv` → `argIndex = 0`
- `FLAG` → `flag.csv` → `argIndex = 0`
- `TFLAG` → `tflag.csv` → `argIndex = 0`
- `CDFLAGNAME1` → `cdflag1.csv` → `argIndex = 0`
- `CDFLAGNAME2` → `cdflag2.csv` → `argIndex = 0`
- `STR` → `strname.csv` → `argIndex = 0`
- `TSTR` → `tstr.csv` → `argIndex = 0`
- `SAVESTR` → `savestr.csv` → `argIndex = 0`
- `GLOBAL` → `global.csv` → `argIndex = 0`
- `GLOBALS` → `globals.csv` → `argIndex = 0`
- `DAY` → `day.csv` → `argIndex = 0`
- `TIME` → `time.csv` → `argIndex = 0`
- `MONEY` → `money.csv` → `argIndex = 0`

#### Non-character variables where the string key is the second argument (`argIndex = 1`)

- `BASE`, `MAXBASE`, `DOWNBASE` → `base.csv` → `argIndex = 1`

### 5.2 Special case: `CDFLAG`

`CDFLAG` selects between two different name tables depending on which index is being string-specified:

- if `argIndex == 1` → use `cdflag1.csv`
- if `argIndex == 2` → use `cdflag2.csv`
- any other `argIndex` in string-key context is an error

## 6) ERD extension: string keys for user-defined variables

When `UseERD` is enabled, additional key dictionaries may be available for certain user-defined variable families (e.g. `VAR`, `CVAR`, and their 2D/3D variants).

The lookup uses the variable’s declared name (`varname`) to select an ERD-provided key dictionary.

ERD dictionary selection is **variable-code-specific** and depends on which argument index is being resolved:

- `VAR`, `VARS`:
  - allowed `argIndex`: `0`
  - ERD dictionary key: `varname`
- `CVAR`, `CVARS`:
  - allowed `argIndex`: `1` (because the final argument list is typically `[chara, index]`)
  - ERD dictionary key: `varname`
- `VAR2D`, `VARS2D`:
  - if resolving `argIndex == 0`: dictionary key is `varname@1`, allowed `argIndex = 0`
  - if resolving `argIndex == 1`: dictionary key is `varname@2`, allowed `argIndex = 1`
- `CVAR2D`, `CVARS2D`:
  - only `argIndex == 2` is allowed (final arguments are typically `[chara, i, j]`)
  - dictionary key is `varname@2`
- `VAR3D`, `VARS3D`:
  - resolving `argIndex == k` uses dictionary key `varname@{k+1}` and allows only that same `argIndex`

If the ERD dictionary is missing, string-key indexing for that variable fails (the engine throws an ERD-specific “key not defined” error).

## Fact-check cross-refs (optional)

- Bare-identifier key parsing in variable-arg context: `emuera.em/Emuera/Runtime/Script/Statements/Expression/ExpressionParser.cs`
- Argument inference and wrapping of string args: `emuera.em/Emuera/Runtime/Script/Statements/Variable/VariableParser.cs`
- Runtime key→index resolution term: `emuera.em/Emuera/Runtime/Script/Statements/Variable/VariableStrArgTerm.cs`
- Key dictionary mapping table + ERD behavior: `emuera.em/Emuera/Runtime/Script/Data/ConstantData.cs`
