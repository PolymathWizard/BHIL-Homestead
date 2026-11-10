---
id: "ADR-001"
title: "Canonical source and drift gate"
status: "accepted"
date: "2026-11-10"
---

# ADR-001: Canonical source and drift gate

## Context

HOMESTEAD's knowledge lives in many places at once: preset docs, reference tables, era spec cards, CSV exports, diagrams, the lint, the mapper, the survey's detection, the rubric tool, and every kit's generated assets. If each is maintained by hand they drift, and a preset page will eventually disagree with the lint that enforces it.

## Decision

`canon/*.json` is the single source of truth. `scripts/build_derived.py` generates every derived artifact from it: preset pages, reference tables, era spec cards, the blank scorecard, data exports, SVG diagrams, kit and example assets, safety layer copies, the example inventory, mapping worksheets, lint reports, GIF audits, and `MANIFEST.sha256`. Tools read canon at run time through `tools/hs_core/canon.py`.

`scripts/verify_drift.py` regenerates everything into a temporary tree and fails on any byte of difference, on any manifest entry the generator no longer produces, and on any stale file in a derived-only folder. CI runs it on every push and pull request.

## Consequences

- A canon edit propagates everywhere in one rebuild.
- Hand edits to derived files fail CI. The fix is always to edit canon and rebuild.
- The example inventory is derived, so a survey regression shows up as drift.
- Generators must be deterministic: seeded randomness, first-seen palette order, sorted iteration.

## Alternatives considered

- **Hand-maintained docs with a checklist.** Rejected; drift is guaranteed over time.
- **Generate at site build only.** Rejected; GitHub readers would see stale or missing pages.

## Open questions

- Should example period pages themselves be generated from a structured content file? Settling criteria: a second worked example that would share more than half its markup with the first.
