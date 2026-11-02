import { useState, useEffect, useRef } from 'react';
import { Navbar } from './components/Navbar';
import { HeroSection } from './components/HeroSection';
import { MarqueeBanner } from './components/MarqueeBanner';
import { PredictorTab } from './components/PredictorTab';
import { HistoryTab } from './components/HistoryTab';
import { ModelAnalyticsTab } from './components/ModelAnalyticsTab';
import { AboutTab } from './components/AboutTab';
import { Footer } from './components/Footer';
import { checkHealth } from './api';

export function App() {
  const [activeTab, setActiveTab] = useState<'predictor' | 'history' | 'analytics' | 'about'>('predictor');
  const [apiConnected, setApiConnected] = useState<boolean>(false);
  const [modelSha, setModelSha] = useState<string | undefined>(undefined);
  const predictorRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const runHealthCheck = async () => {
      const res = await checkHealth();
      if (res.status === 'healthy') {
        setApiConnected(true);
        setModelSha(res.model_artifact_sha256);
      } else {
        setApiConnected(false);
      }
    };

    runHealthCheck();
    const interval = setInterval(runHealthCheck, 5000);
    return () => clearInterval(interval);
  }, []);

  const scrollToPredictor = () => {
    if (activeTab !== 'predictor') {
      setActiveTab('predictor');
    }
    setTimeout(() => {
      if (predictorRef.current) {
        predictorRef.current.scrollIntoView({ behavior: 'smooth' });
      }
    }, 50);
  };

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [activeTab]);

  return (
    <div className="min-h-screen flex flex-col bg-[#09090b] text-neutral-100 selection:bg-white selection:text-black">
      {/* Floating Centered Pill Navbar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        apiConnected={apiConnected}
        modelSha={modelSha}
      />

      <main className="flex-1 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
        {/* On Predictor tab, show the editorial Hero + 4 Showcase Cards + Marquee */}
        {activeTab === 'predictor' && (
          <>
            <HeroSection
              onNavigateTab={setActiveTab}
              onScrollToPredictor={scrollToPredictor}
            />

            <MarqueeBanner />

            <div ref={predictorRef} className="pt-8">
              <div className="flex items-center justify-between pb-6 mb-2">
                <div>
                  <span className="text-xs font-semibold uppercase tracking-wider text-neutral-400">
                    Live Inference Suite
                  </span>
                  <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-white mt-1">
                    Student Placement Prediction
                  </h2>
                </div>
              </div>

              <PredictorTab />
            </div>
          </>
        )}

        {/* Dedicated Views for Analytics, History, About with clean editorial spacing */}
        {activeTab === 'analytics' && (
          <div className="pt-24 sm:pt-32">
            <div className="pb-8">
              <span className="text-xs font-semibold uppercase tracking-wider text-neutral-400">
                Empirical Evaluation
              </span>
              <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight text-white mt-1">
                Model Analytics &amp; Holdout Benchmark
              </h1>
            </div>
            <ModelAnalyticsTab />
          </div>
        )}

        {activeTab === 'history' && (
          <div className="pt-24 sm:pt-32">
            <div className="pb-8">
              <span className="text-xs font-semibold uppercase tracking-wider text-neutral-400">
                Audit Trail
              </span>
              <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight text-white mt-1">
                SQLite Prediction History
              </h1>
            </div>
            <HistoryTab />
          </div>
        )}

        {activeTab === 'about' && (
          <div className="pt-24 sm:pt-32">
            <div className="pb-8">
              <span className="text-xs font-semibold uppercase tracking-wider text-neutral-400">
                Documentation &amp; Contracts
              </span>
              <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight text-white mt-1">
                About the System &amp; Specifications
              </h1>
            </div>
            <AboutTab />
          </div>
        )}
      </main>

      {/* Editorial Footer with "Ready to predict?" CTA */}
      <Footer
        onScrollToPredictor={scrollToPredictor}
        onNavigateTab={setActiveTab}
      />
    </div>
  );
}

export default App;
