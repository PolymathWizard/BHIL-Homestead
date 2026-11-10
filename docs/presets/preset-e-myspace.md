---
title: "Preset E: MySpace profile / Xanga / LiveJournal"
description: "Era spec for preset E (2004-2009)."
generated: true
preset: "E"
preset_status: "kit"
---

<!-- Generated from canon/ by scripts/build_derived.py. Do not edit by hand; edit canon and rebuild. -->

# Preset E: MySpace profile / Xanga / LiveJournal

**Years:** 2004-2009. **Status:** kit. Kit available at [kits/preset-e-myspace](../../kits/preset-e-myspace/README.md).

## Identity

| Field | Value |
|---|---|
| Target resolution | 1024x768 (800x600 still common) |
| Target browser | Firefox 2 or Internet Explorer 6 or 7 |
| Host context | A profile on a social network with user CSS pasted into About Me |
| Canvas | 800 px. Default profile tables at about 800 px. INFERENCE. |
| Palette mode | full |
| Layout mode | profile-template |
| Motion budget | 6 moving items per page |
| Audio | click-to-play |

## Palette

| Role | Color | Web-safe |
|---|---|---|
| bg | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#000000;vertical-align:middle"></span> `#000000` | yes |
| text | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#FFFFFF;vertical-align:middle"></span> `#FFFFFF` | yes |
| link | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#FF66CC;vertical-align:middle"></span> `#FF66CC` | yes |
| vlink | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#CC99FF;vertical-align:middle"></span> `#CC99FF` | yes |
| alink | <span style="display:inline-block;width:14px;height:14px;border:1px solid #888;background:#00FFFF;vertical-align:middle"></span> `#00FFFF` | yes |

Full color, black and pink and neon. Glitter is the marker of this era, not stars (C-024).

## Fonts

| Role | Stack |
|---|---|
| body | Verdana, Arial, sans-serif |
| heading | Verdana, Arial, sans-serif |
| display | Comic Sans MS, cursive |
| mono | Courier New, Courier, monospace |

System fonts only. See [font map](../reference/font-map.md) and [legal notes](../10-legal-and-licensing.md).

## Layout and navigation

Fixed two-column default profile template with a gaudy user CSS block layered on top. Keep the skeleton visible underneath.

Navigation: A thin network nav bar across the top, then profile sections. Links live in About Me.

## Widgets

Required (the lint warns when a marker is missing):

| Widget | What it is |
|---|---|
| `safe-mode-toggle` | Persistent control that pauses animation, stops marquees, mutes audio, and raises contrast. Provided by the safety layer and required on every build. |
| `text-only-link` | A plain link to a stripped, high-contrast version of the page. Period-correct and the main accessibility escape hatch. |
| `user-css-layout` | A pasted style block that restyles the default profile tables. The layering is the point. |
| `profile-blurbs` | About Me and Who I'd Like to Meet sections. |
| `interests-details` | Interests rows and a Details table with status, hometown, and similar fields. |
| `contact-table` | Send Message, Add to Friends, Instant Message, and similar actions in a grid. |
| `top-8` | Grid of eight friend avatars with names. Replaces customer logo strips. |
| `comments-wall` | Friend comments with avatars, timestamps, and graphics such as Thanks for the add. |
| `profile-music-player` | Small player box for the profile song, click to play only. |
| `glitter-text` | Sparkling animated text graphic for the display name or headings. |
| `blinkies` | Small 150 by 20 animated text strips that declare likes and moods. |
| `online-now` | Small Online Now graphic next to the profile photo. |
| `profile-views` | Profile Views count in plain text, the profile era replacement for the hit counter. |

Optional: `aim-icq`, `custom-cursor`.

Era mixing (the lint errors unless the era spec declares a time capsule): `last-updated`, `mailto-text`, `email-me`, `browser-badge`, `hit-counter`, `guestbook`, `webring`, `under-construction`, `rainbow-rule`, `star-tile-bg`, `neighborhood-address`, `whats-new`, `midi-player`, `splash-page`, `cursor-trail`, `button-88x31`, `status-bar-scroller`, `shared-borders`, `theme-banner`, `hover-buttons`, `search-form`, `feedback-form`, `copyright-footer`, `printer-friendly-link`, `broken-component-placeholder`, `frames-notice`, `banner-ad-manager`, `flash-intro`, `web-portal-modules`.

Forbidden elements: shared borders; theme banners; webrings; hit counters; neighborhood addresses; web fonts; emoji; real song lyrics; network logos or wordmarks.

## Voice

Teen-confessional, decorated punctuation, inside jokes. Never quote real song lyrics.

- ~*~xOxO~*~
- thanks for the add!!
- PC4PC
- i heart spreadsheets
- rawr means i love you in dinosaur

## Lived-in details

- Thanks for the add graphics in comments
- Online Now indicator
- Top 8 ordering that tells a story
- A comment that says PC4PC

## Component mapping for this preset

| Modern pattern | Preset E equivalent | Widgets |
|---|---|---|
| Hero section | Profile banner image plus a glitter display name | glitter-text |
| Sticky header or hamburger menu | Thin network nav bar across the top | none |
| Mega-menu | Links typed into About Me | profile-blurbs |
| Cards or feature grid | Interests table rows | interests-details |
| Pricing table | Details table rows | interests-details |
| Testimonials | Comments wall with Thanks for the add graphics | comments-wall |
| Blog, changelog, or news | Blog or Bulletins box | none |
| Social icons | Contact table with Send Message, Add to Friends, and Instant Message | contact-table |
| Analytics | Profile Views count | profile-views |
| Cookie banner | Dropped: profiles carried no equivalent | none |
| Newsletter signup | Add to Friends | contact-table |
| Site search | Network search bar | none |
| Product pages or shop | Dropped: list items in About Me instead | none |
| SaaS app or dashboard | My Apps module | none |
| Login | Network login box | none |
| Chatbot or live chat | Instant Message link in the contact table | contact-table |
| Video | Embedded video player box | none |
| Docs or help center | Dropped | none |
| FAQ accordion | Who I'd Like to Meet written as questions | profile-blurbs |
| Dark mode | Pick a dark user layout | user-css-layout |
| Careers | Dropped | none |
| Customer logo strip | Top 8 friends | top-8 |
| Footer | Network footer links | none |
| Accessibility statement | Text-only version link | text-only-link |

## Reference sources

- [Blogs: MySpace (Wikibooks mirror)](https://www.englishgratis.com/1/wikibooks/blogs/myspace.htm) (`S-WIKIBOOKS-MYSPACE`)
- [MySpace layout generator (Quackit)](https://www.quackit.com/myspace/myspace_code_generators/myspace_layout_generator.cfm) (`S-QUACKIT-GEN`)
- [JellyMuffin glitter layouts](https://www.jellymuffin.com/layouts/Glitter/) (`S-JELLYMUFFIN`)
- [Fillster layout codes](https://www.fillster.com/layout2codes/326.html) (`S-FILLSTER`)
- [MySpace launches Profile 2.0 (TechCrunch, 2008)](https://techcrunch.com/2008/10/26/myspace-launches-profile-20-with-drag-and-drop-interface/) (`S-TC-PROFILE2`)
- [Vernacular Web 2 interview (artificial.dk)](http://www.artificial.dk/articles/olia.htm) (`S-LIALINA-VW2`)
