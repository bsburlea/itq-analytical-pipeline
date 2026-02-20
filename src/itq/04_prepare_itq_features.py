import pandas as pd
import json
from sklearn.preprocessing import StandardScaler


# =========================
# Configuration
# =========================

DATA_PATH = "data/data.csv"
OUTPUT_DIR = "data/"

TARGET = "think_about_leaving"

EXCLUDE = [
    "think_about_leaving",   # target
    "region",                # derived geography (excluded from model)
    "state_province",        # raw geography (already dropped in EDA)
    "language",
    "sex",
    "age",
    "education",
    "minority",
    "experience",
]


# =========================
# Main logic
# =========================

def build_features():
    # Load clean data
    df = pd.read_csv(DATA_PATH)

    # -------------------------
    # Target
    # -------------------------
    if TARGET not in df.columns:
        raise ValueError(f"Target column '{TARGET}' not found in dataframe")

    y = df[TARGET]

    # -------------------------
    # Features
    # -------------------------
    feature_cols = [c for c in df.columns if c not in EXCLUDE]

    X = df[feature_cols]

    # Safety check
    if X.isnull().sum().sum() > 0:
        print("Warning: Missing values detected in X")
        print(X.isnull().sum().sort_values(ascending=False).head())

    # -------------------------
    # Standardization
    # -------------------------
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_scaled_df = pd.DataFrame(X_scaled, columns=feature_cols)

    # -------------------------
    # Save outputs
    # -------------------------
    X_scaled_df.to_csv(f"{OUTPUT_DIR}/X.csv", index=False)
    y.to_csv(f"{OUTPUT_DIR}/y.csv", index=False)

    with open(f"{OUTPUT_DIR}/feature_names.json", "w") as f:
        json.dump(feature_cols, f, indent=2)

    print("Feature engineering completed.")
    print(f"X shape: {X_scaled_df.shape}")
    print(f"y length: {len(y)}")
    print(f"Number of features: {len(feature_cols)}")

    return X_scaled_df, y, feature_cols


# =========================
# CLI entry point
# =========================

if __name__ == "__main__":
    build_features()
