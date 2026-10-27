"""Run inside Fusion. Native parametric 2x2 frame demonstrator and panel library.
All dimensions are millimetres in expressions; Fusion API coordinates are cm.
Hardware is nominal envelope CAD, not a purchased manufacturer's certified part.
"""
import adsk.core, adsk.fusion, os, json
V=adsk.core.ValueInput.createByString
P=adsk.core.Point3D.create
H=adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation
Y=adsk.fusion.DimensionOrientations.VerticalDimensionOrientation
NEW=adsk.fusion.FeatureOperations.NewBodyFeatureOperation
CUT=adsk.fusion.FeatureOperations.CutFeatureOperation
JOIN=adsk.fusion.FeatureOperations.JoinFeatureOperation
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def timeline_items(items):
    for t in items:
        if t.objectType==adsk.fusion.TimelineGroup.classType():yield from timeline_items(t)
        else:yield t

class Builder:
    def __init__(self, name, columns=6, rows=6):
        self.app=adsk.core.Application.get()
        self.doc=self.app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        self.doc.name=name
        self.d=adsk.fusion.Design.cast(self.app.activeProduct)
        self.d.designType=adsk.fusion.DesignTypes.ParametricDesignType
        self.root=self.d.rootComponent
        for n,e,u,c in [
            ('columns',str(columns),'','Even integer 4..14; each cell is 20 mm'),
            ('rows',str(rows),'','Even integer 4..14'),
            ('pitch','20 mm','mm','Keep for dense SKADIS compatible lattice'),
            ('panelWidth','columns*pitch','mm','Nominal module pitch X'),
            ('panelHeight','rows*pitch','mm','Nominal module pitch Y'),
            ('seamGap','0.2 mm','mm','Physical envelope shrinks around fixed lattice'),
            ('boardThickness','5 mm','mm','Fit-test with real hooks'),
            ('slotWidth','5 mm','mm','Minimum throat width'),
            ('slotHeight','15 mm','mm','Minimum throat height'),
            ('entryRadius','0.4 mm','mm','Front slot and perimeter edge rounding'),
            ('cornerRadius','6 mm','mm','Plan-view panel corner rounding'),
            ('hookClearance','10 mm','mm','PROVISIONAL: board rear to front of extrusion'),
            ('frameZ','boardThickness+hookClearance','mm','Front extrusion datum'),
            ('mountInset','12 mm','mm','Exterior node inset from outside module edge'),
            ('mountBore','8.4 mm','mm','Clearance around 8 mm metal shoulder'),
            ('capDiameter','18 mm','mm','Visible decorative mounting disk'),
            ('capThickness','2 mm','mm','Metal clamping cap / washer'),
            ('seatThickness','2 mm','mm','Printed rear bearing washer'),
            ('screwDiameter','5 mm','mm','Nominal M5 reference, threads omitted'),
            ('screwClearance','5.5 mm','mm','Cap and spacer bore'),
            ('keyWidth','4 mm','mm','Registration key corridor width'),
            ('keyThickness','2 mm','mm','Rear removable key body'),
            ('keyPegDiameter','3 mm','mm','Rear locating peg'),
            ('keySocketDiameter','3.4 mm','mm','0.2 mm radial starting fit'),
            ('keyPegHeight','0.8 mm','mm','Peg penetration'),
            ('keySocketDepth','1 mm','mm','Blind locating pocket'),
        ]: self.d.userParameters.add(n,V(e),u,c)
    def value(self,e): return self.d.unitsManager.evaluateExpression(str(e),'cm')
    def comp(self,name):
        c=self.root.occurrences.addNewComponent(adsk.core.Matrix3D.create()).component
        c.name=name
        return c
    def plane(self,c,z):
        if z=='0 mm': return c.xYConstructionPlane
        i=c.constructionPlanes.createInput(); i.setByOffset(c.xYConstructionPlane,V(z))
        p=c.constructionPlanes.add(i); p.name='Datum Z = '+z; p.isLightBulbOn=False
        return p
    def locate(self,s,pt,x,y):
        for axis,e in [(H,x),(Y,y)]:
            if abs(self.value(e))<1e-8:
                (s.geometricConstraints.addVerticalPoints if axis==H else s.geometricConstraints.addHorizontalPoints)(s.originPoint,pt)
            else:
                s.sketchDimensions.addDistanceDimension(s.originPoint,pt,axis,P(-2,-2,0)).parameter.expression='abs('+e+')'
    def rect(self,c,x,y,w,h,z,name):
        s=c.sketches.add(self.plane(c,z)); s.name=name
        a,b,ww,hh=[self.value(t) for t in (x,y,w,h)]
        ls=s.sketchCurves.sketchLines.addTwoPointRectangle(P(a,b,0),P(a+ww,b+hh,0))
        for i,l in enumerate(ls):
            (s.geometricConstraints.addHorizontal if i%2==0 else s.geometricConstraints.addVertical)(l)
        self.locate(s,ls[0].startSketchPoint,x,y)
        s.sketchDimensions.addDistanceDimension(ls[0].startSketchPoint,ls[0].endSketchPoint,H,P(a,b-1,0)).parameter.expression=w
        s.sketchDimensions.addDistanceDimension(ls[1].startSketchPoint,ls[1].endSketchPoint,Y,P(a+ww+1,b,0)).parameter.expression=h
        return s
    def circle(self,c,x,y,dia,z,name):
        s=c.sketches.add(self.plane(c,z));s.name=name
        q=s.sketchCurves.sketchCircles.addByCenterRadius(P(self.value(x),self.value(y),0),self.value(dia)/2)
        if abs(self.value(x))+abs(self.value(y))<1e-8:
            s.geometricConstraints.addCoincident(q.centerSketchPoint,s.originPoint)
        else:self.locate(s,q.centerSketchPoint,x,y)
        s.sketchDimensions.addDiameterDimension(q,P(self.value(x)+1,self.value(y)+1,0)).parameter.expression=dia
        return s
    def ext(self,c,s,depth,op,name):
        f=c.features.extrudeFeatures.addSimple(s.profiles.item(0),V(depth),op)
        f.name=name;s.isVisible=False
        return f
    def box(self,c,x,y,w,h,z,depth,name,op=NEW):
        return self.ext(c,self.rect(c,x,y,w,h,z,name+' sketch'),depth,op,name)
    def disk(self,c,x,y,dia,z,depth,name,op=NEW):
        return self.ext(c,self.circle(c,x,y,dia,z,name+' sketch'),depth,op,name)
    def fillet(self,c,entities,r,name):
        oc=adsk.core.ObjectCollection.create()
        for e in entities:oc.add(e)
        i=c.features.filletFeatures.createInput()
        i.edgeSetInputs.addConstantRadiusEdgeSet(oc,V(r),False)
        f=c.features.filletFeatures.add(i);f.name=name
        return f
    def slot_pattern(self,c,x,y,nx,ny,name):
        s=c.sketches.add(c.xYConstructionPlane);s.name=name+' constrained seed'
        xx=self.value(x);yy=self.value(y);ll=self.value('slotHeight-slotWidth')
        es=s.addCenterToCenterSlot(P(xx,yy-ll/2,0),P(xx,yy+ll/2,0),V('slotWidth'),True,V('slotHeight-slotWidth'),V('90 deg'))
        s.sketchDimensions.item(0).parameter.expression='slotWidth'
        s.sketchDimensions.item(1).parameter.expression='slotHeight-slotWidth'
        s.geometricConstraints.addHorizontal(es[5])
        s.sketchDimensions.addDistanceDimension(es[5].startSketchPoint,es[5].endSketchPoint,H,P(xx+1,yy+1,0)).parameter.expression='pitch/2'
        self.locate(s,es[4].startSketchPoint,x,'('+y+')-(slotHeight-slotWidth)/2')
        f=self.ext(c,s,'boardThickness',CUT,name+' through cut')
        oc=adsk.core.ObjectCollection.create();oc.add(f)
        pi=c.features.rectangularPatternFeatures.createInput(oc,c.xConstructionAxis,V(nx),V('pitch'),adsk.fusion.PatternDistanceType.SpacingPatternDistanceType)
        pi.setDirectionTwo(c.yConstructionAxis,V(ny),V('pitch'))
        pat=c.features.rectangularPatternFeatures.add(pi);pat.name=name+' lattice'
    def panel(self,name,ox='0 mm',oy='0 mm',edges=(0,0,0,0),prefix='panel'):
        assert all(e in (0,1) for e in edges),'Edge modes must be 0 or 1'
        assert self.d.userParameters.itemByName('rows').value>sum(edges[2:])+2,'Use at least 6 rows when both top and bottom are finished'
        c=self.comp(name)
        for suffix,value in zip(('Left','Right','Bottom','Top'),edges):
            self.d.userParameters.add(prefix+suffix,V(str(value)),'','0 internal / 1 finished; full cell border and inset mounting')
        l,r,b,t=[prefix+s for s in ('Left','Right','Bottom','Top')]
        x='('+ox+')';y='('+oy+')'
        self.box(c,x+'+seamGap/2',y+'+seamGap/2','panelWidth-seamGap','panelHeight-seamGap','0 mm','boardThickness','01 Panel blank')
        body=c.bRepBodies.item(0);body.name=name
        vertical=[]
        for e in body.edges:
            bb=e.boundingBox
            if abs(bb.maxPoint.z-bb.minPoint.z-self.value('boardThickness'))>1e-6:continue
            left=abs(bb.minPoint.x-self.value(x+'+seamGap/2'))<1e-6
            bottom=abs(bb.minPoint.y-self.value(y+'+seamGap/2'))<1e-6
            if edges[0 if left else 1] and edges[2 if bottom else 3]:vertical.append(e)
        if vertical:self.fillet(c,vertical,'cornerRadius','02 Rounded exterior corners')
        # Four pattern strips reserve COMPLETE slots near each mounting node.
        self.slot_pattern(c,x+'+pitch/4+pitch*('+l+'+1)',y+'+pitch/2+pitch*'+b,'columns-'+l+'-'+r+'-1','rows-'+b+'-'+t,'03 A main')
        self.slot_pattern(c,x+'+pitch/4+pitch*'+l,y+'+3*pitch/2+pitch*'+b,'1','rows-'+b+'-'+t+'-2','04 A end strip')
        self.slot_pattern(c,x+'+3*pitch/4+pitch*'+l,y+'+pitch*'+b,'columns-'+l+'-'+r+'-1','rows+1-'+b+'-'+t,'05 B main')
        self.slot_pattern(c,x+'+panelWidth-pitch/4-pitch*'+r,y+'+pitch+pitch*'+b,'1','rows-1-'+b+'-'+t,'06 B end strip')
        for xx in [x+'+mountInset*'+l,x+'+panelWidth-mountInset*'+r]:
            for yy in [y+'+mountInset*'+b,y+'+panelHeight-mountInset*'+t]:
                self.disk(c,xx,yy,'mountBore','0 mm','boardThickness','07 Shared node clearance',CUT)
        # Front face selection follows new pattern instances when counts change.
        front=[f for f in body.faces if abs(f.boundingBox.minPoint.z)<1e-7 and abs(f.boundingBox.maxPoint.z)<1e-7]
        self.fillet(c,front,'entryRadius','08 Rounded slot entrances and face edges')
        # Key sockets are only generated on internal sides; regenerating an edge
        # configuration updates sockets. Dimensional resizing remains native.
        sockets=[]
        if not edges[0]:sockets.append((x+'+pitch/4',y+'+panelHeight/2+pitch'))
        if not edges[1]:sockets.append((x+'+panelWidth-pitch/4',y+'+panelHeight/2+pitch/2'))
        if not edges[2]:sockets.append((x+'+panelWidth/2+pitch/2',y+'+pitch/4'))
        if not edges[3]:sockets.append((x+'+panelWidth/2+pitch/2',y+'+panelHeight-pitch/4'))
        for xx,yy in sockets:
            self.disk(c,xx,yy,'keySocketDiameter','boardThickness','-keySocketDepth','09 Blind rear key socket',CUT)
        return c
    def key(self,name,x,y,vertical=False):
        c=self.comp(name);z='boardThickness'
        if vertical:
            self.box(c,x+'-keyWidth/2',y+'-pitch/4-keyWidth/2','keyWidth','pitch/2+keyWidth',z,'keyThickness','Key spine')
            self.box(c,x+'-pitch/4-keyWidth/2',y+'-pitch/4-keyWidth/2','pitch/4+keyWidth','keyWidth',z,'keyThickness','Lower arm',JOIN)
            self.box(c,x+'-keyWidth/2',y+'+pitch/4-keyWidth/2','pitch/4+keyWidth','keyWidth',z,'keyThickness','Upper arm',JOIN)
            anchors=[(x+'-pitch/4',y+'-pitch/4'),(x+'+pitch/4',y+'+pitch/4')]
        else:
            self.box(c,x+'-keyWidth/2',y+'-pitch/4-keyWidth/2','keyWidth','pitch/2+keyWidth',z,'keyThickness','Key body')
            anchors=[(x,y+'-pitch/4'),(x,y+'+pitch/4')]
        for xx,yy in anchors:self.disk(c,xx,yy,'keyPegDiameter',z,'-keyPegHeight','Locating peg',JOIN)
        return c
    def rail(self,name,x,y,w,h):
        c=self.comp(name+' - nominal 2020 slot-6 envelope')
        self.box(c,x,y,w,h,'frameZ','20 mm','Extrusion envelope')
        # Simplified front T channel with 6 mm mouth and 10 mm nut cavity.
        if w=='20 mm':
            sx=x+'+7 mm';sy=y;sw='6 mm';sh=h
            ix=x+'+5 mm';iy=y;iw='10 mm';ih=h
        else:
            sx=x;sy=y+'+7 mm';sw=w;sh='6 mm'
            ix=x;iy=y+'+5 mm';iw=w;ih='10 mm'
        self.box(c,sx,sy,sw,sh,'frameZ','1.8 mm','Front slot mouth',CUT)
        self.box(c,ix,iy,iw,ih,'frameZ+1.8 mm','4.2 mm','T nut channel',CUT)
        return c
    def node(self,label,x,y):
        cap=self.comp('METAL cap '+label)
        self.disk(cap,x,y,'capDiameter','-capThickness','capThickness','Visible cap')
        self.disk(cap,x,y,'screwClearance','-capThickness','capThickness','M5 clearance',CUT)
        seat=self.comp('PRINT rear bearing seat '+label)
        self.disk(seat,x,y,'capDiameter','boardThickness','seatThickness','Rear bearing seat')
        self.disk(seat,x,y,'mountBore','boardThickness','seatThickness','Shoulder clearance',CUT)
        spacer=self.comp('METAL stepped compression spacer '+label)
        self.disk(spacer,x,y,'8 mm','0 mm','boardThickness+seatThickness','8 mm shoulder')
        self.disk(spacer,x,y,'12 mm','boardThickness+seatThickness','hookClearance-seatThickness','12 mm base',JOIN)
        self.disk(spacer,x,y,'screwClearance','0 mm','frameZ','Through bore',CUT)
        bolt=self.comp('REFERENCE M5 screw '+label+' - length follows stack')
        self.disk(bolt,x,y,'9.5 mm','-capThickness-3 mm','3 mm','Nominal button head')
        self.disk(bolt,x,y,'screwDiameter','-capThickness','frameZ+capThickness+5 mm','Unthreaded shank envelope',JOIN)
        nut=self.comp('REFERENCE M5 slot-6 T nut '+label)
        self.box(nut,x+'-4.8 mm',y+'-5 mm','9.6 mm','10 mm','frameZ+2 mm','4 mm','T nut envelope')
        self.disk(nut,x,y,'5.2 mm','frameZ+2 mm','4 mm','Thread envelope',CUT)
        return cap,seat,spacer,bolt,nut
    def export(self,name,parts):
        os.makedirs(os.path.join(ROOT,'models','v02'),exist_ok=True)
        ex=self.d.exportManager;folder=os.path.join(ROOT,'models','v02')
        assert ex.execute(ex.createFusionArchiveExportOptions(os.path.join(folder,name+'.f3d')))
        for c,filename in parts:
            assert ex.execute(ex.createSTEPExportOptions(os.path.join(folder,filename+'.step'),c))
            stl=ex.createSTLExportOptions(c,os.path.join(folder,filename+'.stl'))
            stl.meshRefinement=adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
            assert ex.execute(stl)
        self.d.userParameters.exportUserParameters([p for p in self.d.userParameters],os.path.join(ROOT,'fusion',name+'-parameters.csv'))
    def health(self):
        bad=[(t.name,t.errorOrWarningMessage) for t in timeline_items(self.d.timeline) if t.healthState!=adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState]
        assert not bad,str(bad)
        loose=[(c.name,s.name) for c in self.d.allComponents for s in c.sketches if not s.isFullyConstrained]
        assert not loose,str(loose)
        for c in self.d.allComponents:
            if c!=self.root:assert c.bRepBodies.count==1 and c.bRepBodies.item(0).isSolid,c.name
        return {'healthy':True,'fully_constrained_sketches':True,'components':self.root.occurrences.count,'timeline_features':self.d.timeline.count}

