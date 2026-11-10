"""Regression tests for the HOMESTEAD toolchain.

Every test docstring names the bug it prevents. Run with:
    python3 -m unittest discover -s tests -v
"""

import json
import os
import shutil
import sys
import tempfile
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import era_lint  # noqa: E402
import gif_audit  # noqa: E402
import gifsmith  # noqa: E402
import map as mapper  # noqa: E402
import rubric  # noqa: E402
import survey  # noqa: E402
from hs_core import audio, canon, color, gif, png, raster  # noqa: E402

SAFE_HEAD = '<link rel="stylesheet" href="homestead-safe.css"><script src="homestead-safe.js" defer></script>'


def page(body, head=SAFE_HEAD):
    return "<!DOCTYPE html><html><head><meta charset=\"utf-8\"><title>t</title>%s</head><body>%s</body></html>" % (head, body)


class ColorTests(unittest.TestCase):
    def test_per_channel_snap_rounds_to_nearest(self):
        """Prevents the floor-instead-of-nearest bug that turned BHIL cobalt #1B4FD8 into #0033CC instead of #3366CC."""
        self.assertEqual(color.to_hex(color.snap_per_channel(color.parse_hex("#1B4FD8"))), "#3366CC")

    def test_short_hex_expands(self):
        """Prevents #RGB shorthand being read as #0R0G0B, which made #fc0 look off-palette."""
        self.assertEqual(color.parse_hex("#fc0"), (255, 204, 0))
        self.assertTrue(color.is_websafe(color.parse_hex("#fc0")))

    def test_websafe_palette_has_216_colors(self):
        """Prevents a levels typo silently shrinking the cube (claim C-003)."""
        self.assertEqual(len(set(color.websafe_palette())), 216)

    def test_perceptual_switch_only_when_better(self):
        """Prevents the perceptual fallback choosing a color farther away than the per-channel snap."""
        result = color.snap(color.parse_hex("#6D28D9"))
        self.assertLessEqual(result["delta_e"], color.delta_e(color.parse_hex("#6D28D9"), color.parse_hex(result["per_channel"])) + 1e-9)


class GifTests(unittest.TestCase):
    def test_roundtrip_noise_forces_table_reset(self):
        """Prevents the LZW off-by-one at 4096 codes that corrupted large, noisy frames after the dictionary reset."""
        import random
        rnd = random.Random(3)
        w, h = 180, 120
        pal = [(rnd.randrange(256), rnd.randrange(256), rnd.randrange(256)) for _ in range(256)]
        frame = bytes(rnd.randrange(256) for _ in range(w * h))
        decoded = gif.decode(gif.encode(w, h, pal, [frame]))
        self.assertEqual(decoded["frames"][0]["rgb"], [pal[p] for p in frame])

    def test_tiny_images_roundtrip(self):
        """Prevents the empty-trailing-bits bug that broke 1x1 spacer GIFs."""
        for size in (1, 2, 3):
            pal = [(0, 0, 0), (255, 255, 255)]
            frame = bytes((i % 2) for i in range(size * size))
            decoded = gif.decode(gif.encode(size, size, pal, [frame]))
            self.assertEqual(decoded["frames"][0]["rgb"], [pal[p] for p in frame])

    def test_probe_reads_delays(self):
        """Prevents the audit reading the delay of the next frame, which hid fast first frames."""
        a = raster.Canvas(4, 4, (0, 0, 0))
        b = raster.Canvas(4, 4, (255, 255, 255))
        data = raster.encode_frames([a, b], [12, 50])
        self.assertEqual(gif.probe(data)["delays_cs"], [12, 50])


