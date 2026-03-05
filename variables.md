# Variables (built-in, arrays, user-defined)

EraBasic has a large set of built-in variables (engine-provided) plus user-defined variables.

Variables are either **numeric** (`Int64` / `long`) or **string** (`string`). Many variables are arrays (including multi-dimensional arrays).

## Types and indexing

- Numeric variables evaluate to `Int64` / `long`.
- String variables evaluate to `string`.
- Many variables are arrays, indexed using `:`:

    A:10 = 123
    CFLAG:TARGET:1 = 1

Multi-dimensional arrays use multiple `:` separators.

Important precision note (engine-accurate):

- “numeric” in this engine means `Int64` / `long`, not 32-bit `int`.

## Arrays are storage, not first-class expression values

Emuera has many array variables, but the language’s value model is still **scalar**:

- Expressions evaluate to a single `long` or `string`, never an “array value”.
- A variable reference with `:` indices refers to a **single cell** (after index evaluation and bounds checks).
- Some built-in instructions that “operate on arrays” take a **variable term** (so the engine can find the underlying array storage), not an array-typed value.

Practical consequence (important for compatibility):

- For **non-character 1D arrays**, writing `NAME` is treated as `NAME:0` by variable parsing.
- For **character-data 1D arrays**, the value form uses two indices `[chara, index]`; many “array storage” operations only use the character selector and effectively treat the element index as a dummy.
- For **2D/3D arrays**, omitting indices can parse as a special “no-arg variable term” that cannot be read or assigned as a value (it throws a “missing variable argument” error if evaluated).

## Variable terms (r-values, l-values, and “by-ref-like” uses)

In this reference, a **variable term** means the expression node produced by parsing a variable reference such as:

- `V` / `V:0` / `V:1:2` / `LOCAL@OtherFunction:3`

Engine-accurate model:

- The parser first resolves the identifier (and optional `@subKey`) into a **variable token** (the resolved variable identity + its type/dimension metadata).
- It then parses up to three `:` index expressions and applies argument inference rules (see below).
- The resulting variable term can be used in different roles:
  - **r-value** (most expressions): reads one scalar cell value (`long` or `string`)
  - **l-value** (assignment LHS, `++/--`): identifies a writable cell (must not be `CONST`)
  - **“by-ref-like” operand** for some built-ins: the operand must be a variable term so the engine can locate the underlying variable storage (for example, array manipulation built-ins, and method arguments whose rule includes a `Ref*` constraint).

Evaluation note:

- A variable term’s index expressions are evaluated **each time** the term is evaluated, left-to-right.
- A single source line may evaluate the “same-looking” variable term more than once (for example, a compound assignment that lowers into a read-then-write path), so indices with side effects can be observed more than once.

Special forms that matter for compatibility:

- **Fixed variable terms**: when all indices are compile-time constants, the engine may restructure a variable term into a “fixed” form that stores the indices as numeric constants.
  - This is observable only via error timing (some bounds/type errors can occur at load time due to constant folding).
- **No-arg variable terms** (missing required indices): for some arrays, writing no `:` indices at all can produce a distinct term that cannot be read/written as a value.
  - Evaluating it as a value (or assigning to it) throws a “missing variable argument” error.
  - Some built-ins accept this form only via instruction-specific special cases. Do not assume it behaves like “the whole array”.

## Variable names vs variable terms (important for built-ins)

Some built-ins take a **variable term** (a parsed variable reference like `CFLAG:TARGET:0`) so they can operate on the underlying storage.
Other built-ins take a **variable name** (a single identifier token like `CFLAG`) and do not parse any `:` indices.

This difference is observable:

- If a built-in takes a **variable name identifier**, writing `NAME:...` after it is just extra trailing text.
  - The engine may warn, but the `:...` part is not treated as a character selector or element index, and is not evaluated.
  - Example: `VARSIZE CFLAG:TARGET:0` is treated as `VARSIZE CFLAG`.
