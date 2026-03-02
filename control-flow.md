# Control Flow (statements and blocks)

EraBasic is primarily statement-and-block based. Conditions are **numeric**: `0` is false and any non-zero value is true.

## Execution model note (important for reimplementation)

In this engine, the main interpreter loop advances to `CurrentLine.NextLine` **before** executing anything.

As a result:

- “Jump targets” are typically **marker lines** (e.g. `REPEAT`, `FOR`, `WHILE`, `IF`, `CASE`).
- After `JumpTo(marker)`, the next executed line is usually `marker.NextLine` (so the marker line itself is not re-executed).

This is crucial for understanding why loop headers initialize variables only once, while loop tails (`REND/NEXT/WEND/LOOP`) drive iteration.

## Conditional execution

- `IF / ELSEIF / ELSE / ENDIF` — block conditional
- `SIF` — “single-line IF”: executes or skips the *next line*

### `SIF`

`SIF <cond>` executes **only the next line** if `<cond>` is true; otherwise it skips that next line.

This is commonly used as a compact guard:

    SIF TARGET < 0
        RETURN

Engine-accurate structural constraints (load-time checks):

- There must be a “next line” to skip/execute. If `SIF` is the last line in a function (or is immediately followed by function/file end), `SIF` is an **error**.
- The “next line” must not be a function label (`@...`) or file boundary marker.
- The “next line” must not be a local label definition (`$...`); this is an **error**.
- If the “next line” is an instruction line whose instruction is **partial / structural** (e.g. `IF`, `SELECTCASE`, loops, `CATCH`-family markers), `SIF` is an **error**.
  - This prevents `SIF` from conditionally skipping a structural marker line and breaking block matching.
- If the skipped line is not immediately the next physical source line (line numbers are not adjacent), the loader emits a warning (level 0).

Runtime behavior:

- If `<cond> == 0`, the interpreter skips exactly one logical line by calling an extra `ShiftNextLine()` (so the skipped line is treated as if it had executed normally and advanced once).

### `IF / ELSEIF / ELSE / ENDIF`

`IF` begins a conditional block. The engine evaluates conditions in order:

- If `IF` condition is true, it executes until the next `ELSEIF`, `ELSE`, or `ENDIF`, then jumps to `ENDIF`.
- If `IF` condition is false, it skips ahead to the next `ELSEIF` / `ELSE` / `ENDIF`.
- Each `ELSEIF` behaves like a new `IF` at that point.
- `ELSE` (if present) runs when no earlier branch matched.

Practical rules:

- `ELSE` is optional.
- If present, `ELSE` must follow an `IF`/`ELSEIF`, and `ENDIF` closes the whole construct.

Engine-accurate evaluation model (important):

- Only the `IF` instruction line performs branching logic at runtime.
  - It evaluates the `IF` condition and each `ELSEIF` condition in sequence and jumps to the first matching marker line (or to `ELSE`, or to `ENDIF`).
  - When it “jumps to” an `ELSEIF` or `ELSE` marker line, the engine’s execution model causes execution to begin at that marker’s **body** (`marker.NextLine`), not on the marker line itself.
- The `ELSEIF` and `ELSE` marker lines exist only to prevent fall-through:
  - when reached sequentially (because an earlier branch executed), they immediately jump to the `ENDIF` marker.

Engine-accurate load-time checks:

- `ELSEIF` / `ELSE` outside an `IF` block are **errors**.
- `ENDIF` without a matching `IF` is an **error**.
- `ELSEIF` / `ELSE` after an `ELSE` emits a warning (the loader still accepts it, but it is effectively unreachable in normal structured control flow).

## Multi-way branching

- `SELECTCASE / CASE / CASEELSE / ENDSELECT`

Supports value cases, ranges (`a TO b`), and comparison cases (`IS <= expr`).

### Semantics

`SELECTCASE` evaluates a single value once, then selects a matching `CASE` block.

- There is **no fall-through**: once a `CASE` matches, only that block runs, then execution continues after `ENDSELECT`.
- If no `CASE` matches, `CASEELSE` runs if present; otherwise it jumps to `ENDSELECT`.
- A `CASE` line can contain multiple conditions separated by commas; conditions are checked left-to-right and stop at the first match (short-circuit within the `CASE` line).

### `CASE` condition formats

1) **Direct values**

    SELECTCASE X
        CASE 1
            ...
        CASE 2, 3
            ...
    ENDSELECT

2) **Ranges** (`a TO b`, inclusive)

    CASE 10 TO 20

3) **Comparisons** (`IS <op> <expr>`)

    CASE IS <= 30

`IS` and `TO` are only meaningful in the exact `CASE` syntaxes above (they are not general-purpose expression operators).

### Strings

If the `SELECTCASE` argument is a string expression, then the `CASE` conditions must also be string expressions.

