"""Separate native development coupons; not load-rated production hardware."""
import adsk.core,adsk.fusion,runpy,os,json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M=runpy.run_path(os.path.join(ROOT,'fusion','FrameSystemV05.py'))
V,P,NEW,CUT,JOIN=[M[k] for k in ('V','P','NEW','CUT','JOIN')]

def finish(b,stem,keep_open=False):
    health=b.health();folder=os.path.join(ROOT,'models','v05','prototypes');os.makedirs(folder,exist_ok=True)
    ex=b.d.exportManager;path=os.path.join(folder,stem)
    cam=b.app.activeViewport.camera;cam.isPerspective=False;cam.isSmoothTransition=False
    cam.eye=P(35,-25,-45);cam.target=P(12,12,0);cam.upVector=adsk.core.Vector3D.create(0,1,0)
    b.app.activeViewport.camera=cam;b.app.activeViewport.fit()
    assert ex.execute(ex.createFusionArchiveExportOptions(path+'.f3d'))
    assert ex.execute(ex.createSTEPExportOptions(path+'.step'))
    seen=set()
    for o in b.root.occurrences:
        if o.component.entityToken in seen:continue
        seen.add(o.component.entityToken)
        stl=ex.createSTLExportOptions(o.component,path+'--'+o.component.name.replace(' ','-')+'.stl')
        stl.meshRefinement=adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
        assert ex.execute(stl)
    b.app.activeViewport.saveAsImageFile(path+'.png',1200,1000)
    with open(path+'-health.json','w') as f:json.dump(health,f,indent=2)
    print(stem,health)
    if not keep_open:
        b.doc.close(False)
        if any(d.name==M['NAME'] for d in b.app.documents):M['active']()

def jig(_context):
    b=M['Builder']();b.doc.name='SKADIS v0.5 carrier positioning jig'
    c=b.comp('PRINT alignment jig')
    b.box(c,'4 mm','14 mm','12 mm','panelHeight-28 mm','0 mm','boardThickness','Left spine')
    b.box(c,'4 mm','14 mm','panelWidth-8 mm','12 mm','0 mm','boardThickness','Bottom bridge',JOIN)
    b.box(c,'panelWidth-16 mm','14 mm','12 mm','panelHeight-28 mm','0 mm','boardThickness','Right spine',JOIN)
    b.box(c,'4 mm','panelHeight-26 mm','panelWidth-8 mm','12 mm','0 mm','boardThickness','Top bridge',JOIN)
    for x in ['pitch/2','panelWidth-pitch/2']:
        for y in ['pitch','panelHeight-pitch']:
            b.disk(c,x,y,'panelClearance','0 mm','boardThickness','Temporary M2 locating screw',CUT)
            b.cone(c,x,y,'panelHeadPocket','0 mm','(panelHeadPocket-panelClearance)/2',CUT,'Flush temporary screw seat')
            b.box(c,x+'-tongueWidth/2-registerClearance',y+'-tongueLength/2-registerClearance','tongueWidth+2*registerClearance','tongueLength+2*registerClearance','boardThickness','-tongueDepth-0.2 mm','Carrier pad locating socket',CUT)
        b.disk(c,x,'panelHeight-pitch-11 mm','10 mm','0 mm','boardThickness','Upper M5 driver access',CUT)
    finish(b,'carrier-jig-240')

