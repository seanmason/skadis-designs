from pathlib import Path
import shutil,json
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent;repo=R.parents[1]
(R/'assets').mkdir(exist_ok=True);(R/'captions').mkdir(exist_ok=True)
for p in (repo/'models/v05/prototypes').glob('*.stl'):
    if p.name.startswith(('carrier-jig-240--','panel-handling-tool-concept--')) or (p.name.startswith('axial-mosaic-tile--') and 'fit-coupon' not in p.name):
        shutil.copy2(p,R/'assets'/p.name)
shots=[
(0,4,'reveal','Infinite SKÅDIS HD','240 mm panels · 480 mm frame · v0.5 CAD prototype'),
(4,9,'explode','A system of replaceable parts','Printed panels · carriers · fasteners · 2020 frame'),
(9,13,'nuts','Load the rail nuts first','Slide channel nuts through the open extrusion ends.'),
(13,18,'frame','Build and mount the frame','Join the frame with flush wall tabs · hardware is provisional.'),
(18,24,'carriers','Captive nuts. Clear hook space.','Integral spring stops retain M2 nuts · fit-test prototype'),
(24,29,'jig','Align before tightening','The jig locates carriers and leaves M5 access open.'),
(29,37,'panels','Install panels from the front','Four flush M2 screws retain each panel independently.'),
(37,40,'seam','Whole slots across every seam','Stepped edges follow the 10 mm pixel grid.'),
(40,43,'cavity','Room behind the board','10 mm hook cavity between support blades · to be tested'),
(43,47,'tile','Two pixels per tile','Axial push-in retention · fit-test prototype'),
(47,50,'art','Build the artwork one tile at a time','Separate color regions share one printed core.'),
(50,53,'handle','Clear access and engage the handle','Quarter-turn keys support the panel · handling concept'),
(53,57,'service','Service one panel from the front','Remove its screws, then withdraw the panel and artwork.'),
(57,60,'finish','An expandable canvas','Print-test the interfaces before scaling up.')]
data=[]
title=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf',43)
body=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',27)
for a,b,key,t,sub in shots:
    im=Image.new('RGBA',(1920,1080));d=ImageDraw.Draw(im)
    for y in range(850,1080):d.line((0,y,1920,y),fill=(3,8,15,int(205*min(1,(y-850)/110))))
    d.rounded_rectangle((78,925,84,1016),radius=3,fill=(67,206,196,255))
    d.text((106,918),t,font=title,fill=(232,239,245,255))
    d.text((108,978),sub,font=body,fill=(170,190,207,255))
    im.save(R/'captions'/f'{key}.png')
    data.append(dict(start=a*24+1,end=b*24,key=key,title=t,subtitle=sub))
(R/'shots.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
print('Prepared',len(data),'captioned segments and CAD prototype assets')
