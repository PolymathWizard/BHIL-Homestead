#!/usr/bin/env python3
"""validate: the HOMESTEAD repository quality gate.

Checks, in order:
  1. Dash gate: no em or en dash bytes (or their HTML entities) in any text file.
  2. Every JSON file parses.
  3. Canon integrity: presets, widgets, mapping, rubric, lint rules, claims,
     process, and agents reference each other consistently.
  4. Counts are code: expected counts below must match canon. Change a count
     and its expectation in the same commit.
  5. Schemas: era spec cards, example specs, inventory, and scorecards validate.
  6. Agent tool isolation: .claude/agents/*.md tools match canon/agents.json.
  7. Kits and example builds pass era_lint strict and gif_audit; example
     scorecards score SHIP.
  8. Frontmatter on every Markdown file in content folders.
  9. Relative Markdown links resolve.
 10. Required root files exist; launch copy obeys its limits.

Usage:
    python3 scripts/validate.py

Exit codes: 0 PASS, 1 FAIL. Stdlib only.
"""

import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import era_lint  # noqa: E402
import gif_audit  # noqa: E402
import rubric  # noqa: E402
from hs_core import canon, color, schema  # noqa: E402

EXPECTED = {
    "presets": 6,
    "kit_presets": 3,
    "widgets": 44,
    "mapping_rows": 24,
    "rubric_rows": 20,
    "rubric_max": 40,
    "lint_rules": 28,
    "techniques": 15,
    "claims": 43,
    "phases": 7,
    "agents": 6,
    "prompts": 11,
    "adrs": 8,
    "example_builds": 3,
}

SKIP_DIRS = {".git", "site", "site-src", "__pycache__", "node_modules"}
BINARY_EXT = {".gif", ".png", ".jpg", ".jpeg", ".wav", ".mid", ".ico", ".zip", ".gz", ".bundle", ".pdf"}
DASH_BYTES = (b"\xe2\x80\x93", b"\xe2\x80\x94")
DASH_ENTITIES = tuple(b"&" + name for name in (b"mdash;", b"ndash;", b"#8211;", b"#8212;"))  # built so this file passes its own gate
FRONTMATTER_DIRS = ("docs", "support", "adr", "prompts", "kits", ".claude/agents", ".claude/commands", "skill", "launch")
REQUIRED_ROOT = ("README.md", "LICENSE", "LICENSE-CONTENT", "CONTRIBUTING.md", "CHANGELOG.md", "CITATION.cff", "AGENTS.md",
                 "CLAUDE.md", "SECURITY.md", "CODE_OF_CONDUCT.md", "mkdocs.yml", ".gitignore", "engagements/.gitkeep",
                 "requirements-docs.txt")
TAGLINE = "Human-Directed. AI-Enabled. Commercially Tested."
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


class Gate:
    def __init__(self):
        self.failures = []
        self.passes = 0

    def check(self, ok, message):
        if ok:
            self.passes += 1
        else:
            self.failures.append(message)


def walk_files():
    for root, dirs, names in os.walk(ROOT):
        rel_root = os.path.relpath(root, ROOT).replace(os.sep, "/")
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not (rel_root == "." and d == "engagements"))
        for name in sorted(names):
            yield os.path.relpath(os.path.join(root, name), ROOT).replace(os.sep, "/")


def dash_gate(g):
    for rel in walk_files():
        if os.path.splitext(rel)[1].lower() in BINARY_EXT:
            continue
        with open(os.path.join(ROOT, rel), "rb") as handle:
            data = handle.read()
        hits = [b for b in DASH_BYTES + DASH_ENTITIES if b in data]
        g.check(not hits, "dash gate: %s contains %s" % (rel, ", ".join(repr(h) for h in hits)))


def json_gate(g):
    for rel in walk_files():
        if rel.endswith(".json"):
            try:
                with open(os.path.join(ROOT, rel), "r", encoding="utf-8") as handle:
                    json.load(handle)
                g.check(True, "")
            except ValueError as exc:
                g.check(False, "json: %s does not parse (%s)" % (rel, exc))


