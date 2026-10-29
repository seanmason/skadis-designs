"""Native layout/clearance study, NOT a release-ready retention mechanism."""
import adsk.core,adsk.fusion,runpy,os,json,math
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M=runpy.run_path(os.path.join(ROOT,'fusion','FrameSystemV03.py'))
V,P,NEW,CUT=M['V'],M['P'],M['NEW'],M['CUT']
class Builder(M['Builder']):
    def __init__(self):
        super().__init__('SKADIS v0.4 - clean-face connector CLEARANCE STUDY',6,6)
        for n,e,c in [('supportWidth','3 mm','Candidate blade width, not a strength-validated part'),('supportLength','12 mm','Candidate blade length along slot column'),('hookEnvelopeWidth','6 mm','Provisional hook sweep width: 5 mm throat plus 0.5 mm each side'),('hookLift','8 mm','Provisional vertical insertion travel'),('carrierThickness','4 mm','Larger hardware stays behind hook clearance datum')]:
            self.d.userParameters.add(n,V(e),'mm',c)
        self.d.userParameters.itemByName('frameZ').expression='boardThickness+hookClearance+carrierThickness'
    def clean_panel(self,name,ox,edges,prefix):
        c=self.comp(name);x='('+ox+')'
        self.box(c,x+'+seamGap/2','seamGap/2','panelWidth-seamGap','panelHeight-seamGap','0 mm','boardThickness','01 Panel blank')
        body=c.bRepBodies.item(0)
        vertical=[]
        for edge in body.edges:
            bb=edge.boundingBox
            if abs(bb.maxPoint.z-bb.minPoint.z-self.value('boardThickness'))>1e-6:continue
            left=abs(bb.minPoint.x-self.value(x+'+seamGap/2'))<1e-6
            bottom=abs(bb.minPoint.y-self.value('seamGap/2'))<1e-6
            if edges[0 if left else 1] and edges[2 if bottom else 3]:vertical.append(edge)
        if vertical:self.fillet(c,vertical,'cornerRadius','02 Exterior corner rounds')
        # No mounting-node omissions. Finished horizontal edges omit only split B slots.
        self.slot_pattern(c,x+'+pitch/4','pitch/2','columns','rows','03 Complete A field')
        self.slot_pattern(c,x+'+3*pitch/4','pitch','columns','rows-1','04 Complete B field - finished top and bottom')
        front=[f for f in body.faces if abs(f.boundingBox.minPoint.z)<1e-7 and abs(f.boundingBox.maxPoint.z)<1e-7]
        self.fillet(c,front,'entryRadius','05 Rounded entrances and edges')
        return c
def run(_context):
    b=Builder()
    left=b.clean_panel('Panel left - restored slot field','0 mm',(1,0,1,1),'left')
    right=b.clean_panel('Panel right - restored slot field','panelWidth',(0,1,1,1),'right')
    envelopes=[]
    for i in range(24):
        envelope=b.comp('REFERENCE ONLY - hook insertion corridor '+str(i))
        b.box(envelope,'pitch/4+'+str(i)+'*pitch/2-hookEnvelopeWidth/2','0 mm','hookEnvelopeWidth','panelHeight','boardThickness','hookClearance','Provisional swept hook column '+str(i))
        envelopes.append(envelope)
    supports=[]
    for x in ['pitch/2','panelWidth-pitch/2','panelWidth+pitch/2','2*panelWidth-pitch/2']:
        for y in ['pitch','panelHeight-pitch']:
            c=b.comp('CONCEPT support blade - retention NOT DESIGNED')
            b.box(c,'('+x+')-supportWidth/2','('+y+')-supportLength/2','supportWidth','supportLength','boardThickness','hookClearance','Solid-web support envelope')
            supports.append(c)
    carriers=[]
    for x,w in [('0 mm','20 mm'),('panelWidth-15 mm','30 mm'),('2*panelWidth-20 mm','20 mm')]:
        for y in ['pitch','panelHeight-pitch']:
            c=b.comp('CONCEPT carrier envelope - hardware NOT DESIGNED')
            b.box(c,x,'('+y+')-8 mm',w,'24 mm','boardThickness+hookClearance','carrierThickness','Rear carrier space reservation')
            carriers.append(c)
    for i,x in enumerate(['10 mm','panelWidth','2*panelWidth-10 mm']):
        b.rail('REFERENCE 2020 rail '+str(i),'y','2 mm','panelHeight-4 mm',x)
    # Conservative hook columns cover every y position; valid even for adjacent hooks.
    lateral=(b.value('pitch/2-hookEnvelopeWidth-supportWidth')/2)*10
    assert lateral>0
    old_projection=b.value('capThickness+3 mm')*10
    report={'status':'clearance architecture study; retention and assembly release mechanism unresolved','old_front_projection_mm':old_projection,'candidate_front_projection_mm':0,'provisional_hook_width_mm':b.value('hookEnvelopeWidth')*10,'provisional_hook_lift_mm':b.value('hookLift')*10,'blade_to_hook_envelope_side_clearance_mm':lateral,'hook_cavity_mm':b.value('hookClearance')*10,'proposed_face_to_wall_mm':b.value('frameZ+20 mm')*10,'holes_per_120_panel':66,'notes':['No cap-node slot omissions','Finished top/bottom contain complete slots only','Outer border is narrower than v03 and needs edge-strength testing','Carriers/blades are space reservations, not printable approved mounts','Actual hook sweep and mosaic rear surface remain unmeasured']}
    report['health']=b.health()
    folder=os.path.join(ROOT,'models','v04-study');os.makedirs(folder,exist_ok=True)
    for envelope in envelopes:envelope.isBodiesFolderLightBulbOn=False
    b.app.activeViewport.fit()
    ex=b.d.exportManager
    assert ex.execute(ex.createFusionArchiveExportOptions(os.path.join(folder,'connector-clearance-study.f3d')))
    assert ex.execute(ex.createSTEPExportOptions(os.path.join(folder,'connector-clearance-study.step')))
    with open(os.path.join(ROOT,'docs','connector-clearance-v04.json'),'w') as f:json.dump(report,f,indent=2)
    b.app.activeViewport.saveAsImageFile(os.path.join(folder,'study.png'),1600,1000)
    print(json.dumps(report))
