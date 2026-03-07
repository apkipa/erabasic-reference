#!/usr/bin/env python3
"""
Generate current-schema override files for the PRINT / PRINTDATA / DATA families.

This is a repo-local maintenance/bootstrap tool for authored override docs under
`builtins-overrides/instructions/`.

Properties:
- Emits the current instruction section schema used by `reference_lint.py`
- Preserves the repo's conservative default: existing files are left untouched
  unless `--force` is passed
- Keeps the PRINT / PRINTDATA / DATA family material in one place so it can be
  regenerated without hand-editing dozens of near-mechanical variants
"""

from __future__ import annotations

from dataclasses import dataclass
import argparse
import re

import reference_common as ref_common
import reference_engine_registry as ref_engine
import reference_lint as ref_lint


PATH_FUNCTION_IDENTIFIER = ref_engine.PATH_FUNCTION_IDENTIFIER
INSTRUCTION_OVERRIDES_DIR = ref_common.INSTRUCTION_OVERRIDES_DIR

SECTION_ORDER = [*ref_lint.USER_INSTRUCTION_SECTIONS, "Progress state"]

_ADD_PRINT_RE = re.compile(r"\baddPrintFunction\s*\(\s*FunctionCode\.(?P<name>[A-Z0-9_]+)\s*\)")
_ADD_PRINTDATA_RE = re.compile(r"\baddPrintDataFunction\s*\(\s*FunctionCode\.(?P<name>[A-Z0-9_]+)\s*\)")


_read_text = ref_common.read_text
_write_text = ref_common.write_text


def _extract_print_keywords() -> tuple[list[str], list[str]]:
    text = _read_text(PATH_FUNCTION_IDENTIFIER)
    prints = sorted({m.group("name") for m in _ADD_PRINT_RE.finditer(text)})
    printdatas = sorted({m.group("name") for m in _ADD_PRINTDATA_RE.finditer(text)})
    return prints, printdatas


def _render_sections(sections: dict[str, list[str]]) -> str:
    out: list[str] = []
    for title in SECTION_ORDER:
        body = sections.get(title, [])
        if not body:
            continue
        out.append(f"**{title}**")
        out.extend(body)
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def _with_common_metadata(name: str, sections: dict[str, list[str]]) -> dict[str, list[str]]:
    out = {title: list(body) for title, body in sections.items()}
    if name.startswith("PRINTDATA"):
        tags = ["io", "data-blocks"]
    elif name.startswith("PRINT"):
        tags = ["io"]
    else:
        tags = ["data-blocks"]
    out.setdefault("Tags", [f"- {tag}" for tag in tags])
    out.setdefault("Progress state", ["- complete"])
    return out


