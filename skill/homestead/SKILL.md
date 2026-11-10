---
name: homestead-retro-redesign
description: Analyze an existing modern website and redesign it as an old-school site from one web era (1990s GeoCities homepage, FrontPage corporate site, 2000s MySpace profile, and more). Use when asked to make a site look like Geocities, Angelfire, FrontPage, Dreamweaver, MySpace, the 90s web, or Y2K web, or for a retro, nostalgic, or vintage version of a website.
---

# HOMESTEAD: retro-web redesign

Turn a modern website into a convincing site from one earlier web era. The work is a translation, not a costume: lock one era, inventory the site, map every component, build in period markup, then audit it strictly.

If the BHIL-Homestead repository (https://github.com/PolymathWizard/BHIL-Homestead) is available, use its tools (`tools/survey.py`, `map.py`, `websafe.py`, `gifsmith.py`, `era_lint.py`, `gif_audit.py`, `rubric.py`) and kits. Without the repository, follow the same steps by hand with the tables below.

## Step 1: Intake

Ask only what changes the build, and ask before starting:

1. Which site (URL, or paste the HTML)?
2. Which era, or should you recommend one?
3. Purpose: client, portfolio, commentary, or internal? Does the requester own the brand?

Defaults when the person does not say: recommend the era, portfolio purpose, original assets only, and a footer line saying the page is an unofficial retro concept if the brand is not theirs.

## Step 2: Survey

Fetch the site and list: navigation items in order; patterns present (hero, sticky header, feature cards, pricing, testimonials, blog, social icons, analytics, cookie banner, newsletter, search, product pages, app or dashboard, login, chat widget, video, docs, FAQ, dark mode, careers, customer logos, footer); brand colors as hex; fonts; voice; and every fact, price, and call to action that must survive.

## Step 3: Lock one era

| Preset | Years | Pick for | Canvas | Palette | Fonts |
|---|---|---|---|---|---|
| A Proto-Web | 1993-1996 | Research, docs, academic | Fluid on gray | Browser default | Times, Courier |
| B GeoCities | 1995-2000 | Personal, creator, small shop | 600 px (760 for 1999-2000) | 216 web-safe | Times New Roman, Arial, Comic Sans MS |
| C FrontPage | 1997-2003 | Company, service, catalog, B2B | 760 px | Theme, web-safe flat art | Verdana, Book Antiqua, Impact |
| D Portal | 1999-2004 | Media, news, dense data | 760 px | Fuller color | Verdana 10-11px, Tahoma |
| E MySpace | 2004-2009 | Community, music, fashion, social | 800 px | Full color, black and pink, glitter | Verdana, Comic Sans MS |
| F Revival | 2013-now | Knowing tribute | Any | Deliberately retro | Retro or pixel fonts |

Never mix presets on one page unless the person asks for a story that spans eras (for example a 1998 page last updated in 2006).

## Step 4: Map every component

| Modern | B GeoCities | C FrontPage | E MySpace |
|---|---|---|---|
| Hero | WordArt title, animated GIF, Welcome to my homepage! | Splash page with ENTER, or Flash-style intro with Skip Intro | Banner image and glitter display name |
| Sticky header | Text links separated by pipes | Left shared border of beveled buttons | Network nav bar |
| Feature cards | Bulleted list with ball GIFs | Bordered table with theme bullets | Interests rows |
| Pricing | Prices table | Catalog table with Order Form | Details rows |
| Testimonials | Guestbook entries | What Our Customers Say | Comments with Thanks for the add |
| Blog or changelog | What's New with NEW graphics | Press Releases | Blog box |
| Social icons | Webring box, Email me, ICQ number | Contact Us form | Contact table |
| Analytics | Visible hit counter | Odometer counter or a [Hit Counter] placeholder | Profile Views |
| Cookie banner | Best viewed at 800x600 badge | This site requires a newer browser notice | Dropped |
| Newsletter | Join my mailing list | e-Newsletter form | Add to Friends |
| App or dashboard | Screenshot of a desktop program window and Download Now! | Product Tour with numbered screenshots and Free 30-Day Trial | My Apps box |
| Chat widget | ICQ number | Email our Webmaster | Instant Message link |
| Video | Download link with QuickTime size | Media player box | Video box |
| Customer logos | Button wall or Cool Sites list | Our Clients list | Top 8 friends |
| Footer | Last updated date, mailto, counter | Copyright, All rights reserved, Webmaster line | Network footer |

Cap navigation at five to eight items. Rewrite all copy in the era voice: B exuberant and personal; C brochure (Welcome to our Web site!); E lowercase and decorated. Keep every fact accurate. Remove modern phrases (get started, book a demo, seamless, AI-powered).

## Step 5: Assets

- Snap flat colors for presets A to C to the 216 web-safe colors: round each channel to 00, 33, 66, 99, CC, or FF.
- Make every image yourself: pixel WordArt titles, beveled buttons, 88x31 badges with generic text, odometer digits, rainbow rules, star tiles, glitter text. No third-party logos, characters, or mascots.
- Music only as an original or public-domain melody, click to play.

## Step 6: Build

Write period markup: table layouts at the canvas width, `font` tags, `center`, spacer GIFs, `bgcolor` attributes. For FrontPage add `webbot` comments and a GENERATOR meta tag; for MySpace keep default profile tables and paste a user `style` block inside About Me.

Never use flexbox, grid, rounded corners, blurred shadows, gradients, web fonts, SVG, emoji, or responsive breakpoints in presets A to E.

Every page must have:

1. A Safe Mode button that stops every marquee, blink, animation, and sound and switches to black text on white. It starts on when the visitor prefers reduced motion. Use the repo's `kits/safety-layer/` files when available.
2. Animated GIFs no faster than 340 ms per frame, with a still frame for Safe Mode.
3. No audio until a click.
4. Alt text on every image and a link to a text-only version.

Deliver the build as a self-contained HTML page (or a small set of pages) the person can open, plus a short list of the mapping decisions.

## Step 7: Audit strictly

Score 20 rows from 0 to 2 with one line of evidence each: era locked, canvas width, colors, fonts, layout look, images, widgets present, widgets era-correct, copy voice, navigation, brand legibility, content parity, View Source, lived-in details, browser badges, motion, audio, Safe Mode, accessibility, legal hygiene. SHIP at 34 or more; Safe Mode must score 2 and audio and motion at least 1. Fix rows below 2 before handing over, and report the final score honestly. Never call the build clean or perfect.
