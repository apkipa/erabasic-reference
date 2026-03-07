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

from dataclasses import dataclass
from pathlib import Path
import argparse
import datetime as _dt
import os
import re
import sys
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[2]

PATH_FUNCTION_IDENTIFIER = REPO_ROOT / "emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs"
PATH_FUNCTION_ARG_TYPE = REPO_ROOT / "emuera.em/Emuera/Runtime/Script/Statements/FunctionArgType.cs"
PATH_ARGUMENT_BUILDER = REPO_ROOT / "emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs"
PATH_SCRIPT_PROC = REPO_ROOT / "emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs"
PATH_METHOD_CREATOR = REPO_ROOT / "emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs"
PATH_METHOD_IMPL = REPO_ROOT / "emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs"

OUTPUT_MD = REPO_ROOT / "erabasic-reference/builtins-reference.md"
OUTPUT_ENGINE_MD = REPO_ROOT / "erabasic-reference/appendix/tooling/builtins-reference-engine.md"
OUTPUT_INDEX_MD = REPO_ROOT / "erabasic-reference/builtins-index.md"
OUTPUT_PROGRESS_MD = REPO_ROOT / "erabasic-reference/builtins-overrides/builtins-progress.md"
OVERRIDES_DIR = REPO_ROOT / "erabasic-reference/builtins-overrides"
INSTRUCTION_OVERRIDES_DIR = OVERRIDES_DIR / "instructions"
METHOD_OVERRIDES_DIR = OVERRIDES_DIR / "methods"

USER_INSTRUCTION_SECTIONS = [
    "Summary",
    "Tags",
    "Syntax",
    "Arguments",
    "Semantics",
    "Errors & validation",
    "Examples",
]

USER_METHOD_SECTIONS = [
    "Summary",
    "Tags",
    "Syntax",
    "Signatures / argument rules",
    "Arguments",
    "Semantics",
    "Errors & validation",
    "Examples",
]

OPTIONAL_USER_SECTIONS = {"Tags"}


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _lines(path: Path) -> list[str]:
    return _read_text(path).splitlines()


def _strip_csharp_comment(s: str) -> str:
    # Keep inline comment as "note"; we don't try to translate it.
    return s.split("//", 1)[0].rstrip()


def _split_flags(expr: str) -> list[str]:
    if not expr:
        return []
    # Normalize: remove parentheses, trailing semicolons, extra spaces.
    expr = expr.replace("(", " ").replace(")", " ")
    expr = expr.replace(";", " ")
    parts: list[str] = []
    for p in expr.split("|"):
        t = p.strip()
        if not t:
            continue
        # Filter obvious non-flags that sometimes appear in arg builder calls.
        parts.append(t)
    return parts


def _format_flags(flags: Iterable[str]) -> str:
    fs = [f for f in flags if f]
    if not fs:
        return "(none)"
    return ", ".join(f"`{f}`" for f in fs)


def _md_anchor(text: str) -> str:
    # GitHub-ish anchors; good enough for internal links in the same doc.
    t = text.strip().lower()
    t = re.sub(r"[^a-z0-9 _-]+", "", t)
    t = t.replace(" ", "-")
    t = re.sub(r"-{2,}", "-", t)
    return t


def _best_effort_translate_argtype_hint(jp: str) -> str:
    """
    Translate the compact FunctionArgType enum comment mini-language into English-ish text.
    This is best-effort and must be treated as a hint, not a complete spec.
    """
    s = jp.strip()
    if not s:
        return ""
    rep = [
        ("引数なし", "no arguments"),
        ("文字列式型", "string expression"),
        ("数式型", "int expression"),
        ("単純文字列型", "raw string"),
        ("単純string型", "raw string"),
        ("変数の型は不問", "variable type unconstrained"),
        ("文字列式", "string expr"),
        ("数式", "int expr"),
        ("数値型変数", "int variable term"),
        ("可変数値変数", "changeable int variable term"),
        ("可変文字列変数", "changeable string variable term"),
        ("可変変数", "changeable variable term"),
        ("変数", "variable term"),
        ("書式付文字列", "FORM string"),
        ("文字列", "string"),
        ("数値", "int"),
        ("キャラクタ変数", "character variable term"),
        ("ソート順序", "sort order"),
        ("範囲初値", "range start"),
        ("範囲終値", "range end"),
        ("省略可能", "optional"),
        ("任意数", "variadic"),
        ("未使用", "unused"),
    ]
    for a, b in rep:
        s = s.replace(a, b)
    s = s.replace("（", "(").replace("）", ")").replace("，", ",").replace("・", " / ")
    s = s.replace("、", ", ")
    return s


def _contains_japanese(s: str) -> bool:
    # Rough detection for Kanji/Hiragana/Katakana.
    return any(
        ("\u3040" <= ch <= "\u30ff")  # hiragana/katakana
        or ("\u4e00" <= ch <= "\u9fff")  # kanji
        for ch in s
    )


@dataclass(frozen=True)
class InstructionReg:
    name: str  # FunctionCode name (keyword)
    kind: str  # "instruction"
    reg_kind: str  # "AInstruction" | "Switch" | "Internal"
    impl_ctor: str | None  # e.g. "new CALL_Instruction(false, true, ...)" when known
    arg_type: str | None  # FunctionArgType
    flags_expr: str | None
    additional_flags_expr: str | None
    notes: list[str]


@dataclass(frozen=True)
class StructuralInfo:
    match_end: str | None
    parent: str | None


@dataclass(frozen=True)
class ArgSpecInfo:
    arg_type: str
    builder_expr: str
    hint_raw: str | None
    hint_en: str | None
    summary_lines: list[str]


@dataclass(frozen=True)
class ImplSnippet:
    where: str  # file path + symbol
    line_no: int | None
    key_ops: list[str]
    throws: list[str]


@dataclass(frozen=True)
class MethodReg:
    name: str
    ctor_expr: str  # e.g. "new FindcharaMethod(true)"
    class_name: str


@dataclass(frozen=True)
class MethodClassInfo:
    class_name: str
    start_line: int | None
    return_type: str | None
    can_restructure: str | None
    arg_rules: list[str]  # human-readable bullet lines
    key_ops: list[str]
    throws: list[str]
    mentions_name_dispatch: bool


def parse_structural_info(function_identifier_lines: list[str]) -> dict[str, StructuralInfo]:
    match: dict[str, str] = {}
    parent: dict[str, str] = {}
    r_match = re.compile(r'funcMatch\[FunctionCode\.(\w+)\]\s*=\s*"(\w+)"\s*;')
    r_parent = re.compile(r"funcParent\[FunctionCode\.(\w+)\]\s*=\s*FunctionCode\.(\w+)\s*;")
    for ln in function_identifier_lines:
        m = r_match.search(ln)
        if m:
            match[m.group(1)] = m.group(2)
        p = r_parent.search(ln)
        if p:
            parent[p.group(1)] = p.group(2)
    out: dict[str, StructuralInfo] = {}
    keys = set(match) | set(parent)
    for k in keys:
        out[k] = StructuralInfo(match_end=match.get(k), parent=parent.get(k))
    return out


def parse_function_argtype_hints(function_arg_type_lines: list[str]) -> dict[str, str]:
    """
    Map FunctionArgType enum member -> inline comment text (raw).

    Example:
      SP_COPY_ARRAY,//<文字列式>,<文字列式>
    """
    out: dict[str, str] = {}
    r = re.compile(r"^\s*(\w+)\s*,\s*//\s*(.+?)\s*$")
    for ln in function_arg_type_lines:
        m = r.match(ln)
        if not m:
            continue
        out[m.group(1)] = m.group(2).strip()
    return out


