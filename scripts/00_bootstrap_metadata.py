import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

q = pd.read_csv(PROJECT_ROOT / "data" / "q.csv")

meta = pd.DataFrame({
    "old_name": q.columns,
    "cluster": "",
    "sub_cluster": "",
    "feature": q.columns,   # start identical
    "question": ""
})

meta.to_csv(PROJECT_ROOT / "data" / "metadata_new.csv", index=False)
print("Created metadata_new.csv with", len(meta), "rows")
