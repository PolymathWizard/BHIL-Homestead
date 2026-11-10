---
id: "P09"
title: "The Blind Authenticity Audit"
phase: "6"
owner: "authenticity-auditor"
key_variables: ["Era Spec", "Build Folder", "Lint Report", "Inventory", "Asset Log"]
---

# P09: The Blind Authenticity Audit

*Grade the build the way a visitor from the era and a visitor from today would, without hearing the builder's case.*

## Prompt metadata

| Field | Detail |
|---|---|
| **Writing type** | 40-point scorecard with evidence and QA notes |
| **Research focus** | Era fidelity, content parity, safety, and rights, scored on the HOMESTEAD rubric |
| **Rhetorical mode** | Evaluative, forensic |
| **Purpose** | The final gate. Turns "make it look 90s" into a gradeable result |
| **Target audience** | Orchestrator, human approver |
| **Tone** | Strict, specific |
| **Named framework** | HOMESTEAD rubric (`canon/rubric.json`) |
| **Key variables** | `[Era Spec]`, `[Build Folder]`, `[Lint Report]`, `[Inventory]`, `[Asset Log]` |

## Rubric rows

1 Era locked. 2 Canvas width. 3 Colors. 4 Fonts. 5 Layout engine look. 6 Images. 7 Widgets present. 8 Widgets era-correct. 9 Copy voice. 10 Navigation. 11 Brand legibility. 12 Content parity. 13 View Source. 14 Lived-in details. 15 Browser badges. 16 Motion. 17 Audio. 18 Safe Mode. 19 Accessibility basics. 20 Legal hygiene.

Each row scores 0, 1, or 2; descriptors are in `docs/reference/rubric.md`. Bands: SHIP 34 to 40, REVISE 26 to 33, REBUILD 25 or less. Hard gates: audio (row 17) at least 1, Safe Mode (row 18) at 2, motion (row 16) at least 1. A row with a failing lint rule cannot score 2.

## Blind protocol

- Read only the era spec, the build, the inventory, the asset log, and the lint report.
- Do not read the mapping rationale or decisions log until scores are final.
- Score first, then explain. Never raise a score because a choice was explained.
- Never call the build clean or safe. Report what was checked.

## Mandatory output structure

1. Scorecard JSON valid against `schemas/scorecard.schema.json`.
2. QA notes: tool results, manual checks, reference comparison, verdict, rows to fix with the change that would earn a 2.

## The prompt

> *You are a strict auditor who did not build this site. Audit `[Build Folder]` against `[Era Spec]`. You have the lint report `[Lint Report]`, the inventory `[Inventory]` for content parity, and the asset log `[Asset Log]`.*
>
> *Read every page as source and as a visitor. Score all 20 rubric rows from 0 to 2 with one sentence of evidence each. Cap at 1 any row whose lint rule fails. Apply the hard gates. Return the scorecard JSON and QA notes ending in SHIP, REVISE, or REBUILD, with the specific change that would raise each row below 2.*

## Quality bar

- Every score has evidence a second auditor could verify.
- No row is 2 by default.
- The verdict matches `tools/rubric.py`.

## Feeds into

P10 (fix loop), the human ship decision.
