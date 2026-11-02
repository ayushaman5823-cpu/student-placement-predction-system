import React, { useState, useEffect } from 'react';
import { 
  Sparkles, CheckCircle2, AlertTriangle, XCircle, RotateCcw, 
  UserCheck, ShieldAlert, Award, FileCode, Check, ArrowRight
} from 'lucide-react';
import type { StudentInput, PredictionResult, SampleProfile } from '../types';
import { predictStudentPlacement, fetchSampleProfiles } from '../api';

const DEFAULT_INPUT: StudentInput = {
  Branch: 'CSE',
  College_Tier: 'Tier 1',
  '10th_Percentage': 85.0,
  '12th_Percentage': 82.0,
  Current_CGPA: 8.20,
  Backlogs: 0,
  Attendance_Percentage: 88.0,
  Projects: 3,
  Internships: 1,
};

const BRANCH_OPTIONS = [
  'AI/ML', 'Biotechnology', 'CSE', 'Chemical', 'Civil',
  'Data Science', 'ECE', 'EEE', 'IT', 'Mechanical'
];

const TIER_OPTIONS = ['Tier 1', 'Tier 2', 'Tier 3'];

export const PredictorTab: React.FC = () => {
  const [formData, setFormData] = useState<StudentInput>(DEFAULT_INPUT);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [sampleProfiles, setSampleProfiles] = useState<SampleProfile[]>([]);
  const [activePreset, setActivePreset] = useState<string | null>(null);

  useEffect(() => {
    fetchSampleProfiles()
      .then(profiles => setSampleProfiles(profiles))
      .catch(() => {});
  }, []);

  const handleChange = (field: keyof StudentInput, value: any) => {
    setActivePreset(null);
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handlePresetSelect = (profile: SampleProfile) => {
    setActivePreset(profile.id);
    setFormData(profile.data);
    setError(null);
  };

  const handleReset = () => {
    setFormData(DEFAULT_INPUT);
    setActivePreset(null);
    setResult(null);
    setError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const pred = await predictStudentPlacement(formData);
      setResult(pred);
    } catch (err: any) {
      setError(err.message || 'Prediction request failed. Ensure backend API is running.');
    } finally {
      setLoading(false);
    }
  };

  const isAttendanceCritical = formData.Attendance_Percentage < 75.0;
  const isHighBacklogs = formData.Backlogs >= 3;

  return (
    <div className="space-y-8 max-w-7xl mx-auto py-4">
      {/* 1. Quick Preset Loaders (Inspired by Joey® component pills) */}
      <div className="rounded-[32px] bg-neutral-900/60 border border-neutral-800/80 p-6 sm:p-7 backdrop-blur-xl shadow-xl">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-5">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center text-white">
              <UserCheck className="w-4 h-4" />
            </div>
            <div>
              <h3 className="font-bold text-white text-base tracking-tight">
                Holdout Student Presets
              </h3>
              <p className="text-xs text-neutral-400">
                1-click selection from verified test set profiles
              </p>
            </div>
          </div>
          <span className="text-xs font-mono text-neutral-500">
            5 Verified Reference Profiles
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
          {sampleProfiles.map((p) => {
            const isSelected = activePreset === p.id;
            return (
              <button
                key={p.id}
                type="button"
                onClick={() => handlePresetSelect(p)}
                className={`text-left p-4 rounded-2xl border text-xs transition-all duration-200 cursor-pointer ${
                  isSelected
                    ? 'border-white bg-white text-black shadow-lg scale-[1.02]'
                    : 'border-neutral-800 bg-neutral-950/60 hover:bg-neutral-800/80 hover:border-neutral-700 text-neutral-200'
                }`}
              >
                <div className="font-bold truncate mb-1 text-sm tracking-tight">
                  {p.name}
                </div>
                <div className={`text-[11px] line-clamp-2 leading-relaxed mb-3 ${
                  isSelected ? 'text-neutral-700 font-medium' : 'text-neutral-400'
                }`}>
                  {p.description}
                </div>
                <div className="flex items-center justify-between text-[11px] font-mono font-bold pt-2 border-t border-black/10 dark:border-white/10">
                  <span className={
                    isSelected 
                      ? (p.expected_status === 'Placed' ? 'text-emerald-800' : 'text-rose-800')
                      : (p.expected_status === 'Placed' ? 'text-emerald-400' : 'text-rose-400')
                  }>
                    {p.expected_status}
                  </span>
                  <span className={isSelected ? 'text-black' : 'text-neutral-300'}>
                    {p.expected_prob_placed.toFixed(1)}%
                  </span>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* 2. Feature Input Form */}
        <div className="lg:col-span-7 rounded-[32px] bg-neutral-900/60 border border-neutral-800/80 p-6 sm:p-10 backdrop-blur-xl shadow-xl">
          <div className="flex items-center justify-between pb-6 mb-6 border-b border-neutral-800">
            <div>
              <span className="text-xs font-semibold uppercase tracking-wider text-neutral-400">
                Inference Inputs
              </span>
              <h2 className="text-2xl font-extrabold tracking-tight text-white mt-0.5">
                9-Feature Academic Profile
              </h2>
            </div>
            <button
              type="button"
              onClick={handleReset}
              className="inline-flex items-center gap-1.5 text-xs font-semibold text-neutral-400 hover:text-white px-3.5 py-2 rounded-full border border-neutral-800 hover:border-neutral-700 hover:bg-neutral-800 transition-all cursor-pointer"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Reset</span>
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Categorical Selectors */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
              {/* Branch */}
              <div>
                <label className="block text-xs font-semibold text-neutral-300 uppercase tracking-wider mb-2">
                  1. Engineering Branch
                </label>
                <select
                  value={formData.Branch}
                  onChange={e => handleChange('Branch', e.target.value)}
                  className="w-full text-sm rounded-2xl border border-neutral-800 bg-neutral-950/80 px-4 py-3 text-white shadow-inner focus:border-white focus:outline-hidden focus:ring-1 focus:ring-white transition-all font-medium cursor-pointer"
                >
                  {BRANCH_OPTIONS.map(b => (
                    <option key={b} value={b} className="bg-neutral-900 text-white">{b}</option>
                  ))}
                </select>
              </div>

              {/* College Tier */}
              <div>
                <label className="block text-xs font-semibold text-neutral-300 uppercase tracking-wider mb-2">
                  2. College Tier
                </label>
                <div className="grid grid-cols-3 gap-2">
                  {TIER_OPTIONS.map(t => {
                    const isSelected = formData.College_Tier === t;
                    return (
                      <button
                        key={t}
                        type="button"
                        onClick={() => handleChange('College_Tier', t)}
                        className={`py-3 px-2 rounded-2xl text-xs font-bold transition-all cursor-pointer ${
                          isSelected
                            ? 'bg-white text-black shadow-md'
                            : 'bg-neutral-950/80 border border-neutral-800 text-neutral-400 hover:text-white hover:bg-neutral-800'
                        }`}
                      >
                        {t}
                      </button>
                    );
                  })}
                </div>
              </div>
            </div>

            {/* Academic Board Percentages */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
              {/* 10th Percentage */}
              <div className="p-4 sm:p-5 rounded-2xl bg-neutral-950/60 border border-neutral-800/80">
                <div className="flex items-center justify-between mb-3">
                  <label className="text-xs font-semibold text-neutral-300 uppercase tracking-wider">
                    3. 10th Board Exam %
                  </label>
                  <span className="text-sm font-bold font-mono text-white px-2.5 py-1 rounded-lg bg-neutral-900 border border-neutral-800">
                    {formData['10th_Percentage'].toFixed(1)}%
                  </span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="100"
                  step="0.5"
                  value={formData['10th_Percentage']}
                  onChange={e => handleChange('10th_Percentage', parseFloat(e.target.value))}
                  className="w-full cursor-pointer"
                />
                <div className="flex justify-between text-[10px] font-mono text-neutral-500 mt-2">
                  <span>0%</span>
                  <span>Cutoff ~60%</span>
                  <span>100%</span>
                </div>
              </div>

              {/* 12th Percentage */}
              <div className="p-4 sm:p-5 rounded-2xl bg-neutral-950/60 border border-neutral-800/80">
                <div className="flex items-center justify-between mb-3">
                  <label className="text-xs font-semibold text-neutral-300 uppercase tracking-wider">
                    4. 12th Board Exam %
                  </label>
                  <span className="text-sm font-bold font-mono text-white px-2.5 py-1 rounded-lg bg-neutral-900 border border-neutral-800">
                    {formData['12th_Percentage'].toFixed(1)}%
                  </span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="100"
                  step="0.5"
                  value={formData['12th_Percentage']}
                  onChange={e => handleChange('12th_Percentage', parseFloat(e.target.value))}
                  className="w-full cursor-pointer"
                />
                <div className="flex justify-between text-[10px] font-mono text-neutral-500 mt-2">
                  <span>0%</span>
                  <span>Cutoff ~60%</span>
                  <span>100%</span>
                </div>
              </div>
            </div>

            {/* Current CGPA */}
            <div className="p-5 rounded-2xl bg-neutral-950/60 border border-neutral-800/80">
              <div className="flex items-center justify-between mb-3">
                <div>
                  <label className="text-xs font-semibold text-neutral-300 uppercase tracking-wider">
                    5. Current CGPA (0.00 – 10.00)
                  </label>
                  <span className="text-[11px] text-neutral-500 block mt-0.5">
                    Primary academic determinant (14.53% feature weight)
                  </span>
                </div>
                <span className="text-lg font-bold font-mono text-white px-3 py-1 rounded-xl bg-neutral-900 border border-neutral-800">
                  {formData.Current_CGPA.toFixed(2)}
                </span>
              </div>
              <input
                type="range"
                min="0"
                max="10"
                step="0.05"
                value={formData.Current_CGPA}
                onChange={e => handleChange('Current_CGPA', parseFloat(e.target.value))}
                className="w-full cursor-pointer"
              />
              <div className="flex justify-between text-[10px] font-mono text-neutral-500 mt-2">
                <span>0.00</span>
                <span>Tier 3 avg (6.5)</span>
                <span>Competitive (7.5+)</span>
                <span>10.00</span>
              </div>
            </div>

            {/* Attendance Percentage (With Critical Warning) */}
            <div className={`p-5 rounded-2xl border transition-all ${
              isAttendanceCritical
                ? 'bg-amber-950/30 border-amber-500/50'
                : 'bg-neutral-950/60 border-neutral-800/80'
            }`}>
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <label className="text-xs font-semibold text-neutral-300 uppercase tracking-wider">
                    6. Attendance Percentage (0 – 100%)
                  </label>
                  {isAttendanceCritical && (
                    <span className="inline-flex items-center gap-1 text-[11px] font-bold text-amber-400 bg-amber-950/60 border border-amber-500/40 px-2.5 py-0.5 rounded-full">
                      <AlertTriangle className="w-3.5 h-3.5" />
                      &lt;75% Critical
                    </span>
                  )}
                </div>
                <span className={`text-lg font-bold font-mono px-3 py-1 rounded-xl border ${
                  isAttendanceCritical 
                    ? 'text-amber-400 bg-amber-950/80 border-amber-500/50' 
                    : 'text-white bg-neutral-900 border-neutral-800'
                }`}>
                  {formData.Attendance_Percentage.toFixed(1)}%
                </span>
              </div>
              <input
                type="range"
                min="0"
                max="100"
                step="0.5"
                value={formData.Attendance_Percentage}
                onChange={e => handleChange('Attendance_Percentage', parseFloat(e.target.value))}
                className="w-full cursor-pointer"
              />
              <div className="flex justify-between text-[10px] font-mono text-neutral-500 mt-2">
                <span>0%</span>
                <span className="text-amber-400 font-semibold">Mandatory Cutoff (75%)</span>
                <span>100%</span>
              </div>
              {isAttendanceCritical && (
                <p className="text-xs text-amber-300 mt-3 font-medium leading-relaxed bg-amber-950/40 p-3 rounded-xl border border-amber-500/20">
                  Institutional Warning: The underlying model learned that students with &lt;75% attendance had a 0% placement rate due to campus drive disqualification.
                </p>
              )}
            </div>

            {/* Count Steppers: Backlogs, Projects, Internships */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {/* Backlogs */}
              <div className="p-4 rounded-2xl bg-neutral-950/60 border border-neutral-800/80 text-center">
                <label className="block text-xs font-semibold text-neutral-300 uppercase tracking-wider mb-2">
                  7. Backlogs
                </label>
                <div className="flex items-center justify-center gap-3">
                  <button
                    type="button"
                    onClick={() => handleChange('Backlogs', Math.max(0, formData.Backlogs - 1))}
                    className="w-9 h-9 rounded-full bg-neutral-800 text-white font-bold hover:bg-neutral-700 transition-colors cursor-pointer"
                  >
                    -
                  </button>
                  <span className={`text-xl font-bold font-mono w-8 ${
                    isHighBacklogs ? 'text-rose-400' : 'text-white'
                  }`}>
                    {formData.Backlogs}
                  </span>
                  <button
                    type="button"
                    onClick={() => handleChange('Backlogs', Math.min(5, formData.Backlogs + 1))}
                    className="w-9 h-9 rounded-full bg-neutral-800 text-white font-bold hover:bg-neutral-700 transition-colors cursor-pointer"
                  >
                    +
                  </button>
                </div>
                <span className="text-[10px] font-mono text-neutral-500 mt-2 block">0 to 5</span>
              </div>

              {/* Projects */}
              <div className="p-4 rounded-2xl bg-neutral-950/60 border border-neutral-800/80 text-center">
                <label className="block text-xs font-semibold text-neutral-300 uppercase tracking-wider mb-2">
                  8. Projects
                </label>
                <div className="flex items-center justify-center gap-3">
                  <button
                    type="button"
                    onClick={() => handleChange('Projects', Math.max(0, formData.Projects - 1))}
                    className="w-9 h-9 rounded-full bg-neutral-800 text-white font-bold hover:bg-neutral-700 transition-colors cursor-pointer"
                  >
                    -
                  </button>
                  <span className="text-xl font-bold font-mono text-white w-8">
                    {formData.Projects}
                  </span>
                  <button
                    type="button"
                    onClick={() => handleChange('Projects', Math.min(5, formData.Projects + 1))}
                    className="w-9 h-9 rounded-full bg-neutral-800 text-white font-bold hover:bg-neutral-700 transition-colors cursor-pointer"
                  >
                    +
                  </button>
                </div>
                <span className="text-[10px] font-mono text-neutral-500 mt-2 block">0 to 5</span>
              </div>

              {/* Internships */}
              <div className="p-4 rounded-2xl bg-neutral-950/60 border border-neutral-800/80 text-center">
                <label className="block text-xs font-semibold text-neutral-300 uppercase tracking-wider mb-2">
                  9. Internships
                </label>
                <div className="flex items-center justify-center gap-3">
                  <button
                    type="button"
                    onClick={() => handleChange('Internships', Math.max(0, formData.Internships - 1))}
                    className="w-9 h-9 rounded-full bg-neutral-800 text-white font-bold hover:bg-neutral-700 transition-colors cursor-pointer"
                  >
                    -
                  </button>
                  <span className="text-xl font-bold font-mono text-white w-8">
                    {formData.Internships}
                  </span>
                  <button
                    type="button"
                    onClick={() => handleChange('Internships', Math.min(4, formData.Internships + 1))}
                    className="w-9 h-9 rounded-full bg-neutral-800 text-white font-bold hover:bg-neutral-700 transition-colors cursor-pointer"
                  >
                    +
                  </button>
                </div>
                <span className="text-[10px] font-mono text-neutral-500 mt-2 block">0 to 4</span>
              </div>
            </div>

            {/* Error Message */}
            {error && (
              <div className="p-4 rounded-2xl bg-rose-950/40 border border-rose-500/40 text-rose-300 text-xs flex items-start gap-3">
                <XCircle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                <div className="leading-relaxed">{error}</div>
              </div>
            )}

            {/* Submit Action Button (Inspired by Joey® solid pill button) */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-4 px-8 rounded-full bg-white hover:bg-neutral-200 text-black font-extrabold text-sm sm:text-base tracking-tight shadow-xl flex items-center justify-center gap-3 transition-all duration-200 hover:scale-[1.01] active:scale-[0.99] disabled:opacity-50 cursor-pointer group"
            >
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-black/30 border-t-black rounded-full animate-spin" />
                  <span>Computing Inference Pipeline...</span>
                </>
              ) : (
                <>
                  <span>Generate Placement Prediction</span>
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </>
              )}
            </button>
          </form>
        </div>

        {/* 3. Prediction Result Panel */}
        <div className="lg:col-span-5 space-y-6">
          {result ? (
            <div className="rounded-[32px] bg-neutral-900/60 border border-neutral-800/80 p-6 sm:p-8 backdrop-blur-xl shadow-2xl space-y-6">
              <div className="flex items-center justify-between pb-4 border-b border-neutral-800">
                <span className="text-xs font-semibold tracking-wider uppercase text-neutral-400">
                  Model Output
                </span>
                {result.history_id && (
                  <span className="text-[11px] font-mono text-neutral-300 bg-neutral-800 border border-neutral-700 px-3 py-1 rounded-full">
                    SQLite #{result.history_id}
                  </span>
                )}
              </div>

              {/* Status Outcome Banner */}
              <div className={`p-8 rounded-[28px] border text-center transition-all ${
                result.predicted_status === 'Placed'
                  ? 'bg-gradient-to-br from-emerald-950/70 to-emerald-900/40 border-emerald-500/40 text-emerald-100 shadow-lg shadow-emerald-950/30'
                  : 'bg-gradient-to-br from-rose-950/70 to-rose-900/40 border-rose-500/40 text-rose-100 shadow-lg shadow-rose-950/30'
              }`}>
                <div className="w-16 h-16 mx-auto rounded-full flex items-center justify-center mb-4 shadow-xl">
                  {result.predicted_status === 'Placed' ? (
                    <div className="w-16 h-16 rounded-full bg-emerald-500 text-black flex items-center justify-center shadow-lg shadow-emerald-500/40">
                      <CheckCircle2 className="w-9 h-9" />
                    </div>
                  ) : (
                    <div className="w-16 h-16 rounded-full bg-rose-500 text-white flex items-center justify-center shadow-lg shadow-rose-500/40">
                      <XCircle className="w-9 h-9" />
                    </div>
                  )}
                </div>

                <span className="text-xs uppercase tracking-widest font-bold opacity-80">
                  Inference Classification
                </span>
                <h3 className="text-3xl sm:text-4xl font-black tracking-tight mt-1">
                  {result.predicted_status === 'Placed' ? 'LIKELY PLACED' : 'NOT PLACED'}
                </h3>
              </div>

              {/* Probability Meters */}
              <div className="space-y-4 pt-2">
                <div>
                  <div className="flex items-center justify-between text-xs font-semibold mb-2">
                    <span className="text-emerald-400 flex items-center gap-1.5">
                      <span className="w-2 h-2 rounded-full bg-emerald-400" />
                      Placed Probability
                    </span>
                    <span className="font-mono font-bold text-white text-sm">
                      {result.probability_placed.toFixed(2)}%
                    </span>
                  </div>
                  <div className="w-full h-3 bg-neutral-950 rounded-full overflow-hidden p-0.5 border border-neutral-800">
                    <div 
                      className="h-full bg-emerald-400 rounded-full transition-all duration-700 ease-out shadow-xs shadow-emerald-400/50"
                      style={{ width: `${result.probability_placed}%` }}
                    />
                  </div>
                </div>

                <div>
                  <div className="flex items-center justify-between text-xs font-semibold mb-2">
                    <span className="text-rose-400 flex items-center gap-1.5">
                      <span className="w-2 h-2 rounded-full bg-rose-400" />
                      Not Placed Probability
                    </span>
                    <span className="font-mono font-bold text-white text-sm">
                      {result.probability_not_placed.toFixed(2)}%
                    </span>
                  </div>
                  <div className="w-full h-3 bg-neutral-950 rounded-full overflow-hidden p-0.5 border border-neutral-800">
                    <div 
                      className="h-full bg-rose-400 rounded-full transition-all duration-700 ease-out shadow-xs shadow-rose-400/50"
                      style={{ width: `${result.probability_not_placed}%` }}
                    />
                  </div>
                </div>

                {/* Confidence Score Pill */}
                <div className="p-4 rounded-2xl bg-neutral-950/80 border border-neutral-800/80 flex items-center justify-between">
                  <div>
                    <span className="text-xs font-semibold text-neutral-300 block">
                      Top Class Confidence
                    </span>
                    <span className="text-[11px] font-mono text-neutral-500">
                      max(prob_placed, prob_not_placed)
                    </span>
                  </div>
                  <span className="text-xl font-black font-mono text-white">
                    {result.confidence_score.toFixed(2)}%
                  </span>
                </div>
              </div>

              {/* Actionable Academic Diagnostics (Figma list style) */}
              <div className="pt-4 border-t border-neutral-800">
                <h4 className="text-xs font-bold text-neutral-400 uppercase tracking-wider mb-3">
                  Academic Diagnostics &amp; Decision Factors
                </h4>
                <div className="space-y-2 text-xs">
                  {formData.Attendance_Percentage >= 85 ? (
                    <div className="flex items-start gap-2.5 text-emerald-300 bg-emerald-950/40 p-3 rounded-2xl border border-emerald-500/30">
                      <Check className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                      <span><strong>Attendance (88%+)</strong>: Strong attendance safely exceeds corporate campus drive eligibility criteria.</span>
                    </div>
                  ) : formData.Attendance_Percentage < 75 ? (
                    <div className="flex items-start gap-2.5 text-rose-300 bg-rose-950/40 p-3 rounded-2xl border border-rose-500/30">
                      <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                      <span><strong>Attendance Penalty (&lt;75%)</strong>: Model applies heavy negative weight; sub-75% attendance disqualifies students from placement drives.</span>
                    </div>
                  ) : (
                    <div className="flex items-start gap-2.5 text-amber-300 bg-amber-950/40 p-3 rounded-2xl border border-amber-500/30">
                      <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                      <span><strong>Attendance Borderline (75-85%)</strong>: Meets minimum eligibility, but higher attendance strengthens recruiter confidence.</span>
                    </div>
                  )}

                  {formData.Backlogs > 0 && (
                    <div className="flex items-start gap-2.5 text-amber-300 bg-amber-950/40 p-3 rounded-2xl border border-amber-500/30">
                      <ShieldAlert className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                      <span><strong>Backlog Penalty ({formData.Backlogs})</strong>: Active backlogs directly reduce likelihood; clearing them is essential for Tier 1 recruiters.</span>
                    </div>
                  )}

                  {formData.Current_CGPA >= 8.0 && (
                    <div className="flex items-start gap-2.5 text-blue-300 bg-blue-950/40 p-3 rounded-2xl border border-blue-500/30">
                      <Award className="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />
                      <span><strong>CGPA Advantage ({formData.Current_CGPA.toFixed(2)})</strong>: Strong grade average qualifies for high-tier technical interview rounds.</span>
                    </div>
                  )}
                </div>
              </div>

              {/* Provenance Footer */}
              <div className="pt-3 border-t border-neutral-800 flex items-center justify-between text-[11px] text-neutral-500 font-mono">
                <span>Gradient Boosting Pipeline</span>
                <span>SHA: {result.model_version.slice(0, 10)}...</span>
              </div>
            </div>
          ) : (
            /* Standby State */
            <div className="rounded-[32px] bg-neutral-900/60 border border-neutral-800/80 p-8 sm:p-10 backdrop-blur-xl text-center shadow-xl">
              <div className="w-16 h-16 mx-auto rounded-full bg-neutral-800/80 border border-neutral-700 flex items-center justify-center text-white mb-5 shadow-lg">
                <Sparkles className="w-7 h-7" />
              </div>
              <h3 className="font-extrabold text-white text-lg tracking-tight">
                Awaiting Student Profile
              </h3>
              <p className="text-xs sm:text-sm text-neutral-400 mt-2 max-w-xs mx-auto leading-relaxed">
                Adjust features on the left or select a verified preset above, then click <strong>Generate Placement Prediction</strong>.
              </p>
              <div className="mt-8 p-5 rounded-2xl bg-neutral-950/80 border border-neutral-800/80 text-left text-xs text-neutral-400 space-y-2">
                <div className="font-bold text-white flex items-center gap-2">
                  <FileCode className="w-4 h-4 text-neutral-300" />
                  <span>Pipeline Execution Contract:</span>
                </div>
                <p className="text-[11px] leading-relaxed text-neutral-400">
                  Raw input values pass through scikit-learn `ColumnTransformer` (OneHotEncoder + StandardScaler) into `GradientBoostingClassifier` without retaining PII.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
