import bpy,json
from pathlib import Path
s=bpy.context.scene;R=Path(__file__).resolve().parent
cam=s.camera;last=None;changes=[]
for f in range(1,841):
    s.frame_set(f);pos=cam.location.copy();q=cam.rotation_euler.to_quaternion()
    if last:changes.append((f,(pos-last[0]).length,q.rotation_difference(last[1]).angle))
    last=(pos,q)
(R/'camera-analysis.json').write_text(json.dumps(sorted(changes,key=lambda x:x[1],reverse=True)[:30],indent=2))
print('CAMERA',sorted(changes,key=lambda x:x[1],reverse=True)[:10])
