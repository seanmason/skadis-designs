"""Blender 4.5. Actual v0.5 CAD, staged explanatory motions, explicit shot cuts.
Flexure shape keys are illustrative, not a mechanical/force simulation.
"""
import bpy,json,math
from pathlib import Path
from mathutils import Vector,Matrix
R=Path(__file__).resolve().parent
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=32
s.cycles.use_denoising=True;s.cycles.adaptive_threshold=.045;s.cycles.max_bounces=5
s.render.resolution_x=1920;s.render.resolution_y=1080;s.render.resolution_percentage=100
s.render.fps=24;s.frame_start=1;s.frame_end=1440;s.render.use_persistent_data=False
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
s.render.film_transparent=False;s.render.use_motion_blur=False;s.view_settings.view_transform='AgX'
s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=-1.25
s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.009,.014,.024,1)
s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.35
A=Matrix(((.001,0,0,-.24),(0,0,-.001,0),(0,.001,0,0),(0,0,0,1)))
def delta(x=0,y=0,z=0):return Vector((x/1000,-z/1000,y/1000))
def mat(name,c,metal=0,rough=.3):
    m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
    return m
palette=[mat('Metallic copper',(.31,.095,.038),.72),mat('Metallic petrol',(.025,.18,.17),.7),mat('Metallic blue graphite',(.065,.115,.18),.7),mat('Metallic bronze',(.30,.20,.055),.74)]
railmat=mat('Graphite anodized 2020',(.045,.065,.09),.8,.3)
steel=mat('Satin steel',(.3,.37,.44),.88,.27);gold=mat('Warm metal nut highlight',(.55,.29,.065),.8,.27)
plastic=mat('Teal carrier polymer',(.025,.22,.23),.08,.32);jigmat=mat('Orange alignment tool',(.65,.18,.035),.1,.35)
coremat=mat('Dark tile core',(.025,.04,.06),.05,.34)
pixels=[mat('Pixel '+str(i),c,.45,.27) for i,c in enumerate([(.02,.38,.37),(.025,.15,.27),(.75,.29,.045),(.36,.065,.03),(.12,.27,.34),(.52,.36,.10)])]
cache={};allobjs=[];base={};parts=[];groups={};records={}
def raw(path):
    path=str(path)
    if path not in cache:
        bpy.ops.wm.stl_import(filepath=path);o=bpy.context.object
        cache[path]=o.data;bpy.data.objects.remove(o,do_unlink=True)
    return cache[path]
def make(name,path,matrix,material):
    mesh=raw(path).copy();mesh.transform(matrix)
    lo=Vector(tuple(min(v.co[i] for v in mesh.vertices) for i in range(3)))
    hi=Vector(tuple(max(v.co[i] for v in mesh.vertices) for i in range(3)))
    center=(lo+hi)/2;mesh.transform(Matrix.Translation(-center))
    o=bpy.data.objects.new(name,mesh);s.collection.objects.link(o);o.location=center
    mesh.materials.clear();mesh.materials.append(material)
    for p in mesh.polygons:p.use_smooth=False
    base[o]=center.copy();allobjs.append(o);return o
def kind(n):
    if n.startswith('Panel '):return 'panel'
    if n.startswith('Vertical rail'):return 'vertical'
    if n.startswith('Horizontal tie'):return 'tie'
    if n.startswith('PRINT carrier'):return 'carrier'
    if n.startswith('METAL M2 nut'):return 'm2nut'
    if n.startswith('METAL channel nut'):return 'tnut'
    if n.startswith('REFERENCE panel M2'):return 'panelscrew'
    if n.startswith('REFERENCE carrier M5'):return 'm5'
    if 'wall anchor' in n:return 'anchor'
    return 'framehardware'
def cad(o):return ((base[o].x+.24)*1000,base[o].z*1000,-base[o].y*1000)
def quadrant(o):
    x,y,_=cad(o);return ('l' if x<240 else 'r')+('l' if y<240 else 'u')
for p in json.loads((R/'manifest.json').read_text())['parts']:
    k=kind(p['component']);material=plastic if k=='carrier' else gold if k in ['m2nut','tnut'] else railmat if k in ['vertical','tie'] else steel
    o=make(p['name'],R/p['file'],A@Matrix(p['transform_mm']),material)
    if k=='panel':o.data.materials[0]=palette[['ll','rl','lu','ru'].index(quadrant(o))]
    groups.setdefault(k,[]).append(o);records[o]=p;parts.append(o)
