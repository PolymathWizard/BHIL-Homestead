# AGENTS.md: HOMESTEAD agent context

> Vendor-neutral instructions for Claude Code, Cursor, Codex, Copilot, and any AGENTS.md-compatible tool.
> This file is the single source of agent context. CLAUDE.md imports it.
> Framework: HOMESTEAD v1.0.0 | REF HOMESTEAD-001 | Barry Hurd Intelligence Lab

---

## What this repository is

HOMESTEAD is a process, a toolchain, and an agent team for one job: take any existing modern website, analyze it, and rebuild it as a convincing site from an earlier web era, such as a 1998 GeoCities homepage, a 2001 FrontPage corporate site, or a 2007 MySpace profile.

It is a **framework repository**. It contains the canon (era presets, mapping table, rubric, lint rules), stdlib-only Python tools, preset kits, prompts, and documentation. Client and portfolio work happens in `engagements/<slug>/`, which is gitignored.

## The pipeline governs every engagement

```
0 Intake -> 1 Site survey -> 2 Era lock -> 3 Component mapping -> 4 Assets -> 5 Build -> 6 Authenticity and safety QA
```

Do not skip a phase. Do not start building before the era is locked and every detected pattern has a mapping decision. Phase details: [docs/02-process.md](docs/02-process.md) and [docs/reference/phase-map.md](docs/reference/phase-map.md).

## Agent team (CADRE pattern)

The orchestrator (the main session, run with `/homestead`) owns intake, sequencing, human checkpoints, and writing the auditor's results into `06-qa/`. Six subagents each own one phase and hand back a contract.

| Agent | Phase | Writes | Cannot |
|---|---|---|---|
| `site-surveyor` | 1 | `01-inventory/` | Edit |
| `era-archivist` | 2 | `02-era-spec.json` | Bash, Edit |
| `component-mapper` | 3 | `03-mapping.md`, `03-copy-deck.md` | WebFetch, WebSearch |
| `asset-smith` | 4 | `04-asset-log.csv`, `05-build/images/`, `05-build/audio/` | WebSearch, Edit |
| `period-builder` | 5 | `05-build/` | WebSearch, WebFetch |
| `authenticity-auditor` | 6 | nothing; returns the scorecard | Write, Edit, WebSearch, WebFetch |

The auditor never sees the builder's notes and cannot write files, so the work never grades itself (ADR-005). Tool lists are canon in `canon/agents.json`; `scripts/validate.py` fails if a definition drifts.

## Commands

```bash
# Engagement workflow
python3 tools/scaffold.py new <slug> --target <url> --preset <A-F> --purpose portfolio
python3 tools/survey.py <url-or-file> --pages 6 --out engagements/<slug>/01-inventory/inventory.json
python3 tools/map.py engagements/<slug>/01-inventory/inventory.json --spec engagements/<slug>/02-era-spec.json --out engagements/<slug>/03-mapping.md
python3 tools/websafe.py snap --from-inventory engagements/<slug>/01-inventory/inventory.json
python3 tools/gifsmith.py recipe engagements/<slug>/05-build/recipe.json --out engagements/<slug>/05-build
python3 tools/dither.py photo.png engagements/<slug>/05-build/images/photo.gif --max-width 320
python3 tools/chiptune.py render ode-to-joy engagements/<slug>/05-build/audio/theme.wav
python3 tools/era_lint.py engagements/<slug>/05-build --spec engagements/<slug>/02-era-spec.json
python3 tools/gif_audit.py engagements/<slug>/05-build --page-bg "#000000"
python3 tools/rubric.py score engagements/<slug>/06-qa/scorecard.json --lint lint.json

# Framework maintenance
python3 scripts/build_derived.py      # regenerate every derived artifact from canon/
python3 scripts/verify_drift.py       # fail on any hand edit to a derived artifact
python3 scripts/validate.py           # full quality gate
python3 -m unittest discover -s tests # regression tests
```

## ALWAYS / ASK / NEVER

### ALWAYS
- Lock exactly one era preset per build. Mixing presets requires `time_capsule: true` and a written story in the era spec.
- Mark every period widget with `<!-- hs:widget ID -->` using IDs from `canon/widgets.json`.
- Link `homestead-safe.css` and `homestead-safe.js` on every page, and give every animated GIF a `data-still` frame.
- Keep audio click-to-play only, through `data-hs-audio`.
- Link a text-only version from every page.
- Snap flat colors to the web-safe cube for presets A to C and log the before and after.
- Log every asset in the asset log with source, license, and era check.
- Run `tools/era_lint.py` after every build edit (the Claude Code hook does this automatically).
- Tag factual claims with an evidence tier from `canon/sources.json` when writing docs.

### ASK BEFORE
- Choosing the archive-allowed asset policy, or using any archived GIF, MIDI, or font.
- Using any real third-party brand, browser, or platform logo, or a named product badge, in client work.
- Redesigning a third-party brand for anything other than clearly labeled commentary or portfolio work.
- Editing anything in `canon/`, or adding a preset, widget, lint rule, or rubric row.
- Shipping a build whose scorecard is below SHIP.

### NEVER
- Hand-edit a derived artifact (`docs/presets/`, `docs/reference/`, `templates/era-spec-cards/`, `data/`, `assets/figures/` (except `png/`), kit and example images, `MANIFEST.sha256`). Edit canon and run `scripts/build_derived.py`.
- Load web fonts, `@font-face`, CSS gradients, rounded corners, flexbox, grid, or emoji in a preset A to E build.
- Autoplay audio, ship frames faster than 340 ms, or ship without Safe Mode.
- Use real song lyrics, recognizable third-party characters, network logos, or self-hosted Microsoft core fonts.
- Write em dashes or en dashes anywhere. The dash gate fails CI.
- Report any lint or audit result as clean. No findings is INCONCLUSIVE (ADR-007).
- Commit anything under `engagements/` except `.gitkeep`.

## Repository map

| Path | Contents |
|---|---|
| `canon/` | Single source of truth: presets, widgets, mapping, rubric, lint rules, techniques, fonts, process, agents, sources |
| `tools/` | Stdlib-only engagement tools and the `hs_core` library |
| `scripts/` | Derived-artifact generator, drift gate, validator, site assembler, Claude Code hook |
| `kits/` | Preset B, C, and E starters plus the safety layer |
| `prompts/` | P00 to P10 prompt system |
| `.claude/` | Subagents, slash commands, settings, and the lint hook |
| `docs/`, `support/`, `adr/` | Documentation, help layer, decisions |
| `examples/nimbus-ledger/` | One fictional site taken through every phase into three eras |
| `engagements/` | Your work. Gitignored. |

## Conventions

- Python 3.10 or newer, standard library only. No pip dependencies for tools.
- Conventional commits scoped to the framework: `feat(homestead):`, `fix(homestead):`, `docs(homestead):`.
- Dual license: MIT for code and schemas, CC BY 4.0 for content and generated assets.
- Regression tests name the bug they prevent in their docstring.
