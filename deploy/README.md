# Running it on the server

The app runs on ax41 as a rootless Podman container under the user `web`, started by systemd through the Quadlet unit in `quadlet/`. Caddy reaches it over the network of wediga.dev and, once Caddy has moved to the repository `NuviraLabs/polaris`, over port 8103 on `127.0.0.1`.

There is no automatic deploy yet. A new version is built on the server from the checkout in `~/monster-cr-predictor` and started by hand, as `web`:

```
export XDG_RUNTIME_DIR=/run/user/$(id -u)
cd ~/monster-cr-predictor
git pull
podman build -t localhost/cr-predictor:latest .
cp deploy/quadlet/cr-predictor.container ~/.config/containers/systemd/
systemctl --user daemon-reload
systemctl --user restart cr-predictor.service
```

The site is gone for a few seconds while the container restarts.
