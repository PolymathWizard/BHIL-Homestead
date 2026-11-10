---
id: "P02"
title: "The Site Survey"
phase: "1"
owner: "site-surveyor"
key_variables: ["Target URL", "Page Budget", "Inventory JSON"]
---

# P02: The Site Survey

*Take a complete, evidence-backed inventory of a modern site before deciding anything about its past.*

## Prompt metadata

| Field | Detail |
|---|---|
| **Writing type** | Structured inventory plus field notes |
| **Research focus** | Map information architecture, components, brand tokens, and voice; detect the modern patterns that need period translations |
| **Rhetorical mode** | Forensic, inventorial |
| **Purpose** | Give mapping and build phases a complete list of what must survive the redesign |
| **Target audience** | Component mapper, asset smith, auditor (for parity) |
| **Tone** | Clinical |
| **Named framework** | HOMESTEAD Inventory (schema: `schemas/inventory.schema.json`) |
| **Key variables** | `[Target URL]`, `[Page Budget]`, `[Inventory JSON]` from `tools/survey.py` |

## Inventory fields and how each transforms later

| Field | Capture | Later transform |
|---|---|---|
| Information architecture | Top navigation, depth, page count | Cap at five to eight period nav items |
| Navigation | Sticky header, hamburger, mega-menu, footer links | Text links, shared borders, image map, or network bar |
| Content types | Hero, features, pricing, blog, docs, testimonials, FAQ, careers, legal | Mapping table rows |
| Brand colors | Hex of primary, secondary, accent, background | Web-safe snap with a logged delta |
| Logo | Wordmark, symbol, or both | WordArt or beveled GIF |
| Typography | Web fonts in use | System font stacks per preset |
| Imagery | Photos, illustrations, 3D, icons | Dithered GIF, posterized art, original pixel glyphs |
| CTAs | Button text and targets | Click Here!, Enter, Download Now!, Order Form |
| Voice | Formality, jargon, emoji | Era voice rules |
| Interactive features | Search, login, chat, dashboard, video, forms | Mapping table rows |
| Trust and legal | Cookie banner, privacy, compliance badges | Browser notices, text-only link |

## Mandatory output structure

1. `inventory.json` from the tool, unedited.
2. Notes: IA in order; patterns the tool missed or misread, each with evidence and its canon mapping id; brand summary; three short voice quotes and the modern tells; must-keep facts and CTAs; open questions.

## The prompt

> *You are surveying `[Target URL]` for a HOMESTEAD retro redesign, with a budget of `[Page Budget]` pages. Here is the tool output: `[Inventory JSON]`.*
>
> *Check the inventory against the live site. List every pattern the tool missed or misread, with evidence and the canon mapping id it belongs to. Summarize the brand in four lines: name, logo form, the two or three colors that carry it, and type personality. Quote three short phrases that capture the voice and list the modern tells. List every fact, price, product name, and call to action that the period build must not lose. Record; do not redesign.*

## Quality bar

- Every pattern in the inventory is either confirmed or corrected.
- Must-keep list is specific enough that the auditor can check parity from it.
- No third-party assets copied; URLs only.

## Feeds into

P03 (brand and audience signal for era choice), P04 (pattern list), P05 (voice and must-keep copy), P06 (colors, logo, imagery), P09 (parity check).
