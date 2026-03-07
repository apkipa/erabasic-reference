**Summary**
- List-item line inside `TRYCALLLIST` / `TRYJUMPLIST` / `TRYGOTOLIST` blocks.

**Tags**
- functions

**Syntax**
- Inside `TRYCALLLIST` / `TRYJUMPLIST`:
  - `FUNC <formString>`
  - `FUNC <formString>()`
  - `FUNC <formString>, <arg1> [, <arg2> ... ]`
  - `FUNC <formString>(<arg1> [, <arg2> ... ])`
  - `FUNC <formString>[<subName1>, <subName2>, ...]`
  - `FUNC <formString>[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`
  - The bracket segment is accepted for compatibility, but is currently unused by `TRYCALLLIST` / `TRYJUMPLIST`.
- Inside `TRYGOTOLIST`:
  - `FUNC <formString>`

**Arguments**
- `<formString>` (FORM/formatted string): evaluated to a function name or label name.
- `<argN>` (optional, expression): call argument; not allowed for `TRYGOTOLIST`.
- `<subNameN>` (optional): only for `TRYCALLLIST` / `TRYJUMPLIST`; parsed from the bracket segment after `<formString>` and currently ignored.

**Semantics**
- Not executed as a standalone statement.
- During load, Emuera collects `FUNC` lines into a list owned by the surrounding `TRY*LIST` instruction.
- At runtime, the surrounding `TRY*LIST` evaluates these items in order (see `TRYCALLLIST` / `TRYJUMPLIST` / `TRYGOTOLIST`).
- Argument parsing is the same as `CALLFORM`: candidate name is a FORM string; call arguments are normal expressions.
- In `TRYCALLLIST` / `TRYJUMPLIST`, the optional `[...]` subname segment is parsed and stored, but it is not used when selecting/calling the function.

**Errors & validation**
- `FUNC` must appear only inside `TRY*LIST ... ENDFUNC`; otherwise it is a load-time error (the line is marked as error).

**Examples**
- `FUNC HOOK_%TARGET%, TARGET`

**Progress state**
- complete
