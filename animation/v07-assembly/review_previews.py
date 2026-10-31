from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
R=Path(__file__).resolve().parent;shots=json.loads((R/'shots.json').read_text())
paths=sorted((R/'preview').glob('*.png'));sheet=Image.new('RGB',(1440,270*7),(8,12,20))
for i,p in enumerate(paths):
    f=int(p.stem);sh=next(x for x in shots if x['start']<=f<=x['end'])
    im=Image.open(p).convert('RGBA');cap=Image.open(R/'captions'/f"{sh['key']}.png").resize(im.size,Image.Resampling.LANCZOS)
    im=Image.alpha_composite(im,cap).convert('RGB');im.resize((720,405)).save(R/'preview'/f'captioned-{f:04d}.jpg',quality=93)
    im=im.resize((480,270));sheet.paste(im,((i%3)*480,(i//3)*270))
sheet=sheet.crop((0,0,1440,270*((len(paths)+2)//3)));sheet.save(R/'preview-contact-sheet.jpg',quality=94)
print('Reviewed caption layout on',len(paths),'representative frames')
