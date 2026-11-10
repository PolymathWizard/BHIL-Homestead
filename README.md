<p align="center">
  <img src="assets/figures/hs-01-masthead.svg" alt="HOMESTEAD masthead: a dot-matrix HOMESTEAD wordmark over the BHIL dot constellation, with preset badges for GeoCities 1998, FrontPage 2001, MySpace 2007, and Safe Mode." width="100%">
</p>

# BHIL-Homestead

**Analyze any modern website and rebuild it the way GeoCities, FrontPage, or MySpace would have.**

HOMESTEAD is a repeatable process, a stdlib-only toolchain, and a Claude Code agent team for retro web redesigns. Point it at a modern site, lock one era, and it walks you from inventory to a period build that survives View Source, ships with a Safe Mode for today's visitors, and carries a 40-point authenticity score. Every image and sound is generated from scratch, so builds carry no borrowed GIFs, fonts, or songs.

REF HOMESTEAD-001 | v1.1.0 | Barry Hurd Intelligence Lab

| Modern source | Preset B, 1998 | Preset C, 2001 | Preset E, 2007 |
|---|---|---|---|
| [Nimbus Ledger, 2026](examples/nimbus-ledger/source/index.html) | [GeoCities homepage](examples/nimbus-ledger/builds/preset-b-1998/index.html) | [FrontPage company site](examples/nimbus-ledger/builds/preset-c-2001/index.html) | [Profile page](examples/nimbus-ledger/builds/preset-e-2007/index.html) |

![The worked example as a 1998 GeoCities homepage](examples/nimbus-ledger/screenshots/preset-b-1998.png)

## Start here

| If you want to | Go to |
|---|---|
| See a result in five minutes | [Quickstart](support/quickstart.md) |
| Understand the method | [Overview](docs/01-overview.md), then [Process](docs/02-process.md) |
| Run it with Claude Code | `/homestead <url> recommend`, see [Agent architecture](docs/11-agent-architecture.md) |
| Run it in any chat tool | [P00 Command Center](prompts/P00-command-center.md) or the [portable skill](skill/README.md) |
| Pick an era | [Era lock](docs/04-era-lock.md) |
| Check the rights picture | [Legal and licensing](docs/10-legal-and-licensing.md) |
| Use the figures | [Figure kit](assets/figures/README.md) |
| Contribute | [CONTRIBUTING.md](CONTRIBUTING.md) |

## Six locked eras, not one retro look

![Timeline from 1993 to 2026 showing the six HOMESTEAD era presets, with kits for GeoCities, FrontPage, and MySpace and spec-only presets for Proto-Web, Portal, and Revival.](assets/figures/hs-02-era-neighborhoods.svg)

Proto-Web, GeoCities, FrontPage corporate, Web 1.5 portal, MySpace profile, and modern revival, each with a canvas width, palette, fonts, widgets, voice, and motion budget. Every build locks one preset and one year; mixing eras is a lint error unless the build declares a time capsule. Kits ship for the three best-documented eras. [Presets](docs/presets/README.md) · [Era lock](docs/04-era-lock.md)

## Seven phases, each closed by a written contract

![BHIL ASCII pipeline on an ink panel: intake, survey, era lock, map, assets, build, and audit, with each phase owner and its written output.](assets/figures/hs-03-pipeline.svg)

| Phase | Owner | Tool |
|---|---|---|
| 0 Intake | orchestrator | `tools/scaffold.py` |
| 1 Site survey | site-surveyor | `tools/survey.py` |
| 2 Era lock | era-archivist | era spec cards |
| 3 Component mapping | component-mapper | `tools/map.py` |
| 4 Assets | asset-smith | `tools/websafe.py`, `gifsmith.py`, `dither.py`, `chiptune.py` |
| 5 Build | period-builder | kits, safety layer, `tools/era_lint.py` |
| 6 Authenticity QA | authenticity-auditor | `tools/era_lint.py`, `gif_audit.py`, `rubric.py` |

[Process](docs/02-process.md) · [Phase map](docs/reference/phase-map.md) · [Prompts](prompts/README.md)

## Component-by-component translation

![Table mapping six modern patterns to their GeoCities, FrontPage, and MySpace equivalents, each shown as a small period badge.](assets/figures/hs-05-component-mapping.svg)

24 modern patterns (hero, cards, pricing, testimonials, cookie banner, chat widget, analytics) each mapped to their period equivalent per era, with detection signals the survey uses to find them. [Mapping](docs/05-component-mapping.md) · [Mapping table](docs/reference/mapping-table.md)

## Safe Mode on every page

![The same period page as built, with starfield, marquee, and blinking badge, and in Safe Mode, plain and readable, with the WCAG criteria it answers.](assets/figures/hs-08-safe-mode.svg)

