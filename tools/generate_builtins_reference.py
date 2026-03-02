#!/usr/bin/env python3
"""
Generate a single Markdown catalog for all EraBasic built-in instructions and expression functions
from the EvilMask/Emuera engine source.

Output:
  erabasic-reference/builtins-reference.md

Design goals:
  - English
  - No tables (per user preference)
  - Self-contained for built-in catalog use: includes an argument-spec glossary
  - Source of truth: emuera.em (engine code)
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import datetime as _dt
import re
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[2]

PATH_FUNCTION_IDENTIFIER = REPO_ROOT / "emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs"
PATH_FUNCTION_ARG_TYPE = REPO_ROOT / "emuera.em/Emuera/Runtime/Script/Statements/FunctionArgType.cs"
PATH_ARGUMENT_BUILDER = REPO_ROOT / "emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs"
PATH_SCRIPT_PROC = REPO_ROOT / "emuera.em/Emuera/Runtime/Script/Process.ScriptProc.cs"
PATH_METHOD_CREATOR = REPO_ROOT / "emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.cs"
PATH_METHOD_IMPL = REPO_ROOT / "emuera.em/Emuera/Runtime/Script/Statements/Function/Creator.Method.cs"

OUTPUT_MD = REPO_ROOT / "erabasic-reference/builtins-reference.md"
OUTPUT_PROGRESS_MD = REPO_ROOT / "erabasic-reference/builtins-overrides/builtins-progress.md"
OVERRIDES_DIR = REPO_ROOT / "erabasic-reference/builtins-overrides"
INSTRUCTION_OVERRIDES_DIR = OVERRIDES_DIR / "instructions"
METHOD_OVERRIDES_DIR = OVERRIDES_DIR / "methods"


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


# Legacy in-script overrides. Prefer `erabasic-reference/builtins-overrides/**/<NAME>.md`.
# Manual overrides for entries where we have already done a deeper read.
# This is how we gradually upgrade entries to the SORTCHARA/FINDCHARA level
# without pretending that everything can be inferred automatically.
INSTRUCTION_OVERRIDES: dict[str, dict[str, list[str]]] = {
    "ARRAYCOPY": {
        "Summary": [
            "- Copies elements from one array variable to another array variable of the same element type and dimension.",
        ],
        "Syntax": [
            "- `ARRAYCOPY <srcVarNameExpr>, <dstVarNameExpr>`",
        ],
        "Arguments": [
            "- `<srcVarNameExpr>`: string expression whose value is a variable name.",
            "- `<dstVarNameExpr>`: string expression whose value is a variable name.",
        ],
        "Defaults / optional arguments": [
            "- None.",
        ],
        "Semantics": [
            "- Resolves both variable names to variable tokens (early when literal, otherwise at runtime).",
            "- Requires both to be arrays (1D/2D/3D), non-character-data; destination must be non-const.",
            "- Copies element-wise, clamped by destination sizes per dimension; does not clear the rest.",
        ],
        "Errors & validation": [
            "- Errors if a name does not resolve to a variable, if either is not an array, if either is character-data, if destination is const, or if dimension/type mismatch.",
        ],
        "Examples": [
            "- `ARRAYCOPY \"ABL\", \"ABL_BAK\"`",
            "- `ARRAYCOPY \"ITEM\", SAVETO`",
        ],
    },
    "ARRAYSHIFT": {
        "Summary": [
            "- Shifts elements in a mutable 1D array variable by a signed offset and fills new slots with a default value.",
        ],
        "Syntax": [
            "- `ARRAYSHIFT <arrayVar>, <shift>, <default> [, <start> [, <count>]]`",
        ],
        "Arguments": [
            "- `<arrayVar>`: changeable 1D array variable term.",
            "- `<shift>`: int expression.",
            "- `<default>`: expression of the same value type as the array element type.",
            "- `<start>`: int expression (default `0`).",
            "- `<count>`: int expression (default “to end”; runtime uses `-1` sentinel).",
        ],
        "Defaults / optional arguments": [
            "- `<start>` defaults to `0`.",
            "- `<count>` omitted means “to the end” (engine passes `-1`).",
        ],
        "Semantics": [
            "- Operates on the segment `[start, start+count)` (or `[start, end)` if count omitted).",
            "- If `shift == 0`, does nothing.",
            "- If shifting removes all overlap, fills the whole segment with `<default>`.",
            "- If `start + count` exceeds array length, the engine clamps `count` to fit.",
        ],
        "Errors & validation": [
            "- Errors if `<arrayVar>` is not 1D, if `start < 0`, if `count < 0` (when provided), or if `start >= arrayLength`.",
        ],
        "Examples": [
            "- `ARRAYSHIFT SOME_INT_ARRAY, 1, 0`",
            "- `ARRAYSHIFT SOME_STR_ARRAY, -2, \"\", 10`",
        ],
    },
    "SORTCHARA": {
        "Summary": [
            "- Reorders the engine’s character list (`0 .. CHARANUM-1`) by a key taken from a character-data variable.",
            "- Observable engine behavior: keeps `MASTER` fixed at its numeric position for this instruction (`fixMaster=true`).",
        ],
        "Syntax": [
            "- `SORTCHARA`",
            "- `SORTCHARA FORWARD | BACK`",
            "- `SORTCHARA <charaVarTerm> [ , FORWARD | BACK ]`",
        ],
        "Arguments": [
            "- `<charaVarTerm>`: a variable term whose identifier is a character-data variable.",
            "- Order: `FORWARD` = ascending, `BACK` = descending.",
            "- If the key variable is an array, the element indices are taken from the variable term’s subscripts after the character selector.",
        ],
        "Defaults / optional arguments": [
            "- If no args: defaults to `NO` ascending.",
        ],
        "Semantics": [
            "- Computes a sort key for each character via `CharacterData.SetSortKey(sortkey, elem)`; null strings are treated as empty string.",
            "- Stable sort: ties broken by original order.",
            "- After sorting, `TARGET`/`ASSI` are updated to keep pointing at the same character objects; `MASTER` is fixed at its index for this instruction.",
        ],
        "Errors & validation": [
            "- Parse-time error if `<charaVarTerm>` is not a character-data variable term.",
            "- Runtime error if the selected element indices are out of range for the variable.",
        ],
        "Examples": [
            "- `SORTCHARA NO`",
            "- `SORTCHARA CFLAG:3, BACK`",
            "- `SORTCHARA NAME, FORWARD`",
        ],
    },
}

METHOD_OVERRIDES: dict[str, dict[str, list[str]]] = {
    "SUBSTRING": {
        "Summary": [
            "- Returns a substring where `start`/`length` are measured in the engine’s current language-encoding byte count (not Unicode code units).",
        ],
        "Signatures / argument rules": [
            "- `SUBSTRING(str)` → `string`",
            "- `SUBSTRING(str, start)` → `string`",
            "- `SUBSTRING(str, start, length)` → `string`",
        ],
        "Arguments": [
            "- `str`: string.",
            "- `start` (optional): int (byte offset, 0-based).",
            "- `length` (optional): int (byte length; `<0` means “to end”).",
        ],
        "Semantics": [
            "- Uses `LangManager.GetSubStringLang(str, start, length)` (encoding-aware).",
            "- If `start >= totalByte` or `length == 0`: returns `\"\"`.",
            "- If `length < 0` or `length > totalByte`: treated as `totalByte`.",
            "- Does not split characters: advances by character while tracking encoded byte counts.",
        ],
        "Errors & validation": [
            "- Argument type/count errors are rejected by `FunctionMethod.CheckArgumentType`.",
        ],
        "Examples": [
            "- `SUBSTRING(\"ABCDE\", 1, 2)` → `\"BC\"` (ASCII)",
        ],
    },
    "FINDCHARA": {
        "Summary": [
            "- Returns the first character index in the current character list whose chara-variable cell equals a target value.",
        ],
        "Signatures / argument rules": [
            "- `FINDCHARA(charaVarTerm, value)` → `long`",
            "- `FINDCHARA(charaVarTerm, value, startIndex)` → `long`",
            "- `FINDCHARA(charaVarTerm, value, startIndex, lastIndex)` → `long`",
        ],
        "Arguments": [
            "- `charaVarTerm`: character-data variable term (may be array; element indices taken from subscripts after the character selector).",
            "- `value`: same scalar type as the variable (string or int).",
            "- `startIndex` (optional, default `0`): inclusive start.",
            "- `lastIndex` (optional, default `CHARANUM`): exclusive end.",
        ],
        "Semantics": [
            "- Searches forward in `[startIndex, lastIndex)`; returns matching index or `-1` if not found or if `startIndex >= lastIndex`.",
            "- Equality check is direct (`==`) on the per-character cell value.",
        ],
        "Errors & validation": [
            "- Errors if `startIndex`/`lastIndex` are out of range; errors if `charaVarTerm` is not a character-data variable term.",
        ],
        "Examples": [
            "- `idx = FINDCHARA(NAME, \"Alice\")`",
            "- `idx = FINDCHARA(CFLAG:3, 1, 10)`",
        ],
    },
    "FINDLASTCHARA": {
        "Summary": [
            "- Like `FINDCHARA`, but searches backward and returns the last matching character index in the range.",
        ],
    },
}


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

    Search order:
      1) Markdown override file in `erabasic-reference/builtins-overrides/`
      2) Legacy in-script override dict
    """
    if kind == "instruction":
        p = INSTRUCTION_OVERRIDES_DIR / f"{name}.md"
        if p.exists():
            return _parse_override_sections(_read_text(p))
        return INSTRUCTION_OVERRIDES.get(name, {})
    if kind == "method":
        p = METHOD_OVERRIDES_DIR / f"{name}.md"
        if p.exists():
            return _parse_override_sections(_read_text(p))
        return METHOD_OVERRIDES.get(name, {})
    return {}


