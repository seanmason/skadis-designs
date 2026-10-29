# RTX 3080 delivery

Full, consistent OptiX render of the corrected v0.5 `smooth.blend` on the Ubuntu host's RTX 3080 10 GB, using Blender 4.5.9. All 840 frames use GPU rendering and GPU-accelerated denoising; settings remain 1080p, 24 fps, 32 samples and the corrected camera. Prior CPU frames are retained separately. The unrelated SK2 render is not stopped.

The container SSH identity was checked against the host key supplied by the user. Dedicated credentials and pinned known_hosts live outside Git under the Windows user's `.ssh` directory. Endpoint: `render@192.168.148.1:2222`.

Measured benchmark results on frames 1, 260, 462:

| Mode | First frame | Frame 260 | Frame 462 |
|---|---:|---:|---:|
| OptiX, CPU denoising, competing CPU render active | 8.68 s | 6.51 s | 6.28 s |
| OptiX, GPU denoising, this project's CPU job stopped | 1.63 s | 0.95 s | 0.97 s |
| OptiX + CPU, GPU denoising | 2.39 s | 1.06 s | 1.31 s |

The first comparison changes two factors, so the improvement cannot be attributed solely to GPU denoising. GPU-only was selected over combined rendering. First frames include startup overhead. These are measured scene timings, not extrapolated hardware benchmark scores.

`remote_render.sh` runs in the container independently of SSH and records its exit status. `finish_remote.py` waits locally, retrieves the completed PNG sequence to `frames/`, and runs `encode.py`. That script checks all decoded frames for black frames and isolated brightness spikes, then publishes `infinite-skadis-gpu.mp4`. Final visual review is still required. Progress and log files are ignored by Git; benchmark results are retained.
