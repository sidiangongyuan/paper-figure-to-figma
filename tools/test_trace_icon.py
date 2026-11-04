import importlib.util
import tempfile
import unittest
from pathlib import Path
import xml.etree.ElementTree as ET
from trace_icon import trace_object

AVAILABLE = bool(importlib.util.find_spec('PIL') and importlib.util.find_spec('vtracer'))

@unittest.skipUnless(AVAILABLE, 'Optional Pillow/VTracer dependencies are not installed')
class TraceTests(unittest.TestCase):
    def test_crop_retains_original_coordinate_scale_and_vector_content(self):
        from PIL import Image, ImageDraw
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'source.png';im=Image.new('RGB',(80,60),'white')
            d=ImageDraw.Draw(im);d.ellipse((24,14,54,44),fill='#578d9b');im.save(p)
            svg,meta=trace_object(p,[20,10,60,50],scale=2,remove_flat_background=True)
            r=ET.fromstring(svg)
            self.assertEqual(r.get('viewBox'),'0 0 40 40')
            self.assertTrue(any(n.tag.endswith('path') for n in r.iter()))
            self.assertFalse(any(n.tag.endswith('image') for n in r.iter()))
            self.assertEqual(meta['crop'],[20,10,60,50])
            self.assertEqual(meta['visualReview'],'pending')
            with self.assertRaises(ValueError):trace_object(p,[20,10,90,50])
            reduced,meta=trace_object(p,[20,10,60,50],scale=2,palette_colors=8,remove_flat_background=True)
            self.assertEqual(meta['paletteColors'],8)
            self.assertEqual(ET.fromstring(reduced).get('viewBox'),'0 0 40 40')
            with self.assertRaises(ValueError):trace_object(p,palette_colors=1)

if __name__=='__main__':unittest.main()
