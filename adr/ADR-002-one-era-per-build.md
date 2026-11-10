---
id: "ADR-002"
title: "One era per build, time capsules by declaration"
status: "accepted"
date: "2026-11-10"
---

# ADR-002: One era per build, time capsules by declaration

## Context

The most visible failure of retro redesigns is era mixing: glitter text on a 1996 starry page, a Top 8 on a FrontPage corporate site, Frutiger Aero gloss on GeoCities. The research pass that seeded HOMESTEAD found that the old web is better treated as at least five dated presets than as one look.

## Decision

Every build locks exactly one preset from `canon/presets.json`. Each preset lists the widgets it allows in `canon/widgets.json`. Builds mark widgets with `<!-- hs:widget ID -->`, and the lint fails (HL022) on any marker the preset does not allow.

A build may span eras only when the era spec sets `time_capsule: true`, writes the story in `time_capsule_story`, and lists the extra widgets in `allowed_extra_widgets`. The auditor scores rubric row 1 against that story.

## Consequences

- Era mixing becomes a lint error rather than a matter of taste.
- Builders must mark widgets, which also powers the required-widget check (HL021).
- Some legitimate hybrids need paperwork. That is intended.

## Alternatives considered

- **A single retro style with optional flourishes.** Rejected; produces exactly the mixed pastiche HOMESTEAD exists to avoid.
- **Detect eras from markup heuristics.** Rejected for v1; markers are explicit and cheap.

## Open questions

- Should mapping columns exist for presets A, D, and F? Settling criteria: a kit for that preset reaches the same lint and rubric bar as the B, C, and E kits.
