import time
import os

import requests
import json

response = requests.get("https://www.dnd5eapi.co/api/2014/monsters")

monsters = []

for monster in response.json()["results"]:
    time.sleep(0.05)
    detailed_monster = requests.get("https://www.dnd5eapi.co" + monster["url"])
    monsters.append(detailed_monster.json())

os.makedirs("data/raw", exist_ok=True)

with open("data/raw/monsters.json", "w") as f:
    json.dump(monsters, f, indent=2)