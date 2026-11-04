import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
from extract_pdf_assets import extract

AVAILABLE = bool(importlib.util.find_spec('fitz') and importlib.util.find_spec('PIL'))


@unittest.skipUnless(AVAILABLE, 'Optional PyMuPDF/Pillow dependencies are not installed')
class PdfAssetTests(unittest.TestCase):
    def test_native_pixels_transparency_and_repeated_placements(self):
        import fitz
        from PIL import Image
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            image = Image.new('RGBA', (32, 24), (200, 30, 50, 0))
            image.putpixel((12, 8), (200, 30, 50, 255))
            buffer = io.BytesIO(); image.save(buffer, format='PNG')
            doc = fitz.open(); doc.new_page(width=200, height=200)
            page = doc.new_page(width=200, height=200)
            xref = page.insert_image(fitz.Rect(10, 20, 74, 68), stream=buffer.getvalue())
            page.insert_image(fitz.Rect(90, 100, 154, 148), xref=xref)
            doc.save(root / 'paper.pdf'); doc.close()
            result = extract(root / 'paper.pdf', root / 'objects', 2, 'https://example.org/paper.pdf')
            self.assertEqual(len(result['images']), 1)
            info = result['images'][0]
            self.assertEqual((info['width'], info['height']), (32, 24))
            self.assertEqual(len(info['placementsPoints']), 2)
            self.assertEqual(info['representation'], 'bitmap')
            with Image.open(root / 'objects' / info['file']) as actual:
                self.assertEqual(actual.getpixel((12, 8)), (200, 30, 50, 255))
                self.assertEqual(actual.getpixel((0, 0))[3], 0)
            with self.assertRaises(FileExistsError):
                extract(root / 'paper.pdf', root / 'objects', 2)
            with self.assertRaises(ValueError):
                extract(root / 'paper.pdf', root / 'invalid-page', 3)
            self.assertFalse((root / 'invalid-page').exists())
            empty = extract(root / 'paper.pdf', root / 'empty-page', 1)
            self.assertEqual(empty['images'], [])


if __name__ == '__main__':
    unittest.main()
