---
title: "Component mapping worksheet"
preset: "C"
generated_by: tools/map.py
---

# Component mapping: Nimbus Ledger as preset C (2001)

Canvas: 760 px. Confirm or override every decision. Allowed decisions: MAP, MERGE (name the target row), DROP (give a reason).

## Detected patterns

| Modern pattern | Evidence | Period equivalent | Widgets | Decision | Notes |
|---|---|---|---|---|---|
| Hero section | html:<h1[\s>] | Splash page with logo and ENTER link, or a Flash-style intro with Skip Intro | splash-page, theme-banner | MAP | |
| Sticky header or hamburger menu | html:<nav[\s>]<br>html:aria-label="[^"]*menu<br>html:<header[\s>] | Left shared border of theme buttons, or a left frame emulation | shared-borders, hover-buttons | MAP | |
| Cards or feature grid | html:class="[^"]*(card|feature)[^"]*"<br>css:display:\s*grid | Two or three column table with border=1 and theme bullets | none | MAP | |
| Pricing table | html:class="[^"]*pric<br>text:pricing<br>text:/mo\b | Catalog table with an Order Form that posts to mailto or Save Results | feedback-form | MAP | |
| Testimonials | html:<blockquote<br>html:class="[^"]*(testimonial|review|quote) | What Our Customers Say page with italic quotes | none | MAP | |
| Blog, changelog, or news | text:changelog<br>href:/blog<br>href:/changelog | Press Releases page with a Timestamp line | whats-new, last-updated | MAP | |
| Social icons | href:x\.com/<br>href:linkedin\.com<br>href:instagram\.com | Contact Us feedback form | feedback-form | MAP | |
| Analytics | script:googletagmanager<br>script:gtag\( | Odometer hit counter, or a [Hit Counter] placeholder | hit-counter, broken-component-placeholder | MAP | |
| Cookie banner | html:class="[^"]*cookie<br>html:id="[^"]*cookie<br>text:we use cookies | This site uses frames or requires a newer browser notice | frames-notice, browser-badge | MAP | |
| Newsletter signup | html:type="email"<br>text:subscribe | Subscribe to our e-Newsletter form | feedback-form | MAP | |
| Product pages or shop | href:/product | Catalog table with thumbnails linking to larger JPEGs | none | MAP | |
| SaaS app or dashboard | text:start free trial<br>text:free trial<br>href:app\. | Product Tour with numbered screenshots and a Free 30-Day Trial download | none | MAP | |
| Login | text:log in<br>text:sign in<br>href:/login | Registration component or login form in a gray table | none | MAP | |
| Chatbot or live chat | script:intercom | Live Help pop-up, or Email our Webmaster | mailto-text | MAP | |
| Video | html:<iframe[^>]+(youtube|vimeo|wistia|loom) | Embedded media box with a player-style frame | none | MAP | |
| Docs or help center | text:help center<br>href:/docs | Support section with a Table of Contents line | none | MAP | |
| FAQ accordion | html:<details[\s>]<br>html:class="[^"]*(faq|accordion)<br>text:frequently asked | FAQ page with a numbered question list and bookmarks | none | MAP | |
| Dark mode | html:data-theme<br>html:class="[^"]*theme-toggle<br>text:dark mode | Printer-friendly version link | printer-friendly-link | MAP | |
| Careers | text:we're hiring<br>href:/careers | Employment Opportunities page | none | MAP | |
| Customer logo strip | html:alt="[^"]*logo<br>text:trusted by | Our Clients bulleted list with small logo GIFs | none | MAP | |
| Footer | html:<footer[\s>] | Copyright company Inc. All rights reserved, Webmaster line, and Best viewed with a browser badge | copyright-footer, mailto-text, browser-badge | MAP | |
| Accessibility statement | text:accessibility<br>href:/accessibility | Text-only version link | text-only-link | MAP | |

Not detected (check by eye before dropping): Mega-menu, Site search.

## Navigation plan

Source navigation: Product, Pricing, Customers, Blog, Docs, Careers, Log in, Get started.

Period navigation (cap applied): Product | Pricing | Customers | Blog | Docs | Careers | Log in | Get started.

## Required widget checklist

| Widget | Label | Supplied by | Placed on page |
|---|---|---|---|
| safe-mode-toggle | Safe Mode toggle | lived-in addition (no modern source) | |
| text-only-link | Text-only version link | Accessibility statement | |
| last-updated | Last updated stamp | Blog, changelog, or news | |
| mailto-text | Plain mailto footer | Chatbot or live chat, Footer | |
| browser-badge | Best viewed badge | Cookie banner, Footer | |
| shared-borders | Shared borders | Sticky header or hamburger menu | |
| theme-banner | Theme page banner | Hero section | |
| hover-buttons | Hover button navigation | Sticky header or hamburger menu | |
| search-form | Search this site form | lived-in addition (no modern source) | |
| feedback-form | Feedback form | Pricing table, Social icons, Newsletter signup | |
| copyright-footer | Corporate copyright footer | Footer | |
| whats-new | What's New log | Blog, changelog, or news | |
| hit-counter or broken-component-placeholder | one of these | pick one | |

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
| Inter | sans | Verdana, Arial, Helvetica, sans-serif |
| JetBrains Mono | mono | Courier New, Courier, monospace |

## Copy deck seeds

Voice rules:

- Small-business formal with a hint of brochure.
- The company speaks as we; the product is Nimbus Ledger Professional 2001.
- Boxed software vocabulary: edition, free 30-day trial, order form, CD-ROM.
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
