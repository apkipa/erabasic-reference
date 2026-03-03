# Functions (CALL/RETURN, arguments, expression functions)

## Calling normal functions

Normal functions are defined by `@NAME` labels and called by commands such as:

- `CALL`, `CALLFORM`, `TRYCALL...`
- `JUMP`, `JUMPFORM`, etc.

### Call target tails: `NAME[subNames](args)` (engine behavior)

Many call-like built-ins parse their *target* with optional “tails”:

- `NAME` (raw text or a FORM string, depending on the instruction)
- optional bracket list: `[...]` (“subNames” in the engine)
- optional argument list: `(arg1, arg2, ...)` or comma form `, arg1, arg2, ...`

Engine-accurate notes:

- The `NAME` text is read up to one of: `(`, `[`, `,`, `;` (then trimmed of half-width spaces/tabs). `;` starts a comment.
- In this Emuera codebase, the bracket list is **parsed and stored** on the call argument object as `SubNames`, but it is **not used for runtime dispatch**:
  - it does not change which `@NAME` / `$NAME` is selected,
  - and it is not evaluated at runtime (so it cannot cause runtime errors/side-effects by itself).
- Some constructs still enforce **loader-time constraints** using this parsed data. For example, `TRYGOTOLIST` explicitly forbids `[...]` (and also forbids an argument list).

### `CALL`

`CALL funcName` invokes a function label named `@funcName`.

- Execution transfers into the called function.
- When the called function ends, execution returns to the line after the `CALL`.
- If the function reaches its end without an explicit `RETURN`, `RESULT` becomes `0`.

## Calling expression functions as statements (`METHOD`-dispatch and `CALLF`)

Expression functions (built-in methods and user-defined `#FUNCTION/#FUNCTIONS`) are normally called inside expressions:

- `X = FOO(1, 2)`

This engine also supports statement-style invocation in two different ways:

1) **Statement-form method execution (keyword = method name)**

- If a line’s keyword matches a registered expression function name, the engine executes that function and writes:
  - numeric result → `RESULT`
  - string result → `RESULTS`
- This is available only when the method name is also registered as an instruction keyword (no conflict with an existing instruction keyword).

2) **`CALLF` / `CALLFORMF` (explicit method-name call)**

- `CALLF` / `CALLFORMF` resolve and evaluate an expression function by name.
- In this codebase, these instructions **do not** assign the return value into `RESULT/RESULTS` (the value is computed and discarded).
  - Use expression-call form (assignment) if you need the value.

## “Try” call/jump/goto variants (`TRY*` and `TRYC*`)

This engine implements two “soft failure” families for `CALL`/`JUMP`/`GOTO`.

### 1) `TRY...` (no catch block)

Examples:

    TRYCALL FOO
    TRYJUMP BAR
    TRYGOTO $LABEL

Semantics (engine-accurate):

- If the target function/label **does not exist**, the instruction does **nothing** and execution continues with the next line.
- If the target exists, it behaves like the corresponding non-TRY instruction (`CALL`/`JUMP`/`GOTO`).

Important limitations (engine behavior, not just “spec advice”):

- `TRY*` does **not** catch runtime errors thrown while executing the called function body.
- It does **not** catch “hard” resolution errors that are thrown as `CodeEE` rather than returning “not found”:
  - calling an event function via normal `CALL` when `CompatiCallEvent=NO`
  - calling a user-defined expression function (`#FUNCTION/#FUNCTIONS`) via `CALL` (must use `CALLF`/`CALLFORMF`)
  - jumping to an *invalid* `$` label (a `$` label line that was itself invalid)

### 2) `TRYC... CATCH ... ENDCATCH` (missing-target catch block)

Examples:

```text
TRYCCALL FOO
    ; success path continues to next line
CATCH
    ; runs only if @FOO was not found (or $ label not found for TRYCGOTO)
ENDCATCH
```

Engine-accurate semantics:

- `TRYC*` is a structural marker that must be paired with `CATCH` and `ENDCATCH` (see `grammar.md`).
- If the target exists, the `TRYC*` instruction behaves like the corresponding non-TRY instruction and then control reaches the `CATCH` marker line, which skips the catch body.
- If the target does not exist:
  - the engine jumps to the `CATCH` marker line (so execution begins at the catch body), and
  - after the catch body, execution continues after `ENDCATCH`.

