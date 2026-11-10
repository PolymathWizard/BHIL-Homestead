#!/usr/bin/env python3
"""build_derived: regenerate every derived artifact from canon/ (ADR-001).

Derived artifacts are never hand-edited. This script writes them and
scripts/verify_drift.py regenerates them into a temporary tree and fails CI on
any byte of difference.

What it writes:
    kits/*/ and examples/*/builds/*/   recipe assets (GIF, WAV, MID) and safety layer copies
    examples/*/inventory.json          survey of the example source page
    examples/*/mapping-<P>.md          mapping worksheet per built preset
    examples/*/qa/lint-<P>.json        era lint report per build
    examples/*/qa/gif-audit-<P>.json   GIF audit per build
    docs/presets/*.md                  one page per era preset
    docs/reference/*.md                reference tables
    templates/era-spec-cards/*.json    era spec card per preset
    templates/scorecard.json           blank scorecard
    data/*                             CSV and JSON exports for agents and sheets
    assets/figures/*                   the ten-figure kit, its gallery, and its README (scripts/figures.py)
    MANIFEST.sha256                    hash of every derived file

Usage:
    python3 scripts/build_derived.py            write into the repo
    python3 scripts/build_derived.py --out DIR  write into another root (used by the drift gate)

Stdlib only.
"""

import argparse
import csv
import hashlib
import io
import json
import os
import shutil
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import era_lint  # noqa: E402
import gif_audit  # noqa: E402
import gifsmith  # noqa: E402
import map as mapper  # noqa: E402
import survey  # noqa: E402
from hs_core import canon, color  # noqa: E402

sys.path.insert(0, os.path.join(ROOT, "scripts"))
import figures  # noqa: E402

GENERATED_NOTE = "<!-- Generated from canon/ by scripts/build_derived.py. Do not edit by hand; edit canon and rebuild. -->"


