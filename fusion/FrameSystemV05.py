"""v0.5 stepped whole-slot panel prototype. Native feature patterns permit resizing.

The 480 mm demonstration retains provisional v0.4 frame hardware and adds captive
nut springs. Tooling, mosaic and metal-clamp studies have separate native models.
Run phases separately.
"""
import adsk.core, adsk.fusion, runpy, os, json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M=runpy.run_path(os.path.join(ROOT,'fusion','FrameSystemV04.py'))
V,P,NEW,CUT,JOIN=[M[k] for k in ('V','P','NEW','CUT','JOIN')]
NAME='Infinite SKADIS HD v0.5 - stepped seam 480 prototype'

class Builder(M['Builder']):
    def __init__(self):
        super().__init__()
        self.doc.name=NAME
        for n,e in [('columns','12'),('rows','12'),('seamGap','0.35 mm')]:
            self.d.userParameters.itemByName(n).expression=e
        self.d.userParameters.add('stepCorner',V('0.6 mm'),'mm','Small plan corner relief; printed fit remains untested')
    def pattern_x(self,c,f,name,count='columns'):
        oc=adsk.core.ObjectCollection.create()
        for feature in (f if isinstance(f,list) else [f]):oc.add(feature)
        pi=c.features.rectangularPatternFeatures.createInput(oc,c.xConstructionAxis,V(count),V('pitch'),adsk.fusion.PatternDistanceType.SpacingPatternDistanceType)
        pi.setDirectionTwo(c.yConstructionAxis,V('1'),V('pitch'))
        p=c.features.rectangularPatternFeatures.add(pi);p.name=name
        return p
    def round_step_tip(self,c,y,xlo,xhi,name):
        edges=[]
        for e in c.bRepBodies.item(0).edges:
            bb=e.boundingBox
            if abs(bb.maxPoint.z-bb.minPoint.z-self.value('boardThickness'))>1e-6:continue
            if abs(bb.minPoint.y-self.value(y))<1e-6 and any(abs(bb.minPoint.x-self.value(x))<1e-6 for x in [xlo,xhi]):edges.append(e)
        assert edges,name
        return self.fillet(c,edges,'stepCorner',name)
    def carrier(self,i,j):
        c=super().carrier(i,j)
        label=str(i)+str(j);x=M['XS'][i];y=M['YS'][j]
        # Replace separate keeper plugs with a roof cantilever and retaining ramp.
        for o in list(self.root.occurrences):
            if o.component.name.startswith('PRINT nut keeper '+label):o.deleteMe()
        axes=[x+'-pitch/2',x+'+pitch/2'] if i==1 else [x]
        for xx in axes:
            self.box(c,xx+'-2.15 mm',y+'+2.5 mm','4.3 mm','0.5 mm','carrierZ+4 mm','3 mm','Release free end of nut-retaining spring',CUT)
            self.box(c,xx+'-2.15 mm',y+'+3 mm','4.3 mm','10 mm','carrierZ+4.8 mm','2.2 mm','Nut spring deflection space',CUT)
            for dx in ['-2.15 mm','+1.65 mm']:
                self.box(c,xx+dx,y+'+3 mm','0.5 mm','10 mm','carrierZ+4 mm','0.8 mm','Nut spring side relief',CUT)
            verts=[[xx+'-1.65 mm',y+'+3 mm','carrierZ+4.2 mm'],[xx+'-1.65 mm',y+'+4.6 mm','carrierZ+4.2 mm'],[xx+'-1.65 mm',y+'+3.8 mm','carrierZ+2.8 mm'],[xx+'-1.65 mm',y+'+3 mm','carrierZ+2.8 mm']]
            self.poly3(c,'x',xx+'-1.65 mm',verts,'3.3 mm',JOIN,'Integral nut retaining ramp - flex test required')
        return c
    def clean_panel(self,label,ox,oy,edges,prefix):
        c=self.comp('Panel '+label);x='('+ox+')';y='('+oy+')'
        for s,e in zip(('Left','Right','Bottom','Top'),edges):
            p=self.d.userParameters.itemByName(prefix+s)
            if p:assert p.value==e,(prefix+s,p.value,e)
            else:self.d.userParameters.add(prefix+s,V(str(e)),'','Edge topology selected when generated; regenerate to change edge type')
        self.box(c,x+'+seamGap/2',y+'+seamGap/2','panelWidth-seamGap','panelHeight-seamGap','0 mm','boardThickness','01 Main panel web')
        if not edges[3]:
            f=self.box(c,x+'+pitch/2+seamGap/2',y+'+panelHeight-1 mm','pitch/2-seamGap','pitch/2+1 mm-seamGap/2','0 mm','boardThickness','02 Whole-slot upper tooth',JOIN)
            tip=self.round_step_tip(c,y+'+panelHeight+pitch/2-seamGap/2',x+'+pitch/2+seamGap/2',x+'+pitch-seamGap/2','02 Rounded tooth tip seed')
            self.pattern_x(c,[f,tip],'03 Upper teeth and rounding follow column count')
        if not edges[2]:
            f=self.box(c,x+'+pitch/2-seamGap/2',y+'-1 mm','pitch/2+seamGap','pitch/2+1 mm+seamGap/2','0 mm','boardThickness','04 Lower receiving step',CUT)
            tip=self.round_step_tip(c,y+'+pitch/2+seamGap/2',x+'+pitch/2-seamGap/2',x+'+pitch+seamGap/2','04 Rounded receiving step seed')
            self.pattern_x(c,[f,tip],'05 Receiving steps and rounding follow column count','columns-1')
            self.box(c,x+'+panelWidth-pitch/2-seamGap/2',y+'-1 mm','pitch/2+seamGap','pitch/2+1 mm+seamGap/2','0 mm','boardThickness','05 Terminal receiving step',CUT)
            self.round_step_tip(c,y+'+pitch/2+seamGap/2',x+'+panelWidth-pitch/2-seamGap/2',x+'+panelWidth+seamGap/2','05 Rounded terminal receiving step')
        body=c.bRepBodies.item(0)
        outer=[]
        for edge in body.edges:
            bb=edge.boundingBox
            if abs(bb.maxPoint.z-bb.minPoint.z-self.value('boardThickness'))>1e-6:continue
            xx=(bb.minPoint.x+bb.maxPoint.x)/2;yy=(bb.minPoint.y+bb.maxPoint.y)/2
            atleft=abs(xx-self.value(x+'+seamGap/2'))<1e-6
            atright=abs(xx-self.value(x+'+panelWidth-seamGap/2'))<1e-6
            atbottom=abs(yy-self.value(y+'+seamGap/2'))<1e-6
            attop=abs(yy-self.value(y+'+panelHeight-seamGap/2'))<1e-6
            if ((atleft and edges[0]) or (atright and edges[1])) and ((atbottom and edges[2]) or (attop and edges[3])):outer.append(edge)
        if outer:self.fillet(c,outer,'cornerRadius','06 Finished exterior corner radius')
        # Round the feature seeds before patterning. Selecting every repeated edge
        # here loses references when columns decreases and is intentionally avoided.
        self.slot_pattern(c,x+'+pitch/4',y+'+pitch/2','columns','rows','08 Whole A slots')
        self.slot_pattern(c,x+'+3*pitch/4',y+'+pitch','columns','rows-'+prefix+'Top','09 Whole B slots owned by this panel')
        front=[f for f in body.faces if abs(f.boundingBox.minPoint.z)<1e-7 and abs(f.boundingBox.maxPoint.z)<1e-7]
        self.fillet(c,front,'entryRadius','10 Rounded slot entrances and face outline')
        for xx in [x+'+pitch/2',x+'+panelWidth-pitch/2']:
            for yy in [y+'+pitch',y+'+panelHeight-pitch']:
                self.disk(c,xx,yy,'panelClearance','0 mm','boardThickness','11 M2 through bore',CUT)
                self.cone(c,xx,yy,'panelHeadPocket','0 mm','(panelHeadPocket-panelClearance)/2',CUT,'12 Flush countersink')
                self.box(c,xx+'-tongueWidth/2-registerClearance',yy+'-tongueLength/2-registerClearance','tongueWidth+2*registerClearance','tongueLength+2*registerClearance','boardThickness','-tongueDepth-0.2 mm','13 Blind rear registration',CUT)
        return c