- If a built-in takes a **variable name string** (e.g. a method like `VARSIZE("CFLAG")`), the lookup is done on the entire string.
  - A string that includes `:` indices (e.g. `"CFLAG:TARGET:0"`) does not match any variable name and is rejected.

Practical reading tip:

- “Ignored tail” can mean two different things depending on how the built-in parses arguments:
  - **Identifier-only** parsing (like `VARSIZE <name>`): the tail is not parsed at all (it may contain arbitrary characters), and it is not evaluated.
  - **Compatibility tail** parsing (like `GOTO LABEL, expr...`): the tail must still be syntactically valid according to expression grammar, but the engine does not evaluate it (no side effects).

## Variable sizes and prohibiting variables

In Emuera, the element count of many built-in array variables is configurable via `csv/VariableSize.csv`.

- Setting a variable’s size to `-1` prohibits using that variable in ERB.
- Using or referencing a prohibited variable causes an error.
- If the engine internally needs a prohibited variable, assignments may be ignored and the value treated as `-1`.

This is primarily a compatibility/safety feature for specific games/engines.

## Bounds checking and error behavior (engine-accurate)

### Prohibited variables

At variable-token resolution time:

- If a variable is marked prohibited (`IsForbid == true`), resolving it as a variable token throws an error (“used prohibited var”).
- Some system variables are not intended to be prohibited; if they are prohibited by configuration, the engine may throw a fatal error when the variable token is resolved.

### Out-of-range indices

Variable indices are numeric (`long`) but must satisfy normal array bounds:

- For a 1D array: `0 <= i < length`
- For a 2D array: `0 <= i < len0` and `0 <= j < len1`
- For a 3D array: `0 <= i < len0`, `0 <= j < len1`, `0 <= k < len2`

For character variables, the first index is the character selector:

- `0 <= chara < CHARANUM` (current character list count)

When an index is out of range at runtime, the engine throws an error (it converts internal index/overflow exceptions into a bounds-checked `CodeEE`).

### Null string cells read as empty

When reading a string variable cell, if the underlying storage contains `null`, the engine returns `""` (empty string) instead of `null`.

This applies both to normal string variables and to `RESULTS`/`RESULTS:n`.

## “Calculated” variables (`__CALC__`) and special cases

Some built-in variables are marked as “calculated” in the engine (`__CALC__` flag).
This is a metadata flag on the variable token; it does **not** change the surface syntax of variable terms.

Typical examples include:

- `RAND:n` (random value; see the dedicated argument restrictions below)
- `CHARANUM` (derived from the current character list length)
- `__FILE__`, `__FUNCTION__`, `__LINE__` (debug/introspection variables)
- `WINDOW_TITLE` (engine/UI state; writable in this codebase)

Compatibility-relevant implications:

- Many calculated variables are also `CONST`/unchangeable, but not all of them.
- Some “by-ref-like” contexts explicitly reject calculated variables even if they look like normal variable terms (for example, method arguments whose rule includes a `Ref*` requirement).

## Batch assignment to arrays

Emuera supports assigning comma-separated values to consecutive array elements:

    A:10 = 1,2,3
    DA:0:0 = 1,2,3

Key rules (engine-accurate):

- Batch assignment is only accepted when the assignment operator is the *plain* assignment operator for the variable’s type:
  - **integer variables**: `=`
  - **string variables**: `'=`
- It does not work with compound assignments (e.g. `+= 1,2,3` is rejected at parse time).
- The RHS is parsed as a comma-separated list of expressions; **no element may be omitted** (`,,` is an error).
- The parser does not require the LHS to actually be an array at parse time. If you write a list assignment to a scalar variable, it parses but then fails at runtime when the engine attempts an N-element write into a non-array token.

### Semantics: which elements are written

Let `V` be an `N`-dimensional array variable, and let the LHS provide exactly `N` indices.

Batch assignment always writes along the **last** dimension, starting from the last index:

