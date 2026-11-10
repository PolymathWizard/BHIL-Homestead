"""GIF89a encoder and decoder in pure Python.

Encoder: palette-indexed frames, per-frame delays in centiseconds, optional
transparency, NETSCAPE2.0 looping. Output is deterministic for identical
input, which the drift gate relies on.

Decoder: enough of the format to audit animations. It reads the logical
screen, color tables, graphic control extensions, image descriptors, and LZW
data, then composites frames honoring disposal methods 0 to 3 so that
tools/gif_audit.py can measure luminance change between displayed frames.
"""

import struct


# ---------------------------------------------------------------------------
# Encoder
# ---------------------------------------------------------------------------

def _palette_bits(count):
    bits = 1
    while (1 << bits) < count:
        bits += 1
    return bits


def lzw_encode(indices, min_code_size):
    """Return LZW-compressed bytes for a sequence of palette indices."""
    clear = 1 << min_code_size
    eoi = clear + 1
    code_size = min_code_size + 1
    next_code = eoi + 1
    table = {}
    out = bytearray()
    state = {"buf": 0, "count": 0}

    def emit(code, size):
        state["buf"] |= code << state["count"]
        state["count"] += size
        while state["count"] >= 8:
            out.append(state["buf"] & 0xFF)
            state["buf"] >>= 8
            state["count"] -= 8

    emit(clear, code_size)
    if not indices:
        emit(eoi, code_size)
        if state["count"]:
            out.append(state["buf"] & 0xFF)
        return bytes(out)

    prefix = indices[0]
    for pixel in indices[1:]:
        key = (prefix, pixel)
        found = table.get(key)
        if found is not None:
            prefix = found
            continue
        emit(prefix, code_size)
        table[key] = next_code
        next_code += 1
        if next_code > (1 << code_size) and code_size < 12:
            code_size += 1
        if next_code >= 4096:
            emit(clear, code_size)
            table = {}
            code_size = min_code_size + 1
            next_code = eoi + 1
        prefix = pixel
    emit(prefix, code_size)
    emit(eoi, code_size)
    if state["count"]:
        out.append(state["buf"] & 0xFF)
    return bytes(out)


def _sub_blocks(data):
    out = bytearray()
    for start in range(0, len(data), 255):
        chunk = data[start:start + 255]
        out.append(len(chunk))
        out.extend(chunk)
    out.append(0)
    return bytes(out)


def encode(width, height, palette, frames, delays_cs=None, loop=0, transparent=None):
    """Encode frames into GIF89a bytes.

    palette     list of (r, g, b) tuples, at most 256
    frames      list of bytes-like objects of length width * height
    delays_cs   list of per-frame delays in centiseconds (ignored for stills)
    loop        NETSCAPE2.0 loop count, 0 means forever; None omits the block
    transparent palette index treated as transparent, or None
    """
    if not 1 <= len(palette) <= 256:
        raise ValueError("palette must hold 1 to 256 colors")
    for frame in frames:
        if len(frame) != width * height:
            raise ValueError("frame size does not match dimensions")
    bits = _palette_bits(max(2, len(palette)))
    table_size = 1 << bits
    padded = list(palette) + [(0, 0, 0)] * (table_size - len(palette))
    animated = len(frames) > 1
    if delays_cs is None:
        delays_cs = [0] * len(frames)

    out = bytearray(b"GIF89a")
    out += struct.pack("<HHBBB", width, height, 0x80 | ((bits - 1) << 4) | (bits - 1), 0, 0)
    for r, g, b in padded:
        out += bytes((r, g, b))
    if animated and loop is not None:
        out += b"\x21\xFF\x0BNETSCAPE2.0\x03\x01" + struct.pack("<H", loop) + b"\x00"
    min_code_size = max(2, bits)
    for index, frame in enumerate(frames):
        if animated or transparent is not None:
            flags = 0
            if transparent is not None:
                flags |= 0x01
            flags |= (1 << 2)  # disposal 1: leave in place
            out += b"\x21\xF9\x04" + bytes((flags,)) + struct.pack("<H", delays_cs[index] if animated else 0)
            out += bytes((transparent if transparent is not None else 0,)) + b"\x00"
        out += b"\x2C" + struct.pack("<HHHHB", 0, 0, width, height, 0)
        out.append(min_code_size)
        out += _sub_blocks(lzw_encode(bytes(frame), min_code_size))
    out.append(0x3B)
    return bytes(out)


# ---------------------------------------------------------------------------
# Decoder
# ---------------------------------------------------------------------------

class GifFormatError(ValueError):
    pass


def lzw_decode(data, min_code_size, pixel_count):
    clear = 1 << min_code_size
    eoi = clear + 1
    code_size = min_code_size + 1
    table = [bytes((i,)) for i in range(clear)] + [b"", b""]
    out = bytearray()
    buf = 0
    count = 0
    prev = None
    pos = 0
    while len(out) < pixel_count:
        while count < code_size:
            if pos >= len(data):
                return bytes(out[:pixel_count]) + bytes(pixel_count - min(len(out), pixel_count))
            buf |= data[pos] << count
            pos += 1
            count += 8
        code = buf & ((1 << code_size) - 1)
        buf >>= code_size
        count -= code_size
        if code == clear:
            table = [bytes((i,)) for i in range(clear)] + [b"", b""]
            code_size = min_code_size + 1
            prev = None
            continue
        if code == eoi:
            break
        if prev is None:
            entry = table[code]
            out += entry
            prev = entry
            continue
        if code < len(table):
            entry = table[code]
            if len(table) < 4096:
                table.append(prev + entry[:1])
        elif code == len(table):
            entry = prev + prev[:1]
            table.append(entry)
        else:
            raise GifFormatError("invalid LZW code %d" % code)
        out += entry
        prev = entry
        if len(table) >= (1 << code_size) and code_size < 12:
            code_size += 1
    if len(out) < pixel_count:
        out += bytes(pixel_count - len(out))
    return bytes(out[:pixel_count])


