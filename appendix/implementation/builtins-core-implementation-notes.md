# Built-ins (Implementation-Oriented Notes: Core Control Flow)

This document is a **readable, implementation-oriented** companion to:

- `control-flow.md` (spec-facing control-flow rules)
- `runtime-model.md` (execution + stack model)
- `../tooling/builtins-engine-metadata.md` (engine registration metadata)

It describes **how Emuera (EvilMask/Emuera) roughly implements** the core control-flow / call / return instructions.

Important:

- This file is **not** trying to be perfectly normative. Where it is incomplete, it tries to remain *non-misleading* and still support a “roughly compatible” reimplementation.
- Engine cross-refs are provided only for fact-check. The explanations below are self-contained.

## Covered instructions (core)

Conditionals:

- `IF` / `ELSEIF` / `ELSE` / `ENDIF` — multi-branch conditional using marker lines and loader-wired jump anchors
- `SIF` — single-line conditional that executes or skips the next *logical* line
- `SELECTCASE` / `CASE` / `CASEELSE` / `ENDSELECT` — switch-like selection (integer or string selector)

Loops:

- `REPEAT` / `REND` — counted loop using the system variable `COUNT`
- `FOR` / `NEXT` — for-like loop with explicit counter/bounds/step
- `WHILE` / `WEND` — condition-controlled loop
- `DO` / `LOOP` — do-loop with condition at `LOOP`
- `BREAK` / `CONTINUE` — loop control (with engine-specific counter/anchor behavior)

Calls / jumps / returns:

- `CALL` / `CALLFORM` — call a user-defined `@LABEL` function (with optional arguments)
- `JUMP` / `JUMPFORM` — call a function, but return “past the caller” when the callee returns
- `GOTO` / `GOTOFORM` — jump to a `$label` within the current function
- `RETURN` / `RETURNFORM` — return from a function and set `RESULT` (and `RESULT_ARRAY`)
- `RETURNF` — return from a `#FUNCTION/#FUNCTIONS` body (user-defined expression function)

Try-family (sketch only):

- `TRY*`, `CATCH`, `ENDCATCH` — try variants of call/jump with optional catch blocks

## Call target syntax: `name[subNames](args)` (what are “subNames”?)

Several built-ins share the same “call target” parsing shape for the *target name* and optional tails:

- a target `name` (either raw string text or FORM-parsed string, depending on the built-in)
- an optional bracket list: `[...]` (called “subNames” in the engine)
- an optional argument list: `(arg1, arg2, ...)` or a comma form `, arg1, arg2, ...` depending on the built-in

In this codebase, **subNames are mostly parsed but not used for runtime dispatch**:

- Call-site parsing (`CALL*`/`GOTO*`/`JUMP*`/`CALLF*`) stores `SubNames` on the argument object, but the runtime call/jump implementations do not consult it for selecting a different callee.
- Definition-site parsing for `@LABEL[...]` exists, but the loader currently does not attach the parsed subNames onto the label object (it is left as a commented-out TODO).

Practical consequence: treat `[...]` as a syntactic feature that may trigger **loader-time validation** in a few places (for example, it is explicitly forbidden in some list-style constructs), but do not assume it changes which function/label is called in this engine.

## 0) Key execution-model fact that explains many “weird jumps”

In this engine, the script interpreter loop advances to the *next* logical line **before** executing anything:

- Each iteration begins with “move to `CurrentLine.NextLine`”, then executes that new `CurrentLine`.

As a consequence, **`JumpTo(X)` does not execute line `X`**. It sets `CurrentLine = X`, and then the next interpreter iteration immediately advances to `X.NextLine` and executes *that*.

Practical mental model:

- Many control-flow “marker” lines (`ENDIF`, `WEND`, `REND`, `NEXT`, `DO`, `CASE`, `ELSEIF`, …) exist largely as **anchors** you jump *to*, so that execution resumes *after* them.

## 1) Common data carried on instruction lines

Several core instructions rely on fields attached to `InstructionLine` nodes (built during load):

- `InstructionLine.JumpTo`: “anchor” to jump to (meaning execution resumes at `JumpTo.NextLine`)
- `InstructionLine.IfCaseList`: `IF` and `SELECTCASE` store an ordered list of case-marker lines
- `InstructionLine.LoopCounter`, `LoopEnd`, `LoopStep`: loop bookkeeping stored on the loop’s *start marker line* (`REPEAT`/`FOR`)
- `InstructionLine.JumpToEndCatch`: `TRYC*`/`CATCH` pairing uses this for try/catch control-flow

## 2) `IF` / `ELSEIF` / `ELSE` / `ENDIF`

### Load-time wiring (rough)

- When the loader sees `IF`, it pushes it on a nesting stack and creates `IfCaseList = [IF]`.
- Each following `ELSEIF`/`ELSE` appends itself to that same `IfCaseList`.
- When the loader sees `ENDIF`, it:
  - pops the matching `IF`
  - sets `JumpTo` of **every** case-marker line in `IfCaseList` (`IF`, each `ELSEIF`, and `ELSE`) to the `ENDIF` anchor

Consequences:

- All “case marker” lines know where the end of the whole `IF` chain is (`ENDIF`).
- Reaching a later case marker “from above” means “skip the rest”.

### Runtime behavior (rough)

- `IF expr`
  - evaluates each case condition in order (`IF`, then each `ELSEIF`) until one is true
  - if none are true, it selects `ELSE` if present, otherwise `ENDIF`
  - it then `JumpTo(selectedCaseMarker)` so execution resumes **at the first line of that case body**
- `ELSEIF` / `ELSE`
  - do **not** evaluate anything when reached sequentially
  - they immediately `JumpTo(ENDIF)` (because some earlier case already ran and “fell through” into them)
- `ENDIF`
  - is a marker; its instruction body is effectively a no-op

## 3) `SIF` (single-line IF)

### Load-time checks

During load, `SIF` inspects the **next logical line** and emits errors for cases that would make its “skip exactly one logical line” semantics ambiguous or unsafe, notably:

