#!/bin/bash
# Run on the Ubuntu HOST, not inside the Windows VM or container.
set -euo pipefail
command -v nvidia-smi >/dev/null || { echo 'Install the Ubuntu NVIDIA driver first, then rerun.'; exit 1; }
nvidia-smi
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
if ! command -v docker >/dev/null; then sudo apt-get install -y docker.io; fi
sudo systemctl start docker
if sudo docker run --rm --gpus all ubuntu:24.04 nvidia-smi; then
    echo 'Docker GPU access already works; runtime setup skipped.'
    exit 0
fi
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor --yes -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -fsSL https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list |
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' |
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list >/dev/null
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
echo 'Restarting Docker to enable the NVIDIA runtime (may interrupt other containers).'
sudo systemctl restart docker
sudo docker run --rm --gpus all ubuntu:24.04 nvidia-smi