- **1D**: `V:i = a,b,c` writes `V[i]=a`, `V[i+1]=b`, `V[i+2]=c`.
- **2D**: `V:i:j = a,b,c` writes `V[i,j]=a`, `V[i,j+1]=b`, `V[i,j+2]=c`.
- **3D**: `V:i:j:k = a,b,c` writes `V[i,j,k]=a`, `V[i,j,k+1]=b`, `V[i,j,k+2]=c`.

For **character data** arrays, the first index is the character selector, but the “write along the last dimension” rule is the same:

    CFLAG:TARGET:0 = 1,2,3    ; writes CFLAG[TARGET,0], CFLAG[TARGET,1], CFLAG[TARGET,2]

### Evaluation order and partial writes

- The RHS expressions are evaluated left-to-right to produce a temporary value list.
- The engine then writes the list in increasing index order.
- If an out-of-range happens partway through the write, earlier elements may already have been updated; there is no rollback.

### Out-of-range behavior (engine-accurate)

In batch assignment, bounds behavior differs depending on *what* is out of range:

- If any *provided* index is out of range (e.g. `i < 0`, `i >= len`), the engine throws the same “index out of range” error family as normal indexing.
- If the starting indices are valid but the write runs past the end of the last dimension (e.g. `i + count > len`), the engine throws a generic “assign out of range” error for that variable (rather than reporting the specific failing element).

## String-based indexing (CSV names)

For many CSV-backed variables, you can index by the name defined in `*.csv` instead of a numeric index:

    ABL:Skill += 1
    ABL:"Skill" += 1

Dynamic string expressions can be used with parentheses:

    ABL:(RESULTS:0) += 1

Notes:

- You can also write quoted names (e.g. `ABL:"Skill"`). This is still “name indexing”, not a general string expression.
- If you omit parentheses, a bare name can be ambiguous with a variable name. In ambiguous cases, the engine may prefer the variable interpretation.
- If the “name” looks like a number, it may be interpreted as a numeric index instead of a CSV name.

## Argument inference rules for character variables (engine-accurate)

Many built-in variables are **character data variables** (their first index is a character selector such as `TARGET`).

The parser applies argument inference rules for these variables when you use `:` arguments.

Terminology used below:

- “args omitted” means you wrote no `:` arguments at all (e.g. `PALAM` not `PALAM:...`).
- “provided args” means the raw `:` arguments you wrote before inference.
- The final argument list is the list actually stored in the parsed `VariableTerm`.

### 0D character variables (scalar per character)

Expected final args: 1 argument: `[chara]`.

- If args omitted and `SystemNoTarget` is `true`: parsed as a “no-arg variable term” (special form; not equivalent to `TARGET`).
- If args omitted and `SystemNoTarget` is `false`: `chara` defaults to `TARGET`.
- If you provide more than 1 argument: error.
- If you provide no chara argument while `SystemNoTarget` is `true`: error (the only exception is “args omitted” which becomes the no-arg term).

### 1D character variables (per-character arrays)

Expected final args: 2 arguments: `[chara, index]`.

- If you provide 0 args:
  - if `SystemNoTarget` is `true`: parsed as a no-arg variable term
  - else: defaults to `[TARGET, 0]`
- If you provide 1 arg:
  - if `SystemNoTarget` is `true`: error (you must provide both `chara` and `index`)
  - else: the single arg is treated as `index`, and `chara` defaults to `TARGET`
- If you provide 2 args: they are `[chara, index]` as written.
- If you provide 3+ args: error.

### 2D character variables (per-character 2D arrays)

Expected final args: 3 arguments: `[chara, index1, index2]`.

- If you provide 0 args: parsed as a no-arg variable term.
- If you provide 1–2 args: error (cannot omit any required index in this form).
- If you provide 3 args: they are used as written.
- If you provide 4+ args: error.

## Argument rules for non-character arrays (engine-accurate)

For non-character arrays:

- 1D arrays default a missing index to `0` (`VAR:0`) except for `RAND` (see below).
- 2D/3D arrays require all indices if any are present; partial omission is an error.
- Any variable (character or not) rejects more than 3 `:` arguments syntactically.

