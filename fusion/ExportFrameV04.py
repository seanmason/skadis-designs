import adsk.core,adsk.fusion,runpy,os,json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def run(_context):
    b=runpy.run_path(os.path.join(ROOT,'fusion','FrameSystemV04.py'))['active']();d=b.d
    health=b.health();folder=os.path.join(ROOT,'models','v04');os.makedirs(folder,exist_ok=True);ex=d.exportManager
    assert d.userParameters.itemByName('columns').value==6 and d.userParameters.itemByName('rows').value==6
    printable={'Panel lower left':'panel-lower-left-120','Panel lower right':'panel-lower-right-120','Panel upper left':'panel-upper-left-120','Panel upper right':'panel-upper-right-120','PRINT carrier 00 single':'carrier-single','PRINT carrier 10 double':'carrier-double','PRINT nut keeper 000':'nut-keeper'}
    done=set()
    for o in b.root.occurrences:
        c=o.component
        if c.name not in printable or c.entityToken in done:continue
        done.add(c.entityToken)
        path=os.path.join(folder,printable[c.name])
        assert ex.execute(ex.createSTEPExportOptions(path+'.step',c))
        stl=ex.createSTLExportOptions(c,path+'.stl');stl.meshRefinement=adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
        assert ex.execute(stl)
    # Group contiguous timeline ranges only after all geometry and checks are complete.
    if d.timeline.timelineGroups.count==0:
        seen=set();starts=[]
        for o in b.root.occurrences:
            c=o.component
            if c.entityToken in seen:continue
            seen.add(c.entityToken)
            if c.name.startswith(('Panel ','Vertical rail','Horizontal tie','PRINT carrier','METAL in-bay','METAL flush wall')):starts.append((o.timelineObject.index,c.name))
        starts+= [(f.timelineObject.index,f.name) for f in b.root.features.rectangularPatternFeatures]
        starts+= [(f.timelineObject.index,f.name) for f in b.root.features.circularPatternFeatures]
        last_pattern=max(f.timelineObject.index for f in list(b.root.features.rectangularPatternFeatures)+list(b.root.features.circularPatternFeatures))
        late=[f.timelineObject.index-2 for c in d.allComponents for f in c.features.extrudeFeatures if f.name=='Split registration into printable end pads' and f.timelineObject.index>last_pattern]
        if late:starts.append((min(late),'Printability refinement - registration pads'))
        starts.sort()
        for i in range(len(starts)-1,-1,-1):
            end=starts[i+1][0]-1 if i+1<len(starts) else d.timeline.count-1
            if end>starts[i][0]:d.timeline.timelineGroups.add(starts[i][0],end).name=starts[i][1]
    assert ex.execute(ex.createFusionArchiveExportOptions(os.path.join(folder,'frame-assembly-v04.f3d')))
    assert ex.execute(ex.createSTEPExportOptions(os.path.join(folder,'frame-assembly-v04.step')))
    d.userParameters.exportUserParameters([p for p in d.userParameters],os.path.join(ROOT,'fusion','frame-assembly-v04-parameters.csv'))
    cam=b.app.activeViewport.camera;cam.isPerspective=False;cam.isSmoothTransition=False
    cam.eye=adsk.core.Point3D.create(12,12,-60);cam.target=adsk.core.Point3D.create(12,12,0);cam.upVector=adsk.core.Vector3D.create(0,1,0)
    b.app.activeViewport.camera=cam;b.app.activeViewport.fit();b.app.activeViewport.refresh()
    b.app.activeViewport.saveAsImageFile(os.path.join(folder,'front.png'),1400,1200)
    cam=b.app.activeViewport.camera;cam.eye=adsk.core.Point3D.create(42,-25,55);cam.target=adsk.core.Point3D.create(12,12,2);cam.upVector=adsk.core.Vector3D.create(0,1,0)
    b.app.activeViewport.camera=cam;b.app.activeViewport.fit();b.app.activeViewport.refresh()
    b.app.activeViewport.saveAsImageFile(os.path.join(folder,'rear.png'),1600,1200)
    for o in b.root.occurrences:
        o.isLightBulbOn=o.name in ['PRINT carrier 00 single:1','METAL M2 nut 000:1','PRINT nut keeper 000:1','REFERENCE panel M2x20 000:1','REFERENCE carrier M5x12 00:1','METAL channel nut 00:1','Vertical rail 0 - measured sloped-slot approximation:1']
    cam=b.app.activeViewport.camera;cam.eye=adsk.core.Point3D.create(8,-7,-6);cam.target=adsk.core.Point3D.create(1,2,1.5);cam.upVector=adsk.core.Vector3D.create(0,1,0);cam.viewExtents=6
    b.app.activeViewport.camera=cam;b.app.activeViewport.refresh()
    b.app.activeViewport.saveAsImageFile(os.path.join(folder,'connection-detail-panel-hidden.png'),1400,1100)
    for o in b.root.occurrences:o.isLightBulbOn=True
    cam=b.app.activeViewport.camera;cam.eye=adsk.core.Point3D.create(12,12,-60);cam.target=adsk.core.Point3D.create(12,12,0);cam.upVector=adsk.core.Vector3D.create(0,1,0)
    b.app.activeViewport.camera=cam;b.app.activeViewport.fit()
    assert ex.execute(ex.createFusionArchiveExportOptions(os.path.join(folder,'frame-assembly-v04.f3d')))
    print('Export complete',health)
