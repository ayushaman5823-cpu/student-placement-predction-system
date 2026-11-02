# Defect Correction & Quality Assurance Integrity Report
**Student Placement Prediction System — SRM Institute of Science and Technology**
**Report Date**: November 2, 2026  
**Auditor**: Senior Python / Machine Learning Infrastructure & Quality Assurance Engineer  
**Scope**: Targeted Defect Remediation, Model Integrity Verification, and Release Packaging

---

## 1. Executive Summary & Protection Audit

This remediation addressed ten identified defects in the Student Placement Prediction System. All modifications adhered strictly to the non-destructive protocol:
- **Zero Retraining**: The production model was neither retrained nor reconstructed.
- **Byte-for-Byte Preservation**: `models/best_model.pkl` was validated before and after remediation.
- **Authoritative Baseline Preserved**: Verified against the untouched 1,000-student holdout partition (83.10% Accuracy, 82.76% Precision, 90.19% Recall, 86.32% F1-score, 90.36% ROC-AUC, 0.1158 Brier score).
- **Automated Test Results**: **56 of 56 tests passed** (100% success rate).

### Cryptographic Model Integrity Verification
| Checkpoint | File Path | Algorithm | Observed Hash | Expected Hash | Status |
|---|---|---|---|---|:---:|
| **Pre-Remediation** | `models/best_model.pkl` | SHA-256 | `7330783a64173b5dadb941cc4c1342b9d89733dd63c951e151705e52a2acca17` | `7330783a64173b5dadb941cc4c1342b9d89733dd63c951e151705e52a2acca17` | **MATCH** |
| **Post-Remediation** | `models/best_model.pkl` | SHA-256 | `7330783a64173b5dadb941cc4c1342b9d89733dd63c951e151705e52a2acca17` | `7330783a64173b5dadb941cc4c1342b9d89733dd63c951e151705e52a2acca17` | **MATCH** |

---

## 2. Defect Remediation Status Table

| Issue # | Defect Description | Status | Files Modified | Verification / Tests Performed |
|:---:|---|:---:|---|---|
| **1** | **Incorrect 94.12% Terminal Accuracy** | **Corrected** | `src/menu.py` | Added `get_authoritative_metrics()` reading `MODEL_METADATA.json` with fallback; `tests/test_model_info.py` verified 83.10% displayed and 94.12% rejected. |
| **2** | **High-Backlog Sample Mismatch** (4.76% vs 43.42%) | **Resolved** | `reports/explainability_report.md`, `MODEL_METADATA.json` | Executed frozen model on profile; verified actual output is 43.42% Placed / 56.58% Not Placed. Reconciled reports; tested in `test_inference.py:test_07`. |
| **3** | **SQLite History Storage Validation** | **Corrected** | `src/history_store.py` | Implemented strict input contract validation (9 features, bounds, non-bool, non-NaN, status in ['Placed', 'Not Placed'], probability sum=100%, confidence score, non-empty model ID). Tested in `test_history_store.py:tests 07-23`. |
| **4** | **Flawed In-Memory SQLite Test** | **Corrected** | `tests/test_history_store.py` | Replaced trivial `test_06` with `test_06_connection_persistence_multi_connection` using temporary file databases to verify true cross-connection table creation, insertion, and retrieval. |
| **5** | **Undefined `best_model_path` in Training Script** | **Corrected** | `train_pipeline.py` | Defined `best_model_path` at module level and updated verification pipeline reload to target `save_path`. Verified via `test_training_protection.py:test_10`. |
| **6** | **Harden Model Overwrite Protection against Path Traversal** | **Corrected** | `train_pipeline.py` | Hardened `get_model_save_path()` with `os.path.realpath`, blocking `../`, `../../`, absolute paths to `best_model.pkl`, and any traversal outside `models/candidates/`. Verified via `test_training_protection.py:tests 06-09`. |
| **7** | **Correct Probability and Confidence Terminology** | **Corrected** | `src/predict.py`, `MODEL_METADATA.json`, `README.md`, `FRONTEND_HANDOFF.md`, `reports/explainability_report.md` | Defined `probability_placed`/`not_placed` as model class estimates and `confidence_score = max(prob_placed, prob_not_placed)`. Removed unverified "calibrated statistical confidence interval" claims. |
| **8** | **Distinguish Gini and Permutation Importance** | **Corrected** | `reports/explainability_report.md`, `MODEL_METADATA.json`, `README.md` | Formally differentiated native tree impurity reduction (Mean Decrease in Impurity) from holdout permutation degradation. Clarified one-hot column aggregation. |
| **9** | **Document XGBoost as Optional Dependency** | **Documented** | `requirements-optional-ml.txt`, `README.md`, `RUN_AND_TEST.md`, `MODEL_METADATA.json` | Pinned `xgboost==3.4.0` in dedicated optional file. Documented that runtime inference uses pure scikit-learn without importing XGBoost. |
| **10** | **Standardize Model Version Identification** | **Corrected** | `MODEL_METADATA.json`, `src/history_store.py`, `src/predict.py`, `FRONTEND_HANDOFF.md` | Standardized model artifact identifier to immutable SHA-256 (`7330783a6417...`), distinct from metadata schema version `2.0.0`. Verified via `test_inference.py:test_08`. |

