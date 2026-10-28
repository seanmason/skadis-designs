"""Native panel variants using v0.3 node registration pockets."""
import adsk.core,adsk.fusion,os,runpy,json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def export_variant(name,edges):
    m=runpy.run_path(os.path.join(ROOT,'fusion','FrameSystemV03.py'));records=[]
    assembly=adsk.core.Application.get().activeDocument
    folder=os.path.join(ROOT,'models','v03');os.makedirs(folder,exist_ok=True)
    for name,edges in [(name,edges)]:
        b=m['Builder']('SKADIS v0.3 - '+name,6,6);c=b.panel('Panel '+name,edges=edges)
        checks=[]
        for cols,rows in ([(4,4),(8,12),(14,14),(6,6)] if name=='interior' else [(6,6)]):
            b.d.userParameters.itemByName('columns').expression=str(cols)
            b.d.userParameters.itemByName('rows').expression=str(rows)
            check=b.health();bb=c.bRepBodies.item(0).boundingBox
            size=[round((getattr(bb.maxPoint,k)-getattr(bb.minPoint,k))*10,4) for k in ('x','y','z')]
            assert size==[cols*20-.2,rows*20-.2,5],size
            check.update({'columns':cols,'rows':rows,'bounds_mm':size});checks.append(check)
        records.append({'configuration':name,'edges_LRBT':edges,'checks':checks})
        ex=b.d.exportManager
        assert ex.execute(ex.createFusionArchiveExportOptions(os.path.join(folder,'panel-'+name+'-v03.f3d')))
        assert ex.execute(ex.createSTEPExportOptions(os.path.join(folder,'panel-'+name+'-120.step'),c))
        stl=ex.createSTLExportOptions(c,os.path.join(folder,'panel-'+name+'-120.stl'));stl.meshRefinement=adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
        assert ex.execute(stl)
        report_path=os.path.join(ROOT,'docs','panel-library-validation-v03.json')
        previous=json.load(open(report_path)) if os.path.exists(report_path) else []
        records=[r for r in previous if r['configuration']!=name]+records
        with open(report_path,'w') as f:json.dump(records,f,indent=2)
        b.doc.close(False)
    assembly.activate();print(json.dumps(records))

def run(_context: str):
    for name,edges in [('interior',(0,0,0,0)),('left-edge',(1,0,0,0)),('right-edge',(0,1,0,0)),('bottom-edge',(0,0,1,0)),('top-edge',(0,0,0,1)),('standalone',(1,1,1,1))]:export_variant(name,edges)
