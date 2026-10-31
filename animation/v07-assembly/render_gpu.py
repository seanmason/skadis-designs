import bpy,sys,json,time
from pathlib import Path
args=sys.argv[sys.argv.index('--')+1:]
R=Path(__file__).resolve().parent;s=bpy.context.scene
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
for device in prefs.devices:device.use=device.type=='OPTIX'
assert any(d.use and d.type=='OPTIX' for d in prefs.devices),'No OptiX GPU'
s.cycles.device='GPU';s.cycles.denoiser='OPTIX';s.cycles.denoising_use_gpu=True
s.render.use_persistent_data=False
preview='--preview' in args
out=R/('preview' if preview else 'frames');out.mkdir(exist_ok=True)
if preview:
    frames=[48,170,265,390,510,650,790,925,995,1062,1175,1252,1336,1410]
    s.render.resolution_percentage=50;s.cycles.samples=24
else:
    first=int(args[args.index('--start')+1]);last=int(args[args.index('--end')+1]);frames=range(first,last+1)
times=[]
for f in frames:
    target=out/f'{f:04d}.png'
    if target.exists() and not preview and '--overwrite' not in args:continue
    s.frame_set(f);s.cycles.seed=f;s.render.filepath=str(target)
    t=time.time();bpy.ops.render.render(write_still=True);times.append(time.time()-t)
    progress='preview-progress.json' if preview else 'repair-progress.json' if '--repair' in args else 'render-progress.json'
    (R/progress).write_text(json.dumps({'frame':f,'total':1440,'last_frame_seconds':times[-1],'gpu':[d.name for d in prefs.devices if d.use]}))
if preview:(R/'preview-timings.json').write_text(json.dumps({'frames':frames,'seconds':times},indent=2))
