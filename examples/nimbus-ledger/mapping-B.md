---
title: "Component mapping worksheet"
preset: "B"
generated_by: tools/map.py
---

# Component mapping: Nimbus Ledger as preset B (1998)

Canvas: 600 px. Confirm or override every decision. Allowed decisions: MAP, MERGE (name the target row), DROP (give a reason).

## Detected patterns

| Modern pattern | Evidence | Period equivalent | Widgets | Decision | Notes |
|---|---|---|---|---|---|
| Hero section | html:<h1[\s>] | Big centered WordArt title, an animated GIF, and Welcome to my homepage! | neighborhood-address | MAP | |
| Sticky header or hamburger menu | html:<nav[\s>]<br>html:aria-label="[^"]*menu<br>html:<header[\s>] | Text links separated by pipes at top and bottom | none | MAP | |
| Cards or feature grid | html:class="[^"]*(card|feature)[^"]*"<br>css:display:\s*grid | Bulleted list with ball bullet GIFs | none | MAP | |
| Pricing table | html:class="[^"]*pric<br>text:pricing<br>text:/mo\b | Prices page with a bordered table | none | MAP | |
| Testimonials | html:<blockquote<br>html:class="[^"]*(testimonial|review|quote) | Guestbook entries such as Cool site!! | guestbook | MAP | |
| Blog, changelog, or news | text:changelog<br>href:/blog<br>href:/changelog | What's New log with dated entries and NEW graphics | whats-new | MAP | |
| Social icons | href:x\.com/<br>href:linkedin\.com<br>href:instagram\.com | Webring box, an Email me graphic, and an ICQ number or AIM screen name | webring, email-me, aim-icq | MAP | |
| Analytics | script:googletagmanager<br>script:gtag\( | Visible hit counter: You are visitor #004217 | hit-counter | MAP | |
| Cookie banner | html:class="[^"]*cookie<br>html:id="[^"]*cookie<br>text:we use cookies | Best viewed at 800x600 badge | browser-badge | MAP | |
| Newsletter signup | html:type="email"<br>text:subscribe | Join my mailing list form, or Sign my guestbook | guestbook | MAP | |
| Product pages or shop | href:/product | Photo, description, and price in a table | none | MAP | |
| SaaS app or dashboard | text:start free trial<br>text:free trial<br>href:app\. | Screenshots page of a desktop program window and a Download Now! (2.3 MB) link | none | MAP | |
| Login | text:log in<br>text:sign in<br>href:/login | Members Only password page | none | MAP | |
| Chatbot or live chat | script:intercom | Chat Room link, or Leave a message on my ICQ | aim-icq | MAP | |
| Video | html:<iframe[^>]+(youtube|vimeo|wistia|loom) | Click here to download (QuickTime, 4.1 MB) | none | MAP | |
| Docs or help center | text:help center<br>href:/docs | FAQ page with anchor links | none | MAP | |
| FAQ accordion | html:<details[\s>]<br>html:class="[^"]*(faq|accordion)<br>text:frequently asked | FAQ page with Q: and A: pairs and a Back to top link | none | MAP | |
| Dark mode | html:data-theme<br>html:class="[^"]*theme-toggle<br>text:dark mode | Black or starry background is already the default; add a text-only version link | text-only-link, star-tile-bg | MAP | |
| Careers | text:we're hiring<br>href:/careers | Help Wanted! graphic | none | MAP | |
| Customer logo strip | html:alt="[^"]*logo<br>text:trusted by | Cool Sites I Like list or an 88x31 button wall | button-88x31 | MAP | |
| Footer | html:<footer[\s>] | Last updated date, mailto, webring, award badges, and the counter | last-updated, email-me, webring, hit-counter | MAP | |
| Accessibility statement | text:accessibility<br>href:/accessibility | Text-only version link | text-only-link | MAP | |

Not detected (check by eye before dropping): Mega-menu, Site search.

## Navigation plan

Source navigation: Product, Pricing, Customers, Blog, Docs, Careers, Log in, Get started.

Period navigation (cap applied): Product | Pricing | Customers | Blog | Docs | Careers | Log in | Get started.

## Required widget checklist

| Widget | Label | Supplied by | Placed on page |
|---|---|---|---|
| safe-mode-toggle | Safe Mode toggle | lived-in addition (no modern source) | |
| text-only-link | Text-only version link | Dark mode, Accessibility statement | |
| last-updated | Last updated stamp | Footer | |
| email-me | Email me graphic | Social icons, Footer | |
| browser-badge | Best viewed badge | Cookie banner | |
| hit-counter | Visible hit counter | Analytics, Footer | |
| guestbook | Guestbook | Testimonials, Newsletter signup | |
| webring | Webring box | Social icons, Footer | |
| under-construction | Under construction sign | lived-in addition (no modern source) | |
| rainbow-rule | Rainbow horizontal rule | lived-in addition (no modern source) | |
| neighborhood-address | Neighborhood address | Hero section | |
| whats-new | What's New log | Blog, changelog, or news | |
| midi-player | Click-to-play background music | lived-in addition (no modern source) | |

## Color plan (web-safe snap)

| Original | Snapped | Method | Delta E | Uses in source |
|---|---|---|---|---|
| #0F172A | #000000 | perceptual | 16.50 | 3 |
| #6D28D9 | #6600CC | perceptual | 7.58 | 2 |
| #0EA5E9 | #3399CC | perceptual | 10.36 | 1 |
| #10B981 | #00CC99 | per-channel | 7.88 | 1 |
| #F8FAFC | #FFFFFF | per-channel | 2.20 | 3 |
| #FFFFFF | #FFFFFF | per-channel | 0.00 | 2 |
| #E2E8F0 | #FFFFFF | perceptual | 9.43 | 1 |

## Font plan

| Source family | Category | Era stack |
|---|---|---|
| Inter | sans | Arial, Helvetica, sans-serif |
| JetBrains Mono | mono | Courier New, Courier, monospace |

## Copy deck seeds

Voice rules:

- Exuberant, personal, generous with exclamation points and capital letters.
- The founder speaks in first person about 'my program'.
- Shareware vocabulary: download, register, 30 day trial, by mail.
- Never use modern phrases such as get started, book a demo, or seamless.

| Source heading or CTA | Era rewrite |
|---|---|
| Bookkeeping that runs itself. | |
| Everything your books need. Nothing they don't. | |
| Invoices on autopilot | |
| Receipts, sorted | |
| Tax-ready in one click | |
| Freelancers love their books again | |
| Simple pricing | |
| Starter | |
| Pro | |
| Studio | |
| Frequently asked questions | |
| Get the Friday money memo | |
| Dark mode | |
| Get started | |
| Menu | |
| Start free trial | |
| Book a demo | |
| Subscribe | |
| Accept all | |
| Cookie preferences | |
