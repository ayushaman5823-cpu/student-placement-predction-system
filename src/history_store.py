"""
SQLite Prediction History Store
Student Placement Prediction System — SRM Institute of Science and Technology

Provides lightweight, robust, thread-safe persistence for student placement predictions.
Stores strictly authorized academic features and model probabilities.
Never stores personal student data (names, registration numbers, gender, or college names).
"""

import os
import math
import json
import sqlite3
import numpy as np
from datetime import datetime, timezone

# Default SQLite database path (under data/ directory, with Vercel serverless /tmp fallback)
def get_default_db_path() -> str:
    env_path = os.environ.get("HISTORY_DB_PATH")
    if env_path:
        return env_path
    if os.environ.get("VERCEL"):
        return "/tmp/history.sqlite"
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "history.sqlite")

DEFAULT_DB_PATH = get_default_db_path()

# Standardized immutable model artifact identifier (SHA-256 of models/best_model.pkl)
DEFAULT_MODEL_VERSION = "7330783a64173b5dadb941cc4c1342b9d89733dd63c951e151705e52a2acca17"

REQUIRED_FEATURES = [
    'Branch', 'College_Tier', '10th_Percentage', '12th_Percentage',
    'Current_CGPA', 'Backlogs', 'Attendance_Percentage', 'Projects', 'Internships'
]

VALID_BRANCHES = [
    'AI/ML', 'Biotechnology', 'CSE', 'Chemical', 'Civil',
    'Data Science', 'ECE', 'EEE', 'IT', 'Mechanical'
]

VALID_TIERS = ['Tier 1', 'Tier 2', 'Tier 3']

NUMERICAL_CONSTRAINTS = {
    '10th_Percentage': {'min': 0.0, 'max': 100.0, 'type': 'float'},
    '12th_Percentage': {'min': 0.0, 'max': 100.0, 'type': 'float'},
    'Current_CGPA': {'min': 0.0, 'max': 10.0, 'type': 'float'},
    'Backlogs': {'min': 0, 'max': 5, 'type': 'int'},
    'Attendance_Percentage': {'min': 0.0, 'max': 100.0, 'type': 'float'},
    'Projects': {'min': 0, 'max': 5, 'type': 'int'},
    'Internships': {'min': 0, 'max': 4, 'type': 'int'}
}

