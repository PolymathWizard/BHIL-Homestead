---
id: "ADR-005"
title: "Blind, read-only auditor"
status: "accepted"
date: "2026-11-10"
---

# ADR-005: Blind, read-only auditor

## Context

A builder that grades its own work reliably over-scores it. Explanations of a choice ("generic badges for rights reasons") are persuasive and bias the grade even when the choice was right.

## Decision

Phase 6 belongs to the `authenticity-auditor` subagent, whose tools are Read, Glob, Grep, and Bash only. It reads the era spec, the build, the inventory, and the asset log. It does not read the mapping rationale or decisions log until scores are final. It returns a scorecard and notes; the orchestrator writes them verbatim and runs `tools/rubric.py`, which also caps any row tied to a failing lint rule.

## Consequences

- Scores are evidence-based and reproducible by a second auditor.
- The orchestrator cannot quietly adjust a score; the rubric tool recomputes totals and verdicts.
- Some well-reasoned trades still cost points. They are visible, which is the point.

## Alternatives considered

- **Builder self-scores with lint support.** Rejected; the work would grade itself.
- **Human-only audit.** Kept as checkpoint 4, not as the only gate.
