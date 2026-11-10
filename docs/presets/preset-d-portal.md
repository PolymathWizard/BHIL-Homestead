---
title: "Preset D: Web 1.5 portal / Y2K corporate"
description: "Era spec for preset D (1999-2004)."
generated: true
preset: "D"
preset_status: "spec-only"
---

<!-- Generated from canon/ by scripts/build_derived.py. Do not edit by hand; edit canon and rebuild. -->

# Preset D: Web 1.5 portal / Y2K corporate

**Years:** 1999-2004. **Status:** spec-only. Spec only. No kit yet; scaffold starts from a blank page.

## Identity

| Field | Value |
|---|---|
| Target resolution | 800x600 to 1024x768 |
| Target browser | Internet Explorer 5.5 or 6 |
| Host context | Corporate or media domain |
| Canvas | 760 px (alternate 780 px). Three-column table at 760 to 780 px. INFERENCE from C-002. |
| Palette mode | full |
| Layout mode | three-column |
| Motion budget | 3 moving items per page |
| Audio | none |

## Palette

| Role | Color | Web-safe |
|---|---|---|
| bg | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#FFFFFF;vertical-align:middle"></span> `#FFFFFF` | yes |
| text | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#000000;vertical-align:middle"></span> `#000000` | yes |
| link | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#003399;vertical-align:middle"></span> `#003399` | yes |
| vlink | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#666699;vertical-align:middle"></span> `#666699` | yes |
| alink | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#CC0000;vertical-align:middle"></span> `#CC0000` | yes |

Fuller color with glossy gradients rendered as GIF images, silver and blue tech accents.

## Fonts

| Role | Stack |
|---|---|
| body | Verdana, Tahoma, Arial, sans-serif |
| heading | Tahoma, Verdana, sans-serif |
| display | Arial Black, Arial, sans-serif |
| mono | Courier New, Courier, monospace |

System fonts only. See [font map](../reference/font-map.md) and [legal notes](../10-legal-and-licensing.md).

## Layout and navigation

Three-column tables, dense link rails, tabbed navigation GIFs.

Navigation: Tab GIF row across the top and a dense left link rail.

## Widgets

Required (the lint warns when a marker is missing):

| Widget | What it is |
|---|---|
| `safe-mode-toggle` | Persistent control that pauses animation, stops marquees, mutes audio, and raises contrast. Provided by the safety layer and required on every build. |
| `text-only-link` | A plain link to a stripped, high-contrast version of the page. Period-correct and the main accessibility escape hatch. |
| `last-updated` | A hand-typed or Timestamp-component date such as Last updated 3/14/98. |
| `web-portal-modules` | Weather, stocks, headlines, and My Page style boxes in a three-column table. |
| `search-form` | A small search form, FreeFind style on personal pages or the Search component on corporate pages. |
| `banner-ad-manager` | 468 by 60 rotating banner, originally a Java applet, rebuilt as an image swap. |
| `copyright-footer` | Copyright, company, All rights reserved, and a Webmaster mailto. |
| `printer-friendly-link` | Printer-friendly version link, the period answer to alternate color schemes. |

Optional: `mailto-text`, `browser-badge`, `hit-counter`, `splash-page`, `aim-icq`, `feedback-form`, `flash-intro`.

Era mixing (the lint errors unless the era spec declares a time capsule): `email-me`, `guestbook`, `webring`, `under-construction`, `rainbow-rule`, `star-tile-bg`, `neighborhood-address`, `whats-new`, `midi-player`, `cursor-trail`, `button-88x31`, `status-bar-scroller`, `shared-borders`, `theme-banner`, `hover-buttons`, `broken-component-placeholder`, `frames-notice`, `user-css-layout`, `profile-blurbs`, `interests-details`, `contact-table`, `top-8`, `comments-wall`, `profile-music-player`, `glitter-text`, `blinkies`, `online-now`, `profile-views`, `custom-cursor`.

Forbidden elements: glitter text; webrings; starry backgrounds; web fonts; rounded corners; emoji.

## Voice

Corporate-cheerful. e-everything.

- Your e-business solution
- Personalize this page
- Click here to make us your home page

## Lived-in details

- Make this my home page link
- Weather box for a default city
- Flash banner slot

## Reference sources

- [Wayback Machine (Internet Archive)](https://web.archive.org) (`S-WAYBACK`)