def build_assembly():
    b=Builder('Infinite SKADIS HD v0.2 - parametric frame assembly')
    parts=[]
    for name,x,y,edges,prefix in [
        ('Panel lower left','0 mm','0 mm',(1,0,1,0),'ll'),
        ('Panel lower right','panelWidth','0 mm',(0,1,1,0),'lr'),
        ('Panel upper left','0 mm','panelHeight',(1,0,0,1),'ul'),
        ('Panel upper right','panelWidth','panelHeight',(0,1,0,1),'ur')]:
        c=b.panel(name,x,y,edges,prefix);parts.append((c,prefix+'-panel-120'))
    kh=b.key('PRINT horizontal alignment key L','panelWidth/2+pitch/2','panelHeight')
    b.key('PRINT horizontal alignment key R','3*panelWidth/2+pitch/2','panelHeight')
    kv=b.key('PRINT vertical alignment key B','panelWidth','panelHeight/2+3*pitch/4',True)
    b.key('PRINT vertical alignment key T','panelWidth','3*panelHeight/2+3*pitch/4',True)
    parts.extend([(kh,'alignment-key-horizontal'),(kv,'alignment-key-vertical')])
    xs=['mountInset','panelWidth','2*panelWidth-mountInset']
    ys=['mountInset','panelHeight','2*panelHeight-mountInset']
    for i,x in enumerate(xs):b.rail('Vertical rail '+str(i),x+'-10 mm','mountInset-10 mm','20 mm','2*panelHeight-2*mountInset+20 mm')
    for j,y in enumerate([ys[0],ys[2]]):
        for i in range(2):b.rail('Horizontal tie '+str(i)+str(j),xs[i]+'+10 mm',y+'-10 mm',xs[i+1]+'-('+xs[i]+')-20 mm','20 mm')
    for i,x in enumerate(xs):
        for j,y in enumerate(ys):
            cap,seat,spacer,bolt,nut=b.node(str(i)+str(j),x,y)
            if i==0 and j==0:parts.append((seat,'rear-bearing-seat'))
    print('BUILD COMPLETE',b.health())
    b.export('frame-assembly-v02',parts)
    return b

def run(_context: str):
    build_assembly()