def parse_instruction_registrations(function_identifier_lines: list[str]) -> list[InstructionReg]:
    regs: list[InstructionReg] = []

    # Track simple config gating blocks we know about.
    gated_stack: list[str] = []
    brace_depth = 0
    gate_start_re = re.compile(r"if\s*\(\s*JSONConfig\.Data\.UseScopedVariableInstruction\s*\)")

    def current_gate_notes() -> list[str]:
        if not gated_stack:
            return []
        return [f"Config-gated: `{gated_stack[-1]}`"]

    # Patterns
    r_add_new = re.compile(
        r"addFunction\(\s*FunctionCode\.(\w+)\s*,\s*new\s+([A-Za-z0-9_]+)\((.*?)\)\s*(?:,\s*([A-Za-z0-9_| ]+))?\s*\)\s*;"
    )
    r_add_argb = re.compile(
        r"addFunction\(\s*FunctionCode\.(\w+)\s*,\s*argb\[FunctionArgType\.(\w+)\]\s*(?:,\s*([A-Za-z0-9_| ]+))?\s*\)\s*;"
    )
    r_add_argb_noflag = re.compile(
        r"addFunction\(\s*FunctionCode\.(\w+)\s*,\s*argb\[FunctionArgType\.(\w+)\]\s*\)\s*;"
    )
    r_add_print = re.compile(r"addPrintFunction\(\s*FunctionCode\.(\w+)\s*\)\s*;")
    r_add_printdata = re.compile(r"addPrintDataFunction\(\s*FunctionCode\.(\w+)\s*\)\s*;")
    r_set_internal = re.compile(r'setFunc\s*=\s*new\s+FunctionIdentifier\("SET"\s*,\s*FunctionCode\.SET\s*,\s*new\s+([A-Za-z0-9_]+)\(\)\s*\)\s*;')

    for raw in function_identifier_lines:
        ln = raw.strip()
        if ln.startswith("//"):
            continue

        # Gate tracking: this file uses braces for the if-block; track very conservatively.
        if gate_start_re.search(ln):
            gated_stack.append("JSONConfig.Data.UseScopedVariableInstruction")
            # braces may start on same or next line; handled by brace_depth below

        # Update brace depth after we process this line's registrations (so the addFunction lines inside gate are tagged).
        internal = r_set_internal.search(ln)
        if internal:
            regs.append(
                InstructionReg(
                    name="SET",
                    kind="instruction",
                    reg_kind="Internal",
                    impl_ctor=f"new {internal.group(1)}()",
                    arg_type=None,
                    flags_expr=None,
                    additional_flags_expr=None,
                    notes=["Internal pseudo-instruction used for assignment parsing (not a normal keyword)."],
                )
            )

        m_print = r_add_print.search(ln)
        if m_print:
            name = m_print.group(1)
            regs.append(
                InstructionReg(
                    name=name,
                    kind="instruction",
                    reg_kind="AInstruction",
                    impl_ctor='new PRINT_Instruction("<keyword>")',
                    arg_type=None,
                    flags_expr=None,
                    additional_flags_expr=None,
                    notes=current_gate_notes(),
                )
            )
        m_pd = r_add_printdata.search(ln)
        if m_pd:
            name = m_pd.group(1)
            regs.append(
                InstructionReg(
                    name=name,
                    kind="instruction",
                    reg_kind="AInstruction",
                    impl_ctor='new PRINT_DATA_Instruction("<keyword>")',
                    arg_type=None,
                    flags_expr=None,
                    additional_flags_expr=None,
                    notes=current_gate_notes(),
                )
            )

        m_new = r_add_new.search(ln)
        if m_new:
            code = m_new.group(1)
            cls = m_new.group(2)
            args = (m_new.group(3) or "").strip()
            ctor = f"new {cls}({args})" if args else f"new {cls}()"
            additional = (m_new.group(4) or "").strip() or None
            regs.append(
                InstructionReg(
                    name=code,
                    kind="instruction",
                    reg_kind="AInstruction",
                    impl_ctor=ctor,
                    arg_type=None,
                    flags_expr=None,
                    additional_flags_expr=additional,
                    notes=current_gate_notes(),
                )
            )

        m_argb = r_add_argb.search(ln)
        if m_argb:
            code = m_argb.group(1)
            argt = m_argb.group(2)
            flags = (m_argb.group(3) or "").strip() or None
            regs.append(
                InstructionReg(
                    name=code,
                    kind="instruction",
                    reg_kind="Switch",
                    impl_ctor=None,
                    arg_type=argt,
                    flags_expr=flags,
                    additional_flags_expr=None,
                    notes=current_gate_notes(),
                )
            )
        else:
            m_argb2 = r_add_argb_noflag.search(ln)
            if m_argb2:
                code = m_argb2.group(1)
                argt = m_argb2.group(2)
                regs.append(
                    InstructionReg(
                        name=code,
                        kind="instruction",
                        reg_kind="Switch",
                        impl_ctor=None,
                        arg_type=argt,
                        flags_expr=None,
                        additional_flags_expr=None,
                        notes=current_gate_notes(),
                    )
                )

        # brace depth update
        brace_depth += ln.count("{")
        brace_depth -= ln.count("}")
        if gated_stack and brace_depth <= 0:
            # End of the gated block (best-effort).
            gated_stack.pop()
            brace_depth = 0

    # De-dup while preserving order (FunctionIdentifier adds methods into same dictionary; we only want instruction registrations here)
    seen: set[str] = set()
    out: list[InstructionReg] = []
    for r in regs:
        if r.name in seen:
            continue
        seen.add(r.name)
        out.append(r)
    return out


def _extract_key_ops(code_lines: list[str], *, max_ops: int = 10) -> tuple[list[str], list[str]]:
    ops: list[str] = []
    throws: list[str] = []
    for raw in code_lines:
        ln = raw.strip()
        if not ln:
            continue
        if ln.startswith("//"):
            continue
        if "throw new" in ln:
            # Keep the exception type and (if obvious) the error id.
            throws.append(ln.rstrip(";"))
            continue
        # Major side-effect calls and IO
        if any(tok in ln for tok in ("exm.", "vEvaluator.", "VariableEvaluator.", "console.", "state.")):
            # Try to compress common patterns.
            ops.append(ln.rstrip(";"))
    # De-noise and cap.
    def _normalize(s: str) -> str:
        s = re.sub(r"\s+", " ", s).strip()
        return s

    ops2: list[str] = []
    seen: set[str] = set()
    for o in ops:
        o2 = _normalize(o)
        if len(o2) < 5:
            continue
        if o2 in seen:
            continue
        seen.add(o2)
        ops2.append(o2)
        if len(ops2) >= max_ops:
            break

    throws2: list[str] = []
    seen_t: set[str] = set()
    for t in throws:
        t2 = _normalize(t)
        if t2 in seen_t:
            continue
        seen_t.add(t2)
        throws2.append(t2)
        if len(throws2) >= max_ops:
            break
    return ops2, throws2


def _scan_csharp_classes(root: Path, *, class_name_suffix: str) -> dict[str, tuple[Path, int, int, list[str]]]:
    """
    Return mapping: class name -> (file, start_line_no(1-based), end_line_no(1-based), lines)
    where lines is the entire class block (including header) for simple parsing.
    """
    out: dict[str, tuple[Path, int, int, list[str]]] = {}
    cs_files = sorted(root.rglob("*.cs"))
    r_class = re.compile(rf"\bclass\s+([A-Za-z0-9_]+{re.escape(class_name_suffix)})\b")
    for p in cs_files:
        text_lines = _lines(p)
        for idx, raw in enumerate(text_lines):
            m = r_class.search(raw)
            if not m:
                continue
            cls = m.group(1)
            # Extract full class block by brace counting from the first '{' after this line.
            start = idx
            # Find first '{'
            j = idx
            brace = 0
            started = False
            while j < len(text_lines):
                line = text_lines[j]
                if "{" in line:
                    brace += line.count("{")
                    started = True
                if "}" in line and started:
                    brace -= line.count("}")
                    if brace <= 0:
                        end = j
                        out[cls] = (p, start + 1, end + 1, text_lines[start : end + 1])
                        break
                j += 1
    return out


