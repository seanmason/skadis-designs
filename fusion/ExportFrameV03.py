import adsk.core,adsk.fusion,os,runpy
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(_context: str):
    b=runpy.run_path(os.path.join(ROOT,'fusion','FrameSystemV03.py'))['active']();d=b.d
    print(b.health())
    folder=os.path.join(ROOT,'models','v03');os.makedirs(folder,exist_ok=True);ex=d.exportManager
    printable={'Panel lower left':'ll-panel-120','Panel lower right':'lr-panel-120','Panel upper left':'ul-panel-120','Panel upper right':'ur-panel-120','PRINT registration seat 00':'registration-seat'}
    metal={'METAL cap 00':'metal-cap','METAL stepped compression spacer 00':'metal-compression-spacer','METAL in-bay corner 00L':'metal-in-bay-corner','METAL flush wall tab 00':'metal-flush-wall-tab-left','METAL flush wall tab 10':'metal-flush-wall-tab-right'}
    assert d.userParameters.itemByName('columns').value==6 and d.userParameters.itemByName('rows').value==6
    if d.timeline.timelineGroups.count==0:
        starts=sorted([(o.timelineObject.index,o.component.name) for o in d.rootComponent.occurrences])
        for i in range(len(starts)-1,-1,-1):
            end=starts[i+1][0]-1 if i+1<len(starts) else d.timeline.count-1
            if end>starts[i][0]:d.timeline.timelineGroups.add(starts[i][0],end).name=starts[i][1]
    for o in d.rootComponent.occurrences:
        c=o.component
        if c.name not in printable and c.name not in metal:continue
        filename=printable.get(c.name,metal.get(c.name))
        assert ex.execute(ex.createSTEPExportOptions(os.path.join(folder,filename+'.step'),c))
        if c.name in printable:
            stl=ex.createSTLExportOptions(c,os.path.join(folder,filename+'.stl'));stl.meshRefinement=adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
            assert ex.execute(stl)
    assert ex.execute(ex.createFusionArchiveExportOptions(os.path.join(folder,'frame-assembly-v03.f3d')))
    assert ex.execute(ex.createSTEPExportOptions(os.path.join(folder,'frame-assembly-v03.step'),b.root))
    d.userParameters.exportUserParameters([p for p in d.userParameters],os.path.join(ROOT,'fusion','frame-assembly-v03-parameters.csv'))
    print('v0.3 assembly and part exports complete')
