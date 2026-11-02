import React from 'react';
import { ArrowDown, ArrowUpRight, Cpu, Target, Layers, Database } from 'lucide-react';

interface HeroSectionProps {
  onNavigateTab: (tab: 'predictor' | 'history' | 'analytics' | 'about') => void;
  onScrollToPredictor: () => void;
}

export const HeroSection: React.FC<HeroSectionProps> = ({
  onNavigateTab,
  onScrollToPredictor,
}) => {
  return (
    <section className="pt-24 sm:pt-32 pb-12 sm:pb-16 flex flex-col gap-12 sm:gap-16">
      {/* Editorial Headline (Inspired by Websites & Branding from Figma) */}
      <div className="flex flex-col gap-8">
        <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-6">
          <h1 className="text-5xl sm:text-7xl lg:text-8xl font-extrabold tracking-tight text-white leading-[0.95]">
            Placement<span className="text-neutral-500">&</span>
            <br />
            Intelligence
          </h1>

          <div className="flex items-center gap-3 self-start lg:self-end">
            <button
              onClick={onScrollToPredictor}
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-neutral-900 border border-white/10 text-xs sm:text-sm font-semibold tracking-wide text-neutral-300 hover:text-white hover:border-white/30 hover:bg-neutral-800 transition-all group"
            >
              <span>SCROLL DOWN</span>
              <ArrowDown className="w-3.5 h-3.5 group-hover:translate-y-0.5 transition-transform" />
            </button>
          </div>
        </div>

        {/* 2-Column Editorial Subtext */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-6 pt-4 border-t border-neutral-800/80 text-sm">
          <div className="md:col-span-4 flex flex-col gap-1">
            <span className="text-xs uppercase tracking-wider font-bold text-neutral-400">
              Department & Affiliation
            </span>
            <span className="text-white font-medium">
              SRM Institute of Science and Technology
            </span>
            <span className="text-neutral-500 text-xs">
              Department of Computer Science & Engineering · B.Tech Capstone
            </span>
          </div>

          <div className="md:col-span-8 text-neutral-400 leading-relaxed font-normal">
            An end-to-end Machine Learning prediction engine engineered with a frozen Gradient Boosting ensemble. Evaluated on an untouched 1,000-student holdout partition, achieving an authoritative <strong className="text-white font-semibold">83.10% accuracy</strong> and <strong className="text-white font-semibold">90.19% recall</strong> across strictly nine verified academic features with complete demographic fairness.
          </div>
        </div>
      </div>

      {/* The 4 Signature Showcase Cards (Inspired by the 4 vibrant color cards from Figma template) */}
      <div className="flex flex-col gap-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl sm:text-3xl font-bold tracking-tight text-white">
              System Modules
            </h2>
            <p className="text-xs sm:text-sm text-neutral-400">
              Explore the four core operational engines powering the placement prediction suite.
            </p>
          </div>
          <span className="text-xs font-mono text-neutral-500 hidden sm:inline">
            4 / 4 Active
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5 sm:gap-6">
          {/* Card 1: Electric Purple / Violet (Predictor) */}
          <div
            onClick={onScrollToPredictor}
            className="group relative rounded-[32px] bg-gradient-to-br from-[#7C3AED] to-[#5B21B6] p-8 sm:p-10 text-white flex flex-col justify-between min-h-[300px] sm:min-h-[340px] cursor-pointer shadow-xl transition-all duration-300 hover:scale-[1.01] hover:shadow-purple-500/20"
          >
            <div className="flex items-start justify-between">
              <span className="px-3.5 py-1.5 rounded-full bg-white/15 backdrop-blur-md text-xs font-semibold tracking-wide uppercase border border-white/20">
                Core Engine
              </span>
              <div className="w-10 h-10 rounded-full bg-white/10 backdrop-blur-md flex items-center justify-center group-hover:bg-white group-hover:text-purple-900 transition-all">
                <ArrowUpRight className="w-5 h-5 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
              </div>
            </div>

            <div className="flex flex-col gap-3 mt-8">
              <div className="flex items-center gap-2">
                <Cpu className="w-5 h-5 opacity-80" />
                <span className="text-xs tracking-wider uppercase font-semibold opacity-90">
                  Interactive Inference
                </span>
              </div>
              <h3 className="text-3xl sm:text-4xl font-extrabold tracking-tight leading-tight">
                Placement Predictor
              </h3>
              <p className="text-white/80 text-sm max-w-sm">
                Estimate placement likelihood using 9 strict academic features, real-time probability meters, and 5 verified holdout student presets.
              </p>
            </div>
          </div>

          {/* Card 2: Lime / Acid Neon Green (Empirical Benchmark) */}
          <div
            onClick={() => onNavigateTab('analytics')}
            className="group relative rounded-[32px] bg-[#A3E635] p-8 sm:p-10 text-neutral-950 flex flex-col justify-between min-h-[300px] sm:min-h-[340px] cursor-pointer shadow-xl transition-all duration-300 hover:scale-[1.01] hover:shadow-lime-500/20"
          >
            <div className="flex items-start justify-between">
              <span className="px-3.5 py-1.5 rounded-full bg-black/10 backdrop-blur-md text-xs font-bold tracking-wide uppercase border border-black/15">
                83.10% Holdout
              </span>
              <div className="w-10 h-10 rounded-full bg-black/10 backdrop-blur-md flex items-center justify-center group-hover:bg-black group-hover:text-lime-400 transition-all">
                <ArrowUpRight className="w-5 h-5 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
              </div>
            </div>

            <div className="flex flex-col gap-3 mt-8">
              <div className="flex items-center gap-2">
                <Target className="w-5 h-5 opacity-90" />
                <span className="text-xs tracking-wider uppercase font-bold opacity-90">
                  Model Analytics
                </span>
              </div>
              <h3 className="text-3xl sm:text-4xl font-black tracking-tight leading-tight">
                Empirical Benchmark
              </h3>
              <p className="text-neutral-800 text-sm max-w-sm font-medium">
                Holdout confusion matrix, 90.19% recall, 0.8632 F1 score, and comparative 7-algorithm cross-validation audit.
              </p>
            </div>
          </div>

          {/* Card 3: Deep Royal Blue (Feature Importance) */}
          <div
            onClick={() => onNavigateTab('analytics')}
            className="group relative rounded-[32px] bg-gradient-to-br from-[#2563EB] to-[#1D4ED8] p-8 sm:p-10 text-white flex flex-col justify-between min-h-[300px] sm:min-h-[340px] cursor-pointer shadow-xl transition-all duration-300 hover:scale-[1.01] hover:shadow-blue-500/20"
          >
            <div className="flex items-start justify-between">
              <span className="px-3.5 py-1.5 rounded-full bg-white/15 backdrop-blur-md text-xs font-semibold tracking-wide uppercase border border-white/20">
                Gini Impurity
              </span>
              <div className="w-10 h-10 rounded-full bg-white/10 backdrop-blur-md flex items-center justify-center group-hover:bg-white group-hover:text-blue-900 transition-all">
                <ArrowUpRight className="w-5 h-5 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
              </div>
            </div>

            <div className="flex flex-col gap-3 mt-8">
              <div className="flex items-center gap-2">
                <Layers className="w-5 h-5 opacity-80" />
                <span className="text-xs tracking-wider uppercase font-semibold opacity-90">
                  Explainability
                </span>
              </div>
              <h3 className="text-3xl sm:text-4xl font-extrabold tracking-tight leading-tight">
                Decision Drivers
              </h3>
              <p className="text-white/80 text-sm max-w-sm">
                Attendance Percentage (57.80%) and Current CGPA (14.53%) account for 72.33% of the total ensemble split weights.
              </p>
            </div>
          </div>

          {/* Card 4: Tangerine / Coral Orange (History & Audit) */}
          <div
            onClick={() => onNavigateTab('history')}
            className="group relative rounded-[32px] bg-gradient-to-br from-[#EA580C] to-[#C2410C] p-8 sm:p-10 text-white flex flex-col justify-between min-h-[300px] sm:min-h-[340px] cursor-pointer shadow-xl transition-all duration-300 hover:scale-[1.01] hover:shadow-orange-500/20"
          >
            <div className="flex items-start justify-between">
              <span className="px-3.5 py-1.5 rounded-full bg-white/15 backdrop-blur-md text-xs font-semibold tracking-wide uppercase border border-white/20">
                SQLite Store
              </span>
              <div className="w-10 h-10 rounded-full bg-white/10 backdrop-blur-md flex items-center justify-center group-hover:bg-white group-hover:text-orange-950 transition-all">
                <ArrowUpRight className="w-5 h-5 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
              </div>
            </div>

            <div className="flex flex-col gap-3 mt-8">
              <div className="flex items-center gap-2">
                <Database className="w-5 h-5 opacity-80" />
                <span className="text-xs tracking-wider uppercase font-semibold opacity-90">
                  Audit Logging
                </span>
              </div>
              <h3 className="text-3xl sm:text-4xl font-extrabold tracking-tight leading-tight">
                Inference History
              </h3>
              <p className="text-white/80 text-sm max-w-sm">
                Thread-safe local persistence logging every inference run with zero PII retention, live search, and CSV/JSON export capability.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

