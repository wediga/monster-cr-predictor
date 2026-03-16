import json
import joblib
import numpy
import pandas as pd

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from fastapi.staticfiles import StaticFiles

app = FastAPI()

model = joblib.load("trained_model/model.joblib")

with open("trained_model/metadata.json", "r") as f:
    metadata = json.load(f)


class MonsterInput(BaseModel):
    hit_points: int = Field(ge=1, le=1000)
    strength: int = Field(ge=1, le=30)
    dexterity: int = Field(ge=1, le=30)
    constitution: int = Field(ge=1, le=30)
    intelligence: int = Field(ge=1, le=30)
    wisdom: int = Field(ge=1, le=30)
    charisma: int = Field(ge=1, le=30)
    armor_class: int = Field(ge=0, le=30)
    num_resistances: int = Field(ge=0, le=10)
    num_immunities: int = Field(ge=0, le=10)
    num_actions: int = Field(ge=0, le=10)
    has_legendary_actions: bool
    has_spellcasting: bool
    num_special_abilities: int = Field(ge=0, le=10)


app.mount("/static", StaticFiles(directory="src/cr_predictor/static"), name="static")

@app.get("/")
def index():
    return FileResponse("src/cr_predictor/static/index.html")

@app.post("/api/predict")
def predict(monster: MonsterInput):
    monster_dict = monster.model_dump()
    monster_dict["hit_points"] = numpy.log1p(monster_dict["hit_points"])

    monster_dict["has_legendary_actions"] = int(monster_dict["has_legendary_actions"])
    monster_dict["has_spellcasting"] = int(monster_dict["has_spellcasting"])

    df = pd.DataFrame([monster_dict])

    return {"predicted_cr": model.predict(df)[0]}