assert len(parts)==143
def proto(prefix,offset=Vector((0,0,0)),material=plastic):
    result=[]
    for path in sorted((R/'assets').glob(prefix+'*.stl')):
        o=make(path.stem,path,A,material);o.location+=offset;base[o]=o.location.copy();result.append(o)
    return result
jig=proto('carrier-jig',material=jigmat)
handle=proto('panel-handling',delta(185,190),jigmat)
for o in handle:
    if 'REFERENCE' in o.name:o.data.materials[0]=steel
handle_rot=[o for o in handle if 'bridge' not in o.name]
tile_templates=proto('axial-mosaic-tile--',material=coremat)
tiles={};tile_all=[]
for k in range(12,36):
    x=5+10*k
    for j in range(6,18):
        y=(10 if k%2==0 else 20)+20*j
        members=[]
        for template in tile_templates:
            o=bpy.data.objects.new('Art %03d %03d '%(x,y)+template.name,template.data);s.collection.objects.link(o)
            o.location=base[template]+delta(x,y);base[o]=o.location.copy();allobjs.append(o);members.append(o);tile_all.append(o)
            o.material_slots[0].link='OBJECT'
            if 'COLOR' in template.name:
                py=y+(-5 if 'lower' in template.name else 5)
                wave=math.sin((x-120)/31)+math.cos((py-120)/38)
                idx=2 if abs(wave)<.35 else 0 if wave>.35 else 1
                if (x+py)%70<20:idx=4 if wave>0 else 5
                o.material_slots[0].material=pixels[idx]
            else:o.material_slots[0].material=coremat
        tiles[(x,y)]=members
for o in tile_templates:
    allobjs.remove(o);del base[o];bpy.data.objects.remove(o,do_unlink=True)
hero_tile=tiles[(235,240)]
clear_sites={(185,190),(225,190),(225,210),(225,230),(235,220)}
clear_tiles=[o for p in clear_sites for o in tiles[p]]
ll_art=[o for (x,y),oo in tiles.items() if x<240 and y<=240 for o in oo]
def cube(name,loc,size,material):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material)
    allobjs.append(o);base[o]=o.location.copy();return o
wall=cube('Illustrative wall surface',(0,-.048,.3),(1.8,.01,1.3),mat('Charcoal wall',(.006,.009,.015),0,.85))
floor=cube('Studio plinth',(0,0,-.085),(200,200,.01),mat('Midnight floor',(.002,.003,.005),0,.85))
# A generic driver bit, presented as an assembly aid rather than CAD hardware.
bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=.0015,depth=.045,location=delta(10,209,-8)+Vector((-.24,0,0)),rotation=(math.pi/2,0,0))
driver=bpy.context.object;driver.name='Illustrative M5 driver';driver.data.materials.append(steel)
bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
tip=[]
for size in [(.0005,.0008,.003),(.003,.0008,.0005)]:
    bpy.ops.mesh.primitive_cube_add(size=1,location=delta(10,209,14.9)+Vector((-.24,0,0)));t=bpy.context.object;t.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);tip.append(t)
bpy.ops.object.select_all(action='DESELECT');driver.select_set(True)
for t in tip:t.select_set(True)
bpy.context.view_layer.objects.active=driver;bpy.ops.object.join()
allobjs.append(driver);base[driver]=driver.location.copy()
def line(name,a,b,r=.00025):
    v=Vector(b)-Vector(a);bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=r,depth=v.length,location=(Vector(a)+Vector(b))/2)
    o=bpy.context.object;o.name=name;o.rotation_euler=v.to_track_quat('Z','Y').to_euler();o.data.materials.append(gold)
    bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);allobjs.append(o);base[o]=o.location.copy();return o
dimension=[line('10 mm cavity dimension',(-.248,-.005,.020),(-.248,-.015,.020))]
for yy in [-.005,-.015]:dimension.append(line('Dimension tick',(-.248,yy,.017),(-.248,yy,.023)))
def flex(o,name,fn):
    o.data=o.data.copy();o.shape_key_add(name='Basis');key=o.shape_key_add(name=name)
    for i,v in enumerate(o.data.vertices):key.data[i].co=fn(v.co.copy(),base[o])
    return key
hero_carrier=min(groups['carrier'],key=lambda o:abs(cad(o)[0]-240)+abs(cad(o)[1]-18.5))
def spring(v,b):
    w=v+b;x=(w.x+.24)*1000;y=w.z*1000;z=-w.y*1000
    if min(abs(x-230),abs(x-250))<=1.651 and 23<=y<=33 and 17.79<=z<=19.801:
        v.y-=.001*((33-y)/10)**2
    return v
