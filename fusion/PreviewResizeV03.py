import adsk.core,adsk.fusion,os,runpy,json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P=adsk.core.Point3D.create

def run(_context: str):
    b=runpy.run_path(os.path.join(ROOT,'fusion','FrameSystemV03.py'))['active']();d=b.d;app=b.app
    reports=[]
    for cols,rows in [(4,4),(6,6)]:
        d.userParameters.itemByName('columns').expression=str(cols)
        d.userParameters.itemByName('rows').expression=str(rows)
        report=b.health();report.update({'columns':cols,'rows':rows})
        for o in b.root.occurrences:
            if o.component.name.startswith('Panel'):
                bb=o.component.bRepBodies.item(0).boundingBox
                bounds=[round((getattr(bb.maxPoint,k)-getattr(bb.minPoint,k))*10,4) for k in ('x','y','z')]
                assert bounds==[cols*20-.2,rows*20-.2,5],bounds
        reports.append(report)
    with open(os.path.join(ROOT,'docs','resize-validation-v03.json'),'w') as f:json.dump(reports,f,indent=2)
    palette={};b.root.isOriginFolderLightBulbOn=False
    for o in b.root.occurrences:
        c=o.component;body=c.bRepBodies.item(0);o.isLightBulbOn=True;body.isLightBulbOn=True;c.isOriginFolderLightBulbOn=False
        rgb=(225,222,211) if c.name.startswith('Panel') else ((52,58,64) if ('rail' in c.name or 'tie' in c.name) else ((193,135,63) if 'cap ' in c.name else (115,126,136)))
        if rgb not in palette:
            ap=d.appearances.addByCopy(body.appearance,'v03 '+str(rgb))
            colors=[p for p in ap.appearanceProperties if p.objectType==adsk.core.ColorProperty.classType()]
            if colors:colors[0].value=adsk.core.Color.create(*rgb,255)
            palette[rgb]=ap
        body.appearance=palette[rgb]
    for label,eye in [('front',(12,-15,-40)),('rear',(12,-15,45)),('side',(50,12,2)),('bare-frame',(12,-15,-40))]:
        if label=='bare-frame':
            for o in b.root.occurrences:
                o.isLightBulbOn=not o.component.name.startswith(('Panel','METAL cap','PRINT registration','METAL stepped','REFERENCE front'))
        cam=app.activeViewport.camera;cam.isPerspective=False;cam.eye=P(*eye);cam.target=P(12,12,1);cam.upVector=adsk.core.Vector3D.create(0,1,0);cam.isFitView=True
        app.activeViewport.camera=cam;app.activeViewport.refresh()
        assert app.activeViewport.saveAsImageFile(os.path.join(ROOT,'previews','v03-'+label+'.png'),1600,1200)
    for o in b.root.occurrences:o.isLightBulbOn=True
    cam=app.activeViewport.camera;cam.eye=P(12,-15,-40);cam.isFitView=True;app.activeViewport.camera=cam
    print(json.dumps(reports))
