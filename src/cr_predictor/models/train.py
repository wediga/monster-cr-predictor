import pandas as pd
import joblib
import json
import os

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

def load_data(path):
    df = pd.read_csv(path)

    x = df.drop(columns=["challenge_rating", "index"])
    y = df["challenge_rating"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    return {
        "x_train": x_train,
        "y_train": y_train,
        "x_test": x_test,
        "y_test": y_test,
    }


def train_and_evaluate(model, training_data):
    model.fit(training_data["x_train"], training_data["y_train"])
    prediction = model.predict(training_data["x_test"])
    mae = mean_absolute_error(training_data["y_test"], prediction)
    r2 = r2_score(training_data["y_test"], prediction)

    print(model.__class__.__name__)
    print(f"MAE: {mae:.2f}")
    print(f"R2: {r2:.2f}")
    print("-------------------------------------------------------")

    return model, mae, r2


def evaluate_best_model(result_lr, result_rf, result_gb):
    results = [result_lr, result_rf, result_gb]

    candidates = [r for r in results if hasattr(r[0], "feature_importances_")]

    best_model = min(candidates, key=lambda r: r[1])

    return best_model


def save_model(model_tuple, training_data):
    model, mae, r2 = model_tuple
    feature_names = training_data["x_train"].columns.tolist()
    importances = model.feature_importances_
    model_name = model.__class__.__name__

    os.makedirs("trained_model", exist_ok=True)

    joblib.dump(model, "trained_model/model.joblib")

    metadata = {
        "model": model_name,
        "mae": mae,
        "r2": r2,
        "features": feature_names,
        "feature_importances": dict(zip(feature_names, importances.tolist())),
    }

    with open("trained_model/metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"{model_name} saved")


if __name__ == "__main__":
    training_data = load_data("data/processed/monsters.csv")
    result_lr = train_and_evaluate(LinearRegression(), training_data)
    result_rf = train_and_evaluate(RandomForestRegressor(random_state=42), training_data)
    result_gb = train_and_evaluate(GradientBoostingRegressor(random_state=42), training_data)

    best_model = evaluate_best_model(result_lr, result_rf, result_gb)

    print(f"best Model: {best_model[0].__class__.__name__}")

    save_model(result_gb, training_data)
