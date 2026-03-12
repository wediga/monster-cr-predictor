#!/bin/bash

uv sync

uv run python src/cr_predictor/data/fetch.py

uv run python src/cr_predictor/features/engineering.py

uv run python src/cr_predictor/models/train.py

docker compose up -d --build