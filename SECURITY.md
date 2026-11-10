# Security policy

HOMESTEAD ships static pages and offline tools. The parts with real risk are:

- `tools/survey.py`, which fetches remote pages. It never submits forms or follows links off the target domain.
- `kits/safety-layer/homestead-safe.js`, which runs on every published page.
- Photosensitive safety: any animation that can exceed WCAG flash thresholds is treated as a security-grade bug.

## Reporting

Please report vulnerabilities and flash-safety bugs privately through GitHub's private vulnerability reporting on this repository, not in a public issue. Include the file, the steps to reproduce, and for flash issues the GIF or page and the browser.

We aim to acknowledge reports within five business days.
