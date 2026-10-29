"""CPU motion draft using exported Fusion geometry; run with v03 reveal.blend loaded."""
import bpy, json, math
from pathlib import Path
from mathutils import Vector, Matrix
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
scene=bpy.context.scene
old=list(scene.objects)
manifest=json.loads((ROOT.parent/'v03-reveal/manifest.json').read_text())
sources={p['name']:p for p in manifest['parts']}
protos={n:bpy.data.objects[n] for n in sources}
root=bpy.data.objects.new('720 x 480 mm | 24 panels | REVIEW',None)
scene.collection.objects.link(root);root.location=(0,0,.7)
parts=[]
def add(obj, center, kind):
    obj.animation_data_clear();obj.parent=root;obj.rotation_euler=(0,0,0)
    obj.location=((center[0]-360)*.001,.0175-center[2]*.001,(center[1]-240)*.001)
    parts.append((obj,obj.location.copy(),kind))
def clone(name,dx=0,dy=0,sx=1):
    p=sources[name];obj=protos[name].copy();obj.data=protos[name].data
    scene.collection.objects.link(obj);obj.name=name+' review '+str(len(parts))
    center=[(a+b)/2 for a,b in zip(*p['bounds_mm'])];center[0]+=dx;center[1]+=dy
    obj.scale=(sx,1,1)
    kind='rail' if name.startswith(('Vertical','Horizontal')) else ('cap' if 'cap ' in name else 'hardware')
    add(obj,center,kind)
xs=[12,120,240,360,480,600,708];ys=[12,120,240,360,468]
for x in xs:clone('Vertical rail 0 - measured sloped-slot approximation',x-12)
for j in range(2):
    for i in range(6):
        clone('Horizontal tie 0'+str(j)+' - measured sloped-slot approximation',(xs[i]+xs[i+1])/2-126,0,(xs[i+1]-xs[i]-20)/208)
        for side,dx in [('L',xs[i]-12),('R',xs[i+1]-240)]:
            tag='0'+str(j)+side
            for name in sources:
                if name.endswith(' '+tag) or name.endswith(' '+tag+' X') or name.endswith(' '+tag+' Y'):clone(name,dx)
for x in xs:
    for y in ys:
        for prefix in ['METAL cap','PRINT registration seat','METAL stepped compression spacer','REFERENCE front M5x25','REFERENCE thin METAL channel nut front']:
            clone(prefix+' 00',x-12,y-12)
for name in sources:
    if 'wall ' in name or 'wall tab ' in name or 'anchor HEAD ONLY' in name:
        tag=name.split()[-1];clone(name,240 if tag[0]=='1' else 0)
def material(name,c,metal):
    m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=.29
    return m
palette=[material('Panel deep teal',(.012,.15,.17),0),material('Panel midnight blue',(.008,.028,.09),0),material('Panel warm ivory',(.68,.70,.64),0),material('Panel copper finish',(.52,.20,.08),.85),material('Panel satin aluminum finish',(.45,.50,.55),.85)]
for j in range(4):
    for i in range(6):
        if i in (0,5) and j in (0,3):name=('l' if j==0 else 'u')+('l' if i==0 else 'r')+'-panel-120.stl'
        elif i==0:name='panel-left-edge-120.stl'
        elif i==5:name='panel-right-edge-120.stl'
        elif j==0:name='panel-bottom-edge-120.stl'
        elif j==3:name='panel-top-edge-120.stl'
        else:name='panel-interior-120.stl'
        bpy.ops.wm.stl_import(filepath=str(REPO/'models/v03'/name));obj=bpy.context.object
        corners=[Vector(v) for v in obj.bound_box];c=sum(corners,Vector())/8
        obj.data.transform(Matrix(((.001,0,0,-c.x*.001),(0,0,-.001,c.z*.001),(0,.001,0,-c.y*.001),(0,0,0,1))))
        obj.name=f'Panel {i+1},{j+1} | {name}';obj.data.materials.clear();obj.data.materials.append(palette[(i+2*j)%5])
        add(obj,((i+.5)*120,(j+.5)*120,2.5),'panel')
assert len(parts)==362,len(parts)
for obj in old:
    if obj.name in protos or obj.type=='EMPTY':bpy.data.objects.remove(obj,do_unlink=True)
