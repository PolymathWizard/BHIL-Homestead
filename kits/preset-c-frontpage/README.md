---
title: "Kit: preset C, FrontPage corporate"
preset: "C"
years: "1997-2003"
---

# Kit: preset C, FrontPage corporate

A working starter for the small-business and corporate sites that FrontPage and Dreamweaver users shipped between 1997 and 2003. The look comes from an original theme, Ledger Blue, drawn from scratch by `tools/gifsmith.py`. HOMESTEAD does not ship or imitate any specific Microsoft theme files (ADR-004).

| File | Purpose |
|---|---|
| [index.html](index.html) | Shared borders (top, left, bottom), theme banner, hover-swap nav buttons, search form, products table, press releases, feedback form, corporate footer |
| [text-only.html](text-only.html) | Text-only and printer-friendly version |
| [recipe.json](recipe.json) | Logo, banners, and nav buttons with hover states |
| `homestead-safe.css`, `homestead-safe.js` | Safety layer copies, drift-checked |

## What makes it read as FrontPage

- Top, left, and bottom shared borders, marked in source with `webbot bot="Include"` comments pointing at `_borders/`.
- A `GENERATOR` meta tag and theme meta tags. These are View Source details; drop the generator tag for client marketing if counsel prefers (see docs/10-legal-and-licensing.md).
- Beveled nav buttons with hover states rebuilt as JavaScript image swaps, with matching focus and blur handlers so keyboard users see the same state.
- A `[Hit Counter]` placeholder in the footer, which is what visitors saw when a host lacked server extensions. It satisfies the hit counter requirement as a lived-in detail.
- Brochure copy: Welcome to our Web site!, Click here, Copyright with All rights reserved.

## How to use it

1. Scaffold with `python3 tools/scaffold.py new <slug> --target <url> --preset C`.
2. Regenerate the logo, banners, and buttons with the brand name and nav labels from `03-mapping.md`. Keep five to eight buttons.
3. Replace every `[bracketed]` value with copy from `03-copy-deck.md`.
4. Run `python3 tools/era_lint.py 05-build --preset C` after every edit.