def _sections_for_print_base(name: str) -> dict[str, list[str]]:
    return _with_common_metadata(
        name,
        {
            "Summary": [
                "- Prints a **raw literal string** (the remainder of the source line) into the console output buffer.",
                "- This entry also documents **common PRINT-family semantics** (suffix letters, buffering, `K`/`D`, `C`/`LC`).",
            ],
            "Syntax": [
                "- `PRINT`",
                "- `PRINT <raw text>`",
                "- `PRINT;<raw text>`",
            ],
            "Arguments": [
                '- `<raw text>` (optional, default `""`): raw text, not an expression.',
                "- `<raw text>` is taken as the raw character sequence after the instruction delimiter.",
                "- The parser consumes exactly one delimiter character after the keyword:",
                "  - a single space / tab",
                "  - or a full-width space if `SystemAllowFullSpace` is enabled",
                "  - or a semicolon `;`",
                "- Because only *one* delimiter character is consumed:",
                "  - `PRINT X` prints `X` (the one space was consumed as delimiter).",
                '  - `PRINT  X` prints `" X"` (the second space remains in the argument).',
                "  - `PRINT;X` prints `X` (no leading whitespace in the argument).",
            ],
            "Semantics": [
                "- Output is appended to the engine’s **pending print buffer**; see `output-flow.md` for the shared layer model.",
                "- Appending buffered `PRINT*` output does **not** immediately create a visible display-line entry.",
                "- If output skipping is active (`SKIPDISP`):",
                "  - these instructions are skipped before execution by the interpreter,",
                "  - arguments are not evaluated and there are no side effects.",
                "- Argument/evaluation modes by base variant (before suffix letters):",
                "  - `PRINT*` (raw): uses the raw literal remainder-of-line (not an expression).",
                "  - `PRINTS*`: evaluates one string expression.",
                "  - `PRINTV*`: evaluates a comma-separated list of expressions; each element must be either integer or string; results are concatenated with no separator (left-to-right).",
                "  - `PRINTFORM*`: parses its argument as a FORM/formatted string at load/parse time, then evaluates it at runtime.",
                "  - `PRINTFORMS*`: evaluates one string expression to obtain a format-string source, then parses and evaluates it as a FORM string at runtime (see below).",
                "- Suffix letters and their meaning (parser order is important):",
                "  - `C` / `LC` (cell output): after building the output string, outputs a fixed-width cell.",
                "    - `...C` uses right alignment, `...LC` uses left alignment.",
                "    - This is **not** the same as the newline suffix `L`; for example, `PRINTLC` means “left-aligned cell”, not “PRINTL + C”.",
                "    - Cell formatting rules are defined by the console implementation; see `PRINTC` / `PRINTLC`.",
                "    - Cell variants do not use the `...L / ...W / ...N` newline/wait handling; they only append a cell to the buffer.",
                "  - `K` (kana conversion): applies kana conversion as configured by `FORCEKANA`.",
                "  - `D` (ignore `SETCOLOR` color): ignores `SETCOLOR`’s *color* for this output (font name/style still apply).",
                "  - `L` (line end): after printing, flushes the current buffer as visible output and ends the logical line.",
                "  - `W` (line end + wait): like `L`, then waits for a key.",
                "  - `N` (flush + wait without line end): flushes current buffered content to visible output, then waits **without** ending the logical line.",
                "    - the next later flush is merged into the same logical line.",
                "- FORM-at-runtime behavior (`PRINTFORMS*`):",
                "  - evaluates the string expression to `src`,",
                "  - normalizes escapes using the FORM escape rules,",
                "  - parses `src` as a FORM string up to end-of-line,",
                "  - evaluates it and prints the result.",
                "- `PRINT` itself:",
                "  - uses the raw literal argument as the output string,",
                "  - appends it with `lineEnd = true`, so when the buffer is later flushed it belongs to a logical line that ends at that point.",
                "- Buffer/temporary-line boundary:",
                "  - appending `PRINT*` content to the pending print buffer does not by itself remove a trailing temporary line,",
                "  - the temporary line is only replaced when later visible output is actually appended.",
            ],
            "Errors & validation": [
                "- None for `PRINT` itself (argument is optional and not parsed as an expression).",
            ],
            "Examples": [
                "- `PRINT Hello`",
                "- `PRINT;Hello`",
                "- `PRINT  (leading space is preserved)`",
            ],
        },
    )


