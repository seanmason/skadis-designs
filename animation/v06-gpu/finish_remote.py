"""Wait for the remote render, retrieve frames, then encode and validate locally."""
from pathlib import Path
import subprocess,time,json,tarfile,sys
R=Path(__file__).resolve().parent
home=Path.home()
common=['-i',str(home/'.ssh/codex_skadis_render'),'-o','UserKnownHostsFile='+str(home/'.ssh/skadis_render_known_hosts'),'-o','StrictHostKeyChecking=yes','-o','BatchMode=yes','-o','ConnectTimeout=10']
ssh=['ssh',*common,'-p','2222','render@192.168.148.1']
while True:
    r=subprocess.run(ssh+['if test -f /work/full-gpu.exit; then cat /work/full-gpu.exit; else echo running; fi'],capture_output=True,text=True)
    if r.returncode:time.sleep(20);continue
    state=r.stdout.strip()
    if state!='running':
        if state!='0':raise RuntimeError('Remote GPU render failed: '+state)
        break
    progress=subprocess.run(ssh+['cat /work/full-gpu/progress.json'],capture_output=True,text=True)
    if progress.returncode==0:
        data=json.loads(progress.stdout);(R/'render-progress.json').write_text(json.dumps(data,indent=2))
    time.sleep(20)
archive=R/'frames-transfer.tar'
with archive.open('wb') as out:
    subprocess.run(ssh+['tar -C /work/full-gpu -cf - .'],stdout=out,check=True)
frames=R/'frames';frames.mkdir(exist_ok=True)
with tarfile.open(archive) as t:
    for member in t.getmembers():
        target=(frames/member.name).resolve()
        assert target.is_relative_to(frames.resolve()),member.name
        assert member.isfile() or member.isdir(),member.name
    t.extractall(frames,filter='data')
archive.unlink()
subprocess.run([sys.executable,str(R/'encode.py')],check=True)
print('GPU DELIVERY COMPLETE',flush=True)
