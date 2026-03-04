**Summary**
- List-item line inside `TRYCALLLIST` / `TRYJUMPLIST` / `TRYGOTOLIST` blocks.

**Tags**
- functions

**Syntax**
- Inside `TRYCALLLIST` / `TRYJUMPLIST`:
  - `FUNC <formString> [, <arg1>, <arg2>, ... ]`
  - `FUNC <formString>(<arg1>, <arg2>, ... )`
- Inside `TRYGOTOLIST`:
  - `FUNC <formString>`

**Arguments**
- `<formString>`: a FORM/formatted string expression evaluated to a function name or label name.
- `<argN>`: optional call arguments (not allowed for `TRYGOTOLIST`).

**Semantics**
- Not executed as a standalone statement.
- During load, Emuera collects `FUNC` lines into the surrounding `TRY*LIST` instruction’s internal `callList`.
- At runtime, the surrounding `TRY*LIST` evaluates these items in order (see `TRYCALLLIST` / `TRYJUMPLIST` / `TRYGOTOLIST`).
- Argument parsing is the same as `CALLFORM`: candidate name is a FORM string; call arguments are normal expressions.
- In `TRYCALLLIST` / `TRYJUMPLIST`, the optional `[...]` subname segment is parsed and stored, but it is not used when selecting/calling the function.

**Errors & validation**
- `FUNC` must appear only inside `TRY*LIST ... ENDFUNC`; otherwise it is a load-time error (the line is marked as error).

**Examples**
- `FUNC HOOK_%TARGET%, TARGET`

**Progress state**
- complete
