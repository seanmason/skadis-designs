"""Migration utility for the first v0.2 build; current generators already select exterior corners."""
import adsk.core, adsk.fusion

def run(_context: str):
    d=adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    for name,left,bottom in [('Panel lower left',True,True),('Panel lower right',False,True),('Panel upper left',True,False),('Panel upper right',False,False)]:
        c=next(o.component for o in d.rootComponent.occurrences if o.component.name==name)
        f=c.features.filletFeatures.item(0)
        f.timelineObject.rollTo(True)
        edges=f.edgeSets.item(0).edges
        coords=[(e,e.boundingBox.minPoint.x,e.boundingBox.minPoint.y) for e in edges]
        xx=(min if left else max)(q[1] for q in coords)
        yy=(min if bottom else max)(q[2] for q in coords)
        chosen=adsk.core.ObjectCollection.create()
        for e,x,y in coords:
            if abs(x-xx)<1e-6 and abs(y-yy)<1e-6:chosen.add(e)
        assert chosen.count==1
        f.edgeSets.item(0).edges=chosen
        f.name='02 Rounded exterior corner'
        d.timeline.moveToEnd()
    print('Exterior corner selections corrected')
