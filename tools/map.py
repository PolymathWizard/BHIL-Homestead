#!/usr/bin/env python3
"""map: build the component mapping worksheet (Phase 3).

Joins a survey inventory with an era spec and canon/mapping.json to produce a
worksheet where every detected modern pattern already carries its period
equivalent and a default decision. The mapper then confirms or overrides each
row, plans navigation, and drafts the copy deck.

Usage:
    python3 tools/map.py INVENTORY.json --spec ERA_SPEC.json --out 03-mapping.md
    python3 tools/map.py INVENTORY.json --preset B --json

Stdlib only.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hs_core import canon, color  # noqa: E402


def build(inventory, spec):
    preset_id = spec["preset"]
    rows = {r["id"]: r for r in canon.mapping_rows()}
    widgets = canon.widget_index()
    params = canon.params()
    detected = []
    supplied = {}
    for pattern in inventory["patterns"]:
        row = rows[pattern["id"]]
        equivalent = row.get(preset_id)
        if equivalent is None:
            equivalent = "No canon mapping for preset %s yet. Decide and record the reason." % preset_id
            decision = "DECIDE"
        else:
            decision = "DROP" if equivalent.lower().startswith("dropped") else "MAP"
        row_widgets = row.get("widgets", {}).get(preset_id, [])
        for w in row_widgets:
            supplied.setdefault(w, []).append(row["modern_pattern"])
        detected.append({
            "id": row["id"],
            "modern_pattern": row["modern_pattern"],
            "evidence": pattern["evidence"],
            "equivalent": equivalent,
            "widgets": row_widgets,
            "decision": decision,
            "tier": row["tier"],
        })
    undetected = [r["modern_pattern"] for r in canon.mapping_rows() if r["id"] not in {d["id"] for d in detected}]
    nav = inventory["summary"].get("nav_items", [])
    cap = params["nav_cap_max"]
    nav_plan = nav[:cap - 1] + ["More Stuff!"] if len(nav) > cap else list(nav)
    overflow = nav[cap - 1:] if len(nav) > cap else []
    checklist = []
    for wid in spec["required_widgets"]:
        source = supplied.get(wid)
        checklist.append({
            "widget": wid,
            "label": widgets[wid]["label"],
            "source": ", ".join(source) if source else "lived-in addition (no modern source)",
        })
    for group in spec.get("required_any", []):
        checklist.append({"widget": " or ".join(group), "label": "one of these", "source": "pick one"})
    colors = []
    if spec["palette_mode"] in ("web-safe-216", "theme", "browser-default"):
        for c in inventory["brand"]["colors"][:8]:
            snap = color.snap(color.parse_hex(c["hex"]), params["websafe_perceptual_switch_delta_e"])
            colors.append(dict(snap, count=c["count"], neutral=c["neutral"]))
    fonts_canon = {c["id"]: c["stacks"] for c in canon.load("fonts")["categories"]}
    fonts = [{"family": f["family"], "category": f["category"], "era_stack": fonts_canon[f["category"]][preset_id]}
             for f in inventory["brand"]["fonts"]]
    headings = [h["text"] for p in inventory["pages"] for h in p["headings"]][:24]
    ctas = []
    for p in inventory["pages"]:
        for c in p["ctas"]:
            if c["text"] not in ctas:
                ctas.append(c["text"])
    return {
        "preset": preset_id,
        "preset_name": spec.get("preset_name", ""),
        "year": spec["year"],
        "canvas_width_px": spec["canvas_width_px"],
        "brand": inventory["brand"]["name_guess"],
        "detected": detected,
        "undetected": undetected,
        "nav_source": nav,
        "nav_plan": nav_plan,
        "nav_overflow": overflow,
        "widget_checklist": checklist,
        "colors": colors,
        "fonts": fonts,
        "copy_seeds": {"headings": headings, "ctas": ctas[:16], "voice_rules": spec["voice_rules"]},
    }


def to_markdown(m):
    out = []
    out.append("---")
    out.append("title: \"Component mapping worksheet\"")
    out.append("preset: \"%s\"" % m["preset"])
    out.append("generated_by: tools/map.py")
    out.append("---")
    out.append("")
    out.append("# Component mapping: %s as preset %s (%s)" % (m["brand"], m["preset"], m["year"]))
    out.append("")
    out.append("Canvas: %s px. Confirm or override every decision. Allowed decisions: MAP, MERGE (name the target row), DROP (give a reason)." % m["canvas_width_px"])
    out.append("")
    out.append("## Detected patterns")
    out.append("")
    out.append("| Modern pattern | Evidence | Period equivalent | Widgets | Decision | Notes |")
    out.append("|---|---|---|---|---|---|")
    for d in m["detected"]:
        out.append("| %s | %s | %s | %s | %s | |" % (
            d["modern_pattern"], "<br>".join(d["evidence"][:3]), d["equivalent"],
            ", ".join(d["widgets"]) or "none", d["decision"]))
    out.append("")
    out.append("Not detected (check by eye before dropping): " + (", ".join(m["undetected"]) or "none") + ".")
    out.append("")
    out.append("## Navigation plan")
    out.append("")
    out.append("Source navigation: " + (", ".join(m["nav_source"]) or "none found") + ".")
    out.append("")
    out.append("Period navigation (cap applied): " + (" | ".join(m["nav_plan"]) or "define by hand") + ".")
    if m["nav_overflow"]:
        out.append("")
        out.append("Overflow moved to a More Stuff! or Site Map page: " + ", ".join(m["nav_overflow"]) + ".")
    out.append("")
    out.append("## Required widget checklist")
    out.append("")
    out.append("| Widget | Label | Supplied by | Placed on page |")
    out.append("|---|---|---|---|")
    for w in m["widget_checklist"]:
        out.append("| %s | %s | %s | |" % (w["widget"], w["label"], w["source"]))
    out.append("")
    if m["colors"]:
        out.append("## Color plan (web-safe snap)")
        out.append("")
        out.append("| Original | Snapped | Method | Delta E | Uses in source |")
        out.append("|---|---|---|---|---|")
        for c in m["colors"]:
            out.append("| %s | %s | %s | %.2f | %d |" % (c["original"], c["snapped"], c["method"], c["delta_e"], c["count"]))
        out.append("")
    out.append("## Font plan")
    out.append("")
    out.append("| Source family | Category | Era stack |")
    out.append("|---|---|---|")
    for f in m["fonts"] or [{"family": "none detected", "category": "sans", "era_stack": "use preset body stack"}]:
        out.append("| %s | %s | %s |" % (f["family"], f["category"], f["era_stack"]))
    out.append("")
    out.append("## Copy deck seeds")
    out.append("")
    out.append("Voice rules:")
    out.append("")
    for rule in m["copy_seeds"]["voice_rules"]:
        out.append("- " + rule)
    out.append("")
    out.append("| Source heading or CTA | Era rewrite |")
    out.append("|---|---|")
    for text in m["copy_seeds"]["headings"] + m["copy_seeds"]["ctas"]:
        out.append("| %s | |" % text.replace("|", "/"))
    out.append("")
    return "\n".join(out)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build the HOMESTEAD component mapping worksheet.")
    parser.add_argument("inventory")
    parser.add_argument("--spec", help="era spec JSON (02-era-spec.json)")
    parser.add_argument("--preset", help="preset id when no spec exists yet")
    parser.add_argument("--out")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of Markdown")
    args = parser.parse_args(argv)
    with open(args.inventory, "r", encoding="utf-8") as handle:
        inventory = json.load(handle)
    if args.spec:
        with open(args.spec, "r", encoding="utf-8") as handle:
            spec = json.load(handle)
    elif args.preset:
        spec = canon.era_spec_from_preset(args.preset.upper())
    else:
        parser.error("give --spec or --preset")
    result = build(inventory, spec)
    payload = json.dumps(result, indent=2, ensure_ascii=False) + "\n" if args.json else to_markdown(result)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(payload)
        print("wrote %s: %d detected patterns, %d required widgets" % (args.out, len(result["detected"]), len(result["widget_checklist"])))
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
