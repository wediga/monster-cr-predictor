import json
import os
import numpy

import pandas as pd

def build_monster():
    os.makedirs("data/processed", exist_ok=True)

    with open('data/raw/monsters.json', "r") as f:
        monsters = json.load(f)

    final_monsters = []

    for monster in monsters:
        transformed_monster = {
            "index": monster["index"],
            "hit_points": numpy.log1p(monster["hit_points"]),
            "strength": monster["strength"],
            "dexterity": monster["dexterity"],
            "constitution": monster["constitution"],
            "intelligence": monster["intelligence"],
            "wisdom": monster["wisdom"],
            "charisma": monster["charisma"],
            "armor_class": monster["armor_class"][0]["value"],
            "num_resistances": len(monster["damage_resistances"]),
            "num_immunities": len(monster["damage_immunities"]),
            "num_actions": len(monster["actions"]),
            "has_legendary_actions": 1 if monster["legendary_actions"] else 0,
            "has_spellcasting": 1 if any(
                "Spellcasting" in a["name"] for a in monster.get("special_abilities", [])) else 0,
            "num_special_abilities": len(monster.get("special_abilities", [])),
            "challenge_rating": monster["challenge_rating"],
        }

        final_monsters.append(transformed_monster)

    df = pd.DataFrame(final_monsters)
    df.to_csv("data/processed/monsters.csv", index=False)


if __name__ == "__main__":
    build_monster()