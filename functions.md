# Functions (CALL/RETURN, arguments, expression functions)

## Calling normal functions

Normal functions are defined by `@NAME` labels and called by commands such as:

- `CALL`, `CALLFORM`, `TRYCALL...`
- `JUMP`, `JUMPFORM`, etc.

### Call target tails: `NAME[subNames](args)` (engine behavior)

Many call-like built-ins parse their *target* with optional “tails”:

- `NAME` (each instruction defines whether this part is parsed as raw text or as a FORM string)
- optional bracket list: `[...]` (“subNames” in the engine)
- optional argument list: `(arg1, arg2, ...)` or comma form `, arg1, arg2, ...`

Engine-accurate notes:

- The `NAME` text is read up to one of: `(`, `[`, `,`, `;` (then trimmed of half-width spaces/tabs). `;` starts a comment.
- For the comma-form argument tail, only an empty field **between commas** creates an omitted/`null` slot:
  - `CALL X, a,,c` produces row arguments `[a, null, c]`
  - `CALL X, a,` does **not** produce an extra final omitted slot; it is parsed like one argument `[a]`
- In this Emuera codebase, the bracket list is **parsed and stored** on the call argument object as `SubNames`, but it is **not used for runtime dispatch**:
  - it does not change which `@NAME` / `$NAME` is selected,
  - and it is not evaluated at runtime (so it cannot cause runtime errors/side-effects by itself).
- Some constructs still enforce **loader-time constraints** using this parsed data. For example, `TRYGOTOLIST` explicitly forbids `[...]` (and also forbids an argument list).

### Load-time linking vs runtime resolution (compatibility-critical)

This engine performs a load-time “linking” pass over many control-flow instructions.

Key rule:

- If a call/jump/goto target name is a **compile-time constant** (including some `...FORM` cases where the FORM reduces to a constant), the loader resolves it during load.
  - If resolution fails and the instruction is not a `TRY*` form, the line is marked as an **error line** during load (execution will throw if reached).
  - Config item `FunctionNotFoundWarning` can suppress *printing* of the warning, but it does not prevent the line from becoming an error line.
- If the target name is **not** compile-time constant, the loader records that runtime target resolution is needed and defers resolution to runtime.
  - In that case, missing targets raise runtime errors for non-`TRY*` instructions, and are soft-fail for `TRY*`/`TRYC*` instructions.

These behaviors also interact with whole-program “function never called” checks; see `pipeline.md`.

### `CALL`

`CALL funcName` invokes a function label named `@funcName`.

- Execution transfers into the called function.
- When the called function ends, execution returns to the line after the `CALL`.
- If the function reaches its end without an explicit `RETURN`, `RESULT` becomes `0`.

## Calling expression functions as statements (`METHOD`-dispatch, `CALLF`, `TRYCALLF`)

Expression functions (built-in methods and user-defined `#FUNCTION/#FUNCTIONS`) are normally called inside expressions:

- `X = FOO(1, 2)`

This engine also supports statement-level method execution in three related forms:

1) **Statement-form method execution (keyword = method name)**

- If a line’s keyword matches a registered expression function name, the engine executes that function and writes:
  - numeric result → `RESULT`
  - string result → `RESULTS`
- This path exists only when no ordinary instruction keyword already owns that name.
- In the current engine, the auto-exposed statement-form names come from the built-in expression-method registry, not from user-defined `#FUNCTION/#FUNCTIONS`.
- Statement form parses the post-keyword tail as the normal top-level expression list to end-of-line, not as `CALLF`-style parenthesized argument syntax.
  - Valid standalone line: `TOSTR 42`
  - Valid standalone line: `TOSTR(42)` (`(42)` is just one grouped expression, not an ordinary function-call expression being used as a statement)
  - Invalid standalone line: `TOSTR(1, 2)` (the comma inside the parentheses is not a top-level argument separator here)
  - Invalid standalone line: `USER_FUNCTION()`

2) **`CALLF` / `CALLFORMF` (explicit method-name call)**

- `CALLF` / `CALLFORMF` resolve and evaluate an expression function by name.
- In this engine, these instructions **do not** assign the return value into `RESULT/RESULTS` (the value is computed and discarded).
  - Use expression-call form if you need the value in surrounding expression evaluation; built-in statement-form method execution also writes `RESULT` / `RESULTS`, but user-defined `#FUNCTION/#FUNCTIONS` are not auto-exposed through that path.

3) **`TRYCALLF` / `TRYCALLFORMF` (soft user-method call)**