def _extract_instruction_class_info(class_block: list[str], class_name: str) -> tuple[list[str], list[str], list[str], list[str]]:
    """
    Best-effort extraction:
      - ArgBuilder assignment
      - flag assignment
      - key ops, throws from DoInstruction body
    """
    arg_builders: list[str] = []
    flag_stmts: list[str] = []
    do_body: list[str] = []
    in_do = False
    brace = 0
    for ln in class_block:
        s = ln.strip()
        if s.startswith("//"):
            continue
        if "ArgBuilder" in s and "=" in s and "ArgumentParser" in s:
            # e.g. ArgBuilder = ArgumentParser.GetArgumentBuilder(FunctionArgType.SP_SWAP);
            arg_builders.append(s.rstrip(";"))
        if s.startswith("flag") and ("=" in s):
            flag_stmts.append(s.rstrip(";"))
        if s.startswith("public override void DoInstruction"):
            in_do = True
            brace = 0
            continue
        if in_do:
            if "{" in ln:
                brace += ln.count("{")
            if "}" in ln:
                brace -= ln.count("}")
                if brace < 0:
                    in_do = False
                    continue
            do_body.append(ln)
    key_ops, throws = _extract_key_ops(do_body)
    # De-dup while preserving order.
    def _dedup(xs: list[str]) -> list[str]:
        seen: set[str] = set()
        out: list[str] = []
        for x in xs:
            x2 = re.sub(r"\s+", " ", x).strip()
            if x2 in seen:
                continue
            seen.add(x2)
            out.append(x2)
        return out

    return _dedup(arg_builders), _dedup(flag_stmts), key_ops, throws


def _infer_arg_types_from_argbuilder_lines(argb_lines: list[str]) -> list[str]:
    """
    Extract referenced FunctionArgType values from ArgBuilder assignment statements.

    Note: many instruction classes assign ArgBuilder conditionally based on constructor args
    (e.g. the PRINT family). In those cases this returns multiple candidates and callers
    should avoid claiming a single Arg spec.
    """
    out: list[str] = []
    seen: set[str] = set()
    for ln in argb_lines:
        for m in re.finditer(r"\bFunctionArgType\.(\w+)\b", ln):
            t = m.group(1)
            if t in seen:
                continue
            seen.add(t)
            out.append(t)
    return out


def parse_switch_cases(script_proc_lines: list[str]) -> dict[str, ImplSnippet]:
    """
    Extract per-FunctionCode snippets from:
      - doNormalFunction switch
      - doFlowControlFunction switch
    """
    text = "\n".join(script_proc_lines)

    def _extract_switch(method_name: str) -> dict[str, list[str]]:
        # Find method
        m = re.search(rf"\b(?:void|bool)\s+{re.escape(method_name)}\s*\(.*?\)\s*\{{", text, flags=re.S)
        if not m:
            return {}
        start = m.start()
        # Find matching method end by braces.
        i = m.end() - 1
        brace = 0
        while i < len(text) and text[i] != "{":
            i += 1
        if i >= len(text):
            return {}
        brace = 1
        j = i + 1
        while j < len(text) and brace > 0:
            if text[j] == "{":
                brace += 1
            elif text[j] == "}":
                brace -= 1
            j += 1
        method_body = text[i + 1 : j - 1]

        # Find the switch body similarly.
        sm = re.search(r"switch\s*\(\s*func\.FunctionCode\s*\)\s*\{", method_body)
        if not sm:
            return {}
        k = sm.end() - 1
        brace = 1
        l = k + 1
        while l < len(method_body) and brace > 0:
            ch = method_body[l]
            if ch == "{":
                brace += 1
            elif ch == "}":
                brace -= 1
            l += 1
        switch_body = method_body[k + 1 : l - 1]

        # Parse cases by scanning lines and tracking brace nesting within the case.
        out_cases: dict[str, list[str]] = {}
        lines = switch_body.splitlines()
        current_labels: list[str] = []
        in_label_sequence = False
        buf: list[str] = []
        depth = 0
        r_case = re.compile(r"^\s*case\s+FunctionCode\.(\w+)\s*:")
        r_default = re.compile(r"^\s*default\s*:")

        def _flush() -> None:
            nonlocal current_labels, buf, in_label_sequence
            if not current_labels:
                buf = []
                in_label_sequence = False
                return
            for lab in current_labels:
                out_cases[lab] = buf[:]
            current_labels = []
            buf = []
            in_label_sequence = False

        for raw in lines:
            mc = r_case.match(raw)
            if mc and depth == 0:
                name = mc.group(1)
                if not current_labels:
                    current_labels = [name]
                    buf = [raw]
                    in_label_sequence = True
                elif in_label_sequence:
                    # Grouped case labels (fallthrough) for the same body.
                    current_labels.append(name)
                    buf.append(raw)
                else:
                    _flush()
                    current_labels = [name]
                    buf = [raw]
                    in_label_sequence = True
                continue
            if r_default.match(raw) and depth == 0:
                _flush()
                continue
            if current_labels:
                # First non-label line ends the case-label run.
                if in_label_sequence and raw.strip() != "":
                    in_label_sequence = False
                buf.append(raw)
                depth += raw.count("{")
                depth -= raw.count("}")
                if depth < 0:
                    depth = 0
        _flush()
        return out_cases

    cases_normal = _extract_switch("doNormalFunction")
    cases_flow = _extract_switch("doFlowControlFunction")

    out: dict[str, ImplSnippet] = {}
    for name, body in cases_normal.items():
        ops, thr = _extract_key_ops(body)
        out[name] = ImplSnippet(
            where=f"`{PATH_SCRIPT_PROC.relative_to(REPO_ROOT)}` (`doNormalFunction` case `{name}`)",
            line_no=None,
            key_ops=ops,
            throws=thr,
        )
    for name, body in cases_flow.items():
        ops, thr = _extract_key_ops(body)
        out[name] = ImplSnippet(
            where=f"`{PATH_SCRIPT_PROC.relative_to(REPO_ROOT)}` (`doFlowControlFunction` case `{name}`)",
            line_no=None,
            key_ops=ops,
            throws=thr,
        )
    return out


def parse_argument_specs(arg_builder_lines: list[str], argtype_hints: dict[str, str]) -> dict[str, ArgSpecInfo]:
    """
    Extract FunctionArgType -> builder mapping from ArgumentParser.Initialize().
    Also tries to describe each arg type based on the builder's constructor fields.
    """
    # Map arg type to builder expression.
    mapping: dict[str, str] = {}
    r_map = re.compile(r"argb\[FunctionArgType\.(\w+)\]\s*=\s*new\s+([A-Za-z0-9_]+)\((.*?)\)\s*;")
    for ln in arg_builder_lines:
        m = r_map.search(ln)
        if not m:
            continue
        argt = m.group(1)
        builder = m.group(2)
        args = m.group(3).strip()
        expr = f"{builder}({args})" if args else f"{builder}()"
        mapping[argt] = expr

    # Find builder class blocks inside the same file for lightweight metadata.
    builder_classes = _scan_csharp_classes(PATH_ARGUMENT_BUILDER.parent, class_name_suffix="_ArgumentBuilder")
    # SP_COPY_ARRAY_Arguments / other non-suffix builders exist; include them too.
    r_any_builder_class = re.compile(r"\bclass\s+([A-Za-z0-9_]+)\b")

    def _builder_summary(expr: str) -> list[str]:
        # Try to use constructor extraction if class is known.
        cls = expr.split("(", 1)[0]
        block = builder_classes.get(cls)
        if not block:
            return ["Custom parser (builder class not indexed by this generator)."]
        _file, _start, _end, lines = block
        # Parse simple fields from the constructor.
        arg_types = None
        min_arg = None
        arg_any = None
        for raw in lines:
            s = raw.strip()
            if s.startswith("argumentTypeArray") and "=" in s:
                arg_types = s.split("=", 1)[1].strip().rstrip(";")
            if s.startswith("minArg") and "=" in s:
                min_arg = s.split("=", 1)[1].strip().rstrip(";")
            if s.startswith("argAny") and "=" in s:
                arg_any = s.split("=", 1)[1].strip().rstrip(";")
        out_lines: list[str] = []
        if arg_types:
            out_lines.append(f"Type pattern: `{arg_types}` (`typeof(long)` = int expr, `typeof(string)` = string expr, `typeof(void)` = special/variable term depending on builder).")
        if min_arg is not None:
            out_lines.append(f"Minimum args: `{min_arg}`.")
        if arg_any is not None:
            out_lines.append(f"Variadic (`argAny`): `{arg_any}`.")
        return out_lines

    out: dict[str, ArgSpecInfo] = {}
    for argt, expr in sorted(mapping.items()):
        hint_raw = argtype_hints.get(argt)
        hint_en = _best_effort_translate_argtype_hint(hint_raw) if hint_raw else None
        out[argt] = ArgSpecInfo(
            arg_type=argt,
            builder_expr=expr,
            hint_raw=hint_raw,
            hint_en=hint_en if hint_en else None,
            summary_lines=_builder_summary(expr),
        )
    return out


