# Changelog

All notable changes to HOMESTEAD are recorded here. Versions follow semantic versioning.

## [1.1.1] - 2026-11-10

### Added

- Intro GIF (`launch/media/bhil-homestead-intro.gif`, twelve-second seamless loop, 1200 x 675) and its poster frame, linked from the README to the new project page.
- Project page and scroll-through tour at https://barryhurd.com/project/BHIL-Homestead.html, recorded in `canon/homestead.json` as `project_page`, with `docs_site` for GitHub Pages.

### Changed

- The repository publishes as github.com/PolymathWizard/BHIL-Homestead. Canon, mkdocs, CITATION.cff, schema `$id` values, the issue template, the survey user agent, and absolute doc links follow.
- Launch copy closes each LinkedIn variant with the tour and code links, and the GitHub description notes set the website field.

### Fixed

- The worked example's brand colors now follow the web-safe snap rule the tool and figures already use: violet `#6600CC` and sky `#3399CC` (the per-channel values `#6633CC` and `#0099FF` moved more than delta E 10). Recipes, era specs, asset logs, the 2007 stylesheet, generated GIFs, screenshots, the example README, the preset B scorecard evidence, and the docs 03 and 06 tables agree again.

## [1.1.0] - 2026-11-10

### Added

- Figure kit: ten 1600 x 900 figures, HS-01 to HS-10, that put period web specimens (pixel type, bevel chrome, 88x31 badges, odometers, marquees, real gifsmith output) inside the BHIL instrument frame from BHIL Brand Guidelines v1.0. Animated SVG with a designed static frame zero, plus static PNG renders and a standalone gallery ([ADR-009](adr/ADR-009-figure-kit.md)).
- `canon/brand.json`: palette, type stacks, brand strip, figure rules, and every figure's title, alt text, motion note, and placements.
- `scripts/figures.py`, called by `scripts/build_derived.py`, so the drift gate covers the figures; `scripts/render_figures.py` for PNG renders with a source hash.
- Visual README: masthead, one figure per major idea, and a two-column gallery of all ten.
- Validator figure gate: count, accessibility, reduced motion, 96 KB size budget, every canon placement embedded, PNG present at 1600 x 900 and rendered from the current SVG.
- Regression tests for the figure kit and repository hygiene.
- Pixel font glyphs for `[`, `]`, and the middle dot.

### Changed

- Every figure placement: README, method docs 01 to 09 and 11, generated reference pages, presets index, prompts index, safety layer, and the worked example.
- Docs site stylesheet moved from the older cobalt tokens to Brand Guidelines v1.0: Terminal Navy, BH Blue, Newsreader headlines, hairline tables, square corners.
- Figure kit page added to the site navigation; ADR count is now nine.

### Removed

- The seven v1.0.0 diagrams in `assets/diagrams/`, replaced by the figure kit.

### Fixed

- `.gitignore` pattern `site/` also matched `assets/site/`, so the docs stylesheet was never committed in v1.0.0. Build output patterns are now root anchored.
- The site assembler now rewrites relative links to the root README, which publishes as `index.md`.

## [1.0.0] - 2026-11-10

### Added

- Canon: six era presets, 44 widgets, 24-row modern-to-retro mapping table with detection signals, 20-row rubric with bands and hard gates, 28 lint rules, 15 period techniques, font map, seven-phase process, agent roster, and a 43-claim evidence register.
- Tools (stdlib only): `survey.py`, `map.py`, `websafe.py`, `dither.py`, `gifsmith.py`, `chiptune.py`, `era_lint.py`, `gif_audit.py`, `rubric.py`, `scaffold.py`, plus the `hs_core` library (GIF89a codec, 5x7 pixel font, PNG decoder, WAV and MIDI writers).
- Kits for preset B (GeoCities), C (FrontPage, original Ledger Blue theme), and E (MySpace), and the Safe Mode safety layer.
- Worked example: Nimbus Ledger rebuilt as 1998, 2001, and 2007 sites, each scored 39 of 40.
- Agent layer: AGENTS.md, CLAUDE.md, six tool-isolated subagents, seven slash commands, a PostToolUse lint hook.
- Prompt system P00 to P10 and a portable skill.
- Documentation (eleven pages), generated preset pages and reference tables, eight ADRs, support layer.
- Quality gates: validator, drift gate, regression tests, GitHub Actions for quality, drift, and Pages publishing.
