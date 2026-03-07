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
- Prefer external, user-visible terminology over internal helper names, temporary variable names, or call-chain descriptions.
- If a behavior matches a stable external spec (e.g. a .NET formatting API), it is OK to reference that external spec directly (example: “equivalent to `Int64.ToString(format)`”).
- Do **not** justify behavior by pointing at internal call chains or internal helper names (e.g. “because `SomeInternalClass.SomeMethod()` does X”).

## Topic completion discipline

Do not describe a topic as `complete`, `done`, or `reimplementation-grade` unless **all major submodels within that topic** have been checked and brought to the same standard.

Guardrails:
- Do **not** treat “the main path is documented” as equivalent to “the whole topic is complete”.
- If a topic includes multiple layers/subsystems (for example: normal output, temporary lines, island layers, readback APIs, or button objects), explicitly verify each layer before claiming completion.
- If one important submodel is still only partially specified, describe the **whole topic** as partial, even if the main path is already strong.
- When a shared topic mentions a built-in family as part of the contract surface, re-check the corresponding built-in entries before calling the topic complete.
- If `coverage.md` still marks the relevant surface as `🟡`, do not claim the topic is complete unless you also update `coverage.md` and can justify the status change.

## Mandatory self-review before claiming reimplementation grade

Before claiming that a topic or built-in group is reimplementation-grade, run an explicit self-check against the questions below.

Checklist:
- **Surface inventory**: Have all major layers / submodels / related built-in surfaces been enumerated?
- **Positive definition**: For each important submodel, did the docs explain how it works, not merely what it is excluded from?
- **Boundary triggers**: Are entry / exit / visibility / overwrite / deletion / persistence triggers stated as concrete rules?
- **Getter / helper classification**: Are helper APIs and getters grouped under the correct state model, rather than inferred from name similarity?
- **Cross-doc sync**: If a shared topic relies on certain built-ins, were those built-in entries updated to the same precision level?
- **Coverage sync**: Does `coverage.md` still expose any major unresolved hole for this exact surface?
- **Reader burden**: Would an independent implementer still need to guess any important branch or lifecycle step? If yes, the topic is not done.

When reporting status after such a review, explicitly distinguish:
- what is complete,
- what remains partial,
- and whether the overall topic is therefore still partial or can genuinely be called complete.

## Public contract fidelity

When a type, method, helper surface, or signature is part of the externally observable contract, prefer preserving it rather than paraphrasing it away.

Guidelines:
- Preserve public/API-facing names when they are part of compatibility.
- If a literal interface/type definition is the clearest contract artifact, it is acceptable to keep or quote that definition rather than replacing it with a looser summary.
- Treat helper APIs exposed to scripts/plugins/extensions as part of the public contract unless there is clear evidence they are purely internal.

## Reader-first precision

Write for a reader who wants to reproduce behavior, not for a reader who already knows the engine internals.

Guidelines:
- Prefer the most precise wording that stays readable to a newcomer.
- Avoid unexplained internal identifiers when a user-facing description is sufficient.
- When internal terminology must be mentioned for compatibility, immediately anchor it to an observable meaning.
- If a mechanism is easy to misread from prose alone, add a small example instead of relying on dense wording.

## Ambiguity tightening

When a statement would materially affect compatibility, do not leave it at vague wording if the behavior can be determined.

Prefer replacing vague phrases such as:
- `some cases`
- `typically`
- `in many cases`
- `depending on ...`

with exact conditions, explicit branch rules, or narrowly scoped exceptions.

If exact behavior is still unknown, explicitly mark the uncertainty and fence it so readers can see what is known vs unknown.

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

## Omitted vs empty vs sentinel discipline

When documenting parameters, argument lists, defaults, or optional tails, explicitly distinguish these cases unless the external contract truly makes them equivalent:

- omitted argument / omitted slot
- explicit empty value (for example `""`)
- explicit sentinel value (for example `0`, `-1`)
- supplied-but-invalid value

Authoring rules:
- In this reference, parameters are required unless explicitly marked `optional`. `optional` means the argument position is genuinely omittable. Do not describe a parameter as `optional` if the call shape still requires that argument position and only allows an empty value.
- Only write `default X` when omission is observably equivalent to supplying `X`.
- State whether omission is handled at parse time, binding time, or runtime semantic handling when that distinction affects observable behavior.
- State the observable result of omission precisely: error, warning + substitution, silent substitution, preserved prior value, ignored tail, or no effect.
- Treat coercion / auto-conversion as a separate rule from omission unless the public contract explicitly unifies them.
- If later optional parameters depend on earlier ones, document the tail behavior explicitly (for example: ignored tail, disabled tail, or per-slot defaults).

For reimplementation-grade entries, the reader should never have to guess whether `omitted`, `""`, `0`, and supplied-but-invalid values are distinct cases or collapsed into one behavior.

## Completeness checklist for `Progress state: complete`

Before marking an override entry `complete`, sanity-check the most common “spec holes”:

- **Omitted / empty / sentinel handling**: distinguish omitted argument vs empty string vs `0` / other sentinel values where relevant.
- **Invalid input / rejection path** (especially for input and parsing built-ins):
  - Does the operation reject and retry (stay in a wait state), clamp, coerce, or error?
  - Are any `RESULT*` / side-channel variables written on rejection, or only on acceptance?
  - Is rejected text echoed to output, or suppressed?
- **Default substitution rules**: when a default is used (e.g. “empty input uses default only when not running a timer”).
- **Skip interactions**: `SKIPDISP` / `MesSkip` / skip-print modes, including whether evaluation/side effects happen.
- **Normalization rules**: case-folding, trimming, encoding, or locale-dependent behaviors (document only if observable/compat-relevant).

When a behavior is “obvious” to script authors but can still fork compatibility (e.g. empty/invalid handling in `INPUT`), prefer one extra explicit bullet over relying on reader assumptions.
