"""Bounded solid interference test using temporary BRep differences.
Includes positive and negative controls; never modifies design geometry.
Tangential/coincident contacts are excluded by positive-overlap AABB filter.
"""
import adsk.core,adsk.fusion,os,json,itertools
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(_context: str):
    d=adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    tm=adsk.fusion.TemporaryBRepManager.get();op=adsk.fusion.BooleanTypes.DifferenceBooleanType
    bodies=[(o.component.name,o.component.bRepBodies.item(0)) for o in d.rootComponent.occurrences]
    seed=next(b for n,b in bodies if n=='PRINT horizontal alignment key L')
    a=tm.copy(seed);t=tm.copy(seed);mat=adsk.core.Matrix3D.create();mat.translation=adsk.core.Vector3D.create(0.1,0,0);tm.transform(t,mat)
    before=a.volume;assert tm.booleanOperation(a,t,op)
    assert before-a.volume>0.001,'Positive collision control did not detect overlap'
    a=tm.copy(seed);mat.translation=adsk.core.Vector3D.create(100,0,0);tm.transform(t,mat)
    before=a.volume;assert tm.booleanOperation(a,t,op)
    assert abs(before-a.volume)<1e-7,'Negative collision control changed the body'
    collisions=[];unknown=[];candidates=0
    for (na,ba),(nb,bb) in itertools.combinations(bodies,2):
        aa=ba.boundingBox;ab=bb.boundingBox
        if not all(min(getattr(aa.maxPoint,k),getattr(ab.maxPoint,k))-max(getattr(aa.minPoint,k),getattr(ab.minPoint,k))>1e-6 for k in ('x','y','z')):continue
        candidates+=1;a=tm.copy(ba);before=a.volume
        if not tm.booleanOperation(a,bb,op):unknown.append([na,nb]);continue
        after=a.volume if a.isValid else 0
        loss=(before-after)*1000
        if loss>0.01:collisions.append({'a':na,'b':nb,'overlap_mm3':loss})
    report={'method':'Temporary solid difference with positive and negative controls','components':len(bodies),'aabb_candidates':candidates,'collision_tolerance_mm3':0.01,'collisions':collisions,'unresolved_operations':unknown}
    with open(os.path.join(ROOT,'docs','interference-v02.json'),'w') as f:json.dump(report,f,indent=2)
    print(json.dumps(report))
    assert not collisions and not unknown,'Review interference report before export'
