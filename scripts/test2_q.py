import pandas as pd
import numpy as np

old = pd.read_csv("data/q_old.csv")
new = pd.read_csv("data/q.csv")

# Where values differ
diff_mask = (old != new) & ~(old.isna() & new.isna())

# Count differences per column
diff_counts = diff_mask.sum().sort_values(ascending=False)
print(diff_counts[diff_counts > 0].head(20))
