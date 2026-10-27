import adsk.core, adsk.fusion, os, math, json
P=adsk.core.Point3D.create
V=adsk.core.ValueInput.createByString
def run(_context: str):
    app=adsk.core.Application.get()
    folder=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    doc=app.importManager.importToNewDocument(app.importManager.createFusionArchiveImportOptions(os.path.join(folder,'models','infinite-skadis-hd-v01.f3d')))
    doc.name='HD pegboard - fixed 80 mm coupon assembly'
    d=adsk.fusion.Design.cast(app.activeProduct)
    d.userParameters.itemByName('columns').expression='4'
    d.userParameters.itemByName('rows').expression='4'
    root=d.rootComponent
    panel=next(o.component for o in root.occurrences if o.component.name.startswith('Panel'))
    hc=next(o.component for o in root.occurrences if o.component.name.startswith('Bridge H'))
    vc=next(o.component for o in root.occurrences if o.component.name.startswith('Bridge V'))
    for o in root.occurrences:
        if o.component!=panel: o.isLightBulbOn=False
    def instance(c,x,y,z):
        m=adsk.core.Matrix3D.create();m.translation=adsk.core.Vector3D.create(x,y,z)
        o=root.occurrences.addExistingComponent(c,m); return o
    for x,y in [(8,0),(0,8),(8,8)]: instance(panel,x,y,0)
    screwcenters=[]
    for x in [0,4,8,12]:
        instance(hc,x,8,0.5)
        screwcenters.extend([(x+1,7.5),(x+1,8.5)])
    for y in [1.5,5.5,9.5,13.5]:
        instance(vc,8,y,0.5)
        screwcenters.extend([(7.5,y-0.5),(8.5,y+0.5)])
    # A nominal hardware reference, excluded from printable part exports.
    screw=root.occurrences.addNewComponent(adsk.core.Matrix3D.create()).component
    screw.name='REFERENCE ONLY - M2x8 socket screw'
    sk=screw.sketches.add(screw.xYConstructionPlane)
    circ=sk.sketchCurves.sketchCircles.addByCenterRadius(P(0,0,0),0.19)
    circ.isFixed=True
    head=screw.features.extrudeFeatures.addSimple(sk.profiles.item(0),V('-2 mm'),adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    sk.isVisible=False
    sk=screw.sketches.add(screw.xYConstructionPlane)
    circ=sk.sketchCurves.sketchCircles.addByCenterRadius(P(0,0,0),0.1);circ.isFixed=True
    screw.features.extrudeFeatures.addSimple(sk.profiles.item(0),V('8 mm'),adsk.fusion.FeatureOperations.JoinFeatureOperation)
    sk.isVisible=False
    pi=screw.constructionPlanes.createInput();pi.setByOffset(screw.xYConstructionPlane,V('-2 mm'))
    pl=screw.constructionPlanes.add(pi)
    sk=screw.sketches.add(pl); sk.name='Nominal 1.5 mm socket - visual reference'
    pts=[P(0.15/math.sqrt(3)*math.cos(i*math.pi/3),0.15/math.sqrt(3)*math.sin(i*math.pi/3),0) for i in range(6)]
    for i in range(6):
        line=sk.sketchCurves.sketchLines.addByTwoPoints(pts[i],pts[(i+1)%6]);line.isFixed=True
    screw.features.extrudeFeatures.addSimple(sk.profiles.item(0),V('1 mm'),adsk.fusion.FeatureOperations.CutFeatureOperation);sk.isVisible=False
    # Contrasting hardware appearance copied from its existing appearance.
    body=screw.bRepBodies.item(0)
    appearance=d.appearances.addByCopy(body.appearance,'Dark socket screws - reference')
    colors=[p for p in appearance.appearanceProperties if p.objectType==adsk.core.ColorProperty.classType()]
    if colors: colors[0].value=adsk.core.Color.create(35,40,45,255)
    body.appearance=appearance
    root.occurrences.item(root.occurrences.count-1).isLightBulbOn=False
    for x,y in screwcenters: instance(screw,x,y,0)
    for o in root.occurrences:
        o.isLightBulbOn=not (o.name.endswith(':1') and not o.name.startswith('Panel'))
    d.computeAll()
    for i in range(d.timeline.count):
        t=d.timeline.item(i)
        assert t.healthState==adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState,(t.name,t.errorOrWarningMessage)
    assert d.exportManager.execute(d.exportManager.createFusionArchiveExportOptions(os.path.join(folder,'models','coupon-assembly-2x2-fixed80.f3d')))
    cam=app.activeViewport.camera
    cam.isPerspective=False
    cam.eye=P(8,-10,-24);cam.target=P(8,8,0);cam.upVector=adsk.core.Vector3D.create(0,1,0)
    cam.isFitView=True;app.activeViewport.camera=cam;app.activeViewport.refresh()
    app.activeViewport.saveAsImageFile(os.path.join(folder,'previews','assembly-front.png'),1600,1200)
    cam=app.activeViewport.camera;cam.eye=P(8,-10,26);cam.target=P(8,8,0);cam.upVector=adsk.core.Vector3D.create(0,1,0);cam.isFitView=True
    app.activeViewport.camera=cam;app.activeViewport.refresh()
    app.activeViewport.saveAsImageFile(os.path.join(folder,'previews','assembly-rear.png'),1600,1200)
    print('Assembly saved: four 80 mm panels, eight bridges, sixteen nominal screw references. Fixed layout: resize the master, not this demonstration.')

