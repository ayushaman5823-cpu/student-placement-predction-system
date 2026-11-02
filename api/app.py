"""
FastAPI REST API Service
Student Placement Prediction System — SRM Institute of Science and Technology

Provides high-performance, asynchronous REST endpoints for:
- Placement prediction with centralized input schema validation
- Model metadata, architecture, and authoritative performance metrics
- SQLite prediction history persistence
- Sample profile presets
"""

import os
import sys
import json
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

# Ensure project root and src/ are in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from predict import StudentPlacementPredictor, validate_student_input, REQUIRED_FEATURES, DEFAULT_MODEL_VERSION
from history_store import save_prediction, get_history, get_prediction_by_id, clear_history

# Initialize predictor singleton
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "best_model.pkl")
METADATA_PATH = os.path.join(PROJECT_ROOT, "MODEL_METADATA.json")

predictor = StudentPlacementPredictor(model_path=MODEL_PATH)

app = FastAPI(
    title="Student Placement Prediction API",
    description="SRM Institute of Science and Technology — Machine Learning Placement Prediction Engine",
    version="2.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Request Models
class StudentInputSchema(BaseModel):
    Branch: str = Field(..., description="Engineering department branch")
    College_Tier: str = Field(..., description="Institutional classification tier")
    tenth_Percentage: float = Field(..., alias="10th_Percentage", ge=0.0, le=100.0, description="10th Board Exam %")
    twelfth_Percentage: float = Field(..., alias="12th_Percentage", ge=0.0, le=100.0, description="12th Board Exam %")
    Current_CGPA: float = Field(..., ge=0.0, le=10.0, description="Cumulative Grade Point Average (0-10)")
    Backlogs: int = Field(..., ge=0, le=5, description="Active backlog count (0-5)")
    Attendance_Percentage: float = Field(..., ge=0.0, le=100.0, description="Academic attendance % (0-100)")
    Projects: int = Field(..., ge=0, le=5, description="Completed technical projects (0-5)")
    Internships: int = Field(..., ge=0, le=4, description="Completed internships (0-4)")

    model_config = {
        "populate_by_name": True
    }

    def to_feature_dict(self) -> Dict[str, Any]:
        return {
            "Branch": self.Branch,
            "College_Tier": self.College_Tier,
            "10th_Percentage": self.tenth_Percentage,
            "12th_Percentage": self.twelfth_Percentage,
            "Current_CGPA": self.Current_CGPA,
            "Backlogs": self.Backlogs,
            "Attendance_Percentage": self.Attendance_Percentage,
            "Projects": self.Projects,
            "Internships": self.Internships
        }


def load_metadata_dict() -> Dict[str, Any]:
    if os.path.exists(METADATA_PATH):
        try:
            with open(METADATA_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


@app.get("/api/health")
def health_check():
    """Health check endpoint to verify service and model status."""
    return {
        "status": "healthy",
        "service": "Student Placement Prediction API",
        "institution": "SRM Institute of Science and Technology",
        "model_artifact_sha256": DEFAULT_MODEL_VERSION,
        "features_count": len(REQUIRED_FEATURES)
    }


@app.get("/api/model/info")
def get_model_info():
    """
    Returns complete model architecture details, authoritative holdout metrics,
    input contract definitions, and feature importances.
    """
    metadata = load_metadata_dict()
    return {
        "status": "success",
        "data": {
            "architecture": "Gradient Boosting Classifier (scikit-learn Pipeline)",
            "model_artifact_sha256": DEFAULT_MODEL_VERSION,
            "metadata_schema_version": metadata.get("metadata_schema_version", "2.0.0"),
            "holdout_test_metrics": metadata.get("evaluation_context", {}).get("holdout_test_metrics", {
                "accuracy": 0.8310,
                "precision": 0.8276,
                "recall": 0.9019,
                "f1_score": 0.8632,
                "roc_auc": 0.9036,
                "brier_score": 0.1158
            }),
            "confusion_matrix": metadata.get("evaluation_context", {}).get("confusion_matrix", {
                "true_negatives": 298,
                "false_positives": 111,
                "false_negatives": 58,
                "true_positives": 533
            }),
            "valid_branches": predictor.valid_branches,
            "valid_tiers": predictor.valid_tiers,
            "required_features": REQUIRED_FEATURES,
            "feature_importances": [
                {"feature": "Attendance_Percentage", "importance_pct": 57.80},
                {"feature": "Current_CGPA", "importance_pct": 14.53},
                {"feature": "12th_Percentage", "importance_pct": 12.41},
                {"feature": "10th_Percentage", "importance_pct": 7.27},
                {"feature": "Backlogs", "importance_pct": 4.88},
                {"feature": "Internships", "importance_pct": 1.28},
                {"feature": "Projects", "importance_pct": 0.94},
                {"feature": "College_Tier", "importance_pct": 0.60},
                {"feature": "Branch", "importance_pct": 0.29}
            ],
            "probability_semantics": metadata.get("probability_and_confidence_semantics", {})
        }
    }


@app.get("/api/sample-profiles")
def get_sample_profiles():
    """Returns the 5 verified student profiles with pre-computed reference predictions."""
    profiles = [
        {
            "id": "profile_1",
            "name": "Strong Academic Student",
            "description": "High CGPA (9.20), 92% attendance, 0 backlogs, Tier 1 CSE",
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
            },
            "expected_status": "Placed",
            "expected_prob_placed": 97.05
        },
        {
            "id": "profile_2",
            "name": "Average Student",
            "description": "Moderate CGPA (7.60), 82% attendance, 1 backlog, Tier 2 ECE",
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
            },
            "expected_status": "Placed",
            "expected_prob_placed": 90.64
        },
        {
            "id": "profile_3",
            "name": "Weak Academic Student",
            "description": "Low CGPA (5.80), sub-60% school grades, 2 backlogs, Tier 3 Civil",
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
            },
            "expected_status": "Not Placed",
            "expected_prob_placed": 3.60
        },
        {
            "id": "profile_4",
            "name": "High Backlog Student",
            "description": "5 active backlogs, CGPA 7.20, 80% attendance, Tier 2 IT",
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
            },
            "expected_status": "Not Placed",
            "expected_prob_placed": 43.42
        },
        {
            "id": "profile_5",
            "name": "Tier 3 Strong Academic",
            "description": "High CGPA (8.40), 88% attendance, 0 backlogs, Tier 3 Mechanical",
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
            },
            "expected_status": "Placed",
            "expected_prob_placed": 94.87
        }
    ]
    return {"status": "success", "data": profiles}


