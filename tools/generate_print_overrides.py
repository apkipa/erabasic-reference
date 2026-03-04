#!/usr/bin/env python3
"""
Generate manual override snippets for the PRINT-family and PRINTDATA-family instructions.

These overrides are intentionally "manual" (written out in Markdown) so that:
  - `builtins-reference.md` stays self-contained and readable
  - `builtins-overrides/builtins-progress.md` can treat these entries as "covered"

The content here is based on direct engine-source reading (EvilMask/Emuera):
  - emuera.em/Emuera/Runtime/Script/Statements/Instraction.Child.cs (PRINT_Instruction / PRINT_DATA_Instruction)
  - emuera.em/Emuera/Runtime/Script/Statements/ArgumentBuilder.cs (STR / FORM / PRINTV / VAR_INT / VAR_STR)
  - emuera.em/Emuera/Runtime/Script/Loader/ErbLoader.cs (PRINTDATA / STRDATA / DATA / DATALIST nesting rules)
  - emuera.em/Emuera/UI/Game/EmueraConsole.Print.cs + PrintStringBuffer.cs (flush/lineEnd behavior)
  - emuera.em/Emuera/Runtime/Script/Statements/ExpressionMediator.cs (OutputToConsole / ConvertStringType / CheckEscape)

By default this script is conservative: it will NOT overwrite existing override files.
Use --force to overwrite.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import re


REPO_ROOT = Path(__file__).resolve().parents[2]
PATH_FUNCTION_IDENTIFIER = REPO_ROOT / "emuera.em/Emuera/Runtime/Script/Statements/FunctionIdentifier.cs"

INSTRUCTION_OVERRIDES_DIR = REPO_ROOT / "erabasic-reference/builtins-overrides/instructions"


_ADD_PRINT_RE = re.compile(r"\baddPrintFunction\s*\(\s*FunctionCode\.(?P<name>[A-Z0-9_]+)\s*\)")
_ADD_PRINTDATA_RE = re.compile(r"\baddPrintDataFunction\s*\(\s*FunctionCode\.(?P<name>[A-Z0-9_]+)\s*\)")


def _read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def _write_text(p: Path, s: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")


def _extract_print_keywords() -> tuple[list[str], list[str]]:
    text = _read_text(PATH_FUNCTION_IDENTIFIER)
    prints = sorted({m.group("name") for m in _ADD_PRINT_RE.finditer(text)})
    printdatas = sorted({m.group("name") for m in _ADD_PRINTDATA_RE.finditer(text)})
    return prints, printdatas


def _md_sections(sections: dict[str, list[str]]) -> str:
    out: list[str] = []
    for title in [
        "Summary",
        "Syntax",
        "Arguments",
        "Defaults / optional arguments",
        "Semantics",
        "Errors & validation",
        "Examples",
    ]:
        body = sections.get(title, [])
        if not body:
            continue
        out.append(f"**{title}**")
        out.extend(body)
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def _print_family_overview_bullets() -> list[str]:
    return [
        "- This engine implements many PRINT-like commands using a single internal implementation that is selected by the *instruction keyword*.",
        "- Suffix letters are part of the keyword (e.g. `PRINTFORMW`, `PRINTVKW`, `PRINTFORMSD`).",
        "- Keyword structure (conceptual; only some combinations exist as registered built-ins):",
        "  - `PRINT` + optional `SINGLE`",
        "  - then one of: `(none)` / `V` / `S` / `FORM` / `FORMS`",
        "  - then optional: `C` / `LC` (fixed-width cell output)",
        "  - then optional: `K` (kana conversion) / `D` (ignore `SETCOLOR` color)",
        "  - then optional: `N` (wait for key *without* ending the logical output line)",
        "  - then optional: `L` (newline) or `W` (newline + wait for key).",
    ]


def _sections_for_print_base(name: str) -> dict[str, list[str]]:
    # Detailed write-up lives on PRINT / PRINTDATA; variants refer to it.
    return {
        "Summary": [
            "- Prints a **raw literal string** (the remainder of the source line) into the console output buffer.",
            "- See also: `PRINTV` (variadic expressions), `PRINTS` (string expression), `PRINTFORM` (FORM scanned at load-time), `PRINTFORMS` (FORM scanned at runtime).",
            "- This entry also documents **common PRINT-family semantics** (suffix letters, buffering, `K`/`D`, `C`/`LC`).",
        ],
        "Syntax": [
            "- `PRINT`",
            "- `PRINT <raw text>`",
            "- `PRINT;<raw text>`",
        ],
        "Arguments": [
            "- `<raw text>` is **not an expression**. It is taken as the raw character sequence after the instruction delimiter.",
            "- The parser consumes exactly one delimiter character after the keyword:",
            "  - a single space / tab",
            "  - or a full-width space if `SystemAllowFullSpace` is enabled",
            "  - or a semicolon `;`",
            "- Because only *one* delimiter character is consumed:",
            "  - `PRINT X` prints `X` (the one space was consumed as delimiter).",
            "  - `PRINT  X` prints `\" X\"` (the second space remains in the argument).",
            "  - `PRINT;X` prints `X` (no leading whitespace in the argument).",
        ],
        "Defaults / optional arguments": [
            "- If omitted, the argument is treated as the empty string.",
        ],
        "Semantics": [
            "- Output is appended to the engine’s **print buffer** (it is not necessarily flushed to the UI immediately).",
            "- Common behavior across the PRINT family:",
            "  - `...L` variants: after output, flush and append a newline (`Console.NewLine()`).",
            "  - `...W` variants: like `...L`, then wait for a key (`Console.ReadAnyKey()`).",
            "  - `...N` variants: wait for a key **without ending the logical output line** (implementation detail: prints with `lineEnd=false` before flushing).",
            "  - `...K` variants: apply kana conversion to the produced string, as configured by `FORCEKANA` (`ConvertStringType`).",
            "  - `...D` variants: ignore `SETCOLOR`’s *color* for this output (still respects font style and font name).",
            "  - `...C` / `...LC` variants: output a fixed-width *cell* using `Config.PrintCLength`; width is measured in **Shift-JIS byte count** (implementation detail).",
            "- `PRINT` itself:",
            "  - Uses the raw literal argument as the output string.",
            "  - Treats the output as ending a logical line (`lineEnd=true`) even though it does not insert a newline by itself.",
        ],
        "Errors & validation": [
            "- None for `PRINT` itself (argument is optional and not parsed as an expression).",
        ],
        "Examples": [
            "- `PRINT Hello`",
            "- `PRINT;Hello`",
            "- `PRINT  (leading space is preserved)`",
        ],
    }


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

    syntax: list[str] = []
    args: list[str] = []
    defaults: list[str] = []
    semantics: list[str] = [see_print()]

    # Argument mode
    if shape.mode == "RAW":
        syntax = [f"- `{name} [<raw text>]`", f"- `{name};<raw text>`"]
        args = ["- Optional raw literal text (not an expression)."]
        defaults = ["- Omitted argument prints the empty string."]
    elif shape.mode == "V":
        syntax = [f"- `{name} <expr1> [, <expr2> ...]`"]
        args = [
            "- One or more comma-separated expressions (each may be int or string).",
            "- Each argument is evaluated; ints are converted with `ToString` and concatenated with no separator.",
        ]
        defaults = ["- None (missing arguments are an error)."]
        semantics.append("- Concatenates all arguments into a single output string, then prints it.")
    elif shape.mode == "S":
        syntax = [f"- `{name} <string expr>`"]
        args = ["- A single string expression (must be present)."]
        defaults = ["- None (missing argument is an error)."]
        semantics.append("- Evaluates the string expression and prints the result.")
    elif shape.mode == "FORM":
        syntax = [f"- `{name} [<FORM string>]`"]
        args = [
            "- A FORM/formatted string scanned to end-of-line (supports `%...%` and `{...}` placeholders, etc.).",
            "- The argument is optional for the `...FORM...` PRINT family (missing means empty string).",
        ]
        defaults = ["- Omitted argument prints the empty string."]
        semantics.append("- The formatted string is scanned at load/parse time and evaluated at runtime.")
    elif shape.mode == "FORMS":
        syntax = [f"- `{name} <string expr>`"]
        args = [
            "- A string expression (must be present).",
            "- The resulting string is then treated as a FORM/formatted string **at runtime**.",
        ]
        defaults = ["- None (missing argument is an error)."]
        semantics.extend(
            [
                "- Evaluates the string expression to produce a format-string source.",
                "- Applies escape normalization, scans it as a FORM string at runtime, and prints the evaluated result.",
            ]
        )
    else:
        raise ValueError(shape.mode)

    # Output shape modifiers
    if shape.is_single:
        semantics.extend(
            [
                "- Flushes any pending buffered output first, then prints as a **single display line** (`Console.PrintSingleLine`).",
                "- `PRINTSINGLE*` keywords are separate built-ins; they do not combine with the `...L`/`...W` suffix mechanism.",
            ]
        )

    if shape.align in {"C", "LC"}:
        args.extend(
            [
                "- Output is padded/truncated to a fixed-width cell (`Config.PrintCLength`) using Shift-JIS byte count (implementation detail).",
            ]
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

    return {
        "Summary": [
            f"- `{name}` is a PRINT-family variant.",
            see_print(),
        ],
        "Syntax": syntax,
        "Arguments": args,
        "Defaults / optional arguments": defaults,
        "Semantics": semantics,
        "Errors & validation": [
            "- Argument parsing/type-checking errors follow the underlying argument mode for this variant.",
        ],
        "Examples": [
            f"- `{name} ...`",
        ],
    }


def _sections_for_printdata_base() -> dict[str, list[str]]:
    return {
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
            "- Optional `<intVarTerm>`: a changeable int variable term that receives the 0-based chosen index.",
        ],
        "Defaults / optional arguments": [
            "- If `<intVarTerm>` is omitted, the chosen index is not stored anywhere.",
        ],
        "Semantics": [
            "- Load-time structure rules (enforced by the loader):",
            "  - `PRINTDATA*` must be closed by a matching `ENDDATA`.",
            "  - `DATA` / `DATAFORM` must appear inside `PRINTDATA*`, `STRDATA`, or inside a `DATALIST` that is itself inside one of those blocks.",
            "  - Nested `PRINTDATA*` blocks are rejected (warning/error).",
            "  - `STRDATA` cannot be nested inside `PRINTDATA*` and vice versa (warning/error).",
            "- Runtime behavior:",
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
            "- Errors/warnings for missing `ENDDATA`, `DATA` outside a block, `ENDLIST` without `DATALIST`, etc., are produced by the loader.",
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
    }


def _sections_for_printdata_variant(name: str) -> dict[str, list[str]]:
    ends_l = name.endswith("L")
    ends_w = name.endswith("W")
    rest = name[len("PRINTDATA") :] if name.startswith("PRINTDATA") else ""
    has_k = rest.startswith("K")
    has_d = rest.startswith("D")
    return {
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
        "Defaults / optional arguments": [
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
    }


def _sections_for_data_instructions(name: str) -> dict[str, list[str]]:
    if name == "DATA":
        return {
            "Summary": [
                "- Declares one printable choice inside a surrounding `PRINTDATA*` / `STRDATA` / `DATALIST` block.",
                "- `DATA` lines are *not* intended to execute as standalone statements; they are consumed by the loader into the surrounding block’s data list.",
            ],
            "Syntax": [
                "- `DATA [<raw text>]`",
                "- `DATA;<raw text>`",
            ],
            "Arguments": [
                "- Optional raw literal text (not an expression).",
            ],
            "Defaults / optional arguments": [
                "- Omitted argument is treated as empty string.",
            ],
            "Semantics": [
                "- At load time, the loader attaches `DATA` lines to the nearest surrounding block (`PRINTDATA*`, `STRDATA`, or `DATALIST`).",
                "- At runtime, `PRINTDATA*` / `STRDATA` evaluate the stored `DATA` line as a string and print/concatenate it when selected.",
            ],
            "Errors & validation": [
                "- Using `DATA` outside a valid surrounding block produces loader warnings/errors and the line will not participate in any `PRINTDATA*` / `STRDATA` selection.",
            ],
            "Examples": [
                "```erabasic",
                "PRINTDATA",
                "  DATA Hello",
                "  DATA;World",
                "ENDDATA",
                "```",
            ],
        }
    if name == "DATAFORM":
        return {
            "Summary": [
                "- Like `DATA`, but the text is a FORM/formatted string (scanned at load time).",
            ],
            "Syntax": [
                "- `DATAFORM [<FORM string>]`",
            ],
            "Arguments": [
                "- Optional FORM/formatted string scanned to end-of-line.",
            ],
            "Defaults / optional arguments": [
                "- Omitted argument is treated as empty string.",
            ],
            "Semantics": [
                "- Stored into the surrounding `PRINTDATA*` / `STRDATA` / `DATALIST` data list at load time.",
                "- When selected, evaluated to a string at runtime and printed/concatenated.",
            ],
            "Errors & validation": [
                "- Must appear inside a valid surrounding block, same as `DATA`.",
            ],
            "Examples": [
                "```erabasic",
                "PRINTDATA",
                "  DATAFORM Hello, %NAME%!",
                "ENDDATA",
                "```",
            ],
        }
    if name == "DATALIST":
        return {
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
            "Defaults / optional arguments": [
                "- N/A.",
            ],
            "Semantics": [
                "- At load time, the loader accumulates contained `DATA` / `DATAFORM` lines into a single list entry and attaches it to the surrounding `PRINTDATA*` / `STRDATA` block.",
            ],
            "Errors & validation": [
                "- `DATALIST` outside `PRINTDATA*` / `STRDATA` is rejected by the loader.",
                "- Missing `ENDLIST` produces loader diagnostics; an empty list produces a warning.",
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
        }
    if name == "ENDLIST":
        return {
            "Summary": [
                "- Closes a `DATALIST` block.",
            ],
            "Syntax": [
                "- `ENDLIST`",
            ],
            "Arguments": [
                "- None.",
            ],
            "Defaults / optional arguments": [
                "- N/A.",
            ],
            "Semantics": [
                "- Load-time only structural marker. At runtime it does nothing.",
            ],
            "Errors & validation": [
                "- `ENDLIST` without an open `DATALIST` produces loader diagnostics.",
            ],
            "Examples": [
                "- (See `DATALIST`.)",
            ],
        }
    if name == "ENDDATA":
        return {
            "Summary": [
                "- Closes a `PRINTDATA*` or `STRDATA` block.",
            ],
            "Syntax": [
                "- `ENDDATA`",
            ],
            "Arguments": [
                "- None.",
            ],
            "Defaults / optional arguments": [
                "- N/A.",
            ],
            "Semantics": [
                "- Load-time only structural marker. At runtime it does nothing.",
                "- The loader wires `PRINTDATA*` / `STRDATA` to jump here after printing/selection.",
            ],
            "Errors & validation": [
                "- `ENDDATA` without an open `PRINTDATA*` / `STRDATA` produces loader diagnostics.",
                "- Closing a block while a `DATALIST` is still open produces a loader diagnostic.",
            ],
            "Examples": [
                "- (See `PRINTDATA`.)",
            ],
        }
    if name == "STRDATA":
        return {
            "Summary": [
                "- Like `PRINTDATA`, but instead of printing, it selects a `DATA`/`DATAFORM` choice and concatenates it into a destination string variable.",
            ],
            "Syntax": [
                "- `STRDATA [<strVarTerm>]` ... `ENDDATA`",
            ],
            "Arguments": [
                "- Optional `<strVarTerm>`: changeable string variable term to receive the result.",
                "- If omitted, defaults to `RESULTS` (engine behavior).",
            ],
            "Defaults / optional arguments": [
                "- Destination defaults to `RESULTS` when omitted.",
            ],
            "Semantics": [
                "- Shares the same block structure as `PRINTDATA` (`DATA`, `DATAFORM`, `DATALIST`, `ENDDATA`).",
                "- Selects one entry uniformly at random.",
                "- Concatenates the selected lines with `\\n` between them (for `DATALIST` multi-line entries).",
                "- Stores the result into the destination variable and jumps to `ENDDATA`.",
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
        }
    raise ValueError(f"Unsupported DATA-block instruction: {name}")


def _maybe_write_override(name: str, sections: dict[str, list[str]], *, force: bool) -> bool:
    p = INSTRUCTION_OVERRIDES_DIR / f"{name}.md"
    if p.exists() and not force:
        return False
    _write_text(p, _md_sections(sections))
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="Overwrite existing override files.")
    args = ap.parse_args()

    print_keywords, printdata_keywords = _extract_print_keywords()

    created = 0
    updated = 0

    # PRINT family
    for kw in print_keywords:
        secs = _sections_for_print_base(kw) if kw == "PRINT" else _sections_for_print_variant(kw)
        path = INSTRUCTION_OVERRIDES_DIR / f"{kw}.md"
        existed = path.exists()
        wrote = _maybe_write_override(kw, secs, force=args.force)
        if wrote:
            if existed:
                updated += 1
            else:
                created += 1

    # PRINTDATA family
    for kw in printdata_keywords:
        secs = _sections_for_printdata_base() if kw == "PRINTDATA" else _sections_for_printdata_variant(kw)
        path = INSTRUCTION_OVERRIDES_DIR / f"{kw}.md"
        existed = path.exists()
        wrote = _maybe_write_override(kw, secs, force=args.force)
        if wrote:
            if existed:
                updated += 1
            else:
                created += 1

    # DATA-block structural instructions (not registered via addPrintFunction)
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
