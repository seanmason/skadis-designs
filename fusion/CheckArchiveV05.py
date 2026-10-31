"""Reopen the delivered native archive and verify its editable state."""
import adsk.core,adsk.fusion,runpy,os,json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(_context):
    m=runpy.run_path(os.path.join(ROOT,'fusion','FrameSystemV05.py'))
    app=adsk.core.Application.get();previous=app.activeDocument
    doc=app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(os.path.join(ROOT,'models','v05','frame-assembly-v05.f3d')))
    b=m['Builder'].__new__(m['Builder']);b.app=app;b.doc=doc
    b.d=adsk.fusion.Design.cast(app.activeProduct);b.root=b.d.rootComponent
    assert b.d.computeAll()
    health=b.health();expected=json.load(open(os.path.join(ROOT,'docs','health-v05.json')))
    assert health==expected,(health,expected)
    assert b.d.userParameters.itemByName('columns').value==12
    assert b.d.userParameters.itemByName('rows').value==12
    assert abs(b.value('seamGap')-.035)<1e-8
    assert all(o.isLightBulbOn for o in b.root.occurrences)
    result={'reopened_native_archive':True,'health':health,'panel_pitch_mm':240,'seam_gap_mm':.35}
    with open(os.path.join(ROOT,'docs','archive-validation-v05.json'),'w') as f:json.dump(result,f,indent=2)
    doc.close(False);previous.activate();print(result)
