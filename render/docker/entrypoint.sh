#!/bin/bash
set -euo pipefail
test -s /run/render-authorized-key
install -o root -g root -m 644 /run/render-authorized-key /etc/ssh/authorized_keys/render
if [ ! -f /etc/ssh/keys/ssh_host_ed25519_key ]; then
    ssh-keygen -q -t ed25519 -N '' -f /etc/ssh/keys/ssh_host_ed25519_key
fi
chown render:render /work
mkdir -p /run/sshd
/usr/sbin/sshd -t
exec /usr/sbin/sshd -D -e
