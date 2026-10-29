"""Encode the CPU draft and verify decoded frames; no typography."""
from pathlib import Path
import subprocess,json
import imageio_ffmpeg
from PIL import Image,ImageOps
ROOT=Path(__file__).resolve().parent
exe=imageio_ffmpeg.get_ffmpeg_exe()
out=ROOT/'infinite-skadis-motion-review.mp4'
subprocess.run([exe,'-y','-framerate','12','-i',str(ROOT/'frames/%04d.png'),'-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],check=True)
reader=imageio_ffmpeg.read_frames(str(out),pix_fmt='rgb24');metadata=next(reader)
samples=[];count=0
for count,data in enumerate(reader,1):
    if count in (1,61,121,157,205,241,277,313,361,420):
        samples.append(Image.frombytes('RGB',metadata['size'],data))
assert count==420,(count,metadata)
assert abs(metadata['duration']-35)<.1,metadata
sheet=Image.new('RGB',(640*2,360*5))
for i,im in enumerate(samples):sheet.paste(im,((i%2)*640,(i//2)*360))
sheet.save(ROOT/'review-contact-sheet.jpg',quality=90)
(ROOT/'delivery-validation.json').write_text(json.dumps({'decoded_frames':count,'duration_s':metadata['duration'],'size':metadata['size'],'fps':metadata['fps'],'bytes':out.stat().st_size},indent=2))
print('VERIFIED',out,metadata)
