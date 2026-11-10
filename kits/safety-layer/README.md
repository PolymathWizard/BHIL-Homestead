---
title: "Safety layer"
description: "Safe Mode, blink emulation, and click-to-play audio shipped next to every HOMESTEAD page."
---

# Safety layer

Two small files that make period pages safe for 2026 visitors without changing how they look by default. They are modern by design and exempt from the era lint ([ADR-003](../../adr/ADR-003-period-markup-with-safety-layer.md)). Every kit and build carries byte-identical copies; the quality gate fails if a copy drifts from this folder.

| File | What it does |
|---|---|
| [homestead-safe.css](homestead-safe.css) | Emulates `blink` at one cycle per second, styles the Safe Mode toggle, and defines Safe Mode: no background images, white backgrounds, black text, standard link colors, no custom cursors. Hides animated images under reduced motion until still frames are swapped in. |
| [homestead-safe.js](homestead-safe.js) | Adds the toggle as the first focusable element, swaps `img[data-still]` to its still frame, stops every `marquee`, stops audio, remembers the choice, starts in Safe Mode when the visitor prefers reduced motion, and wires click-to-play audio on `[data-hs-audio]`. Exposes `window.homesteadSafe()` for period scripts. |

## Wiring a page

```html
<head>
<link rel="stylesheet" href="homestead-safe.css">
<script src="homestead-safe.js" defer></script>
</head>
```

Animated GIF with a still frame for Safe Mode:

```html
<img src="images/new.gif" data-still="images/new-still.gif" alt="NEW!">
```

Click-to-play music (nothing ever autoplays):

```html
<a href="audio/theme.wav" data-hs-audio="audio/theme.wav"><img src="images/badge-music.gif" alt="Turn on music"></a>
```

A period script that should pause in Safe Mode:

```html
<script language="JavaScript">
<!--
function tick() {
  if (!(window.homesteadSafe && window.homesteadSafe())) { /* advance the effect */ }
  setTimeout("tick()", 200);
}
//-->
</script>
```

## Standards it answers

| Requirement | How the layer meets it |
|---|---|
| WCAG 2.2.2 pause, stop, hide | The toggle stops marquees, blink emulation, animated GIFs, and scripted effects |
| WCAG 1.4.2 audio control | Audio starts only on a click and stops on a second click or when Safe Mode turns on |
| WCAG 2.3.1 three flashes | Blink runs at one cycle per second; gifsmith enforces the 340 ms frame floor and gif_audit checks area and rate |
| prefers-reduced-motion | Safe Mode starts on, and animated images stay hidden until stills are in place |

Safe Mode is a mechanism, not a guarantee. The auditor still checks every page by hand ([docs/09](../../docs/09-accessibility-and-safety.md)).
