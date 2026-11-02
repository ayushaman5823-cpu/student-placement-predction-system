# Student Placement Prediction System using Machine Learning
### SRM Institute of Science and Technology — Department of Computer Science & Engineering

A robust, portable, and reproducible distribution of the **Student Placement Prediction System**, engineered for local inference, centralized input validation, SQLite prediction history persistence, and seamless React frontend and FastAPI integration.

---

## 1. Executive Summary

- **Project Type**: B.Tech Academic Machine Learning Project.
- **Institution**: SRM Institute of Science and Technology.
- **Best Model Selected**: **Gradient Boosting Classifier** (Pipeline containing `OneHotEncoder`, `StandardScaler`, and `GradientBoostingClassifier`).
- **Production Artifact**: `models/best_model.pkl` (Cryptographic SHA-256: `7330783a64173b5dadb941cc4c1342b9d89733dd63c951e151705e52a2acca17`).
- **Candidate Algorithms Evaluated**: **7 model families** benchmarked via 5-Fold Stratified Cross-Validation on 4,000 training records:
  1. Gradient Boosting (Selected Best Model)
  2. Random Forest
  3. XGBoost
  4. Support Vector Machine
  5. Decision Tree
  6. K-Nearest Neighbors
  7. Logistic Regression
- **Authoritative Benchmark**: **83.10% Holdout Test Accuracy**, 86.32% F1-score, 90.36% ROC-AUC on the 1,000-sample test partition.
- **Inference & Execution Interfaces**:
  - Full-Stack React + Vite Web UI (`frontend/`)
  - Asynchronous FastAPI Backend Service (`api/app.py`)
  - Single-Command Launchers (`run_app.bat` and `run_app.ps1`)
  - Interactive Terminal CLI (`src/terminal_app.py`)
  - Programmatic Prediction API (`src/predict.py`)
  - SQLite Prediction History (`src/history_store.py`)
  - Automated Quality Assurance Suite (`tests/` — 63/63 passing tests)

> [!IMPORTANT]
> **Dataset Limitation Disclaimer**: The dataset utilized in training was synthetic/augmented. High model accuracy reflects the underlying synthetic pattern generation rules rather than real-world job market placement likelihood.

---

## 2. Model Input Contract & Centralized Validation

The prediction engine strictly requires **exactly nine features** in the specified order:

| # | Feature Name | Permitted Range / Values | Type |
|---|---|---|---|
| 1 | `Branch` | `'AI/ML'`, `'Biotechnology'`, `'Chemical'`, `'Civil'`, `'CSE'`, `'Data Science'`, `'ECE'`, `'EEE'`, `'IT'`, `'Mechanical'` | Categorical String |
| 2 | `College_Tier` | `'Tier 1'`, `'Tier 2'`, `'Tier 3'` | Categorical String |
| 3 | `10th_Percentage` | `0.0` to `100.0` | Numeric Float |
| 4 | `12th_Percentage` | `0.0` to `100.0` | Numeric Float |
| 5 | `Current_CGPA` | `0.0` to `10.0` | Numeric Float |
| 6 | `Backlogs` | `0` to `5` | Integer Count |
| 7 | `Attendance_Percentage` | `0.0` to `100.0` | Numeric Float |
| 8 | `Projects` | `0` to `5` | Integer Count |
| 9 | `Internships` | `0` to `4` | Integer Count |

### Centralized Validation Rule (`src/predict.py: validate_student_input`)
- Rejects missing required fields (`KeyError`).
- Rejects unauthorized or extraneous fields (`ValueError`) such as `Student_ID`, `Name`, `Gender`, `College_Name`, or `Placement_Probability`.
- Rejects values outside authorized ranges, fractional integer counts, booleans, NaNs, and infinities (`ValueError` / `TypeError`).

---

## 3. Probability and Confidence Semantics

Output returned by `StudentPlacementPredictor.predict_student()`:
```python
{
    "predicted_status": "Placed",          # 'Placed' or 'Not Placed'
    "probability_placed": 96.42,           # Model predict_proba() class 1 (%)
    "probability_not_placed": 3.58,        # Model predict_proba() class 0 (%)
    "confidence_score": 96.42,             # max(probability_placed, probability_not_placed)
    "model_version": "7330783a64173b5dadb941cc4c1342b9d89733dd63c951e151705e52a2acca17"
}
```