def parse_method_registrations(creator_lines: list[str]) -> list[MethodReg]:
    # Ignore full-line comments so we don't document commented-out method entries.
    text = "\n".join(ln for ln in creator_lines if not ln.strip().startswith("//"))
    regs: list[MethodReg] = []
    # Scan dictionary initializer entries: ["NAME"] = new Class(args),
    i = 0
    while True:
        m = re.search(r'\["([^"]+)"\]\s*=\s*new\s+([A-Za-z0-9_]+)\s*\(', text[i:])
        if not m:
            break
        name = m.group(1)
        cls = m.group(2)
        start = i + m.end() - 1  # position at '('
        # Find matching ')'
        depth = 0
        j = start
        while j < len(text):
            ch = text[j]
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        args = text[start + 1 : j].strip()
        ctor_expr = f"new {cls}({args})" if args else f"new {cls}()"
        regs.append(MethodReg(name=name, ctor_expr=ctor_expr, class_name=cls))
        i = j + 1

    # De-dup: same name can appear only once, but be safe.
    seen: set[str] = set()
    out: list[MethodReg] = []
    for r in regs:
        if r.name in seen:
            continue
        seen.add(r.name)
        out.append(r)
    return out


def parse_method_classes(method_impl_lines: list[str]) -> dict[str, MethodClassInfo]:
    # Extract class blocks for *all* FunctionMethod subclasses in this file.
    text = "\n".join(method_impl_lines)
    out: dict[str, MethodClassInfo] = {}
    r_cls = re.compile(r"\bclass\s+([A-Za-z0-9_]+)\s*:\s*FunctionMethod\b")
    for m in r_cls.finditer(text):
        cls = m.group(1)
        # Find opening brace for class
        start = text.rfind("\n", 0, m.start()) + 1
        brace_pos = text.find("{", m.end())
        if brace_pos == -1:
            continue
        depth = 1
        j = brace_pos + 1
        while j < len(text) and depth > 0:
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
            j += 1
        block = text[start:j]
        block_lines = block.splitlines()

        # Best-effort: grab first constructor assignments (many classes have a single constructor).
        return_type = None
        can_restructure = None
        mentions_name = False
        arg_type_array_literals: list[str] = []
        arg_type_list_specs: list[str] = []

        def _dedup_keep_order(xs: list[str]) -> list[str]:
            seen: set[str] = set()
            out2: list[str] = []
            for x in xs:
                x2 = re.sub(r"\s+", " ", x).strip()
                if not x2 or x2 in seen:
                    continue
                seen.add(x2)
                out2.append(x2)
            return out2

        # Capture ArgTypeList initializers (argumentTypeArrayEx).
        i = 0
        while i < len(block_lines):
            raw = block_lines[i]
            s = raw.strip()

            if "ReturnType" in s and "typeof(" in s:
                mm = re.search(r"ReturnType\s*=\s*typeof\((\w+)\)", s)
                if mm and return_type is None:
                    return_type = mm.group(1)
            if s.startswith("CanRestructure") and "=" in s:
                can_restructure = s.split("=", 1)[1].strip().rstrip(";")

            # Simple argumentTypeArray literal: `argumentTypeArray = [typeof(string), typeof(long)];`
            if "argumentTypeArray" in s and "=" in s and "[" in s and "]" in s:
                mm = re.search(r"\bargumentTypeArray\s*=\s*(\[[^\]]*\])", s)
                if mm:
                    arg_type_array_literals.append(mm.group(1))

            # ArgTypeList initializer, often inside an `argumentTypeArrayEx = [ ... ];` block.
            if "new ArgTypeList" in s and "{" in s:
                brace = 0
                started = False
                j = i
                chunks: list[str] = []
                while j < len(block_lines):
                    ln = block_lines[j]
                    if "new ArgTypeList" in ln and not started:
                        started = True
                    if started:
                        chunks.append(ln.strip())
                        brace += ln.count("{")
                        brace -= ln.count("}")
                        if brace <= 0 and "}" in ln:
                            break
                    j += 1
                snippet = " ".join(chunks)
                snippet = re.sub(r"\s+", " ", snippet).strip().rstrip(",")
                if snippet:
                    # Pull out ArgTypes, OmitStart, MatchVariadicGroup when present.
                    argtypes = None
                    mm_types = re.search(r"ArgTypes\s*=\s*\{\s*(.*?)\s*\}", snippet)
                    if mm_types:
                        argtypes = mm_types.group(1).strip()
                    omit = None
                    mm_omit = re.search(r"OmitStart\s*=\s*(\d+)", snippet)
                    if mm_omit:
                        omit = mm_omit.group(1)
                    mvg = None
                    mm_mvg = re.search(r"MatchVariadicGroup\s*=\s*(true|false)", snippet, flags=re.I)
                    if mm_mvg:
                        mvg = mm_mvg.group(1).lower()

                    line = "ArgTypeList"
                    if argtypes:
                        line += f": ArgTypes = {{ {argtypes} }}"
                    if omit is not None:
                        line += f"; OmitStart = {omit}"
                    if mvg is not None:
                        line += f"; MatchVariadicGroup = {mvg}"
                    arg_type_list_specs.append(line)
                i = max(i + 1, j + 1)
                continue

            if "Name" in s and ("Name." in s or "Name " in s or "Name)" in s):
                mentions_name = True

            i += 1

        arg_type_array_literals = _dedup_keep_order(arg_type_array_literals)
        arg_type_list_specs = _dedup_keep_order(arg_type_list_specs)

        arg_rules: list[str] = []
        if arg_type_array_literals:
            if len(arg_type_array_literals) == 1:
                arg_rules.append(f"Argument rules: `argumentTypeArray = {arg_type_array_literals[0]}`.")
            else:
                arg_rules.append("Argument rules: multiple `argumentTypeArray` assignments detected (name/branch dependent).")
                for lit in arg_type_array_literals[:6]:
                    arg_rules.append(f"`argumentTypeArray = {lit}`.")
        if arg_type_list_specs:
            arg_rules.append("Argument rules: `argumentTypeArrayEx` (ArgTypeList-based; supports refs/arrays/variadics/omission).")
            for spec_line in arg_type_list_specs[:10]:
                arg_rules.append(spec_line + ".")

        # Key ops from GetIntValue/GetStrValue bodies (best-effort)
        key_ops, throws = _extract_key_ops(block_lines, max_ops=12)

        out[cls] = MethodClassInfo(
            class_name=cls,
            start_line=None,
            return_type=return_type,
            can_restructure=can_restructure,
            arg_rules=arg_rules[:14] if arg_rules else ["Argument rules: custom check (no `argumentTypeArray`/`argumentTypeArrayEx` assignment detected)."],
            key_ops=key_ops,
            throws=throws,
            mentions_name_dispatch=mentions_name,
        )
    return out


def index_line_numbers_for_cases(script_proc_lines: list[str]) -> dict[str, int]:
    out: dict[str, int] = {}
    r = re.compile(r"\bcase\s+FunctionCode\.(\w+)\s*:")
    for i, ln in enumerate(script_proc_lines, start=1):
        m = r.search(ln)
        if m:
            out.setdefault(m.group(1), i)
    return out


def index_line_numbers_for_method_classes(method_impl_lines: list[str]) -> dict[str, int]:
    out: dict[str, int] = {}
    r = re.compile(r"\bclass\s+([A-Za-z0-9_]+)\s*:\s*FunctionMethod\b")
    for i, ln in enumerate(method_impl_lines, start=1):
        m = r.search(ln)
        if m:
            out.setdefault(m.group(1), i)
    return out


def _render_section(title: str, body_lines: list[str]) -> list[str]:
    out: list[str] = [f"**{title}**"]
    if not body_lines:
        out.append("- (TODO)")
        return out
    out.extend(body_lines)
    return out


