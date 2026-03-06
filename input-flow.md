# Input Flow and Wait-State Semantics

This document specifies the shared **input-flow contract** used by this engine: how script execution enters an input wait, which completion paths can satisfy that wait, how submitted text is normalized and segmented, how accepted/rejected segments are consumed, and when remaining submitted segments are discarded.

It is written as a shared contract for the `INPUT*`, `BINPUT*`, `ONEINPUT*`, `WAIT*`, `TWAIT`, `INPUTANY`, and `INPUTMOUSEKEY` families.
Per-instruction syntax, exact `RESULT*` assignments, timeout/default argument shapes, and button-side metadata remain documented in `builtins-reference.md`.

Config keys are referenced by their `config-items.md` names.

## 1) Scope and request classes

At runtime, the console can enter a **wait state**. While in that state, normal script execution is suspended until some compatible completion path satisfies the current wait.

Observable request classes are:

- **Value waits**: expect a value and usually assign `RESULT` / `RESULTS`.
  - Examples: `INPUT`, `INPUTS`, `TINPUT*`, `BINPUT*`, `INPUTANY`, and their `ONE*` variants.
- **Confirmation waits**: wait for Enter/any-key/click style confirmation and do not assign `RESULT*`.
  - Examples: `WAIT`, `WAITANYKEY`, `FORCEWAIT`, and `TWAIT` in its confirmation mode.
- **No-input waits**: remain in a wait state but do not accept textbox/button submission as input data.
  - Example: `TWAIT` in its no-input mode.
- **Primitive event waits**: report low-level mouse/key/timeout events rather than textbox submission.
  - Example: `INPUTMOUSEKEY`.

This document covers the **shared host-side flow** around these waits. It does not restate every instruction-specific acceptance rule.

## 2) Wait lifecycle

The shared lifecycle is:

1. Script execution runs normally until an instruction requests a wait.
2. The console enters a wait state for that request.
3. Some compatible completion path satisfies the wait.
4. Script execution resumes immediately.
5. Execution continues until it reaches another wait, quits, errors, or otherwise leaves the running state.

Because step 4 resumes normal script execution immediately, one accepted input can carry execution across arbitrary script code before the same overall input-handling pass either:

- reaches another compatible wait and continues consuming later submitted segments, or
- leaves the wait-driven path and discards the rest.

## 3) Completion paths

### 3.1 Keyboard/textbox submission path

For normal textbox submission (for example pressing Enter in a value wait):

- the submitted text goes through the **keyboard/textbox submission path**,
- it may contain multiple segments,
- those segments are processed in order during one submission pass.

Before segment splitting, this path has two observable preprocessing stages.

#### 3.1.1 Debug/system-command interception

If all of the following are true:

- the submitted text length is greater than `1`,
- the current wait is **not** a one-input wait,
- the submitted text begins with `@`,

then the submission is treated as a host debug/system command instead of normal script input.
The current wait is not satisfied by that submission.
A lone `@` is **not** intercepted by this rule.

#### 3.1.2 Input-expansion transform

If the **original submitted text** contains `(` anywhere, the engine applies a small expansion syntax before segment splitting:

- parenthesized groups can nest,
- a group followed by `*<digits>` is repeated that many times,
- `\n` becomes a newline character,
- `\r` becomes a carriage-return character,
- `\e` becomes the literal marker `\e` followed by a newline,
- backslash followed by a physical newline is removed,
- other backslash escapes drop the backslash and keep the following character.

If the original submitted text does **not** contain `(`, this transform is skipped entirely.

#### 3.1.3 Segment splitting

After the optional transform above, the engine splits the submission into segments using these separators:

- the two-character sequence `\n`,
- CRLF,
- LF,
- CR.

So one textbox submission can supply multiple candidate inputs.

#### 3.1.4 Minimal examples of the input-expansion transform

These examples describe the **expanded submission text** first, and then the segments seen by the submission pass.

- Submitted text `(ab)*3`
  - expands to `ababab`
  - yields one segment: `ababab`
- Submitted text `(12)*2\n34`
  - expands to `1212\n34`
  - yields two segments: `1212`, `34`
- Submitted text `(X)\e(Y)`
  - expands to `X`, then the literal marker `\e`, then a newline, then `Y`
  - yields two segments: `X\e`, `Y`
  - before the first segment is applied, `\e` is removed from that segment and `MesSkip` is turned on (see §7.1)

Practical reading rule:

- the input-expansion transform runs only when the original submission contains `(`,
- parentheses and `*<digits>` belong to that transform syntax,
- segment splitting happens **after** that transform,
- one-input truncation (if any) happens later, per segment,
- literal `\n` is still a segment separator even when the transform did not run, but literal `\r` only becomes a carriage-return character through the transform.

### 3.2 Mouse-click completion path

For non-primitive value waits, clicking a selectable **normal-output button** can submit that button's string/value as input.

Shared properties of this path:

- the engine uses the **mouse-click completion path**,
- the clicked normal-output button contributes one submitted string/value,
- that submission is treated as a single segment,
- the keyboard-only debug-command interception and input-expansion transform do not run on this path.

Important boundary distinctions:

- This path is about **normal-output button regions** embedded in the ordinary output model; it is not the same as the separate `CBG` button-map layer.
- For `INPUT` / `INPUTS` / `INPUTANY`-style value waits, clickable normal-output buttons can satisfy the wait even when the instruction did not request the extra mouse side-channel mode.
- The optional `mouse` argument on `INPUT` / `INPUTS` / `TINPUT*` / `BINPUT*` families mainly controls whether the UI also writes the extra mouse side-channel metadata; see the corresponding built-in entries for exact `RESULT*` slots.

On this host, a right-click completion path can also request `MesSkip`, so one mouse completion can both satisfy the current wait and enable immediate skip-driven continuation of later waits in the same handling pass.

### 3.3 Timeout completion path

Timed waits (`TINPUT*`, `TWAIT`, `INPUTMOUSEKEY <timeMs>`) can also complete because the timer expires.

Observable rules:

- for timed value waits, timeout re-enters the normal acceptance path using an empty submitted string,
- that empty string then interacts with the instruction's default-value rules,
- for primitive event waits, timeout produces that instruction's explicit timeout event payload instead of a textbox submission,
- the exact timeout message/display behavior remains instruction-specific.

### 3.4 `MesSkip` no-wait path

Some input instructions accept a `canSkip` option.
When that option is present and `MesSkip` is already enabled, the engine may accept the request immediately without entering a UI wait.

This path:

- does not create a textbox submission,
- does not use segment splitting,
- does not echo submitted text,
- uses the instruction's own no-wait/default rules.

### 3.5 No-input waits (`Void`-style waits)

Some waits intentionally do **not** accept user text/button submission at all.
The clearest script-visible example is `TWAIT` in its no-input mode.

Observable rules for this class:

- the wait remains active for its timer/host-controlled duration,
- ordinary keyboard/textbox submission does not satisfy it,
- mouse/button text selection is likewise not treated as submitted input for that wait,
- it can still be passed by timeout,
- it can also be bypassed by the same skip/macro-driven continuation rules that apply to other non-value waits.

In other words, this class participates in the wait-state lifecycle, but not in the textbox/button acceptance model.

### 3.6 Primitive event waits

`INPUTMOUSEKEY` does **not** use the textbox-segmentation model described in §3.1.
It waits for primitive mouse/key/timeout events and reports them through its own `RESULT:*` payload contract.

It still follows the same high-level rule that an accepted event resumes script execution immediately, but it does not consume textbox segments and does not participate in the multi-segment submission-pass model.

## 4) Generic acceptance and rejection effects

This section describes the **shared** effects around textbox/button-based completion.
Instruction-specific value parsing and `RESULT*` layout still belong to the built-in entries.

### 4.1 Accepted textbox/button submission

When a non-primitive wait accepts a textbox/button submission through the normal UI path:

- the wait timer (if any) stops,
- the accepted submitted text is echoed to output,
- script execution resumes immediately.

Important exceptions:

- the `MesSkip` no-wait path does not echo text, because there is no actual UI submission,
- primitive event waits are outside this model,
- if the accepted text is the empty string, the echo is correspondingly empty (so it may produce no visible output).

### 4.2 Rejected textbox/button submission

For acceptance models that can reject submitted text (for example invalid integer input or button mismatch):

- the current wait remains active,
- script execution does not resume yet,
- the rejected text is not echoed,
- acceptance-side `RESULT*` writes do not occur for that segment.

A rejected segment does **not** by itself terminate the surrounding submission pass; later segments from the same submission may still be tried.

## 5) Submission-pass model for keyboard/textbox input

For waits completed through the keyboard/textbox submission path, one submitted payload starts a **submission pass**.
Within that pass, the engine may consume not only the first accepted segment, but also later segments from the same submission if script execution returns to another compatible wait state quickly enough.

A submission pass is **not** a persistent global input queue.
Remaining submitted segments are discarded as soon as the pass ends.

### 5.1 Per-segment processing order

Within one keyboard/textbox submission pass, the engine processes segments in order.
For each segment:

1. Apply any per-segment special handling (for example one-input truncation, or `\e` handling described in §7.1).
2. Try to satisfy the current wait using that segment.
3. If the segment is rejected, the same submission pass may continue with the next segment.
4. If the segment is accepted, script execution resumes immediately.
5. When execution stops again, the engine checks whether the console has returned to another compatible wait.
   - If yes, the submission pass may continue with the next remaining segment.
   - If no, the submission pass ends and all remaining segments are discarded.

### 5.2 Rejected segments do not terminate the pass

Example submission:

```text
abc
12
```

If the current wait is integer input:

- `abc` is rejected,
- the engine remains in the same wait,
- `12` is then tried by the same submission pass and may be accepted.