class GifsmithTests(unittest.TestCase):
    def test_output_is_deterministic(self):
        """Prevents nondeterministic palettes, which made the drift gate fail on every run."""
        first = gifsmith.KINDS["glitter"]({"text": "HI", "seed": 4})
        second = gifsmith.KINDS["glitter"]({"text": "HI", "seed": 4})
        self.assertEqual(first, second)

    def test_badge_is_88_by_31(self):
        """Prevents badges drifting off the 88x31 standard when text is long."""
        data = gifsmith.KINDS["badge"]({"lines": ["A VERY LONG BADGE LINE", "TWO"]})[0][1]
        info = gif.probe(data)
        self.assertEqual((info["width"], info["height"]), (88, 31))

    def test_animation_respects_house_budget(self):
        """Prevents a recipe asking for 10 cs frames from shipping a strobing GIF."""
        anim = gifsmith.KINDS["new"]({"delay_cs": 5})[0][1]
        floor = canon.params()["gif_min_frame_delay_ms"] // 10
        self.assertTrue(all(d >= floor for d in gif.probe(anim)["delays_cs"]))

    def test_animated_assets_ship_still_frames(self):
        """Prevents Safe Mode having nothing to swap in for an animated asset."""
        out = gifsmith.KINDS["construction"]({})
        self.assertEqual([suffix for suffix, _ in out], ["", "-still"])
        self.assertEqual(gif.probe(out[1][1])["frames"], 1)


class AuditTests(unittest.TestCase):
    def _write(self, data):
        tmp = tempfile.NamedTemporaryFile(suffix=".gif", delete=False)
        tmp.write(data)
        tmp.close()
        self.addCleanup(os.unlink, tmp.name)
        return tmp.name

    def test_fast_frames_fail_budget(self):
        """Prevents fast animations passing because the budget compared centiseconds with milliseconds."""
        a = raster.Canvas(8, 8, (0, 0, 0))
        b = raster.Canvas(8, 8, (255, 255, 255))
        path = self._write(raster.encode_frames([a, b], [10, 10]))
        result = gif_audit.audit_file(path, canon.params(), (255, 255, 255))
        self.assertTrue(result["fail"])
        self.assertEqual(result["verdict"], "OVER TIMING BUDGET")

    def test_zero_delay_treated_as_100ms(self):
        """Prevents zero-delay frames being reported as 0 ms instead of the 100 ms browsers actually show."""
        self.assertEqual(gif_audit.effective_ms(0, canon.params()), 100)

    def test_large_full_contrast_flash_is_flagged(self):
        """Prevents short loops being simulated for under one second, which undercounted flashes on a large full-contrast strobe."""
        path = self._write(gif.encode(400, 300, [(0, 0, 0), (255, 255, 255)], [bytes(400 * 300), bytes([1]) * (400 * 300)], [8, 8]))
        result = gif_audit.audit_file(path, canon.params(), (255, 255, 255))
        self.assertTrue(result["fail"])
        self.assertGreater(result["flashes_per_second"], 3)

    def test_best_verdict_is_never_clean(self):
        """Prevents a passing audit from reading as an all-clear (ADR-007)."""
        a = raster.Canvas(8, 8, (0, 0, 0))
        b = raster.Canvas(8, 8, (51, 51, 51))
        path = self._write(raster.encode_frames([a, b], [60, 60]))
        result = gif_audit.audit_file(path, canon.params(), (255, 255, 255))
        self.assertIn("INCONCLUSIVE", result["verdict"])
        self.assertNotIn("CLEAN", result["verdict"])


class LintTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir)

    def lint(self, html, preset="B", name="index.html", spec_extra=None):
        with open(os.path.join(self.dir, name), "w", encoding="utf-8") as handle:
            handle.write(html)
        spec = canon.era_spec_from_preset(preset)
        spec.update(spec_extra or {})
        return era_lint.lint(self.dir, spec)

    def rules(self, report):
        return {f["rule"] for f in report["findings"]}

    def test_webfont_is_an_error(self):
        """Prevents Google Fonts slipping into a 1998 build through a link tag."""
        report = self.lint(page('<table width="600"><tr><td>x</td></tr></table>', SAFE_HEAD + '<link href="https://fonts.googleapis.com/css2?family=Inter" rel="stylesheet">'))
        self.assertIn("HL001", self.rules(report))
        self.assertEqual(report["verdict"], "FINDINGS")

    def test_safety_layer_files_are_exempt(self):
        """Prevents the modern safety layer failing its own lint (ADR-003)."""
        shutil.copy(os.path.join(ROOT, "kits", "safety-layer", "homestead-safe.css"), self.dir)
        report = self.lint(page('<table width="600"><tr><td>x</td></tr></table>'))
        self.assertNotIn("HL024", self.rules(report))
        self.assertNotIn("HL005", self.rules(report))

    def test_era_mixing_detected(self):
        """Prevents MySpace glitter text appearing on a FrontPage corporate build unnoticed."""
        report = self.lint(page('<table width="760"><tr><td><!-- hs:widget glitter-text --></td></tr></table>'), preset="C")
        self.assertIn("HL022", self.rules(report))

    def test_time_capsule_allows_mixing(self):
        """Prevents the era-mixing rule blocking a declared time capsule story."""
        report = self.lint(page('<table width="760"><tr><td><!-- hs:widget glitter-text --></td></tr></table>'), preset="C", spec_extra={"time_capsule": True})
        self.assertNotIn("HL022", self.rules(report))

    def test_music_note_is_not_emoji(self):
        """Prevents the eighth note used on Turn on music badges from tripping the emoji rule."""
        report = self.lint(page('<table width="600"><tr><td>♪ music ♪</td></tr></table>'))
        self.assertNotIn("HL006", self.rules(report))
        report = self.lint(page('<table width="600"><tr><td>party \U0001F389</td></tr></table>'))
        self.assertIn("HL006", self.rules(report))

    def test_commented_bgsound_is_allowed(self):
        """Prevents the View Source bgsound comment being treated as autoplaying audio."""
        report = self.lint(page('<!-- <bgsound src="a.mid" loop="infinite"> --><table width="600"><tr><td>x</td></tr></table>'))
        self.assertNotIn("HL012", self.rules(report))
        report = self.lint(page('<bgsound src="a.mid"><table width="600"><tr><td>x</td></tr></table>'))
        self.assertIn("HL012", self.rules(report))

    def test_anchor_href_is_not_a_color(self):
        """Prevents href="#add" being read as the off-palette color #AADDDD."""
        report = self.lint(page('<table width="600"><tr><td><a href="#add">add</a></td></tr></table>'))
        self.assertNotIn("HL020", self.rules(report))

    def test_missing_safety_layer_is_an_error(self):
        """Prevents a build shipping without Safe Mode."""
        report = self.lint(page('<table width="600"><tr><td><marquee>hi</marquee></td></tr></table>', head=""))
        self.assertIn("HL015", self.rules(report))
        self.assertIn("HL014", self.rules(report))

    def test_no_findings_is_inconclusive(self):
        """Prevents lint reporting a clean bill when it cannot judge visual authenticity (ADR-007)."""
        report = era_lint.lint(os.path.join(ROOT, "kits", "preset-c-frontpage"), canon.era_spec_from_preset("C"))
        self.assertEqual(report["verdict"], "NO FINDINGS (INCONCLUSIVE)")


class SurveyMapTests(unittest.TestCase):
    def test_survey_detects_example_patterns(self):
        """Prevents survey regressions that dropped cookie banners, chat widgets, and web fonts from the inventory."""
        cwd = os.getcwd()
        os.chdir(ROOT)
        try:
            inv = survey.survey("examples/nimbus-ledger/source/index.html")
        finally:
            os.chdir(cwd)
        ids = {p["id"] for p in inv["patterns"]}
        for expected in ("hero", "cookie-banner", "chat-widget", "testimonials", "pricing", "analytics", "faq"):
            self.assertIn(expected, ids)
        self.assertTrue(inv["brand"]["web_fonts_loaded"])
        self.assertIn("#6D28D9", [c["hex"] for c in inv["brand"]["colors"]])

    def test_sans_serif_is_not_classified_serif(self):
        """Prevents 'sans-serif' matching the serif detector and mapping Inter to Times."""
        self.assertEqual(survey.classify_font("Inter"), "sans")
        self.assertEqual(survey.classify_font("IBM Plex Mono"), "mono")

    def test_mapping_caps_navigation(self):
        """Prevents a twelve-item modern nav becoming a twelve-button period nav."""
        inv = {"patterns": [], "summary": {"nav_items": ["n%d" % i for i in range(12)]},
               "brand": {"colors": [], "fonts": [], "name_guess": "X"}, "pages": [{"headings": [], "ctas": []}]}
        result = mapper.build(inv, canon.era_spec_from_preset("C"))
        self.assertLessEqual(len(result["nav_plan"]), canon.params()["nav_cap_max"])
        self.assertTrue(result["nav_overflow"])


