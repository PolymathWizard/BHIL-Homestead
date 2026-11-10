---
title: "Kit: preset E, MySpace profile"
preset: "E"
years: "2004-2009"
---

# Kit: preset E, MySpace profile

A working starter for the profile era. The point of this preset is layering: a plain default profile template underneath, a gaudy user layout pasted into About Me on top. Profiles allowed HTML but not JavaScript in their fields (claim C-020), so the layout is a style block with `!important` overrides, which is exactly what this kit ships.

| File | Purpose |
|---|---|
| [index.html](index.html) | Network bar, glitter name, photo, contact table, profile song, interests, details, blinkies, blurbs with the user layout block, Top 8, comments, profile views |
| [text-only.html](text-only.html) | Plain version of the profile |
| [recipe.json](recipe.json) | Glitter name, profile photo, sparkle background, avatars, blinkies, song |
| `homestead-safe.css`, `homestead-safe.js` | Safety layer copies, drift-checked |

## Rules this kit enforces

- No network logos or wordmarks. The top bar says `[Network]`; put a fictional network name there.
- No real song lyrics anywhere, including the tagline and comments. The profile song is an original HOMESTEAD melody rendered by `tools/chiptune.py`.
- No sensitive demographic fields in Details. The kit uses status, here for, hometown, zodiac sign, and occupation.
- Glitter, not stars (claim C-024). The sparkle background is a pink tile, and glitter is generated with `gifsmith.py` kind `glitter`.
- Motion budget is six: glitter name, Online Now, two blinkies, and up to two comment graphics.

## How to use it

1. Scaffold with `python3 tools/scaffold.py new <slug> --target <url> --preset E`.
2. Regenerate the glitter name: `python3 tools/gifsmith.py one glitter 05-build/images/glitter-name.gif --params '{"text": "BRAND NAME", "scale": 3}'`.
3. Map customer logos to the Top 8, testimonials to comments, social links to the contact table.
4. Run `python3 tools/era_lint.py 05-build --preset E` after every edit.
