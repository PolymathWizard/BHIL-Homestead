#!/usr/bin/env python3
"""gifsmith: generate original period-style GIFs and audio from recipes.

Every asset is drawn from shapes and a hand-entered 5x7 pixel font, so the
output carries no third-party rights (ADR-004). Animated assets also get a
<name>-still.gif first frame that the safety layer swaps in during Safe Mode.
All frame delays respect the house budget in canon/homestead.json.

Usage:
    python3 tools/gifsmith.py kinds
    python3 tools/gifsmith.py recipe RECIPE.json --out DIR
    python3 tools/gifsmith.py one KIND OUTFILE --params '{"lines": ["HELLO", "WORLD"]}'

Stdlib only.
"""

import argparse
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hs_core import audio, canon, color, raster, tunes  # noqa: E402

RAINBOW = ["#FF0000", "#FF6600", "#FFCC00", "#FFFF00", "#99FF00", "#00FF00", "#00FF99",
           "#00FFFF", "#0099FF", "#0000FF", "#6600FF", "#CC00FF", "#FF00FF", "#FF0099"]


def rgb(value):
    return color.parse_hex(value)


def _min_delay_cs():
    return int(round(canon.params()["gif_min_frame_delay_ms"] / 10.0))


def _delay(requested):
    floor = _min_delay_cs()
    return max(int(requested), floor)


def _animated(canvases, delay_cs, transparent=None):
    delays = [_delay(delay_cs)] * len(canvases)
    anim = raster.encode_frames(canvases, delays, loop=0, transparent_rgb=transparent)
    still = raster.encode_frames([canvases[0]], transparent_rgb=transparent)
    return anim, still


# ---------------------------------------------------------------------------
# Generators. Each returns a list of (suffix, bytes); suffix "" is the main file.
# ---------------------------------------------------------------------------

def k_spacer(_p):
    c = raster.Canvas(1, 1, (255, 0, 255))
    return [("", raster.encode_frames([c], transparent_rgb=(255, 0, 255)))]


def k_stars(p):
    w, h = p.get("width", 64), p.get("height", 64)
    rnd = random.Random(p.get("seed", 7))
    c = raster.Canvas(w, h, rgb(p.get("bg", "#000000")))
    colors = [rgb(x) for x in p.get("colors", ["#FFFFFF", "#FFFF99", "#99CCFF", "#CCCCCC"])]
    for i in range(p.get("count", 22)):
        x, y = rnd.randrange(w), rnd.randrange(h)
        col = colors[i % len(colors)]
        c.set(x, y, col)
        if i % 6 == 0:
            dim = rgb(p.get("dim", "#666666"))
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                c.set((x + dx) % w, (y + dy) % h, dim)
    return [("", raster.encode_frames([c]))]


