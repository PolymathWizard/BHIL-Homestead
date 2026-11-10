---
title: "Portable skill"
description: "The HOMESTEAD process packaged as a single SKILL.md for chat tools without the repository."
---

# Portable skill

[homestead/SKILL.md](homestead/SKILL.md) condenses the whole process (intake, survey, era lock, mapping, assets, build, audit) into one skill file that works in any Claude surface that supports skills, with or without this repository.

| Situation | Use |
|---|---|
| Claude Code inside this repo | `/homestead` and the subagents in `.claude/agents/` |
| A chat surface with skills | Install `skill/homestead/` as a skill |
| Any chat tool without skills | Paste [prompts/P00-command-center.md](../prompts/P00-command-center.md) |

## Install

Zip the `skill/homestead/` folder and upload it as a skill, or copy `SKILL.md` into your skills directory. The skill's tables are a snapshot of canon at v1.0.0. When canon changes, update the skill in the same release and note it in the changelog.
