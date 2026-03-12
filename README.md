# Monster CR Predictor

**Predicting D&D 5e Monster Challenge Ratings with Machine Learning**

[Live Demo](https://cr-prediction.wediga.dev) | [API Docs](https://cr-prediction.wediga.dev/docs)

---

## Why This Exists

I wanted a portfolio project that's not another TODO app or Titanic dataset. D&D felt like a good fit because the data is freely available, the domain is fun, and the CR system has always bugged me as a player. Some CR 1 monsters are a joke, others will wipe a level 1 party. So: can a model figure out what actually makes a monster dangerous?

Turns out, it mostly can. And the answer is surprisingly boring: **Hit Points. That's basically it.**

## What It Does

Takes monster stats from the [D&D 5e SRD API](https://www.dnd5eapi.co) (334 monsters), engineers 14 features from them, and trains three regression models to predict CR. The best model gets saved and served through a FastAPI web app where you can punch in your own monster stats.

## Key Findings

### Model Performance

| Model | MAE | R² |
|-------|-----|-----|
| Linear Regression | 0.94 | 0.96 |
| **Random Forest** | **0.82** | **0.95** |
| Gradient Boosting | 0.86 | 0.96 |

I went with Random Forest. Not because it has the best R², but because it gives you `feature_importances_` out of the box, which was the whole point for me. I wanted to see *why* a monster gets its CR, not just predict a number.

### Feature Importance

| Feature | Importance |
|---------|-----------|
| Hit Points | 85.9% |
| Constitution | 3.3% |
| Charisma | 2.4% |
| Armor Class | 2.2% |
| Legendary Actions | 2.1% |
| Intelligence | 1.0% |
| Actions | 0.6% |
| Wisdom | 0.5% |
| Special Abilities | 0.5% |
| Strength | 0.5% |
| Dexterity | 0.3% |
| Immunities | 0.3% |
| Resistances | 0.2% |
| Spellcasting | 0.2% |

HP dominates everything at 86%. The EDA already hinted at this (correlation of 0.94 with CR), but seeing it confirmed through the model was still funny. Dexterity, which feels so important when you're actually playing, does essentially nothing for CR. Armor Class barely matters. It's all about how long the monster stays alive, not how hard it is to hit.

## Try It

### Web Interface

Visit the [live demo](https://cr-prediction.wediga.dev) to predict the CR of your homebrew monsters.

### API

```bash
curl -X POST https://cr-prediction.wediga.dev/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "hit_points": 256,
    "armor_class": 19,
    "strength": 27,
    "dexterity": 10,
    "constitution": 25,
    "intelligence": 16,
    "wisdom": 13,
    "charisma": 21,
    "num_actions": 3,
    "num_resistances": 0,
    "num_immunities": 1,
    "num_special_abilities": 1,
    "has_spellcasting": false,
    "has_legendary_actions": true
  }'
```

### Run Locally

```bash
git clone https://github.com/wediga/monster-cr-predictor.git
cd monster-cr-predictor
chmod +x setup.sh
./setup.sh
```

This fetches the data, builds features, trains the model, and starts the app in Docker at `http://localhost:8000`.

### Docker Only

If data and model are already present:

```bash
docker compose up --build
```

## Project Structure

```
monster-cr-predictor/
  src/cr_predictor/
    data/           # Data fetching from D&D 5e API
    features/       # Feature engineering pipeline
    models/         # Model training and selection
    static/         # Web UI (HTML/CSS/JS)
    api.py          # FastAPI application
  notebooks/        # EDA and analysis
  tests/            # API, feature and model tests
  trained_model/    # Serialized model (generated)
  setup.sh          # Full pipeline setup script
  Dockerfile
  compose.yaml
```

## Tech Stack

- **Python 3.12** with **uv** for dependency management
- **Scikit-learn** for model training
- **Pandas** for data processing
- **FastAPI** for the API and web server
- **Docker** for containerization and deployment

## Data Source

All monster data comes from the [D&D 5e SRD API](https://www.dnd5eapi.co), which provides content released under the [Systems Reference Document 5.1](https://dnd.wizards.com/resources/systems-reference-document) (Creative Commons).

## License

MIT
