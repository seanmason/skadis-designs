import adsk.core,adsk.fusion,runpy,os,json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def check(columns,rows):
    b=runpy.run_path(os.path.join(ROOT,'fusion','FrameSystemV04.py'))['active']()
    b.d.userParameters.itemByName('columns').expression=str(columns)
    b.d.userParameters.itemByName('rows').expression=str(rows)
    assert b.d.computeAll()
    report={'columns':columns,'rows':rows,'health':b.health()}
    panel=next(o.component.bRepBodies.item(0) for o in b.root.occurrences if o.component.name=='Panel lower left')
    bb=panel.boundingBox
    actual=[(bb.maxPoint.x-bb.minPoint.x)*10,(bb.maxPoint.y-bb.minPoint.y)*10]
    expected=[columns*20-.2,rows*20-.2]
    assert all(abs(a-e)<.001 for a,e in zip(actual,expected)),(actual,expected)
    report['panel_bounds_mm']=actual
    path=os.path.join(ROOT,'docs','resize-validation-v04.json')
    results=json.load(open(path)) if os.path.exists(path) else []
    results.append(report)
    with open(path,'w') as f:json.dump(results,f,indent=2)
    print(report)
