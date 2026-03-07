**Summary**
- Like `JUMPFORM`, but if the evaluated function name does not resolve to a function the instruction **does not error** and simply falls through.

**Tags**
- calls

**Syntax**
- `TRYJUMPFORM <formString>`
- `TRYJUMPFORM <formString>()`
- `TRYJUMPFORM <formString>, <arg1> [, <arg2> ... ]`
- `TRYJUMPFORM <formString>(<arg1> [, <arg2> ... ])`
- `TRYJUMPFORM <formString>[<subName1>, <subName2>, ...]`
- `TRYJUMPFORM <formString>[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`
- The bracket segment is accepted for compatibility, but is currently unused.

**Arguments**
- Same as `JUMPFORM`.

**Semantics**
- If the target function exists: behaves like `JUMPFORM`.
- If not: does nothing (continues at the next line after `TRYJUMPFORM`).

**Errors & validation**
- Still errors for invalid argument binding/type conversion when a function is found.

**Examples**
- `TRYJUMPFORM "OPTIONAL_%COUNT%"`

**Progress state**
- complete