def canon_gate(g):
    presets = canon.presets()
    widgets = canon.widget_index()
    sources = {s["id"] for s in canon.load("sources")["sources"]}
    claims = {c["id"]: c for c in canon.load("sources")["claims"]}
    tiers = set(canon.load("sources")["tiers"])
    lint_rules = canon.load("lint-rules")["rules"]
    lint_ids = [r["id"] for r in lint_rules]
    g.check(len(set(lint_ids)) == len(lint_ids), "canon: duplicate lint rule ids")
    g.check(len(widgets) == len(canon.widgets()), "canon: duplicate widget ids")
    ids = [p["id"] for p in presets]
    g.check(ids == list("ABCDEF"), "canon: presets must be A to F in order, got %s" % ids)
    for p in presets:
        allowed = canon.allowed_widgets(p["id"])
        for wid in p["required_widgets"]:
            g.check(wid in allowed, "canon: preset %s requires %s which it does not allow" % (p["id"], wid))
        for group in p.get("required_any", []):
            for wid in group:
                g.check(wid in allowed, "canon: preset %s required_any names %s which it does not allow" % (p["id"], wid))
        g.check("safe-mode-toggle" in p["required_widgets"], "canon: preset %s must require safe-mode-toggle" % p["id"])
        for sid in p["reference_sources"]:
            g.check(sid in sources, "canon: preset %s cites unknown source %s" % (p["id"], sid))
        if p["status"] == "kit":
            g.check(p["kit"] and os.path.isdir(os.path.join(ROOT, p["kit"])), "canon: kit folder missing for preset %s" % p["id"])
        for role, hexv in p["palette"].items():
            if p["palette_mode"] == "web-safe-216":
                g.check(color.is_websafe(color.parse_hex(hexv)), "canon: preset %s palette %s %s is not web-safe" % (p["id"], role, hexv))
        for cid in re.findall(r"C-\d{3}", json.dumps(p)):
            g.check(cid in claims, "canon: preset %s cites unknown claim %s" % (p["id"], cid))
    for row in canon.mapping_rows():
        for pid in "BCE":
            g.check(pid in row, "canon: mapping row %s lacks preset %s" % (row["id"], pid))
            for wid in row["widgets"].get(pid, []):
                g.check(wid in canon.allowed_widgets(pid), "canon: mapping row %s maps %s to %s, not a preset %s widget" % (row["id"], pid, wid, pid))
        for kind, pats in row["detect"].items():
            for pat in pats:
                try:
                    re.compile(pat)
                except re.error as exc:
                    g.check(False, "canon: mapping %s regex %r fails (%s)" % (row["id"], pat, exc))
    rub = canon.load("rubric")
    g.check([r["row"] for r in rub["rows"]] == list(range(1, 21)), "canon: rubric rows must be 1 to 20")
    g.check(rub["max_score"] == 2 * len(rub["rows"]), "canon: rubric max must equal twice the row count")
    for r in rub["rows"]:
        for lid in r["lint"]:
            g.check(lid in lint_ids, "canon: rubric row %d names unknown lint rule %s" % (r["row"], lid))
    for r in lint_rules:
        if r["pattern"]:
            try:
                re.compile(r["pattern"])
            except re.error as exc:
                g.check(False, "canon: lint %s regex fails (%s)" % (r["id"], exc))
        g.check(set(r["applies"]) <= set("ABCDEF"), "canon: lint %s applies to unknown preset" % r["id"])
        g.check(1 <= r["rubric_row"] <= 20, "canon: lint %s points at rubric row %s" % (r["id"], r["rubric_row"]))
    for c in claims.values():
        g.check(c["tier"] in tiers, "canon: claim %s has unknown tier %s" % (c["id"], c["tier"]))
        for sid in c["sources"]:
            g.check(sid in sources, "canon: claim %s cites unknown source %s" % (c["id"], sid))
        if c["tier"] == "CORROBORATED":
            g.check(len(c["sources"]) >= 2, "canon: claim %s is CORROBORATED with fewer than two sources" % c["id"])
    for t in canon.load("techniques")["techniques"]:
        for cid in t["claims"]:
            g.check(cid in claims, "canon: technique %s cites unknown claim %s" % (t["id"], cid))
    proc = canon.load("process")["phases"]
    g.check([p["id"] for p in proc] == list(range(7)), "canon: phases must be 0 to 6")
    agent_names = {a["name"] for a in canon.load("agents")["agents"]} | {"orchestrator"}
    for ph in proc:
        g.check(ph["agent"] in agent_names, "canon: phase %d owner %s is not an agent" % (ph["id"], ph["agent"]))
        g.check(os.path.isfile(os.path.join(ROOT, "prompts", "%s.md" % prompt_file(ph["prompt"]))), "canon: phase %d prompt %s missing" % (ph["id"], ph["prompt"]))
        for tool in ph["tools"]:
            g.check(os.path.isfile(os.path.join(ROOT, tool)), "canon: phase %d tool %s missing" % (ph["id"], tool))


