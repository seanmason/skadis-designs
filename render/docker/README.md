# Ubuntu RTX render worker

Run on the Ubuntu host with a working NVIDIA driver (`nvidia-smi`). `bash setup-host.sh` installs Docker if absent and configures NVIDIA Container Toolkit only if the GPU smoke test fails. The configuration step may restart Docker and interrupt existing containers. It does not install or replace the host GPU driver. Uses the rootful system Docker daemon.

`bash start.sh` builds Blender 4.5.9 with its published SHA-256, then starts an SSH worker on port 2222. It selects VMware vmnet8's host IPv4 address if available; override with `RENDER_BIND_IP=192.168.x.x bash start.sh`. The address must be reachable from the Windows VM. No firewall rules are changed. Password/root login, SSH forwarding and tunnels are disabled. SSH runs as root to handle login; rendering runs as the unprivileged `render` account, without sudo or Docker socket access. No host home directory is mounted. Render data and SSH host keys persist in named Docker volumes.

This session's dedicated SSH public key is installed by the launcher; its private key remains at `C:/Users/mason/.ssh/codex_skadis_render` outside Git. Send the printed endpoint and host-key fingerprint to the chat. We can then verify host identity, upload the self-contained `animation/v05-smooth/smooth.blend` via SFTP/SCP, and benchmark frames 1, 260 and 462 using OptiX before changing the current CPU job. Access can be stopped with `sudo docker stop skadis-render`.

Example inside the container after upload:

```bash
blender --background /work/smooth.blend --python-exit-code 1 \
  --python /opt/gpu_render.py -- --frames 1,260,462 --output /work/benchmark-optix
```

Add `--with-cpu` and use a different output directory to compare mixed CPU/GPU rendering. For a full job, replace `--frames ...` with `--start 1 --end 840`. GPU discovery fails explicitly if OptiX is unavailable. First-frame kernel initialization is included in timings. Runs resume by skipping existing output PNGs; do not reuse output directories after scene changes. Encoding and all-frame validation can run back in the Windows workspace after retrieval.

These files were statically checked in Windows; the image build, Linux libraries, network reachability and GPU access require validation on the Ubuntu host.

Sources: [NVIDIA Container Toolkit setup](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html), [Blender 4.5.9 downloads and checksums](https://download.blender.org/release/Blender4.5/).
