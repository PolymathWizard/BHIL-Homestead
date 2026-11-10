---
title: "Legal and licensing"
description: "A practical risk map for fonts, archived GIFs and MIDI, trademarks and badges, and third-party brands. Not legal advice."
---

# Legal and licensing

This page is a practical risk map, not legal advice. Fair use, parody, and trademark analysis vary by jurisdiction and by use. Get counsel before using a HOMESTEAD build in client marketing that involves anyone else's marks.

## Summary

| Asset | Risk | HOMESTEAD default |
|---|---|---|
| Fonts | Core web fonts were never licensed for web embedding (CORROBORATED, [C-031](reference/evidence-register.md#c-031)); Comic Sans webfont licensing is sold separately (STATED, [C-032](reference/evidence-register.md#c-032)) | Reference system fonts by name only. No `@font-face` for presets A to E. Never self-host Microsoft fonts |
| Archived GIFs | Authorship and rights unknown; many were copied clip art or ripped characters | Generate originals with gifsmith. Archive glyphs only under archive-allowed, generic only, each logged by source URL |
| Archived MIDI and songs | Compositions and recordings may be protected | Public-domain compositions sequenced fresh, or originals. Never real song lyrics |
| Browser and platform badges | Trademarks (browser logos, platform names, product badges) | Generic text badges ("Best viewed at 800 x 600"). Naming a browser in plain text is descriptive |
| Network and platform chrome | Logos and wordmarks are trademarks | Fictional network names in profile builds ("FriendGrid") |
| GENERATOR meta tags and webbot comments | Name a product in source | Descriptive View Source detail; log it; remove for client marketing if counsel prefers |
| Third-party brands | Confusion, implied endorsement | Label as an unofficial concept or tribute; never imply the brand made it |

## Fonts

Period fonts are referenced, never shipped:

```html
<font face="Comic Sans MS,Arial">Welcome!</font>
```

Visitors who have the font installed see it; others get the fallback. That is also how it worked in 1998. If a build truly needs a specific look on every machine, render the text into a GIF with gifsmith instead of embedding a font.

Preset F (modern revival) may use web fonts, but only openly licensed ones, logged in the asset log.

## Archived assets

GifCities makes millions of GeoCities GIFs searchable and links each to its original page (CORROBORATED, [C-027](reference/evidence-register.md#c-027)). That makes them findable, not licensed. Under the archive-allowed policy:

1. Use generic glyphs only: bullets, rules, construction signs, arrows.
2. Never use characters, mascots, logos, or anything recognizable.
3. Log the source URL in the asset log.
4. Prefer replacing the glyph with a generated original before the build ships.

Client work stays originals-only.

## Third-party brands

Redesigning someone else's site as a portfolio piece or commentary is a common genre (CORROBORATED, [C-035](reference/evidence-register.md#c-035)). Keep it clearly labeled:

- A footer line on every page: "Unofficial retro concept. Not affiliated with or endorsed by <brand>."
- No use of the result in advertising for anyone else.
- Keep the brand's name and colors; do not copy its photography or illustration.

For the requester's own brand there is no issue beyond the asset rules above.

## Our own licenses

| What | License |
|---|---|
| Code, schemas, and tools | MIT ([LICENSE](https://github.com/PolymathWizard/BHIL-Homestead/blob/main/LICENSE)) |
| Documentation, prompts, kits, and generated assets | CC BY 4.0 ([LICENSE-CONTENT](https://github.com/PolymathWizard/BHIL-Homestead/blob/main/LICENSE-CONTENT)) |
| Ode to Joy track | Composition public domain; HOMESTEAD sequencing CC BY 4.0 |
| HOMESTEAD riff | Original, CC BY 4.0 |

## Related reading

- [Assets](06-assets.md)
- [ADR-004: originals-first assets](../adr/ADR-004-originals-first-assets.md)
