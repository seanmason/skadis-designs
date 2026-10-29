import bpy,json,sys
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parent;s=bpy.context.scene
parts=[o for o in s.objects if 'CAD source' in o]
assert len(parts)==120
extents=[1,1,0,0];clipped=[]
for frame in range(1,601):
    s.frame_set(frame);bpy.context.view_layer.update()
    for o in parts:
        for corner in o.bound_box:
            p=world_to_camera_view(s,s.camera,o.matrix_world@Vector(corner))
            extents=[min(extents[0],p.x),min(extents[1],p.y),max(extents[2],p.x),max(extents[3],p.y)]
            if p.z<=0 or not (.025<p.x<.975 and .025<p.y<.975):clipped.append((frame,o.name))
assert not clipped,clipped[:20]
for o in parts:
    s.frame_set(1);start=o.location.copy();s.frame_set(600)
    assert (o.location-start).length<1e-8,o.name
report={'CAD_parts':len(parts),'frames':600,'fps':24,'duration_seconds':25,'framing_extents_normalized':extents,'all_frames_within_safe_border':True,'assembled_positions_restored':True,'explosion_is_presentation_not_installation_simulation':True}
(ROOT/'animation-validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
if '--stills' in sys.argv:
    for frame in [1,144,336,600]:
        s.frame_set(frame);s.render.filepath=str(ROOT/'stills'/f'frame-{frame:04d}.png');bpy.ops.render.render(write_still=True)
if '--render' in sys.argv:
    (ROOT/'frames').mkdir(exist_ok=True)
    s.render.filepath=str(ROOT/'frames'/'frame_');bpy.ops.render.render(animation=True)
