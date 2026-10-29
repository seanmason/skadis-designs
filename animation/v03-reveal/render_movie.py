"""Render moving shots; editorial title/end holds reuse frames 72 and 504."""
import bpy,json,os,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent;s=bpy.context.scene
(ROOT/'frames').mkdir(exist_ok=True)
start=time.time()
for frame in range(72,505):
    target=ROOT/'frames'/f'frame_{frame:04d}.png'
    if target.exists():continue
    s.frame_set(frame);s.render.filepath=str(target);bpy.ops.render.render(write_still=True)
    (ROOT/'render-progress.json').write_text(json.dumps({'frame':frame,'last_moving_frame':504,'elapsed_seconds':round(time.time()-start),'pid':os.getpid()}))
print('MOVING SHOTS COMPLETE',flush=True)
