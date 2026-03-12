FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./

RUN uv sync --no-dev --frozen

COPY src/ ./src/
COPY trained_model/ ./trained_model/

CMD ["uv", "run", "uvicorn", "cr_predictor.api:app", "--host", "0.0.0.0", "--port", "8000"]