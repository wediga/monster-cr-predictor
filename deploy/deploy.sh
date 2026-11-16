#!/usr/bin/env bash
# Deploys one commit of the CR Predictor. GitHub Actions runs it over SSH with
# a key whose line in authorized_keys of web forces this script, so the key can
# do nothing else.
#
# The commit SHA arrives as the SSH command. Stdin brings the GITHUB_TOKEN of
# the job on its first line, followed by a tar of deploy/quadlet and this
# script, both from that commit. The token can only read the images of the
# repository and expires with the job.
set -euo pipefail

IMAGE=ghcr.io/wediga/monster-cr-predictor
REGISTRY="${IMAGE%%/*}"
# The unit starts this name, see quadlet/cr-predictor.container.
LOCAL_IMAGE=localhost/cr-predictor:deployed
UNIT=cr-predictor.container
SERVICE=cr-predictor.service
APP_DIR="$HOME/cr-predictor"
# The units of wediga-dev live here as well, so only this app's unit is
# replaced.
UNIT_DIR="$HOME/.config/containers/systemd"

sha="${SSH_ORIGINAL_COMMAND:-}"

if [[ ! "$sha" =~ ^[0-9a-f]{40}$ ]]; then
  echo "expected a commit SHA, got '$sha'" >&2

  exit 1
fi

# A forced command gets no login session, and systemctl --user needs this.
XDG_RUNTIME_DIR="/run/user/$(id -u)"
export XDG_RUNTIME_DIR

IFS= read -r token
work="$(mktemp -d)"
trap 'rm -rf "$work"; podman logout "$REGISTRY" >/dev/null 2>&1 || true' EXIT
tar -x -C "$work"

# Empty on the first deploy, when there is no previous image yet.
previous="$(podman image inspect --format '{{.Id}}' "$LOCAL_IMAGE" 2>/dev/null || true)"
printf '%s' "$token" | podman login "$REGISTRY" --username token --password-stdin >/dev/null
podman pull --quiet "$IMAGE:$sha" >/dev/null
podman logout "$REGISTRY" >/dev/null
podman tag "$IMAGE:$sha" "$LOCAL_IMAGE"
# Without the second argument, untag would drop the local name as well.
podman untag "$IMAGE:$sha" "$IMAGE:$sha"

mkdir -p "$UNIT_DIR"
cp "$work/quadlet/$UNIT" "$UNIT_DIR/"
systemctl --user daemon-reload
systemctl --user restart "$SERVICE"

current="$(podman image inspect --format '{{.Id}}' "$LOCAL_IMAGE")"

if [ -n "$previous" ] && [ "$previous" != "$current" ]; then
  podman rmi "$previous" >/dev/null
fi

# Replaced last and by renaming, because bash keeps reading this file while it
# runs and must not see the new version halfway.
install -m 700 "$work/deploy.sh" "$APP_DIR/.deploy.sh.new"
mv "$APP_DIR/.deploy.sh.new" "$APP_DIR/deploy.sh"