def mosaic(_context,terminal='none'):
    assert terminal in ['none','top','bottom']
    b=M['Builder']();b.doc.name='SKADIS v0.5 axial mosaic '+terminal+' coupon'
    for n,e in [('pixelGap','0.4 mm'),('pixelThickness','1.2 mm'),('tileBack','0.8 mm'),('snapInterference','0.4 mm')]:
        b.d.userParameters.add(n,V(e),'mm','Prototype; tune after physical testing')
    c=b.comp('PRINT tile core')
    b.box(c,'-4.5 mm','-19.5 mm' if terminal=='bottom' else '-9.5 mm','9 mm','19 mm' if terminal=='none' else '29 mm','-tileBack','tileBack','Structural backing with terminal extension')
    b.box(c,'-0.6 mm','-slotHeight/2+0.2 mm','1.2 mm','slotHeight-0.4 mm','0 mm','boardThickness-0.2 mm','Central gravity bearing and vertical registration spine',JOIN)
    # Two independent cantilevers bend toward the middle during axial insertion.
    for side in [-1,1]:
        pts=[('0.8 mm','0 mm'),('2.2 mm','0 mm'),('2.2 mm','boardThickness-0.2 mm'),('(slotWidth+snapInterference)/2','boardThickness+0.5 mm'),('(slotWidth+snapInterference)/2','boardThickness+0.9 mm'),('1.6 mm','boardThickness+2.1 mm'),('0.8 mm','boardThickness+2.1 mm')]
        verts=[['('+x+')*'+str(side),'-3 mm',z] for x,z in pts]
        b.poly3(c,'y','-3 mm',verts,'6 mm',JOIN,'Axial spring '+str(side)+' with insertion and release ramps')
    pixels=[('lower','-10 mm+pixelGap/2'),('upper','pixelGap/2')]
    if terminal!='none':pixels.append(('terminal',('10 mm' if terminal=='top' else '-20 mm')+'+pixelGap/2'))
    for label,y in pixels:
        f=b.comp('COLOR pixel '+label)
        b.box(f,'-5 mm+pixelGap/2',y,'10 mm-pixelGap','10 mm-pixelGap','-tileBack-pixelThickness','pixelThickness','Co-printed pixel color region')
    # Printed coupon uses the same slot tool as the production board.
    q=b.comp('PRINT fit coupon')
    b.box(q,'20 mm','-10 mm','20 mm','40 mm','0 mm','boardThickness','Coupon blank')
    b.slot_pattern(q,'30 mm','0 mm','1','2','Standard throat test slots')
    body=q.bRepBodies.item(0)
    front=[f for f in body.faces if abs(f.boundingBox.minPoint.z)<1e-7 and abs(f.boundingBox.maxPoint.z)<1e-7]
    b.fillet(q,front,'entryRadius','Rounded coupon entrances')
    finish(b,'axial-mosaic-tile'+('' if terminal=='none' else '-'+terminal+'-terminal'))

def handle(_context):
    b=M['Builder']();b.doc.name='SKADIS v0.5 two-slot handling tool concept'
    b.d.userParameters.add('handlePitch',V('40 mm'),'mm','Use two A slots on one panel; clear surrounding artwork first')
    c=b.comp('PRINT handle bridge')
    b.box(c,'-7 mm','-7 mm','handlePitch+14 mm','14 mm','-16 mm','5 mm','Front handle bridge')
    for x in ['0 mm','handlePitch']:
        b.disk(c,x,'0 mm','5.3 mm','-16 mm','5 mm','Rotating key and assembly clearance',CUT)
        k=b.comp('PRINT quarter-turn key '+x)
        b.disk(k,x,'0 mm','4 mm','-16 mm','24 mm','Key shaft')
        b.box(k,x+'-1.8 mm','-1.8 mm','3.6 mm','3.6 mm','-18 mm','2 mm','Square knob drive',JOIN)
        b.disk(k,x,'0 mm','1.6 mm','-18 mm','6 mm','M2 pilot - tapping trial required',CUT)
        b.box(k,x+'-4.5 mm','-1.5 mm','9 mm','3 mm','5.5 mm','2.5 mm','Locked transverse bearing tab',JOIN)
        knob=b.comp('PRINT thumb knob '+x)
        b.disk(knob,x,'0 mm','12 mm','-21 mm','5 mm','Separate thumb knob')
        b.box(knob,x+'-1.9 mm','-1.9 mm','3.8 mm','3.8 mm','-16 mm','-2.2 mm','Square drive socket',CUT)
        b.disk(knob,x,'0 mm','2.4 mm','-21 mm','5 mm','M2 fixing clearance',CUT)
        b.cone(knob,x,'0 mm','4 mm','-21 mm','0.8 mm',CUT,'M2 flush head recess')
        b.screw('REFERENCE handle M2x6 '+x,x,'0 mm','2 mm','3.8 mm','-20.9 mm','6 mm')
    finish(b,'panel-handling-tool-concept')

