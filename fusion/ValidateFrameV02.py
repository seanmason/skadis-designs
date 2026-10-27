"""Run against the v0.2 assembly after FrameSystemV02.py."""
import adsk.core, adsk.fusion, os, json, runpy
P=adsk.core.Point3D.create
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(_context: str):
    app=adsk.core.Application.get();d=adsk.fusion.Design.cast(app.activeProduct)
    assert 'v0.2' in app.activeDocument.name
    walk=runpy.run_path(os.path.join(ROOT,'fusion','FrameSystemV02.py'))['timeline_items']
    reports=[]
    for cols,rows in [(4,4),(6,6)]:
        d.userParameters.itemByName('columns').expression=str(cols)
        d.userParameters.itemByName('rows').expression=str(rows)
        errors=[(t.name,t.errorOrWarningMessage) for t in walk(d.timeline) if t.healthState!=adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState]
        assert not errors,str(errors)
        panels=[]
        for occ in d.rootComponent.occurrences:
            c=occ.component
            assert c.bRepBodies.count==1 and c.bRepBodies.item(0).isSolid,c.name
            if c.name.startswith('Panel'):
                bb=c.bRepBodies.item(0).boundingBox
                dims=[round((getattr(bb.maxPoint,k)-getattr(bb.minPoint,k))*10,4) for k in ('x','y','z')]
                assert dims==[cols*20-0.2,rows*20-0.2,5],(c.name,dims)
                panels.append({'name':c.name,'bounds_mm':dims,'volume_cm3':c.bRepBodies.item(0).volume})
        reports.append({'columns':cols,'rows':rows,'healthy':True,'panels':panels})
    with open(os.path.join(ROOT,'docs','cad-validation-v02.json'),'w') as f:json.dump(reports,f,indent=2)
    ex=d.exportManager
    assert ex.execute(ex.createFusionArchiveExportOptions(os.path.join(ROOT,'models','v02','frame-assembly-v02.f3d')))
    # Apply color by function to make the assembly review legible.
    palette={}
    d.rootComponent.isOriginFolderLightBulbOn=False
    for occ in d.rootComponent.occurrences:
        c=occ.component;body=c.bRepBodies.item(0)
        occ.isLightBulbOn=True
        body.isLightBulbOn=True
        c.isOriginFolderLightBulbOn=False
        rgb=(225,222,211) if c.name.startswith('Panel') else ((52,58,64) if ('rail' in c.name or 'tie' in c.name) else ((193,135,63) if 'cap ' in c.name else (115,126,136)))
        if rgb not in palette:
            ap=d.appearances.addByCopy(body.appearance,'v02 '+str(rgb))
            colors=[p for p in ap.appearanceProperties if p.objectType==adsk.core.ColorProperty.classType()]
            if colors:colors[0].value=adsk.core.Color.create(*rgb,255)
            palette[rgb]=ap
        body.appearance=palette[rgb]
    for label,eye in [('front',(12,-15,-40)),('rear',(12,-15,45)),('face',(12,12,-45)),('side',(50,12,2))]:
        cam=app.activeViewport.camera;cam.isPerspective=False;cam.eye=P(*eye);cam.target=P(12,12,1);cam.upVector=adsk.core.Vector3D.create(0,1,0);cam.isFitView=True
        app.activeViewport.camera=cam;app.activeViewport.refresh()
        assert app.activeViewport.saveAsImageFile(os.path.join(ROOT,'previews','v02-'+label+'.png'),1600,1200)
    cam=app.activeViewport.camera;cam.eye=P(12,-15,-40);cam.target=P(12,12,1);cam.isFitView=True;app.activeViewport.camera=cam
    assert ex.execute(ex.createFusionArchiveExportOptions(os.path.join(ROOT,'models','v02','frame-assembly-v02.f3d')))
    print(json.dumps(reports))
