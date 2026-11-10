---
title: "Quickstart"
description: "Open an engagement, survey a site, and see a period build in five minutes."
---

# Quickstart

You need Python 3.10 or newer. Nothing to install.

## 1. Look at the finished example

Open these in a browser straight from the repository:

- `examples/nimbus-ledger/source/index.html`: the modern page
- `examples/nimbus-ledger/builds/preset-b-1998/index.html`: as a 1998 GeoCities homepage
- `examples/nimbus-ledger/builds/preset-c-2001/index.html`: as a 2001 FrontPage company site
- `examples/nimbus-ledger/builds/preset-e-2007/index.html`: as a 2007 profile

Press the SAFE MODE button at the bottom right of any period page to stop motion and sound and raise contrast.

## 2. Open your own engagement

```bash
python3 tools/scaffold.py new mysite --target https://example.com --preset B
```

This creates `engagements/mysite/` with an intake form, an era spec card, and a working preset B kit in `05-build/`. Open `engagements/mysite/05-build/index.html` now; it already works.

## 3. Survey the modern site

```bash
python3 tools/survey.py https://example.com --pages 6 --out engagements/mysite/01-inventory/inventory.json
```

If the site blocks the request, save the page from your browser and pass the file path instead.

## 4. Map it

```bash
python3 tools/map.py engagements/mysite/01-inventory/inventory.json \
  --spec engagements/mysite/02-era-spec.json --out engagements/mysite/03-mapping.md
```

Open `03-mapping.md`: every modern pattern already has a period equivalent and a default decision.

## 5. Make the title and build

```bash
python3 tools/gifsmith.py one wordart engagements/mysite/05-build/images/title.gif \
  --params '{"text": "MY SITE", "scale": 5, "shadow": "#660066", "outline": "#000000"}'
```

Edit `05-build/index.html`, replacing every `[bracketed]` value with mapped content.

## 6. Check it

```bash
python3 tools/era_lint.py engagements/mysite/05-build --preset B
python3 tools/gif_audit.py engagements/mysite/05-build --page-bg "#000000"
```

## With Claude Code

```text
/homestead https://example.com recommend
```

The orchestrator runs all seven phases with its subagents and stops at four checkpoints for your decisions.

## Next

- [Process](../docs/02-process.md)
- [Era presets](../docs/presets/README.md)
- [FAQ](faq.md)
