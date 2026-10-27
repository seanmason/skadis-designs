"""Metal wall interface concept. Anchor selection and load rating remain site-specific."""
import adsk.core,adsk.fusion,os,runpy
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(_context: str):
    m=runpy.run_path(os.path.join(ROOT,'fusion','FrameSystemV02.py'))
    b=m['Builder'].__new__(m['Builder']);b.app=adsk.core.Application.get();b.doc=b.app.activeDocument
    b.d=adsk.fusion.Design.cast(b.app.activeProduct);b.root=b.d.rootComponent
    b.d.userParameters.add('wallGap',m['V']('10 mm'),'mm','Frame rear to wall plane; metal bracket clearance, site-specific')
    b.d.userParameters.add('wallAnchorClearance',m['V']('6.5 mm'),'mm','Placeholder anchor shank clearance; select for actual wall')
    for i,x in enumerate(['mountInset','2*panelWidth-mountInset']):
        for j,y in enumerate(['panelHeight/2','3*panelHeight/2']):
            c=b.comp('METAL wall standoff '+str(i)+str(j)+' - welded or machined')
            b.box(c,x+'-10 mm',y+'-15 mm','20 mm','30 mm','frameZ+20 mm','3 mm','Rail pad')
            # Inward-facing foot stays behind the panel silhouette.
            web=x+'+7 mm' if i==0 else x+'-10 mm'
            foot=x+'+7 mm' if i==0 else x+'-32 mm'
            anchor=x+'+22 mm' if i==0 else x+'-22 mm'
            b.box(c,web,y+'-15 mm','3 mm','30 mm','frameZ+23 mm','wallGap-6 mm','Standoff web',m['JOIN'])
            b.box(c,foot,y+'-15 mm','25 mm','30 mm','frameZ+20 mm+wallGap-3 mm','3 mm','Wall foot',m['JOIN'])
            b.disk(c,anchor,y,'wallAnchorClearance','frameZ+20 mm+wallGap-3 mm','3 mm','Wall anchor interface',m['CUT'])
            for k,yy in enumerate([y+'-8 mm',y+'+8 mm']):
                b.disk(c,x,yy,'5.5 mm','frameZ+20 mm','3 mm','Rail attachment clearance',m['CUT'])
                screw=b.comp('REFERENCE wall bracket M5x8 '+str(i)+str(j)+str(k))
                b.disk(screw,x,yy,'9.5 mm','frameZ+23 mm','3 mm','Head')
                b.disk(screw,x,yy,'5 mm','frameZ+23 mm','-8 mm','Shank',m['JOIN'])
                nut=b.comp('REFERENCE wall bracket T nut '+str(i)+str(j)+str(k))
                b.box(nut,x+'-4.8 mm',yy+'-4.8 mm','9.6 mm','9.6 mm','frameZ+14 mm','4 mm','Nut')
                b.disk(nut,x,yy,'5.2 mm','frameZ+14 mm','4 mm','Thread envelope',m['CUT'])
    print(b.health())
