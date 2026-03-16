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
| Linear Regression | 1.33 | 0.91 |
| Random Forest | 0.83 | 0.95 |
| **Gradient Boosting** | **0.87** | **0.96** |

Random Forest actually had the best MAE, but I went with Gradient Boosting. [Here's why.](#why-gradient-boosting)

### Feature Importance

| Feature | Importance |
|---------|-----------|
| Hit Points | 84.2% |
| Constitution | 4.5% |
| Armor Class | 3.0% |
| Charisma | 2.5% |
| Legendary Actions | 2.0% |
| Intelligence | 1.9% |
| Actions | 0.6% |
| Wisdom | 0.3% |
| Immunities | 0.3% |
| Strength | 0.2% |
| Dexterity | 0.2% |
| Spellcasting | 0.1% |
| Special Abilities | 0.1% |
| Resistances | 0.05% |

HP dominates everything at 84%. The EDA already hinted at this (correlation of 0.94 with CR), but seeing it confirmed through the model was still funny. Dexterity, which feels so important when you're actually playing, does essentially nothing for CR. Armor Class barely matters. It's all about how long the monster stays alive, not how hard it is to hit.

### Why Gradient Boosting

I originally shipped Random Forest. Then I cranked HP to 100,000 on a default stat block and got... CR 15.6. Same prediction as HP 676. Same as HP 1,000. It just flatlines.

Makes sense once you think about it. A Random Forest averages training data in leaf nodes. Extreme inputs all land in the same leaves, so you get the same output no matter how far you go. The model can't predict anything it hasn't seen.

Gradient Boosting isn't magic either, but it builds trees on residuals (the errors of previous trees), so it at least degrades more gracefully at the edges. The MAE is marginally worse (0.87 vs 0.83), but the predictions don't just hit a wall.

Two more things I changed along the way: HP gets a `log1p` transform before training, because the raw distribution is wild (most monsters have 5-100 HP, the Tarrasque sits at 676). And all inputs are capped to D&D-realistic ranges (HP 0-1000, ability scores 1-30, etc.) so you can't feed the model values it has no business predicting.

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
