# Deployment Guide — Student Placement Prediction System
### SRM Institute of Science and Technology · Department of Computer Science & Engineering

This guide provides instructions for deploying the full-stack Student Placement Prediction System to Vercel.

---

## 1. Quick Deploy to Vercel

The repository is pre-configured with `vercel.json`, root `package.json`, and `api/index.py`.

### Steps:
1. Log into your [Vercel Dashboard](https://vercel.com/dashboard).
2. Click **"Add New..."** → **"Project"**.
3. Select your GitHub repository: `ayushaman5823-cpu/student-placement-predction-system`.
4. In the Project Configuration:
   - **Framework Preset**: Vite (detected automatically).
   - **Root Directory**: `./` (Leave as default).
   - **Build Command**: `cd frontend && npm install && npm run build` (configured automatically via `vercel.json`).
   - **Output Directory**: `frontend/dist` (configured automatically).
5. Click **Deploy**.

---

## 2. Architecture on Vercel

- **Frontend**: React 19 + TypeScript + Tailwind CSS v4 built statically to `frontend/dist`.
- **Backend API**: Python FastAPI served via Vercel Serverless Function (`api/index.py`).
- **Rewrites**: All requests to `/api/*` are routed to the serverless function, while page navigation routes to `/index.html`.
- **Model Bundle**: `models/best_model.pkl` is bundled automatically via `includeFiles` in `vercel.json`.

---

## 3. Optional: Separate Backend Deployment (Render / Railway / Fly.io)

If you prefer to host the FastAPI backend on a dedicated Python container (e.g., Render, Railway, Fly.io, or VPS) and use Vercel purely for the high-performance edge React frontend:

1. **Deploy Backend**:
   - Host `api/app.py` with `uvicorn api.app:app --host 0.0.0.0 --port $PORT`.
   - Your backend will have a URL like `https://placement-api.onrender.com`.
2. **Configure Vercel Environment Variable**:
   - In Vercel Project Settings → **Environment Variables**:
     - Key: `VITE_API_URL`
     - Value: `https://placement-api.onrender.com`
   - Re-deploy. The React frontend will automatically send requests to your backend without code changes.

---

## 4. Local Execution

```bash
# 1-Click Launch on Windows
.\run_app.bat

# Or run via PowerShell
.\run_app.ps1
```
