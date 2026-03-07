#!/usr/bin/env python3
"""Engine-source registration parsing helpers for reference tooling."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

import reference_common as ref_common


REPO_ROOT = ref_common.MONOREPO_ROOT
PATH_FUNCTION_IDENTIFIER = REPO_ROOT / "emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs"
PATH_FUNCTION_ARG_TYPE = REPO_ROOT / "emuera.em/Emuera/Runtime/Script/Statements/FunctionArgType.cs"
PATH_ARGUMENT_BUILDER = REPO_ROOT / "emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs"
PATH_SCRIPT_PROC = REPO_ROOT / "emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs"
PATH_METHOD_CREATOR = REPO_ROOT / "emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs"
PATH_METHOD_IMPL = REPO_ROOT / "emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs"

_lines = ref_common.lines
_strip_csharp_comment = ref_common.strip_csharp_comment
_best_effort_translate_argtype_hint = ref_common.best_effort_translate_argtype_hint


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


def load_regs_for_lint() -> tuple[list[InstructionReg], list[MethodReg]]:
    fi_lines = _lines(PATH_FUNCTION_IDENTIFIER)
    fa_lines = _lines(PATH_FUNCTION_ARG_TYPE)
    ab_lines = _lines(PATH_ARGUMENT_BUILDER)
    instr_regs = parse_instruction_registrations(fi_lines)
    argtype_hints = parse_function_argtype_hints(fa_lines)
    parse_argument_specs(ab_lines, argtype_hints)
    method_lines = _lines(PATH_METHOD_CREATOR)
    method_regs = parse_method_registrations(method_lines)
    return instr_regs, method_regs
