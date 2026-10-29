from pathlib import Path
import numpy as np,json
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent
files=sorted((R.parent/'v04-metallic/frames').glob('*.png'))
a=np.array([np.asarray(Image.open(f).resize((160,90)),dtype=float) for f in files])
mean=a.mean((1,2,3));change=np.abs(np.diff(a,axis=0)).mean((1,2,3))
spike=np.abs(mean[1:-1]-(mean[:-2]+mean[2:])/2)
idx=np.argsort(spike)[-12:]+1
report={'largest_brightness_spikes':[(int(i+1),float(mean[i]),float(spike[i-1])) for i in idx[::-1]],'largest_frame_changes':[(int(i+2),float(change[i])) for i in np.argsort(change)[-12:][::-1]]}
(R/'frame-analysis.json').write_text(json.dumps(report,indent=2))
sheet=Image.new('RGB',(960,12*200));d=ImageDraw.Draw(sheet)
for row,i in enumerate(idx[::-1]):
    for col,j in enumerate((i-1,i,i+1)):
        im=Image.open(files[j]);im.thumbnail((320,180));sheet.paste(im,(col*320,row*200));d.text((col*320,row*200+180),str(j+1),fill='white')
sheet.save(R/'spikes.jpg');print(report)
