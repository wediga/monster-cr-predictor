FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./

RUN uv sync --no-dev --frozen

COPY src/ ./src/
COPY data/raw/monsters.json ./data/raw/monsters.json

RUN uv run python src/cr_predictor/features/engineering.py
RUN uv run python src/cr_predictor/models/train.py

CMD ["uv", "run", "uvicorn", "cr_predictor.api:app", "--host", "0.0.0.0", "--port", "8000"]