Engine-accurate details:

- `TO` ranges are **inclusive** (`left <= value <= right`) for both integer and string cases.
- `IS <op> expr` compares the **SELECTCASE value** to `expr` (e.g. `CASE IS <= 30` means `selectValue <= 30`).
- For strings, comparisons (including range bounds) use **ordinal** string comparison (case-sensitive, not affected by `IgnoreCase`).
- Like `IF`, only the `SELECTCASE` line performs the selection work:
  - it evaluates the `SELECTCASE` value once
  - it then evaluates `CASE` condition expressions as needed
  - it jumps to the selected `CASE`/`CASEELSE` marker line (or to `ENDSELECT`)
- `CASE` / `CASEELSE` marker lines exist only to prevent fall-through:
  - when reached sequentially (because a previous case block executed), they immediately jump to `ENDSELECT`.

Engine-accurate load-time checks:

- `CASE` / `CASEELSE` outside a `SELECTCASE` block are **errors**.
- Before the first `CASE`/`CASEELSE`, no other instructions are allowed inside the `SELECTCASE` block; attempting to place statements directly after `SELECTCASE` is an **error**.
- `ENDSELECT` without a matching `SELECTCASE` is an **error**.
- `CASE` after `CASEELSE` emits a warning (still accepted, but is effectively unreachable as a selector).
- If a `CASE` contains no condition expressions, it is an **error**.
- If a `CASE` expression’s type does not match the `SELECTCASE` expression’s type (int vs string), it is an **error**.

## Loops

Common loop constructs include:

- `FOR ... NEXT`
- `WHILE ... WEND`
- `REPEAT ... REND`
- `DO ... LOOP`

All loop constructs support `CONTINUE` and `BREAK`.

### `REPEAT / REND`

    REPEAT loopCount
        ...
    REND

Runs the body `loopCount` times.

- The loop counter is stored in `COUNT` (specifically `COUNT:0`).
- The first iteration runs with `COUNT == 0`.
- After the loop ends, `COUNT` becomes `loopCount`.

Engine-accurate details:

- `REPEAT loopCount` is internally treated like a `FOR` loop with:
  - counter variable: `COUNT:0`
  - start: `0`
  - end: `loopCount`
  - step: `1`
- `loopCount` is evaluated once on loop entry and stored (changes to variables used to compute it do not affect the running loop).
- The end bound is **exclusive** (`COUNT` continues while `loopCount > COUNT`).
- If `loopCount` is a constant `<= 0`, the engine marks the `REPEAT` line as an error during argument parsing.
- If `COUNT` is prohibited (size 0 via `VariableSize.csv`), using `REPEAT` is an error.
- Nested `REPEAT` emits a warning, but is still accepted.

### `FOR / NEXT`

    FOR counterVar, startNum, endNum(, step)
        ...
    NEXT

`FOR` is like an enhanced `REPEAT`:

- You choose the counter variable (must be numeric).
- You choose the start value (`startNum`) and the per-iteration step (`step`, default `1`).
- The loop terminates using a strict bound rule (engine-accurate):
  - When `step > 0`, it continues while `endNum > counterVar` (end is **exclusive**).
  - When `step < 0`, it continues while `endNum < counterVar` (end is **exclusive**).
  - When `step == 0`, the body is never entered (but `counterVar` is still assigned `startNum`).
- `startNum`, `endNum`, and `step` are **fixed at loop entry** (later changes to variables used to compute them do not affect the running loop).

Engine-accurate argument rules:

- `startNum` may be omitted by leaving an empty field: `FOR X,,END` means `startNum = 0`.
- `step` may be omitted: `FOR X,START,END` means `step = 1`.
- The counter variable must be a non-const, non-character-data numeric variable term.

Engine-accurate warnings:

- `REPEAT` inside a `FOR` that uses `COUNT:n` can emit a warning if it would conflict with the same `COUNT` index (notably `COUNT:0`).
- Nested `FOR` loops that reuse the same `COUNT:n` index can emit a warning.

### `WHILE / WEND`

    WHILE cond
        ...
    WEND

Engine-accurate semantics:

- `WHILE cond` evaluates `cond` once on entry:
  - if `cond != 0`, enter the body
  - else, skip to after `WEND`
- `WEND` reevaluates the *same* `cond` expression (the one stored on the `WHILE` marker line):
  - if `cond != 0`, it jumps back to the `WHILE` marker so execution continues at the loop body again
  - else, it exits the loop

### `DO / LOOP`

    DO
        ...
    LOOP cond

Like C/VB `do { ... } while (...)`: it always executes the body at least once, then continues while `cond` is non-zero.

Note: `CONTINUE` inside a `DO...LOOP` does **not** necessarily jump to `DO`; it proceeds to `LOOP` and may exit if the condition is false.

