**Summary**
- List-item line inside `TRYCALLLIST` / `TRYJUMPLIST` / `TRYGOTOLIST`.

**Syntax**
- Inside `TRYCALLLIST` / `TRYJUMPLIST`:
  - `FUNC <formString> [, <arg1>, <arg2>, ... ]`
  - `FUNC <formString>(<arg1>, <arg2>, ... )`
- Inside `TRYGOTOLIST`:
  - `FUNC <formString>`

**Arguments**
- `<formString>`: FORM/formatted string evaluated to a function name or label name.
- `<argN>`: optional call arguments (not allowed for `TRYGOTOLIST`).

**Defaults / optional arguments**
- None.

**Semantics**
- Not executed directly as a standalone control-flow statement; it is consumed by the surrounding `TRY*LIST` construct.

**Errors & validation**
- `FUNC` outside a `TRY*LIST ... ENDFUNC` block produces a load-time warning.

**Examples**
- `FUNC "HOOK_%TARGET%", TARGET`
