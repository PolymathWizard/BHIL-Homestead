---
id: "P03"
title: "The Era Lock"
phase: "2"
owner: "era-archivist"
key_variables: ["Inventory Summary", "Intake Preference", "Preset Card"]
---

# P03: The Era Lock

*Decide exactly when and where this site would have lived, and write it down so the builder cannot drift.*

## Prompt metadata

| Field | Detail |
|---|---|
| **Writing type** | Era spec card with justification and references |
| **Research focus** | Match brand, audience, and purpose to one of six dated presets; fix every visual and technical constraint |
| **Rhetorical mode** | Archival, decisive |
| **Purpose** | Prevent the most common failure of retro redesigns: mixing 1996 GeoCities with 2007 MySpace on one page |
| **Target audience** | Component mapper, asset smith, period builder, auditor |
| **Tone** | Exact |
| **Named framework** | HOMESTEAD era presets (`canon/presets.json`) |
| **Key variables** | `[Inventory Summary]`, `[Intake Preference]`, `[Preset Card]` |

## Choosing a preset

| Signal in the brand | Preset | Why |
|---|---|---|
| One person's voice, hobby, creator, small shop | B GeoCities | Personal homepages were the dominant amateur form |
| Company, service, catalog, team, B2B | C FrontPage corporate | Small businesses used the same few dozen themes |
| Community, music, fashion, youth, social | E MySpace profile | Profiles were where brands met fans |
| Media, news, dashboards, dense data | D Web 1.5 portal | Three-column portals carried density (spec only) |
| Research, documentation, academic | A Proto-Web | Unstyled pages on gray (spec only) |
| A knowing tribute for today's small web | F Revival | Neocities culture (spec only) |

## Field rules

- **Year**: inside the preset range, justified in one sentence.
- **Canvas**: B 600 px (1996 to 1998) or 760 px (1999 to 2000); C and D 760 px; E 800 px; A fluid.
- **Palette**: presets A to C keep flat colors on the web-safe cube; record brand colors after snapping.
- **Host context**: a concrete story. For B, a neighborhood that fits the topic (Area51 for sci-fi, Hollywood for film, SiliconValley for computers, Petsburgh for pets).
- **Required widgets and forbidden elements**: copied from the preset unchanged.
- **Time capsule**: false unless the intake asks for a story that spans eras, which must be written out.
- **References**: two or three period pages from the archives for the auditor to compare against.

## Mandatory output structure

1. Era spec JSON valid against `schemas/era-spec.schema.json`.
2. One-sentence justification for preset and year.
3. Reference URLs with one line each on what to compare.
4. Risks: for example a brand color that shifts visibly when snapped.

## The prompt

> *You are a web historian locking the era for a HOMESTEAD redesign. The survey summary is `[Inventory Summary]`, the requester's preference is `[Intake Preference]`, and the starting preset card is `[Preset Card]`.*
>
> *Choose one preset and one year, using the selection table unless the requester's preference is explicit. Fill every era spec field by the field rules. Write the host context as a concrete story. Copy required widgets and forbidden elements unchanged. Set time_capsule to false unless a cross-era story was requested, and if so write the story. Name two or three archive pages for the auditor to compare against. Then list any risk that the era will strain the brand.*

## Quality bar

- Nothing in the spec contradicts the preset card.
- The justification would persuade someone who knows the era.
- The builder could start without asking a single question about style.

## Feeds into

P04, P05, P06, P07, P09.
