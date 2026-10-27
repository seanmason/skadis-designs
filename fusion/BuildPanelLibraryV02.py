"""Generate a selected native panel configuration, with independently finished sides.
Edit EDGES and NAME, then run inside Fusion. 0=internal, 1=finished.
Use this generator to change edge topology; resize the resulting native F3D
with columns/rows. Assembly boundary flags should not be changed independently.
"""
import os, runpy
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDGES=(0,0,0,0)  # left, right, bottom, top
NAME='interior'
COLUMNS=12
ROWS=12

def run(_context: str):
    m=runpy.run_path(os.path.join(ROOT,'fusion','FrameSystemV02.py'))
    b=m['Builder']('SKADIS v0.2 panel - '+NAME,COLUMNS,ROWS)
    c=b.panel('Panel '+NAME,edges=EDGES)
    print(b.health())
    b.export('panel-'+NAME+'-v02',[(c,'panel-'+NAME+'-'+str(COLUMNS*20)+'x'+str(ROWS*20))])
