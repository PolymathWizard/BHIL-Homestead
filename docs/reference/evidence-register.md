---
title: "Evidence register"
description: "Every factual claim HOMESTEAD relies on, with its evidence tier and sources."
generated: true
---

<!-- Generated from canon/ by scripts/build_derived.py. Do not edit by hand; edit canon and rebuild. -->

# Evidence register

Claims were compiled from a November 2026 research pass (REF HOMESTEAD-001). No claim is marked VERIFIED because no primary artifact was re-checked at build time. Promote a claim only with a commit that records what was checked.

## Tiers

- **VERIFIED**: Checked directly against a primary artifact by the maintainer.
- **CORROBORATED**: Two or more independent sources agree.
- **STATED**: A single credible source states it.
- **UNCORROBORATED**: Only a weak, secondary, or retrospective source supports it, or sources disagree.
- **INFERENCE**: HOMESTEAD reasoning built on the cited claims. Treat as design guidance, not fact.

## Claims

### C-001

**STATED.** In January 2000 W3Schools logged 800x600 at 56 percent of visitors, 1024x768 at 25 percent, and lower resolutions at 15 percent; 12 percent still ran 256 colors. The audience skews toward developers, so treat these as an upper bound on screen size.

Sources: [W3Schools browser display statistics (mirror)](http://www-db.deis.unibo.it/courses/TW/DOCS/w3schools/browsers/browsers_display.asp.html).

### C-002

**STATED.** By January 2004 W3Schools logged 1024x768 at 47 percent and 800x600 at 37 percent.

Sources: [W3Schools browser display statistics (mirror)](http://www-db.deis.unibo.it/courses/TW/DOCS/w3schools/browsers/browsers_display.asp.html).

### C-003

**CORROBORATED.** The 216 web-safe colors are every combination of 00, 33, 66, 99, CC, and FF across red, green, and blue, shipped for 8-bit displays where the operating system reserved 40 colors.

Sources: [Programming Web Graphics, chapter 2.4 (O'Reilly)](https://www.oreilly.com/library/view/programming-web-graphics/1565924789/ch02s04.html); [Web safe colors (colortable.org)](https://colortable.org/web-safe/); [Web safe colors (ColorSlurp blog)](https://colorslurp.com/blog/web-safe-colors).

### C-004

**STATED.** Period guidance held that the browser-safe palette suits flat illustrations and logos but should not be used to remap color photographs.

Sources: [Digital History, hex color reading 4.22a (George Mason University)](https://chnm.gmu.edu/digitalhistory/links/pdf/chapter4/4.22a.pdf).

### C-005

**STATED.** Only 22 of the 216 web-safe colors displayed reliably on 16-bit screens (Lehn and Stern). HOMESTEAD does not ship that sub-palette until the list is checked against the primary source.

Sources: [Digital History, hex color reading 4.22a (George Mason University)](https://chnm.gmu.edu/digitalhistory/links/pdf/chapter4/4.22a.pdf).

### C-006

**STATED.** The marquee element is obsolete in the HTML specification but still implemented by current browsers.

Sources: [Deadhead rules: marquee element](https://deadhead.cevdet.ch/rules/element/marquee).

### C-007

**STATED.** The blink element does nothing in current browsers. Firefox, the last browser to blink, removed it in version 23 (2013); it maps to HTMLUnknownElement.

Sources: [Deadhead rules: blink element](https://deadhead.cevdet.ch/rules/element/blink).

### C-008

**STATED.** Adobe ended Flash Player support on December 31, 2020 and blocked Flash content from January 12, 2021.

Sources: [SWF player notes on Flash end of life (Amara Software)](https://amarasoftware.com/swf-player/).

### C-009

**UNCORROBORATED.** The research pass reported that frameset documents are no longer supported. This conflicts with the HTML standard still describing frameset rendering. HOMESTEAD emulates frames for linkability, accessibility, and mobile reasons regardless of browser support.

Sources: none retrieved. See the tier note.

### C-010

**STATED.** GeoCities was founded in November 1994 by David Bohnett and John Rezner as Beverly Hills Internet and from mid-1995 gave Homesteaders free pages of 2 MB in themed neighborhoods.

Sources: [GeoCities (Wikipedia)](https://en.wikipedia.org/wiki/GeoCities).

### C-011

**CORROBORATED.** Neighborhood names were part of the page address. Examples include Area51, Athens, BourbonStreet, Broadway, CapitolHill, Hollywood, Paris, Petsburgh, and SiliconValley.

Sources: [GeoCities (Wikipedia)](https://en.wikipedia.org/wiki/GeoCities); [GeoCities (Website Wiki)](https://website.fandom.com/wiki/GeoCities).

### C-012

**STATED.** Yahoo acquired GeoCities on January 28, 1999, announced closure on April 23, 2009, and ended the United States service on October 26, 2009.

Sources: [GeoCities (Wikipedia)](https://en.wikipedia.org/wiki/GeoCities).

### C-013

**STATED.** There were over 38 million GeoCities pages when the United States service shut down.

Sources: [Beat your eyeballs to death with this majestic GeoCities tribute (VICE)](https://www.vice.com/en/article/beat-your-eyeballs-to-death-with-this-majestic-geocities-tribute/).

### C-014

**CORROBORATED.** The amateur web of the 1990s is catalogued by starry tiled backgrounds, animated Under Construction signs, rainbow rules, Mail Me envelopes, MIDI background music, and collections of animated GIFs.

Sources: [A Vernacular Web, excerpts (Olia Lialina)](https://www.andorgallery.com/shows/images/vernacular_web_excerpts.pdf); [Vernacular web notes (dev.null.org)](http://dev.null.org/blog/item/200709090120_vernweb).

### C-015

**STATED.** FrontPage 98 shipped named themes including Arcs, Artsy, Automotive, Barcode, Bars, Blends, Blocks, Blueprint, Bubbles, Cactus, Expedition, and Sumi Painting.

Sources: [FrontPage 98 themes help document (help archive)](https://helparchive.huntertur.net/document/16630).

### C-016

**STATED.** Microsoft announced FrontPage 2000 with 10 new business-ready themes among more than 60 professionally designed themes.

Sources: [Microsoft unveils new FrontPage 2000 (Microsoft, 1998)](https://news.microsoft.com/source/1998/09/30/microsoft-unveils-new-frontpage-2000-broad-new-feature-set-delivers-a-breakthrough-in-ease-of-use/).

### C-017

**STATED.** FrontPage components included Annotation, Categories, Confirmation Field, Discussion, Hit Counter, Include, Registration, Save Results, Scheduled Image, Scheduled Include, Search, Substitution, Table of Contents, Timestamp, and Validation.

Sources: [FrontPage WebBot components (Microsoft Learn, previous versions)](https://learn.microsoft.com/en-us/previous-versions/office/developer/sharepoint-2010/ms464803(v=office.14)).

### C-018

**STATED.** Shared borders lived in _borders, hover buttons and the banner ad manager were Java applets kept in _fpclass, and the hit counter needed server extensions on the host.

Sources: [Special files and directories maintained by FrontPage (Softpanorama)](https://softpanorama.org/Office/Frontpage/special_files_and_directories_maintained_by_frontpage.shtml); [FrontPage hit counter thread (Office Forums)](https://www.office-forums.com/threads/frontpage-hit-counter.2070685/).

### C-019

**STATED.** Experienced FrontPage users of the period advised against Java hover buttons because visitors without a Java VM saw no buttons, and recommended image swaps instead.

Sources: [FrontPage hover button advice (help archive)](https://helparchive.huntertur.net/document/16583).

### C-020

**STATED.** MySpace allowed HTML but not JavaScript in profile fields, so layouts were CSS blocks pasted into About Me that restyled the default tables.

Sources: [Blogs: MySpace (Wikibooks mirror)](https://www.englishgratis.com/1/wikibooks/blogs/myspace.htm).

### C-021

**STATED.** WCAG 2.3.1 forbids more than three flashes in any one second unless below thresholds, and estimates the 10 degree visual field as a 341 x 256 pixel rectangle at 1024 x 768.

Sources: [Understanding SC 2.3.1 three flashes or below threshold (Digital A11Y)](https://www.digitala11y.com/understanding-sc-2-3-1-three-flashes-or-below-threshold/).

### C-022

**STATED.** WCAG 1.4.2 requires a pause, stop, or volume mechanism for any audio that plays automatically for more than 3 seconds.

Sources: [Understanding audio control, SC 1.4.2 (W3C)](https://www.w3.org/WAI/WCAG20/Understanding/audio-control).

### C-023

**CORROBORATED.** MySpace began testing the drag-and-drop Profile 2.0 editor in October 2008 and rolled it out optionally in November 2008.

Sources: [MySpace launches Profile 2.0 (TechCrunch, 2008)](https://techcrunch.com/2008/10/26/myspace-launches-profile-20-with-drag-and-drop-interface/); [MySpace upgrades itself to Profile 2.0 (BetaNews)](https://betanews.com/article/myspace-upgrades-itself-to-profile-2-0/).

### C-024

**STATED.** In the later profile-based amateur web, glitter replaced stars as the signature decoration.

Sources: [Vernacular Web 2 interview (artificial.dk)](http://www.artificial.dk/articles/olia.htm).

### C-025

**UNCORROBORATED.** Top Friends was originally limited to eight and later allowed between 4 and 24, while the name Top 8 stuck.

Sources: [What was MySpace Top 8 (Knowledge Nuts)](https://knowledgenuts.com/2026/08/06/what-was-myspace-top-8-and-why-important/).

### C-026

**STATED.** MySpace peaked in the United States at 75.9 million monthly unique visitors in December 2008 (comScore).

Sources: [MySpace stats then and now (Expanded Ramblings)](https://expandedramblings.com/index.php/myspace-stats-then-now/).

### C-027

**CORROBORATED.** GifCities indexes over 4.5 million GeoCities GIFs, launched in 2016, and gained semantic search and size filters in June 2025.

Sources: [GifCities: the GeoCities animated GIF search engine (Internet Archive blog, 2016)](https://blog.archive.org/2016/11/01/gifcities-the-geocities-animated-gif-search-engine/); [Keep on GIFin: a new version of GifCities (Internet Archive blog, 2025)](https://blog.archive.org/2025/06/09/keep-on-gifin-a-new-version-of-gifcities-internet-archives-geocities-animated-gif-search-engine/); [The Internet Archive modernizes its GeoCities GIF search engine (Engadget)](https://www.engadget.com/entertainment/the-internet-archive-modernizes-its-geocities-gif-search-engine-192315963.html).

### C-028

**CORROBORATED.** The 1996 Space Jam website remains online and is the canonical surviving studio site of the era.

Sources: [Space Jam original 1996 website still active (Pedestrian)](https://www.pedestrian.tv/online/space-jam-original-1996-website-active/); [Space Jam forever: the website that would not die (Rolling Stone)](https://www.rollingstone.com/tv-movies/tv-movie-news/space-jam-forever-the-website-that-wouldnt-die-70507/).

### C-029

**STATED.** Neocities launched on June 28, 2013 and passed one million sites on February 10, 2025.

Sources: [Neocities (Wikipedia)](https://en.wikipedia.org/wiki/Neocities).

### C-030

**UNCORROBORATED.** Early browsers rendered unstyled pages on a gray background close to C0C0C0. Source is research synthesis only.

Sources: none retrieved. See the tier note.

### C-031

**CORROBORATED.** The Core fonts for the Web were redistributable only in their original installer packages and were never licensed for web embedding.

Sources: [Core fonts for the Web (Wikipedia)](https://en.wikipedia.org/wiki/Core_fonts_for_the_Web); [Core fonts FAQ (SourceForge)](https://corefonts.sourceforge.net/faq8.htm).

### C-032

**STATED.** Comic Sans webfont licensing is sold separately.

Sources: [Comic Sans licenses (Fonts.com)](https://www.fonts.com/font/microsoft-corporation/comic-sans/licenses).

### C-033

**STATED.** An existing agent skill converts a landing page into a FrontPage 97, 98, or 2000 style site with themes and components.

Sources: [ms-frontpage-visual-skill (jamarks, GitHub)](https://github.com/jamarks/ms-frontpage-visual-skill).

### C-034

**CORROBORATED.** web98 uses a language model to render any address as if it were 1996. Useful for ideation, prone to invented period details.

Sources: [web98 (Nate Parrott, GitHub)](https://github.com/nate-parrott/web98); [web98 write-up (Glance)](https://www.glance.fyi/blog/web98).

### C-035

**CORROBORATED.** A 2021 concept set reimagined popular apps as 1990s websites as static mockups.

Sources: [Web designers reimagine popular apps as 90s websites (Digital Information World)](https://www.digitalinformationworld.com/2021/08/web-designers-reimagine-popular-apps-as-90s-websites.html); [Popular websites remade 90s style (Bored Panda)](https://www.boredpanda.com/popular-website-remade-90s-style-zyro/).

### C-036

**STATED.** 98.css recreates Windows 98 interface chrome from semantic HTML without JavaScript. It styles operating system chrome, not web pages.

Sources: [98.css](https://jdan.github.io/98.css/).

### C-037

**STATED.** Cameron's World is a 2015 web collage of GIFs and text from archived GeoCities pages.

Sources: [Beat your eyeballs to death with this majestic GeoCities tribute (VICE)](https://www.vice.com/en/article/beat-your-eyeballs-to-death-with-this-majestic-geocities-tribute/).

### C-038

**STATED.** One Terabyte of Kilobyte Age posts screenshots of restored GeoCities pages rendered in period browsers.

Sources: [Authenticity, access, and digital preservation of GeoCities (Rhizome)](https://rhizome.org/editorial/2014/feb/10/authenticity-access-digital-preservation-geocities/).

### C-039

**CORROBORATED.** Profile layout generators exposed background color and image, tiling, font family and size, text and link colors, table background, and border width, style, and color.

Sources: [MySpace layout generator (Quackit)](https://www.quackit.com/myspace/myspace_code_generators/myspace_layout_generator.cfm); [Fillster layout codes](https://www.fillster.com/layout2codes/326.html); [JellyMuffin glitter layouts](https://www.jellymuffin.com/layouts/Glitter/).

### C-040

**STATED.** A profile carried About Me, Who I'd Like to Meet, Interests, a Details table, a contact table, a friends grid, and a comments wall.

Sources: [Blogs: MySpace (Wikibooks mirror)](https://www.englishgratis.com/1/wikibooks/blogs/myspace.htm).

### C-041

**INFERENCE.** Design to 600 to 620 px of content for 1996 to 1998 and 760 px for 1999 to 2003.

Sources: [W3Schools browser display statistics (mirror)](http://www-db.deis.unibo.it/courses/TW/DOCS/w3schools/browsers/browsers_display.asp.html).

### C-042

**INFERENCE.** Period markup with a thin modern safety layer passes View Source scrutiny and leaks fewer spacing and typography tells than a modern framework styled to look old.

Sources: none retrieved. See the tier note.

### C-043

**INFERENCE.** A minimum frame delay of 340 ms for animated GIFs keeps two-frame alternation at about half the WCAG flash limit.

Sources: [Understanding SC 2.3.1 three flashes or below threshold (Digital A11Y)](https://www.digitala11y.com/understanding-sc-2-3-1-three-flashes-or-below-threshold/).

## Reference resources

- [98.css](https://jdan.github.io/98.css/) (`S-98CSS`)
- [XP.css](https://botoxparty.github.io/XP.css/) (`S-XPCSS`)
- [7.css](https://khang-nd.github.io/7.css/) (`S-7CSS`)
- [retro-css list (GitHub)](https://github.com/matt-auckland/retro-css) (`S-RETRO-CSS`)
- [Wayback Machine (Internet Archive)](https://web.archive.org) (`S-WAYBACK`)
- [GifCities](https://gifcities.org) (`S-GIFCITIES`)
- [Restorativland GeoCities Gallery](https://geocities.restorativland.org) (`S-RESTORATIVLAND`)
- [One Terabyte of Kilobyte Age (GeoCities Research Institute blog)](https://blog.geocities.institute) (`S-OOKA`)
- [Cameron's World](https://www.cameronsworld.net) (`S-CAMERONSWORLD`)
- [Space Jam (1996 site)](https://www.spacejam.com/1996/) (`S-SPACEJAM`)
- [A Vernacular Web essays (Olia Lialina)](http://art.teleportacia.org/observation/vernacular/) (`S-LIALINA-ESSAYS`)
- [Neocities](https://neocities.org/) (`S-NEOCITIES`)
- [Ruffle Flash emulator](https://ruffle.rs) (`S-RUFFLE`)
