---
title: "FAQ"
description: "Answers to the questions people ask about HOMESTEAD."
---

# FAQ

## About the framework

### What does HOMESTEAD actually produce?

A set of static HTML pages that rebuild a modern site as if it were made in one earlier web era, plus the paper trail: inventory, era spec, mapping, copy deck, asset log, lint report, GIF audit, and a 40-point scorecard. See the [worked example](../examples/nimbus-ledger/README.md).

### Why only three kits when there are six presets?

GeoCities (B), FrontPage corporate (C), and MySpace (E) have the best-documented signatures and cover most requests. A, D, and F are complete specs; scaffold starts them from a blank page until a kit reaches the same quality bar ([ADR-002](../adr/ADR-002-one-era-per-build.md)).

### Can I mix eras?

Only on purpose. Set `time_capsule: true` in the era spec, write the story (for example a 1998 page last updated in 2006), and list the extra widgets. Otherwise the lint fails on era mixing.

### Why does the lint never say pass?

Because it cannot see. It knows the tells (web fonts, rounded corners, emoji) but not whether the page looks right. Its best verdict is NO FINDINGS (INCONCLUSIVE), and the auditor decides ([ADR-007](../adr/ADR-007-no-clean-verdicts.md)).

## Era and design

### Which era should I pick?

Personal or creator brands suit GeoCities, companies suit FrontPage, community and music brands suit MySpace. The full guide is [era lock](../docs/04-era-lock.md).

### Why are the pages so narrow?

Period pages were designed for 640x480 and 800x600 screens and did not reflow. The canvas widths follow resolution data from the time ([C-001](../docs/reference/evidence-register.md#c-001)).

### Why do my brand colors look a little off?

Presets A to C snap flat colors to the 216 web-safe colors, as designers did for 8-bit displays. Check the delta with `python3 tools/websafe.py snap "#RRGGBB"`.

### Why is there no Comic Sans on my machine?

Fonts are referenced by name, never embedded, because the period fonts were never licensed for web embedding. Visitors with the font see it; others see the fallback, exactly as in 1998.

## Safety and rights

### Is it accessible?

Every page ships Safe Mode (stops all motion and sound, raises contrast, starts on for reduced-motion visitors), click-to-play audio, a 340 ms animation floor, alt text, and a text-only version. See [accessibility and safety](../docs/09-accessibility-and-safety.md).

### Can I use GIFs from GifCities?

Only under the archive-allowed policy, only generic glyphs, and only with the source URL logged. Client work is originals-only. See [legal and licensing](../docs/10-legal-and-licensing.md).

### Can I redesign someone else's site?

As clearly labeled portfolio or commentary work, yes: put an unofficial concept line on every page. Not as marketing for anyone else.

### Can I put real browser badges on the page?

Use generic text badges. Browser and platform logos are trademarks.

## Tooling

### Do I need to install anything?

Python 3.10 or newer. The tools use the standard library only. MkDocs is needed only to build the documentation site.

### Can I use JPEG photos?

Convert them to an 8-bit PNG first, then run `tools/dither.py`.

### How do I add a widget, preset, or lint rule?

Edit `canon/`, run `python3 scripts/build_derived.py`, update the expected counts in `scripts/validate.py`, and open a pull request. See [CONTRIBUTING](https://github.com/PolymathWizard/BHIL-Homestead/blob/main/CONTRIBUTING.md).
