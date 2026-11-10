"""Palette canvas, bevel drawing, and a 5x7 pixel font.

Everything HOMESTEAD draws is original: shapes and a hand-entered bitmap
font, so generated assets carry no third-party rights (ADR-004).
"""

from . import gif as gifcodec

GLYPHS = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11100", "10010", "10001", "10001", "10001", "10010", "11100"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "10001", "11001", "10101", "10011", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "10001", "01010", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000",) * 7,
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00010", "00100", "00000", "00100"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "-": ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "/": ("00000", "00001", "00010", "00100", "01000", "10000", "00000"),
    "'": ("01100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "\"": ("01010", "01010", "01010", "00000", "00000", "00000", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "#": ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    "@": ("01110", "10001", "00001", "01101", "10101", "10101", "01110"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "*": ("00000", "00100", "10101", "01110", "10101", "00100", "00000"),
    "<": ("00010", "00100", "01000", "10000", "01000", "00100", "00010"),
    ">": ("01000", "00100", "00010", "00001", "00010", "00100", "01000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    "~": ("00000", "00000", "01000", "10101", "00010", "00000", "00000"),
    "%": ("11000", "11001", "00010", "00100", "01000", "10011", "00011"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "|": ("00100", "00100", "00100", "00100", "00100", "00100", "00100"),
    "♥": ("00000", "01010", "11111", "11111", "01110", "00100", "00000"),
    "♪": ("00110", "00101", "00100", "00100", "11100", "11100", "00000"),
}

GLYPH_W = 5
GLYPH_H = 7


def glyph(ch):
    return GLYPHS.get(ch.upper(), GLYPHS["?"])


def text_width(text, scale=1, spacing=1):
    if not text:
        return 0
    return len(text) * (GLYPH_W + spacing) * scale - spacing * scale


class Canvas:
    """A palette-indexed raster. Colors are registered by RGB tuple."""

    def __init__(self, width, height, background=(0, 0, 0)):
        self.width = width
        self.height = height
        self.palette = []
        self._index = {}
        bg = self.color(background)
        self.pixels = bytearray([bg]) * (width * height)

    def color(self, rgb):
        rgb = tuple(int(c) for c in rgb)
        if rgb not in self._index:
            if len(self.palette) >= 256:
                raise ValueError("palette full")
            self._index[rgb] = len(self.palette)
            self.palette.append(rgb)
        return self._index[rgb]

    def copy(self):
        clone = Canvas.__new__(Canvas)
        clone.width = self.width
        clone.height = self.height
        clone.palette = list(self.palette)
        clone._index = dict(self._index)
        clone.pixels = bytearray(self.pixels)
        return clone

    def set(self, x, y, rgb):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y * self.width + x] = self.color(rgb)

    def get(self, x, y):
        return self.palette[self.pixels[y * self.width + x]]

    def fill_rect(self, x, y, w, h, rgb):
        idx = self.color(rgb)
        for yy in range(max(0, y), min(self.height, y + h)):
            row = yy * self.width
            for xx in range(max(0, x), min(self.width, x + w)):
                self.pixels[row + xx] = idx

    def hline(self, x, y, w, rgb):
        self.fill_rect(x, y, w, 1, rgb)

    def vline(self, x, y, h, rgb):
        self.fill_rect(x, y, 1, h, rgb)

    def rect(self, x, y, w, h, rgb):
        self.hline(x, y, w, rgb)
        self.hline(x, y + h - 1, w, rgb)
        self.vline(x, y, h, rgb)
        self.vline(x + w - 1, y, h, rgb)

    def bevel(self, x, y, w, h, light, dark, depth=2, raised=True):
        """Windows-style raised or sunken bevel border."""
        top, bottom = (light, dark) if raised else (dark, light)
        for d in range(depth):
            self.hline(x + d, y + d, w - 2 * d, top)
            self.vline(x + d, y + d, h - 2 * d, top)
            self.hline(x + d, y + h - 1 - d, w - 2 * d, bottom)
            self.vline(x + w - 1 - d, y + d, h - 2 * d, bottom)

    def text(self, x, y, text, rgb, scale=1, spacing=1, shadow=None, row_colors=None):
        """Draw text with the 5x7 font. row_colors paints each glyph row."""
        cursor = x
        for ch in text:
            rows = glyph(ch)
            for ry, bits in enumerate(rows):
                for rx, bit in enumerate(bits):
                    if bit != "1":
                        continue
                    color = row_colors[ry] if row_colors else rgb
                    px, py = cursor + rx * scale, y + ry * scale
                    if shadow is not None:
                        self.fill_rect(px + scale, py + scale, scale, scale, shadow)
                    self.fill_rect(px, py, scale, scale, color)
            cursor += (GLYPH_W + spacing) * scale
        return cursor

    def text_centered(self, y, text, rgb, scale=1, spacing=1, shadow=None, row_colors=None, x0=0, width=None):
        width = self.width if width is None else width
        tw = text_width(text, scale, spacing)
        x = x0 + (width - tw) // 2
        return self.text(x, y, text, rgb, scale, spacing, shadow, row_colors)


def encode_frames(canvases, delays_cs=None, loop=0, transparent_rgb=None):
    """Encode one or more canvases (same size) into GIF bytes.

    All frames share one global palette built in first-seen order, which keeps
    output deterministic.
    """
    first = canvases[0]
    palette = []
    index = {}
    for canvas in canvases:
        for rgb in canvas.palette:
            if rgb not in index:
                index[rgb] = len(palette)
                palette.append(rgb)
    if transparent_rgb is not None and transparent_rgb not in index:
        index[transparent_rgb] = len(palette)
        palette.append(transparent_rgb)
    frames = []
    for canvas in canvases:
        remap = bytes(index[rgb] for rgb in canvas.palette)
        frames.append(bytes(remap[p] for p in canvas.pixels))
    transparent = index[transparent_rgb] if transparent_rgb is not None else None
    return gifcodec.encode(first.width, first.height, palette, frames, delays_cs, loop, transparent)
