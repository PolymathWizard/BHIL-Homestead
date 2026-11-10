---
title: "Prompt system: P00 to P10"
description: "The eleven-prompt HOMESTEAD system: a command center plus ten phase specialists."
---

# Prompt system: P00 to P10

Eleven prompts built around the Retro-Web Redesign Architecture (RWRA). P00 runs every phase in one pass. P01 to P10 are specialists for a single phase, used directly in any chat tool or by the matching subagent in `.claude/agents/`.

| Prompt | Name | Phase | Owner | Primary output |
|---|---|---|---|---|
| [P00](P00-command-center.md) | The Retro-Web Command Center | 0 to 6 | orchestrator | Full redesign in one pass |
| [P01](P01-intake.md) | The Intake and Rights Desk | 0 | orchestrator | Intake record, asset policy, disclaimer |
| [P02](P02-site-survey.md) | The Site Survey | 1 | site-surveyor | Inventory and field notes |
| [P03](P03-era-lock.md) | The Era Lock | 2 | era-archivist | Era spec card |
| [P04](P04-component-mapping.md) | The Component Translator | 3 | component-mapper | Decided mapping table and sitemap |
| [P05](P05-era-copy-deck.md) | The Era Copy Deck | 3 | component-mapper | Copy deck |
| [P06](P06-asset-plan.md) | The Asset Smithy | 4 | asset-smith | Recipe, assets, asset log |
| [P07](P07-period-build.md) | The Period Builder | 5 | period-builder | HTML pages |
| [P08](P08-safety-pass.md) | The Safety and Accessibility Pass | 5 | period-builder | Safety checklist and fixes |
| [P09](P09-authenticity-audit.md) | The Blind Authenticity Audit | 6 | authenticity-auditor | Scorecard and QA notes |
| [P10](P10-fix-loop-and-ship.md) | The Fix Loop and Ship Report | 6 | orchestrator | Remediation routing, ship report |

## How the prompts feed each other

```
P01 Intake
  -> P02 Survey ------------------------------------+
  -> P03 Era lock                                   |
  -> P04 Mapping -> P05 Copy deck                   |
  -> P06 Assets                                     |
  -> P07 Build -> P08 Safety pass                   |
  -> P09 Blind audit <---- inventory for parity ----+
  -> P10 Fix loop (back to P04, P06, or P07) and ship report
```

## Deployment options

| Option | Prompts | Best for |
|---|---|---|
| Quick concept | P00 alone | A fast mockup in any chat tool |
| Agent run | `/homestead` in Claude Code | Full engagement with tools, hook, and blind audit |
| Strategy only | P01, P02, P03, P04 | Deciding the era and mapping before a team builds |
| Audit an existing retro build | P09, then P10 | Grading work someone else made |
| Copy only | P05 | Rewriting a site's copy in an era voice |

## Key variables

| Variable | Meaning |
|---|---|
| `[Target URL]` | The modern site, or a saved HTML file |
| `[Era Preset]` | A to F, see [docs/presets](../docs/presets/README.md) |
| `[Year]` | Inside the preset range |
| `[Purpose]` | client, portfolio, commentary, or internal |
| `[Asset Policy]` | originals-only or archive-allowed |
| `[Deliverable]` | static-mock, live-site, screenshots, or video |