- These resolve only **user-defined** expression functions (`#FUNCTION/#FUNCTIONS`). Built-in expression methods are not part of this lookup.
- If no callable user-defined expression function is resolved, the instruction is a no-op.
- Like `CALLF`, the return value is computed and discarded.

Examples:

```erabasic
TOSTR 12
; writes RESULTS = "12"

CALLF TOSTR, 12
; computes "12" but does not write RESULTS
```

```erabasic
@ADD1(ARG:0)
#FUNCTION
    RETURNF ARG:0 + 1

ADD1 41
; if no ordinary instruction named ADD1 exists, writes RESULT = 42

TRYCALLF ADD1, 41
; runs the user-defined method if it exists, but still does not write RESULT
```

Important boundary rule:

- The “try” behavior covers failure to resolve a callable user-defined method. It does **not** promise to swallow every later failure.
- In dynamic-name paths, wrong-kind targets and argument-binding failures can still throw.
- In constant-name fast paths, the loader may collapse some of those same resolution failures into the no-op outcome instead of deferring them to runtime.

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
- It does **not** catch “hard” resolution errors that throw immediately rather than returning “not found”:
  - calling an event function via normal `CALL` when config item `CompatiCallEvent` = `NO`
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

Compatibility detail:

- Even for `...FORM` variants, if the engine can fold the FORM into a constant at load time, it may still link the target during the load-time linking pass (so “target not found” can become a load-time error line rather than a runtime error).

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

## Resolution failures, wrong-kind calls, and compatibility switches

### Constant-target linking vs runtime lookup

This engine tries to resolve many call/jump targets during load when the target name is constant.

Observable consequences:

- Non-`TRY` `CALL` / `JUMP` / `GOTO` / `CALLF` lines with constant missing targets become **error lines** during load.
- Config item `FunctionNotFoundWarning` changes whether the warning text is printed, but it does **not** stop the line from becoming an error line.
- If the target name is not constant, resolution is deferred to runtime instead.

### Missing target vs wrong kind

This engine distinguishes “target not found” from “name exists but is the wrong callable kind”.

- Ordinary `CALL` / `JUMP` expect a normal `@function` label.
  - Missing normal function → non-TRY runtime error (or TRY soft-fail).
  - Name resolves only to an event function → hard wrong-kind error unless `CompatiCallEvent=YES` exposes a compatibility non-event entry point.
  - Name resolves to a user-defined expression function → hard wrong-kind error; use `CALLF` / `CALLFORMF` instead.
- Ordinary `GOTO` expects a valid local `$label` in the current function.
  - Missing label → non-TRY runtime error (or TRY soft-fail).
  - Invalid `$label` lines remain hard errors rather than TRY-soft-fail targets.
- `CALLF` / `CALLFORMF` expect an expression function.
  - Missing method → error.
  - Name resolves to a normal non-method `@function` → wrong-kind error.

### Event-call paths at a glance

There are three distinct ways an event-function name can be reached:

- **Host/system dispatch**: built-in phase flow can invoke event hooks such as `@EVENTFIRST` / `@EVENTTRAIN`; this uses event-dispatch semantics (see `system-flow.md` and `runtime-model.md` §5).
- **`CALLEVENT`**: script-side explicit event dispatch; this also uses event-dispatch semantics.
- **Ordinary `CALL` / `JUMP`**: these do **not** use event dispatch. By default they reject event-function targets; with `CompatiCallEvent=YES`, they instead call only the first-defined event label as a compatibility non-event entry point.

### `CompatiCallEvent`

`CompatiCallEvent` is the main compatibility switch that changes ordinary call resolution.

- When disabled, ordinary `CALL` / `JUMP` to an event-function name is a hard error.
- When enabled, the engine also exposes the first-defined event label through the ordinary non-event label lookup, so a normal call can reach it without event-group dispatch.

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
  - with `k` arguments, it sets `RESULT:i` for `0 <= i < k` (truncated to the physical `RESULT` length) and leaves all other cells unchanged

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

These rules describe the behavior of this engine; do not generalize them to other Emuera variants without re-checking.

## Arguments: `ARG` / `ARGS`

You can declare arguments on the function side and pass expressions on the call side:

    @FOOBAR, ARG:0, ARGS:0
        ; ...

    CALL FOOBAR, 123, "abc"

Notes:

- Numeric arguments accept numeric expressions; string arguments accept string expressions.
- Arguments can be omitted only when the formal has a default value (including an implicit default inserted for some formals) or when a compatibility option permits omission. See `runtime-model.md` for the exact binding rules used by this engine.
- Passing is *by value* by default.

### Omitted actuals vs explicit values

Do not confuse these cases:

- **omitted actual**: the caller leaves an argument slot empty,
- **explicit value**: the caller supplies a real value such as `0`, `""`, or some other expression.

For user-defined functions, an omitted actual is **not** treated as though the caller had explicitly written `0` or `""`.
The engine first keeps that slot as **absent**, then applies the callee's binding rules:

- if the formal has a default, that default is used,
- otherwise omission is an error unless config item `CompatiFuncArgOptional` is enabled,
- if omission is allowed without a default, the formal is left unchanged on entry rather than being auto-filled with a fresh `0` / `""`.

Only after this binding step does the callee observe a concrete value or reference binding.

A separate compatibility rule can auto-convert **explicit** integer actuals to strings for string formals (config item `CompatiFuncArgAutoConvert`).
That is **not** the same thing as omitted-argument handling.

Compatibility implication:

- “optional” does not automatically mean “equivalent to writing `0` / `""`”,
- and “empty string” is still a supplied string value, not an omitted argument.

### Definition syntax notes

- Parentheses around the argument list in the *definition* are optional in many Emuera setups (`@FUNC, ARG:0` vs `@FUNC(ARG:0)`).
- Parentheses are required when calling **expression functions** inside expressions; bare-name call syntax does not work there.

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

- A `REF` parameter must be a **private** variable declared with `#DIM REF` / `#DIMS REF` in the same function's post-label `#...` declaration block (see `variables.md`).
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
- In this engine, `RETURN` / `RETURNFORM` are not “method-safe” instructions, so using them inside `#FUNCTION/#FUNCTIONS` bodies is rejected during load (the line is marked as an error line). Use `RETURNF`.
- If a method reaches end-of-function without `RETURNF`, it returns the default value (`0` for `#FUNCTION`, `""` for `#FUNCTIONS`).

### Calling form

Expression-function calls inside expressions use `()` syntax:

    X = MYFUNC(1, 2)

The definition may use either:

    @MYFUNC(ARG:0, ARG:1)
    @MYFUNC, ARG:0, ARG:1

The definition form is engine-/style-dependent, but the *call* in an expression uses parentheses.

### Restrictions inside expression functions

Expression functions are checked line-by-line against the engine's **method-safe** instruction classification.

Shared contract:

- If an instruction inside a `#FUNCTION/#FUNCTIONS` body is not method-safe, the loader emits a warning and marks that line as an error line.
- So this is not just a style recommendation: an incompatible reimplementation would accept scripts that this engine rejects.

Main consequences:

- `RETURNF` is the method return instruction. `RETURN` and `RETURNFORM` are rejected here.
- Ordinary `CALL`, `JUMP`, `CALLEVENT`, and `BEGIN`-style host phase transitions are rejected here.
- Input/wait and other host-suspending instructions are rejected here.
- In practice, local control flow, ordinary assignments, array/variable helpers, many plain output instructions, and method-oriented calls such as expression-call form / `CALLF` / `TRYCALLF` remain usable.

### Side effects and evaluation caveats

Expression functions can still mutate state, but compatibility-sensitive code should assume only these ordering guarantees:

- expression operands are evaluated left-to-right,
- short-circuiting operators can skip later operands,
- load-time restructuring/constant folding can precompute constant subexpressions before runtime.

So a side effect placed inside an expression function call is **not** equivalent to “always runs exactly where the source text appears”.

### Execution-mode interactions

Two engine execution modes matter for calls that eventually reach output/input instructions:

- **print-skip mode** (`SKIPDISP` and internal host skip-print paths):
  - skips only instructions in the engine's print-like classification,
  - does **not** skip ordinary control flow, variable mutation, or function-call mechanics themselves,
  - in practice covers ordinary print/output instructions and wait/input instructions, while debug-only print instructions are excluded from this classification.
- **message skip** (`MesSkip`):
  - does not bypass ordinary function calls or control-flow on its own,
  - only changes the behavior of waits that explicitly consult it (see `input-flow.md`).

Compatibility consequence:

- a called function still runs under these modes, but its print-like instructions may be suppressed by print-skip, and its wait instructions may auto-advance only when that instruction family defines a `MesSkip` path.
- If user-controlled `SKIPDISP` reaches an input instruction, this engine errors rather than silently auto-accepting input.
