"""The CI, the deploy script and the unit name the same images."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/ci.yml"
DEPLOY_SCRIPT = ROOT / "deploy/deploy.sh"
UNIT = ROOT / "deploy/quadlet/cr-predictor.container"


def value(path: Path, pattern: str) -> str:
    match = re.search(pattern, path.read_text(encoding="utf-8"), re.MULTILINE)

    assert match, f"{pattern} not found in {path.name}"

    return match.group(1)


def test_deploy_pulls_the_image_the_ci_pushes() -> None:
    pushed = value(WORKFLOW, r"^  IMAGE: (\S+)$")
    pulled = value(DEPLOY_SCRIPT, r"^IMAGE=(\S+)$")

    assert pulled == pushed


def test_unit_starts_the_image_the_deploy_tags() -> None:
    tagged = value(DEPLOY_SCRIPT, r"^LOCAL_IMAGE=(\S+)$")
    started = value(UNIT, r"^Image=(\S+)$")

    assert started == tagged
