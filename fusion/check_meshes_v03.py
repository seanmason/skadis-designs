"""Standalone binary STL topology/scale checks; no third-party packages needed."""
import struct, collections, json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
report=[]
paths=sorted((root/'models'/'v03').glob('*.stl'))
assert len(paths)==11,len(paths)
for path in paths:
    data=path.read_bytes();count=struct.unpack_from('<I',data,80)[0]
    assert len(data)==84+50*count,path
    edges=collections.Counter();points=[]
    volume=0
    for i in range(count):
        values=struct.unpack_from('<12fH',data,84+50*i)
        tri=[tuple(round(x,5) for x in values[k:k+3]) for k in (3,6,9)]
        points.extend(tri)
        for j in range(3):edges[tuple(sorted((tri[j],tri[(j+1)%3])))]+=1
        a,b,c=tri
        volume+=(a[0]*(b[1]*c[2]-b[2]*c[1])+a[1]*(b[2]*c[0]-b[0]*c[2])+a[2]*(b[0]*c[1]-b[1]*c[0]))/6
    bad=sum(n!=2 for n in edges.values())
    assert bad==0,(path,bad)
    bounds=[round(max(p[k] for p in points)-min(p[k] for p in points),4) for k in range(3)]
    expected=[18,18,2.8] if path.stem=='registration-seat' else [119.8,119.8,5]
    # Circular STL bounds can undershoot the analytic diameter by chord error.
    assert all(abs(a-b)<.01 for a,b in zip(bounds,expected)),(path,bounds)
    assert abs(volume)>0,path
    report.append({'file':path.name,'triangles':count,'closed_edge_incidence':True,'bounds_mm':bounds,'volume_mm3':round(abs(volume),3)})
(root/'docs'/'mesh-validation-v03.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))

