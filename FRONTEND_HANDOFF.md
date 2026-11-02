# Frontend & API Integration Specification
## Student Placement Prediction System — SRM Institute of Science and Technology

This document provides the technical integration specification for connecting the upcoming React frontend and FastAPI backend to the existing Python machine learning inference engine and SQLite prediction history storage.

---

## 1. Current State & Implementation Status

To prevent architectural ambiguity during frontend development, the implementation boundary is explicitly defined:

### Already Implemented (Operational & Verified)
- **Fitted Machine Learning Pipeline**: Serialized Gradient Boosting pipeline (`models/best_model.pkl`) trained on 5,000 student records (SHA-256 verified).
- **Core Inference Engine**: `src/predict.py` providing `StudentPlacementPredictor`, `predict_student()`, and `predict_batch()`.
- **Centralized Input Validation**: `validate_student_input()` in `src/predict.py` strictly enforcing the 9-feature schema, ranges, types, and categorical values.
- **Interactive Terminal Application**: `src/terminal_app.py`, `src/menu.py`, `src/input_handler.py`, and `src/display.py`.
- **Prediction History Storage Layer**: `src/history_store.py` providing SQLite persistence (`init_db`, `save_prediction`, `get_history`, `get_prediction_by_id`).
- **Automated Test Suite**: Unit and integration tests in `tests/` covering inference, validation rules, history storage, and training script protection.
- **Model Evaluation Reports**: Benchmark comparison across 7 candidate algorithms (`reports/model_comparison.csv`), ROC curves, and explainability reports.

### Not Yet Implemented (Next Development Stage)
- **React Frontend**: Web user interface (pages, forms, state management, and display widgets).
- **FastAPI REST Service**: HTTP server exposing API endpoints to browser clients.
- **API-to-History Route Integration**: Connecting endpoint calls to `history_store.py`.
- **Authentication & Authorization**: Role-based access control or passkey for history viewing.
- **Campus Network Deployment**: Live hosting on college LAN / Wi-Fi subnet.

---

## 2. Target End-to-End System Architecture

```text
React Frontend (Vite / TypeScript / CSS)
      │
      │ HTTP POST / JSON (port 5173 -> 8000)
      ▼
FastAPI Backend (app.py)
      │
      ▼
Centralized Input Validation (src/predict.py: validate_student_input)
      │
      ▼
StudentPlacementPredictor (src/predict.py)
      │
      ▼
Frozen Production Pipeline (models/best_model.pkl)
      │
      ├───► SQLite History Storage (src/history_store.py)
      │
      ▼
Prediction JSON Response (status, probability_placed, probability_not_placed, confidence_score)
      │
      ▼
React Result Interface (Result card, probability gauges, guidance tips)
```

---

## 3. Machine Learning Input Contract

The machine learning pipeline requires **exactly nine features** in the specified order.

### Feature Specification Table

| Feature Name | Data Type | Permitted Range / Values | Description |
| :--- | :--- | :--- | :--- |
| `Branch` | String (Categorical) | `'AI/ML'`, `'Biotechnology'`, `'Chemical'`, `'Civil'`, `'CSE'`, `'Data Science'`, `'ECE'`, `'EEE'`, `'IT'`, `'Mechanical'` | Academic engineering department |
| `College_Tier` | String (Categorical) | `'Tier 1'`, `'Tier 2'`, `'Tier 3'` | Institutional tier classification |
| `10th_Percentage` | Float | `0.0` to `100.0` | Secondary school board examination score |
| `12th_Percentage` | Float | `0.0` to `100.0` | Higher secondary board examination score |
| `Current_CGPA` | Float | `0.0` to `10.0` | Cumulative Grade Point Average |
| `Backlogs` | Integer | `0` to `5` | Active backlog count (integers only) |
| `Attendance_Percentage` | Float | `0.0` to `100.0` | Overall academic attendance record |
| `Projects` | Integer | `0` to `5` | Completed technical and academic projects |
| `Internships` | Integer | `0` to `4` | Completed professional internships |

> [!CAUTION]
> **Strictly Excluded Columns**:
> `Student_ID`, `Name`, `Gender`, `College_Name`, and `Placement_Probability` must **NEVER** be accepted by the API or forwarded to the model.

---

## 4. Proposed REST API Endpoints (FastAPI)

When implementing the FastAPI service in the next stage, expose the following standard endpoints:

### Endpoint 1: `POST /api/predict`
Executes single student prediction with centralized validation.

- **Request Body (JSON)**:
  ```json
  {
    "Branch": "CSE",
    "College_Tier": "Tier 1",
    "10th_Percentage": 88.5,
    "12th_Percentage": 86.0,
    "Current_CGPA": 8.75,
    "Backlogs": 0,
    "Attendance_Percentage": 91.0,
    "Projects": 3,
    "Internships": 2
  }
  ```

