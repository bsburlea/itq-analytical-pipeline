# ============================================================
# 05_models.py  — GLOBAL MODELLING VERSION
# ============================================================
# Progressive modelling pipeline (FULL SAMPLE N=499)
#
# M1: ITQ ~ Mechanisms
# M2: ITQ ~ Mechanisms + Controls + Environment
# M3: ITQ ~ Mechanisms + Controls + Environment + Personality
#
# Phase 2:
#   Mechanisms ~ Personality + Controls + Environment
#
# Phase 3 (NEW):
#   Personality → Outcomes (Task / Team / Stress / ITQ)
#
# Phase 4 (NEW):
#   Independent Mechanism → ITQ models
#
# Output:
#   data/structured_results.json
# ============================================================

import json
import numpy as np
import pandas as pd

from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

# ============================================================
# CONFIG
# ============================================================

DATA_PATH = "data/data.csv"
OUTPUT_PATH = "data/structured_results.json"

ALPHA = 1.0
RANDOM_STATE = 42

# ============================================================
# COLUMN DEFINITIONS
# ============================================================

ITQ_COL = "think_about_leaving"

MECHANISM_COLS = [
    "perform_effectively",
    "succeed",
    "obtain_outcomes",
    "achieve_goals",
    "assess_team_productivity",
    "satisfied_with_colleagues",
    "nervous/stressed",
    "upset_about_something",
]

CONTROL_COLS = [
    "rely_on_supervisor_for_backup",
    "organization_cares_about_me",
    "help_available_from_organization",
    "seek_family_support",
]

ENVIRONMENT_COLS = [
    "hybrid_experience",
    "current_in_person",
]

PERSONALITY_COLS = [
    "like_order",
    "sympathize",
    "imagination",
    "relaxed",
    "easily_upset",
    "networking",
    "communication",
    "get_people_to_like_me",
    "understand_hidden_agendas",
]

# ============================================================
# OUTCOME GROUPS (NEW)
# ============================================================

TASK_EFFECTIVENESS_COLS = [
    "perform_effectively",
    "succeed",
    "obtain_outcomes",
    "achieve_goals",
]

TEAM_EFFECTIVENESS_COLS = [
    "assess_team_productivity",
    "satisfied_with_colleagues",
]

JOB_STRESS_COLS = [
    "nervous/stressed",
    "upset_about_something",
]

OUTCOME_GROUPS = {
    "TASK_EFFECTIVENESS": TASK_EFFECTIVENESS_COLS,
    "TEAM_EFFECTIVENESS": TEAM_EFFECTIVENESS_COLS,
    "JOB_STRESS": JOB_STRESS_COLS,
    "ITQ": [ITQ_COL],
}

# ============================================================
# UTILS
# ============================================================

def rmse(y_true, y_pred):
    return np.sqrt(mean_squared_error(y_true, y_pred))


def standardize_df(df: pd.DataFrame):
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df)
    return pd.DataFrame(scaled, columns=df.columns, index=df.index)


def fit_ridge_model(X: pd.DataFrame, y: pd.Series):

    model = Ridge(alpha=ALPHA, random_state=RANDOM_STATE)
    model.fit(X, y)

    y_pred = model.predict(X)

    return {
        "coefficients": dict(zip(X.columns, model.coef_)),
        "r2": float(r2_score(y, y_pred)),
        "rmse": float(rmse(y, y_pred)),
        "mae": float(mean_absolute_error(y, y_pred)),
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print("Loading full dataframe...")
    df = pd.read_csv(DATA_PATH)

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------
    required_cols = (
        [ITQ_COL]
        + MECHANISM_COLS
        + CONTROL_COLS
        + ENVIRONMENT_COLS
        + PERSONALITY_COLS
    )

    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in data.csv:\n{missing}")

    # --------------------------------------------------------
    # BUILD GLOBAL MATRICES
    # --------------------------------------------------------
    X_M = standardize_df(df[MECHANISM_COLS])
    X_C = standardize_df(df[CONTROL_COLS])
    X_E = df[ENVIRONMENT_COLS]  # binary → DO NOT standardize
    X_P = standardize_df(df[PERSONALITY_COLS])

    y_itq = df[ITQ_COL]

    print(f"Running GLOBAL models (N = {len(df)})")

    # ========================================================
    # M1 — Mechanisms
    # ========================================================
    M1 = fit_ridge_model(X_M, y_itq)

    # ========================================================
    # M2 — + Controls + Environment
    # ========================================================
    X_M2 = pd.concat([X_M, X_C, X_E], axis=1)
    M2 = fit_ridge_model(X_M2, y_itq)

    # ========================================================
    # M3 — + Personality
    # ========================================================
    X_M3 = pd.concat([X_M, X_C, X_E, X_P], axis=1)
    M3 = fit_ridge_model(X_M3, y_itq)

    print(f"M1 R2={M1['r2']:.3f} | M2 R2={M2['r2']:.3f} | M3 R2={M3['r2']:.3f}")

    # ========================================================
    # PHASE 2 — MECHANISM MODELS
    # ========================================================
    print("Running upstream mechanism models...")

    mech_models = {}
    X_upstream = pd.concat([X_C, X_E, X_P], axis=1)

    for mech in MECHANISM_COLS:
        y = df[mech]
        mech_models[mech] = fit_ridge_model(X_upstream, y)

    # ========================================================
    # PHASE 3 — PERSONALITY → OUTCOME MAPPING (NEW)
    # ========================================================
    print("Running personality influence models...")

    personality_models = {}

    X_personality_base = pd.concat([X_C, X_E, X_P], axis=1)

    for outcome_name, cols in OUTCOME_GROUPS.items():

        if len(cols) > 1:
            y = df[cols].mean(axis=1)
        else:
            y = df[cols[0]]

        personality_models[outcome_name] = fit_ridge_model(
            X_personality_base,
            y,
        )

    # ========================================================
    # PHASE 4 — INDEPENDENT MECHANISM → ITQ (NEW)
    # ========================================================
    print("Running independent mechanism models...")

    mech_independent = {}

    for mech in MECHANISM_COLS:
        X_single = X_M[[mech]]
        mech_independent[mech] = fit_ridge_model(X_single, y_itq)

    # ========================================================
    # SAVE RESULTS
    # ========================================================
    results = {
        "GLOBAL": {
            "M1": M1,
            "M2": M2,
            "M3": M3,
            "MECHANISMS": mech_models,
            "PERSONALITY_EFFECTS": personality_models,
            "MECH_INDEPENDENT": mech_independent,
        }
    }

    print("\nSaving structured results...")
    with open(OUTPUT_PATH, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Saved to: {OUTPUT_PATH}")
    print("Done.")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