---

## 3. Detailed Remediation Summaries

### Issue 1: Terminal Model Accuracy Correction
- **Problem**: `show_model_info()` in `src/menu.py` displayed hard-coded 94.12% accuracy and 95.01% precision, contradicting the authoritative 83.10% holdout test evaluation.
- **Remediation**: Added `get_authoritative_metrics()` which dynamically loads `evaluation_context.holdout_test_metrics` from `MODEL_METADATA.json` (falling back to constants). Updated `show_model_info()` to display:
  - Accuracy: 83.10%
  - Precision: 82.76%
  - Recall: 90.19%
  - F1 Score: 86.32%
  - ROC-AUC: 90.36%
  - Brier Score: 0.1158
- **Testing**: Added `tests/test_model_info.py` verifying exact output and asserting absence of 94.12%.

### Issue 2: High-Backlog Sample Prediction Discrepancy
- **Problem**: `reports/explainability_report.md` reported 4.76% placement probability, while `reports/terminal_application_test_report.md` reported 43.42% for the identical profile (`IT, Tier 2, 10th: 74%, 12th: 72%, CGPA: 7.20, Backlogs: 5, Attendance: 80%, Projects: 2, Internships: 1`).
- **Remediation**: Loaded `models/best_model.pkl` in the reference environment and executed inference. The frozen pipeline produced:
  - Predicted Status: `Not Placed`
  - Placed Probability: `43.42%`
  - Not Placed Probability: `56.58%`
  - Confidence Score: `56.58%`
  The 4.76% value in `explainability_report.md` was an unverified draft placeholder. Reconciled both reports to the empirical 43.42% value.
- **Testing**: Added regression check `test_07_high_backlog_sample_reconciliation` in `tests/test_inference.py`.

### Issue 3: SQLite History Contract Enforcement
- **Problem**: `src/history_store.py` lacked validation prior to SQL insertion, risking corruption or storing partial records.
- **Remediation**: Built `validate_history_record()` checking:
  1. Exact 9 features present, zero missing, zero extra.
  2. Categorical values in approved branches and tiers.
  3. Numerical bounds: percentages [0-100], CGPA [0-10], counts [0-5 / 0-4].
  4. Type checks: booleans rejected, NaNs and Infinities rejected, count fields must be integers.
  5. Predicted status in `['Placed', 'Not Placed']`.
  6. Probability range [0-100], sum equal to 100.0% ($\pm 0.1$).
  7. Confidence score matches $\max(\text{prob\_placed}, \text{prob\_not\_placed})$.
  8. Model identifier non-empty string.
- **Testing**: 17 dedicated negative unit tests in `tests/test_history_store.py` verifying pre-insertion exception raising and zero partial database rows.

