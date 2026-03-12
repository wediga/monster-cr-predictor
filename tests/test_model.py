from cr_predictor.models.train import load_data, train_and_evaluate, evaluate_best_model

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor


def test_load_data_returns_correct_splits():
    data = load_data("data/processed/monsters.csv")

    assert "x_train" in data
    assert "x_test" in data
    assert "y_train" in data
    assert "y_test" in data
    assert len(data["x_train"]) > len(data["x_test"])


def test_load_data_excludes_target_and_index():
    data = load_data("data/processed/monsters.csv")

    assert "challenge_rating" not in data["x_train"].columns
    assert "index" not in data["x_train"].columns


def test_model_has_14_features():
    data = load_data("data/processed/monsters.csv")

    assert data["x_train"].shape[1] == 14


def test_evaluate_best_model_picks_model_with_feature_importances():
    data = load_data("data/processed/monsters.csv")

    result_lr = train_and_evaluate(LinearRegression(), data)
    result_rf = train_and_evaluate(RandomForestRegressor(random_state=42), data)
    result_gb = train_and_evaluate(GradientBoostingRegressor(random_state=42), data)

    best = evaluate_best_model(result_lr, result_rf, result_gb)

    assert hasattr(best[0], "feature_importances_")
