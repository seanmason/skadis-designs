"""Check imported mesh scale/volume against Fusion's analytic body manifest."""
import bpy,bmesh,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'manifest.json').read_text())
records=[]
for part in manifest['parts']:
    obj=next(o for o in bpy.context.scene.objects if o.get('CAD source')==part['file'])
    bm=bmesh.new();bm.from_mesh(obj.data);volume=abs(bm.calc_volume())*1e9;bm.free()
    error=abs(volume-part['volume_mm3'])/part['volume_mm3']
    # Small round fasteners lose a little analytic volume to STL chord facets.
    assert error<.005,(part['name'],error)
    for frame in [72,504,600]:
        bpy.context.scene.frame_set(frame)
        if frame==72:assembled=obj.location.copy()
        else:assert (obj.location-assembled).length<1e-8,obj.name
    records.append({'part':part['name'],'CAD_volume_mm3':part['volume_mm3'],'mesh_volume_mm3':volume,'relative_error':error})
report={'parts':len(records),'maximum_relative_volume_error':max(r['relative_error'] for r in records),'threshold':.005,'editorial_start_and_end_positions_match':True,'checks':records}
(ROOT/'geometry-validation.json').write_text(json.dumps(report,indent=2))
print({k:v for k,v in report.items() if k!='checks'})
