import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
import motion_review


class MotionReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = Path(tempfile.mkdtemp(prefix="motion-review-"))
        self.assemblies = self.temp / "assemblies"
        self.assemblies.mkdir()
        self.loop_dir = self._make_assembly("loop", True, [100, 120], [(255, 0, 0, 255), (0, 255, 0, 255)])
        self.shot_dir = self._make_assembly("shot", False, [80, 80], [(0, 0, 255, 255), (0, 0, 255, 255)])
        self.comparison = self.temp / "comparison.json"
        self._write_comparison(
            [
                {"id": "loop", "title": "Loop", "assembly": "assemblies/loop", "source_label": "source <alpha>", "review": "hold", "notes": "manual note"},
                {"id": "shot", "title": "One shot", "assembly": "assemblies/shot", "source_label": "source two"},
            ]
        )

    def tearDown(self):
        shutil.rmtree(self.temp, ignore_errors=True)

    def _make_assembly(self, name, repeat, durations, colors):
        directory = self.assemblies / name
        directory.mkdir()
        for index, color in enumerate(colors):
            Image.new("RGBA", (2, 2), color).save(directory / f"frame_{index:03}.png")
        assembly = {
            "canvas": [2, 2],
            "repeat_for_preview": repeat,
            "frames": [{"duration_ms": duration} for duration in durations],
        }
        (directory / "assembly.json").write_text(json.dumps(assembly), encoding="utf-8")
        return directory

    def _write_comparison(self, sequences):
        self.comparison.write_text(
            json.dumps({"title": "Test comparison", "background": "black", "sequences": sequences}),
            encoding="utf-8",
        )

    def test_build_preserves_input_hashes_and_writes_diagnostics(self):
        before = {}
        for path in [self.comparison, *self.loop_dir.glob("*"), *self.shot_dir.glob("*")]:
            before[path] = hashlib.sha256(path.read_bytes()).hexdigest()
        output = self.temp / "out"
        diagnostics = motion_review.build(self.comparison, output)
        self.assertEqual(diagnostics["visual_acceptance"], "not_assessed")
        self.assertTrue((output / "index.html").is_file())
        self.assertTrue((output / "diagnostics.json").is_file())
        for path, digest in before.items():
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), digest, str(path))

    def test_loop_and_one_shot_data_and_duplicate_frames(self):
        diagnostics = motion_review.build(self.comparison, self.temp / "out")
        by_id = {item["id"]: item for item in diagnostics["sequences"]}
        self.assertEqual(by_id["loop"]["playback_semantics"], "loop")
        self.assertEqual(by_id["shot"]["playback_semantics"], "one-shot")
        self.assertEqual(by_id["shot"]["identical_pixel_frame_pairs"], [{"first": 0, "second": 1}])
        self.assertIn("not a quality", by_id["loop"]["loop_end_to_start_difference"]["note"])
        self.assertEqual(by_id["loop"]["loop_end_to_start_difference"]["difference_bbox"], [0, 0, 2, 2])

    def test_labels_are_script_safe_and_rendered_as_text(self):
        output = self.temp / "out"
        motion_review.build(self.comparison, output)
        html = (output / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("<alpha>", html)
        self.assertIn(r"\u003c", html)
        self.assertIn("textContent", html)
        self.assertIn("displayScale", html)
        self.assertIn("Restart", html)
        self.assertIn("Restart all", html)
        self.assertIn("currentCycleTime", html)
        self.assertIn("stepIndices", html)
        self.assertIn("After frame stepping, Start restarts all sequences", html)
        self.assertIn("cycle", html)
        self.assertIn("Notes:", html)

    def test_duplicate_sequence_ids_rejected(self):
        self._write_comparison(
            [
                {"id": "same", "assembly": "assemblies/loop"},
                {"id": "same", "assembly": "assemblies/shot"},
            ]
        )
        with self.assertRaises(motion_review.ReviewError):
            motion_review.build(self.comparison, self.temp / "duplicate")

    def test_nonempty_output_is_not_overwritten(self):
        output = self.temp / "existing"
        output.mkdir()
        sentinel = output / "sentinel.txt"
        sentinel.write_text("keep", encoding="utf-8")
        with self.assertRaises(motion_review.ReviewError):
            motion_review.build(self.comparison, output)
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")

    def test_invalid_duration_size_and_missing_frame_rejected_without_output(self):
        invalids = []
        bad_duration = self._make_assembly("bad-duration", False, [9], [(1, 1, 1, 255)])
        invalids.append(("assemblies/bad-duration", "duration"))
        bad_size = self.assemblies / "bad-size"
        bad_size.mkdir()
        Image.new("RGBA", (3, 2), (1, 1, 1, 255)).save(bad_size / "frame_000.png")
        (bad_size / "assembly.json").write_text(json.dumps({"canvas": [2, 2], "frames": [{"duration_ms": 10}]}), encoding="utf-8")
        invalids.append(("assemblies/bad-size", "size"))
        missing = self.assemblies / "missing"
        missing.mkdir()
        (missing / "assembly.json").write_text(json.dumps({"canvas": [2, 2], "frames": [{"duration_ms": 10}]}), encoding="utf-8")
        invalids.append(("assemblies/missing", "missing"))
        for assembly, _label in invalids:
            self._write_comparison([{"id": "bad", "assembly": assembly}])
            output = self.temp / ("out-" + _label)
            with self.assertRaises(motion_review.ReviewError):
                motion_review.build(self.comparison, output)
            self.assertFalse(output.exists(), _label)


if __name__ == "__main__":
    unittest.main()
