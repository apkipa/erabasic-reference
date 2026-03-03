**Summary**
- Like `CALLFORM`, but if the evaluated function name does not resolve to a function the instruction **does not error** and simply falls through.

**Syntax**
- `TRYCALLFORM <formString> [, <arg1>, <arg2>, ... ]`
- `TRYCALLFORM <formString>(<arg1>, <arg2>, ... )`

**Arguments**
- Same as `CALLFORM`.

**Defaults / optional arguments**
- Same as `CALLFORM`.

**Semantics**
- If the target function exists: behaves like `CALLFORM`.
- If not: does nothing (continues at the next line after `TRYCALLFORM`).

**Errors & validation**
- Still errors for invalid argument binding/type conversion when a function is found.

**Examples**
- `TRYCALLFORM "HOOK_%TARGET%"`

**Progress state**
- complete
