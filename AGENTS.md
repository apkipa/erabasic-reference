# Authoring rules (`erabasic-reference/`)

This file defines the default rules for editing this reference, including built-ins overrides and shared spec-facing documents.

## 1) Interaction protocol

If the user explicitly requests analysis only (`仅分析`, `先plan`, `不要动手`, `不要进行修改`):

- treat the workspace as read-only,
- do not edit files, regenerate outputs, or run commands whose main purpose is to modify tracked files,
- before switching from analysis to execution, obtain explicit permission.

If the user asks the assistant to “remember” a rule, persist it into `erabasic-reference/AGENTS.md` (or another explicitly specified location) without requiring an extra prompt.

## 2) Root-cause policy

When a doc/tooling/lint problem is discovered, fix the **canonical rule/model** rather than only the newly observed symptom.

Default policy:

- prefer one-shot migration over compatibility layers,
- do not add one-off branches, sibling lints, or narrowly scoped exceptions if a shared rule can be tightened instead,
- if a counterexample shows the current rule is incomplete, generalize the rule first,
- when reporting the change, state whether it is a root-cause generalization or a deliberately narrow exception.

## 3) Source of truth

Keep documentation sources reviewable and diffable.

- Do not add ad-hoc fallback dictionaries or hidden override sources inside generators.
- Built-ins overrides must live in `erabasic-reference/builtins-overrides/**/<NAME>.md`.
- Preserve sections explicitly labeled as intentional explanatory notes unless the user asks to remove or rewrite them.

## 4) Reimplementation-grade standard

Spec-facing text must be good enough that an independent implementation can reproduce compatible behavior **without reading this engine’s source code**.

These are not “final polish” goals. They apply while drafting any spec-facing text, not only when deciding whether to call a topic complete.

This implies the hard requirements below.

### 4.1 Observable-contract first

Define behavior in terms of inputs, outputs, state changes, visibility, persistence, rejection, and errors.

- Prefer user-visible / script-visible terminology.
- If a stable external spec is the clearest contract, it is acceptable to reference it directly.
- Do not justify behavior by pointing at internal call chains or helper names.

### 4.2 Dependency closure

Normative prose must be self-resolving within the reference.

If the text uses a nontrivial term, quantity, threshold, budget, offset, width, state, or phase, the reader must be able to resolve it **from the reference itself**:

- define it in place, or
- link to its defining spec-facing document.

If a reader would need to inspect source just to understand what a named quantity means, the text is incomplete.

### 4.3 Derived values must be reproducible

If a rule depends on a derived runtime value, define that value from documented inputs.

- Do not treat an implementation property name as a sufficient definition.
- “`SomeInternalName`” is only a mapping note, not the contract.
- First define the value reproducibly; only then, if useful, add `(implementation property: ...)`.

### 4.4 Preserve public names without letting them replace definitions

If a name/signature/type/helper surface is externally observable, preserve it.

But preserving the name is not enough:

- a public or compatibility-relevant name must still be defined observably or reproducibly,
- implementation/property names are not spec-facing definitions by themselves.

### 4.5 First-use classification for nontrivial identifiers

On first use in spec-facing prose, any nontrivial identifier-like term must be classified explicitly unless the immediately surrounding spec-facing text already classifies it unambiguously.

Use one of these roles (or equally explicit wording):

- `config item ...`
- `derived runtime value ...`
- `public script/plugin surface ...`
- `implementation property ...` / `implementation helper ...` (mapping note only)

Do not present names from different layers in the same bare style when that would make them look equivalent.
If a reader could reasonably mistake a config item name for a derived value, or a derived value for an implementation property, the prose is incomplete.

## 5) Completion discipline

Do not describe a topic as `complete`, `done`, or `reimplementation-grade` unless **all major submodels within that topic** have been checked and brought to the same standard.

Guardrails:

- “main path documented” is not the same as “topic complete”,
- if one important submodel is still partial, the whole topic remains partial,
- if a shared topic depends on built-in families, re-check those built-in entries before claiming completion,
- if `coverage.md` still marks the relevant surface as unresolved, do not claim completion unless `coverage.md` is also updated and the status change is justified.

