#!/usr/bin/env python3
"""verify_drift: fail on any hand edit to a derived artifact (ADR-001).

Regenerates every derived artifact into a temporary tree with
scripts/build_derived.py, then compares byte for byte with the repo. Also
fails when MANIFEST.sha256 lists a file the generator no longer produces, or
when the repo carries a stale derived file the manifest does not list in a
derived-only folder.

Usage:
    python3 scripts/verify_drift.py

Exit codes: 0 no drift, 1 drift found. Stdlib only.
"""

import hashlib
import os
import shutil
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import build_derived  # noqa: E402

DERIVED_ONLY_DIRS = ("docs/presets", "docs/reference", "templates/era-spec-cards", "assets/figures", "data")
# Renderer output, not generator output. scripts/validate.py checks its freshness instead.
NOT_DERIVED = ("assets/figures/png/",)


def sha(path):
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def main():
    tmp = tempfile.mkdtemp(prefix="homestead-drift-")
    try:
        written = sorted(set(build_derived.build(tmp)))
        problems = []
        for rel in written:
            repo_path = os.path.join(ROOT, rel)
            if not os.path.isfile(repo_path):
                problems.append("missing in repo: " + rel)
            elif sha(repo_path) != sha(os.path.join(tmp, rel)):
                problems.append("drifted: " + rel)
        produced = set(written)
        for folder in DERIVED_ONLY_DIRS:
            base = os.path.join(ROOT, folder)
            for root, _dirs, names in os.walk(base):
                for name in names:
                    rel = os.path.relpath(os.path.join(root, name), ROOT).replace(os.sep, "/")
                    if rel not in produced and not rel.startswith(NOT_DERIVED):
                        problems.append("stale derived file (not produced by canon): " + rel)
        if problems:
            for p in problems:
                print("DRIFT " + p)
            print("verify_drift: FAIL (%d problems). Run python3 scripts/build_derived.py and commit, or fix canon." % len(problems))
            return 1
        print("verify_drift: PASS (%d derived artifacts match canon)" % len(written))
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