def prompt_file(pid):
    for name in os.listdir(os.path.join(ROOT, "prompts")):
        if name.startswith(pid + "-") and name.endswith(".md"):
            return name[:-3]
    return pid


def counts_gate(g):
    actual = {
        "presets": len(canon.presets()),
        "kit_presets": sum(1 for p in canon.presets() if p["status"] == "kit"),
        "widgets": len(canon.widgets()),
        "mapping_rows": len(canon.mapping_rows()),
        "rubric_rows": len(canon.load("rubric")["rows"]),
        "rubric_max": canon.load("rubric")["max_score"],
        "lint_rules": len(canon.load("lint-rules")["rules"]),
        "techniques": len(canon.load("techniques")["techniques"]),
        "claims": len(canon.load("sources")["claims"]),
        "phases": len(canon.load("process")["phases"]),
        "agents": len(canon.load("agents")["agents"]),
        "prompts": len([n for n in os.listdir(os.path.join(ROOT, "prompts")) if re.match(r"P\d\d-.*\.md$", n)]),
        "adrs": len([n for n in os.listdir(os.path.join(ROOT, "adr")) if re.match(r"ADR-\d{3}-.*\.md$", n)]),
        "example_builds": sum(len(os.listdir(os.path.join(ROOT, "examples", e, "builds")))
                              for e in os.listdir(os.path.join(ROOT, "examples"))
                              if os.path.isdir(os.path.join(ROOT, "examples", e, "builds"))),
    }
    for key, want in EXPECTED.items():
        g.check(actual[key] == want, "counts: %s is %s, expected %s" % (key, actual[key], want))


def load_schema(name):
    with open(os.path.join(ROOT, "schemas", name), "r", encoding="utf-8") as handle:
        return json.load(handle)


def schema_gate(g):
    era = load_schema("era-spec.schema.json")
    inv = load_schema("inventory.schema.json")
    card = load_schema("scorecard.schema.json")
    for rel in walk_files():
        if rel.startswith("templates/era-spec-cards/") or rel.endswith("/era-spec.json"):
            with open(os.path.join(ROOT, rel), "r", encoding="utf-8") as handle:
                errs = schema.validate(json.load(handle), era)
            g.check(not errs, "schema: %s: %s" % (rel, "; ".join(errs[:3])))
        if rel.endswith("/inventory.json"):
            with open(os.path.join(ROOT, rel), "r", encoding="utf-8") as handle:
                errs = schema.validate(json.load(handle), inv)
            g.check(not errs, "schema: %s: %s" % (rel, "; ".join(errs[:3])))
        if rel == "templates/scorecard.json" or re.search(r"qa/scorecard-[A-F]\.json$", rel):
            with open(os.path.join(ROOT, rel), "r", encoding="utf-8") as handle:
                errs = schema.validate(json.load(handle), card)
            g.check(not errs, "schema: %s: %s" % (rel, "; ".join(errs[:3])))