def _read_sub_blocks(data, pos):
    chunks = bytearray()
    while True:
        size = data[pos]
        pos += 1
        if size == 0:
            return bytes(chunks), pos
        chunks += data[pos:pos + size]
        pos += size


def decode(data):
    """Decode GIF bytes into a dict with composited RGB frames and timing."""
    if data[:6] not in (b"GIF87a", b"GIF89a"):
        raise GifFormatError("not a GIF")
    width, height, flags, bg_index, _aspect = struct.unpack("<HHBBB", data[6:13])
    pos = 13
    global_table = None
    if flags & 0x80:
        size = 1 << ((flags & 0x07) + 1)
        global_table = [tuple(data[pos + i * 3:pos + i * 3 + 3]) for i in range(size)]
        pos += size * 3
    canvas = [None] * (width * height)  # None means transparent
    frames = []
    gce = {"delay_cs": 0, "transparent": None, "disposal": 0}
    loop = None
    while pos < len(data):
        block = data[pos]
        pos += 1
        if block == 0x3B:
            break
        if block == 0x21:
            label = data[pos]
            pos += 1
            if label == 0xF9:
                size = data[pos]
                packed = data[pos + 1]
                delay = struct.unpack("<H", data[pos + 2:pos + 4])[0]
                tindex = data[pos + 4]
                gce = {
                    "delay_cs": delay,
                    "transparent": tindex if packed & 0x01 else None,
                    "disposal": (packed >> 2) & 0x07,
                }
                pos += size + 1
                pos += 1  # block terminator
            elif label == 0xFF:
                size = data[pos]
                ident = data[pos + 1:pos + 1 + size]
                pos += 1 + size
                payload, pos = _read_sub_blocks(data, pos)
                if ident.startswith(b"NETSCAPE2.0") and len(payload) >= 3:
                    loop = struct.unpack("<H", payload[1:3])[0]
            else:
                _payload, pos = _read_sub_blocks(data, pos)
            continue
        if block == 0x2C:
            left, top, fw, fh, fflags = struct.unpack("<HHHHB", data[pos:pos + 9])
            pos += 9
            table = global_table
            if fflags & 0x80:
                size = 1 << ((fflags & 0x07) + 1)
                table = [tuple(data[pos + i * 3:pos + i * 3 + 3]) for i in range(size)]
                pos += size * 3
            if table is None:
                raise GifFormatError("frame without a color table")
            interlaced = bool(fflags & 0x40)
            min_code = data[pos]
            pos += 1
            lzw, pos = _read_sub_blocks(data, pos)
            indices = lzw_decode(lzw, min_code, fw * fh)
            rows = list(range(fh))
            if interlaced:
                rows = list(range(0, fh, 8)) + list(range(4, fh, 8)) + list(range(2, fh, 4)) + list(range(1, fh, 2))
            previous = list(canvas) if gce["disposal"] == 3 else None
            for src_row, dst_row in enumerate(rows):
                y = top + dst_row
                if y >= height:
                    continue
                for x_off in range(fw):
                    x = left + x_off
                    if x >= width:
                        continue
                    idx = indices[src_row * fw + x_off]
                    if gce["transparent"] is not None and idx == gce["transparent"]:
                        continue
                    canvas[y * width + x] = table[idx] if idx < len(table) else (0, 0, 0)
            frames.append({
                "delay_cs": gce["delay_cs"],
                "disposal": gce["disposal"],
                "rect": (left, top, fw, fh),
                "rgb": list(canvas),
            })
            if gce["disposal"] == 2:
                for dy in range(fh):
                    for dx in range(fw):
                        x, y = left + dx, top + dy
                        if x < width and y < height:
                            canvas[y * width + x] = None
            elif gce["disposal"] == 3 and previous is not None:
                canvas = previous
            gce = {"delay_cs": 0, "transparent": None, "disposal": 0}
            continue
        raise GifFormatError("unknown block 0x%02X at %d" % (block, pos - 1))
    return {"width": width, "height": height, "loop": loop, "frames": frames, "bg_index": bg_index}


def probe(data):
    """Cheap metadata read: dimensions, frame count, delays. No pixel decode."""
    if data[:6] not in (b"GIF87a", b"GIF89a"):
        raise GifFormatError("not a GIF")
    width, height, flags = struct.unpack("<HHB", data[6:11])
    pos = 13
    if flags & 0x80:
        pos += 3 * (1 << ((flags & 0x07) + 1))
    delays = []
    pending = 0
    while pos < len(data):
        block = data[pos]
        pos += 1
        if block == 0x3B:
            break
        if block == 0x21:
            label = data[pos]
            pos += 1
            if label == 0xF9:
                pending = struct.unpack("<H", data[pos + 2:pos + 4])[0]
            _payload, pos = _read_sub_blocks(data, pos)
            continue
        if block == 0x2C:
            fflags = data[pos + 8]
            pos += 9
            if fflags & 0x80:
                pos += 3 * (1 << ((fflags & 0x07) + 1))
            pos += 1
            _lzw, pos = _read_sub_blocks(data, pos)
            delays.append(pending)
            pending = 0
            continue
        raise GifFormatError("unknown block 0x%02X" % block)
    return {"width": width, "height": height, "frames": len(delays), "delays_cs": delays}
