#!/usr/bin/env python3
"""figures: the HOMESTEAD figure kit (HS-01 to HS-10).

Ten 1600 x 900 animated SVG figures that put period web specimens (pixel
type, bevels, 88x31 badges, odometers, marquees) inside the BHIL instrument
frame defined by BHIL Brand Guidelines v1.0 and recorded in canon/brand.json.

Every figure is generated from canon and example data, so the drift gate
covers it (ADR-001). Animations are CSS only, slow, small in area, stop under
prefers-reduced-motion, and frame zero is the designed static frame.

Called by scripts/build_derived.py. Standalone:
    python3 scripts/figures.py --out DIR

Stdlib only.
"""

import argparse
import json
import os
import random
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import gifsmith  # noqa: E402
from hs_core import canon, color, gif, raster  # noqa: E402

W, H = 1600, 900
X0, X1 = 80, 1520


def brand():
    return canon.load("brand")


def C(name):
    return brand()["palette"][name]


def F(name):
    return brand()["type"][name]


def esc(text):
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;")


def n(v):
    """Compact number formatting for SVG attributes."""
    if isinstance(v, float):
        v = round(v, 2)
        if v == int(v):
            v = int(v)
    return str(v)


BASE_CSS = """
@keyframes hs-blink { 0%, 49.9% { opacity: 1; } 50%, 100% { opacity: 0; } }
@keyframes hs-twinkle { 0%, 100% { opacity: 0.25; } 50% { opacity: 1; } }
@keyframes hs-breathe { 0%, 100% { opacity: 1; } 50% { opacity: 0.55; } }
.hs-blink { animation: hs-blink 1s step-end infinite; }
.hs-twinkle { animation: hs-twinkle 4s ease-in-out infinite; }
.hs-breathe { animation: hs-breathe 2.4s ease-in-out infinite; }
@media (prefers-reduced-motion: reduce) { * { animation: none !important; } .hs-anim { display: none; } }
"""


class Svg:
    def __init__(self, fid, title, desc):
        self.fid = fid
        self.title = title
        self.desc = desc
        self.parts = []
        self.defs = []
        self.css = [BASE_CSS]
        _GLYPHS_USED.clear()

    def add(self, s):
        self.parts.append(s)

    def rect(self, x, y, w, h, fill="none", stroke=None, sw=1, extra=""):
        s = '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"' % (n(x), n(y), n(w), n(h), fill)
        if stroke:
            s += ' stroke="%s" stroke-width="%s"' % (stroke, n(sw))
        self.add(s + extra + "/>")

    def line(self, x1, y1, x2, y2, stroke, sw=1, extra=""):
        self.add('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s/>' % (n(x1), n(y1), n(x2), n(y2), stroke, n(sw), extra))

    def text(self, x, y, s, font="mono", size=14, fill=None, anchor="start", weight=None, track=0.0,
             opacity=None, italic=False, cls=None, length=None):
        fill = fill or C("paper")
        attrs = ['x="%s"' % n(x), 'y="%s"' % n(y), 'font-family="%s"' % F(font), 'font-size="%s"' % n(size), 'fill="%s"' % fill]
        if anchor != "start":
            attrs.append('text-anchor="%s"' % anchor)
        if weight:
            attrs.append('font-weight="%s"' % weight)
        if track:
            attrs.append('letter-spacing="%s"' % n(round(size * track, 2)))
        if opacity is not None:
            attrs.append('fill-opacity="%s"' % n(opacity))
        if italic:
            attrs.append('font-style="italic"')
        if cls:
            attrs.append('class="%s"' % cls)
        if length:
            attrs.append('textLength="%s" lengthAdjust="spacingAndGlyphs"' % n(length))
            attrs.append('xml:space="preserve"')
        self.add("<text %s>%s</text>" % (" ".join(attrs), esc(s)))

    def render(self):
        out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-labelledby="t d">' % (W, H, W, H),
               '<title id="t">%s %s</title>' % (self.fid, esc(self.title)),
               '<desc id="d">%s</desc>' % esc(self.desc),
               "<style>%s</style>" % "".join(self.css)]
        defs = "".join(self.defs) + glyph_defs()
        if defs:
            out.append("<defs>" + defs + "</defs>")
        out.append('<rect width="%d" height="%d" fill="%s"/>' % (W, H, C("terminal_navy")))
        out += self.parts
        out.append("</svg>")
        return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# Pixel helpers: the retro half of the fusion
# ---------------------------------------------------------------------------

_GLYPHS_USED = set()


def glyph_id(ch):
    return "px-%x" % ord(ch.upper() if ch.upper() in raster.GLYPHS else "?")


def glyph_defs():
    out = []
    for gid in sorted(_GLYPHS_USED):
        ch = chr(int(gid[3:], 16))
        rects = []
        for ry, bits in enumerate(raster.glyph(ch)):
            rx = 0
            while rx < 5:
                if bits[rx] == "1":
                    start = rx
                    while rx < 5 and bits[rx] == "1":
                        rx += 1
                    rects.append('<rect x="%d" y="%d" width="%d" height="1"/>' % (start, ry, rx - start))
                else:
                    rx += 1
        out.append('<g id="%s">%s</g>' % (gid, "".join(rects)))
    return "".join(out)


def pixel_text(text, x, y, s, fill, spacing=1, cls=None):
    """Pixel-font text. Each glyph is defined once per figure and reused."""
    uses = []
    cx = x
    for ch in text:
        if ch != " ":
            gid = glyph_id(ch)
            _GLYPHS_USED.add(gid)
            uses.append('<use href="#%s" transform="translate(%s %s) scale(%s)"/>' % (gid, n(cx), n(y), n(s)))
        cx += (5 + spacing) * s
    c = ' class="%s"' % cls if cls else ""
    return '<g fill="%s"%s>%s</g>' % (fill, c, "".join(uses))


def pw(text, s, spacing=1):
    return raster.text_width(text, s, spacing)


def dot_matrix(text, x, y, pitch, r, on, off, off_opacity=0.35, trailing_gap=False):
    on_dots, off_dots = [], []
    cx = x
    for i, ch in enumerate(text):
        rows = raster.glyph(ch)
        cols = 6 if (i < len(text) - 1 or trailing_gap) else 5
        for ry in range(7):
            for rx in range(cols):
                lit = rx < 5 and rows[ry][rx] == "1"
                d = '<circle cx="%s" cy="%s" r="%s"/>' % (n(cx + rx * pitch + pitch / 2.0), n(y + ry * pitch + pitch / 2.0), n(r))
                (on_dots if lit else off_dots).append(d)
        cx += 6 * pitch
    return ('<g fill="%s" fill-opacity="%s">%s</g><g fill="%s">%s</g>' % (off, n(off_opacity), "".join(off_dots), on, "".join(on_dots)))


def rgb_rects(rgb, width, height, x, y, s, skip_none=True):
    groups = {}
    order = []
    for yy in range(height):
        xx = 0
        row = rgb[yy * width:(yy + 1) * width]
        while xx < width:
            px = row[xx]
            start = xx
            while xx < width and row[xx] == px:
                xx += 1
            if px is None and skip_none:
                continue
            key = color.to_hex(px) if px is not None else "none"
            if key not in groups:
                groups[key] = []
                order.append(key)
            groups[key].append('<rect x="%s" y="%s" width="%s" height="%s"/>' % (n(x + start * s), n(y + yy * s), n((xx - start) * s), n(s)))
    return "".join('<g fill="%s">%s</g>' % (k, "".join(groups[k])) for k in order)


def gif_image(kind, params, x, y, s, pick=0):
    """Embed real gifsmith output as a pixelated data-URI image.

    Animated assets embed both the animation and its still frame; the
    animation is hidden under prefers-reduced-motion. Returns (svg, w, h).
    """
    import base64
    results = gifsmith.KINDS[kind](params)
    main = results[pick][1]
    info = gif.probe(main)
    w, h = info["width"] * s, info["height"] * s
    style = 'style="image-rendering: crisp-edges; image-rendering: pixelated"'

    def img(data, cls=""):
        return '<image x="%s" y="%s" width="%s" height="%s" %s%s href="data:image/gif;base64,%s"/>' % (
            n(x), n(y), n(w), n(h), style, cls, base64.b64encode(data).decode("ascii"))

    if info["frames"] > 1:
        still = dict(results).get("-still")
        return img(still) + img(main, ' class="hs-anim"'), w, h
    return img(main), w, h


