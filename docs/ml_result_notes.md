# Prediction Validation Layer — Intention to Quit (ITQ)

**Position in Pipeline**

EDA → Prediction Validation → Stage A–D Interpretation → Conceptual Diagrams

---

## Scope of the Prediction Analysis

This document describes the prediction experiments used as an **empirical validation layer** for the staged psychosocial modelling framework (Stages A–D).

These experiments are **not** intended to produce a production-grade predictive system.
Instead, their purpose is to:

* verify that ITQ contains systematic, learnable structure,
* quantify how predictable ITQ is from psychosocial variables,
* demonstrate that observed relationships are non-random and robust,
* provide empirical grounding for the layered conceptual interpretation developed later in the project.

The prediction layer precedes and supports the interpretative stages (Stage A–D).
It should therefore be read as **evidence of structured signal**, not as the primary contribution of the study.

---

## Data and Features

**Source pipeline**

* Feature preparation: `04_prepare_itq_features.py`
* Prediction experiments: `05_itq_prediction_experiments.py`
* Analytical context: `05_models`, `06_results_interpretation`

**Input data**

* ~499 participants
* ~135 engineered psychosocial features
* All predictors standardized
* Demographic and geographic variables excluded from modelling to avoid causal over-interpretation

**Outcome definitions**

* Continuous ITQ score (1–5 scale)
* Binary ITQ (low vs high risk)

All models were evaluated using a fixed 80/20 train–test split with performance reported on held-out test data.

No feature selection was performed; all variables were retained to minimize researcher degrees of freedom and preserve theoretical neutrality.

---

## Regression Models — Predicting Continuous ITQ

**Models evaluated**

| Model                    | Role                         |
| ------------------------ | ---------------------------- |
| Ridge Regression         | Linear baseline              |
| Random Forest (baseline) | Non-linear ensemble          |
| Tuned Random Forest      | Regularized non-linear model |

**Metrics reported**

* R²
* RMSE
* MAE

**Key observation**

Random Forest models capture substantially more variance in ITQ than linear Ridge models, indicating meaningful non-linear structure in psychosocial predictors.
However, performance levels also suggest the presence of irreducible noise and individual variability.

Interpretation focus:

* The goal is **not** maximizing predictive accuracy.
* The comparison demonstrates that psychosocial mechanisms likely interact in non-linear ways.

---

## Regression Visualization

Predicted vs. true ITQ plots illustrate several expected behaviours:

* Regression toward the mean:

  * low ITQ slightly overestimated,
  * high ITQ slightly underestimated.
* Effects arise naturally due to:

  * bounded survey scales (1–5),
  * measurement noise,
  * scarcity of extreme responses.

Regularization in tuned Random Forest models:

* reduces variance for low ITQ values,
* does not fundamentally alter overall predictive structure.

**Important qualitative insight**

Individuals with very high ITQ scores are rarely mapped into the low-risk prediction range.
This indicates that models preserve risk ranking even when numerical precision is imperfect.

---

## Classification Models — High vs Low ITQ

Binary framing was introduced to evaluate discrimination rather than numeric precision.

**Models**

* Logistic regression (linear baseline)
* Random Forest classifier (non-linear)

**Metrics**

* AUC
* Accuracy
* F1 score

**Interpretation**

* High-risk individuals can be identified with strong reliability.
* Non-linear interactions improve classification performance.
* Logistic regression provides a stable baseline; Random Forest captures additional interaction effects.

The classification task complements regression by demonstrating that ITQ signal is robust under different modelling assumptions.

---

## ROC Curve Behaviour

ROC analysis shows:

* High true-positive rates at relatively low false-positive rates.
* Strong separation between low and high ITQ groups.

Interpretation emphasis:

* The system is particularly effective at detecting higher-risk individuals.
* From a research perspective, this confirms the presence of structured psychosocial signal rather than noise.

---

## Methodological Positioning

These prediction experiments should be interpreted as:

* **evidence of structured signal**, not causal inference,
* complementary to classical modelling approaches,
* validation that psychosocial variables encode meaningful predictive information.

Hyperparameter tuning was intentionally limited and theory-driven to preserve interpretability rather than optimize performance.

From a statistical perspective, the Random Forest acts as a flexible non-parametric model approximating high-order interactions without explicitly specifying interaction terms.

---

## Relationship to the Stage A–D Conceptual Framework

The prediction layer motivates the staged modelling framework:

* Demonstrating predictability establishes that ITQ is not random.
* Observed non-linear structure suggests layered psychosocial interactions.
* These findings motivate the decomposition introduced in Stages A–D:

  * proximal mechanisms,
  * contextual pathways,
  * distal personality structure.

Thus, prediction serves as an empirical foundation upon which the conceptual synthesis is built.

---

## Reporting Guidance

When referenced in the manuscript:

* Frame prediction results as **validation of structured psychosocial signal**.
* Avoid presenting machine learning performance as the central contribution.
* Emphasize interpretability and theoretical alignment rather than optimization.

This document supports the transition from empirical modelling toward conceptual integration and final conclusions.
