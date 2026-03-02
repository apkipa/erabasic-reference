# EraBasic Runtime Model (Emuera)

This document specifies the **core runtime behavior** needed to execute EraBasic scripts compatibly with this Emuera codebase.

It focuses on:

- function/label resolution (`@...`, `$...`)
- call stack behavior (`CALL`, `JUMP`, `RETURN`)
- event-function execution (`@EVENT...` with `#PRI/#LATER/#SINGLE/#ONLY`)
- user-defined expression functions (`#FUNCTION/#FUNCTIONS`)
- variable scope behavior that is essential for compatibility (especially `#DIM` private variables and `ARG/ARGS`)

UI, graphics, audio, save UI, and other “built-in command semantics” are intentionally not fully specified here (see `coverage.md` for scope tracking).

## 1) Executable unit: a linked list of logical lines

After loading and parsing, Emuera executes a **linked list** of `LogicalLine` objects per function body.

Important line kinds:

- `FunctionLabelLine` — the `@NAME` line that starts a function.
- `InstructionLine` — an instruction/assignment line with parsed arguments.
- `GotoLabelLine` — a `$NAME` line that declares a goto target within a function.
- `NullLine` — file boundary markers (start/end).
- `InvalidLine` / `InvalidLabelLine` — parse/load errors.

Note: an “assignment statement” (e.g. `A = 1`, `STR '= "x"`, `X++`) is also stored as an `InstructionLine`, implemented via a parser-internal pseudo instruction (`SETFunction`). See `grammar.md` for details.

### 1.1 Program counter update order (engine-accurate)

The engine’s main script loop updates the “program counter” in this order:

1) `ShiftNextLine()` (advance to `CurrentLine.NextLine`)
2) execute the resulting `CurrentLine`

Conceptually:

```text
while running:
  state.ShiftNextLine()
  execute(state.CurrentLine)
```

This means control-flow “jumps” typically target **marker lines** (labels, loop headers, `IF`/`CASE` markers):

- `JumpTo(marker)` sets `CurrentLine = marker`
- the next interpreter iteration executes `marker.NextLine`

So the marker line itself is usually not re-executed after a jump.

This ordering is crucial for loop semantics such as:

- `REPEAT` initializes `COUNT` once, while `REND` drives subsequent iterations by jumping to the `REPEAT` marker.
- `WHILE` checks the condition on entry, while `WEND` drives subsequent iterations by rechecking the stored expression and jumping to the `WHILE` marker.

### 1.2 Movement primitives

At the `ProcessState` level, the engine uses two movement primitives:

- **sequential advance**: `ShiftNextLine()` → `CurrentLine = CurrentLine.NextLine`
- **set marker**: `JumpTo(line)` → `CurrentLine = line`

### 1.3 Consequence: jumping *to* a line usually starts *after* it

Because execution always starts by calling `ShiftNextLine()`, control transfers have a distinctive property:

- If control sets `CurrentLine = X` (via `JumpTo(X)` or by entering a function with `CurrentLine = @LABEL`), the next executed line is usually `X.NextLine`.

This matters for two kinds of “marker lines”:

- `GotoLabelLine` (`$NAME`): it is never executed; it is a pure jump target.
- Many structural/control-flow `InstructionLine`s are intended to be *markers* (e.g. `ELSEIF`, `ELSE`, `CASE`, `REND`, `NEXT`, `WEND`, `LOOP`, `CATCH`).

Engine-accurate implications:

- When `IF` selects an `ELSEIF`/`ELSE` branch, it “jumps to the marker line”, which means execution begins at the marker’s **body** (`marker.NextLine`).
- When you jump *into* a control-flow construct using unstructured control transfer (typically `GOTO $label`), you can enter the middle of an `IF`/`SELECTCASE`/loop body without running the corresponding marker/header instruction first.
  - This is allowed by the engine (there is no “structured entry” enforcement).
  - It can change behavior (for example, entering a loop body without executing the header can leave loop-counter bindings unset; `REND/NEXT/CONTINUE` then exit the loop, while `BREAK` can throw due to a missing counter binding).

This “marker-skipping” model is an Emuera implementation detail, but it is required for compatibility with scripts that rely on it (intentionally or accidentally).

## 2) Labels: functions (`@`) and goto targets (`$`)

### 2.1 Function labels `@NAME`