The catch block is specifically for “target not found” cases:

- `TRYCCALL` / `TRYCJUMP` / `TRYCCALLFORM` / `TRYCJUMPFORM`: only the “function label not defined” case enters the catch.
- `TRYCGOTO` / `TRYCGOTOFORM`: only the “$ label not defined in this function” case enters the catch.

Just like `TRY*`, `TRYC*` does not catch runtime errors thrown after the target was resolved.

### 3) FORM-name variants

For `...FORM` variants (`CALLFORM`, `TRYCCALLFORM`, `TRYCGOTOFORM`, etc.), the target name is obtained by evaluating a formatted string first.
See `formatted-strings.md` for FORM scanning rules.

### 4) “Try list” blocks: `TRYCALLLIST` / `TRYJUMPLIST` / `TRYGOTOLIST`

These are block-structured “try multiple targets” forms.

Shape:

```text
TRYCALLLIST        ; or TRYJUMPLIST / TRYGOTOLIST
    FUNC <target>  ; repeated
    FUNC <target>
ENDFUNC
```

Engine-accurate semantics:

- The engine evaluates each `FUNC` target in order and selects the **first** one that resolves:
  - `TRYCALLLIST`: first existing `@function` is called (normal call).
  - `TRYJUMPLIST`: first existing `@function` is entered as a `JUMP` call.
  - `TRYGOTOLIST`: first existing `$label` in the *current function* is jumped to (local goto).
- If no `FUNC` target resolves, the engine continues after `ENDFUNC`.

Engine-accurate parsing constraints:

- These blocks are not nestable; nesting emits an error.
- Inside the block, only `FUNC` lines and `ENDFUNC` are allowed.
- Each `FUNC` line uses the same call-target parsing shape as `CALLFORM`-family targets (it reads a target up to `(`, `[`, `,`, or `;` and can use FORM syntax in the target name).
- For `TRYGOTOLIST`, each `FUNC` line must specify only a bare target (no subnames `[...]` and no argument list).

## `RETURN` and results

When a function ends:

- If it reaches end-of-function without `RETURN`, `RESULT` becomes `0`.
- If it executes `RETURN ...`, it assigns values into `RESULT` (and `RESULT:n`) and terminates the function.

### Multiple return values

`RETURN` can set multiple numeric return values:

    RETURN 5, 7, 3

This assigns:

- `RESULT:0 = 5`
- `RESULT:1 = 7`
- `RESULT:2 = 3`

Engine-accurate notes:

- `RESULT` is an alias for `RESULT:0`.
- `RETURN` does **not** clear `RESULT:1+`:
  - with no arguments, it sets only `RESULT:0 = 0`
  - with `k` arguments, it sets `RESULT:i` for `i=0..k-1` (truncated to the physical `RESULT` length) and leaves all other cells unchanged

### `RETURNFORM`

`RETURNFORM` is a variant that parses its argument as a *formatted string* first, then returns the parsed result as if by `RETURN`.

Engine-accurate behavior:

- The engine first evaluates the FORM argument to a single string.
- It then parses that string as a comma-separated list of **integer expressions** (each segment is lexed as an expression).
  - After each comma, it skips only half-width spaces (`' '`), not tabs.
- The resulting values are assigned into `RESULT:0`, `RESULT:1`, ... (without clearing any remaining cells), and the function returns normally.
- If the resulting list is empty, it returns `0`.

Important detail: in `RETURNFORM`, `%` is treated as “start of a string expression / FORM content”, not the modulo operator. So:

    RETURN A % 100      ; OK (modulo)
    RETURNFORM A % 100  ; parses as string/FORM, not modulo

Because these are engine commands, exact parsing edge cases depend on the engine version/config.

## Arguments: `ARG` / `ARGS`

You can declare arguments on the function side and pass expressions on the call side:

    @FOOBAR, ARG:0, ARGS:0
        ; ...

    CALL FOOBAR, 123, "abc"

Notes:

- Numeric arguments accept numeric expressions; string arguments accept string expressions.
- Arguments can be omitted only when the formal has a default value (including an implicit default inserted for some formals) or when a compatibility option permits omission. See `runtime-model.md` for the exact binding rules used by this engine.
- Passing is *by value* by default.

### Definition syntax notes

