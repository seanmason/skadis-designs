"""Parametric flush-wall frame; measured-profile approximation, not rated hardware.
Run build_base, then add_nodes, add_joint_pair for each bay/end, add_wall_tabs.
All scripts operate on their own new v0.3 document. Existing documents are preserved.
"""
import adsk.core,adsk.fusion,os,runpy,json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M=runpy.run_path(os.path.join(ROOT,'fusion','FrameSystemV02.py'))
V,P,NEW,CUT,JOIN=M['V'],M['P'],M['NEW'],M['CUT'],M['JOIN']

class Builder(M['Builder']):
    def health(self):
        report=super().health()
        report['timeline_features']=sum(1 for _ in M['timeline_items'](self.d.timeline))
        report['timeline_groups']=self.d.timeline.timelineGroups.count
        return report
    def __init__(self,name='Infinite SKADIS HD v0.3 - flush wall assembly',columns=6,rows=6):
        super().__init__(name,columns,rows)
        self.d.userParameters.itemByName('capThickness').expression='5 mm'
        for n,e,c in [
            ('profileMouth','6.28 mm','User measured mouth'),
            ('profileCavity','11 mm','User measured widest cavity'),
            ('profileDepth','6.2 mm','User measured face-to-floor depth'),
            ('profileFloor','5.7 mm','User estimate, lower confidence'),
            ('profileLip','1.5 mm','Unmeasured; tentative comparable catalog value'),
            ('profileTaperStart','profileDepth-(profileCavity-profileFloor)/2','Assumed 45-degree inner slopes'),
            ('profileBore','5 mm','Unmeasured central bore, reference only'),
            ('nutWidth','8.8 mm','Provisional low-profile METAL T-nut envelope, not old rectangular carrier'),
            ('nutLength','12 mm','End-loaded anti-rotation metal nut envelope'),
            ('nutThickness','2.7 mm','Thin nut reference; fit/load still unverified'),
            ('jointLeg','18 mm','In-bay angle footprint'),
            ('jointThickness','3 mm','Metal bracket thickness'),
            ('jointDepth','16 mm','Bracket depth within 20 mm rail'),
            ('sideScrewLength','8 mm','M5x8 reference; check against actual bracket and nut'),
            ('registerPin','2 mm','Node-seat locating pins'),
            ('registerSocket','2.4 mm','Starting printed locating clearance'),
            ('registerPinHeight','0.8 mm','Pin into rear socket'),
            ('registerSocketDepth','1 mm','Blind panel socket'),
            ('registerOffset','5 mm','Four pegs at node +/- offset'),
            ('wallTabHeight','24 mm','Tab along extrusion'),
            ('wallTabReach','22 mm','Tab into open bay'),
            ('wallAnchorClearance','6.5 mm','Placeholder wall anchor interface'),
            ('wallShim','0 mm','Only actual leveling shims; no designed rear air gap'),
            ('wallDriverDiameter','12 mm','Clear tool envelope in open bays'),
            ('keyDriverDiameter','5 mm','Short hex-key working-leg envelope'),
            ('keyDriverReach','20 mm','Short hex-key working-leg reach'),
        ]:self.d.userParameters.add(n,V(e),'mm',c)
    def comp(self,name):
        c=super().comp(name)
        with open(os.path.join(ROOT,'docs','v03-build-progress.json'),'w') as f:json.dump({'latest_component':name,'components':self.root.occurrences.count},f)
        return c
    def circle(self,c,x,y,dia,z,name):
        s=c.sketches.add(self.plane(c,z));s.name=name;s.isComputeDeferred=True
        q=s.sketchCurves.sketchCircles.addByCenterRadius(P(self.value(x),self.value(y),0),self.value(dia)/2)
        if abs(self.value(x))+abs(self.value(y))<1e-8:s.geometricConstraints.addCoincident(q.centerSketchPoint,s.originPoint)
        else:self.locate(s,q.centerSketchPoint,x,y)
        s.sketchDimensions.addDiameterDimension(q,P(self.value(x)+1,self.value(y)+1,0)).parameter.expression=dia
        s.isComputeDeferred=False
        return s
    def ext(self,c,s,depth,op,name):
        i=c.features.extrudeFeatures.createInput(s.profiles.item(0),op)
        i.setDistanceExtent(False,V(depth))
        if op==CUT:i.participantBodies=list(c.bRepBodies)
        f=c.features.extrudeFeatures.add(i);f.name=name;s.isVisible=False
        return f
    def axis_sketch(self,c,axis,station,name):
        base={'x':c.yZConstructionPlane,'y':c.xZConstructionPlane,'z':c.xYConstructionPlane}[axis]
        sign=getattr(base.geometry.normal,axis)
        pi=c.constructionPlanes.createInput();pi.setByOffset(base,V('('+station+')*'+str(sign)))
        pl=c.constructionPlanes.add(pi);pl.name=name+' datum';pl.isLightBulbOn=False
        s=c.sketches.add(pl);s.name=name
        origin=s.sketchToModelSpace(P(0,0,0))
        axes=[]
        for point in [P(1,0,0),P(0,1,0)]:
            q=s.sketchToModelSpace(point)
            vec=[getattr(q,k)-getattr(origin,k) for k in ('x','y','z')]
            i=max(range(3),key=lambda j:abs(vec[j]));axes.append((i,round(vec[i])))
        return s,sign,axes
    def poly3(self,c,axis,station,vertices,depth,op,name):
        s,sign,axes=self.axis_sketch(c,axis,station,name+' sketch')
        pts=[];coordinates=[{},{}]
        for xyz in vertices:
            pt=s.sketchPoints.add(s.modelToSketchSpace(P(*[self.value(e) for e in xyz])))
            u,v=['('+xyz[i]+')*'+str(sg) for i,sg in axes]
            for k,expr in enumerate([u,v]):
                if expr in coordinates[k]:
                    (s.geometricConstraints.addVerticalPoints if k==0 else s.geometricConstraints.addHorizontalPoints)(coordinates[k][expr],pt)
                elif abs(self.value(expr))<1e-8:
                    (s.geometricConstraints.addVerticalPoints if k==0 else s.geometricConstraints.addHorizontalPoints)(s.originPoint,pt)
                else:
                    s.sketchDimensions.addDistanceDimension(s.originPoint,pt,M['H'] if k==0 else M['Y'],P(-3-len(pts),-3-len(pts),0)).parameter.expression='abs('+expr+')'
                coordinates[k][expr]=pt
            pts.append(pt)
        for i,pt in enumerate(pts):s.sketchCurves.sketchLines.addByTwoPoints(pt,pts[(i+1)%len(pts)])
        return self.ext(c,s,'('+depth+')*'+str(sign),op,name)
    def disk3(self,c,axis,station,xyz,dia,depth,op,name):
        s,sign,axes=self.axis_sketch(c,axis,station,name+' sketch')
        q=s.sketchCurves.sketchCircles.addByCenterRadius(s.modelToSketchSpace(P(*[self.value(e) for e in xyz])),self.value(dia)/2)
        u,v=['('+xyz[i]+')*'+str(sg) for i,sg in axes]
        self.locate(s,q.centerSketchPoint,u,v)
        s.sketchDimensions.addDiameterDimension(q,P(2,2,0)).parameter.expression=dia
        return self.ext(c,s,'('+depth+')*'+str(sign),op,name)
    def panel(self,name,ox='0 mm',oy='0 mm',edges=(0,0,0,0),prefix='panel'):
        c=super().panel(name,ox,oy,edges,prefix)
        # Old loose bridge sockets are superseded by node registration.
        for f in list(c.features.extrudeFeatures):
            if f.name.startswith('09 Blind rear key socket'):f.deleteMe()
        l,r,bt,t=[prefix+s for s in ('Left','Right','Bottom','Top')]
        for x in ['('+ox+')+mountInset*'+l,'('+ox+')+panelWidth-mountInset*'+r]:
            for y in ['('+oy+')+mountInset*'+bt,'('+oy+')+panelHeight-mountInset*'+t]:
                for dx in [-1,1]:
                    for dy in [-1,1]:
                        xx=x+'+('+str(dx)+')*registerOffset';yy=y+'+('+str(dy)+')*registerOffset'
                        if self.value(ox)<self.value(xx)<self.value('('+ox+')+panelWidth') and self.value(oy)<self.value(yy)<self.value('('+oy+')+panelHeight'):
                            self.disk(c,xx,yy,'registerSocket','boardThickness','-registerSocketDepth','10 Node register socket',CUT)
        return c
    def rail(self,name,axis,start,length,center):
        c=self.comp(name+' - measured sloped-slot approximation')
        def xyz(u,v):return [u,start,v] if axis=='y' else [start,u,v]
        u0='('+center+')-10 mm';u1='('+center+')+10 mm'
        self.poly3(c,axis,start,[xyz(u0,'frameZ'),xyz(u1,'frameZ'),xyz(u1,'frameZ+20 mm'),xyz(u0,'frameZ+20 mm')],length,NEW,'Profile blank')
        section=[('-profileMouth/2','0 mm'),('-profileMouth/2','profileLip'),('-profileCavity/2','profileLip'),('-profileCavity/2','profileTaperStart'),('-profileFloor/2','profileDepth'),('profileFloor/2','profileDepth'),('profileCavity/2','profileTaperStart'),('profileCavity/2','profileLip'),('profileMouth/2','profileLip'),('profileMouth/2','0 mm')]
        for side in range(4):
            points=[]
            for u,v in section:
                if side==0:uu='('+center+')+('+u+')';vv='frameZ+('+v+')'
                elif side==1:uu='('+center+')+10 mm-('+v+')';vv='frameZ+10 mm+('+u+')'
                elif side==2:uu='('+center+')-('+u+')';vv='frameZ+20 mm-('+v+')'
                else:uu='('+center+')-10 mm+('+v+')';vv='frameZ+10 mm-('+u+')'
                points.append(xyz(uu,vv))
            self.poly3(c,axis,start,points,length,CUT,'Sloped T channel '+str(side))
        self.disk3(c,axis,start,xyz(center,'frameZ+10 mm'),'profileBore',length,CUT,'Reference center bore')
        return c
    def node(self,label,x,y):
        cap=self.comp('METAL cap '+label)
        self.disk(cap,x,y,'capDiameter','-capThickness','capThickness','Visible cap')
        self.disk(cap,x,y,'screwClearance','-capThickness','capThickness','M5 clearance',CUT)
        seat=self.comp('PRINT registration seat '+label)
        self.disk(seat,x,y,'capDiameter','boardThickness','seatThickness','Rear bearing seat')
        self.disk(seat,x,y,'mountBore','boardThickness','seatThickness','Shoulder clearance',CUT)
        for dx in [-1,1]:
            for dy in [-1,1]:self.disk(seat,x+'+('+str(dx)+')*registerOffset',y+'+('+str(dy)+')*registerOffset','registerPin','boardThickness','-registerPinHeight','Forward registration peg',JOIN)
        spacer=self.comp('METAL stepped compression spacer '+label)
        self.disk(spacer,x,y,'8 mm','0 mm','boardThickness+seatThickness','8 mm shoulder')
        self.disk(spacer,x,y,'12 mm','boardThickness+seatThickness','hookClearance-seatThickness','12 mm base',JOIN)
        self.disk(spacer,x,y,'screwClearance','0 mm','frameZ','Through bore',CUT)
        bolt=self.comp('REFERENCE front M5x25 '+label)
        self.disk(bolt,x,y,'9.5 mm','-capThickness-3 mm','3 mm','Button head envelope')
        self.disk(bolt,x,y,'5 mm','-capThickness','frameZ+capThickness+5 mm','Shank envelope',JOIN)
        nut=self.comp('REFERENCE thin METAL channel nut front '+label)
        self.box(nut,x+'-nutWidth/2',y+'-nutLength/2','nutWidth','nutLength','frameZ+profileLip','nutThickness','Thin nut envelope')
        self.disk(nut,x,y,'5.2 mm','frameZ+profileLip','nutThickness','Thread envelope',CUT)
        return cap,seat,spacer,bolt,nut
    def side_hardware(self,label,axis,face,along,n):
        sg=str(n);zc='frameZ+10 mm';base='('+face+')+('+sg+')*jointThickness'
        def xyz(a):return [a,along,zc] if axis=='x' else [along,a,zc]
        screw=self.comp('REFERENCE side M5x8 '+label)
        self.disk3(screw,axis,base,xyz(base),'9.5 mm','('+sg+')*3 mm',NEW,'Button head envelope')
        self.disk3(screw,axis,base,xyz(base),'5 mm','-('+sg+')*sideScrewLength',JOIN,'Shank envelope')
        nut=self.comp('REFERENCE thin METAL channel nut side '+label)
        mn='('+face+')-profileLip-nutThickness' if n>0 else '('+face+')+profileLip'
        if axis=='x':self.box(nut,mn,along+'-nutLength/2','nutThickness','nutLength','frameZ+10 mm-nutWidth/2','nutWidth','Thin nut envelope')
        else:self.box(nut,along+'-nutLength/2',mn,'nutLength','nutThickness','frameZ+10 mm-nutWidth/2','nutWidth','Thin nut envelope')
        self.disk3(nut,axis,mn,xyz(mn),'5.2 mm','nutThickness',CUT,'Thread envelope')
        return screw,nut
    def joint(self,label,xface,yface,sx,sy):
        c=self.comp('METAL in-bay corner '+label)
        x='('+xface+')';y='('+yface+')'
        xx=x if sx>0 else x+'-jointThickness';yy=y if sy>0 else y+'-jointLeg'
        self.box(c,xx,yy,'jointThickness','jointLeg','frameZ+2 mm','jointDepth','Vertical bracket leg')
        xx=x if sx>0 else x+'-jointLeg';yy=y if sy>0 else y+'-jointThickness'
        self.box(c,xx,yy,'jointLeg','jointThickness','frameZ+2 mm','jointDepth','Horizontal bracket leg',JOIN)
        by=y+'+('+str(sy)+')*12 mm';bx=x+'+('+str(sx)+')*12 mm'
        self.disk3(c,'x',x,[x,by,'frameZ+10 mm'],'5.5 mm',str(sx)+'*jointThickness',CUT,'Vertical rail bolt')
        self.disk3(c,'y',y,[bx,y,'frameZ+10 mm'],'5.5 mm',str(sy)+'*jointThickness',CUT,'Tie bolt')
        self.side_hardware(label+' X','x',x,by,sx)
        self.side_hardware(label+' Y','y',y,bx,sy)
    def wall_tab(self,label,xface,y,n):
        c=self.comp('METAL flush wall tab '+label)
        x='('+xface+')';sg=str(n)
        x0=x if n>0 else x+'-jointThickness'
        self.box(c,x0,y+'-wallTabHeight/2','jointThickness','wallTabHeight','frameZ','20 mm','Side attachment leg')
        x0=x if n>0 else x+'-wallTabReach'
        self.box(c,x0,y+'-wallTabHeight/2','wallTabReach','wallTabHeight','frameZ+20 mm-jointThickness','jointThickness','Flush wall foot',JOIN)
        for k,dy in enumerate([-6,6]):
            yy=y+'+('+str(dy)+' mm)'
            self.disk3(c,'x',x,[x,yy,'frameZ+10 mm'],'5.5 mm',sg+'*jointThickness',CUT,'Side fixing')
            self.side_hardware('wall '+label+str(k),'x',x,yy,n)
        ax=x+'+('+sg+')*13 mm'
        self.disk(c,ax,y,'wallAnchorClearance','frameZ+20 mm-jointThickness','jointThickness','Wall anchor clearance',CUT)
        a=self.comp('REFERENCE wall anchor HEAD ONLY '+label)
        self.disk(a,ax,y,'12 mm','frameZ+20 mm-jointThickness-3 mm','3 mm','Anchor head envelope')
        self.disk(a,ax,y,'6 mm','frameZ+20 mm-jointThickness','jointThickness','Clearance shank only - anchor not selected',JOIN)

