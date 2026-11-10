"""HOMESTEAD core library.

Stdlib-only helpers shared by the tools in tools/. Nothing here talks to the
network or writes outside the paths a caller passes in.

Modules:
    canon    load the canonical JSON sources in canon/
    color    hex parsing, web-safe snapping, CIELAB distance
    gif      GIF89a encoder and decoder (LZW, frames, delays, disposal)
    raster   palette canvas, bevels, and the 5x7 pixel font
    png      minimal PNG decoder for tools/dither.py
    audio    WAV and Standard MIDI File writers for tools/chiptune.py
    htmlscan comment stripping, style extraction, visible text
    schema   minimal JSON Schema subset validator
"""

__version__ = "1.1.0"