def parse_frontmatter(path):
    with open(path, "r", encoding="utf-8") as handle:
        text = handle.read()
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end < 0:
        return None
    meta = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()
    return meta, text[4:end]


def agents_gate(g):
    spec = {a["name"]: a for a in canon.load("agents")["agents"]}
    agent_dir = os.path.join(ROOT, ".claude", "agents")
    found = set()
    for name in sorted(os.listdir(agent_dir)):
        if not name.endswith(".md"):
            continue
        parsed = parse_frontmatter(os.path.join(agent_dir, name))
        g.check(parsed is not None, "agents: %s lacks frontmatter" % name)
        if not parsed:
            continue
        meta, raw = parsed
        agent = meta.get("name")
        found.add(agent)
        g.check(agent in spec, "agents: %s defines unknown agent %s" % (name, agent))
        if agent not in spec:
            continue
        tools = [t.strip() for t in meta.get("tools", "").split(",") if t.strip()]
        g.check(sorted(tools) == sorted(spec[agent]["tools"]), "agents: %s tools %s differ from canon %s" % (agent, tools, spec[agent]["tools"]))
        for bad in spec[agent]["forbidden"]:
            g.check(bad not in tools, "agents: %s has forbidden tool %s" % (agent, bad))
        g.check(meta.get("model") == spec[agent]["model"], "agents: %s model %s differs from canon" % (agent, meta.get("model")))
        _ = raw
    g.check(found == set(spec), "agents: definitions %s do not match canon %s" % (sorted(found), sorted(spec)))


def builds_gate(g):
    params = canon.params()
    targets = []
    for p in canon.presets():
        if p["kit"]:
            targets.append((p["kit"], canon.era_spec_from_preset(p["id"])))
    examples = os.path.join(ROOT, "examples")
    for ex in sorted(os.listdir(examples)):
        builds = os.path.join(examples, ex, "builds")
        if not os.path.isdir(builds):
            continue
        for b in sorted(os.listdir(builds)):
            with open(os.path.join(builds, b, "era-spec.json"), "r", encoding="utf-8") as handle:
                targets.append(("examples/%s/builds/%s" % (ex, b), json.load(handle)))
    for rel, spec in targets:
        report = era_lint.lint(os.path.join(ROOT, rel), spec)
        g.check(report["errors"] == 0 and report["warnings"] == 0,
                "builds: %s lint %s: %s" % (rel, report["verdict"], "; ".join("%s %s %s" % (f["rule"], f["file"], f["detail"]) for f in report["findings"][:4])))
        bg = color.parse_hex(spec.get("palette", {}).get("bg", "#FFFFFF"))
        for f in gif_audit.collect([os.path.join(ROOT, rel)]):
            r = gif_audit.audit_file(f, params, bg)
            g.check(not r["fail"], "builds: %s gif audit %s" % (os.path.relpath(f, ROOT), r["verdict"]))
        for name in canon.load("lint-rules")["exempt_files"]:
            with open(os.path.join(ROOT, rel, name), "rb") as a, open(os.path.join(ROOT, "kits", "safety-layer", name), "rb") as b:
                g.check(a.read() == b.read(), "builds: %s/%s differs from kits/safety-layer" % (rel, name))
    for rel in walk_files():
        m = re.search(r"^(examples/[^/]+)/qa/scorecard-([A-F])\.json$", rel)
        if not m:
            continue
        with open(os.path.join(ROOT, rel), "r", encoding="utf-8") as handle:
            card = json.load(handle)
        lint_path = os.path.join(ROOT, m.group(1), "qa", "lint-%s.json" % m.group(2))
        with open(lint_path, "r", encoding="utf-8") as handle:
            lint_report = json.load(handle)
        result = rubric.evaluate(card, lint_report)
        g.check(result["verdict"] == "SHIP", "builds: %s scores %s (%s)" % (rel, result["verdict"], result.get("total")))
        g.check(card.get("total") == result["total"] and card.get("verdict") == result["verdict"],
                "builds: %s recorded total or verdict disagrees with tools/rubric.py" % rel)


