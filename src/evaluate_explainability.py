import os
import joblib
import pandas as pd
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from predict import StudentPlacementPredictor, REQUIRED_FEATURES

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "best_model.pkl")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

os.makedirs(REPORTS_DIR, exist_ok=True)

# 1. Load trained pipeline
pipeline = joblib.load(MODEL_PATH)
preprocessor = pipeline.named_steps['preprocessor']
classifier = pipeline.named_steps['classifier']

# Extract feature names after OneHotEncoder and StandardScaler
cat_transformer = preprocessor.named_transformers_['cat']
cat_cols = ['Branch', 'College_Tier']
cat_feature_names = cat_transformer.get_feature_names_out(cat_cols).tolist()

num_cols = ['10th_Percentage', '12th_Percentage', 'Current_CGPA', 'Backlogs', 'Attendance_Percentage', 'Projects', 'Internships']

transformed_feature_names = cat_feature_names + num_cols
importances = classifier.feature_importances_

# Create individual feature importance dataframe
df_importance_indiv = pd.DataFrame({
    'Transformed_Feature': transformed_feature_names,
    'Importance': importances
}).sort_values(by='Importance', ascending=False).reset_index(drop=True)

# Map back to original 9 features by grouping
def get_original_feature_name(t_name):
    for col in REQUIRED_FEATURES:
        if t_name.startswith(col):
            return col
    return t_name

df_importance_indiv['Original_Feature'] = df_importance_indiv['Transformed_Feature'].apply(get_original_feature_name)

df_importance_grouped = df_importance_indiv.groupby('Original_Feature')['Importance'].sum().reset_index()
df_importance_grouped['Importance_Pct'] = np.round(df_importance_grouped['Importance'] * 100, 2)
df_importance_grouped = df_importance_grouped.sort_values(by='Importance', ascending=False).reset_index(drop=True)

# Save reports/feature_importance.csv
csv_path = os.path.join(REPORTS_DIR, "feature_importance.csv")
df_importance_grouped.to_csv(csv_path, index=False)
print(f"Saved feature importance table to {csv_path}")

# Generate reports/feature_importance.png plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Plot 1: Grouped original 9 features
sns.barplot(
    data=df_importance_grouped,
    x='Importance_Pct',
    y='Original_Feature',
    palette='viridis',
    ax=ax1
)
ax1.set_title('Aggregated Feature Importance by Original Feature (Gradient Boosting)')
ax1.set_xlabel('Importance (%)')
ax1.set_ylabel('Original Feature')
for p in ax1.patches:
    width = p.get_width()
    ax1.annotate(f'{width:.2f}%', (width + 0.5, p.get_y() + p.get_height() / 2.),
                 ha='left', va='center', fontsize=10)

# Plot 2: Top 10 transformed features
df_top10 = df_importance_indiv.head(10).copy()
df_top10['Importance_Pct'] = np.round(df_top10['Importance'] * 100, 2)
sns.barplot(
    data=df_top10,
    x='Importance_Pct',
    y='Transformed_Feature',
    palette='magma',
    ax=ax2
)
ax2.set_title('Top 10 One-Hot & Scaled Feature Importances')
ax2.set_xlabel('Importance (%)')
ax2.set_ylabel('Transformed Feature')
for p in ax2.patches:
    width = p.get_width()
    ax2.annotate(f'{width:.2f}%', (width + 0.3, p.get_y() + p.get_height() / 2.),
                 ha='left', va='center', fontsize=9)

plt.tight_layout()
png_path = os.path.join(REPORTS_DIR, "feature_importance.png")
plt.savefig(png_path, dpi=300)
plt.close()
print(f"Saved feature importance plot to {png_path}")

# 2. Run Sample Predictions on 5 Student Profiles using src/predict.py
predictor = StudentPlacementPredictor(model_path=MODEL_PATH)

sample_profiles = [
    {
        "Profile_Name": "Strong Academic Profile",
        "Description": "High CGPA (9.20), high attendance (92%), 0 backlogs, CSE Tier 1",
        "data": {
            "Branch": "CSE",
            "College_Tier": "Tier 1",
            "10th_Percentage": 92.0,
            "12th_Percentage": 90.0,
            "Current_CGPA": 9.20,
            "Backlogs": 0,
            "Attendance_Percentage": 92.0,
            "Projects": 4,
            "Internships": 2
        }
    },
    {
        "Profile_Name": "Average Profile",
        "Description": "Moderate CGPA (7.60), 82% attendance, 1 backlog, ECE Tier 2",
        "data": {
            "Branch": "ECE",
            "College_Tier": "Tier 2",
            "10th_Percentage": 75.0,
            "12th_Percentage": 74.0,
            "Current_CGPA": 7.60,
            "Backlogs": 1,
            "Attendance_Percentage": 82.0,
            "Projects": 2,
            "Internships": 1
        }
    },
    {
        "Profile_Name": "Weak Academic Profile",
        "Description": "Low CGPA (5.80), 10th <60%, 12th <60%, 2 backlogs, Civil Tier 3",
        "data": {
            "Branch": "Civil",
            "College_Tier": "Tier 3",
            "10th_Percentage": 58.0,
            "12th_Percentage": 56.0,
            "Current_CGPA": 5.80,
            "Backlogs": 2,
            "Attendance_Percentage": 78.0,
            "Projects": 1,
            "Internships": 0
        }
    },
    {
        "Profile_Name": "High Backlog Profile",
        "Description": "5 Active Backlogs, CGPA 7.20, IT Tier 2, 80% attendance",
        "data": {
            "Branch": "IT",
            "College_Tier": "Tier 2",
            "10th_Percentage": 74.0,
            "12th_Percentage": 72.0,
            "Current_CGPA": 7.20,
            "Backlogs": 5,
            "Attendance_Percentage": 80.0,
            "Projects": 2,
            "Internships": 1
        }
    },
    {
        "Profile_Name": "Tier 3 College Profile",
        "Description": "High CGPA (8.40), 0 backlogs, Tier 3 Mechanical, 88% attendance",
        "data": {
            "Branch": "Mechanical",
            "College_Tier": "Tier 3",
            "10th_Percentage": 82.0,
            "12th_Percentage": 80.0,
            "Current_CGPA": 8.40,
            "Backlogs": 0,
            "Attendance_Percentage": 88.0,
            "Projects": 3,
            "Internships": 1
        }
    }
]

