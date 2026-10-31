"""Export unique native components plus occurrence transforms for animation.
The CAD design is not changed; instances retain their true assembly placements.
"""
import adsk.core,adsk.fusion,runpy,os,json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(ROOT,'animation','v07-assembly')
def run(_context):
    m=runpy.run_path(os.path.join(ROOT,'fusion','FrameSystemV05.py'));b=m['active']()
    os.makedirs(os.path.join(OUT,'meshes'),exist_ok=True)
    cache={};parts=[]
    for o in b.root.occurrences:
        c=o.component;token=c.entityToken
        if token not in cache:
            file='meshes/part-%03d.stl'%len(cache)
            opt=b.d.exportManager.createSTLExportOptions(c,os.path.join(OUT,file))
            opt.meshRefinement=adsk.fusion.MeshRefinementSettings.MeshRefinementMedium
            assert b.d.exportManager.execute(opt)
            cache[token]=file
        mat=[[o.transform2.getCell(i,j) for j in range(4)] for i in range(4)]
        for i in range(3):mat[i][3]*=10
        parts.append({'name':o.fullPathName,'component':c.name,'file':cache[token],'transform_mm':mat,'volume_mm3':c.bRepBodies.item(0).volume*1000})
    assert len(parts)==143
    with open(os.path.join(OUT,'manifest.json'),'w') as f:json.dump({'source':'models/v05/frame-assembly-v05.f3d','units':'mm','health':b.health(),'unique_meshes':len(cache),'parts':parts},f,indent=2)
    print('Exported',len(parts),'instances and',len(cache),'unique native meshes')
