# Local Setup, Execution, and Testing Guide
## Student Placement Prediction System — SRM Institute of Science and Technology

This guide provides exact commands to set up, run, and test the Student Placement Prediction System from a fresh extraction without pre-existing environment dependencies.

---

## 1. Prerequisites

- **Python**: Version `3.12.4` (Target runtime recorded in `.python-version`)
- **Operating System**: Windows (PowerShell), macOS, or Linux
- **Package Manager**: `pip` (bundled with Python)

---

## 2. Environment Setup

### Option A: Windows (PowerShell)

```powershell
# 1. Open PowerShell and navigate to the project directory
cd Student_Placement_Prediction_Shared_Final

# 2. Create an isolated virtual environment using Python 3.12.4
py -3.12 -m venv .venv

# 3. Activate the virtual environment
.venv\Scripts\Activate.ps1

# 4. Upgrade pip
python -m pip install --upgrade pip

# 5. Install exact runtime dependencies from lockfile
python -m pip install -r requirements-runtime.lock

# (Optional) Install exact development & testing dependencies
python -m pip install -r requirements-dev.lock

# (Optional) Install offline retraining dependencies (e.g., XGBoost)
# python -m pip install -r requirements-optional-ml.txt
```

### Option B: macOS / Linux (bash/zsh)

```bash
# 1. Open terminal and navigate to the project directory
cd Student_Placement_Prediction_Shared_Final

# 2. Create an isolated virtual environment using Python 3.12.4
python3.12 -m venv .venv

# 3. Activate the virtual environment
source .venv/bin/activate

# 4. Upgrade pip
python -m pip install --upgrade pip

# 5. Install exact runtime dependencies from lockfile
python -m pip install -r requirements-runtime.lock

# (Optional) Install exact development & testing dependencies
python -m pip install -r requirements-dev.lock

# (Optional) Install offline retraining dependencies (e.g., XGBoost)
# python -m pip install -r requirements-optional-ml.txt
```

---

## 3. Running the Full-Stack Application (React + FastAPI)

### Option A: 1-Click Launch (Windows)
Double-click `run_app.bat` or run:
```powershell
.\run_app.ps1
```
This automatically starts the FastAPI backend, the React Vite server, and opens your browser.

### Option B: Manual Multi-Process Launch

#### Terminal 1 — FastAPI Backend Service:
```powershell
# Activate python environment
python -m uvicorn api.app:app --host 127.0.0.1 --port 8000 --reload
```
- API Base: `http://127.0.0.1:8000`
- Interactive OpenAPI / Swagger UI: `http://127.0.0.1:8000/docs`

#### Terminal 2 — React Frontend UI:
```powershell
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```
- Web Application: `http://127.0.0.1:5173`

---

## 4. Running the Interactive Terminal Application

Launch the CLI application:

```bash
python src/terminal_app.py
```

### Interactive Workflow:
1. View the opening banner and press **ENTER**.
2. Select **`[1] Enter Student Details & Predict Placement`**.
3. Complete the 9-step guided feature form:
   - Branch selection (`1` to `10`)
   - College Tier selection (`1` to `3`)
   - 10th Percentage (`0.0` to `100.0`)
   - 12th Percentage (`0.0` to `100.0`)
   - Current CGPA (`0.0` to `10.0`)
   - Backlogs count (`0` to `5`)
   - Attendance Percentage (`0.0` to `100.0`)
   - Projects count (`0` to `5`)
   - Internships count (`0` to `4`)
4. Review the confirmation summary screen.
5. Choose **`[1] Confirm & Predict`** to see placement class (`Placed` / `Not Placed`) and model probability outputs.

---

## 4. Running the Automated Test Suite

### Full Test Suite with Pytest (Recommended)

```bash
pytest -v
```

Expected output:
```text
tests/test_inference.py::TestPlacementPredictionSystem::test_01_model_artifact_integrity PASSED
tests/test_inference.py::TestPlacementPredictionSystem::test_02_feature_contract PASSED
tests/test_inference.py::TestPlacementPredictionSystem::test_03_single_student_prediction_contract PASSED
tests/test_inference.py::TestPlacementPredictionSystem::test_04_batch_fixtures_json PASSED
tests/test_inference.py::TestPlacementPredictionSystem::test_05_batch_dataframe_fixtures_csv PASSED
tests/test_inference.py::TestPlacementPredictionSystem::test_06_missing_required_feature_raises_error PASSED
tests/test_validation.py::TestInputValidation::test_01_valid_profile_passes PASSED
...
tests/test_history_store.py::TestHistoryStore::test_01_init_db PASSED
...
tests/test_training_protection.py::TestTrainingOutputProtection::test_01_default_output_targets_candidate_directory PASSED
...
============================= 30 passed in 3.5s ==============================
```

### Running Individual Test Modules via Built-in Python Runner:

```bash
python tests/test_model_info.py
python tests/test_inference.py
python tests/test_validation.py
python tests/test_history_store.py
python tests/test_training_protection.py
```

---

## 5. Generating Feature Importance & Explainability Reports

To regenerate feature importance charts and CSV summaries using the frozen model:

```bash
python src/evaluate_explainability.py
```

Outputs generated in `reports/`:
- `reports/feature_importance.csv`
- `reports/feature_importance.png`

---

## 6. Deactivating the Environment

```bash
deactivate
```
