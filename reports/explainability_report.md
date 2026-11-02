# Model Explainability & Final Prediction Engine Report
**Student Placement Prediction System — SRM Institute of Science and Technology**

## Executive Summary

This report establishes model explainability analysis for the frozen production **Gradient Boosting Classifier** (`models/best_model.pkl`, SHA-256 `7330783a64173b5dadb941cc4c1342b9d89733dd63c951e151705e52a2acca17`) and documents the operational prediction engine (`src/predict.py`).

---

## 1. Feature Importance Methodology: Gini Impurity vs. Permutation Importance

The system distinguishes between two fundamental feature importance methodologies:

### A. Gini Impurity (Mean Decrease in Impurity — MDI)
- **Methodology**: Computed natively from the tree split impurity reductions across all decision trees in the Gradient Boosting ensemble.
- **Aggregation**: Preprocessing includes one-hot encoding for `Branch` (10 columns) and `College_Tier` (3 columns). The transformed importances are mapped back to their original 9 feature groups by summing one-hot components.
- **Characteristics**: Fast and structural; reflects tree split frequency and node purity improvement.

### B. Permutation Feature Importance
- **Methodology**: Evaluates holdout test performance degradation when a single feature's column is randomly shuffled, breaking its relationship with the target while preserving feature distribution.
- **Characteristics**: Model-agnostic and robust against cardinally biased trees; retained as an independent audited methodology.

---

## 2. Gini Feature Importance Ranking (Aggregated by Original Features)

Feature importances computed directly from Gini impurity reduction across all trees in `models/best_model.pkl`:

| Original_Feature      |   Importance |   Importance_Pct |
|:----------------------|-------------:|-----------------:|
| Attendance_Percentage |   0.578000   |            57.80%|
| Current_CGPA          |   0.145346   |            14.53%|
| 12th_Percentage       |   0.124110   |            12.41%|
| 10th_Percentage       |   0.072678   |             7.27%|
| Backlogs              |   0.048790   |             4.88%|
| Internships           |   0.012755   |             1.28%|
| Projects              |   0.009431   |             0.94%|
| College_Tier          |   0.006039   |             0.60%|
| Branch                |   0.002852   |             0.29%|

### Key Empirical Drivers:
1. **`Attendance_Percentage` (57.80%)**: The single most influential determinant. In Phase 1 EDA, attendance < 75% yielded a hard 0% placement rate. The model learned this threshold cleanly.
2. **`Current_CGPA` (14.53%)**: The primary academic performance metric driving placement likelihood.
3. **`12th_Percentage` (12.41%) & `10th_Percentage` (7.27%)**: Secondary screening criteria.
4. **`Backlogs` (4.88%)**: Represents academic risk and penalizes placement probability.

---

## 3. Probability and Confidence Semantics

The prediction engine outputs model-estimated class probabilities via `pipeline.predict_proba()`:

- **`probability_placed`**: The classifier probability estimate for class `Placed`, expressed as a percentage ($0.0\%$ to $100.0\%$).
- **`probability_not_placed`**: The classifier probability estimate for class `Not Placed`, expressed as a percentage ($0.0\%$ to $100.0\%$).
- **`confidence_score`**: Defined strictly as $\max(\text{probability\_placed}, \text{probability\_not\_placed})$.
  > [!NOTE]
  > The `confidence_score` represents the highest class probability output by the model. It is **NOT** a calibrated Bayesian posterior, a statistical confidence interval, or an absolute guarantee of campus placement.

---

## 4. Methodological Limitations: Correlation vs. Causation

> [!WARNING]
> **Statistical Limitations**:
> 1. **Tree Impurity / Gain Metrics**: Feature importance measures how frequently and effectively a feature is used to split nodes in the tree ensemble. It does **NOT** establish causal mechanisms.
> 2. **Synthetic Data Artifacts**: Correlation structures in synthetic datasets reflect generator rules.
> 3. **Non-Causal Interventions**: Increasing attendance or project count alone will not automatically produce job offers if academic cutoff thresholds are missed.

---

## 5. Operational Verification (5 Sample Profiles)

The prediction engine was verified against 5 diverse student profiles using the frozen production pipeline `models/best_model.pkl`:

| Profile_Name            | predicted_status   |   probability_placed |   probability_not_placed |   confidence_score | Status |
|:------------------------|:-------------------|---------------------:|-------------------------:|-------------------:|:------:|
| Strong Academic Profile | Placed             |                97.05%|                     2.95%|              97.05%| PASSED |
| Average Profile         | Placed             |                90.64%|                     9.36%|              90.64%| PASSED |
| Weak Academic Profile   | Not Placed         |                 3.60%|                    96.40%|              96.40%| PASSED |
| High Backlog Profile    | Not Placed         |                43.42%|                    56.58%|              56.58%| PASSED |
| Tier 3 College Profile  | Placed             |                94.87%|                     5.13%|              94.87%| PASSED |

### High-Backlog Profile Reconciliation Note:
An earlier draft report contained a $4.76\%$ placement probability for the High Backlog Profile (`IT, Tier 2, 10th: 74%, 12th: 72%, CGPA: 7.20, Backlogs: 5, Attendance: 80%, Projects: 2, Internships: 1`).
Direct execution against the frozen production model artifact (`models/best_model.pkl`) definitively confirmed that the frozen model outputs **`43.42%` Placed** and **`56.58%` Not Placed** (`Not Placed`). The historical $4.76\%$ figure was an unverified prototype placeholder that has been reconciled to the verified model output.

---

## 6. Artifact Paths Generated

- **Prediction Module**: `src/predict.py`
- **Feature Importance Table**: `reports/feature_importance.csv`
- **Feature Importance Chart**: `reports/feature_importance.png`
- **Explainability Report**: `reports/explainability_report.md`
