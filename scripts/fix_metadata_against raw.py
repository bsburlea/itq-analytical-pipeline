#!/usr/bin/env python3

"""
Fix metadata.csv so that metadata.old_name matches raw Qualtrics columns.

This script:
- Normalizes Unicode (smart quotes, etc.)
- Canonicalizes column names
- Drops metadata rows that do not exist in raw data
- Saves a permanent, clean metadata.csv

Run ONCE.
"""

from pathlib import Path
import pandas as pd
import unicodedata
import re

# -------------------------------------------------
# Project root resolution (script-safe)
# -------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_PATH = PROJECT_ROOT / "data" / "raw" / "Qualtrics.xlsx"
META_IN = PROJECT_ROOT / "data" / "metadata.csv"
META_OUT = PROJECT_ROOT / "data" / "metadata.csv"  # overwrite on purpose

print("Project root:", PROJECT_ROOT)
print("Raw data:    ", RAW_PATH)
print("Metadata in: ", META_IN)

# -------------------------------------------------
# Text normalization (CRITICAL)
# -------------------------------------------------
def normalize_text(s: str) -> str:
    """Fix Unicode issues (smart quotes, hidden chars, etc.)."""
    if not isinstance(s, str):
        return s
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.strip()
    return s

# -------------------------------------------------
# Column canonicalization
# -------------------------------------------------
def canonicalize_column(col: str) -> str:
    """
    Canonical form used everywhere in the project.
    Example: "Q24_1 " -> "q24_1"
    """
    col = normalize_text(col)
    col = col.lower()
    col = re.sub(r"\s+", "_", col)
    col = re.sub(r"[^a-z0-9_]", "", col)
    return col

# -------------------------------------------------
# Load raw data
# -------------------------------------------------
raw = pd.read_excel(RAW_PATH, sheet_name=0)
raw_columns = list(raw.columns)

raw_canonical = {canonicalize_column(c) for c in raw_columns}

print("\nRaw columns after canonicalization:", len(raw_canonical))

# -------------------------------------------------
# Load metadata
# -------------------------------------------------
meta = pd.read_csv(META_IN)

print("\nOriginal metadata columns:")
print(list(meta.columns))

REQUIRED_COLUMNS = ["old_name", "cluster", "sub_cluster", "feature", "question"]

missing_required = set(REQUIRED_COLUMNS) - set(meta.columns)
if missing_required:
    raise ValueError(f"❌ Metadata missing required columns: {missing_required}")

# -------------------------------------------------
# Normalize + canonicalize metadata.old_name
# -------------------------------------------------
meta["old_name"] = meta["old_name"].apply(normalize_text)
meta["_canonical_old_name"] = meta["old_name"].apply(canonicalize_column)

# -------------------------------------------------
# Drop metadata rows not present in raw
# -------------------------------------------------
mask_present = meta["_canonical_old_name"].isin(raw_canonical)
dropped = meta.loc[~mask_present, "old_name"].tolist()

if dropped:
    print("\n⚠️ Dropping metadata entries not found in raw data:")
    for d in dropped:
        print("  -", repr(d))

meta = meta.loc[mask_present].copy()
meta.drop(columns="_canonical_old_name", inplace=True)

print("\nMetadata rows kept:", len(meta))

if len(meta) == 0:
    raise RuntimeError(
        "❌ All metadata rows were dropped.\n"
        "This means normalization failed. Do NOT proceed."
    )

# -------------------------------------------------
# Save permanently
# -------------------------------------------------
meta.to_csv(META_OUT, index=False)

print("\n✅ Metadata fixed permanently.")
print("Saved to:", META_OUT)
