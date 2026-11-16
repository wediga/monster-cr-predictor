"""The unit publishes the app only on loopback and runs it on a read-only filesystem."""

from pathlib import Path

UNIT = Path(__file__).resolve().parents[1] / "deploy/quadlet/cr-predictor.container"
# The port polaris assigns, so its Caddy reaches the app on the server's
# loopback address.
PUBLISHED_PORT = "PublishPort=127.0.0.1:8103:8000"


def unit_lines() -> list[str]:
    return UNIT.read_text(encoding="utf-8").splitlines()


def test_app_is_published_only_on_loopback() -> None:
    published = [line for line in unit_lines() if line.startswith("PublishPort=")]

    assert published == [PUBLISHED_PORT]


def test_root_filesystem_is_read_only() -> None:
    assert "ReadOnly=true" in unit_lines()
