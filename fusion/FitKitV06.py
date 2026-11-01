"""Four-part, native-feature fit kit; same interfaces as v0.6, no load rating."""
import os,runpy,json,adsk.core,adsk.fusion
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M=runpy.run_path(os.path.join(ROOT,'fusion','FrameSystemV05.py'))
V,P,CUT,JOIN=[M[k] for k in ('V','P','CUT','JOIN')]
OUT=os.path.join(ROOT,'models','v06','fit-kit')

def run(_context):
 b=M['Builder']();b.doc.name='SKADIS v0.6 minimal interface fit kit'
 b.d.userParameters.itemByName('columns').expression='2'
 b.d.userParameters.itemByName('rows').expression='2'
 lower=b.comp('Panel mounting coupon')
 b.box(lower,'seamGap/2','seamGap/2','2*pitch-seamGap','2*pitch-seamGap','0 mm','boardThickness','Mount coupon web')
 f=b.box(lower,'pitch/2+seamGap/2','2*pitch-1 mm','pitch/2-seamGap','pitch/2+1 mm-seamGap/2','0 mm','boardThickness','Whole slot seam tooth',JOIN)
 tip=b.round_step_tip(lower,'2*pitch+pitch/2-seamGap/2','pitch/2+seamGap/2','pitch-seamGap/2','Rounded tooth seed')
 b.pattern_x(lower,[f,tip],'Two teeth')
 b.slot_pattern(lower,'pitch/4','pitch/2','2','2','A slots')
 b.slot_pattern(lower,'3*pitch/4','pitch','2','2','B slots including seam')
 def front_round(c):
  faces=[f for f in c.bRepBodies.item(0).faces if abs(f.boundingBox.minPoint.z)<1e-7 and abs(f.boundingBox.maxPoint.z)<1e-7]
  b.fillet(c,faces,'entryRadius','Production slot and perimeter rounding')
 front_round(lower)
 b.disk(lower,'pitch/2','pitch','panelClearance','0 mm','boardThickness','11 M2 through bore',CUT)
 b.cone(lower,'pitch/2','pitch','panelHeadPocket','0 mm','(panelHeadPocket-panelClearance)/2',CUT,'12 Flush countersink')
 b.box(lower,'pitch/2-tongueWidth/2-registerClearance','pitch-tongueLength/2-registerClearance','tongueWidth+2*registerClearance','tongueLength+2*registerClearance','boardThickness','-tongueDepth-0.2 mm','Blind rear production registration',CUT)
 upper=b.comp('PRINT seam mate')
 b.box(upper,'seamGap/2','2*pitch+seamGap/2','2*pitch-seamGap','pitch-seamGap','0 mm','boardThickness','Small seam mate web')
 for x in ['pitch/2','3*pitch/2']:
  b.box(upper,x+'-seamGap/2','2*pitch-1 mm','pitch/2+seamGap','pitch/2+1 mm+seamGap/2','0 mm','boardThickness','Receiving step',CUT)
  b.round_step_tip(upper,'2*pitch+pitch/2+seamGap/2',x+'-seamGap/2',x+'+pitch/2+seamGap/2','Rounded receiving step')
 b.slot_pattern(upper,'pitch/4','2*pitch+pitch/2','2','1','Whole A slots')
 front_round(upper)
 carrier=b.carrier(0,0)
 runpy.run_path(os.path.join(ROOT,'fusion','ReviseCenteredM2V06.py'))['revise']('',builder=b,record=False)
 # A monochrome two-pixel version of the existing axial mosaic prototype.
 for n,e in [('pixelGap','0.4 mm'),('pixelThickness','1.2 mm'),('tileBack','0.8 mm'),('snapInterference','0.4 mm')]:b.d.userParameters.add(n,V(e),'mm','Same as v0.5 axial tile prototype; fit trial')
 tile=b.comp('PRINT two pixel tile')
 b.box(tile,'60 mm-4.5 mm','-9.5 mm','9 mm','19 mm','-tileBack','tileBack','Tile core')
 b.box(tile,'60 mm-0.6 mm','-slotHeight/2+0.2 mm','1.2 mm','slotHeight-0.4 mm','0 mm','boardThickness-0.2 mm','Gravity bearing spine',JOIN)
 for side in [-1,1]:
  pts=[('0.8 mm','0 mm'),('2.2 mm','0 mm'),('2.2 mm','boardThickness-0.2 mm'),('(slotWidth+snapInterference)/2','boardThickness+0.5 mm'),('(slotWidth+snapInterference)/2','boardThickness+0.9 mm'),('1.6 mm','boardThickness+2.1 mm'),('0.8 mm','boardThickness+2.1 mm')]
  verts=[['60 mm+('+x+')*'+str(side),'-3 mm',z] for x,z in pts]
  b.poly3(tile,'y','-3 mm',verts,'6 mm',JOIN,'Mosaic spring '+str(side))
 for y in ['-10 mm+pixelGap/2','pixelGap/2']:
  b.box(tile,'60 mm-5 mm+pixelGap/2',y,'10 mm-pixelGap','10 mm-pixelGap','-tileBack-pixelThickness','pixelThickness','Pixel face',JOIN)
 os.makedirs(OUT,exist_ok=True);ex=b.d.exportManager
 parts=[('01-mount-coupon',lower),('02-seam-mate',upper),('03-single-carrier',carrier),('04-two-pixel-tile',tile)]
 report={'health':b.health(),'parts':[],'physical_fit_verified':False}
 for name,c in parts:
  opt=ex.createSTLExportOptions(c,os.path.join(OUT,name+'.stl'));opt.meshRefinement=adsk.fusion.MeshRefinementSettings.MeshRefinementHigh;assert ex.execute(opt)
  bb=c.bRepBodies.item(0).boundingBox
  report['parts'].append({'file':name+'.stl','volume_mm3':c.bRepBodies.item(0).volume*1000,'bounds_mm':[10*(getattr(bb.maxPoint,k)-getattr(bb.minPoint,k)) for k in ['x','y','z']]})
 assert ex.execute(ex.createFusionArchiveExportOptions(os.path.join(OUT,'fit-kit-v06.f3d')))
 assert ex.execute(ex.createSTEPExportOptions(os.path.join(OUT,'fit-kit-v06.step')))
 cam=b.app.activeViewport.camera;cam.isPerspective=False;cam.isSmoothTransition=False;cam.eye=P(12,-9,-22);cam.target=P(3,2,0);cam.upVector=adsk.core.Vector3D.create(0,1,0);b.app.activeViewport.camera=cam;b.app.activeViewport.fit();b.app.activeViewport.refresh();b.app.activeViewport.saveAsImageFile(os.path.join(OUT,'preview.png'),1200,1000)
 with open(os.path.join(OUT,'validation.json'),'w') as f:json.dump(report,f,indent=2)
 print(report)
