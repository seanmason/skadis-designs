import adsk.core,adsk.fusion,json,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def run(_context):
 d=adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
 tm=adsk.fusion.TemporaryBRepManager.get()
 comps={c.name:c for c in d.allComponents}
 panel=comps['Panel mounting coupon'].bRepBodies.item(0)
 tile=comps['PRINT two pixel drop hook tile'].bRepBodies.item(0)
 def move(body,x,y,z):
  t=tm.copy(body);m=adsk.core.Matrix3D.create();m.translation=adsk.core.Vector3D.create(x/10,y/10,z/10);assert tm.transform(t,m);return t
 def overlap(a,b):
  t=tm.copy(a);v=t.volume;assert tm.booleanOperation(t,b,adsk.fusion.BooleanTypes.DifferenceBooleanType);return max(0,(v-(t.volume if t.isValid else 0))*1000)
 errors=[];tests=0
 # A slot at (5,10), second tile already seated one pitch below/above.
 for phase in ['insert','drop']:
  for i in range(41):
   lift=3.5 if phase=='insert' else 3.5*(1-i/40)
   z=-10*(1-i/40) if phase=='insert' else 0
   moving=move(tile,-55,10+lift,z)
   for name,body in [('board',panel),('tile below',move(tile,-55,-10,0))]:
    v=overlap(moving,body);tests+=1
    if v>.001:errors.append([phase,i,name,v])
 seated=move(tile,-55,10,0)
 straight_pull_overlap=overlap(move(seated,0,0,-1),panel)
 mate=comps['PRINT seam mate'].bRepBodies.item(0)
 carrier=next(c for n,c in comps.items() if n.startswith('PRINT carrier')).bRepBodies.item(0)
 report={'motion_samples':tests,'collisions':errors,'straight_pull_blocked_overlap_mm3':straight_pull_overlap,'carrier_panel_overlap_mm3':overlap(carrier,panel),'seam_overlap_mm3':overlap(panel,mate),'installation':'bottom upward; remove top downward; lift 3.5 mm before pulling','physical_fit_verified':False}
 out=os.path.join(ROOT,'models','v061','fit-kit','motion-validation.json')
 with open(out,'w') as f:json.dump(report,f,indent=2)
 print(report)
 assert not errors,errors
 assert straight_pull_overlap>.01
