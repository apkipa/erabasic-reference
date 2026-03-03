# Legacy (Core Control-Flow Implementation Notes)

This file is **legacy**.

It previously contained an implementation-oriented walkthrough of core control-flow / call / return behavior, plus a large instruction keyword catalog.

The content has been migrated into the main, self-contained reference:

- Core control flow (`IF/SIF`, loops, `SELECTCASE`, try-family): `control-flow.md`
- Runtime execution model (advance-first execution, markers, stack, `JUMP` vs `CALL`): `runtime-model.md`
- Call-target tail syntax `NAME[...]` (“subNames”, parsed but ignored here): `functions.md`
- Label-side `@NAME[...]` parsing (validated then discarded): `labels.md`
- Full built-in instruction + method catalog (engine-extracted + overrides): `builtins-reference.md`

This file is kept only to avoid breaking older links and may be removed in the future.

