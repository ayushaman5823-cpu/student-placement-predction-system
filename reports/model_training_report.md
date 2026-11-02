# Phase 2: Machine Learning Model Training & Evaluation Report

## Executive Summary

Phase 2 completed comprehensive model training and evaluation for the Student Placement Prediction System.
A total of **7 classification algorithms** were benchmarked using **5-fold stratified cross-validation** on the 4,000-student training dataset, followed by final evaluation on an untouched 1,000-student test set.

The optimal model selected is **Gradient Boosting**, achieving a **Test F1-Score of 0.8632**, **Test ROC-AUC of 0.9036**, and **Test Accuracy of 0.8310**.

> [!IMPORTANT]
> **Dataset Limitation Warning**: The dataset utilized is synthetic/augmented. Model performance achieved on this dataset does not establish real-world placement prediction accuracy across actual institutional environments.

---

## 1. Dataset & Feature Configuration

- **Dataset Used**: `data/raw/student_prediction_5000_with_probability.csv`
- **Total Records**: 5,000 (4,000 Train / 1,000 Test stratified 80/20 split, `random_state=42`)
- **Target Variable**: `Placement_Status` (`Placed` vs `Not Placed`)

### Included ML Features (9 Features)
- **Categorical Features (2)**: `Branch`, `College_Tier`
- **Numerical Features (7)**: `10th_Percentage`, `12th_Percentage`, `Current_CGPA`, `Backlogs`, `Attendance_Percentage`, `Projects`, `Internships`

### Excluded Columns (5 Columns)
- `Student_ID` (Identifier)
- `Name` (Identifier)
- `Gender` (Excluded from feature set)
- `College_Name` (Excluded from feature set)
- `Placement_Probability` (Reference column only — strictly excluded from input features)

---

## 2. Preprocessing & Modeling Pipeline

The entire workflow is encapsulated in an end-to-end `sklearn.pipeline.Pipeline` object:
1. **Categorical Feature Preprocessing**: `OneHotEncoder(handle_unknown='ignore', sparse_output=False)` applied to `Branch` and `College_Tier`.
2. **Numerical Feature Preprocessing**: `StandardScaler()` applied to all 7 continuous/discrete numerical features.
3. **Classifier**: `Gradient Boosting` classifier.

The complete pipeline is serialized to `models/best_model.pkl` so that raw feature dataframes containing the 9 raw features can be passed directly to `.predict()` and `.predict_proba()`.

---

## 3. Model Benchmark & Cross-Validation Results

All models were evaluated across 5 stratified folds on the 4,000-sample training data.

### 5-Fold Cross-Validation & Test Metrics Summary

| Model                  |   CV_F1_Mean |   CV_ROC_AUC_Mean |   CV_Recall_Mean |   CV_Precision_Mean |   CV_Accuracy_Mean |   Test_F1_Score |   Test_ROC_AUC |   Test_Recall |   Test_Precision |   Test_Accuracy |   Test_Brier_Score |
|:-----------------------|-------------:|------------------:|-----------------:|--------------------:|-------------------:|----------------:|---------------:|--------------:|-----------------:|----------------:|-------------------:|
| Gradient Boosting      |     0.864602 |          0.912179 |         0.905732 |            0.827471 |            0.83225 |        0.863158 |       0.903599 |      0.901861 |         0.82764  |           0.831 |           0.115767 |
| Random Forest          |     0.858907 |          0.905356 |         0.887985 |            0.831952 |            0.8275  |        0.859706 |       0.896131 |      0.891709 |         0.829921 |           0.828 |           0.118493 |
| XGBoost                |     0.856987 |          0.894531 |         0.887567 |            0.828665 |            0.82475 |        0.843314 |       0.881875 |      0.869712 |         0.818471 |           0.809 |           0.140353 |
| Support Vector Machine |     0.84067  |          0.867562 |         0.874042 |            0.809961 |            0.804   |        0.84634  |       0.864525 |      0.890017 |         0.806748 |           0.809 |           0.141147 |
| Decision Tree          |     0.807512 |          0.768262 |         0.800919 |            0.814417 |            0.77425 |        0.80789  |       0.771338 |      0.796954 |         0.81913  |           0.776 |           0.224    |
| K-Nearest Neighbors    |     0.80594  |          0.795267 |         0.876156 |            0.746344 |            0.7505  |        0.807339 |       0.788833 |      0.893401 |         0.736402 |           0.748 |           0.18     |
| Logistic Regression    |     0.799686 |          0.815476 |         0.830086 |            0.771839 |            0.754   |        0.800327 |       0.812617 |      0.827411 |         0.77496  |           0.756 |           0.167757 |

---

## 4. Best Model Selection & Test Set Performance

### Selected Winner: **Gradient Boosting**
- **Test Accuracy**: 83.10%
- **Test Precision**: 82.76%
- **Test Recall**: 90.19%
- **Test F1-Score**: 0.8632
- **Test ROC-AUC**: 0.9036
- **Test Brier Score**: 0.1158

### Confusion Matrix Interpretation (Gradient Boosting)
- **True Negatives (Not Placed correctly predicted)**: 298
- **False Positives (Predicted Placed, actually Not Placed)**: 111
- **False Negatives (Predicted Not Placed, actually Placed)**: 58
- **True Positives (Placed correctly predicted)**: 533

---

## 5. Probability Generation & Calibration Audit

- **Probability Source**: Generated dynamically via `model.predict_proba()` from the trained Scikit-Learn Pipeline. No synthetic or pre-existing probability column is utilized.
- **Brier Score**: `0.1158` (lower indicates well-calibrated probabilities).
- **Calibration Status**: Gradient Boosting produces naturally smooth and well-calibrated class probabilities across the 0% to 100% range without requiring isotonic or sigmoid post-hoc probability calibration.

---

## 6. Synthetic Dataset Limitations

The dataset is synthetic/augmented. High performance metrics on this synthetic dataset reflect the underlying pattern generation logic rather than real-world employment prediction capability. Deployment in production should involve retraining on actual institutional placement records.

---

## 7. Generated Artifacts

- **Trained Pipeline**: `models/best_model.pkl`
- **Comparison Table**: `reports/model_comparison.csv`
- **Test Predictions**: `reports/test_predictions.csv`
- **Visualizations**:
  - `reports/model_comparison.png`
  - `reports/roc_curve_comparison.png`
  - `reports/confusion_matrix_gradient_boosting.png`
