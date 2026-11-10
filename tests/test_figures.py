"""Regression tests for the HOMESTEAD figure kit (ADR-009).

Every test docstring names the bug it prevents. Run with:
    python3 -m unittest discover -s tests -v
"""

import os
import re
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import figures  # noqa: E402
from hs_core import canon, raster  # noqa: E402


def build():
    return figures.build_svgs(ROOT)


class FigureKitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.svgs = build()

    def test_every_figure_char_has_a_pixel_glyph(self):
        """Prevents figure text silently rendering "?" for characters the 5x7 font lacked ("[", "]", and the middle dot in the HS-03 webring, the HS-05 hit counter, and the HS-07 window title)."""
        seen = set()
        real_glyph_id = figures.glyph_id
        real_glyph = raster.glyph

        def spy_id(ch):
            seen.add(ch)
            return real_glyph_id(ch)

        def spy_glyph(ch):
            seen.add(ch)
            return real_glyph(ch)

        figures.glyph_id = spy_id
        raster.glyph = spy_glyph
        try:
            build()
        finally:
            figures.glyph_id = real_glyph_id
            raster.glyph = real_glyph
        missing = sorted(ch for ch in seen if ch != " " and ch.upper() not in raster.GLYPHS)
        self.assertEqual(missing, [], "pixel font has no glyph for %r" % missing)

    def test_keyframe_percentages_are_not_double_escaped(self):
        """Prevents the HS-04 build crashing with "unsupported format character" and, once escaped, leaking "%%" into keyframes that browsers then ignore."""
        for name, svg in self.svgs.items():
            self.assertNotIn("%%", svg, name)
            for block in re.findall(r"@keyframes [\w-]+ \{(.*?)\}\s*\}", svg, re.S):
                self.assertRegex(block, r"(\d+(\.\d+)?%|from|to) \{", name)

    def test_hs04_scan_band_is_clipped_to_the_page(self):
        """Prevents the HS-04 scan band showing as a stray blue bar above the modern page at frame zero."""
        svg = self.svgs["hs-04-site-survey.svg"]
        self.assertRegex(svg, r'<clipPath id="pg"><rect [^>]+/></clipPath>')
        self.assertIn('<g clip-path="url(#pg)"><g class="hs04-scan">', svg)

    def test_hs01_stars_stay_off_the_wordmark_and_copy(self):
        """Prevents twinkle stars landing on the HOMESTEAD wordmark, the title, or the preset badges."""
        svg = self.svgs["hs-01-masthead.svg"]
        stars = [(int(x), int(y)) for x, y in re.findall(r'<circle cx="(\d+)" cy="(\d+)" r="2.6"[^>]*class="hs-twinkle"', svg)]
        self.assertEqual(len(stars), 26)
        zones = [(130, 180, 1470, 380), (330, 380, 1270, 510), (380, 530, 1220, 630)]
        for x, y in stars:
            for a, b, c, d in zones:
                self.assertFalse(a <= x <= c and b <= y <= d, "star at %d,%d overlaps content" % (x, y))

    def test_every_figure_stops_under_reduced_motion(self):
        """Prevents a figure that keeps animating, or keeps playing an embedded GIF, for viewers who ask for reduced motion."""
        for name, svg in self.svgs.items():
            self.assertIn("@media (prefers-reduced-motion: reduce) { * { animation: none !important; } .hs-anim { display: none; } }", svg, name)

    def test_animated_gif_specimens_carry_a_still_frame(self):
        """Prevents HS-06 showing an empty slot under reduced motion because an animated GIF had no still frame behind it."""
        svg = self.svgs["hs-06-asset-smithy.svg"]
        animated = re.findall(r'(<image [^>]*?/>)(<image [^>]*class="hs-anim"[^>]*/>)', svg)
        self.assertGreaterEqual(len(animated), 2)
        for still, anim in animated:
            self.assertNotIn("hs-anim", still)
            self.assertEqual(re.search(r'x="([\d.]+)" y="([\d.]+)"', still).groups(), re.search(r'x="([\d.]+)" y="([\d.]+)"', anim).groups())

    def test_figures_are_deterministic(self):
        """Prevents unseeded randomness or dict ordering making the drift gate fail on an unchanged canon."""
        self.assertEqual(self.svgs, build())

    def test_no_gradients_on_motifs(self):
        """Prevents the HS-01 dot constellation fading through a radial gradient, which BHIL Brand Guidelines v1.0 rule out for motifs."""
        for name, svg in self.svgs.items():
            self.assertNotIn("Gradient", svg, name)

    def test_one_motif_per_surface(self):
        """Prevents the dot constellation or the ASCII pipeline appearing outside their single home figure."""
        for name, svg in self.svgs.items():
            if name != "hs-01-masthead.svg":
                self.assertNotIn('<pattern id="dots"', svg, name)
            if name != "hs-03-pipeline.svg":
                self.assertNotIn("RETRO-WEB REDESIGN ARCHITECTURE", svg, name)

    def test_counts_in_figures_follow_canon(self):
        """Prevents the masthead quoting stale counts after a canon change."""
        svg = self.svgs["hs-01-masthead.svg"]
        self.assertIn("%d LINT RULES" % len(canon.load("lint-rules")["rules"]), svg)
        self.assertIn("V%s" % canon.load("homestead")["version"], svg)

    def test_no_dashes_in_figures(self):
        """Prevents an em or en dash reaching a figure through canon text, past the repository dash gate."""
        for name, svg in self.svgs.items():
            self.assertFalse(re.search("[%s%s]" % (chr(0x2013), chr(0x2014)), svg), name)


class RepositoryHygieneTests(unittest.TestCase):
    def test_gitignore_build_patterns_are_root_anchored(self):
        """Prevents ".gitignore" pattern "site/" also ignoring assets/site/, which kept bhil.css out of v1.0.0 and left the docs site unstyled."""
        with open(os.path.join(ROOT, ".gitignore"), "r", encoding="utf-8") as handle:
            lines = [ln.strip() for ln in handle]
        self.assertNotIn("site/", lines)
        self.assertNotIn("site-src/", lines)
        self.assertIn("/site/", lines)
        self.assertIn("/site-src/", lines)


if __name__ == "__main__":
    unittest.main()