One control stops every marquee, blink, animation, and sound and raises contrast; it starts on for reduced-motion visitors. The GIF audit checks frame timing and WCAG flash area, and audio only plays after a click. [Accessibility and safety](docs/09-accessibility-and-safety.md) · [Safety layer](kits/safety-layer/README.md)

## A lint for anachronisms and a blind grade

![Odometer showing 39 of 40 for the Nimbus Ledger 1998 build, the twenty rubric rows with their scores, the score bands, and the hard gates.](assets/figures/hs-09-rubric.svg)

28 lint rules catch web fonts, rounded corners, flexbox, emoji, era mixing, and missing safety wiring. A 20-row rubric scores the build out of 40, with hard gates no total can override. [Authenticity QA](docs/08-authenticity-qa.md) · [Rubric](docs/reference/rubric.md) · [Lint rules](docs/reference/lint-rules.md)

## The crew

![Profile-style friend grid of the human director, the orchestrator, and six subagents with their phases, models, and tool lists; the auditor is marked read only.](assets/figures/hs-10-agent-crew.svg)

A human director, an Opus orchestrator, and six tool-isolated Sonnet subagents. The agent that grades the build cannot write files and never sees the builder's notes. [Agent architecture](docs/11-agent-architecture.md) · [Agent roster](docs/reference/agent-roster.md)

## Quick commands

```bash
python3 tools/scaffold.py new acme --target https://acme.example --preset B
python3 tools/survey.py https://acme.example --pages 6 --out engagements/acme/01-inventory/inventory.json
python3 tools/map.py engagements/acme/01-inventory/inventory.json --spec engagements/acme/02-era-spec.json --out engagements/acme/03-mapping.md
python3 tools/era_lint.py engagements/acme/05-build --spec engagements/acme/02-era-spec.json
python3 tools/rubric.py score engagements/acme/06-qa/scorecard.json
```

Python 3.10 or newer, standard library only.

## The figure kit

Ten 1600 x 900 figures put period web specimens (pixel type, bevels, 88x31 badges, odometers, marquees) inside the BHIL instrument frame. They are generated from canon and example data by `scripts/figures.py`, drift-checked with everything else, and animate gently until the viewer prefers reduced motion. Static PNG renders for slides and social posts live in `assets/figures/png/`. Full notes: [figure kit](assets/figures/README.md).

<table>
  <tr>
    <td width="50%"><a href="assets/figures/hs-01-masthead.svg"><img src="assets/figures/hs-01-masthead.svg" alt="HS-01 masthead" width="400"></a><br><sub><b>HS-01</b> Retro-Web Redesign Engine</sub></td>
    <td width="50%"><a href="assets/figures/hs-02-era-neighborhoods.svg"><img src="assets/figures/hs-02-era-neighborhoods.svg" alt="HS-02 era neighborhoods" width="400"></a><br><sub><b>HS-02</b> Six neighborhoods. One address per build.</sub></td>
  </tr>
  <tr>
    <td width="50%"><a href="assets/figures/hs-03-pipeline.svg"><img src="assets/figures/hs-03-pipeline.svg" alt="HS-03 pipeline" width="400"></a><br><sub><b>HS-03</b> Seven phases. Every one leaves paper.</sub></td>
    <td width="50%"><a href="assets/figures/hs-04-site-survey.svg"><img src="assets/figures/hs-04-site-survey.svg" alt="HS-04 site survey" width="400"></a><br><sub><b>HS-04</b> Inventory before era.</sub></td>
  </tr>
  <tr>
    <td width="50%"><a href="assets/figures/hs-05-component-mapping.svg"><img src="assets/figures/hs-05-component-mapping.svg" alt="HS-05 component mapping" width="400"></a><br><sub><b>HS-05</b> Translate component by component.</sub></td>
    <td width="50%"><a href="assets/figures/hs-06-asset-smithy.svg"><img src="assets/figures/hs-06-asset-smithy.svg" alt="HS-06 asset smithy" width="400"></a><br><sub><b>HS-06</b> Every glyph drawn here. Nothing borrowed.</sub></td>
  </tr>
  <tr>
    <td width="50%"><a href="assets/figures/hs-07-view-source.svg"><img src="assets/figures/hs-07-view-source.svg" alt="HS-07 view source" width="400"></a><br><sub><b>HS-07</b> View Source never lies.</sub></td>
    <td width="50%"><a href="assets/figures/hs-08-safe-mode.svg"><img src="assets/figures/hs-08-safe-mode.svg" alt="HS-08 safe mode" width="400"></a><br><sub><b>HS-08</b> Keep the chaos. Give it an off switch.</sub></td>
  </tr>
  <tr>
    <td width="50%"><a href="assets/figures/hs-09-rubric.svg"><img src="assets/figures/hs-09-rubric.svg" alt="HS-09 rubric" width="400"></a><br><sub><b>HS-09</b> Graded blind. Scored to forty.</sub></td>
    <td width="50%"><a href="assets/figures/hs-10-agent-crew.svg"><img src="assets/figures/hs-10-agent-crew.svg" alt="HS-10 agent crew" width="400"></a><br><sub><b>HS-10</b> The crew's Top 8. One of them can't write.</sub></td>
  </tr>
