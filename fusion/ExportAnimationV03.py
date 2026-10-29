"""Create a separate, larger native assembly and tessellate its actual parts."""
import adsk.core,adsk.fusion,os,json,runpy
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(ROOT,'animation','v03-reveal')

def run(_context: str):
    app=adsk.core.Application.get();im=app.importManager
    doc=im.importToNewDocument(im.createFusionArchiveImportOptions(os.path.join(ROOT,'models','v03','frame-assembly-v03.f3d')))
    doc.name='Infinite SKADIS HD - 480 mm animation source'
    d=adsk.fusion.Design.cast(app.activeProduct)
    d.userParameters.itemByName('columns').expression='12'
    d.userParameters.itemByName('rows').expression='12'
    m=runpy.run_path(os.path.join(ROOT,'fusion','FrameSystemV03.py'))
    b=m['Builder'].__new__(m['Builder']);b.app=app;b.doc=doc;b.d=d;b.root=d.rootComponent
    health=b.health();ex=d.exportManager
    assert health['components']==120
    assert ex.execute(ex.createFusionArchiveExportOptions(os.path.join(OUT,'assembly-480.f3d')))
    records=[]
    for i,o in enumerate(d.rootComponent.occurrences):
        c=o.component;body=c.bRepBodies.item(0);bb=body.boundingBox
        filename=f'{i:03d}.stl'
        opt=ex.createSTLExportOptions(c,os.path.join(OUT,'meshes',filename))
        opt.meshRefinement=adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
        assert ex.execute(opt)
        records.append({'name':c.name,'file':'meshes/'+filename,'bounds_mm':[[getattr(p,k)*10 for k in ('x','y','z')] for p in (bb.minPoint,bb.maxPoint)],'volume_mm3':body.volume*1000})
    with open(os.path.join(OUT,'manifest.json'),'w') as f:json.dump({'source':'Fusion v0.3 native assembly','module_mm':240,'assembly_nominal_mm':[480,480,35],'health':health,'parts':records},f,indent=2)
    print('Exported 120 native part meshes and separate 480 mm parametric assembly')
