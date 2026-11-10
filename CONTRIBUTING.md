# Contributing to HOMESTEAD

Thanks for helping. HOMESTEAD has three kinds of content, and each changes differently.

| Kind | Where | How to change it |
|---|---|---|
| Canon | `canon/*.json` | Edit the JSON, run `python3 scripts/build_derived.py`, update `EXPECTED` counts in `scripts/validate.py` if a count changed, commit everything together |
| Derived artifacts | `docs/presets/`, `docs/reference/`, `templates/era-spec-cards/`, `data/`, `assets/diagrams/`, kit and example images and audio, `MANIFEST.sha256` | Never by hand. The drift gate fails on any hand edit |
| Hand-written content | `docs/0*.md` to `docs/11*.md`, `support/`, `adr/`, `prompts/`, `.claude/`, kit and example HTML, `tools/`, `scripts/`, `tests/` | Edit directly |

## Before you open a pull request

```bash
python3 scripts/build_derived.py
python3 scripts/verify_drift.py
python3 scripts/validate.py
python3 -m unittest discover -s tests
```

All four must pass. CI runs the same commands.

## House rules

- **Stdlib only.** Tools and scripts use the Python standard library. No pip dependencies outside the docs site.
- **No em dashes or en dashes.** Anywhere, including period copy. Use commas, colons, or "to" (ADR-006).
- **Evidence tiers.** New factual claims go in `canon/sources.json` with a tier and sources. CORROBORATED needs two independent sources (ADR-008).
- **Regression tests name their bugs.** Every test docstring starts with "Prevents" and names the bug.
- **Never report clean.** Tool verdicts stay within the vocabulary in ADR-007.
- **Originals first.** New kit assets come from `tools/gifsmith.py` or `tools/chiptune.py`. No archived GIFs, real songs, third-party logos, or embedded fonts in the repository (ADR-004).
- **Conventional commits** scoped to the framework: `feat(homestead):`, `fix(homestead):`, `docs(homestead):`, `test(homestead):`, `ci(homestead):`.

## Common contributions

### Add a widget

1. Add it to `canon/widgets.json` with the presets that allow it.
2. Reference it from a mapping row or a preset's required list if appropriate.
3. Rebuild, update the widget count in `scripts/validate.py`, and run the gates.

### Add a lint rule

1. Add it to `canon/lint-rules.json` with severity per preset, a rubric row, a message, and a fix.
2. If it needs a new `kind`, implement it in `tools/era_lint.py`.
3. Add a test that names the bug it prevents. Rebuild, update the count, run the gates.

### Build a kit for preset A, D, or F

1. Create `kits/preset-<id>-<slug>/` with pages, a `recipe.json`, and a README with frontmatter.
2. Set the preset's `status` to `kit` and `kit` path in `canon/presets.json`.
3. The kit must pass `era_lint --strict` and `gif_audit` with no failures. Update `kit_presets` in the validator.

### Add a worked example

Create `examples/<name>/source/index.html` (fictional brand), then `builds/<preset>-<year>/` with `era-spec.json`, `recipe.json`, pages, and `asset-log.csv`. Rebuild to generate the inventory, mappings, lint reports, and audits. Score each build in `qa/scorecard-<P>.json` with `tools/rubric.py`.

## Reporting problems

Use the issue forms: correction, question, suggestion, anachronism report, or new preset proposal. Flash-safety problems go through private reporting in [SECURITY.md](SECURITY.md).
