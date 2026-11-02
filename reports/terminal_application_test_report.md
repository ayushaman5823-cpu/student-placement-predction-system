# Terminal Application Test & Integration Report

## Executive Summary

This report documents the testing, input validation verification, and model integration audit for the **Student Placement Prediction Terminal Application** (`src/terminal_app.py`).

The terminal interface was implemented using a modular architecture (`display.py`, `input_handler.py`, `menu.py`, `predict.py`, `terminal_app.py`) built strictly around the exact 9-feature contract of the trained Gradient Boosting model (`models/best_model.pkl`).

---

## 1. Model Integration & Feature Contract Audit

- **Trained Pipeline Loaded**: `models/best_model.pkl` loaded via `src/predict.py`.
- **Exact 9 Features Collected**:
  1. `Branch`
  2. `College_Tier`
  3. `10th_Percentage`
  4. `12th_Percentage`
  5. `Current_CGPA`
  6. `Backlogs`
  7. `Attendance_Percentage`
  8. `Projects`
  9. `Internships`
- **Excluded Features Verified**: No input prompts exist for `Student_ID`, `Name`, `Gender`, `College_Name`, or `Placement_Probability`.
- **No Hard-coded ML Logic**: Predictions are generated exclusively via `pipeline.predict()` and probabilities via `pipeline.predict_proba()`.

---

## 2. Sample Student Profile Integration Tests (5 Profiles)

All 5 required student test profiles were processed through `StudentPlacementPredictor` in `src/predict.py`:

| Test Profile | Input Features | Predicted Class | Placed Probability | Not Placed Probability | Status |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **PROFILE 1: Strong Student** | CSE, Tier 1, 10th: 92%, 12th: 90%, CGPA: 9.20, Backlogs: 0, Attendance: 92%, Projects: 4, Internships: 2 | **Placed** | **97.05%** | **2.95%** | **PASSED** |
| **PROFILE 2: Average Student** | ECE, Tier 2, 10th: 75%, 12th: 74%, CGPA: 7.60, Backlogs: 1, Attendance: 82%, Projects: 2, Internships: 1 | **Placed** | **90.64%** | **9.36%** | **PASSED** |
| **PROFILE 3: Weak Academic Student** | Civil, Tier 3, 10th: 58%, 12th: 56%, CGPA: 5.80, Backlogs: 2, Attendance: 78%, Projects: 1, Internships: 0 | **Not Placed** | **3.60%** | **96.40%** | **PASSED** |
| **PROFILE 4: High Backlog Student** | IT, Tier 2, 10th: 74%, 12th: 72%, CGPA: 7.20, Backlogs: 5, Attendance: 80%, Projects: 2, Internships: 1 | **Not Placed** | **43.42%** | **56.58%** | **PASSED** |
| **PROFILE 5: Tier 3 Strong Academic** | Mechanical, Tier 3, 10th: 82%, 12th: 80%, CGPA: 8.40, Backlogs: 0, Attendance: 88%, Projects: 3, Internships: 1 | **Placed** | **94.87%** | **5.13%** | **PASSED** |

---

## 3. Input Validation Test Suite

| Test Case ID | Feature / Input Field | Invalid Input Passed | Expected Handling | Result |
| :---: | :--- | :--- | :--- | :---: |
| **TC-01** | Main Menu Choice | `"99"`, `"abc"`, `""` | Displays error message, re-prompts menu choice | **PASSED** |
| **TC-02** | Branch Selection | `"15"`, `"-1"`, `"CSE"` | Displays error, re-prompts Branch choice (1-10) | **PASSED** |
| **TC-03** | College Tier Selection | `"5"`, `"Tier 1"` | Displays error, re-prompts Tier choice (1-3) | **PASSED** |
| **TC-04** | 10th / 12th / Attendance % | `"-10"`, `"105"`, `"xyz"` | Displays range error (0–100), re-prompts | **PASSED** |
| **TC-05** | Current CGPA | `"11.5"`, `"-2"`, `"eight"` | Displays range error (0–10), re-prompts | **PASSED** |
| **TC-06** | Backlogs Count | `"6"`, `"-1"`, `"2.5"` | Displays integer error (0–5), re-prompts | **PASSED** |
| **TC-07** | Projects Count | `"7"`, `"many"` | Displays integer error (0–5), re-prompts | **PASSED** |
| **TC-08** | Internships Count | `"5"`, `"-1"` | Displays integer error (0–4), re-prompts | **PASSED** |
| **TC-09** | Confirmation Screen | Select `[2] Edit Details` | Restarts feature collection form cleanly | **PASSED** |
| **TC-10** | Confirmation Screen | Select `[3] Cancel` | Aborts prediction, returns to Main Menu | **PASSED** |

---

## 4. Verification Checklist Audit

- [x] Application starts successfully.
- [x] Main menu navigation works cleanly.
- [x] Branch selection supports all 10 trained branches.
- [x] College Tier selection supports Tier 1, Tier 2, Tier 3.
- [x] Percentage validation enforces 0.0 to 100.0.
- [x] CGPA validation enforces 0.0 to 10.0.
- [x] Backlog selection enforces 0 to 5.
- [x] Attendance validation enforces 0.0 to 100.0.
- [x] Project selection enforces 0 to 5.
- [x] Internship selection enforces 0 to 4.
- [x] Confirmation summary screen displays all 9 inputs.
- [x] Edit and Cancel flows function properly.
- [x] Prediction engine calls `models/best_model.pkl` via `src/predict.py`.
- [x] `predict_proba()` calculates dynamic probabilities summing to 100%.
- [x] Predicted class displays `Placed` or `Not Placed`.
- [x] Invalid inputs are caught gracefully without crashing.
- [x] Model Information screen displays 83.10% accuracy and feature list.
- [x] About Project screen displays project context and disclaimers.
- [x] Exit confirmation prompt works.
- [x] 5 sample profiles verified successfully.
- [x] Exactly 9 features passed to model pipeline.
- [x] `Placement_Probability` from raw CSV is never used.
- [x] No hard-coded placement rules in application UI.

---

## 5. Final Status

**System Status**: **OPERATIONAL & FULLY VERIFIED**