class RubricTests(unittest.TestCase):
    def card(self, scores):
        c = rubric.blank("t", "B")
        for row, score in zip(c["rows"], scores):
            row["score"] = score
            row["evidence"] = "test"
        return c

    def test_band_edges(self):
        """Prevents an off-by-one at the 34 and 26 band edges."""
        self.assertEqual(rubric.evaluate(self.card([1] * 6 + [2] * 14))["verdict"], "SHIP")
        self.assertEqual(rubric.evaluate(self.card([1] * 7 + [2] * 13))["verdict"], "REVISE")
        self.assertEqual(rubric.evaluate(self.card([0] + [1] * 13 + [2] * 6))["verdict"], "REBUILD")

    def test_hard_gate_blocks_ship(self):
        """Prevents a high total shipping a build without Safe Mode."""
        scores = [2] * 20
        scores[17] = 1
        self.assertEqual(rubric.evaluate(self.card(scores))["verdict"], "REVISE")

    def test_lint_errors_cap_rows(self):
        """Prevents an auditor awarding full marks on a row whose lint rule is failing."""
        lint = {"findings": [{"rubric_row": 4, "severity": "error"}]}
        result = rubric.evaluate(self.card([2] * 20), lint)
        self.assertEqual(result["capped_rows"], [4])
        self.assertEqual(result["total"], 39)

    def test_unscored_card_is_incomplete(self):
        """Prevents a blank card being totalled as zero and reported as REBUILD."""
        self.assertEqual(rubric.evaluate(rubric.blank("t", "B"))["verdict"], "INCOMPLETE")


class MediaTests(unittest.TestCase):
    def test_png_roundtrip(self):
        """Prevents the Paeth filter regression that broke dithering of exported screenshots."""
        rows = [[(x * 20 % 256, y * 30 % 256, (x + y) * 10 % 256) for x in range(9)] for y in range(7)]
        w, h, out = png.decode(png.encode_rgb(9, 7, rows))
        self.assertEqual((w, h), (9, 7))
        self.assertEqual([[p[:3] for p in r] for r in out], rows)

    def test_wav_is_not_silent_and_midi_has_header(self):
        """Prevents a volume regression that rendered silent click-to-play tracks."""
        notes = [("C5", 1), ("R", 1)]
        self.assertGreater(audio.silence_check(audio.render_wav(notes)), 10)
        self.assertTrue(audio.render_midi(notes).startswith(b"MThd"))


class ScaffoldTests(unittest.TestCase):
    def test_scaffold_seeds_kit_and_spec(self):
        """Prevents an engagement opening without the safety layer or with the wrong preset spec."""
        import scaffold
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp)
        code = scaffold.main(["new", "demo", "--target", "https://example.com", "--preset", "E", "--root", tmp])
        self.assertEqual(code, 0)
        base = os.path.join(tmp, "demo")
        with open(os.path.join(base, "02-era-spec.json"), "r", encoding="utf-8") as handle:
            self.assertEqual(json.load(handle)["preset"], "E")
        for name in ("homestead-safe.css", "homestead-safe.js", "index.html"):
            self.assertTrue(os.path.isfile(os.path.join(base, "05-build", name)))


if __name__ == "__main__":
    unittest.main()
