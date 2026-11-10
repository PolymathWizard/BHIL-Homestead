#!/usr/bin/env python3
"""websafe: snap brand colors to the 216-color web-safe cube.

Each channel rounds to the nearest of 00, 33, 66, 99, CC, FF. If that moves
the color more than the delta E switch in canon/homestead.json, the
perceptually nearest web-safe color is used instead. Every result is meant to
be copied into the asset log so the transform is traceable.

Usage:
    python3 tools/websafe.py snap "#1B4FD8" "#6D28D9"
    python3 tools/websafe.py snap --from-inventory engagements/acme/01-inventory/inventory.json --top 8
    python3 tools/websafe.py palette
    python3 tools/websafe.py check "#336699"

Exit codes: 0 ok, 1 check failed, 2 usage error. Stdlib only.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hs_core import canon, color  # noqa: E402


def snap_many(hexes):
    switch = canon.params()["websafe_perceptual_switch_delta_e"]
    return [color.snap(color.parse_hex(h), switch) for h in hexes]


def main(argv=None):
    parser = argparse.ArgumentParser(description="Snap colors to the web-safe palette.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("snap")
    sp.add_argument("colors", nargs="*")
    sp.add_argument("--from-inventory")
    sp.add_argument("--top", type=int, default=8)
    sp.add_argument("--format", choices=["table", "json", "csv"], default="table")
    sub.add_parser("palette")
    cp = sub.add_parser("check")
    cp.add_argument("colors", nargs="+")
    args = parser.parse_args(argv)

    if args.cmd == "palette":
        for rgb in color.websafe_palette():
            print(color.to_hex(rgb))
        return 0

    if args.cmd == "check":
        bad = [h for h in args.colors if not color.is_websafe(color.parse_hex(h))]
        for h in args.colors:
            print("%s %s" % (h.upper(), "web-safe" if h not in bad else "OFF PALETTE"))
        return 1 if bad else 0

    hexes = list(args.colors)
    if args.from_inventory:
        with open(args.from_inventory, "r", encoding="utf-8") as handle:
            inv = json.load(handle)
        hexes += [c["hex"] for c in inv["brand"]["colors"][: args.top]]
    if not hexes:
        parser.error("give colors or --from-inventory")
    results = snap_many(hexes)
    if args.format == "json":
        print(json.dumps(results, indent=2))
    elif args.format == "csv":
        print("original,snapped,method,delta_e,per_channel,perceptual")
        for r in results:
            print("%s,%s,%s,%s,%s,%s" % (r["original"], r["snapped"], r["method"], r["delta_e"], r["per_channel"], r["perceptual"]))
    else:
        print("%-9s  %-9s  %-11s  %7s" % ("ORIGINAL", "SNAPPED", "METHOD", "DELTA E"))
        for r in results:
            note = "  (already web-safe)" if r["already_safe"] else ""
            print("%-9s  %-9s  %-11s  %7.2f%s" % (r["original"], r["snapped"], r["method"], r["delta_e"], note))
    return 0


if __name__ == "__main__":
    sys.exit(main())
