#!/usr/bin/env python3
"""chiptune: render a click-to-play track as WAV plus a period .mid file.

Browsers no longer play MIDI, so the safety layer plays the WAV after a click
while the .mid sits in View Source inside a commented bgsound line. Tunes are
public-domain compositions sequenced fresh or HOMESTEAD originals.

Usage:
    python3 tools/chiptune.py list
    python3 tools/chiptune.py render ode-to-joy engagements/acme/05-build/audio/theme.wav

Stdlib only.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hs_core import audio, tunes  # noqa: E402


def main(argv=None):
    parser = argparse.ArgumentParser(description="Render chiptune tracks.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    rp = sub.add_parser("render")
    rp.add_argument("tune", choices=sorted(tunes.TUNES))
    rp.add_argument("outfile", help="path ending in .wav; a .mid is written alongside")
    args = parser.parse_args(argv)
    if args.cmd == "list":
        for name, tune in sorted(tunes.TUNES.items()):
            secs = audio.duration_seconds(tune["notes"], tune["bpm"])
            print("%-16s %5.1fs  %s" % (name, secs, tune["credit"]))
        return 0
    tune = tunes.TUNES[args.tune]
    os.makedirs(os.path.dirname(args.outfile) or ".", exist_ok=True)
    with open(args.outfile, "wb") as handle:
        handle.write(audio.render_wav(tune["notes"], bpm=tune["bpm"]))
    mid = os.path.splitext(args.outfile)[0] + ".mid"
    with open(mid, "wb") as handle:
        handle.write(audio.render_midi(tune["notes"], bpm=tune["bpm"]))
    print(args.outfile)
    print(mid)
    return 0


if __name__ == "__main__":
    sys.exit(main())
