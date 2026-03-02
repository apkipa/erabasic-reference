**Summary**
- Tries a list of candidate `CALL` targets and calls the first one that exists; otherwise does nothing.

**Syntax**
- `TRYCALLLIST`
  - `FUNC <formString> [, <arg1>, <arg2>, ... ]`
  - `FUNC <formString>(<arg1>, <arg2>, ... )`
  - `...`
  - `ENDFUNC`

**Arguments**
- None on `TRYCALLLIST` itself.
- Each `FUNC` item provides a function name (as a FORM string expression) and optional arguments.

**Defaults / optional arguments**
- None.

**Semantics**
- At runtime, evaluates each `FUNC` item in order:
  - Evaluates the candidate function name string.
  - If that function exists and is callable, binds arguments and calls it.
  - If not found, proceeds to the next `FUNC`.
- If no candidate is found, jumps to `ENDFUNC` (skipping the list body).

**Errors & validation**
- Only `FUNC` and `ENDFUNC` are valid inside the list; other instructions inside are warned about at load time.
- If a candidate function is found but argument binding fails, it errors (the instruction does not “try the next one” for binding/type errors).

**Examples**
- `TRYCALLLIST`
- `  FUNC "HOOK_%TARGET%", TARGET`
- `  FUNC "HOOK_DEFAULT"`
- `ENDFUNC`
