"""Editorial typography, 24 fps H.264 delivery, and representative QA frames."""
from pathlib import Path
import json,subprocess,sys,time
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parent
W,H=1280,720;FPS=24;COUNT=600
FONT=Path('C:/Windows/Fonts')
fonts={size:ImageFont.truetype(str(FONT/'segoeuil.ttf'),size) for size in [14,16,19,30,40]}
bold=ImageFont.truetype(str(FONT/'segoeuisl.ttf'),30)
def opacity(frame,start,end,fade=12):return max(0,min(1,(frame-start)/fade,(end-frame)/fade))
def title(frame,image):
    im=image.convert('RGBA');layer=Image.new('RGBA',im.size);draw=ImageDraw.Draw(layer)
    a=max(opacity(frame,7,77),opacity(frame,505,601))
    def text(x,y,t,size=16,color=(225,233,236),alpha=1,font=None):
        draw.text((x,y),t,font=font or fonts[size],fill=(*color,int(255*alpha)))
    if a:
        text(54,88,'INFINITE',40,alpha=a)
        text(55,139,'SKÅDIS HD',30,alpha=a,font=bold)
        draw.line((56,195,106,195),fill=(207,158,85,int(255*a)),width=2)
        text(55,221,'One system.',19,alpha=a)
        text(55,250,'120 components.',19,alpha=a)
        text(55,600,'480 × 480 mm',19,alpha=a)
        text(55,629,'240 mm parametric modules',14,color=(160,181,192),alpha=a)
    if 77<=frame<=505:
        if frame<192:label='01  /  THE ASSEMBLY'
        elif frame<384:label='02  /  EVERY COMPONENT'
        else:label='03  /  BACK TOGETHER'
        text(55,650,label,16,color=(205,219,227),alpha=.85)
    if frame>516:text(55,668,'FUSION CAD CONCEPT  /  v0.3',14,color=(160,181,192),alpha=opacity(frame,516,601))
    im=Image.alpha_composite(im,layer).convert('RGB')
    fade=min(1,frame/12,(COUNT-frame)/16)
    if fade<1:im=Image.blend(Image.new('RGB',im.size),im,max(0,fade))
    return im
def source(frame):return min(504,max(72,frame))
def get(frame):return Image.open(ROOT/'frames'/f'frame_{source(frame):04d}.png').convert('RGB')
if '--poster' in sys.argv:
    title(48,get(72)).save(ROOT/'poster.png');sys.exit(0)
if '--wait' in sys.argv:
    while True:
        try:
            if json.loads((ROOT/'render-progress.json').read_text()).get('frame',0)>=504:break
        except (FileNotFoundError,json.JSONDecodeError):pass
        time.sleep(5)
paths=[ROOT/'frames'/f'frame_{f:04d}.png' for f in range(72,505)]
assert all(p.exists() for p in paths),'Incomplete moving-shot render'
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
output=ROOT/'infinite-skadis-reveal.mp4'
working=ROOT/'infinite-skadis-reveal.working.mp4'
args=[ffmpeg,'-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','slow','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(working)]
with open(ROOT/'encode.log','w') as log:
    proc=subprocess.Popen(args,stdin=subprocess.PIPE,stderr=log)
    for frame in range(1,COUNT+1):
        im=title(frame,get(frame));assert im.size==(W,H)
        proc.stdin.write(im.tobytes())
    proc.stdin.close();assert proc.wait()==0,'FFmpeg encoding failed'
working.replace(output)
title(48,get(72)).save(ROOT/'poster.png')
selected=[48,100,144,192,240,288,336,384,432,480,540,580]
sheet=Image.new('RGB',(1280,720),(8,12,18));draw=ImageDraw.Draw(sheet)
# Decode the actual delivery file and verify dimensions, count and useful variation.
reader=imageio_ffmpeg.read_frames(str(output),pix_fmt='rgb24');meta=next(reader)
assert tuple(meta['size'])==(W,H),meta
assert abs(meta['fps']-FPS)<.01,meta
count=0;means=[]
for raw in reader:
    count+=1
    if count in selected:
        arr=np.frombuffer(raw,dtype=np.uint8);means.append(float(arr.mean()))
        thumb=Image.frombytes('RGB',(W,H),raw);thumb.thumbnail((320,180))
        i=selected.index(count);x=(i%4)*320;y=(i//4)*240
        sheet.paste(thumb,(x,y));draw.text((x+10,y+185),f'{count/FPS:.1f} s',font=fonts[16],fill=(220,225,230))
assert count==COUNT,(count,meta)
assert min(means)>5 and max(means)-min(means)>1,means
sheet.save(ROOT/'qa-contact-sheet.jpg',quality=92)
report={'file':output.name,'size_bytes':output.stat().st_size,'decoded_frames':count,'fps':FPS,'duration_seconds':COUNT/FPS,'dimensions':[W,H],'codec':'H.264 / yuv420p','silent':True,'intro_hold_source_frame':72,'outro_hold_source_frame':504,'sample_mean_brightness':means,'all_frames_decoded':True}
(ROOT/'delivery-validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
