"""Combine actual browser-recorded frames into the repository demo GIF."""
import argparse
from pathlib import Path
from PIL import Image


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('frames',type=Path,help='Browser frame directory or an existing GIF to retime')
    parser.add_argument('output',type=Path)
    parser.add_argument('--width',type=int,default=1100)
    parser.add_argument('--duration',type=int,default=360,help='Milliseconds per browser frame')
    parser.add_argument('--slowdown',type=float,default=2,help='Duration multiplier for an existing GIF')
    parser.add_argument('--first-hold',type=int,default=1200)
    parser.add_argument('--last-hold',type=int,default=2800)
    args=parser.parse_args()
    if min(args.duration,args.first_hold,args.last_hold,args.slowdown)<=0:
        parser.error('Durations and slowdown must be positive')
    images=[];durations=[]
    if args.frames.is_file():
        with Image.open(args.frames) as source:
            if source.format!='GIF':parser.error('An existing animation must be a GIF')
            for index in range(source.n_frames):
                source.seek(index)
                images.append(source.convert('RGB').quantize(colors=96,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE))
                durations.append(max(10,round(source.info.get('duration',180)*args.slowdown/10)*10))
    else:
        for path in sorted(args.frames.glob('frame-*.png')):
            with Image.open(path) as source:
                height=round(source.height*args.width/source.width)
                frame=source.convert('RGB').resize((args.width,height),Image.Resampling.LANCZOS)
                images.append(frame.quantize(colors=96,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE))
                durations.append(args.duration)
    if len(images)<2:parser.error('At least two browser frames are required')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    durations[0]=max(durations[0],args.first_hold)
    durations[-1]=max(durations[-1],args.last_hold)
    images[0].save(args.output,save_all=True,append_images=images[1:],loop=0,duration=durations,optimize=True,disposal=2)
    print(f'{len(images)} frames; {sum(durations)/1000:.2f} seconds; {args.output.stat().st_size:,} bytes; {args.output}')


if __name__=='__main__':main()
