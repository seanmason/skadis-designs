"""Add rear slot envelopes and metal frame splice plates to the active v0.2 assembly."""
import adsk.core, adsk.fusion, os, runpy
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(_context: str):
    m=runpy.run_path(os.path.join(ROOT,'fusion','FrameSystemV02.py'))
    b=m['Builder'].__new__(m['Builder'])
    b.app=adsk.core.Application.get();b.doc=b.app.activeDocument
    b.d=adsk.fusion.Design.cast(b.app.activeProduct);b.root=b.d.rootComponent
    assert 'v0.2' in b.doc.name
    # Match the front simplified slot at the rear, for metal join plates.
    xs=['mountInset','panelWidth','2*panelWidth-mountInset']
    ys=['mountInset','2*panelHeight-mountInset']
    for i,x in enumerate(xs):
        c=next(o.component for o in b.root.occurrences if o.component.name.startswith('Vertical rail '+str(i)))
        b.box(c,x+'-3 mm','mountInset-10 mm','6 mm','2*panelHeight-2*mountInset+20 mm','frameZ+20 mm','-1.8 mm','Rear slot mouth',m['CUT'])
        b.box(c,x+'-5 mm','mountInset-10 mm','10 mm','2*panelHeight-2*mountInset+20 mm','frameZ+18.2 mm','-4.2 mm','Rear T nut cavity',m['CUT'])
    for j,y in enumerate(ys):
        for i in range(2):
            c=next(o.component for o in b.root.occurrences if o.component.name.startswith('Horizontal tie '+str(i)+str(j)))
            w=xs[i+1]+'-('+xs[i]+')-20 mm'
            b.box(c,xs[i]+'+10 mm',y+'-3 mm',w,'6 mm','frameZ+20 mm','-1.8 mm','Rear slot mouth',m['CUT'])
            b.box(c,xs[i]+'+10 mm',y+'-5 mm',w,'10 mm','frameZ+18.2 mm','-4.2 mm','Rear T nut cavity',m['CUT'])
        for i,x in enumerate(xs):
            offsets=([0,20] if i==0 else ([-20,0] if i==2 else [-20,0,20]))
            plate=b.comp('METAL rear splice plate '+str(i)+str(j))
            b.box(plate,x+'+('+str(offsets[0]-8)+' mm)',y+'-8 mm',str(offsets[-1]-offsets[0]+16)+' mm','16 mm','frameZ+20 mm','3 mm','Rear rail join plate')
            for k,offset in enumerate(offsets):
                xx=x+'+('+str(offset)+' mm)'
                b.disk(plate,xx,y,'5.5 mm','frameZ+20 mm','3 mm','M5 clearance',m['CUT'])
                screw=b.comp('REFERENCE rear join screw '+str(i)+str(j)+str(k))
                b.disk(screw,xx,y,'9.5 mm','frameZ+23 mm','3 mm','Nominal head')
                b.disk(screw,xx,y,'5 mm','frameZ+23 mm','-8 mm','M5x8 nominal shank',m['JOIN'])
                nut=b.comp('REFERENCE rear T nut '+str(i)+str(j)+str(k))
                b.box(nut,xx+'-4.8 mm',y+'-4.8 mm','9.6 mm','9.6 mm','frameZ+14 mm','4 mm','T nut envelope')
                b.disk(nut,xx,y,'5.2 mm','frameZ+14 mm','4 mm','Thread envelope',m['CUT'])
    print(b.health())
    ex=b.d.exportManager
    assert ex.execute(ex.createFusionArchiveExportOptions(os.path.join(ROOT,'models','v02','frame-assembly-v02.f3d')))