def active():
    b=Builder.__new__(Builder);b.app=adsk.core.Application.get()
    doc=[d for d in b.app.documents if d.name==NAME][-1]
    doc.activate();b.doc=doc;b.d=adsk.fusion.Design.cast(b.app.activeProduct);b.root=b.d.rootComponent
    return b

def start(_context):
    b=Builder();print('Created',b.doc.name)

def panel(index):
    b=active();b.clean_panel(*M['PANELS'][index]);print(b.health())

def replace_panel(index):
    b=active();args=M['PANELS'][index]
    old=[o for o in b.root.occurrences if o.component.name=='Panel '+args[0]]
    assert len(old)==1,len(old)
    old[0].deleteMe()
    start=b.d.timeline.count
    b.clean_panel(*args)
    b.d.timeline.timelineGroups.add(start,b.d.timeline.count-1).name='Revised parametric Panel '+args[0]
    print(b.health())

def phase(name,*args):
    # Reuse the established frame construction without changing historical source.
    fn=M[name];fn.__globals__['active']=active
    fn(*args)

def repeat_carriers(_context):
    b=active();left=[];middle=[]
    def pattern(occs,axis,distance,name):
        col=adsk.core.ObjectCollection.create()
        for o in occs:col.add(o)
        pi=b.root.features.rectangularPatternFeatures.createInput(col,axis,V('2'),V(distance),adsk.fusion.PatternDistanceType.SpacingPatternDistanceType)
        pi.setDirectionTwo(b.root.yConstructionAxis if axis==b.root.xConstructionAxis else b.root.xConstructionAxis,V('1'),V('pitch'))
        b.root.features.rectangularPatternFeatures.add(pi).name=name
    seed_names={'PRINT carrier 00 single','METAL M2 nut 000','REFERENCE panel M2x20 000','REFERENCE carrier M5x12 00','METAL channel nut 00'}
    seed=[o for o in b.root.occurrences if o.component.name in seed_names]
    assert len(seed)==5,len(seed)
    for j,distance in [(1,'panelHeight-2*pitch'),(2,'panelHeight'),(3,'2*panelHeight-2*pitch')]:
        if not any(o.component.name=='PRINT carrier 0'+str(j)+' single' for o in b.root.occurrences):
            pattern(seed,b.root.yConstructionAxis,distance,'Repeated left captive carrier '+str(j))
    for o in b.root.occurrences:
        if o.component.name.startswith(('PRINT carrier','METAL M2 nut','REFERENCE panel M2','REFERENCE carrier M5','METAL channel nut')):
            (left if o.component.bRepBodies.item(0).boundingBox.maxPoint.x<b.value('panelWidth/2') else middle).append(o)
    assert len(left)==20 and len(middle)==7,(len(left),len(middle))
    pattern(left,b.root.xConstructionAxis,'2*panelWidth-pitch','Right rail captive nut carriers')
    for distance in ['panelHeight-2*pitch','panelHeight','2*panelHeight-2*pitch']:
        pattern(middle,b.root.yConstructionAxis,distance,'Shared captive carrier '+distance)
    print(b.health())

