"""Migrate the delivered v0.5 archive to centered M2 stations, preserving history.
Support pads stay on their original axes; the bore opens the left side of the
compression blade. This is a prototype, not a load-rated or hook-certified part.
"""
import adsk.core, adsk.fusion, os, runpy, json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME='Infinite SKADIS HD v0.6 - centered M2 prototype'
M=runpy.run_path(os.path.join(ROOT,'fusion','FrameSystemV05.py'))

def start(_context):
 a=adsk.core.Application.get()
 doc=a.importManager.importToNewDocument(a.importManager.createFusionArchiveImportOptions(os.path.join(ROOT,'models','v05','frame-assembly-v05.f3d')))
 doc.name=NAME
 print('Imported historical archive; run revise, checks, export and jig in bounded calls')

def active():
 a=adsk.core.Application.get();doc=[d for d in a.documents if d.name==NAME][-1];doc.activate()
 b=M['Builder'].__new__(M['Builder']);b.app=a;b.doc=doc;b.d=adsk.fusion.Design.cast(a.activeProduct);b.root=b.d.rootComponent
 return b

def revise(_context):
 b=active();d=b.d
 assert not d.userParameters.itemByName('webCenterOffset'),'Already migrated'
 d.userParameters.add('webCenterOffset',M['V']('(slotHeight-slotWidth)^2/(4*pitch)'),'mm','Equal-distance M2 station for standard staggered lattice; preserve support axis')
 edits={}
 def shift(p):
  if p.name not in edits:edits[p.name]=p.expression
  p.expression='('+edits[p.name]+')-webCenterOffset'
 for c in d.allComponents:
  for s in c.sketches:
   dims=list(s.sketchDimensions)
   if not dims:continue
   if c.name.startswith('Panel ') and s.name.startswith(('11 M2 through bore','12 Flush countersink')):shift(dims[0].parameter)
   if c.name.startswith('PRINT carrier') and s.name.startswith(('M2 through passage','Top-loaded captive','Release free end','Nut spring deflection','Nut spring side relief')):shift(dims[0].parameter)
   if c.name.startswith('REFERENCE panel M2'):shift(dims[0].parameter)
   if c.name.startswith('METAL M2 nut'):
    for idx in ([0,2,4,6] if s.name.startswith('M2 hex nut') else [0]):shift(dims[idx].parameter)
  if c.name.startswith('PRINT carrier'):
   for p in c.modelParameters:
    if p.role=='AlongDistance' and p.createdBy.name.startswith('Integral nut retaining ramp'):shift(p)
 assert d.computeAll()
 h=b.health();assert h['healthy'],h
 out=os.path.join(ROOT,'models','v06');os.makedirs(out,exist_ok=True)
 with open(os.path.join(out,'migration.json'),'w') as f:json.dump({'source':'models/v05/frame-assembly-v05.f3d','original_expressions':edits,'health':h},f,indent=2)
 print(h,len(edits),'parameters revised')

def export(_context):
 b=active();out=os.path.join(ROOT,'models','v06');os.makedirs(out,exist_ok=True);ex=b.d.exportManager
 for c in b.d.allComponents:
  if not c.name.startswith(('Panel ','PRINT carrier')):continue
  stem=os.path.join(out,c.name.replace(' ','-'))
  assert ex.execute(ex.createSTEPExportOptions(stem+'.step',c))
  st=ex.createSTLExportOptions(c,stem+'.stl');st.meshRefinement=adsk.fusion.MeshRefinementSettings.MeshRefinementHigh;assert ex.execute(st)
 assert ex.execute(ex.createFusionArchiveExportOptions(os.path.join(out,'frame-assembly-v06.f3d')))
 assert ex.execute(ex.createSTEPExportOptions(os.path.join(out,'frame-assembly-v06.step')))
 b.d.userParameters.exportUserParameters(list(b.d.userParameters),os.path.join(out,'parameters.csv'))
 cam=b.app.activeViewport.camera;cam.isPerspective=False;cam.isSmoothTransition=False;cam.eye=M['P'](24,24,-90);cam.target=M['P'](24,24,0);cam.upVector=adsk.core.Vector3D.create(0,1,0);b.app.activeViewport.camera=cam;b.app.activeViewport.fit();b.app.activeViewport.refresh()
 b.app.activeViewport.saveAsImageFile(os.path.join(out,'front.png'),1500,1500)
 print(b.health())

def jig(_context):
 a=adsk.core.Application.get();path=os.path.join(ROOT,'models','v05','prototypes','carrier-jig-240.f3d')
 doc=a.importManager.importToNewDocument(a.importManager.createFusionArchiveImportOptions(path));doc.name='SKADIS v0.6 centered M2 positioning jig'
 d=adsk.fusion.Design.cast(a.activeProduct);d.userParameters.add('webCenterOffset',M['V']('(slotHeight-slotWidth)^2/(4*pitch)'),'mm','Match v0.6 screw axis; locating pads stay at original axis')
 for c in d.allComponents:
  for s in c.sketches:
   if s.name.startswith(('Temporary M2 locating','Flush temporary screw seat')):
    p=s.sketchDimensions.item(0).parameter;p.expression='('+p.expression+')-webCenterOffset'
 assert d.computeAll();out=os.path.join(ROOT,'models','v06','carrier-jig-240');ex=d.exportManager
 assert ex.execute(ex.createFusionArchiveExportOptions(out+'.f3d'))
 st=ex.createSTLExportOptions(d.rootComponent,out+'.stl');st.meshRefinement=adsk.fusion.MeshRefinementSettings.MeshRefinementHigh;assert ex.execute(st)
 active();print('Updated jig screw locations; unchanged pad sockets and M5 access')