def panel_variant(size,edges=(0,0,0,0),label='interior',gap='0.35 mm',validate=False):
    b=M['Builder']();b.doc.name='SKADIS v0.5 '+str(size)+' '+label
    for n in ['columns','rows']:b.d.userParameters.itemByName(n).expression=str(size//20)
    b.d.userParameters.itemByName('seamGap').expression=gap
    b.clean_panel(label,'0 mm','0 mm',edges,'variant')
    finish(b,'panel-'+label+'-'+str(size)+'-gap-'+gap.replace(' mm',''),validate)
    if validate:
        resize_check('')
        b.doc.close(False)
        if any(d.name==M['NAME'] for d in b.app.documents):M['active']()

def seam_array(gap='0.35 mm'):
    b=M['Builder']();b.doc.name='SKADIS v0.5 surrounded seam test '+gap
    for n in ['columns','rows']:b.d.userParameters.itemByName(n).expression='4'
    b.d.userParameters.itemByName('seamGap').expression=gap
    b.clean_panel('80 mm whole-slot coupon','0 mm','0 mm',(0,0,0,0),'coupon')
    col=adsk.core.ObjectCollection.create();col.add(b.root.occurrences.item(0))
    pi=b.root.features.rectangularPatternFeatures.createInput(col,b.root.xConstructionAxis,V('3'),V('panelWidth'),adsk.fusion.PatternDistanceType.SpacingPatternDistanceType)
    pi.setDirectionTwo(b.root.yConstructionAxis,V('3'),V('panelHeight'))
    b.root.features.rectangularPatternFeatures.add(pi).name='Nine coupons surround center panel for service test'
    finish(b,'seam-array-3x3-gap-'+gap.replace(' mm',''))

def clamp(_context):
    b=M['Builder']();b.doc.name='SKADIS v0.5 metal compression clamp study'
    b.d.userParameters.add('limiterGap',V('0.2 mm'),'mm','Uncompressed axial gap; establish by material and torque trials')
    c=b.comp('PRINT clamp coupon')
    b.box(c,'0 mm','0 mm','30 mm','31 mm','15 mm','7 mm','Carrier clamp test block')
    b.disk(c,'15 mm','10 mm','8.2 mm','15 mm','7 mm','Metal sleeve bore',CUT)
    b.disk(c,'15 mm','10 mm','12.2 mm','15 mm','3 mm','Front flange bearing counterbore',CUT)
    s=b.comp('CUSTOM METAL flanged countersunk limiter')
    b.disk(s,'15 mm','10 mm','12 mm','15 mm','3 mm','Broad front flange')
    b.disk(s,'15 mm','10 mm','8 mm','18 mm','4 mm-limiterGap','Compression sleeve',JOIN)
    b.disk(s,'15 mm','10 mm','5.5 mm','15 mm','7 mm','M5 passage',CUT)
    b.cone(s,'15 mm','10 mm','9.4 mm','15 mm','1.95 mm',CUT,'M5 countersunk metal seat')
    w=b.comp('METAL rear spreader washer 12x5.5x1')
    b.disk(w,'15 mm','10 mm','12 mm','22 mm','1 mm','Washer bridging profile mouth')
    b.disk(w,'15 mm','10 mm','5.5 mm','22 mm','1 mm','Washer clearance',CUT)
    # Separate study deliberately shows the uncompressed limiter gap. It adds
    # 1 mm to the carrier-to-rail stack and is not substituted in the assembly.
    finish(b,'metal-clamp-study')

def resize_check(_context):
    b=M['Builder'].__new__(M['Builder']);b.app=adsk.core.Application.get()
    b.doc=b.app.activeDocument;b.d=adsk.fusion.Design.cast(b.app.activeProduct);b.root=b.d.rootComponent
    assert 'interior' in b.doc.name and b.root.occurrences.count==1,b.doc.name
    before={n:b.d.userParameters.itemByName(n).expression for n in ['columns','rows']}
    report=[]
    try:
        for count in [4,14,12]:
            assert b.d.modifyParameters([b.d.userParameters.itemByName(n) for n in ['columns','rows']],[V(str(count)),V(str(count))])
            assert b.d.computeAll()
            health=b.health();body=b.root.occurrences.item(0).component.bRepBodies.item(0)
            front=[f for f in body.faces if abs(f.boundingBox.minPoint.z)<1e-7 and abs(f.boundingBox.maxPoint.z)<1e-7]
            slots=sum(f.loops.count-1 for f in front)-4
            assert slots==2*count*count,(slots,count)
            bb=body.boundingBox;bounds=[10*(getattr(bb.maxPoint,k)-getattr(bb.minPoint,k)) for k in ['x','y','z']]
            expected=[20*count-.35,20*count+10-.35,5]
            assert all(abs(a-e)<.001 for a,e in zip(bounds,expected)),(bounds,expected)
            report.append({'cells':count,'whole_slot_loops':slots,'bounds_mm':bounds,'health':health})
    finally:
        assert b.d.modifyParameters([b.d.userParameters.itemByName(n) for n in before],[V(e) for e in before.values()])
        b.d.computeAll()
    with open(os.path.join(ROOT,'docs','resize-validation-v05.json'),'w') as f:json.dump(report,f,indent=2)
    print(report)
