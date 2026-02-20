import pandas as pd

q_new = pd.read_csv("data/q.csv")
q_old = pd.read_csv("data/q_old.csv")

only_in_old = set(q_old.columns) - set(q_new.columns)
only_in_new = set(q_new.columns) - set(q_old.columns)

print("Only in old:", only_in_old)
print("Only in new:", only_in_new)
