#!/usr/bin/env python3
"""scaffold: open a HOMESTEAD engagement folder (Phase 0).

Creates engagements/<slug>/ with the intake form filled in, an era spec card
prefilled from the chosen preset, an empty asset log, a blank scorecard, and
a 05-build/ folder seeded from the preset kit plus the safety layer.

Usage:
    python3 tools/scaffold.py new acme --target https://acme.example --preset B \
        --purpose portfolio --deliverable static-mock --asset-policy originals-only
    python3 tools/scaffold.py presets

The engagements/ folder is gitignored except for .gitkeep, so client work
never lands in the framework history by accident. Stdlib only.
"""

import argparse
import datetime
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hs_core import canon  # noqa: E402

TEMPLATES = os.path.join(canon.REPO_ROOT, "templates")
KITS = os.path.join(canon.REPO_ROOT, "kits")
SAFETY = os.path.join(KITS, "safety-layer")


def fill(template_name, tokens):
    with open(os.path.join(TEMPLATES, template_name), "r", encoding="utf-8") as handle:
        text = handle.read()
    for key, value in tokens.items():
        text = text.replace("{{%s}}" % key, value)
    return text


def seed_build(build_dir, preset):
    os.makedirs(build_dir, exist_ok=True)
    kit = preset.get("kit")
    if kit:
        src = os.path.join(canon.REPO_ROOT, kit)
        for name in sorted(os.listdir(src)):
            if name == "README.md":
                continue
            s, d = os.path.join(src, name), os.path.join(build_dir, name)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
    else:
        with open(os.path.join(build_dir, "index.html"), "w", encoding="utf-8") as handle:
            handle.write(fill("blank-page.html", {"PRESET": preset["id"], "PRESET_NAME": preset["name"]}))
    for name in canon.load("lint-rules")["exempt_files"]:
        shutil.copy2(os.path.join(SAFETY, name), os.path.join(build_dir, name))


def new(args):
    preset = canon.preset(args.preset.upper())
    root = args.root or os.path.join(canon.REPO_ROOT, "engagements")
    base = os.path.join(root, args.slug)
    if os.path.exists(base) and not args.force:
        print("scaffold: %s exists; pass --force to reuse it" % base, file=sys.stderr)
        return 2
    os.makedirs(os.path.join(base, "01-inventory"), exist_ok=True)
    os.makedirs(os.path.join(base, "06-qa"), exist_ok=True)
    tokens = {
        "SLUG": args.slug,
        "TARGET": args.target,
        "PRESET": preset["id"],
        "PRESET_NAME": preset["name"],
        "PURPOSE": args.purpose,
        "DELIVERABLE": args.deliverable,
        "ASSET_POLICY": args.asset_policy,
        "DATE": datetime.date.today().isoformat(),
    }
    with open(os.path.join(base, "README.md"), "w", encoding="utf-8") as handle:
        handle.write(fill("engagement-readme.md", tokens))
    with open(os.path.join(base, "00-intake.md"), "w", encoding="utf-8") as handle:
        handle.write(fill("intake.md", tokens))
    spec = canon.era_spec_from_preset(preset["id"])
    spec["asset_policy"] = args.asset_policy
    with open(os.path.join(base, "02-era-spec.json"), "w", encoding="utf-8") as handle:
        handle.write(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
    shutil.copy2(os.path.join(TEMPLATES, "asset-log.csv"), os.path.join(base, "04-asset-log.csv"))
    shutil.copy2(os.path.join(TEMPLATES, "qa-notes.md"), os.path.join(base, "06-qa", "qa-notes.md"))
    card = json.load(open(os.path.join(TEMPLATES, "scorecard.json"), "r", encoding="utf-8"))
    card["engagement"] = args.slug
    card["preset"] = preset["id"]
    card["date"] = tokens["DATE"]
    with open(os.path.join(base, "06-qa", "scorecard.json"), "w", encoding="utf-8") as handle:
        handle.write(json.dumps(card, indent=2) + "\n")
    seed_build(os.path.join(base, "05-build"), preset)
    print("opened %s" % base)
    print("next: python3 tools/survey.py %s --pages 6 --out %s" % (args.target, os.path.join(base, "01-inventory", "inventory.json")))
    if preset["status"] != "kit":
        print("note: preset %s is spec-only; 05-build starts from a blank page" % preset["id"])
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Open a HOMESTEAD engagement.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("presets")
    np_ = sub.add_parser("new")
    np_.add_argument("slug")
    np_.add_argument("--target", required=True, help="URL or saved HTML path")
    np_.add_argument("--preset", required=True, choices=list("ABCDEFabcdef"))
    hs = canon.load("homestead")
    np_.add_argument("--purpose", default="portfolio", choices=hs["purposes"])
    np_.add_argument("--deliverable", default="static-mock", choices=hs["deliverables"])
    np_.add_argument("--asset-policy", default="originals-only", choices=sorted(hs["asset_policies"]))
    np_.add_argument("--root", help="engagements root (default: repo engagements/)")
    np_.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)
    if args.cmd == "presets":
        for p in canon.presets():
            print("%s  %-12s %-10s %-9s %s" % (p["id"], p["slug"], p["years"], p["status"], p["name"]))
        return 0
    return new(args)


if __name__ == "__main__":
    sys.exit(main())
