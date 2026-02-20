from pathlib import Path
import pandas as pd
import numpy as np

# -----------------------------
# Paths
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "Qualtrics.xlsx"
OUTPUT_PATH = PROJECT_ROOT / "data" / "q.csv"

# -----------------------------
# Load raw
# -----------------------------
print(f"Loading: {RAW_PATH}")
q = pd.read_excel(RAW_PATH)
print("Initial rows:", len(q))

# -----------------------------
# Deduplicate by IP
# -----------------------------
q = q.drop_duplicates(subset="IPAddress", keep="first").reset_index(drop=True)
print("After dedup IP:", len(q))

# -----------------------------
# Remove unfinished
# -----------------------------
q = q[q["Status"] != 1].reset_index(drop=True)
print("After removing unfinished:", len(q))

# -----------------------------
# Drop obvious junk columns
# -----------------------------
DROP_COLS = [
    "StartDate", "EndDate", "Status",
    "Progress", "Finished", "UserLanguage",
    "Q6_5_TEXT", "Q7_4_TEXT",
    "RecordedDate", "ResponseId",
    "RecipientLastName", "RecipientFirstName",
    "RecipientEmail", "ExternalReference",
    "DistributionChannel",
    "opp", "gc", "term", "rid", "RISN",
    "transaction_id", "SVID",
    "Q_BallotBoxStuffing", "Q_RelevantIDDuplicate",
    "Q_RelevantIDDuplicateScore",
    "Q_RecaptchaScore",
    "Q_RelevantIDFraudScore",
    "Q_TotalDuration",
    "V", "LS", "PS",
    "Unnamed: 180"
]

q = q.drop(columns=[c for c in DROP_COLS if c in q.columns])

# -----------------------------
# Drop useless constant columns
# -----------------------------
# Q1: everyone is IT professional
# Q3: everyone USA/Canada
# Q12: unrealistic management distribution
FORCE_DROP = ["Q1", "Q3", "Q12"]
q = q.drop(columns=[c for c in FORCE_DROP if c in q.columns])

# -----------------------------
# Q6 special rule:
# NaN = 4 ("None of the above")
# -----------------------------
if "Q6" in q.columns:
    q.loc[q["Q6"].isnull(), "Q6"] = 4
    q["Q6"] = q["Q6"].astype("int64")

# -----------------------------
# Median imputation for all other numeric columns
# -----------------------------
numeric_cols = q.select_dtypes(include=[np.number]).columns

for col in numeric_cols:
    if col == "Q6":
        continue
    if q[col].isnull().any():
        median = q[col].median()
        q[col] = q[col].fillna(median)

# -----------------------------
# Final sanity
# -----------------------------
print("Final shape:", q.shape)
print("Remaining NaNs:", q.isnull().sum().sum())

# -----------------------------
# Save
# -----------------------------
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
q.to_csv(OUTPUT_PATH, index=False)
print(f"Saved: {OUTPUT_PATH}")
