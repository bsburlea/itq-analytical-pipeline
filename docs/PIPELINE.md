# Data Processing and Analysis Pipeline

This document describes the **end-to-end processing pipeline** used in the project,
including frozen design decisions and planned analytical stages.

Its purpose is to provide a **stable internal reference** for reproducibility,
maintenance, and methodological clarity.

---

## 1. Pipeline Overview

The analysis follows a theory-driven, staged pipeline:

1. Raw survey data ingestion
2. Metadata-driven construct definition
3. Construct-level feature aggregation
4. Dimensionality reduction and stability analysis
5. Visualization and interpretation

Each stage is explicitly separated to avoid semantic leakage and ensure reproducibility.

---

## 2. Raw Data Layer

### 2.1 Source Data

* File: `data/sample_raw.csv`
* Represents anonymized questionnaire responses
* Each column corresponds to a **single questionnaire item**
* No aggregation or transformation is performed at this stage

### 2.2 Identifier Handling (Frozen)

* Direct identifiers (e.g. IP addresses) are **never** treated as constructs
* Identifiers are removed prior to analysis
* Metadata is guaranteed to contain **no identifiers**

This rule is frozen and must not be violated.

---

## 3. Metadata-Driven Semantics (Frozen)

### 3.1 Metadata File

* File: `data/metadata.csv`
* Acts as the **single source of truth** for semantic structure

Key columns:

* `old_name` — questionnaire item (raw column)
* `feature` — construct / scale name
* `sub_cluster` — conceptual grouping
* `cluster` — high-level domain

### 3.2 Frozen Semantic Rules

* A **feature represents a construct / scale**
* Multiple questionnaire items may map to one feature
* No aggregation occurs in metadata
* Scale construction happens **only in code**

These rules are frozen.

---

## 4. Feature Construction

### 4.1 Construct Aggregation

Planned aggregation strategies include:

* Mean or sum of standardized items
* PCA- or factor-based scores (if justified)

The choice of aggregation is explicitly documented in notebooks.

### 4.2 Single-Item Constructs

* Some features are represented by a single questionnaire item
* These are retained intentionally
* Limitations are documented in the paper and README

---

## 5. Analysis Pipeline

### 5.1 Standardization

* Construct-level features are standardized prior to PCA
* Standardization parameters are derived from the sample only

### 5.2 Dimensionality Reduction

* PCA is applied at the **construct level**
* Component interpretation is guided by theory

### 5.3 Bootstrap Stability Analysis

* Respondent-level resampling
* Stability assessed via:

  * loading sign consistency
  * variance explained distributions
  * component robustness

---

## 6. Execution Order

The pipeline is executed via notebooks in numeric order:

1. `01_cleaning.ipynb`
2. `02_constructs.ipynb`
3. `03_pca_bootstrap.ipynb`
4. `04_visualization.ipynb`

---

## 7. Reproducibility Contract

* No hidden state between notebooks
* All transformations are explicit
* Results are reproducible using `sample_raw.csv`

---

## 8. Frozen Status

This document defines **frozen pipeline semantics**.

Changes require:

* explicit justification
* corresponding updates to README and metadata documentation
