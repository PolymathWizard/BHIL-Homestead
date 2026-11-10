---
id: "P04"
title: "The Component Translator"
phase: "3"
owner: "component-mapper"
key_variables: ["Inventory JSON", "Era Spec", "Mapping Worksheet"]
---

# P04: The Component Translator

*Translate component by component, not page by page. Every modern pattern gets a decision and a reason.*

## Prompt metadata

| Field | Detail |
|---|---|
| **Writing type** | Decided mapping table, sitemap, widget placement plan |
| **Research focus** | Map each modern pattern to its period equivalent for the locked preset; plan pages and lived-in details |
| **Rhetorical mode** | Analytical, architectural |
| **Purpose** | Guarantee content parity and era correctness before a single page is written |
| **Target audience** | Asset smith, period builder, auditor |
| **Tone** | Decisive, explained |
| **Named framework** | HOMESTEAD mapping table (`canon/mapping.json`, `docs/reference/mapping-table.md`) |
| **Key variables** | `[Inventory JSON]`, `[Era Spec]`, `[Mapping Worksheet]` from `tools/map.py` |

## Decisions

| Decision | Use when | Record |
|---|---|---|
| MAP | The canon equivalent fits | Page it lives on |
| MERGE | Two modern patterns become one period element, or the survey misread a pattern | The row it merges into |
| DROP | The era had no plausible equivalent, or the equivalent would mislead | Reason, and whether a fact or CTA is lost |

Examples from the canon table: hero becomes a WordArt title (B), splash or Flash-style intro (C), or glitter display name (E). Testimonials become guestbook entries (B), a What Our Customers Say page (C), or comments (E). Analytics becomes a visible hit counter (B), an odometer or a [Hit Counter] placeholder (C), or profile views (E). Customer logos become a button wall (B), an Our Clients list (C), or the Top 8 (E).

## Mandatory output structure

1. Decided mapping table: modern pattern, evidence, decision, period equivalent, widgets, page, notes.
2. Period sitemap: five to eight nav items, overflow page, and which rows each page carries.
3. Required widget placement: widget, page, source pattern or lived-in addition.
4. Lived-in details plan.
5. DROP list for the human checkpoint: every drop that loses a fact or CTA.

## The prompt

> *You are mapping a modern site into era preset `[Era Spec]`. Here is the inventory `[Inventory JSON]` and the generated worksheet `[Mapping Worksheet]`.*
>
> *Confirm or change every row to MAP, MERGE, or DROP, with a reason. Treat survey false positives as merges, not inventions: a Product nav link does not make a shop. Add rows for anything the survey missed. Plan a period sitemap of five to eight nav items and place every required widget on a page. Plan the lived-in details from the era spec. Use only widgets the preset allows. List every DROP that loses a fact or call to action so a human can approve it.*

## Quality bar

- No detected pattern is left undecided.
- Every required widget has a page.
- The auditor can score content parity from this table alone.

## Feeds into

P05 (slots to write), P06 (assets per element), P07 (page plan), P09 (parity).
