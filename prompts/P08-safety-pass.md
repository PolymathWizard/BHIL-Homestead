---
id: "P08"
title: "The Safety and Accessibility Pass"
phase: "5"
owner: "period-builder"
key_variables: ["Build Folder", "Era Spec", "GIF Audit"]
---

# P08: The Safety and Accessibility Pass

*Keep the chaos on screen and the risk off it: every period effect gets an off switch.*

## Prompt metadata

| Field | Detail |
|---|---|
| **Writing type** | Accessibility and safety review with fixes |
| **Research focus** | WCAG 2.3.1 (three flashes), 2.2.2 (pause, stop, hide), 1.4.2 (audio control), reduced motion, keyboard access, text alternatives |
| **Rhetorical mode** | Evaluative, corrective |
| **Purpose** | Resolve the main objection to the aesthetic before the auditor sees the build |
| **Target audience** | Visitors with photosensitivity, vestibular disorders, screen readers, or keyboards |
| **Tone** | Careful |
| **Named framework** | HOMESTEAD Safe Mode (`kits/safety-layer/`) |
| **Key variables** | `[Build Folder]`, `[Era Spec]`, `[GIF Audit]` |

## Checklist

| Area | Check | Fix |
|---|---|---|
| Flash | Every animated GIF at 340 ms or slower; no large full-contrast or saturated red alternation | Regenerate with gifsmith or slow the recipe |
| Motion | Marquee, blink, GIFs, cursor trails, and tickers all stop in Safe Mode | Add `data-still`, use `window.homesteadSafe()` in scripts |
| Motion budget | Moving items per page within the era spec budget | Remove or move below the fold |
| Audio | Nothing plays without a click; a second click stops it | Use `data-hs-audio`; keep `bgsound` commented |
| Reduced motion | Safe Mode starts on when the visitor prefers reduced motion | Safety layer default; do not override |
| Contrast | Safe Mode makes every page readable | Avoid text baked into busy images without alt text |
| Keyboard | Toggle first in tab order; every link and control reachable; hover swaps mirrored on focus | Add `onfocus` and `onblur` |
| Text alternatives | Alt on every image, empty alt on spacers, labels on form fields | Add them |
| Escape hatch | Text-only page linked from every page, carrying every fact | Write or update it |

## Mandatory output structure

1. Checklist with pass or fix per row, per page.
2. GIF audit summary.
3. Changes made.
4. Residual risks the auditor should look at, for example a tiled animated background or a GIF scaled up in markup.

## The prompt

> *You are an accessibility reviewer for the HOMESTEAD build in `[Build Folder]`, era spec `[Era Spec]`, with GIF audit results `[GIF Audit]`.*
>
> *Walk the checklist for every page. Fix what fails, within the era's look. Confirm that Safe Mode stops every moving thing and every sound and raises contrast, that it starts on under reduced motion, and that the text-only page carries every fact and link. List residual risks honestly; a passing audit at native size does not cover scaled or tiled use.*

## Quality bar

- A visitor can stop everything with one control and read every page.
- No item in the checklist is marked pass without evidence.

## Feeds into

P09 (rows 16 to 19).
