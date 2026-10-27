"""Generate the six additional native 120 mm panel configurations.
The four corner variants already exist in the frame assembly.
Closes only documents this script creates, after successful F3D export.
"""
import adsk.core,adsk.fusion,os,runpy,json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(_context: str):
    m=runpy.run_path(os.path.join(ROOT,'fusion','FrameSystemV02.py'))
    records=[]
    assembly=adsk.core.Application.get().activeDocument
    for name,edges in [('interior',(0,0,0,0)),('left-edge',(1,0,0,0)),('right-edge',(0,1,0,0)),('bottom-edge',(0,0,1,0)),('top-edge',(0,0,0,1)),('standalone',(1,1,1,1))]:
        b=m['Builder']('SKADIS v0.2 - '+name,6,6)
        c=b.panel('Panel '+name,edges=edges)
        record={'configuration':name,'edges_LRBT':edges,'checks':[]}
        if name=='interior':
            for cols,rows in [(4,4),(8,12),(14,14),(6,6)]:
                b.d.userParameters.itemByName('columns').expression=str(cols)
                b.d.userParameters.itemByName('rows').expression=str(rows)
                check=b.health();bb=c.bRepBodies.item(0).boundingBox
                size=[round((getattr(bb.maxPoint,k)-getattr(bb.minPoint,k))*10,4) for k in ('x','y','z')]
                assert size==[cols*20-0.2,rows*20-0.2,5],size
                check.update({'columns':cols,'rows':rows,'bounds_mm':size});record['checks'].append(check)
        else:record['checks'].append(b.health())
        b.export('panel-'+name+'-v02',[(c,'panel-'+name+'-120')])
        records.append(record)
        with open(os.path.join(ROOT,'docs','panel-library-validation-v02.json'),'w') as f:json.dump(records,f,indent=2)
        b.doc.close(False)
    assembly.activate()
    print(json.dumps(records))
