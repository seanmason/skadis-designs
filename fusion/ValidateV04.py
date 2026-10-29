"""Geometric prototype checks. No physical strength or real-hook certification implied."""
import adsk.core,adsk.fusion,runpy,os,json,itertools
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P=adsk.core.Point3D.create
def run(_context):
    b=runpy.run_path(os.path.join(ROOT,'fusion','FrameSystemV04.py'))['active']()
    tm=adsk.fusion.TemporaryBRepManager.get();op=adsk.fusion.BooleanTypes.DifferenceBooleanType
    items=[]
    for o in b.root.occurrences:
        body=tm.copy(o.component.bRepBodies.item(0));assert tm.transform(body,o.transform2)
        items.append((o.fullPathName,body))
    def near(a,c):
        aa=a.boundingBox;bb=c.boundingBox
        return all(min(getattr(aa.maxPoint,k),getattr(bb.maxPoint,k))-max(getattr(aa.minPoint,k),getattr(bb.minPoint,k))>1e-6 for k in ('x','y','z'))
    def loss(a,c):
        t=tm.copy(a);before=t.volume
        assert tm.booleanOperation(t,c,op)
        return (before-(t.volume if t.isValid else 0))*1000
    def box(x,y,z,w,h,d):
        return tm.createBox(adsk.core.OrientedBoundingBox3D.create(P(x+w/2,y+h/2,z+d/2),adsk.core.Vector3D.create(1,0,0),adsk.core.Vector3D.create(0,1,0),w,h,d))
    assert loss(box(0,0,0,1,1,1),box(.5,0,0,1,1,1))>100
    assert abs(loss(box(0,0,0,1,1,1),box(2,0,0,1,1,1)))<.01
    collisions=[]
    for (na,a),(nc,c) in itertools.combinations(items,2):
        if near(a,c):
            v=loss(a,c)
            if v>.01:collisions.append([na,nc,round(v,5)])
    hooks=[]
    for i in range(int(b.d.userParameters.itemByName('columns').value)*4):
        center=b.value('pitch/4')+i*b.value('pitch/2');w=b.value('hookEnvelopeWidth')
        corridor=box(center-w/2,0,b.value('boardThickness'),w,b.value('2*panelHeight'),b.value('hookClearance'))
        for n,a in items:
            if near(corridor,a):
                v=loss(corridor,a)
                if v>.01:hooks.append([i,n,round(v,5)])
    moves=[]
    for name,body in items:
        if not name.startswith(('Panel ','REFERENCE panel M2','REFERENCE carrier M5')):continue
        excluded={name}
        if name.startswith('Panel '):
            bb=body.boundingBox
            for n,a in items:
                if n.startswith('REFERENCE panel M2'):
                    q=a.boundingBox
                    if bb.minPoint.x<q.minPoint.x<bb.maxPoint.x and bb.minPoint.y<q.minPoint.y<bb.maxPoint.y:excluded.add(n)
        # Carrier fixing assembly occurs before any panels or their small screws are fitted.
        if name.startswith('REFERENCE carrier M5'):
            excluded|={n for n,a in items if n.startswith(('Panel ','REFERENCE panel M2'))}
        for distance in [.2,.6,1,3,8,15,25]:
            moved=tm.copy(body);tr=adsk.core.Matrix3D.create();tr.translation=adsk.core.Vector3D.create(0,0,-distance/10);tm.transform(moved,tr)
            for n,a in items:
                if n in excluded or not near(moved,a):continue
                v=loss(moved,a)
                if v>.01:moves.append([name,distance,n,round(v,5)])
    # Frame tools operate with carriers installed, panels and their M2 screws absent.
    fixed=[(n,a) for n,a in items if not n.startswith(('Panel ','REFERENCE panel M2'))]
    tool_hits=[];tool_count=0
    def toolcheck(label,body,exclude):
        nonlocal tool_count
        tool_count+=1
        for n,a in fixed:
            if n in exclude or not near(body,a):continue
            v=loss(body,a)
            if v>.01:tool_hits.append({'tool':label,'part':n,'overlap_mm3':v})
    for n,a in items:
        if not n.startswith('REFERENCE side M5x8'):continue
        # Head cylinder is the largest-radius cylindrical face; axis is taken from it.
        cylinders=[adsk.core.Cylinder.cast(f.geometry) for f in a.faces if f.geometry.objectType==adsk.core.Cylinder.classType()]
        cyl=max(cylinders,key=lambda c:c.radius);axis=cyl.axis
        idx=max(range(3),key=lambda i:abs([axis.x,axis.y,axis.z][i]))
        bb=a.boundingBox;mid=[(getattr(bb.minPoint,k)+getattr(bb.maxPoint,k))/2 for k in ('x','y','z')]
        # Head lies at the end with the wider bounding footprint. Compare head-axis
        # origin with the body midpoint to identify its outward direction.
        org=cyl.origin;normal=1 if [org.x,org.y,org.z][idx]>mid[idx] else -1
        tip=mid[:];tip[idx]=getattr(bb.maxPoint,('x','y','z')[idx]) if normal>0 else getattr(bb.minPoint,('x','y','z')[idx])
        bend=tip[:];bend[idx]+=normal*b.value('keyDriverReach')
        rad=b.value('keyDriverDiameter')/2
        toolcheck(n+' working leg',tm.createCylinderOrCone(P(*tip),rad,P(*bend),rad),{n})
        front=bend[:];front[2]=-1
        toolcheck(n+' return leg',tm.createCylinderOrCone(P(*bend),rad,P(*front),rad),{n})
    for n,a in items:
        if not n.startswith('REFERENCE wall anchor HEAD ONLY'):continue
        bb=a.boundingBox;x=(bb.minPoint.x+bb.maxPoint.x)/2;y=(bb.minPoint.y+bb.maxPoint.y)/2
        rad=b.value('wallDriverDiameter')/2
        toolcheck(n+' driver',tm.createCylinderOrCone(P(x,y,-1),rad,P(x,y,b.value('frameZ+20 mm-jointThickness')),rad),{n})
    front=[n for n,a in items if a.boundingBox.minPoint.z < -1e-6]
    behind=[n for n,a in items if a.boundingBox.maxPoint.z > b.value('frameZ+20 mm')+1e-6]
    outside=[]
    for n,a in items:
        bb=a.boundingBox
        if bb.minPoint.x < -1e-6 or bb.minPoint.y < -1e-6 or bb.maxPoint.x>b.value('2*panelWidth')+1e-6 or bb.maxPoint.y>b.value('2*panelHeight')+1e-6:outside.append(n)
    actual=set()
    for n,a in items:
        if n.startswith('REFERENCE panel M2'):
            bb=a.boundingBox;actual.add((round((bb.minPoint.x+bb.maxPoint.x)*5,4),round((bb.minPoint.y+bb.maxPoint.y)*5,4)))
    expected={(round(b.value(x)*10,4),round(b.value(y)*10,4)) for x in ['pitch/2','panelWidth-pitch/2','panelWidth+pitch/2','2*panelWidth-pitch/2'] for y in ['pitch','panelHeight-pitch','panelHeight+pitch','2*panelHeight-pitch']}
    assert actual==expected,(actual,expected)
    report={'health':b.health(),'static_collisions':collisions,'hook_corridor_collisions':hooks,'sampled_panel_and_screw_motion_collisions':moves,'frame_tool_collisions':tool_hits,'frame_tool_envelopes':tool_count,'front_protrusions':front,'behind_wall':behind,'face_to_wall_mm':b.value('frameZ+20 mm')*10,'hook_cavity_mm':b.value('hookClearance')*10,'blade_lateral_clearance_mm':b.value('(pitch/2-hookEnvelopeWidth-supportWidth)/2')*10,'physical_fit_verified':False,'limitations':['Continuous 6 mm wide hook columns are provisional, not measured hook meshes','Motion checked at seven axial offsets, not a continuous kinematic simulation','Metal hardware envelopes omit threads and manufacturer tolerances','No structural rating or large-wall engineering analysis']}
    report['parts_outside_module_array']=outside
    report['panel_screw_station_count']=len(actual)
    with open(os.path.join(ROOT,'docs','validation-v04.json'),'w') as f:json.dump(report,f,indent=2)
    print(json.dumps(report))
    assert not collisions and not hooks and not moves and not tool_hits and not front and not behind and not outside
