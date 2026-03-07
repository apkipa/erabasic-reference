#!/usr/bin/env python3
"""Shared paths and small utility helpers for `erabasic-reference/tools`."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable
import re


MONOREPO_ROOT = Path(__file__).resolve().parents[2]
REFERENCE_ROOT = Path(__file__).resolve().parents[1]
OVERRIDES_DIR = REFERENCE_ROOT / "builtins-overrides"
INSTRUCTION_OVERRIDES_DIR = OVERRIDES_DIR / "instructions"
METHOD_OVERRIDES_DIR = OVERRIDES_DIR / "methods"
OUTPUT_MD = REFERENCE_ROOT / "builtins-reference.md"
OUTPUT_ENGINE_MD = REFERENCE_ROOT / "appendix/tooling/builtins-reference-engine.md"
OUTPUT_INDEX_MD = REFERENCE_ROOT / "builtins-index.md"
OUTPUT_PROGRESS_MD = OVERRIDES_DIR / "builtins-progress.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def lines(path: Path) -> list[str]:
    return read_text(path).splitlines()


def strip_csharp_comment(text: str) -> str:
    return text.split("//", 1)[0].rstrip()


def split_flags(expr: str) -> list[str]:
    if not expr:
        return []
    expr = expr.replace("(", " ").replace(")", " ")
    expr = expr.replace(";", " ")
    parts: list[str] = []
    for part in expr.split("|"):
        token = part.strip()
        if token:
            parts.append(token)
    return parts


def format_flags(flags: Iterable[str]) -> str:
    values = [flag for flag in flags if flag]
    if not values:
        return "(none)"
    return ", ".join(f"`{flag}`" for flag in values)


def md_anchor(text: str) -> str:
    value = text.strip().lower()
    value = re.sub(r"[^a-z0-9 _-]+", "", value)
    value = value.replace(" ", "-")
    value = re.sub(r"-{2,}", "-", value)
    return value


def best_effort_translate_argtype_hint(jp: str) -> str:
    text = jp.strip()
    if not text:
        return ""
    replacements = [
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
    for old, new in replacements:
        text = text.replace(old, new)
    text = text.replace("（", "(").replace("）", ")").replace("，", ",").replace("・", " / ")
    text = text.replace("、", ", ")
    return text


