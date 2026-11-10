"""Minimal PNG decoder.

Supports non-interlaced 8-bit images of color types 0 (gray), 2 (RGB),
3 (palette), 4 (gray plus alpha), and 6 (RGBA). That covers screenshots and
exported photos. Convert anything else (JPEG, 16-bit, interlaced) to an
8-bit PNG first with any image tool.
"""

import struct
import zlib


class PngError(ValueError):
    pass


def _paeth(a, b, c):
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    return b if pb <= pc else c


def decode(data):
    """Return (width, height, rows) where rows is a list of lists of (r, g, b, a)."""
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise PngError("not a PNG")
    pos = 8
    width = height = depth = ctype = interlace = None
    palette = []
    trns = b""
    idat = bytearray()
    while pos < len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        kind = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + length]
        pos += 12 + length
        if kind == b"IHDR":
            width, height, depth, ctype, _comp, _filt, interlace = struct.unpack(">IIBBBBB", body)
        elif kind == b"PLTE":
            palette = [tuple(body[i:i + 3]) for i in range(0, len(body), 3)]
        elif kind == b"tRNS":
            trns = body
        elif kind == b"IDAT":
            idat += body
        elif kind == b"IEND":
            break
    if width is None:
        raise PngError("missing IHDR")
    if depth != 8 or interlace != 0 or ctype not in (0, 2, 3, 4, 6):
        raise PngError("unsupported PNG: depth %s, color type %s, interlace %s" % (depth, ctype, interlace))
    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ctype]
    raw = zlib.decompress(bytes(idat))
    stride = width * channels
    rows = []
    prev = bytearray(stride)
    offset = 0
    for _y in range(height):
        ftype = raw[offset]
        line = bytearray(raw[offset + 1:offset + 1 + stride])
        offset += 1 + stride
        for i in range(stride):
            left = line[i - channels] if i >= channels else 0
            up = prev[i]
            upleft = prev[i - channels] if i >= channels else 0
            if ftype == 1:
                line[i] = (line[i] + left) & 0xFF
            elif ftype == 2:
                line[i] = (line[i] + up) & 0xFF
            elif ftype == 3:
                line[i] = (line[i] + ((left + up) >> 1)) & 0xFF
            elif ftype == 4:
                line[i] = (line[i] + _paeth(left, up, upleft)) & 0xFF
        prev = line
        pixels = []
        for x in range(width):
            px = line[x * channels:(x + 1) * channels]
            if ctype == 0:
                pixels.append((px[0], px[0], px[0], 255))
            elif ctype == 2:
                pixels.append((px[0], px[1], px[2], 255))
            elif ctype == 3:
                r, g, b = palette[px[0]]
                a = trns[px[0]] if px[0] < len(trns) else 255
                pixels.append((r, g, b, a))
            elif ctype == 4:
                pixels.append((px[0], px[0], px[0], px[1]))
            else:
                pixels.append((px[0], px[1], px[2], px[3]))
        rows.append(pixels)
    return width, height, rows


def encode_rgb(width, height, rows):
    """Encode rows of (r, g, b) tuples as an RGB PNG. Used by tests."""
    raw = bytearray()
    for row in rows:
        raw.append(0)
        for r, g, b in row:
            raw += bytes((r, g, b))

    def chunk(kind, body):
        return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body) & 0xFFFFFFFF)

    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))
