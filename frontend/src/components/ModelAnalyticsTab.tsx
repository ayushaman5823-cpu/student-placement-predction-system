import React, { useState, useEffect } from 'react';
import { Award, ShieldCheck, AlertTriangle, Layers, Lock } from 'lucide-react';
import type { ModelInfo } from '../types';
import { fetchModelInfo } from '../api';

export const ModelAnalyticsTab: React.FC = () => {
  const [modelInfo, setModelInfo] = useState<ModelInfo | null>(null);

  useEffect(() => {
    fetchModelInfo()
      .then(info => setModelInfo(info))
      .catch(() => {});
  }, []);

  const metrics = modelInfo?.holdout_test_metrics || {
    accuracy: 0.8310,
    precision: 0.8276,
    recall: 0.9019,
    f1_score: 0.8632,
    roc_auc: 0.9036,
    brier_score: 0.1158
  };

  const cm = modelInfo?.confusion_matrix || {
    true_negatives: 298,
    false_positives: 111,
    false_negatives: 58,
    true_positives: 533
  };

  const featureImportances = modelInfo?.feature_importances || [
    { feature: "Attendance_Percentage", importance_pct: 57.80 },
    { feature: "Current_CGPA", importance_pct: 14.53 },
    { feature: "12th_Percentage", importance_pct: 12.41 },
    { feature: "10th_Percentage", importance_pct: 7.27 },
    { feature: "Backlogs", importance_pct: 4.88 },
    { feature: "Internships", importance_pct: 1.28 },
    { feature: "Projects", importance_pct: 0.94 },
    { feature: "College_Tier", importance_pct: 0.60 },
    { feature: "Branch", importance_pct: 0.29 }
  ];

  return (
    <div className="space-y-8 max-w-7xl mx-auto py-4">
      {/* 1. Architecture Banner (Inspired by Joey® showcase card) */}
      <div className="rounded-[32px] bg-gradient-to-br from-neutral-900 via-neutral-900 to-neutral-950 p-7 sm:p-10 border border-neutral-800/80 text-white shadow-2xl relative overflow-hidden">
        <div className="relative z-10 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="space-y-3 max-w-2xl">
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/10 border border-white/15 text-neutral-300 text-xs font-semibold uppercase tracking-wider">
              <Layers className="w-3.5 h-3.5 text-white" />
              <span>Production Model Architecture</span>
            </div>
            <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-white leading-tight">
              Gradient Boosting Classifier Ensemble
            </h2>
            <p className="text-xs sm:text-sm text-neutral-400 leading-relaxed font-normal">
              Trained on 4,000 student training records using Stratified 5-Fold Cross-Validation, and evaluated on an untouched 1,000-student holdout partition. Selected over Random Forest, XGBoost, SVM, Decision Tree, KNN, and Logistic Regression.
            </p>
          </div>

          <div className="bg-neutral-950/80 backdrop-blur-md rounded-2xl p-5 border border-white/10 text-xs space-y-2 shrink-0 font-mono shadow-xl">
            <div className="flex items-center gap-2 text-white font-bold">
              <Lock className="w-4 h-4 text-emerald-400" />
              <span>FROZEN ARTIFACT</span>
            </div>
            <div className="text-neutral-300 text-xs">models/best_model.pkl</div>
            <div className="text-neutral-500 text-[10px] truncate max-w-[200px]">
              SHA-256: 7330783a64173b5dadb941...
            </div>
          </div>
        </div>
      </div>

      {/* 2. Authoritative Benchmark Metrics Grid */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center text-white">
              <Award className="w-4 h-4" />
            </div>
            <h3 className="text-lg sm:text-xl font-bold tracking-tight text-white">
              Empirical Holdout Metrics (1,000 Untouched Test Samples)
            </h3>
          </div>
          <span className="text-xs font-mono text-neutral-500 hidden sm:inline">
            Fixed Holdout Baseline
          </span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3.5 sm:gap-4">
          <div className="rounded-2xl bg-neutral-900/60 p-5 border border-neutral-800/80 shadow-md">
            <span className="text-[11px] font-semibold text-neutral-400 uppercase tracking-wider block">
              Test Accuracy
            </span>
            <span className="text-2xl sm:text-3xl font-black font-mono text-white mt-1 block">
              {(metrics.accuracy * 100).toFixed(2)}%
            </span>
            <span className="text-[10px] font-mono text-neutral-500 mt-1 block">831 / 1,000 correct</span>
          </div>

          <div className="rounded-2xl bg-neutral-900/60 p-5 border border-neutral-800/80 shadow-md">
            <span className="text-[11px] font-semibold text-neutral-400 uppercase tracking-wider block">
              Test Precision
            </span>
            <span className="text-2xl sm:text-3xl font-black font-mono text-white mt-1 block">
              {(metrics.precision * 100).toFixed(2)}%
            </span>
            <span className="text-[10px] font-mono text-neutral-500 mt-1 block">TP / (TP + FP)</span>
          </div>

          <div className="rounded-2xl bg-neutral-900/60 p-5 border border-neutral-800/80 shadow-md">
            <span className="text-[11px] font-semibold text-neutral-400 uppercase tracking-wider block">
              Test Recall
            </span>
            <span className="text-2xl sm:text-3xl font-black font-mono text-white mt-1 block">
              {(metrics.recall * 100).toFixed(2)}%
            </span>
            <span className="text-[10px] font-mono text-neutral-500 mt-1 block">TP / (TP + FN)</span>
          </div>

          <div className="rounded-2xl bg-neutral-900/60 p-5 border border-neutral-800/80 shadow-md">
            <span className="text-[11px] font-semibold text-neutral-400 uppercase tracking-wider block">
              Test F1-Score
            </span>
            <span className="text-2xl sm:text-3xl font-black font-mono text-white mt-1 block">
              {metrics.f1_score.toFixed(4)}
            </span>
            <span className="text-[10px] font-mono text-neutral-500 mt-1 block">Harmonic Mean</span>
          </div>

          <div className="rounded-2xl bg-neutral-900/60 p-5 border border-neutral-800/80 shadow-md">
            <span className="text-[11px] font-semibold text-neutral-400 uppercase tracking-wider block">
              ROC-AUC
            </span>
            <span className="text-2xl sm:text-3xl font-black font-mono text-white mt-1 block">
              {metrics.roc_auc.toFixed(4)}
            </span>
            <span className="text-[10px] font-mono text-neutral-500 mt-1 block">Discrimination capability</span>
          </div>

          <div className="rounded-2xl bg-neutral-900/60 p-5 border border-neutral-800/80 shadow-md">
            <span className="text-[11px] font-semibold text-neutral-400 uppercase tracking-wider block">
              Brier Score
            </span>
            <span className="text-2xl sm:text-3xl font-black font-mono text-emerald-400 mt-1 block">
              {metrics.brier_score.toFixed(4)}
            </span>
            <span className="text-[10px] font-mono text-neutral-500 mt-1 block">Mean Squared Error</span>
          </div>
        </div>
      </div>

      {/* 3. Confusion Matrix and Feature Importance */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Confusion Matrix */}
        <div className="lg:col-span-5 rounded-[32px] bg-neutral-900/60 p-6 sm:p-8 border border-neutral-800/80 shadow-xl space-y-5">
          <div className="flex items-center justify-between pb-4 border-b border-neutral-800">
            <div>
              <h4 className="font-bold text-white text-base tracking-tight">Holdout Confusion Matrix</h4>
              <p className="text-xs text-neutral-400 mt-0.5">1,000 untouched evaluation samples</p>
            </div>
            <span className="text-xs font-mono font-bold text-neutral-300 bg-neutral-800 border border-neutral-700 px-3 py-1 rounded-full">
              N = 1,000
            </span>
          </div>

          <div className="grid grid-cols-2 gap-3.5 pt-1">
            <div className="p-5 rounded-2xl bg-neutral-950/80 border border-neutral-800 text-center">
              <span className="text-[11px] font-semibold text-neutral-400 uppercase tracking-wider block">
                True Negatives (TN)
              </span>
              <span className="text-3xl font-black font-mono text-white mt-1.5 block">
                {cm.true_negatives}
              </span>
              <span className="text-[10px] font-mono text-neutral-500 mt-1 block">Correct Not Placed</span>
            </div>

            <div className="p-5 rounded-2xl bg-rose-950/30 border border-rose-500/30 text-center">
              <span className="text-[11px] font-semibold text-rose-300 uppercase tracking-wider block">
                False Positives (FP)
              </span>
              <span className="text-3xl font-black font-mono text-rose-400 mt-1.5 block">
                {cm.false_positives}
              </span>
              <span className="text-[10px] font-mono text-rose-500/80 mt-1 block">Type I Error</span>
            </div>

            <div className="p-5 rounded-2xl bg-amber-950/30 border border-amber-500/30 text-center">
              <span className="text-[11px] font-semibold text-amber-300 uppercase tracking-wider block">
                False Negatives (FN)
              </span>
              <span className="text-3xl font-black font-mono text-amber-400 mt-1.5 block">
                {cm.false_negatives}
              </span>
              <span className="text-[10px] font-mono text-amber-500/80 mt-1 block">Type II Error</span>
            </div>

            <div className="p-5 rounded-2xl bg-emerald-950/30 border border-emerald-500/30 text-center">
              <span className="text-[11px] font-semibold text-emerald-300 uppercase tracking-wider block">
                True Positives (TP)
              </span>
              <span className="text-3xl font-black font-mono text-emerald-400 mt-1.5 block">
                {cm.true_positives}
              </span>
              <span className="text-[10px] font-mono text-emerald-500/80 mt-1 block">Correct Placed</span>
            </div>
          </div>

          <div className="p-4 rounded-2xl bg-neutral-950/60 text-xs text-neutral-400 leading-relaxed border border-neutral-800/80">
            <strong className="text-white font-semibold">Balanced Performance</strong>: Sensitivity (Recall) of 90.19% ensures strong capture of eligible students, while precision of 82.76% maintains trustworthy placement likelihoods.
          </div>
        </div>

        {/* Feature Importance Ranking Chart */}
        <div className="lg:col-span-7 rounded-[32px] bg-neutral-900/60 p-6 sm:p-8 border border-neutral-800/80 shadow-xl space-y-5">
          <div className="flex items-center justify-between pb-4 border-b border-neutral-800">
            <div>
              <h4 className="font-bold text-white text-base tracking-tight">Gini Feature Importance (MDI)</h4>
              <p className="text-xs text-neutral-400 mt-0.5">Impurity reduction aggregated across all decision tree splits</p>
            </div>
            <span className="text-xs font-semibold text-white bg-neutral-800 border border-neutral-700 px-3 py-1 rounded-full">
              9 Feature Groups
            </span>
          </div>

          <div className="space-y-3 pt-1">
            {featureImportances.map((item, index) => (
              <div key={item.feature} className="space-y-1.5">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-medium text-neutral-300 flex items-center gap-2">
                    <span className="font-mono text-[11px] text-neutral-500 w-4">{index + 1}.</span>
                    <span>{item.feature}</span>
                  </span>
                  <span className="font-mono font-bold text-white">
                    {item.importance_pct.toFixed(2)}%
                  </span>
                </div>
                <div className="w-full h-2.5 bg-neutral-950 rounded-full overflow-hidden p-0.5 border border-neutral-800">
                  <div
                    className="h-full bg-gradient-to-r from-neutral-200 to-white rounded-full transition-all duration-700"
                    style={{ width: `${Math.max(item.importance_pct, 1.5)}%` }}
                  />
                </div>
              </div>
            ))}
          </div>

          <div className="p-4 rounded-2xl bg-neutral-950/60 text-xs text-neutral-400 leading-relaxed border border-neutral-800/80">
            <strong className="text-white font-semibold">Key Decision Driver</strong>: `Attendance_Percentage` (57.80%) and `Current_CGPA` (14.53%) together account for 72.33% of the total ensemble split weights, reflecting institutional eligibility thresholds.
          </div>
        </div>
      </div>

      {/* 4. Methodological Distinction & Disclaimers */}
      <div className="rounded-[32px] bg-neutral-900/60 p-6 sm:p-8 border border-neutral-800/80 shadow-xl space-y-5">
        <h4 className="text-base font-bold text-white flex items-center gap-2.5">
          <ShieldCheck className="w-5 h-5 text-neutral-300" />
          <span>Scientific Methodology &amp; Limitations</span>
        </h4>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div className="p-5 rounded-2xl bg-neutral-950/60 border border-neutral-800/80 space-y-2">
            <strong className="text-white text-sm block">Gini Impurity (MDI)</strong>
            <p className="text-neutral-400 leading-relaxed">
              Derived natively from tree node impurity reduction. Fast and intrinsic to tree structure. Transformed one-hot features are grouped back to the 9 primary inputs.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-neutral-950/60 border border-neutral-800/80 space-y-2">
            <strong className="text-white text-sm block">Permutation Importance</strong>
            <p className="text-neutral-400 leading-relaxed">
              Evaluates performance drop when a single feature is randomly shuffled on holdout data. Provides a model-agnostic check against cardinally biased trees.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-amber-950/30 border border-amber-500/30 space-y-2">
            <strong className="text-amber-300 text-sm block flex items-center gap-1.5">
              <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
              <span>Synthetic Data Notice</span>
            </strong>
            <p className="text-amber-300/80 leading-relaxed">
              The project dataset is synthetic/augmented. Probabilities reflect model rule learning rather than guaranteed real-world job market offers.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
