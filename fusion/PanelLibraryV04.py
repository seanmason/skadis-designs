"""Create separate native panel variants; export before closing only these new documents."""
import adsk.core,adsk.fusion,runpy,os,json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VARIANTS=[('interior',(0,0,0,0)),('left-edge',(1,0,0,0)),('right-edge',(0,1,0,0)),('bottom-edge',(0,0,1,0)),('top-edge',(0,0,0,1)),('standalone',(1,1,1,1))]
def build(index):
    m=runpy.run_path(os.path.join(ROOT,'fusion','FrameSystemV04.py'))
    previous=adsk.core.Application.get().activeDocument
    label,edges=VARIANTS[index];b=m['Builder']();b.doc.name='SKADIS v0.4 panel - '+label
    c=b.clean_panel(label,'0 mm','0 mm',edges,'variant');health=b.health()
    folder=os.path.join(ROOT,'models','v04','panels');os.makedirs(folder,exist_ok=True)
    path=os.path.join(folder,'panel-'+label+'-120');ex=b.d.exportManager
    cam=b.app.activeViewport.camera;cam.isPerspective=False;cam.isSmoothTransition=False
    cam.eye=adsk.core.Point3D.create(6,6,-40);cam.target=adsk.core.Point3D.create(6,6,0);cam.upVector=adsk.core.Vector3D.create(0,1,0)
    b.app.activeViewport.camera=cam;b.app.activeViewport.fit()
    assert ex.execute(ex.createFusionArchiveExportOptions(path+'.f3d'))
    assert ex.execute(ex.createSTEPExportOptions(path+'.step',c))
    stl=ex.createSTLExportOptions(c,path+'.stl');stl.meshRefinement=adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
    assert ex.execute(stl)
    report=os.path.join(ROOT,'docs','panel-library-validation-v04.json')
    results=json.load(open(report)) if os.path.exists(report) else {}
    results[label]={'finished_edges_LRBT':edges,'health':health}
    with open(report,'w') as f:json.dump(results,f,indent=2)
    # This document was created here and its complete state was exported above.
    b.doc.close(False);previous.activate();print(label,health)
