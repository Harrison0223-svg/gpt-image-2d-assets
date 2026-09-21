"""Offline invariant tests; fixtures are test pixels, not generated game art."""
import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image
from asset_tools import measure, inspect, assemble


class AssetToolsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.source = self.root / 'source.png'
        im = Image.new('RGBA', (4, 2), (9, 8, 7, 0))
        im.putpixel((1, 0), (120, 50, 30, 253))
        im.putpixel((2, 0), (0, 180, 160, 128))
        im.save(self.source)
        self.job = self.root / 'sequence.json'
        self.spec = {'canvas': [4, 2], 'frames': [
            {'source': 'source.png', 'crop': [0, 0, 2, 2], 'offset': [1, 0], 'duration_ms': 120},
            {'source': 'source.png', 'crop': [2, 0, 4, 2], 'offset': [0, 0], 'duration_ms': 80}]}

    def tearDown(self):
        self.tmp.cleanup()

    def run_job(self, name='out'):
        self.job.write_text(json.dumps(self.spec), encoding='utf-8')
        return assemble(self.job, self.root / name)

    def test_alpha_is_not_255_presence(self):
        result = measure(self.source)
        self.assertEqual(result['alpha_extrema'], [0, 253])
        self.assertEqual(result['opaque_pixels'], 0)
        self.assertEqual(result['content_state'], 'has_transparency')
        opaque = self.root / 'opaque.png'
        Image.new('RGB', (2, 2), 'white').save(opaque)
        self.assertEqual(measure(opaque)['content_state'], 'fully_opaque')
        self.assertFalse(measure(opaque)['has_alpha_metadata'])
        empty = self.root / 'empty.png'
        Image.new('RGBA', (2, 2)).save(empty)
        self.assertEqual(measure(empty)['content_state'], 'empty')

    def test_exact_crop_padding_and_time(self):
        before = self.source.read_bytes()
        result = self.run_job()
        with Image.open(self.root / 'out/frame_000.png') as f:
            self.assertEqual(f.getpixel((2, 0)), (120, 50, 30, 253))
            self.assertEqual(f.getpixel((1, 0)), (9, 8, 7, 0))
            self.assertEqual(f.getpixel((0, 0)), (0, 0, 0, 0))
        self.assertEqual(result['gif']['decoded_total_ms'], 200)
        self.assertIsNone(result['gif']['loop_extension'])
        self.assertEqual(before, self.source.read_bytes())

    def test_invalid_crop_and_timing_write_nothing(self):
        for patch in [{'crop': [0, 0, 5, 2]}, {'offset': [3, 0]}, {'duration_ms': 15}]:
            original = dict(self.spec['frames'][0])
            self.spec['frames'][0].update(patch)
            with self.assertRaises(ValueError):
                self.run_job()
            self.assertFalse((self.root / 'out').exists())
            self.spec['frames'][0] = original

    def test_existing_outputs_are_not_overwritten(self):
        out = self.root / 'out'
        out.mkdir()
        sentinel = out / 'keep.txt'
        sentinel.write_text('keep')
        with self.assertRaises(ValueError):
            self.run_job()
        with self.assertRaises(ValueError):
            inspect(self.source, out)
        self.assertEqual(sentinel.read_text(), 'keep')

    def test_repeated_identical_frames_preserve_total_duration(self):
        self.spec['repeat'] = True
        self.spec['frames'][1] = dict(self.spec['frames'][0], duration_ms=80)
        result = self.run_job()
        self.assertEqual(result['gif']['decoded_total_ms'], 200)
        self.assertEqual(result['gif']['loop_extension'], 0)
        self.assertEqual(len(list((self.root / 'out').glob('frame_*.png'))), 2)


if __name__ == '__main__':
    unittest.main()
