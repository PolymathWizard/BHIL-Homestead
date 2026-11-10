---
id: "ADR-004"
title: "Originals-first assets"
status: "accepted"
date: "2026-11-10"
---

# ADR-004: Originals-first assets

## Context

Licensing, not technology, is the weak point of retro work. Archived GeoCities GIFs are findable but of unknown authorship, many were copied clip art or ripped characters, and period fonts were never licensed for web embedding. FrontPage theme files and browser badges belong to their owners.

## Decision

HOMESTEAD generates its own assets. `tools/gifsmith.py` draws every common period glyph (badges, buttons, counters, rules, tiles, construction signs, glitter, blinkies, avatars, program windows, WordArt) from shapes and a hand-entered 5x7 pixel font. `tools/chiptune.py` renders public-domain compositions or original melodies. Fonts are referenced by name, never embedded. The FrontPage kit uses an original theme, Ledger Blue, rather than imitating a specific Microsoft theme.

Two asset policies exist. **originals-only** is the default and is required for client work. **archive-allowed** permits generic archived glyphs for portfolio and commentary work, each logged by source URL, never recognizable characters or logos.

## Consequences

- Kits and examples carry no third-party rights questions.
- Generated assets are deterministic and drift-checked.
- The pixel font limits typographic range; that suits the era.
- Badges are generic, so rubric row 15 often scores 1 instead of 2. That trade is deliberate.

## Alternatives considered

- **Curated archive pack.** Rejected; provenance cannot be established for most files.
- **Pillow or another imaging library.** Rejected; BHIL tooling is stdlib only.

## Open questions

- Should HOMESTEAD ship an original SWF intro played through Ruffle? Settling criteria: a stdlib-only SWF writer, or a client need that HTML and CSS intros cannot meet.
