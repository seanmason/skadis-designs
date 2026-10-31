"""Retrieve this project's completed GPU frames and produce the captioned MP4."""
from pathlib import Path
import subprocess,json,time,tarfile,sys
R=Path(__file__).resolve().parent;home=Path.home()
ssh=['ssh','-p','2222','-i',str(home/'.ssh/codex_skadis_render'),'-o','UserKnownHostsFile='+str(home/'.ssh/skadis_render_known_hosts'),'-o','StrictHostKeyChecking=yes','-o','BatchMode=yes','-o','ConnectTimeout=10','render@192.168.148.1']
while True:
    r=subprocess.run(ssh+['if test -f /work/skadis-v07/render.exit; then cat /work/skadis-v07/render.exit; else echo running; fi'],capture_output=True,text=True)
    if r.returncode:time.sleep(20);continue
    if r.stdout.strip()!='running':
        assert r.stdout.strip()=='0',r.stdout
        break
    p=subprocess.run(ssh+['cat /work/skadis-v07/render-progress.json'],capture_output=True,text=True)
    if p.returncode==0:
        data=json.loads(p.stdout);(R/'render-progress.json').write_text(json.dumps(data,indent=2));print(data,flush=True)
    time.sleep(30)
archive=R/'frames-transfer.tar'
with archive.open('wb') as out:subprocess.run(ssh+['tar -C /work/skadis-v07/frames -cf - .'],stdout=out,check=True)
target=R/'frames';target.mkdir(exist_ok=True)
with tarfile.open(archive) as tar:
    for member in tar.getmembers():
        assert (target/member.name).resolve().is_relative_to(target.resolve())
        assert member.isfile() or member.isdir()
    tar.extractall(target,filter='data')
archive.unlink()
subprocess.run([sys.executable,str(R/'encode.py')],check=True)
print('GPU ANIMATION COMPLETE',flush=True)
