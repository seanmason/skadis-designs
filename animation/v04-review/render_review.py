import bpy
from pathlib import Path
ROOT=Path(__file__).resolve().parent
(ROOT/'frames').mkdir(exist_ok=True)
scene=bpy.context.scene
for frame in range(1,421):
    path=ROOT/'frames'/f'{frame:04d}.png'
    if path.exists():continue
    scene.frame_set(frame);scene.render.filepath=str(path);bpy.ops.render.render(write_still=True)
