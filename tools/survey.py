#!/usr/bin/env python3
"""survey: inventory a modern website for a HOMESTEAD redesign (Phase 1).

Reads a URL or a saved HTML file, extracts navigation, headings, CTAs, forms,
images, embeds, scripts, brand colors, and font families, and detects modern
patterns using the signals in canon/mapping.json. Output validates against
schemas/inventory.schema.json.

Usage:
    python3 tools/survey.py https://example.com --pages 6 --out inventory.json
    python3 tools/survey.py saved-page.html --out inventory.json

URL mode fetches same-origin pages linked from the navigation (up to --pages,
maximum 10) and up to six same-origin stylesheets. It sends a plain
User-Agent, honors timeouts, and never submits forms. If a site blocks
automated fetches, save the page from a browser and pass the file instead.

Stdlib only.
"""

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from collections import Counter, OrderedDict
from html.parser import HTMLParser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hs_core import canon, color, htmlscan  # noqa: E402

USER_AGENT = "HOMESTEAD-survey/1.0 (+https://github.com/PolymathWizard/BHIL-HOMESTEAD)"
HEX_RE = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
RGB_RE = re.compile(r"rgba?\(\s*(\d{1,3})[\s,]+(\d{1,3})[\s,]+(\d{1,3})")
FONT_RE = re.compile(r"font-family\s*:\s*([^;}\"]+)", re.I)
GFONT_RE = re.compile(r"fonts\.googleapis\.com/css2?\?([^\"'>\s]+)", re.I)
CTA_CLASS_RE = re.compile(r"\b(btn|button|cta)\b", re.I)
GENERIC_FAMILIES = {"serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui", "inherit",
                    "initial", "ui-sans-serif", "ui-serif", "ui-monospace", "-apple-system", "blinkmacsystemfont"}
FONT_PRIORITY = ["mono", "playful", "display", "sans", "serif"]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.lang = ""
        self.meta = {}
        self.headings = []
        self.nav_links = []
        self.footer_links = []
        self.links = []
        self.ctas = []
        self.forms = []
        self.images = []
        self.embeds = []
        self.script_srcs = []
        self.inline_scripts = []
        self.stylesheets = []
        self._ctx = Counter()
        self._heading = None
        self._anchor = None
        self._button = None
        self._form = None
        self._in_title = False
        self._in_script = False
        self._script_buf = []

    def handle_starttag(self, tag, attrs):
        a = dict((k.lower(), v or "") for k, v in attrs)
        if tag in ("nav", "header", "footer"):
            self._ctx[tag] += 1
        if tag == "html" and a.get("lang"):
            self.lang = a["lang"]
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            key = (a.get("name") or a.get("property") or "").lower()
            if key:
                self.meta[key] = a.get("content", "")
        elif tag == "link" and "stylesheet" in a.get("rel", "").lower():
            self.stylesheets.append(a.get("href", ""))
        elif tag in ("h1", "h2", "h3"):
            self._heading = {"level": int(tag[1]), "text": ""}
        elif tag == "a":
            self._anchor = {"text": "", "href": a.get("href", ""), "cls": a.get("class", ""), "label": a.get("aria-label", "")}
        elif tag == "button":
            self._button = {"text": "", "label": a.get("aria-label", "")}
        elif tag == "form":
            self._form = {"action": a.get("action", ""), "inputs": [], "role": a.get("role", "")}
        elif tag == "input":
            itype = a.get("type", "text").lower()
            if self._form is not None:
                self._form["inputs"].append(itype)
            if itype in ("submit", "button") and a.get("value"):
                self.ctas.append({"text": a["value"], "href": "", "kind": "input"})
        elif tag == "img":
            self.images.append({"src": a.get("src", ""), "alt": a.get("alt", ""), "width": a.get("width", ""), "height": a.get("height", "")})
        elif tag in ("iframe", "video", "source") and a.get("src"):
            self.embeds.append(a["src"])
        elif tag == "script":
            self._in_script = True
            self._script_buf = []
            if a.get("src"):
                self.script_srcs.append(a["src"])

    def handle_endtag(self, tag):
        if tag in ("nav", "header", "footer") and self._ctx[tag]:
            self._ctx[tag] -= 1
        if tag == "title":
            self._in_title = False
        elif tag in ("h1", "h2", "h3") and self._heading is not None:
            self._heading["text"] = " ".join(self._heading["text"].split())
            if self._heading["text"]:
                self.headings.append(self._heading)
            self._heading = None
        elif tag == "a" and self._anchor is not None:
            text = " ".join(self._anchor["text"].split()) or self._anchor["label"]
            link = {"text": text, "href": self._anchor["href"]}
            self.links.append(link)
            if self._ctx["nav"] or self._ctx["header"]:
                self.nav_links.append(link)
            if self._ctx["footer"]:
                self.footer_links.append(link)
            if CTA_CLASS_RE.search(self._anchor["cls"]) and text:
                self.ctas.append({"text": text, "href": self._anchor["href"], "kind": "link"})
            self._anchor = None
        elif tag == "button" and self._button is not None:
            text = " ".join(self._button["text"].split()) or self._button["label"]
            if text:
                self.ctas.append({"text": text, "href": "", "kind": "button"})
            self._button = None
        elif tag == "form" and self._form is not None:
            self.forms.append(self._form)
            self._form = None
        elif tag == "script":
            if self._script_buf:
                self.inline_scripts.append("".join(self._script_buf))
            self._in_script = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_script:
            self._script_buf.append(data)
            return
        if self._heading is not None:
            self._heading["text"] += data
        if self._anchor is not None:
            self._anchor["text"] += data
        if self._button is not None:
            self._button["text"] += data


