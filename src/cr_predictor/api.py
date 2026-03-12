import json
import joblib
import pandas as pd

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

app = FastAPI()

model = joblib.load("trained_model/model.joblib")

with open("trained_model/metadata.json", "r") as f:
    metadata = json.load(f)


class MonsterInput(BaseModel):
    hit_points: int
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int
    armor_class: int
    num_resistances: int
    num_immunities: int
    num_actions: int
    has_legendary_actions: bool
    has_spellcasting: bool
    num_special_abilities: int


app.mount("/static", StaticFiles(directory="src/cr_predictor/static"), name="static")

@app.get("/")
def index():
    return FileResponse("src/cr_predictor/static/index.html")

@app.post("/api/predict")
def predict(monster: MonsterInput):
    monster_dict = monster.model_dump()

    monster_dict["has_legendary_actions"] = int(monster_dict["has_legendary_actions"])
    monster_dict["has_spellcasting"] = int(monster_dict["has_spellcasting"])

    df = pd.DataFrame([monster_dict])

    return {"predicted_cr": model.predict(df)[0]}
