# ============================================================
# Model Validation Summary Figure — Regression + Classification
# Reads:
#   data/regression_results.json
#   data/classification_results.json
# Produces:
#   Dual-panel summary figure (R² + AUC)
# ============================================================

import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------
REG_PATH = Path("data/regression_results.json")
CLF_PATH = Path("data/classification_results.json")

# ------------------------------------------------------------
# Load results
# ------------------------------------------------------------
with open(REG_PATH, "r") as f:
    reg = json.load(f)

with open(CLF_PATH, "r") as f:
    clf = json.load(f)

# ------------------------------------------------------------
# Extract values (robust to key naming)
# ------------------------------------------------------------
def get_metric(d, keys):
    for k in keys:
        if k in d:
            return d[k]
    return None

# Regression
reg_models = []
reg_r2 = []

for name, metrics in reg.items():
    r2 = get_metric(metrics, ["r2", "R2"])
    if r2 is not None:
        reg_models.append(name.replace("_", " ").title())
        reg_r2.append(r2)

# Classification
clf_models = []
clf_auc = []

for name, metrics in clf.items():
    auc = get_metric(metrics, ["auc", "AUC"])
    if auc is not None:
        clf_models.append(name.replace("_", " ").title())
        clf_auc.append(auc)

# ------------------------------------------------------------
# Plot
# ------------------------------------------------------------
plt.style.use("default")  # match your existing plots

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# ---- Panel 1: Regression R² ----
ax = axes[0]
x = np.arange(len(reg_models))
ax.bar(x, reg_r2)
ax.set_title("Regression Performance — Continuous ITQ")
ax.set_ylabel("R²")
ax.set_xticks(x)
ax.set_xticklabels(reg_models, rotation=20)
ax.set_ylim(0, 1)

# annotate values
for i, v in enumerate(reg_r2):
    ax.text(i, v + 0.02, f"{v:.3f}", ha="center")

# ---- Panel 2: Classification AUC ----
ax = axes[1]
x = np.arange(len(clf_models))
ax.bar(x, clf_auc)
ax.set_title("Classification Performance — High vs Low ITQ")
ax.set_ylabel("AUC")
ax.set_xticks(x)
ax.set_xticklabels(clf_models, rotation=20)
ax.set_ylim(0, 1)

for i, v in enumerate(clf_auc):
    ax.text(i, v + 0.02, f"{v:.3f}", ha="center")

# ---- Overall title ----
fig.suptitle("Model Validation Summary — ITQ Prediction", fontsize=14)

plt.tight_layout(rect=[0, 0, 1, 0.94])

# ------------------------------------------------------------
# Save figure (same folder as your other figures)
# ------------------------------------------------------------
OUT_PATH = Path("data/figures/itq_model_validation_summary.png")
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

plt.savefig(OUT_PATH, dpi=300)
plt.show()

print(f"Saved summary figure to: {OUT_PATH}")