# Database Schema
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS prediction_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    branch TEXT NOT NULL,
    college_tier TEXT NOT NULL,
    tenth_percentage REAL NOT NULL,
    twelfth_percentage REAL NOT NULL,
    current_cgpa REAL NOT NULL,
    backlogs INTEGER NOT NULL,
    attendance_percentage REAL NOT NULL,
    projects INTEGER NOT NULL,
    internships INTEGER NOT NULL,
    student_features TEXT NOT NULL,
    predicted_status TEXT NOT NULL,
    probability_placed REAL NOT NULL,
    probability_not_placed REAL NOT NULL,
    confidence_score REAL NOT NULL,
    model_version TEXT NOT NULL
);
"""

CREATE_INDEX_SQL = """
CREATE INDEX IF NOT EXISTS idx_history_created_at ON prediction_history (created_at DESC);
"""


def validate_history_record(student_features, predicted_status, probability_placed, probability_not_placed, confidence_score=None, model_version=DEFAULT_MODEL_VERSION):
    """
    Validates the complete contract for history persistence.
    Raises TypeError or ValueError on any contract violation.
    """
    # 1. Validate student_features container
    if not isinstance(student_features, dict):
        raise TypeError(f"student_features must be a dictionary, received {type(student_features).__name__}.")

    provided_keys = set(student_features.keys())
    required_keys = set(REQUIRED_FEATURES)

    missing_keys = required_keys - provided_keys
    if missing_keys:
        raise ValueError(f"Missing required feature(s) for history storage: {sorted(list(missing_keys))}.")

    extra_keys = provided_keys - required_keys
    if extra_keys:
        raise ValueError(f"Unexpected extra feature(s) in history storage: {sorted(list(extra_keys))}.")

    # 2. Validate categorical features
    branch = student_features.get('Branch')
    if branch not in VALID_BRANCHES:
        raise ValueError(f"Invalid Branch '{branch}'. Allowed: {VALID_BRANCHES}.")

    tier = student_features.get('College_Tier')
    if tier not in VALID_TIERS:
        raise ValueError(f"Invalid College_Tier '{tier}'. Allowed: {VALID_TIERS}.")

    # 3. Validate numerical features
    for feat_name, spec in NUMERICAL_CONSTRAINTS.items():
        val = student_features.get(feat_name)

        if isinstance(val, bool):
            raise TypeError(f"Feature '{feat_name}' cannot be a boolean value ({val}).")

        if not isinstance(val, (int, float, np.number)):
            raise TypeError(f"Feature '{feat_name}' must be numeric, received {type(val).__name__}.")

        if math.isnan(val) or math.isinf(val):
            raise ValueError(f"Feature '{feat_name}' cannot be NaN or infinite ({val}).")

        if spec['type'] == 'int':
            if isinstance(val, (float, np.floating)):
                if not float(val).is_integer():
                    raise ValueError(f"Feature '{feat_name}' must be an integer count, received fractional value {val}.")
            int_val = int(val)
            if not (spec['min'] <= int_val <= spec['max']):
                raise ValueError(f"Feature '{feat_name}' value {val} is outside permitted range [{spec['min']}, {spec['max']}].")
        else:
            float_val = float(val)
            if not (spec['min'] <= float_val <= spec['max']):
                raise ValueError(f"Feature '{feat_name}' value {val} is outside permitted range [{spec['min']}, {spec['max']}].")

    # 4. Validate predicted_status
    if not isinstance(predicted_status, str) or predicted_status not in ("Placed", "Not Placed"):
        raise ValueError(f"predicted_status must be 'Placed' or 'Not Placed', received '{predicted_status}'.")

    # 5. Validate probability_placed and probability_not_placed
    for prob_name, prob_val in [("probability_placed", probability_placed), ("probability_not_placed", probability_not_placed)]:
        if isinstance(prob_val, bool):
            raise TypeError(f"'{prob_name}' cannot be a boolean value ({prob_val}).")
        if not isinstance(prob_val, (int, float, np.number)):
            raise TypeError(f"'{prob_name}' must be numeric, received {type(prob_val).__name__}.")
        if math.isnan(prob_val) or math.isinf(prob_val):
            raise ValueError(f"'{prob_name}' cannot be NaN or infinite ({prob_val}).")
        if not (0.0 <= float(prob_val) <= 100.0):
            raise ValueError(f"'{prob_name}' must be between 0.0 and 100.0, received {prob_val}.")

    prob_sum = float(probability_placed) + float(probability_not_placed)
    if abs(prob_sum - 100.0) > 0.1:
        raise ValueError(f"Probabilities must sum to 100.0% within floating tolerance (received {prob_sum:.2f}%).")

    # 6. Validate confidence_score
    max_prob = round(max(float(probability_placed), float(probability_not_placed)), 2)
    if confidence_score is not None:
        if isinstance(confidence_score, bool):
            raise TypeError(f"confidence_score cannot be a boolean value ({confidence_score}).")
        if not isinstance(confidence_score, (int, float, np.number)):
            raise TypeError(f"confidence_score must be numeric, received {type(confidence_score).__name__}.")
        if math.isnan(confidence_score) or math.isinf(confidence_score):
            raise ValueError(f"confidence_score cannot be NaN or infinite ({confidence_score}).")
        if abs(float(confidence_score) - max_prob) > 0.1:
            raise ValueError(
                f"confidence_score ({confidence_score}) contradicts maximum class probability ({max_prob})."
            )
        resolved_confidence = float(confidence_score)
    else:
        resolved_confidence = max_prob

    # 7. Validate model_version
    if not model_version or not isinstance(model_version, str) or not model_version.strip():
        raise ValueError("Model version/identifier must be a non-empty string.")

    return resolved_confidence


def get_db_connection(db_path=None):
    """
    Creates and returns a SQLite connection with row factory configured.
    Gracefully falls back to /tmp if filesystem is read-only (e.g., Vercel serverless).
    """
    path = db_path or DEFAULT_DB_PATH
    if path != ":memory:":
        try:
            os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        except OSError:
            path = "/tmp/history.sqlite"
    try:
        conn = sqlite3.connect(path, timeout=10.0)
    except sqlite3.OperationalError:
        path = "/tmp/history.sqlite"
        conn = sqlite3.connect(path, timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path=None):
    """
    Initializes the SQLite database and creates the required schema and indexes.
    """
    conn = get_db_connection(db_path)
    try:
        with conn:
            conn.execute(CREATE_TABLE_SQL)
            conn.execute(CREATE_INDEX_SQL)
    finally:
        conn.close()


def save_prediction(student_features, predicted_status, probability_placed, probability_not_placed, confidence_score=None, model_version=DEFAULT_MODEL_VERSION, db_path=None):
    """
    Records a completed inference prediction into the SQLite store after strict validation.
    
    Parameters:
        student_features: dict containing the 9 authorized features.
        predicted_status: str ('Placed' or 'Not Placed').
        probability_placed: float (0.0 to 100.0).
        probability_not_placed: float (0.0 to 100.0).
        confidence_score: float (must match max(probability_placed, probability_not_placed)).
        model_version: str metadata identifier.
        db_path: optional path to database file (defaults to data/history.sqlite).
        
    Returns:
        int: The auto-generated record ID.
    """
    # 1. Enforce strict input validation BEFORE database access
    resolved_confidence = validate_history_record(
        student_features=student_features,
        predicted_status=predicted_status,
        probability_placed=probability_placed,
        probability_not_placed=probability_not_placed,
        confidence_score=confidence_score,
        model_version=model_version
    )

    # 2. Ensure database table exists
    init_db(db_path)

    now_utc = datetime.now(timezone.utc).isoformat()
    features_json = json.dumps(student_features, sort_keys=True)

    insert_sql = """
    INSERT INTO prediction_history (
        created_at, branch, college_tier, tenth_percentage, twelfth_percentage,
        current_cgpa, backlogs, attendance_percentage, projects, internships,
        student_features, predicted_status, probability_placed, probability_not_placed,
        confidence_score, model_version
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    params = (
        now_utc,
        str(student_features['Branch']),
        str(student_features['College_Tier']),
        float(student_features['10th_Percentage']),
        float(student_features['12th_Percentage']),
        float(student_features['Current_CGPA']),
        int(student_features['Backlogs']),
        float(student_features['Attendance_Percentage']),
        int(student_features['Projects']),
        int(student_features['Internships']),
        features_json,
        str(predicted_status),
        float(probability_placed),
        float(probability_not_placed),
        float(resolved_confidence),
        str(model_version)
    )

    conn = get_db_connection(db_path)
    try:
        with conn:
            cursor = conn.execute(insert_sql, params)
            record_id = cursor.lastrowid
        return record_id
    finally:
        conn.close()


def get_history(limit=50, offset=0, db_path=None):
    """
    Retrieves stored prediction records in reverse chronological order (newest first).
    
    Parameters:
        limit: int maximum records to fetch.
        offset: int offset for pagination.
        db_path: optional path to database file.
        
    Returns:
        list of dict representations of prediction records.
    """
    init_db(db_path)
    conn = get_db_connection(db_path)
    try:
        select_sql = """
        SELECT * FROM prediction_history
        ORDER BY id DESC
        LIMIT ? OFFSET ?
        """
        cursor = conn.execute(select_sql, (limit, offset))
        rows = cursor.fetchall()
        results = []
        for r in rows:
            record = dict(r)
            try:
                record['student_features'] = json.loads(record['student_features'])
            except Exception:
                pass
            results.append(record)
        return results
    finally:
        conn.close()


def get_prediction_by_id(record_id, db_path=None):
    """
    Retrieves a single prediction record by primary key ID.
    Returns dict if found, or None if not found.
    """
    init_db(db_path)
    conn = get_db_connection(db_path)
    try:
        select_sql = "SELECT * FROM prediction_history WHERE id = ?"
        cursor = conn.execute(select_sql, (record_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        record = dict(row)
        try:
            record['student_features'] = json.loads(record['student_features'])
        except Exception:
            pass
        return record
    finally:
        conn.close()


def clear_history(db_path=None):
    """
    Safely clears all records from the prediction history table (useful for test isolation).
    """
    init_db(db_path)
    conn = get_db_connection(db_path)
    try:
        with conn:
            conn.execute("DELETE FROM prediction_history")
    finally:
        conn.close()
