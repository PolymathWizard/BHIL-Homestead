---
description: HOMESTEAD Phase 5 only. Write the period pages with the safety layer, linting after every file.
argument-hint: <slug>
---

# /hs-build

Delegate to the `period-builder` subagent for engagement `$ARGUMENTS`.

Requires the mapping, copy deck, and assets. When it returns, run:

```bash
python3 tools/era_lint.py engagements/<slug>/05-build --spec engagements/<slug>/02-era-spec.json --strict
```

Report the verdict exactly as printed. NO FINDINGS (INCONCLUSIVE) is the best possible lint result; it is not a pass on authenticity.
