# Labels and Name Resolution (engine-accurate)

This document specifies how this engine parses and resolves:

- function labels (`@NAME`)
- local jump labels (`$NAME`)

It also specifies how multi-defined labels are ordered and grouped.

## 1) Case-sensitivity (config-dependent)

Most label dictionaries follow the engine's current identifier-comparison mode:

- If config item `IgnoreCase` = `YES`, label lookup is **case-insensitive** (ordinal ignore-case).
- If `IgnoreCase=NO`, label lookup is **case-sensitive** (ordinal).

This affects:

- whether `@FOO` and `@foo` are the same label
- how duplicates are detected
- how `$` labels are resolved within a function

## 2) Function label names (`@NAME`)

### 2.1 Tokenization and “name characters”

The label name is parsed as an **identifier token** (see `lexical.md`).

Practically:

- it stops at whitespace and at punctuation/operator delimiters (see `lexical.md` for the delimiter set)
- characters like `-`, `.`, `:`, `@`, `$`, `#`, `?`, `;`, quotes/brackets/braces, and operator symbols are not part of identifiers in this engine

### 2.2 Validity checks and warnings

After parsing `NAME`, the engine validates it:

- If the name is empty, it is an **error** (invalid label).
- If the name contains any “bad symbol” character, it is an **error** (invalid label).
  - The forbidden set is engine-defined and includes: operator symbols (`+ - * / % = ! < > | & ^ ~`), whitespace (` `, `\t`), quotes, brackets/braces/parentheses, `, . : \\ @ $ # ? ; '`.
  - This means many non-ASCII letters (including Japanese) are allowed as long as they don’t contain those symbols.
- If the name begins with a **half-width digit**, the engine emits a warning (level 0) but still accepts the label.
  - “Half-width” is detected via the engine’s legacy byte-length routine (`LangManager.GetStrlenLang`): full-width digits do not trigger this warning.

If config item `WarnFunctionOverloading` is enabled, the engine also checks for collisions with built-ins and reserved words:

- Reserved words (e.g. `IS`, `TO`, `INT`, `STR`, `STATIC`, `DYNAMIC`, `GLOBAL`, `SAVEDATA`, `CHARADATA`, `REF`, etc.)
- Built-in expression functions (methods)
- Built-in instructions
- Built-in variables
- User-defined macros / ref-functions

Collision outcomes when `WarnFunctionOverloading=YES`:

- **Reserved word**: warning if config item `AllowFunctionOverloading` = `YES`, error if `AllowFunctionOverloading=NO`.
- **Built-in expression function** (system method): warning if `AllowFunctionOverloading=YES`, error if `AllowFunctionOverloading=NO`.
- **Built-in variable**: warning (never fatal here).
- **Built-in instruction**: warning (never fatal here).
- **User macro**: error (should normally be unreachable if preprocessing/lexing succeeded, but is treated as fatal anyway).
- **User ref-function**: error.

### 2.3 Optional bracket tail: `@NAME[...]` (parsed, then discarded)

After `@NAME`, the loader can also accept a bracket list `[...]` before the normal signature separator (`,` or `(`).

Engine-accurate behavior:

- This bracket list is sometimes called “subNames” in the engine.
- It is **validated** at load time, but then discarded, so it has **no runtime effect** on which label is called.
- The bracket list must be **non-empty**, and each element must be a **constant term** (non-constant expressions are rejected).
- Event functions (`@EVENT...`) do not parse any signature content at all: any trailing tokens (including `[...]`) cause a warning and are ignored for argument-binding purposes.

## 3) Event functions vs normal functions

Some label names are treated as “event functions” by name.

Event label names (engine built-in set):

- `EVENTFIRST`
- `EVENTTRAIN`
- `EVENTSHOP`
- `EVENTBUY`
- `EVENTCOM`
- `EVENTTURNEND`
- `EVENTCOMEND`
- `EVENTEND`
- `EVENTLOAD`

These labels are treated as event functions even if you write them like normal `@NAME` labels.

