#!/usr/bin/env python3
"""
Generate a single Markdown catalog for all EraBasic built-in instructions and expression functions
from the EvilMask/Emuera engine source.

Outputs:
  - User-facing reference (manual overrides only):
      erabasic-reference/builtins-reference.md
  - Writer/debug engine dump (engine-extracted skeletons, signatures, and refs):
      erabasic-reference/appendix/tooling/builtins-reference-engine.md

Design goals:
  - English
  - No tables (per user preference)
  - Source of truth: emuera.em (engine code)

Notes:
  - The user-facing doc intentionally omits engine-internal validation structures and file/line refs.
  - The engine-dump doc exists for fact-checking and doc-authoring only.
"""

from __future__ import annotations

from pathlib import Path
import argparse
import datetime as _dt
import os
import re
import sys

import reference_common as ref_common
import reference_engine_registry as ref_engine
import reference_lint as ref_lint


REPO_ROOT = ref_common.MONOREPO_ROOT

PATH_FUNCTION_IDENTIFIER = ref_engine.PATH_FUNCTION_IDENTIFIER
PATH_FUNCTION_ARG_TYPE = ref_engine.PATH_FUNCTION_ARG_TYPE
PATH_ARGUMENT_BUILDER = ref_engine.PATH_ARGUMENT_BUILDER
PATH_SCRIPT_PROC = ref_engine.PATH_SCRIPT_PROC
PATH_METHOD_CREATOR = ref_engine.PATH_METHOD_CREATOR
PATH_METHOD_IMPL = ref_engine.PATH_METHOD_IMPL

OUTPUT_MD = ref_common.OUTPUT_MD
OUTPUT_ENGINE_MD = ref_common.OUTPUT_ENGINE_MD
OUTPUT_INDEX_MD = ref_common.OUTPUT_INDEX_MD
OUTPUT_PROGRESS_MD = ref_common.OUTPUT_PROGRESS_MD

_lines = ref_common.lines
_split_flags = ref_common.split_flags
_format_flags = ref_common.format_flags
_md_anchor = ref_common.md_anchor

InstructionReg = ref_engine.InstructionReg
StructuralInfo = ref_engine.StructuralInfo
ArgSpecInfo = ref_engine.ArgSpecInfo
ImplSnippet = ref_engine.ImplSnippet
MethodReg = ref_engine.MethodReg
MethodClassInfo = ref_engine.MethodClassInfo

parse_structural_info = ref_engine.parse_structural_info
parse_function_argtype_hints = ref_engine.parse_function_argtype_hints
parse_instruction_registrations = ref_engine.parse_instruction_registrations
_scan_csharp_classes = ref_engine._scan_csharp_classes
_extract_instruction_class_info = ref_engine._extract_instruction_class_info
_infer_arg_types_from_argbuilder_lines = ref_engine._infer_arg_types_from_argbuilder_lines
parse_switch_cases = ref_engine.parse_switch_cases
parse_argument_specs = ref_engine.parse_argument_specs
parse_method_registrations = ref_engine.parse_method_registrations
parse_method_classes = ref_engine.parse_method_classes
index_line_numbers_for_cases = ref_engine.index_line_numbers_for_cases
index_line_numbers_for_method_classes = ref_engine.index_line_numbers_for_method_classes

def _render_section(title: str, body_lines: list[str]) -> list[str]:
    out: list[str] = [f"**{title}**"]
    if not body_lines:
        out.append("- (TODO)")
        return out
    out.extend(body_lines)
    return out


def _parse_tag_lines(lines: list[str]) -> list[str]:
    tags: list[str] = []
    for raw in lines:
        t = raw.strip()
        if not t:
            continue
        if t.startswith(("-", "*")):
            t = t[1:].strip()
        t = t.strip("`").strip()
        if not t:
            continue
        tags.append(t)
    # stable order, unique
    seen: set[str] = set()
    out: list[str] = []
    for t in tags:
        if t in seen:
            continue
        seen.add(t)
        out.append(t)
    return out


def _render_instruction_entry_user(reg: InstructionReg) -> str:
    parts: list[str] = [f"## {reg.name} (instruction)"]
    override = ref_lint.load_override_sections("instruction", reg.name)
    if not ref_lint.has_user_facing_content("instruction", reg.name):
        parts.append("**Summary**")
        parts.append("- (TODO: not yet documented)")
        return "\n".join(parts) + "\n"
    for title in ref_lint.USER_INSTRUCTION_SECTIONS:
        if title == "Tags" and not any(ln.strip() for ln in override.get("Tags", [])):
            continue
        parts.append("")
        parts.extend(_render_section(title, override.get(title, [])))
    return "\n".join(parts) + "\n"