- nothing after `SIF`
- a label line after `SIF`
- a “partial/marker” instruction after `SIF` (e.g. `ENDIF`, `CASE`, …)

### Runtime behavior

- `SIF expr`
  - if `expr` is non-zero, execution continues normally to the next logical line
  - if `expr` is zero, it performs an extra “advance to next line” so that the *next* interpreter iteration executes the line **after** the next logical line

Net effect: “skip exactly one logical line” (in the engine’s `LogicalLine` chain), not necessarily “skip one physical source line”.

## 4) `SELECTCASE` / `CASE` / `CASEELSE` / `ENDSELECT`

### Load-time wiring + type checks (rough)

- `SELECTCASE` pushes itself on a nesting stack and starts an `IfCaseList` containing subsequent `CASE`/`CASEELSE` marker lines.
- `ENDSELECT`:
  - pops and wires `SELECTCASE.JumpTo = ENDSELECT` (the “no match” anchor)
  - sets `JumpTo = ENDSELECT` on every `CASE`/`CASEELSE` marker line (so they can “skip the rest” when reached sequentially)
  - checks that each `CASE` expression’s operand type matches the `SELECTCASE` selector’s operand type, and warns/errors if not
  - warns/errors if `SELECTCASE` has a missing selector, or if a `CASE` has no case expressions

### Runtime behavior (rough)

- `SELECTCASE selectorExpr`
  - evaluates the selector once (either integer-typed or string-typed)
  - scans `IfCaseList` in order:
    - if it finds `CASEELSE`, it becomes the default match
    - for each `CASE`, it evaluates its `CaseExpression` list and picks the first `CASE` that matches
  - then `JumpTo(chosenCaseMarker)` (or `ENDSELECT` if none match), so execution resumes at the first line of that case body
- `CASE` / `CASEELSE`
  - act like `ELSEIF`/`ELSE` markers when reached sequentially: they immediately jump to `ENDSELECT`
- `ENDSELECT`
  - is a marker; its instruction body is effectively a no-op

## 5) `REPEAT` / `REND` and `FOR` / `NEXT`

### Argument shape (rough)

This engine represents both as a normalized “for-like” loop with:

- a counter variable term (`LoopCounter`)
- a start value
- an end value (treated as an exclusive bound)
- a step value

`FOR` supplies these explicitly.

`REPEAT n` is implemented by a special-case in the integer-expression argument builder that rewrites it into a normalized loop:

- counter = system variable `COUNT`
- start = `0`
- end = `n`
- step = `1`

### Load-time wiring + restrictions (rough)

- The loader pairs `REPEAT` ↔ `REND` and `FOR` ↔ `NEXT` and wires:
  - `StartMarker.JumpTo = EndMarker`
  - `EndMarker.JumpTo = StartMarker`
- It emits warnings for certain nest patterns, including “nested `REPEAT`”.
  (There are also special warnings around nesting `REPEAT` inside a `FOR` that uses `COUNT` as its loop variable.)

### Runtime behavior (rough)

- `REPEAT` / `FOR` (start marker)
  - initializes loop bookkeeping on the *start marker line object*:
    - stores `LoopCounter`, `LoopEnd`, `LoopStep`
    - assigns `LoopCounter = start`
  - if the loop has at least one iteration remaining, it falls through into the body
  - otherwise it `JumpTo(EndMarker)` so that execution resumes **after** the end marker (loop body is skipped)

Iteration check used by this engine:

- step > 0: continue if `LoopCounter < LoopEnd`
- step < 0: continue if `LoopCounter > LoopEnd`

- `REND` / `NEXT` (end marker)
  - increments `LoopCounter += LoopStep`
  - if the loop still has iterations remaining, it `JumpTo(StartMarker)` so execution resumes at the top of the body again
  - otherwise it falls through, so execution continues after the end marker

## 6) `WHILE` / `WEND`

### Load-time wiring (rough)

- The loader pairs `WHILE` ↔ `WEND` and wires:
  - `WHILE.JumpTo = WEND` (exit anchor)
  - `WEND.JumpTo = WHILE` (loop-back anchor)

### Runtime behavior (rough)

- `WHILE expr`
  - if `expr` is non-zero: enter body (fall through)
  - if `expr` is zero: `JumpTo(WEND)` so execution resumes after `WEND` (exit loop)
- `WEND`
  - re-evaluates the `WHILE` condition (via the stored `WHILE` line’s parsed expression)
  - if it is non-zero: `JumpTo(WHILE)` so execution resumes at the top of the body again
  - otherwise falls through (exit loop)

## 7) `DO` / `LOOP`

### Load-time wiring (rough)

- The loader pairs `DO` ↔ `LOOP` and wires:
  - `DO.JumpTo = LOOP`
  - `LOOP.JumpTo = DO`

### Runtime behavior (rough)

- `DO`
  - is a marker; its instruction body is effectively a no-op
- `LOOP expr`
  - if `expr` is non-zero: `JumpTo(DO)` so execution resumes after `DO` (continue loop)
  - otherwise falls through (exit loop)

## 8) `BREAK` / `CONTINUE`

### Load-time wiring (rough)

On load, `BREAK` and `CONTINUE` locate the nearest open loop on the nesting stack (`REPEAT`/`FOR`/`WHILE`/`DO`) and set:

- `BREAK.JumpTo = LoopStartMarker`
- `CONTINUE.JumpTo = LoopStartMarker`

### Runtime behavior (rough)

These are implemented in terms of “jump to an anchor, then resume at `anchor.NextLine`”.

- For `REPEAT`/`FOR`:
  - both `BREAK` and `CONTINUE` increment `LoopCounter += LoopStep` first (this matches legacy behavior where `COUNT` advances on break/continue)
  - `BREAK` jumps to the end marker anchor so execution resumes after the loop
  - `CONTINUE` either:
    - jumps to the loop start marker anchor (resume at top of body) if iterations remain, or
    - jumps to the end marker anchor (resume after loop) if not