def repeat_joints(_context):
    b=active()
    occs=[o for o in b.root.occurrences if o.component.name.startswith(('METAL in-bay','REFERENCE side M5x8','REFERENCE thin METAL channel nut side'))]
    assert len(occs)==10,len(occs)
    col=adsk.core.ObjectCollection.create()
    for o in occs:col.add(o)
    pi=b.root.features.rectangularPatternFeatures.createInput(col,b.root.xConstructionAxis,V('2'),V('panelWidth-pitch/2'),adsk.fusion.PatternDistanceType.SpacingPatternDistanceType)
    pi.setDirectionTwo(b.root.yConstructionAxis,V('1'),V('pitch'))
    b.root.features.rectangularPatternFeatures.add(pi).name='Second bay bottom joints'
    phase('repeat_frame_joints','')

def export(_context):
    b=active();folder=os.path.join(ROOT,'models','v05');os.makedirs(folder,exist_ok=True)
    health=b.health();ex=b.d.exportManager
    exported=set()
    for o in b.root.occurrences:
        c=o.component
        label=c.name.lower().replace(' ','-')+'-240' if c.name.startswith('Panel ') else {'PRINT carrier 00 single':'carrier-single-captive','PRINT carrier 10 double':'carrier-double-captive'}.get(c.name)
        if not label or label in exported:continue
        exported.add(label);stem=os.path.join(folder,label)
        assert ex.execute(ex.createSTEPExportOptions(stem+'.step',c))
        opt=ex.createSTLExportOptions(c,stem+'.stl');opt.meshRefinement=adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
        assert ex.execute(opt)
    cam=b.app.activeViewport.camera;cam.isPerspective=False;cam.isSmoothTransition=False
    cam.eye=P(24,24,-90);cam.target=P(24,24,0);cam.upVector=adsk.core.Vector3D.create(0,1,0)
    b.app.activeViewport.camera=cam;b.app.activeViewport.fit();b.app.activeViewport.refresh()
    b.app.activeViewport.saveAsImageFile(os.path.join(folder,'front.png'),1500,1500)
    cam=b.app.activeViewport.camera;cam.viewExtents=8
    b.app.activeViewport.camera=cam;b.app.activeViewport.refresh()
    b.app.activeViewport.saveAsImageFile(os.path.join(folder,'seam-detail.png'),1400,1100)
    visibility=[(o,o.isLightBulbOn) for o in b.root.occurrences]
    for o,_ in visibility:o.isLightBulbOn=o.component.name.startswith('Panel ')
    b.app.activeViewport.refresh()
    b.app.activeViewport.saveAsImageFile(os.path.join(folder,'seam-detail-panels-only.png'),1400,1100)
    for o,visible in visibility:o.isLightBulbOn=visible
    cam=b.app.activeViewport.camera;cam.eye=P(65,-35,85);cam.target=P(24,24,2);cam.upVector=adsk.core.Vector3D.create(0,1,0)
    b.app.activeViewport.camera=cam;b.app.activeViewport.fit();b.app.activeViewport.refresh()
    b.app.activeViewport.saveAsImageFile(os.path.join(folder,'rear.png'),1500,1500)
    cam=b.app.activeViewport.camera;cam.eye=P(24,24,-90);cam.target=P(24,24,0);cam.upVector=adsk.core.Vector3D.create(0,1,0)
    b.app.activeViewport.camera=cam;b.app.activeViewport.fit()
    if b.d.timeline.timelineGroups.count==0:
        starts=[];seen=set()
        for o in b.root.occurrences:
            c=o.component
            if c.entityToken in seen:continue
            seen.add(c.entityToken)
            if c.name.startswith(('Panel ','Vertical rail','Horizontal tie','PRINT carrier','METAL in-bay','METAL flush wall')):
                starts.append((o.timelineObject.index,c.name))
        for f in list(b.root.features.rectangularPatternFeatures)+list(b.root.features.circularPatternFeatures):starts.append((f.timelineObject.index,f.name))
        starts.sort()
        for i in range(len(starts)-1,-1,-1):
            end=starts[i+1][0]-1 if i+1<len(starts) else b.d.timeline.count-1
            if end>starts[i][0]:b.d.timeline.timelineGroups.add(starts[i][0],end).name=starts[i][1]
    health=b.health()
    assert ex.execute(ex.createFusionArchiveExportOptions(os.path.join(folder,'frame-assembly-v05.f3d')))
    assert ex.execute(ex.createSTEPExportOptions(os.path.join(folder,'frame-assembly-v05.step')))
    b.d.userParameters.exportUserParameters(list(b.d.userParameters),os.path.join(ROOT,'fusion','frame-assembly-v05-parameters.csv'))
    with open(os.path.join(ROOT,'docs','health-v05.json'),'w') as f:json.dump(health,f,indent=2)
    print(health)
