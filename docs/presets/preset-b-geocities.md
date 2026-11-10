---
title: "Preset B: GeoCities / Angelfire / Tripod personal homepage"
description: "Era spec for preset B (1995-2000)."
generated: true
preset: "B"
preset_status: "kit"
---

<!-- Generated from canon/ by scripts/build_derived.py. Do not edit by hand; edit canon and rebuild. -->

# Preset B: GeoCities / Angelfire / Tripod personal homepage

**Years:** 1995-2000. **Status:** kit. Kit available at [kits/preset-b-geocities](../../kits/preset-b-geocities/README.md).

## Identity

| Field | Value |
|---|---|
| Target resolution | 640x480 to 800x600 |
| Target browser | Netscape Navigator 3 or 4 |
| Host context | Free homestead in a themed neighborhood, for example SiliconValley/Heights/4021 |
| Canvas | 600 px (alternate 760 px). 600 to 620 px content for 1996 to 1998, 760 px for 1999 to 2000. INFERENCE from C-001. |
| Palette mode | web-safe-216 |
| Layout mode | centered-column |
| Motion budget | 4 moving items per page |
| Audio | click-to-play |

## Palette

| Role | Color | Web-safe |
|---|---|---|
| bg | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#000000;vertical-align:middle"></span> `#000000` | yes |
| text | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#FFFFFF;vertical-align:middle"></span> `#FFFFFF` | yes |
| link | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#00FFFF;vertical-align:middle"></span> `#00FFFF` | yes |
| vlink | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#FF00FF;vertical-align:middle"></span> `#FF00FF` | yes |
| alink | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#FFFF00;vertical-align:middle"></span> `#FFFF00` | yes |

Flat colors snap to the 216 web-safe cube (C-003). Photos use an adaptive palette GIF or a low-quality JPEG (C-004).

## Fonts

| Role | Stack |
|---|---|
| body | Times New Roman, Times, serif |
| heading | Arial, Helvetica, sans-serif |
| display | Comic Sans MS, cursive |
| mono | Courier New, Courier, monospace |

System fonts only. See [font map](../reference/font-map.md) and [legal notes](../10-legal-and-licensing.md).

## Layout and navigation

Centered column via the center element. Tables after about 1997. Framesets were common and are emulated, never used.

Navigation: Text links separated by pipes at top and bottom, plus a few button GIFs.

## Widgets

Required (the lint warns when a marker is missing):

| Widget | What it is |
|---|---|
| `safe-mode-toggle` | Persistent control that pauses animation, stops marquees, mutes audio, and raises contrast. Provided by the safety layer and required on every build. |
| `text-only-link` | A plain link to a stripped, high-contrast version of the page. Period-correct and the main accessibility escape hatch. |
| `last-updated` | A hand-typed or Timestamp-component date such as Last updated 3/14/98. |
| `email-me` | An animated or static Email Me graphic wrapped in a mailto link. |
| `browser-badge` | Best viewed with a named browser at a named resolution. Use generic text or an original badge for client work. |
| `hit-counter` | Odometer digits such as You are visitor #004217. |
| `guestbook` | Sign my guestbook page with dated visitor entries. Replaces testimonials. |
| `webring` | Bordered table with previous, next, random, and list links for a themed ring. |
| `under-construction` | Construction sign on unfinished sections. On FrontPage sites usually a single small GIF on a stub page. |
| `rainbow-rule` | A GIF divider used in place of the hr element. |
| `neighborhood-address` | A themed homestead address such as SiliconValley/Heights/4021 matching the site topic. |
| `whats-new` | Dated update log with NEW graphics. On corporate sites it becomes Press Releases or News. |
| `midi-player` | A Turn on music control that plays a pre-rendered MIDI-style track only after a click. |

Optional: `star-tile-bg`, `splash-page`, `cursor-trail`, `aim-icq`, `button-88x31`, `status-bar-scroller`, `search-form`, `frames-notice`.