def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, errors="replace")


def form_purpose(form):
    inputs = form["inputs"]
    if "password" in inputs:
        return "login"
    if "search" in inputs or form.get("role") == "search":
        return "search"
    if "email" in inputs and len([i for i in inputs if i not in ("hidden", "submit", "button")]) <= 2:
        return "newsletter"
    return "contact"


def classify_font(family):
    low = family.lower()
    cats = {c["id"]: c["detect"] for c in canon.load("fonts")["categories"]}
    for cat in FONT_PRIORITY:
        if any(token in low for token in cats[cat]):
            return cat
    return "sans"


def extract_fonts(css_text, markup):
    found = OrderedDict()
    for match in FONT_RE.finditer(css_text):
        for raw in match.group(1).split(","):
            name = raw.strip().strip("'\"").strip()
            if name and name.lower() not in GENERIC_FAMILIES and not name.startswith("var("):
                found.setdefault(name, 0)
                found[name] += 1
                break
    for match in GFONT_RE.finditer(markup):
        query = urllib.parse.parse_qs(match.group(1).replace("&amp;", "&"))
        for fam in query.get("family", []):
            name = fam.split(":")[0].replace("+", " ")
            found.setdefault(name, 0)
            found[name] += 1
    return [{"family": name, "category": classify_font(name), "count": count} for name, count in found.items()]


def extract_colors(css_text):
    counts = Counter()
    for match in HEX_RE.finditer(css_text):
        counts[color.to_hex(color.parse_hex(match.group(0)))] += 1
    for match in RGB_RE.finditer(css_text):
        rgb = tuple(min(255, int(v)) for v in match.groups())
        counts[color.to_hex(rgb)] += 1
    rows = []
    for hexv, count in counts.items():
        r, g, b = color.parse_hex(hexv)
        neutral = max(r, g, b) - min(r, g, b) < 24
        rows.append({"hex": hexv, "count": count, "neutral": neutral, "websafe": color.is_websafe((r, g, b))})
    rows.sort(key=lambda row: (row["neutral"], -row["count"], row["hex"]))
    return rows[:16]


def tone_notes(text):
    notes = []
    sentences = [s for s in re.split(r"[.!?]+\s", text) if s.strip()]
    words = text.split()
    if sentences:
        notes.append("average sentence length %d words" % round(len(words) / len(sentences)))
    you = sum(1 for w in words if w.lower().strip(",.!?") in ("you", "your", "you're"))
    if words:
        notes.append("second person share %.1f percent" % (100.0 * you / len(words)))
    if text.count("!"):
        notes.append("%d exclamation marks" % text.count("!"))
    buzz = re.findall(r"\b(seamless(?:ly)?|supercharge|unlock|ai-powered|effortless(?:ly)?|all-in-one|level up|get started|book a demo)\b", text, re.I)
    if buzz:
        notes.append("modern marketing phrases: " + ", ".join(sorted(set(b.lower() for b in buzz))))
    if re.search("[\U0001F000-\U0001FAFF]", text):
        notes.append("emoji present")
    return notes


def detect_patterns(pages_raw):
    rows = canon.mapping_rows()
    found = []
    for row in rows:
        evidence = []
        for kind in ("html", "text", "href", "script", "css"):
            for pattern in row["detect"].get(kind, []):
                rx = re.compile(pattern, re.I | re.S)
                for raw in pages_raw:
                    hay = raw[kind]
                    if rx.search(hay):
                        evidence.append("%s:%s" % (kind, pattern))
                        break
        if evidence:
            found.append({"id": row["id"], "modern_pattern": row["modern_pattern"], "evidence": evidence})
    return found


