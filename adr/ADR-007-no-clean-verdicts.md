---
id: "ADR-007"
title: "No component ever reports clean"
status: "accepted"
date: "2026-11-10"
---

# ADR-007: No component ever reports clean

## Context

BHIL principle: absence of anomaly reports is INCONCLUSIVE, never CLEAN. HOMESTEAD's automated checks are partial by nature. The lint catches known tells but cannot see whether a page looks right. The GIF audit measures a file at native size but cannot see a page that scales, tiles, or repeats it.

## Decision

Verdict vocabulary is fixed:

| Tool | Verdicts |
|---|---|
| `era_lint.py` | FINDINGS, WARNINGS ONLY, NO FINDINGS (INCONCLUSIVE) |
| `gif_audit.py` | STATIC, OVER TIMING BUDGET, FLASH RISK, WITHIN BUDGET (INCONCLUSIVE FOR SCALED OR TILED USE) |
| `rubric.py` | INCOMPLETE, REBUILD, REVISE, SHIP |

Agents and docs never describe a build as clean, safe, or perfect. SHIP is a decision backed by a scorecard, not a claim of absence.

## Consequences

- Readers are never told more than the tools know.
- Tests assert that the best verdicts contain INCONCLUSIVE and never CLEAN.
