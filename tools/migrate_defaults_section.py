#!/usr/bin/env python3
"""
Migrate built-ins override markdown files away from the legacy section:
  **Defaults / optional arguments**

New rule: defaults for omitted arguments should be described inline under **Arguments**
(and in **Syntax** / **Signatures**), not as a standalone section.

This script:
  - Removes the Defaults section.
  - If the Defaults section contains meaningful content, appends it under **Arguments**
    as a nested list under a bullet: "- Omitted arguments / defaults:".

It is intentionally conservative and does not attempt to rewrite prose.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys

import reference_common as ref_common


SECTION_RE = re.compile(r"^\*\*(.+?)\*\*\s*$")
DEFAULTS_TITLE = "Defaults / optional arguments"


@dataclass
class Doc:
    preface: list[str]
    sections: list[tuple[str, list[str]]]


def parse_doc(text: str) -> Doc:
    preface: list[str] = []
    sections: list[tuple[str, list[str]]] = []
    cur_title: str | None = None
    cur_lines: list[str] = []

    def flush() -> None:
        nonlocal cur_title, cur_lines
        if cur_title is None:
            return
        while cur_lines and cur_lines[0].strip() == "":
            cur_lines.pop(0)
        while cur_lines and cur_lines[-1].strip() == "":
            cur_lines.pop()
        sections.append((cur_title, list(cur_lines)))
        cur_lines = []

    for raw in text.splitlines():
        m = SECTION_RE.match(raw)
        if m:
            flush()
            cur_title = m.group(1).strip()
            continue
        if cur_title is None:
            preface.append(raw.rstrip())
        else:
            cur_lines.append(raw.rstrip())
    flush()
    return Doc(preface=preface, sections=sections)


def render_doc(doc: Doc) -> str:
    out: list[str] = []
    # Preserve any preface exactly, trimming only trailing blank lines.
    pre = list(doc.preface)
    while pre and pre[-1].strip() == "":
        pre.pop()
    out.extend(pre)
    if out and doc.sections:
        out.append("")
    for idx, (title, lines) in enumerate(doc.sections):
        out.append(f"**{title}**")
        if lines:
            out.extend(lines)
        if idx != len(doc.sections) - 1:
            out.append("")
    return "\n".join(out).rstrip() + "\n"


def _is_trivial_defaults(lines: list[str]) -> bool:
    tokens = [ln.strip() for ln in lines if ln.strip()]
    if not tokens:
        return True
    if len(tokens) == 1:
        t = tokens[0].lstrip("-").strip().lower()
        if t in ("none.", "none", "(todo)", "(todo: not yet documented)", "(todo: not documented)"):
            return True
    return False


def migrate_text(text: str) -> str:
    doc = parse_doc(text)

    defaults_lines: list[str] | None = None
    new_sections: list[tuple[str, list[str]]] = []
    for title, lines in doc.sections:
        if title == DEFAULTS_TITLE:
            defaults_lines = list(lines)
            continue
        new_sections.append((title, list(lines)))

    if defaults_lines is None:
        return text

    if not _is_trivial_defaults(defaults_lines):
        # Find Arguments section; if missing, create it before Semantics when possible.
        inserted = False
        for i, (title, lines) in enumerate(new_sections):
            if title == "Arguments":
                arg_lines = list(lines)
                if arg_lines and arg_lines[-1].strip() != "":
                    arg_lines.append("")
                arg_lines.append("- Omitted arguments / defaults:")
                for ln in defaults_lines:
                    if ln.strip() == "":
                        arg_lines.append("")
                        continue
                    if ln.lstrip().startswith("-"):
                        arg_lines.append("  " + ln.lstrip())
                    else:
                        arg_lines.append("  - " + ln.strip())
                new_sections[i] = (title, arg_lines)
                inserted = True
                break
        if not inserted:
            # Insert a new Arguments section.
            args_block: list[str] = []
            args_block.append("- Omitted arguments / defaults:")
            for ln in defaults_lines:
                if ln.strip() == "":
                    args_block.append("")
                    continue
                if ln.lstrip().startswith("-"):
                    args_block.append("  " + ln.lstrip())
                else:
                    args_block.append("  - " + ln.strip())

            # Prefer inserting before Semantics, otherwise append near the top.
            idx = next((i for i, (t, _l) in enumerate(new_sections) if t == "Semantics"), None)
            if idx is None:
                new_sections.append(("Arguments", args_block))
            else:
                new_sections.insert(idx, ("Arguments", args_block))

    doc2 = Doc(preface=doc.preface, sections=new_sections)
    return render_doc(doc2)


def main(argv: list[str] | None = None) -> int:
    overrides_root = ref_common.OVERRIDES_DIR
    paths = sorted([*overrides_root.glob("instructions/*.md"), *overrides_root.glob("methods/*.md")])

    changed = 0
    for p in paths:
        old = p.read_text(encoding="utf-8", errors="replace")
        new = migrate_text(old)
        if new != old:
            p.write_text(new, encoding="utf-8", errors="strict")
            changed += 1
    print(f"migrated_files={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

