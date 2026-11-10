---
title: "Modern to retro mapping table"
description: "Every modern pattern and its period equivalent for presets B, C, and E."
generated: true
---

<!-- Generated from canon/ by scripts/build_derived.py. Do not edit by hand; edit canon and rebuild. -->

# Modern to retro mapping table

Translate component by component, not page by page. Every inventoried pattern gets a row decision: map, merge, or drop with a reason.

![Table mapping six modern patterns to their GeoCities, FrontPage, and MySpace equivalents, each with a period badge.](../../assets/figures/hs-05-component-mapping.svg)

*FIG HS-05. Translate component by component.*

| Modern pattern | B: GeoCities | C: FrontPage | E: MySpace | Tier |
|---|---|---|---|---|
| Hero section | Big centered WordArt title, an animated GIF, and Welcome to my homepage! | Splash page with logo and ENTER link, or a Flash-style intro with Skip Intro | Profile banner image plus a glitter display name | STATED |
| Sticky header or hamburger menu | Text links separated by pipes at top and bottom | Left shared border of theme buttons, or a left frame emulation | Thin network nav bar across the top | STATED |
| Mega-menu | A Site Map page | Image map navigation banner | Links typed into About Me | STATED |
| Cards or feature grid | Bulleted list with ball bullet GIFs | Two or three column table with border=1 and theme bullets | Interests table rows | STATED |
| Pricing table | Prices page with a bordered table | Catalog table with an Order Form that posts to mailto or Save Results | Details table rows | STATED |
| Testimonials | Guestbook entries such as Cool site!! | What Our Customers Say page with italic quotes | Comments wall with Thanks for the add graphics | STATED |
| Blog, changelog, or news | What's New log with dated entries and NEW graphics | Press Releases page with a Timestamp line | Blog or Bulletins box | STATED |
| Social icons | Webring box, an Email me graphic, and an ICQ number or AIM screen name | Contact Us feedback form | Contact table with Send Message, Add to Friends, and Instant Message | STATED |
| Analytics | Visible hit counter: You are visitor #004217 | Odometer hit counter, or a [Hit Counter] placeholder | Profile Views count | STATED |
| Cookie banner | Best viewed at 800x600 badge | This site uses frames or requires a newer browser notice | Dropped: profiles carried no equivalent | STATED |
| Newsletter signup | Join my mailing list form, or Sign my guestbook | Subscribe to our e-Newsletter form | Add to Friends | STATED |
| Site search | Search this site box, FreeFind style | Search component form | Network search bar | STATED |
| Product pages or shop | Photo, description, and price in a table | Catalog table with thumbnails linking to larger JPEGs | Dropped: list items in About Me instead | STATED |
| SaaS app or dashboard | Screenshots page of a desktop program window and a Download Now! (2.3 MB) link | Product Tour with numbered screenshots and a Free 30-Day Trial download | My Apps module | STATED |
| Login | Members Only password page | Registration component or login form in a gray table | Network login box | STATED |
| Chatbot or live chat | Chat Room link, or Leave a message on my ICQ | Live Help pop-up, or Email our Webmaster | Instant Message link in the contact table | STATED |
| Video | Click here to download (QuickTime, 4.1 MB) | Embedded media box with a player-style frame | Embedded video player box | STATED |
| Docs or help center | FAQ page with anchor links | Support section with a Table of Contents line | Dropped | STATED |
| FAQ accordion | FAQ page with Q: and A: pairs and a Back to top link | FAQ page with a numbered question list and bookmarks | Who I'd Like to Meet written as questions | INFERENCE |
| Dark mode | Black or starry background is already the default; add a text-only version link | Printer-friendly version link | Pick a dark user layout | STATED |
| Careers | Help Wanted! graphic | Employment Opportunities page | Dropped | STATED |
| Customer logo strip | Cool Sites I Like list or an 88x31 button wall | Our Clients bulleted list with small logo GIFs | Top 8 friends | INFERENCE |
| Footer | Last updated date, mailto, webring, award badges, and the counter | Copyright company Inc. All rights reserved, Webmaster line, and Best viewed with a browser badge | Network footer links | STATED |
| Accessibility statement | Text-only version link | Text-only version link | Text-only version link | STATED |

## Detection signals