## `RAND` argument restrictions (config-dependent)

`RAND` is a special 1D numeric variable with extra constraints controlled by `CompatiRAND`:

- If `CompatiRAND` is `false`:
  - omitting the argument (`RAND`) is an error
  - a constant `0` argument (`RAND:0`) is an error
- If `CompatiRAND` is `true`, the parser allows omission (it becomes `RAND:0`).

## String arguments to `:` are not “string indices”

If a `:` argument expression is of string type, the parser converts it into a numeric term that resolves the string key to an integer index via engine tables at runtime.

This is how CSV-name indexing works (e.g. `ABL:"Skill"`).

For the exact mapping of which variables allow string keys, which argument position accepts them, and the ERD extension behavior, see:

- `string-key-indexing.md`

## Local variables

Built-in locals include `LOCAL/LOCALS` and argument locals `ARG/ARGS`.

- `LOCAL/LOCALS` are considered obsolete in modern Emuera style; prefer `#DIM/#DIMS`.
- `ARG/ARGS` are used for passing arguments and are sized to fit argument usage.

### `LOCAL / LOCALS`

`LOCAL` (numeric) and `LOCALS` (string) are “local” in the sense that they are scoped per-function-name internally, but they are **not** automatically reset on each call.

In practice:

- They are not saved.
- They persist across calls to the same function label name.
- Event functions with the same name share them.
- Recursive calls reuse the same underlying storage, which can make recursion brittle.

Prefer `#DIM/#DIMS` variables for clarity and predictable scoping.

### `ARG / ARGS`

`ARG` (numeric) and `ARGS` (string) hold argument values passed to a function.

- They are not saved.
- Their size is at least the configured default, but the engine also ensures enough elements exist to hold the largest referenced argument index for that function.

### Optional local subkey: `LOCAL@subKey` / `ARG@subKey` (engine behavior)

In variable syntax, `NAME@subKey` is **not** a general “variable namespace” feature.
In this codebase, `@subKey` is accepted only for the local-variable families:

- `LOCAL`, `LOCALS`, `ARG`, `ARGS`

Semantics:

- Without `@subKey`, the engine uses the **current function label name** as the implicit subkey. This is why locals are “scoped per function name”.
- With an explicit `@subKey`, the engine selects (and may create) a separate local-variable store keyed by that string, and emits a warning that this is not recommended.

Important constraints:

- Using `@subKey` with a non-local variable (built-in global, ERH global, or `#DIM` private variable) is an error.
- Referencing `LOCAL/ARG/LOCALS/ARGS` without an explicit `@subKey` is an error when the engine is not currently scanning/executing inside a function body (for example, in some debug contexts).

## User-defined variables: `#DIM` / `#DIMS`

Emuera supports user-defined variables via `#DIM` (numeric) and `#DIMS` (string).

They exist in two scopes:

- **Private variables**: declared by `#DIM/#DIMS` *inside an ERB function* (a `#...` line immediately after an `@LABEL` line).
- **Global variables**: declared by `#DIM/#DIMS` *inside ERH headers*.

### 1) Declaration syntax (engine-accurate)

Conceptually the declaration is:

    #DIM  [keywords...]  NAME  [ , size1 [ , size2 [ , size3 ] ] ]  [ = init1 , init2 , ... ]
    #DIMS [keywords...]  NAME  [ , size1 [ , size2 [ , size3 ] ] ]  [ = init1 , init2 , ... ]

The parser reads **zero or more keywords** (as plain identifiers) before `NAME`.
The first identifier that is *not* recognized as a keyword becomes the variable name.

Keywords recognized by this engine:

- `CONST`
- `REF`
- `DYNAMIC`
- `STATIC`
- `GLOBAL`
- `SAVEDATA`
- `CHARADATA`

Compatibility quirk (important): the directive keyword match is done under `Config.StringComparison` (often case-insensitive when `IgnoreCase=YES`), but the “is this string variable?” flag is derived using a **case-sensitive** check against the literal `"DIMS"`. So `#dims ...` can be accepted by the loader but still create a **numeric** variable in this codebase.

