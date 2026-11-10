"""Load the canonical sources in canon/.

Every derived artifact and every tool reads canon through this module so that
a single edit to canon/*.json propagates everywhere (ADR-001).
"""

import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
CANON_DIR = os.path.join(REPO_ROOT, "canon")

CANON_FILES = (
    "homestead",
    "presets",
    "widgets",
    "mapping",
    "rubric",
    "lint-rules",
    "techniques",
    "fonts",
    "process",
    "agents",
    "sources",
    "brand",
)

_cache = {}


def load(name, root=None):
    """Return the parsed JSON for canon/<name>.json."""
    base = os.path.join(root, "canon") if root else CANON_DIR
    key = (base, name)
    if key not in _cache:
        path = os.path.join(base, name + ".json")
        with open(path, "r", encoding="utf-8") as handle:
            _cache[key] = json.load(handle)
    return _cache[key]


def presets(root=None):
    return load("presets", root)["presets"]


def preset(preset_id, root=None):
    for item in presets(root):
        if item["id"] == preset_id:
            return item
    raise KeyError("Unknown preset: %s" % preset_id)


def widgets(root=None):
    return load("widgets", root)["widgets"]


def widget_index(root=None):
    return {w["id"]: w for w in widgets(root)}


def allowed_widgets(preset_id, root=None):
    return {w["id"] for w in widgets(root) if preset_id in w["presets"]}


def mapping_rows(root=None):
    return load("mapping", root)["rows"]


def params(root=None):
    return load("homestead", root)["parameters"]


def era_spec_from_preset(preset_id, root=None):
    """Build an era spec card prefilled from a preset."""
    p = preset(preset_id, root)
    year_lo = int(p["years"].split("-")[0])
    year_hi_text = p["years"].split("-")[1]
    year_hi = 2026 if year_hi_text == "now" else int(year_hi_text)
    year = year_lo + (year_hi - year_lo) // 2
    palette = p["palette"]
    base_bg = palette["bg"]
    if p["id"] == "B":
        base_bg = palette["bg"] + " with images/stars-tile.gif"
    return {
        "preset": p["id"],
        "preset_name": p["name"],
        "year": year,
        "host_context": p["host_context"],
        "target_browser": p["target_browser"],
        "canvas_width_px": p["canvas"]["width_px"],
        "palette_mode": p["palette_mode"],
        "base_bg": base_bg,
        "palette": palette,
        "fonts": {k: ", ".join(v) for k, v in p["fonts"].items()},
        "layout_mode": p["layout_mode"],
        "nav_style": p["nav_style"],
        "required_widgets": list(p["required_widgets"]),
        "required_any": [list(group) for group in p.get("required_any", [])],
        "forbidden_elements": list(p["forbidden_elements"]),
        "voice_rules": [p["voice"]] + ["Example: " + v for v in p["voice_examples"]],
        "motion_budget": p["motion_budget"],
        "audio": p["audio"],
        "easter_eggs": list(p["easter_eggs"]),
        "time_capsule": False,
        "time_capsule_story": "",
        "allowed_extra_widgets": [],
        "reference_urls": [],
        "asset_policy": "originals-only",
    }