- Each `@NAME` defines a function start label.
- Multiple `@NAME` labels with the same name may exist (especially for event functions).
- A function label may be tagged by following `#...` lines (see `grammar.md`), which affect:
  - whether the label is an event function group member,
  - whether it is an expression function (`#FUNCTION/#FUNCTIONS`),
  - private variable declarations (`#DIM/#DIMS`), and
  - local variable sizing directives (`#LOCALSIZE/#LOCALSSIZE`).

### 2.2 Goto labels `$NAME`

`$NAME` labels are **scoped to the containing function** (more precisely: to the current `FunctionLabelLine` at parse time).

Resolution rule:

- `GOTO $X` resolves `$X` relative to the **current function label line** using a `(labelName, parentFunction)` pair key.

This means the same `$LABEL` string in two different functions is two distinct goto targets.

## 3) Call stack: `CalledFunction` frames

The runtime maintains a stack of `CalledFunction` frames.

A frame contains (conceptually):

- `TopLabel`: the canonical function entry label for this call (non-event) or the first label in the current event function sequence
- `CurrentLabel`: the function label currently being executed (may change for event functions)
- `ReturnAddress`: where execution resumes after the call finishes
- `IsEvent`: whether this is an event-function call
- `IsJump`: whether this call is a `JUMP`-style call (does not return normally)

The `ProcessState.CurrentLine` is set to the frame’s `CurrentLabel` on entry.

### 3.0 The actual stack: `functionList` and `ScriptEnd`

Internally, the engine stores call frames in a `functionList` (a `List<CalledFunction>`).

- The **active frame** is `functionList[^1]` (top of stack).
- “Script end” is defined as `functionList.Count == currentMin` (not necessarily “stack is empty”; see §3.1).

When a call frame is entered (`IntoFunction(...)`):

- The frame is appended to `functionList`.
- `CurrentLine` is set to the callee’s `@LABEL` line (the marker), so the next interpreter iteration begins executing at `@LABEL.NextLine` due to the “ShiftNextLine before execute” model.

When a call frame finishes (`Return(...)` for normal functions/events, `ReturnF(...)` for expression functions):

- The engine pops one frame from `functionList` (with special handling for `IsJump`, see §4.2).
- `CurrentLine` is set to the caller’s return marker line (`ReturnAddress`), so the next iteration resumes at `ReturnAddress.NextLine`.

### 3.1 `currentMin`: a “do not pop below this” boundary

Internally, the engine also tracks an integer boundary `currentMin`.

Most of the time:

- `currentMin = 0`
- the active call stack is `functionList[0..]`

During user-defined expression function evaluation (`#FUNCTION/#FUNCTIONS`), the engine temporarily sets:

- `currentMin = functionList.Count` (the current depth)

and then runs the script loop for the method call. This ensures:

- the method’s internal frames can be pushed/popped without disturbing the outer (non-method) call frames
- “script end” for method evaluation means `functionList.Count == currentMin` rather than “stack is empty”

## 4) Calling non-event functions (`CALL` / `JUMP`) and returning (`RETURN`)

### 4.1 `CALL @NAME(...)`

Conceptually:

1) Resolve the function name to a **non-event** `FunctionLabelLine`.
2) Bind arguments into the callee’s formal parameters (`ARG/ARGS` or private vars, and `REF` parameters if any).
3) Push a `CalledFunction` frame with `ReturnAddress = current instruction line`.
4) Set `CurrentLine = callee.CurrentLabel` (the callee’s `@NAME` line), then continue.

If the target name resolves to an event function:

- the engine rejects it by default (“call to event function”), unless the compat toggle `CompatiCallEvent` is enabled (see §5.5).

### 4.2 `JUMP @NAME(...)`

`JUMP` is implemented as a call frame with `IsJump = true`.

Return behavior is different:

- When the callee executes `RETURN`, the engine immediately “returns again” to the caller of the caller (effectively skipping the immediate return address).

Engine-accurate consequence:

- The function that executed `JUMP` is also returned-from as part of this “double return” (using the same return value), so execution does not resume after the `JUMP` line.

In other words: `JUMP` does not preserve a usable return point for normal control flow.

### 4.3 `RETURN [values...]`

`RETURN` ends the current function call and sets the numeric `RESULT` family:

- With no arguments, `RESULT` is treated as `0`.
- With one or more integer expressions, the engine collects them into the `RESULT` array (`RESULT:0`, `RESULT:1`, …) and sets `RESULT` to `RESULT:0`.

Engine-accurate details:

- `RESULT` is an alias for `RESULT:0`.
- When `RETURN` has no arguments, it sets only `RESULT:0 = 0`; it does **not** clear `RESULT:1`, `RESULT:2`, etc.
- When `RETURN` has arguments, it writes `RESULT:i = value_i` for `i = 0..k-1` where `k` is the number of provided values, truncated to the physical `RESULT` array length.
  - Values beyond the array length are ignored.
  - Elements beyond `k-1` are left unchanged (not cleared).

Then:

- For non-event calls: the frame is popped and execution resumes at `ReturnAddress.NextLine`.
- For `JUMP` calls: the frame is popped and the engine immediately performs another return (propagating to the next return address up).

Note: `RETURNFORM` is a specialized variant that returns numeric values parsed from a string/formatted string; it still ends the function in the same way.

### 4.4 Expression-function return (`RETURNF`) does not assign `RESULT`

`RETURNF` is the dedicated “return” instruction for user-defined expression functions (`#FUNCTION/#FUNCTIONS`).

Engine-accurate behavior:

- `RETURNF` does **not** write `RESULT`/`RESULTS`.
- Instead it sets `ProcessState.MethodReturnValue` and pops exactly one “method call” frame (down to `currentMin`).

### 4.5 Implicit return at end of function

If execution “falls off the end” of a function body (the interpreter reaches the next `@LABEL` or file end without a `RETURN`):

- for non-method functions, the engine sets `RESULT:0 = 0` (via `VEvaluator.RESULT = 0`) and then returns
- it does not clear `RESULT:1+`
- for expression functions (`#FUNCTION/#FUNCTIONS`), it returns with `MethodReturnValue = null` (the expression evaluator then supplies the default `0` / `""`), and it does not assign `RESULT`

### 4.6 `RESULT` / `RESULTS` are global variables, not per-frame

`RESULT` (numeric) and `RESULTS` (string) are global engine variables.

- `RETURN` / `RETURNFORM` write only the numeric `RESULT` family.
- The engine does not automatically save/restore `RESULT`/`RESULTS` on function entry/exit.

So the observable “return value behavior” depends on which instructions explicitly write these variables.

## 5) Event functions (`@EVENT...`) and `#PRI/#LATER/#SINGLE/#ONLY`

### 5.1 Which names are “event functions”

Event-ness is determined by the function name matching a hard-coded set, including:

- `EVENTFIRST`, `EVENTTRAIN`, `EVENTSHOP`, `EVENTBUY`, `EVENTCOM`, `EVENTTURNEND`, `EVENTCOMEND`, `EVENTEND`, `EVENTLOAD`

Event functions are also treated as “system” labels by the loader. Exact naming rules (including other system-label names/patterns) are in `labels.md`.

### 5.2 Multiple definitions and grouping order

Event functions may be defined multiple times across files.

During the “sort labels” phase, Emuera groups all `@EVENT...` definitions of the same name into **four ordered groups**:

0) `#ONLY` group
1) `#PRI` group
2) “normal” group (neither `#PRI` nor `#LATER`)
3) `#LATER` group

If a label has both `#PRI` and `#LATER`, it appears in both groups.

### 5.3 Calling an event function (`CALLEVENT`)

Calling an event function produces a `CalledFunction` frame that iterates through the grouped label list.

The frame starts at group 0 and selects the first available label in the first non-empty group; then it proceeds through the groups in numeric order.

Engine constraint:

- Event calls cannot be nested. If an event call is attempted while any other event frame is still on the call stack, the engine throws an error.

### 5.4 Returning from event functions (`RETURN` value matters)

When an event-function label returns:

- If the current label is `#ONLY`: the entire event call finishes immediately.
- Else if the current label is `#SINGLE` and the return value is **exactly** `1`: the engine skips the rest of the current group and continues with the next group.
- Else: the engine proceeds to the next label within the current group; if the group is exhausted, it continues with the next group.

When all groups are exhausted, the event call finishes and returns to the original return address (like a non-event call).

### 5.5 Compatibility option: calling event functions as normal functions

If the config toggle `CompatiCallEvent` is enabled:

- the label dictionary also exposes the *first-defined* event label as a “non-event callable label”, ignoring event grouping and flags.

This emulates an EraMaker-compat behavior where event functions can be invoked like ordinary functions.

### 5.6 Attribute parse-time constraints (engine-accurate)

These `#` attributes are parsed only on `#...` lines immediately following a function label line:

- `#ONLY`, `#PRI`, `#LATER`, `#SINGLE`

Constraints and quirks:

- They are meaningful only on **event functions**. If used on a non-event function, the loader emits a warning and ignores them.
- They are not allowed on user-defined expression functions (`#FUNCTION/#FUNCTIONS`):
  - declaring `#FUNCTION/#FUNCTIONS` clears any previously declared `#PRI/#LATER/#SINGLE/#ONLY` on that label (with warnings).
- `#ONLY` is exclusive:
  - if a label is already marked `#PRI/#LATER/#SINGLE`, declaring `#ONLY` emits warnings and clears those flags.
  - if multiple definitions of the same event name declare `#ONLY`, the loader warns but still accepts them. (At runtime, the first `#ONLY` label reached ends the event call immediately, so later ones are typically unreachable.)

## 6) Arguments, defaults, and `REF` parameters

### 6.1 Formal parameters from `@NAME(...)`

Function labels may declare formal parameters using lvalue-like terms (typically `ARG:n` / `ARGS:n`), optionally with defaults.

At load time, these formals are stored in `FunctionLabelLine.Arg[]` and defaults in `FunctionLabelLine.Def[]`.

### 6.2 Call-site argument binding

At call time, Emuera builds a `UserDefinedFunctionArgument`:

- If too many arguments are provided: error.
- If an argument is omitted:
  - it is replaced by the formal’s default if present;
  - otherwise it is an error unless `CompatiFuncArgOptional` is enabled.
- If types mismatch:
  - string → int is always an error
  - int → string is an error unless `CompatiFuncArgAutoConvert` is enabled, in which case the engine wraps the argument with `TOSTR(...)`.

Evaluation and assignment order (engine-accurate):

- Actual argument expressions are evaluated in the **caller** context, left-to-right, and stored into a temporary “transporter” (`long[]`, `string[]`, `Array[]` for `REF`).
- Only after all actuals are evaluated does the engine enter the callee:
  - it scopes in the callee’s dynamic private variables (`TopLabel.ScopeIn()`), then
  - it assigns formals (`ARG/ARGS`, private vars, or `REF` bindings) from the transporter.
- If an argument is omitted and (via `CompatiFuncArgOptional`) no default is substituted, the corresponding formal lvalue is **not assigned** on entry (it retains its previous value in the underlying storage).

Important engine quirk: during signature parsing, the engine inserts an **implicit default** (`0` / `""`) for any parameter whose lvalue is `ARG:n`, `ARGS:n`, or a private variable *even if you did not write `= ...`*.
This means those parameters can be omitted at call sites without requiring `CompatiFuncArgOptional`.

### 6.3 `REF` parameters (pass-by-reference)

If a formal parameter is `REF`, the call-site argument must be a variable term that refers to an **array** (dimension > 0).

The engine then passes an `Array` reference to the callee, rather than copying values.

Additional constraints enforced by this codebase’s type checker:

- The actual argument must be a variable term (not an arbitrary expression).
- The actual argument must not be:
  - a pseudo/calculated variable
  - a `CONST` variable
  - a character-data variable (this engine path rejects chara vars for `REF` parameters)
- Integer vs string and the dimension count must match exactly.

Binding lifetime (engine-accurate):

- Private `REF` variables are “scoped” via `ScopeIn/ScopeOut` just like other dynamic private variables.
  - On function entry, the engine clears them to an **unbound** state (`array = null`) and pushes the previous binding (if any) to an internal stack.
  - The argument binder then assigns the new binding (`SetRef(actualArray)`).
  - On function exit, the engine restores the previous binding (or returns to unbound).

Implementation note: the argument transporter has a special case for character variables, but the `REF` parameter matcher is invoked with `allowChara=false`, so that path is normally unreachable in user-defined function calls.

## 7) Variable storage and scope (core)

EraBasic variable behavior is a large topic; this section only specifies the scope behavior that is essential to runtime compatibility.

### 7.1 Local variables: `LOCAL/LOCALS`, `ARG/ARGS`

Local-variable families are implemented as “local variable stores” keyed by function name:

- `ARG/ARGS` are resized during label sorting based on each function label’s declared/used argument indices.
- `LOCAL/LOCALS` have default sizes and can be overridden per function via `#LOCALSIZE/#LOCALSSIZE` for non-event functions.
  - In this codebase, `#LOCALSIZE/#LOCALSSIZE` on event functions are warned and ignored, so event functions effectively use the default sizes.

