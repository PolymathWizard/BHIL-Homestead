---
title: "Preset A: Proto-Web / Academic"
description: "Era spec for preset A (1993-1996)."
generated: true
preset: "A"
preset_status: "spec-only"
---

<!-- Generated from canon/ by scripts/build_derived.py. Do not edit by hand; edit canon and rebuild. -->

# Preset A: Proto-Web / Academic

**Years:** 1993-1996. **Status:** spec-only. Spec only. No kit yet; scaffold starts from a blank page.

## Identity

| Field | Value |
|---|---|
| Target resolution | 640x480 |
| Target browser | NCSA Mosaic 2 or Netscape Navigator 1.x |
| Host context | University or ISP home directory, for example /~username/ |
| Canvas | fluid. Unstyled single column that simply wraps at the window edge. |
| Palette mode | browser-default |
| Layout mode | single-column |
| Motion budget | 0 moving items per page |
| Audio | none |

## Palette

| Role | Color | Web-safe |
|---|---|---|
| bg | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#C0C0C0;vertical-align:middle"></span> `#C0C0C0` | no |
| text | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#000000;vertical-align:middle"></span> `#000000` | yes |
| link | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#0000EE;vertical-align:middle"></span> `#0000EE` | no |
| vlink | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#551A8B;vertical-align:middle"></span> `#551A8B` | no |
| alink | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#FF0000;vertical-align:middle"></span> `#FF0000` | yes |

Gray default background is UNCORROBORATED (C-030). Exact default link hex values are INFERENCE.

## Fonts

| Role | Stack |
|---|---|
| body | Times New Roman, Times, serif |
| heading | Times New Roman, Times, serif |
| display | Times New Roman, Times, serif |
| mono | Courier New, Courier, monospace |

System fonts only. See [font map](../reference/font-map.md) and [legal notes](../10-legal-and-licensing.md).

## Layout and navigation

h1, paragraphs, hr, bullet lists, address footer. No tables for layout, no background images.

Navigation: Inline text links and a Back to Home link at the foot of each page.

## Widgets

Required (the lint warns when a marker is missing):

| Widget | What it is |
|---|---|
| `safe-mode-toggle` | Persistent control that pauses animation, stops marquees, mutes audio, and raises contrast. Provided by the safety layer and required on every build. |
| `last-updated` | A hand-typed or Timestamp-component date such as Last updated 3/14/98. |
| `mailto-text` | An address element or webmaster line with a mailto link. |
| `browser-badge` | Best viewed with a named browser at a named resolution. Use generic text or an original badge for client work. |

Optional: `text-only-link`.

Era mixing (the lint errors unless the era spec declares a time capsule): `email-me`, `hit-counter`, `guestbook`, `webring`, `under-construction`, `rainbow-rule`, `star-tile-bg`, `neighborhood-address`, `whats-new`, `midi-player`, `splash-page`, `cursor-trail`, `aim-icq`, `button-88x31`, `status-bar-scroller`, `shared-borders`, `theme-banner`, `hover-buttons`, `search-form`, `feedback-form`, `copyright-footer`, `printer-friendly-link`, `broken-component-placeholder`, `frames-notice`, `banner-ad-manager`, `flash-intro`, `web-portal-modules`, `user-css-layout`, `profile-blurbs`, `interests-details`, `contact-table`, `top-8`, `comments-wall`, `profile-music-player`, `glitter-text`, `blinkies`, `online-now`, `profile-views`, `custom-cursor`.

Forbidden elements: background images; animated GIFs; tables used for layout; font color attributes; marquee; web fonts; CSS of any kind beyond the safety layer.

## Voice

Dry and first-person. Pages describe themselves.

- This page is maintained by
- Last modified:
- Comments to
- Back to my home page

## Lived-in details

- A tilde username path
- Last modified date in the footer
- A text-only access counter line

## Reference sources

- [Wayback Machine (Internet Archive)](https://web.archive.org) (`S-WAYBACK`)
- [A Vernacular Web, excerpts (Olia Lialina)](https://www.andorgallery.com/shows/images/vernacular_web_excerpts.pdf) (`S-LIALINA-VERNACULAR`)
