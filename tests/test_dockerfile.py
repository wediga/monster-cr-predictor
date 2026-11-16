"""The image is built from pinned base images and runs as a non-root user without uv."""

from pathlib import Path

DOCKERFILE = Path(__file__).resolve().parents[1] / "Dockerfile"
DIGEST_MARKER = "@sha256:"
COPY_FROM = "--from="
ROOT_USERS = {"root", "0"}


def instructions() -> list[tuple[str, str]]:
    lines = DOCKERFILE.read_text(encoding="utf-8").splitlines()

    return [
        (keyword.upper(), rest.strip())
        for keyword, _, rest in (line.strip().partition(" ") for line in lines)
        if keyword and not keyword.startswith("#")
    ]


def final_stage() -> list[tuple[str, str]]:
    steps = instructions()
    last_from = max(i for i, (keyword, _) in enumerate(steps) if keyword == "FROM")

    return steps[last_from + 1 :]


def test_every_base_image_is_pinned_to_a_digest() -> None:
    steps = instructions()
    from_args = [args.split() for keyword, args in steps if keyword == "FROM"]
    stages = {words[-1] for words in from_args if len(words) == 3}
    copied_from = [
        word.removeprefix(COPY_FROM)
        for keyword, args in steps
        if keyword == "COPY"
        for word in args.split()
        if word.startswith(COPY_FROM)
    ]
    images = [words[0] for words in from_args]
    images += [source for source in copied_from if source not in stages]

    assert images
    assert all(DIGEST_MARKER in image for image in images), images


def test_app_runs_as_a_non_root_user() -> None:
    users = [args for keyword, args in final_stage() if keyword == "USER"]

    assert users
    assert users[-1].split(":")[0] not in ROOT_USERS


def test_app_starts_without_uv() -> None:
    commands = [args for keyword, args in final_stage() if keyword == "CMD"]

    assert commands
    assert '"uv"' not in commands[-1]
