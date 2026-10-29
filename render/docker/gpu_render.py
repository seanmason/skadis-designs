"""Blender --background scene.blend --python /opt/gpu_render.py -- --frames 1,260,462 --output /work/benchmark"""
import argparse,bpy,json,os,sys,time
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--frames',default='1,260,462')
p.add_argument('--start',type=int);p.add_argument('--end',type=int)
p.add_argument('--output',default='/work/benchmark')
p.add_argument('--with-cpu',action='store_true')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
prefs=bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type='OPTIX';prefs.get_devices()
gpus=[d for d in prefs.devices if d.type=='OPTIX']
if not gpus:raise RuntimeError('No OptiX GPU detected; refusing silent CPU fallback')
for d in prefs.devices:d.use=(d.type=='OPTIX' or (a.with_cpu and d.type=='CPU'))
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='GPU'
if hasattr(s.cycles,'denoising_use_gpu'):s.cycles.denoising_use_gpu=True
s.render.threads_mode='AUTO'
out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
frames=range(a.start,a.end+1) if a.start is not None and a.end is not None else [int(f) for f in a.frames.split(',')]
results=[]
for f in frames:
    dest=out/f'{f:04d}.png'
    if dest.exists():continue
    s.frame_set(f);s.render.filepath=str(dest);t=time.monotonic()
    bpy.ops.render.render(write_still=True)
    results.append({'frame':f,'seconds':time.monotonic()-t})
    (out/'progress.json').write_text(json.dumps({'devices':[{'name':d.name,'type':d.type} for d in prefs.devices if d.use],'results_this_run':results,'last_completed':f},indent=2))
print('GPU_RENDER_COMPLETE',json.dumps(results),flush=True)
