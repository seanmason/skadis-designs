#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
BIND_IP=${RENDER_BIND_IP:-$(ip -4 -o addr show dev vmnet8 2>/dev/null | awk '{split($4,a,"/"); print a[1]; exit}' || true)}
if [ -z "$BIND_IP" ]; then
    ip -4 -o addr show
    read -rp 'Ubuntu host IPv4 address reachable from the Windows VM: ' BIND_IP
fi
python3 - "$BIND_IP" <<'PY'
import ipaddress,sys
ip=ipaddress.IPv4Address(sys.argv[1])
assert not ip.is_unspecified and not ip.is_loopback, 'Choose a host interface reachable from the VM'
PY
if sudo docker container inspect skadis-render >/dev/null 2>&1; then
    echo 'Container skadis-render already exists. Inspect with: sudo docker ps -a --filter name=skadis-render'
    exit 1
fi
sudo docker build -t skadis-render:blender-4.5.9 .
# Public key only; its dedicated private key stays in the Windows VM.
AUTH_FILE="$PWD/authorized_keys"
printf '%s\n' 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKpwINXcoz98KF5KZn+RtA6kVSWUCHahPkws7N810r7u codex-skadis-render' > "$AUTH_FILE"
chmod 644 "$AUTH_FILE"
sudo docker run -d --name skadis-render --restart unless-stopped \
    --gpus all -e NVIDIA_DRIVER_CAPABILITIES=compute,utility,graphics \
    --shm-size=2g --security-opt no-new-privileges:true \
    -p "$BIND_IP:2222:22" \
    --mount type=volume,source=skadis-render-work,target=/work \
    --mount type=volume,source=skadis-render-hostkeys,target=/etc/ssh/keys \
    --mount "type=bind,source=$AUTH_FILE,target=/run/render-authorized-key,readonly" \
    skadis-render:blender-4.5.9
for attempt in $(seq 1 30); do
    if sudo docker exec skadis-render test -f /etc/ssh/keys/ssh_host_ed25519_key.pub; then break; fi
    sleep 1
done
sudo docker exec skadis-render /usr/sbin/sshd -t
sudo docker exec --user render skadis-render nvidia-smi
echo "SSH endpoint: render@$BIND_IP port 2222"
echo 'Send this endpoint and the following host-key fingerprint back to the chat:'
sudo docker exec skadis-render ssh-keygen -lf /etc/ssh/keys/ssh_host_ed25519_key.pub
echo 'Public host key:'
sudo docker exec skadis-render cat /etc/ssh/keys/ssh_host_ed25519_key.pub
