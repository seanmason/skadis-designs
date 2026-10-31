"""Overlay approved chapter captions; encode and inspect every delivered frame."""
from pathlib import Path
import subprocess,json
import imageio_ffmpeg,numpy as np
from PIL import Image
R=Path(__file__).resolve().parent;shots=json.loads((R/'shots.json').read_text())
frames=R/'frames';assert all((frames/f'{f:04d}.png').exists() for f in range(1,1441))
caps={s['key']:Image.open(R/'captions'/f"{s['key']}.png").convert('RGBA') for s in shots}
working=R/'assembly-features.working.mp4';out=R/'skadis-v05-assembly.mp4'
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
args=[ffmpeg,'-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','24','-i','pipe:0','-an','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(working)]
with (R/'encode.log').open('w') as log:
    p=subprocess.Popen(args,stdin=subprocess.PIPE,stdout=log,stderr=subprocess.STDOUT)
    for f in range(1,1441):
        im=Image.open(frames/f'{f:04d}.png').convert('RGBA');assert im.size==(1920,1080)
        sh=next(s for s in shots if s['start']<=f<=s['end']);cap=caps[sh['key']]
        fade=min(1,(f-sh['start']+1)/5,(sh['end']-f+1)/5)
        if fade<1:
            cap=cap.copy();cap.putalpha(cap.getchannel('A').point(lambda v:int(v*fade)))
        im=Image.alpha_composite(im,cap).convert('RGB');p.stdin.write(im.tobytes())
        if f in [48,1410]:im.save(R/('poster.jpg' if f==48 else 'ending.jpg'),quality=95)
        if f%240==0:print('Encoded input',f,flush=True)
    p.stdin.close();assert p.wait()==0,'FFmpeg encode failed'
reader=imageio_ffmpeg.read_frames(str(working),pix_fmt='rgb24');meta=next(reader)
brightness=[];small=[];thumbs=[]
chosen=[48,170,265,390,510,650,790,925,995,1062,1175,1252,1336,1410]
for count,data in enumerate(reader,1):
    im=Image.frombytes('RGB',meta['size'],data)
    a=np.asarray(im.resize((160,90)),dtype=np.float32);brightness.append(float(a.mean()));small.append(a)
    if count in chosen:thumbs.append(im.resize((480,270)))
assert count==1440 and meta['size']==(1920,1080) and meta['fps']==24 and abs(meta['duration']-60)<.1,meta
assert min(brightness)>2,('Black frame',int(np.argmin(brightness))+1)
cuts={x['start'] for x in shots}
spikes=[];image_spikes=[]
for i in range(1,1439):
    f=i+1
    if f in cuts or f+1 in cuts:continue
    spikes.append((abs(brightness[i]-(brightness[i-1]+brightness[i+1])/2),f))
    image_spikes.append((float(np.abs(small[i]-(small[i-1]+small[i+1])/2).mean()),f))
assert max(spikes)[0]<5,('Isolated brightness flash',max(spikes))
assert max(image_spikes)[0]<12,('Isolated image discontinuity',max(image_spikes))
sheet=Image.new('RGB',(1440,1350),(7,11,18))
for i,im in enumerate(thumbs):sheet.paste(im,((i%3)*480,(i//3)*270))
sheet.save(R/'contact-sheet.jpg',quality=94)
working.replace(out)
report={'frames':count,'duration_seconds':meta['duration'],'dimensions':meta['size'],'fps':meta['fps'],'bytes':out.stat().st_size,'minimum_frame_brightness':min(brightness),'largest_within_shot_brightness_spikes':sorted(spikes,reverse=True)[:8],'largest_within_shot_image_spikes':sorted(image_spikes,reverse=True)[:8],'intentional_cut_frames':sorted(cuts),'all_frames_decoded':True,'visual_review':'pending'}
(R/'delivery-validation.json').write_text(json.dumps(report,indent=2));print('DELIVERY ENCODED',report,flush=True)
