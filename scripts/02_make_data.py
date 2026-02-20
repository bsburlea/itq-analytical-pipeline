#!/usr/bin/env python3
import sys
from pathlib import Path
import numpy as np
import pandas as pd

DATA_DIR = Path("data")
Q_PATH = DATA_DIR / "q.csv"
META_PATH = DATA_DIR / "metadata.csv"
LATLON_PATH = DATA_DIR / "lat_lon_location.csv"
OUT_PATH = DATA_DIR / "data.csv"


def die(msg):
    print(msg, file=sys.stderr)
    raise SystemExit(1)


def make_key(lat, lon, decimals=4):
    try:
        if pd.isna(lat) or pd.isna(lon):
            return None
        return (round(float(lat), decimals), round(float(lon), decimals))
    except Exception:
        return None


def main():
    print(f"Loading q.csv: {Q_PATH}")
    q = pd.read_csv(Q_PATH)

    print(f"Loading metadata.csv: {META_PATH}")
    meta = pd.read_csv(META_PATH)

    print(f"Loading lat_lon_location.csv: {LATLON_PATH}")
    ll = pd.read_csv(LATLON_PATH)

    print(f"Columns in q: {q.shape[1]}")
    print(f"Rows in q: {q.shape[0]}")

    # ---- sanity on required columns ----
    if not {"LocationLatitude", "LocationLongitude"}.issubset(q.columns):
        die("❌ q.csv must contain LocationLatitude and LocationLongitude")

    if not {"latitude", "longitude", "state_province"}.issubset(ll.columns):
        die("❌ lat_lon_location.csv must contain latitude, longitude, state_province")

    # ---- build lookup dict from lat_lon_location.csv ----
    lookup = {}
    for _, row in ll.iterrows():
        key = make_key(row["latitude"], row["longitude"])
        if key and key not in lookup:
            lookup[key] = row["state_province"]

    print(f"Lookup table size: {len(lookup)}")

    # ---- add state_province by slow loop ----
    print("Adding state_province using LocationLatitude/LocationLongitude...")
    out = []
    misses = 0

    for lat, lon in zip(q["LocationLatitude"], q["LocationLongitude"]):
        key = make_key(lat, lon)
        if key in lookup:
            out.append(lookup[key])
        else:
            out.append(np.nan)
            misses += 1

    q["state_province"] = out
    print(f"Lookup misses: {misses}")

    # ---- rename columns using metadata ----
    if "old_name" not in meta.columns or "feature" not in meta.columns:
        die("❌ metadata.csv must contain old_name and feature")

    rename_map = dict(zip(meta["old_name"], meta["feature"]))
    q = q.rename(columns=rename_map)
    print(f"Shape after renaming: {q.shape}")

    # ---- drop raw lat/lon ----
    for c in ["LocationLatitude", "LocationLongitude", "latitude", "longitude"]:
        if c in q.columns:
            q = q.drop(columns=c)

    # ---- reorder columns ----
    ordered = meta["feature"].tolist()

    if "language" in ordered:
        idx = ordered.index("language") + 1
        ordered = ordered[:idx] + ["state_province"] + ordered[idx:]
    else:
        ordered = ["state_province"] + ordered

    # --- semantic canonicalization ---
    ### FIX: rename target in data AND in ordered list so it is not dropped
    q = q.rename(columns={"think_about_living": "think_about_leaving"})
    ordered = ["think_about_leaving" if c == "think_about_living" else c for c in ordered]

    # ---- force target last ----
    target = "think_about_leaving"
    if target in ordered:
        ordered = [c for c in ordered if c != target] + [target]

    ordered = [c for c in ordered if c in q.columns]
    q = q[ordered]

    # ---- coerce ints ----
    for col in q.columns:
        if pd.api.types.is_numeric_dtype(q[col]):
            s = q[col]
            if np.all(np.isclose(s.dropna(), np.round(s.dropna()))):
                if s.isna().sum() == 0:
                    q[col] = np.round(s).astype(int)
                else:
                    q[col] = np.round(s).astype("Int64")

    print(f"Final shape after reordering: {q.shape}")
    q.to_csv(OUT_PATH, index=False)
    print(f"Saved to: {OUT_PATH}")
    print("Done.")


if __name__ == "__main__":
    main()
