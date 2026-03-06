# Authoring rules (`erabasic-reference/`)

This file contains the default rules used when writing or editing this reference (including built-ins overrides).

## Interaction protocol (analysis-only requests)

If the user explicitly requests “analysis only” / “plan first” / “do not modify” (e.g. `仅分析`, `先plan`, `不要动手`, `不要进行修改`):

- Treat the workspace as **read-only**:
  - Do not edit files (`apply_patch`), regenerate outputs, or otherwise make persistent changes.
  - Avoid commands whose primary effect is to modify tracked outputs (generators, formatters, etc.).
- You may still inspect existing files (read-only), search, and propose a plan or draft text in-chat.
- Before switching from analysis to execution (any persistent change), obtain **explicit user permission** (“进行修改/开始改/动手”等).

## Rule persistence (when user says “remember”)

If the user asks the assistant to “remember” a rule (e.g. `记住`, `把这个规则记一下`, `持久化此规则`), automatically persist it into `erabasic-reference/agents.md` (or another explicitly specified location) without requiring an extra prompt.

## Refactor policy (default: breaking changes are OK)

When updating schemas/section structures/tooling used by this reference, prefer an **aggressive break + one-shot migration** over compatibility layers.
Do not keep legacy parsing/rendering branches just to accept old section titles; instead, migrate the docs and make the generator strict.

## No generator hacks

Do not add ad-hoc “in-script override” dictionaries or similar fallback sources inside generators.
Overrides must live in `erabasic-reference/builtins-overrides/**/<NAME>.md` so the documentation source of truth stays reviewable and diffable.

## Intentional explanatory notes

If a subsection is explicitly labeled as an intentional explanatory note (for example `Counterfactual design note (intentional)`), preserve it by default even when it is not part of the current accepted-language contract. Treat such sections as boundary-clarification material, not dead text, unless the user explicitly asks to remove or rewrite them.

## Reimplementation-grade writing

When a built-ins override entry is marked `**Progress state**: complete`, it must be detailed enough that an independent implementation can reproduce compatible behavior **without reading this engine’s source code**.

Rule of thumb:
- Specify **observable contracts** (inputs → outputs/state/errors) in engine-agnostic language.
- If a behavior matches a stable external spec (e.g. a .NET formatting API), it is OK to reference that external spec directly (example: “equivalent to `Int64.ToString(format)`”).
- Do **not** justify behavior by pointing at internal call chains or internal helper names (e.g. “because `SomeInternalClass.SomeMethod()` does X”).

## Default evaluation rules (document exceptions only)

Unless an entry explicitly says otherwise:
- Arguments are evaluated left-to-right.
- Each argument (and any subscripts inside it) is evaluated once.
- If output skipping (`SKIPDISP` / script-runner skip-print mode) causes a built-in to be skipped, it performs **no evaluation** and has **no side effects**.

Only document evaluation order/count when it deviates from the defaults above.

## Avoid ambiguous range notation

Avoid `1..99`-style range notation in user-facing contracts.
Prefer explicit inequalities (e.g. `1 <= x <= 99`, `0 <= i < length`) so readers don’t need to guess whether a bound is inclusive or exclusive.

## Concision rule

If a parameter’s evaluation/typing/parsing follows common EraBasic expectations and has no compatibility traps, omit it.
Prefer documenting only the parts that can surprise an implementer or a script author (parsing quirks, clamping, side-channel writes, skip behavior, etc.).

## Keep `coverage.md` in sync

If you discover any new observable contract (new built-in behavior, new host/UI contract, new file convention, or any compatibility-relevant edge case) that is not already reflected in the reference:

- Update `coverage.md` first (add a new tracking bullet/section and mark it ✅/🟡/⛔/🔁 as appropriate).
- Then implement the actual spec text in the relevant document(s) or built-ins override entry.

## Completeness checklist for `Progress state: complete`

Before marking an override entry `complete`, sanity-check the most common “spec holes”:

- **Empty / null handling**: distinguish omitted argument vs empty string vs `0` where relevant.
- **Invalid input / rejection path** (especially for input and parsing built-ins):
  - Does the operation reject and retry (stay in a wait state), clamp, coerce, or error?
  - Are any `RESULT*` / side-channel variables written on rejection, or only on acceptance?
  - Is rejected text echoed to output, or suppressed?
- **Default substitution rules**: when a default is used (e.g. “empty input uses default only when not running a timer”).
- **Skip interactions**: `SKIPDISP` / `MesSkip` / skip-print modes, including whether evaluation/side effects happen.
- **Normalization rules**: case-folding, trimming, encoding, or locale-dependent behaviors (document only if observable/compat-relevant).

When a behavior is “obvious” to script authors but can still fork compatibility (e.g. empty/invalid handling in `INPUT`), prefer one extra explicit bullet over relying on reader assumptions.
