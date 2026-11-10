---
title: "Technical vocabulary"
description: "Period techniques, whether they still render, and how HOMESTEAD emulates them."
generated: true
---

<!-- Generated from canon/ by scripts/build_derived.py. Do not edit by hand; edit canon and rebuild. -->

# Technical vocabulary

| ID | Technique | Era | Renders today | Emulation | Claims |
|---|---|---|---|---|---|
| T01 | Table layouts, nested tables, cellpadding, cellspacing, bgcolor | 1996-2005 | yes | Use as-is. The single biggest authenticity signal. | none |
| T02 | Spacer GIFs (1x1 transparent, stretched with width and height) | 1996-2002 | yes | Use as-is. tools/gifsmith.py emits spacer.gif. | none |
| T03 | font face, size, and color attributes; center; b; i; u | 1995-2002 | yes | Use as-is. Obsolete but rendered. | none |
| T04 | body background, bgcolor, text, link, vlink, alink attributes | 1995-2003 | yes | Use as-is. | none |
| T05 | marquee | 1996-2008 | yes | Use, with the safety layer linked so Safe Mode can stop it. | [C-006](evidence-register.md#c-006) |
| T06 | blink | 1994-2000 | no | Keep the element in source. homestead-safe.css animates it at one cycle per second and stops it in Safe Mode and under reduced motion. | [C-007](evidence-register.md#c-007) |
| T07 | bgsound and embed with autostart MIDI | 1996-2002 | no autoplay | Keep the original line inside an HTML comment. Play a pre-rendered WAV of an original or public-domain tune only after a click. | [C-022](evidence-register.md#c-022) |
| T08 | Framesets | 1996-2001 | disputed | Do not ship real framesets. Emulate with fixed tables or iframes styled as panes. | [C-009](evidence-register.md#c-009) |
| T09 | Client-side image maps (map, area) | 1996-2003 | yes | Use as-is with alt text on every area. | none |
| T10 | Java applets (hover buttons, banner ad manager) | 1997-2001 | no | JavaScript image swap. A gray applet-loading box may stay as flavor. | [C-018](evidence-register.md#c-018), [C-019](evidence-register.md#c-019) |
| T11 | Flash intros with Skip Intro | 1998-2005 | no | HTML and CSS animation on a fixed 550 by 400 stage, or an original SWF through Ruffle. | [C-008](evidence-register.md#c-008) |
| T12 | JavaScript status bar scroller (window.status) | 1997-2001 | no | Period scroller that rotates text inside a form text field, paused in Safe Mode. | none |
| T13 | Cursor trails and falling snow DHTML | 1998-2003 | yes | Use, disabled in Safe Mode and under prefers-reduced-motion. | none |
| T14 | webbot comments, GENERATOR meta tags, _vti_cnf folders | 1997-2003 | source only | Include in source for View Source authenticity. | [C-017](evidence-register.md#c-017), [C-018](evidence-register.md#c-018) |
| T15 | User CSS pasted into a profile field | 2004-2009 | yes | A style block placed inside the About Me cell that overrides the default profile tables with !important. | [C-020](evidence-register.md#c-020), [C-039](evidence-register.md#c-039) |