Important compatibility property:

- local-variable storage is associated with a function label name (and thus reused across calls), unless a different storage class is used (see private `DYNAMIC` variables below).

### 7.2 Function-private variables (`#DIM/#DIMS` inside ERB)

`#DIM/#DIMS` inside an ERB function declares **private variables** owned by that function label.

These private variables are stored in a per-label dictionary and have two important storage modes:

- **static** private variables: persist across calls
- **dynamic** private variables: allocated on function entry and discarded on function return (recursion-safe)

Mechanically, Emuera calls:

- `ScopeIn()` on function entry (allocates/activates dynamic private variables)
- `ScopeOut()` on function exit (deallocates/deactivates them)

This happens:

- for normal calls: around the call frame’s `TopLabel`
- for event calls: around each `CurrentLabel` as the event label iterator advances

### 7.3 Global user-defined variables (`#DIM/#DIMS` in ERH)

ERH-defined user variables exist outside any call frame and can be marked with persistence keywords like `SAVEDATA`, `GLOBAL`, and `CHARADATA`.

Their exact persistence and save/load semantics are out of scope for this doc, but their existence and name resolution affects parsing and execution.

## 8) User-defined expression functions (`#FUNCTION/#FUNCTIONS`)

Expression functions are user-defined functions that can be called from expressions, e.g. `FOO(1,2)`.

### 8.1 Resolution rule

When parsing an expression function call `NAME(...)`, Emuera resolves the name using:

- user-defined expression functions (`@NAME` with `#FUNCTION/#FUNCTIONS`) if labels are initialized, otherwise
- built-in expression functions (method list), otherwise
- it errors (with special messaging depending on whether a non-method user function exists).

### 8.2 Execution model

Evaluating a user-defined method term runs script code:

1) The engine increments a method call depth counter (`methodStack`) and errors if it exceeds a fixed limit (prevents stack overflow).
2) It temporarily sets a “minimum call depth boundary” so the method call’s internal frames can be popped without disturbing outer non-method frames.
3) It sets the method’s return address to the current executing line.
4) It enters the method function via `IntoFunction(...)` and runs the script interpreter loop until the method returns via `RETURNF` (or end-of-function return behavior).
5) The method return value is stored in `ProcessState.MethodReturnValue` and returned to the expression evaluator.

If the method returns no value (`RETURNF` with no expression, or falling off the end of the function), the expression evaluator uses a default:

- `0` for `#FUNCTION`
- `""` for `#FUNCTIONS`

### 8.3 “Method-safe” instruction restriction (engine-accurate)

This engine enforces a hard restriction on which instructions may appear inside `#FUNCTION/#FUNCTIONS` bodies.

During load, for each instruction line inside a method function:

- if the instruction’s metadata flag `METHOD_SAFE` is not set, the loader emits a warning and marks that line as an **error line** (so execution will fail if reached).

Consequences:

- `RETURN` / `RETURNFORM` are **not** method-safe in this codebase; methods must use `RETURNF`.
- Many other instruction families (notably UI/input/wait and normal `CALL`/`JUMP`) are also not method-safe.

This is an engine compatibility rule (not a general EraBasic language rule): a reimplementation targeting this engine must reproduce this restriction to match which scripts are accepted as valid.

## 9) Error and warning behavior (runtime-critical)

This codebase distinguishes:

- **warnings**: recorded and often printed during load; execution may proceed
- **errors** (`CodeEE`): abort the current instruction/function/method evaluation

Compatibility-critical toggle:

- `CompatiErrorLine`: when disabled, the engine exits to title after load if there were uninterpretable lines; when enabled, it continues into execution.

## Fact-check cross-refs (optional)

- Execution state and call stack mechanics: `emuera.em/Emuera/Runtime/Script/Process.State.cs`
- Call frames and argument binding: `emuera.em/Emuera/Runtime/Script/Process.CalledFunction.cs`
- User-defined method evaluation (`#FUNCTION`): `emuera.em/Emuera/Runtime/Script/Process.cs` (`GetValue`)
- Event grouping and label sorting: `emuera.em/Emuera/Runtime/Script/Data/LabelDictionary.cs`
- Private variable scoping hooks: `emuera.em/Emuera/Runtime/Script/Statements/LogicalLine.cs` (`FunctionLabelLine.ScopeIn/ScopeOut`)
