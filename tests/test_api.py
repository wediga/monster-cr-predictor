from fastapi.testclient import TestClient

from cr_predictor.api import app

client = TestClient(app)


def test_predict_returns_cr():
    response = client.post("/api/predict", json={
        "hit_points": 50,
        "strength": 10,
        "dexterity": 10,
        "constitution": 10,
        "intelligence": 10,
        "wisdom": 10,
        "charisma": 10,
        "armor_class": 13,
        "num_resistances": 0,
        "num_immunities": 0,
        "num_actions": 1,
        "has_legendary_actions": False,
        "has_spellcasting": False,
        "num_special_abilities": 0,
    })

    assert response.status_code == 200
    assert "predicted_cr" in response.json()


def test_predict_cr_is_a_number():
    response = client.post("/api/predict", json={
        "hit_points": 256,
        "strength": 27,
        "dexterity": 10,
        "constitution": 25,
        "intelligence": 16,
        "wisdom": 13,
        "charisma": 21,
        "armor_class": 19,
        "num_resistances": 0,
        "num_immunities": 1,
        "num_actions": 3,
        "has_legendary_actions": True,
        "has_spellcasting": False,
        "num_special_abilities": 1,
    })

    cr = response.json()["predicted_cr"]
    assert isinstance(cr, (int, float))
    assert cr >= 0


def test_predict_rejects_missing_fields():
    response = client.post("/api/predict", json={
        "hit_points": 50,
    })

    assert response.status_code == 422


def test_index_serves_html():
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
