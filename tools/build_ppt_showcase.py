"""Build the PowerPoint showcase from reviewed exports and real selection screenshots."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]
def font(size,bold=False):
 for name in (('DejaVuSans-Bold.ttf','arialbd.ttf') if bold else ('DejaVuSans.ttf','arial.ttf')):
  try:return ImageFont.truetype(name,size)
  except OSError:pass
 return ImageFont.load_default()
def place(canvas,path,box):
 im=Image.open(path).convert('RGB');x,y,w,h=box;ratio=min(w/im.width,h/im.height);im=im.resize((round(im.width*ratio),round(im.height*ratio)),Image.Resampling.LANCZOS);canvas.paste(im,(round(x+(w-im.width)/2),round(y+(h-im.height)/2)))
def build():
 im=Image.new('RGB',(2000,1110),'#101b2d');d=ImageDraw.Draw(im)
 d.rounded_rectangle((48,42,110,104),radius=13,fill='#d65b35');d.text((64,45),'P',font=font(42,True),fill='white')
 d.text((134,42),'POWERPOINT',font=font(23,True),fill='#f1a47e');d.text((134,76),'Native text. Editable shapes.',font=font(36,True),fill='white')
 d.rounded_rectangle((1683,48,1950,95),radius=23,fill='#263449');d.text((1710,58),'Windows + PowerPoint',font=font(18),fill='#ecf0f6')
 d.text((48,145),'Research figures you can keep editing.',font=font(43,True),fill='white')
 d.text((50,204),'Actual PowerPoint results and object-selection screenshots.',font=font(23),fill='#a9b8cf')
 for x,w,title,folder in [(48,720,'Aurora','aurora'),(798,1152,'P-GenRM','pgenrm')]:
  d.rounded_rectangle((x,266,x+w,1021),radius=20,fill='#ffffff')
  d.text((x+25,285),title,font=font(29,True),fill='#17253a')
  d.text((x+25,329),'Edit text / move objects / refine layout',font=font(18),fill='#65758a')
  place(im,R/'examples'/folder/'powerpoint-selected.png',(x+20,375,w-40,505))
  d.line((x+25,904,x+w-25,904),fill='#e0e6ed',width=2)
  stats='83 text boxes  /  64 native shapes' if folder=='aurora' else '69 text boxes  /  122 native shapes'
  d.text((x+25,929),stats,font=font(23,True),fill='#b7472a')
  d.text((x+25,971),'Complex illustrations remain independent SVG objects.',font=font(17),fill='#536177')
 d.text((50,1058),'Paper Figure to Figma   /   One skill. Figma or PowerPoint.',font=font(24),fill='#d4deed')
 im.save(R/'assets/powerpoint-showcase.png',optimize=True)
 for folder in ['aurora','pgenrm']:
  s=Image.new('RGB',(2400,930 if folder=='aurora' else 740),'#f1f4f8');dr=ImageDraw.Draw(s)
  dr.text((32,23),'Reference',font=font(27,True),fill='#21354a');dr.text((1232,23),'Native PowerPoint result',font=font(27,True),fill='#b7472a')
  for x,file in [(20,'reference.png'),(1220,'powerpoint.png')]:place(s,R/'examples'/folder/file,(x,80,1160,s.height-104))
  s.save(R/f'assets/{folder}-powerpoint.png',optimize=True)
if __name__=='__main__':build()