prediction_results = []
print("\n--- Phase 3: Sample Student Predictions ---")
for p in sample_profiles:
    res = predictor.predict_student(p["data"])
    res["Profile_Name"] = p["Profile_Name"]
    res["Description"] = p["Description"]
    prediction_results.append(res)
    print(f"[{p['Profile_Name']}] -> Status: {res['predicted_status']} | Placed Prob: {res['probability_placed']}% | Not Placed Prob: {res['probability_not_placed']}%")

df_sample_preds = pd.DataFrame(prediction_results)

# 3. Generate reports/explainability_report.md
report_md = f"""# Phase 3: Model Explainability & Final Prediction Engine Report

## Executive Summary

Phase 3 establishes the operational prediction engine (`src/predict.py`) and completes model explainability analysis for the trained **Gradient Boosting Classifier** (`models/best_model.pkl`).

---

## 1. Feature Importance Ranking (Aggregated by Original Features)

Feature importances were computed directly from Gini impurity reduction across all decision trees in the Gradient Boosting ensemble and aggregated back to the 9 input features:

{df_importance_grouped.to_markdown(index=False)}

### Key Feature Drivers:
1. **`Attendance_Percentage` ({df_importance_grouped.loc[df_importance_grouped['Original_Feature']=='Attendance_Percentage', 'Importance_Pct'].values[0]:.2f}%)**: Identified as the single most influential determinant. This strongly aligns with Phase 1 EDA where Attendance < 75% resulted in a hard 0% placement rate.
2. **`Current_CGPA` ({df_importance_grouped.loc[df_importance_grouped['Original_Feature']=='Current_CGPA', 'Importance_Pct'].values[0]:.2f}%)**: The primary academic performance metric driving placement likelihood.
3. **`12th_Percentage` ({df_importance_grouped.loc[df_importance_grouped['Original_Feature']=='12th_Percentage', 'Importance_Pct'].values[0]:.2f}%) & `10th_Percentage` ({df_importance_grouped.loc[df_importance_grouped['Original_Feature']=='10th_Percentage', 'Importance_Pct'].values[0]:.2f}%)**: Secondary academic screening criteria.
4. **`Backlogs` ({df_importance_grouped.loc[df_importance_grouped['Original_Feature']=='Backlogs', 'Importance_Pct'].values[0]:.2f}%)**: Represents academic risk and penalizes placement probability.

---

## 2. Alignment with Phase 1 Exploratory Data Analysis (EDA)

- **Attendance Filter**: Phase 1 EDA revealed that 948 students with <75% attendance had 0 placements. The model learned this constraint cleanly through high feature weighting on `Attendance_Percentage`.
- **Academic CGPA Cutoff**: Phase 1 EDA showed a steep rise in placement rate for CGPA â‰¥ 7.0 (66.06% vs 35.94%), matching CGPA's high rank in feature importance.
- **Backlog Penalty**: Monotonic decrease in placement rate as backlog count increases from 0 to 5 in Phase 1 EDA matches the negative influence captured by the tree splits.

---

## 3. Methodological Limitations: Correlation vs. Causation

> [!WARNING]
> **Important Statistical Caveat**:
> 1. **Tree Impurity / Gain Metrics**: Feature importance measures how frequently and effectively a feature is used to split nodes in the tree ensemble. It does **NOT** measure causal impact.
> 2. **Synthetic Data Artifacts**: Correlation structures in synthetic datasets reflect generator rules.
> 3. **Non-Causal Advice**: Increasing attendance or project count alone will not automatically guarantee job placement if underlying academic qualifications remain below corporate cutoff criteria.

---

## 4. Operational Test Suite (5 Sample Profiles)

The prediction engine `src/predict.py` was tested against 5 distinct student profiles:

{df_sample_preds[['Profile_Name', 'predicted_status', 'probability_placed', 'probability_not_placed', 'confidence_score']].to_markdown(index=False)}

---

## 5. Artifact Paths Generated

- **Prediction Module**: `src/predict.py`
- **Feature Importance Table**: `reports/feature_importance.csv`
- **Feature Importance Chart**: `reports/feature_importance.png`
- **Explainability Report**: `reports/explainability_report.md`
"""

report_path = os.path.join(REPORTS_DIR, "explainability_report.md")
with open(report_path, "w", encoding="utf-8") as f:
    f.write(report_md)

print(f"Saved explainability report to {report_path}")
print("\n--- PHASE 3 COMPLETED SUCCESSFULLY ---")

