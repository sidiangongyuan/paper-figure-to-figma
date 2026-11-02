"""Lay out comparison images from the committed reference and native Figma preview."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT=Path(__file__).resolve().parents[1]

def font(size,bold=False):
    candidates=['DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf',
                'C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf']
    for path in candidates:
        try:return ImageFont.truetype(path,size)
        except OSError:pass
    return ImageFont.load_default()

def place(canvas,im,box):
    x,y,w,h=box
    im=ImageOps.contain(im.convert('RGB'),(w,h),Image.Resampling.LANCZOS)
    canvas.paste(im,(x+(w-im.width)//2,y+(h-im.height)//2))

def build():
    reference=Image.open(ROOT/'examples/planwam/reference.png').convert('RGB')
    result=Image.open(ROOT/'assets/figma-result.png').convert('RGB')
    canvas=Image.new('RGB',(1600,410),'#f4f6fa');d=ImageDraw.Draw(canvas)
    d.text((30,20),'PlanWAM',font=font(27,True),fill='#17243a')
    d.text((30,62),'REFERENCE',font=font(18,True),fill='#58687c')
    d.text((820,62),'EDITABLE RECONSTRUCTION',font=font(18,True),fill='#176f77')
    for x in [24,814]:d.rounded_rectangle((x,94,x+762,372),radius=10,fill='white',outline='#dbe2ea')
    place(canvas,reference,(30,100,750,264));place(canvas,result,(820,100,750,264))
    d.text((30,384),'43 editable text layers  /  334 vector objects  /  RGB input and output crops retained',font=font(16),fill='#58687c')
    canvas.save(ROOT/'assets/planwam-comparison.png',optimize=True)

    regions=[('Curved connections',(489,207,577,298)),
             ('Gradients & dashed strokes',(742,201,829,256)),
             ('Text backings & layer order',(874,47,961,147))]
    detail=Image.new('RGB',(1440,600),'#f4f6fa');d=ImageDraw.Draw(detail)
    d.text((26,18),'Detail comparison',font=font(26,True),fill='#17243a')
    for i,(title,rect) in enumerate(regions):
        x=24+i*476
        d.rounded_rectangle((x,70,x+456,578),radius=12,fill='white',outline='#dbe2ea')
        d.text((x+18,88),title,font=font(20,True),fill='#17243a')
        d.text((x+18,128),'Reference',font=font(16),fill='#58687c')
        place(detail,reference.crop(rect),(x+18,154,420,170))
        d.line((x+18,340,x+438,340),fill='#e4e9ef',width=1)
        d.text((x+18,352),'Reconstruction',font=font(16),fill='#176f77')
        mapped=tuple(round(v*(result.width/reference.width if j%2==0 else result.height/reference.height)) for j,v in enumerate(rect))
        place(detail,result.crop(mapped),(x+18,380,420,180))
    detail.save(ROOT/'assets/planwam-details.png',optimize=True)
    print('Built comparison and detail assets from existing source images')

def build_agentthink():
    case=ROOT/'examples/agentthink'
    reference=Image.open(case/'reference.png').convert('RGB')
    result=Image.open(case/'preview.png').convert('RGB')
    canvas=Image.new('RGB',(1600,560),'#f4f6fa');d=ImageDraw.Draw(canvas)
    d.text((30,20),'AgentThink',font=font(27,True),fill='#17243a')
    d.text((30,62),'REFERENCE',font=font(18,True),fill='#58687c')
    d.text((820,62),'EDITABLE RECONSTRUCTION',font=font(18,True),fill='#176f77')
    for x in [24,814]:d.rounded_rectangle((x,94,x+762,520),radius=10,fill='white',outline='#dbe2ea')
    place(canvas,reference,(30,100,750,414));place(canvas,result,(820,100,750,414))
    d.text((30,534),'59 editable text layers  /  264 vector path nodes  /  0 bitmap fills',font=font(16),fill='#58687c')
    canvas.save(ROOT/'assets/agentthink-comparison.png',optimize=True)
    regions=[('Editable model blocks',(265,432,538,555)),
             ('Branching paths',(565,325,730,408)),
             ('Reward layers',(738,310,890,395))]
    detail=Image.new('RGB',(1440,600),'#f4f6fa');d=ImageDraw.Draw(detail)
    d.text((26,18),'AgentThink details',font=font(26,True),fill='#17243a')
    for i,(title,rect) in enumerate(regions):
        x=24+i*476
        d.rounded_rectangle((x,70,x+456,578),radius=12,fill='white',outline='#dbe2ea')
        d.text((x+18,88),title,font=font(20,True),fill='#17243a')
        d.text((x+18,128),'Reference',font=font(16),fill='#58687c')
        place(detail,reference.crop(rect),(x+18,154,420,170))
        d.line((x+18,340,x+438,340),fill='#e4e9ef',width=1)
        d.text((x+18,352),'Reconstruction',font=font(16),fill='#176f77')
        mapped=tuple(round(v*(result.width/reference.width if j%2==0 else result.height/reference.height)) for j,v in enumerate(rect))
        place(detail,result.crop(mapped),(x+18,380,420,180))
    detail.save(ROOT/'assets/agentthink-details.png',optimize=True)
    print('Built AgentThink comparison assets')

if __name__=='__main__':
    build()
    build_agentthink()