def _sections_for_print_variant(name: str) -> dict[str, list[str]]:
    def see_print() -> str:
        return "- See `PRINT` for shared PRINT-family rules (delimiter handling, buffering, suffix semantics)."

    @dataclass(frozen=True)
    class PrintShape:
        is_single: bool
        mode: str  # RAW / V / S / FORM / FORMS
        align: str  # NONE / C / LC
        has_k: bool
        has_d: bool
        has_n: bool
        suffix: str  # NONE / L / W

    def parse_keyword(kw: str) -> PrintShape:
        if not kw.startswith("PRINT"):
            raise ValueError(kw)
        rest = kw[len("PRINT") :]

        is_single = False
        if rest.startswith("SINGLE"):
            is_single = True
            rest = rest[len("SINGLE") :]

        mode = "RAW"
        if rest.startswith("FORMS"):
            mode = "FORMS"
            rest = rest[len("FORMS") :]
        elif rest.startswith("FORM"):
            mode = "FORM"
            rest = rest[len("FORM") :]
        elif rest.startswith("V"):
            mode = "V"
            rest = rest[len("V") :]
        elif rest.startswith("S"):
            mode = "S"
            rest = rest[len("S") :]

        align = "NONE"
        if rest.startswith("LC"):
            align = "LC"
            rest = rest[len("LC") :]
        elif rest.startswith("C"):
            align = "C"
            rest = rest[len("C") :]

        has_k = False
        if rest.startswith("K"):
            has_k = True
            rest = rest[len("K") :]

        has_d = False
        if rest.startswith("D"):
            has_d = True
            rest = rest[len("D") :]

        has_n = False
        if rest.startswith("N"):
            has_n = True
            rest = rest[len("N") :]

        suffix = "NONE"
        if rest == "L":
            suffix = "L"
            rest = ""
        elif rest == "W":
            suffix = "W"
            rest = ""
        elif rest != "":
            raise ValueError(f"Unparsed PRINT keyword tail: {kw} -> {rest!r}")

        return PrintShape(
            is_single=is_single,
            mode=mode,
            align=align,
            has_k=has_k,
            has_d=has_d,
            has_n=has_n,
            suffix=suffix,
        )

    shape = parse_keyword(name)

    if shape.mode == "RAW":
        syntax = [f"- `{name} [<raw text>]`", f"- `{name};<raw text>`"]
        arguments = [
            '- `<raw text>` (optional, default `""`): raw literal text, not an expression.',
        ]
    elif shape.mode == "V":
        syntax = [f"- `{name} <expr1> [, <expr2> ...]`"]
        arguments = [
            "- One or more comma-separated expressions (each may be int or string).",
            "- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.",
        ]
    elif shape.mode == "S":
        syntax = [f"- `{name} <string expr>`"]
        arguments = [
            "- A single string expression (must be present).",
        ]
    elif shape.mode == "FORM":
        syntax = [f"- `{name} [<FORM string>]`"]
        arguments = [
            "- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).",
            "- The argument is optional for the `...FORM...` PRINT family (missing means empty string).",
        ]
    elif shape.mode == "FORMS":
        syntax = [f"- `{name} <string expr>`"]
        arguments = [
            "- A string expression (must be present).",
            "- The resulting string is then treated as a FORM/formatted string **at runtime**.",
        ]
    else:
        raise ValueError(shape.mode)

    semantics: list[str] = [see_print()]
    if shape.mode == "V":
        semantics.append("- Concatenates all arguments into a single output string, then prints it.")
    elif shape.mode == "S":
        semantics.append("- Evaluates the string expression and prints the result.")
    elif shape.mode == "FORM":
        semantics.append("- The formatted string is scanned at load/parse time and evaluated at runtime.")
    elif shape.mode == "FORMS":
        semantics.extend(
            [
                "- Evaluates the string expression to produce a format-string source.",
                "- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.",
            ]
        )

    if shape.is_single:
        semantics.extend(
            [
                "- If the produced output string is empty, this instruction does nothing.",
                "- Otherwise, flushes any pending buffered output first, then prints as a **single display line**.",
                "- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.",
            ]
        )

    if shape.align in {"C", "LC"}:
        arguments.append(
            "- Output is padded/truncated to a fixed-width cell (`Config.PrintCLength`) using Shift-JIS byte count (implementation detail)."
        )
        semantics.append("- Writes a fixed-width cell; does not append a newline and does not flush immediately.")
        semantics.append("- Alignment: `...C` right-aligns; `...LC` left-aligns (implementation detail).")

    if shape.has_k:
        if shape.align != "NONE":
            semantics.append("- Applies kana conversion (`FORCEKANA` state) before writing the cell.")
        else:
            semantics.append("- Applies kana conversion (`FORCEKANA` state) before printing.")

    if shape.has_d:
        semantics.append("- Ignores `SETCOLOR`’s color for this output (`PRINTD`-style behavior).")

    if shape.has_n:
        semantics.append("- Waits for a key **without** ending the logical output line (see `PRINT`).")

    if shape.suffix == "L":
        semantics.append("- After printing, flushes and appends a newline.")
    elif shape.suffix == "W":
        semantics.append("- After printing, flushes and appends a newline, then waits for a key.")

    return _with_common_metadata(
        name,
        {
            "Summary": [
                f"- `{name}` is a PRINT-family variant.",
                see_print(),
            ],
            "Syntax": syntax,
            "Arguments": arguments,
            "Semantics": semantics,
            "Errors & validation": [
                "- Argument parsing/type-checking errors follow the underlying argument mode for this variant.",
            ],
            "Examples": [
                f"- `{name} ...`",
            ],
        },
    )


