#!/usr/bin/env python3
"""era_lint: the HOMESTEAD anachronism lint (Phases 5 and 6).

Checks a build folder or file against the rules in canon/lint-rules.json for
one preset: web fonts, rounded corners, flex and grid, emoji, SVG, responsive
breakpoints, modern copy, autoplay audio, missing safety layer, era mixing,
canvas width, web-safe colors, alt text, and the motion budget.

The safety layer files (homestead-safe.css and homestead-safe.js) are exempt
by design (ADR-003). Pages marked <!-- hs:page text-only --> skip the canvas,
motion, and web-safe checks.

Verdicts never say clean. No findings means INCONCLUSIVE, because lint cannot
judge visual authenticity or copy quality (ADR-007).

Usage:
    python3 tools/era_lint.py BUILD_DIR --preset B
    python3 tools/era_lint.py BUILD_DIR --spec 02-era-spec.json --format json
    python3 tools/era_lint.py page.html --preset C --strict

Exit codes: 0 no errors (warnings allowed unless --strict), 1 errors, 2 usage.
Stdlib only.
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hs_core import canon, color, gif, htmlscan  # noqa: E402

HTML_EXT = (".html", ".htm")
CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)
IMG_RE = re.compile(r"<img\b[^>]*>", re.I)
IMG_SRC_RE = re.compile(r"\bsrc\s*=\s*[\"']?([^\"'\s>]+)", re.I)
ALT_RE = re.compile(r"\balt\s*=", re.I)
ATTR_COLOR_RE = re.compile(r"\b(?:bgcolor|color|text|link|vlink|alink|bordercolor|bordercolorlight|bordercolordark)\s*=\s*[\"']?(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3})\b", re.I)
CSS_COLOR_RE = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
PAGE_MARK_RE = re.compile(r"<!--\s*hs:page\s+([a-z\-]+)\s*-->", re.I)
MOTION_TAG_RE = re.compile(r"<marquee\b|<blink\b|class\s*=\s*[\"'][^\"']*hs-blink", re.I)


def collect(target):
    exempt = set(canon.load("lint-rules")["exempt_files"])
    files = []
    if os.path.isfile(target):
        files.append(target)
    else:
        for root, dirs, names in os.walk(target):
            dirs.sort()
            for name in sorted(names):
                if name in exempt:
                    continue
                if name.lower().endswith(HTML_EXT + (".css",)):
                    files.append(os.path.join(root, name))
    return files


def line_of(original, needle):
    pos = original.find(needle)
    return original.count("\n", 0, pos) + 1 if pos >= 0 else 0


def lint(target, spec):
    preset_id = spec["preset"]
    rules = [r for r in canon.load("lint-rules")["rules"] if preset_id in r["applies"]]
    allowed = canon.allowed_widgets(preset_id) | set(spec.get("allowed_extra_widgets", []))
    known = set(canon.widget_index())
    findings = []
    site_markers = set()

    def add(rule, file, line, detail):
        findings.append({
            "rule": rule["id"],
            "title": rule["title"],
            "severity": rule["applies"][preset_id],
            "file": file,
            "line": line,
            "detail": detail,
            "message": rule["message"],
            "fix": rule["fix"],
            "rubric_row": rule["rubric_row"],
        })

    for path in collect(target):
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            original = handle.read()
        rel = os.path.relpath(path, target) if os.path.isdir(target) else os.path.basename(path)
        is_html = path.lower().endswith(HTML_EXT)
        if is_html:
            markers = htmlscan.widget_markers(original)
            site_markers.update(markers)
            page_flags = {m.group(1).lower() for m in PAGE_MARK_RE.finditer(original)}
            html_scope = htmlscan.strip_comments(original)
            css_scope = htmlscan.css_sources(original)
            text_scope = htmlscan.visible_text(original)
        else:
            markers = []
            page_flags = set()
            html_scope = ""
            css_scope = CSS_COMMENT_RE.sub("", original)
            text_scope = ""
        safety_present = is_html and all(name in html_scope for name in canon.load("lint-rules")["exempt_files"])
        for rule in rules:
            kind = rule["kind"]
            if kind == "regex":
                scopes = {"html": [html_scope], "css": [css_scope], "text": [text_scope],
                          "both": [html_scope] if is_html else [css_scope]}[rule["scope"]]
                rx = re.compile(rule["pattern"], re.I)
                for scope in scopes:
                    hits = sorted({m.group(0) for m in rx.finditer(scope)})
                    if hits:
                        add(rule, rel, line_of(original, hits[0]), "found: " + ", ".join(repr(h) for h in hits[:5]))
            elif kind == "requires-safety" and is_html:
                if re.search(rule["pattern"], html_scope, re.I) and not safety_present:
                    add(rule, rel, 0, "safety layer not linked")
            elif kind == "safety-layer" and is_html:
                if not safety_present:
                    missing = [n for n in canon.load("lint-rules")["exempt_files"] if n not in html_scope]
                    add(rule, rel, 0, "missing: " + ", ".join(missing))
            elif kind == "alt-text" and is_html:
                bad = [tag for tag in IMG_RE.findall(html_scope) if not ALT_RE.search(tag)]
                if bad:
                    add(rule, rel, line_of(original, bad[0]), "%d image(s) without alt, first: %s" % (len(bad), bad[0][:80]))
            elif kind == "websafe" and "text-only" not in page_flags:
                colors_found = set()
                if is_html:
                    colors_found.update(m.group(1) for m in ATTR_COLOR_RE.finditer(html_scope))
                colors_found.update("#" + m.group(1) for m in CSS_COLOR_RE.finditer(css_scope))
                off = sorted({c.upper() for c in colors_found if not color.is_websafe(color.parse_hex(c))})
                if off:
                    add(rule, rel, line_of(original, off[0]) or line_of(original, off[0].lower()), "off-palette: " + ", ".join(off[:8]))
            elif kind == "widget-era" and is_html:
                for marker in markers:
                    if marker not in known:
                        findings.append({"rule": rule["id"], "title": "Unknown widget marker", "severity": "warn", "file": rel,
                                         "line": line_of(original, marker), "detail": marker, "message": "Marker names no widget in canon/widgets.json.",
                                         "fix": "Fix the marker id or add the widget to canon.", "rubric_row": rule["rubric_row"]})
                    elif marker not in allowed and not spec.get("time_capsule"):
                        add(rule, rel, line_of(original, marker), "%s is not a preset %s widget" % (marker, preset_id))
            elif kind == "canvas" and is_html and "text-only" not in page_flags:
                width = spec.get("canvas_width_px")
                if not width:
                    continue
                m = re.search(rule["pattern"], html_scope, re.I)
                if not m:
                    add(rule, rel, 0, "no fixed-width outer table found")
                elif abs(int(m.group(1)) - width) > 40:
                    add(rule, rel, line_of(original, m.group(0)), "outer table width %s, era canvas %s" % (m.group(1), width))
            elif kind == "motion-budget" and is_html and "text-only" not in page_flags:
                count = len(MOTION_TAG_RE.findall(html_scope))
                for tag in IMG_RE.findall(html_scope):
                    src = IMG_SRC_RE.search(tag)
                    if not src or not src.group(1).lower().endswith(".gif"):
                        continue
                    img_path = os.path.normpath(os.path.join(os.path.dirname(path), src.group(1)))
                    if os.path.isfile(img_path):
                        with open(img_path, "rb") as fh:
                            try:
                                if gif.probe(fh.read())["frames"] > 1:
                                    count += 1
                            except gif.GifFormatError:
                                pass
                if count > spec["motion_budget"]:
                    add(rule, rel, 0, "%d moving items, budget %d" % (count, spec["motion_budget"]))

    widget_rules = [r for r in rules if r["kind"] == "widget-required"]
    if widget_rules and os.path.isdir(target):
        rule = widget_rules[0]
        for wid in spec["required_widgets"]:
            if wid not in site_markers:
                add(rule, "(site)", 0, "missing marker: " + wid)
        for group in spec.get("required_any", []):
            if not any(w in site_markers for w in group):
                add(rule, "(site)", 0, "missing one of: " + ", ".join(group))

    errors = sum(1 for f in findings if f["severity"] == "error")
    warns = sum(1 for f in findings if f["severity"] == "warn")
    if errors:
        verdict = "FINDINGS"
    elif warns:
        verdict = "WARNINGS ONLY"
    else:
        verdict = "NO FINDINGS (INCONCLUSIVE)"
    rows_touched = sorted({f["rubric_row"] for f in findings})
    return {
        "target": target,
        "preset": preset_id,
        "files_checked": len(collect(target)),
        "errors": errors,
        "warnings": warns,
        "verdict": verdict,
        "rubric_rows_flagged": rows_touched,
        "widget_markers": sorted(site_markers),
        "findings": findings,
    }


def load_spec(args):
    if args.spec:
        with open(args.spec, "r", encoding="utf-8") as handle:
            return json.load(handle)
    if args.preset:
        return canon.era_spec_from_preset(args.preset.upper())
    raise SystemExit("era_lint: give --preset or --spec")


def main(argv=None):
    parser = argparse.ArgumentParser(description="HOMESTEAD anachronism lint.")
    parser.add_argument("target")
    parser.add_argument("--preset")
    parser.add_argument("--spec")
    parser.add_argument("--format", choices=["table", "json"], default="table")
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    args = parser.parse_args(argv)
    if not os.path.exists(args.target):
        print("era_lint: no such path: %s" % args.target, file=sys.stderr)
        return 2
    report = lint(args.target, load_spec(args))
    if args.format == "json":
        print(json.dumps(report, indent=2))
    else:
        print("HOMESTEAD era lint, preset %s, %d file(s)" % (report["preset"], report["files_checked"]))
        for f in report["findings"]:
            loc = "%s:%s" % (f["file"], f["line"]) if f["line"] else f["file"]
            print("  %-5s %s %s  %s  %s" % (f["severity"].upper(), f["rule"], loc, f["title"], f["detail"]))
        print("verdict: %s (%d errors, %d warnings)" % (report["verdict"], report["errors"], report["warnings"]))
    if report["errors"] or (args.strict and report["warnings"]):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
