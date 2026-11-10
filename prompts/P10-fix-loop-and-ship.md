---
id: "P10"
title: "The Fix Loop and Ship Report"
phase: "6"
owner: "orchestrator"
key_variables: ["Scorecard", "QA Notes", "Engagement README"]
---

# P10: The Fix Loop and Ship Report

*Close the gap between the score and the bar, then hand over a build someone can publish without surprises.*

## Prompt metadata

| Field | Detail |
|---|---|
| **Writing type** | Remediation plan, then a ship report |
| **Research focus** | Route each low rubric row to the phase that owns it, re-audit, and document the result |
| **Rhetorical mode** | Decisive, procedural |
| **Purpose** | Finish the engagement with a scored, explained, publishable build |
| **Target audience** | The human requester |
| **Tone** | Short and factual |
| **Named framework** | HOMESTEAD fix loop |
| **Key variables** | `[Scorecard]`, `[QA Notes]`, `[Engagement README]` |

## Routing rows to owners

| Rows | Owner | Typical fix |
|---|---|---|
| 1, 2, 8 | era-archivist then period-builder | Re-lock the era or remove the mixed widget; fix canvas width |
| 9, 11, 12 | component-mapper | Rewrite copy, restore a dropped fact or CTA, strengthen brand cues |
| 3, 6, 15, 20 | asset-smith | Snap colors, dither images, replace badges, complete the asset log |
| 4, 5, 7, 10, 13, 14 | period-builder | Markup, widgets, navigation, View Source details |
| 16 to 19 | period-builder with P08 | Motion, audio, Safe Mode, accessibility |

Loop at most twice. If a build is still below SHIP, report the remaining rows and let the human decide.

## Ship report structure

1. What was built: preset, year, pages, and where to open it.
2. Score and verdict, with every row below 2 and why it stayed there.
3. Decisions the human approved (drops, merges, time capsule, asset policy).
4. Rights notes: disclaimer text, any descriptive use of marks, asset policy.
5. How to host it: static files, any host; serve over HTTPS; keep the safety layer files next to the pages.

## The prompt

> *You are closing a HOMESTEAD engagement. Here is the scorecard `[Scorecard]`, the auditor's notes `[QA Notes]`, and the engagement record `[Engagement README]`.*
>
> *If the verdict is REVISE, route each row below 2 to its owner with the specific change from the auditor's notes, then request a fresh audit. Stop after two loops. If the verdict is REBUILD, return to era lock with the auditor's reasons. If the verdict is SHIP, write the ship report in the structure above, in plain language, with no claim the scorecard does not support.*

## Quality bar

- The ship report says exactly what the scorecard says.
- Every approval the human gave is on record.
- Someone who was not in the room could publish the build safely from the report.
