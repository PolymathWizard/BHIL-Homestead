---
title: "Preset F: Modern revival (Neocities / small web)"
description: "Era spec for preset F (2013-now)."
generated: true
preset: "F"
preset_status: "spec-only"
---

<!-- Generated from canon/ by scripts/build_derived.py. Do not edit by hand; edit canon and rebuild. -->

# Preset F: Modern revival (Neocities / small web)

**Years:** 2013-now. **Status:** spec-only. Spec only. No kit yet; scaffold starts from a blank page.

## Identity

| Field | Value |
|---|---|
| Target resolution | any |
| Target browser | Any current browser |
| Host context | Neocities or another static host |
| Canvas | any. Hand-coded, fixed or fluid by choice. |
| Palette mode | full |
| Layout mode | hand-coded |
| Motion budget | 5 moving items per page |
| Audio | click-to-play |

## Palette

| Role | Color | Web-safe |
|---|---|---|
| bg | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#000033;vertical-align:middle"></span> `#000033` | yes |
| text | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#FFFFFF;vertical-align:middle"></span> `#FFFFFF` | yes |
| link | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#66FFFF;vertical-align:middle"></span> `#66FFFF` | yes |
| vlink | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#FF99FF;vertical-align:middle"></span> `#FF99FF` | yes |
| alink | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#FFFF66;vertical-align:middle"></span> `#FFFF66` | yes |

Deliberately retro, knowingly chosen.

## Fonts

| Role | Stack |
|---|---|
| body | Verdana, Arial, sans-serif |
| heading | Arial Black, Arial, sans-serif |
| display | Comic Sans MS, cursive |
| mono | Courier New, Courier, monospace |

System fonts only. See [font map](../reference/font-map.md) and [legal notes](../10-legal-and-licensing.md).

## Layout and navigation

Hand-coded pages, often with Windows-style window chrome for panels.

Navigation: Sidebar or button wall.

## Widgets

Required (the lint warns when a marker is missing):

| Widget | What it is |
|---|---|
| `safe-mode-toggle` | Persistent control that pauses animation, stops marquees, mutes audio, and raises contrast. Provided by the safety layer and required on every build. |
| `text-only-link` | A plain link to a stripped, high-contrast version of the page. Period-correct and the main accessibility escape hatch. |
| `button-88x31` | A cluster of 88 by 31 pixel link buttons for friends, tools, and causes. |
| `webring` | Bordered table with previous, next, random, and list links for a themed ring. |
| `guestbook` | Sign my guestbook page with dated visitor entries. Replaces testimonials. |

Optional: `last-updated`, `email-me`, `hit-counter`, `under-construction`, `rainbow-rule`, `star-tile-bg`, `whats-new`, `midi-player`, `glitter-text`, `blinkies`.

Era mixing (the lint errors unless the era spec declares a time capsule): `mailto-text`, `browser-badge`, `neighborhood-address`, `splash-page`, `cursor-trail`, `aim-icq`, `status-bar-scroller`, `shared-borders`, `theme-banner`, `hover-buttons`, `search-form`, `feedback-form`, `copyright-footer`, `printer-friendly-link`, `broken-component-placeholder`, `frames-notice`, `banner-ad-manager`, `flash-intro`, `web-portal-modules`, `user-css-layout`, `profile-blurbs`, `interests-details`, `contact-table`, `top-8`, `comments-wall`, `profile-music-player`, `online-now`, `profile-views`, `custom-cursor`.

Forbidden elements: tracking scripts; cookie banners.

## Voice

Knowing and affectionate.

- welcome to my little corner of the web
- sign the guestbook, it's real
- best viewed with your heart

## Lived-in details

- Button wall of friends
- Small web manifesto link

## Reference sources

- [Neocities](https://neocities.org/) (`S-NEOCITIES`)
- [98.css](https://jdan.github.io/98.css/) (`S-98CSS`)
- [retro-css list (GitHub)](https://github.com/matt-auckland/retro-css) (`S-RETRO-CSS`)