### 5.3 Accepted segments can feed later waits

An accepted segment can advance execution through arbitrary script code before the same pass feeds another wait.

Example:

```erabasic
INPUT
PRINTFORM XXX{YYY()}
; arbitrary code
INPUT
```

One submission containing:

```text
12
34
```

can be observed as:

- the first `INPUT` accepts `12`,
- script resumes and runs the intervening code,
- execution reaches the second `INPUT`,
- the same submission pass then lets the second `INPUT` consume `34`.

### 5.4 Why this is not a persistent queue

The model above can look queue-like, but it is submission-scoped, not global.

If execution stops in any non-wait state after an accepted segment (for example script end, quit, error, or another non-input host state), the submission pass ends immediately and any remaining submitted segments are lost.
They are **not** retained for some unrelated later wait.

## 6) One-input mode

The `ONEINPUT*`, `ONEBINPUT*`, `TONEINPUT*`, and equivalent one-input requests use a shared one-input rule:

- one-input truncation is applied **per submitted segment**, not to the whole original textbox string at once,
- each submitted segment is normally truncated to its first character,
- exception: if the segment is accepted through the mouse-click completion path and config option `AllowLongInputByMouse` is enabled, that mouse-submitted segment is used without truncation.

Important boundary rule:

- this truncation applies only to submitted UI text,
- defaults accepted from empty input or from the `MesSkip` no-wait path are used as-is.

See the `ONEINPUT*` / `ONEBINPUT*` / `TONEINPUT*` built-in entries for the request-specific result type after truncation.

## 7) `MesSkip` inside the input loop

### 7.1 `\e` inside a submitted segment

Before a segment is applied to the current wait, the engine checks whether that segment contains the literal two-character sequence `\e`.
If so:

- all `\e` substrings are removed from that segment before normal acceptance/parsing,
- `MesSkip` is turned on before that segment is executed.

This allows one submitted segment to both provide a value and request skip-driven continuation of later waits in the same handling pass.

### 7.2 Immediate auto-advance loop

After a segment is processed, if `MesSkip` is now enabled and execution has returned to another wait state, the engine may immediately auto-advance additional waits in the same handling pass.

Observable rule:

- waits that do **not** require a value can be auto-advanced while `MesSkip` remains enabled,
- waits that require a value stop this auto-advance loop,
- waits that explicitly stop message skip also stop this auto-advance loop.

This is why one accepted submission can sometimes pass through several non-value waits.

### 7.3 `MesSkip` does not persist across explicit later segments

The temporary `MesSkip` state used by one accepted segment is cleared before the engine moves on to the next explicit remaining segment from the same keyboard submission.

So, within one multi-segment submission:

- `MesSkip` can auto-advance later waits that occur **immediately after** one accepted segment,
- but it does not remain latched forever across the rest of the explicit segment list.

## 8) Acceptance classes at a glance

This shared flow feeds several observable acceptance models:

- **integer value waits**: accept only valid integer text (or an instruction-defined default path), otherwise reject and keep waiting,
- **string value waits**: accept submitted text as a string, with instruction-defined empty/default rules,
- **button waits**: accept only text/value that matches a currently selectable button,
- **any-value waits**: accept either an integer or a string depending on parse success,
- **confirmation waits**: accept the confirmation event and continue without assigning `RESULT*`,
- **no-input waits**: do not accept submitted textbox/button text at all; they continue only when their own wait condition is satisfied,
- **primitive event waits**: bypass the textbox/button submission model entirely.

The exact per-instruction acceptance rules stay in `builtins-reference.md`.
This document specifies only the shared flow that surrounds those rules.

## 9) Reimplementation checklist

A compatible reimplementation should preserve all of these observable rules:

- waits suspend script execution until a compatible completion path satisfies them,
- keyboard/textbox submission may yield multiple ordered segments,
- debug/system-command interception happens before normal keyboard/textbox acceptance,
- the optional input-expansion transform runs only when the original submission contains `(`,
- rejected segments do not terminate the same submission pass,
- accepted segments can advance execution into later waits within the same pass,
- remaining segments are discarded once execution stops being in a compatible wait state,
- one-input truncation is per segment and has the mouse/config exception,
- `\e` can turn on `MesSkip` for the immediate post-segment continuation loop,
- that temporary `MesSkip` state is cleared before later explicit segments are processed,
- no-input waits do not accept ordinary textbox/button submission,
- primitive event waits (`INPUTMOUSEKEY`) bypass textbox segmentation entirely.

## 10) Related documents

- `builtins-reference.md` — per-instruction syntax, defaults, `RESULT*`, timeout messages, and side channels.
- `config-items.md` — config keys referenced here, especially `AllowLongInputByMouse`.
- `system-flow.md` — host phase/state transitions outside the local input loop.
- `plugins.md` — plugin helper `WaitInput(...)` surface (host extension API), which is related but not a substitute for the typed ERB input instructions.
