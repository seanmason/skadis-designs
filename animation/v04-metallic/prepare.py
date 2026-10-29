"""Upgrade the approved review scene; run with v04-review/review.blend."""
import bpy,os,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
s=bpy.context.scene
palette=[('Panel deep teal',(.012,.19,.17)),('Panel midnight blue',(.018,.055,.23)),('Panel warm ivory',(.26,.12,.025)),('Panel copper finish',(.46,.13,.045)),('Panel satin aluminum finish',(.065,.085,.12))]
for name,color in palette:
    p=bpy.data.materials[name].node_tree.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Metallic'].default_value=1
    p.inputs['Roughness'].default_value=.32
for obj in s.objects:
    if obj.animation_data and obj.animation_data.action:
        for fc in obj.animation_data.action.fcurves:
            for k in fc.keyframe_points:
                k.co.x=1+(k.co.x-1)*2
                k.handle_left.x=1+(k.handle_left.x-1)*2
                k.handle_right.x=1+(k.handle_right.x-1)*2
s.render.fps=24;s.frame_end=840
s.render.resolution_x=1920;s.render.resolution_y=1080
s.render.threads_mode='FIXED';s.render.threads=os.cpu_count()
s.cycles.device='CPU';s.cycles.samples=32;s.cycles.adaptive_threshold=.06
s.cycles.use_denoising=True;s.cycles.max_bounces=4
s.render.use_motion_blur=True;s.render.motion_blur_shutter=.25
s.view_settings.exposure=-.7
s.frame_set(1);s.render.filepath='//frames/frame_'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'metallic.blend'),compress=True)
for frame,label in [(1,'assembled'),(481,'whirlwind')]:
    s.frame_set(frame);s.render.filepath=str(ROOT/(label+'.png'));bpy.ops.render.render(write_still=True)