def _sections_for_printdata_base() -> dict[str, list[str]]:
    return _with_common_metadata(
        "PRINTDATA",
        {
            "Summary": [
                "- Begins a **PRINTDATA block** that contains `DATA` / `DATAFORM` (and optional `DATALIST` groups).",
                "- At runtime, the engine picks one choice uniformly at random, prints it, then jumps to `ENDDATA`.",
            ],
            "Syntax": [
                "- `PRINTDATA [<intVarTerm>]`",
                "- Block form:",
                "  - `PRINTDATA [<intVarTerm>]`",
                "    - `DATA <raw text>` / `DATAFORM <FORM string>` (one or more choices)",
                "    - optionally, `DATALIST` ... `ENDLIST` groups to make a multi-line choice",
                "  - `ENDDATA`",
            ],
            "Arguments": [
                "- `<intVarTerm>` (optional, changeable int variable term): receives the 0-based chosen index.",
            ],
            "Semantics": [
                "- Load-time structure rules (enforced by the loader):",
                "  - `PRINTDATA*` must be closed by a matching `ENDDATA`.",
                "  - `DATA` / `DATAFORM` must appear inside `PRINTDATA*`, `STRDATA`, or inside a `DATALIST` that is itself inside one of those blocks.",
                "  - Nested `PRINTDATA*` blocks are a load-time error (the line is marked as error).",
                "  - `STRDATA` cannot be nested inside `PRINTDATA*` and vice versa (load-time error).",
                "  - The block body only permits `DATA` / `DATAFORM` / `DATALIST` / `ENDLIST` / `ENDDATA`; any other instruction (and any label definition) inside is a load-time error.",
                "- Runtime behavior:",
                "  - If output skipping is active (via `SKIPDISP`), `PRINTDATA*` is skipped entirely (no selection, no assignment to `<intVarTerm>`, and no jump to `ENDDATA`), so control flows through the block lines normally.",
                "  - If there are no `DATA` choices, nothing is printed and the engine jumps to `ENDDATA`.",
                "  - Otherwise:",
                "    - Choose `choice` uniformly such that `0 <= choice < count` (using the engine RNG).",
                "    - If `<intVarTerm>` is present, assign it the chosen index.",
                "    - Print the selected `DATA` entry:",
                "      - A single `DATA`/`DATAFORM` line prints as one line.",
                "      - A `DATALIST` entry prints each contained `DATA`/`DATAFORM` line separated by newlines.",
                "    - If the keyword has `...L`/`...W` behavior, append a newline (and optionally wait for a key).",
                "    - Jump to the `ENDDATA` line, skipping over the block body.",
            ],
            "Errors & validation": [
                "- Load-time structure errors (the line is marked as error) are produced for missing `ENDDATA`, `DATA` outside a block, `ENDLIST` without `DATALIST`, invalid instructions inside the block, etc.",
                "- Non-fatal loader warnings also exist (e.g. empty choice lists), but the block still loads.",
                "- The optional `<intVarTerm>` must be a changeable int variable term.",
            ],
            "Examples": [
                "```erabasic",
                "PRINTDATA CHOICE",
                "  DATA First option",
                "  DATA Second option",
                "ENDDATA",
                "```",
                "",
                "```erabasic",
                "PRINTDATA",
                "  DATALIST",
                "    DATA Line 1",
                "    DATAFORM Line 2: %TOSTR(RAND:100)%",
                "  ENDLIST",
                "ENDDATA",
                "```",
            ],
        },
    )


def _sections_for_printdata_variant(name: str) -> dict[str, list[str]]:
    ends_l = name.endswith("L")
    ends_w = name.endswith("W")
    rest = name[len("PRINTDATA") :] if name.startswith("PRINTDATA") else ""
    has_k = rest.startswith("K")
    has_d = rest.startswith("D")
    return _with_common_metadata(
        name,
        {
            "Summary": [
                f"- `{name}` is a `PRINTDATA`-family block instruction.",
                "- See `PRINTDATA` for the full block model and structure rules.",
            ],
            "Syntax": [
                f"- `{name} [<intVarTerm>]` ... `ENDDATA`",
            ],
            "Arguments": [
                "- Same as `PRINTDATA`.",
            ],
            "Semantics": [
                "- Same as `PRINTDATA`, with these differences:",
                ("  - Applies kana conversion (`...K`) before printing." if has_k else "  - (No kana conversion flag.)"),
                ("  - Ignores `SETCOLOR`’s color (`...D`) for this output." if has_d else "  - (Honors `SETCOLOR` color.)"),
                ("  - Appends a newline after printing (`...L`)." if ends_l else "  - (No automatic newline suffix.)"),
                ("  - Appends a newline and waits for a key (`...W`)." if ends_w else "  - (No automatic wait suffix.)"),
            ],
            "Errors & validation": [
                "- Same as `PRINTDATA`.",
            ],
            "Examples": [
                f"- `{name} CHOICE` ... `ENDDATA`",
            ],
        },
    )


