FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl xz-utils openssh-server python3 libx11-6 libxi6 \
    libxrender1 libxfixes3 libxkbcommon0 libsm6 libgl1 libegl1 libglib2.0-0t64 \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fL --retry 3 https://download.blender.org/release/Blender4.5/blender-4.5.9-linux-x64.tar.xz -o /tmp/blender.tar.xz \
    && echo 'dcdc3eca6c9825bb35a8033b689c053f3cb5a9b0cd2a61b2eac2a49436b4ad3d  /tmp/blender.tar.xz' | sha256sum -c - \
    && mkdir /opt/blender && tar -xJf /tmp/blender.tar.xz -C /opt/blender --strip-components=1 \
    && rm /tmp/blender.tar.xz && ln -s /opt/blender/blender /usr/local/bin/blender
RUN useradd -m -s /bin/bash render && usermod --password '*' render \
    && mkdir -p /etc/ssh/keys /etc/ssh/authorized_keys /run/sshd /work
COPY sshd_config /etc/ssh/sshd_config
COPY entrypoint.sh /usr/local/bin/render-entrypoint
COPY gpu_render.py /opt/gpu_render.py
RUN chmod 755 /usr/local/bin/render-entrypoint
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility,graphics
EXPOSE 22
ENTRYPOINT ["/usr/local/bin/render-entrypoint"]