### 2) Name validity and conflicts

Name validity checks differ slightly between private and global variables.

For both scopes:

- Names must not contain whitespace or punctuation; practically, use only ASCII letters/digits and `_`.
- Names must not collide (under `IgnoreCase` / `Config.StringComparison`) with:
  - reserved words like `IS`, `TO`, `INT`, `STR`, `STATIC`, `DYNAMIC`, `GLOBAL`, `SAVEDATA`, `CHARADATA`, `REF`, etc.
  - built-in instruction names
  - built-in expression function names
  - built-in variable names
  - user-defined macro names
  - already-declared user-defined global variables

Private-only rule:

- A private variable name starting with an ASCII digit is rejected.

Additional warnings:

- If `UseERD=YES` and `CheckDuplicateIdentifier=YES`, declaring a user variable whose name equals any ERD key name emits a warning.
- If the variable name matches any CSV “name key” (from the built-in name tables), the engine emits a warning.

### 3) Dimensions and size expressions

If you omit all sizes:

- the variable is created as a **1D array of length 1**.

If you provide sizes, they must satisfy:

- Each provided `sizeN` must be a compile-time constant integer (`SingleLongTerm`) and must satisfy `1 <= sizeN <= 1000000`.
- You may specify up to **3** sizes (1D/2D/3D).
- The product `size1 * size2 * size3` must be `<= 1000000` (missing sizes are not part of the product).

If a size expression does not reduce to a constant integer, or is out of range, the declaration fails.

### 4) Initializers (`= ...`)

An initializer list is permitted only when all of these hold:

- the variable is **not** `REF`
- the variable is **not** `CHARADATA`
- the variable is **1D** (0–1 size values were provided)

Initializer rules:

- The initializer list is parsed as a comma-separated list of expressions, but **each element must be a compile-time constant** (`SingleLongTerm` for `#DIM`, `SingleStrTerm` for `#DIMS`).
- Omitted elements (`,,`) are not allowed.
- If a size was specified:
  - the initializer count must be `<= size`
  - for `CONST`, the initializer count must equal `size`
- If no size was specified:
  - the array length becomes the initializer count

If you write `CONST` without an initializer, the declaration fails.

### 5) `CONST`

`CONST` makes the user-defined variable **read-only** (assignment to it is rejected when parsing/building the assignment argument).

Constraints:

- `CONST` requires an initializer list.
- `CONST` must be **1D**.
- `CONST` cannot be combined with: `CHARADATA`, `GLOBAL`, `SAVEDATA`, `REF`, `DYNAMIC`.

### 6) `STATIC` vs `DYNAMIC` (private variables only)

Private variables can be either:

- `STATIC` (default): storage persists across calls to the same function label.
- `DYNAMIC`: storage is (re)allocated on function entry and discarded on return; recursion uses an internal stack to preserve each call frame’s storage.

Constraints:

- `STATIC` and `DYNAMIC` are mutually exclusive.
- Neither can be used with `CHARADATA`.
- `DYNAMIC` cannot be used with `CONST`.
- `STATIC` cannot be used with `REF`.

Initializer application:

- For 1D private variables with an initializer list, those initializer values are copied into the array on each `DYNAMIC` allocation, and also used as the “default state” for `STATIC` variables when the engine resets locals.

### 7) `REF` (reference variables, private only)

`REF` declares a reference-typed variable. It has **no storage** of its own; instead, it can be bound to some other variable’s underlying array.

In this codebase:

- Global `#DIM/#DIMS` declarations with `REF` are treated as “not implemented” and fail during ERH processing.
- Private `REF` variables are supported and are primarily used for **pass-by-reference parameters** in user-defined functions.

Dimension syntax for `REF`:

- The number of commas determines the dimension. `0` size placeholders are permitted but **any non-zero size is rejected**.
- Examples:
  - `#DIM REF X` → 1D reference
  - `#DIM REF X,0,0` or `#DIM REF X,,` → 2D reference
  - `#DIMS REF S,0,0,0` → 3D reference