`event function` is a narrower classification than `system label`. Event functions participate in event dispatch (`CALLEVENT` and host-triggered event hooks), while other system labels such as `@SHOW_SHOP` or `@SYSTEM_TITLE` are special entry points but are not event-dispatch targets.

Other label names are “system labels” (engine built-in names plus regex-matched names). They are not necessarily event labels; they are just recognized as special names by the engine:

- `SHOW_STATUS`
- `SHOW_USERCOM`
- `USERCOM`
- `SOURCE_CHECK`
- `CALLTRAINEND`
- `SHOW_JUEL`
- `SHOW_ABLUP_SELECT`
- `USERABLUP`
- `SHOW_SHOP`
- `SAVEINFO`
- `USERSHOP`
- `TITLE_LOADGAME`
- `SYSTEM_AUTOSAVE`
- `SYSTEM_TITLE`
- `SYSTEM_LOADEND`
- Regex patterns:
  - `COM` + digits (e.g. `COM1`, `COM23`)
  - `COM_ABLE` + digits (e.g. `COM_ABLE0`)
  - `ABLUP` + digits (e.g. `ABLUP12`)

System labels are parsed like normal labels; the “system” classification mainly affects how the engine routes certain built-in flows (outside the core language).

## 4) Multi-definition ordering and selection

The engine may see multiple `@NAME` definitions across ERB files.

### 4.1 Stable order key

For a given `@NAME`, all definitions are sorted by:

1) file load index (`FileIndex`), which depends on ERB load order
2) source line number in that file (`Position.LineNo`)
3) encounter index within the load (`Index`)

So “first-defined” means the earliest according to that ordering.

### 4.2 Normal (non-event) functions

- The engine chooses the **first-defined** definition as the callable target for `CALL @NAME` / `JUMP @NAME`.
- Later definitions with the same name are ignored for normal calls. If config item `WarnNormalFunctionOverloading` = `YES` (or analysis mode is active), the loader emits a level-1 warning when a non-event function name is defined more than once.

### 4.3 Event functions: grouping by `#` attributes

Event functions can have multiple definitions. The engine groups them into up to 4 ordered groups:

0) `#ONLY` group (labels where `#ONLY` was specified)
1) `#PRI` group
2) “normal” group (neither `#PRI` nor `#LATER`)
3) `#LATER` group

Important quirks:

- `#PRI` and `#LATER` are **not exclusive**: a label with both is included in both groups (EraMaker-compatible behavior).
- `#ONLY` clears `#PRI/#LATER/#SINGLE` on that label at parse time (each with a warning).
  - Because `#ONLY` implies neither `#PRI` nor `#LATER`, the label is included in both:
    - group 0 (`#ONLY` list), and
    - group 2 (“normal” list; the engine adds any label that is neither `#PRI` nor `#LATER`).
  - Runtime event iteration stops immediately after returning from a `#ONLY` label, so the “normal group” inclusion never results in a second execution during normal event dispatch (see `runtime-model.md`).
- Within each group, labels are processed in the stable “first-defined” ordering used for label registration.
- If multiple definitions of the same event label name specify `#ONLY`, the loader emits a level-1 warning but still accepts them.

The runtime meaning of these attributes (and how `RETURN` values affect event iteration) is specified in `runtime-model.md`.

### 4.4 Compatibility behavior of config item `CompatiCallEvent`

If `CompatiCallEvent=YES`, the engine also exposes the first-defined event label as a “non-event callable label”, and `CALL @EVENTTRAIN` behaves like calling a normal function (ignoring event groups and flags).

## 5) Local jump labels (`$NAME`)

`$` labels are “local labels” used for `GOTO`-like jumps.

Key rule: `$` labels are **scoped to the surrounding function**.

Mechanically, the engine stores `$NAME` as a mapping:

    (LabelName, ParentFunctionLabel) -> GotoLabelLine

Consequences:

- The same `$NAME` can be used in different functions without conflict.
- Defining the same `$NAME` twice within the same function emits a warning (level 2) and keeps the first-defined label as the target.
- `$` labels are parsed as identifiers; if extra tokens follow `$NAME` on the same line, the engine warns that the label “has arguments”.
