---
id: "P07"
title: "The Period Builder"
phase: "5"
owner: "period-builder"
key_variables: ["Era Spec", "Mapping Table", "Copy Deck", "Asset List", "Kit"]
---

# P07: The Period Builder

*Write pages the way they were written in the era, so View Source tells the same story as the screen.*

## Prompt metadata

| Field | Detail |
|---|---|
| **Writing type** | HTML pages in period markup with a modern safety layer |
| **Research focus** | Table layouts, font tags, spacer GIFs, image maps, period comments, and user CSS, emulating dead technology safely |
| **Rhetorical mode** | Constructive |
| **Purpose** | Produce the deliverable |
| **Target audience** | Visitors, the auditor, anyone who opens View Source |
| **Tone** | The era's |
| **Named framework** | Period markup with safety layer (ADR-003) |
| **Key variables** | `[Era Spec]`, `[Mapping Table]`, `[Copy Deck]`, `[Asset List]`, `[Kit]` |

## Markup rules by preset

| Preset | Skeleton | Signature source details |
|---|---|---|
| B GeoCities | `body background` tile, `center`, outer table at 600 or 760 px | `font face size color`, rainbow rule images, commented `bgsound`, marquee |
| C FrontPage | Outer 760 px table split into top, left, and bottom shared borders | `webbot` include comments, GENERATOR and theme meta tags, image-swap script with focus handlers |
| E MySpace | Default profile tables at 800 px with profile class names | A `style` block pasted inside About Me with `!important` overrides |

Dead technology and its safe emulation: blink stays in source and the safety layer animates it; framesets become tables; applets become image swaps; Flash intros become a 550 by 400 HTML stage; `window.status` scrollers become a form text field ticker that checks `window.homesteadSafe()`.

## Non-negotiables on every page

1. `homestead-safe.css` and `homestead-safe.js` linked in the head.
2. `data-still` on every animated GIF; alt text on every image.
3. Audio only through `data-hs-audio`.
4. A link to the text-only version.
5. A widget marker comment next to every widget.
6. No flexbox, grid, rounded corners, blurred shadows, gradients, rem or viewport units, web fonts, SVG, srcset, lazy loading, or emoji in presets A to E.

## Mandatory output structure

Complete HTML for each page in the sitemap, then `text-only.html`, then the final `era_lint --strict` result and a list of anything from the mapping that could not be placed.

## The prompt

> *You are a web designer in the year set by `[Era Spec]`, starting from `[Kit]`. Build every page in the sitemap from `[Mapping Table]`, using only the copy in `[Copy Deck]` and the files in `[Asset List]`.*
>
> *Write period markup that would survive View Source in that year, at the era canvas width. Follow the markup rules for the preset and the non-negotiables on every page. Emulate dead technology only in the safe forms listed. Lint after every page and fix errors before moving on. Write the text-only page last, carrying every key fact and link.*

## Quality bar

- Opening View Source on any page shows period markup and exactly two modern lines.
- The lint reports no errors and no warnings.
- Nothing from the mapping is silently missing.

## Feeds into

P08, P09.
