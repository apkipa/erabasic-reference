#!/usr/bin/env python3
"""
Normalize built-ins override markdown snippets to match the reference authoring rules.

Current normalization goals:
  - Remove in-entry "- Omitted arguments / defaults:" blocks from **Arguments** sections.
  - Where feasible, merge the omitted/default information into existing argument bullets.
  - Avoid engine-internal terminology; keep user-facing, reimplementation-grade wording.

This tool intentionally applies a small set of conservative rewrites and prints a report.
If a rewrite cannot be applied confidently, it will leave the text unchanged and report it.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import re
import sys

import reference_common as ref_common


OVERRIDES_DIR = ref_common.OVERRIDES_DIR


SECTION_RE = re.compile(r"^\*\*(?P<title>[^*]+)\*\*\s*$")

OMITTED_HEADER = "- Omitted arguments / defaults:"


_INT_EXPR_RE = re.compile(r"\b(integer|int)\s+expression\b", re.IGNORECASE)


@dataclass
class OmittedBlock:
    start: int
    end: int
    sub_bullets: list[str]


_read_text = ref_common.read_text


def _write_text(p: Path, s: str) -> None:
    ref_common.write_text(p, s)


def _split_sections(lines: list[str]) -> list[tuple[str, int, int]]:
    """
    Return a list of (title, start_index, end_index) where start/end bound the
    body lines (excluding the header line). end_index is exclusive.
    """
    headers: list[tuple[str, int]] = []
    for i, line in enumerate(lines):
        m = SECTION_RE.match(line)
        if m:
            headers.append((m.group("title").strip(), i))
    out: list[tuple[str, int, int]] = []
    for idx, (title, header_i) in enumerate(headers):
        body_start = header_i + 1
        body_end = headers[idx + 1][1] if idx + 1 < len(headers) else len(lines)
        out.append((title, body_start, body_end))
    return out


def _find_omitted_blocks(arg_lines: list[str]) -> list[OmittedBlock]:
    blocks: list[OmittedBlock] = []
    i = 0
    while i < len(arg_lines):
        if arg_lines[i].startswith(OMITTED_HEADER):
            start = i
            i += 1
            sub: list[str] = []
            while i < len(arg_lines):
                line = arg_lines[i]
                if line.startswith("**"):
                    break
                if line.startswith("- "):
                    break
                if line.startswith("  - ") or line.startswith("    - "):
                    sub.append(line.strip())
                    i += 1
                    continue
                if line.strip() == "":
                    i += 1
                    continue
                # Any other indentation means we're out of the omitted block.
                if not line.startswith(" "):
                    break
                i += 1
            end = i
            blocks.append(OmittedBlock(start=start, end=end, sub_bullets=sub))
        else:
            i += 1
    return blocks


def _rewrite_raw_optional_default(arg_lines: list[str], *, default_is_no_output: bool) -> bool:
    """
    Rewrite the common PRINT-family pattern:
      - Optional raw literal text (not an expression).

    into:
      - <raw text> (optional, default ""): raw text, not an expression.
    plus, optionally, a note about empty text producing no output.
    """
    for i, line in enumerate(arg_lines):
        if line.strip() == "- Optional raw literal text (not an expression).":
            arg_lines[i] = '- `<raw text>` (optional, default `""`): raw text, not an expression.'
            if default_is_no_output:
                arg_lines.insert(i + 1, "- If the resulting text is empty, nothing is appended.")
            return True
    # Already rewritten or in a different shape.
    return False


def _merge_default_into_arg_bullet(arg_lines: list[str], name: str, default_text: str) -> bool:
    """
    Best-effort: find a bullet line that mentions the arg name and doesn't already
    contain 'default', then append a default note.
    """
    needle_backticked = f"`{name}`"
    needle_angle = f"<{name}>"
    for i, line in enumerate(arg_lines):
        if not line.startswith("- "):
            continue
        if "default" in line:
            continue
        if needle_backticked in line or needle_angle in line or line.startswith(f"- {name}"):
            arg_lines[i] = line.rstrip() + f" (default {default_text})"
            return True
    return False


def _apply_omitted_block_rewrites(path: Path, lines: list[str], arg_start: int, arg_end: int) -> tuple[bool, list[str]]:
    changed = False
    report: list[str] = []

    arg_lines = lines[arg_start:arg_end]
    blocks = _find_omitted_blocks(arg_lines)
    if not blocks:
        return False, report

    # Process from bottom to top to keep indices stable.
    for block in reversed(blocks):
        # Try to apply known merges before removing the block.
        for bullet in block.sub_bullets:
            b = bullet.strip()

            if b in {
                "- Omitted argument prints the empty string.",
                "- Omitted argument is treated as the empty string.",
                "- Omitted argument is treated as empty string.",
                "- If omitted, the argument is treated as the empty string.",
            }:
                if _rewrite_raw_optional_default(arg_lines, default_is_no_output=False):
                    changed = True
                continue

            if b in {
                "- Omitted argument is treated as the empty string, and therefore produces no output.",
                "- Omitted argument is treated as the empty string, and therefore produces no output segment.",
                "- If omitted, the argument is treated as the empty string; empty output produces no output segment.",
                "- Omitted argument is treated as the empty string, and therefore produces no output segment.",
                "- Omitted argument is treated as the empty string, and therefore produces no output.",
            }:
                if _rewrite_raw_optional_default(arg_lines, default_is_no_output=True):
                    changed = True
                continue

            m = re.match(r"^- `(?P<name>[^`]+)` defaults to `(?P<val>[^`]+)`\.$", b)
            if m:
                if _merge_default_into_arg_bullet(arg_lines, m.group("name"), f"`{m.group('val')}`"):
                    changed = True
                else:
                    report.append(f"{path}: could not merge default for {m.group('name')}")
                continue

            m = re.match(r"^- `<(?P<name>[^>]+)>` defaults to `(?P<val>[^`]+)`\.$", b)
            if m:
                if _merge_default_into_arg_bullet(arg_lines, m.group("name"), f"`{m.group('val')}`"):
                    changed = True
                else:
                    report.append(f"{path}: could not merge default for <{m.group('name')}>")
                continue

            if b.startswith("- If the expression is omitted, it defaults to `0`"):
                if _merge_default_into_arg_bullet(arg_lines, "<int expr>", "`0` (with a warning if omitted)"):
                    changed = True
                else:
                    # Common IF/WHILE/LOOP shape: update the first <int expr> bullet.
                    merged = False
                    for i, line in enumerate(arg_lines):
                        if line.startswith("- `<int expr>`") or line.startswith("- <int expr>") or line.startswith("- `<int expr>`:") or line.startswith("- <int expr>:") or "`<int expr>`" in line:
                            if "default" not in line:
                                arg_lines[i] = line.rstrip() + " (optional, default `0` with a warning if omitted)"
                                changed = True
                            merged = True
                            break
                    if not merged:
                        report.append(f"{path}: could not merge omitted-expression default")
                continue

            if b.startswith("- If omitted, the condition defaults to `0`"):
                # Similar to above.
                merged = False
                for i, line in enumerate(arg_lines):
                    if "<int expr>" in line and "default" not in line:
                        arg_lines[i] = line.rstrip() + " (optional, default `0` with a warning if omitted)"
                        changed = True
                        merged = True
                        break
                if not merged:
                    report.append(f"{path}: could not merge omitted-condition default")
                continue

            if b == "- If `<defaultFormString>` is omitted, there is no default value.":
                merged = False
                for i, line in enumerate(arg_lines):
                    if "<defaultFormString>" in line and "default" not in line:
                        arg_lines[i] = line.rstrip() + " (if omitted, there is no default value)"
                        changed = True
                        merged = True
                        break
                if not merged:
                    report.append(f"{path}: could not merge INPUTS defaultFormString omission note")
                continue

            if b == "- If `format` is omitted or `null`: uses the default `i.ToString()` formatting.":
                merged = False
                for i, line in enumerate(arg_lines):
                    if line.startswith("- `format`") and "omitted" not in line:
                        arg_lines[i] = line.rstrip() + " If omitted or `null`, uses default formatting."
                        changed = True
                        merged = True
                        break
                if not merged:
                    report.append(f"{path}: could not merge TOSTR format omission note")
                continue

            if b in {"- None (missing argument is an error).", "- None (missing arguments are an error).", "- N/A.", "- None (but see omitted-argument behavior above)."}:
                # Drop: either redundant or not useful in the sample style.
                continue

            if b.startswith("- Same as `") or b.startswith("- Depends on "):
                # Drop: these variants already refer to the base entry in their prose.
                continue

            # Unrecognized: keep the info by moving it into plain bullets (no heading).
            # This avoids data loss while still removing the "Omitted arguments / defaults:" mini-section.
            report.append(f"{path}: kept unmapped omitted-default bullet: {b}")
            arg_lines.insert(block.start, b)
            changed = True

        # Remove the omitted block lines.
        del arg_lines[block.start:block.end]
        changed = True

    # Light wording normalization inside Arguments.
    for i, line in enumerate(arg_lines):
        if line.startswith("- "):
            arg_lines[i] = _INT_EXPR_RE.sub("int", line)

    lines[arg_start:arg_end] = arg_lines
    return changed, report


def normalize_file(path: Path, *, write: bool) -> tuple[bool, list[str]]:
    text = _read_text(path)
    lines = text.splitlines()
    sections = _split_sections(lines)

    changed = False
    report: list[str] = []

    for title, start, end in sections:
        if title == "Arguments":
            ch, rep = _apply_omitted_block_rewrites(path, lines, start, end)
            changed |= ch
            report.extend(rep)

    new_text = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    if changed and write:
        _write_text(path, new_text)
    return changed, report


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="Do not write; exit non-zero if changes are needed.")
    ap.add_argument("--verbose", action="store_true", help="Print per-file reports.")
    args = ap.parse_args(argv)

    files = sorted([p for p in OVERRIDES_DIR.rglob("*.md") if p.is_file()])
    if not files:
        print(f"No override files found under {OVERRIDES_DIR}", file=sys.stderr)
        return 2

    any_change = False
    reports: list[str] = []
    changed_files: list[Path] = []

    for p in files:
        changed, report = normalize_file(p, write=not args.check)
        if changed:
            any_change = True
            changed_files.append(p)
        if report:
            reports.extend(str(r) for r in report)
            if args.verbose:
                for r in report:
                    print(r)

    if args.check:
        if any_change:
            print(f"Normalization needed for {len(changed_files)} file(s).", file=sys.stderr)
            return 1
        return 0

    print(f"Normalized {len(changed_files)} file(s).")
    if reports:
        print(f"Notes ({len(reports)}):")
        for r in reports:
            print(f"- {r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

