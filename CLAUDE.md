# HOMESTEAD: Claude Code configuration

@AGENTS.md

## Claude Code specifics

- Start an engagement with `/homestead <url> <preset or "recommend">`. The command runs the full pipeline with checkpoints. Single phases: `/hs-survey`, `/hs-era`, `/hs-map`, `/hs-assets`, `/hs-build`, `/hs-audit`.
- Subagents live in `.claude/agents/`. Run the orchestrator on Opus and the subagents on Sonnet (CADRE pattern). Delegate each phase to its subagent with the engagement slug and the paths it needs; do not paste whole files into the delegation.
- `.claude/settings.json` wires `scripts/hook_era_lint.py` as a PostToolUse hook on Write and Edit. When it exits 2, read the findings and fix them before writing the next file.
- Permissions allow writes under `engagements/` and deny writes to `canon/` and derived folders. If a task genuinely needs a canon change, stop and ask.
- When the auditor returns, write its scorecard JSON to `06-qa/scorecard.json` verbatim, then run `python3 tools/rubric.py score ... --write`. Do not adjust the auditor's scores.

## Checkpoints where the orchestrator stops for the human

1. After intake, if purpose, rights, or asset policy is unclear.
2. After era lock, to confirm the preset and year.
3. After mapping, to confirm drops and merges.
4. Before shipping, with the scorecard and QA notes.

When the person has said to run unattended, take the most reasonable reading at each checkpoint, write the choice into the engagement README decisions log, and continue. Never skip checkpoint 4 for client work.
