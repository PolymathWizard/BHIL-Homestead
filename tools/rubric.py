#!/usr/bin/env python3
"""rubric: the 40-point HOMESTEAD authenticity scorecard (Phase 6).

Usage:
    python3 tools/rubric.py blank --engagement acme --preset B --out 06-qa/scorecard.json
    python3 tools/rubric.py score 06-qa/scorecard.json [--lint lint.json] [--write]

score validates the card against schemas/scorecard.schema.json, totals it,
applies the hard gates (autoplay audio, Safe Mode, flash thresholds), and
returns SHIP, REVISE, or REBUILD from canon/rubric.json. With --lint, rows
that the lint flagged with errors are capped at 1, because a row cannot earn
full marks while a rule tied to it is failing.

Exit codes: 0 SHIP, 1 REVISE, REBUILD, or incomplete, 2 usage. Stdlib only.
"""

import argparse
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hs_core import canon, schema  # noqa: E402


def blank(engagement, preset):
    rows = canon.load("rubric")["rows"]
    return {
        "engagement": engagement,
        "preset": preset,
        "auditor": "authenticity-auditor",
        "date": datetime.date.today().isoformat(),
        "rows": [{"row": r["row"], "check": r["check"], "score": None, "evidence": ""} for r in rows],
        "total": None,
        "verdict": None,
        "notes": "",
    }


def evaluate(card, lint_report=None):
    rubric = canon.load("rubric")
    with open(os.path.join(canon.REPO_ROOT, "schemas", "scorecard.schema.json"), "r", encoding="utf-8") as handle:
        errors = schema.validate(card, json.load(handle))
    scores = {r["row"]: r["score"] for r in card["rows"]}
    missing = sorted(row for row, score in scores.items() if score is None)
    capped = []
    if lint_report:
        error_rows = {f["rubric_row"] for f in lint_report["findings"] if f["severity"] == "error"}
        for row in sorted(error_rows):
            if scores.get(row) == 2:
                scores[row] = 1
                capped.append(row)
    if errors or missing:
        return {"verdict": "INCOMPLETE", "total": None, "schema_errors": errors, "missing_rows": missing,
                "capped_rows": capped, "gate_failures": [], "below_two": []}
    total = sum(scores.values())
    gate_failures = [g for g in rubric["hard_gates"] if scores[g["row"]] < g["min"]]
    verdict = next(b["verdict"] for b in rubric["bands"] if b["min"] <= total <= b["max"])
    if gate_failures and verdict == "SHIP":
        verdict = "REVISE"
    below = [{"row": r["row"], "check": r["check"]} for r in rubric["rows"] if scores[r["row"]] < 2]
    return {"verdict": verdict, "total": total, "max": rubric["max_score"], "schema_errors": [], "missing_rows": [],
            "capped_rows": capped, "gate_failures": gate_failures, "below_two": below}


def main(argv=None):
    parser = argparse.ArgumentParser(description="HOMESTEAD authenticity scorecard.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    bp = sub.add_parser("blank")
    bp.add_argument("--engagement", required=True)
    bp.add_argument("--preset", required=True)
    bp.add_argument("--out")
    sp = sub.add_parser("score")
    sp.add_argument("card")
    sp.add_argument("--lint", help="era_lint JSON report to cap flagged rows")
    sp.add_argument("--write", action="store_true", help="write total and verdict back into the card")
    args = parser.parse_args(argv)

    if args.cmd == "blank":
        payload = json.dumps(blank(args.engagement, args.preset.upper()), indent=2) + "\n"
        if args.out:
            os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
            with open(args.out, "w", encoding="utf-8") as handle:
                handle.write(payload)
            print("wrote " + args.out)
        else:
            sys.stdout.write(payload)
        return 0

    with open(args.card, "r", encoding="utf-8") as handle:
        card = json.load(handle)
    lint_report = None
    if args.lint:
        with open(args.lint, "r", encoding="utf-8") as handle:
            lint_report = json.load(handle)
    result = evaluate(card, lint_report)
    if result["verdict"] == "INCOMPLETE":
        for err in result["schema_errors"]:
            print("schema: " + err)
        if result["missing_rows"]:
            print("unscored rows: " + ", ".join(str(r) for r in result["missing_rows"]))
        print("verdict: INCOMPLETE")
        return 1
    print("total: %d / %d" % (result["total"], result["max"]))
    for row in result["capped_rows"]:
        print("capped row %d at 1 because lint reported errors tied to it" % row)
    for gate in result["gate_failures"]:
        print("hard gate failed, row %d: %s" % (gate["row"], gate["reason"]))
    for row in result["below_two"]:
        print("revise row %d: %s" % (row["row"], row["check"]))
    print("verdict: " + result["verdict"])
    if args.write:
        card["total"] = result["total"]
        card["verdict"] = result["verdict"]
        with open(args.card, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(card, indent=2) + "\n")
    return 0 if result["verdict"] == "SHIP" else 1


if __name__ == "__main__":
    sys.exit(main())
