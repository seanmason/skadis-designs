"""Native, parametric clean-face prototype. Run build_panels, frame,
carrier_seed(0,j) for j=0..3, carrier_seed(1,0), repeat_carriers,
joints(i,0) for i=0..1, repeat_frame_joints, wall_seed, repeat_wall_tabs.
Use separate Fusion calls for these phases.
Hardware is nominal envelope geometry; physical hook, screw and printed-fit trials required.
"""
import adsk.core, adsk.fusion, runpy, os, json, math
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M=runpy.run_path(os.path.join(ROOT,'fusion','FrameSystemV03.py'))
V,P,NEW,CUT,JOIN=M['V'],M['P'],M['NEW'],M['CUT'],M['JOIN']
NAME='Infinite SKADIS HD v0.4 - flush screw prototype'
OBSOLETE=['mountInset','mountBore','capDiameter','capThickness','seatThickness','screwDiameter','screwClearance','keyWidth','keyThickness','keyPegDiameter','keySocketDiameter','keyPegHeight','keySocketDepth','registerPin','registerSocket','registerPinHeight','registerSocketDepth','registerOffset','wallShim']
XS=['pitch/2','panelWidth','2*panelWidth-pitch/2']
YS=['pitch','panelHeight-pitch','panelHeight+pitch','2*panelHeight-pitch']
PANELS=[('lower left','0 mm','0 mm',(1,0,1,0),'ll'),('lower right','panelWidth','0 mm',(0,1,1,0),'lr'),('upper left','0 mm','panelHeight',(1,0,0,1),'ul'),('upper right','panelWidth','panelHeight',(0,1,0,1),'ur')]

