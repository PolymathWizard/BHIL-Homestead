---
title: "Phase 1: Site survey"
description: "How to inventory a modern site, what the survey tool detects, and what it misses."
---

# Phase 1: Site survey

The survey records what the modern site contains so nothing important is lost in translation. It does not judge or redesign.

## Run it

```bash
python3 tools/survey.py https://example.com --pages 6 --out engagements/acme/01-inventory/inventory.json
python3 tools/survey.py saved-page.html --out engagements/acme/01-inventory/inventory.json
```

URL mode fetches same-origin pages linked from the navigation (up to ten) and up to six same-origin stylesheets. It sends a plain User-Agent and never submits forms. If a site blocks automated requests, save the page from a browser (HTML only) and survey the file.

## What it extracts

| Field | Source |
|---|---|
| Title, language, meta description | `title`, `html lang`, `meta` |
| Headings | `h1` to `h3` in order |
| Navigation and footer links | links inside `nav`, `header`, and `footer` |
| Calls to action | buttons, links whose class contains btn, button, or cta, and submit inputs |
| Forms | inputs, with a purpose guess: login, search, newsletter, or contact |
| Images and embeds | `img`, `iframe`, `video`, `source` |
| Scripts | external sources plus inline script text for detection |
| Brand colors | hex and rgb values from style blocks, style attributes, and stylesheets, ranked with neutrals last |
| Fonts | `font-family` declarations and Google Fonts families, classified as serif, sans, display, playful, or mono |
| Tone notes | sentence length, second-person share, exclamation marks, modern marketing phrases, emoji |
| Patterns | every row of `canon/mapping.json` whose detection signals match |

The output validates against `schemas/inventory.schema.json`.

## How detection works

Each mapping row in canon carries case-insensitive signals in five channels: raw HTML, visible text, link targets, scripts, and CSS. A pattern counts as detected when any signal matches on any surveyed page, and the inventory records which signals fired as evidence. The full list is in the [mapping table](reference/mapping-table.md#detection-signals).

Because signals are canon, improving detection is a canon change: edit `canon/mapping.json`, rebuild, and the drift gate re-surveys the worked example to prove nothing regressed.

## What it misses

Treat the tool as a first pass. The surveyor checks it by reading the live page.

| Common miss | Why | What to do |
|---|---|---|
| JavaScript-rendered navigation | The tool reads served HTML only | Read the rendered page and add the nav to notes |
| Pricing inside a script or image | No visible text to match | Add a pricing row in notes |
| Sections built from images | No text signals | Describe them in notes |
| False positives | A Product nav link triggers product pages | Mark as MERGE at mapping |
| Brand color buried in a gradient | Ranked low or missed | Name the carrying colors in notes |

## Field notes

The surveyor writes `01-inventory/notes.md` with the IA in order, corrections to the inventory, a four-line brand summary, three short voice quotes, the modern tells, the must-keep list (facts, prices, product names, CTAs), and open questions. The must-keep list is what the auditor uses to score content parity.

## Color snapping, early

Snap the brand colors during the survey so the era archivist can see how the brand will survive a web-safe preset:

```bash
python3 tools/websafe.py snap --from-inventory engagements/acme/01-inventory/inventory.json
```

| Original | Snapped | Method |
|---|---|---|
| `#1B4FD8` (BHIL cobalt) | `#3366CC` | per-channel |
| `#6D28D9` (Nimbus violet) | `#6633CC` | per-channel |

## Related reading

- [Mapping table and detection signals](reference/mapping-table.md)
- [Era lock](04-era-lock.md)
- [Worked example inventory](../examples/nimbus-ledger/inventory.json)