def gif_specimen(kind, params, x, y, s, cls_prefix=None, frame_ms=None):
    """Render real gifsmith output as rects. Animated GIFs become CSS-cycled frame groups."""
    data = gifsmith.KINDS[kind](params)[0][1]
    decoded = gif.decode(data)
    frames = decoded["frames"]
    w, h = decoded["width"], decoded["height"]
    if len(frames) == 1:
        return rgb_rects(frames[0]["rgb"], w, h, x, y, s), w * s, h * s, ""
    total = len(frames)
    css = []
    parts = []
    dur = (frame_ms or frames[0]["delay_cs"] * 10) * total / 1000.0
    for i, fr in enumerate(frames):
        name = "%s-f%d" % (cls_prefix, i)
        a = 100.0 * i / total
        b = 100.0 * (i + 1) / total
        keys = []
        if i > 0:
            keys.append("0%%, %.2f%% { opacity: 0; }" % (a - 0.01))
        keys.append("%.2f%%, %.2f%% { opacity: 1; }" % (a, b - 0.01))
        if b < 100:
            keys.append("%.2f%%, 100%% { opacity: 0; }" % b)
        css.append("@keyframes %s { %s } .%s { animation: %s %ss step-end infinite; }" % (name, " ".join(keys), name, name, n(dur)))
        initial = "" if i == 0 else ' opacity="0"'
        parts.append('<g class="%s"%s>%s</g>' % (name, initial, rgb_rects(fr["rgb"], w, h, x, y, s)))
    return '<g>%s</g>' % "".join(parts), w * s, h * s, "".join(css)


def bevel(svg, x, y, w, h, light, dark, depth=2, raised=True):
    top, bottom = (light, dark) if raised else (dark, light)
    for d in range(depth):
        svg.rect(x + d, y + d, w - 2 * d, 1, top)
        svg.rect(x + d, y + d, 1, h - 2 * d, top)
        svg.rect(x + d, y + h - 1 - d, w - 2 * d, 1, bottom)
        svg.rect(x + w - 1 - d, y + d, 1, h - 2 * d, bottom)


def window(svg, x, y, w, h, title, body=None):
    """Period window chrome in BHIL colors. Returns the content box."""
    svg.rect(x, y, w, h, C("paper_3"))
    bevel(svg, x, y, w, h, C("paper"), C("stone"), depth=2)
    svg.rect(x + 4, y + 4, w - 8, 28, C("bh_blue_2"))
    svg.add(pixel_text(title.upper(), x + 12, y + 11, 2, C("paper")))
    for i, glyph in enumerate(("X", "O", "_")):
        bx = x + w - 30 - i * 26
        svg.rect(bx, y + 8, 22, 20, C("paper_3"))
        bevel(svg, bx, y + 8, 22, 20, C("paper"), C("stone"), depth=1)
        svg.add(pixel_text(glyph, bx + 6, y + 11, 2, C("ink")))
    cx, cy, cw, ch = x + 8, y + 40, w - 16, h - 48
    svg.rect(cx, cy, cw, ch, body or C("paper"))
    bevel(svg, cx, cy, cw, ch, C("stone"), C("paper"), depth=1)
    return cx, cy, cw, ch


