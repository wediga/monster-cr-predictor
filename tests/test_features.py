from cr_predictor.features.engineering import build_monster

import pandas as pd


def test_processed_csv_has_expected_columns():
    build_monster()

    df = pd.read_csv("data/processed/monsters.csv")

    expected_columns = [
        "index", "hit_points", "strength", "dexterity", "constitution",
        "intelligence", "wisdom", "charisma", "armor_class",
        "num_resistances", "num_immunities", "num_actions",
        "has_legendary_actions", "has_spellcasting",
        "num_special_abilities", "challenge_rating",
    ]

    assert list(df.columns) == expected_columns


def test_processed_csv_has_no_missing_values():
    df = pd.read_csv("data/processed/monsters.csv")

    assert df.isnull().sum().sum() == 0


def test_boolean_features_are_binary():
    df = pd.read_csv("data/processed/monsters.csv")

    assert set(df["has_legendary_actions"].unique()).issubset({0, 1})
    assert set(df["has_spellcasting"].unique()).issubset({0, 1})
