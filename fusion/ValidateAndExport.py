import adsk.core, adsk.fusion, os, json
def run(_context: str):
    app=adsk.core.Application.get()
    d=adsk.fusion.Design.cast(app.activeProduct)
    folder=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assert d and d.userParameters.itemByName('registerDiameter'), 'Activate the InfiniteSkadis master first'
    panel=d.rootComponent.occurrences.item(0).component
    assert panel.name.startswith('Panel - dense'), 'Activate the master, not another design'
    report=[]
    def health():
        return [(d.timeline.item(i).name,d.timeline.item(i).errorOrWarningMessage) for i in range(d.timeline.count) if d.timeline.item(i).healthState!=adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState]
    def export_part(c,name):
        ex=d.exportManager
        assert ex.execute(ex.createSTEPExportOptions(os.path.join(folder,'models',name+'.step'),c))
        stl=ex.createSTLExportOptions(c,os.path.join(folder,'models',name+'.stl'))
        stl.meshRefinement=adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
        assert ex.execute(stl)
    for cols,rows in [(4,4),(8,12),(14,14),(12,12)]:
        d.userParameters.itemByName('columns').expression=str(cols)
        d.userParameters.itemByName('rows').expression=str(rows)
        d.computeAll()
        errors=health()
        b=panel.bRepBodies.item(0); box=b.boundingBox
        dims=[round((box.maxPoint.x-box.minPoint.x)*10,4),round((box.maxPoint.y-box.minPoint.y)*10,4),round((box.maxPoint.z-box.minPoint.z)*10,4)]
        assert not errors, str(errors)
        assert dims==[cols*20,rows*20,5], str(dims)
        assert b.isSolid and panel.bRepBodies.count==1
        report.append({'columns':cols,'rows':rows,'size_mm':dims,'healthy':not errors,'solid':b.isSolid,'volume_cm3':b.volume})
        if cols==4: export_part(panel,'panel-fit-coupon-80x80')
        if cols==12: export_part(panel,'panel-240x240')
    for occ in d.rootComponent.occurrences:
        if occ.component!=panel:
            export_part(occ.component,'bridge-horizontal' if 'Bridge H' in occ.component.name else 'bridge-vertical')
    path=os.path.join(folder,'models','infinite-skadis-hd-v01.f3d')
    assert d.exportManager.execute(d.exportManager.createFusionArchiveExportOptions(path))
    d.userParameters.exportUserParameters([p for p in d.userParameters],os.path.join(folder,'fusion','parameters.csv'))
    with open(os.path.join(folder,'docs','cad-validation.json'),'w') as f: json.dump(report,f,indent=2)
    cam=app.activeViewport.camera
    cam.viewOrientation=adsk.core.ViewOrientations.TopViewOrientation
    cam.isFitView=True
    app.activeViewport.camera=cam
    app.activeViewport.refresh()
    assert app.activeViewport.saveAsImageFile(os.path.join(folder,'previews','master-top.png'),1600,1200)
    print(json.dumps(report))
    print('Exported F3D, STEP, STL, parameters and top view')

