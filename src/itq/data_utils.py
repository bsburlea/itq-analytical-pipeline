# src/data_utils.py

from pathlib import Path
import pandas as pd
import numpy as np
import re
import unicodedata


# -------------------------------------------------
# Column canonicalization
# -------------------------------------------------
def canonicalize_column(col: str) -> str:
    """
    Normalize column names so raw data and metadata match reliably.

    Examples:
    - "Q24_1" → "q24_1"
    - "Duration (in seconds)" → "duration_in_seconds"
    - smart quotes / spaces / casing removed
    """
    if col is None:
        return col

    col = str(col)

    # normalize smart quotes
    col = col.replace("’", "'").replace("‘", "'")

    col = col.strip().lower()
    col = re.sub(r"[^\w]+", "_", col)
    col = re.sub(r"_+", "_", col)
    col = col.strip("_")

    return col


# -------------------------------------------------
# Loading functions
# -------------------------------------------------
def load_raw_data(path: Path) -> pd.DataFrame:
    """
    Load raw Qualtrics data (CSV or Excel).
    Canonicalizes column names immediately.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Raw data file not found: {path}")

    if path.suffix.lower() in [".xlsx", ".xls"]:
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path)

    # canonicalize columns
    df.columns = [canonicalize_column(c) for c in df.columns]

    return df


def load_metadata(path: Path) -> pd.DataFrame:
    """
    Load metadata.csv and canonicalize old_name.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Metadata file not found: {path}")

    meta = pd.read_csv(path)

    # drop accidental unnamed columns
    meta = meta.loc[:, ~meta.columns.str.contains("^unnamed", case=False)]

    required = {"old_name", "cluster", "sub_cluster", "feature", "question"}
    missing = required - set(meta.columns)
    if missing:
        raise ValueError(f"Metadata missing required columns: {missing}")

    # canonicalize old_name
    meta["old_name"] = meta["old_name"].apply(canonicalize_column)

    return meta


# -------------------------------------------------
# Validation
# -------------------------------------------------
def validate_metadata_alignment(df: pd.DataFrame, meta: pd.DataFrame) -> None:
    """
    Ensure metadata.old_name references columns that exist in raw data
    AFTER canonicalization.
    """
    df_cols = set(df.columns)
    meta_cols = set(meta["old_name"])

    missing_in_raw = meta_cols - df_cols
    if missing_in_raw:
        raise ValueError(
            "Metadata references columns not found in raw data:\n"
            f"{sorted(missing_in_raw)}"
        )


def clean_column_name(s: str) -> str:
    # Normalize unicode (NFKD splits weird chars)
    s = unicodedata.normalize("NFKD", s)

    # Remove smart quotes and any remaining quotes
    s = s.replace("’", "").replace("‘", "").replace("'", "").replace('"', "")

    # Lowercase
    s = s.lower()

    # Replace non-alphanumeric with underscore
    s = re.sub(r"[^a-z0-9]+", "_", s)

    # Collapse multiple underscores
    s = re.sub(r"_+", "_", s)

    # Strip leading/trailing underscores
    s = s.strip("_")

    return s

# -------------------------------------------------
# Cleaning
# -------------------------------------------------
def clean_raw_survey(
    df: pd.DataFrame,
    meta: pd.DataFrame,
    missing_strategy: str = "median",
) -> pd.DataFrame:
    """
    Clean raw survey data:
    - keep only columns defined in metadata
    - impute missing values
    """
    df = df.copy()

    # keep only survey columns
    keep_cols = meta["old_name"].tolist()
    df = df[keep_cols]

    # convert to numeric where possible
    for c in df.columns:
        try:
            df[c] = pd.to_numeric(df[c])
        except (ValueError, TypeError):
            pass

    # missing value handling
    if missing_strategy == "median":
        for c in df.columns:
            if pd.api.types.is_numeric_dtype(df[c]):
                df[c] = df[c].fillna(df[c].median())

    elif missing_strategy == "mean":
        for c in df.columns:
            if pd.api.types.is_numeric_dtype(df[c]):
                df[c] = df[c].fillna(df[c].mean())

    elif missing_strategy == "drop":
        df = df.dropna()

    else:
        raise ValueError(f"Unknown missing_strategy: {missing_strategy}")

    return df
