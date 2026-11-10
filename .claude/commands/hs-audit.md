---
description: HOMESTEAD Phase 6 only. Blind authenticity and safety audit with a 40-point scorecard.
argument-hint: <slug>
---

# /hs-audit

Delegate to the `authenticity-auditor` subagent for engagement `$ARGUMENTS`. Pass only the era spec, the build folder, the asset log, and the inventory paths. Do not pass the mapping notes or decisions log.

Write the returned scorecard JSON to `engagements/<slug>/06-qa/scorecard.json` and the notes to `06-qa/qa-notes.md` without changing a score, then run:

```bash
python3 tools/era_lint.py engagements/<slug>/05-build --spec engagements/<slug>/02-era-spec.json --format json > engagements/<slug>/06-qa/lint.json
python3 tools/rubric.py score engagements/<slug>/06-qa/scorecard.json --lint engagements/<slug>/06-qa/lint.json --write
```

Report the total, the verdict, any hard gate failures, and every row below 2.