- For `WHILE`:
  - `BREAK` exits by jumping to the `WEND` anchor
  - `CONTINUE` re-checks the `WHILE` condition and either continues or exits
- For `DO`:
  - `BREAK` exits by jumping to the `LOOP` anchor (so execution resumes after `LOOP`)
  - `CONTINUE` is special-cased to evaluate the `LOOP` condition line and choose whether to jump back to `DO` or exit

## 9) `CALL` / `CALLFORM` / `JUMP` / `JUMPFORM` (user-defined functions)

These instructions are implemented by a shared instruction class that:

- parses a label/function name (constant or expression)
- optionally parses argument expressions
- resolves to a `CalledFunction` (top label, return address, event-ness, etc.)
- enters that called function by pushing a frame

### Compile-time (load-time) optimization for constant calls

If the target name is a constant string at load time, the loader tries to pre-resolve:

- the called label (`func.JumpTo = call.TopLabel`) as an anchor
- a converted argument binding (`UserDefinedFunctionArgument`) for the call site

If the call cannot be resolved and the instruction is not a try-family, the loader records an error for that line.

### Runtime behavior (rough)

- `CALL*`/`JUMP*`:
  - resolves the target at runtime if not constant, and converts arguments if needed
  - calls `IntoFunction(...)` which:
    - sets up argument transporters (including pass-by-reference array binding)
    - assigns callee `ARG/ARGS` variables
    - pushes the `CalledFunction` onto the call stack
    - sets the interpreter’s current line anchor to the callee’s label line

### `JUMP` is “call + immediate-return-on-RETURN”

The difference between `CALL` and `JUMP` is encoded as a boolean (`IsJump`) on the `CalledFunction` frame:

- For normal `CALL`, `RETURN` returns to the caller’s return address.
- For `JUMP`, when the callee `RETURN`s, the engine pops the callee frame and then immediately performs another return out of the caller as well (so control does not resume at the original call site).

This is an engine behavior you can reproduce without building a structured AST: it is driven by a runtime call-stack flag.

## 10) `GOTO` / `GOTOFORM` (local `$...` labels)

`GOTO*` is a **within-function** jump to a `$label` (a `GotoLabelLine`).

- If the label name is constant, it can be pre-resolved at load time and stored in `InstructionLine.JumpTo`.
- Otherwise, the label name expression is evaluated at runtime and resolved against the currently executing function frame.

If the label cannot be found:

- non-try variants error
- try variants jump to the active `CATCH`/`ENDCATCH` anchor when applicable (see the try-family section below)

## 11) `RETURN` / `RETURNFORM` (script functions) vs `RETURNF` (methods)

### `RETURN` / `RETURNFORM`

`RETURN` and `RETURNFORM` are “function return” instructions for normal `@LABEL` functions.

They both set `RESULT`/`RESULT_ARRAY` (via `SetResultX(...)`) and then return from the current function frame.

Roughly:

- `RETURN`:
  - parses 0 or more integer expressions
  - if none: `RESULT = 0`
  - else: sets `RESULT_ARRAY[0..]` and `RESULT` (the first element)
  - returns from the current function frame
- `RETURNFORM`:
  - evaluates a string (FORM context)
  - re-lexes that string and parses it as a comma-separated list of integer expressions
  - sets `RESULT_ARRAY` and `RESULT` similarly to `RETURN`
  - returns from the current function frame

### `RETURNF`

`RETURNF` is for `#FUNCTION/#FUNCTIONS` bodies (user-defined expression functions, “methods”).

At load time, the engine warns if:

- `RETURNF` is used outside a method function, or
- the return value’s inferred operand type does not match the method’s declared type

At runtime, it returns a `SingleTerm` value to the method evaluator (separate from the normal `RESULT`-based return path).

## 12) Try-family (high-level sketch)

This engine has try variants of some control-transfer operations (`TRYCALL*`, `TRYGOTO*`, `TRYJUMP*`, plus “try/catch” forms like `TRYCCALL*`, `TRYCGOTO*`, … paired with `CATCH`/`ENDCATCH`).

High-level idea:

- Non-try: unresolved target => error
- Try: unresolved target => instead of error, either:
  - do nothing and continue, or
  - if inside a `TRYC* ... CATCH ... ENDCATCH` block, jump to the `CATCH`/`ENDCATCH` anchor

For exact pairing and allowed nesting, see `control-flow.md` and `../tooling/builtins-engine-metadata.md` (`IS_TRY`, `IS_TRYC`, `PARTIAL`, and `Match End`/`Parent` columns).

## 13) Remaining instruction keywords (catalog)

This section lists the **remaining** statement keywords registered by the engine that are *not* explained in detail above.

What this catalog is (for now):

- A non-normative, implementation-oriented **index** you can use to locate the engine entrypoint (`AInstruction` class) and the argument parsing shape (`FunctionArgType` / `ArgumentBuilder`).
- It is intentionally light on semantics until the per-instruction writeups are expanded.

How to read each entry:

- `arg: FunctionArgType.X (Some_ArgumentBuilder)` means argument parsing is implemented by that builder class.
- `arg: AInstruction: Some_Instruction` means the instruction class owns parsing and/or execution (often it still sets `ArgBuilder`).
- `flags: ...` are `FunctionIdentifier` instruction metadata flags (e.g. `FLOW_CONTROL`, `METHOD_SAFE`, `PARTIAL`, `IS_PRINT`, `IS_INPUT`, `IS_JUMP`, `IS_TRY`, `IS_TRYC`, `FORCE_SETARG`, `DEBUG_FUNC`, `IS_PRINTDATA`).
- `match-end` / `parent` reflect loader-level block pairing tables (`funcMatch` / `funcParent`).

