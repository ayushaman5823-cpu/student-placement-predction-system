import React from 'react';

export const MarqueeBanner: React.FC = () => {
  const items = [
    'GRADIENT BOOSTING ENSEMBLE',
    '83.10% HOLDOUT ACCURACY',
    'ZERO DEMOGRAPHIC BIAS',
    '9 ACADEMIC INPUTS',
    'FASTAPI REST BACKEND',
    'SQLITE AUDIT PERSISTENCE',
    '1,000 UNTOUCHED TEST EVALUATIONS',
    'SRMIST CSE CAPSTONE',
    '0.8632 TEST F1-SCORE',
    '0.9036 ROC-AUC',
  ];

  return (
    <div className="w-full bg-neutral-950 border-y border-white/10 py-5 overflow-hidden my-8 select-none">
      <div className="animate-marquee flex items-center gap-8 whitespace-nowrap">
        {/* First set */}
        {items.map((item, idx) => (
          <div key={`a-${idx}`} className="flex items-center gap-8">
            <span className="text-xl sm:text-2xl font-black tracking-tight text-white/90 uppercase">
              {item}
            </span>
            <span className="w-2.5 h-2.5 rounded-full bg-white/30" />
          </div>
        ))}
        {/* Duplicate set for seamless looping */}
        {items.map((item, idx) => (
          <div key={`b-${idx}`} className="flex items-center gap-8">
            <span className="text-xl sm:text-2xl font-black tracking-tight text-white/90 uppercase">
              {item}
            </span>
            <span className="w-2.5 h-2.5 rounded-full bg-white/30" />
          </div>
        ))}
      </div>
    </div>
  );
};