def _render_method_entry_user(reg: MethodReg) -> str:
    parts: list[str] = [f"## {reg.name} (expression function)"]
    override = ref_lint.load_override_sections("method", reg.name)
    if not ref_lint.has_user_facing_content("method", reg.name):
        parts.append("**Summary**")
        parts.append("- (TODO: not yet documented)")
        return "\n".join(parts) + "\n"
    for title in ref_lint.USER_METHOD_SECTIONS:
        if title == "Tags" and not any(ln.strip() for ln in override.get("Tags", [])):
            continue
        parts.append("")
        parts.extend(_render_section(title, override.get(title, [])))
    return "\n".join(parts) + "\n"


def generate_builtins_index_md(
    *,
    gen_date: str,
    instr_regs: list[InstructionReg],
    method_regs: list[MethodReg],
) -> str:
    """
    Build a user-facing tag index based solely on override files.

    Only entries with user-facing content are indexed.
    """
    tag_map: dict[str, list[tuple[str, str]]] = {}  # tag -> [(kind, name)]
    uncategorized: list[tuple[str, str]] = []

    def add(kind: str, name: str, tags: list[str]) -> None:
        if not tags:
            uncategorized.append((kind, name))
            return
        for tg in tags:
            tag_map.setdefault(tg, []).append((kind, name))

    for r in instr_regs:
        if not ref_lint.has_user_facing_content("instruction", r.name):
            continue
        secs = ref_lint.load_override_sections("instruction", r.name)
        tags = _parse_tag_lines(secs.get("Tags", []))
        add("instruction", r.name, tags)

    for r in method_regs:
        if not ref_lint.has_user_facing_content("method", r.name):
            continue
        secs = ref_lint.load_override_sections("method", r.name)
        tags = _parse_tag_lines(secs.get("Tags", []))
        add("method", r.name, tags)

    def link(kind: str, name: str) -> str:
        suffix = "(instruction)" if kind == "instruction" else "(expression function)"
        anchor = _md_anchor(f"{name} {suffix}")
        return f"- [`{name}`](builtins-reference.md#{anchor}) ({kind})"

    out: list[str] = []
    out.append("# EraBasic Built-ins Index (by tag)")
    out.append("")
    out.append(f"Generated on `{gen_date}`.")
    out.append("")
    out.append("> [!WARNING]")
    out.append("> This file is generated. Do **not** edit `builtins-index.md` by hand.")
    out.append(
        f"> Update `{ref_lint.OVERRIDES_DIR.relative_to(REPO_ROOT)}/**` or the generator/tooling inputs, then regenerate this file."
    )
    out.append("")
    out.append("This index is built from `builtins-overrides/**` tags and links into `builtins-reference.md`.")
    out.append("")

    for tg in sorted(tag_map.keys(), key=lambda s: s.lower()):
        out.append(f"## {tg}")
        out.append("")
        items = sorted(tag_map[tg], key=lambda it: (it[0], it[1]))
        for kind, name in items:
            out.append(link(kind, name))
        out.append("")

    if uncategorized:
        out.append("## (uncategorized)")
        out.append("")
        for kind, name in sorted(uncategorized, key=lambda it: (it[0], it[1])):
            out.append(link(kind, name))
        out.append("")

    return "\n".join(out).rstrip() + "\n"