def _has_manual_override(kind: str, name: str) -> bool:
    secs = _load_override_sections(kind, name)
    return bool(secs)


def _render_instruction_entry(
    reg: InstructionReg,
    structural: StructuralInfo | None,
    arg_specs: dict[str, ArgSpecInfo],
    instr_class_impl: dict[str, tuple[Path, int, int, list[str]]],
    switch_impl: dict[str, ImplSnippet],
) -> str:
    parts: list[str] = [f"## {reg.name} (instruction)"]

    override = _load_override_sections("instruction", reg.name)

    # Summary
    parts.extend(_render_section("Summary", override.get("Summary", [])))

    # Metadata
    meta: list[str] = []
    if reg.arg_type:
        meta.append(f"- Arg spec: `{reg.arg_type}` (see #{_md_anchor('Argument spec: ' + reg.arg_type)})")
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
    spec = arg_specs.get(reg.arg_type) if reg.arg_type else None

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

    if "Defaults / optional arguments" in override:
        defaults = override["Defaults / optional arguments"]
    else:
        defaults = []
        if spec:
            defaults.append("- Optional/default behavior is builder-specific; see engine refs.")

    parts.append("")
    parts.extend(_render_section("Syntax", syntax))
    parts.append("")
    parts.extend(_render_section("Arguments", arguments))
    parts.append("")
    parts.extend(_render_section("Defaults / optional arguments", defaults))

    # Semantics / Errors: engine-extracted key operations + throws
    semantics: list[str] = list(override.get("Semantics", []))
    errors: list[str] = list(override.get("Errors & validation", []))
    refs: list[str] = []

    refs.append(f"- Registration: `{PATH_FUNCTION_IDENTIFIER.relative_to(REPO_ROOT)}`")
    if reg.arg_type:
        refs.append(f"- Arg builder mapping: `{PATH_ARGUMENT_BUILDER.relative_to(REPO_ROOT)}` (search `FunctionArgType.{reg.arg_type}`)")

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
        cls = None
        if reg.impl_ctor:
            mm = re.match(r"new\s+([A-Za-z0-9_]+)\b", reg.impl_ctor)
            if mm:
                cls = mm.group(1)
        if cls and cls not in instr_class_impl:
            cls = None
        if not cls:
            cls = f"{reg.name}_Instruction"
        if cls in instr_class_impl:
            p, start, _end, block = instr_class_impl[cls]
            argb_lines, flag_lines, ops, thr = _extract_instruction_class_info(block, cls)
            refs.append(f"- Execution: `{p.relative_to(REPO_ROOT)}`:{start} (`{cls}`)")
            base_flag_lines = [fl for fl in flag_lines if re.match(r"^flag\s*=", fl)]
            if base_flag_lines:
                semantics.append("- Engine-extracted notes (base flags from class):")
                for fl in base_flag_lines[:5]:
                    semantics.append(f"  - `{fl}`")
            if ops:
                semantics.append("- Engine-extracted notes (key operations):")
                for op in ops[:12]:
                    semantics.append(f"  - `{op}`")
            if thr:
                errors.append("- Engine-extracted notes (throws/errors):")
                for t in thr[:10]:
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


