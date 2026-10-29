import bpy,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
(ROOT/'frames').mkdir(exist_ok=True)
s=bpy.context.scene
start=time.time()
for frame in range(1,841):
    path=ROOT/'frames'/f'{frame:04d}.png'
    if path.exists():continue
    s.frame_set(frame);s.render.filepath=str(path);bpy.ops.render.render(write_still=True)
    (ROOT/'render-progress.json').write_text(json.dumps({'frame':frame,'total':840,'elapsed_s':time.time()-start}))