def frontmatter_gate(g):
    for rel in walk_files():
        if not rel.endswith(".md"):
            continue
        if not any(rel.startswith(d + "/") for d in FRONTMATTER_DIRS):
            continue
        g.check(parse_frontmatter(os.path.join(ROOT, rel)) is not None, "frontmatter: %s lacks YAML frontmatter" % rel)


def links_gate(g):
    for rel in walk_files():
        if not rel.endswith(".md"):
            continue
        path = os.path.join(ROOT, rel)
        with open(path, "r", encoding="utf-8") as handle:
            text = handle.read()
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        text = re.sub(r"`[^`\n]*`", "", text)
        for target in LINK_RE.findall(text):
            if re.match(r"^(https?:|mailto:|#)", target):
                continue
            clean = target.split("#")[0]
            if not clean:
                continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), clean))
            g.check(os.path.exists(resolved), "links: %s points at missing %s" % (rel, target))


def root_gate(g):
    for name in REQUIRED_ROOT:
        g.check(os.path.exists(os.path.join(ROOT, name)), "root: missing %s" % name)
    desc_path = os.path.join(ROOT, "launch", "github-descriptions.md")
    if os.path.isfile(desc_path):
        with open(desc_path, "r", encoding="utf-8") as handle:
            text = handle.read()
        blocks = re.findall(r"```text\n(.*?)\n```", text, re.S)
        g.check(len(blocks) == 3, "launch: expected three GitHub description options, found %d" % len(blocks))
        for i, block in enumerate(blocks, 1):
            g.check(len(block) <= 350, "launch: GitHub description option %d is %d characters (limit 350)" % (i, len(block)))
    posts_path = os.path.join(ROOT, "launch", "linkedin-posts.md")
    if os.path.isfile(posts_path):
        with open(posts_path, "r", encoding="utf-8") as handle:
            text = handle.read()
        posts = re.findall(r"```text\n(.*?)\n```", text, re.S)
        g.check(len(posts) == 3, "launch: expected three LinkedIn variants, found %d" % len(posts))
        for i, post in enumerate(posts, 1):
            g.check(post.rstrip().endswith(TAGLINE), "launch: LinkedIn variant %d must close with the BHIL tagline" % i)
            stripped = re.sub(r"\b(19[89]\d|200\d)\b", "", post)
            g.check(not re.search(r"\d|%", stripped), "launch: LinkedIn variant %d carries numbers; storytelling posts omit statistics" % i)


def main():
    g = Gate()
    for name, fn in (("dash", dash_gate), ("json", json_gate), ("canon", canon_gate), ("counts", counts_gate),
                     ("schema", schema_gate), ("agents", agents_gate), ("builds", builds_gate),
                     ("frontmatter", frontmatter_gate), ("links", links_gate), ("root", root_gate)):
        before = len(g.failures)
        try:
            fn(g)
        except Exception as exc:  # noqa: BLE001 - a crashing check is a failing check
            g.failures.append("%s gate crashed: %r" % (name, exc))
        print("  %-12s %s" % (name, "ok" if len(g.failures) == before else "FAIL (%d)" % (len(g.failures) - before)))
    if g.failures:
        for f in g.failures:
            print("FAIL " + f)
        print("validate: FAIL (%d failures, %d checks passed)" % (len(g.failures), g.passes))
        return 1
    print("validate: PASS (%d checks)" % g.passes)
    return 0


if __name__ == "__main__":
    sys.exit(main())
