import React, { useState } from 'react';
import { api } from '../services/api';
import type { FlowType } from '../types/api';

interface Props {
  onFlowSelect: (flow: FlowType, sessionId: string) => void;
}

const FlowSelector: React.FC<Props> = ({ onFlowSelect }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const select = async (flow: FlowType) => {
    setLoading(true);
    setError('');
    try {
      const { session_id } = await api.startSession(flow);
      onFlowSelect(flow, session_id);
    } catch {
      setError('Could not start session. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto animate-slide-up">
      {/* Hero */}
      <div className="text-center mb-14">
        <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-brand-500 to-brand-700 shadow-glow mb-6">
          <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" strokeWidth={1.8} viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight text-dark mb-4">
          Land your <span className="text-gradient">dream job</span>
        </h1>
        <p className="text-lg text-muted max-w-xl mx-auto leading-relaxed">
          Upload your resume, paste a job listing, and let AI craft a
          perfectly tailored resume &amp; cover letter in seconds.
        </p>
      </div>

      {/* Cards */}
      <div className="grid sm:grid-cols-2 gap-6">
        {/* Improve */}
        <button
          onClick={() => select('improve')}
          disabled={loading}
          className="group relative bg-white rounded-2xl p-8 shadow-card hover:shadow-card-hover
                     transition-all duration-300 hover:-translate-y-1
                     border-2 border-transparent hover:border-brand-300
                     disabled:opacity-50 disabled:cursor-not-allowed text-left"
        >
          <div className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity">
            <svg className="w-5 h-5 text-brand-400" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </div>

          <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center mb-5 shadow-sm group-hover:scale-105 transition-transform">
            <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </div>
          <h3 className="text-xl font-bold text-dark mb-2">Improve Resume</h3>
          <p className="text-sm text-muted leading-relaxed">
            Polish wording, fix formatting, and make your resume ATS-friendly with AI-powered enhancements.
          </p>
        </button>

        {/* Apply */}
        <button
          onClick={() => select('apply')}
          disabled={loading}
          className="group relative bg-white rounded-2xl p-8 shadow-card hover:shadow-card-hover
                     transition-all duration-300 hover:-translate-y-1
                     border-2 border-transparent hover:border-brand-300
                     disabled:opacity-50 disabled:cursor-not-allowed text-left"
        >
          <div className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity">
            <svg className="w-5 h-5 text-brand-400" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </div>

          <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center mb-5 shadow-sm group-hover:scale-105 transition-transform">
            <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
          <h3 className="text-xl font-bold text-dark mb-2">Apply to Jobs</h3>
          <p className="text-sm text-muted leading-relaxed">
            Paste job URLs, and AI tailors your resume &amp; generates a cover letter matched to each posting.
          </p>
        </button>
      </div>

      {/* Error */}
      {error && (
        <div className="mt-8 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm text-center animate-fade-in">
          {error}
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div className="mt-8 flex items-center justify-center gap-3 text-brand-600">
          <div className="w-5 h-5 border-2 border-brand-600 border-t-transparent rounded-full animate-spin" />
          <span className="text-sm font-medium">Starting session&hellip;</span>
        </div>
      )}
    </div>
  );
};

export default FlowSelector;