## Loop control: `CONTINUE` and `BREAK`

`CONTINUE` and `BREAK` are valid inside `REPEAT`, `FOR`, `WHILE`, and `DO`.

- `CONTINUE` starts the next iteration.
  - In `REPEAT` and `FOR`, it advances the loop counter as if the end of the loop body was reached normally.
- `BREAK` terminates the loop and continues after the loop-end line.

Engine-accurate notes:

- For `REPEAT`/`FOR`, both `CONTINUE` and `REND/NEXT` increment the counter by `step` in an **unchecked** context (64-bit wraparound is possible).
- For `REPEAT`/`FOR`, `BREAK` also increments the counter by `step` before exiting (EraMaker-compat quirk).
- For `WHILE`/`DO`, there is no loop counter to adjust.
- `BREAK` and `CONTINUE` always target the **innermost** enclosing loop (determined at load time by a nesting stack).
- If the engine cannot determine the loop counter term for a `REPEAT`/`FOR` (e.g. control flow reaches `REND/NEXT/CONTINUE` without passing through the loop header), it exits the loop instead of looping.
- Implementation quirk: `BREAK` does not guard against a missing loop-counter binding; if you jump into a `REPEAT/FOR` body without executing the header and then execute `BREAK`, this engine can throw an unexpected runtime exception (whereas `REND/NEXT/CONTINUE` explicitly handle the “missing counter” case by exiting).

Engine-accurate `DO...LOOP` special case:

- `CONTINUE` inside a `DO...LOOP` re-evaluates the `LOOP` condition expression immediately:
  - if true, it jumps back to the `DO` marker (begin next iteration)
  - if false, it jumps to the `LOOP` marker so execution continues after the loop
- If the `LOOP` line is marked as an error, executing `CONTINUE` throws that error.

## Jumping / early exit

Control-transfer commands exist, including:

- `GOTO`
- `JUMP` / `JUMPFORM`
- `TRY*` / `TRYC*` variants of call/jump/goto (missing-target soft failure)
- `TRYCALLLIST` / `TRYJUMPLIST` / `TRYGOTOLIST` (try multiple targets)
- `RETURN`
- `BREAK` / `CONTINUE` (loops only; they do not “break out” of `SELECTCASE`)

### Unstructured `GOTO` into blocks (engine behavior)

The engine does not enforce “structured entry” into `IF`/`SELECTCASE`/loop blocks. In particular:

- `GOTO` targets a `$label` line within the current function, and execution begins at the line **after** that `$label`.
- If the `$label` is placed inside a branch body, `GOTO` can enter that body regardless of the branch condition / selected case.
- If the `$label` is placed inside a loop body (after the loop header), `GOTO` can enter the loop without initializing the loop header state.

Because of the “advance first, execute after” model (see `runtime-model.md`), entering a block mid-body can also skip marker semantics:

- Jumping to the `ELSEIF` marker line would start at its body (and would *not* execute the `ELSEIF` line’s “jump to ENDIF” behavior).
- Jumping to a loop-end marker line (e.g. `REND`, `NEXT`, `WEND`, `LOOP`) starts execution **after** that line, so it does not perform the end-of-loop increment/check that would occur when reaching the marker sequentially.

Practical compatibility note:

- `REND/NEXT/CONTINUE` explicitly handle “missing loop counter binding” by exiting the loop.
- `BREAK` does not: if you enter a `REPEAT/FOR` body without executing the header and then execute `BREAK`, this engine can throw an unexpected runtime exception.

## Fact-check cross-refs (optional)

If you want to verify exact edge cases, these are the upstream references:

- `emuera.em.doc/docs/Reference/IF.en.md`
- `emuera.em.doc/docs/Reference/SELECTCASE.en.md`
- `emuera.em.doc/docs/Reference/REPEAT.en.md`
- `emuera.em.doc/docs/Reference/FOR.en.md`
- `emuera.em.doc/docs/Reference/WHILE.en.md`
- `emuera.em.doc/docs/Reference/DO.en.md`
- `emuera.em.doc/docs/Reference/CONTINUE.en.md`

Engine source of truth for this codebase:

- Block matching + jump-link construction: `emuera.em/Emuera/Runtime/Script/Loader/ErbLoader.cs` (`nestCheck`)
- Runtime implementations: `emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs` (`IF_Instruction`, `SELECTCASE_Instruction`, `REPEAT_Instruction`, `WEND_Instruction`, `LOOP_Instruction`, `BREAK_Instruction`, `CONTINUE_Instruction`, `SIF_Instruction`)
- CASE parsing + evaluation: `emuera.em/Emuera/Runtime/Script/Statements/Expression/ExpressionParser.cs` (`reduceCaseExpression`), `emuera.em/Emuera/Runtime/Script/Statements/CaseExpression.cs`
