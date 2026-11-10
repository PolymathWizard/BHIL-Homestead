---
id: "P05"
title: "The Era Copy Deck"
phase: "3"
owner: "component-mapper"
key_variables: ["Mapping Table", "Era Voice Rules", "Source Copy"]
---

# P05: The Era Copy Deck

*Rewrite every word the build needs in the voice of the era, without inventing a single fact.*

## Prompt metadata

| Field | Detail |
|---|---|
| **Writing type** | Slot-by-slot copy deck |
| **Research focus** | Translate modern marketing copy into period voice while preserving facts, prices, names, and calls to action |
| **Rhetorical mode** | Editorial, imitative |
| **Purpose** | Remove the most common modern tell, copy cadence, before the builder starts |
| **Target audience** | Period builder, auditor |
| **Tone** | Whatever the era spec says, exactly |
| **Named framework** | HOMESTEAD voice rules (`canon/presets.json`, field `voice` and `voice_examples`) |
| **Key variables** | `[Mapping Table]`, `[Era Voice Rules]`, `[Source Copy]` |

## Voice reference by preset

| Preset | Voice | Sounds like |
|---|---|---|
| A Proto-Web | Dry, first person, pages describe themselves | This page is maintained by. Last modified. |
| B GeoCities | Exuberant, personal, capitals and exclamation points | Welcome to my HOMEPAGE!!! Sign my guestbook! |
| C FrontPage | Small-business brochure | Welcome to our Web site! Click here. All rights reserved. |
| D Portal | Corporate-cheerful, e-everything | Your e-business solution. Personalize this page. |
| E MySpace | Lowercase, decorated, confessional | heyyy!! thanks for the add ~*~ |
| F Revival | Knowing and affectionate | welcome to my little corner of the web |

## Translation rules

- Keep every fact, number, price, and product name accurate. Era framing may change units of delivery (download size, CD-ROM), not claims.
- Replace modern phrases: get started, book a demo, seamless, supercharge, unlock, AI-powered, we use cookies. The lint warns on these.
- Replace emoji with ASCII smileys or GIF graphics.
- Never write real song lyrics, even partial lines.
- Testimonials keep the customer's meaning; their wording may move into the era voice.

## Mandatory output structure

A table with columns: page, slot, source text (short), era rewrite. Then a list of facts that could not be expressed in the era voice without distortion, with the chosen compromise.

## The prompt

> *You are a copywriter working in the era described by `[Era Voice Rules]`. Using the mapping `[Mapping Table]` and the modern copy `[Source Copy]`, write the era rewrite for every slot on every period page.*
>
> *Keep every fact, price, product name, and call to action accurate. Remove every modern marketing phrase and every emoji. Do not invent customers, quotes, awards, or numbers. Never write real song lyrics. Where the era voice would distort a fact, keep the fact and note the compromise.*

## Quality bar

- Reads aloud like the era.
- Passes `grep` for modern phrases.
- A fact-checker comparing source and deck finds no new claims.

## Feeds into

P07 (the builder uses only deck copy), P09 (copy voice row).