def active():
    b=Builder.__new__(Builder);b.app=adsk.core.Application.get();b.doc=b.app.activeDocument
    assert b.doc.name=='Infinite SKADIS HD v0.3 - flush wall assembly',b.doc.name
    b.d=adsk.fusion.Design.cast(b.app.activeProduct);b.root=b.d.rootComponent
    return b

def build_base(_context):
    b=Builder()
    for name,x,y,edges,prefix in [('Panel lower left','0 mm','0 mm',(1,0,1,0),'ll'),('Panel lower right','panelWidth','0 mm',(0,1,1,0),'lr'),('Panel upper left','0 mm','panelHeight',(1,0,0,1),'ul'),('Panel upper right','panelWidth','panelHeight',(0,1,0,1),'ur')]:b.panel(name,x,y,edges,prefix)
    xs=['mountInset','panelWidth','2*panelWidth-mountInset']
    for i,x in enumerate(xs):b.rail('Vertical rail '+str(i),'y','mountInset-10 mm','2*panelHeight-2*mountInset+20 mm',x)
    for j,y in enumerate(['mountInset','2*panelHeight-mountInset']):
        for i in range(2):b.rail('Horizontal tie '+str(i)+str(j),'x',xs[i]+'+10 mm',xs[i+1]+'-('+xs[i]+')-20 mm',y)
    print('Base',b.health())