class Builder(M['Builder']):
    def __init__(self):
        super().__init__(NAME,6,6)
        for n,e,c in [('supportWidth','3.2 mm','Prototype blade; two perimeter lines need print review'),('supportLength','12 mm','Compression bearing length'),('hookEnvelopeWidth','6 mm','Conservative provisional continuous hook column'),('carrierThickness','7 mm','Room for captive M2 nut and stock M5x12'),('panelClearance','2.4 mm','M2 clearance'),('panelHeadPocket','4 mm','DIN965 3.8 mm head plus 0.1 mm recess'),('carrierHeadPocket','9.4 mm','DIN965 M5 9.2 mm head plus recess'),('carrierBore','5.5 mm','M5 clearance'),('tongueWidth','2.8 mm','Rear axial registration tongue'),('tongueLength','8 mm','Axial release registration'),('tongueDepth','0.6 mm','Tongue engagement'),('registerClearance','0.2 mm','Each side of printed tongue'),('carrierZ','boardThickness+hookClearance','Rear hook cavity boundary')]:
            self.d.userParameters.add(n,V(e),'mm',c)
        self.d.userParameters.itemByName('frameZ').expression='carrierZ+carrierThickness'
        self.d.userParameters.itemByName('hookClearance').comment='PROVISIONAL unobstructed depth behind board; carriers begin at its rear boundary'
        for n in OBSOLETE:self.d.userParameters.itemByName(n).deleteMe()
    def cone(self,c,x,y,dia,z,depth,op,name):
        s=self.circle(c,x,y,dia,z,name+' sketch')
        i=c.features.extrudeFeatures.createInput(s.profiles.item(0),op)
        i.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(V(depth)),adsk.fusion.ExtentDirections.PositiveExtentDirection,V('-45 deg'))
        if op==CUT:i.participantBodies=list(c.bRepBodies)
        f=c.features.extrudeFeatures.add(i);f.name=name;s.isVisible=False
        return f
    def clean_panel(self,label,ox,oy,edges,prefix):
        c=self.comp('Panel '+label);x='('+ox+')';y='('+oy+')'
        for s,e in zip(('Left','Right','Bottom','Top'),edges):self.d.userParameters.add(prefix+s,V(str(e)),'','Finished edge flag; change by rebuilding variant, resize natively')
        self.box(c,x+'+seamGap/2',y+'+seamGap/2','panelWidth-seamGap','panelHeight-seamGap','0 mm','boardThickness','01 Panel blank')
        body=c.bRepBodies.item(0);vertical=[]
        for edge in body.edges:
            bb=edge.boundingBox
            if abs(bb.maxPoint.z-bb.minPoint.z-self.value('boardThickness'))>1e-6:continue
            left=abs(bb.minPoint.x-self.value(x+'+seamGap/2'))<1e-6
            bottom=abs(bb.minPoint.y-self.value(y+'+seamGap/2'))<1e-6
            if edges[0 if left else 1] and edges[2 if bottom else 3]:vertical.append(edge)
        if vertical:self.fillet(c,vertical,'cornerRadius','02 Rounded outer corners')
        self.slot_pattern(c,x+'+pitch/4',y+'+pitch/2','columns','rows','03 Complete A lattice')
        self.slot_pattern(c,x+'+3*pitch/4',y+'+pitch*'+prefix+'Bottom','columns','rows+1-'+prefix+'Bottom-'+prefix+'Top','04 B lattice with finished horizontal edges')
        front=[f for f in body.faces if abs(f.boundingBox.minPoint.z)<1e-7 and abs(f.boundingBox.maxPoint.z)<1e-7]
        self.fillet(c,front,'entryRadius','05 Rounded slot entrances and perimeter')
        for xx in [x+'+pitch/2',x+'+panelWidth-pitch/2']:
            for yy in [y+'+pitch',y+'+panelHeight-pitch']:
                self.disk(c,xx,yy,'panelClearance','0 mm','boardThickness','06 M2 through bore',CUT)
                self.cone(c,xx,yy,'panelHeadPocket','0 mm','(panelHeadPocket-panelClearance)/2',CUT,'07 Flush countersink')
                self.box(c,xx+'-tongueWidth/2-registerClearance',yy+'-tongueLength/2-registerClearance','tongueWidth+2*registerClearance','tongueLength+2*registerClearance','boardThickness','-tongueDepth-0.2 mm','08 Blind rear registration',CUT)
        return c
    def screw(self,label,x,y,size,head,z,length):
        c=self.comp(label)
        self.cone(c,x,y,head,z,'('+head+'-'+size+')/2',NEW,'Nominal 90 degree head')
        self.disk(c,x,y,size,z+'+('+head+'-'+size+')/2',length+'-('+head+'-'+size+')/2','Unthreaded major-diameter envelope',JOIN)
        # Cross recess is visual/tool-access reference, not a tooling drawing.
        for w,h in [('0.55 mm',head+'*0.6'),(head+'*0.6','0.55 mm')]:
            self.box(c,x+'-('+w+')/2',y+'-('+h+')/2',w,h,z,'0.35 mm','Cross drive envelope',CUT)
        return c
    def carrier(self,i,j):
        x=XS[i];y=YS[j];label=str(i)+str(j);w='30 mm' if i==1 else '20 mm'
        c=self.comp('PRINT carrier '+label+(' double' if i==1 else ' single'))
        self.box(c,x+'-('+w+')/2',y+'-17 mm',w,'31 mm','carrierZ','carrierThickness','Carrier bearing block')
        axes=[x+'-pitch/2',x+'+pitch/2'] if i==1 else [x]
        for k,xx in enumerate(axes):
            self.box(c,xx+'-supportWidth/2',y+'-supportLength/2','supportWidth','supportLength','carrierZ','-hookClearance','Integrated compression blade',JOIN)
            self.box(c,xx+'-tongueWidth/2',y+'-tongueLength/2','tongueWidth','tongueLength','boardThickness','-tongueDepth','Axially releasing registration tongue',JOIN)
            self.box(c,xx+'-tongueWidth/2',y+'-2 mm','tongueWidth','4 mm','boardThickness-tongueDepth','tongueDepth','Split registration into printable end pads',CUT)
            self.disk(c,xx,y,'panelClearance','boardThickness-tongueDepth','hookClearance+carrierThickness+tongueDepth','M2 through passage',CUT)
            self.box(c,xx+'-2.15 mm',y+'-2.4 mm','4.3 mm','16.4 mm','carrierZ+2 mm','2 mm','Top-loaded captive hex nut track',CUT)
            n=self.comp('METAL M2 nut '+label+str(k))
            verts=[]
            for ang in [30,90,150,210,270,330]:
                verts.append([xx+'+('+str(round(4/math.sqrt(3)*math.cos(math.radians(ang)),6))+' mm)',y+'+('+str(round(4/math.sqrt(3)*math.sin(math.radians(ang)),6))+' mm)','carrierZ+2.2 mm'])
            self.poly3(n,'z','carrierZ+2.2 mm',verts,'1.6 mm',NEW,'M2 hex nut AF4 envelope')
            self.disk(n,xx,y,'2.1 mm','carrierZ+2.2 mm','1.6 mm','Thread envelope',CUT)
            keeper=self.comp('PRINT nut keeper '+label+str(k))
            self.box(keeper,xx+'-2.1 mm',y+'+11 mm','4.2 mm','3 mm','carrierZ+2.05 mm','1.9 mm','Sliding keeper plug - fit trial')
            self.box(keeper,xx+'-3 mm',y+'+14 mm','6 mm','0.8 mm','carrierZ+1 mm','4 mm','Keeper handling flange',JOIN)
            self.screw('REFERENCE panel M2x20 '+label+str(k),xx,y,'2 mm','3.8 mm','0.1 mm','20 mm')
        yy=y+'-11 mm'
        # Two shallow keys prevent carrier rotation while its M5 is tightened.
        for dy in ['-5 mm','+5 mm']:
            self.box(c,x+'-2.9 mm',yy+dy+'-1 mm','5.8 mm','2 mm','frameZ','0.8 mm','Extrusion mouth anti-rotation key',JOIN)
        self.disk(c,x,yy,'carrierBore','carrierZ','carrierThickness','Carrier M5 bore',CUT)
        self.cone(c,x,yy,'carrierHeadPocket','carrierZ','(carrierHeadPocket-carrierBore)/2',CUT,'Recessed carrier fixing')
        self.screw('REFERENCE carrier M5x12 '+label,x,yy,'5 mm','9.2 mm','carrierZ+0.1 mm','12 mm')
        nut=self.comp('METAL channel nut '+label)
        self.box(nut,x+'-nutWidth/2',yy+'-nutLength/2','nutWidth','nutLength','frameZ+profileLip','nutThickness','Provisional metal channel nut')
        self.disk(nut,x,yy,'5.2 mm','frameZ+profileLip','nutThickness','Thread envelope',CUT)
        return c

