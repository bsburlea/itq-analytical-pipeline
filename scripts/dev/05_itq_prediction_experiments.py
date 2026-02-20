import pandas as pd
import numpy as np
import json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import (
    r2_score, mean_squared_error, mean_absolute_error,
    roc_auc_score, accuracy_score, f1_score
)

# =========================
# Configuration
# =========================

RANDOM_STATE = 42
DATA_DIR = "data/"
TEST_SIZE = 0.2

# =========================
# Utilities
# =========================

def load_data():
    X = pd.read_csv(f"{DATA_DIR}/X.csv")
    y = pd.read_csv(f"{DATA_DIR}/y.csv").iloc[:, 0]
    return X, y

def rmse(y_true, y_pred):
    mse = mean_squared_error(y_true, y_pred)
    return np.sqrt(mse)

# =========================
# Regression
# =========================

def run_regression_models(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    results = {}
    tuning_results = {}

    # ---- Ridge ----
    ridge = Ridge(alpha=1.0)
    ridge.fit(X_train, y_train)
    y_pred = ridge.predict(X_test)

    results["ridge"] = {
        "r2": r2_score(y_test, y_pred),
        "rmse": rmse(y_test, y_pred),
        "mae": mean_absolute_error(y_test, y_pred),
        "y_true": y_test.tolist(),
        "y_pred": y_pred.tolist()
    }

    # ---- Random Forest baseline ----
    rf = RandomForestRegressor(
        n_estimators=300,
        random_state=RANDOM_STATE
    )
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)

    results["rf_baseline"] = {
        "r2": r2_score(y_test, y_pred),
        "rmse": rmse(y_test, y_pred),
        "mae": mean_absolute_error(y_test, y_pred),
        "y_true": y_test.tolist(),
        "y_pred": y_pred.tolist()
    }

    # ---- Random Forest tuning ----
    rf_configs = [
        {"max_depth": None, "min_samples_leaf": 1},
        {"max_depth": 20,   "min_samples_leaf": 1},
        {"max_depth": 10,   "min_samples_leaf": 3},
    ]

    for cfg in rf_configs:
        rf = RandomForestRegressor(
            n_estimators=300,
            random_state=RANDOM_STATE,
            **cfg
        )
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_test)

        key = f"rf_{cfg}"
        tuning_results[key] = {
            "r2": r2_score(y_test, y_pred),
            "rmse": rmse(y_test, y_pred),
            "mae": mean_absolute_error(y_test, y_pred),
            "y_true": y_test.tolist(),
            "y_pred": y_pred.tolist()
        }

    return results, tuning_results

# =========================
# Classification
# =========================

def run_classification_models(X, y):
    y_bin = (y > y.median()).astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_bin, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    results = {}
    tuning_results = {}

    # ---- Logistic ----
    logit = LogisticRegression(max_iter=2000)
    logit.fit(X_train, y_train)
    y_prob = logit.predict_proba(X_test)[:, 1]
    y_pred = logit.predict(X_test)

    results["logistic"] = {
        "auc": roc_auc_score(y_test, y_prob),
        "accuracy": accuracy_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "y_true": y_test.tolist(),
        "y_prob": y_prob.tolist()
    }

    # ---- Random Forest baseline ----
    rf = RandomForestClassifier(
        n_estimators=300,
        random_state=RANDOM_STATE
    )
    rf.fit(X_train, y_train)
    y_prob = rf.predict_proba(X_test)[:, 1]
    y_pred = rf.predict(X_test)

    results["rf_baseline"] = {
        "auc": roc_auc_score(y_test, y_prob),
        "accuracy": accuracy_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "y_true": y_test.tolist(),
        "y_prob": y_prob.tolist()
    }

    # ---- Random Forest tuning ----
    rf_configs = [
        {"max_depth": None, "min_samples_leaf": 1},
        {"max_depth": 20,   "min_samples_leaf": 1},
        {"max_depth": 10,   "min_samples_leaf": 3},
    ]

    for cfg in rf_configs:
        rf = RandomForestClassifier(
            n_estimators=300,
            random_state=RANDOM_STATE,
            **cfg
        )
        rf.fit(X_train, y_train)
        y_prob = rf.predict_proba(X_test)[:, 1]
        y_pred = rf.predict(X_test)

        key = f"rf_{cfg}"
        tuning_results[key] = {
            "auc": roc_auc_score(y_test, y_prob),
            "accuracy": accuracy_score(y_test, y_pred),
            "f1": f1_score(y_test, y_pred),
            "y_true": y_test.tolist(),
            "y_prob": y_prob.tolist()
        }

    return results, tuning_results

# =========================
# Main
# =========================

if __name__ == "__main__":
    X, y = load_data()

    # Regression
    reg_results, reg_tuning = run_regression_models(X, y)

    # Classification
    clf_results, clf_tuning = run_classification_models(X, y)

    # Save artifacts
    with open(f"{DATA_DIR}/regression_results.json", "w") as f:
        json.dump(reg_results, f, indent=2)

    with open(f"{DATA_DIR}/regression_rf_tuning.json", "w") as f:
        json.dump(reg_tuning, f, indent=2)

    with open(f"{DATA_DIR}/classification_results.json", "w") as f:
        json.dump(clf_results, f, indent=2)

    with open(f"{DATA_DIR}/classification_rf_tuning.json", "w") as f:
        json.dump(clf_tuning, f, indent=2)

    # -------------------------
    # Human-readable summary
    # -------------------------

    print("\n=== Regression (main) ===")
    for model, res in reg_results.items():
        print(f"{model.upper():12s} | R2={res['r2']:.3f} | RMSE={res['rmse']:.3f} | MAE={res['mae']:.3f}")

    print("\n=== Regression RF tuning ===")
    for model, res in reg_tuning.items():
        print(f"{model:20s} | R2={res['r2']:.3f} | RMSE={res['rmse']:.3f}")

    print("\n=== Classification (main) ===")
    for model, res in clf_results.items():
        print(f"{model.upper():12s} | AUC={res['auc']:.3f} | Acc={res['accuracy']:.3f} | F1={res['f1']:.3f}")

    print("\n=== Classification RF tuning ===")
    for model, res in clf_tuning.items():
        print(f"{model:20s} | AUC={res['auc']:.3f} | Acc={res['accuracy']:.3f}")
