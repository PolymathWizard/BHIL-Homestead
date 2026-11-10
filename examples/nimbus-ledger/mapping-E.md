---
title: "Component mapping worksheet"
preset: "E"
generated_by: tools/map.py
---

# Component mapping: Nimbus Ledger as preset E (2007)

Canvas: 800 px. Confirm or override every decision. Allowed decisions: MAP, MERGE (name the target row), DROP (give a reason).

## Detected patterns

| Modern pattern | Evidence | Period equivalent | Widgets | Decision | Notes |
|---|---|---|---|---|---|
| Hero section | html:<h1[\s>] | Profile banner image plus a glitter display name | glitter-text | MAP | |
| Sticky header or hamburger menu | html:<nav[\s>]<br>html:aria-label="[^"]*menu<br>html:<header[\s>] | Thin network nav bar across the top | none | MAP | |
| Cards or feature grid | html:class="[^"]*(card|feature)[^"]*"<br>css:display:\s*grid | Interests table rows | interests-details | MAP | |
| Pricing table | html:class="[^"]*pric<br>text:pricing<br>text:/mo\b | Details table rows | interests-details | MAP | |
| Testimonials | html:<blockquote<br>html:class="[^"]*(testimonial|review|quote) | Comments wall with Thanks for the add graphics | comments-wall | MAP | |
| Blog, changelog, or news | text:changelog<br>href:/blog<br>href:/changelog | Blog or Bulletins box | none | MAP | |
| Social icons | href:x\.com/<br>href:linkedin\.com<br>href:instagram\.com | Contact table with Send Message, Add to Friends, and Instant Message | contact-table | MAP | |
| Analytics | script:googletagmanager<br>script:gtag\( | Profile Views count | profile-views | MAP | |
| Cookie banner | html:class="[^"]*cookie<br>html:id="[^"]*cookie<br>text:we use cookies | Dropped: profiles carried no equivalent | none | DROP | |
| Newsletter signup | html:type="email"<br>text:subscribe | Add to Friends | contact-table | MAP | |
| Product pages or shop | href:/product | Dropped: list items in About Me instead | none | DROP | |
| SaaS app or dashboard | text:start free trial<br>text:free trial<br>href:app\. | My Apps module | none | MAP | |
| Login | text:log in<br>text:sign in<br>href:/login | Network login box | none | MAP | |
| Chatbot or live chat | script:intercom | Instant Message link in the contact table | contact-table | MAP | |
| Video | html:<iframe[^>]+(youtube|vimeo|wistia|loom) | Embedded video player box | none | MAP | |
| Docs or help center | text:help center<br>href:/docs | Dropped | none | DROP | |
| FAQ accordion | html:<details[\s>]<br>html:class="[^"]*(faq|accordion)<br>text:frequently asked | Who I'd Like to Meet written as questions | profile-blurbs | MAP | |
| Dark mode | html:data-theme<br>html:class="[^"]*theme-toggle<br>text:dark mode | Pick a dark user layout | user-css-layout | MAP | |
| Careers | text:we're hiring<br>href:/careers | Dropped | none | DROP | |
| Customer logo strip | html:alt="[^"]*logo<br>text:trusted by | Top 8 friends | top-8 | MAP | |
| Footer | html:<footer[\s>] | Network footer links | none | MAP | |
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
| user-css-layout | User CSS layout | Dark mode | |
| profile-blurbs | Profile blurbs | FAQ accordion | |
| interests-details | Interests and Details tables | Cards or feature grid, Pricing table | |
| contact-table | Contact table | Social icons, Newsletter signup, Chatbot or live chat | |
| top-8 | Top 8 friends | Customer logo strip | |
| comments-wall | Comments wall | Testimonials | |
| profile-music-player | Profile song player | lived-in addition (no modern source) | |
| glitter-text | Glitter text | Hero section | |
| blinkies | Blinkies | lived-in addition (no modern source) | |
| online-now | Online Now indicator | lived-in addition (no modern source) | |
| profile-views | Profile views count | Analytics | |

## Font plan

| Source family | Category | Era stack |
|---|---|---|
| Inter | sans | Verdana, Arial, sans-serif |
| JetBrains Mono | mono | Courier New, Courier, monospace |

## Copy deck seeds

Voice rules:

- A 2007 brand trying very hard to be a person: decorated punctuation, lowercase, inside jokes.
- Customers appear as friends; testimonials appear as comments.
- Never quote real song lyrics; the profile song is an original track.
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
