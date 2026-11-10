---
title: "Widget registry"
description: "Every period widget, its marker, and the presets it belongs to."
generated: true
---

<!-- Generated from canon/ by scripts/build_derived.py. Do not edit by hand; edit canon and rebuild. -->

# Widget registry

Mark each widget in the build with `<!-- hs:widget ID -->`. The lint reads the markers to check required widgets and to catch era mixing.

| ID | Widget | A | B | C | D | E | F | Description |
|---|---|---|---|---|---|---|---|---|
| `safe-mode-toggle` | Safe Mode toggle | yes | yes | yes | yes | yes | yes | Persistent control that pauses animation, stops marquees, mutes audio, and raises contrast. Provided by the safety layer and required on every build. |
| `text-only-link` | Text-only version link | yes | yes | yes | yes | yes | yes | A plain link to a stripped, high-contrast version of the page. Period-correct and the main accessibility escape hatch. |
| `last-updated` | Last updated stamp | yes | yes | yes | yes |  | yes | A hand-typed or Timestamp-component date such as Last updated 3/14/98. |
| `mailto-text` | Plain mailto footer | yes |  | yes | yes |  |  | An address element or webmaster line with a mailto link. |
| `email-me` | Email me graphic |  | yes |  |  |  | yes | An animated or static Email Me graphic wrapped in a mailto link. |
| `browser-badge` | Best viewed badge | yes | yes | yes | yes |  |  | Best viewed with a named browser at a named resolution. Use generic text or an original badge for client work. |
| `hit-counter` | Visible hit counter |  | yes | yes | yes |  | yes | Odometer digits such as You are visitor #004217. |
| `guestbook` | Guestbook |  | yes | yes |  |  | yes | Sign my guestbook page with dated visitor entries. Replaces testimonials. |
| `webring` | Webring box |  | yes |  |  |  | yes | Bordered table with previous, next, random, and list links for a themed ring. |
| `under-construction` | Under construction sign |  | yes | yes |  |  | yes | Construction sign on unfinished sections. On FrontPage sites usually a single small GIF on a stub page. |
| `rainbow-rule` | Rainbow horizontal rule |  | yes |  |  |  | yes | A GIF divider used in place of the hr element. |
| `star-tile-bg` | Starry tiled background |  | yes |  |  |  | yes | Black, dark blue, or purple tile scattered with stars. |
| `neighborhood-address` | Neighborhood address |  | yes |  |  |  |  | A themed homestead address such as SiliconValley/Heights/4021 matching the site topic. |
| `whats-new` | What's New log |  | yes | yes |  |  | yes | Dated update log with NEW graphics. On corporate sites it becomes Press Releases or News. |
| `midi-player` | Click-to-play background music |  | yes | yes |  |  | yes | A Turn on music control that plays a pre-rendered MIDI-style track only after a click. |
| `splash-page` | Splash or Enter page |  | yes | yes | yes |  |  | Logo plus an ENTER link before the real home page. |
| `cursor-trail` | Cursor trail |  | yes | yes |  |  |  | DHTML sparkle or dot trail following the pointer. Disabled in Safe Mode. |
| `aim-icq` | Instant messenger handle |  | yes |  | yes | yes |  | ICQ number or AIM screen name in place of chat or social links. |
| `button-88x31` | 88x31 button wall |  | yes |  |  |  | yes | A cluster of 88 by 31 pixel link buttons for friends, tools, and causes. |
| `status-bar-scroller` | Status bar or text box scroller |  | yes | yes |  |  |  | Scrolling message, faked in a form text field or a styled status strip because browsers ignore window.status. |
| `shared-borders` | Shared borders |  |  | yes |  |  |  | FrontPage-style top, left, and bottom regions repeated on every page. |
| `theme-banner` | Theme page banner |  |  | yes |  |  |  | A themed banner graphic carrying the page title, generated per page. |
| `hover-buttons` | Hover button navigation |  |  | yes |  |  |  | Beveled nav buttons with a hover state, rebuilt as image swaps the way careful developers did after Java applets failed. |
| `search-form` | Search this site form |  | yes | yes | yes |  |  | A small search form, FreeFind style on personal pages or the Search component on corporate pages. |
| `feedback-form` | Feedback form |  |  | yes | yes |  |  | Contact Us form with name, email, comments, and a gray Submit button. |
| `copyright-footer` | Corporate copyright footer |  |  | yes | yes |  |  | Copyright, company, All rights reserved, and a Webmaster mailto. |
| `printer-friendly-link` | Printer-friendly link |  |  | yes | yes |  |  | Printer-friendly version link, the period answer to alternate color schemes. |
| `broken-component-placeholder` | Broken component placeholder |  |  | yes |  |  |  | A bracketed placeholder such as [Hit Counter] shown when a host lacked server extensions. A lived-in detail. |
| `frames-notice` | Frames or browser notice |  | yes | yes |  |  |  | This site uses frames or requires a newer browser notice, the period equivalent of a cookie banner. |
| `banner-ad-manager` | Rotating banner ad |  |  | yes | yes |  |  | 468 by 60 rotating banner, originally a Java applet, rebuilt as an image swap. |
| `flash-intro` | Flash-style intro |  |  | yes | yes |  |  | Fixed 550 by 400 stage with an animated intro and Skip Intro link, rebuilt in HTML and CSS. |
| `web-portal-modules` | Portal modules |  |  |  | yes |  |  | Weather, stocks, headlines, and My Page style boxes in a three-column table. |
| `user-css-layout` | User CSS layout |  |  |  |  | yes |  | A pasted style block that restyles the default profile tables. The layering is the point. |
| `profile-blurbs` | Profile blurbs |  |  |  |  | yes |  | About Me and Who I'd Like to Meet sections. |
| `interests-details` | Interests and Details tables |  |  |  |  | yes |  | Interests rows and a Details table with status, hometown, and similar fields. |
| `contact-table` | Contact table |  |  |  |  | yes |  | Send Message, Add to Friends, Instant Message, and similar actions in a grid. |
| `top-8` | Top 8 friends |  |  |  |  | yes |  | Grid of eight friend avatars with names. Replaces customer logo strips. |
| `comments-wall` | Comments wall |  |  |  |  | yes |  | Friend comments with avatars, timestamps, and graphics such as Thanks for the add. |
| `profile-music-player` | Profile song player |  |  |  |  | yes |  | Small player box for the profile song, click to play only. |
| `glitter-text` | Glitter text |  |  |  |  | yes | yes | Sparkling animated text graphic for the display name or headings. |
| `blinkies` | Blinkies |  |  |  |  | yes | yes | Small 150 by 20 animated text strips that declare likes and moods. |
| `online-now` | Online Now indicator |  |  |  |  | yes |  | Small Online Now graphic next to the profile photo. |
| `profile-views` | Profile views count |  |  |  |  | yes |  | Profile Views count in plain text, the profile era replacement for the hit counter. |
| `custom-cursor` | Custom cursor |  |  |  |  | yes |  | Custom cursor image set through user CSS. |
