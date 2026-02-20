#!/usr/bin/env python3

"""
Fix and canonicalize metadata file once and for all.

- Loads old_clusters.csv
- Cleans broken / quoted / Excel-corrupted column names
- Enforces canonical schema
- Saves clean metadata.csv

Run from project root:
    python scripts/fix_metadata.py
"""

from pathlib import Path
import pandas as pd
import re
import sys

# -------------------------------------------------
# Project paths (script-safe, not notebook-safe)
# -------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_META = PROJECT_ROOT / "data" / "old_clusters.csv"
OUTPUT_META = PROJECT_ROOT / "data" / "metadata.csv"

# -------------------------------------------------
# Canonical schema (THIS is the contract)
# -------------------------------------------------
CANONICAL_COLUMNS = [
    "old_name",
    "cluster",
    "sub_cluster",
    "feature",
    "question",
]

# -------------------------------------------------
# Column canonicalization
# -------------------------------------------------
def canonicalize_column(col: str) -> str:
    """
    Extract semantic column name regardless of:
    - smart quotes
    - doubled quotes
    - Excel artifacts
    - Unicode junk
    """
    col_lower = col.lower()

    match = re.search(
        r"(old[_\s]*name|cluster|sub[_\s]*cluster|feature|question)",
        col_lower,
    )

    if not match:
        return col_lower  # keep unknowns for inspection

    value = match.group(1)
    value = value.replace(" ", "_")

    if value == "old_name":
        return "old_name"
    if value == "sub_cluster":
        return "sub_cluster"

    return value

# -------------------------------------------------
# Main
# -------------------------------------------------
def main():
    print(f"Loading metadata from: {INPUT_META}")

    if not INPUT_META.exists():
        raise FileNotFoundError(f"Metadata file not found: {INPUT_META}")

    meta = pd.read_csv(INPUT_META)

    print("\nOriginal columns (repr):")
    for c in meta.columns:
        print(repr(c))

    # Canonicalize column names
    meta.columns = [canonicalize_column(c) for c in meta.columns]

    # Drop unnamed / junk columns
    meta = meta.loc[:, ~meta.columns.str.startswith("unnamed")]

    print("\nCleaned columns (repr):")
    for c in meta.columns:
        print(repr(c))

    # Validate schema
    missing = set(CANONICAL_COLUMNS) - set(meta.columns)
    if missing:
        raise ValueError(
            f"❌ Missing required columns after cleaning: {missing}"
        )

    # Enforce canonical order
    meta = meta[CANONICAL_COLUMNS]

    # Final sanity check
    assert list(meta.columns) == CANONICAL_COLUMNS

    # Save clean metadata
    meta.to_csv(OUTPUT_META, index=False)

    print("\n✅ Metadata fixed permanently.")
    print(f"Saved to: {OUTPUT_META}")

# -------------------------------------------------
if __name__ == "__main__":
    main()