- Parentheses around the argument list in the *definition* are optional in many Emuera setups (`@FUNC, ARG:0` vs `@FUNC(ARG:0)`).
- Parentheses are required when calling **expression functions** inside expressions (see below).

### Default values

You can set default values for `ARG/ARGS` and `#DIM/#DIMS` private variables used as parameters:

    @FUNC, ARG:0 = 111, ARGS:0 = "kaki"

Default values must be constants/constant strings.

Implicit defaults (engine quirk):

- If a parameter lvalue is `ARG:n`, `ARGS:n`, or a **private variable**, then omitting `= ...` still gives it an implicit default:
  - numeric → `0`
  - string → `""`
- For other parameter lvalues, `= ...` is forbidden and omission at the call site requires `CompatiFuncArgOptional=YES`.

### Pass-by-reference (via `REF`)

This engine supports pass-by-reference for user-defined functions via `REF`-typed parameters.

Typical pattern:

    @TEST(R)
    #DIM REF R
    R = 100
    RETURN

Rules (engine-accurate):

- A `REF` parameter must be a **private** variable declared with `#DIM REF` / `#DIMS REF` immediately after the label (see `variables.md`).
- In the label signature, a `REF` parameter is written as that variable name (no subscript is required for `REF` parameters).
- At the call site, the corresponding actual argument must be a **variable term** (not an arbitrary expression).
- The actual argument’s variable must have `Dimension != 0` (i.e. it must be an array-like variable; many built-in scalar variables cannot be passed by ref).
- Type and dimension must match:
  - numeric `REF` parameters only accept numeric variables
  - string `REF` parameters only accept string variables
  - 1D/2D/3D must match exactly
- The actual argument cannot be:
  - a pseudo/calculated variable
  - a `CONST` variable
  - a character-data variable (this engine path rejects chara vars for `REF` params)

Binding behavior:

- On function entry, the engine binds the `REF` parameter to the actual argument’s underlying array.
- Using a `REF` variable while it is unbound raises an “empty ref var” error (this can happen if argument binding failed earlier, or for non-parameter `REF` variables).

## Expression functions (`#FUNCTION` / `#FUNCTIONS`)

You can define user functions callable inside expressions:

- `#FUNCTION` — returns numeric (`Int64` / `long`)
- `#FUNCTIONS` — returns string (`string`)

They are primarily called from expressions:

    X = GET_CFLAG(TARGET, 0)
    STR = %GET_NAME(TARGET)%

Returning:

- `RETURNF` is the dedicated “return from expression function” instruction.
- In this codebase, `RETURN` / `RETURNFORM` are not “method-safe” instructions, so using them inside `#FUNCTION/#FUNCTIONS` bodies is rejected during load (the line is marked as an error line). Use `RETURNF`.
- If a method reaches end-of-function without `RETURNF`, it returns the default value (`0` for `#FUNCTION`, `""` for `#FUNCTIONS`).

### Calling form

Expression-function calls inside expressions use `()` syntax:

    X = MYFUNC(1, 2)

The definition may use either:

    @MYFUNC(ARG:0, ARG:1)
    @MYFUNC, ARG:0, ARG:1

depending on style and engine rules, but the *call* in an expression uses parentheses.

### Restrictions inside expression functions

Expression functions have restrictions to keep expressions safe/deterministic:

- They cannot be called via normal `CALL` (but can be invoked via `CALLF`/`CALLFORMF`).
- Some commands (input/wait, normal function calls) are disallowed and raise errors.
- Avoid side effects; while most expression evaluation is effectively left-to-right, the engine performs restructuring/constant-folding during load, and short-circuiting operators (`&&`, `||`, `!&`, `!|`, ternary) can skip evaluations.

## Fact-check cross-refs (optional)

- `emuera.em.doc/docs/Reference/CALL.en.md`
- `emuera.em.doc/docs/Reference/RETURN.en.md`
- `emuera.em.doc/docs/Emuera/function.en.md`
- `emuera.em.doc/docs/Emuera/user_defined_variables.en.md`
- `emuera.em.doc/docs/Emuera/user_defined_in_expression_function.en.md`
- Engine source of truth: `runtime-model.md`
- Implementation reference (try-family): `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs` (`CALL_Instruction`, `GOTO_Instruction`, `CATCH_Instruction`), `emuera.em/Emuera/Runtime/Script/Loader/ErbLoader.cs` (`nestCheck` pairing)