</table>

## Repository structure

```
BHIL-Homestead/
  canon/          single source of truth: presets, widgets, mapping, rubric, lint rules, claims, brand
  tools/          stdlib engagement tools and the hs_core library (GIF codec, pixel font, PNG, audio)
  scripts/        derived-artifact generator, figure generator, drift gate, validator, site assembler, lint hook
  kits/           preset B, C, and E starters plus the safety layer
  examples/       Nimbus Ledger taken through every phase into three eras
  prompts/        P00 to P10 prompt system
  .claude/        six subagents, seven slash commands, settings, hook wiring
  skill/          portable SKILL.md
  docs/           process docs, generated preset pages and reference tables
  support/        quickstart, FAQ, troubleshooting, glossary
  adr/            nine architecture decisions
  templates/      intake, era spec cards, asset log, scorecard, QA notes
  schemas/        inventory, era spec, scorecard
  assets/         figure kit (ten SVG figures, PNG renders, gallery) and the docs site stylesheet
  data/           CSV and JSON exports of canon
  launch/         GitHub descriptions and LinkedIn copy
  engagements/    your work (gitignored)
```

## Contents

| Area | Pages |
|---|---|
| Method | [Overview](docs/01-overview.md), [Process](docs/02-process.md), [Survey](docs/03-site-survey.md), [Era lock](docs/04-era-lock.md), [Mapping](docs/05-component-mapping.md), [Assets](docs/06-assets.md), [Build](docs/07-build.md), [QA](docs/08-authenticity-qa.md) |
| Safety and rights | [Accessibility and safety](docs/09-accessibility-and-safety.md), [Legal and licensing](docs/10-legal-and-licensing.md), [Safety layer](kits/safety-layer/README.md) |
| Agents and prompts | [Agent architecture](docs/11-agent-architecture.md), [Agent roster](docs/reference/agent-roster.md), [Prompts](prompts/README.md), [AGENTS.md](AGENTS.md) |
| Reference | [Presets](docs/presets/README.md), [Mapping table](docs/reference/mapping-table.md), [Widgets](docs/reference/widget-registry.md), [Rubric](docs/reference/rubric.md), [Lint rules](docs/reference/lint-rules.md), [Technical vocabulary](docs/reference/technical-vocabulary.md), [Fonts](docs/reference/font-map.md), [Web-safe palette](docs/reference/web-safe-palette.md), [Evidence register](docs/reference/evidence-register.md) |
| Kits | [Preset B](kits/preset-b-geocities/README.md), [Preset C](kits/preset-c-frontpage/README.md), [Preset E](kits/preset-e-myspace/README.md) |
| Brand | [Figure kit](assets/figures/README.md), [gallery](assets/figures/gallery.html) |
| Decisions | [ADR index](adr/README.md) |
| Help | [Support](support/README.md) |

## Quality gates

```bash
python3 scripts/validate.py            # dash gate, canon integrity, counts, schemas, agent tools, builds, figures, links
python3 scripts/verify_drift.py        # every derived artifact, figures included, matches canon byte for byte
python3 -m unittest discover -s tests  # regression tests, each naming the bug it prevents
python3 scripts/render_figures.py      # optional: refresh PNG renders (needs Playwright and Chrome)
```

## Credits and license

Built by Barry Hurd Intelligence Lab. Research inputs are recorded with evidence tiers in the [evidence register](docs/reference/evidence-register.md), including Olia Lialina's writing on the vernacular web, the Internet Archive's GifCities, Restorativland, One Terabyte of Kilobyte Age, and prior art such as web98 and an existing FrontPage agent skill. Nimbus Ledger and every person, band, and network in the example are fictional. The figure kit follows BHIL Brand Guidelines v1.0; every pixel glyph, badge, and GIF in it is drawn by this repository's own tools.

Code and schemas: MIT ([LICENSE](LICENSE)). Documentation, prompts, kits, figures, and generated assets: CC BY 4.0 ([LICENSE-CONTENT](LICENSE-CONTENT)). Not legal advice.

*Human-Directed. AI-Enabled. Commercially Tested.*
