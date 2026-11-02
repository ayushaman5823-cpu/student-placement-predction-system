"""
Machine Learning Prediction and Centralized Input Validation Engine
Student Placement Prediction System — SRM Institute of Science and Technology
"""

import os
import math
import joblib
import pandas as pd
import numpy as np

# Path to trained model
DEFAULT_MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "best_model.pkl")

# Standardized immutable production model artifact identifier (SHA-256 of models/best_model.pkl)
DEFAULT_MODEL_VERSION = "7330783a64173b5dadb941cc4c1342b9d89733dd63c951e151705e52a2acca17"

# Authorized feature contract (strictly 9 features in order)
REQUIRED_FEATURES = [
    'Branch', 'College_Tier', '10th_Percentage', '12th_Percentage',
    'Current_CGPA', 'Backlogs', 'Attendance_Percentage', 'Projects', 'Internships'
]

# Baseline trained categories
DEFAULT_VALID_BRANCHES = [
    'AI/ML', 'Biotechnology', 'CSE', 'Chemical', 'Civil',
    'Data Science', 'ECE', 'EEE', 'IT', 'Mechanical'
]
DEFAULT_VALID_TIERS = ['Tier 1', 'Tier 2', 'Tier 3']

VALID_BRANCHES = list(DEFAULT_VALID_BRANCHES)
VALID_TIERS = list(DEFAULT_VALID_TIERS)

# Feature specification bounds and types
NUMERICAL_CONSTRAINTS = {
    '10th_Percentage': {'min': 0.0, 'max': 100.0, 'type': 'float'},
    '12th_Percentage': {'min': 0.0, 'max': 100.0, 'type': 'float'},
    'Current_CGPA': {'min': 0.0, 'max': 10.0, 'type': 'float'},
    'Backlogs': {'min': 0, 'max': 5, 'type': 'int'},
    'Attendance_Percentage': {'min': 0.0, 'max': 100.0, 'type': 'float'},
    'Projects': {'min': 0, 'max': 5, 'type': 'int'},
    'Internships': {'min': 0, 'max': 4, 'type': 'int'}
}


def _extract_categories_from_pipeline(pipeline):
    """
    Safely retrieves the valid trained categories directly from the fitted OneHotEncoder.
    """
    try:
        preprocessor = pipeline.named_steps.get('preprocessor')
        if preprocessor is not None:
            cat_transformer = preprocessor.named_transformers_.get('cat')
            if cat_transformer is not None and hasattr(cat_transformer, 'categories_'):
                cats = cat_transformer.categories_
                return list(cats[0]), list(cats[1])
    except Exception:
        pass
    return DEFAULT_VALID_BRANCHES, DEFAULT_VALID_TIERS


def validate_student_input(student_data, valid_branches=None, valid_tiers=None, raise_exception=True):
    """
    Centralized validation function for student input profiles.
    Strictly enforces:
      - Dictionary or single-row pandas DataFrame format
      - Exactly the 9 authorized features (no missing features, no extra/unauthorized columns)
      - Valid categorical disciplines and institutional tiers
      - Numeric bounds, absence of NaN/inf, rejection of booleans, and integer constraints
    
    Parameters:
        student_data: dict or pd.DataFrame representing a single student profile.
        valid_branches: list of allowed branch strings (optional).
        valid_tiers: list of allowed college tier strings (optional).
        raise_exception: if True, raises ValueError/KeyError; if False, returns (is_valid, error_msg).
    
    Returns:
        (True, "") if valid.
    """
    branches = valid_branches or VALID_BRANCHES
    tiers = valid_tiers or VALID_TIERS

    # 1. Format check
    if isinstance(student_data, dict):
        data = student_data
    elif isinstance(student_data, pd.DataFrame):
        if len(student_data) != 1:
            err = f"validate_student_input expects a single student record, got DataFrame of shape {student_data.shape}."
            if raise_exception:
                raise ValueError(err)
            return False, err
        data = student_data.iloc[0].to_dict()
    elif isinstance(student_data, pd.Series):
        data = student_data.to_dict()
    else:
        err = f"Input must be a dictionary, pandas Series, or single-row DataFrame, received {type(student_data).__name__}."
        if raise_exception:
            raise TypeError(err)
        return False, err

    keys = set(data.keys())
    required_set = set(REQUIRED_FEATURES)

    # 2. Schema check: missing features
    missing = [col for col in REQUIRED_FEATURES if col not in keys]
    if missing:
        err = f"Missing required feature(s): {missing}"
        if raise_exception:
            raise KeyError(err)
        return False, err

    # 3. Schema check: unexpected extra columns
    extra = sorted(list(keys - required_set))
    if extra:
        err = f"Unauthorized/unexpected feature(s) detected: {extra}. Only the 9 authorized features are accepted."
        if raise_exception:
            raise ValueError(err)
        return False, err

    # 4. Categorical feature validation: Branch
    branch_val = data['Branch']
    if not isinstance(branch_val, str) or branch_val not in branches:
        err = f"Invalid Branch '{branch_val}'. Allowed values: {branches}"
        if raise_exception:
            raise ValueError(err)
        return False, err

    # 5. Categorical feature validation: College_Tier
    tier_val = data['College_Tier']
    if not isinstance(tier_val, str) or tier_val not in tiers:
        err = f"Invalid College_Tier '{tier_val}'. Allowed values: {tiers}"
        if raise_exception:
            raise ValueError(err)
        return False, err

    # 6. Numerical feature validation
    for feat_name, spec in NUMERICAL_CONSTRAINTS.items():
        val = data[feat_name]

        # Explicitly reject boolean types (which in Python are a subclass of int)
        if isinstance(val, bool):
            err = f"Invalid boolean value '{val}' for numeric feature '{feat_name}'."
            if raise_exception:
                raise TypeError(err)
            return False, err

        # Check for non-numeric type
        if not isinstance(val, (int, float, np.integer, np.floating)):
            err = f"Feature '{feat_name}' must be numeric, received {type(val).__name__} ({val})."
            if raise_exception:
                raise TypeError(err)
            return False, err

        # Check for NaN / inf
        if math.isnan(val) or math.isinf(val):
            err = f"Feature '{feat_name}' cannot be NaN or infinite ({val})."
            if raise_exception:
                raise ValueError(err)
            return False, err

        # Integer constraint enforcement (reject fractional values)
        if spec['type'] == 'int':
            if isinstance(val, (float, np.floating)):
                if not float(val).is_integer():
                    err = f"Feature '{feat_name}' must be an integer count, received fractional value {val}."
                    if raise_exception:
                        raise ValueError(err)
                    return False, err
            int_val = int(val)
            if not (spec['min'] <= int_val <= spec['max']):
                err = f"Feature '{feat_name}' value {val} is outside permitted range [{spec['min']}, {spec['max']}]."
                if raise_exception:
                    raise ValueError(err)
                return False, err
        else:
            # Float range check
            float_val = float(val)
            if not (spec['min'] <= float_val <= spec['max']):
                err = f"Feature '{feat_name}' value {val} is outside permitted range [{spec['min']}, {spec['max']}]."
                if raise_exception:
                    raise ValueError(err)
                return False, err

    return True, ""


