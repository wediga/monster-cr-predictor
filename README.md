# Monster CR Predictor

**Predicting D&D 5e Monster Challenge Ratings with Machine Learning**

[Live Demo](https://cr-predictor.yourdomain.de) | [API Docs](https://cr-predictor.yourdomain.de/docs)

---

## Why This Exists

The Challenge Rating (CR) system in Dungeons & Dragons 5th Edition is notoriously inconsistent. A CR 1 creature can be trivial or deadly depending on its stat combination, and the official formula in the Dungeon Master's Guide doesn't capture the complexity of what actually makes a monster dangerous.

As a D&D player and machine learning practitioner, I wanted to answer a straightforward question: **Can a model learn what makes a monster hard, better than the official guidelines?**

This project trains a supervised ML model on 300+ monsters from the D&D 5e SRD to predict Challenge Ratings from stat blocks. Beyond the prediction itself, the feature importance analysis reveals which stats actually drive difficulty - and where the official CR system gets it wrong.

## What It Does

- Fetches monster data from the [D&D 5e SRD API](https://www.dnd5eapi.co)
- Engineers meaningful features from raw stat blocks (damage output, defensive stats, action economy, special abilities)
- Trains and evaluates multiple models (Linear Regression, Random Forest, Gradient Boosting)
- Provides a web interface where you can input custom monster stats and get a predicted CR
- Exposes a REST API for programmatic access

## Try It

### Web Interface

Visit the [live demo](https://cr-predictor.yourdomain.de) to predict the CR of your homebrew monsters.

### API

```bash
curl -X POST https://cr-predictor.yourdomain.de/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "hit_points": 135,
    "armor_class": 18,
    "strength": 23,
    "dexterity": 10,
    "constitution": 21,
    "intelligence": 14,
    "wisdom": 11,
    "charisma": 13,
    "num_actions": 3,
    "num_resistances": 2,
    "num_immunities": 1,
    "has_spellcasting": false,
    "has_legendary_actions": false
  }'
```

### Run Locally

```bash
# Clone and set up
git clone https://github.com/yourusername/monster-cr-predictor.git
cd monster-cr-predictor
uv sync

# Fetch data, train model, start server
uv run python -m cr_predictor.data.fetch
uv run python -m cr_predictor.train
uv run fastapi dev src/cr_predictor/api.py
```

### Docker

```bash
docker compose up
```

The app will be available at `http://localhost:8000`.

## Project Structure

```
monster-cr-predictor/
  src/cr_predictor/
    data/           # Data fetching and processing
    features/       # Feature engineering pipeline
    models/         # Model training and evaluation
    api.py          # FastAPI application
    templates/      # Web UI (Jinja2)
    static/         # CSS/JS
  notebooks/        # EDA and analysis notebooks
  tests/
  trained_model/    # Serialized model (generated)
  pyproject.toml
  Dockerfile
  compose.yaml
```

## Tech Stack

- **Python 3.12** with **uv** for dependency management
- **Scikit-learn** for model training
- **Pandas** for data processing
- **FastAPI** for the API and web server
- **Matplotlib / Seaborn** for analysis visualizations
- **Docker** for deployment

## Key Findings

_This section will be filled after training. Expected content: feature importance ranking, model accuracy (MAE, R2), examples of monsters where the model disagrees with official CR, and what that tells us about the CR system._

## Data Source

All monster data comes from the [D&D 5e SRD API](https://www.dnd5eapi.co), which provides content released under the [Systems Reference Document 5.1](https://dnd.wizards.com/resources/systems-reference-document) (Creative Commons).

## License

MIT
