---
description: Run the full HOMESTEAD pipeline on a site, from intake to a scored period build.
argument-hint: <url-or-saved-html> <preset A-F or recommend> [slug]
---

# /homestead

Redesign `$ARGUMENTS` as an old-school website with the full HOMESTEAD pipeline. You are the orchestrator (Opus). Delegate each phase to its subagent and keep the engagement folder as the record.

## 0. Intake (you)

1. Parse the arguments: target, preset (or `recommend`), and slug (default: the target's domain name without dots).
2. Open the engagement:

   ```bash
   python3 tools/scaffold.py new <slug> --target <target> --preset <preset or B> --purpose <purpose> --asset-policy originals-only
   ```

3. Fill `engagements/<slug>/00-intake.md`. If purpose, brand ownership, or asset policy is unclear and the person is present, ask now (checkpoint 1). Default to portfolio and originals-only when working unattended, and log that choice.

## 1. Survey

Delegate to `site-surveyor` with the slug, target, and page budget. Expect `01-inventory/inventory.json` and `notes.md`.

## 2. Era lock

Delegate to `era-archivist`. Expect a finished `02-era-spec.json`. Show the person the preset, year, and canvas (checkpoint 2). If the archivist picked a spec-only preset (A, D, F), say the build starts from a blank page.

## 3. Mapping

Delegate to `component-mapper`. Expect `03-mapping.md` and `03-copy-deck.md`. Show every DROP that loses a key fact or CTA (checkpoint 3).

## 4. Assets

Delegate to `asset-smith`. Expect images, audio, and `04-asset-log.csv`, with zero gif_audit failures.

## 5. Build

Delegate to `period-builder`. The PostToolUse hook lints every write. Expect `era_lint --strict` to exit 0.

## 6. QA

Delegate to `authenticity-auditor` with only the era spec, the build, the asset log, and the inventory. Write its scorecard JSON to `06-qa/scorecard.json` and its notes to `06-qa/qa-notes.md` verbatim, then:

```bash
python3 tools/era_lint.py engagements/<slug>/05-build --spec engagements/<slug>/02-era-spec.json --format json > engagements/<slug>/06-qa/lint.json
python3 tools/rubric.py score engagements/<slug>/06-qa/scorecard.json --lint engagements/<slug>/06-qa/lint.json --write
```

- SHIP: present the build (checkpoint 4) with the score and the rows below 2.
- REVISE: send the rows to fix back to `period-builder` (or `component-mapper` for copy and parity rows), then audit again. Stop after two loops and report.
- REBUILD: return to era lock with the auditor's reasons.

## Finish

Update the phase tracker in `engagements/<slug>/README.md`, then report: preset and year, pages built, score and verdict, the lowest rows, and how to view the build (open `05-build/index.html`).
