"""Color helpers: hex parsing, web-safe snapping, CIELAB distance.

The web-safe palette is every combination of 00, 33, 66, 99, CC, FF across
red, green, and blue (claim C-003). Snapping rounds each channel to the
nearest multiple of 0x33. When that per-channel snap moves a brand color too
far perceptually, HOMESTEAD picks the perceptually nearest web-safe color
instead (CIE76 delta E in CIELAB).
"""

import re

LEVELS = (0x00, 0x33, 0x66, 0x99, 0xCC, 0xFF)
HEX_RE = re.compile(r"#?([0-9a-fA-F]{6}|[0-9a-fA-F]{3})$")


def parse_hex(text):
    """Parse #RGB or #RRGGBB into an (r, g, b) tuple of ints."""
    match = HEX_RE.match(text.strip())
    if not match:
        raise ValueError("Not a hex color: %r" % text)
    body = match.group(1)
    if len(body) == 3:
        body = "".join(ch * 2 for ch in body)
    return tuple(int(body[i:i + 2], 16) for i in (0, 2, 4))


def to_hex(rgb):
    return "#%02X%02X%02X" % tuple(int(c) for c in rgb)


def is_websafe(rgb):
    return all(c in LEVELS for c in rgb)


def snap_channel(value):
    """Nearest multiple of 51. Ties round up, matching 0x33 arithmetic."""
    return min(LEVELS, key=lambda level: (abs(level - value), -level))


def snap_per_channel(rgb):
    return tuple(snap_channel(c) for c in rgb)


def websafe_palette():
    return [(r, g, b) for r in LEVELS for g in LEVELS for b in LEVELS]


def _srgb_to_linear(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb):
    """WCAG relative luminance, 0.0 to 1.0."""
    r, g, b = (_srgb_to_linear(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def to_lab(rgb):
    r, g, b = (_srgb_to_linear(c) for c in rgb)
    x = (r * 0.4124 + g * 0.3576 + b * 0.1805) / 0.95047
    y = (r * 0.2126 + g * 0.7152 + b * 0.0722) / 1.00000
    z = (r * 0.0193 + g * 0.1192 + b * 0.9505) / 1.08883

    def f(t):
        return t ** (1.0 / 3.0) if t > 0.008856 else (7.787 * t) + (16.0 / 116.0)

    fx, fy, fz = f(x), f(y), f(z)
    return (116.0 * fy - 16.0, 500.0 * (fx - fy), 200.0 * (fy - fz))


def delta_e(rgb_a, rgb_b):
    la, lb = to_lab(rgb_a), to_lab(rgb_b)
    return sum((p - q) ** 2 for p, q in zip(la, lb)) ** 0.5


def nearest_websafe_perceptual(rgb):
    return min(websafe_palette(), key=lambda cand: delta_e(rgb, cand))


def snap(rgb, switch_delta_e=10.0):
    """Return a dict describing the web-safe snap of one color.

    method is "per-channel" unless that result is more than switch_delta_e
    away, in which case the perceptual nearest is used.
    """
    per_channel = snap_per_channel(rgb)
    de_channel = delta_e(rgb, per_channel)
    perceptual = nearest_websafe_perceptual(rgb)
    de_perceptual = delta_e(rgb, perceptual)
    if de_channel > switch_delta_e and de_perceptual < de_channel:
        chosen, method, de = perceptual, "perceptual", de_perceptual
    else:
        chosen, method, de = per_channel, "per-channel", de_channel
    return {
        "original": to_hex(rgb),
        "snapped": to_hex(chosen),
        "method": method,
        "delta_e": round(de, 2),
        "per_channel": to_hex(per_channel),
        "perceptual": to_hex(perceptual),
        "already_safe": is_websafe(rgb),
    }


def contrast_ratio(rgb_a, rgb_b):
    la, lb = relative_luminance(rgb_a), relative_luminance(rgb_b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)
