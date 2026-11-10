---
id: "P00"
title: "The Retro-Web Command Center"
phase: "0 to 6"
owner: "orchestrator"
key_variables: ["Target URL", "Era Preset", "Year", "Purpose", "Asset Policy", "Deliverable"]
---

# P00: The Retro-Web Command Center

*End-to-end orchestrator: analyze a modern website and rebuild it as a convincing site from one locked web era, in a single pass.*

## Prompt metadata

| Field | Detail |
|---|---|
| **Writing type** | Multi-phase redesign specification plus period build |
| **Research focus** | Deconstruct a modern site, lock one era, translate every component, and assemble a period site that survives View Source and a 40-point authenticity audit |
| **Rhetorical mode** | Analytical, archival, editorial, constructive |
| **Purpose** | Prompt zero for HOMESTEAD. Sequences all seven phases of the Retro-Web Redesign Architecture (RWRA) when no agent team or tooling is available, or as the brief the orchestrator follows |
| **Target audience** | Designers, marketers, brand teams, agencies, and anyone producing retro tributes, portfolio pieces, launch stunts, or commentary |
| **Tone** | Precise, playful in the output, strict in the process |
| **Named framework** | Retro-Web Redesign Architecture (RWRA) |
| **Key variables** | `[Target URL]`, `[Era Preset]`, `[Year]`, `[Purpose]`, `[Asset Policy]`, `[Deliverable]` |

## Seven-phase cognitive architecture

Complete every phase in order before writing any page.

**Phase 0, Intake.** Record target, purpose (client, portfolio, commentary, internal), deliverable, and asset policy. If the brand is not the requester's own, plan an unofficial-tribute disclaimer.

**Phase 1, Survey.** Inventory navigation, information architecture, headings, CTAs, forms, embeds, scripts, brand colors, fonts, imagery, and voice. Detect modern patterns (hero, sticky header, cards, pricing, testimonials, blog, social icons, analytics, cookie banner, newsletter, search, login, chat, video, docs, FAQ, dark mode, careers, logo strip, footer).

**Phase 2, Era lock.** Choose exactly one preset: A Proto-Web (1993 to 1996), B GeoCities (1995 to 2000), C FrontPage corporate (1997 to 2003), D Web 1.5 portal (1999 to 2004), E MySpace profile (2004 to 2009), F modern revival. Fix year, browser, canvas width, palette mode, fonts, layout mode, required widgets, forbidden elements, voice, motion budget, and audio mode.

**Phase 3, Mapping.** Give every detected pattern a MAP, MERGE, or DROP decision using the HOMESTEAD mapping table. Cap navigation at five to eight items. Rewrite all copy in the era voice.

**Phase 4, Assets.** Snap flat colors to the 216 web-safe colors (00, 33, 66, 99, CC, FF per channel) for presets A to C. Rebuild the logo as WordArt or a beveled GIF. Downscale and dither photos. Generate original buttons, badges, counters, rules, and tiles. Log every asset.

**Phase 5, Build.** Write period markup: table layouts at the canvas width, font tags, spacer GIFs, period comments. Link the safety layer, give every animated GIF a still frame, make audio click-to-play, and link a text-only version.

**Phase 6, QA.** Lint for anachronisms, audit animation timing and flash, then score the 40-point rubric with evidence. SHIP at 34 or more with no hard gate failures.

## Mandatory output structure

1. **Intake record**: target, purpose, deliverable, asset policy, rights notes.
2. **Inventory**: IA list, pattern table with evidence, brand colors, fonts, voice notes, must-keep facts.
3. **Era spec card**: every field in `schemas/era-spec.schema.json`, plus a one-sentence justification for the year.
4. **Mapping table**: modern pattern, decision, period equivalent, widgets, page.
5. **Copy deck**: every slot rewritten in the era voice.
6. **Asset log**: file, kind, source, license, era check.
7. **The build**: complete HTML for every page, the text-only page, and asset recipes.
8. **Scorecard**: 20 rows scored 0 to 2 with evidence, total, verdict, and rows to fix.

## The prompt

> *You are a web designer working in `[Year]`, building with that year's tools, and a strict web historian checking your own work afterward. Redesign `[Target URL]` as if it had been built in era preset `[Era Preset]`. The purpose is `[Purpose]`, the deliverable is `[Deliverable]`, and the asset policy is `[Asset Policy]`.*
>
> *Run the Retro-Web Redesign Architecture in order. Inventory the modern site. Lock one era and write the era spec card. Map every modern component to its period equivalent with a MAP, MERGE, or DROP decision, cap navigation at five to eight items, and rewrite all copy in the era voice. Plan and log every asset; for presets A to C snap flat colors to the web-safe palette. Build every page in period markup at the era canvas width, with the HOMESTEAD safety layer linked, still frames for every animation, click-to-play audio only, alt text throughout, and a text-only version linked from every page.*
>
> *Never use web fonts, rounded corners, gradients, flexbox, grid, emoji, SVG, responsive breakpoints, or modern marketing phrases in presets A to E. Never mix eras unless the spec declares a time capsule. Never use real song lyrics, third-party logos, or recognizable characters. Then score the build on the 40-point HOMESTEAD rubric, strictly, with one sentence of evidence per row, and fix every row below 2 before you call it finished.*

## Quality bar

- A first-time visitor in the era year would not spot the build as a fake.
- A 2026 visitor can stop all motion and sound with one control and read every page.
- Every fact, price, and CTA from the modern site survives somewhere, or its drop is explained.

## Feeds into

P01 to P10 are the specialist modules for each phase. Use them when one phase needs more depth than this single pass allows.
