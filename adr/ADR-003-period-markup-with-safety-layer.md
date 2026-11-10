---
id: "ADR-003"
title: "Period markup with a thin modern safety layer"
status: "accepted"
date: "2026-11-10"
---

# ADR-003: Period markup with a thin modern safety layer

## Context

Two ways to build a retro page: write genuinely period markup (tables, font tags, spacer GIFs), or write modern code styled to look old. Modern code fails View Source and tends to leak spacing and typography tells. Pure period markup cannot meet modern needs: blink no longer renders, autoplay audio is blocked and inaccessible, and there is no off switch for motion.

## Decision

Pages are written in period markup. Two files, `homestead-safe.css` and `homestead-safe.js`, provide everything modern: blink emulation, Safe Mode, still-frame swaps, marquee handling, click-to-play audio, and reduced-motion defaults. Every page links both. The lint exempts exactly those two file names and nothing else.

Every kit and build carries byte-identical copies, checked against `kits/safety-layer/` by the validator and the drift gate.

## Consequences

- View Source shows period markup plus two link lines.
- Accessibility work happens once, in one place, and applies to every build.
- Period scripts integrate by checking `window.homesteadSafe()`.
- The safety layer must stay small and boring; feature growth there is a smell.

## Alternatives considered

- **Modern framework styled retro.** Rejected; fails View Source and the authenticity rubric.
- **Pure period markup with no safety layer.** Rejected; fails WCAG 2.2.2, 1.4.2, and reduced-motion expectations.
- **A browser extension for safety.** Rejected; visitors would need to install it.

## Open questions

- Should Safe Mode offer a middle setting (motion off, colors kept)? Settling criteria: requests from two or more engagements.