class Writer:
    def __init__(self, out_root):
        self.out_root = out_root
        self.written = []

    def path(self, rel):
        full = os.path.join(self.out_root, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        return full

    def text(self, rel, content):
        with open(self.path(rel), "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
        self.written.append(rel)

    def binary(self, rel, data):
        with open(self.path(rel), "wb") as handle:
            handle.write(data)
        self.written.append(rel)

    def copy(self, src_rel, dst_rel):
        shutil.copyfile(os.path.join(ROOT, src_rel), self.path(dst_rel))
        self.written.append(dst_rel)

    def adopt(self, abs_paths):
        for p in abs_paths:
            self.written.append(os.path.relpath(p, self.out_root).replace(os.sep, "/"))


def frontmatter(title, description, extra=None):
    lines = ["---", "title: \"%s\"" % title, "description: \"%s\"" % description, "generated: true"]
    for key, value in (extra or {}).items():
        lines.append("%s: \"%s\"" % (key, value))
    lines += ["---", "", GENERATED_NOTE, ""]
    return "\n".join(lines)


def md_cell(text):
    return str(text).replace("|", "/").replace("\n", " ")


# ---------------------------------------------------------------------------
# Kits and example builds
# ---------------------------------------------------------------------------

def figure_embed(fid, page_rel):
    """Markdown for one kit figure, linked relative to the page that embeds it."""
    meta = next(f for f in canon.load("brand")["figures"] if f["id"] == fid)
    target = "assets/figures/" + figures.figure_file(meta)
    rel = os.path.relpath(target, os.path.dirname(page_rel) or ".").replace(os.sep, "/")
    return "![%s](%s)\n\n*FIG %s. %s*" % (meta["alt"], rel, fid, meta["title"])


def build_folders():
    folders = []
    kits = os.path.join(ROOT, "kits")
    for name in sorted(os.listdir(kits)):
        if name.startswith("preset-") and os.path.isfile(os.path.join(kits, name, "recipe.json")):
            folders.append("kits/" + name)
    examples = os.path.join(ROOT, "examples")
    for ex in sorted(os.listdir(examples)):
        builds = os.path.join(examples, ex, "builds")
        if os.path.isdir(builds):
            for b in sorted(os.listdir(builds)):
                if os.path.isfile(os.path.join(builds, b, "recipe.json")):
                    folders.append("examples/%s/builds/%s" % (ex, b))
    return folders


def render_builds(w):
    for folder in build_folders():
        out_dir = os.path.join(w.out_root, folder)
        os.makedirs(out_dir, exist_ok=True)
        written = gifsmith.run_recipe(os.path.join(ROOT, folder, "recipe.json"), out_dir)
        w.adopt(written)
        for name in canon.load("lint-rules")["exempt_files"]:
            w.copy("kits/safety-layer/" + name, folder + "/" + name)


def build_examples(w):
    examples = os.path.join(ROOT, "examples")
    cwd = os.getcwd()
    os.chdir(ROOT)
    try:
        for ex in sorted(os.listdir(examples)):
            source = "examples/%s/source/index.html" % ex
            if not os.path.isfile(os.path.join(ROOT, source)):
                continue
            inventory = survey.survey(source, 1)
            w.text("examples/%s/inventory.json" % ex, json.dumps(inventory, indent=2, ensure_ascii=False) + "\n")
            builds = os.path.join(examples, ex, "builds")
            for b in sorted(os.listdir(builds)) if os.path.isdir(builds) else []:
                spec_path = os.path.join(builds, b, "era-spec.json")
                if not os.path.isfile(spec_path):
                    continue
                with open(spec_path, "r", encoding="utf-8") as handle:
                    spec = json.load(handle)
                pid = spec["preset"]
                mapping = mapper.build(inventory, spec)
                w.text("examples/%s/mapping-%s.md" % (ex, pid), mapper.to_markdown(mapping))
                build_rel = "examples/%s/builds/%s" % (ex, b)
                report = era_lint.lint(os.path.join(ROOT, build_rel), spec)
                report["target"] = build_rel
                w.text("examples/%s/qa/lint-%s.json" % (ex, pid), json.dumps(report, indent=2) + "\n")
                params = canon.params()
                bg = color.parse_hex(spec.get("palette", {}).get("bg", "#FFFFFF"))
                files = gif_audit.collect([os.path.join(ROOT, build_rel)])
                results = []
                for f in files:
                    r = gif_audit.audit_file(f, params, bg)
                    r["file"] = os.path.relpath(f, ROOT).replace(os.sep, "/")
                    results.append(r)
                audit = {"build": build_rel, "page_bg": color.to_hex(bg), "files": results,
                         "failures": sum(1 for r in results if r["fail"])}
                w.text("examples/%s/qa/gif-audit-%s.json" % (ex, pid), json.dumps(audit, indent=2) + "\n")
    finally:
        os.chdir(cwd)


# ---------------------------------------------------------------------------
# Docs: presets and reference
# ---------------------------------------------------------------------------

def swatch(hexv):
    return "<span style=\"display:inline-block;width:14px;height:14px;border:1px solid #888;background:%s;vertical-align:middle\"></span> `%s`" % (hexv, hexv)


def claim_index():
    return {c["id"]: c for c in canon.load("sources")["claims"]}


def source_index():
    return {s["id"]: s for s in canon.load("sources")["sources"]}


def preset_pages(w):
    widgets = canon.widget_index()
    rows = canon.mapping_rows()
    sources = source_index()
    for p in canon.presets():
        pid = p["id"]
        allowed = canon.allowed_widgets(pid)
        required = p["required_widgets"]
        optional = [wid for wid in widgets if wid in allowed and wid not in required]
        forbidden = [wid for wid in widgets if wid not in allowed]
        out = [frontmatter("Preset %s: %s" % (pid, p["name"]), "Era spec for preset %s (%s)." % (pid, p["years"]),
                           {"preset": pid, "preset_status": p["status"]})]
        out.append("# Preset %s: %s" % (pid, p["name"]))
        out.append("")
        status = "Kit available at [%s](../../%s/README.md)." % (p["kit"], p["kit"]) if p["kit"] else "Spec only. No kit yet; scaffold starts from a blank page."
        out.append("**Years:** %s. **Status:** %s. %s" % (p["years"], p["status"], status))
        out.append("")
        out.append("## Identity")
        out.append("")
        out.append("| Field | Value |")
        out.append("|---|---|")
        out.append("| Target resolution | %s |" % p["target_resolution"])
        out.append("| Target browser | %s |" % p["target_browser"])
        out.append("| Host context | %s |" % p["host_context"])
        canvas = p["canvas"]
        cw = "%s px" % canvas["width_px"] if canvas["width_px"] else canvas["mode"]
        if canvas.get("alt_width_px"):
            cw += " (alternate %s px)" % canvas["alt_width_px"]
        out.append("| Canvas | %s. %s |" % (cw, canvas["note"]))
        out.append("| Palette mode | %s |" % p["palette_mode"])
        out.append("| Layout mode | %s |" % p["layout_mode"])
        out.append("| Motion budget | %d moving items per page |" % p["motion_budget"])
        out.append("| Audio | %s |" % p["audio"])
        out.append("")
        out.append("## Palette")
        out.append("")
        out.append("| Role | Color | Web-safe |")
        out.append("|---|---|---|")
        for role, hexv in p["palette"].items():
            out.append("| %s | %s | %s |" % (role, swatch(hexv), "yes" if color.is_websafe(color.parse_hex(hexv)) else "no"))
        out.append("")
        out.append(p["palette_note"])
        out.append("")
        out.append("## Fonts")
        out.append("")
        out.append("| Role | Stack |")
        out.append("|---|---|")
        for role, stack in p["fonts"].items():
            out.append("| %s | %s |" % (role, ", ".join(stack)))
        out.append("")
        out.append("System fonts only. See [font map](../reference/font-map.md) and [legal notes](../10-legal-and-licensing.md).")
        out.append("")
        out.append("## Layout and navigation")
        out.append("")
        out.append(p["layout"])
        out.append("")
        out.append("Navigation: " + p["nav_style"])
        out.append("")
        out.append("## Widgets")
        out.append("")
        out.append("Required (the lint warns when a marker is missing):")
        out.append("")
        out.append("| Widget | What it is |")
        out.append("|---|---|")
        for wid in required:
            out.append("| `%s` | %s |" % (wid, md_cell(widgets[wid]["description"])))
        for group in p.get("required_any", []):
            out.append("| one of `%s` | %s |" % ("`, `".join(group), "Any one satisfies the requirement."))
        out.append("")
        out.append("Optional: " + (", ".join("`%s`" % x for x in optional) or "none") + ".")
        out.append("")
        out.append("Era mixing (the lint errors unless the era spec declares a time capsule): " + (", ".join("`%s`" % x for x in forbidden) or "none") + ".")
        out.append("")
        out.append("Forbidden elements: " + "; ".join(p["forbidden_elements"]) + ".")
        out.append("")
        out.append("## Voice")
        out.append("")
        out.append(p["voice"])
        out.append("")
        for ex in p["voice_examples"]:
            out.append("- %s" % ex)
        out.append("")
        out.append("## Lived-in details")
        out.append("")
        for egg in p["easter_eggs"]:
            out.append("- %s" % egg)
        out.append("")
        if any(pid in r for r in rows):
            out.append("## Component mapping for this preset")
            out.append("")
            out.append("| Modern pattern | Preset %s equivalent | Widgets |" % pid)
            out.append("|---|---|---|")
            for r in rows:
                if pid in r:
                    out.append("| %s | %s | %s |" % (r["modern_pattern"], md_cell(r[pid]), ", ".join(r["widgets"].get(pid, [])) or "none"))
            out.append("")
        out.append("## Reference sources")
        out.append("")
        for sid in p["reference_sources"]:
            s = sources[sid]
            out.append("- [%s](%s) (`%s`)" % (s["title"], s["url"], sid))
        out.append("")
        w.text("docs/presets/preset-%s-%s.md" % (pid.lower(), p["slug"]), "\n".join(out))


def presets_index(w):
    out = [frontmatter("Era presets", "The six locked era presets and their status.")]
    out.append("# Era presets")
    out.append("")
    out.append(canon.load("presets")["rule"])
    out.append("")
    out.append(figure_embed("HS-02", "docs/presets/README.md"))
    out.append("")
    out.append("| Preset | Name | Years | Canvas | Palette | Status |")
    out.append("|---|---|---|---|---|---|")
    for p in canon.presets():
        canvas = "%s px" % p["canvas"]["width_px"] if p["canvas"]["width_px"] else p["canvas"]["mode"]
        out.append("| [%s](preset-%s-%s.md) | %s | %s | %s | %s | %s |" % (
            p["id"], p["id"].lower(), p["slug"], p["name"], p["years"], canvas, p["palette_mode"], p["status"]))
    out.append("")
    out.append("Kits exist for B, C, and E, the three presets with the best-documented signatures. A, D, and F are full specs that scaffold from a blank page until a kit lands.")
    out.append("")
    w.text("docs/presets/README.md", "\n".join(out))


def reference_pages(w):
    widgets = canon.widgets()
    rows = canon.mapping_rows()

    # mapping table
    out = [frontmatter("Modern to retro mapping table", "Every modern pattern and its period equivalent for presets B, C, and E.")]
    out.append("# Modern to retro mapping table")
    out.append("")
    out.append(canon.load("mapping")["rule"])
    out.append("")
    out.append(figure_embed("HS-05", "docs/reference/mapping-table.md"))
    out.append("")
    out.append("| Modern pattern | B: GeoCities | C: FrontPage | E: MySpace | Tier |")
    out.append("|---|---|---|---|---|")
    for r in rows:
        out.append("| %s | %s | %s | %s | %s |" % (r["modern_pattern"], md_cell(r["B"]), md_cell(r["C"]), md_cell(r["E"]), r["tier"]))
    out.append("")
    out.append("## Detection signals")
    out.append("")
    out.append(canon.load("mapping")["detect_note"])
    out.append("")
    out.append("| Pattern | Signals |")
    out.append("|---|---|")
    for r in rows:
        sig = []
        for kind, pats in r["detect"].items():
            for pat in pats:
                sig.append("%s: `%s`" % (kind, md_cell(pat)))
        out.append("| %s | %s |" % (r["modern_pattern"], "<br>".join(sig) or "none"))
    out.append("")
    w.text("docs/reference/mapping-table.md", "\n".join(out))

    # widget registry
    out = [frontmatter("Widget registry", "Every period widget, its marker, and the presets it belongs to.")]
    out.append("# Widget registry")
    out.append("")
    out.append("Mark each widget in the build with `<!-- hs:widget ID -->`. The lint reads the markers to check required widgets and to catch era mixing.")
    out.append("")
    out.append("| ID | Widget | A | B | C | D | E | F | Description |")
    out.append("|---|---|---|---|---|---|---|---|---|")
    for wd in widgets:
        cells = ["yes" if pid in wd["presets"] else "" for pid in "ABCDEF"]
        out.append("| `%s` | %s | %s | %s |" % (wd["id"], wd["label"], " | ".join(cells), md_cell(wd["description"])))
    out.append("")
    w.text("docs/reference/widget-registry.md", "\n".join(out))

    # rubric
    rubric = canon.load("rubric")
    out = [frontmatter("Authenticity rubric", "The 40-point scorecard, bands, and hard gates.")]
    out.append("# Authenticity rubric")
    out.append("")
    out.append("Score each row 0, 1, or 2. Maximum %d." % rubric["max_score"])
    out.append("")
    out.append(figure_embed("HS-09", "docs/reference/rubric.md"))
    out.append("")
    out.append("| Row | Check | 0 | 1 | 2 | Lint rules |")
    out.append("|---|---|---|---|---|---|")
    for r in rubric["rows"]:
        out.append("| %d | %s | %s | %s | %s | %s |" % (r["row"], r["check"], md_cell(r["0"]), md_cell(r["1"]), md_cell(r["2"]), ", ".join(r["lint"]) or "manual"))
    out.append("")
    out.append("## Bands")
    out.append("")
    out.append("| Verdict | Score | Action |")
    out.append("|---|---|---|")
    for b in rubric["bands"]:
        out.append("| %s | %d to %d | %s |" % (b["verdict"], b["min"], b["max"], b["action"]))
    out.append("")
    out.append("## Hard gates")
    out.append("")
    out.append("A build cannot SHIP while any gate fails, whatever the total.")
    out.append("")
    for g in rubric["hard_gates"]:
        out.append("- Row %d must score at least %d. %s" % (g["row"], g["min"], g["reason"]))
    out.append("")
    w.text("docs/reference/rubric.md", "\n".join(out))

    # lint rules
    lint = canon.load("lint-rules")
    out = [frontmatter("Lint rules", "Every anachronism lint rule, its severity per preset, and the fix.")]
    out.append("# Lint rules")
    out.append("")
    out.append("Exempt files: %s. Severity is per preset; a blank cell means the rule does not apply." % ", ".join("`%s`" % f for f in lint["exempt_files"]))
    out.append("")
    out.append(figure_embed("HS-07", "docs/reference/lint-rules.md"))
    out.append("")
    out.append("| ID | Rule | A | B | C | D | E | F | Row | Fix |")
    out.append("|---|---|---|---|---|---|---|---|---|---|")
    for r in lint["rules"]:
        cells = [r["applies"].get(pid, "") for pid in "ABCDEF"]
        out.append("| %s | %s | %s | %d | %s |" % (r["id"], r["title"], " | ".join(cells), r["rubric_row"], md_cell(r["fix"])))
    out.append("")
    out.append("## Verdicts")
    out.append("")
    for k, v in lint["verdicts"].items():
        out.append("- **%s**: %s" % (k, v))
    out.append("")
    w.text("docs/reference/lint-rules.md", "\n".join(out))

    # technical vocabulary
    out = [frontmatter("Technical vocabulary", "Period techniques, whether they still render, and how HOMESTEAD emulates them.")]
    out.append("# Technical vocabulary")
    out.append("")
    out.append("| ID | Technique | Era | Renders today | Emulation | Claims |")
    out.append("|---|---|---|---|---|---|")
    for t in canon.load("techniques")["techniques"]:
        cl = ", ".join("[%s](evidence-register.md#%s)" % (c, c.lower()) for c in t["claims"]) or "none"
        out.append("| %s | %s | %s | %s | %s | %s |" % (t["id"], md_cell(t["technique"]), t["era"], t["renders_today"], md_cell(t["emulation"]), cl))
    out.append("")
    w.text("docs/reference/technical-vocabulary.md", "\n".join(out))

    # font map
    fonts = canon.load("fonts")
    out = [frontmatter("Font map", "Modern font categories mapped to era system stacks per preset.")]
    out.append("# Font map")
    out.append("")
    out.append(fonts["policy"])
    out.append("")
    out.append("| Category | Detects | A | B | C | D | E | F |")
    out.append("|---|---|---|---|---|---|---|---|")
    for c in fonts["categories"]:
        out.append("| %s | %s | %s |" % (c["id"], ", ".join(c["detect"][:8]) + (" ..." if len(c["detect"]) > 8 else ""),
                                         " | ".join(c["stacks"][pid] for pid in "ABCDEF")))
    out.append("")
    w.text("docs/reference/font-map.md", "\n".join(out))

    # web-safe palette
    out = [frontmatter("Web-safe palette", "The 216 colors of the web-safe cube.")]
    out.append("# Web-safe palette")
    out.append("")
    out.append("Every combination of 00, 33, 66, 99, CC, and FF across red, green, and blue ([C-003](evidence-register.md#c-003)). Snap brand colors with `python3 tools/websafe.py snap`.")
    out.append("")
    out.append(figure_embed("HS-06", "docs/reference/web-safe-palette.md"))
    out.append("")
    levels = ["00", "33", "66", "99", "CC", "FF"]
    for r in levels:
        out.append("## Red %s" % r)
        out.append("")
        out.append("| G \\ B | " + " | ".join(levels) + " |")
        out.append("|---|" + "---|" * 6)
        for g in levels:
            out.append("| %s | %s |" % (g, " | ".join("`#%s%s%s`" % (r, g, b) for b in levels)))
        out.append("")
    w.text("docs/reference/web-safe-palette.md", "\n".join(out))

    # evidence register
    src = canon.load("sources")
    sindex = source_index()
    out = [frontmatter("Evidence register", "Every factual claim HOMESTEAD relies on, with its evidence tier and sources.")]
    out.append("# Evidence register")
    out.append("")
    out.append(src["provenance_note"])
    out.append("")
    out.append("## Tiers")
    out.append("")
    for k, v in src["tiers"].items():
        out.append("- **%s**: %s" % (k, v))
    out.append("")
    out.append("## Claims")
    out.append("")
    for c in src["claims"]:
        out.append("### %s" % c["id"])
        out.append("")
        out.append("**%s.** %s" % (c["tier"], c["claim"]))
        out.append("")
        if c["sources"]:
            out.append("Sources: " + "; ".join("[%s](%s)" % (sindex[s]["title"], sindex[s]["url"]) for s in c["sources"]) + ".")
        else:
            out.append("Sources: none retrieved. See the tier note.")
        out.append("")
    out.append("## Reference resources")
    out.append("")
    for s in src["sources"]:
        if s["kind"] == "reference":
            out.append("- [%s](%s) (`%s`)" % (s["title"], s["url"], s["id"]))
    out.append("")
    w.text("docs/reference/evidence-register.md", "\n".join(out))

    # phase map
    proc = canon.load("process")
    out = [frontmatter("Phase map", "The seven phases of the Retro-Web Redesign Architecture.")]
    out.append("# Phase map: %s" % proc["framework_name"])
    out.append("")
    out.append(proc["core_principle"])
    out.append("")
    out.append(figure_embed("HS-03", "docs/reference/phase-map.md"))
    out.append("")
    for ph in proc["phases"]:
        out.append("## Phase %d: %s" % (ph["id"], ph["name"]))
        out.append("")
        out.append("*%s*" % ph["question"])
        out.append("")
        out.append("Owner: `%s`. Prompt: [%s](../../prompts/README.md). Worksheet: `%s`. Tools: %s." % (
            ph["agent"], ph["prompt"], ph["worksheet"], ", ".join("`%s`" % t for t in ph["tools"]) or "none"))
        out.append("")
        for i, step in enumerate(ph["steps"], 1):
            out.append("%d. %s" % (i, step))
        out.append("")
        out.append("Outputs: " + ", ".join("`%s`" % o for o in ph["outputs"]) + ".")
        out.append("")
    w.text("docs/reference/phase-map.md", "\n".join(out))

    # agent roster
    agents = canon.load("agents")
    out = [frontmatter("Agent roster", "The CADRE orchestrator and its six tool-isolated subagents.")]
    out.append("# Agent roster")
    out.append("")
    out.append(agents["pattern"])
    out.append("")
    out.append(figure_embed("HS-10", "docs/reference/agent-roster.md"))
    out.append("")
    out.append("| Agent | Phase | Model | Tools | Forbidden | Writes | Contract |")
    out.append("|---|---|---|---|---|---|---|")
    o = agents["orchestrator"]
    out.append("| orchestrator | 0 and checkpoints | %s | all | none | engagement folder | owns sequencing and sign-off |" % o["model"])
    for a in agents["agents"]:
        out.append("| `%s` | %d | %s | %s | %s | %s | %s |" % (a["name"], a["phase"], a["model"], ", ".join(a["tools"]),
                                                          ", ".join(a["forbidden"]), md_cell(a["writes"]), md_cell(a["contract"])))
    out.append("")
    out.append("Definitions live in `.claude/agents/`. `scripts/validate.py` fails if any definition's tools drift from this table.")
    out.append("")
    w.text("docs/reference/agent-roster.md", "\n".join(out))

    # reference index
    out = [frontmatter("Reference", "Generated reference tables.")]
    out.append("# Reference")
    out.append("")
    out.append("Everything in this folder is generated from `canon/` and drift-checked.")
    out.append("")
    for name, desc in (
        ("phase-map.md", "Seven phases, steps, owners, and outputs"),
        ("mapping-table.md", "Modern pattern to period equivalent, with detection signals"),
        ("widget-registry.md", "Every widget, its marker, and its presets"),
        ("rubric.md", "The 40-point scorecard, bands, and hard gates"),
        ("lint-rules.md", "Anachronism lint rules and fixes"),
        ("technical-vocabulary.md", "Period techniques and how to emulate them"),
        ("font-map.md", "Modern font categories to era stacks"),
        ("web-safe-palette.md", "The 216-color cube"),
        ("agent-roster.md", "Orchestrator and subagents"),
        ("evidence-register.md", "Claims, tiers, and sources"),
    ):
        out.append("- [%s](%s): %s" % (name.replace(".md", "").replace("-", " ").title(), name, desc))
    out.append("")
    w.text("docs/reference/README.md", "\n".join(out))


# ---------------------------------------------------------------------------
# Templates and data exports
# ---------------------------------------------------------------------------

def templates_and_data(w):
    for p in canon.presets():
        spec = canon.era_spec_from_preset(p["id"])
        w.text("templates/era-spec-cards/preset-%s-%s.json" % (p["id"].lower(), p["slug"]), json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
    rubric = canon.load("rubric")
    card = {"engagement": "TEMPLATE", "preset": "B", "auditor": "authenticity-auditor", "date": "",
            "rows": [{"row": r["row"], "check": r["check"], "score": None, "evidence": ""} for r in rubric["rows"]],
            "total": None, "verdict": None, "notes": ""}
    w.text("templates/scorecard.json", json.dumps(card, indent=2) + "\n")

    buf = io.StringIO()
    cw = csv.writer(buf, lineterminator="\n")
    cw.writerow(["id", "modern_pattern", "tier", "B", "C", "E", "widgets_B", "widgets_C", "widgets_E"])
    for r in canon.mapping_rows():
        cw.writerow([r["id"], r["modern_pattern"], r["tier"], r["B"], r["C"], r["E"],
                     ";".join(r["widgets"]["B"]), ";".join(r["widgets"]["C"]), ";".join(r["widgets"]["E"])])
    w.text("data/mapping.csv", buf.getvalue())

    buf = io.StringIO()
    cw = csv.writer(buf, lineterminator="\n")
    cw.writerow(["id", "label", "A", "B", "C", "D", "E", "F", "description"])
    for wd in canon.widgets():
        cw.writerow([wd["id"], wd["label"]] + ["1" if pid in wd["presets"] else "0" for pid in "ABCDEF"] + [wd["description"]])
    w.text("data/widgets.csv", buf.getvalue())

    buf = io.StringIO()
    cw = csv.writer(buf, lineterminator="\n")
    cw.writerow(["row", "check", "score_0", "score_1", "score_2", "lint_rules"])
    for r in rubric["rows"]:
        cw.writerow([r["row"], r["check"], r["0"], r["1"], r["2"], ";".join(r["lint"])])
    w.text("data/rubric.csv", buf.getvalue())

    index = {name: canon.load(name) for name in canon.CANON_FILES}
    w.text("data/homestead-index.json", json.dumps(index, indent=2, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------

def manifest(w):
    lines = []
    for rel in sorted(set(w.written)):
        with open(os.path.join(w.out_root, rel), "rb") as handle:
            lines.append("%s  %s" % (hashlib.sha256(handle.read()).hexdigest(), rel))
    w.text("MANIFEST.sha256", "\n".join(lines) + "\n")


def build(out_root):
    w = Writer(out_root)
    render_builds(w)
    build_examples(w)
    preset_pages(w)
    presets_index(w)
    reference_pages(w)
    templates_and_data(w)
    figures.build(w)
    manifest(w)
    return w.written


def main(argv=None):
    parser = argparse.ArgumentParser(description="Regenerate HOMESTEAD derived artifacts.")
    parser.add_argument("--out", default=ROOT)
    args = parser.parse_args(argv)
    written = build(os.path.abspath(args.out))
    print("build_derived: wrote %d derived artifacts" % len(set(written)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
