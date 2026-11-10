---
id: "ADR-006"
title: "Repository-wide dash gate"
status: "accepted"
date: "2026-11-10"
---

# ADR-006: Repository-wide dash gate

## Context

BHIL repositories forbid em dashes and en dashes in derived prose. Some BHIL repositories scope the rule because a canonical source mandates dashes. HOMESTEAD has no such source: its canon, docs, prompts, kits, and period copy are all written for this repository.

## Decision

The dash gate is repository-wide. `scripts/validate.py` scans the raw bytes of every non-binary file for the em dash and en dash characters and for their HTML entities, and fails on any hit. Period copy in kits and examples is included; ranges use "to" or a hyphen-minus.

## Consequences

- No scoping exceptions to maintain.
- Contributors pasting copy from modern sites will hit the gate; the fix is mechanical.

## Alternatives considered

- **Scoped gate like the VIC repository.** Rejected; no canonical source requires dashes here.
