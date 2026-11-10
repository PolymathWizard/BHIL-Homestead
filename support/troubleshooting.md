---
title: "Troubleshooting"
description: "Fixes for the problems people hit most often."
---

# Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `survey.py` fails with HTTP 403 or a timeout | The site blocks automated requests | Save the page from a browser (HTML only) and survey the file |
| Survey finds almost no patterns | Navigation and content are rendered by JavaScript | Save the rendered page from the browser, or add patterns to `notes.md` by hand |
| `era_lint.py` reports HL015 on every page | The safety layer is not linked | Add both `homestead-safe.css` and `homestead-safe.js` to the head and copy the files next to the page |
| HL021 missing marker for a widget you built | The widget has no marker comment | Add `<!-- hs:widget ID -->` next to it |
| HL022 era mixing on a deliberate hybrid | No time capsule declared | Set `time_capsule: true`, write the story, list the widgets in `allowed_extra_widgets` |
| HL023 canvas warning on a plain page | Page has no fixed-width outer table | Add one, or mark a text-only page with `<!-- hs:page text-only -->` |
| HL020 off-palette color | A flat color is not web-safe | `python3 tools/websafe.py snap "#RRGGBB"` and use the result |
| HL028 motion budget exceeded | Too many marquees, blinks, or animated GIFs on one page | Remove some or move them to another page |
| `gif_audit.py` OVER TIMING BUDGET | Frames faster than 340 ms | Regenerate with gifsmith, which floors delays automatically |
| `dither.py` says unsupported PNG | 16-bit, interlaced, or not a PNG | Re-export as an 8-bit non-interlaced PNG |
| Music does not play | Browsers block audio without a click, or Safe Mode is on | Click the music control; turn Safe Mode off |
| Safe Mode button missing | `homestead-safe.js` failed to load | Check the path and that the file sits next to the page |
| `verify_drift.py` fails after an edit | A derived file was edited by hand, or canon changed without a rebuild | Edit canon, run `python3 scripts/build_derived.py`, commit both |
| `validate.py` counts failure | A canon count changed | Update `EXPECTED` in `scripts/validate.py` in the same commit |
| `validate.py` dash gate failure | An em or en dash slipped in | Replace with a comma, colon, or "to" |
| `mkdocs build --strict` warns about a link | A link points outside the assembled tree | Run `python3 scripts/build_site.py --assemble` first, then use repo-relative links |
