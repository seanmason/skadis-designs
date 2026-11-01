"""Native mounting-detail comparison; not a load qualification or released panel."""
import os,runpy,json,adsk.core,adsk.fusion
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M=runpy.run_path(os.path.join(ROOT,'fusion','FrameSystemV05.py'))
V,P,CUT=M['V'],M['P'],M['CUT']
def run(_context):
 b=M['Builder']();b.doc.name='SKADIS mounting ligament comparison - design study'
 b.d.userParameters.add('webCenterOffset',V('(pitch/2-(pitch-(slotHeight-slotWidth))/2)^2/pitch'),'mm','Equal clearance to three adjacent slot outlines; 1.25 mm at standard lattice')
 folder=os.path.join(ROOT,'models','mounting-study');os.makedirs(folder,exist_ok=True)
 for i,label in enumerate(['Original M2','Centered M2','Solid-land M3']):
  ox=i*70;c=b.comp(label)
  b.box(c,str(ox)+' mm','0 mm','60 mm','60 mm','0 mm','boardThickness','Coupon blank')
  for col in range(6):
   x=ox+5+10*col
   for y in ([10,30,50] if col%2==0 else [20,40]):
    if i==2 and col==2 and y==30:continue
    b.slot_pattern(c,str(x)+' mm',str(y)+' mm','1','1','Slot '+str(col)+' '+str(y))
  body=c.bRepBodies.item(0);front=[f for f in body.faces if abs(f.boundingBox.minPoint.z)<1e-7 and abs(f.boundingBox.maxPoint.z)<1e-7]
  b.fillet(c,front,'entryRadius','Rounded entrances')
  x=str(ox+30)+' mm'+('-webCenterOffset' if i==1 else '')
  y='20 mm';bore='2.4 mm';head='4 mm'
  if i==2:x=str(ox+25)+' mm';y='30 mm';bore='3.4 mm';head='6.2 mm'
  b.disk(c,x,y,bore,'0 mm','boardThickness','Mount bore',CUT)
  b.cone(c,x,y,head,'0 mm','('+head+'-'+bore+')/2',CUT,'Flush screw seat')
  opt=b.d.exportManager.createSTLExportOptions(c,os.path.join(folder,label.replace(' ','-')+'.stl'));opt.meshRefinement=adsk.fusion.MeshRefinementSettings.MeshRefinementHigh;assert b.d.exportManager.execute(opt)
 h=b.health();assert h['healthy']
 assert b.d.exportManager.execute(b.d.exportManager.createFusionArchiveExportOptions(os.path.join(folder,'mounting-comparison.f3d')))
 cam=b.app.activeViewport.camera;cam.isPerspective=False;cam.isSmoothTransition=False;cam.eye=P(10,3,-40);cam.target=P(10,3,0);cam.upVector=adsk.core.Vector3D.create(0,1,0);b.app.activeViewport.camera=cam;b.app.activeViewport.fit();b.app.activeViewport.refresh();b.app.activeViewport.saveAsImageFile(os.path.join(folder,'comparison.png'),1800,800)
 with open(os.path.join(folder,'health.json'),'w') as f:json.dump(h,f,indent=2)
 print(h)