def badge(svg, x, y, l1, l2, bg, fg1, fg2, s=2, light=None, dark=None, border=None):
    w, h = 88 * s, 31 * s
    svg.rect(x, y, w, h, bg)
    if border:
        svg.rect(x + 0.5, y + 0.5, w - 1, h - 1, "none", border, 1)
    else:
        bevel(svg, x, y, w, h, light or C("paper"), dark or C("ink"), depth=max(1, s // 2))
    lines = [t for t in (l1, l2) if t]
    if len(lines) == 1:
        tw = pw(lines[0], s)
        svg.add(pixel_text(lines[0], x + (w - tw) / 2.0, y + (h - 7 * s) / 2.0, s, fg1))
    else:
        for i, (t, fg) in enumerate(((l1, fg1), (l2, fg2))):
            tw = pw(t, s)
            svg.add(pixel_text(t, x + (w - tw) / 2.0, y + (6 + i * 10) * s, s, fg))


# ---------------------------------------------------------------------------
# BHIL frame: brand strip, eyebrow, title, dek, footer
# ---------------------------------------------------------------------------

def frame(svg, eyebrow, title, dek, chevron=True, center=False):
    b = brand()["strip"]
    svg.text(X0, 44, "%s · %s" % (b["lab"], b["product"]), size=12, track=0.28, opacity=0.62)
    svg.text(X1, 44, "%s · FIG %s" % (b["ref"], svg.fid), size=12, track=0.28, opacity=0.62, anchor="end")
    svg.line(X0, 62, X1, 62, C("bh_blue_3"))
    if eyebrow:
        ex = W / 2 if center else X0
        anchor = "middle" if center else "start"
        label = ("▸ " if chevron else "") + eyebrow
        svg.text(ex, 122, label, size=15, fill=C("bh_blue_bright"), track=0.22, anchor=anchor)
    if title:
        svg.text(W / 2 if center else X0, 184, title, font="serif", size=52, anchor="middle" if center else "start")
    if dek:
        svg.text(W / 2 if center else X0, 224, dek, font="serif", size=22, italic=True, opacity=0.72, anchor="middle" if center else "start")
    svg.line(X0, 842, X1, 842, C("bh_blue_3"))
    svg.text(X0, 870, "%s · FIG %s" % (b["footer"], svg.fid), size=12, track=0.28, opacity=0.62)
    svg.text(X1, 870, b["site"], size=12, track=0.28, opacity=0.62, anchor="end")


def step_keyframes(name, positions, axis, seconds):
    """Discrete steps through positions (px offsets) along one axis."""
    k = len(positions)
    frames = []
    for i, p in enumerate(positions):
        a = 100.0 * i / k
        b = 100.0 * (i + 1) / k - 0.01
        t = "translate(%spx, 0)" % n(p) if axis == "x" else "translate(0, %spx)" % n(p)
        frames.append("%.2f%%, %.2f%% { transform: %s; }" % (a, b, t))
    frames.append("100%% { transform: %s; }" % ("translate(%spx, 0)" % n(positions[0]) if axis == "x" else "translate(0, %spx)" % n(positions[0])))
    return "@keyframes %s { %s } .%s { animation: %s %ss linear infinite; }" % (name, " ".join(frames), name, name, n(seconds))


# ---------------------------------------------------------------------------
# HS-01 Masthead
# ---------------------------------------------------------------------------

def hs01(meta):
    svg = Svg("HS-01", meta["title"], meta["alt"])
    svg.defs.append('<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="12" cy="12" r="1.6" fill="%s"/></pattern>' % C("bh_blue"))
    # Stepped falloff, not a gradient: three hard-edged bands, like a dithered palette.
    svg.defs.append('<mask id="m"><rect width="%d" height="%d" fill="#fff" fill-opacity="0.12"/>'
                    '<ellipse cx="800" cy="420" rx="760" ry="350" fill="#fff" fill-opacity="0.26"/>'
                    '<ellipse cx="800" cy="420" rx="540" ry="250" fill="#fff" fill-opacity="0.44"/></mask>' % (W, H))
    svg.rect(0, 70, W, 760, "url(#dots)", extra=' mask="url(#m)"')
    rnd = random.Random(1998)
    keep_out = [(500, 92, 1100, 140), (130, 180, 1470, 380), (330, 380, 1270, 510), (380, 530, 1220, 630), (240, 690, 1360, 790)]
    placed = 0
    while placed < 26:
        x = 12 + 24 * rnd.randrange(3, 64)
        y = 12 + 24 * rnd.randrange(4, 33)
        if any(a <= x <= c and b <= y <= d for a, b, c, d in keep_out):
            continue
        i = placed
        placed += 1
        svg.add('<circle cx="%d" cy="%d" r="2.6" fill="%s" class="hs-twinkle" style="animation-delay:-%.1fs"/>' % (x, y, C("bh_blue_bright"), (i * 0.37) % 4))
    frame(svg, "OPEN FRAMEWORK · RETRO-WEB REDESIGN · V%s" % canon.load("homestead")["version"], None, None, chevron=False, center=True)
    pitch, r = 22, 8.2
    cols = len("HOMESTEAD") * 6 - 1 + 1 + 5
    x0 = (W - cols * pitch) / 2.0
    y0 = 196
    svg.add(dot_matrix("HOMESTEAD", x0, y0, pitch, r, C("bh_blue_bright"), C("bh_blue_3"), 0.42))
    cx = x0 + (len("HOMESTEAD") * 6) * pitch
    cur = "".join('<circle cx="%s" cy="%s" r="%s"/>' % (n(cx + i * pitch + pitch / 2.0), n(y0 + 6 * pitch + pitch / 2.0), n(r)) for i in range(5))
    svg.add('<g fill="%s" class="hs-blink">%s</g>' % (C("paper"), cur))
    svg.text(W / 2, 438, meta["title"], font="serif", size=58, anchor="middle")
    svg.text(W / 2, 484, "Analyze any modern site. Rebuild it the way GeoCities, FrontPage, or MySpace would have.", font="serif", size=24, italic=True, opacity=0.74, anchor="middle")
    labels = [("PRESET B", "GEOCITIES 1998"), ("PRESET C", "FRONTPAGE 2001"), ("PRESET E", "MYSPACE 2007"), ("SAFE MODE", "ON EVERY PAGE")]
    bw, gap = 176, 28
    bx = (W - (4 * bw + 3 * gap)) / 2.0
    for i, (a, b) in enumerate(labels):
        badge(svg, bx + i * (bw + gap), 548, a, b, C("bh_blue_3"), C("paper"), C("bh_blue_bright"), s=2, light=C("bh_blue_bright"), dark=C("ink"))
    counts = "%d ERA PRESETS · %d WIDGETS · %d MAPPINGS · %d LINT RULES · %d-POINT RUBRIC · STDLIB PYTHON" % (
        len(canon.presets()), len(canon.widgets()), len(canon.mapping_rows()), len(canon.load("lint-rules")["rules"]), canon.load("rubric")["max_score"])
    svg.line(400, 680, 1200, 680, C("bh_blue_3"))
    svg.text(W / 2, 720, counts, size=15, track=0.18, opacity=0.8, anchor="middle")
    svg.text(W / 2, 776, canon.load("homestead")["bhil_tagline"], font="serif", size=22, italic=True, fill=C("bh_blue_bright"), anchor="middle")
    return svg


# ---------------------------------------------------------------------------
# HS-02 Era neighborhoods
# ---------------------------------------------------------------------------

def hs02(meta):
    svg = Svg("HS-02", meta["title"], meta["alt"])
    frame(svg, "ERA PRESETS · CANON/PRESETS.JSON", meta["title"],
          "Every build locks a single preset and year. Mixing eras is a lint error unless a time capsule is declared.")
    lo, hi = 1993, 2026
    ax0, ax1 = 560, 1500

    def X(year):
        return ax0 + (ax1 - ax0) * (year - lo) / float(hi - lo + 1)

    row0, step, bh = 282, 76, 46
    rows_y = []
    for i, p in enumerate(canon.presets()):
        y = row0 + i * step
        rows_y.append(y)
        kit = p["status"] == "kit"
        svg.add(pixel_text(p["id"], X0 + 10, y + 4, 5, C("bh_blue_bright") if kit else C("bh_blue")))
        svg.text(X0 + 64, y + 20, p["slug"].replace("-", " ").upper(), size=16, track=0.12)
        canvas = "%s PX" % p["canvas"]["width_px"] if p["canvas"]["width_px"] else p["canvas"]["mode"].upper()
        svg.text(X0 + 64, y + 40, "%s · %s · %s" % (canvas, p["palette_mode"].upper(), "KIT" if kit else "SPEC ONLY"), size=12, track=0.14, opacity=0.6)
        start = int(p["years"].split("-")[0])
        end_t = p["years"].split("-")[1]
        end = hi if end_t == "now" else int(end_t)
        x, w = X(start), X(end + 1) - X(start)
        label = p["years"].upper()
        inside = pw(label, 2) + 24 <= w
        lx = x + 12 if inside else x + w + 12
        if kit:
            svg.rect(x, y, w, bh, C("bh_blue_3"), C("bh_blue"), 1)
            bevel(svg, x, y, w, bh, C("bh_blue"), C("ink"), depth=1)
            svg.add(pixel_text(label, lx, y + 16, 2, C("paper") if inside else C("bh_blue_bright")))
        else:
            svg.rect(x + 0.5, y + 0.5, w - 1, bh - 1, "none", C("bh_blue_2"), 1, extra=' stroke-dasharray="6 5"')
            svg.add(pixel_text(label, lx, y + 16, 2, C("bh_blue_bright")))
    ay = row0 + 6 * step + 6
    svg.line(ax0, ay, ax1, ay, C("bh_blue_2"))
    for year in range(lo, hi + 1):
        if (year - lo) % 3 == 0 or year == hi:
            xx = X(year) + (X(year + 1) - X(year)) / 2.0
            svg.line(xx, ay, xx, ay + 8, C("bh_blue_2"))
            svg.text(xx, ay + 28, str(year), size=12, opacity=0.7, anchor="middle")
    svg.rect(X0, ay + 52, 16, 16, C("bh_blue_3"), C("bh_blue"), 1)
    svg.text(X0 + 26, ay + 65, "KIT: WORKING PAGES, RECIPE, SAFETY LAYER", size=12, track=0.14, opacity=0.75)
    svg.rect(X0 + 470.5, ay + 52.5, 15, 15, "none", C("bh_blue_2"), 1, extra=' stroke-dasharray="4 3"')
    svg.text(X0 + 496, ay + 65, "SPEC ONLY: SCAFFOLD STARTS FROM A BLANK PAGE", size=12, track=0.14, opacity=0.75)
    order = [1, 2, 3, 4, 5, 0]
    positions = [rows_y[i] - rows_y[1] for i in order]
    svg.css.append(step_keyframes("hs02-step", positions, "y", 12))
    svg.add('<g class="hs02-step"><rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="%s" stroke-width="2"/></g>' % (
        X0 - 4, rows_y[1] - 10, X1 - X0 + 8, bh + 20, C("bh_blue_bright")))
    return svg


# ---------------------------------------------------------------------------
# HS-03 Pipeline (BHIL ASCII pipeline motif)
# ---------------------------------------------------------------------------

def hs03(meta):
    svg = Svg("HS-03", meta["title"], meta["alt"])
    frame(svg, "PIPELINE · RETRO-WEB REDESIGN ARCHITECTURE", meta["title"],
          "Intake to audit. Each phase is owned by one agent and closed by a written contract.", chevron=False)
    phases = canon.load("process")["phases"]
    short = ["INTAKE", "SURVEY", "ERA LOCK", "MAP", "ASSETS", "BUILD", "AUDIT"]
    cell = 11
    sep = " → "
    ncols = 100
    inner = ncols - 2
    lead = 3
    cells = ["%d %s" % (i, s) for i, s in enumerate(short)]
    flow = (" " * lead) + sep.join(c.ljust(cell) for c in cells)
    starts = [lead + i * (cell + len(sep)) for i in range(7)]

    def boxed(content):
        return "│" + content.ljust(inner)[:inner] + "│"

    title = "─ RETRO-WEB REDESIGN ARCHITECTURE "
    lines = ["┌" + title + "─" * (inner - len(title)) + "┐", boxed(""), boxed(flow)]
    map_c = starts[3] + 2
    aud_c = starts[6] + 2
    loop1 = [" "] * inner
    loop1[map_c] = "▲"
    loop1[aud_c] = "│"
    lines.append(boxed("".join(loop1)))
    loop2 = [" "] * inner
    loop2[map_c] = "└"
    loop2[aud_c] = "┘"
    for c in range(map_c + 1, aud_c):
        loop2[c] = "─"
    label = " REVISE "
    mid = (map_c + aud_c) // 2 - len(label) // 2
    for i, ch in enumerate(label):
        loop2[mid + i] = ch
    lines.append(boxed("".join(loop2)))
    lines.append(boxed(""))
    lines.append(boxed("   PH  OWNER                 OUTPUT"))
    for ph in phases:
        out = ", ".join(o.replace("engagements/<slug>/", "") for o in ph["outputs"])
        lines.append(boxed("   %-3s %-21s %s" % (ph["id"], ph["agent"], out[:inner - 30])))
    lines.append("└" + "─" * inner + "┘")
    px, py, pw_, ph_ = 100, 262, 1400, 450
    svg.rect(px, py, pw_, ph_, C("ink"), C("bh_blue_3"), 1)
    cw = 13.0
    tx = px + (pw_ - ncols * cw) / 2.0
    ty0, step = py + 36, 26.5
    hx = [tx + (1 + s) * cw for s in starts]
    svg.css.append(step_keyframes("hs03-step", [x - hx[0] for x in hx], "x", 14))
    svg.add('<g class="hs03-step"><rect x="%s" y="%s" width="%s" height="%s" fill="%s"/></g>' % (
        n(hx[0] - 3), n(ty0 + 2 * step - 19), n(cell * cw + 6), 26, C("bh_blue_3")))
    for i, ln in enumerate(lines):
        svg.text(tx, ty0 + i * step, ln, size=21.5, fill=C("bh_blue_bright"), length=ncols * cw)
    ring = "[ << PREV | THE HOMESTEAD WEBRING | NEXT >> ]"
    svg.add(pixel_text(ring, (W - pw(ring, 2)) / 2.0, 744, 2, C("bh_blue")))
    svg.text(W / 2, 796, "SHIP ENDS THE RUN. REVISE LOOPS TO MAPPING, ASSETS, OR BUILD. REBUILD RE-LOCKS THE ERA.", size=13, track=0.16, opacity=0.62, anchor="middle")
    return svg


# ---------------------------------------------------------------------------
# HS-04 Site survey
# ---------------------------------------------------------------------------

def hs04(meta, out_root):
    svg = Svg("HS-04", meta["title"], meta["alt"])
    frame(svg, "PHASE 1 · TOOLS/SURVEY.PY", meta["title"], "The survey records what the modern site contains, so nothing important is lost in translation.")
    with open(os.path.join(out_root, "examples", "nimbus-ledger", "inventory.json"), "r", encoding="utf-8") as handle:
        inv = json.load(handle)
    mx, my, mw, mh = 100, 270, 540, 520
    svg.text(mx, my - 8, "MODERN SOURCE · NIMBUS LEDGER · 2026", size=12, track=0.18, opacity=0.6)
    svg.rect(mx, my, mw, mh, C("paper"))
    g, d = C("paper_3"), "#D9D9D4"
    svg.rect(mx, my, mw, 44, g)
    svg.rect(mx + 18, my + 14, 80, 16, C("stone"))
    for i in range(5):
        svg.rect(mx + 150 + i * 56, my + 18, 40, 8, d)
    svg.rect(mx + mw - 96, my + 11, 78, 22, C("ink"))
    svg.rect(mx + 70, my + 84, 400, 26, C("ink"))
    svg.rect(mx + 120, my + 120, 300, 14, d)
    svg.rect(mx + 140, my + 142, 260, 10, d)
    svg.rect(mx + 160, my + 172, 100, 26, C("ink"))
    svg.rect(mx + 280.5, my + 172.5, 99, 25, "none", C("stone"), 1)
    for i in range(3):
        cx = mx + 26 + i * 170
        svg.rect(cx, my + 230, 150, 104, g)
        svg.rect(cx + 14, my + 246, 70, 10, C("stone"))
        svg.rect(cx + 14, my + 266, 120, 6, d)
        svg.rect(cx + 14, my + 278, 110, 6, d)
        svg.rect(cx + 14, my + 290, 90, 6, d)
    svg.rect(mx + 26, my + 352, 4, 50, C("sage"))
    svg.rect(mx + 40, my + 360, 300, 10, d)
    svg.rect(mx + 40, my + 380, 200, 8, d)
    svg.rect(mx + 10, my + mh - 64, mw - 20, 48, C("ink"))
    svg.rect(mx + 26, my + mh - 46, 220, 10, "#3A3A3A")
    svg.rect(mx + mw - 170, my + mh - 52, 70, 24, C("paper_3"))
    svg.add('<circle cx="%d" cy="%d" r="20" fill="%s"/>' % (mx + mw - 34, my + mh - 100, C("bh_blue_2")))
    svg.defs.append('<clipPath id="pg"><rect x="%d" y="%d" width="%d" height="%d"/></clipPath>' % (mx, my, mw, mh))
    svg.css.append("@keyframes hs04-scan { 0%% { transform: translate(0, 0); } 100%% { transform: translate(0, %dpx); } } .hs04-scan { animation: hs04-scan 4s linear infinite; }" % (mh - 4))
    svg.add('<g clip-path="url(#pg)"><g class="hs04-scan"><rect x="%d" y="%d" width="%d" height="18" fill="%s" fill-opacity="0.14"/><rect x="%d" y="%d" width="%d" height="2" fill="%s"/></g></g>' % (
        mx, my - 16 + 2, mw, C("bh_blue_bright"), mx, my + 2, mw, C("bh_blue_bright")))
    svg.line(664, 530, 726, 530, C("bh_blue"), 2)
    svg.add('<path d="M726 522 L740 530 L726 538 Z" fill="%s"/>' % C("bh_blue"))
    wx, wy, ww, wh = 760, 262, 740, 536
    cx, cy, cw_, ch_ = window(svg, wx, wy, ww, wh, "inventory.json")
    found = {p["id"] for p in inv["patterns"]}
    rows = canon.mapping_rows()
    ink = C("ink")
    svg.text(cx + 18, cy + 30, "PATTERNS", size=13, fill=C("bh_blue_2"), track=0.2, weight="600")
    for i, r in enumerate(rows):
        col, row = divmod(i, 8)
        x = cx + 18 + col * 236
        y = cy + 58 + row * 24
        hit = r["id"] in found
        if hit:
            svg.rect(x, y - 11, 12, 12, C("bh_blue_2"))
        else:
            svg.rect(x + 0.5, y - 10.5, 11, 11, "none", C("stone"), 1)
        svg.text(x + 20, y, r["id"], size=14, fill=ink if hit else C("stone"))
    by = cy + 270
    svg.line(cx + 18, by - 16, cx + cw_ - 18, by - 16, "#D9D9D4")
    svg.text(cx + 18, by + 10, "BRAND", size=13, fill=C("bh_blue_2"), track=0.2, weight="600")
    shown = [c for c in inv["brand"]["colors"] if not c["neutral"]][:4]
    for i, c in enumerate(shown):
        snap = color.snap(color.parse_hex(c["hex"]))
        x = cx + 18 + i * 172
        svg.rect(x, by + 24, 22, 22, c["hex"])
        svg.text(x + 30, by + 41, "→", size=14, fill=ink)
        svg.rect(x + 48, by + 24, 22, 22, snap["snapped"])
        svg.text(x, by + 66, "%s %s" % (c["hex"], snap["snapped"]), size=11.5, fill=ink)
    fy = by + 104
    svg.text(cx + 18, fy, "FONTS", size=13, fill=C("bh_blue_2"), track=0.2, weight="600")
    stacks = {c["id"]: c["stacks"]["B"].split(",")[0] for c in canon.load("fonts")["categories"]}
    ftxt = "   ".join("%s → %s" % (f["family"], stacks[f["category"]]) for f in inv["brand"]["fonts"])
    svg.text(cx + 100, fy, ftxt, size=14, fill=ink)
    ty = fy + 32
    svg.text(cx + 18, ty, "TONE", size=13, fill=C("bh_blue_2"), track=0.2, weight="600")
    tone = [t for t in inv["summary"]["tone_notes"] if t.startswith("modern")]
    svg.text(cx + 100, ty, (tone[0] if tone else "no modern tells").replace("modern marketing phrases: ", "modern tells: "), size=14, fill=C("copper"))
    pyb = cy + ch_ - 44
    total = len(rows)
    cnt = len(found)
    bw = (cw_ - 36) / float(total)
    svg.rect(cx + 18, pyb, cw_ - 36, 24, C("paper"))
    bevel(svg, cx + 18, pyb, cw_ - 36, 24, C("stone"), C("paper"), depth=1)
    for i in range(cnt):
        svg.rect(cx + 21 + i * bw, pyb + 3, bw - 3, 18, C("bh_blue_2"))
    svg.text(cx + cw_ - 18, pyb - 8, "%d OF %d CANON PATTERNS DETECTED" % (cnt, total), size=12, fill=ink, anchor="end", track=0.14)
    return svg


# ---------------------------------------------------------------------------
# HS-05 Component mapping
# ---------------------------------------------------------------------------

BADGES = {
    "hero": {"B": ("WELCOME TO", "MY PAGE!!!"), "C": ("CLICK TO", "ENTER"), "E": ("GLITTER", "NAME")},
    "testimonials": {"B": ("SIGN MY", "GUESTBOOK!"), "C": ("WHAT OUR", "CUSTOMERS SAY"), "E": ("THANKS FOR", "THE ADD!")},
    "analytics": {"B": ("VISITOR", "0004217"), "C": ("[HIT", "COUNTER]"), "E": ("PROFILE", "VIEWS 4217")},
    "logo-strip": {"B": ("COOL SITES", "I LIKE"), "C": ("OUR", "CLIENTS"), "E": ("TOP 8", "FRIENDS")},
    "cookie-banner": {"B": ("BEST VIEWED", "800 X 600"), "C": ("REQUIRES", "IE 5.0"), "E": (None, None)},
    "chat-widget": {"B": ("ICQ #", "4021998"), "C": ("EMAIL THE", "WEBMASTER"), "E": ("INSTANT", "MESSAGE")},
}
ERA_STYLE = {
    "B": ("#000066", "#FFFF00", "#00FFFF"),
    "C": ("#CCCCFF", "#000033", "#003399"),
    "E": ("#000000", "#FF66CC", "#FFFFFF"),
}


def wrap(text, width, lines=2):
    words = text.split()
    out, cur = [], ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) <= width:
            cur = (cur + " " + w).strip()
        else:
            out.append(cur)
            cur = w
            if len(out) == lines:
                break
    if len(out) < lines and cur:
        out.append(cur)
    used = " ".join(out)
    if len(used) < len(" ".join(words)) and out:
        out[-1] = out[-1][: max(0, width - 3)].rstrip(" ,.") + "..."
    return out


def hs05(meta):
    svg = Svg("HS-05", meta["title"], meta["alt"])
    frame(svg, "PHASE 3 · CANON/MAPPING.JSON", meta["title"],
          "Six of the %d mappings. One modern pattern becomes a different object in each era." % len(canon.mapping_rows()))
    rows = {r["id"]: r for r in canon.mapping_rows()}
    cols = [("B", "B · GEOCITIES 1998"), ("C", "C · FRONTPAGE 2001"), ("E", "E · MYSPACE 2007")]
    c0, cx0, cwid = 100, 410, 364
    hy = 284
    svg.text(c0, hy, "MODERN PATTERN", size=13, track=0.22, fill=C("bh_blue_bright"))
    for j, (_pid, label) in enumerate(cols):
        svg.text(cx0 + j * cwid, hy, label, size=13, track=0.22, fill=C("bh_blue_bright"))
    svg.line(c0, hy + 14, 1500, hy + 14, C("bh_blue_2"), 2)
    rh = 82
    ry0 = hy + 30
    order = ["hero", "testimonials", "analytics", "logo-strip", "cookie-banner", "chat-widget"]
    for i, rid in enumerate(order):
        y = ry0 + i * rh
        r = rows[rid]
        svg.text(c0, y + 38, r["modern_pattern"], font="sans", size=20)
        svg.text(c0, y + 60, rid.upper(), size=11, track=0.18, opacity=0.5)
        for j, (pid, _l) in enumerate(cols):
            x = cx0 + j * cwid
            l1, l2 = BADGES[rid][pid]
            if l1 is None:
                svg.rect(x + 0.5, y + 12.5, 131, 46, "none", C("stone"), 1, extra=' stroke-dasharray="5 4"')
                svg.add(pixel_text("DROPPED", x + (132 - pw("DROPPED", 1.5)) / 2.0, y + 30, 1.5, C("stone")))
            else:
                bg, f1, f2 = ERA_STYLE[pid]
                badge(svg, x, y + 12, l1, l2, bg, f1, f2, s=1.5, light="#FFFFFF", dark="#333333")
            for k, ln in enumerate(wrap(r[pid], 25)):
                svg.text(x + 146, y + 30 + k * 21, ln, font="sans", size=15, opacity=0.82)
        if i < len(order) - 1:
            svg.line(c0, y + rh - 4, 1500, y + rh - 4, C("bh_blue_3"))
    positions = [i * rh for i in range(len(order))]
    svg.css.append(step_keyframes("hs05-step", positions, "y", 12))
    svg.add('<g class="hs05-step"><rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="%s" stroke-width="2"/></g>' % (
        c0 - 12, ry0 + 2, 1500 - c0 + 24, rh - 10, C("bh_blue_bright")))
    return svg


# ---------------------------------------------------------------------------
# HS-06 Asset smithy
# ---------------------------------------------------------------------------

def hs06(meta):
    svg = Svg("HS-06", meta["title"], meta["alt"])
    frame(svg, "PHASE 4 · TOOLS/GIFSMITH.PY · TOOLS/WEBSAFE.PY", meta["title"],
          "Brand colors snapped to the 216-color cube. Specimens below are real gifsmith output, drawn pixel for pixel.")
    levels = ["00", "33", "66", "99", "CC", "FF"]
    sx, sy, cell = 100, 290, 15
    svg.text(sx, sy - 14, "THE 216 · WEB-SAFE CUBE", size=12, track=0.2, fill=C("bh_blue_bright"))
    for ri, rr in enumerate(levels):
        ox = sx + (ri % 3) * (6 * cell + 18)
        oy = sy + (ri // 3) * (6 * cell + 30)
        svg.text(ox, oy + 6 * cell + 18, "R " + rr, size=11, opacity=0.6)
        for gi, gg in enumerate(levels):
            for bi, bb in enumerate(levels):
                svg.rect(ox + bi * cell, oy + gi * cell, cell - 1, cell - 1, "#%s%s%s" % (rr, gg, bb))
    ty = 560
    svg.text(sx, ty, "BHIL PALETTE, SNAPPED", size=12, track=0.2, fill=C("bh_blue_bright"))
    for i, key in enumerate(("bh_blue", "bh_blue_2", "bh_blue_3", "terminal_navy", "copper")):
        y = ty + 22 + i * 44
        orig = C(key)
        snap = color.snap(color.parse_hex(orig))
        svg.rect(sx, y, 30, 30, orig, C("bh_blue_3"), 1)
        svg.text(sx + 42, y + 21, "→", size=16)
        svg.rect(sx + 66, y, 30, 30, snap["snapped"], C("bh_blue_3"), 1)
        svg.text(sx + 110, y + 13, "%s → %s" % (orig, snap["snapped"]), size=13)
        svg.text(sx + 110, y + 29, "%s · ΔE %.1f" % (key.replace("_", " ").upper(), snap["delta_e"]), size=11, opacity=0.6, track=0.1)
    svg.line(560, 280, 560, 800, C("bh_blue_3"))
    rx = 610
    lib = {a["name"]: a for a in json.load(open(os.path.join(ROOT, "kits", "shared", "recipe.json"), "r", encoding="utf-8"))["assets"]}
    specimens = [
        ("badge", lib["badge-800x600"]["params"], rx, 290, 3, 0, "BADGE · 88 X 31"),
        ("construction", {}, rx + 330, 290, 3, 0, "CONSTRUCTION · 2 FRAMES · 600 MS"),
        ("navbutton", {"label": "Products"}, rx + 330, 476, 2, 0, "NAVBUTTON · NORMAL AND HOVER"),
        ("navbutton", {"label": "Products"}, rx + 590, 476, 2, 1, None),
        ("glitter", {"text": "HOMESTEAD", "scale": 2, "seed": 9, "base": ["#6699CC", "#99CCFF", "#66CCFF"],
                     "sparkle": ["#FFFFFF", "#CCFFFF", "#FFFFCC"], "outline": "#003366"}, rx, 606, 3, 0, "GLITTER · 3 FRAMES · 400 MS"),
    ]
    for kind, params, x, y, sc, pick, label in specimens:
        g_, w_, h_ = gif_image(kind, params, x, y, sc, pick)
        svg.add(g_)
        if label:
            svg.text(x, y + h_ + 22, label, size=11.5, track=0.16, opacity=0.62)
    import base64
    digits = gifsmith.KINDS["digits"]({})
    for i, dch in enumerate("004217"):
        svg.add('<image x="%d" y="470" width="42" height="60" style="image-rendering: crisp-edges; image-rendering: pixelated" href="data:image/gif;base64,%s"/>' % (
            rx + i * 42, base64.b64encode(digits[int(dch)][1]).decode("ascii")))
    svg.text(rx, 552, "DIGITS · ODOMETER", size=11.5, track=0.16, opacity=0.62)
    alpha = "ABCDEFGHIJKLM NOPQRSTUVWXYZ 0123456789 !?♥♪"
    svg.add(pixel_text(alpha, rx, 740, 3, C("bh_blue_bright")))
    svg.text(rx, 788, "5 X 7 PIXEL FONT · HAND-ENTERED · NO THIRD-PARTY GLYPHS", size=11.5, track=0.16, opacity=0.62)
    return svg


# ---------------------------------------------------------------------------
# HS-07 View Source
# ---------------------------------------------------------------------------

def hs07(meta):
    svg = Svg("HS-07", meta["title"], meta["alt"])
    frame(svg, "PHASE 5 · TOOLS/ERA_LINT.PY", meta["title"],
          "Period markup plus exactly two modern lines. Anything else that smells like 2026 is a finding.")
    rules = {r["id"]: r for r in canon.load("lint-rules")["rules"]}
    src = [
        ("<html><head>", None),
        ('<link rel="stylesheet" href="homestead-safe.css">', "safe"),
        ('<script src="homestead-safe.js" defer></script>', "safe"),
        ('<link href="https://fonts.googleapis.com/css2?family=Inter">', "HL001"),
        ("</head>", None),
        ('<body background="images/stars-tile.gif" bgcolor="#000000">', None),
        ("<!-- hs:widget hit-counter -->", None),
        ('<table width="600" border="0" cellpadding="0">', None),
        ('<tr><td style="border-radius: 12px">', "HL002"),
        ('<font face="Comic Sans MS,Arial" size="5">Welcome!!!</font>', None),
        ("<marquee>Thanks for stopping by!!!</marquee>", None),
        ("<p>Get started today.</p>", "HL011"),
        ('<!--webbot bot="Timestamp" S-Type="EDITED" -->', None),
        ("</td></tr></table>", None),
    ]
    cx, cy, cw_, ch_ = window(svg, 100, 262, 930, 540, "index.html · view source")
    step = 33
    for i, (ln, flag) in enumerate(src):
        y = cy + 30 + i * step
        if flag and flag != "safe":
            svg.add('<g class="hs-breathe"><rect x="%s" y="%s" width="%s" height="%s" fill="%s" fill-opacity="0.16"/><rect x="%s" y="%s" width="5" height="%s" fill="%s"/></g>' % (
                n(cx + 2), n(y - 21), n(cw_ - 4), n(step - 3), C("copper"), n(cx + 2), n(y - 21), n(step - 3), C("copper")))
        if flag == "safe":
            svg.rect(cx + 2, y - 21, 5, step - 3, C("bh_blue_2"))
        svg.text(cx + 18, y, "%2d" % (i + 1), size=15, fill=C("stone"))
        svg.text(cx + 54, y, ln, size=15.5, fill=C("ink"))
    cur_y = cy + 30 + 9 * step
    svg.add('<rect x="%s" y="%s" width="2" height="20" fill="%s" class="hs-blink"/>' % (n(cx + 54 + 9.3 * len(src[9][0])), n(cur_y - 16), C("ink")))
    rx = 1070
    svg.text(rx, 290, "HOMESTEAD ERA LINT · PRESET B", size=13, track=0.2, fill=C("bh_blue_bright"))
    svg.line(rx, 304, X1, 304, C("bh_blue_3"))
    y = 340
    for rid, line_no in (("HL001", 4), ("HL002", 9), ("HL011", 12)):
        r = rules[rid]
        sev = r["applies"]["B"].upper()
        svg.text(rx, y, "%-5s %s  LINE %d" % (sev, rid, line_no), size=14, fill=C("copper"), track=0.08)
        svg.text(rx, y + 24, r["title"], font="sans", size=17)
        for k, ln in enumerate(wrap(r["fix"], 46)):
            svg.text(rx, y + 46 + k * 19, ln, font="sans", size=13.5, opacity=0.66)
        y += 112
    svg.line(rx, y - 20, X1, y - 20, C("bh_blue_3"))
    svg.text(rx, y + 8, "VERDICT: FINDINGS · 2 ERRORS · 1 WARNING", size=13, fill=C("copper"), track=0.08)
    svg.text(rx, y + 40, "AFTER FIX: NO FINDINGS (INCONCLUSIVE)", size=13, fill=C("bh_blue_bright"), track=0.08)
    svg.text(rx, y + 80, "Lint knows the tells. It cannot see the page,", font="serif", size=19, italic=True, opacity=0.8)
    svg.text(rx, y + 104, "so it never says clean.", font="serif", size=19, italic=True, opacity=0.8)
    return svg


# ---------------------------------------------------------------------------
# HS-08 Safe Mode
# ---------------------------------------------------------------------------

def hs08(meta):
    svg = Svg("HS-08", meta["title"], meta["alt"])
    frame(svg, "SAFETY LAYER · KITS/SAFETY-LAYER", meta["title"],
          "One switch stops every marquee, blink, animation, and sound, and raises contrast. It starts on under reduced motion.")
    lx, ly, lw, lh = 100, 290, 600, 400
    rx = 900
    svg.text(lx, ly - 12, "AS BUILT · PRESET B · 1998", size=12, track=0.2, opacity=0.62)
    svg.text(rx, ly - 12, "SAFE MODE ON · SAME PAGE", size=12, track=0.2, opacity=0.62)
    svg.defs.append('<clipPath id="lc"><rect x="%d" y="%d" width="%d" height="%d"/></clipPath>' % (lx, ly, lw, lh))
    svg.defs.append('<clipPath id="mq"><rect x="%d" y="%d" width="%d" height="%d"/></clipPath>' % (lx + 60, ly + 130, lw - 120, 34))
    svg.rect(lx, ly, lw, lh, "#000000")
    rnd = random.Random(7)
    stars = []
    for i in range(60):
        x, y = lx + rnd.randrange(lw), ly + rnd.randrange(lh)
        cls = ' class="hs-twinkle" style="animation-delay:-%.1fs"' % ((i * 0.53) % 4) if i % 4 == 0 else ""
        stars.append('<rect x="%d" y="%d" width="2" height="2" fill="%s"%s/>' % (x, y, ("#FFFFFF", "#FFFF99", "#99CCFF")[i % 3], cls))
    svg.add('<g clip-path="url(#lc)">%s</g>' % "".join(stars))
    title = "WELCOME!!!"
    svg.add(pixel_text(title, lx + (lw - pw(title, 6)) / 2.0, ly + 40, 6, "#FFFF00"))
    svg.rect(lx + 60, ly + 130, lw - 120, 34, "#000066")
    msg = "THANKS FOR STOPPING BY!!! SIGN MY GUESTBOOK!!!     "
    L = pw(msg, 2) + 12
    svg.css.append("@keyframes hs08-marq { from { transform: translate(0, 0); } to { transform: translate(-%spx, 0); } } .hs08-marq { animation: hs08-marq 14s linear infinite; }" % n(L))
    svg.add('<g clip-path="url(#mq)"><g class="hs08-marq">%s%s</g></g>' % (
        pixel_text(msg, lx + 80, ly + 140, 2, "#FFFF00"), pixel_text(msg, lx + 80 + L, ly + 140, 2, "#FFFF00")))
    nw = pw("NEW!", 3) + 18
    svg.add('<g class="hs-blink"><rect x="%d" y="%d" width="%d" height="33" fill="#FF0000"/>%s</g>' % (lx + 60, ly + 206, nw, pixel_text("NEW!", lx + 69, ly + 212, 3, "#FFFF00")))
    svg.add(pixel_text("MY COOL LINKS", lx + 80 + nw, ly + 212, 3, "#00FFFF"))
    sp = []
    for k in range(0, lw + 80, 40):
        sp.append('<path d="M%d %d l20 0 l-26 26 l-20 0 z" fill="#000000"/>' % (lx + k, ly + lh - 40))
    svg.css.append("@keyframes hs08-stripe { from { transform: translate(0, 0); } to { transform: translate(-40px, 0); } } .hs08-stripe { animation: hs08-stripe 4s linear infinite; }")
    svg.rect(lx, ly + lh - 40, lw, 26, "#FFCC00")
    svg.add('<g clip-path="url(#lc)"><g class="hs08-stripe">%s</g></g>' % "".join(sp))
    svg.add(pixel_text("UNDER CONSTRUCTION", lx + (lw - pw("UNDER CONSTRUCTION", 2)) / 2.0, ly + lh - 78, 2, "#FFCC00"))
    svg.rect(rx, ly, lw, lh, C("paper"))
    svg.text(rx + 40, ly + 70, "Welcome!!!", font="serif", size=46, fill=C("ink"), weight="500")
    svg.text(rx + 40, ly + 120, "Thanks for stopping by! Sign my guestbook!", font="serif", size=22, fill=C("ink"))
    svg.text(rx + 40, ly + 176, "NEW! My cool links", font="serif", size=22, fill=C("ink"))
    svg.add('<text x="%d" y="%d" font-family="%s" font-size="22" fill="#0000EE" text-decoration="underline">Sign my guestbook</text>' % (rx + 40, ly + 222, F("serif")))
    svg.add('<text x="%d" y="%d" font-family="%s" font-size="22" fill="#0000EE" text-decoration="underline">Text-only version</text>' % (rx + 40, ly + 268, F("serif")))
    svg.text(rx + 40, ly + lh - 32, "Under construction. Come back soon!", font="serif", size=20, fill=C("ink"), italic=True)
    bx, by, bw_, bh_ = 726, 450, 148, 52
    svg.rect(bx, by, bw_, bh_, "#FFFF99")
    bevel(svg, bx, by, bw_, bh_, C("stone"), C("paper"), depth=2, raised=False)
    svg.add(pixel_text("SAFE MODE:", bx + (bw_ - pw("SAFE MODE:", 2)) / 2.0, by + 10, 2, C("ink")))
    svg.add(pixel_text("ON", bx + (bw_ - pw("ON", 2)) / 2.0, by + 28, 2, C("ink")))
    svg.line(706, 476, 724, 476, C("bh_blue"), 2)
    svg.line(876, 476, 892, 476, C("bh_blue"), 2)
    svg.add('<path d="M892 469 L900 476 L892 483 Z" fill="%s"/>' % C("bh_blue"))
    cy = 742
    for i, (code, txt) in enumerate((("WCAG 2.3.1", "340 MS FRAME FLOOR · FLASH AREA AND RATE AUDITED"),
                                      ("WCAG 2.2.2", "ONE SWITCH STOPS EVERY MOVING THING"),
                                      ("WCAG 1.4.2", "AUDIO PLAYS ON CLICK, NEVER ON LOAD"))):
        x = 100 + i * 470
        svg.text(x, cy, code, size=15, fill=C("bh_blue_bright"), track=0.16, weight="600")
        svg.text(x, cy + 26, txt, size=12, track=0.12, opacity=0.7)
    return svg


# ---------------------------------------------------------------------------
# HS-09 Rubric
# ---------------------------------------------------------------------------

def hs09(meta):
    svg = Svg("HS-09", meta["title"], meta["alt"])
    frame(svg, "PHASE 6 · TOOLS/RUBRIC.PY", meta["title"],
          "The auditor cannot write and never sees the builder's notes. A perfect score should make it suspicious.")
    with open(os.path.join(ROOT, "examples", "nimbus-ledger", "qa", "scorecard-B.json"), "r", encoding="utf-8") as handle:
        card = json.load(handle)
    rub = canon.load("rubric")
    total = card["total"]
    for i, dch in enumerate("%02d" % total):
        x = 100 + i * 150
        svg.rect(x, 280, 136, 186, C("ink"), C("bh_blue_3"), 1)
        svg.rect(x, 372, 136, 1, C("bh_blue_3"))
        svg.add(pixel_text(dch, x + 23, 310, 18, C("bh_blue_bright")))
    svg.text(410, 456, "/ %d" % rub["max_score"], font="serif", size=64, opacity=0.85)
    svg.text(100, 506, "NIMBUS LEDGER · PRESET B · 1998", size=13, track=0.2, opacity=0.62)
    stx, sty = 100, 530
    sw = pw("SHIP", 5) + 40
    svg.add('<g class="hs-breathe"><rect x="%d" y="%d" width="%d" height="64" fill="none" stroke="%s" stroke-width="3"/>%s</g>' % (
        stx, sty, sw, C("bh_blue_bright"), pixel_text("SHIP", stx + 20, sty + 15, 5, C("bh_blue_bright"))))
    bx0, bx1, by = 100, 620, 660
    colors = {"REBUILD": C("stone"), "REVISE": C("copper"), "SHIP": C("bh_blue_2")}

    def BX(v):
        return bx0 + (bx1 - bx0) * v / 40.0

    for b in rub["bands"]:
        a, z = BX(b["min"]), BX(b["max"] + 1 if b["max"] < 40 else 40)
        svg.rect(a, by, z - a - 2, 24, colors[b["verdict"]])
        svg.text((a + z - 2) / 2.0, by + 17, b["verdict"], size=11.5, track=0.14, anchor="middle", weight="600")
        svg.text((a + z - 2) / 2.0, by + 46, "%d-%d" % (b["min"], b["max"]), size=11.5, track=0.12, opacity=0.75, anchor="middle")
    mx = BX(total) - 1
    svg.add('<path d="M%s %d l-8 -12 l16 0 z" fill="%s"/>' % (n(mx + 6), by - 2, C("paper")))
    gates = " · ".join("ROW %d %s %d" % (g["row"], "=" if g["min"] == 2 else "≥", g["min"]) for g in rub["hard_gates"])
    svg.text(100, 760, "HARD GATES · " + gates, size=12.5, track=0.14, opacity=0.7)
    svg.line(680, 270, 680, 800, C("bh_blue_3"))
    scores = {r["row"]: r["score"] for r in card["rows"]}
    for r in rub["rows"]:
        col, row = divmod(r["row"] - 1, 10)
        x = 720 + col * 400
        y = 300 + row * 48
        low = scores[r["row"]] < 2
        svg.text(x, y, "%02d" % r["row"], size=14, fill=C("bh_blue_bright"), track=0.1)
        name = r["check"] if len(r["check"]) <= 27 else r["check"][:25] + "..."
        svg.text(x + 40, y, name, font="sans", size=17, fill=C("copper") if low else C("paper"), opacity=None if low else 0.88)
        for k in range(2):
            cxp = x + 336 + k * 22
            if k < scores[r["row"]]:
                svg.add('<circle cx="%d" cy="%d" r="7" fill="%s"/>' % (cxp, y - 6, C("copper") if low else C("bh_blue_bright")))
            else:
                svg.add('<circle cx="%d" cy="%d" r="6.5" fill="none" stroke="%s" stroke-width="1.5"/>' % (cxp, y - 6, C("copper")))
        if row < 9:
            svg.line(x, y + 18, x + 370, y + 18, C("bh_blue_3"))
    return svg


# ---------------------------------------------------------------------------
# HS-10 Agent crew
# ---------------------------------------------------------------------------

def identicon(svg, x, y, size, seed):
    rnd = random.Random(seed)
    cells = 6
    c = size / float(cells)
    fg = rnd.choice([C("bh_blue"), C("bh_blue_bright"), C("bh_blue_2"), C("sage"), C("copper")])
    svg.rect(x, y, size, size, C("ink"))
    for yy in range(cells):
        for xx in range(cells // 2):
            if rnd.random() < 0.5:
                svg.rect(x + xx * c, y + yy * c, c, c, fg)
                svg.rect(x + (cells - 1 - xx) * c, y + yy * c, c, c, fg)
    svg.rect(x + 0.5, y + 0.5, size - 1, size - 1, "none", C("bh_blue_3"), 1)


def hs10(meta):
    svg = Svg("HS-10", meta["title"], meta["alt"])
    frame(svg, "AGENTS · CANON/AGENTS.JSON", meta["title"],
          "A human director, an Opus orchestrator, and six tool-isolated subagents. The auditor grades blind.")
    agents = canon.load("agents")
    cards = [{"name": "YOU", "role": "HUMAN DIRECTOR", "lines": ["Owns every claim.", "Signs off at four checkpoints."], "tools": [], "forbidden": []},
             {"name": "orchestrator", "role": "PHASE 0 · %s" % agents["orchestrator"]["model"].upper(), "lines": ["Intake, sequencing,", "checkpoints, sign-off."], "tools": ["all"], "forbidden": []}]
    for a in agents["agents"]:
        cards.append({"name": a["name"], "role": "PHASE %d · %s" % (a["phase"], a["model"].upper()), "lines": [], "tools": a["tools"], "forbidden": a["forbidden"]})
    cw_, ch_, gap = 332, 244, 24
    x0, y0 = 100, 270
    for i, cd in enumerate(cards):
        col, row = i % 4, i // 4
        x = x0 + col * (cw_ + gap)
        y = y0 + row * (ch_ + gap)
        svg.rect(x + 0.5, y + 0.5, cw_ - 1, ch_ - 1, "none", C("bh_blue_3"), 1)
        svg.rect(x, y, cw_, 34, C("bh_blue_3"))
        svg.text(x + 14, y + 23, cd["name"], size=16, fill=C("bh_blue_bright"), weight="600")
        identicon(svg, x + 14, y + 48, 84, "hs10-" + cd["name"])
        svg.text(x + 112, y + 64, cd["role"], size=12, track=0.12, opacity=0.7)
        for k, ln in enumerate(cd["lines"]):
            svg.text(x + 112, y + 92 + k * 22, ln, font="sans", size=15, opacity=0.85)
        ty = y + 154 if cd["tools"] else y + 154
        tools = ["+ " + t for t in cd["tools"]] + ["- " + t for t in cd["forbidden"]]
        for k, t in enumerate(tools):
            tx = x + 14 + (k % 3) * 106
            tyy = ty + (k // 3) * 22 if not cd["lines"] else ty + 16 + (k // 3) * 22
            svg.text(tx, tyy, t, size=13, fill=C("copper") if t.startswith("-") else C("bh_blue_bright"))
        if cd["name"] == "orchestrator":
            ow = pw("ONLINE NOW!", 2) + 12
            svg.add('<g class="hs-blink"><rect x="%d" y="%d" width="%d" height="24" fill="none" stroke="%s"/>%s</g>' % (
                x + 112, y + 146, ow, C("copper"), pixel_text("ONLINE NOW!", x + 118, y + 151, 2, C("copper"))))
        if "Write" in cd["forbidden"]:
            rw = pw("READ ONLY", 2) + 16
            svg.rect(x + 112, y + 84, rw, 26, "none", C("copper"), 2)
            svg.add(pixel_text("READ ONLY", x + 120, y + 90, 2, C("copper")))
        if cd["name"] == "YOU":
            tw_ = pw("TOP FRIEND #1", 2) + 16
            svg.rect(x + 14, y + 156, tw_, 26, "none", C("bh_blue_bright"), 1)
            svg.add(pixel_text("TOP FRIEND #1", x + 22, y + 162, 2, C("bh_blue_bright")))
    svg.text(100, 806, "TOOL LISTS ARE CANON. SCRIPTS/VALIDATE.PY FAILS IF ANY AGENT DEFINITION DRIFTS.", size=12, track=0.16, opacity=0.6)
    return svg


BUILDERS = {"HS-01": hs01, "HS-02": hs02, "HS-03": hs03, "HS-05": hs05, "HS-06": hs06, "HS-07": hs07,
            "HS-08": hs08, "HS-09": hs09, "HS-10": hs10}


def figure_file(meta):
    return "%s-%s.svg" % (meta["id"].lower(), meta["slug"])


def build_svgs(out_root):
    out = {}
    for meta in brand()["figures"]:
        if meta["id"] == "HS-04":
            svg = hs04(meta, out_root)
        else:
            svg = BUILDERS[meta["id"]](meta)
        out[figure_file(meta)] = svg.render()
    return out


def gallery_html(files):
    b = brand()
    p = b["palette"]
    items = []
    for meta in b["figures"]:
        f = figure_file(meta)
        items.append('<figure><img src="%s" alt="%s" width="1600" height="900" loading="eager"><figcaption><span>%s</span> %s<br><small>%s</small></figcaption></figure>' % (
            f, esc(meta["alt"]), meta["id"], esc(meta["title"]), esc(meta["motion"])))
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>HOMESTEAD figure kit</title>
<style>
body { margin: 0; background: %(navy)s; color: %(paper)s; font-family: %(sans)s; }
header, main { max-width: 1440px; margin: 0 auto; padding: 0 40px; }
header { padding-top: 48px; border-bottom: 1px solid %(blue3)s; padding-bottom: 24px; }
.eyebrow { font-family: %(mono)s; letter-spacing: 0.22em; font-size: 12px; color: %(bright)s; text-transform: uppercase; }
h1 { font-family: %(serif)s; font-weight: 400; font-size: 48px; margin: 12px 0 4px; }
.dek { font-family: %(serif)s; font-style: italic; opacity: 0.75; font-size: 20px; margin: 0; }
figure { margin: 40px 0; }
img { width: 100%%; height: auto; display: block; border: 1px solid %(blue3)s; }
figcaption { font-size: 15px; margin-top: 10px; opacity: 0.9; }
figcaption span { font-family: %(mono)s; letter-spacing: 0.2em; color: %(bright)s; }
small { opacity: 0.6; }
</style>
</head>
<body>
<header>
<div class="eyebrow">Barry Hurd Intelligence Lab · HOMESTEAD figure kit</div>
<h1>Ten figures, one frame.</h1>
<p class="dek">Period web specimens inside the BHIL instrument frame. Animations stop when your system prefers reduced motion.</p>
</header>
<main>
%(items)s
</main>
</body>
</html>
""" % {"navy": p["terminal_navy"], "paper": p["paper"], "blue3": p["bh_blue_3"], "bright": p["bh_blue_bright"],
       "sans": b["type"]["sans"], "mono": b["type"]["mono"], "serif": b["type"]["serif"], "items": "\n".join(items)}


def readme_md():
    b = brand()
    out = ["---", 'title: "Figure kit"', 'description: "Ten BHIL figures with a retro-web feel, HS-01 to HS-10."', "generated: true", "---", "",
           "<!-- Generated from canon/brand.json by scripts/figures.py. Do not edit by hand; edit canon and rebuild. -->", "",
           "# Figure kit", "",
           "Ten 1600 x 900 figures that put period web specimens (pixel type, bevels, 88x31 badges, odometers, marquees) inside the BHIL instrument frame from %s. Every figure is drawn from canon and the worked example's data by `scripts/figures.py`, written by `scripts/build_derived.py`, and drift-checked with the rest of the repository ([ADR-009](../../adr/ADR-009-figure-kit.md))." % b["source"], "",
           "Animations are CSS only, slow, and small in area. Frame zero is the designed static frame, and every animation stops when the viewer prefers reduced motion. A standalone [gallery](gallery.html) shows all ten.", "",
           "## Files", "",
           "| Form | Where | Use |",
           "|---|---|---|",
           "| Animated SVG | `assets/figures/hs-NN-*.svg` | README, docs site, anywhere an `<img>` tag works. Falls back to Georgia, Arial, and Courier New where brand fonts cannot load |",
           "| Static PNG, 1600 x 900 | `assets/figures/png/hs-NN-*.png` | Slides, documents, social posts. Rendered with the brand fonts |",
           "| Gallery | `assets/figures/gallery.html` | Review all ten on one page |", "",
           "Refresh the PNGs after any figure change with `python3 scripts/render_figures.py` (needs Playwright and Chrome). `scripts/validate.py` fails when a PNG is older than its SVG.", "",
           "## Brand rules applied", ""]
    for rule in b["rules"]:
        out.append("- " + rule)
    out += ["", "## The figures", ""]
    for meta in b["figures"]:
        f = figure_file(meta)
        out.append("### %s: %s" % (meta["id"], meta["title"]))
        out.append("")
        out.append("![%s](%s)" % (meta["alt"], f))
        out.append("")
        out.append("Motion: %s" % meta["motion"])
        out.append("")
        links = []
        for p_ in meta["placements"]:
            links.append("[`%s`](%s)" % (p_, "../../" + p_))
        out.append("Placed in: " + ", ".join(links) + ". PNG: [`png/%s`](png/%s)." % (f.replace(".svg", ".png"), f.replace(".svg", ".png")))
        out.append("")
    return "\n".join(out)


def build(w):
    """Write the figure kit through a build_derived Writer."""
    for name, content in build_svgs(w.out_root).items():
        w.text("assets/figures/" + name, content)
    w.text("assets/figures/gallery.html", gallery_html(None))
    w.text("assets/figures/README.md", readme_md())


def main(argv=None):
    parser = argparse.ArgumentParser(description="Generate the HOMESTEAD figure kit.")
    parser.add_argument("--out", default=os.path.join(ROOT, "assets", "figures"))
    args = parser.parse_args(argv)
    os.makedirs(args.out, exist_ok=True)
    for name, content in build_svgs(ROOT).items():
        with open(os.path.join(args.out, name), "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
        print(os.path.join(args.out, name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
