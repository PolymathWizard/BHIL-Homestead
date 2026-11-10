---
title: "Preset C: FrontPage / Dreamweaver small-business and corporate"
description: "Era spec for preset C (1997-2003)."
generated: true
preset: "C"
preset_status: "kit"
---

<!-- Generated from canon/ by scripts/build_derived.py. Do not edit by hand; edit canon and rebuild. -->

# Preset C: FrontPage / Dreamweaver small-business and corporate

**Years:** 1997-2003. **Status:** kit. Kit available at [kits/preset-c-frontpage](../../kits/preset-c-frontpage/README.md).

## Identity

| Field | Value |
|---|---|
| Target resolution | 800x600 |
| Target browser | Internet Explorer 5 or Netscape Navigator 4 |
| Host context | Company domain on a host with server extensions |
| Canvas | 760 px. Fixed table of about 760 px centered on a patterned background. INFERENCE from C-002. |
| Palette mode | theme |
| Layout mode | shared-borders |
| Motion budget | 3 moving items per page |
| Audio | none-or-click-to-play |

## Palette

| Role | Color | Web-safe |
|---|---|---|
| bg | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#FFFFFF;vertical-align:middle"></span> `#FFFFFF` | yes |
| text | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#000033;vertical-align:middle"></span> `#000033` | yes |
| link | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#003399;vertical-align:middle"></span> `#003399` | yes |
| vlink | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#663399;vertical-align:middle"></span> `#663399` | yes |
| alink | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#CC0000;vertical-align:middle"></span> `#CC0000` | yes |

Theme-driven. Flat art web-safe, photos adaptive. HOMESTEAD ships original look-alike themes, never Microsoft theme files.

## Fonts

| Role | Stack |
|---|---|
| body | Verdana, Arial, Helvetica, sans-serif |
| heading | Book Antiqua, Times New Roman, serif |
| display | Impact, Arial Black, sans-serif |
| mono | Courier New, Courier, monospace |

System fonts only. See [font map](../reference/font-map.md) and [legal notes](../10-legal-and-licensing.md).

## Layout and navigation

Top, left, and bottom shared borders around a nested table body. Image maps for banners. Frames emulated if the concept calls for them.

Navigation: Left shared border with beveled theme buttons and hover image swaps, plus a text link row in the bottom border.

## Widgets

Required (the lint warns when a marker is missing):

| Widget | What it is |
|---|---|
| `safe-mode-toggle` | Persistent control that pauses animation, stops marquees, mutes audio, and raises contrast. Provided by the safety layer and required on every build. |
| `text-only-link` | A plain link to a stripped, high-contrast version of the page. Period-correct and the main accessibility escape hatch. |
| `last-updated` | A hand-typed or Timestamp-component date such as Last updated 3/14/98. |
| `mailto-text` | An address element or webmaster line with a mailto link. |
| `browser-badge` | Best viewed with a named browser at a named resolution. Use generic text or an original badge for client work. |
| `shared-borders` | FrontPage-style top, left, and bottom regions repeated on every page. |
| `theme-banner` | A themed banner graphic carrying the page title, generated per page. |
| `hover-buttons` | Beveled nav buttons with a hover state, rebuilt as image swaps the way careful developers did after Java applets failed. |
| `search-form` | A small search form, FreeFind style on personal pages or the Search component on corporate pages. |
| `feedback-form` | Contact Us form with name, email, comments, and a gray Submit button. |
| `copyright-footer` | Copyright, company, All rights reserved, and a Webmaster mailto. |
| `whats-new` | Dated update log with NEW graphics. On corporate sites it becomes Press Releases or News. |
| one of `hit-counter`, `broken-component-placeholder` | Any one satisfies the requirement. |

Optional: `hit-counter`, `guestbook`, `under-construction`, `midi-player`, `splash-page`, `cursor-trail`, `status-bar-scroller`, `printer-friendly-link`, `broken-component-placeholder`, `frames-notice`, `banner-ad-manager`, `flash-intro`.

