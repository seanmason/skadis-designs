import adsk.core,adsk.fusion,os,json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(_context: str):
    a=adsk.core.Application.get();d=adsk.fusion.Design.cast(a.activeProduct)
    assert 'frame assembly' in a.activeDocument.name
    folder=os.path.join(ROOT,'models','v02');ex=d.exportManager
    printable={'Panel lower left':'ll-panel-120','Panel lower right':'lr-panel-120','Panel upper left':'ul-panel-120','Panel upper right':'ur-panel-120','PRINT horizontal alignment key L':'alignment-key-horizontal','PRINT vertical alignment key B':'alignment-key-vertical','PRINT rear bearing seat 00':'rear-bearing-seat'}
    metal={'METAL cap 00':'metal-cap','METAL stepped compression spacer 00':'metal-compression-spacer','METAL rear splice plate 00':'metal-splice-end','METAL rear splice plate 10':'metal-splice-middle','METAL wall standoff 00 - welded or machined':'metal-wall-standoff-left','METAL wall standoff 10 - welded or machined':'metal-wall-standoff-right'}
    assert abs(d.userParameters.itemByName('columns').value-6)<1e-6
    assert abs(d.userParameters.itemByName('rows').value-6)<1e-6
    if d.timeline.timelineGroups.count==0:
        starts=sorted([(o.timelineObject.index,o.component.name) for o in d.rootComponent.occurrences])
        for i in range(len(starts)-1,-1,-1):
            end=starts[i+1][0]-1 if i+1<len(starts) else d.timeline.count-1
            if end>starts[i][0]:
                g=d.timeline.timelineGroups.add(starts[i][0],end);g.name=starts[i][1]
    for o in d.rootComponent.occurrences:
        c=o.component
        if c.name not in printable and c.name not in metal:continue
        filename=printable.get(c.name,metal.get(c.name))
        assert ex.execute(ex.createSTEPExportOptions(os.path.join(folder,filename+'.step'),c))
        if c.name in printable:
            stl=ex.createSTLExportOptions(c,os.path.join(folder,filename+'.stl'));stl.meshRefinement=adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
            assert ex.execute(stl)
    assert ex.execute(ex.createFusionArchiveExportOptions(os.path.join(folder,'frame-assembly-v02.f3d')))
    assert ex.execute(ex.createSTEPExportOptions(os.path.join(folder,'frame-assembly-v02.step'),d.rootComponent))
    d.userParameters.exportUserParameters([p for p in d.userParameters],os.path.join(ROOT,'fusion','frame-assembly-v02-parameters.csv'))
    print('Exported native assembly, assembly STEP, seven printable parts, six metal part STEP files, and parameters')
