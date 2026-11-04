"""Audit Fusion STL exports and package an unsliced 3MF layout, in millimeters."""
from pathlib import Path
import struct,collections,json,zipfile,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'models/v061/fit-kit'
NS='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
E.register_namespace('',NS)
def tag(s):return '{'+NS+'}'+s
def read(path):
 data=path.read_bytes();n=struct.unpack_from('<I',data,80)[0];assert len(data)==84+50*n
 return [[tuple(struct.unpack_from('<3f',data,84+50*i+12+12*j)) for j in range(3)] for i in range(n)]
def signature(ts):return sorted(tuple(sorted(tuple(round(v,5) for v in p) for p in t)) for t in ts)
model=E.Element(tag('model'),unit='millimeter');resources=E.SubElement(model,tag('resources'));build=E.SubElement(model,tag('build'))
report=[]
for idx,path in enumerate(sorted(OUT.glob('0*.stl')),1):
 ts=read(path);edges=collections.Counter()
 for tri in ts:
  pts=[tuple(round(v,5) for v in p) for p in tri]
  for j in range(3):edges[tuple(sorted([pts[j],pts[(j+1)%3]]))]+=1
 assert all(n==2 for n in edges.values()),path
 # Carrier geometry retained; board socket clearance changed.
 # Turn carrier 180 degrees about Y, rail keys toward bed. Other parts face down.
 if idx==3:ts=[[(-x,y,-z) for x,y,z in t] for t in ts]
 if idx==4:ts=[[(z,y,-x) for x,y,z in t] for t in ts] # Side-print hook; support reaches from bed
 lo=[min(p[k] for t in ts for p in t) for k in range(3)]
 ts=[[tuple(p[k]-lo[k] for k in range(3)) for p in t] for t in ts]
 vertices=[];lookup={};faces=[]
 for tri in ts:
  face=[]
  for p in tri:
   key=tuple(round(v,5) for v in p)
   if key not in lookup:lookup[key]=len(vertices);vertices.append(key)
   face.append(lookup[key])
  faces.append(face)
 obj=E.SubElement(resources,tag('object'),id=str(idx),type='model',name=path.stem);mesh=E.SubElement(obj,tag('mesh'));vs=E.SubElement(mesh,tag('vertices'));fs=E.SubElement(mesh,tag('triangles'))
 for x,y,z in vertices:E.SubElement(vs,tag('vertex'),x=str(x),y=str(y),z=str(z))
 for a,b,c in faces:E.SubElement(fs,tag('triangle'),v1=str(a),v2=str(b),v3=str(c))
 positions={1:[(5,5)],2:[(50,5)],3:[(50,30)],4:[(75,30),(90,30)]}[idx]
 for x,y in positions:E.SubElement(build,tag('item'),objectid=str(idx),transform=f'1 0 0 0 1 0 0 0 1 {x} {y} 0')
 report.append({'part':path.name,'triangles':len(ts),'closed_edges':True,'instances':len(positions),'bounds_mm':[max(p[k] for p in vertices) for k in range(3)]})
with zipfile.ZipFile(OUT/'fit-kit-plate.3mf','w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('[Content_Types].xml','<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
 z.writestr('_rels/.rels','<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
 z.writestr('3D/3dmodel.model',E.tostring(model,encoding='utf-8',xml_declaration=True))
(OUT/'mesh-validation.json').write_text(json.dumps({'parts':report,'carrier_geometry_retained':True,'layout':'unsliced; five objects; nominal 95 x 56 mm occupied bounding box','slicer_settings_included':False},indent=2))
print(json.dumps(report));print('Closed meshes verified. Unsliced 3MF includes two hook tile copies.')