springkey=flex(hero_carrier,'Illustrative captive spring deflection',spring)
core=next(o for o in hero_tile if 'core' in o.name)
def snap(v,b):
    w=v+b;xx=(w.x+.24)*1000-235;yy=w.z*1000-240;zz=-w.y*1000
    if abs(xx)>.79 and abs(yy)<=3.01 and zz>.1:
        v.x-=math.copysign(.00025*(min(zz,5.5)/5.5)**2,xx)
    return v
snapkey=flex(core,'Illustrative axial clip compression',snap)
def key(o,f,offset=None,show=None,rot=None):
    if offset is not None:o.location=base[o]+Vector(offset);o.keyframe_insert(data_path='location',frame=f)
    if show is not None:o.hide_render=not show;o.keyframe_insert(data_path='hide_render',frame=f)
    if rot is not None:o.rotation_euler=rot;o.keyframe_insert(data_path='rotation_euler',frame=f)
def move(objs,a,b,offset):
    for o in objs:key(o,a,offset,True);key(o,b,(0,0,0),True)
def leave(objs,a,b,offset):
    for o in objs:key(o,a,(0,0,0),True);key(o,b,offset,True)
def shaped(k,points):
    for f,v in points:k.value=v;k.keyframe_insert(data_path='value',frame=f)
shots=json.loads((R/'shots.json').read_text());frameset=set(parts)
frameparts=[o for o in parts if o not in groups['panel']+groups['panelscrew']]
railparts=groups['vertical']+groups['tie']
def setup(sh,visible):
    visible=set(visible)|{floor};a,b=sh['start'],sh['end']
    for o in allobjs:
        for f in [a,b]:key(o,f,(0,0,0),o in visible,(0,0,0))
    for k in [springkey,snapkey]:shaped(k,[(a,0),(b,0)])
