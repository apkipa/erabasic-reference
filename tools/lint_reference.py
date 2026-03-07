#!/usr/bin/env python3
from __future__ import annotations

import argparse

import reference_lint as ref_lint
import reference_engine_registry as ref_engine


def _load_regs():
    return ref_engine.load_regs_for_lint()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Lint EraBasic reference authored docs without regenerating outputs.")
    ap.add_argument("--report", action="store_true", help="Print a detailed validation report to stderr.")
    ap.add_argument("--no-fail", action="store_true", help="Do not exit non-zero on validation issues.")
    ap.add_argument(
        "--only",
        choices=["all", "overrides", "topics"],
        default="all",
        help="Restrict linting to override entries, topic docs, or both.",
    )
    ap.add_argument(
        "--fail-on",
        action="append",
        default=[],
        choices=ref_lint.FAIL_ON_CODES,
        help="Exit non-zero if any matching validation issue exists (can be repeated).",
    )
    args = ap.parse_args(argv)

    issues = []
    if args.only in ("all", "overrides"):
        instr_regs, method_regs = _load_regs()
        issues.extend(ref_lint.validate_builtins_overrides(instr_regs, method_regs))
    if args.only in ("all", "topics"):
        issues.extend(ref_lint.validate_topic_docs())

    ref_lint.print_validation_report(issues, verbose=args.report)

    if not issues or args.no_fail:
        return 0
    if args.fail_on:
        wanted = set(args.fail_on)
        return 2 if any(it.code in wanted for it in issues) else 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
