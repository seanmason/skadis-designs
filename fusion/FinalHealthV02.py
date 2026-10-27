import adsk.core,adsk.fusion,os,json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(_context: str):
    a=adsk.core.Application.get();d=adsk.fusion.Design.cast(a.activeProduct)
    def walk(items):
        for t in items:
            if t.objectType==adsk.fusion.TimelineGroup.classType():yield from walk(t)
            else:yield t
    items=list(walk(d.timeline))
    bad=[(t.name,t.errorOrWarningMessage) for t in items if t.healthState!=adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState]
    loose=[(c.name,s.name) for c in d.allComponents for s in c.sketches if not s.isFullyConstrained]
    report={'document':a.activeDocument.name,'components':d.rootComponent.occurrences.count,'timeline_groups':d.timeline.timelineGroups.count,'checked_timeline_items':len(items),'unconstrained_sketches':loose,'unhealthy_features':bad,'all_components_one_solid':all(o.component.bRepBodies.count==1 and o.component.bRepBodies.item(0).isSolid for o in d.rootComponent.occurrences)}
    with open(os.path.join(ROOT,'docs','final-cad-health-v02.json'),'w') as f:json.dump(report,f,indent=2)
    print(json.dumps(report))
    assert not loose and not bad and report['all_components_one_solid']