> [!NOTE]
> `confidence_score` is explicitly defined as `max(probability_placed, probability_not_placed)`. It reflects the model's highest binary class probability output, NOT a statistically calibrated confidence interval. Placement probability must not be interpreted as a guaranteed real-world job offer.

---

## 4. Feature Importance Methodology

- **Gini Importance (MDI)**: Intrinsic feature importance calculated from impurity reduction across decision trees in the Gradient Boosting ensemble. Aggregated back to 9 original features after one-hot encoding.
- **Permutation Importance**: Measures holdout score degradation when a specific feature is randomly permuted.
- Historical raw-column feature importance tables in early prototypes were marked invalid due to one-hot column alignment. The audited permutation results and visual charts in `reports/` are preserved separately.

---

## 5. Dependency Management & Installation

The package clearly separates broad compatibility specifications from exact pinned lockfiles:

- **Target Interpreter**: Python **`3.12.4`** (declared in `.python-version`).
- **`requirements.txt`**: Broad compatibility range specification.
- **`requirements-runtime.lock`**: Exact pinned runtime dependencies and transitives (scikit-learn 1.9.0).
- **`requirements-dev.txt` / `requirements-dev.lock`**: Development and testing dependencies (`pytest`, `matplotlib`, `seaborn`).
- **`requirements-optional-ml.txt`**: Optional dependencies for offline retraining or benchmarking experiments (`xgboost==3.4.0`). NOT required for runtime inference or terminal CLI.

### Setup with Exact Runtime Lock (Recommended)

#### Windows PowerShell
```powershell
# Create and activate virtual environment
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1

# Upgrade pip and install exact runtime lockfile
python -m pip install --upgrade pip
python -m pip install -r requirements-runtime.lock

# (Optional) Install exact development dependencies for pytest
python -m pip install -r requirements-dev.lock
```

#### macOS / Linux
```bash
# Create and activate virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# Upgrade pip and install exact runtime lockfile
python -m pip install --upgrade pip
python -m pip install -r requirements-runtime.lock

# (Optional) Install exact development dependencies for pytest
python -m pip install -r requirements-dev.lock
```

---

## 6. Running Application & Automated Tests

### 1-Click Full-Stack Launch (React + FastAPI)
Double-click `run_app.bat` or run in PowerShell:
```powershell
.\run_app.ps1
```
This automatically starts:
- **FastAPI Backend**: `http://127.0.0.1:8000` (Interactive Docs: `http://127.0.0.1:8000/docs`)
- **React Frontend**: `http://127.0.0.1:5173`
- Launches your default web browser to `http://127.0.0.1:5173`.

### Interactive Terminal CLI
```bash
python src/terminal_app.py
```

### Running Backend Independently
```bash
python -m uvicorn api.app:app --host 127.0.0.1 --port 8000 --reload
```

### Running Frontend Independently
```bash
cd frontend
npm install
npm run dev
```

### Automated Test Suite
Run all unit, integration, validation, persistence, API, and safety tests:
```bash
pytest -v
```
*(63 tests covering validation, model integrity, prediction logic, SQLite history, training protection, and FastAPI REST endpoints).*

---

## 7. Model Overwrite & Path Traversal Protection

To prevent accidental destruction or malicious overwriting of the frozen production model (`models/best_model.pkl`), `train_pipeline.py` enforces canonical path resolution:
- Default candidate destination: `models/candidates/`
- Direct attempts to overwrite `models/best_model.pkl` are blocked with `PermissionError`.
- Path traversal sequences (`../`, `../../`, absolute paths resolving to `best_model.pkl` or escaping `models/candidates/`) are strictly rejected.
- Override requires explicit `allow_production_overwrite=True` or `ALLOW_OVERWRITE_PRODUCTION_MODEL=1`.

---

## 8. Frontend & API Handoff

For full technical specifications on the upcoming React client, proposed FastAPI endpoints, campus network LAN setup, and prediction history access control, see [FRONTEND_HANDOFF.md](FRONTEND_HANDOFF.md).
