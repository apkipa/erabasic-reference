**Summary**
- Tries a list of candidate non-event functions and `CALL`s the first one that exists; otherwise skips the block.

**Syntax**
- `TRYCALLLIST`
  - `FUNC <formString> [, <arg1>, <arg2>, ... ]`
  - `FUNC <formString>(<arg1>, <arg2>, ... )`
  - `...`
  - `ENDFUNC`

**Arguments**
- None on `TRYCALLLIST` itself.
- Each `FUNC` item provides:
  - a candidate function name as a **FORM/formatted string expression** (evaluated to a string at runtime)
  - optional call arguments (expressions)

**Defaults / optional arguments**
- None.

**Semantics**
- Structural notes:
  - The lines between `TRYCALLLIST` and `ENDFUNC` are **list items**, not a normal executable block body.
  - Emuera stores the `FUNC` lines into an internal `callList` during load, and executes only `TRYCALLLIST` at runtime.
- Runtime algorithm:
  - For each `FUNC` item in source order:
    - Evaluate the candidate name to a string.
    - If no non-event `@function` with that name exists, try the next item.
    - Otherwise, bind arguments and enter that function (like `CALL`).
      - When the callee returns, execution resumes at the `ENDFUNC` line (then continues after it).
  - If no candidate matches, jump directly to the `ENDFUNC` line (then continue after it).
- Implementation detail: `FUNC` syntax is parsed using the same argument builder as `CALLFORM` (candidate name is a FORM string; arguments are normal expressions).

**Errors & validation**
- Load-time structure errors (the line is marked as error):
  - `TRYCALLLIST` cannot be nested inside another `TRY*LIST` block.
  - Only `FUNC` and `ENDFUNC` are allowed between `TRYCALLLIST` and `ENDFUNC`; any other instruction (and any label definition) is an error.
  - `FUNC`/`ENDFUNC` outside a matching `TRY*LIST ... ENDFUNC` block is an error.
- Runtime errors:
  - If a candidate name resolves to an event function (and `CompatiCallEvent` is not applicable here), it errors rather than trying the next item.
  - If a candidate function exists but is a user-defined expression function (`#FUNCTION/#FUNCTIONS`), it errors.
  - If argument binding fails (too many args, omitted required args, type conversion not permitted, invalid `REF` binding, etc.), it errors (it does **not** “try the next one”).

**Examples**
- `TRYCALLLIST`
- `  FUNC HOOK_%TARGET%, TARGET`
- `  FUNC HOOK_DEFAULT`
- `ENDFUNC`

**Progress state**
- complete
