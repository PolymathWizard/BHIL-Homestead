#!/usr/bin/env python3
"""dither: turn a modern photo or screenshot into a period GIF.

Downscales an 8-bit PNG, then quantizes it either to the 216 web-safe colors
or to an adaptive palette (median cut), with optional Floyd-Steinberg error
diffusion. Period guidance kept the web-safe palette for flat art and used
adaptive palettes for photos (claim C-004), so adaptive is the default.

Usage:
    python3 tools/dither.py in.png out.gif --max-width 320
    python3 tools/dither.py in.png out.gif --palette websafe --no-dither
    python3 tools/dither.py in.png out.gif --palette adaptive --colors 32

Input must be a non-interlaced 8-bit PNG. Convert JPEG or other formats to
PNG first with any image tool. Stdlib only.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hs_core import color, gif, png  # noqa: E402


def downscale(width, height, rows, max_width):
    """Box-filter downscale to max_width, flattening alpha onto white."""
    flat = [[(r * a // 255 + 255 * (255 - a) // 255,
              g * a // 255 + 255 * (255 - a) // 255,
              b * a // 255 + 255 * (255 - a) // 255) for (r, g, b, a) in row] for row in rows]
    if width <= max_width:
        return width, height, flat
    nw = max_width
    nh = max(1, round(height * nw / width))
    out = []
    for y in range(nh):
        y0, y1 = y * height // nh, max(y * height // nh + 1, (y + 1) * height // nh)
        line = []
        for x in range(nw):
            x0, x1 = x * width // nw, max(x * width // nw + 1, (x + 1) * width // nw)
            acc = [0, 0, 0]
            n = 0
            for yy in range(y0, y1):
                src = flat[yy]
                for xx in range(x0, x1):
                    p = src[xx]
                    acc[0] += p[0]
                    acc[1] += p[1]
                    acc[2] += p[2]
                    n += 1
            line.append(tuple(v // n for v in acc))
        out.append(line)
    return nw, nh, out


def median_cut(pixels, count):
    boxes = [list(pixels)]
    while len(boxes) < count:
        boxes.sort(key=len, reverse=True)
        box = boxes.pop(0)
        if len(box) < 2:
            boxes.append(box)
            break
        ranges = [max(p[i] for p in box) - min(p[i] for p in box) for i in range(3)]
        axis = ranges.index(max(ranges))
        box.sort(key=lambda p: p[axis])
        mid = len(box) // 2
        boxes += [box[:mid], box[mid:]]
    palette = []
    for box in boxes:
        if box:
            palette.append(tuple(sum(p[i] for p in box) // len(box) for i in range(3)))
    return palette


def quantize(width, height, rows, palette, dither=True):
    cache = {}

    def nearest(rgb):
        if rgb not in cache:
            cache[rgb] = min(range(len(palette)), key=lambda i: sum((a - b) ** 2 for a, b in zip(rgb, palette[i])))
        return cache[rgb]

    work = [[list(px) for px in row] for row in rows]
    out = bytearray(width * height)
    for y in range(height):
        for x in range(width):
            old = tuple(max(0, min(255, int(v))) for v in work[y][x])
            idx = nearest(old)
            out[y * width + x] = idx
            if not dither:
                continue
            err = [o - n for o, n in zip(old, palette[idx])]
            for dx, dy, f in ((1, 0, 7 / 16), (-1, 1, 3 / 16), (0, 1, 5 / 16), (1, 1, 1 / 16)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    cell = work[ny][nx]
                    for i in range(3):
                        cell[i] += err[i] * f
    return bytes(out)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Dither a PNG into a period GIF.")
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--max-width", type=int, default=320)
    parser.add_argument("--palette", choices=["adaptive", "websafe"], default="adaptive")
    parser.add_argument("--colors", type=int, default=64)
    parser.add_argument("--no-dither", action="store_true")
    args = parser.parse_args(argv)
    with open(args.input, "rb") as handle:
        width, height, rows = png.decode(handle.read())
    width, height, rows = downscale(width, height, rows, args.max_width)
    if args.palette == "websafe":
        palette = color.websafe_palette()
    else:
        sample = [px for row in rows[::2] for px in row[::2]] or [px for row in rows for px in row]
        palette = median_cut(sample, max(2, min(256, args.colors)))
    frame = quantize(width, height, rows, palette, dither=not args.no_dither)
    used = sorted(set(frame))
    remap = {old: new for new, old in enumerate(used)}
    compact = [palette[i] for i in used]
    data = gif.encode(width, height, compact, [bytes(remap[p] for p in frame)])
    with open(args.output, "wb") as handle:
        handle.write(data)
    print("%s %dx%d %d colors (%s%s)" % (args.output, width, height, len(compact), args.palette,
                                         "" if args.no_dither else ", Floyd-Steinberg"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
