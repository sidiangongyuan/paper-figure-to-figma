"""Combine actual browser-recorded frames into the repository demo GIF."""
import argparse
from pathlib import Path
from PIL import Image


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('frames',type=Path)
    parser.add_argument('output',type=Path)
    parser.add_argument('--width',type=int,default=1100)
    parser.add_argument('--duration',type=int,default=180)
    args=parser.parse_args()
    images=[]
    for path in sorted(args.frames.glob('frame-*.png')):
        with Image.open(path) as source:
            height=round(source.height*args.width/source.width)
            frame=source.convert('RGB').resize((args.width,height),Image.Resampling.LANCZOS)
            images.append(frame.quantize(colors=96,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE))
    if len(images)<2:parser.error('At least two browser frames are required')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    images[0].save(args.output,save_all=True,append_images=images[1:],loop=0,duration=[args.duration]*(len(images)-1)+[1400],optimize=True,disposal=2)
    print(f'{len(images)} frames; {args.output.stat().st_size:,} bytes; {args.output}')


if __name__=='__main__':main()
