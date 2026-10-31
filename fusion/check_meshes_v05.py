"""Binary STL closed-edge and scale audit; run with any CPython 3 interpreter."""
import struct,collections,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
report=[]
paths=sorted((root/'models'/'v05').rglob('*.stl'))
assert paths,'No exports found'
for path in paths:
    data=path.read_bytes();count=struct.unpack_from('<I',data,80)[0]
    assert len(data)==84+50*count,path
    edges=collections.Counter();points=[];volume=0
    for i in range(count):
        values=struct.unpack_from('<12fH',data,84+50*i)
        tri=[tuple(round(x,5) for x in values[k:k+3]) for k in (3,6,9)]
        points.extend(tri)
        for j in range(3):edges[tuple(sorted((tri[j],tri[(j+1)%3])))]+=1
        a,b,c=tri
        volume+=(a[0]*(b[1]*c[2]-b[2]*c[1])+a[1]*(b[2]*c[0]-b[0]*c[2])+a[2]*(b[0]*c[1]-b[1]*c[0]))/6
    bad=sum(n!=2 for n in edges.values());assert bad==0,(path,bad)
    bounds=[round(max(p[k] for p in points)-min(p[k] for p in points),4) for k in range(3)]
    assert abs(volume)>0,path
    if path.parent.name=='v05' and path.stem.startswith('panel-'):
        expected=[239.65,249.65 if 'lower' in path.stem else 239.65,5]
        assert all(abs(a-b)<.02 for a,b in zip(bounds,expected)),(path,bounds,expected)
    report.append({'file':str(path.relative_to(root)),'triangles':count,'closed_edge_incidence':True,'bounds_mm':bounds,'volume_mm3':round(abs(volume),3)})
(root/'docs'/'mesh-validation-v05.json').write_text(json.dumps(report,indent=2))
print('Passed',len(report),'closed STL exports')
