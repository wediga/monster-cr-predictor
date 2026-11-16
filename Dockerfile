# Image for the CR Predictor. The build stage installs the dependencies with
# uv and trains the model, the runtime stage only gets what serving needs.
# Both base images are pinned to the same digests as the wediga.dev backend.

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim@sha256:e5b65587bce7de595f299855d7385fe7fca39b8a74baa261ba1b7147afa78e58 AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1 \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Dependencies first and without the project itself, so this layer stays
# cached as long as the lockfile does not change.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

COPY pyproject.toml uv.lock ./
COPY src/ ./src/
COPY data/raw/monsters.json ./data/raw/monsters.json
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# The training is seeded, so every build produces the same model.
RUN .venv/bin/python src/cr_predictor/features/engineering.py \
    && .venv/bin/python src/cr_predictor/models/train.py

FROM python:3.12-slim-bookworm@sha256:392307d22300de8b5986851a12d9176dfc0fc073e65bf6523ebd7dcbeb23564e AS runtime

# Apply the Debian security updates published since the base image was built.
RUN apt-get update \
    && apt-get upgrade -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# The app runs from the virtualenv built by uv, so the base image's pip is
# never used and would only add its own vulnerabilities.
RUN pip uninstall -y pip

RUN groupadd --gid 999 nonroot \
    && useradd --uid 999 --gid 999 --no-create-home nonroot

WORKDIR /app

# The app opens the model and the static files by paths relative to /app and
# never writes, so the root filesystem can be read-only.
COPY --from=builder /app/.venv ./.venv
COPY --from=builder /app/src ./src
COPY --from=builder /app/trained_model ./trained_model

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

USER nonroot

EXPOSE 8000

CMD ["uvicorn", "cr_predictor.api:app", "--host", "0.0.0.0", "--port", "8000"]
