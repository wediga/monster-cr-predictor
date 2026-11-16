# Running it on the server

The app runs on ax41 as a rootless Podman container under the user `web`, started by systemd through the Quadlet unit in `quadlet/`. Caddy reaches it over the network of wediga.dev and, once Caddy has moved to the repository `NuviraLabs/polaris`, over port 8103 on `127.0.0.1`.

The commands in this file run as `web`. After `ssh ax41` and `sudo -iu web`, run `export XDG_RUNTIME_DIR=/run/user/$(id -u)` once, because `sudo` does not set it and `systemctl --user` cannot reach the user's systemd without it.

## Layout

| What | Where on the server |
|---|---|
| Quadlet unit (`quadlet/cr-predictor.container`) | `~/.config/containers/systemd/` |
| Deploy script (`deploy.sh`) | `~/cr-predictor/deploy.sh` |

The units of wediga-dev live in the same folder, so the deploy replaces only this one file.

## What a deploy does

Every push to `main` runs `.github/workflows/ci.yml`. It tests the app, builds the image and fails if Trivy finds a HIGH or CRITICAL vulnerability with a fix. Only a push sends the image to GHCR as `ghcr.io/wediga/monster-cr-predictor:<sha>`, and every version older than the newest five is deleted there. A pull request runs the same build and scan without pushing.

Once every job has passed, the deploy job connects as `web` with a key that may only run `~/cr-predictor/deploy.sh`. It sends the commit SHA as the command, and on stdin its own `GITHUB_TOKEN` followed by a tar of `quadlet/` and `deploy.sh` from that commit. The script

1. pulls the image of the commit with the token, which expires with the job, and tags it `localhost/cr-predictor:deployed`,
2. replaces the unit and restarts `cr-predictor.service`,
3. deletes the image that was running before and replaces itself with the version from the commit.

The unit starts `localhost/cr-predictor:deployed` with `Pull=never`, so a restart after a reboot uses the image of the last deploy and nothing is fetched from GitHub at boot. The site is gone for a few seconds while the container restarts. The secrets of the deploy live in the GitHub environment `production`, which only runs of `main` may use.

## First setup

Create the folder and install the deploy script from the commit that should run first:

```
mkdir -p ~/cr-predictor && chmod 700 ~/cr-predictor
curl -fsSL https://raw.githubusercontent.com/wediga/monster-cr-predictor/<sha>/deploy/deploy.sh -o /tmp/deploy.sh
install -m 700 /tmp/deploy.sh ~/cr-predictor/deploy.sh && rm /tmp/deploy.sh
```

Every later deploy replaces it on its own. Append the public deploy key to `~/.ssh/authorized_keys` with the forced command in front, and keep the file at 600, because sshd ignores a file others can write to:

```
echo 'restrict,command="/home/web/cr-predictor/deploy.sh" ssh-ed25519 AAAA... github-actions-cr-predictor' >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

The environment `production` holds the private key as the secret `DEPLOY_SSH_KEY`, the output of `ssh-keyscan` for the server as the secret `DEPLOY_KNOWN_HOSTS` and the address `web@<server>` as the variable `DEPLOY_TARGET`.