def active():
    b=Builder.__new__(Builder);b.app=adsk.core.Application.get()
    doc=b.app.activeDocument
    if doc.name!=NAME:doc=[d for d in b.app.documents if d.name==NAME][-1]
    doc.activate();b.doc=doc
    b.d=adsk.fusion.Design.cast(b.app.activeProduct);b.root=b.d.rootComponent;return b
def build_panels(_context):
    b=Builder()
    for args in PANELS:b.clean_panel(*args)
    print(b.health())
def frame(_context):
    b=active()
    for i,x in enumerate(XS):b.rail('Vertical rail '+str(i),'y','2 mm','2*panelHeight-4 mm',x)
    for j,y in enumerate(['10 mm','2*panelHeight-10 mm']):
        for i in range(2):b.rail('Horizontal tie '+str(i)+str(j),'x',XS[i]+'+10 mm',XS[i+1]+'-('+XS[i]+')-20 mm',y)
    print(b.health())
def carriers(i):
    b=active()
    for j in range(4):b.carrier(i,j)
    print(b.health())
def carrier_seed(i,j):
    assert i==0 or (i==1 and j==0)
    b=active();b.carrier(i,j);print(b.health())
def repeat_carriers(_context):
    """Reuse whole carrier/hardware stations through native occurrence patterns."""
    b=active()
    left=[];middle=[]
    for o in b.root.occurrences:
        n=o.component.name
        if n.startswith(('PRINT carrier','METAL M2 nut','PRINT nut keeper','REFERENCE panel M2','REFERENCE carrier M5','METAL channel nut')):
            (left if o.component.bRepBodies.item(0).boundingBox.maxPoint.x<b.value('panelWidth/2') else middle).append(o)
    assert len(left)==24 and len(middle)==9,(len(left),len(middle))
    def pattern(occs,axis,distance,name):
        collection=adsk.core.ObjectCollection.create()
        for o in occs:collection.add(o)
        pi=b.root.features.rectangularPatternFeatures.createInput(collection,axis,V('2'),V(distance),adsk.fusion.PatternDistanceType.SpacingPatternDistanceType)
        pi.setDirectionTwo(b.root.yConstructionAxis if axis==b.root.xConstructionAxis else b.root.xConstructionAxis,V('1'),V('pitch'))
        f=b.root.features.rectangularPatternFeatures.add(pi);f.name=name
    pattern(left,b.root.xConstructionAxis,'2*panelWidth-pitch','Right rail carrier stations')
    for distance in ['panelHeight-2*pitch','panelHeight','2*panelHeight-2*pitch']:
        pattern(middle,b.root.yConstructionAxis,distance,'Shared carrier station at '+distance)
    print(b.health())