Era mixing (the lint errors unless the era spec declares a time capsule): `mailto-text`, `shared-borders`, `theme-banner`, `hover-buttons`, `feedback-form`, `copyright-footer`, `printer-friendly-link`, `broken-component-placeholder`, `banner-ad-manager`, `flash-intro`, `web-portal-modules`, `user-css-layout`, `profile-blurbs`, `interests-details`, `contact-table`, `top-8`, `comments-wall`, `profile-music-player`, `glitter-text`, `blinkies`, `online-now`, `profile-views`, `custom-cursor`.

Forbidden elements: glitter text; Top 8 grids; shared borders; theme banners; web fonts; rounded corners; CSS gradients; emoji.

## Voice

Exuberant, personal, generous with exclamation points and capital letters.

- Welcome to my HOMEPAGE!!!
- Sign my guestbook!
- This page is under construction, come back soon!
- You are visitor number
- Thanks for stopping by!

## Lived-in details

- Neighborhood address that matches the topic
- Last updated date that is slightly stale
- Webring previous and next links
- A generic Best viewed at 800x600 badge

## Component mapping for this preset

| Modern pattern | Preset B equivalent | Widgets |
|---|---|---|
| Hero section | Big centered WordArt title, an animated GIF, and Welcome to my homepage! | neighborhood-address |
| Sticky header or hamburger menu | Text links separated by pipes at top and bottom | none |
| Mega-menu | A Site Map page | none |
| Cards or feature grid | Bulleted list with ball bullet GIFs | none |
| Pricing table | Prices page with a bordered table | none |
| Testimonials | Guestbook entries such as Cool site!! | guestbook |
| Blog, changelog, or news | What's New log with dated entries and NEW graphics | whats-new |
| Social icons | Webring box, an Email me graphic, and an ICQ number or AIM screen name | webring, email-me, aim-icq |
| Analytics | Visible hit counter: You are visitor #004217 | hit-counter |
| Cookie banner | Best viewed at 800x600 badge | browser-badge |
| Newsletter signup | Join my mailing list form, or Sign my guestbook | guestbook |
| Site search | Search this site box, FreeFind style | search-form |
| Product pages or shop | Photo, description, and price in a table | none |
| SaaS app or dashboard | Screenshots page of a desktop program window and a Download Now! (2.3 MB) link | none |
| Login | Members Only password page | none |
| Chatbot or live chat | Chat Room link, or Leave a message on my ICQ | aim-icq |
| Video | Click here to download (QuickTime, 4.1 MB) | none |
| Docs or help center | FAQ page with anchor links | none |
| FAQ accordion | FAQ page with Q: and A: pairs and a Back to top link | none |
| Dark mode | Black or starry background is already the default; add a text-only version link | text-only-link, star-tile-bg |
| Careers | Help Wanted! graphic | none |
| Customer logo strip | Cool Sites I Like list or an 88x31 button wall | button-88x31 |
| Footer | Last updated date, mailto, webring, award badges, and the counter | last-updated, email-me, webring, hit-counter |
| Accessibility statement | Text-only version link | text-only-link |

## Reference sources

- [Restorativland GeoCities Gallery](https://geocities.restorativland.org) (`S-RESTORATIVLAND`)
- [One Terabyte of Kilobyte Age (GeoCities Research Institute blog)](https://blog.geocities.institute) (`S-OOKA`)
- [GifCities](https://gifcities.org) (`S-GIFCITIES`)
- [Cameron's World](https://www.cameronsworld.net) (`S-CAMERONSWORLD`)
- [A Vernacular Web, excerpts (Olia Lialina)](https://www.andorgallery.com/shows/images/vernacular_web_excerpts.pdf) (`S-LIALINA-VERNACULAR`)
- [Space Jam (1996 site)](https://www.spacejam.com/1996/) (`S-SPACEJAM`)
