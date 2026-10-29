from pathlib import Path
import subprocess,json
import imageio_ffmpeg
from PIL import Image
ROOT=Path(__file__).resolve().parent
out=ROOT/'infinite-skadis-metallic.mp4'
working=ROOT/'infinite-skadis-metallic.working.mp4'
assert all((ROOT/'frames'/f'{f:04d}.png').exists() for f in range(1,841))
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-framerate','24','-i',str(ROOT/'frames/%04d.png'),'-c:v','libx264','-preset','slow','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(working)],check=True)
reader=imageio_ffmpeg.read_frames(str(working),pix_fmt='rgb24');meta=next(reader)
sheet=Image.new('RGB',(1280,1800));n=0
for count,data in enumerate(reader,1):
    if count in (1,121,241,313,409,481,553,625,721,840):
        im=Image.frombytes('RGB',meta['size'],data);im.thumbnail((640,360))
        sheet.paste(im,((n%2)*640,(n//2)*360));n+=1
assert count==840 and abs(meta['duration']-35)<.1 and meta['size']==(1920,1080) and meta['fps']==24,meta
working.replace(out);sheet.save(ROOT/'contact-sheet.jpg',quality=92)
(ROOT/'delivery-validation.json').write_text(json.dumps({'decoded_frames':count,'duration_s':meta['duration'],'dimensions':meta['size'],'fps':meta['fps'],'bytes':out.stat().st_size,'status':'encoded and decoded successfully; visual review pending'},indent=2))