Runtime behavior:

- A `REF` variable starts **unbound** when a function call frame is entered.
- Reading/writing an unbound `REF` variable raises an error (“empty ref var”).
- The engine binds/unbinds `REF` parameters as part of the function call argument binding process (see `functions.md` for how user function arguments are evaluated and assigned).

## Global-scope user-defined variables (ERH)

In `*.ERH` you can declare global variables used from any ERB:

    #DIM MY_INT
    #DIMS MY_STR_ARRAY, 100

Header-scope keywords (engine-accurate):

- `SAVEDATA` — marks the variable as belonging to normal save data.
- `GLOBAL` — marks the variable as belonging to “global” storage (separate from normal save-load; typically saved/loaded by dedicated commands).
- `CHARADATA` — per-character storage (creates a character-data variable).

Header constraints:

- `STATIC` / `DYNAMIC` are not permitted in ERH declarations.
- `REF` is treated as “not implemented” for ERH and the header load fails if it is used.
- `GLOBAL` cannot be combined with `CHARADATA`.

Binary-save constraint (config-dependent):

- If `SAVEDATA` is used and `SystemSaveInBinary` is disabled:
  - string variables with dimension > 1 are rejected
  - any `CHARADATA` variable is rejected (in this codebase, regardless of element type)

ERH notes:

- ERH files are processed before ERB files.
- In this codebase, an enabled ERH line must start with `#` (any other leading character is a header load error).
- Only `#DEFINE` and `#DIM/#DIMS` are intended for ERH in this engine.
  - Unknown `#...` directives in ERH are treated as errors (they are not silently ignored).
  - `#FUNCTION/#FUNCTIONS` is recognized by the header loader but is currently **not implemented** here (it throws and fails header loading if used).

## Storage classes and reset boundaries (engine-accurate, language-adjacent)

Emuera’s variable semantics are tightly coupled to the engine’s notion of **storage classes** and “reset” operations.
These are not surface-level syntax, but they affect compatible runtime behavior (especially across “new game”, “load”, and “reset” actions).

### 1) Built-in local families

- `ARG/ARGS` and `LOCAL/LOCALS` are stored in per-function local-variable stores.
- They are cleared/reset by the engine when entering/leaving call frames and/or when the engine performs a “reset data” operation (exact call sites depend on built-ins; the storage behavior is described in `runtime-model.md`).

### 2) Built-in global families

- `GLOBAL` (numeric) and `GLOBALS` (string) are global arrays owned by the engine.
- Their values are **not** reset by the engine’s normal “reset data” operation; they are reset only by a dedicated “reset global” operation.

### 3) User-defined variables (how the engine categorizes them)

User-defined variables (`#DIM/#DIMS`) are categorized using the declaration keywords:

- **Private variables** (declared under `@LABEL` in ERB):
  - `STATIC` (default): stored in a global static list and persist across calls, but are reset by “reset data”.
  - `DYNAMIC`: allocated on function entry and discarded on function return (recursion-safe).
  - `REF`: has no storage of its own; it is bound/unbound during user-function argument binding.
- **Global variables** (declared in ERH):
  - no `GLOBAL` keyword: treated as “static (non-global)” user variables; reset by “reset data”.
  - `GLOBAL`: treated as “global user variables”; reset only by “reset global”.

In this codebase, the engine internally maintains separate lists for:

- “static non-global” user-defined variables (includes ERH non-`GLOBAL` vars and ERB `STATIC` private vars)
- user-defined global variables (ERH `GLOBAL`)
- user-defined save-data variables (those declared with `SAVEDATA`, split further into global vs non-global)

### 4) `SAVEDATA` / `GLOBAL` persistence boundaries (conceptual)

The `SAVEDATA` keyword does not change expression syntax; it changes which save/load streams include the variable.

High-level model:

