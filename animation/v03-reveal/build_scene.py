"""Blender 4.5: actual Fusion part geometry, presentation-only exploded transforms."""
import bpy,json,math,os,sys
from pathlib import Path
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parent
FPS=24; END=600
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=12
scene.cycles.use_denoising=True;scene.cycles.adaptive_threshold=.12
scene.cycles.max_bounces=4;scene.cycles.diffuse_bounces=2;scene.cycles.glossy_bounces=3
scene.render.resolution_x=1280;scene.render.resolution_y=720;scene.render.resolution_percentage=100
scene.render.fps=FPS;scene.frame_start=1;scene.frame_end=END
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB'
scene.render.use_persistent_data=True
scene.render.threads_mode='FIXED';scene.render.threads=8
scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.008,.012,.02,1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.25
scene.view_settings.view_transform='AgX'
def material(name,color,metal=0,rough=.35):
    m=bpy.data.materials.new(name);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
    return m
mats={
 'panel':material('Warm porcelain | printed panel',(.68,.72,.69),0,.3),
 'rail':material('Graphite anodized aluminum',(.025,.038,.052),.78,.28),
 'cap':material('Champagne brass | decorative cap',(.58,.32,.095),.85,.23),
 'seat':material('Deep teal | printed locating seat',(.018,.13,.14),0,.35),
 'metal':material('Satin aluminum | frame fittings',(.27,.32,.37),.85,.28),
 'screw':material('Dark steel | reference fastener',(.075,.095,.12),.85,.26)}
root=bpy.data.objects.new('ASSEMBLY | 480 mm | 120 CAD components',None);scene.collection.objects.link(root);root.location=(0,0,.42)
manifest=json.loads((ROOT/'manifest.json').read_text());parts=[]
for part in manifest['parts']:
    bpy.ops.wm.stl_import(filepath=str(ROOT/part['file']))
    obj=bpy.context.object;obj.name=part['name'];name=obj.name
    lo,hi=part['bounds_mm'];center=[(a+b)/2 for a,b in zip(lo,hi)]
    # Millimetres in CAD -> metres, right-handed X,-Z,Y presentation coordinates.
    transform=Matrix(((.001,0,0,-center[0]*.001),(0,0,-.001,center[2]*.001),(0,.001,0,-center[1]*.001),(0,0,0,1)))
    obj.data.transform(transform);obj.parent=root
    base=Vector((center[0]*.001-.24,.0175-center[2]*.001,center[1]*.001-.24))
    obj.location=base
    if name.startswith('Panel'):kind='panel';delta=Vector((base.x*.55,.22,base.z*.55));delay=.6
    elif 'cap ' in name:kind='cap';delta=Vector((base.x*.60,.37,base.z*.60));delay=0
    elif 'registration seat' in name:kind='seat';delta=Vector((base.x*.60,.13,base.z*.60));delay=1
    elif 'compression spacer' in name:kind='metal';delta=Vector((base.x*.60,.065,base.z*.60));delay=1.2
    elif name.startswith('REFERENCE front'):kind='screw';delta=Vector((base.x*.6,.46,base.z*.6));delay=0
    elif name.startswith(('Vertical rail','Horizontal tie')):
        kind='rail';delta=Vector((base.x*.35,-.12,base.z*.35));delay=2
    elif 'nut front' in name:kind='metal';delta=Vector((base.x*.60,-.035,base.z*.60));delay=1.4
    else:
        kind='screw' if 'REFERENCE' in name else 'metal'
        outward=Vector((1 if base.x>=0 else -1,0,1 if base.z>=0 else -1))
        delta=Vector((base.x*.45,-.09,base.z*.45))
        if 'nut side' in name:delta+=Vector((outward.x*.075,-.085,outward.z*.045))
        elif 'side M5' in name:delta+=Vector((outward.x*.14,.015,outward.z*.075))
        elif 'anchor HEAD' in name:delta+=Vector((outward.x*.20,.075,outward.z*.03))
        delay=1.6
    obj.data.materials.clear();obj.data.materials.append(mats[kind])
    obj['CAD source']=part['file'];obj['CAD volume mm3']=part['volume_mm3']
    # Stationary assembled -> explode -> hold -> return. Paths are illustrative.
    for frame,factor in [(1,0),(int(8*FPS+delay*FPS),0),(int(12*FPS+delay*FPS*.35),1),(int(16*FPS+delay*FPS*.35),1),(int(21*FPS-delay*FPS*.6),0),(END,0)]:
        obj.location=base+delta*factor;obj.keyframe_insert(data_path='location',frame=frame)
    parts.append(obj)
assert len(parts)==120
for frame,deg in [(1,-22),(72,-12),(192,338),(288,345),(384,400),(504,350),(600,338)]:
    root.rotation_euler[2]=math.radians(deg);root.keyframe_insert(data_path='rotation_euler',frame=frame)
def aim(obj,target):obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Camera | product reveal';scene.camera=cam;cam.data.lens=58
for frame,pos,target in [(1,(.08,1.85,.9),(0,0,.43)),(72,(.10,1.95,.93),(0,0,.43)),(192,(.08,2.1,.98),(0,0,.43)),(288,(.05,3.65,1.32),(0,0,.39)),(384,(.05,3.65,1.32),(0,0,.39)),(504,(.08,2,.95),(0,0,.43)),(600,(.08,1.85,.9),(0,0,.43))]:
    cam.location=pos;aim(cam,target);cam.keyframe_insert(data_path='location',frame=frame);cam.keyframe_insert(data_path='rotation_euler',frame=frame)
def area(name,pos,power,color,size,target=(0,0,.4)):
    data=bpy.data.lights.new(name,'AREA');data.energy=power;data.color=color;data.shape='DISK';data.size=size
    obj=bpy.data.objects.new(name,data);scene.collection.objects.link(obj);obj.location=pos;aim(obj,target)
area('Key | broad softbox',(.9,1.1,1.6),260,(1,.88,.74),1.2)
area('Fill | cool strip',(-.9,.6,.8),140,(.65,.82,1),.85)
area('Rim | cyan edge',(.4,-.8,1.3),340,(.45,.76,1),.75)
area('Rim | warm edge',(-.8,-.45,.7),180,(1,.7,.38),.65)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,0));floor=bpy.context.object;floor.name='Studio floor'
floor_mat=material('Midnight studio',(.004,.006,.01),0,1)
floor_mat.node_tree.nodes['Principled BSDF'].inputs['Specular IOR Level'].default_value=0
floor.data.materials.append(floor_mat)
# Clamp Bezier handles to avoid motion overshoot at assembled and exploded holds.
for obj in [root,cam]+parts:
    if obj.animation_data and obj.animation_data.action:
        for fc in obj.animation_data.action.fcurves:
            for k in fc.keyframe_points:k.handle_left_type='AUTO_CLAMPED';k.handle_right_type='AUTO_CLAMPED'
scene.frame_set(1);scene.render.filepath='//frames/frame_'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'reveal.blend'),compress=True)
if '--preview' in sys.argv:
    frame=int(sys.argv[sys.argv.index('--preview')+1]);scene.frame_set(frame)
    scene.render.filepath=str(ROOT/'stills'/f'frame-{frame:04d}.png');bpy.ops.render.render(write_still=True)
