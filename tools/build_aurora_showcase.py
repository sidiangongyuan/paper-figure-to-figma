"""Build Aurora comparisons from the reference and reviewed Figma previews."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / 'examples' / 'aurora'
ASSETS = ROOT / 'assets'


def font(size):
    for family in ('DejaVuSans.ttf', 'Arial.ttf', 'C:/Windows/Fonts/arial.ttf'):
        try:
            return ImageFont.truetype(family, size)
        except OSError:
            pass
    return ImageFont.load_default()


def main():
    images = [Image.open(EXAMPLE / name).convert('RGB') for name in
              ('reference.png', 'screenshot.png', 'source-assisted.png')]
    labels = ('Reference', 'From a screenshot', 'With paper source')
    width, height, gap, margin, header = 1092, 998, 24, 24, 72
    sheet = Image.new('RGB', (width * 3 + gap * 2 + margin * 2, height + header + margin), 'white')
    draw = ImageDraw.Draw(sheet)
    for i, (im, label) in enumerate(zip(images, labels)):
        x = margin + i * (width + gap)
        draw.text((x + 12, 20), label, font=font(30), fill='#21354a')
        sheet.paste(im.resize((width, height), Image.Resampling.LANCZOS), (x, header))
    sheet.save(ASSETS / 'aurora-reconstruction.png', optimize=True)

    # Crop in reference coordinates; source previews are twice the reference resolution.
    regions = [('Domain illustrations', (187, 236, 387, 435)),
               ('Series curves and rotated labels', (88, 128, 285, 318)),
               ('Modalities and training symbols', (610, 674, 878, 975)),
               ('Aurora illustration', (940, 815, 1055, 965))]
    cell_w, cell_h, row_title = 520, 430, 48
    details = Image.new('RGB', (3 * cell_w + 4 * gap, header + len(regions) * (cell_h + row_title) + gap), 'white')
    draw = ImageDraw.Draw(details)
    for i, label in enumerate(labels):
        draw.text((gap + i * (cell_w + gap), 20), label, font=font(25), fill='#21354a')
    for row, (title, bounds) in enumerate(regions):
        top = header + row * (cell_h + row_title)
        draw.text((gap, top), title, font=font(24), fill='#455b68')
        for i, im in enumerate(images):
            scale = im.width / width
            crop = im.crop(tuple(round(v * scale) for v in bounds))
            ratio = min((cell_w - 24) / crop.width, (cell_h - 24) / crop.height)
            crop = crop.resize((round(crop.width * ratio), round(crop.height * ratio)), Image.Resampling.LANCZOS)
            x = gap + i * (cell_w + gap)
            draw.rounded_rectangle((x, top + row_title, x + cell_w, top + row_title + cell_h - 8), radius=12, fill='#f4f7f9')
            details.paste(crop, (x + (cell_w - crop.width) // 2, top + row_title + (cell_h - crop.height) // 2))
    details.save(ASSETS / 'aurora-reconstruction-details.png', optimize=True)


if __name__ == '__main__':
    main()