- `SAVEDATA` (without `GLOBAL`): belongs to the normal save slot data.
- `GLOBAL` + `SAVEDATA`: belongs to the “global save” data (separate from normal save slot data).
- `GLOBAL` (without `SAVEDATA`): persists in memory across normal “reset data”, but is not necessarily persisted to disk unless dedicated global-save mechanisms are used.

This document only specifies how the engine partitions variable storage (and the reset/load boundaries).
The semantics of the save/load built-ins are documented in `builtins-reference.md`.
The on-disk file formats are specified in `save-files.md` (binary + legacy text).

### 5) `CHARADATA` variables

`CHARADATA` user-defined variables are stored per `CharacterData` entry.

- Their arrays are allocated when a character record is created.
- Their default values are the language defaults of the underlying arrays (numeric `0`, string `null` which reads as `""`).
- Whether/how they are persisted is part of the engine’s character save/load logic (deferred).

### 6) Reset and load boundaries (engine-accurate)

In this engine, “persistence” is not only “what gets written to disk”: it is also defined by which buckets are cleared by the built-in reset/load operations.

#### 6.1 `ResetData()` (normal reset) — what it clears

The engine’s normal reset operation does **not** reset `GLOBAL/GLOBALS`.

It performs these steps (in this order):

1) Remove “save-partition” EM extension data (`RemoveEMSaveData()`):
   - clears selected `DataStringMaps` entries
   - removes selected `DataXmlDocument` entries
   - clears selected `DataDataTables` entries
   The key sets are configured by `VarExt*.csv` (see `data-files.md`).
2) Reset local-variable stores and static user variables (`SetDefaultLocalValue()`):
   - resets all existing `LOCAL/LOCALS` and `ARG/ARGS` stores (keyed by function name)
   - resets all “static non-global” user-defined variables (ERH non-`GLOBAL` vars + ERB `STATIC` private vars)
3) Reset “non-global built-in variables” (`SetDefaultValue(constant)`):
   - clears most built-in variable arrays (numeric to `0`, string to `null`)
   - leaves `GLOBAL/GLOBALS` untouched
   - re-applies some engine defaults (notably `TARGET:0 = 1`, `ASSI:0 = -1`, and config-driven defaults like `PALAMLV`/`EXPLV`)
4) Dispose and clear the entire `CharacterList` (all characters are removed).

#### 6.2 `ResetGlobalData()` (global reset) — what it clears

The engine’s global reset operation affects **only** “global” buckets:

1) Remove “global-save” EM extension data (`RemoveEMGlobalData()`).
2) Remove “static” EM extension data (`RemoveEMStaticData()`).
3) Reset `GLOBAL/GLOBALS` and ERH `GLOBAL` user variables (`SetDefaultGlobalValue()`).

It does **not** reset other built-in variables or character data.

#### 6.3 Load-time clearing for EM extension data

When loading from disk, this codebase clears only the corresponding EM extension partition before reading:

- Normal slot load (`LoadFrom(...)`) clears only the “save” partition (`RemoveEMSaveData()`).
- Global load (`LoadGlobal()`) clears only the “global-save” partition (`RemoveEMGlobalData()`), and does not clear the “static” partition.

## Fact-check cross-refs (optional)

Primary sources used:

- Declaration parsing + keyword constraints: `emuera.em/Emuera/Runtime/Script/Data/UserDefinedVariable.cs`
- Name validity/conflict rules: `emuera.em/Emuera/Runtime/Script/Data/IdentifierDictionary.cs`
- Private scope allocation model: `emuera.em/Emuera/Runtime/Script/Statements/LogicalLine.cs`, `emuera.em/Emuera/Runtime/Script/Statements/Variable/VariableToken.cs`
- Storage partitioning + reset operations: `emuera.em/Emuera/Runtime/Script/Statements/Variable/VariableData.cs`, `emuera.em/Emuera/Runtime/Script/Statements/Variable/VariableEvaluator.cs`
- Character-data allocation for `CHARADATA`: `emuera.em/Emuera/Runtime/Script/Statements/Variable/CharacterData.cs`
