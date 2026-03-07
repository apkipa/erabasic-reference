#!/usr/bin/env python3
"""
Repo-specific lint utilities for `erabasic-reference` authored documentation.

Rule layering:
- Topic docs use the shared authored-doc checks.
- Built-in override docs use the same shared checks plus stricter override-only
  structure / contract checks.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys
import re

import reference_common as ref_common
import reference_engine_registry as ref_engine


REPO_ROOT = ref_common.MONOREPO_ROOT
OUTPUT_MD = ref_common.OUTPUT_MD
OUTPUT_ENGINE_MD = ref_common.OUTPUT_ENGINE_MD
OUTPUT_INDEX_MD = ref_common.OUTPUT_INDEX_MD
OUTPUT_PROGRESS_MD = ref_common.OUTPUT_PROGRESS_MD
OVERRIDES_DIR = ref_common.OVERRIDES_DIR
INSTRUCTION_OVERRIDES_DIR = ref_common.INSTRUCTION_OVERRIDES_DIR
METHOD_OVERRIDES_DIR = ref_common.METHOD_OVERRIDES_DIR

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

FAIL_ON_CODES = (
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
    "redundant-expression-type-wording",
    "suspicious-escaped-quote",
    "noncanonical-default-syntax",
    "noncanonical-required-marker",
    "noncanonical-argument-metadata-placement",
    "noncanonical-omission-warning-phrase",
    "user-doc-source-path-leak",
    "user-doc-internal-symbol-leak",
    "banned-vague-phrase",
    "range-shorthand",
    "broken-local-crossref",
    "duplicate-heading-anchor",
    "see-above-below-crossref",
    "topic-doc-source-path-leak",
    "topic-doc-internal-symbol-leak",
    "topic-doc-vague-phrase",
    "structured-syntax-missing-code-block",
    "structured-examples-missing-erabasic-block",
)

_read_text = ref_common.read_text
_lines = ref_common.lines
_md_anchor = ref_common.md_anchor

def parse_override_sections(md_text: str) -> dict[str, list[str]]:
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


def load_override_sections(kind: str, name: str) -> dict[str, list[str]]:
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
            return parse_override_sections(_read_text(p))
        return {}
    if kind == "method":
        p = METHOD_OVERRIDES_DIR / f"{name}.md"
        if p.exists():
            return parse_override_sections(_read_text(p))
        return {}
    return {}


def has_user_facing_content(kind: str, name: str) -> bool:
    """
    Return True if an override contributes any user-facing content lines.

    Overrides may contain internal tooling-only sections (e.g. Progress state)
    without documenting the built-in for readers.
    """
    secs = load_override_sections(kind, name)
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


def override_progress_state(secs: dict[str, list[str]]) -> str:
    """Return the user-facing progress bucket for an override entry."""
    if not secs:
        return "none"
    state = _progress_state_value(secs)
    if state == "complete":
        return "complete"
    return "partial"


@dataclass(frozen=True)
class ArgumentDocSpec:
    name: str
    optional: bool
    has_default: bool
    raw: str


_OVERRIDE_SECTION_RE = re.compile(r"^\*\*(.+?)\*\*\s*$")
_TODO_MARKER_RE = re.compile(r"\b(?:TODO|TBD)\b|\?\?\?|not yet documented", re.IGNORECASE)
_SOURCE_PATH_RE = re.compile(r"(?:emuera\.em/[^`\s)]+|[A-Za-z0-9_./-]+\.cs(?::\d+)?(?![A-Za-z0-9_]))")
_DOTDOT_FRAGMENT_RE = re.compile(r"(?<!\.)`?([A-Za-z0-9_*()\[\]+\-/%]+)`?\s*\.\.\s*`?([A-Za-z0-9_*()\[\]+\-/%]+)`?(?!\.)")
_UPPER_PAIR_TOKEN_RE = re.compile(r"^[A-Z_][A-Z0-9_*]*$")
_RANGEY_TOKEN_RE = re.compile(r"[0-9a-z]|[()\[\]+\-*/%]")
_SEE_ABOVE_BELOW_RE = re.compile(
    r"""(?:
        \b(?:see|described|discussed|listed|shown|summarized|covered|explained|defined|noted)\s+(?:just\s+)?(?:above|below|earlier|later)\b
      | \b(?:table|tables|list|lists|section|sections|example|examples|rule|rules|note|notes|bullet|bullets|model|models|discussion)\s+(?:above|below|earlier|later)\b
      | (?:见|详见)(?:上文|下文)
      | (?:上文|下文)(?:所述|所示|所列)?
    )""",
    re.IGNORECASE | re.VERBOSE,
)
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


_TOPIC_REFERENCE_ALLOWED_HEADING_RES = [
    re.compile(r"^Fact-check cross-refs\b", re.IGNORECASE),
    re.compile(r"^Sources\b", re.IGNORECASE),
    re.compile(r"^Engine source of truth\b", re.IGNORECASE),
    re.compile(r"^Engine source repository\b", re.IGNORECASE),
    re.compile(r"^Documentation repository\b", re.IGNORECASE),
    re.compile(r"\bNon-normative\b", re.IGNORECASE),
]
_TOPIC_REFERENCE_BLOCK_START_RES = [
    re.compile(r"^Fact-check cross-ref(?:s)?\s*\(optional\)\s*:", re.IGNORECASE),
    re.compile(r"^Engine references?\s*\(fact-check\)\s*:", re.IGNORECASE),
    re.compile(r"^Implementation reference\s*:", re.IGNORECASE),
    re.compile(r"^Engine source of truth(?:\s+for\s+this\s+codebase)?\s*:", re.IGNORECASE),
]
_OVERRIDE_REQUIRED_MARKER_SECTIONS = {"Arguments", "Signatures / argument rules"}
_REQUIRED_MARKER_RE = re.compile(r"\(required\s+[^)]+\)")


_ARGUMENT_REDUNDANT_EXPRESSION_TYPE_RE = re.compile(r"\(([^)]*\b(?:int|string|bool) expression\b[^)]*)\)", re.IGNORECASE)
_ARGUMENT_LABEL_WITHOUT_METADATA_PARENS_RE = re.compile(r"^-\s+(.+?):\s+")
_ARGUMENT_LABEL_WITH_METADATA_PARENS_RE = re.compile(r"^-\s+(.+?)\s+\(([^)]*)\):\s+(.*)$")
_ARGUMENT_METADATA_KIND_RE = re.compile(r"\b(?:int|string|bool|literal|token|raw|formatted|form|identifier|keyword|variable|term|array|html|ref|chara|expression)\b", re.IGNORECASE)
_ARGUMENT_DESC_TYPEISH_RE = re.compile(
    r"^(?:"
    r"(?:first|second|third|fourth|fifth)\s+array size written as an integer literal"
    r"|scalar initializer written as a double-quoted literal"
    r"|(?:a\s+)?FORM/formatted string\b"
    r"|raw(?:\s+string)?(?:\s+token)?\b"
    r"|raw(?:\s+literal)?\s+text\b"
    r"|identifier token\b"
    r"|changeable\b"
    r"|integer literal\b"
    r"|double-quoted literal\b"
    r"|zero or more expressions\b"
    r"|one or more\b"
    r"|expression\b"
    r")",
    re.IGNORECASE,
)
_ARGUMENT_VARIABLE_TERM_KIND_RE = re.compile(r"^(?:(?:zero|one)\s+or\s+more\s+)?(?:a\s+|an\s+)?([^.:;]+?\bvariable terms?)\b", re.IGNORECASE)
_ARGUMENT_VARIABLE_TERM_QUALIFIER_RE = re.compile(r"\b(?:\d+d|changeable|non-character|character-data|int|integer|string)\b", re.IGNORECASE)
_ARGUMENT_DESC_FORMATTED_STRING_RE = re.compile(r"^(?:formatted string expression\b|FORM/formatted string\b)", re.IGNORECASE)
_CALL_FAMILY_EFFECTIVE_ARGTYPES = {"SP_CALL", "SP_CALLFORM", "SP_CALLF", "SP_CALLFORMF", "SP_CALLCSHARP"}


def _ordered_unique(items: Iterable[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def _extract_argument_label_names(prefix: str) -> list[str]:
    names: list[str] = []
    for frag in _extract_code_spans(prefix):
        for arg_name in _scan_argument_names_from_fragment(frag):
            if arg_name not in names:
                names.append(arg_name)
    for arg_name in re.findall(r"<([^<>]+)>", prefix):
        canon = _canonical_arg_name(arg_name)
        if canon not in names:
            names.append(canon)
    return names


def _canonical_arg_name(name: str) -> str:
    if "|" in name:
        return name
    name = re.sub(r"\.\.\.$", "", name)
    name = re.sub(r"\*$", "", name)
    name = re.sub(r"\d+$", "", name)
    if len(name) >= 2 and name.endswith("N") and name[-2].islower():
        name = name[:-1]
    return name


def _has_range_shorthand(raw: str) -> bool:
    for m in _DOTDOT_FRAGMENT_RE.finditer(raw):
        left = m.group(1).strip("`")
        right = m.group(2).strip("`")
        if _UPPER_PAIR_TOKEN_RE.fullmatch(left) and _UPPER_PAIR_TOKEN_RE.fullmatch(right):
            continue
        if _RANGEY_TOKEN_RE.search(left) or _RANGEY_TOKEN_RE.search(right):
            return True
    return False




def _has_unescaped_double_quote(raw: str) -> bool:
    for idx, ch in enumerate(raw):
        if ch != '"':
            continue
        backslashes = 0
        probe = idx - 1
        while probe >= 0 and raw[probe] == "\\":
            backslashes += 1
            probe -= 1
        if backslashes % 2 == 0:
            return True
    return False


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
            name = re.sub(r"\s+", " ", text[i + 1 : j].strip())
            if name:
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
    first_semicolon = text.find(";")
    delim_positions = [pos for pos in (first_space, first_semicolon) if pos != -1]
    first_delim = min(delim_positions) if delim_positions else -1
    if first_paren != -1 and (first_delim == -1 or first_paren < first_delim):
        text = text[first_paren + 1 : text.rfind(")")]
    else:
        if first_delim == -1:
            return []
        text = text[first_delim + 1 :].lstrip()
    return _scan_token_stream(text)


def _scan_argument_names_from_fragment(fragment: str) -> list[str]:
    return [name for name, _ in _scan_token_stream(fragment.strip())]


def _collect_syntax_placeholder_names(secs: dict[str, list[str]]) -> list[str]:
    names: list[str] = []
    for raw in secs.get("Syntax", []):
        if not re.match(r"^-\s+`", raw):
            continue
        for frag in _extract_code_spans(raw):
            for placeholder in re.findall(r"<([^<>]+)>", frag):
                canon = _canonical_arg_name(re.sub(r"\s+", " ", placeholder.strip()))
                if canon and canon not in names:
                    names.append(canon)
    return names


def _collect_syntax_contract(secs: dict[str, list[str]]) -> tuple[list[str], dict[str, bool]]:
    forms: list[list[tuple[str, bool]]] = []
    for raw in secs.get("Syntax", []):
        if not re.match(r"^-\s+`", raw):
            continue
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
    form_names: list[list[str]] = []
    saw_required: set[str] = set()
    saw_optional: set[str] = set()
    for form in forms:
        names_in_form: list[str] = []
        seen_in_form: set[str] = set()
        for name, is_optional in form:
            if name not in order:
                order.append(name)
            if is_optional:
                saw_optional.add(name)
            else:
                saw_required.add(name)
            if name in seen_in_form:
                continue
            seen_in_form.add(name)
            names_in_form.append(name)
        form_names.append(names_in_form)

    can_omit: dict[str, bool] = {
        name: (name in saw_optional and name not in saw_required)
        for name in order
    }

    for shorter in form_names:
        for longer in form_names:
            if len(longer) <= len(shorter):
                continue
            if longer[: len(shorter)] != shorter:
                continue
            for name in longer[len(shorter) :]:
                can_omit[name] = True

    for name in order:
        can_omit.setdefault(name, False)
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
        m = re.match(r"^-\s+(.*?)(?:\s+\(|:|\s+is\b|\s+are\b)", stripped)
        prefix = m.group(1) if m else stripped[2:]
        names: list[str] = []
        for frag in _extract_code_spans(prefix):
            for name in _scan_argument_names_from_fragment(frag):
                if name not in names:
                    names.append(name)
        for name in re.findall(r"<([^<>\s]+)>", prefix):
            canon = _canonical_arg_name(name)
            if canon not in names:
                names.append(canon)
        if not names:
            continue
        is_optional = bool(re.search(r"\([^)]*\boptional\b", stripped, re.IGNORECASE))
        has_default = bool(re.search(r"\([^)]*\bdefault\b", stripped, re.IGNORECASE))
        for name in names:
            if name not in order:
                order.append(name)
            meta.setdefault(name, ArgumentDocSpec(name=name, optional=is_optional, has_default=has_default, raw=stripped))
    return order, meta


def _line_pattern_issues(*, path: Path, kind: str, name: str, lines: list[str], source_path_code: str, internal_symbol_code: str, vague_code: str, check_required_marker: bool = True, source_path_exempt_lines: set[int] | None = None, internal_symbol_exempt_lines: set[int] | None = None) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    rel = path.relative_to(REPO_ROOT)
    source_exempt_lines = source_path_exempt_lines or set()
    internal_exempt_lines = internal_symbol_exempt_lines or set()
    for line_no, raw in enumerate(lines, start=1):
        if r'\"' in raw and not _has_unescaped_double_quote(raw):
            issues.append(ValidationIssue(severity="WARN", code="suspicious-escaped-quote", kind=kind, name=name, message=f"{rel}:{line_no}: contains only backslash-escaped double quotes; if the backslashes are not literal, prefer plain double quotes in Markdown prose/examples."))
        if "default =" in raw:
            issues.append(ValidationIssue(severity="WARN", code="noncanonical-default-syntax", kind=kind, name=name, message=f"{rel}:{line_no}: uses `default =`; prefer a canonical form such as `default `0`` or `default current array length`."))
        if check_required_marker and _REQUIRED_MARKER_RE.search(raw):
            issues.append(ValidationIssue(severity="WARN", code="noncanonical-required-marker", kind=kind, name=name, message=f"{rel}:{line_no}: uses a `(required ...)` marker; rely on the global default-required rule unless special disambiguation is needed."))
        if "with a warning if omitted" in raw:
            issues.append(ValidationIssue(severity="WARN", code="noncanonical-omission-warning-phrase", kind=kind, name=name, message=f"{rel}:{line_no}: uses legacy wording `with a warning if omitted`; prefer `default X; omission emits a warning`."))
        if line_no not in source_exempt_lines and _SOURCE_PATH_RE.search(raw):
            issues.append(ValidationIssue(severity="ERROR", code=source_path_code, kind=kind, name=name, message=f"{rel}:{line_no}: leaks a source path or `.cs` reference into user-facing prose."))
        if line_no not in internal_exempt_lines and any(p.search(raw) for p in _INTERNAL_SYMBOL_RES):
            issues.append(ValidationIssue(severity="WARN", code=internal_symbol_code, kind=kind, name=name, message=f"{rel}:{line_no}: mentions engine-internal symbol names; prefer external/observable contract wording."))
        if any(p.search(raw) for p in _VAGUE_PHRASE_RES):
            issues.append(ValidationIssue(severity="WARN", code=vague_code, kind=kind, name=name, message=f"{rel}:{line_no}: contains vague wording that may weaken reimplementation-grade precision."))
        if _has_range_shorthand(raw):
            issues.append(ValidationIssue(severity="WARN", code="range-shorthand", kind=kind, name=name, message=f"{rel}:{line_no}: uses `a..b`-style shorthand; prefer canonical interval notation such as `[0, n)` or explicit inequalities."))
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


def _topic_reference_exempt_lines(lines: list[str]) -> set[int]:
    exempt: set[int] = set()
    heading_stack: list[str] = []
    block_mode = False
    for line_no, raw in enumerate(lines, start=1):
        stripped = raw.strip()
        heading_exempt = any(rx.search(title) for title in heading_stack for rx in _TOPIC_REFERENCE_ALLOWED_HEADING_RES)
        block_start = any(rx.search(stripped) for rx in _TOPIC_REFERENCE_BLOCK_START_RES)
        if raw.startswith("#"):
            level = len(raw) - len(raw.lstrip("#"))
            title = raw[level:].strip()
            heading_stack = heading_stack[: level - 1]
            if title:
                heading_stack.append(title)
            block_mode = False
            heading_exempt = any(rx.search(title) for title in heading_stack for rx in _TOPIC_REFERENCE_ALLOWED_HEADING_RES)
            block_start = False
        elif block_start:
            block_mode = True
        elif block_mode and stripped and not stripped.startswith(("- ", "* ")) and not re.match(r"^\d+[.)]\s", stripped):
            block_mode = False
        if heading_exempt or block_mode or block_start:
            exempt.add(line_no)
    return exempt


def _lint_override_required_markers(*, path: Path, kind: str, name: str) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    rel = path.relative_to(REPO_ROOT)
    current_section: str | None = None
    for line_no, raw in enumerate(_lines(path), start=1):
        m = _OVERRIDE_SECTION_RE.match(raw)
        if m:
            current_section = m.group(1).strip()
            continue
        if current_section not in _OVERRIDE_REQUIRED_MARKER_SECTIONS:
            continue
        if _REQUIRED_MARKER_RE.search(raw):
            issues.append(ValidationIssue(severity="WARN", code="noncanonical-required-marker", kind=kind, name=name, message=f"{rel}:{line_no}: uses a `(required ...)` marker; rely on the global default-required rule unless special disambiguation is needed."))
    return issues


def _lint_override_argument_wording(*, path: Path, kind: str, name: str) -> list[ValidationIssue]:
    """Lint canonical `Arguments` bullet shape.

    Canonical form:
    - `- <arg> (metadata): description`

    Authoring rules enforced here:
    - before the colon, keep only the parameter name / family name
    - place all argument metadata in the post-name parentheses
      (type / token-kind / binding-kind / optionality / default / omission behavior)
    - after the colon, start with the parameter's semantic role / effect, not another
      type-ish phrase that should have lived in the parentheses

    This intentionally uses one shared lint code for all of these:
    - metadata written after the colon with no parentheses,
    - metadata written only partially in parentheses (for example `(optional): int literal ...`), and
    - parentheses that use only a weaker umbrella kind while the description still starts
      with a more specific kind phrase that should have lived in the parentheses.
    """
    issues: list[ValidationIssue] = []
    rel = path.relative_to(REPO_ROOT)
    current_section: str | None = None
    for line_no, raw in enumerate(_lines(path), start=1):
        m = _OVERRIDE_SECTION_RE.match(raw)
        if m:
            current_section = m.group(1).strip()
            continue
        if current_section != "Arguments":
            continue
        if not raw.startswith("- "):
            continue

        stripped = raw.strip()

        m_label = _ARGUMENT_LABEL_WITHOUT_METADATA_PARENS_RE.match(stripped)
        if m_label:
            prefix = m_label.group(1).strip()
            if "(" not in prefix and _extract_argument_label_names(prefix):
                issues.append(ValidationIssue(severity="WARN", code="noncanonical-argument-metadata-placement", kind=kind, name=name, message=f"{rel}:{line_no}: place all argument metadata in parentheses after the argument name (for example: `<arg>` `(int): ...`) instead of writing it after the colon."))

        m_meta = _ARGUMENT_LABEL_WITH_METADATA_PARENS_RE.match(stripped)
        if m_meta:
            prefix = m_meta.group(1).strip()
            meta = m_meta.group(2).strip()
            desc = m_meta.group(3).strip()
            meta_l = meta.lower().replace("integer", "int")
            if _extract_argument_label_names(prefix) and ("optional" in meta_l or "default" in meta_l) and not _ARGUMENT_METADATA_KIND_RE.search(meta) and _ARGUMENT_DESC_TYPEISH_RE.search(desc):
                issues.append(ValidationIssue(severity="WARN", code="noncanonical-argument-metadata-placement", kind=kind, name=name, message=f"{rel}:{line_no}: the parentheses contain only control metadata such as `optional`/`default`, but the post-colon text still starts with argument-kind metadata; move that metadata into the parentheses (for example: `(optional, int literal)`)."))
            if _extract_argument_label_names(prefix) and "variable term" in meta_l:
                m_var = _ARGUMENT_VARIABLE_TERM_KIND_RE.match(desc)
                if m_var:
                    desc_kind = m_var.group(1).lower().replace("integer", "int")
                    meta_tokens = set(_ARGUMENT_VARIABLE_TERM_QUALIFIER_RE.findall(meta_l))
                    desc_tokens = set(_ARGUMENT_VARIABLE_TERM_QUALIFIER_RE.findall(desc_kind))
                    if desc_tokens - meta_tokens:
                        issues.append(ValidationIssue(severity="WARN", code="noncanonical-argument-metadata-placement", kind=kind, name=name, message=f"{rel}:{line_no}: the parentheses use a generic variable-term kind, but the post-colon text starts with a more specific variable-term kind; move the specific kind into the parentheses."))
            if _extract_argument_label_names(prefix) and re.search(r"\bstring\b", meta_l) and not re.search(r"\b(?:form|formatted)\b", meta_l) and _ARGUMENT_DESC_FORMATTED_STRING_RE.search(desc):
                issues.append(ValidationIssue(severity="WARN", code="noncanonical-argument-metadata-placement", kind=kind, name=name, message=f"{rel}:{line_no}: the parentheses say `string`, but the post-colon text starts with formatted-string kind metadata; move `FORM/formatted string` into the parentheses."))

        m_type = _ARGUMENT_REDUNDANT_EXPRESSION_TYPE_RE.search(raw)
        if not m_type:
            continue
        issues.append(ValidationIssue(severity="WARN", code="redundant-expression-type-wording", kind=kind, name=name, message=f"{rel}:{line_no}: in `Arguments`, prefer `int`/`string`/`bool` over `int expression`/`string expression`/`bool expression`."))
    return issues


def _effective_instruction_arg_types(instr_regs: list[InstructionReg]) -> dict[str, str | None]:
    out: dict[str, str | None] = {}
    instr_class_impl = ref_engine._scan_csharp_classes(ref_engine.PATH_ARGUMENT_BUILDER.parent, class_name_suffix="_Instruction")
    for reg in instr_regs:
        effective = reg.arg_type
        if effective is None and reg.reg_kind not in ("Switch", "Internal"):
            cls_name: str | None = None
            if reg.impl_ctor:
                mm = re.match(r"new\s+([A-Za-z0-9_]+)\b", reg.impl_ctor)
                if mm:
                    cls_name = mm.group(1)
            if cls_name and cls_name not in instr_class_impl:
                cls_name = None
            if not cls_name:
                cls_name = f"{reg.name}_Instruction"
            if cls_name in instr_class_impl:
                _p, _start, _end, block = instr_class_impl[cls_name]
                argb_lines, _flag_lines, _ops, _thr = ref_engine._extract_instruction_class_info(block, cls_name)
                candidates = ref_engine._infer_arg_types_from_argbuilder_lines(argb_lines)
                if len(candidates) == 1:
                    effective = candidates[0]
        out[reg.name] = effective
    return out


def _lint_call_family_syntax(*, path: Path, kind: str, name: str, secs: dict[str, list[str]], effective_arg_type: str | None) -> list[ValidationIssue]:
    if kind != "instruction" or effective_arg_type not in _CALL_FAMILY_EFFECTIVE_ARGTYPES:
        return []
    rel = path.relative_to(REPO_ROOT)
    syntax_text = "\n".join(secs.get("Syntax", []))
    missing: list[str] = []
    if "()" not in syntax_text:
        missing.append("explicit empty-paren form `...()`")
    if "[<subName1>, <subName2>, ...]" not in syntax_text:
        missing.append("bracket compatibility form `...[<subName1>, <subName2>, ...]`")
    if "[<subName1>, <subName2>, ...](<arg1>" not in syntax_text:
        missing.append("combined bracket-plus-argument form `...[<subName1>, <subName2>, ...](<arg1> ...)`")
    if not missing:
        return []
    return [ValidationIssue(severity="WARN", code="incomplete-call-family-syntax", kind=kind, name=name, message=f"{rel}: uses `{effective_arg_type}`, whose parser also accepts empty-paren and bracket compatibility forms, but `Syntax` does not document: {', '.join(missing)}.")]


def _syntax_starts_with_text_fence(secs: dict[str, list[str]]) -> bool:
    for raw in secs.get("Syntax", []):
        stripped = raw.strip()
        if not stripped:
            continue
        return stripped == "```text"
    return False


def _structured_syntax_instruction_names(instr_regs: list[InstructionReg]) -> set[str]:
    structural_map = ref_engine.parse_structural_info(_lines(ref_engine.PATH_FUNCTION_IDENTIFIER))
    engine_instr = {r.name for r in instr_regs}
    return {name for name, info in structural_map.items() if info.match_end and name in engine_instr}


def _structured_example_instruction_names(instr_regs: list[InstructionReg]) -> set[str]:
    structural_map = ref_engine.parse_structural_info(_lines(ref_engine.PATH_FUNCTION_IDENTIFIER))
    engine_instr = {r.name for r in instr_regs}
    return {name for name in structural_map if name in engine_instr}


def _first_nonblank_line(lines: list[str]) -> str:
    for raw in lines:
        stripped = raw.strip()
        if stripped:
            return stripped
    return ""


def _iter_fenced_blocks(lines: list[str]) -> list[tuple[str, list[str]]]:
    blocks: list[tuple[str, list[str]]] = []
    current_fence: str | None = None
    current_lines: list[str] = []
    for raw in lines:
        stripped = raw.strip()
        if current_fence is None:
            if stripped.startswith("```"):
                current_fence = stripped
                current_lines = []
            continue
        if stripped == "```":
            blocks.append((current_fence, list(current_lines)))
            current_fence = None
            current_lines = []
            continue
        current_lines.append(raw)
    return blocks


def _structured_block_has_noncanonical_indent(lines: list[str]) -> bool:
    positive_indents: list[int] = []
    for raw in lines:
        if not raw.strip():
            continue
        if raw.startswith("	"):
            return True
        indent = len(raw) - len(raw.lstrip(" "))
        if indent > 0:
            positive_indents.append(indent)
    if not positive_indents:
        return False
    min_positive = min(positive_indents)
    if min_positive != 4:
        return True
    return any(indent % 4 != 0 for indent in positive_indents)


def _lint_structured_syntax_presentation(*, path: Path, kind: str, name: str, secs: dict[str, list[str]], structured_syntax_instruction_names: set[str]) -> list[ValidationIssue]:
    if kind != "instruction" or name not in structured_syntax_instruction_names:
        return []
    if _syntax_starts_with_text_fence(secs):
        return []
    rel = path.relative_to(REPO_ROOT)
    return [ValidationIssue(severity="WARN", code="structured-syntax-missing-code-block", kind=kind, name=name, message=f"{rel}: structured instruction syntax should start with a fenced `text` block showing the overall multi-line construct; keep machine-readable bullet/backtick forms below it.")]


def _lint_structured_examples_presentation(*, path: Path, kind: str, name: str, secs: dict[str, list[str]], structured_example_instruction_names: set[str]) -> list[ValidationIssue]:
    if kind != "instruction" or name not in structured_example_instruction_names:
        return []
    rel = path.relative_to(REPO_ROOT)
    example_lines = secs.get("Examples", [])
    first = _first_nonblank_line(example_lines)
    issues: list[ValidationIssue] = []
    if first and first != "```erabasic":
        issues.append(ValidationIssue(severity="WARN", code="structured-examples-missing-erabasic-block", kind=kind, name=name, message=f"{rel}: structured instruction examples should start with a fenced `erabasic` block showing the full construct."))
    for fence, block_lines in _iter_fenced_blocks(example_lines):
        if fence != "```erabasic":
            continue
        if _structured_block_has_noncanonical_indent(block_lines):
            issues.append(ValidationIssue(severity="WARN", code="structured-examples-noncanonical-indent", kind=kind, name=name, message=f"{rel}: structured instruction examples should use 4-space indentation per nesting level inside fenced `erabasic` blocks."))
            break
    return issues


def _lint_override_argument_contracts(*, path: Path, kind: str, name: str, secs: dict[str, list[str]]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    rel = path.relative_to(REPO_ROOT)
    syntax_order, syntax_optional = _collect_syntax_contract(secs)
    syntax_placeholders = _collect_syntax_placeholder_names(secs)
    arg_order, arg_meta = _parse_argument_bullets(secs)
    arg_lines = secs.get("Arguments", [])
    if any(re.match(r"^\s*-\s+Same as\b", raw) for raw in arg_lines):
        for spec in arg_meta.values():
            if spec.has_default and not spec.optional:
                issues.append(ValidationIssue(severity="ERROR", code="default-without-optional", kind=kind, name=name, message=f"{rel}: argument `{spec.name}` documents a default but is not marked `optional`."))
        return issues

    for spec in arg_meta.values():
        if spec.has_default and not spec.optional:
            issues.append(ValidationIssue(severity="ERROR", code="default-without-optional", kind=kind, name=name, message=f"{rel}: argument `{spec.name}` documents a default but is not marked `optional`."))

    if syntax_placeholders and not arg_meta:
        issues.append(ValidationIssue(severity="ERROR", code="missing-argument-doc-for-syntax-placeholder", kind=kind, name=name, message=f"{rel}: `Syntax` uses placeholder names but `Arguments` has no named argument bullets; document them with canonical bullets such as `<arg>` `(int): ...`."))
        return issues

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
    effective_instr_arg_type = _effective_instruction_arg_types(instr_regs)
    structured_syntax_instruction_names = _structured_syntax_instruction_names(instr_regs)
    structured_example_instruction_names = _structured_example_instruction_names(instr_regs)
    is_input_instr: dict[str, bool] = {}
    for r in instr_regs:
        flags = (r.flags_expr or "") + " " + (r.additional_flags_expr or "")
        is_input_instr[r.name] = "IS_INPUT" in flags

    allowed_instruction = set(USER_INSTRUCTION_SECTIONS) | {"Progress state", "Progress"}
    allowed_method = set(USER_METHOD_SECTIONS) | {"Progress state", "Progress"}

    def check_override_file(kind: str, name: str, path: Path, secs: dict[str, list[str]]) -> None:
        issues.extend(_line_pattern_issues(path=path, kind=kind, name=name, lines=_lines(path), source_path_code="user-doc-source-path-leak", internal_symbol_code="user-doc-internal-symbol-leak", vague_code="banned-vague-phrase", check_required_marker=False))
        issues.extend(_lint_override_structure(path=path, kind=kind, name=name, secs=secs))
        issues.extend(_lint_override_required_markers(path=path, kind=kind, name=name))
        issues.extend(_lint_override_argument_wording(path=path, kind=kind, name=name))
        issues.extend(_lint_override_argument_contracts(path=path, kind=kind, name=name, secs=secs))
        issues.extend(_lint_call_family_syntax(path=path, kind=kind, name=name, secs=secs, effective_arg_type=effective_instr_arg_type.get(name) if kind == "instruction" else None))
        issues.extend(_lint_structured_syntax_presentation(path=path, kind=kind, name=name, secs=secs, structured_syntax_instruction_names=structured_syntax_instruction_names))
        issues.extend(_lint_structured_examples_presentation(path=path, kind=kind, name=name, secs=secs, structured_example_instruction_names=structured_example_instruction_names))

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
        secs = parse_override_sections(_read_text(p))
        check_override_file("instruction", name, p, secs)

    for p in sorted(METHOD_OVERRIDES_DIR.glob("*.md")):
        name = p.stem
        if name not in engine_meth:
            issues.append(ValidationIssue(severity="WARN", code="stale-override", kind="method", name=name, message=f"Override file exists but method is not engine-registered: `{p.relative_to(REPO_ROOT)}`"))
            continue
        secs = parse_override_sections(_read_text(p))
        check_override_file("method", name, p, secs)

    for r in instr_regs:
        if not has_user_facing_content("instruction", r.name):
            issues.append(ValidationIssue(severity="WARN", code="missing-user-doc", kind="instruction", name=r.name, message="No user-facing override content (will render as TODO)."))
    for r in method_regs:
        if not has_user_facing_content("method", r.name):
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


def _broken_local_md_ref_message(*, rel: Path, line_no: int, ref: str) -> str:
    target = ref.split("#", 1)[0].strip()
    if target.startswith(("emuera.em.doc/", "emuera.em/")):
        return f"{rel}:{line_no}: local markdown reference not found: `{ref}`. This looks like a sibling-repo path; if intentional, add a leading `../`."
    return f"{rel}:{line_no}: local markdown reference not found: `{ref}`."


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
        reference_exempt_lines = _topic_reference_exempt_lines(lines)

        issues.extend(_line_pattern_issues(path=path, kind="doc", name=doc_name, lines=lines, source_path_code="topic-doc-source-path-leak", internal_symbol_code="topic-doc-internal-symbol-leak", vague_code="topic-doc-vague-phrase", check_required_marker=False, source_path_exempt_lines=reference_exempt_lines, internal_symbol_exempt_lines=reference_exempt_lines))

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
                issues.append(ValidationIssue(severity="WARN", code="see-above-below-crossref", kind="doc", name=doc_name, message=f"{rel}:{line_no}: uses unstable relative cross-reference wording like `see below`/`model above`; prefer an explicit file/section reference instead."))
            refs = _ordered_unique(_MD_LINK_RE.findall(raw) + _BACKTICK_MD_REF_RE.findall(raw))
            for ref in refs:
                resolved, anchor = _resolve_local_md_ref(path, ref)
                if resolved is None:
                    issues.append(ValidationIssue(severity="ERROR", code="broken-local-crossref", kind="doc", name=doc_name, message=_broken_local_md_ref_message(rel=rel, line_no=line_no, ref=ref)))
                    continue
                if anchor:
                    anchors = heading_cache.setdefault(resolved, _heading_anchor_set(resolved))
                    if anchor not in anchors:
                        issues.append(ValidationIssue(severity="ERROR", code="broken-local-crossref", kind="doc", name=doc_name, message=f"{rel}:{line_no}: markdown reference target `{ref}` exists, but anchor `#{anchor}` does not."))
    return issues

def validate_topic_docs() -> list[ValidationIssue]:
    return validate_authored_docs()


def validate_reference_docs(instr_regs, method_regs) -> list[ValidationIssue]:
    return validate_builtins_overrides(instr_regs, method_regs) + validate_topic_docs()


def print_validation_report(issues: list[ValidationIssue], *, verbose: bool) -> None:
    if not issues:
        print("OK: no reference validation issues found.", file=sys.stderr)
        return
    counts: dict[tuple[str, str], int] = {}
    for it in issues:
        counts[(it.severity, it.code)] = counts.get((it.severity, it.code), 0) + 1
    summary = ", ".join([f"{sev}:{code}={n}" for (sev, code), n in sorted(counts.items())])
    print(f"WARN: reference validation issues found: {summary}", file=sys.stderr)
    if not verbose:
        return
    for it in issues:
        print(f"{it.severity} {it.code} {it.kind} {it.name}: {it.message}", file=sys.stderr)
