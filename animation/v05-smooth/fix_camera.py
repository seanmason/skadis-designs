"""Smooth the original camera path and unwrap its Euler rotation before motion blur."""
import bpy,math,json
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
R=Path(__file__).resolve().parent;s=bpy.context.scene;cam=s.camera
raw=[];rot=[]
for f in range(1,841):
    s.frame_set(f);raw.append(cam.location.copy());rot.append(cam.rotation_euler.copy())
rotation_jumps=[(i+1,max(abs(rot[i][k]-rot[i-1][k]) for k in range(3))) for i in range(1,840)]
target=Vector((0,0,.7))
dist=[(p-target).length for p in raw]
# Spread the discrete auto-fit corrections across two seconds without camera steps.
sigma=12;radius=36
weights=[math.exp(-.5*(j/sigma)**2) for j in range(-radius,radius+1)]
smoothed=[sum(dist[max(0,min(839,i+j))]*w for j,w in zip(range(-radius,radius+1),weights))/sum(weights) for i in range(840)]
cam.animation_data_clear();previous=None;positions=[];angles=[]
for i in range(840):
    direction=(raw[i]-target).normalized()
    # Small global margin covers smoothed auto-fit corrections without new per-frame jumps.
    cam.location=target+direction*(smoothed[i]*1.04)
    mat=(target-cam.location).to_track_quat('-Z','Y').to_matrix()
    e=mat.to_euler('XYZ',previous) if previous is not None else mat.to_euler('XYZ')
    cam.rotation_euler=e;previous=e.copy();positions.append(cam.location.copy());angles.append(e.copy())
    cam.keyframe_insert(data_path='location',frame=i+1);cam.keyframe_insert(data_path='rotation_euler',frame=i+1)
for fc in cam.animation_data.action.fcurves:
    for k in fc.keyframe_points:k.interpolation='LINEAR'
parts=[o for o in s.objects if o.parent and o.type=='MESH']
assert len(parts)==362
minimum=1
for f in range(1,841):
    s.frame_set(f)
    for obj in parts:
        for v in obj.bound_box:
            p=world_to_camera_view(s,cam,obj.matrix_world@Vector(v))
            minimum=min(minimum,p.x,1-p.x,p.y,1-p.y)
            assert p.z>0 and 0<p.x<1 and 0<p.y<1,('cropped',f,obj.name)
jumps=[max(abs(angles[i][k]-angles[i-1][k]) for k in range(3)) for i in range(1,840)]
assert max(jumps)<.02,max(jumps)
report={'original_largest_euler_jumps_radians':sorted(rotation_jumps,key=lambda x:x[1],reverse=True)[:6],'corrected_max_euler_step_radians':max(jumps),'corrected_max_camera_step_m':max((positions[i]-positions[i-1]).length for i in range(1,840)),'minimum_frame_margin':minimum,'frames_checked':840,'components':362}
(R/'camera-validation.json').write_text(json.dumps(report,indent=2));print(report)
s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(R/'smooth.blend'),compress=True)
(R/'checks').mkdir(exist_ok=True)
for f in [258,259,260,261,262,311,312,313,341,342,343,460,461,462,463,464]:
    s.frame_set(f);s.render.resolution_percentage=50;s.render.filepath=str(R/'checks'/f'{f:04d}.png');bpy.ops.render.render(write_still=True)