def sec(sh,t):return min(sh['end'],sh['start']+round(t*24))
for sh in shots:
    name=sh['key'];a,b=sh['start'],sh['end']
    if name in ['reveal','finish']:setup(sh,parts+tile_all)
    elif name=='explode':
        setup(sh,parts)
        for o in parts:
            k=kind(records[o]['component']);p=base[o]
            if k=='panel':off=Vector((p.x*.38,.16,(p.z-.24)*.38))
            elif k=='panelscrew':off=Vector((p.x*.38,.23,(p.z-.24)*.38))
            elif k=='carrier':off=Vector((p.x*.12,.07,(p.z-.24)*.12))
            elif k in ['m2nut','m5']:off=Vector((p.x*.12,.11,(p.z-.24)*.12))
            elif k=='tnut':off=Vector((p.x*.05,.025,(p.z-.24)*.05))
            else:off=Vector((p.x*.15,-.06,(p.z-.24)*.15))
            leave([o],a,sec(sh,3),off);key(o,b,off)
    elif name=='nuts':
        setup(sh,groups['vertical']+groups['tnut'])
        nut=min(groups['tnut'],key=lambda o:abs(cad(o)[0]-240)+abs(cad(o)[1]-449))
        offset=delta(0,505-cad(nut)[1],0);key(nut,a,offset,True)
        move([nut],a+12,b-24,offset)
    elif name=='frame':
        xnuts=[o for o in parts if 'thin METAL channel nut side' in o.name and ' Y:' not in o.name]
        show=groups['vertical']+groups['tnut']+xnuts+[wall];setup(sh,show)
        targets=[o for o in frameparts if kind(records[o]['component']) in ['tie','framehardware','anchor']]
        for o in targets:
            if o in xnuts:continue
            offset=Vector((0,.11,0));start=sec(sh,1.8);duration=32
            if kind(records[o]['component'])=='tie' or 'thin METAL channel nut side' in o.name:start=sec(sh,.3)
            elif 'REFERENCE side M5x8' in o.name:
                paired=records[o]['name'].replace('REFERENCE side M5x8','REFERENCE thin METAL channel nut side')
                nut=next(q for q in parts if records[q]['name']==paired)
                offset=(base[o]-base[nut]).normalized()*.035
                # Orthogonal screws share an approach crossing: insert X first,
                # then Y, instead of letting them pass through each other.
                start=sec(sh,4.0 if ' Y:' in o.name else 3.0);duration=18
            elif kind(records[o]['component'])=='anchor':start=sec(sh,3.4)
            key(o,a,offset,False);move([o],start,min(b-6,start+duration),offset);key(o,b,(0,0,0),True)
    elif name=='carriers':
        setup(sh,[o for o in frameparts if o not in groups['carrier']+groups['m2nut']+groups['m5']]+[wall])
        station=[o for o in groups['carrier']+groups['m2nut']+groups['m5'] if abs(cad(o)[0]-240)<16 and cad(o)[1]<40]
        for o in station:
            k=kind(records[o]['component'])
            if k=='carrier':move([o],a+6,a+38,(0,.045,0))
            elif k=='m5':move([o],a+38,a+60,(0,.04,0))
            else:move([o],a+64,a+116,delta(0,22,0))
            key(o,b,(0,0,0),True)
        shaped(springkey,[(a,0),(a+82,0),(a+96,1),(a+109,1),(a+119,0),(b,0)])
    elif name=='jig':
        setup(sh,frameparts+[wall])
        move(jig,a+4,a+30,(0,.075,0));leave(jig,b-26,b,(0,.075,0))
        screws=[o for o in groups['panelscrew'] if quadrant(o)=='ll']
        move(screws,a+30,a+42,(0,.06,0));leave(screws,b-44,b-30,(0,.06,0))
        for o in screws:key(o,b,(0,.06,0),False)
        move([driver],a+44,a+60,(0,.055,0));leave([driver],a+77,a+89,(0,.055,0));key(driver,b,(0,.055,0),False)
    elif name=='panels':
        setup(sh,frameparts+[wall])
        for i,quad in enumerate(['ll','rl','lu','ru']):
            pp=[o for o in groups['panel'] if quadrant(o)==quad];ss=[o for o in groups['panelscrew'] if quadrant(o)==quad]
            start=a+i*44+2;move(pp,start,start+26,(0,.15,0));move(ss,start+27,start+40,(0,.07,0))
            for o in pp+ss:key(o,b,(0,0,0),True)
    elif name in ['seam','cavity']:
        setup(sh,parts+[wall]+(dimension if name=='cavity' else []))
    elif name=='tile':
        setup(sh,parts+[wall]);move(hero_tile,a+5,a+66,(0,.025,0))
        for o in hero_tile:key(o,b,(0,0,0),True)
        shaped(snapkey,[(a,0),(a+35,0),(a+49,1),(a+60,1),(a+67,0),(b,0)])
    elif name=='art':
        setup(sh,parts+[wall]+hero_tile)
        for (x,y),objs in tiles.items():
            if (x,y)==(235,240):continue
            start=a+int(((x-125)+(y-130))/.43/10)
            start=min(start,b-20);move(objs,start,start+18,(0,.035,0))
            for o in objs:key(o,b,(0,0,0),True)
    elif name=='handle':
        setup(sh,parts+tile_all+[wall])
        leave(clear_tiles,a+2,a+22,(0,.12,0))
        for o in clear_tiles:key(o,a+23,(0,.12,0),False);key(o,b,(0,.12,0),False)
        move(handle,a+24,a+49,(0,.07,0))
        for o in handle:key(o,b,(0,0,0),True)
        for o in handle_rot:
            key(o,a+24,rot=(0,math.pi/2,0));key(o,a+49,rot=(0,math.pi/2,0));key(o,a+62,rot=(0,0,0))
    elif name=='service':
        setup(sh,parts+[o for o in tile_all if o not in clear_tiles]+handle+[wall])
        ss=[o for o in groups['panelscrew'] if quadrant(o)=='ll']
        leave(ss,a+2,a+24,(0,.14,0))
        for o in ss:key(o,a+25,(0,.14,0),False);key(o,b,(0,.14,0),False)
        moving=[o for o in groups['panel'] if quadrant(o)=='ll']+[o for o in ll_art if o not in clear_tiles]+handle
        leave(moving,a+30,a+78,(0,.14,0))
        for o in moving:key(o,b,(0,.14,0),True)

def aim(o,target):o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
def light(name,power,pos,size,color):
    d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;d.color=color
    o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=pos;aim(o,(0,0,.24))
