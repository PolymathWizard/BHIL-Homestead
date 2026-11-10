---
id: "P06"
title: "The Asset Smithy"
phase: "4"
owner: "asset-smith"
key_variables: ["Era Spec", "Mapping Table", "Brand Colors", "Asset Policy"]
---

# P06: The Asset Smithy

*Make every image and sound the build needs, prove the build may use them, and keep motion inside safe limits.*

## Prompt metadata

| Field | Detail |
|---|---|
| **Writing type** | Asset plan, generator recipe, asset log |
| **Research focus** | Period-correct color, logo, photo, glyph, and audio treatment under an explicit rights policy |
| **Rhetorical mode** | Technical, procedural |
| **Purpose** | Close the weak point of retro work, licensing, while hitting the era's look |
| **Target audience** | Period builder, auditor, counsel when needed |
| **Tone** | Exact |
| **Named framework** | HOMESTEAD originals-first asset policy (ADR-004) |
| **Key variables** | `[Era Spec]`, `[Mapping Table]`, `[Brand Colors]`, `[Asset Policy]` |

## Transform rules

| Asset | Treatment | Tool |
|---|---|---|
| Brand colors | Round each channel to 00, 33, 66, 99, CC, FF; switch to perceptual nearest if the shift exceeds delta E 10 | `tools/websafe.py snap` |
| Logo | Pixel WordArt with row gradient and drop shadow, or beveled GIF; transparent key on dark pages | `gifsmith.py` kind `wordart` |
| Photos | Downscale to 320 px or less; adaptive palette with error diffusion | `tools/dither.py` |
| Dashboards, apps | Program window screenshot with rows of the product's real data labels | kind `appwindow` |
| Navigation | Beveled buttons with hover states, five to eight | kind `navbutton` |
| Badges | 88 x 31, generic text, no third-party logos | kind `badge` |
| Counters | Odometer digits | kind `digits` |
| Dividers, tiles | Rainbow rule, star tile, ruled-paper tile | kinds `rainbow`, `stars`, `tile` |
| Profile flair | Glitter text, blinkies, avatars, Online Now | kinds `glitter`, `blinkie`, `avatar`, `online` |
| Music | Public-domain composition or original melody, WAV plus MIDI, click to play | `tools/chiptune.py` |

Every animated asset ships a still frame and keeps frames at 340 ms or slower.

## Mandatory output structure

1. Color snap table: original, snapped, method, delta E.
2. Recipe JSON for the build.
3. Asset log rows: file, kind, source, source URL, license, generator or author, era check, notes.
4. GIF audit summary with zero failures.
5. Policy flags: any asset that needed a rights decision.

## The prompt

> *You are producing assets for a HOMESTEAD build in `[Era Spec]` under the `[Asset Policy]` policy. The mapping is `[Mapping Table]` and the brand colors are `[Brand Colors]`.*
>
> *Snap the brand colors and report the deltas. Write a gifsmith recipe that covers every image the mapping needs: logo, banners, buttons, badges, counters, dividers, tiles, screenshots, and any preset-specific flair. Plan photo dithering and audio. Use only original generators unless the policy is archive-allowed, and even then only generic glyphs with logged sources. Never use third-party logos, characters, or real song recordings. Then write the asset log and confirm every animation keeps frames at 340 ms or slower with a still frame for Safe Mode.*

## Quality bar

- Every file in `images/` and `audio/` has a log row.
- No asset needs a conversation with a lawyer, or the one that does is flagged.
- `tools/gif_audit.py` reports no failures.

## Feeds into

P07 (file names and dimensions), P08 (still frames, audio wiring), P09 (legal hygiene row).
