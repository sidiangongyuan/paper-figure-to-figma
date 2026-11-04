"""Trace an isolated reference object; outputs SVG paths, never a raster-filled SVG."""
from pathlib import Path
import argparse
import hashlib
import json
import math
import tempfile
import xml.etree.ElementTree as ET
from icon_assets import normalize_svg, NS

def trace_object(source, crop=None, scale=1, filter_speckle=4, color_precision=6,
                 layer_difference=16, remove_flat_background=False, path_precision=2, palette_colors=None):
    try:
        from PIL import Image
        import vtracer
    except ImportError as error:
        raise RuntimeError('Local tracing needs Pillow and vtracer (tested: 0.6.15); use a task environment or another vector source') from error
    if not math.isfinite(scale) or not 1 <= scale <= 8:
        raise ValueError('Scale must be between 1 and 8; enlargement does not restore missing detail')
    if palette_colors is not None and (not isinstance(palette_colors, int) or not 2 <= palette_colors <= 256):
        raise ValueError('Palette size must be an integer between 2 and 256')
    for value, low, high in [(filter_speckle,0,128),(color_precision,1,8),(layer_difference,0,255),(path_precision,0,4)]:
        if not isinstance(value,int) or not low <= value <= high:
            raise ValueError('Tracing parameter outside supported range')
    with Image.open(source) as original:
        original_size = original.size
        bounds = crop or [0,0,*original_size]
        if len(bounds) != 4 or any(not isinstance(v,int) for v in bounds):
            raise ValueError('Crop must be four integer source-pixel coordinates')
        x,y,right,bottom = bounds
        if x<0 or y<0 or right<=x or bottom<=y or right>original.width or bottom>original.height:
            raise ValueError('Crop falls outside the source image')
        image = original.convert('RGBA').crop(bounds)
    w,h=image.size
    # Inspect the real, unscaled corner colors before deciding whether a flat backing can be removed.
    corners=[image.getpixel((u,v)) for u,v in [(0,0),(w-1,0),(0,h-1),(w-1,h-1)]]
    uniform=all(c[3]==255 and sum((c[k]-corners[0][k])**2 for k in range(3))<100 for c in corners)
    target=(round(w*scale),round(h*scale))
    resized=image.resize(target,Image.Resampling.LANCZOS) if target!=image.size else image
    if palette_colors is not None:
        resized=resized.quantize(colors=palette_colors,method=Image.Quantize.FASTOCTREE).convert('RGBA')
    with tempfile.TemporaryDirectory(prefix='figure-trace-') as temp:
        inp=Path(temp)/'object.png'; dest=Path(temp)/'object.svg'; resized.save(inp)
        vtracer.convert_image_to_svg_py(str(inp),str(dest),colormode='color',hierarchical='stacked',
            mode='spline',filter_speckle=filter_speckle,color_precision=color_precision,
            layer_difference=layer_difference,corner_threshold=60,length_threshold=4,
            max_iterations=10,splice_threshold=45,path_precision=path_precision)
        root=ET.parse(dest).getroot()
    removed=False
    if remove_flat_background and uniform and len(root):
        first=root[0];color=first.get('fill','')
        if first.tag.split('}')[-1]=='path' and len(color)==7 and color.startswith('#'):
            rgb=[int(color[k:k+2],16) for k in [1,3,5]]
            if sum((rgb[k]-corners[0][k])**2 for k in range(3))<1600:
                root.remove(first);removed=True
    svg=ET.Element('{'+NS+'}svg',{'viewBox':f'0 0 {w} {h}'})
    group=ET.SubElement(svg,'{'+NS+'}g',{'id':'traced-object','transform':f'scale({w/target[0]} {h/target[1]})'})
    for child in root:group.append(child)
    output=normalize_svg(ET.tostring(svg,encoding='unicode'))
    from importlib.metadata import version
    metadata={'method':'local-trace','source':Path(source).name,'sourceSha256':hashlib.sha256(Path(source).read_bytes()).hexdigest(),
              'referenceSize':original_size,'crop':bounds,'scale':scale,'filterSpeckle':filter_speckle,
              'colorPrecision':color_precision,'layerDifference':layer_difference,'pathPrecision':path_precision,'vtracerVersion':version('vtracer'),
              'paletteColors':palette_colors,
              'removedFlatBackground':removed,'visualReview':'pending','license':'retain source image terms',
              'outputSha256':hashlib.sha256(output.encode()).hexdigest()}
    return output,metadata

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('source',type=Path);p.add_argument('output',type=Path)
    p.add_argument('--crop',type=int,nargs=4);p.add_argument('--scale',type=float,default=1)
    p.add_argument('--filter-speckle',type=int,default=4);p.add_argument('--color-precision',type=int,default=6)
    p.add_argument('--layer-difference',type=int,default=16);p.add_argument('--remove-flat-background',action='store_true')
    p.add_argument('--palette-colors',type=int,help='Optional palette reduction for flat-colored artwork; inspect detail loss')
    p.add_argument('--path-precision',type=int,default=2)
    a=p.parse_args()
    if a.output.exists() or a.output.with_suffix('.source.json').exists():raise FileExistsError('Choose a new output path')
    svg,info=trace_object(a.source,a.crop,a.scale,a.filter_speckle,a.color_precision,a.layer_difference,a.remove_flat_background,a.path_precision,a.palette_colors)
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(svg,encoding='utf-8')
    a.output.with_suffix('.source.json').write_text(json.dumps(info,indent=2),encoding='utf-8')
    print(json.dumps({'svg':str(a.output),'crop':info['crop'],'visualReview':'pending'}))

if __name__=='__main__':main()