light('Warm softbox',180,(.75,.9,1.1),1.0,(1,.83,.68))
light('Cool fill',140,(-.75,.8,.65),.8,(.58,.8,1))
light('Top strip',180,(0,.1,1.25),.65,(.8,.92,1))
light('Rear edge',160,(.5,-.25,.8),.5,(.4,.75,1))
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Stable shot camera';cam.data.type='ORTHO';s.camera=cam
cam.rotation_mode='QUATERNION';cam.data.clip_start=.001;cam.data.clip_end=100
views={
'reveal':((.23,1.1,.65),(0,0,.20),1.16),
'finish':((-.20,1.1,.61),(0,0,.20),1.16),
'explode':((.62,1.15,.72),(0,0,.21),1.65),
'nuts':((.075,.16,.51),(0,-.024,.467),.19),
'frame':((.32,1.1,.65),(0,-.02,.20),1.19),
'carriers':((.10,.17,.10),(0,-.018,.020),.17),
'jig':((-.38,.75,.40),(-.12,-.005,.105),.75),
'panels':((.43,1.15,.68),(0,.02,.21),1.32),
'seam':((.012,.4,.255),(0,0,.235),.18),
'cavity':((-.46,.028,.065),(-.235,-.014,.020),.15),
'tile':((.042,.16,.28),(-.005,0,.240),.105),
'art':((.16,1,.61),(0,0,.21),1.15),
'handle':((.04,.20,.255),(-.035,.008,.190),.235),
'service':((-.37,.8,.36),(-.12,.03,.08),.86)}
camera_steps=[];prev=None
for sh in shots:
    pos,target,scale=views[sh['key']];pos=Vector(pos);target=Vector(target)
    for f in range(sh['start'],sh['end']+1):
        t=(f-sh['start'])/max(1,sh['end']-sh['start']);u=t*t*(3-2*t)
        drift=Vector((.035*(u-.5),0,0)) if sh['key'] in ['reveal','finish','art'] else Vector((0,0,0))
        cam.location=pos+drift;q=(target-cam.location).to_track_quat('-Z','Y')
        if prev is not None and prev.dot(q)<0:q.negate()
        if f>sh['start'] and prev is not None:camera_steps.append(prev.rotation_difference(q).angle)
        prev=q.copy();cam.rotation_quaternion=q;cam.data.ortho_scale=scale
        cam.keyframe_insert(data_path='location',frame=f);cam.keyframe_insert(data_path='rotation_quaternion',frame=f);cam.data.keyframe_insert(data_path='ortho_scale',frame=f)
for o in allobjs+[cam]:
    if o.animation_data and o.animation_data.action:
        for fc in o.animation_data.action.fcurves:
            for k in fc.keyframe_points:
                if fc.data_path=='hide_render':k.interpolation='CONSTANT'
                elif o==cam:k.interpolation='LINEAR'
                else:k.interpolation='BEZIER';k.handle_left_type='AUTO_CLAMPED';k.handle_right_type='AUTO_CLAMPED'
for fc in cam.data.animation_data.action.fcurves:
    for k in fc.keyframe_points:k.interpolation='CONSTANT'
s.frame_set(1)
report={'cad_instances':len(parts),'unique_cad_meshes':49,'mosaic_tiles':len(tiles),'duration_seconds':60,'fps':24,'frames':1440,'shots':len(shots),'maximum_within_shot_camera_rotation_radians':max(camera_steps),'notes':['Intentional cuts at shot boundaries','Spring and snap deflections are illustrative, not force simulation','Wall anchors and frame hardware remain provisional','Exploded overview is not an installation path','Metal clamp study is not included in assembly']}
for f in [96,888,1440]:
    s.frame_set(f)
    assert all(not o.hide_render and (o.location-base[o]).length<1e-6 for o in parts),('Assembly pose',f)
report['assembled_pose_frames_verified']=[96,888,1440]
s.frame_set(1368)
assert all(not o.hide_render and (o.location-base[o]-Vector((0,.14,0))).length<1e-6 for o in groups['panel'] if quadrant(o)=='ll')
assert all((o.location-base[o]).length<1e-6 for o in groups['panel'] if quadrant(o)!='ll')
report['independent_service_panel_pose_verified']=True
nutshot=next(sh for sh in shots if sh['key']=='nuts')
nut=min(groups['tnut'],key=lambda o:abs(cad(o)[0]-240)+abs(cad(o)[1]-449))
z=[]
for f in range(nutshot['start'],nutshot['end']+1):s.frame_set(f);z.append(nut.location.z)
assert all(q<=p+1e-7 for p,q in zip(z,z[1:])), 'Nut must enter from the rail end without reversing'
report['rail_nut_insertion_monotonic']=True
artshot=next(sh for sh in shots if sh['key']=='art')
for f in [artshot['start'],artshot['end']]:
    s.frame_set(f);assert all(not o.hide_render and (o.location-base[o]).length<1e-6 for o in hero_tile)
report['first_tile_remains_installed_during_art_build']=True
s.frame_set(1)
(R/'scene-validation.json').write_text(json.dumps(report,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(R/'assembly.blend'),compress=True)
print(report)