def _parse_override_sections(md_text: str) -> dict[str, list[str]]:
    """
    Parse a simple override snippet file into sections.

    The file is expected to contain one or more sections formatted as:
      **Section Title**
      - bullets...

    Blank lines are preserved inside a section (trimmed at head/tail).
    """
    out: dict[str, list[str]] = {}
    current_title: str | None = None
    current_lines: list[str] = []
    r = re.compile(r"^\*\*(.+?)\*\*\s*$")

    def _flush() -> None:
        nonlocal current_title, current_lines
        if current_title is None:
            current_lines = []
            return
        # Trim leading/trailing blank lines, preserve internal blanks.
        while current_lines and current_lines[0].strip() == "":
            current_lines.pop(0)
        while current_lines and current_lines[-1].strip() == "":
            current_lines.pop()
        out[current_title] = list(current_lines)
        current_lines = []

    for raw in md_text.splitlines():
        m = r.match(raw)
        if m:
            _flush()
            current_title = m.group(1).strip()
            continue
        if current_title is None:
            continue
        current_lines.append(raw.rstrip())
    _flush()
    return out


def _load_override_sections(kind: str, name: str) -> dict[str, list[str]]:
    """
    Load override sections for an entry.

    kind:
      - "instruction"
      - "method"

    Source of truth:
      - Markdown override files in `erabasic-reference/builtins-overrides/`
    """
    if kind == "instruction":
        p = INSTRUCTION_OVERRIDES_DIR / f"{name}.md"
        if p.exists():
            return _parse_override_sections(_read_text(p))
        return {}
    if kind == "method":
        p = METHOD_OVERRIDES_DIR / f"{name}.md"
        if p.exists():
            return _parse_override_sections(_read_text(p))
        return {}
    return {}


def _has_manual_override(kind: str, name: str) -> bool:
    secs = _load_override_sections(kind, name)
    return bool(secs)


def _has_user_facing_content(kind: str, name: str) -> bool:
    """
    Return True if an override contributes any user-facing content lines.

    Overrides may contain internal tooling-only sections (e.g. Progress state)
    without documenting the built-in for readers.
    """
    secs = _load_override_sections(kind, name)
    if not secs:
        return False
    titles = USER_INSTRUCTION_SECTIONS if kind == "instruction" else USER_METHOD_SECTIONS
    for t in titles:
        if t in OPTIONAL_USER_SECTIONS:
            continue
        body = secs.get(t, [])
        if any(ln.strip() for ln in body):
            return True
    return False


def _render_instruction_entry_user(reg: InstructionReg) -> str:
    parts: list[str] = [f"## {reg.name} (instruction)"]
    override = _load_override_sections("instruction", reg.name)
    if not _has_user_facing_content("instruction", reg.name):
        parts.append("**Summary**")
        parts.append("- (TODO: not yet documented)")
        return "\n".join(parts) + "\n"
    for title in USER_INSTRUCTION_SECTIONS:
        if title == "Tags" and not any(ln.strip() for ln in override.get("Tags", [])):
            continue
        parts.append("")
        parts.extend(_render_section(title, override.get(title, [])))
    return "\n".join(parts) + "\n"


def _render_method_entry_user(reg: MethodReg) -> str:
    parts: list[str] = [f"## {reg.name} (expression function)"]
    override = _load_override_sections("method", reg.name)
    if not _has_user_facing_content("method", reg.name):
        parts.append("**Summary**")
        parts.append("- (TODO: not yet documented)")
        return "\n".join(parts) + "\n"
    for title in USER_METHOD_SECTIONS:
        if title == "Tags" and not any(ln.strip() for ln in override.get("Tags", [])):
            continue
        parts.append("")
        parts.extend(_render_section(title, override.get(title, [])))
    return "\n".join(parts) + "\n"


@dataclass(frozen=True)
class ValidationIssue:
    severity: str  # "WARN" | "ERROR"
    code: str
    kind: str  # "instruction" | "method" | "doc"
    name: str
    message: str


def _progress_state_raw(secs: dict[str, list[str]]) -> list[str]:
    return secs.get("Progress state", []) or secs.get("Progress", []) or []


def _progress_state_value(secs: dict[str, list[str]]) -> str | None:
    raw = _progress_state_raw(secs)
    if not raw:
        return None
    for ln in raw:
        t = ln.strip().lstrip("-").strip().lower()
        if not t:
            continue
        if t in ("complete", "completed", "done"):
            return "complete"
        if t in ("partial", "incomplete", "wip", "draft"):
            return "partial"
    return "invalid"


@dataclass(frozen=True)
class ArgumentDocSpec:
    name: str
    optional: bool
    has_default: bool
    raw: str


