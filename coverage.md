# Coverage Plan (Reimplementable Core Spec)

Goal: a reader can reimplement a **fully compatible EraBasic parser + core interpreter** for this engine family *using only* `erabasic-reference/*`.

Scope (current phase): **core language** only.

- Included: loading order, preprocessing, lexing, parsing, expression evaluation, variables/scopes, user functions, control flow, runtime model for execution.
- Deferred: full semantics of all built-in commands/functions (UI/graphics/audio/input/save/etc.). We keep a catalog (`builtins*.md`) and will add semantics later in a controlled way.

This document tracks what is already specified vs what still needs to be written.

Legend:

- ✅ Spec complete (sufficient to implement + test)
- 🟡 Partially specified (needs edge cases / error conditions / exact phase ordering)
- ⛔ Not specified yet
- 🔁 Deferred (out of current phase)

## 1) Source of truth and versioning

- ✅ Engine codebase is `emuera.em` (EvilMask-flavored Emuera; also contains some Emuera.NET/EMEE-compat code paths).
- ✅ Documentation used for fact-checking is `emuera.em.doc` (English pages exist for `docs/Reference` entries).
- 🟡 Target “compatibility” must be pinned to specific commits/tags and to a config profile (many behaviors are config-dependent).

## 2) Input model (files, folders, load order)

- ✅ Folder layout assumptions (csv/ERH/ERB, subfolder loading rules, and filesystem case-sensitivity caveat).
- ✅ Load order and phase boundaries (CSV → rename/replace → ERH macros/vars → ERB).
- ✅ File encodings and newline normalization.
- 🟡 Error/warning behavior on duplicate definitions and missing references.

Where described today:

- `program-structure.md`
- `pipeline.md`
- `data-files.md`

## 3) Preprocessing

### 3.1 Line concatenation blocks (`{` … `}`)

- ✅ Syntax and basic rules.
- ✅ Interaction with comments and preprocessing (phase ordering in `lexical.md` and `preprocessor-and-macros.md`).
- ✅ Error conditions: invalid brace lines, nesting rejection, EOF handling.

Where described today:

- `lexical.md`

### 3.2 Comment processing

- ✅ `;` full-line and end-of-line comment concept.
- ✅ Special executable prefixes: `;!;`, `;#;`, `;^;`.
- ✅ Core rule for “why `;` is sometimes literal”: it depends on the instruction’s argument parsing mode (expression lexing vs FORM scanning vs raw-string slice).
- 🟡 Still missing: a complete per-built-in mapping table (which instructions use which argument parsing mode).

Where described today:

- `lexical.md`

### 3.3 Macro system (`#DEFINE`) and conditional blocks

- ✅ Macro expansion model: token-based, where expansion applies, recursion limit.
- ✅ Conditional inclusion blocks: `[IF]...[ENDIF]`, `[IF_DEBUG]`, `[IF_NDEBUG]`, and their interaction with line reading.
- ✅ `[SKIPSTART]...[SKIPEND]` handling (skip-forces-disabled, but directives still parsed).

Where described today:

- `preprocessor-and-macros.md` (engine-accurate)

## 4) Lexical rules (tokenization)

- ✅ Full delimiter set; exact identifier scanning rules.
- ✅ Whitespace rules, including full-width spaces and config gating.
- ✅ Numeric literal grammar (binary/hex/p/e forms, overflow behavior).
- ✅ String literal grammar, escapes, and unterminated literal errors.
- ✅ Operator scanning (including assignment operators like `'+='`, `'=`).

Where described today:

- `lexical.md` (user-facing behavior)
- `expressions.md` (operators summary)

## 5) Grammar: program and statement parsing

### 5.1 Function labels (`@...`)

- ✅ Label grammar (allowed chars, begin-with-digit rules, case-sensitivity).
- ✅ Duplicate labels, multi-definition ordering, and event grouping rules.
- 🟡 Interaction with “event function” categories and attributes (runtime meaning is partly in `runtime-model.md`).

Where described today:

- `program-structure.md`
- `labels.md`

### 5.2 `#` directives under labels

- ✅ Full directive set and constraints (where allowed, conflicts, precedence).
- ✅ Attribute semantics: `#ONLY`, `#FUNCTION/#FUNCTIONS`, `#PRI/#LATER/#SINGLE`, and `#LOCALSIZE/#LOCALSSIZE` (including engine quirks).

### 5.3 Statement list and block structures

- ✅ Canonical statement grammar for:
  - `IF/ELSEIF/ELSE/ENDIF`, `SIF`
  - `SELECTCASE/CASE/CASEELSE/ENDSELECT` (including `IS ...` and `a TO b` case conditions)
  - loops: `REPEAT/REND`, `FOR/NEXT`, `WHILE/WEND`, `DO/LOOP`
  - `BREAK/CONTINUE`
  - `CALL/JUMP/RETURN/RETURNFORM/RETURNF` interactions with `RESULT/RESULTS`
- 🟡 Error behavior on malformed blocks, cross-block jumps, and direct-entry via `GOTO/JUMP` into blocks.
  - ✅ Unstructured entry via `GOTO $label` (allowed) and the “advance-first” marker-skipping implications are specified (see `runtime-model.md` and `control-flow.md`).
  - 🟡 Still missing: a fully enumerated matrix of which malformed-nest situations become “error lines” vs warnings, and which ones can still run.

