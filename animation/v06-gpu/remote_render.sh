#!/bin/sh
blender --background /work/smooth.blend --python-exit-code 1 --python /work/gpu_render.py -- --start 1 --end 840 --output /work/full-gpu
status=$?
printf '%s\n' "$status" > /work/full-gpu.exit
exit "$status"