_OVERRIDE_SECTION_RE = re.compile(r"^\*\*(.+?)\*\*\s*$")
_TODO_MARKER_RE = re.compile(r"\b(?:TODO|TBD)\b|\?\?\?|not yet documented", re.IGNORECASE)
_SOURCE_PATH_RE = re.compile(r"(?:emuera\.em/[^`\s)]+|[A-Za-z0-9_./-]+\.cs(?::\d+)?(?![A-Za-z0-9_]))")
_RANGE_SHORTHAND_RE = re.compile(r"(?<!\.)\b[A-Za-z_][A-Za-z0-9_]*\.\.[A-Za-z_][A-Za-z0-9_]*\b(?!\.)")
_SEE_ABOVE_BELOW_RE = re.compile(r"\b(?:above|below|earlier|later|前文|后文|上文|下文)\b", re.IGNORECASE)
_MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+\.md(?:#[^)]+)?)\)")
_BACKTICK_MD_REF_RE = re.compile(r"`([A-Za-z0-9_./-]+\.md(?:#[A-Za-z0-9_-]+)?)`")
_INTERNAL_SYMBOL_RES = [
    re.compile(r"\b[A-Za-z0-9_]+_(?:Instruction|ArgumentBuilder)\b"),
    re.compile(r"\b(?:ArgumentParser|ExpressionParser|LexicalAnalyzer|ExpressionMediator|ProcessState|AExpression|VariableTerm|GlobalStatic|FunctionArgType|Sp[A-Za-z0-9_]+Argument|GetStrValue|GetIntValue|ReduceExpressionTerm)\b"),
    re.compile(r"\bexm\.[A-Za-z_][A-Za-z0-9_]*\b"),
]
_VAGUE_PHRASE_RES = [
    re.compile(r"\betc\.\b", re.IGNORECASE),
    re.compile(r"\band so on\b", re.IGNORECASE),
    re.compile(r"\bin some cases\b", re.IGNORECASE),
    re.compile(r"\bsome cases\b", re.IGNORECASE),
    re.compile(r"\bbasically\b", re.IGNORECASE),
    re.compile(r"\broughly\b", re.IGNORECASE),
]


def _ordered_unique(items: Iterable[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def _canonical_arg_name(name: str) -> str:
    if "|" in name:
        return name
    name = re.sub(r"\.\.\.$", "", name)
    name = re.sub(r"\*$", "", name)
    name = re.sub(r"\d+$", "", name)
    if len(name) >= 2 and name.endswith("N") and name[-2].islower():
        name = name[:-1]
    return name


def _scan_override_section_structure(path: Path) -> tuple[list[str], list[tuple[str, int, int]], list[tuple[int, str]]]:
    titles: list[str] = []
    duplicates: list[tuple[str, int, int]] = []
    stray: list[tuple[int, str]] = []
    seen_lines: dict[str, int] = {}
    current_title: str | None = None
    for line_no, raw in enumerate(_lines(path), start=1):
        m = _OVERRIDE_SECTION_RE.match(raw)
        if m:
            title = m.group(1).strip()
            titles.append(title)
            if title in seen_lines:
                duplicates.append((title, seen_lines[title], line_no))
            else:
                seen_lines[title] = line_no
            current_title = title
            continue
        if current_title is None and raw.strip():
            stray.append((line_no, raw.strip()))
    return titles, duplicates, stray


def _extract_code_spans(line: str) -> list[str]:
    return re.findall(r"`([^`]+)`", line)


def _scan_token_stream(text: str) -> list[tuple[str, bool]]:
    out: list[tuple[str, bool]] = []
    seen: set[tuple[str, bool]] = set()
    skip_words = {"int", "long", "string", "bool", "void"}
    i = 0
    depth = 0
    while i < len(text):
        ch = text[i]
        if ch == "[":
            depth += 1
            i += 1
            continue
        if ch == "]":
            depth = max(0, depth - 1)
            i += 1
            continue
        if ch == "<":
            j = text.find(">", i + 1)
            if j == -1:
                break
            name = text[i + 1 : j].strip()
            if name and " " not in name:
                name = _canonical_arg_name(name)
                pair = (name, depth > 0)
                if pair not in seen:
                    seen.add(pair)
                    out.append(pair)
            i = j + 1
            continue
        if ch.isalpha() or ch == "_":
            j = i + 1
            while j < len(text) and (text[j].isalnum() or text[j] == "_"):
                j += 1
            token = text[i:j]
            k = j
            while k < len(text) and text[k].isspace():
                k += 1
            if text[k : k + 3] == "...":
                token += "..."
                k += 3
            while True:
                k2 = k
                while k2 < len(text) and text[k2].isspace():
                    k2 += 1
                if k2 >= len(text) or text[k2] != "|":
                    break
                k2 += 1
                while k2 < len(text) and text[k2].isspace():
                    k2 += 1
                j2 = k2
                if j2 >= len(text) or not (text[j2].isalpha() or text[j2] == "_"):
                    break
                j2 += 1
                while j2 < len(text) and (text[j2].isalnum() or text[j2] == "_"):
                    j2 += 1
                token += "|" + text[k2:j2]
                k = j2
            if token.lower() not in skip_words:
                token = _canonical_arg_name(token)
                pair = (token, depth > 0)
                if pair not in seen:
                    seen.add(pair)
                    out.append(pair)
            i = max(k, j)
            continue
        i += 1
    return out


def _scan_syntax_tokens_from_fragment(fragment: str) -> list[tuple[str, bool]]:
    text = fragment.strip()
    if text.startswith("<"):
        return _scan_token_stream(text)
    first_paren = text.find("(")
    first_space = text.find(" ")
    if first_paren != -1 and (first_space == -1 or first_paren < first_space):
        text = text[first_paren + 1 : text.rfind(")")]
    else:
        if first_space == -1:
            return []
        text = text[first_space + 1 :]
    return _scan_token_stream(text)


def _scan_argument_names_from_fragment(fragment: str) -> list[str]:
    return [name for name, _ in _scan_token_stream(fragment.strip())]


def _collect_syntax_contract(secs: dict[str, list[str]]) -> tuple[list[str], dict[str, bool]]:
    forms: list[list[tuple[str, bool]]] = []
    for raw in secs.get("Syntax", []):
        code_spans = _extract_code_spans(raw)
        if not code_spans:
            continue
        form_tokens: list[tuple[str, bool]] = []
        for frag in code_spans:
            form_tokens.extend(_scan_syntax_tokens_from_fragment(frag))
        forms.append(form_tokens)
    if not forms:
        return [], {}

    order: list[str] = []
    all_names: list[str] = []
    per_form: list[dict[str, list[bool]]] = []
    for form in forms:
        per_name: dict[str, list[bool]] = {}
        for name, is_optional in form:
            if name not in order:
                order.append(name)
            per_name.setdefault(name, []).append(is_optional)
            if name not in all_names:
                all_names.append(name)
        per_form.append(per_name)

    can_omit: dict[str, bool] = {}
    for name in all_names:
        form_can_omit = False
        for per_name in per_form:
            optionalities = per_name.get(name)
            if not optionalities:
                form_can_omit = True
                break
            if all(optionalities):
                form_can_omit = True
                break
        can_omit[name] = form_can_omit
    return order, can_omit


def _parse_argument_bullets(secs: dict[str, list[str]]) -> tuple[list[str], dict[str, ArgumentDocSpec]]:
    order: list[str] = []
    meta: dict[str, ArgumentDocSpec] = {}
    for raw in secs.get("Arguments", []):
        if not raw.startswith("- "):
            continue
        stripped = raw.strip()
        if re.match(r"^-\s+Same as\b", stripped):
            continue
        if not re.match(r"^-\s+(?:`|Each\s+`|One or more\b|Zero or more\b|None\.)", stripped):
            continue
        m = re.match(r"^-\s+(.*?)(?:\s+\(|:|\s+is\b|\s+are\b)", stripped)
        prefix = m.group(1) if m else stripped[2:]
        names: list[str] = []
        for name in _scan_argument_names_from_fragment(prefix):
            if name not in names:
                names.append(name)
        for frag in _extract_code_spans(prefix):
            for name in _scan_argument_names_from_fragment(frag):
                if name not in names:
                    names.append(name)
        if not names:
            continue
        is_optional = bool(re.search(r"\([^)]*\boptional\b", stripped, re.IGNORECASE))
        has_default = bool(re.search(r"\([^)]*\bdefault\b", stripped, re.IGNORECASE))
        for name in names:
            if name not in order:
                order.append(name)
            meta.setdefault(name, ArgumentDocSpec(name=name, optional=is_optional, has_default=has_default, raw=stripped))
    return order, meta


def _line_pattern_issues(*, path: Path, kind: str, name: str, lines: list[str], source_path_code: str, internal_symbol_code: str, japanese_code: str, vague_code: str) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    rel = path.relative_to(REPO_ROOT)
    for line_no, raw in enumerate(lines, start=1):
        if r'\"' in raw:
            issues.append(ValidationIssue(severity="WARN", code="suspicious-escaped-quote", kind=kind, name=name, message=f"{rel}:{line_no}: contains a backslash-escaped quote (`\\\"`); avoid escaping quotes in Markdown examples/code unless the backslash is literal."))
        if "default =" in raw:
            issues.append(ValidationIssue(severity="WARN", code="noncanonical-default-syntax", kind=kind, name=name, message=f"{rel}:{line_no}: uses `default =`; prefer a canonical form such as `default `0`` or `default current array length`."))
        if re.search(r"\(required\s+[^)]+\)", raw):
            issues.append(ValidationIssue(severity="WARN", code="noncanonical-required-marker", kind=kind, name=name, message=f"{rel}:{line_no}: uses a `(required ...)` marker; rely on the global default-required rule unless special disambiguation is needed."))
        if "with a warning if omitted" in raw:
            issues.append(ValidationIssue(severity="WARN", code="noncanonical-omission-warning-phrase", kind=kind, name=name, message=f"{rel}:{line_no}: uses legacy wording `with a warning if omitted`; prefer `default X; omission emits a warning`."))
        if _SOURCE_PATH_RE.search(raw):
            issues.append(ValidationIssue(severity="ERROR", code=source_path_code, kind=kind, name=name, message=f"{rel}:{line_no}: leaks a source path or `.cs` reference into user-facing prose."))
        if any(p.search(raw) for p in _INTERNAL_SYMBOL_RES):
            issues.append(ValidationIssue(severity="WARN", code=internal_symbol_code, kind=kind, name=name, message=f"{rel}:{line_no}: mentions engine-internal symbol names; prefer external/observable contract wording."))
        if _contains_japanese(raw):
            issues.append(ValidationIssue(severity="WARN", code=japanese_code, kind=kind, name=name, message=f"{rel}:{line_no}: contains Japanese text in user-facing documentation."))
        if any(p.search(raw) for p in _VAGUE_PHRASE_RES):
            issues.append(ValidationIssue(severity="WARN", code=vague_code, kind=kind, name=name, message=f"{rel}:{line_no}: contains vague wording that may weaken reimplementation-grade precision."))
        if _RANGE_SHORTHAND_RE.search(raw):
            issues.append(ValidationIssue(severity="WARN", code="range-shorthand", kind=kind, name=name, message=f"{rel}:{line_no}: uses `a..b`-style shorthand; prefer explicit inequalities or half-open interval notation."))
    return issues


def _lint_override_structure(*, path: Path, kind: str, name: str, secs: dict[str, list[str]]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    rel = path.relative_to(REPO_ROOT)
    titles, duplicates, stray = _scan_override_section_structure(path)
    for title, first_line, dup_line in duplicates:
        issues.append(ValidationIssue(severity="ERROR", code="duplicate-section", kind=kind, name=name, message=f"{rel}:{dup_line}: duplicate section `**{title}**` (first defined at line {first_line})."))
    for line_no, content in stray:
        issues.append(ValidationIssue(severity="ERROR", code="stray-content-outside-sections", kind=kind, name=name, message=f"{rel}:{line_no}: content appears before the first section header: `{content}`"))

    canonical = USER_INSTRUCTION_SECTIONS if kind == "instruction" else USER_METHOD_SECTIONS
    seen_user = [title for title in titles if title in canonical]
    indices = [canonical.index(title) for title in seen_user]
    if indices != sorted(indices):
        issues.append(ValidationIssue(severity="WARN", code="noncanonical-section-order", kind=kind, name=name, message=f"{rel}: section order is noncanonical ({', '.join(f'`{t}`' for t in seen_user)})."))

    if _progress_state_value(secs) == "complete":
        for body in secs.values():
            for raw in body:
                if _TODO_MARKER_RE.search(raw):
                    issues.append(ValidationIssue(severity="ERROR", code="complete-entry-has-todo-marker", kind=kind, name=name, message=f"{rel}: marked complete but still contains TODO/TBD/placeholder text."))
                    return issues
    return issues


def _lint_override_argument_contracts(*, path: Path, kind: str, name: str, secs: dict[str, list[str]]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    rel = path.relative_to(REPO_ROOT)
    syntax_order, syntax_optional = _collect_syntax_contract(secs)
    arg_order, arg_meta = _parse_argument_bullets(secs)
    arg_lines = secs.get("Arguments", [])
    if any(re.match(r"^\s*-\s+(?:Same as|One or more|Zero or more|Each|None\.)", raw) for raw in arg_lines):
        for spec in arg_meta.values():
            if spec.has_default and not spec.optional:
                issues.append(ValidationIssue(severity="ERROR", code="default-without-optional", kind=kind, name=name, message=f"{rel}: argument `{spec.name}` documents a default but is not marked `optional`."))
        return issues

    for spec in arg_meta.values():
        if spec.has_default and not spec.optional:
            issues.append(ValidationIssue(severity="ERROR", code="default-without-optional", kind=kind, name=name, message=f"{rel}: argument `{spec.name}` documents a default but is not marked `optional`."))

    if not syntax_order or not arg_meta:
        return issues

    missing = [arg_name for arg_name in syntax_order if arg_name not in arg_meta]
    if missing:
        issues.append(ValidationIssue(severity="ERROR", code="missing-argument-doc-for-syntax-placeholder", kind=kind, name=name, message=f"{rel}: syntax placeholders/tokens missing from `Arguments`: {', '.join(f'`{n}`' for n in missing)}."))

    orphan = [arg_name for arg_name in arg_order if arg_name not in syntax_optional]
    if orphan:
        issues.append(ValidationIssue(severity="WARN", code="orphan-argument-bullet", kind=kind, name=name, message=f"{rel}: `Arguments` documents names not present in `Syntax`: {', '.join(f'`{n}`' for n in orphan)}."))

    expected_common = [n for n in syntax_order if n in arg_meta]
    actual_common = [n for n in arg_order if n in syntax_optional]
    if expected_common and actual_common and expected_common != actual_common:
        issues.append(ValidationIssue(severity="WARN", code="argument-order-mismatch", kind=kind, name=name, message=f"{rel}: `Arguments` order does not match `Syntax` order."))

    for arg_name in [n for n in syntax_order if n in arg_meta]:
        syntax_is_optional = syntax_optional[arg_name]
        doc_is_optional = arg_meta[arg_name].optional
        if syntax_is_optional != doc_is_optional:
            issues.append(ValidationIssue(severity="ERROR", code="syntax-optional-mismatch", kind=kind, name=name, message=f"{rel}: `{arg_name}` optionality differs between `Syntax` and `Arguments`."))
    return issues


def validate_builtins_overrides(instr_regs: list[InstructionReg], method_regs: list[MethodReg]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    engine_instr = {r.name for r in instr_regs}
    engine_meth = {r.name for r in method_regs}
    is_input_instr: dict[str, bool] = {}
    for r in instr_regs:
        flags = (r.flags_expr or "") + " " + (r.additional_flags_expr or "")
        is_input_instr[r.name] = "IS_INPUT" in flags

    allowed_instruction = set(USER_INSTRUCTION_SECTIONS) | {"Progress state", "Progress"}
    allowed_method = set(USER_METHOD_SECTIONS) | {"Progress state", "Progress"}

    def check_override_file(kind: str, name: str, path: Path, secs: dict[str, list[str]]) -> None:
        issues.extend(_line_pattern_issues(path=path, kind=kind, name=name, lines=_lines(path), source_path_code="user-doc-source-path-leak", internal_symbol_code="user-doc-internal-symbol-leak", japanese_code="user-doc-japanese-text", vague_code="banned-vague-phrase"))
        issues.extend(_lint_override_structure(path=path, kind=kind, name=name, secs=secs))
        issues.extend(_lint_override_argument_contracts(path=path, kind=kind, name=name, secs=secs))

        allowed = allowed_instruction if kind == "instruction" else allowed_method
        unknown = sorted([k for k in secs.keys() if k not in allowed])
        for section_title in unknown:
            issues.append(ValidationIssue(severity="WARN", code="unknown-section", kind=kind, name=name, message=f"Unknown override section title: `{section_title}` (typo?)"))
        ps = _progress_state_value(secs)
        if ps == "invalid":
            issues.append(ValidationIssue(severity="WARN", code="invalid-progress-state", kind=kind, name=name, message="Progress state is present but not recognized (use `partial`/`complete`)."))

        titles = USER_INSTRUCTION_SECTIONS if kind == "instruction" else USER_METHOD_SECTIONS
        missing_sections = [title for title in titles if title not in OPTIONAL_USER_SECTIONS and not any(ln.strip() for ln in secs.get(title, []))]
        if ps == "complete" and missing_sections:
            issues.append(ValidationIssue(severity="WARN", code="complete-missing-sections", kind=kind, name=name, message="Marked complete but missing user-facing sections: " + ", ".join(f"`{title}`" for title in missing_sections)))

        if ps == "complete" and kind == "instruction" and is_input_instr.get(name, False):
            sem = "\n".join(secs.get("Semantics", []))
            sem_l = sem.lower()
            if re.search(r"\b(same as|like)\s+`[a-z0-9_]+`", sem_l):
                return
            if "empty" not in sem_l or "invalid" not in sem_l:
                issues.append(ValidationIssue(severity="WARN", code="complete-missing-input-handling", kind=kind, name=name, message="Marked complete but missing explicit empty/invalid input handling in `Semantics`."))

    for p in sorted(INSTRUCTION_OVERRIDES_DIR.glob("*.md")):
        name = p.stem
        if name not in engine_instr and name != "builtins-progress":
            issues.append(ValidationIssue(severity="WARN", code="stale-override", kind="instruction", name=name, message=f"Override file exists but instruction is not engine-registered: `{p.relative_to(REPO_ROOT)}`"))
            continue
        secs = _parse_override_sections(_read_text(p))
        check_override_file("instruction", name, p, secs)

    for p in sorted(METHOD_OVERRIDES_DIR.glob("*.md")):
        name = p.stem
        if name not in engine_meth:
            issues.append(ValidationIssue(severity="WARN", code="stale-override", kind="method", name=name, message=f"Override file exists but method is not engine-registered: `{p.relative_to(REPO_ROOT)}`"))
            continue
        secs = _parse_override_sections(_read_text(p))
        check_override_file("method", name, p, secs)

    for r in instr_regs:
        if not _has_user_facing_content("instruction", r.name):
            issues.append(ValidationIssue(severity="WARN", code="missing-user-doc", kind="instruction", name=r.name, message="No user-facing override content (will render as TODO)."))
    for r in method_regs:
        if not _has_user_facing_content("method", r.name):
            issues.append(ValidationIssue(severity="WARN", code="missing-user-doc", kind="method", name=r.name, message="No user-facing override content (will render as TODO)."))
    return issues


def _iter_authored_doc_paths() -> list[Path]:
    root = REPO_ROOT / "erabasic-reference"
    generated = {OUTPUT_MD.resolve(), OUTPUT_ENGINE_MD.resolve(), OUTPUT_INDEX_MD.resolve(), OUTPUT_PROGRESS_MD.resolve()}
    out: list[Path] = []
    for path in sorted(root.glob("*.md")):
        rp = path.resolve()
        if rp in generated:
            continue
        if path.name in {"agents.md", "builtins-reference.md", "builtins-index.md"}:
            continue
        out.append(path)
    return out


def _resolve_local_md_ref(from_path: Path, ref: str) -> tuple[Path | None, str | None]:
    ref = ref.strip()
    if "://" in ref:
        return None, None
    target, anchor = (ref.split("#", 1) + [None])[:2]
    target = target.strip()
    if not target:
        return None, anchor
    candidates: list[Path] = []
    if target.startswith("erabasic-reference/"):
        candidates.append(REPO_ROOT / target)
    else:
        candidates.append(from_path.parent / target)
        candidates.append(REPO_ROOT / "erabasic-reference" / target)
    for cand in candidates:
        if cand.exists():
            return cand.resolve(), anchor
    return None, anchor


def _heading_anchor_set(path: Path) -> set[str]:
    anchors: set[str] = set()
    for raw in _lines(path):
        if not raw.startswith("#"):
            continue
        title = raw.lstrip("#").strip()
        if title:
            anchors.add(_md_anchor(title))
    return anchors


def validate_authored_docs() -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    heading_cache: dict[Path, set[str]] = {}
    for path in _iter_authored_doc_paths():
        rel = path.relative_to(REPO_ROOT)
        lines = _lines(path)
        doc_name = str(rel)

        issues.extend(_line_pattern_issues(path=path, kind="doc", name=doc_name, lines=lines, source_path_code="topic-doc-source-path-leak", internal_symbol_code="topic-doc-internal-symbol-leak", japanese_code="topic-doc-japanese-text", vague_code="topic-doc-vague-phrase"))

        seen_anchor_lines: dict[str, int] = {}
        for line_no, raw in enumerate(lines, start=1):
            if raw.startswith("#"):
                title = raw.lstrip("#").strip()
                if title:
                    anchor = _md_anchor(title)
                    if anchor in seen_anchor_lines:
                        issues.append(ValidationIssue(severity="WARN", code="duplicate-heading-anchor", kind="doc", name=doc_name, message=f"{rel}:{line_no}: duplicate heading anchor `{anchor}` (first defined at line {seen_anchor_lines[anchor]})."))
                    else:
                        seen_anchor_lines[anchor] = line_no
            if _SEE_ABOVE_BELOW_RE.search(raw):
                issues.append(ValidationIssue(severity="WARN", code="see-above-below-crossref", kind="doc", name=doc_name, message=f"{rel}:{line_no}: uses unstable relative cross-reference wording like above/below/earlier/later."))
            refs = _ordered_unique(_MD_LINK_RE.findall(raw) + _BACKTICK_MD_REF_RE.findall(raw))
            for ref in refs:
                resolved, anchor = _resolve_local_md_ref(path, ref)
                if resolved is None:
                    issues.append(ValidationIssue(severity="ERROR", code="broken-local-crossref", kind="doc", name=doc_name, message=f"{rel}:{line_no}: local markdown reference not found: `{ref}`."))
                    continue
                if anchor:
                    anchors = heading_cache.setdefault(resolved, _heading_anchor_set(resolved))
                    if anchor not in anchors:
                        issues.append(ValidationIssue(severity="ERROR", code="broken-local-crossref", kind="doc", name=doc_name, message=f"{rel}:{line_no}: markdown reference target `{ref}` exists, but anchor `#{anchor}` does not."))
    return issues

def _print_validation_report(issues: list[ValidationIssue], *, verbose: bool) -> None:
    if not issues:
        print("OK: no built-ins override validation issues found.", file=sys.stderr)
        return
    counts: dict[tuple[str, str], int] = {}
    for it in issues:
        counts[(it.severity, it.code)] = counts.get((it.severity, it.code), 0) + 1
    summary = ", ".join([f"{sev}:{code}={n}" for (sev, code), n in sorted(counts.items())])
    print(f"WARN: built-ins override validation issues found: {summary}", file=sys.stderr)
    if not verbose:
        return
    for it in issues:
        print(f"{it.severity} {it.code} {it.kind} {it.name}: {it.message}", file=sys.stderr)


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
        if not _has_user_facing_content("instruction", r.name):
            continue
        secs = _load_override_sections("instruction", r.name)
        tags = _parse_tag_lines(secs.get("Tags", []))
        add("instruction", r.name, tags)

    for r in method_regs:
        if not _has_user_facing_content("method", r.name):
            continue
        secs = _load_override_sections("method", r.name)
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
        f"> Update `{OVERRIDES_DIR.relative_to(REPO_ROOT)}/**` or the generator/tooling inputs, then regenerate this file."
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


def _progress_state(override: dict[str, list[str]]) -> str:
    """
    Writing-progress state for overrides.

    States:
      - "none": no manual override exists
      - "partial": manual override exists but is not declared complete
      - "complete": explicitly declared complete in the override file

    This is intentionally conservative: in absence of an explicit marker, we treat
    an override as "partial" even if it looks detailed.
    """
    if not override:
        return "none"
    raw = override.get("Progress state", []) or override.get("Progress", [])
    for ln in raw:
        t = ln.strip().lstrip("-").strip().lower()
        if not t:
            continue
        if t in ("complete", "completed", "done"):
            return "complete"
        if t in ("partial", "incomplete", "wip", "draft"):
            return "partial"
    return "partial"


def _render_instruction_entry(
    reg: InstructionReg,
    structural: StructuralInfo | None,
    arg_specs: dict[str, ArgSpecInfo],
    instr_class_impl: dict[str, tuple[Path, int, int, list[str]]],
    switch_impl: dict[str, ImplSnippet],
) -> str:
    parts: list[str] = [f"## {reg.name} (instruction)"]

    override = _load_override_sections("instruction", reg.name)

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

    override = _load_override_sections("method", reg.name)

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
        choices=[
            "missing-user-doc",
            "stale-override",
            "unknown-section",
            "invalid-progress-state",
            "complete-missing-sections",
            "complete-entry-has-todo-marker",
            "duplicate-section",
            "stray-content-outside-sections",
            "noncanonical-section-order",
            "missing-argument-doc-for-syntax-placeholder",
            "orphan-argument-bullet",
            "argument-order-mismatch",
            "syntax-optional-mismatch",
            "default-without-optional",
            "suspicious-escaped-quote",
            "noncanonical-default-syntax",
            "noncanonical-required-marker",
            "noncanonical-omission-warning-phrase",
            "user-doc-source-path-leak",
            "user-doc-internal-symbol-leak",
            "user-doc-japanese-text",
            "banned-vague-phrase",
            "range-shorthand",
            "broken-local-crossref",
            "duplicate-heading-anchor",
            "see-above-below-crossref",
            "topic-doc-source-path-leak",
            "topic-doc-internal-symbol-leak",
            "topic-doc-japanese-text",
            "topic-doc-vague-phrase",
        ],
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

    issues = validate_builtins_overrides(instr_regs, method_regs) + validate_authored_docs()
    _print_validation_report(issues, verbose=args.report)

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
        f"> Make persistent content changes in `{OVERRIDES_DIR.relative_to(REPO_ROOT)}/**` or the generator/tooling inputs, then regenerate this file."
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
    md_user.append("- **Error**: the engine reports an error (typically aborting the current execution).")
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
        f"> Update `{OVERRIDES_DIR.relative_to(REPO_ROOT)}/**` or the generator/tooling inputs, then regenerate this file."
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
        st = _progress_state(_load_override_sections("instruction", r.name))
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
        st = _progress_state(_load_override_sections("method", r.name))
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
        override = _load_override_sections("instruction", r.name)
        st = _progress_state(override)
        mark = "⛔" if st == "none" else ("✅" if st == "complete" else "🟡")
        anchor = _md_anchor(f"{r.name} (instruction)")
        prog.append(f"- {mark} [`{r.name}`]({progress_link_target}#{anchor})")
    prog.append("")

    prog.append("## Expression functions")
    prog.append("")
    for r in method_regs:
        override = _load_override_sections("method", r.name)
        st = _progress_state(override)
        mark = "⛔" if st == "none" else ("✅" if st == "complete" else "🟡")
        anchor = _md_anchor(f"{r.name} (expression function)")
        prog.append(f"- {mark} [`{r.name}`]({progress_link_target}#{anchor})")
    prog.append("")

    OUTPUT_PROGRESS_MD.write_text("\n".join(prog).rstrip() + "\n", encoding="utf-8")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