def _render_instruction_entry(
    reg: InstructionReg,
    structural: StructuralInfo | None,
    arg_specs: dict[str, ArgSpecInfo],
    instr_class_impl: dict[str, tuple[Path, int, int, list[str]]],
    switch_impl: dict[str, ImplSnippet],
) -> str:
    parts: list[str] = [f"## {reg.name} (instruction)"]

    override = ref_lint.load_override_sections("instruction", reg.name)

    # Best-effort: some AInstruction classes set ArgBuilder to a standard FunctionArgType,
    # but the registration site does not declare it. Infer it from the class body when
    # it is unambiguous (exactly one FunctionArgType referenced in ArgBuilder assignments).
    inferred_arg_type: str | None = None
    inferred_arg_note: str | None = None
    cls_impl: tuple[Path, int, int, list[str]] | None = None
    cls_name: str | None = None
    cls_argb_lines: list[str] = []
    cls_flag_lines: list[str] = []
    cls_ops: list[str] = []
    cls_thr: list[str] = []

    if reg.reg_kind not in ("Switch", "Internal"):
        if reg.impl_ctor:
            mm = re.match(r"new\s+([A-Za-z0-9_]+)\b", reg.impl_ctor)
            if mm:
                cls_name = mm.group(1)
        if cls_name and cls_name not in instr_class_impl:
            cls_name = None
        if not cls_name:
            cls_name = f"{reg.name}_Instruction"
        if cls_name in instr_class_impl:
            cls_impl = instr_class_impl[cls_name]
            _p, _start, _end, _block = cls_impl
            cls_argb_lines, cls_flag_lines, cls_ops, cls_thr = _extract_instruction_class_info(_block, cls_name)
            candidates = _infer_arg_types_from_argbuilder_lines(cls_argb_lines)
            if reg.arg_type is None and len(candidates) == 1:
                inferred_arg_type = candidates[0]
                inferred_arg_note = f"(inferred from `{cls_name}` ArgBuilder assignment)"

    # Summary
    parts.extend(_render_section("Summary", override.get("Summary", [])))

    # Metadata
    meta: list[str] = []
    effective_arg_type = reg.arg_type or inferred_arg_type
    if effective_arg_type:
        note = ""
        if reg.arg_type is None and inferred_arg_note:
            note = f" {inferred_arg_note}"
        meta.append(f"- Arg spec: `{effective_arg_type}` (see #{_md_anchor('Argument spec: ' + effective_arg_type)}){note}")
    else:
        meta.append("- Arg spec: (instruction-defined)")
    if reg.impl_ctor:
        meta.append(f"- Implementor (registration): `{reg.impl_ctor}`")
    if reg.flags_expr:
        meta.append(f"- Flags (registration): {_format_flags(_split_flags(reg.flags_expr))}")
    if reg.additional_flags_expr:
        meta.append(f"- Additional flags (registration): {_format_flags(_split_flags(reg.additional_flags_expr))}")
    if structural and structural.match_end:
        meta.append(f"- Structural match end: `{structural.match_end}`")
    if structural and structural.parent:
        meta.append(f"- Structural parent: `{structural.parent}`")
    for n in reg.notes:
        meta.append(f"- Note: {n}")
    parts.append("")
    parts.extend(_render_section("Metadata", meta))

    # Syntax / Arguments (best-effort from arg spec hints + builder metadata)
    spec = arg_specs.get(effective_arg_type) if effective_arg_type else None

    if "Syntax" in override:
        syntax = override["Syntax"]
    else:
        syntax = []
        if spec:
            if spec.hint_en:
                syntax.append(f"- Hint (translated, best-effort): {spec.hint_en}")
            if spec.hint_raw:
                syntax.append(f"- Hint (raw comment): `{spec.hint_raw}`")
            syntax.append("- General shape: `INSTR arg1, arg2, ...` (exact parsing depends on the builder).")

    if "Arguments" in override:
        arguments = override["Arguments"]
    else:
        arguments = []
        if spec:
            arguments.append(f"- Builder: `{spec.builder_expr}`")
            for ln in spec.summary_lines[:6]:
                arguments.append(f"- {ln}")

    parts.append("")
    parts.extend(_render_section("Syntax", syntax))
    parts.append("")
    parts.extend(_render_section("Arguments", arguments))

    # Semantics / Errors: engine-extracted key operations + throws
    semantics: list[str] = list(override.get("Semantics", []))
    errors: list[str] = list(override.get("Errors & validation", []))
    refs: list[str] = []

    refs.append(f"- Registration: `{PATH_FUNCTION_IDENTIFIER.relative_to(REPO_ROOT)}`")
    if effective_arg_type:
        refs.append(f"- Arg builder mapping: `{PATH_ARGUMENT_BUILDER.relative_to(REPO_ROOT)}` (search `FunctionArgType.{effective_arg_type}`)")

    if reg.reg_kind == "Switch":
        impl = switch_impl.get(reg.name)
        if impl:
            if impl.line_no:
                refs.append(f"- Execution: `{PATH_SCRIPT_PROC.relative_to(REPO_ROOT)}`:{impl.line_no} (case `{reg.name}`)")
            else:
                refs.append(f"- Execution: {impl.where}")
            if impl.key_ops:
                semantics.append("- Engine-extracted notes (key operations):")
                for op in impl.key_ops[:12]:
                    semantics.append(f"  - `{op}`")
            if impl.throws:
                errors.append("- Engine-extracted notes (throws/errors):")
                for t in impl.throws[:10]:
                    errors.append(f"  - `{t}`")
        else:
            if not semantics:
                semantics.append("- (TODO)")
            refs.append(f"- Execution: `{PATH_SCRIPT_PROC.relative_to(REPO_ROOT)}`")
    elif reg.reg_kind == "Internal":
        if not semantics:
            semantics.append("- Internal pseudo-instruction used by the parser/runtime; not a user-facing keyword.")
        refs.append(f"- Internal: `{PATH_FUNCTION_IDENTIFIER.relative_to(REPO_ROOT)}` (`setFunc` / `SETFunction`)")
    else:
        if cls_impl and cls_name:
            p, start, _end, _block = cls_impl
            refs.append(f"- Execution: `{p.relative_to(REPO_ROOT)}`:{start} (`{cls_name}`)")
            base_flag_lines = [fl for fl in cls_flag_lines if re.match(r"^flag\\s*=", fl)]
            if base_flag_lines:
                semantics.append("- Engine-extracted notes (base flags from class):")
                for fl in base_flag_lines[:5]:
                    semantics.append(f"  - `{fl}`")
            if cls_ops:
                semantics.append("- Engine-extracted notes (key operations):")
                for op in cls_ops[:12]:
                    semantics.append(f"  - `{op}`")
            if cls_thr:
                errors.append("- Engine-extracted notes (throws/errors):")
                for t in cls_thr[:10]:
                    errors.append(f"  - `{t}`")
        else:
            if not semantics:
                semantics.append("- (TODO)")

    parts.append("")
    parts.extend(_render_section("Semantics", semantics))
    parts.append("")
    parts.extend(_render_section("Errors & validation", errors))
    parts.append("")
    parts.extend(_render_section("Examples", override.get("Examples", [])))
    parts.append("")
    parts.extend(_render_section("Engine references (fact-check)", refs))

    return "\n".join(parts) + "\n"


