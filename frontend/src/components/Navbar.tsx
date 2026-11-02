import React, { useState } from 'react';
import { Menu, X, Sparkles, History, BarChart3, Info } from 'lucide-react';

interface NavbarProps {
  activeTab: 'predictor' | 'history' | 'analytics' | 'about';
  setActiveTab: (tab: 'predictor' | 'history' | 'analytics' | 'about') => void;
  apiConnected: boolean;
  modelSha?: string;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  setActiveTab,
  apiConnected,
  modelSha,
}) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navItems: { id: 'predictor' | 'history' | 'analytics' | 'about'; label: string; icon: React.ReactNode }[] = [
    { id: 'predictor', label: 'Predictor', icon: <Sparkles className="w-3.5 h-3.5" /> },
    { id: 'analytics', label: 'Analytics', icon: <BarChart3 className="w-3.5 h-3.5" /> },
    { id: 'history', label: 'History', icon: <History className="w-3.5 h-3.5" /> },
    { id: 'about', label: 'About', icon: <Info className="w-3.5 h-3.5" /> },
  ];

  return (
    <>
      {/* Floating Centered Pill Navbar */}
      <header className="fixed top-4 sm:top-6 left-0 right-0 z-50 flex justify-center px-4 pointer-events-none">
        <div className="pointer-events-auto flex items-center justify-between gap-2 sm:gap-4 bg-neutral-900/90 backdrop-blur-xl border border-white/10 p-1.5 sm:p-2 rounded-full shadow-2xl max-w-full">
          {/* Brand Mark (Inspired by Joey®) */}
          <div
            onClick={() => setActiveTab('predictor')}
            className="flex items-center gap-1.5 pl-3 sm:pl-4 pr-1 sm:pr-2 cursor-pointer select-none group"
          >
            <span className="font-extrabold text-base sm:text-lg tracking-tight text-white group-hover:text-neutral-200 transition-colors">
              Placement<sup className="text-[10px] text-neutral-400 font-normal">®</sup>
            </span>
          </div>

          {/* Desktop Navigation Capsule */}
          <nav className="hidden md:flex items-center gap-1">
            {navItems.map((item) => {
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`flex items-center gap-1.5 px-4 sm:px-5 py-2 rounded-full text-xs sm:text-sm font-semibold tracking-tight transition-all duration-200 ${
                    isActive
                      ? 'bg-white text-black shadow-md shadow-white/10 scale-[1.02]'
                      : 'text-neutral-400 hover:text-white hover:bg-neutral-800/60'
                  }`}
                >
                  {isActive && <span className="w-1.5 h-1.5 rounded-full bg-black animate-pulse" />}
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>

          {/* Right Status Pill */}
          <div className="flex items-center gap-2 pr-1">
            <div
              className={`flex items-center gap-1.5 px-2.5 sm:px-3 py-1.5 rounded-full text-[11px] font-mono border transition-all ${
                apiConnected
                  ? 'bg-emerald-950/60 text-emerald-400 border-emerald-500/30'
                  : 'bg-rose-950/60 text-rose-400 border-rose-500/30'
              }`}
              title={modelSha ? `Frozen SHA-256: ${modelSha}` : 'API Status'}
            >
              <span className="relative flex h-2 w-2">
                {apiConnected && (
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
                )}
                <span
                  className={`relative inline-flex rounded-full h-2 w-2 ${
                    apiConnected ? 'bg-emerald-500' : 'bg-rose-500'
                  }`}
                />
              </span>
              <span className="hidden sm:inline font-semibold">
                {apiConnected ? (modelSha ? `SHA: ${modelSha.slice(0, 8)}` : 'Live') : 'Offline'}
              </span>
              <span className="sm:hidden font-semibold">
                {apiConnected ? 'Live' : 'Offline'}
              </span>
            </div>

            {/* Mobile Hamburger Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden w-8 h-8 rounded-full bg-neutral-800 text-white flex items-center justify-center border border-white/10 hover:bg-neutral-700 transition-colors"
              aria-label="Toggle Navigation Menu"
            >
              {mobileMenuOpen ? <X className="w-4 h-4" /> : <Menu className="w-4 h-4" />}
            </button>
          </div>
        </div>
      </header>

      {/* Mobile Drawer Overlay */}
      {mobileMenuOpen && (
        <div className="fixed inset-0 z-40 bg-black/80 backdrop-blur-md md:hidden flex flex-col justify-center items-center px-6 animate-fadeIn">
          <div className="w-full max-w-xs bg-neutral-900 border border-white/10 rounded-3xl p-6 shadow-2xl flex flex-col gap-3">
            <div className="flex items-center justify-between pb-3 border-b border-neutral-800">
              <span className="font-extrabold text-xl text-white">
                Placement<sup className="text-xs text-neutral-400">®</sup>
              </span>
              <button
                onClick={() => setMobileMenuOpen(false)}
                className="w-8 h-8 rounded-full bg-neutral-800 text-neutral-300 flex items-center justify-center hover:bg-neutral-700"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <p className="text-xs text-neutral-400 pb-2">
              SRM Institute of Science and Technology · CSE Capstone
            </p>

            <div className="flex flex-col gap-2">
              {navItems.map((item) => {
                const isActive = activeTab === item.id;
                return (
                  <button
                    key={item.id}
                    onClick={() => {
                      setActiveTab(item.id);
                      setMobileMenuOpen(false);
                    }}
                    className={`flex items-center justify-between px-5 py-3 rounded-2xl text-sm font-semibold transition-all ${
                      isActive
                        ? 'bg-white text-black shadow-lg'
                        : 'bg-neutral-800/80 text-neutral-200 hover:bg-neutral-800'
                    }`}
                  >
                    <span className="flex items-center gap-2">
                      {item.icon}
                      {item.label}
                    </span>
                    {isActive && <span className="w-2 h-2 rounded-full bg-black" />}
                  </button>
                );
              })}
            </div>

            <div className="mt-4 pt-3 border-t border-neutral-800 flex items-center justify-between text-[11px] text-neutral-500 font-mono">
              <span>Status: {apiConnected ? 'Connected' : 'Disconnected'}</span>
              <span>v2.0 Gradient Boost</span>
            </div>
          </div>
        </div>
      )}
    </>
  );
};
