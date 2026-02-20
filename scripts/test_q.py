import pandas as pd

new = pd.read_csv("data/q.csv")
old = pd.read_csv("data/q_old.csv")

print(new.shape, old.shape)
print("Identical:", new.equals(old))
