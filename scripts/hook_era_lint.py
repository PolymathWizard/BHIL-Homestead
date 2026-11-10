#!/usr/bin/env python3
"""hook_era_lint: Claude Code PostToolUse hook for period builds.

Wired in .claude/settings.json on Write and Edit. Reads the hook payload from
stdin. When the touched file is HTML or CSS inside engagements/<slug>/05-build/
(or a kit or example build), it lints that build against the engagement's era
spec and, on errors, exits 2 so the findings are fed back to the agent before
it moves on. Any other file passes through silently.

Stdlib only.
"""

import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import era_lint  # noqa: E402
from hs_core import canon  # noqa: E402

BUILD_RE = re.compile(r"(engagements/[^/]+)/05-build/")
EXAMPLE_RE = re.compile(r"(examples/[^/]+/builds/[^/]+)/")
KIT_RE = re.compile(r"kits/preset-([a-f])-[^/]+/")


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return 0
    path = (payload.get("tool_input") or {}).get("file_path", "")
    if not path.lower().endswith((".html", ".htm", ".css")):
        return 0
    rel = os.path.relpath(os.path.abspath(path), ROOT).replace(os.sep, "/")
    spec = None
    target = None
    m = BUILD_RE.search(rel)
    if m:
        target = os.path.join(ROOT, m.group(1), "05-build")
        spec_path = os.path.join(ROOT, m.group(1), "02-era-spec.json")
        if os.path.isfile(spec_path):
            with open(spec_path, "r", encoding="utf-8") as handle:
                spec = json.load(handle)
    m = EXAMPLE_RE.search(rel) if spec is None else None
    if m:
        target = os.path.join(ROOT, m.group(1))
        spec_path = os.path.join(target, "era-spec.json")
        if os.path.isfile(spec_path):
            with open(spec_path, "r", encoding="utf-8") as handle:
                spec = json.load(handle)
    m = KIT_RE.search(rel) if spec is None else None
    if m:
        target = os.path.join(ROOT, rel.split("/")[0], rel.split("/")[1])
        spec = canon.era_spec_from_preset(m.group(1).upper())
    if spec is None or target is None:
        return 0
    report = era_lint.lint(target, spec)
    errors = [f for f in report["findings"] if f["severity"] == "error"]
    if not errors:
        return 0
    lines = ["HOMESTEAD era lint found %d error(s) in %s (preset %s):" % (len(errors), os.path.relpath(target, ROOT), spec["preset"])]
    for f in errors[:12]:
        lines.append("- %s %s:%s %s. %s Fix: %s" % (f["rule"], f["file"], f["line"], f["title"], f["detail"], f["fix"]))
    print("\n".join(lines), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
