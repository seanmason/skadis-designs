#!/bin/sh
set -eu
cd /work/skadis-v07
trap 'echo $? > render.exit' EXIT
for start in $(seq 1 96 1440); do
    end=$((start + 95))
    blender --background assembly.blend --python-exit-code 1 --python render_gpu.py -- --start "$start" --end "$end" > "chunk-$start.log" 2>&1
done