class StudentPlacementPredictor:
    """
    Production Inference Engine for Student Placement Prediction System.
    Loads the trained scikit-learn pipeline and produces placement predictions
    with validated input contracts and model-estimated class probabilities.
    
    Probability Semantics:
      - probability_placed: Classifier probability estimate for class Placed (percentage 0-100%).
      - probability_not_placed: Classifier probability estimate for class Not Placed (percentage 0-100%).
      - confidence_score: Defined strictly as max(probability_placed, probability_not_placed).
        Represents the highest class probability returned by the model, not a calibrated statistical confidence interval.
    """
    def __init__(self, model_path=DEFAULT_MODEL_PATH, model_version=DEFAULT_MODEL_VERSION):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}. Production pipeline artifact is required.")
        self.model_path = model_path
        self.model_version = model_version
        self.pipeline = joblib.load(model_path)

        # Synchronize categorical options from fitted pipeline
        branches, tiers = _extract_categories_from_pipeline(self.pipeline)
        self.valid_branches = branches
        self.valid_tiers = tiers

    def predict_student(self, student_data):
        """
        Accepts a dictionary or single-row pandas DataFrame containing raw feature values.
        Applies centralized input validation, then executes pipeline inference.
        Returns dictionary with predicted status, dynamic probabilities, confidence score, and model version.
        """
        # Centralized validation check
        validate_student_input(
            student_data,
            valid_branches=self.valid_branches,
            valid_tiers=self.valid_tiers,
            raise_exception=True
        )

        if isinstance(student_data, dict):
            df_input = pd.DataFrame([student_data])
        elif isinstance(student_data, pd.DataFrame):
            df_input = student_data.copy()
        elif isinstance(student_data, pd.Series):
            df_input = pd.DataFrame([student_data.to_dict()])
        else:
            df_input = pd.DataFrame([student_data])

        # Enforce exact column order
        X_raw = df_input[REQUIRED_FEATURES]

        pred_code = self.pipeline.predict(X_raw)[0]
        probas = self.pipeline.predict_proba(X_raw)[0]

        prob_not_placed = float(np.round(probas[0] * 100, 2))
        prob_placed = float(np.round(probas[1] * 100, 2))
        predicted_status = "Placed" if pred_code == 1 else "Not Placed"
        confidence = float(np.round(max(prob_placed, prob_not_placed), 2))

        return {
            "predicted_status": predicted_status,
            "probability_placed": prob_placed,
            "probability_not_placed": prob_not_placed,
            "confidence_score": confidence,
            "model_version": self.model_version
        }

    def predict_batch(self, df_batch):
        """
        Accepts a multi-row pandas DataFrame containing raw feature values.
        Validates every row and returns the DataFrame with predictions and probabilities appended.
        """
        if not isinstance(df_batch, pd.DataFrame):
            raise TypeError("df_batch must be a pandas DataFrame")

        # Validate each row against centralized schema
        for idx in range(len(df_batch)):
            row = df_batch.iloc[idx].to_dict()
            try:
                validate_student_input(
                    row,
                    valid_branches=self.valid_branches,
                    valid_tiers=self.valid_tiers,
                    raise_exception=True
                )
            except Exception as e:
                raise ValueError(f"Batch validation error at row index {idx}: {e}") from e

        X_raw = df_batch[REQUIRED_FEATURES].copy()
        pred_codes = self.pipeline.predict(X_raw)
        probas = self.pipeline.predict_proba(X_raw)

        df_result = df_batch.copy()
        df_result['predicted_Placement_Status'] = np.where(pred_codes == 1, "Placed", "Not Placed")
        df_result['probability_Not_Placed'] = np.round(probas[:, 0] * 100, 2)
        df_result['probability_Placed'] = np.round(probas[:, 1] * 100, 2)

        return df_result


def predict_single_student(student_dict, model_path=DEFAULT_MODEL_PATH):
    """
    Convenience wrapper to predict for a single student dictionary.
    """
    predictor = StudentPlacementPredictor(model_path=model_path)
    return predictor.predict_student(student_dict)
