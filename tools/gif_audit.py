#!/usr/bin/env python3
"""gif_audit: timing and flash audit for animated GIFs (Phase 6).

For every GIF under the given paths:
  1. Reads frame delays. Delays under 20 ms are treated as 100 ms, matching
     common browser clamping (INFERENCE, verify per browser).
  2. Fails any animation whose shortest effective delay is under the house
     budget in canon/homestead.json (340 ms by default, claim C-043).
  3. Decodes and composites frames, then counts pixels whose relative
     luminance changes enough to form half of a WCAG general flash
     (difference of 0.1 or more with the darker side under 0.8), plus
     saturated-red transitions. A transition is flash-capable when that area
     reaches 25 percent of a 341 x 256 field (claim C-021).
  4. Fails any file with more than three flash-capable flashes in any one
     second.

The audit measures the GIF at native size. Scaled, tiled, or repeated use on
a page can create a flash the file alone does not, so the best verdict is
WITHIN BUDGET (INCONCLUSIVE FOR SCALED OR TILED USE). Nothing is ever called
safe or clean (ADR-007).

Usage:
    python3 tools/gif_audit.py BUILD_DIR
    python3 tools/gif_audit.py a.gif b.gif --format json --page-bg "#000000"

Exit codes: 0 no failures, 1 at least one failure, 2 usage. Stdlib only.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hs_core import canon, color, gif  # noqa: E402


def effective_ms(delay_cs, params):
    ms = delay_cs * 10
    if ms < params["gif_tiny_delay_threshold_ms"]:
        return params["gif_tiny_delay_clamp_ms"]
    return ms


def _is_red(rgb):
    total = sum(rgb)
    return total > 0 and rgb[0] / float(total) >= 0.8


def transition_area(frame_a, frame_b, page_bg):
    general = 0
    red = 0
    lum_cache = {}

    def lum(rgb):
        if rgb not in lum_cache:
            lum_cache[rgb] = color.relative_luminance(rgb)
        return lum_cache[rgb]

    for pa, pb in zip(frame_a, frame_b):
        a = pa if pa is not None else page_bg
        b = pb if pb is not None else page_bg
        if a == b:
            continue
        la, lb = lum(a), lum(b)
        if abs(la - lb) >= 0.1 and min(la, lb) < 0.8:
            general += 1
        if (_is_red(a) or _is_red(b)) and abs(la - lb) >= 0.05:
            red += 1
    return general, red


def audit_file(path, params, page_bg):
    with open(path, "rb") as handle:
        data = handle.read()
    info = gif.probe(data)
    result = {"file": path, "width": info["width"], "height": info["height"], "frames": info["frames"]}
    if info["frames"] <= 1:
        result.update(verdict="STATIC", fail=False, min_delay_ms=None, flashes_per_second=0.0, notes=[])
        return result
    delays = [effective_ms(d, params) for d in info["delays_cs"]]
    budget = params["gif_min_frame_delay_ms"]
    field_w, field_h = params["large_animation_area_px"]
    threshold_area = int(field_w * field_h * 0.25)
    decoded = gif.decode(data)
    frames = [f["rgb"] for f in decoded["frames"]]
    capable = []
    max_general = max_red = 0
    for i in range(len(frames)):
        j = (i + 1) % len(frames)
        general, red = transition_area(frames[i], frames[j], page_bg)
        max_general = max(max_general, general)
        max_red = max(max_red, red)
        capable.append(general >= threshold_area or red >= threshold_area)
    times = []
    t = 0
    cycle_ms = max(1, sum(delays))
    cycles = max(2, min(2000, 2000 // cycle_ms + 2))  # simulate at least two seconds of looping
    for _cycle in range(cycles):
        for i, d in enumerate(delays):
            t += d
            times.append((t, capable[i]))
    flash_times = [tt for tt, cap in times if cap]
    worst = 0
    for start in flash_times:
        in_window = sum(1 for tt in flash_times if start <= tt < start + 1000)
        worst = max(worst, in_window)
    flashes_per_second = worst / 2.0
    notes = []
    fail = False
    verdict = "WITHIN BUDGET (INCONCLUSIVE FOR SCALED OR TILED USE)"
    if min(delays) < budget:
        verdict = "OVER TIMING BUDGET"
        fail = True
        notes.append("shortest effective delay %d ms is under the %d ms house budget" % (min(delays), budget))
    if flashes_per_second > 3:
        verdict = "FLASH RISK"
        fail = True
        notes.append("%.1f flash-capable flashes per second" % flashes_per_second)
    if info["width"] * info["height"] >= field_w * field_h:
        notes.append("animation covers a full 341 x 256 field at native size; review with a PEAT-class tool")
    if max_general and max_general < threshold_area:
        notes.append("largest luminance transition %d px, below the %d px area threshold" % (max_general, threshold_area))
    result.update(verdict=verdict, fail=fail, min_delay_ms=min(delays), flashes_per_second=flashes_per_second,
                  max_transition_px=max_general, max_red_transition_px=max_red, notes=notes)
    return result


def collect(paths):
    out = []
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, names in os.walk(p):
                dirs.sort()
                out += [os.path.join(root, n) for n in sorted(names) if n.lower().endswith(".gif")]
        elif p.lower().endswith(".gif"):
            out.append(p)
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description="HOMESTEAD GIF timing and flash audit.")
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--page-bg", default="#FFFFFF", help="color assumed behind transparent pixels")
    parser.add_argument("--format", choices=["table", "json"], default="table")
    args = parser.parse_args(argv)
    params = canon.params()
    files = collect(args.paths)
    if not files:
        print("gif_audit: no GIF files found", file=sys.stderr)
        return 2
    page_bg = color.parse_hex(args.page_bg)
    results = [audit_file(f, params, page_bg) for f in files]
    failures = [r for r in results if r["fail"]]
    if args.format == "json":
        print(json.dumps({"files": results, "failures": len(failures)}, indent=2))
    else:
        for r in results:
            if r["verdict"] == "STATIC":
                continue
            print("%-60s %3d frames  min %4s ms  %s" % (os.path.relpath(r["file"]), r["frames"], r["min_delay_ms"], r["verdict"]))
            for note in r["notes"]:
                print("    - " + note)
        static = sum(1 for r in results if r["verdict"] == "STATIC")
        print("audited %d GIFs: %d static, %d animated, %d failing" % (len(results), static, len(results) - static, len(failures)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
