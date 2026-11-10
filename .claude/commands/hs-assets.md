---
description: HOMESTEAD Phase 4 only. Generate and log every image and sound the build needs.
argument-hint: <slug>
---

# /hs-assets

Delegate to the `asset-smith` subagent for engagement `$ARGUMENTS`.

Requires `03-mapping.md` and `03-copy-deck.md`. When it returns, confirm every file in `05-build/images/` and `05-build/audio/` appears in `04-asset-log.csv` and that `python3 tools/gif_audit.py engagements/<slug>/05-build` reports no failures.
