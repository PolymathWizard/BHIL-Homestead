---
title: "QA notes"
phase: 6
---

# QA notes

The authenticity auditor fills this in without reading the builder's notes. Paste tool output, then judge.

## Tool results

| Check | Command | Result |
|---|---|---|
| Anachronism lint | `python3 tools/era_lint.py 05-build --spec 02-era-spec.json --format json` | |
| GIF timing and flash audit | `python3 tools/gif_audit.py 05-build --page-bg "<page bg>"` | |
| Scorecard | `python3 tools/rubric.py score 06-qa/scorecard.json --lint lint.json` | |

## Manual checks

- [ ] View Source on every page reads as period markup apart from the two safety layer links
- [ ] Safe Mode stops every marquee, blink, animated GIF, cursor effect, and sound
- [ ] Safe Mode raises contrast enough to read every page
- [ ] The text-only page carries every link and every key fact
- [ ] Keyboard alone reaches every link, button, and form field in a sensible order
- [ ] Every image has alt text; spacer GIFs have empty alt
- [ ] Every file in images/ and audio/ appears in the asset log
- [ ] Third-party marks are descriptive only, and the disclaimer is present when needed
- [ ] Two or three archive references for the preset were compared side by side

## Reference comparison

| Reference URL | What matches | What does not |
|---|---|---|
| | | |

## Verdict

SHIP, REVISE, or REBUILD, with the rows to fix and why.