cam=scene.camera;cam.animation_data_clear();cam.data.lens=50
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=2
scene.cycles.use_denoising=True;scene.cycles.max_bounces=3
scene.render.resolution_x=640;scene.render.resolution_y=360;scene.render.resolution_percentage=100
scene.render.fps=12;scene.frame_start=1;scene.frame_end=420
scene.render.threads_mode='FIXED';scene.render.threads=8
def smooth(t):return max(0,min(1,t))**2*(3-2*max(0,min(1,t)))
def interp(t,points):
    for (a,x),(b,y) in zip(points,points[1:]):
        if t<=b:return x+(y-x)*smooth((t-a)/(b-a))
    return points[-1][1]
for frame in range(1,421):
    t=(frame-1)/12
    root.rotation_euler[2]=math.radians(interp(t,[(0,-20),(5,340),(10,345),(14,400),(23,450),(30,700),(35,720)]))
    root.keyframe_insert(data_path='rotation_euler',frame=frame)
    for index,(obj,base,kind) in enumerate(parts):
        phase=index*2.39996323
        depth=.22 if kind=='panel' else (.36 if kind=='cap' else (-.15 if kind=='rail' else .07+.12*math.sin(phase)))
        exploded=base+Vector((base.x*.65,depth,base.z*.65))
        e=smooth((t-5)/5);w=smooth((t-14)/3);r=smooth((t-23)/7)
        radius=(.58+.14*math.sin(phase)) if kind=='panel' else (.44+.30*(.5+.5*math.sin(phase)))
        angular=(t-14)*(.7 if kind=='rail' else (1 if kind=='panel' else 1.35))+phase
        orbit=Vector((radius*math.cos(angular),radius*math.sin(angular),(.18 if kind=='rail' else .38)*math.sin(phase+(t-14)*.4)))
        obj.location=((base.lerp(exploded,e)).lerp(orbit,w)).lerp(base,r)
        spin=w*(1-r)
        obj.rotation_euler=(spin*.45*math.sin(angular),spin*.65*math.cos(angular),spin*(angular-phase))
        obj.keyframe_insert(data_path='location',frame=frame);obj.keyframe_insert(data_path='rotation_euler',frame=frame)
    distance=interp(t,[(0,2.1),(5,2.1),(10,3.1),(14,3.1),(17,4.5),(23,4.5),(30,2.1),(35,2.1)])
    az=interp(t,[(0,.05),(10,.05),(14,-.4),(23,.25),(30,.05),(35,.05)])
    target=Vector((0,0,.7));direction=Vector((math.sin(az),math.cos(az),.23)).normalized()
    cam.location=target+direction*distance;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
    bpy.context.view_layer.update()
    for attempt in range(8):
        projected=[world_to_camera_view(scene,cam,obj.matrix_world@Vector(v)) for obj,_,_ in parts for v in obj.bound_box]
        if all(.055<p.x<.945 and .055<p.y<.945 and p.z>0 for p in projected):break
        distance*=1.08;cam.location=target+direction*distance;bpy.context.view_layer.update()
    assert attempt<7,('framing',frame)
    cam.keyframe_insert(data_path='location',frame=frame);cam.keyframe_insert(data_path='rotation_euler',frame=frame)
for obj in [root,cam]+[p[0] for p in parts]:
    for fc in obj.animation_data.action.fcurves:
        for k in fc.keyframe_points:k.interpolation='LINEAR'
scene.frame_set(420)
assert all((obj.location-base).length<1e-7 and obj.rotation_euler.to_quaternion().angle<1e-6 for obj,base,_ in parts)
(ROOT/'validation.json').write_text(json.dumps({'panels':24,'components':362,'module_mm':120,'assembly_mm':[720,480],'fps':12,'frames':420,'duration_s':35,'framing_checked_frames':420,'final_assembled_pose_verified':True,'cpu_only':True,'text_overlays':False,'status':'Motion review; repeated CAD parts, horizontal rails resized along constant-profile axis; native expanded assembly not yet verified'},indent=2))
scene.frame_set(1);scene.render.filepath='//frames/frame_'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'review.blend'),compress=True)
for frame,label in [(1,'assembled'),(157,'exploded'),(241,'whirlwind')]:
    scene.frame_set(frame);scene.render.filepath=str(ROOT/(label+'.png'));bpy.ops.render.render(write_still=True)
