#!/usr/bin/env python
"""
geocode_locations.py

Reads an Excel file containing latitude/longitude,
uses geopy (Nominatim) to get a 2-letter US state / Canadian province code,
shows progress with tqdm, and writes a small CSV with:
    latitude, longitude, location
"""

import pandas as pd
from tqdm import tqdm
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# ----------------------------- CONFIG ---------------------------------

INPUT_EXCEL = "data/Qualtrics.xlsx"
LAT_COL = "LocationLatitude"
LON_COL = "LocationLongitude"
OUTPUT_CSV = "data/lat_lon_location.csv"

# ----------------------------- GEOCODER --------------------------------

_geolocator = Nominatim(user_agent="itq_project_geocoder")
_reverse = RateLimiter(_geolocator.reverse, min_delay_seconds=1.0)

# small in-memory cache to avoid re-querying near-duplicate points
_geocode_cache = {}

def _latlon_to_state_cached(lat, lon):
    key = (round(lat, 5), round(lon, 5))

    if key in _geocode_cache:
        return _geocode_cache[key]

    try:
        location = _reverse((lat, lon), zoom=10, addressdetails=True)

        code = None
        if location and "address" in location.raw:
            addr = location.raw["address"]

            candidates = ["state_code", "state", "province", "ISO3166-2-lvl4"]

            for k in candidates:
                if k in addr and isinstance(addr[k], str) and addr[k]:
                    val = addr[k]
                    if len(val) == 2:
                        code = val.upper()
                        break
                    if "-" in val and len(val.split("-")[-1]) == 2:
                        code = val.split("-")[-1].upper()
                        break

            # fallback: country code if nothing else
            if code is None and "country_code" in addr:
                code = addr["country_code"].upper()

        _geocode_cache[key] = code
        return code

    except Exception as e:
        print(f"\n⚠️  Geocoding error for ({lat}, {lon}): {e}")
        _geocode_cache[key] = None
        return None

# ----------------------------- MAIN ------------------------------------

def main():
    print(f"📂 Loading Excel file: {INPUT_EXCEL}")
    df = pd.read_excel(INPUT_EXCEL)

    if LAT_COL not in df.columns or LON_COL not in df.columns:
        raise ValueError(
            f"Expected columns '{LAT_COL}' and '{LON_COL}' in the Excel file.\n"
            f"Found: {list(df.columns)}"
        )

    work = df[[LAT_COL, LON_COL]].dropna().copy()

    print(f"🌍 Geocoding {len(work)} locations (this will take ~{len(work)} seconds)...")

    locations = []
    for lat, lon in tqdm(zip(work[LAT_COL], work[LON_COL]), total=len(work)):
        locations.append(_latlon_to_state_cached(float(lat), float(lon)))

    work["location"] = locations

    print(f"💾 Saving results to: {OUTPUT_CSV}")
    work.to_csv(OUTPUT_CSV, index=False)

    print("✅ Done!")
    print(work.head())

if __name__ == "__main__":
    main()