## 6) Mandatory self-review for spec-facing work

Run this checklist whenever you add or materially rewrite spec-facing text.
Do not wait until the end of the task.

Before claiming that a topic or built-in group is reimplementation-grade, run it again explicitly as a final gate.

- **Surface inventory**: have all major layers / submodels / related built-in surfaces been enumerated?
- **Positive definition**: for each important submodel, does the text explain how it works, not merely what it excludes?
- **Boundary triggers**: are entry / exit / overwrite / deletion / persistence / visibility triggers stated as concrete rules?
- **Hidden derived values**: does the text rely on any named runtime quantity that is not defined from documented inputs?
- **Name-layer check**: on first use, are config item names, derived runtime values, public script/plugin names, and implementation names explicitly classified when needed, rather than left as bare ambiguous identifiers?
- **Getter / helper classification**: are getters/helpers grouped under the correct state model rather than inferred from name similarity?
- **Cross-doc sync**: if the topic relies on other documents or built-ins, were those updated to the same precision level?
- **Coverage sync**: does `coverage.md` still expose a major unresolved hole for this exact surface?
- **Reader burden**: would an independent implementer still need to guess an important branch, lifecycle step, or formula? If yes, the topic is not done.

When reporting status, explicitly distinguish:

- what is complete,
- what remains partial,
- and whether the overall topic is therefore still partial or can genuinely be called complete.

## 7) Writing style for spec-facing docs

Write for a reader who wants to reproduce behavior, not for one who already knows the engine internals.

Default style:

- prefer precise wording that stays readable,
- replace vague phrases such as `some cases`, `typically`, `in many cases`, `depending on ...` with exact conditions whenever behavior is known,
- if exact behavior is still unknown, mark the uncertainty explicitly and fence what is known vs unknown,
- use explicit inequalities instead of `1..99`-style notation,
- stay concise, but do not omit compatibility-relevant branches just because they look “obvious”.

## 8) Shared defaults and document-exceptions-only rule

Unless an entry explicitly says otherwise:

- arguments are evaluated left-to-right,
- each argument (and any subscripts inside it) is evaluated once,
- if output skipping (`SKIPDISP` / skip-print mode) skips a built-in, it performs no evaluation and has no side effects.

Document these only when a topic/entry deviates from them.

## 9) Parameter and branch discipline

When documenting parameters, defaults, and acceptance/rejection behavior, distinguish cases that can fork compatibility.

Always separate these when they are observably different:

- omitted argument / omitted slot,
- explicit empty value,
- explicit sentinel value such as `0` or `-1`,
- supplied-but-invalid value.

Rules:

- mark a parameter `optional` only if that argument position is genuinely omittable,
- write `default X` only when omission is observably equivalent to supplying `X`,
- state whether omission/invalid handling happens at parse time, binding time, or runtime semantic handling when that affects behavior,
- state the observable outcome precisely: reject and retry, clamp, coerce, error, warning + substitution, ignored tail, preserved prior value, or no effect.

For `Progress state: complete`, sanity-check at least:

- omitted / empty / sentinel handling,
- invalid input / rejection path,
- default substitution rules,
- skip interactions,
- normalization rules such as trimming, case-folding, encoding, or locale-dependent behavior when observable.

## 10) Structured syntax presentation

When an instruction’s syntax is inherently multi-line or block-structured:

- show the overall structure in `Syntax` with a fenced `text` block,
- keep `Syntax` as `text`, not `erabasic`,
- keep machine-readable bullet/backtick syntax lines below it,
- prefer fenced `erabasic` blocks in `Examples` for runnable-looking structured examples.

Ordinary single-line instructions/functions should keep the normal bullet/backtick `Syntax` style.

## 11) Keep `coverage.md` in sync

If you discover a new observable contract or a materially new compatibility-relevant edge case that is not already reflected in the reference:

- update `coverage.md` first,
- then update the relevant spec text / built-ins override entry,
- do not mark a surface complete until the coverage state and the actual docs agree.
