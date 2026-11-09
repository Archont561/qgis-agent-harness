# The one toolchain: pixi, from the image that ships it, pinned by digest.
#
# The digest is the multi-architecture index for 0.84.1; `docker buildx imagetools inspect
# ghcr.io/prefix-dev/pixi:0.84.1` prints it again if it ever needs checking. Nothing is installed with
# apt, pip or npm afterwards: a second toolchain path is how a container and CI drift apart, and this
# repository has exactly one way to run anything (`pixi run <task>`).
FROM ghcr.io/prefix-dev/pixi:0.84.1@sha256:2d8821a1f3ee11a7fe8055f2c72d2b116d22f00c4caa73809857b5f216fcdebc

ARG USER_NAME=dev
ARG USER_UID=1000
ARG USER_GID=1000

# A non-root account, because a container that runs the harness should not also be able to rewrite the
# toolchain that scores it. `pixi` lives in /usr/local/bin, so it is already on this user's PATH.
RUN groupadd --gid "${USER_GID}" "${USER_NAME}" \
 && useradd --uid "${USER_UID}" --gid "${USER_GID}" --create-home --shell /bin/bash "${USER_NAME}" \
 && mkdir -p /pixi-cache /workspaces \
 && chown -R "${USER_NAME}:${USER_NAME}" /pixi-cache /workspaces

# QGIS is used headless: there is no display in the container, and `QT_QPA_PLATFORM=offscreen` is what
# keeps a PyQGIS import from blocking on one. The cache lives on a named volume, so a rebuild does not
# re-download three gigabytes of environments.
ENV PIXI_CACHE_DIR=/pixi-cache \
    QT_QPA_PLATFORM=offscreen

USER ${USER_NAME}
WORKDIR /workspaces
