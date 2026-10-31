import bpy,json
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
R=Path(__file__).resolve().parent;s=bpy.context.scene
names=[p['name'] for p in json.loads((R/'manifest.json').read_text())['parts']]
parts=[bpy.data.objects[n] for n in names]
shots=json.loads((R/'shots.json').read_text());results=[]
for sh in shots:
    if sh['key'] not in ['reveal','explode','frame','panels','art','finish']:continue
    margin=1;checked=0
    for f in sorted(set([sh['start'],sh['end']]+list(range(sh['start'],sh['end']+1,8)))):
        s.frame_set(f)
        for o in parts:
            if o.hide_render:continue
            for corner in o.bound_box:
                p=world_to_camera_view(s,s.camera,o.matrix_world@Vector(corner))
                assert p.z>0 and 0<p.x<1 and 0<p.y<1,(sh['key'],f,o.name,tuple(p))
                margin=min(margin,p.x,p.y,1-p.x,1-p.y);checked+=1
    results.append({'shot':sh['key'],'sampled_corner_projections':checked,'minimum_screen_margin':margin})
panel=next(o for o in parts if o.name.startswith('Panel lower left'))
service=[]
for f in [1273,1303,1336,1368]:
    s.frame_set(f);points=[world_to_camera_view(s,s.camera,panel.matrix_world@Vector(c)) for c in panel.bound_box]
    assert all(0<p.x<1 and 0<p.y<1 for p in points),('Service panel cropped',f)
    service.append({'frame':f,'bottom_screen_fraction':min(p.y for p in points)})
(R/'camera-framing-validation.json').write_text(json.dumps({'wide_shots':results,'service_panel':service},indent=2))
print(results,service)