def main() -> None:
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

    # Compose markdown.
    gen_date = _dt.date.today().isoformat()
    md: list[str] = []
    md.append("# EraBasic Built-ins Reference (Emuera / EvilMask)")
    md.append("")
    md.append(f"Generated from engine source on `{gen_date}`.")
    md.append("")
    md.append("This document is intentionally **no-table** and uses a per-entry template:")
    md.append("- Summary / Syntax / Arguments / Defaults / Semantics / Errors / Examples / Engine refs")
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
    md.append(f"Total (method names in `FunctionMethodCreator`): `{len(method_regs)}`.")
    md.append("")
    for reg in method_regs:
        info = method_classes.get(reg.class_name)
        md.append(_render_method_entry(reg, info).rstrip())
        md.append("")

    OUTPUT_MD.write_text("\n".join(md).rstrip() + "\n", encoding="utf-8")

    # Progress tracker (manual overrides vs skeleton).
    prog: list[str] = []
    prog.append("# EraBasic Built-ins Writing Progress (Emuera / EvilMask)")
    prog.append("")
    prog.append(f"Generated on `{gen_date}`.")
    prog.append("")
    prog.append("Legend:")
    prog.append("- `✅` manual entry written (override present)")
    prog.append("- `⛔` skeleton only (needs manual write-up)")
    prog.append("")

    instr_done = sum(1 for r in instr_regs if _has_manual_override("instruction", r.name))
    meth_done = sum(1 for r in method_regs if _has_manual_override("method", r.name))

    prog.append(f"Instructions with manual override: `{instr_done}` / `{len(instr_regs)}`.")
    prog.append(f"Expression functions with manual override: `{meth_done}` / `{len(method_regs)}`.")
    prog.append("")

    prog.append("## Instructions")
    prog.append("")
    for r in instr_regs:
        mark = "✅" if _has_manual_override("instruction", r.name) else "⛔"
        anchor = _md_anchor(f"{r.name} (instruction)")
        prog.append(f"- {mark} `{r.name}` (`builtins-reference.md#{anchor}`)")
    prog.append("")

    prog.append("## Expression functions")
    prog.append("")
    for r in method_regs:
        mark = "✅" if _has_manual_override("method", r.name) else "⛔"
        anchor = _md_anchor(f"{r.name} (expression function)")
        prog.append(f"- {mark} `{r.name}` (`builtins-reference.md#{anchor}`)")
    prog.append("")

    OUTPUT_PROGRESS_MD.write_text("\n".join(prog).rstrip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
