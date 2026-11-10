---
id: "P01"
title: "The Intake and Rights Desk"
phase: "0"
owner: "orchestrator"
key_variables: ["Target URL", "Requester", "Purpose", "Deliverable", "Brand Owner"]
---

# P01: The Intake and Rights Desk

*Settle what is being redesigned, for whom, and under what rights before anyone looks at pixels.*

## Prompt metadata

| Field | Detail |
|---|---|
| **Writing type** | Engagement brief and rights assessment |
| **Research focus** | Establish purpose, audience, deliverable, brand ownership, and asset policy so later phases know what the build may contain |
| **Rhetorical mode** | Diagnostic, procedural |
| **Purpose** | Prevent the two expensive failures: building the wrong thing, and building something the requester cannot publish |
| **Target audience** | The orchestrator and the human requester |
| **Tone** | Plain and specific |
| **Named framework** | HOMESTEAD Intake (template: `templates/intake.md`) |
| **Key variables** | `[Target URL]`, `[Requester]`, `[Purpose]`, `[Deliverable]`, `[Brand Owner]` |

## Decision logic

| If the brand belongs to | And the purpose is | Then |
|---|---|---|
| The requester | Client or internal | Originals-only by default; no disclaimer needed; product badges need counsel only if marketing will use them |
| The requester | Portfolio | Originals-only; disclaimer optional |
| A third party | Portfolio or commentary | Label as an unofficial concept or tribute on every page; originals-only unless archive-allowed is chosen and logged |
| A third party | Client marketing for someone else | Stop. Ask who owns the brand and whether they approved |

Asset policy defaults: originals-only for client work; archive-allowed only for portfolio and commentary, generic glyphs only, every file logged with its source URL.

## Mandatory output structure

1. Target and scope: URL or saved file, pages in scope.
2. Purpose, audience, deliverable, due date, where it will be shown.
3. Era preference: requested preset and year, or "recommend", and any time capsule story.
4. Rights: brand owner, marks expected on the page, disclaimer decision, counsel flag.
5. Asset policy with its reason.
6. Safety commitments checklist (Safe Mode, no autoplay, frame budget, text-only page).
7. Open questions, or "none".

## The prompt

> *You are the intake desk for a HOMESTEAD retro redesign. The requester is `[Requester]`, the target is `[Target URL]`, the stated purpose is `[Purpose]`, the deliverable is `[Deliverable]`, and the brand owner is `[Brand Owner]`.*
>
> *Fill the HOMESTEAD intake record. Decide the asset policy using the decision table, and say why in one sentence. If the brand belongs to someone other than the requester, decide the disclaimer wording. List every open question that would change what the build may contain, and nothing else. Do not choose an era yet unless the requester named one; if they did, record it as a preference for the era archivist, not a decision.*

## Quality bar

- Every field is filled or explicitly marked unknown with an owner to resolve it.
- The asset policy and disclaimer follow the decision table.
- Open questions are about rights, purpose, or scope, never about taste.

## Feeds into

P02 (survey scope), P03 (era preference), P06 (asset policy), P10 (disclaimer check at ship).
