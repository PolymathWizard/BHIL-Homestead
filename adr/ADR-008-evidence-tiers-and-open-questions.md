---
id: "ADR-008"
title: "Evidence tiers for claims, open questions with settling criteria"
status: "accepted"
date: "2026-11-10"
---

# ADR-008: Evidence tiers for claims, open questions with settling criteria

## Context

HOMESTEAD's presets rest on historical claims: resolution shares, the web-safe palette, FrontPage components, MySpace profile anatomy, browser support for dead tags. Some are well sourced, some come from retrospective or tutorial sites, and one (frameset support) is contradicted by the HTML standard. Treating them all as fact would bake errors into canon.

## Decision

Every factual claim lives in `canon/sources.json` with an ID, a tier (VERIFIED, CORROBORATED, STATED, UNCORROBORATED, INFERENCE), and its sources. CORROBORATED requires two or more independent sources, enforced by the validator. No claim is VERIFIED at v1.0.0 because no primary artifact was re-checked at build time; promoting a claim requires a commit recording what was checked. Docs cite claims inline by tier and ID. HOMESTEAD design guidance derived from claims is tagged INFERENCE.

Unresolved design questions are recorded in ADRs with settling criteria rather than closed silently.

## Consequences

- Readers can see which constraints are history and which are house style.
- Disputed claims (C-009 frameset support, C-025 Top 8 history) stay visible and do not drive hard rules alone.

## Open questions

| Question | Settling criteria |
|---|---|
| Ship the 22-color "really safe" sub-palette (C-005)? | The list is checked against the primary Lehn and Stern source |
| Treat 0 and 1 centisecond GIF delays as 100 ms everywhere? | Verified in current Chrome, Firefox, and Safari |
| Add red-flash detection beyond the saturated-red heuristic? | A reference implementation of the WCAG red flash definition that runs in stdlib |