Signals are case-insensitive regular expressions run by tools/survey.py. html signals match raw markup, text signals match visible text, href signals match link targets, script signals match script sources and inline script, css signals match style blocks and linked same-origin stylesheets.

| Pattern | Signals |
|---|---|
| Hero section | html: `<h1[\s>]` |
| Sticky header or hamburger menu | html: `<nav[\s>]`<br>html: `aria-label="[^"]*menu`<br>html: `<header[\s>]`<br>css: `position:\s*(sticky/fixed)` |
| Mega-menu | html: `<nav[^>]*>(?:(?!</nav>).){0,4000}<ul(?:(?!</nav>).){0,4000}<ul` |
| Cards or feature grid | html: `class="[^"]*(card/feature)[^"]*"`<br>css: `display:\s*grid` |
| Pricing table | html: `class="[^"]*pric`<br>text: `pricing`<br>text: `per month`<br>text: `/mo\b`<br>text: `per seat`<br>href: `/pricing` |
| Testimonials | html: `<blockquote`<br>html: `class="[^"]*(testimonial/review/quote)` |
| Blog, changelog, or news | text: `changelog`<br>text: `what's new`<br>text: `latest posts`<br>href: `/blog`<br>href: `/news`<br>href: `/changelog`<br>href: `/updates` |
| Social icons | href: `twitter\.com`<br>href: `x\.com/`<br>href: `linkedin\.com`<br>href: `facebook\.com`<br>href: `instagram\.com`<br>href: `youtube\.com`<br>href: `github\.com`<br>href: `tiktok\.com`<br>href: `threads\.net`<br>href: `bsky\.app` |
| Analytics | script: `googletagmanager`<br>script: `google-analytics`<br>script: `gtag\(`<br>script: `plausible`<br>script: `segment\.(com/io)`<br>script: `mixpanel`<br>script: `hotjar`<br>script: `posthog`<br>script: `amplitude` |
| Cookie banner | html: `class="[^"]*cookie`<br>html: `id="[^"]*cookie`<br>text: `we use cookies`<br>text: `accept all`<br>text: `cookie preferences`<br>script: `cookiebot`<br>script: `onetrust`<br>script: `cookieyes` |
| Newsletter signup | html: `type="email"`<br>text: `newsletter`<br>text: `subscribe` |
| Site search | html: `type="search"`<br>html: `role="search"`<br>href: `/search`<br>script: `algolia`<br>script: `docsearch` |
| Product pages or shop | text: `add to cart`<br>text: `buy now`<br>href: `/product`<br>href: `/shop`<br>href: `/store`<br>href: `/cart`<br>script: `shopify` |
| SaaS app or dashboard | text: `dashboard`<br>text: `start free trial`<br>text: `free trial`<br>href: `app\.`<br>href: `/dashboard`<br>href: `/signup`<br>href: `/register` |
| Login | html: `type="password"`<br>text: `log in`<br>text: `sign in`<br>href: `/login`<br>href: `/signin`<br>href: `/sign-in` |
| Chatbot or live chat | text: `chat with us`<br>script: `intercom`<br>script: `drift\.com`<br>script: `crisp\.chat`<br>script: `zendesk`<br>script: `tawk\.to`<br>script: `hs-scripts`<br>script: `livechat` |
| Video | html: `<video[\s>]`<br>html: `<iframe[^>]+(youtube/vimeo/wistia/loom)` |
| Docs or help center | text: `documentation`<br>text: `help center`<br>href: `/docs`<br>href: `/help`<br>href: `/support`<br>href: `docs\.` |
| FAQ accordion | html: `<details[\s>]`<br>html: `class="[^"]*(faq/accordion)`<br>text: `frequently asked`<br>text: `\bfaq\b` |
| Dark mode | html: `data-theme`<br>html: `class="[^"]*theme-toggle`<br>text: `dark mode`<br>css: `prefers-color-scheme` |
| Careers | text: `we're hiring`<br>text: `join our team`<br>href: `/careers`<br>href: `/jobs` |
| Customer logo strip | html: `alt="[^"]*logo`<br>text: `trusted by`<br>text: `used by` |
| Footer | html: `<footer[\s>]` |
| Accessibility statement | text: `accessibility`<br>href: `/accessibility` |
