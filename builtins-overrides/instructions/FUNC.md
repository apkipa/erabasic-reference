**Summary**
- List-item line inside `TRYCALLLIST` / `TRYJUMPLIST` / `TRYGOTOLIST` blocks.

**Syntax**
- Inside `TRYCALLLIST` / `TRYJUMPLIST`:
  - `FUNC <formString> [, <arg1>, <arg2>, ... ]`
  - `FUNC <formString>(<arg1>, <arg2>, ... )`
- Inside `TRYGOTOLIST`:
  - `FUNC <formString>`

**Arguments**
- `<formString>`: a FORM/formatted string expression evaluated to a function name or label name.
- `<argN>`: optional call arguments (not allowed for `TRYGOTOLIST`).

**Defaults / optional arguments**
- None.

**Semantics**
- Not executed as a standalone statement.
- During load, Emuera collects `FUNC` lines into the surrounding `TRY*LIST` instruction’s internal `callList`.
- At runtime, the surrounding `TRY*LIST` evaluates these items in order (see `TRYCALLLIST` / `TRYJUMPLIST` / `TRYGOTOLIST`).
- Implementation detail: `FUNC` is parsed using the same argument builder as `CALLFORM`.
- Implementation detail: in `TRYCALLLIST` / `TRYJUMPLIST`, the optional `[...]` subname segment is parsed and stored, but the current runtime implementation does not use it when selecting/calling the function.

**Errors & validation**
- `FUNC` must appear only inside `TRY*LIST ... ENDFUNC`; otherwise it is a load-time error (the line is marked as error).

**Examples**
- `FUNC HOOK_%TARGET%, TARGET`

**Progress state**
- complete
