"""Build full-figure and detail comparisons from curated native Figma previews."""
from pathlib import Path
from PIL import Image, ImageDraw
from build_showcase_assets import font, place

ROOT = Path(__file__).resolve().parents[1]
BG, INK, MUTED = '#f3f7f5', '#183d32', '#567067'

def crop(im, bounds):
    return im.crop(tuple(round(v * (im.width/1100 if i%2 == 0 else im.height/613))
                         for i, v in enumerate(bounds)))

def build():
    folder = ROOT / 'examples/agentthink-v2'
    reference = Image.open(ROOT/'examples/agentthink/reference.png').convert('RGB')
    versions = [Image.open(folder/name).convert('RGB') for name in ['v1.png', 'v2.png', 'source-assisted.png']]
    if len({im.size for im in versions}) != 1:
        raise ValueError('Native version previews must use the same dimensions')
    images = [reference] + versions
    titles = ['Reference', 'V1', 'V2 | Screenshot reconstruction', 'Source-assisted reconstruction']
    notes = ['Supplied image', 'Initial full reconstruction', 'Complete redraw from the screenshot', 'Rebuilt with matching paper assets']
    hero = Image.new('RGB', (1800, 655), BG); d = ImageDraw.Draw(hero)
    d.text((28,18), 'AgentThink | V1 to V2', font=font(30,True), fill=INK)
    for i,(name,im) in enumerate([('V1',versions[0]),('V2 | Complete screenshot reconstruction',versions[1])]):
        x=25+i*895; d.text((x,72),name,font=font(21,True),fill=INK)
        d.rounded_rectangle((x,112,x+860,604),12,fill='white')
        place(hero,im,(x+8,119,844,478))
    d.text((28,622),'Native Figma previews at the same scale. V2 redraws all four panels.',font=font(18),fill=MUTED)
    hero.save(ROOT/'assets/agentthink-v1-v2.png',optimize=True)
    whole=Image.new('RGB',(2320,1610),BG);d=ImageDraw.Draw(whole)
    d.text((35,20),'AgentThink | Reference, V1 and two reconstruction routes',font=font(36,True),fill=INK)
    for i,(title,note,im) in enumerate(zip(titles,notes,images)):
        x=30+(i%2)*1150;y=100+(i//2)*710
        d.text((x+10,y),title,font=font(28,True),fill=INK)
        d.text((x+10,y+43),note,font=font(23),fill=MUTED)
        place(whole,im,(x+10,y+85,1100,613))
    d.text((40,1535),'V2 uses the supplied screenshot; the source-assisted case uses original embedded paper assets.',font=font(24),fill=MUTED)
    whole.save(ROOT/'assets/agentthink-v2-routes.png',optimize=True)
    rows=[('Compound icons',[(242,145,516,205)]),
          ('Maps and vehicles',[(47,258,200,302)]),
          ('Frozen / Trainable',[(475,440,506,472),(476,506,504,540)]),
          ('Evaluation symbols',[(938,386,974,423),(938,428,974,466),(938,467,974,504),(938,507,974,545),(938,548,974,586)]),
          ('Character contours',[(143,436,200,497),(1022,170,1057,209)])]
    detail=Image.new('RGB',(2000,1640),BG);d=ImageDraw.Draw(detail)
    d.text((30,20),'AgentThink | Whole-workflow detail comparison',font=font(33,True),fill=INK)
    column_titles=['Reference','V1','V2 | Screenshot','Source-assisted']
    for i,title in enumerate(column_titles):d.text((25+i*500,87),title,font=font(25,True),fill=INK)
    for row,(label,bounds) in enumerate(rows):
        y=139+row*282;d.text((25,y),label,font=font(22,True),fill=MUTED)
        for col,im in enumerate(images):
            x=15+500*col;d.rounded_rectangle((x,y+36,x+470,y+260),12,fill='white')
            width=440/len(bounds)
            for j,b in enumerate(bounds):place(detail,crop(im,b),(round(x+15+j*width),y+50,round(width-8),195))
    d.text((25,1578),'Actual full-figure Figma previews. Fine character detail remains approximate.',font=font(21),fill=MUTED)
    detail.save(ROOT/'assets/agentthink-v1-v2-details.png',optimize=True)
    focus=Image.new('RGB',(1600,720),BG);d=ImageDraw.Draw(focus)
    d.text((25,18),'Details | Reference and reconstruction',font=font(29,True),fill=INK)
    for i,(label,im) in enumerate([('Reference',reference),('Reconstructed from a screenshot',versions[1])]):
        y=80+i*305;d.text((28,y),label,font=font(24,True),fill=INK)
        bounds=[(242,145,516,205),(938,386,974,423),(938,428,974,466),(938,507,974,545)]
        boxes=[(25,y+42,760,235),(820,y+42,220,235),(1070,y+42,220,235),(1320,y+42,220,235)]
        for b,box in zip(bounds,boxes):place(focus,crop(im,b),box)
    focus.save(ROOT/'assets/agentthink-v2-focus.png',optimize=True)
    # Public showcase describes the input and result; version history stays in comparison assets.
    public_images=[reference,versions[1],versions[2]]
    public_titles=['Reference','From a screenshot','With original source assets']
    public=Image.new('RGB',(2400,570),BG);d=ImageDraw.Draw(public)
    for i,(label,im) in enumerate(zip(public_titles,public_images)):
        x=20+i*800;d.text((x+12,22),label,font=font(29,True),fill=INK)
        d.rounded_rectangle((x,75,x+760,515),12,fill='white')
        place(public,im,(x+8,83,744,424))
    d.text((32,534),'Text, shapes and connections remain editable.',font=font(22),fill=MUTED)
    public.save(ROOT/'assets/agentthink-reconstruction.png',optimize=True)
    public_detail=Image.new('RGB',(1800,1640),BG);d=ImageDraw.Draw(public_detail)
    d.text((30,20),'AgentThink | Detail comparison',font=font(33,True),fill=INK)
    for i,title in enumerate(public_titles):d.text((25+i*600,87),title,font=font(25,True),fill=INK)
    for row,(label,bounds) in enumerate(rows):
        y=139+row*282;d.text((25,y),label,font=font(22,True),fill=MUTED)
        for col,im in enumerate(public_images):
            x=15+600*col;d.rounded_rectangle((x,y+36,x+570,y+260),12,fill='white')
            width=540/len(bounds)
            for j,b in enumerate(bounds):place(public_detail,crop(im,b),(round(x+15+j*width),y+50,round(width-8),195))
    d.text((25,1578),'Enlarged regions from the figures above.',font=font(21),fill=MUTED)
    public_detail.save(ROOT/'assets/agentthink-reconstruction-details.png',optimize=True)
    print('Built V1/V2 overview, four-way whole figures, five detail groups and focused comparison')

if __name__ == '__main__':
    build()