- `ADDCHARA` — arg: AInstruction: ADDCHARA_Instruction; flags: METHOD_SAFE
- `ADDCOPYCHARA` — arg: AInstruction: ADDCOPYCHARA_Instruction; flags: METHOD_SAFE
- `ADDDEFCHARA` — arg: FunctionArgType.VOID (VOID_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `ADDSPCHARA` — arg: AInstruction: ADDCHARA_Instruction; flags: METHOD_SAFE
- `ADDVOIDCHARA` — arg: AInstruction: ADDVOIDCHARA_Instruction; flags: EXTENDED \| METHOD_SAFE
- `ALIGNMENT` — arg: FunctionArgType.STR (STR_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `ARRAYCOPY` — arg: FunctionArgType.SP_COPY_ARRAY (SP_COPY_ARRAY_Arguments); flags: EXTENDED \| METHOD_SAFE
- `ARRAYREMOVE` — arg: FunctionArgType.SP_CONTROL_ARRAY (SP_CONTROL_ARRAY_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `ARRAYSHIFT` — arg: FunctionArgType.SP_SHIFT_ARRAY (SP_SHIFT_ARRAY_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `ARRAYSORT` — arg: FunctionArgType.SP_SORTARRAY (SP_SORT_ARRAY_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `ASSERT` — arg: FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE \| DEBUG_FUNC
- `AWAIT` — arg: AInstruction: AWAIT_Instruction; flags: EXTENDED
- `BAR` — arg: AInstruction: BAR_Instruction; flags: EXTENDED \| METHOD_SAFE \| IS_PRINT
- `BARL` — arg: AInstruction: BAR_Instruction; flags: EXTENDED \| METHOD_SAFE \| IS_PRINT
- `BEGIN` — arg: AInstruction: BEGIN_Instruction; flags: FLOW_CONTROL
- `BINPUT` — arg: AInstruction: BINPUT_Instruction; flags: IS_PRINT \| IS_INPUT
- `BINPUTS` — arg: AInstruction: BINPUTS_Instruction; flags: IS_PRINT \| IS_INPUT
- `CALLEVENT` — arg: AInstruction: CALLEVENT_Instruction; flags: FLOW_CONTROL \| EXTENDED
- `CALLF` — arg: AInstruction: CALLF_Instruction; flags: EXTENDED \| METHOD_SAFE \| FORCE_SETARG
- `CALLFORMF` — arg: AInstruction: CALLF_Instruction; flags: EXTENDED \| METHOD_SAFE \| FORCE_SETARG
- `CALLSHARP` — arg: AInstruction: CALLSHARP_Instruction; flags: EXTENDED \| METHOD_SAFE \| FORCE_SETARG
- `CALLTRAIN` — arg: FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder); flags: FLOW_CONTROL \| EXTENDED
- `CATCH` — arg: AInstruction: CATCH_Instruction; flags: FLOW_CONTROL \| EXTENDED \| METHOD_SAFE \| PARTIAL; match-end: `ENDCATCH`
- `CLEARBGIMAGE` — arg: AInstruction: CLEARBGIMAGE_Instruction; flags: EXTENDED \| METHOD_SAFE
- `CLEARBIT` — arg: AInstruction: SETBIT_Instruction; flags: EXTENDED \| METHOD_SAFE
- `CLEARLINE` — arg: AInstruction: CLEARLINE_Instruction; flags: EXTENDED \| METHOD_SAFE \| IS_PRINT
- `CLEARTEXTBOX` — arg: FunctionArgType.VOID (VOID_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `COPYCHARA` — arg: AInstruction: COPYCHARA_Instruction; flags: EXTENDED \| METHOD_SAFE
- `CUPCHECK` — arg: FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `CUSTOMDRAWLINE` — arg: AInstruction: CUSTOMDRAWLINE_Instruction; flags: EXTENDED \| METHOD_SAFE
- `CVARSET` — arg: AInstruction: CVARSET_Instruction; flags: EXTENDED \| METHOD_SAFE
- `DATA` — arg: FunctionArgType.STR_NULLABLE (STR_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE \| PARTIAL
- `DATAFORM` — arg: FunctionArgType.FORM_STR_NULLABLE (FORM_STR_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE \| PARTIAL
- `DATALIST` — arg: FunctionArgType.VOID (VOID_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE \| PARTIAL; match-end: `ENDLIST`
- `DEBUGCLEAR` — arg: AInstruction: DEBUGCLEAR_Instruction; flags: EXTENDED \| METHOD_SAFE \| DEBUG_FUNC
- `DEBUGPRINT` — arg: AInstruction: DEBUGPRINT_Instruction; flags: EXTENDED \| METHOD_SAFE \| DEBUG_FUNC
- `DEBUGPRINTFORM` — arg: AInstruction: DEBUGPRINT_Instruction; flags: EXTENDED \| METHOD_SAFE \| DEBUG_FUNC
- `DEBUGPRINTFORML` — arg: AInstruction: DEBUGPRINT_Instruction; flags: EXTENDED \| METHOD_SAFE \| DEBUG_FUNC
- `DEBUGPRINTL` — arg: AInstruction: DEBUGPRINT_Instruction; flags: EXTENDED \| METHOD_SAFE \| DEBUG_FUNC
- `DELALLCHARA` — arg: FunctionArgType.VOID (VOID_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `DELCHARA` — arg: AInstruction: ADDCHARA_Instruction; flags: METHOD_SAFE
- `DELDATA` — arg: AInstruction: DELDATA_Instruction; flags: EXTENDED \| METHOD_SAFE
- `DOTRAIN` — arg: FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder); flags: FLOW_CONTROL \| EXTENDED
- `DRAWLINE` — arg: FunctionArgType.VOID (VOID_ArgumentBuilder); flags: METHOD_SAFE
- `DRAWLINEFORM` — arg: FunctionArgType.FORM_STR (FORM_STR_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `DT_COLUMN_OPTIONS` — arg: AInstruction: DT_COLUMN_OPTIONS_Instruction; flags: EXTENDED \| METHOD_SAFE
- `DUMPRAND` — arg: AInstruction: DUMPRAND_Instruction; flags: EXTENDED \| METHOD_SAFE
- `ENCODETOUNI` — arg: FunctionArgType.FORM_STR_NULLABLE (FORM_STR_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `ENDCATCH` — arg: AInstruction: ENDIF_Instruction; flags: FLOW_CONTROL \| EXTENDED \| METHOD_SAFE \| PARTIAL \| FORCE_SETARG
- `ENDDATA` — arg: AInstruction: DO_NOTHING_Instruction; flags: EXTENDED \| METHOD_SAFE \| PARTIAL
- `ENDFUNC` — arg: AInstruction: ENDIF_Instruction; flags: FLOW_CONTROL \| EXTENDED \| PARTIAL \| FORCE_SETARG
- `ENDLIST` — arg: FunctionArgType.VOID (VOID_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE \| PARTIAL
- `ENDNOSKIP` — arg: FunctionArgType.VOID (VOID_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE \| PARTIAL
- `FONTBOLD` — arg: AInstruction: FONTBOLD_Instruction; flags: EXTENDED \| METHOD_SAFE
- `FONTITALIC` — arg: AInstruction: FONTITALIC_Instruction; flags: EXTENDED \| METHOD_SAFE
- `FONTREGULAR` — arg: AInstruction: FONTREGULAR_Instruction; flags: EXTENDED \| METHOD_SAFE
- `FONTSTYLE` — arg: FunctionArgType.INT_EXPRESSION_NULLABLE (INT_EXPRESSION_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `FORCEKANA` — arg: FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `FORCEWAIT` — arg: AInstruction: WAIT_Instruction; flags: IS_PRINT
- `FORCE_BEGIN` — arg: AInstruction: FORCE_BEGIN_Instruction; flags: FLOW_CONTROL
- `FORCE_QUIT` — arg: FunctionArgType.VOID (VOID_ArgumentBuilder)
- `FORCE_QUIT_AND_RESTART` — arg: FunctionArgType.VOID (VOID_ArgumentBuilder)
- `FUNC` — arg: FunctionArgType.SP_CALLFORM (SP_CALL_ArgumentBuilder); flags: FLOW_CONTROL \| EXTENDED \| PARTIAL \| FORCE_SETARG
- `GETTIME` — arg: FunctionArgType.VOID (VOID_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `HTML_PRINT` — arg: AInstruction: HTML_PRINT_Instruction; flags: EXTENDED \| METHOD_SAFE
- `HTML_PRINT_ISLAND` — arg: AInstruction: HTML_PRINT_ISLAND_Instruction; flags: EXTENDED \| METHOD_SAFE
- `HTML_PRINT_ISLAND_CLEAR` — arg: AInstruction: HTML_PRINT_ISLAND_CLEAR_Instruction; flags: EXTENDED \| METHOD_SAFE
- `HTML_TAGSPLIT` — arg: AInstruction: HTML_TAGSPLIT_Instruction; flags: EXTENDED \| METHOD_SAFE
- `INITRAND` — arg: AInstruction: INITRAND_Instruction; flags: EXTENDED \| METHOD_SAFE
- `INPUT` — arg: AInstruction: INPUT_Instruction; flags: IS_PRINT \| IS_INPUT
- `INPUTANY` — arg: AInstruction: INPUTANY_Instruction; flags: EXTENDED
- `INPUTMOUSEKEY` — arg: AInstruction: INPUTMOUSEKEY_Instruction; flags: EXTENDED
- `INPUTS` — arg: AInstruction: INPUTS_Instruction; flags: IS_PRINT \| IS_INPUT
- `INVERTBIT` — arg: AInstruction: SETBIT_Instruction; flags: EXTENDED \| METHOD_SAFE
- `LOADCHARA` — arg: AInstruction: LOADCHARA_Instruction; flags: EXTENDED \| METHOD_SAFE
- `LOADDATA` — arg: FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder); flags: FLOW_CONTROL \| EXTENDED
- `LOADGAME` — arg: AInstruction: SAVELOADGAME_Instruction; flags: FLOW_CONTROL
- `LOADGLOBAL` — arg: AInstruction: LOADGLOBAL_Instruction; flags: EXTENDED \| METHOD_SAFE
- `LOADVAR` — arg: AInstruction: LOADVAR_Instruction; flags: EXTENDED \| METHOD_SAFE
- `NOSKIP` — arg: FunctionArgType.VOID (VOID_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE \| PARTIAL; match-end: `ENDNOSKIP`
- `ONEBINPUT` — arg: AInstruction: ONEBINPUT_Instruction; flags: IS_PRINT \| IS_INPUT
- `ONEBINPUTS` — arg: AInstruction: ONEBINPUTS_Instruction; flags: IS_PRINT \| IS_INPUT
- `ONEINPUT` — arg: AInstruction: ONEINPUT_Instruction; flags: EXTENDED \| IS_PRINT \| IS_INPUT
- `ONEINPUTS` — arg: AInstruction: ONEINPUTS_Instruction; flags: EXTENDED \| IS_PRINT \| IS_INPUT
- `PICKUPCHARA` — arg: FunctionArgType.INT_ANY (INT_ANY_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `PLAYBGM` — arg: AInstruction: PLAYBGM_Instruction; flags: EXTENDED \| METHOD_SAFE
- `PLAYSOUND` — arg: AInstruction: PLAYSOUND_Instruction; flags: EXTENDED \| METHOD_SAFE
- `POWER` — arg: FunctionArgType.SP_POWER (SP_POWER_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `PRINT` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTBUTTON` — arg: FunctionArgType.SP_BUTTON (SP_BUTTON_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `PRINTBUTTONC` — arg: FunctionArgType.SP_BUTTON (SP_BUTTON_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `PRINTBUTTONLC` — arg: FunctionArgType.SP_BUTTON (SP_BUTTON_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `PRINTC` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTCD` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTCK` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTCPERLINE` — arg: FunctionArgType.SP_GETINT (SP_GETINT_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `PRINTD` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTDATA` — arg: AInstruction: PRINT_DATA_Instruction; flags: EXTENDED \| PARTIAL \| IS_PRINT \| IS_PRINTDATA; match-end: `ENDDATA`
- `PRINTDATAD` — arg: AInstruction: PRINT_DATA_Instruction; flags: EXTENDED \| PARTIAL \| IS_PRINT \| IS_PRINTDATA; match-end: `ENDDATA`
- `PRINTDATADL` — arg: AInstruction: PRINT_DATA_Instruction; flags: EXTENDED \| PARTIAL \| IS_PRINT \| IS_PRINTDATA; match-end: `ENDDATA`
- `PRINTDATADW` — arg: AInstruction: PRINT_DATA_Instruction; flags: EXTENDED \| PARTIAL \| IS_PRINT \| IS_PRINTDATA; match-end: `ENDDATA`
- `PRINTDATAK` — arg: AInstruction: PRINT_DATA_Instruction; flags: EXTENDED \| PARTIAL \| IS_PRINT \| IS_PRINTDATA; match-end: `ENDDATA`
- `PRINTDATAKL` — arg: AInstruction: PRINT_DATA_Instruction; flags: EXTENDED \| PARTIAL \| IS_PRINT \| IS_PRINTDATA; match-end: `ENDDATA`
- `PRINTDATAKW` — arg: AInstruction: PRINT_DATA_Instruction; flags: EXTENDED \| PARTIAL \| IS_PRINT \| IS_PRINTDATA; match-end: `ENDDATA`
- `PRINTDATAL` — arg: AInstruction: PRINT_DATA_Instruction; flags: EXTENDED \| PARTIAL \| IS_PRINT \| IS_PRINTDATA; match-end: `ENDDATA`
- `PRINTDATAW` — arg: AInstruction: PRINT_DATA_Instruction; flags: EXTENDED \| PARTIAL \| IS_PRINT \| IS_PRINTDATA; match-end: `ENDDATA`
- `PRINTDL` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTDW` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTFORM` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTFORMC` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTFORMCD` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTFORMCK` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTFORMD` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTFORMDL` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTFORMDW` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTFORMK` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTFORMKL` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTFORMKW` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTFORML` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTFORMLC` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTFORMLCD` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTFORMLCK` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTFORMN` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTFORMS` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTFORMSD` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTFORMSDL` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTFORMSDW` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTFORMSK` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTFORMSKL` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTFORMSKW` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTFORMSL` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTFORMSN` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTFORMSW` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTFORMW` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTK` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTKL` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTKW` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTL` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTLC` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTLCD` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTLCK` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTN` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTPLAIN` — arg: FunctionArgType.STR_NULLABLE (STR_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `PRINTPLAINFORM` — arg: FunctionArgType.FORM_STR_NULLABLE (FORM_STR_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `PRINTS` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTSD` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTSDL` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTSDW` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTSINGLE` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTSINGLED` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTSINGLEFORM` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTSINGLEFORMD` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTSINGLEFORMK` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTSINGLEFORMS` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTSINGLEFORMSD` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTSINGLEFORMSK` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTSINGLEK` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTSINGLES` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTSINGLESD` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTSINGLESK` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTSINGLEV` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTSINGLEVD` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTSINGLEVK` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTSK` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTSKL` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTSKW` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTSL` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTSN` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTSW` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTV` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTVD` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTVDL` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTVDW` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTVK` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTVKL` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTVKW` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTVL` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTVN` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTVW` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINTW` — arg: AInstruction: PRINT_Instruction; flags: IS_PRINT
- `PRINT_ABL` — arg: FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder); flags: METHOD_SAFE
- `PRINT_EXP` — arg: FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder); flags: METHOD_SAFE
- `PRINT_IMG` — arg: AInstruction: PRINT_IMG_Instruction; flags: EXTENDED \| METHOD_SAFE
- `PRINT_ITEM` — arg: FunctionArgType.VOID (VOID_ArgumentBuilder); flags: METHOD_SAFE
- `PRINT_MARK` — arg: FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder); flags: METHOD_SAFE
- `PRINT_PALAM` — arg: FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder); flags: METHOD_SAFE
- `PRINT_RECT` — arg: AInstruction: PRINT_RECT_Instruction; flags: EXTENDED \| METHOD_SAFE
- `PRINT_SHOPITEM` — arg: FunctionArgType.VOID (VOID_ArgumentBuilder); flags: METHOD_SAFE
- `PRINT_SPACE` — arg: AInstruction: PRINT_SPACE_Instruction; flags: EXTENDED \| METHOD_SAFE
- `PRINT_TALENT` — arg: FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder); flags: METHOD_SAFE
- `PUTFORM` — arg: FunctionArgType.FORM_STR_NULLABLE (FORM_STR_ArgumentBuilder); flags: METHOD_SAFE
- `QUIT` — arg: FunctionArgType.VOID (VOID_ArgumentBuilder)
- `QUIT_AND_RESTART` — arg: FunctionArgType.VOID (VOID_ArgumentBuilder)
- `RANDOMIZE` — arg: AInstruction: RANDOMIZE_Instruction; flags: EXTENDED \| METHOD_SAFE
- `REDRAW` — arg: FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `REF` — arg: AInstruction: REF_Instruction; flags: EXTENDED \| METHOD_SAFE
- `REFBYNAME` — arg: AInstruction: REF_Instruction; flags: EXTENDED \| METHOD_SAFE
- `REMOVEBGIMAGE` — arg: AInstruction: REMOVEBGIMAGE_Instruction; flags: EXTENDED \| METHOD_SAFE
- `RESETBGCOLOR` — arg: AInstruction: RESETBGCOLOR_Instruction; flags: EXTENDED \| METHOD_SAFE
- `RESETCOLOR` — arg: AInstruction: RESETCOLOR_Instruction; flags: EXTENDED \| METHOD_SAFE
- `RESETDATA` — arg: AInstruction: RESETDATA_Instruction; flags: EXTENDED \| METHOD_SAFE
- `RESETGLOBAL` — arg: AInstruction: RESETGLOBAL_Instruction; flags: EXTENDED \| METHOD_SAFE
- `RESET_STAIN` — arg: FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `RESTART` — arg: AInstruction: RESTART_Instruction; flags: FLOW_CONTROL \| EXTENDED \| METHOD_SAFE
- `REUSELASTLINE` — arg: AInstruction: REUSELASTLINE_Instruction; flags: EXTENDED \| METHOD_SAFE \| IS_PRINT
- `SAVECHARA` — arg: AInstruction: SAVECHARA_Instruction; flags: EXTENDED \| METHOD_SAFE
- `SAVEDATA` — arg: FunctionArgType.SP_SAVEDATA (SP_SAVEDATA_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `SAVEGAME` — arg: AInstruction: SAVELOADGAME_Instruction; flags: FLOW_CONTROL
- `SAVEGLOBAL` — arg: AInstruction: SAVEGLOBAL_Instruction; flags: EXTENDED \| METHOD_SAFE
- `SAVENOS` — arg: FunctionArgType.SP_GETINT (SP_GETINT_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `SAVEVAR` — arg: AInstruction: SAVEVAR_Instruction; flags: EXTENDED \| METHOD_SAFE
- `SETBGCOLOR` — arg: FunctionArgType.SP_COLOR (SP_COLOR_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `SETBGCOLORBYNAME` — arg: FunctionArgType.STR (STR_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `SETBGIMAGE` — arg: AInstruction: SETBGIMAGE_Instruction; flags: EXTENDED \| METHOD_SAFE
- `SETBGMVOLUME` — arg: AInstruction: SETBGMVOLUME_Instruction; flags: EXTENDED \| METHOD_SAFE
- `SETBIT` — arg: AInstruction: SETBIT_Instruction; flags: EXTENDED \| METHOD_SAFE
- `SETCOLOR` — arg: FunctionArgType.SP_COLOR (SP_COLOR_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `SETCOLORBYNAME` — arg: FunctionArgType.STR (STR_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `SETFONT` — arg: FunctionArgType.STR_EXPRESSION_NULLABLE (STR_EXPRESSION_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `SETSOUNDVOLUME` — arg: AInstruction: SETSOUNDVOLUME_Instruction; flags: EXTENDED \| METHOD_SAFE
- `SKIPDISP` — arg: FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `SKIPLOG` — arg: FunctionArgType.INT_EXPRESSION (INT_EXPRESSION_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `SORTCHARA` — arg: AInstruction: SORTCHARA_Instruction; flags: EXTENDED \| METHOD_SAFE
- `SPLIT` — arg: FunctionArgType.SP_SPLIT (SP_SPLIT_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `STOPBGM` — arg: AInstruction: STOPBGM_Instruction; flags: EXTENDED \| METHOD_SAFE
- `STOPCALLTRAIN` — arg: FunctionArgType.VOID (VOID_ArgumentBuilder); flags: FLOW_CONTROL \| EXTENDED
- `STOPSOUND` — arg: AInstruction: STOPSOUND_Instruction; flags: EXTENDED \| METHOD_SAFE
- `STRDATA` — arg: FunctionArgType.VAR_STR (VAR_STR_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE \| PARTIAL; match-end: `ENDDATA`
- `STRLEN` — arg: AInstruction: STRLEN_Instruction; flags: EXTENDED \| METHOD_SAFE
- `STRLENFORM` — arg: AInstruction: STRLEN_Instruction; flags: EXTENDED \| METHOD_SAFE
- `STRLENFORMU` — arg: AInstruction: STRLEN_Instruction; flags: EXTENDED \| METHOD_SAFE
- `STRLENU` — arg: AInstruction: STRLEN_Instruction; flags: EXTENDED \| METHOD_SAFE
- `SWAP` — arg: FunctionArgType.SP_SWAPVAR (SP_SWAPVAR_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `SWAPCHARA` — arg: AInstruction: SWAPCHARA_Instruction; flags: EXTENDED \| METHOD_SAFE
- `THROW` — arg: FunctionArgType.FORM_STR_NULLABLE (FORM_STR_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `TIMES` — arg: AInstruction: TIMES_Instruction; flags: METHOD_SAFE
- `TINPUT` — arg: AInstruction: TINPUT_Instruction; flags: EXTENDED \| IS_PRINT \| IS_INPUT
- `TINPUTS` — arg: AInstruction: TINPUTS_Instruction; flags: EXTENDED \| IS_PRINT \| IS_INPUT
- `TONEINPUT` — arg: AInstruction: TINPUT_Instruction; flags: EXTENDED \| IS_PRINT \| IS_INPUT
- `TONEINPUTS` — arg: AInstruction: TINPUTS_Instruction; flags: EXTENDED \| IS_PRINT \| IS_INPUT
- `TOOLTIP_CUSTOM` — arg: AInstruction: TOOLTIP_CUSTOM_Instruction; flags: EXTENDED
- `TOOLTIP_FORMAT` — arg: AInstruction: TOOLTIP_FORMAT_Instruction; flags: EXTENDED
- `TOOLTIP_IMG` — arg: AInstruction: TOOLTIP_IMG_Instruction; flags: EXTENDED
- `TOOLTIP_SETCOLOR` — arg: AInstruction: TOOLTIP_SETCOLOR_Instruction; flags: EXTENDED \| METHOD_SAFE
- `TOOLTIP_SETDELAY` — arg: AInstruction: TOOLTIP_SETDELAY_Instruction; flags: EXTENDED \| METHOD_SAFE
- `TOOLTIP_SETDURATION` — arg: AInstruction: TOOLTIP_SETDURATION_Instruction; flags: EXTENDED \| METHOD_SAFE
- `TOOLTIP_SETFONT` — arg: AInstruction: TOOLTIP_SETFONT_Instruction; flags: EXTENDED
- `TOOLTIP_SETFONTSIZE` — arg: AInstruction: TOOLTIP_SETFONTSIZE_Instruction; flags: EXTENDED
- `TRYCALL` — arg: AInstruction: CALL_Instruction; flags: FLOW_CONTROL \| EXTENDED \| FORCE_SETARG
- `TRYCALLF` — arg: AInstruction: TRYCALLF_Instruction; flags: EXTENDED \| METHOD_SAFE \| FORCE_SETARG
- `TRYCALLFORM` — arg: AInstruction: CALL_Instruction; flags: FLOW_CONTROL \| EXTENDED \| FORCE_SETARG
- `TRYCALLFORMF` — arg: AInstruction: TRYCALLF_Instruction; flags: EXTENDED \| METHOD_SAFE \| FORCE_SETARG
- `TRYCALLLIST` — arg: FunctionArgType.VOID (VOID_ArgumentBuilder); flags: FLOW_CONTROL \| EXTENDED \| PARTIAL \| IS_TRY; match-end: `ENDFUNC`
- `TRYCCALL` — arg: AInstruction: CALL_Instruction; flags: FLOW_CONTROL \| EXTENDED \| FORCE_SETARG; match-end: `CATCH`
- `TRYCCALLFORM` — arg: AInstruction: CALL_Instruction; flags: FLOW_CONTROL \| EXTENDED \| FORCE_SETARG; match-end: `CATCH`
- `TRYCGOTO` — arg: AInstruction: GOTO_Instruction; flags: FLOW_CONTROL \| EXTENDED \| METHOD_SAFE \| FORCE_SETARG; match-end: `CATCH`
- `TRYCGOTOFORM` — arg: AInstruction: GOTO_Instruction; flags: FLOW_CONTROL \| EXTENDED \| METHOD_SAFE \| FORCE_SETARG; match-end: `CATCH`
- `TRYCJUMP` — arg: AInstruction: CALL_Instruction; flags: FLOW_CONTROL \| EXTENDED \| FORCE_SETARG; match-end: `CATCH`
- `TRYCJUMPFORM` — arg: AInstruction: CALL_Instruction; flags: FLOW_CONTROL \| EXTENDED \| FORCE_SETARG; match-end: `CATCH`
- `TRYGOTO` — arg: AInstruction: GOTO_Instruction; flags: FLOW_CONTROL \| EXTENDED \| METHOD_SAFE \| FORCE_SETARG
- `TRYGOTOFORM` — arg: AInstruction: GOTO_Instruction; flags: FLOW_CONTROL \| EXTENDED \| METHOD_SAFE \| FORCE_SETARG
- `TRYGOTOLIST` — arg: FunctionArgType.VOID (VOID_ArgumentBuilder); flags: FLOW_CONTROL \| EXTENDED \| PARTIAL \| IS_TRY; match-end: `ENDFUNC`
- `TRYJUMP` — arg: AInstruction: CALL_Instruction; flags: FLOW_CONTROL \| EXTENDED \| FORCE_SETARG
- `TRYJUMPFORM` — arg: AInstruction: CALL_Instruction; flags: FLOW_CONTROL \| EXTENDED \| FORCE_SETARG
- `TRYJUMPLIST` — arg: FunctionArgType.VOID (VOID_ArgumentBuilder); flags: FLOW_CONTROL \| EXTENDED \| PARTIAL \| IS_JUMP \| IS_TRY; match-end: `ENDFUNC`
- `TWAIT` — arg: AInstruction: TWAIT_Instruction; flags: EXTENDED \| IS_PRINT
- `UPCHECK` — arg: FunctionArgType.VOID (VOID_ArgumentBuilder); flags: METHOD_SAFE
- `UPDATECHECK` — arg: AInstruction: UPDATECHECK_Instruction; flags: EXTENDED \| METHOD_SAFE
- `VARI` — arg: AInstruction: VARI_Instruction; notes: Only registered when JSONConfig.Data.UseScopedVariableInstruction is true.
- `VARS` — arg: AInstruction: VARS_Instruction; notes: Only registered when JSONConfig.Data.UseScopedVariableInstruction is true.
- `VARSET` — arg: AInstruction: VARSET_Instruction; flags: EXTENDED \| METHOD_SAFE
- `VARSIZE` — arg: FunctionArgType.SP_VAR (SP_VAR_ArgumentBuilder); flags: EXTENDED \| METHOD_SAFE
- `WAIT` — arg: AInstruction: WAIT_Instruction; flags: IS_PRINT
- `WAITANYKEY` — arg: AInstruction: WAITANYKEY_Instruction; flags: IS_PRINT
- `SET` — kind: pseudo-instruction; arg: AInstruction: SET_Instruction; flags: METHOD_SAFE; notes: Internal pseudo instruction used for assignment statements; not a normal statement keyword.

## 14) Expression functions (methods) (planned)

This file will eventually include the **expression-function (method)** catalog and notes, but that content is not landed yet.

Current state in this reference:

- Engine-extracted *method name list* is available in `../tooling/builtins-engine.md` (267 names).
- Doc-derived signatures for many methods are available in `../tooling/builtins-signatures.md` (for offline lookup / fact-check).

Planned landing here (later):

- a method name catalog (embedded, so the file stays self-contained)
- a “call shape” note (methods can be invoked in expressions; this engine also inserts many method names into the identifier dictionary so they can be invoked as statements in some cases)
- signatures/constraints derived from engine sources (not only docs)

## Engine sources (fact-check)

- Interpreter “shift-next-then-execute” behavior: `emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs`
- Control-flow instruction bodies: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs`
- Load-time wiring (`JumpTo`, `IfCaseList`, block pairing, validity checks): `emuera.em/Emuera/Runtime/Script/Loader/ErbLoader.cs`
- Call stack entry/return and `JUMP` behavior: `emuera.em/Emuera/Runtime/Script/Process.State.cs`, `emuera.em/Emuera/Runtime/Script/Process.CalledFunction.cs`
