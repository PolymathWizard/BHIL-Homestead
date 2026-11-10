#!/usr/bin/env python3
"""build_site: assemble the publishable tree for MkDocs.

MkDocs cannot use the repo root as docs_dir, so this mirrors the publishable
folders into a gitignored site-src/ and renames the root README.md to
index.md. Directory README.md files serve as section indexes so relative
links written for GitHub also resolve on the published site. The kits and
example builds are copied too, so the period pages are live demos on Pages.

Usage:
    python3 scripts/build_site.py --assemble
    mkdocs build --strict

Stdlib only.
"""

import argparse
import os
import shutil
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SITE_SRC = os.path.join(ROOT, "site-src")
PUBLISH_DIRS = ("docs", "support", "adr", "prompts", "templates", "kits", "examples", "assets", "data", "schemas", "launch", "skill")
PUBLISH_FILES = ("CONTRIBUTING.md", "CHANGELOG.md", "AGENTS.md", "CODE_OF_CONDUCT.md", "SECURITY.md", "LICENSE", "LICENSE-CONTENT")


def resolve_index_collisions():
    """A folder with both index.html (a live period demo) and README.md would
    publish two index pages. Rename README.md to overview.md in the assembled
    tree only, and rewrite links that point at it."""
    renamed = []
    for root, _dirs, names in os.walk(SITE_SRC):
        if "README.md" in names and "index.html" in names:
            os.rename(os.path.join(root, "README.md"), os.path.join(root, "overview.md"))
            renamed.append(os.path.basename(root))
    if not renamed:
        return
    for root, _dirs, names in os.walk(SITE_SRC):
        for name in names:
            if not name.endswith(".md"):
                continue
            path = os.path.join(root, name)
            with open(path, "r", encoding="utf-8") as handle:
                text = handle.read()
            new_text = text
            for folder in renamed:
                new_text = new_text.replace(folder + "/README.md", folder + "/overview.md")
            if new_text != text:
                with open(path, "w", encoding="utf-8") as handle:
                    handle.write(new_text)


def assemble():
    if os.path.isdir(SITE_SRC):
        shutil.rmtree(SITE_SRC)
    os.makedirs(SITE_SRC)
    shutil.copyfile(os.path.join(ROOT, "README.md"), os.path.join(SITE_SRC, "index.md"))
    for name in PUBLISH_FILES:
        src = os.path.join(ROOT, name)
        if os.path.isfile(src):
            shutil.copyfile(src, os.path.join(SITE_SRC, name))
    for folder in PUBLISH_DIRS:
        src = os.path.join(ROOT, folder)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(SITE_SRC, folder), ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    resolve_index_collisions()
    count = sum(len(files) for _r, _d, files in os.walk(SITE_SRC))
    print("build_site: assembled %d files into site-src/" % count)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Assemble the MkDocs source tree.")
    parser.add_argument("--assemble", action="store_true")
    args = parser.parse_args(argv)
    if not args.assemble:
        parser.print_help()
        return 2
    assemble()
    return 0


if __name__ == "__main__":
    sys.exit(main())