Where described today:

- `control-flow.md` (behavioral summary for main blocks)
- `functions.md` (CALL/RETURN family overview)

## 6) Expression language (core)

### 6.1 Types, coercions, and type errors

- ✅ Exact typing rules: int vs string; required-type contexts across core constructs.
- ✅ Conversion rules and config-controlled behaviors (notably user-function arg binding).

### 6.2 Operator semantics

- ✅ Full operator list and precedence/associativity as implemented.
- ✅ Short-circuit semantics (`&&`, `||`, `!&`, `!|`, ternary; `^^` does not short-circuit).
- ✅ Ternary operators (numeric `? #` and string `\@ ? # \@`), including parse rules and nesting.
- ✅ Increment/decrement (`++/--`) as statement and expression operators (variable-only, const rejection, prefix vs postfix result value).

### 6.3 String expressions and FORM syntax

- 🟡 Formal definition of “string expression” vs “raw string argument”.
- ✅ `%...%` and `{...}` interpolation grammar, compilation, and evaluation semantics.
- ✅ `@"..."` rules (FORM-in-string-expression literal) and `\@...\@` string-ternary literal form.
- ✅ Escape rules inside FORM literal segments.
- 🟡 Where FORM is accepted vs treated as literal text (command-category-dependent).

Where described today:

- `expressions.md` (high level)
- `formatted-strings.md` (engine-accurate)

## 7) Variables and storage model

### 7.1 Built-in variables (core semantics)

- ✅ `RESULT/RESULTS/COUNT` core behavior across calls/loops (RETURN/implicit return, REPEAT counter, null-string reads).
- ✅ Array indexing syntax with `:`; multi-dimensional indexing and omission/inference rules.
- ✅ Batch assignment (`A:i = v1,v2,...` / `A:i:j = ...`) including which elements are written and out-of-range behavior.
- ✅ Bounds checking and prohibited-variable errors (no config knobs observed for relaxing bounds checks).
- ✅ CSV-name indexing resolution rules and ambiguity rules.

### 7.2 User-defined variables

- ✅ `#DIM/#DIMS` declaration grammar (keywords, dimensions, initializers) and timing (ERH batch + ERB sharp lines).
- ✅ `DYNAMIC` lifetime and recursion behavior.
- ✅ `CONST` write-protection and interaction constraints.
- ✅ `REF` reference binding rules and mutation behavior (for user-function ref parameters).

### 7.3 Global scope (ERH variables)

- ✅ `SAVEDATA/GLOBAL/CHARADATA` storage partitioning and reset/load boundaries (engine-accurate). (On-disk IO formats and full save/load built-in semantics remain deferred.)

Where described today:

- `variables.md` (core rules + inference)
- `string-key-indexing.md` (engine-accurate mapping + runtime resolution)
- `control-flow.md` and `runtime-model.md` (`COUNT` + `RESULT` return semantics)

## 8) Function call model

- ✅ Call stack model and `RESULT/RESULTS` assignment boundaries.
- ✅ Argument binding (`ARG/ARGS`) including defaults and omitted args (including implicit defaults for some formals).
- ✅ Pass-by-reference via `REF` formal parameters.
- 🟡 Expression functions (`#FUNCTION/#FUNCTIONS`): call sites, restrictions, side-effect caveats, and disallowed instructions.
- 🟡 Error behavior on missing functions and labels (including `TRY*`, `TRYC*`, and `TRY*LIST`), calling event functions, and config-dependent relaxations.

Where described today:

- `functions.md` (high level)

## 9) Error/warning model (core)

- 🟡 Taxonomy of parse-time vs load-time vs runtime errors.
- 🟡 Warning vs error behavior for missing functions, reserved words, overrides, etc.
- ✅ Line/position reporting and how concatenated lines map to file locations.

Where described today:

- `errors-and-warnings.md` (core mechanics)
- `source-position-mapping.md` (engine-accurate file/line mapping rules)

## 10) Built-in commands/functions

- 🔁 Full semantics: deferred.
- ✅ Signature catalog for lookup: `appendix/tooling/builtins.md` and `appendix/tooling/builtins-signatures.md`.

## Next concrete deliverables (to reach “reimplementable core”)

1) ✅ Write a **phase-ordered pipeline spec**: `pipeline.md`.
2) ✅ Document **config + CSV formats** that affect parsing/runtime: `data-files.md`.
   - ✅ Catalog config keys, types, defaults: `config-items.md`.
3) 🟡 Write a **formal-ish grammar** for statements and expressions (EBNF + edge-case rules).
 - ✅ Statement-level grammar + block matching: `grammar.md`.
 - ✅ Expression grammar (EBNF + precedence): `expression-grammar.md`.
 - ✅ FORM/formatted-string subgrammar: `formatted-strings.md`.
4) ⛔ Define the **runtime model** for variables, call stack, and control-flow constructs.
   - 🟡 Core runtime model (stack, events, scopes): `runtime-model.md`.
5) ⛔ Add a **conformance test suite plan** (golden tests) that validates parsing + core execution without UI/audio/save.
