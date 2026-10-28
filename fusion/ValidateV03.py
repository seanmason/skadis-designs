import adsk.core,adsk.fusion,os,runpy,json,itertools
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P=adsk.core.Point3D.create

def run(_context: str):
    m=runpy.run_path(os.path.join(ROOT,'fusion','FrameSystemV03.py'));b=m['active']();d=b.d
    health=b.health()
    assert health['components']==120,health
    items=[(o.component.name,o.component.bRepBodies.item(0)) for o in b.root.occurrences]
    tm=adsk.fusion.TemporaryBRepManager.get();op=adsk.fusion.BooleanTypes.DifferenceBooleanType
    def overlap(a,c):
        aa=a.boundingBox;bb=c.boundingBox
        return all(min(getattr(aa.maxPoint,k),getattr(bb.maxPoint,k))-max(getattr(aa.minPoint,k),getattr(bb.minPoint,k))>1e-6 for k in ('x','y','z'))
    def loss(a,c):
        t=tm.copy(a);before=t.volume
        assert tm.booleanOperation(t,c,op),'Unresolved Boolean operation'
        return (before-(t.volume if t.isValid else 0))*1000
    box=tm.createBox(adsk.core.OrientedBoundingBox3D.create(P(0,0,0),adsk.core.Vector3D.create(1,0,0),adsk.core.Vector3D.create(0,1,0),1,1,1))
    shifted=tm.copy(box);tr=adsk.core.Matrix3D.create();tr.translation=adsk.core.Vector3D.create(.5,0,0);tm.transform(shifted,tr)
    assert loss(box,shifted)>100
    tr.translation=adsk.core.Vector3D.create(10,0,0);tm.transform(shifted,tr);assert abs(loss(box,shifted))<.01
    collisions=[];pairs=0
    for (na,a),(nc,c) in itertools.combinations(items,2):
        if not overlap(a,c):continue
        pairs+=1;v=loss(a,c)
        if v>.01:collisions.append({'a':na,'b':nc,'overlap_mm3':v})
    wall=b.value('frameZ+20 mm')
    behind=[n for n,a in items if a.boundingBox.maxPoint.z>wall+1e-6]
    in_cavity=[n for n,a in items if (n.startswith('METAL in-bay') or n.startswith('METAL flush wall') or n.startswith('REFERENCE side') or n.startswith('REFERENCE wall anchor') or 'channel nut side' in n) and a.boundingBox.minPoint.z<b.value('frameZ')-1e-6]
    # Tools operate with panels/front mounting stacks absent, nuts already loaded.
    fixed=[(n,a) for n,a in items if n.startswith(('Vertical rail','Horizontal tie','METAL in-bay','METAL flush wall','REFERENCE side','REFERENCE thin METAL channel nut','REFERENCE wall anchor'))]
    tool_hits=[];tool_count=0
    def toolcheck(label,body,exclude):
        nonlocal tool_count
        tool_count+=1
        for n,a in fixed:
            if n in exclude or not overlap(body,a):continue
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
    withdrawals=[]
    mapping={'Panel lower left':['00','01','10','11'],'Panel lower right':['10','11','20','21'],'Panel upper left':['01','02','11','12'],'Panel upper right':['11','12','21','22']}
    for name,nodes in mapping.items():
        body=next(a for n,a in items if n==name);hits=[]
        excluded={name}|{'METAL cap '+n for n in nodes}|{'REFERENCE front M5x25 '+n for n in nodes}
        for distance in [.2,.5,1,2,5,10]:
            moved=tm.copy(body);tr=adsk.core.Matrix3D.create();tr.translation=adsk.core.Vector3D.create(0,0,-distance/10);tm.transform(moved,tr)
            for n,a in items:
                if n in excluded or not overlap(moved,a):continue
                v=loss(moved,a)
                if v>.01:hits.append({'distance_mm':distance,'part':n,'overlap_mm3':v})
        withdrawals.append({'panel':name,'sampled_forward_travel_mm':[.2,.5,1,2,5,10],'hits':hits})
    report={'health':health,'profile_measurements_mm':{'mouth':6.28,'cavity':11,'depth':6.2,'floor_estimate':5.7},'static_candidates':pairs,'static_collisions':collisions,'parts_behind_wall_datum':behind,'frame_hardware_in_hook_cavity':in_cavity,'tool_envelopes':tool_count,'tool_collisions':tool_hits,'panel_withdrawal':withdrawals,'nominal_face_to_wall_mm':wall*10,'physical_fit_verified':False}
    with open(os.path.join(ROOT,'docs','validation-v03.json'),'w') as f:json.dump(report,f,indent=2)
    print(json.dumps(report))
    assert not collisions and not behind and not in_cavity and not tool_hits and all(not x['hits'] for x in withdrawals)
