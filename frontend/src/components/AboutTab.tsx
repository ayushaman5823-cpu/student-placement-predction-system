import React, { useState } from 'react';
import { GraduationCap, Ban, Server, Database, Code2, Cpu, Plus, Minus } from 'lucide-react';

interface AccordionItem {
  id: string;
  title: string;
  content: React.ReactNode;
}

export const AboutTab: React.FC = () => {
  const [openItems, setOpenItems] = useState<Record<string, boolean>>({
    'contract': true,
    'exclusions': true,
  });

  const toggleItem = (id: string) => {
    setOpenItems(prev => ({
      ...prev,
      [id]: !prev[id]
    }));
  };

  const accordionData: AccordionItem[] = [
    {
      id: 'contract',
      title: 'Strict 9-Feature Input Contract & Permitted Bounds',
      content: (
        <div className="space-y-4 pt-2">
          <p className="text-xs sm:text-sm text-neutral-400 leading-relaxed">
            The frozen Gradient Boosting pipeline strictly requires nine academic features in order. All values are validated against schema boundaries before pipeline inference:
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
            {[
              { num: '1', name: 'Branch', range: '10 engineering disciplines' },
              { num: '2', name: 'College_Tier', range: 'Tier 1, Tier 2, Tier 3' },
              { num: '3', name: '10th_Percentage', range: '0.0 to 100.0%' },
              { num: '4', name: '12th_Percentage', range: '0.0 to 100.0%' },
              { num: '5', name: 'Current_CGPA', range: '0.00 to 10.00' },
              { num: '6', name: 'Backlogs', range: '0 to 5 (integer count)' },
              { num: '7', name: 'Attendance_Percentage', range: '0.0 to 100.0%' },
              { num: '8', name: 'Projects', range: '0 to 5 (integer count)' },
              { num: '9', name: 'Internships', range: '0 to 4 (integer count)' },
            ].map(f => (
              <div key={f.num} className="p-3.5 rounded-2xl bg-neutral-950/80 border border-neutral-800">
                <span className="font-mono font-bold text-white text-xs">{f.num}. {f.name}</span>
                <span className="text-neutral-400 text-[11px] block mt-0.5">{f.range}</span>
              </div>
            ))}
          </div>
        </div>
      )
    },
    {
      id: 'exclusions',
      title: 'Explicit Anti-Leakage & Privacy Rules (Blocked Columns)',
      content: (
        <div className="space-y-3 pt-2">
          <p className="text-xs sm:text-sm text-neutral-400 leading-relaxed">
            The following columns are strictly blocked at both the API schema and inference pipeline levels to preserve demographic fairness and avoid target leakage:
          </p>
          <div className="flex flex-wrap gap-2.5 pt-1">
            {[
              { label: 'Student_ID', reason: 'Direct PII' },
              { label: 'Name', reason: 'Direct PII' },
              { label: 'Gender', reason: 'Demographic Fairness' },
              { label: 'College_Name', reason: 'High Cardinality Bias' },
              { label: 'Placement_Probability', reason: 'Target Leakage Prevention' },
            ].map(col => (
              <span
                key={col.label}
                className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-rose-950/40 border border-rose-500/30 text-rose-300 font-mono text-xs"
              >
                <Ban className="w-3.5 h-3.5 text-rose-400" />
                <span>{col.label}</span>
                <span className="text-rose-400/60 font-sans text-[10px]">({col.reason})</span>
              </span>
            ))}
          </div>
        </div>
      )
    },
    {
      id: 'probabilities',
      title: 'Probability Calculation & Confidence Semantics',
      content: (
        <div className="space-y-3 pt-2 text-xs sm:text-sm text-neutral-400 leading-relaxed">
          <p>
            The placement likelihood is calculated directly via <code className="text-white font-mono bg-neutral-950 px-2 py-0.5 rounded">model.predict_proba()</code> on the frozen Gradient Boosting ensemble. The probabilities for <strong className="text-white">Placed</strong> and <strong className="text-white">Not Placed</strong> sum to 100%.
          </p>
          <p>
            <strong className="text-white">Confidence Score</strong> is defined as <code className="text-white font-mono bg-neutral-950 px-2 py-0.5 rounded">max(probability_placed, probability_not_placed)</code>. It indicates the classifier certainty in its top binary decision, rather than an uncalibrated heuristic.
          </p>
        </div>
      )
    },
    {
      id: 'limitations',
      title: 'Synthetic Data Notice & Academic Limitations',
      content: (
        <div className="space-y-3 pt-2 text-xs sm:text-sm text-neutral-400 leading-relaxed">
          <p>
            The dataset used in this academic project consists of 5,000 synthetic undergraduate records designed to simulate placement dynamics. The 83.10% holdout accuracy demonstrates that the ensemble successfully uncovered the underlying synthetic generation logic.
          </p>
          <p className="text-amber-300/90 bg-amber-950/30 p-4 rounded-2xl border border-amber-500/30">
            <strong>Important Notice</strong>: Predicted probabilities reflect academic rule evaluation and should not be treated as a guarantee of external corporate employment offers.
          </p>
        </div>
      )
    }
  ];

  return (
    <div className="space-y-12 max-w-5xl mx-auto py-4">
      {/* 1. Project Overview Header */}
      <div className="rounded-[32px] bg-neutral-900/60 p-8 sm:p-10 border border-neutral-800/80 shadow-2xl space-y-5">
        <div className="flex items-center gap-3.5">
          <div className="w-12 h-12 rounded-full bg-white/10 flex items-center justify-center text-white shadow-lg">
            <GraduationCap className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              Student Placement Prediction System
            </h2>
            <p className="text-xs sm:text-sm text-neutral-400 font-medium">
              SRM Institute of Science and Technology · Department of Computer Science &amp; Engineering
            </p>
          </div>
        </div>
        <p className="text-xs sm:text-sm text-neutral-400 leading-relaxed font-normal">
          An end-to-end Machine Learning web application designed to forecast undergraduate engineering placement likelihood based strictly on verified academic metrics. The underlying classifier was trained and evaluated on 5,000 student records, achieving an authoritative 83.10% accuracy on an untouched holdout partition.
        </p>
      </div>

      {/* 2. Minimalist Accordion (Directly inspired by FAQ accordion in Figma Image 1) */}
      <div className="rounded-[32px] bg-neutral-900/60 p-6 sm:p-10 border border-neutral-800/80 shadow-2xl space-y-6">
        <div>
          <span className="text-xs font-semibold uppercase tracking-wider text-neutral-400">
            Architecture &amp; Rules
          </span>
          <h3 className="text-2xl font-extrabold tracking-tight text-white mt-1">
            System Specifications &amp; Contracts
          </h3>
        </div>

        <div className="divide-y divide-neutral-800">
          {accordionData.map((item) => {
            const isOpen = !!openItems[item.id];
            return (
              <div key={item.id} className="py-5 first:pt-2 last:pb-2">
                <button
                  type="button"
                  onClick={() => toggleItem(item.id)}
                  className="w-full flex items-center justify-between text-left text-sm sm:text-base font-bold text-white hover:text-neutral-300 transition-colors cursor-pointer group"
                >
                  <span className="tracking-tight">{item.title}</span>
                  <div className="w-8 h-8 rounded-full bg-neutral-800 text-neutral-300 flex items-center justify-center group-hover:bg-neutral-700 transition-all shrink-0 ml-4">
                    {isOpen ? <Minus className="w-4 h-4" /> : <Plus className="w-4 h-4" />}
                  </div>
                </button>

                {isOpen && (
                  <div className="mt-3 animate-fadeIn">
                    {item.content}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* 3. Full-Stack Architecture Grid */}
      <div className="rounded-[32px] bg-neutral-900/60 p-6 sm:p-10 border border-neutral-800/80 shadow-2xl space-y-6">
        <div>
          <span className="text-xs font-semibold uppercase tracking-wider text-neutral-400">
            Technology Stack
          </span>
          <h3 className="text-2xl font-extrabold tracking-tight text-white mt-1">
            Four-Tier System Architecture
          </h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs">
          <div className="p-5 rounded-2xl bg-neutral-950/80 border border-neutral-800 space-y-2">
            <div className="flex items-center gap-2 font-bold text-white text-sm">
              <Code2 className="w-4 h-4 text-neutral-300" />
              <span>React 19 + Vite</span>
            </div>
            <p className="text-neutral-400 leading-relaxed">
              TypeScript SPA styled with Tailwind CSS v4, Lucide icons, responsive tables, and interactive input sliders.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-neutral-950/80 border border-neutral-800 space-y-2">
            <div className="flex items-center gap-2 font-bold text-white text-sm">
              <Server className="w-4 h-4 text-neutral-300" />
              <span>FastAPI REST</span>
            </div>
            <p className="text-neutral-400 leading-relaxed">
              Asynchronous Python backend with Pydantic schema validation, CORS security, and error handling.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-neutral-950/80 border border-neutral-800 space-y-2">
            <div className="flex items-center gap-2 font-bold text-white text-sm">
              <Cpu className="w-4 h-4 text-neutral-300" />
              <span>ML Inference</span>
            </div>
            <p className="text-neutral-400 leading-relaxed">
              Scikit-learn Gradient Boosting pipeline (`models/best_model.pkl`) with verified SHA-256 integrity.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-neutral-950/80 border border-neutral-800 space-y-2">
            <div className="flex items-center gap-2 font-bold text-white text-sm">
              <Database className="w-4 h-4 text-neutral-300" />
              <span>SQLite Store</span>
            </div>
            <p className="text-neutral-400 leading-relaxed">
              Thread-safe query logging (`data/history.sqlite`) storing only academic features and model probabilities.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
