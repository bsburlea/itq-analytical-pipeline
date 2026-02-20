# Metadata Specification

This document defines the **semantic meaning, constraints, and frozen rules**
governing the metadata file used in this project.

The metadata is treated as a **contract**, not a convenience table.

---

## 1. Metadata File

* File: `data/metadata.csv`
* Purpose: define conceptual structure and questionnaire-to-construct mapping

---

## 2. Column Definitions (Frozen)

### `old_name`

* Represents a **single questionnaire item**
* Corresponds directly to a column in `sample_raw.csv`
* Must be unique at the questionnaire-item level

---

### `feature`

* Represents a **latent construct or scale**
* May map to one or multiple questionnaire items
* Used as the unit of analysis and modeling

---

### `sub_cluster`

* Intermediate conceptual grouping
* Used for organizational clarity
* Not used directly in modeling

---

### `cluster`

* High-level domain grouping
* Examples:

  * Personality
  * Work Environment
  * Political Skills
  * Intention to Quit

---

## 3. Mapping Rules (Frozen)

* Many `old_name` → one `feature`
* One `old_name` → exactly one `feature`
* No identifier fields are allowed
* No aggregation occurs in metadata

---

## 4. Identifier Policy (Frozen)

* Identifiers (e.g. IP addresses) are explicitly excluded
* Metadata is guaranteed to be identifier-free
* Any identifier handling occurs **outside** metadata

---

## 5. Single-Item Constructs

* Some features consist of a single item
* These are retained intentionally
* Limitations are documented at the analysis and paper level

---

## 6. Validation Expectations

Any valid metadata file must satisfy:

* All `old_name` values exist in the raw data
* No duplicate `(old_name, feature)` pairs
* No identifier leakage
* Consistent cluster labeling

---

## 7. Frozen Status

This metadata specification is **frozen**.

Any change requires:

* explicit justification
* versioned metadata
* documented impact on analysis
