from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
R=Path(__file__).resolve().parent
files=sorted((R/'checks').glob('*.png'));assert len(files)==16
sheet=Image.new('RGB',(1280,800));d=ImageDraw.Draw(sheet);means={}
for i,f in enumerate(files):
    im=Image.open(f);means[f.stem]=float(np.asarray(im.resize((160,90)),dtype=float).mean())
    assert means[f.stem]>5,f
    im.thumbnail((320,180));sheet.paste(im,((i%4)*320,(i//4)*200));d.text(((i%4)*320,(i//4)*200+180),f.stem,fill='white')
for f in ('0260','0462'):
    n=int(f);delta=abs(means[f]-(means[f'{n-1:04d}']+means[f'{n+1:04d}'])/2)
    assert delta<2,(f,delta)
sheet.save(R/'regression-contact-sheet.jpg',quality=92)
(R/'regression-validation.json').write_text(json.dumps({'frames':16,'brightness':means,'previous_black_frames_pass':True},indent=2))
