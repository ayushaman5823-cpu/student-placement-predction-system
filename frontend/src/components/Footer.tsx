import React from 'react';
import { ArrowUpRight } from 'lucide-react';

interface FooterProps {
  onScrollToPredictor?: () => void;
  onNavigateTab?: (tab: 'predictor' | 'history' | 'analytics' | 'about') => void;
}

export const Footer: React.FC<FooterProps> = ({
  onScrollToPredictor,
  onNavigateTab,
}) => {
  return (
    <footer className="w-full bg-[#09090b] text-neutral-300 pt-16 sm:pt-24 pb-12 border-t border-neutral-900 mt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col gap-16 sm:gap-20">
        {/* Large "Ready to Predict?" Call to Action (Inspired by Let's talk! from Figma) */}
        <div className="flex flex-col items-center text-center gap-6 sm:gap-8">
          <h2 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-white">
            Ready to predict?
          </h2>

          <div className="flex flex-wrap items-center justify-center gap-4">
            <button
              onClick={() => {
                if (onNavigateTab) onNavigateTab('predictor');
                if (onScrollToPredictor) onScrollToPredictor();
              }}
              className="inline-flex items-center gap-3 px-8 sm:px-10 py-4 rounded-full bg-white text-black text-sm sm:text-base font-bold tracking-tight hover:bg-neutral-200 transition-all duration-200 shadow-xl shadow-white/5 hover:scale-[1.02] active:scale-[0.98] group"
            >
              <span>Launch Prediction Engine</span>
              <ArrowUpRight className="w-4 h-4 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
            </button>

            <a
              href="http://127.0.0.1:8000/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-6 sm:px-8 py-4 rounded-full bg-neutral-900 border border-white/10 text-white text-sm sm:text-base font-semibold hover:bg-neutral-800 transition-all"
            >
              <span>Explore Swagger API</span>
              <ArrowUpRight className="w-4 h-4 text-neutral-400" />
            </a>
          </div>
        </div>

        {/* Bottom Minimalist Bar (Inspired by Figma footer) */}
        <div className="pt-8 border-t border-neutral-900 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-neutral-500 font-medium">
          <div>
            <span>2026 © — SRM Institute of Science and Technology · Department of CSE</span>
          </div>

          <div className="flex items-center gap-6">
            <button
              onClick={() => onNavigateTab && onNavigateTab('predictor')}
              className="hover:text-white transition-colors"
            >
              Predictor
            </button>
            <button
              onClick={() => onNavigateTab && onNavigateTab('analytics')}
              className="hover:text-white transition-colors"
            >
              Model Analytics
            </button>
            <button
              onClick={() => onNavigateTab && onNavigateTab('history')}
              className="hover:text-white transition-colors"
            >
              History
            </button>
            <button
              onClick={() => onNavigateTab && onNavigateTab('about')}
              className="hover:text-white transition-colors"
            >
              About & Schema
            </button>
            <a
              href="http://127.0.0.1:8000/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-white transition-colors"
            >
              FastAPI Docs ↗
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};
