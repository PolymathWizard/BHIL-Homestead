---
id: "ADR-009"
title: "A generated figure kit in the BHIL frame"
status: "accepted"
date: "2026-11-10"
---

# ADR-009: A generated figure kit in the BHIL frame

## Context

Version 1.0.0 shipped seven small SVG diagrams drawn in an older set of cobalt tokens. They explained the method but did not look like BHIL work, did not look like the web HOMESTEAD rebuilds, and drew their own pixel type separately from the toolchain. The README had no visual spine, and BHIL Brand Guidelines v1.0 had since replaced the cobalt palette with Terminal Navy and BH Blue, Newsreader headlines, and IBM Plex.

## Decision

HOMESTEAD carries ten figures, HS-01 to HS-10, one per major idea in the method. Each is a 1600 x 900 SVG that puts period specimens inside the BHIL instrument frame: brand strip, mono eyebrow with the prompt chevron, Newsreader headline and italic dek, hairline rules, footer with figure ID and BARRYHURD.COM. The retro feel comes only from the specimens: the toolchain's own 5x7 pixel font, Win9x bevel chrome recolored in brand blues, 88x31 badges, odometers, marquees, and real `gifsmith` output.

1. **Canon first.** `canon/brand.json` holds the palette, type stacks, strip text, rules, and every figure's title, alt text, motion note, and placements. `scripts/figures.py` draws the figures from canon and from the worked example's data, and `scripts/build_derived.py` writes them, so the drift gate covers them.
2. **One motif per surface.** The dot constellation appears only on the masthead; the ASCII pipeline only on HS-03. No gradients on motifs, no drop shadows, square corners, and no recreation of the BHIL terminal-badge logo.
3. **Motion is optional.** Animations are CSS only, slow, and small in area. Frame zero is the designed static frame, and a `prefers-reduced-motion` rule stops every animation and hides animated GIF specimens behind their still frames.
4. **PNGs are renderer output.** `scripts/render_figures.py` renders frame zero with the brand fonts through a headless browser. The PNGs sit in `assets/figures/png/` with a `SOURCES.sha256` of the SVGs they came from; the drift gate skips that folder and the validator fails when a PNG is older than its SVG.
5. **Placements are checked.** The validator fails when a page listed in a figure's placements does not embed that figure.

## Consequences

- The README, docs, generated reference pages, kit and example pages share one visual system.
- Changing a canon count or the worked example's score changes the figures in the same commit.
- SVGs viewed through an `<img>` tag cannot load web fonts, so they fall back to Georgia, Arial, and Courier New. Layout tolerates the fallback; the PNGs carry the exact brand type.
- PNG refresh needs Playwright and Chrome, which breaks the stdlib-only rule for that one optional script. The gates themselves stay stdlib only.

## Alternatives considered

- **Hand-drawn figures in a design tool.** Rejected; they would drift from canon on the first count change.
- **Embedding subset fonts in every SVG.** Rejected; it adds weight to every figure for a difference the PNGs already cover.
- **Period colors throughout.** Rejected; the figures are BHIL publications about period work, so the frame stays on brand and only the specimens wear period color.

## Open questions

- Should the kit ship a LinkedIn carousel cut (1080 x 1350) of the ten figures? Settling criteria: a launch post that needs it.