- **Successful Response (200 OK)**:
  ```json
  {
    "status": "success",
    "data": {
      "predicted_status": "Placed",
      "probability_placed": 96.42,
      "probability_not_placed": 3.58,
      "confidence_score": 96.42,
      "model_version": "7330783a64173b5dadb941cc4c1342b9d89733dd63c951e151705e52a2acca17"
    }
  }
  ```

- **Validation Error Response (422 Unprocessable Entity)**:
  ```json
  {
    "status": "error",
    "detail": "Input validation failed: Current_CGPA must be between 0.0 and 10.0. Received 11.5"
  }
  ```

### Endpoint 2: `GET /api/model/info`
Returns model metadata, input schema definitions, allowed categorical values, and verified holdout metrics:
- **Architecture**: Gradient Boosting Classifier (`sklearn.ensemble.GradientBoostingClassifier`)
- **Artifact SHA-256**: `7330783a64173b5dadb941cc4c1342b9d89733dd63c951e151705e52a2acca17`
- **Authoritative Metrics**:
  - Test Accuracy: 83.10%
  - Test Precision: 82.76%
  - Test Recall: 90.19%
  - Test F1 Score: 86.32%
  - Test ROC-AUC: 90.36%
  - Brier Score: 0.1158

### Endpoint 3: `GET /api/history`
Returns logged predictions from SQLite storage (`src/history_store.py`) in reverse chronological order:
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "created_at": "2026-11-02T18:00:00+00:00",
      "branch": "CSE",
      "college_tier": "Tier 1",
      "tenth_percentage": 92.0,
      "twelfth_percentage": 90.0,
      "current_cgpa": 9.20,
      "backlogs": 0,
      "attendance_percentage": 92.0,
      "projects": 4,
      "internships": 2,
      "predicted_status": "Placed",
      "probability_placed": 97.05,
      "probability_not_placed": 2.95,
      "confidence_score": 97.05,
      "model_version": "7330783a64173b5dadb941cc4c1342b9d89733dd63c951e151705e52a2acca17"
    }
  ]
}
```

---

## 5. Probability Semantics & Confidence Score Definition

- **`probability_placed`**: Classifier probability estimate from `predict_proba()` for class `Placed` ($0.0\%$ to $100.0\%$).
- **`probability_not_placed`**: Classifier probability estimate from `predict_proba()` for class `Not Placed` ($0.0\%$ to $100.0\%$).
- **`confidence_score`**: Defined strictly as $\max(\text{probability\_placed}, \text{probability\_not\_placed})$.
  > [!NOTE]
  > The confidence score reflects the classifier's top class probability. It is **NOT** a Bayesian posterior, a statistical confidence interval, or a guarantee of employment.

---

## 5. JavaScript / React Client Example

In the React application, send POST requests using native `fetch` or Axios:

```javascript
async function predictPlacement(studentData) {
  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
  
  const response = await fetch(`${apiBaseUrl}/api/predict`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(studentData)
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Prediction request failed");
  }

  const result = await response.json();
  return result.data;
}
```

Configure `.env.example` in the frontend directory:
```bash
VITE_API_BASE_URL=http://localhost:8000
```

---

## 6. College Campus Network & LAN Demonstration Guide

For hosting the demonstration across a campus Wi-Fi network:

### Server Binding
- **FastAPI Backend**: Bind to all network interfaces on port 8000:
  ```bash
  uvicorn app:app --host 0.0.0.0 --port 8000
  ```
- **React Vite Frontend**: Enable host listening on port 5173:
  ```bash
  npm run dev -- --host 0.0.0.0 --port 5173
  ```

### Cross-Origin Resource Sharing (CORS) Security
Do **not** use open wildcard `allow_origins=["*"]` by default. Configure explicit origins:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://<SERVER_LAN_IP>:5173"  # Replace with actual campus LAN IP
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)
```

### Firewall Configuration
Ensure the host operating system permits inbound TCP traffic on ports `8000` and `5173` from the institutional subnet.

---

## 7. Prediction History & Access Control Requirements

The persistence layer (`src/history_store.py`) uses SQLite.

### Access Control Architecture Rules:
1. **Never treat campus Wi-Fi presence as authentication**: Any student on the network could view peer predictions if history is unauthenticated.
2. **Do not implement hard-coded plain passwords**: When implementing the admin route in FastAPI, use standard hashed tokens or environment variables.
3. **Privacy by Design**: The history database stores strictly the 9 academic features and model probabilities. Personal identifiers (names, registration numbers, phone numbers) are never stored.
