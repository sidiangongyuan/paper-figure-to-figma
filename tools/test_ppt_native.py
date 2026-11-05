"""Portable checks for PowerPoint geometry and destructive-operation guards."""
import copy
import tempfile
import unittest
from pathlib import Path
import xml.etree.ElementTree as ET

from ppt_native import NS, native_svg_shape, render


class NativePowerPointTests(unittest.TestCase):
    def shape(self, path, attrs='', viewbox='10 20 100 100'):
        pic = ET.fromstring(f'''<p:pic xmlns:p="{NS['p']}" xmlns:a="{NS['a']}">
          <p:nvPicPr><p:cNvPr id="7" name="curve"/></p:nvPicPr>
          <p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="1270000" cy="1270000"/></a:xfrm></p:spPr>
        </p:pic>''')
        node = {'id': 'curve', 'w': 100, 'opacity': .5,
                'svg': f'<svg viewBox="{viewbox}"><path d="{path}" {attrs}/></svg>'}
        return native_svg_shape(pic, node, 1)

    def scene(self):
        return {'version': 1, 'name': 'test', 'width': 100, 'height': 50,
                'assets': {}, 'nodes': [{'id': 'label', 'type': 'text',
                'x': 0, 'y': 0, 'w': 100, 'h': 30, 'text': 'Label', 'size': 20}]}

    def test_open_curve_preserves_control_points_and_origin(self):
        shape = self.shape('M10 20 C20 30 40 50 60 70', 'fill="none" stroke="#123456"')
        path = shape.find('.//a:path', NS)
        self.assertIsNone(path.find('a:close', NS))
        self.assertEqual(path.get('fill'), 'none')
        points = path.findall('a:cubicBezTo/a:pt', NS)
        self.assertEqual([(p.get('x'), p.get('y')) for p in points],
                         [('10000', '10000'), ('30000', '30000'), ('50000', '50000')])
        self.assertEqual(shape.find('p:nvSpPr/p:cNvPr', NS).get('id'), '7')

    def test_closed_fill_and_opacity(self):
        shape = self.shape('M10 20 L30 40 L10 40 Z', 'fill="#ffffff" fill-opacity="0.5"')
        self.assertIsNotNone(shape.find('.//a:path/a:close', NS))
        self.assertEqual(shape.find('p:spPr/a:solidFill/a:srgbClr/a:alpha', NS).get('val'), '25000')

    def test_stroke_width_and_transparency(self):
        shape = self.shape('M10 20 L30 40', 'fill="none" stroke="#123456" stroke-width="2" stroke-opacity="0.5"')
        line = shape.find('p:spPr/a:ln', NS)
        self.assertEqual(line.get('w'), '25400')
        self.assertEqual(line.find('a:solidFill/a:srgbClr/a:alpha', NS).get('val'), '25000')

    def test_unsupported_and_incomplete_paths_fail(self):
        for path, attrs, viewbox in [('M0 0 Q1 2 3 4', '', '0 0 10 10'),
                                    ('M0', '', '0 0 10 10'),
                                    ('M0 0', 'transform="scale(2)"', '0 0 10 10'),
                                    ('M0 0', '', '0 0 0 10')]:
            with self.subTest(path=path, attrs=attrs, viewbox=viewbox), self.assertRaises(ValueError):
                self.shape(path, attrs, viewbox)

    def test_all_output_paths_are_protected_before_com(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / 'test.pptx'
            for suffix in ('.pptx', '.png', '.report.json'):
                existing = output.with_suffix(suffix)
                existing.write_bytes(b'keep me')
                with self.assertRaises(FileExistsError):
                    render(self.scene(), output)
                self.assertEqual(existing.read_bytes(), b'keep me')
                existing.unlink()

    def test_scaled_fonts_and_small_runs_fail_before_com(self):
        with tempfile.TemporaryDirectory() as folder:
            scene = self.scene()
            scene['ppt'] = {'pointsPerUnit': .5}
            with self.assertRaisesRegex(ValueError, 'font below minimum'):
                render(scene, Path(folder) / 'scaled.pptx')
            scene = self.scene()
            scene['nodes'][0]['runs'] = [{'start': 0, 'length': 1, 'size': 10}]
            with self.assertRaisesRegex(ValueError, 'font below minimum'):
                render(scene, Path(folder) / 'runs.pptx')

    def test_invalid_slide_dimensions_fail_before_com(self):
        with tempfile.TemporaryDirectory() as folder:
            scene = self.scene()
            scene['width'] = 5000
            with self.assertRaisesRegex(ValueError, '56 inches'):
                render(scene, Path(folder) / 'large.pptx')


if __name__ == '__main__':
    unittest.main()
