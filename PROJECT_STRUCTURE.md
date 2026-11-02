# Project Structure
## Student Placement Prediction System — SRM Institute of Science and Technology

This document details the corrected, reproducible directory layout of the self-contained package.

```text
Student_Placement_Prediction_Shared_Final/
├── .gitignore                      # Git exclusion rules (virtual environments, databases, node_modules)
├── .python-version                 # Declares exact Python runtime version (3.12.4)
├── EXCLUDED_ITEMS_REPORT.md        # Audit of excluded large datasets, databases, & caches
├── FRONTEND_HANDOFF.md             # Integration contract & specs for upcoming React/FastAPI stages
├── MODEL_METADATA.json             # Serialized pipeline metadata, hash verification, & schema
├── PACKAGE_MANIFEST.csv            # Itemized manifest of all packaged files with sizes & hashes
├── PROJECT_STRUCTURE.md            # This annotated directory layout overview
├── README.md                       # Comprehensive project documentation & usage guide
├── RUN_AND_TEST.md                 # Step-by-step setup, execution, & testing guide
├── run_app.bat                     # Windows 1-click launcher for FastAPI backend + React frontend
├── run_app.ps1                     # PowerShell 1-click launcher for full-stack system
├── SHA256SUMS.txt                  # Cryptographic SHA-256 checksums of all package contents
├── requirements.txt                # Broad compatibility dependency specification (incl. FastAPI, uvicorn)
├── requirements-runtime.lock       # Exact pinned runtime lockfile with transitives
├── requirements-dev.txt            # Development & testing dependency specification (incl. httpx, pytest)
├── requirements-dev.lock           # Exact pinned development lockfile
├── requirements-optional-ml.txt    # Optional offline retraining / benchmarking dependencies (xgboost)
├── train_pipeline.py               # Guarded training pipeline script (offline development only)
│
├── api/                            # Asynchronous FastAPI REST Backend Service
│   ├── __init__.py                 # Package initializer
│   └── app.py                      # FastAPI endpoints (/health, /predict, /model/info, /history)
│
├── frontend/                       # Modern React 19 + TypeScript + Vite Web Application
│   ├── package.json                # Frontend dependencies (@tailwindcss/vite, lucide-react)
│   ├── vite.config.ts              # Vite bundler configuration with backend API proxy (/api)
│   ├── tsconfig.json               # TypeScript compiler options
│   ├── index.html                  # HTML entry point
│   └── src/
│       ├── main.tsx                # React DOM root mounting
│       ├── App.tsx                 # Core application shell & navigation state
│       ├── types.ts                # TypeScript interfaces matching backend ML schema
│       ├── api.ts                  # Typed Axios/Fetch client connecting to FastAPI
│       ├── index.css               # Tailwind CSS v4 directives
│       └── components/             # Modular React UI components
│           ├── Navbar.tsx          # SRMIST header, live model SHA badge, & tab switcher
│           ├── PredictorTab.tsx    # 9-feature form, sliders, preset loaders, outcome card
│           ├── HistoryTab.tsx      # SQLite prediction records table, summary metrics & filters
│           ├── ModelAnalyticsTab.tsx # Holdout metrics, confusion matrix, Gini feature importance
│           ├── AboutTab.tsx        # Academic context, 9-feature contract, PII exclusions
│           └── Footer.tsx          # Academic footer
│
├── models/
│   ├── best_model.pkl              # Frozen production Gradient Boosting pipeline (SHA-256 verified)
│   └── candidates/                 # Destination folder for new candidate training outputs
│
├── reports/
│   ├── DEFECT_CORRECTION_REPORT.md # Remediation audit of all 10 identified defects & test results
│   ├── confusion_matrix_gradient_boosting.png # Test set confusion matrix visualization
│   ├── explainability_report.md    # Model explainability analysis & feature rankings
│   ├── feature_importance.csv      # Tabular feature importance values by original feature
│   ├── feature_importance.png      # Feature importance bar plots (grouped & top transformed)
│   ├── model_comparison.csv        # Benchmark metrics comparing all 7 candidate algorithms
│   ├── model_comparison.png        # Comparative performance metric bar chart
│   ├── model_training_report.md    # Phase 2 training & 5-fold CV evaluation report
│   ├── roc_curve_comparison.png    # ROC curves for all 7 evaluated candidate models
│   └── terminal_application_test_report.md # Verification report for terminal CLI application
│
├── src/
│   ├── __init__.py                 # Package initializer
│   ├── display.py                  # Terminal UI layout, banners, dividers, & styling helpers
│   ├── evaluate_explainability.py  # Model explainability script (regenerates feature importance)
│   ├── history_store.py            # SQLite prediction history persistence layer
│   ├── input_handler.py            # Guided 9-step feature collection form & input validation
│   ├── menu.py                     # Main menu navigation, summary review, & workflow routing
│   ├── predict.py                  # Core inference engine & centralized input validation
│   └── terminal_app.py             # CLI application entry point (`python src/terminal_app.py`)
│
└── tests/
    ├── __init__.py                 # Package initializer for test suite
    ├── test_api.py                 # FastAPI test suite (health, predict, validation, info, history)
    ├── test_inference.py           # Unit tests (hash check, 9-feature contract, pipeline inference)
    ├── test_validation.py          # Centralized validation suite (schema, ranges, types, NaN, bool)
    ├── test_history_store.py       # SQLite persistence tests (CRUD, multi-connection, bounds)
    ├── test_model_info.py          # Terminal model information display & authoritative metrics
    ├── test_training_protection.py # Model overwrite & path-traversal guard tests
    └── fixtures/
        ├── sample_students.csv     # 5 sanitized synthetic student profiles (CSV format)
        └── sample_students.json    # 5 sanitized synthetic student profiles (JSON format)
```

---

## Key Modules & Roles

1. **`src/predict.py`**:
   Houses `validate_student_input()` and `StudentPlacementPredictor`. Acts as the single source of truth for schema validation and prediction.
2. **`src/history_store.py`**:
   Provides independent SQLite persistence for student predictions. Parameterized queries, transaction safety, and reverse-chronological retrieval.
3. **`train_pipeline.py`**:
   Equipped with `get_model_save_path()`. Protects `models/best_model.pkl` from accidental overwriting by defaulting outputs to `models/candidates/`.
4. **`tests/`**:
   Comprehensive test coverage across inference, validation, persistence, and training protection. Runnable via `pytest -v`.