def _sections_for_data_instructions(name: str) -> dict[str, list[str]]:
    if name == "DATA":
        return _with_common_metadata(
            name,
            {
                "Summary": [
                    "- Declares one printable choice inside a surrounding `PRINTDATA*` / `STRDATA` / `DATALIST` block.",
                    "- `DATA` lines are *not* intended to execute as standalone statements; they are consumed by the loader into the surrounding block’s data list.",
                ],
                "Syntax": [
                    "- `DATA [<raw text>]`",
                    "- `DATA;<raw text>`",
                ],
                "Arguments": [
                    '- `<raw text>` (optional, default `""`): raw text, not an expression.',
                    "- Parsing detail: as with most instructions, Emuera consumes exactly one delimiter character after the keyword (space/tab/full-width-space if enabled, or `;`). The remainder of the line becomes the raw text.",
                ],
                "Semantics": [
                    "- At load time, the loader attaches `DATA` lines to the nearest surrounding block (`PRINTDATA*`, `STRDATA`, or `DATALIST`).",
                    "- At runtime, `PRINTDATA*` / `STRDATA` evaluate the stored `DATA` line as a string and print/concatenate it when selected.",
                ],
                "Errors & validation": [
                    "- Using `DATA` outside a valid surrounding block is a load-time error (the line is marked as error) and it will not participate in any `PRINTDATA*` / `STRDATA` selection.",
                ],
                "Examples": [
                    "```erabasic",
                    "PRINTDATA",
                    "  DATA Hello",
                    "  DATA;World",
                    "ENDDATA",
                    "```",
                ],
            },
        )
    if name == "DATAFORM":
        return _with_common_metadata(
            name,
            {
                "Summary": [
                    "- Like `DATA`, but the text is a FORM/formatted string (scanned at load time).",
                ],
                "Syntax": [
                    "- `DATAFORM [<FORM string>]`",
                ],
                "Arguments": [
                    '- `<FORM string>` (optional, default `""`): FORM/formatted string scanned to end-of-line.',
                ],
                "Semantics": [
                    "- Stored into the surrounding `PRINTDATA*` / `STRDATA` / `DATALIST` data list at load time.",
                    "- When selected, evaluated to a string at runtime and printed/concatenated.",
                    "  - The FORM string is scanned at load time and stored as an expression that is evaluated later (so it can still depend on runtime variables).",
                ],
                "Errors & validation": [
                    "- Must appear inside a valid surrounding block; otherwise it is a load-time error (the line is marked as error).",
                ],
                "Examples": [
                    "```erabasic",
                    "PRINTDATA",
                    "  DATAFORM Hello, %NAME%!",
                    "ENDDATA",
                    "```",
                ],
            },
        )
    if name == "DATALIST":
        return _with_common_metadata(
            name,
            {
                "Summary": [
                    "- Starts a **multi-line** choice list inside a surrounding `PRINTDATA*` or `STRDATA` block.",
                    "- Each `DATA` / `DATAFORM` inside the list becomes a separate output line when this choice is selected.",
                ],
                "Syntax": [
                    "- `DATALIST`",
                    "  - `DATA ...` / `DATAFORM ...` (one or more)",
                    "- `ENDLIST`",
                ],
                "Arguments": [
                    "- None.",
                ],
                "Semantics": [
                    "- At load time, the loader accumulates contained `DATA` / `DATAFORM` lines into a single list entry and attaches it to the surrounding `PRINTDATA*` / `STRDATA` block.",
                ],
                "Errors & validation": [
                    "- `DATALIST` must appear inside `PRINTDATA*` or `STRDATA`; otherwise it is a load-time error (the line is marked as error).",
                    "- Missing `ENDLIST` produces a load-time error at end of file/load.",
                    "- An empty list produces a non-fatal loader warning, but still creates an empty choice entry.",
                ],
                "Examples": [
                    "```erabasic",
                    "PRINTDATA",
                    "  DATALIST",
                    "    DATA Line 1",
                    "    DATA Line 2",
                    "  ENDLIST",
                    "ENDDATA",
                    "```",
                ],
            },
        )
    if name == "ENDLIST":
        return _with_common_metadata(
            name,
            {
                "Summary": [
                    "- Closes a `DATALIST` block.",
                ],
                "Syntax": [
                    "- `ENDLIST`",
                ],
                "Arguments": [
                    "- None.",
                ],
                "Semantics": [
                    "- Load-time only structural marker. At runtime it does nothing.",
                ],
                "Errors & validation": [
                    "- `ENDLIST` without an open `DATALIST` is a load-time error (the line is marked as error).",
                ],
                "Examples": [
                    "- (See `DATALIST`.)",
                ],
            },
        )
    if name == "ENDDATA":
        return _with_common_metadata(
            name,
            {
                "Summary": [
                    "- Closes a `PRINTDATA*` or `STRDATA` block.",
                ],
                "Syntax": [
                    "- `ENDDATA`",
                ],
                "Arguments": [
                    "- None.",
                ],
                "Semantics": [
                    "- Load-time only structural marker. At runtime it does nothing.",
                    "- The loader wires `PRINTDATA*` / `STRDATA` to jump here after printing/selection.",
                ],
                "Errors & validation": [
                    "- `ENDDATA` without an open `PRINTDATA*` / `STRDATA` is a load-time error (the line is marked as error).",
                    "- Closing a block while a `DATALIST` is still open is a load-time error.",
                ],
                "Examples": [
                    "- (See `PRINTDATA`.)",
                ],
            },
        )
    if name == "STRDATA":
        return _with_common_metadata(
            name,
            {
                "Summary": [
                    "- Like `PRINTDATA`, but instead of printing, it selects a `DATA`/`DATAFORM` choice and concatenates it into a destination string variable.",
                ],
                "Syntax": [
                    "- `STRDATA [<strVarTerm>]` ... `ENDDATA`",
                ],
                "Arguments": [
                    "- `<strVarTerm>` (optional; default `RESULTS`): changeable string variable term to receive the result.",
                ],
                "Semantics": [
                    "- Shares the same block structure as `PRINTDATA` (`DATA`, `DATAFORM`, `DATALIST`, `ENDDATA`).",
                    "- Selects one entry uniformly at random.",
                    "- Concatenates the selected lines with `\\n` between them (for `DATALIST` multi-line entries).",
                    "- Stores the result into the destination variable and jumps to `ENDDATA`.",
                    "- If the block contains no `DATA`/`DATAFORM` choices at all, it simply jumps to `ENDDATA` and does **not** assign anything to the destination variable (it remains unchanged).",
                ],
                "Errors & validation": [
                    "- The destination must be a changeable string variable term.",
                    "- Same structural diagnostics as `PRINTDATA`.",
                ],
                "Examples": [
                    "```erabasic",
                    "STRDATA",
                    "  DATA Hello",
                    "  DATA World",
                    "ENDDATA",
                    "PRINTFORML RESULTS",
                    "```",
                ],
            },
        )
    raise ValueError(f"Unsupported DATA-block instruction: {name}")


