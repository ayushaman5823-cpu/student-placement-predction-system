import type { StudentInput, PredictionResult, ModelInfo, SampleProfile, HistoryRecord } from './types';

// Resolves Vercel service binding (API_URL), custom environment override (VITE_API_URL), or default relative path (/api)
const API_BASE = (import.meta as any).env?.API_URL 
  ? `${(import.meta as any).env.API_URL}/api`
  : (import.meta as any).env?.VITE_API_URL 
    ? `${(import.meta as any).env.VITE_API_URL}/api` 
    : '/api';

export async function checkHealth(): Promise<{ status: string; model_artifact_sha256?: string }> {
  try {
    const res = await fetch(`${API_BASE}/health`, { signal: AbortSignal.timeout(3000) });
    if (!res.ok) throw new Error('Health check failed');
    return await res.json();
  } catch (err) {
    return { status: 'offline' };
  }
}

export async function predictStudentPlacement(input: StudentInput): Promise<PredictionResult> {
  const res = await fetch(`${API_BASE}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input)
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Unknown inference error' }));
    throw new Error(err.detail || 'Prediction failed');
  }

  const json = await res.json();
  return json.data;
}

export async function fetchModelInfo(): Promise<ModelInfo> {
  const res = await fetch(`${API_BASE}/model/info`);
  if (!res.ok) throw new Error('Failed to fetch model info');
  const json = await res.json();
  return json.data;
}

export async function fetchSampleProfiles(): Promise<SampleProfile[]> {
  const res = await fetch(`${API_BASE}/sample-profiles`);
  if (!res.ok) throw new Error('Failed to fetch sample profiles');
  const json = await res.json();
  return json.data;
}

export async function fetchHistoryRecords(limit = 50, offset = 0): Promise<HistoryRecord[]> {
  const res = await fetch(`${API_BASE}/history?limit=${limit}&offset=${offset}`);
  if (!res.ok) throw new Error('Failed to fetch history');
  const json = await res.json();
  return json.data;
}

export async function clearAllHistory(): Promise<void> {
  const res = await fetch(`${API_BASE}/history`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Failed to clear history');
}
