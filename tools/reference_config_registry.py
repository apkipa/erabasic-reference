#!/usr/bin/env python3
"""Parse config-adjacent registries from `config-items.md`."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import re

import reference_common as ref_common


CONFIG_ITEMS_MD = ref_common.REFERENCE_ROOT / "config-items.md"

_TEXT_CACHE = ref_common.TextCache()
_lines = _TEXT_CACHE.lines


@dataclass(frozen=True)
class ConfigSurfaceReg:
    kind: str
    canonical_term: str
    accepted_classifiers: tuple[str, ...]
    implementation_names: tuple[str, ...]


_MAIN_CONFIG_ITEM_SECTION_RE = re.compile(r"^##\s+5\)\s+Main config items\b")
_DEBUG_CONFIG_ITEM_SECTION_RE = re.compile(r"^##\s+6\)\s+Debug config items\b")
_REPLACE_ITEM_SECTION_RE = re.compile(r"^##\s+7\)\s+Replace items\b")
_DERIVED_SECTION_RE = re.compile(r"^##\s+8\)\s+Shared derived runtime values\b")
_LEVEL2_SECTION_RE = re.compile(r"^##\s+")
_CODE_SPAN_RE = re.compile(r"`([^`]+)`")
_TABLE_SEPARATOR_RE = re.compile(r"^:?-{3,}:?$")


def _split_md_table_row(raw: str) -> list[str] | None:
    stripped = raw.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        return None
    return [cell.strip() for cell in stripped.strip("|").split("|")]


def _config_item_section_meta(raw: str) -> tuple[str, tuple[str, ...]] | None:
    if _MAIN_CONFIG_ITEM_SECTION_RE.match(raw):
        return ("config item", ())
    if _DEBUG_CONFIG_ITEM_SECTION_RE.match(raw):
        return ("debug item", ("debug item",))
    if _REPLACE_ITEM_SECTION_RE.match(raw):
        return ("replace item", ("replace item",))
    return None


def _accepted_classifiers_for_main_config_item(canonical_term: str) -> tuple[str, ...]:
    heads = ["config item", "config option", "config key"]
    if canonical_term.startswith("Compati"):
        heads.append("compatibility config item")
    return tuple(heads)


def _parse_config_item_regs(lines: list[str]) -> list[ConfigSurfaceReg]:
    in_section = False
    section_meta: tuple[str, tuple[str, ...]] | None = None
    regs: list[ConfigSurfaceReg] = []
    for raw in lines:
        if not in_section:
            section_meta = _config_item_section_meta(raw)
            if section_meta is not None:
                in_section = True
            continue
        if _LEVEL2_SECTION_RE.match(raw):
            if _DERIVED_SECTION_RE.match(raw):
                break
            section_meta = _config_item_section_meta(raw)
            in_section = section_meta is not None
            continue
        if not in_section:
            continue
        cells = _split_md_table_row(raw)
        if not cells or len(cells) < 1:
            continue
        if cells[0].lower() == "code":
            continue
        if all(_TABLE_SEPARATOR_RE.fullmatch(cell.replace(" ", "")) for cell in cells):
            continue
        code_spans = _CODE_SPAN_RE.findall(cells[0])
        if not code_spans:
            continue
        canonical_term = code_spans[0]
        kind, accepted_classifiers = section_meta or ("config item", ("config item",))
        if kind == "config item":
            accepted_classifiers = _accepted_classifiers_for_main_config_item(canonical_term)
        regs.append(
            ConfigSurfaceReg(
                kind=kind,
                canonical_term=canonical_term,
                accepted_classifiers=accepted_classifiers,
                implementation_names=(f"Config.{canonical_term}",),
            )
        )
    return regs


def _parse_derived_runtime_value_regs(lines: list[str]) -> list[ConfigSurfaceReg]:
    in_section = False
    regs: list[ConfigSurfaceReg] = []
    for raw in lines:
        if not in_section:
            if _DERIVED_SECTION_RE.match(raw):
                in_section = True
            continue
        if _LEVEL2_SECTION_RE.match(raw):
            break
        cells = _split_md_table_row(raw)
        if not cells or len(cells) < 3:
            continue
        if cells[0].lower() == "canonical spec term":
            continue
        if all(_TABLE_SEPARATOR_RE.fullmatch(cell.replace(" ", "")) for cell in cells):
            continue
        canonical_terms = _CODE_SPAN_RE.findall(cells[0])
        implementation_names = tuple(_CODE_SPAN_RE.findall(cells[2]))
        if not canonical_terms or not implementation_names:
            continue
        regs.append(
            ConfigSurfaceReg(
                kind="derived runtime value",
                canonical_term=canonical_terms[0],
                accepted_classifiers=("derived runtime value",),
                implementation_names=implementation_names,
            )
        )
    return regs


@lru_cache(maxsize=1)
def load_config_surface_regs() -> tuple[ConfigSurfaceReg, ...]:
    lines = _lines(CONFIG_ITEMS_MD)
    regs = _parse_config_item_regs(lines)
    regs.extend(_parse_derived_runtime_value_regs(lines))
    return tuple(regs)
