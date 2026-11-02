import React, { useState, useEffect } from 'react';
import { History, RefreshCw, Trash2, Search, CheckCircle2, XCircle } from 'lucide-react';
import type { HistoryRecord } from '../types';
import { fetchHistoryRecords, clearAllHistory } from '../api';

export const HistoryTab: React.FC = () => {
  const [records, setRecords] = useState<HistoryRecord[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [statusFilter, setStatusFilter] = useState<'All' | 'Placed' | 'Not Placed'>('All');
  const [showClearConfirm, setShowClearConfirm] = useState<boolean>(false);

  const loadHistory = async () => {
    setLoading(true);
    try {
      const data = await fetchHistoryRecords(100);
      setRecords(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const handleClear = async () => {
    try {
      await clearAllHistory();
      setRecords([]);
      setShowClearConfirm(false);
    } catch (err) {
      console.error(err);
    }
  };

  const filteredRecords = records.filter(r => {
    const matchesStatus = statusFilter === 'All' || r.predicted_status === statusFilter;
    const matchesSearch = 
      r.branch.toLowerCase().includes(searchTerm.toLowerCase()) ||
      r.college_tier.toLowerCase().includes(searchTerm.toLowerCase()) ||
      String(r.id).includes(searchTerm);
    return matchesStatus && matchesSearch;
  });

  const totalPlaced = records.filter(r => r.predicted_status === 'Placed').length;
  const placementRate = records.length > 0 ? (totalPlaced / records.length) * 100 : 0;
  const avgCgpa = records.length > 0
    ? records.reduce((acc, curr) => acc + curr.current_cgpa, 0) / records.length
    : 0;

  return (
    <div className="space-y-8 max-w-7xl mx-auto py-4">
      {/* 1. Metric Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="rounded-[28px] bg-neutral-900/60 p-6 border border-neutral-800/80 shadow-md">
          <span className="text-xs font-semibold text-neutral-400 uppercase tracking-wider block">
            Logged Inferences
          </span>
          <span className="text-3xl font-black font-mono text-white mt-1 block">
            {records.length}
          </span>
          <span className="text-[11px] font-mono text-neutral-500 mt-1 block">data/history.sqlite</span>
        </div>

        <div className="rounded-[28px] bg-neutral-900/60 p-6 border border-neutral-800/80 shadow-md">
          <span className="text-xs font-semibold text-neutral-400 uppercase tracking-wider block">
            Predicted Placed
          </span>
          <span className="text-3xl font-black font-mono text-emerald-400 mt-1 block">
            {totalPlaced}
          </span>
          <span className="text-[11px] font-mono text-neutral-500 mt-1 block">Students Qualified</span>
        </div>

        <div className="rounded-[28px] bg-neutral-900/60 p-6 border border-neutral-800/80 shadow-md">
          <span className="text-xs font-semibold text-neutral-400 uppercase tracking-wider block">
            Placement Rate
          </span>
          <span className="text-3xl font-black font-mono text-white mt-1 block">
            {placementRate.toFixed(1)}%
          </span>
          <span className="text-[11px] font-mono text-neutral-500 mt-1 block">Historical Query Ratio</span>
        </div>

        <div className="rounded-[28px] bg-neutral-900/60 p-6 border border-neutral-800/80 shadow-md">
          <span className="text-xs font-semibold text-neutral-400 uppercase tracking-wider block">
            Average CGPA
          </span>
          <span className="text-3xl font-black font-mono text-white mt-1 block">
            {avgCgpa > 0 ? avgCgpa.toFixed(2) : '—'}
          </span>
          <span className="text-[11px] font-mono text-neutral-500 mt-1 block">Across Stored Records</span>
        </div>
      </div>

      {/* 2. Controls & Filter Bar */}
      <div className="rounded-[32px] bg-neutral-900/60 p-5 sm:p-6 border border-neutral-800/80 shadow-xl flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex flex-col sm:flex-row items-center gap-3 w-full md:w-auto">
          <div className="relative w-full sm:w-72">
            <Search className="w-4 h-4 text-neutral-500 absolute left-4 top-3.5" />
            <input
              type="text"
              placeholder="Search branch, tier, or ID..."
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
              className="w-full text-xs rounded-full border border-neutral-800 bg-neutral-950/80 pl-11 pr-4 py-3 text-white placeholder-neutral-500 focus:border-white focus:outline-hidden transition-all"
            />
          </div>

          <div className="flex items-center gap-1.5 w-full sm:w-auto">
            {(['All', 'Placed', 'Not Placed'] as const).map((status) => (
              <button
                key={status}
                type="button"
                onClick={() => setStatusFilter(status)}
                className={`px-4 py-2.5 rounded-full text-xs font-semibold transition-all cursor-pointer ${
                  statusFilter === status
                    ? 'bg-white text-black shadow-md'
                    : 'bg-neutral-950/80 text-neutral-400 border border-neutral-800 hover:text-white hover:bg-neutral-800'
                }`}
              >
                {status}
              </button>
            ))}
          </div>
        </div>

        <div className="flex items-center gap-2.5 self-end md:self-auto">
          <button
            type="button"
            onClick={loadHistory}
            className="inline-flex items-center gap-2 text-xs font-semibold text-neutral-300 hover:text-white px-4 py-2.5 rounded-full bg-neutral-950/80 border border-neutral-800 hover:bg-neutral-800 transition-all cursor-pointer"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>

          {records.length > 0 && (
            <button
              type="button"
              onClick={() => setShowClearConfirm(true)}
              className="inline-flex items-center gap-2 text-xs font-semibold text-rose-400 hover:text-rose-300 px-4 py-2.5 rounded-full bg-rose-950/40 border border-rose-500/30 hover:bg-rose-950/70 transition-all cursor-pointer"
            >
              <Trash2 className="w-3.5 h-3.5" />
              <span>Clear History</span>
            </button>
          )}
        </div>
      </div>

      {/* 3. History Table */}
      <div className="rounded-[32px] bg-neutral-900/60 border border-neutral-800/80 shadow-2xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="bg-neutral-950/80 border-b border-neutral-800 text-neutral-400 font-semibold tracking-wider uppercase text-[11px]">
                <th className="py-4 px-5 font-mono"># ID</th>
                <th className="py-4 px-5">Timestamp (UTC)</th>
                <th className="py-4 px-5">Branch &amp; Tier</th>
                <th className="py-4 px-5 text-center">CGPA</th>
                <th className="py-4 px-5 text-center">Attendance</th>
                <th className="py-4 px-5 text-center">Backlogs</th>
                <th className="py-4 px-5 text-center">Projects</th>
                <th className="py-4 px-5 text-center">Internships</th>
                <th className="py-4 px-5 text-center">Outcome</th>
                <th className="py-4 px-5 text-right">Placed %</th>
                <th className="py-4 px-5 text-right font-mono">Confidence</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-neutral-800/60 text-neutral-300">
              {filteredRecords.length > 0 ? (
                filteredRecords.map(r => (
                  <tr key={r.id} className="hover:bg-neutral-800/40 transition-colors">
                    <td className="py-4 px-5 font-mono text-neutral-400 font-bold">#{r.id}</td>
                    <td className="py-4 px-5 text-neutral-500 font-mono text-[11px] whitespace-nowrap">
                      {new Date(r.created_at).toLocaleString()}
                    </td>
                    <td className="py-4 px-5 font-semibold text-white whitespace-nowrap">
                      <div>{r.branch}</div>
                      <div className="text-[10px] text-neutral-500 font-normal">{r.college_tier}</div>
                    </td>
                    <td className="py-4 px-5 text-center font-mono font-bold text-white">
                      {r.current_cgpa.toFixed(2)}
                    </td>
                    <td className="py-4 px-5 text-center font-mono">
                      <span className={`px-2.5 py-1 rounded-full text-[11px] font-semibold ${
                        r.attendance_percentage < 75 
                          ? 'bg-rose-950/80 text-rose-400 border border-rose-500/40' 
                          : 'text-neutral-300'
                      }`}>
                        {r.attendance_percentage.toFixed(1)}%
                      </span>
                    </td>
                    <td className="py-4 px-5 text-center font-mono">
                      <span className={r.backlogs > 0 ? 'text-amber-400 font-bold' : 'text-neutral-500'}>
                        {r.backlogs}
                      </span>
                    </td>
                    <td className="py-4 px-5 text-center font-mono text-neutral-400">{r.projects}</td>
                    <td className="py-4 px-5 text-center font-mono text-neutral-400">{r.internships}</td>
                    <td className="py-4 px-5 text-center">
                      <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-bold ${
                        r.predicted_status === 'Placed'
                          ? 'bg-emerald-950/60 text-emerald-400 border border-emerald-500/30'
                          : 'bg-rose-950/60 text-rose-400 border border-rose-500/30'
                      }`}>
                        {r.predicted_status === 'Placed' ? (
                          <CheckCircle2 className="w-3.5 h-3.5" />
                        ) : (
                          <XCircle className="w-3.5 h-3.5" />
                        )}
                        <span>{r.predicted_status}</span>
                      </span>
                    </td>
                    <td className="py-4 px-5 text-right font-mono font-bold text-white">
                      {r.probability_placed.toFixed(2)}%
                    </td>
                    <td className="py-4 px-5 text-right font-mono text-neutral-300 font-medium">
                      {r.confidence_score.toFixed(2)}%
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={11} className="py-16 text-center text-neutral-500">
                    <History className="w-10 h-10 text-neutral-600 mx-auto mb-3" />
                    <p className="font-bold text-white text-base">No prediction records found</p>
                    <p className="text-xs text-neutral-500 mt-1">
                      {records.length === 0
                        ? 'Generate your first prediction from the Predictor tab to view query history.'
                        : 'No records match the current search or status filter.'}
                    </p>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Clear History Confirmation Modal */}
      {showClearConfirm && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-md flex items-center justify-center p-4 z-50">
          <div className="rounded-[32px] bg-neutral-900 border border-neutral-800 max-w-md w-full p-7 shadow-2xl space-y-4">
            <h4 className="text-xl font-extrabold text-white tracking-tight">Clear Prediction History?</h4>
            <p className="text-xs text-neutral-400 leading-relaxed">
              This will permanently delete all logged predictions from the local SQLite store (`data/history.sqlite`). This action is irreversible.
            </p>
            <div className="pt-4 flex items-center justify-end gap-3">
              <button
                type="button"
                onClick={() => setShowClearConfirm(false)}
                className="px-5 py-2.5 text-xs font-semibold text-neutral-300 hover:text-white hover:bg-neutral-800 rounded-full transition-colors cursor-pointer"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleClear}
                className="px-5 py-2.5 text-xs font-bold text-white bg-rose-600 hover:bg-rose-500 rounded-full shadow-lg transition-all cursor-pointer"
              >
                Yes, Delete All
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