Era mixing (the lint errors unless the era spec declares a time capsule): `email-me`, `webring`, `rainbow-rule`, `star-tile-bg`, `neighborhood-address`, `aim-icq`, `button-88x31`, `web-portal-modules`, `user-css-layout`, `profile-blurbs`, `interests-details`, `contact-table`, `top-8`, `comments-wall`, `profile-music-player`, `glitter-text`, `blinkies`, `online-now`, `profile-views`, `custom-cursor`.

Forbidden elements: glitter text; webrings; starry backgrounds; neighborhood addresses; rainbow rules; web fonts; rounded corners; emoji.

## Voice

Small-business formal with a hint of brochure.

- Welcome to our Web site!
- Click here for more information.
- Copyright 2001 All rights reserved.
- Please send comments to our Webmaster.
- This page was last updated on

## Lived-in details

- A [Hit Counter] placeholder where extensions are missing
- webbot comments in the source
- A GENERATOR meta tag
- References to _borders and _vti_cnf folders

## Component mapping for this preset

| Modern pattern | Preset C equivalent | Widgets |
|---|---|---|
| Hero section | Splash page with logo and ENTER link, or a Flash-style intro with Skip Intro | splash-page, theme-banner |
| Sticky header or hamburger menu | Left shared border of theme buttons, or a left frame emulation | shared-borders, hover-buttons |
| Mega-menu | Image map navigation banner | none |
| Cards or feature grid | Two or three column table with border=1 and theme bullets | none |
| Pricing table | Catalog table with an Order Form that posts to mailto or Save Results | feedback-form |
| Testimonials | What Our Customers Say page with italic quotes | none |
| Blog, changelog, or news | Press Releases page with a Timestamp line | whats-new, last-updated |
| Social icons | Contact Us feedback form | feedback-form |
| Analytics | Odometer hit counter, or a [Hit Counter] placeholder | hit-counter, broken-component-placeholder |
| Cookie banner | This site uses frames or requires a newer browser notice | frames-notice, browser-badge |
| Newsletter signup | Subscribe to our e-Newsletter form | feedback-form |
| Site search | Search component form | search-form |
| Product pages or shop | Catalog table with thumbnails linking to larger JPEGs | none |
| SaaS app or dashboard | Product Tour with numbered screenshots and a Free 30-Day Trial download | none |
| Login | Registration component or login form in a gray table | none |
| Chatbot or live chat | Live Help pop-up, or Email our Webmaster | mailto-text |
| Video | Embedded media box with a player-style frame | none |
| Docs or help center | Support section with a Table of Contents line | none |
| FAQ accordion | FAQ page with a numbered question list and bookmarks | none |
| Dark mode | Printer-friendly version link | printer-friendly-link |
| Careers | Employment Opportunities page | none |
| Customer logo strip | Our Clients bulleted list with small logo GIFs | none |
| Footer | Copyright company Inc. All rights reserved, Webmaster line, and Best viewed with a browser badge | copyright-footer, mailto-text, browser-badge |
| Accessibility statement | Text-only version link | text-only-link |

## Reference sources

- [Microsoft unveils new FrontPage 2000 (Microsoft, 1998)](https://news.microsoft.com/source/1998/09/30/microsoft-unveils-new-frontpage-2000-broad-new-feature-set-delivers-a-breakthrough-in-ease-of-use/) (`S-MS-FP2000`)
- [FrontPage 98 themes help document (help archive)](https://helparchive.huntertur.net/document/16630) (`S-FP98-THEMES`)
- [FrontPage WebBot components (Microsoft Learn, previous versions)](https://learn.microsoft.com/en-us/previous-versions/office/developer/sharepoint-2010/ms464803(v=office.14)) (`S-MS-WEBBOTS`)
- [Special files and directories maintained by FrontPage (Softpanorama)](https://softpanorama.org/Office/Frontpage/special_files_and_directories_maintained_by_frontpage.shtml) (`S-FP-FOLDERS`)
- [ms-frontpage-visual-skill (jamarks, GitHub)](https://github.com/jamarks/ms-frontpage-visual-skill) (`S-FP-SKILL`)