def add_nodes(_context):
    b=active()
    for i,x in enumerate(['mountInset','panelWidth','2*panelWidth-mountInset']):
        for j,y in enumerate(['mountInset','panelHeight','2*panelHeight-mountInset']):b.node(str(i)+str(j),x,y)
    print('Nodes',b.health())

def add_joint_pair(i,j):
    b=active();xs=['mountInset','panelWidth','2*panelWidth-mountInset']
    y='mountInset+10 mm' if j==0 else '2*panelHeight-mountInset-10 mm';sy=1 if j==0 else -1
    b.joint(str(i)+str(j)+'L',xs[i]+'+10 mm',y,1,sy)
    b.joint(str(i)+str(j)+'R',xs[i+1]+'-10 mm',y,-1,sy)
    print('Joint pair',i,j,'complete')

def add_wall_tabs(_context):
    b=active()
    for i,(x,n) in enumerate([('mountInset+10 mm',1),('2*panelWidth-mountInset-10 mm',-1)]):
        for j,y in enumerate(['2*panelHeight/3','4*panelHeight/3']):b.wall_tab(str(i)+str(j),x,y,n)
    print('Wall tabs',b.health())

def run(_context: str):
    build_base(_context);add_nodes(_context)
    for j in range(2):
        for i in range(2):add_joint_pair(i,j)
    add_wall_tabs(_context)
