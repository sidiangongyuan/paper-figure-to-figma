"""Extract original bitmap objects from one PDF page, preserving transparency and placements."""
from pathlib import Path
import argparse
import hashlib
import io
import json


def extract(pdf, output, page_number, source_url=None):
    try:
        import fitz
        from PIL import Image
    except ImportError as error:
        raise RuntimeError('PDF asset extraction needs PyMuPDF and Pillow in the task environment') from error
    pdf, output = Path(pdf), Path(output)
    if output.exists():
        raise FileExistsError('Choose a new extraction directory; existing assets are retained')
    with fitz.open(pdf) as doc:
        if doc.needs_pass:
            raise ValueError('Supply an accessible PDF; this helper does not unlock documents')
        if not isinstance(page_number, int) or not 1 <= page_number <= len(doc):
            raise ValueError('Page number must be between 1 and the PDF page count')
        page = doc[page_number - 1]
        manifest = {'source': source_url or pdf.name,
                    'sourceSha256': hashlib.sha256(pdf.read_bytes()).hexdigest(),
                    'page': page_number, 'pageSizePoints': [page.rect.width, page.rect.height],
                    'vectorDrawingCount': len(page.get_drawings()),
                    'images': [], 'review': 'Select objects matching the reference before reconstruction'}
        output.mkdir(parents=True)
        seen = set()
        for item in page.get_images(full=True):
            xref, smask = item[:2]
            if xref in seen:
                continue
            seen.add(xref)
            placements = page.get_image_rects(xref)
            if not placements:
                continue
            data = doc.extract_image(xref)
            with Image.open(io.BytesIO(data['image'])) as original:
                image = original.convert('RGBA')
            if smask:
                with Image.open(io.BytesIO(doc.extract_image(smask)['image'])) as mask:
                    if mask.size != image.size:
                        raise ValueError('Image and transparency mask have different dimensions')
                    image.putalpha(mask.convert('L'))
            name = f'image-{xref}.png'
            image.save(output / name)
            manifest['images'].append({'file': name, 'xref': xref, 'maskXref': smask,
                                       'width': image.width, 'height': image.height,
                                       'placementsPoints': [list(r) for r in placements],
                                       'representation': 'bitmap',
                                       'sha256': hashlib.sha256((output / name).read_bytes()).hexdigest()})
        (output / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--page', required=True, type=int, help='One-based page number')
    parser.add_argument('--source-url', help='Original source URL for provenance; not fetched by this helper')
    args = parser.parse_args()
    manifest = extract(args.pdf, args.output, args.page, args.source_url)
    print(json.dumps({'page': manifest['page'], 'imageObjects': len(manifest['images']),
                      'manifest': str(args.output / 'manifest.json')}))


if __name__ == '__main__':
    main()