def _maybe_write_override(name: str, sections: dict[str, list[str]], *, force: bool) -> bool:
    path = INSTRUCTION_OVERRIDES_DIR / f"{name}.md"
    if path.exists() and not force:
        return False
    _write_text(path, _render_sections(sections))
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate PRINT / PRINTDATA / DATA family override files.")
    ap.add_argument("--force", action="store_true", help="Overwrite existing override files.")
    args = ap.parse_args()

    print_keywords, printdata_keywords = _extract_print_keywords()

    created = 0
    updated = 0

    for kw in print_keywords:
        sections = _sections_for_print_base(kw) if kw == "PRINT" else _sections_for_print_variant(kw)
        path = INSTRUCTION_OVERRIDES_DIR / f"{kw}.md"
        existed = path.exists()
        wrote = _maybe_write_override(kw, sections, force=args.force)
        if wrote:
            if existed:
                updated += 1
            else:
                created += 1

    for kw in printdata_keywords:
        sections = _sections_for_printdata_base() if kw == "PRINTDATA" else _sections_for_printdata_variant(kw)
        path = INSTRUCTION_OVERRIDES_DIR / f"{kw}.md"
        existed = path.exists()
        wrote = _maybe_write_override(kw, sections, force=args.force)
        if wrote:
            if existed:
                updated += 1
            else:
                created += 1

    for kw in ["DATA", "DATAFORM", "DATALIST", "ENDLIST", "ENDDATA", "STRDATA"]:
        path = INSTRUCTION_OVERRIDES_DIR / f"{kw}.md"
        existed = path.exists()
        wrote = _maybe_write_override(kw, _sections_for_data_instructions(kw), force=args.force)
        if wrote:
            if existed:
                updated += 1
            else:
                created += 1

    print(f"Wrote overrides: created={created}, updated={updated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
