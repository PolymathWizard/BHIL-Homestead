---
description: HOMESTEAD Phase 1 only. Inventory a modern site into an engagement folder.
argument-hint: <slug> <url-or-saved-html> [pages]
---

# /hs-survey

Delegate to the `site-surveyor` subagent with these arguments: `$ARGUMENTS`.

If `engagements/<slug>/` does not exist yet, open it first with `python3 tools/scaffold.py new <slug> --target <target> --preset B` and note that the preset is a placeholder until era lock.

Report the pattern count, nav item count, web fonts found, top brand colors with their web-safe snaps, and the surveyor's must-keep list.