def joints(i,j):
    b=active();y='20 mm' if j==0 else '2*panelHeight-20 mm';sy=1 if j==0 else -1
    b.joint(str(i)+str(j)+'L',XS[i]+'+10 mm',y,1,sy)
    b.joint(str(i)+str(j)+'R',XS[i+1]+'-10 mm',y,-1,sy)
    print('Joint pair',i,j)
def walls(_context):
    b=active()
    for i,(x,n) in enumerate([('20 mm',1),('2*panelWidth-20 mm',-1)]):
        for j,y in enumerate(['2*panelHeight/3','4*panelHeight/3']):b.wall_tab(str(i)+str(j),x,y,n)
    print(b.health())
def half_turn(b,occs,name):
    axis=b.root.constructionAxes.itemByName('Frame center rotation axis')
    if not axis:
        planes=[]
        for base,expr in [(b.root.yZConstructionPlane,'panelWidth'),(b.root.xZConstructionPlane,'panelHeight')]:
            pi=b.root.constructionPlanes.createInput();pi.setByOffset(base,V(expr));pl=b.root.constructionPlanes.add(pi);pl.isLightBulbOn=False;planes.append(pl)
        ai=b.root.constructionAxes.createInput();ai.setByTwoPlanes(*planes);axis=b.root.constructionAxes.add(ai);axis.name='Frame center rotation axis';axis.isLightBulbOn=False
    oc=adsk.core.ObjectCollection.create()
    for o in occs:oc.add(o)
    pi=b.root.features.circularPatternFeatures.createInput(oc,axis);pi.quantity=V('2');pi.totalAngle=V('180 deg');pi.isSymmetric=False
    f=b.root.features.circularPatternFeatures.add(pi);f.name=name
def repeat_frame_joints(_context):
    b=active();occs=[o for o in b.root.occurrences if o.component.name.startswith(('METAL in-bay','REFERENCE side M5x8','REFERENCE thin METAL channel nut side'))]
    assert len(occs)==20,len(occs)
    half_turn(b,occs,'Upper frame joints - rotated instances')
    print(b.health())
def wall_seed(_context):
    b=active();b.wall_tab('00','20 mm','2*panelHeight/3',1);print(b.health())
def repeat_wall_tabs(_context):
    b=active();occs=[o for o in b.root.occurrences if o.component.name.startswith(('METAL flush wall','REFERENCE side M5x8 wall','REFERENCE thin METAL channel nut side wall','REFERENCE wall anchor'))]
    assert len(occs)==6,len(occs)
    oc=adsk.core.ObjectCollection.create()
    for o in occs:oc.add(o)
    pi=b.root.features.rectangularPatternFeatures.createInput(oc,b.root.yConstructionAxis,V('2'),V('2*panelHeight/3'),adsk.fusion.PatternDistanceType.SpacingPatternDistanceType)
    pi.setDirectionTwo(b.root.xConstructionAxis,V('1'),V('pitch'))
    b.root.features.rectangularPatternFeatures.add(pi).name='Second left wall tab'
    occs=[o for o in b.root.occurrences if o.component.name.startswith(('METAL flush wall','REFERENCE side M5x8 wall','REFERENCE thin METAL channel nut side wall','REFERENCE wall anchor'))]
    assert len(occs)==12,len(occs)
    half_turn(b,occs,'Right wall tabs - rotated instances')
    print(b.health())