def survey_page(markup, base, mode):
    parser = PageParser()
    parser.feed(markup)
    parser.close()
    css_parts = [htmlscan.css_sources(markup)]
    for href in parser.stylesheets[:6]:
        if "fonts.googleapis" in href:
            continue
        if mode == "url":
            target = urllib.parse.urljoin(base, href)
            if urllib.parse.urlparse(target).netloc == urllib.parse.urlparse(base).netloc:
                try:
                    css_parts.append(fetch(target))
                except Exception:  # noqa: BLE001 - a missing stylesheet must not stop the survey
                    pass
        else:
            path = os.path.join(os.path.dirname(base), href)
            if os.path.isfile(path):
                with open(path, "r", encoding="utf-8", errors="replace") as handle:
                    css_parts.append(handle.read())
    css_text = "\n".join(css_parts)
    text = htmlscan.visible_text(markup)
    page = OrderedDict()
    page["url"] = base
    page["title"] = " ".join(parser.title.split())
    page["lang"] = parser.lang
    page["meta_description"] = parser.meta.get("description", "")
    page["headings"] = parser.headings
    page["nav_links"] = parser.nav_links
    page["footer_links"] = parser.footer_links
    page["ctas"] = parser.ctas
    page["forms"] = [dict(f, purpose=form_purpose(f)) for f in parser.forms]
    page["images"] = parser.images
    page["embeds"] = parser.embeds
    page["scripts"] = parser.script_srcs
    page["word_count"] = len(text.split())
    raw = {
        "html": htmlscan.strip_comments(markup),
        "text": text,
        "href": "\n".join(link["href"] for link in parser.links),
        "script": "\n".join(parser.script_srcs + parser.inline_scripts),
        "css": css_text,
    }
    return page, raw, parser


def survey(target, max_pages=1):
    mode = "url" if re.match(r"https?://", target) else "file"
    if mode == "file":
        with open(target, "r", encoding="utf-8", errors="replace") as handle:
            queue = [(target, handle.read())]
    else:
        queue = [(target, fetch(target))]
    pages, raws, parsers = [], [], []
    seen = {target}
    while queue and len(pages) < max_pages:
        base, markup = queue.pop(0)
        page, raw, parser = survey_page(markup, base, mode)
        pages.append(page)
        raws.append(raw)
        parsers.append(parser)
        if mode == "url" and len(pages) < max_pages:
            for link in parser.nav_links:
                nxt = urllib.parse.urljoin(base, link["href"]).split("#")[0]
                if urllib.parse.urlparse(nxt).netloc != urllib.parse.urlparse(target).netloc or nxt in seen:
                    continue
                seen.add(nxt)
                try:
                    queue.append((nxt, fetch(nxt)))
                except Exception:  # noqa: BLE001 - skip unreachable pages, keep surveying
                    continue
                if len(queue) + len(pages) >= max_pages:
                    break
    all_css = "\n".join(r["css"] for r in raws)
    all_html = "\n".join(r["html"] for r in raws)
    fonts = extract_fonts(all_css, all_html)
    first = parsers[0]
    name = first.meta.get("og:site_name") or re.split(r"\s[|\-:]\s", pages[0]["title"] or "Untitled")[0]
    logos = [img["src"] for img in pages[0]["images"] if "logo" in (img["src"] + img["alt"]).lower()][:4]
    patterns = detect_patterns(raws)
    nav_texts = []
    for p in pages:
        for link in p["nav_links"]:
            if link["text"] and link["text"] not in nav_texts:
                nav_texts.append(link["text"])
    inventory = OrderedDict()
    inventory["homestead_version"] = canon.load("homestead")["version"]
    inventory["source"] = {"input": target, "mode": mode, "fetched_pages": len(pages)}
    inventory["pages"] = pages
    inventory["brand"] = {
        "name_guess": name.strip(),
        "colors": extract_colors(all_css),
        "fonts": fonts,
        "web_fonts_loaded": bool(re.search(r"@font-face|fonts\.googleapis|use\.typekit", all_css + all_html, re.I)),
        "logo_candidates": logos,
    }
    inventory["patterns"] = patterns
    inventory["summary"] = {
        "page_count": len(pages),
        "pattern_count": len(patterns),
        "nav_item_count": len(nav_texts),
        "nav_items": nav_texts,
        "tone_notes": tone_notes(" ".join(r["text"] for r in raws)),
    }
    return inventory


def main(argv=None):
    parser = argparse.ArgumentParser(description="Inventory a modern site for a HOMESTEAD redesign.")
    parser.add_argument("target", help="URL or saved HTML file")
    parser.add_argument("--pages", type=int, default=1, help="pages to survey in URL mode (max 10)")
    parser.add_argument("--out", help="write inventory JSON here instead of stdout")
    args = parser.parse_args(argv)
    inventory = survey(args.target, max(1, min(10, args.pages)))
    payload = json.dumps(inventory, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(payload)
        print("wrote %s: %d pages, %d patterns, %d colors, %d fonts" % (
            args.out, inventory["summary"]["page_count"], inventory["summary"]["pattern_count"],
            len(inventory["brand"]["colors"]), len(inventory["brand"]["fonts"])))
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
