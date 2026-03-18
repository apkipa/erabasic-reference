**Summary**
- Calls a C# plugin method (from `Plugins/*.dll`) by name.

**Tags**
- plugins

**Syntax**
- `CALLSHARP <methodName>`
- `CALLSHARP <methodName>()`
- `CALLSHARP <methodName>, <arg1> [, <arg2> ... ]`
- `CALLSHARP <methodName>(<arg1> [, <arg2> ... ])`
- `CALLSHARP <methodName>[<subName1>, <subName2>, ...]`
- `CALLSHARP <methodName>[<subName1>, <subName2>, ...](<arg1> [, <arg2> ... ])`

**Arguments**
- `<methodName>` (raw string token): matched against the registered plugin method name.
- `<argN>` (optional, expression): each occurrence is evaluated and passed to the plugin as either a string or an integer.
- `<subNameN>` (optional): values parsed from the bracket segment accepted by the parser for compatibility.
  - The current implementation accepts and stores them, but they do not affect plugin-method lookup or invocation.

**Semantics**
- `CALLSHARP` resolves `<methodName>` to a plugin method registered by the plugin system and calls it.
- `<methodName>` is not an expression:
  - It is parsed as raw text up to the first `(`, `[`, `,`, or `;`, then trimmed.
  - Backslash escapes are processed while parsing the raw token (e.g. `\s` = space, `\t` = tab, and `\,` can be used to include a comma in the name).
  - Quotation marks are not special here; `CALLSHARP "X"` looks for a method literally named `"X"`.
- Argument passing:
  - Each `<argN>` is evaluated before the plugin is invoked.
  - If `<argN>` is a string expression, the plugin receives a string value; otherwise it receives an integer value.
- Write-back (out/ref-like behavior):
  - After the plugin returns, any `<argN>` that is a variable term is assigned a new value from the plugin’s corresponding argument slot.
  - Non-variable arguments (constants, computed expressions, etc.) are not written back.
- Optional bracket segment:
  - The parser accepts `CALLSHARP <methodName>[...]` in the same “subname” shape as `CALL/CALLF`.
  - This bracket segment is ignored by `CALLSHARP`: it is parsed for compatibility, but not evaluated and not passed to the plugin.

**Errors & validation**
- If `<methodName>` is empty: load-time error.
- If `<methodName>` does not match any registered plugin method:
  - The engine emits a load-time warning.
  - Executing the instruction still fails at runtime (missing method binding).
- If an argument position is left empty (e.g. `CALLSHARP M, , 1`): runtime error.
- If the plugin throws an exception: runtime error.

Method-name case sensitivity follows config item `IgnoreCase`:
- If `IgnoreCase = true`, plugin methods are looked up case-insensitively.
- Otherwise, method names are case-sensitive.

See `plugins.md` for how plugins are discovered/loaded and how methods are registered.

**Examples**
- `CALLSHARP MyMethod`
- `CALLSHARP MyMethod, 123, "abc", X, S`
- `CALLSHARP MyMethod(X, S)` (equivalent argument parsing)

**Progress state**
- complete