def _render_method_entry(reg: MethodReg, info: MethodClassInfo | None) -> str:
    parts: list[str] = [f"## {reg.name} (expression function)"]

    override = ref_lint.load_override_sections("method", reg.name)

    parts.extend(_render_section("Summary", override.get("Summary", [])))

    meta: list[str] = [f"- Implementor: `{reg.ctor_expr}`"]
    if info and info.return_type:
        meta.append(f"- Return type: `{info.return_type}`")
    else:
        meta.append("- Return type: (see engine implementation)")
    if info and info.can_restructure is not None:
        meta.append(f"- Constant folding (`CanRestructure`): `{info.can_restructure}`")
    if info and info.mentions_name_dispatch:
        meta.append("- Note: implementation appears to branch on the method name (`Name`), so aliases may differ by name.")
    parts.append("")
    parts.extend(_render_section("Metadata", meta))

    parts.append("")
    parts.extend(_render_section("Syntax", override.get("Syntax", [])))

    sig: list[str] = []
    if "Signatures / argument rules" in override:
        sig = override["Signatures / argument rules"]
    else:
        if info:
            for r in info.arg_rules[:10]:
                sig.append(f"- {r}")
    parts.append("")
    parts.extend(_render_section("Signatures / argument rules", sig))
    parts.append("")
    parts.extend(_render_section("Arguments", override.get("Arguments", [])))

    sem: list[str] = list(override.get("Semantics", []))
    errs: list[str] = list(override.get("Errors & validation", []))
    refs: list[str] = []
    refs.append(f"- Registration: `{PATH_METHOD_CREATOR.relative_to(REPO_ROOT)}` (dictionary `methodList`)")
    if info and info.start_line:
        refs.append(f"- Implementation: `{PATH_METHOD_IMPL.relative_to(REPO_ROOT)}`:{info.start_line} (class `{reg.class_name}`)")
    else:
        refs.append(f"- Implementation: `{PATH_METHOD_IMPL.relative_to(REPO_ROOT)}` (class `{reg.class_name}`)")
    if info and info.key_ops:
        sem.append("- Engine-extracted notes (key operations):")
        for op in info.key_ops[:12]:
            sem.append(f"  - `{op}`")
    if info and info.throws:
        errs.append("- Engine-extracted notes (throws/errors):")
        for t in info.throws[:10]:
            errs.append(f"  - `{t}`")

    parts.append("")
    parts.extend(_render_section("Semantics", sem))
    parts.append("")
    parts.extend(_render_section("Errors & validation", errs))
    parts.append("")
    parts.extend(_render_section("Examples", override.get("Examples", [])))
    parts.append("")
    parts.extend(_render_section("Engine references (fact-check)", refs))

    return "\n".join(parts) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Generate and/or validate EraBasic built-ins documentation outputs.")
    ap.add_argument("--no-write", action="store_true", help="Do not write any markdown outputs; run validation only.")
    ap.add_argument(
        "--no-fail",
        action="store_true",
        help="Do not exit non-zero on validation issues (still prints a warning report).",
    )
    ap.add_argument("--report", action="store_true", help="Print a detailed validation report to stderr.")
    ap.add_argument(
        "--fail-on",
        action="append",
        default=[],
        choices=ref_lint.FAIL_ON_CODES,
        help="Exit non-zero if any matching validation issue exists (can be repeated).",
    )
    args = ap.parse_args(argv)

    fi_lines = _lines(PATH_FUNCTION_IDENTIFIER)
    fa_lines = _lines(PATH_FUNCTION_ARG_TYPE)
    ab_lines = _lines(PATH_ARGUMENT_BUILDER)
    sp_lines = _lines(PATH_SCRIPT_PROC)
    creator_lines = _lines(PATH_METHOD_CREATOR)
    method_lines = _lines(PATH_METHOD_IMPL)

    structural_map = parse_structural_info(fi_lines)
    instr_regs = parse_instruction_registrations(fi_lines)
    argtype_hints = parse_function_argtype_hints(fa_lines)
    arg_specs = parse_argument_specs(ab_lines, argtype_hints)
    switch_impl = parse_switch_cases(sp_lines)
    case_line_map = index_line_numbers_for_cases(sp_lines)
    switch_impl = {
        k: ImplSnippet(where=v.where, line_no=case_line_map.get(k), key_ops=v.key_ops, throws=v.throws) for k, v in switch_impl.items()
    }

    # Index instruction classes (best-effort) under Statements/
    instr_class_impl = _scan_csharp_classes(PATH_ARGUMENT_BUILDER.parent, class_name_suffix="_Instruction")

    method_regs = parse_method_registrations(creator_lines)
    method_classes = parse_method_classes(method_lines)
    method_line_map = index_line_numbers_for_method_classes(method_lines)
    method_classes = {
        k: MethodClassInfo(
            class_name=v.class_name,
            start_line=method_line_map.get(k),
            return_type=v.return_type,
            can_restructure=v.can_restructure,
            arg_rules=v.arg_rules,
            key_ops=v.key_ops,
            throws=v.throws,
            mentions_name_dispatch=v.mentions_name_dispatch,
        )
        for k, v in method_classes.items()
    }

    issues = ref_lint.validate_reference_docs(instr_regs, method_regs)
    ref_lint.print_validation_report(issues, verbose=args.report)

    exit_code = 0
    if issues and not args.no_fail:
        # Default behavior: fail on *any* validation issue.
        # If --fail-on is specified, restrict failure to those codes.
        if args.fail_on:
            wanted = set(args.fail_on)
            if any(it.code in wanted for it in issues):
                exit_code = 2
        else:
            exit_code = 2

    if args.no_write:
        return exit_code

    gen_date = _dt.date.today().isoformat()

    # ---------------------------------------------------------------------
    # User-facing doc (manual overrides only)
    # ---------------------------------------------------------------------
    md_user: list[str] = []
    md_user.append("# EraBasic Built-ins Reference (Emuera / EvilMask)")
    md_user.append("")
    md_user.append(f"Generated on `{gen_date}`.")
    md_user.append("")
    md_user.append("> [!WARNING]")
    md_user.append("> This file is generated. Do **not** edit `builtins-reference.md` by hand.")
    md_user.append(
        f"> Make persistent content changes in `{ref_lint.OVERRIDES_DIR.relative_to(REPO_ROOT)}/**` or the generator/tooling inputs, then regenerate this file."
    )
    md_user.append("")
    md_user.append("This file is **user-facing**: it contains only human-written documentation overrides.")
    md_user.append("Undocumented built-ins are listed but contain only a `(TODO)` placeholder.")
    md_user.append("")
    md_user.append("For engine-extracted skeletons, validation structures, and file/line references, see:")
    md_user.append(f"- `{OUTPUT_ENGINE_MD.relative_to(REPO_ROOT)}` (writer/debug dump; not user-facing)")
    md_user.append("")
    md_user.append("# Conventions used by this reference")
    md_user.append("")
    md_user.append("Unless an entry explicitly says otherwise, interpret this reference using the conventions below.")
    md_user.append("")
    md_user.append("## Evaluation order (default)")
    md_user.append("")
    md_user.append("- Arguments are evaluated left-to-right.")
    md_user.append("- Each argument (and any subscripts inside it) is evaluated once.")
    md_user.append("- If an entry describes a different evaluation rule, that entry overrides this default.")
    md_user.append("")
    md_user.append("## Optional arguments and defaults")
    md_user.append("")
    md_user.append("- Whether an argument can be omitted is defined by an entry’s `Syntax` (instructions) or `Signatures` (methods).")
    md_user.append("- Optional arguments can be omitted by leaving an empty argument slot (e.g. `FUNC(a, , c)`); in that case the argument value is treated as “omitted” for the purpose of default substitution.")
    md_user.append("- Default values/behaviors for omitted arguments are documented inline under that entry’s `Arguments` (e.g. “optional, default `0`”).")
    md_user.append("- Omitted arguments are not the same as passing an empty string; if empty-string behavior matters for compatibility, the entry documents it explicitly.")
    md_user.append("")
    md_user.append("## Output skipping / skipped execution")
    md_user.append("")
    md_user.append("- Some instructions are skipped entirely when output skipping is active (e.g. `SKIPDISP` / skip-print mode).")
    md_user.append("- When an instruction is **skipped**, it is not executed: arguments are not evaluated and there are no side effects.")
    md_user.append("- Note: the engine may still parse/compile the line’s arguments before the skip check; skips only suppress execution-time evaluation and side effects.")
    md_user.append("")
    md_user.append("## Range notation")
    md_user.append("")
    md_user.append("- This reference avoids `a..b` range notation, because inclusive/exclusive bounds are easy to misread.")
    md_user.append("- Ranges are written using explicit inequalities (e.g. `0 <= i < n`) or half-open interval notation (e.g. `[startIndex, lastIndex)`).")
    md_user.append("")
    md_user.append("## Terminology: errors vs rejection")
    md_user.append("")
    md_user.append("- **Error**: the engine reports an error. This is distinct from rejection; the exact aftermath is documented per topic/built-in where relevant.")
    md_user.append("- **Reject** (input/choice contexts): the engine ignores the input and continues waiting; side effects such as `RESULT*` writes happen only as documented for the accepting path.")
    md_user.append("")
    md_user.append("# Expression functions as statements")
    md_user.append("")
    md_user.append("Some expression functions are also accepted as standalone statements (without `=` assignment).")
    md_user.append("In statement form, the engine evaluates the function and writes the return value to:")
    md_user.append("- `RESULT` for integer-returning functions")
    md_user.append("- `RESULTS` for string-returning functions")
    md_user.append("")

    md_user.append("# Instructions")
    md_user.append("")
    for reg in instr_regs:
        md_user.append(_render_instruction_entry_user(reg).rstrip())
        md_user.append("")

    md_user.append("# Expression functions (methods)")
    md_user.append("")
    for reg in method_regs:
        md_user.append(_render_method_entry_user(reg).rstrip())
        md_user.append("")

    OUTPUT_MD.write_text("\n".join(md_user).rstrip() + "\n", encoding="utf-8")

    # Tag index (user-facing; derived from overrides)
    OUTPUT_INDEX_MD.write_text(
        generate_builtins_index_md(gen_date=gen_date, instr_regs=instr_regs, method_regs=method_regs),
        encoding="utf-8",
    )

    # ---------------------------------------------------------------------
    # Engine dump (writer/debug)
    # ---------------------------------------------------------------------
    md: list[str] = []
    md.append("# EraBasic Built-ins Reference — Engine Dump (Emuera / EvilMask)")
    md.append("")
    md.append(f"Generated from engine source on `{gen_date}`.")
    md.append("")
    md.append("> [!WARNING]")
    md.append("> This file is generated. Do **not** edit `appendix/tooling/builtins-reference-engine.md` by hand.")
    md.append("> Change the generator/tooling inputs, then regenerate this file.")
    md.append("")
    md.append("This file is **not user-facing**.")
    md.append("It exists for doc authors and fact-checking, and includes engine-extracted skeletons, validation structures, and file/line references.")
    md.append("")
    md.append("User-facing built-ins documentation lives in:")
    md.append(f"- `{OUTPUT_MD.relative_to(REPO_ROOT)}`")
    md.append("")
    md.append("This document is intentionally **no-table** and uses a per-entry template:")
    md.append("- Summary / Syntax / Arguments / Semantics / Errors / Examples / Engine refs")
    md.append("")
    md.append("Important:")
    md.append("- The generator can reliably extract hooks (argument builders, flags, code entry points).")
    md.append("- Deeper semantic structure often requires manual analysis; “engine-extracted key operations” are a starting point, not a full spec.")
    md.append("")

    md.append("# Expression functions as statements (METHOD-dispatch)")
    md.append("")
    md.append("In this engine, **expression functions** (the `# Expression functions (methods)` section below) are also registered as **instruction keywords** when there is no name conflict with an existing instruction keyword.")
    md.append("This allows writing method names as standalone statements (without `=` assignment).")
    md.append("")
    md.append("Statement form (best-effort description):")
    md.append("- A line whose keyword matches an expression function name is executed by a shared internal instruction (`METHOD_Instruction`).")
    md.append("- The argument text is parsed as comma-separated expressions (parentheses are allowed but not required).")
    md.append("- The engine validates argument types/count using the method’s own argument checker.")
    md.append("- The method is evaluated; if it returns:")
    md.append("  - `long`: assigns `RESULT` (integer).")
    md.append("  - `string`: assigns `RESULTS` (string).")
    md.append("")
    md.append("Examples:")
    md.append("- `TOSTR 42` sets `RESULTS` to `\"42\"`.")
    md.append("- `FINDCHARA NAME, \"Alice\"` sets `RESULT` to the found index (or `-1`).")
    md.append("")

    # Argument spec glossary
    md.append("# Argument specs (FunctionArgType)")
    md.append("")
    md.append("Each instruction registered with an `Arg spec` references one of the `FunctionArgType` values below.")
    md.append("The entries here are generated from `ArgumentParser.Initialize()` and (best-effort) builder-class constructors.")
    md.append("")
    md.append("How to interpret argument parsing (important):")
    md.append("- The `Arg spec` / builder largely determines whether the argument region is parsed as raw text vs expressions vs FORM, and whether `;` starts an inline comment or is literal.")
    md.append("- This document intentionally does not repeat the parsing rules per instruction. See `argument-parsing-modes.md` for the normative, self-contained parsing-mode definitions and examples.")
    md.append("")

    for argt in sorted(arg_specs):
        spec = arg_specs[argt]
        md.append(f"## Argument spec: {argt}")
        md.append("")
        md.append(f"- Builder: `{spec.builder_expr}`")
        if spec.hint_en:
            md.append(f"- Hint (translated, best-effort): {spec.hint_en}")
        if spec.hint_raw:
            md.append(f"- Hint (raw comment): `{spec.hint_raw}`")
        for ln in spec.summary_lines:
            md.append(f"- {ln}")
        md.append("")

    # Instructions
    md.append("# Instructions")
    md.append("")
    md.append(f"Total (engine-registered keywords, incl. internal `SET`): `{len(instr_regs)}`.")
    md.append("")
    for reg in instr_regs:
        structural = structural_map.get(reg.name)
        md.append(
            _render_instruction_entry(
                reg=reg,
                structural=structural,
                arg_specs=arg_specs,
                instr_class_impl=instr_class_impl,
                switch_impl=switch_impl,
            ).rstrip()
        )
        md.append("")

    # Methods
    md.append("# Expression functions (methods)")
    md.append("")
    md.append("## How to read method argument rules")
    md.append("")
    md.append("Method entries describe argument checking using one of two engine models:")
    md.append("- `argumentTypeArray = [typeof(...), ...]`: fixed arity and fixed operand types (`long` vs `string`).")
    md.append("- `argumentTypeArrayEx`: a list of `ArgTypeList` signature options used for refs/arrays/variadics/optional args.")
    md.append("")
    md.append("For `argumentTypeArrayEx` entries:")
    md.append("- Each `ArgTypeList:` line is one **signature option** (an overload-like alternative). Any one option may match; the engine accepts the first one that passes all checks.")
    md.append("- `OmitStart = k` is a **0-based index** controlling omission/`null`:")
    md.append("  - Argument count must satisfy `k <= argc <= len(ArgTypes)` (unless variadic). If `OmitStart = -1`, then `argc` must equal `len(ArgTypes)` (unless variadic).")
    md.append("  - Trailing arguments may be omitted by passing fewer than `len(ArgTypes)` arguments (method supplies defaults in its implementation, typically by checking `arguments.Count`).")
    md.append("  - A blank argument inside the call (e.g. `FUNC(a,,c)` or `FUNC(a,)`) becomes `null`. `null` is rejected for positions `< OmitStart`, and may also be rejected at/after `OmitStart` when the rule includes `DisallowVoid`.")
    md.append("- Common `ArgType` flags you may see:")
    md.append("  - `Ref*`: argument must be a variable term (by-reference-like), not an arbitrary expression.")
    md.append("  - `AllowConstRef`: allows referencing `CONST` variables where otherwise refs reject them.")
    md.append("  - `CharacterData`: requires a character-data variable term (chara var).")
    md.append("  - `Variadic*`: variable-length tail; when `MatchVariadicGroup=true`, the tail repeats in fixed-size groups.")
    md.append("  - `SameAsFirst`: enforces operand-type equality with argument 1 for that position.")
    md.append("  - `DisallowVoid`: forbids omission/`null` for that position even when `OmitStart` would allow it.")
    md.append("")
    md.append(f"Total (method names in `FunctionMethodCreator`): `{len(method_regs)}`.")
    md.append("")
    for reg in method_regs:
        info = method_classes.get(reg.class_name)
        md.append(_render_method_entry(reg, info).rstrip())
        md.append("")

    OUTPUT_ENGINE_MD.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_ENGINE_MD.write_text("\n".join(md).rstrip() + "\n", encoding="utf-8")

    # Progress tracker (manual overrides vs skeleton).
    prog: list[str] = []
    prog.append("# EraBasic Built-ins Writing Progress (Emuera / EvilMask)")
    prog.append("")
    prog.append(f"Generated on `{gen_date}`.")
    prog.append("")
    prog.append("> [!WARNING]")
    prog.append("> This file is generated. Do **not** edit `builtins-progress.md` by hand.")
    prog.append(
        f"> Update `{ref_lint.OVERRIDES_DIR.relative_to(REPO_ROOT)}/**` or the generator/tooling inputs, then regenerate this file."
    )
    prog.append("")
    prog.append("Legend:")
    prog.append("- `⛔` none: no manual override yet")
    prog.append("- `🟡` partial: manual override exists but not declared complete")
    prog.append("- `✅` complete: declared complete (explicit marker in override file)")
    prog.append("")
    prog.append("Notes:")
    prog.append("- To mark an entry complete, add a section `**Progress state**` with `- complete` to the override file.")
    prog.append("")

    instr_none = 0
    instr_partial = 0
    instr_complete = 0
    for r in instr_regs:
        st = ref_lint.override_progress_state(ref_lint.load_override_sections("instruction", r.name))
        if st == "none":
            instr_none += 1
        elif st == "complete":
            instr_complete += 1
        else:
            instr_partial += 1

    meth_none = 0
    meth_partial = 0
    meth_complete = 0
    for r in method_regs:
        st = ref_lint.override_progress_state(ref_lint.load_override_sections("method", r.name))
        if st == "none":
            meth_none += 1
        elif st == "complete":
            meth_complete += 1
        else:
            meth_partial += 1

    prog.append(f"Instructions: `⛔ {instr_none}` / `🟡 {instr_partial}` / `✅ {instr_complete}` (total `{len(instr_regs)}`).")
    prog.append(f"Expression functions: `⛔ {meth_none}` / `🟡 {meth_partial}` / `✅ {meth_complete}` (total `{len(method_regs)}`).")
    prog.append("")

    prog.append("## Instructions")
    prog.append("")
    progress_link_target = Path(os.path.relpath(OUTPUT_MD, OUTPUT_PROGRESS_MD.parent)).as_posix()
    for r in instr_regs:
        override = ref_lint.load_override_sections("instruction", r.name)
        st = ref_lint.override_progress_state(override)
        mark = "⛔" if st == "none" else ("✅" if st == "complete" else "🟡")
        anchor = _md_anchor(f"{r.name} (instruction)")
        prog.append(f"- {mark} [`{r.name}`]({progress_link_target}#{anchor})")
    prog.append("")

    prog.append("## Expression functions")
    prog.append("")
    for r in method_regs:
        override = ref_lint.load_override_sections("method", r.name)
        st = ref_lint.override_progress_state(override)
        mark = "⛔" if st == "none" else ("✅" if st == "complete" else "🟡")
        anchor = _md_anchor(f"{r.name} (expression function)")
        prog.append(f"- {mark} [`{r.name}`]({progress_link_target}#{anchor})")
    prog.append("")

    OUTPUT_PROGRESS_MD.write_text("\n".join(prog).rstrip() + "\n", encoding="utf-8")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
