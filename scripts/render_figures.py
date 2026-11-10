#!/usr/bin/env python3
"""render_figures: render the figure kit's static PNGs (ADR-009).

Renders frame zero of every assets/figures/hs-NN-*.svg at 1600 x 900 with the
BHIL brand fonts, writes assets/figures/png/hs-NN-*.png, and records the hash
of each source SVG in assets/figures/png/SOURCES.sha256. scripts/validate.py
compares those hashes with the current SVGs and fails when a PNG is stale.

This is the one HOMESTEAD script that is not stdlib only. It needs Playwright
for Python and a Chromium or Chrome browser:

    pip install playwright && python3 -m playwright install chromium

Brand fonts come from the system, or from a folder of fontsource-style WOFF2
files named <family>-latin-<weight>-<style>.woff2 (for example
newsreader-latin-400-italic.woff2):

    python3 scripts/render_figures.py
    python3 scripts/render_figures.py --fonts ~/fonts/node_modules/@fontsource
    python3 scripts/render_figures.py --chrome /usr/bin/google-chrome
    python3 scripts/render_figures.py --allow-fallback   # render even if a brand font is missing

Exit codes: 0 rendered, 1 a brand font is missing or rendering failed, 2 Playwright is not installed.
"""

import argparse
import asyncio
import hashlib
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
FIG_DIR = os.path.join(ROOT, "assets", "figures")
PNG_DIR = os.path.join(FIG_DIR, "png")
FIGURE_RE = re.compile(r"^hs-\d\d-[a-z0-9-]+\.svg$")
FAMILIES = {"newsreader": "Newsreader", "ibm-plex-mono": "IBM Plex Mono", "ibm-plex-sans": "IBM Plex Sans"}
FACE_RE = re.compile(r"^(newsreader|ibm-plex-mono|ibm-plex-sans)-latin-(\d{3})-(normal|italic)\.woff2$")
# A face counts as present when the page's font set loads it (--fonts) or when
# the system font changes text metrics against both generic fallbacks.
FONT_PROBE = """s => document.fonts.load(s).then(f => f.length > 0, () => false).then(ok => {
  if (ok) return true;
  const c = document.createElement('canvas').getContext('2d');
  const t = 'HOMESTEAD retro-web 0123 ilWM';
  const fam = s.match(/"([^"]+)"/)[1];
  return ['monospace', 'serif'].some(base => {
    c.font = '32px ' + base; const a = c.measureText(t).width;
    c.font = '32px "' + fam + '", ' + base; return c.measureText(t).width !== a;
  });
})"""
REQUIRED = ('400 16px "Newsreader"', 'italic 400 16px "Newsreader"', '400 16px "IBM Plex Mono"', '400 16px "IBM Plex Sans"')


def figure_files():
    return sorted(n for n in os.listdir(FIG_DIR) if FIGURE_RE.match(n))


def sha256(path):
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def font_faces(fonts_dir):
    if not fonts_dir:
        return ""
    faces = []
    for root, _dirs, names in os.walk(os.path.expanduser(fonts_dir)):
        for name in sorted(names):
            m = FACE_RE.match(name)
            if m:
                faces.append("@font-face{font-family:'%s';font-style:%s;font-weight:%s;src:url('file://%s')}" % (
                    FAMILIES[m.group(1)], m.group(3), m.group(2), os.path.join(root, name)))
    return "\n".join(faces)


async def render(args):
    from playwright.async_api import async_playwright

    os.makedirs(PNG_DIR, exist_ok=True)
    faces = font_faces(args.fonts)
    lines = []
    async with async_playwright() as p:
        launch = {"args": ["--no-sandbox", "--allow-file-access-from-files"]}
        if args.chrome:
            launch["executable_path"] = args.chrome
        browser = await p.chromium.launch(**launch)
        page = await browser.new_page(viewport={"width": 1600, "height": 900})
        for name in figure_files():
            src = os.path.join(FIG_DIR, name)
            with open(src, "r", encoding="utf-8") as handle:
                svg = handle.read()
            html = ("<!DOCTYPE html><html><head><meta charset='utf-8'><style>%s\n"
                    "html,body{margin:0;background:#0D1B2E}svg{display:block}"
                    "*{animation:none!important}</style></head><body>%s</body></html>") % (faces, svg)
            tmp = os.path.join(PNG_DIR, ".render.html")
            with open(tmp, "w", encoding="utf-8") as handle:
                handle.write(html)
            try:
                await page.goto("file://" + tmp)
            finally:
                os.remove(tmp)
            await page.evaluate("document.fonts.ready")
            missing = []
            for spec in REQUIRED:
                loaded = await page.evaluate(FONT_PROBE, spec)
                if not loaded:
                    missing.append(spec)
            if missing and not args.allow_fallback:
                await browser.close()
                print("render_figures: brand font missing (%s). Install it or pass --fonts; --allow-fallback renders anyway." % ", ".join(missing))
                return 1
            await page.wait_for_timeout(200)
            out = os.path.join(PNG_DIR, name[:-4] + ".png")
            await page.screenshot(path=out, clip={"x": 0, "y": 0, "width": 1600, "height": 900})
            lines.append("%s  %s" % (sha256(src), name))
            print("rendered " + os.path.relpath(out, ROOT))
        await browser.close()
    with open(os.path.join(PNG_DIR, "SOURCES.sha256"), "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines) + "\n")
    print("render_figures: %d PNGs rendered" % len(lines))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Render the HOMESTEAD figure kit to PNG.")
    parser.add_argument("--fonts", help="folder of fontsource-style brand WOFF2 files")
    parser.add_argument("--chrome", help="path to a Chrome or Chromium executable")
    parser.add_argument("--allow-fallback", action="store_true", help="render even when a brand font is missing")
    args = parser.parse_args(argv)
    try:
        import playwright  # noqa: F401
    except ImportError:
        print("render_figures: Playwright is not installed. pip install playwright && python3 -m playwright install chromium")
        return 2
    return asyncio.run(render(args))


if __name__ == "__main__":
    sys.exit(main())
