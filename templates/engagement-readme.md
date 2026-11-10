---
title: "Engagement: {{SLUG}}"
engagement: "{{SLUG}}"
preset: "{{PRESET}}"
opened: "{{DATE}}"
---

# Engagement: {{SLUG}}

Target: {{TARGET}}. Preset {{PRESET}} ({{PRESET_NAME}}). Purpose: {{PURPOSE}}. Asset policy: {{ASSET_POLICY}}.

## Phase tracker

| Phase | Output | Owner | Status |
|---|---|---|---|
| 0 Intake | 00-intake.md | orchestrator | open |
| 1 Site survey | 01-inventory/inventory.json, notes.md | site-surveyor | |
| 2 Era lock | 02-era-spec.json | era-archivist | prefilled |
| 3 Component mapping | 03-mapping.md, 03-copy-deck.md | component-mapper | |
| 4 Assets | 04-asset-log.csv, 05-build/images/ | asset-smith | |
| 5 Build | 05-build/ | period-builder | seeded from kit |
| 6 QA | 06-qa/scorecard.json, qa-notes.md | authenticity-auditor | |

## Commands

```bash
python3 tools/survey.py {{TARGET}} --pages 6 --out engagements/{{SLUG}}/01-inventory/inventory.json
python3 tools/map.py engagements/{{SLUG}}/01-inventory/inventory.json --spec engagements/{{SLUG}}/02-era-spec.json --out engagements/{{SLUG}}/03-mapping.md
python3 tools/websafe.py snap --from-inventory engagements/{{SLUG}}/01-inventory/inventory.json --format csv
python3 tools/era_lint.py engagements/{{SLUG}}/05-build --spec engagements/{{SLUG}}/02-era-spec.json
python3 tools/gif_audit.py engagements/{{SLUG}}/05-build
python3 tools/rubric.py score engagements/{{SLUG}}/06-qa/scorecard.json
```

## Decisions log

| Date | Decision | Why | By |
|---|---|---|---|
| {{DATE}} | Engagement opened with preset {{PRESET}} | Intake request | orchestrator |
