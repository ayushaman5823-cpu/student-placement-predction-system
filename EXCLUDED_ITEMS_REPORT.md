# Excluded Items & Integrity Audit Report
## Student Placement Prediction System — SRM Institute of Science and Technology

In accordance with strict packaging integrity and data protection rules, all disposable, machine-specific, cached, large research, and privacy-sensitive assets are deliberately excluded from this distribution archive.

---

## 1. Summary of Excluded Categories

| Category | Excluded Items / Patterns | Justification & Technical Reason |
| :--- | :--- | :--- |
| **Virtual Environments** | `.venv/`, `venv/`, `env/` | Machine-specific binaries, symlinks, and absolute OS paths. Must be freshly installed from `requirements-runtime.lock` or `requirements.txt`. |
| **Python Bytecode & Caches** | `__pycache__/`, `*.pyc`, `*.pyo`, `.pytest_cache/` | Ephemeral build artifacts generated dynamically during runtime execution. |
| **SQLite Databases & WAL Files**| `*.db`, `*.sqlite`, `*.sqlite3`, `*.db-wal`, `*.db-shm` | Live database files are excluded so recipients receive a clean schema ready for initialization. Zero runtime data is pre-populated. |
| **Version Control & Editor Metadata** | `.git/`, `.vscode/`, `.idea/`, `.DS_Store`, `Thumbs.db` | Developer-specific workstation state, editor configurations, and full local VCS history. |
| **Full Raw Datasets** | `student_placement_prediction_5000_with_probability.csv`, `student_placement_train_4000_with_probability.csv`, `student_placement_test_1000_with_probability.csv`, `data/raw/*` | Excluded to keep the distribution compact (~880 KB) and prevent data leakage. The inference engine relies solely on the frozen serialized model (`models/best_model.pkl`). |
| **Student Identification Records** | `reports/test_predictions.csv` | Contains student identifiers (`Student_ID`) and individual test set outcomes. Excluded to protect student privacy. Sanitized 9-feature test profiles (`tests/fixtures/`) are included instead. |
| **Local Secrets & Environment Files** | `.env`, `.env.*` (except `.env.example`) | Safeguards against credential or token leakage. |

---

## 2. Itemized File Exclusions Audit

### A. Raw CSV Datasets Excluded from Root & `data/raw/`
1. `student_placement_prediction_5000_with_probability.csv` (478,416 bytes)
2. `student_placement_train_4000_with_probability.csv` (382,803 bytes)
3. `student_placement_test_1000_with_probability.csv` (95,805 bytes)
4. `data/raw/student_placement_prediction_5000_with_probability.csv` (478,416 bytes)

**Total Dataset Size Excluded**: ~1.43 MB of raw research data.

### B. Live Database Files Excluded
- `data/*.sqlite`, `data/*.db`: All live database instances excluded. Re-created automatically on first write via `src/history_store.py: init_db()`.

### C. Student Test Set Log Excluded
- `reports/test_predictions.csv` (39,442 bytes): Contains 1,000 synthetic student IDs (`STU104736`, etc.).

---

## 3. Retained & Verified Assets
- **`models/best_model.pkl`**: Verified against reference SHA-256 hash `7330783a64173b5dadb941cc4c1342b9d89733dd63c951e151705e52a2acca17`.
- **`reports/*.png` & `reports/*.md`**: Preserved to document Phase 2 benchmark evaluation across 7 candidate algorithms.
- **`tests/fixtures/`**: Retained 5 synthetic profiles containing **strictly** the 9 authorized model inputs.