def k_rainbow(p):
    w, h = p.get("width", 480), p.get("height", 6)
    c = raster.Canvas(w, h, (0, 0, 0))
    bands = p.get("colors", RAINBOW)
    for x in range(w):
        c.vline(x, 0, h, rgb(bands[(x * len(bands)) // w]))
    return [("", raster.encode_frames([c]))]


def _stripes(c, y, h, offset, a, b):
    for yy in range(y, y + h):
        for x in range(c.width):
            band = ((x + yy + offset) // 4) % 2
            c.set(x, yy, a if band else b)


def k_construction(p):
    w, h = p.get("width", 120), p.get("height", 45)
    yellow, black = rgb(p.get("bg", "#FFCC00")), rgb(p.get("fg", "#000000"))
    lines = p.get("lines", ["UNDER", "CONSTRUCTION"])
    frames = []
    for offset in (0, 4):
        c = raster.Canvas(w, h, yellow)
        _stripes(c, 0, 7, offset, yellow, black)
        _stripes(c, h - 7, 7, offset, yellow, black)
        top = 7 + (h - 14 - (len(lines) * 9 - 2)) // 2
        for i, line in enumerate(lines):
            c.text_centered(top + i * 9, line, black)
        c.rect(0, 0, w, h, black)
        frames.append(c)
    anim, still = _animated(frames, p.get("delay_cs", 60))
    return [("", anim), ("-still", still)]


def k_new(p):
    text = p.get("text", "NEW!")
    w = raster.text_width(text) + 6
    a, b = rgb(p.get("color_a", "#FF0000")), rgb(p.get("color_b", "#FFFF00"))
    frames = []
    for fg, bg in ((a, b), (b, a)):
        c = raster.Canvas(w, 11, bg)
        c.text(3, 2, text, fg)
        frames.append(c)
    anim, still = _animated(frames, p.get("delay_cs", 60))
    return [("", anim), ("-still", still)]


def k_ball(p):
    size = p.get("size", 12)
    base = rgb(p.get("color", "#FF0000"))
    key = (255, 0, 255)
    c = raster.Canvas(size, size, key)
    r = size / 2.0 - 0.5
    cx = cy = (size - 1) / 2.0
    for y in range(size):
        for x in range(size):
            dx, dy = x - cx, y - cy
            if dx * dx + dy * dy > r * r + 0.5:
                continue
            light = 1.0 - (((dx + r * 0.45) ** 2 + (dy + r * 0.45) ** 2) ** 0.5) / (r * 2.0)
            shade = 0.45 + 0.75 * max(0.0, light)
            col = tuple(min(255, int(ch * shade)) for ch in base)
            if (x - cx + r * 0.4) ** 2 + (y - cy + r * 0.4) ** 2 < (r * 0.28) ** 2:
                col = (255, 255, 255)
            c.set(x, y, color.snap_per_channel(col))
    return [("", raster.encode_frames([c], transparent_rgb=key))]


def k_digits(p):
    fg, bg = rgb(p.get("fg", "#00FF00")), rgb(p.get("bg", "#000000"))
    hi, lo = rgb(p.get("frame_light", "#666666")), rgb(p.get("frame_dark", "#333333"))
    out = []
    for d in "0123456789":
        c = raster.Canvas(14, 20, bg)
        c.hline(0, 0, 14, hi)
        c.hline(0, 19, 14, lo)
        c.vline(0, 0, 20, hi)
        c.vline(13, 0, 20, lo)
        c.text(2, 3, d, fg, scale=2)
        out.append((d, raster.encode_frames([c])))
    return out


def _badge_canvas(p, lines, fg, bg):
    c = raster.Canvas(88, 31, bg)
    border = p.get("border", "bevel")
    if border == "bevel":
        c.bevel(0, 0, 88, 31, rgb(p.get("light", "#FFFFFF")), rgb(p.get("dark", "#666666")), depth=1)
    else:
        c.rect(0, 0, 88, 31, rgb(p.get("border_color", "#FFFFFF")))
    accent = p.get("accent")
    if accent:
        c.fill_rect(2, 2, 84, 2, rgb(accent))
        c.fill_rect(2, 27, 84, 2, rgb(accent))
    if len(lines) == 1:
        c.text_centered(12, lines[0], fg)
    else:
        c.text_centered(7, lines[0], fg)
        c.text_centered(17, lines[1], rgb(p.get("fg2", p.get("fg", "#FFFFFF"))))
    return c


def k_badge(p):
    lines = [s[:14] for s in p.get("lines", ["HOMESTEAD", "RETRO WEB"])]
    fg, bg = rgb(p.get("fg", "#FFFFFF")), rgb(p.get("bg", "#000099"))
    return [("", raster.encode_frames([_badge_canvas(p, lines, fg, bg)]))]


def k_emailme(p):
    bg, fg = rgb(p.get("bg", "#000066")), rgb(p.get("fg", "#FFFF00"))
    paper, ink = rgb("#FFFFFF"), rgb("#000000")
    frames = []
    for lift in (0, 2):
        c = raster.Canvas(88, 31, bg)
        c.bevel(0, 0, 88, 31, rgb("#9999FF"), rgb("#000033"), depth=1)
        ex, ey = 6, 9 - lift
        c.fill_rect(ex, ey, 22, 14, paper)
        c.rect(ex, ey, 22, 14, ink)
        for i in range(11):
            c.set(ex + i, ey + i // 2 + 1, ink)
            c.set(ex + 21 - i, ey + i // 2 + 1, ink)
        c.text(34, 7, "EMAIL", fg)
        c.text(34, 17, "ME!", rgb("#00FFFF"))
        frames.append(c)
    anim, still = _animated(frames, p.get("delay_cs", 70))
    return [("", anim), ("-still", still)]


def k_wordart(p):
    text = p["text"]
    scale = p.get("scale", 4)
    rows = [rgb(x) for x in p.get("row_colors", ["#FFFF00", "#FFCC00", "#FF9900", "#FF6600", "#FF3300", "#CC0000", "#990000"])]
    shadow = rgb(p["shadow"]) if p.get("shadow") else None
    key = rgb(p.get("bg", "#FF00FF"))
    pad = p.get("pad", 4)
    w = raster.text_width(text, scale) + pad * 2 + scale
    h = 7 * scale + pad * 2 + scale
    c = raster.Canvas(w, h, key)
    if p.get("outline"):
        oc = rgb(p["outline"])
        for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            c.text(pad + ox, pad + oy, text, oc, scale=scale)
    big_rows = []
    for color_row in rows:
        big_rows.append(color_row)
    c.text(pad, pad, text, None, scale=scale, shadow=shadow, row_colors=big_rows)
    transparent = key if p.get("transparent", True) else None
    return [("", raster.encode_frames([c], transparent_rgb=transparent))]


def k_navbutton(p):
    label = p["label"]
    w, h = p.get("width", 120), p.get("height", 24)
    out = []
    for suffix, face, ink, raised in (("", p.get("face", "#336699"), p.get("text", "#FFFFFF"), True),
                                      ("-over", p.get("over_face", "#FFCC00"), p.get("over_text", "#000033"), False)):
        c = raster.Canvas(w, h, rgb(face))
        c.bevel(0, 0, w, h, rgb(p.get("light", "#99CCFF")), rgb(p.get("dark", "#003366")), depth=2, raised=raised)
        shift = 0 if raised else 1
        c.text_centered((h - 7) // 2 + shift, label.upper(), rgb(ink), x0=shift)
        out.append((suffix, raster.encode_frames([c])))
    return out


def k_banner(p):
    text = p["text"].upper()
    w, h = p.get("width", 480), p.get("height", 56)
    c = raster.Canvas(w, h, rgb(p.get("bg", "#FFFFFF")))
    bars = [rgb(x) for x in p.get("bars", ["#003366", "#336699", "#6699CC", "#99CCFF"])]
    for i, bar in enumerate(bars):
        c.fill_rect(0, 6 + i * 11, 70 - i * 14, 9, bar)
    c.hline(0, h - 3, w, rgb(p.get("rule", "#003366")))
    c.hline(0, h - 1, w, rgb(p.get("rule2", "#6699CC")))
    scale = 3
    if raster.text_width(text, 3) > w - 90:
        scale = 2
    c.text(84, (h - 7 * scale) // 2 - 2, text, rgb(p.get("fg", "#003366")), scale=scale, shadow=rgb(p.get("shadow", "#99CCFF")))
    return [("", raster.encode_frames([c]))]


def k_tile(p):
    w, h = p.get("width", 40), p.get("height", 20)
    c = raster.Canvas(w, h, rgb(p.get("bg", "#FFFFFF")))
    c.hline(0, h - 1, w, rgb(p.get("line", "#CCCCFF")))
    if p.get("vline"):
        c.vline(w - 1, 0, h, rgb(p["vline"]))
    return [("", raster.encode_frames([c]))]


def _mask(text, scale):
    w = raster.text_width(text, scale)
    h = 7 * scale
    mask = [[False] * w for _ in range(h)]
    cursor = 0
    for ch in text:
        for ry, bits in enumerate(raster.glyph(ch)):
            for rx, bit in enumerate(bits):
                if bit == "1":
                    for yy in range(scale):
                        for xx in range(scale):
                            mask[ry * scale + yy][cursor + rx * scale + xx] = True
        cursor += 6 * scale
    return mask


def k_glitter(p):
    text = p["text"].upper()
    scale = p.get("scale", 3)
    pad = 2
    mask = _mask(text, scale)
    mh, mw = len(mask), len(mask[0])
    w, h = mw + pad * 2, mh + pad * 2
    bg = rgb(p.get("bg", "#000000"))
    base = [rgb(x) for x in p.get("base", ["#FF66CC", "#FF99CC", "#CC66FF"])]
    sparkle = [rgb(x) for x in p.get("sparkle", ["#FFFFFF", "#FFFFCC", "#CCFFFF"])]
    outline = rgb(p.get("outline", "#660066"))
    density = p.get("density", 0.16)
    frames = []
    for f in range(p.get("frames", 3)):
        rnd = random.Random(p.get("seed", 11) * 31 + f)
        c = raster.Canvas(w, h, bg)
        for y in range(mh):
            for x in range(mw):
                if mask[y][x]:
                    col = base[(x // max(1, scale) + y // max(1, scale) + f) % len(base)]
                    if rnd.random() < density:
                        col = sparkle[rnd.randrange(len(sparkle))]
                    c.set(x + pad, y + pad, col)
                else:
                    near = any(0 <= y + dy < mh and 0 <= x + dx < mw and mask[y + dy][x + dx]
                               for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                    if near:
                        c.set(x + pad, y + pad, outline)
        frames.append(c)
    transparent = bg if p.get("transparent", False) else None
    anim, still = _animated(frames, p.get("delay_cs", 40), transparent)
    return [("", anim), ("-still", still)]


def k_blinkie(p):
    text = p["text"].upper()[:24]
    w, h = p.get("width", 150), p.get("height", 20)
    pairs = [(rgb(p.get("fg1", "#FF0099")), rgb(p.get("bg1", "#FFCCFF"))),
             (rgb(p.get("fg2", "#FFFFFF")), rgb(p.get("bg2", "#FF66CC")))]
    border = rgb(p.get("border", "#990066"))
    frames = []
    for fg, bg in pairs:
        c = raster.Canvas(w, h, bg)
        c.rect(0, 0, w, h, border)
        c.text_centered((h - 7) // 2, text, fg)
        frames.append(c)
    anim, still = _animated(frames, p.get("delay_cs", 60))
    return [("", anim), ("-still", still)]


def k_online(p):
    text = p.get("text", "ONLINE NOW!")
    w = raster.text_width(text) + 4
    frames = []
    for fg in (p.get("fg1", "#FF9900"), p.get("fg2", "#FFCC00")):
        c = raster.Canvas(w, 11, rgb(p.get("bg", "#000000")))
        c.text(2, 2, text, rgb(fg))
        frames.append(c)
    anim, still = _animated(frames, p.get("delay_cs", 70))
    return [("", anim), ("-still", still)]


def k_avatar(p):
    size = p.get("size", 48)
    cells = 6
    rnd = random.Random(p.get("seed", 1))
    levels = color.LEVELS
    fg = (rnd.choice(levels[2:]), rnd.choice(levels), rnd.choice(levels[1:]))
    bg = rgb(p.get("bg", "#FFFFFF"))
    c = raster.Canvas(size, size, bg)
    cell = size // cells
    for y in range(cells):
        for x in range(cells // 2):
            if rnd.random() < 0.5:
                c.fill_rect(x * cell, y * cell, cell, cell, fg)
                c.fill_rect((cells - 1 - x) * cell, y * cell, cell, cell, fg)
    c.rect(0, 0, size, size, rgb(p.get("border", "#000000")))
    return [("", raster.encode_frames([c]))]


def k_appwindow(p):
    w, h = p.get("width", 320), p.get("height", 200)
    gray, white, black = rgb("#C0C0C0"), rgb("#FFFFFF"), rgb("#000000")
    navy, dark = rgb(p.get("title_bg", "#000080")), rgb("#808080")
    c = raster.Canvas(w, h, gray)
    c.bevel(0, 0, w, h, white, dark, depth=2)
    c.fill_rect(3, 3, w - 6, 13, navy)
    c.text(6, 6, p.get("title", "PROGRAM").upper()[: (w - 40) // 6], white)
    for i in range(3):
        bx = w - 15 - i * 12
        c.fill_rect(bx, 5, 10, 9, gray)
        c.bevel(bx, 5, 10, 9, white, dark, depth=1)
    c.text(6, 19, p.get("menu", "FILE  EDIT  VIEW  HELP"), black)
    top, bottom = 29, h - 16
    c.fill_rect(5, top, w - 10, bottom - top, white)
    c.bevel(5, top, w - 10, bottom - top, dark, white, depth=1)
    cols = p.get("columns", ["DATE", "ITEM", "AMOUNT"])
    col_w = (w - 12) // len(cols)
    c.fill_rect(6, top + 1, w - 12, 11, gray)
    for i, name in enumerate(cols):
        c.text(9 + i * col_w, top + 3, name.upper()[: col_w // 6], black)
        if i:
            c.vline(6 + i * col_w, top + 1, bottom - top - 2, rgb("#CCCCCC"))
    row_y = top + 14
    for row in p.get("rows", []):
        if row_y + 9 > bottom:
            break
        for i, cell in enumerate(row):
            c.text(9 + i * col_w, row_y, str(cell).upper()[: col_w // 6], rgb(p.get("ink", "#000000")))
        row_y += 10
    c.text(8, h - 12, p.get("status", "READY"), black)
    return [("", raster.encode_frames([c]))]


def k_chiptune(p):
    tune = tunes.TUNES[p.get("tune", "ode-to-joy")]
    wav = audio.render_wav(tune["notes"], bpm=tune["bpm"])
    mid = audio.render_midi(tune["notes"], bpm=tune["bpm"])
    return [("", wav), ("@mid", mid)]


KINDS = {
    "spacer": k_spacer, "stars": k_stars, "rainbow": k_rainbow, "construction": k_construction,
    "new": k_new, "ball": k_ball, "digits": k_digits, "badge": k_badge, "emailme": k_emailme,
    "wordart": k_wordart, "navbutton": k_navbutton, "banner": k_banner, "tile": k_tile,
    "glitter": k_glitter, "blinkie": k_blinkie, "online": k_online, "avatar": k_avatar,
    "appwindow": k_appwindow, "chiptune": k_chiptune,
}


def render(kind, params, out_path):
    """Render one asset. Returns the list of written file paths."""
    results = KINDS[kind](params)
    written = []
    stem, ext = os.path.splitext(out_path)
    for suffix, payload in results:
        if kind == "digits":
            path = os.path.join(out_path, "d%s.gif" % suffix)
        elif suffix == "@mid":
            path = stem + ".mid"
        else:
            path = stem + suffix + ext
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "wb") as handle:
            handle.write(payload)
        written.append(path)
    return written


LIBRARY = os.path.join(canon.REPO_ROOT, "kits", "shared", "recipe.json")


def resolve_recipe(recipe):
    """Expand include names from the shared library, then append own assets."""
    items = []
    if recipe.get("include"):
        with open(LIBRARY, "r", encoding="utf-8") as handle:
            library = {a["name"]: a for a in json.load(handle)["assets"]}
        for name in recipe["include"]:
            if name not in library:
                raise KeyError("recipe includes unknown library asset: %s" % name)
            items.append(library[name])
    items += recipe.get("assets", [])
    return items


def run_recipe(recipe_path, out_dir):
    with open(recipe_path, "r", encoding="utf-8") as handle:
        recipe = json.load(handle)
    if os.path.abspath(recipe_path) == os.path.abspath(LIBRARY):
        recipe = {"assets": recipe["assets"]}
    written = []
    for item in resolve_recipe(recipe):
        written += render(item["kind"], item.get("params", {}), os.path.join(out_dir, item["out"]))
    return written


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("kinds", help="list asset kinds")
    rp = sub.add_parser("recipe", help="render every asset in a recipe file")
    rp.add_argument("recipe")
    rp.add_argument("--out", required=True)
    one = sub.add_parser("one", help="render a single asset")
    one.add_argument("kind", choices=sorted(KINDS))
    one.add_argument("outfile")
    one.add_argument("--params", default="{}")
    args = parser.parse_args(argv)
    if args.cmd == "kinds":
        for name in sorted(KINDS):
            doc = KINDS[name].__doc__ or ""
            print(name + ("  " + doc.strip() if doc else ""))
        return 0
    if args.cmd == "recipe":
        for path in run_recipe(args.recipe, args.out):
            print(path)
        return 0
    for path in render(args.kind, json.loads(args.params), args.outfile):
        print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