@app.post("/api/predict")
def predict(payload: StudentInputSchema):
    """
    Predicts student placement status and class probabilities from raw feature values.
    Validates features using centralized input validation and logs the record to SQLite.
    """
    feature_dict = payload.to_feature_dict()

    # 1. Centralized ML validation
    try:
        validate_student_input(
            feature_dict,
            valid_branches=predictor.valid_branches,
            valid_tiers=predictor.valid_tiers,
            raise_exception=True
        )
    except (KeyError, ValueError, TypeError) as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Input validation error: {str(e)}"
        )

    # 2. Pipeline inference
    try:
        prediction_result = predictor.predict_student(feature_dict)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference execution failed: {str(e)}"
        )

    # 3. SQLite persistence
    history_id = None
    try:
        history_id = save_prediction(
            student_features=feature_dict,
            predicted_status=prediction_result["predicted_status"],
            probability_placed=prediction_result["probability_placed"],
            probability_not_placed=prediction_result["probability_not_placed"],
            confidence_score=prediction_result["confidence_score"],
            model_version=prediction_result["model_version"]
        )
    except Exception as e:
        # Logging failure should not break prediction response
        print(f"Warning: Failed to save prediction to history: {e}")

    return {
        "status": "success",
        "data": {
            **prediction_result,
            "history_id": history_id,
            "input_features": feature_dict
        }
    }


@app.get("/api/history")
def get_prediction_history(limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0)):
    """Retrieves stored predictions from SQLite in reverse chronological order."""
    try:
        records = get_history(limit=limit, offset=offset)
        return {
            "status": "success",
            "count": len(records),
            "data": records
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")


@app.delete("/api/history")
def clear_prediction_history():
    """Safely clears prediction history records (useful for demo resets)."""
    try:
        clear_history()
        return {"status": "success", "message": "Prediction history cleared successfully."}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
