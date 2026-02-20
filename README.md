# Psychosocial Predictors of Intention to Quit

**Exploratory PCA and Stability Analysis**

## Overview

This repository contains the analysis code and visualizations supporting a study on the psychosocial predictors of employees’ *intention to quit*.
The work focuses on six theoretically grounded constructs and uses **Principal Component Analysis (PCA)** with **bootstrap resampling** to assess structural stability and interpretability.

The repository is designed to support **methodological transparency** and **reproducibility**, while respecting data privacy constraints.

---

## Project Structure

This repository separates narrative analysis, executable code, and frozen design
decisions to support reproducibility and clarity.

- This README provides a high-level overview of the study and results.
- Analyses are implemented step-by-step in `notebooks/`.
- Reusable data processing and modelling logic lives in `src/`.
- Semantic definitions, metadata structure, and pipeline decisions are documented
  in `docs/PIPELINE.md`.

---

## Constructs Used

The analysis is based on the following six psychosocial constructs:

* Perceived Stress
* Work Environment
* Agreeableness
* Neuroticism
* Political Skills
* Self-Monitoring

Construct definitions and questionnaire mappings are provided in `data/metadata.csv`.

---

## Methodology Summary

1. Data cleaning and construct aggregation
2. Standardization of features
3. PCA on six constructs
4. 3D visualization of dominant components
5. **Bootstrap PCA (resampling respondents)** to assess:

   * Loading stability
   * Sign consistency
   * Explained variance confidence intervals

This allows us to distinguish **structural components** from sampling noise.

---

## Repository Structure

```
├── data/
│   ├── sample_raw.csv      # 50-row representative, anonymized sample
│   └── metadata.csv        # construct & question mapping
│
├── notebooks/
│   ├── 01_cleaning.ipynb
│   ├── 02_constructs.ipynb
│   ├── 03_pca_bootstrap.ipynb
│   └── 04_visualization.ipynb
│
├── requirements.txt
└── README.md
```

---

## Data Availability

Due to privacy considerations, the full raw dataset cannot be shared publicly.

* `sample_raw.csv` contains a **distribution-preserving subset (n=50)**
* Latitude/longitude and direct identifiers have been removed
* All analyses can be reproduced structurally using this sample

---

## Reproducibility

To reproduce the analysis:

```bash
pip install -r requirements.txt
```

Then run the notebooks in numerical order.

---

## Key Findings (Brief)

* The first principal component is dominated by **perceived stress**, **neuroticism**, and **self-monitoring**
* PCA structure is **highly stable under bootstrap resampling**
* Secondary components show acceptable but lower stability, consistent with theory

---

## Citation

If you use or reference this work, please cite the accompanying paper (details to be added upon publication).

---

## Contact

For questions or collaboration inquiries, please open an issue or contact the author via GitHub.
