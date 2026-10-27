import adsk.core, adsk.fusion
V = adsk.core.ValueInput.createByString
P = adsk.core.Point3D.create
def build_panel(_context: str):
    app=adsk.core.Application.get()
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    doc.name='Infinite SKADIS HD - v0.1 engineering prototype'
    d=adsk.fusion.Design.cast(app.activeProduct)
    d.designType=adsk.fusion.DesignTypes.ParametricDesignType
    for name,expr,unit,comment in [
        ('columns','12','','Integer 20 mm cells across; use even values 4 to 14'),
        ('rows','12','','Integer 20 mm cells high; use even values 4 to 14'),
        ('pitch','20 mm','mm','Dense lattice repeat; keep 20 for IKEA-compatible subset'),
        ('slotWidth','5 mm','mm','Nominal community-measured slot width; fit-test'),
        ('slotHeight','15 mm','mm','Retain full size slots'),
        ('boardThickness','5 mm','mm','Initial hook engagement thickness; fit-test'),
        ('panelWidth','columns*pitch','mm','Derived panel width, do not scale in slicer'),
        ('panelHeight','rows*pitch','mm','Derived panel height'),
        ('pilotDiameter','1.6 mm','mm','M2 thread-forming pilot, test before production'),
        ('pilotDepth','4 mm','mm','Blind depth into rear bridge'),
        ('registerDiameter','3.6 mm','mm','Rear locating recess'),
        ('registerDepth','0.8 mm','mm','Rear locating recess depth'),
        ('bridgeThickness','6 mm','mm','Rear connector thickness'),
        ('bridgeWidth','4.4 mm','mm','Fits 5 mm lattice corridors'),
        ('pegDiameter','3.2 mm','mm','Locating peg: 0.2 mm radial clearance'),
        ('pegHeight','0.6 mm','mm','Locating peg: 0.2 mm depth clearance'),
        ('screwClearance','2.2 mm','mm','M2 screw clearance'),
    ]:
        d.userParameters.add(name,V(expr),unit,comment)
    root=d.rootComponent
    comp=root.occurrences.addNewComponent(adsk.core.Matrix3D.create()).component
    comp.name='Panel - dense staggered lattice'
    sk=comp.sketches.add(comp.xYConstructionPlane); sk.name='01 Panel envelope - constrained'
    lines=sk.sketchCurves.sketchLines.addTwoPointRectangle(P(0,0,0),P(24,24,0))
    sk.geometricConstraints.addCoincident(lines[0].startSketchPoint,sk.originPoint)
    for i,l in enumerate(lines):
        (sk.geometricConstraints.addHorizontal if i%2==0 else sk.geometricConstraints.addVertical)(l)
    dims=sk.sketchDimensions
    dims.addDistanceDimension(lines[0].startSketchPoint,lines[0].endSketchPoint,adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,P(12,-1,0)).parameter.expression='panelWidth'
    dims.addDistanceDimension(lines[1].startSketchPoint,lines[1].endSketchPoint,adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,P(25,12,0)).parameter.expression='panelHeight'
    e=comp.features.extrudeFeatures.addSimple(sk.profiles.item(0),V('boardThickness'),adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    e.name='02 Face plate'; e.bodies.item(0).name='Panel'
    for label,x,y,xx,yy,qty in [('A',0.5,0.5,'pitch/4','pitch/2-(slotHeight-slotWidth)/2','rows'),('B',1.5,-0.5,'3*pitch/4','(slotHeight-slotWidth)/2','rows+1')]:
        s=comp.sketches.add(comp.xYConstructionPlane); s.name='03 Slot '+label+' - constrained seed'
        entities=s.addCenterToCenterSlot(P(x,y,0),P(x,y+1,0),V('slotWidth'),True,V('slotHeight-slotWidth'),V('90 deg'))
        s.sketchDimensions.item(0).parameter.expression='slotWidth'
        s.sketchDimensions.item(1).parameter.expression='slotHeight-slotWidth'
        cl=entities[4]
        al=entities[5]
        s.geometricConstraints.addHorizontal(al)
        s.sketchDimensions.addDistanceDimension(al.startSketchPoint,al.endSketchPoint,adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,P(2,2,0)).parameter.expression='pitch/2'
        s.sketchDimensions.addDistanceDimension(s.originPoint,cl.startSketchPoint,adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,P(x,-1.5,0)).parameter.expression=xx
        s.sketchDimensions.addDistanceDimension(s.originPoint,cl.startSketchPoint,adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,P(-1,y,0)).parameter.expression=yy
        cut=comp.features.extrudeFeatures.addSimple(s.profiles.item(0),V('boardThickness'),adsk.fusion.FeatureOperations.CutFeatureOperation)
        cut.name='04 Slot '+label+' through cut'
        objects=adsk.core.ObjectCollection.create(); objects.add(cut)
        pi=comp.features.rectangularPatternFeatures.createInput(objects,comp.xConstructionAxis,V('columns'),V('pitch'),adsk.fusion.PatternDistanceType.SpacingPatternDistanceType)
        pi.setDirectionTwo(comp.yConstructionAxis,V(qty),V('pitch'))
        pat=comp.features.rectangularPatternFeatures.add(pi); pat.name='05 Lattice '+label
        s.isVisible=False
    sk.isVisible=False
    app.activeViewport.fit()
    print('Created',comp.name,'bodies',comp.bRepBodies.count)
    for s in comp.sketches: print(s.name,'fullyConstrained',s.isFullyConstrained)
    print('Volume cm3',comp.bRepBodies.item(0).volume)


import adsk.core, adsk.fusion
V=adsk.core.ValueInput.createByString
P=adsk.core.Point3D.create
H=adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation
Y=adsk.fusion.DimensionOrientations.VerticalDimensionOrientation
NEW=adsk.fusion.FeatureOperations.NewBodyFeatureOperation
CUT=adsk.fusion.FeatureOperations.CutFeatureOperation
JOIN=adsk.fusion.FeatureOperations.JoinFeatureOperation
def build_connectors(_context: str):
    app=adsk.core.Application.get()
    d=adsk.fusion.Design.cast(app.activeProduct)
    root=d.rootComponent; comp=root.occurrences.item(0).component
    d.userParameters.itemByName('bridgeThickness').expression='6 mm'
    d.userParameters.itemByName('pilotDepth').expression='4 mm'
    def val(expr): return d.unitsManager.evaluateExpression(expr,'cm')
    def plane(c,expr,name):
        pi=c.constructionPlanes.createInput(); pi.setByOffset(c.xYConstructionPlane,V(expr))
        p=c.constructionPlanes.add(pi); p.name=name; return p
    def circle(c,pl,x,y,diam,name):
        s=c.sketches.add(pl); s.name=name
        circ=s.sketchCurves.sketchCircles.addByCenterRadius(P(val(x),val(y),0),val(diam)/2)
        s.sketchDimensions.addDiameterDimension(circ,P(val(x)+0.5,val(y)+0.5,0)).parameter.expression=diam
        s.sketchDimensions.addDistanceDimension(s.originPoint,circ.centerSketchPoint,H,P(val(x),-1,0)).parameter.expression=x if val(x)>0 else '-('+x+')'
        s.sketchDimensions.addDistanceDimension(s.originPoint,circ.centerSketchPoint,Y,P(-1,val(y),0)).parameter.expression=y if val(y)>0 else '-('+y+')'
        return s
    def ext(c,s,depth,operation,name):
        f=c.features.extrudeFeatures.addSimple(s.profiles.item(0),V(depth),operation); f.name=name; s.isVisible=False; return f
    def pattern(c,features,axis,quantity,name):
        os=adsk.core.ObjectCollection.create()
        for f in features: os.add(f)
        pi=c.features.rectangularPatternFeatures.createInput(os,axis,V(quantity),V('2*pitch'),adsk.fusion.PatternDistanceType.SpacingPatternDistanceType)
        f=c.features.rectangularPatternFeatures.add(pi); f.name=name
    rear=plane(comp,'boardThickness','06 Rear datum')
    for edge,x,y,axis,qty in [
        ('South','pitch/2','pitch/4',comp.xConstructionAxis,'columns/2'),
        ('North','pitch/2','panelHeight-pitch/4',comp.xConstructionAxis,'columns/2'),
        ('West','pitch/4','pitch',comp.yConstructionAxis,'rows/2'),
        ('East','panelWidth-pitch/4','pitch/2',comp.yConstructionAxis,'rows/2')]:
        s=circle(comp,comp.xYConstructionPlane,x,y,'screwClearance','07 '+edge+' visible screw clearance')
        f=ext(comp,s,'boardThickness',CUT,'08 '+edge+' M2 through hole')
        s=circle(comp,rear,x,y,'registerDiameter','09 '+edge+' rear register')
        g=ext(comp,s,'-registerDepth',CUT,'10 '+edge+' locating pocket')
        pattern(comp,[f,g],axis,qty,'11 '+edge+' 40 mm connector rhythm')
    def rect(c,x0,y0,w,h,name,op):
        s=c.sketches.add(c.xYConstructionPlane); s.name=name
        ls=s.sketchCurves.sketchLines.addTwoPointRectangle(P(val(x0),val(y0),0),P(val(x0)+val(w),val(y0)+val(h),0))
        for i,l in enumerate(ls): (s.geometricConstraints.addHorizontal if i%2==0 else s.geometricConstraints.addVertical)(l)
        for point,axis,expr in [(ls[0].startSketchPoint,H,x0),(ls[0].startSketchPoint,Y,y0)]:
            s.sketchDimensions.addDistanceDimension(s.originPoint,point,axis,P(-2,-2,0)).parameter.expression=expr if val(expr)>0 else '-('+expr+')'
        s.sketchDimensions.addDistanceDimension(ls[0].startSketchPoint,ls[0].endSketchPoint,H,P(0,-2,0)).parameter.expression=w
        s.sketchDimensions.addDistanceDimension(ls[1].startSketchPoint,ls[1].endSketchPoint,Y,P(2,0,0)).parameter.expression=h
        return ext(c,s,'bridgeThickness',op,name+' extrusion')
    for name,ztype in [('Bridge H - straight',False),('Bridge V - staggered',True)]:
        matrix=adsk.core.Matrix3D.create(); matrix.translation=adsk.core.Vector3D.create(28,4 if not ztype else 8,0)
        c=root.occurrences.addNewComponent(matrix).component; c.name=name
        if not ztype:
            rect(c,'pitch/2-bridgeWidth/2','-pitch/4-bridgeWidth/2','bridgeWidth','pitch/2+bridgeWidth','12 Straight bridge blank',NEW)
            anchors=[('pitch/2','-pitch/4'),('pitch/2','pitch/4')]
        else:
            rect(c,'-bridgeWidth/2','-pitch/4-bridgeWidth/2','bridgeWidth','pitch/2+bridgeWidth','12 Spine',NEW)
            rect(c,'-pitch/4-bridgeWidth/2','-pitch/4-bridgeWidth/2','pitch/4+bridgeWidth','bridgeWidth','13 Lower arm',JOIN)
            rect(c,'-bridgeWidth/2','pitch/4-bridgeWidth/2','pitch/4+bridgeWidth','bridgeWidth','14 Upper arm',JOIN)
            anchors=[('-pitch/4','-pitch/4'),('pitch/4','pitch/4')]
        front=plane(c,'-pegHeight','15 Peg tip plane')
        for i,(x,y) in enumerate(anchors):
            s=circle(c,c.xYConstructionPlane,x,y,'pegDiameter','16 Registration peg '+str(i+1))
            ext(c,s,'-pegHeight',JOIN,'17 Registration peg')
            s=circle(c,front,x,y,'pilotDiameter','18 M2 pilot '+str(i+1))
            ext(c,s,'pilotDepth+pegHeight',CUT,'19 Blind pilot into bridge')
        c.bRepBodies.item(0).name=name
    d.computeAll()
    for c in d.allComponents:
        for s in c.sketches: print(s.name,'fullyConstrained',s.isFullyConstrained)
    print('Bodies',[(c.name,c.bRepBodies.count) for c in d.allComponents])
    app.activeViewport.fit()


def run(_context: str):
    build_panel(_context)
    build_connectors(_context)