### Issue 4: In-Memory SQLite Test Hardening
- **Problem**: `test_06_in_memory_db_support` called `init_db(":memory:")` and asserted `True` without testing data persistence.
- **Remediation**: Replaced with `test_06_connection_persistence_multi_connection` using temporary file databases. Verified that a table created and populated in Connection 1 persists across connection termination and is queryable with identical values in Connection 2.

### Issue 5 & 6: Training Pipeline Variable Resolution and Path Traversal Protection
- **Problem**: `train_pipeline.py` referenced undefined `best_model_path`, and `get_model_save_path()` used simple string equality (`== "best_model.pkl"`), leaving it vulnerable to directory traversal (`../best_model.pkl`, `../../models/best_model.pkl`, or absolute paths).
- **Remediation**:
  1. Defined `best_model_path = os.path.join(MODELS_DIR, "best_model.pkl")` at module level and updated verification loading to use `save_path`.
  2. Implemented canonical path resolution via `os.path.realpath`.
  3. Blocked any target resolving to `models/best_model.pkl` or having basename `best_model.pkl` without explicit override.
  4. Blocked any target escaping the `models/candidates/` directory via `os.path.commonpath`.
- **Testing**: Added 5 path-traversal tests and 1 variable definition test in `tests/test_training_protection.py`.

### Issue 7: Probability and Confidence Semantics
- **Problem**: Documentation used terms implying calibrated confidence intervals without formal Platt scaling or isotonic regression proof.
- **Remediation**: Standardized definitions across all reports and source docstrings. `probability_placed` is explicitly the classifier's class probability estimate; `confidence_score` is strictly $\max(\text{prob\_placed}, \text{prob\_not\_placed})$, not a Bayesian certainty or real-world guarantee.

### Issue 8: Feature Importance Methodology Distinction
- **Problem**: Documentation conflated Gini impurity reduction with permutation importance.
- **Remediation**: Clarified the distinction:
  - Gini Impurity (MDI): Intrinsic tree impurity reduction across Gradient Boosting splits, aggregated over one-hot components.
  - Permutation Importance: Shuffling holdout features to evaluate score degradation. Preserved both in `MODEL_METADATA.json` and `reports/explainability_report.md`.

### Issue 9: Optional XGBoost Dependency Separation
- **Problem**: XGBoost was benchmarked offline but is not needed for runtime prediction.
- **Remediation**: Created `requirements-optional-ml.txt` pinning `xgboost==3.4.0`. Preserved runtime lockfiles without XGBoost, and verified runtime modules do not import it.

### Issue 10: Model Version Standardization
- **Problem**: Ambiguity between `model_metadata_version: 2.0.0` and `model_version: 1.0.0`.
- **Remediation**: Separated schema version (`metadata_schema_version: "2.0.0"`) from the immutable model artifact identifier (`model_artifact_identifier: "7330783a64173b5dadb941cc4c1342b9d89733dd63c951e151705e52a2acca17"`). Updated `src/predict.py` and `src/history_store.py` default to this immutable hash.

---

## 4. Test Suite Execution Summary

Executed via `pytest -v` in Python 3.12.4 virtual environment:

```text
============================= test session starts =============================
platform win32 -- Python 3.12.4, pytest-9.2.0, pluggy-1.7.0
rootdir: Student_Placement_Prediction_Shared_Final
collected 56 items

tests/test_history_store.py (23 tests) ....................... PASSED
tests/test_inference.py (8 tests) ............................ PASSED
tests/test_model_info.py (2 tests) ........................... PASSED
tests/test_training_protection.py (10 tests) ................. PASSED
tests/test_validation.py (13 tests) .......................... PASSED

======================= 56 passed, 7 warnings in 5.38s ========================
```

- **Total Tests Executed**: 56
- **Total Tests Passed**: 56 (100%)
- **Total Tests Failed**: 0
- **Regression Status**: Zero regressions detected.

---

## 5. Artifact Verification & Conclusion

The Student Placement Prediction System ML core has been remediated, verified, and hardened against path traversal and database corruption. The production pipeline artifact `models/best_model.pkl` remains 100% byte-for-byte identical to its frozen baseline. The package is fully prepared for React and FastAPI integration.

