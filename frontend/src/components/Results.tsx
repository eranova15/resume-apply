import React, { useState } from 'react';
import { api } from '../services/api';
import type { EngineResponse, FlowType } from '../types/api';

interface Props {
  result: EngineResponse;
  flow: FlowType | null;
  onShowFeedback: () => void;
  onStartOver: () => void;
}

type Tab = 'suggestions' | 'resume' | 'cover';

const Results: React.FC<Props> = ({ result, flow, onShowFeedback, onStartOver }) => {
  const hasSuggestions = result.suggestions && result.suggestions.length > 0;
  const hasCover = !!result.cover_letter_text;
  const defaultTab: Tab = hasSuggestions ? 'suggestions' : 'resume';
  const [tab, setTab] = useState<Tab>(defaultTab);

  const tabs: { key: Tab; label: string; show: boolean; count?: number }[] = [
    { key: 'suggestions', label: 'Suggestions', show: hasSuggestions, count: result.suggestions?.length },
    { key: 'resume', label: 'Resume', show: true },
    { key: 'cover', label: 'Cover Letter', show: hasCover },
  ];

  return (
    <div className="max-w-5xl mx-auto animate-slide-up">
      {/* Success banner */}
      <div className="bg-gradient-to-r from-brand-600 to-brand-500 rounded-2xl p-6 sm:p-8 text-white mb-6 shadow-glow">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div className="flex items-center gap-4">
            <div className="flex-shrink-0 w-12 h-12 rounded-xl bg-white/20 backdrop-blur flex items-center justify-center">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h2 className="text-xl font-bold">Results Ready</h2>
              <p className="text-sm text-white/80">
                Iteration {result.iteration} &middot; Review your enhanced documents below
              </p>
            </div>
          </div>

          {/* Download buttons */}
          <div className="flex gap-2">
            {result.resume_pdf && (
              <a
                href={api.downloadUrl(result.resume_pdf)}
                download
                className="inline-flex items-center gap-2 px-4 py-2 bg-white/20 hover:bg-white/30 backdrop-blur rounded-lg text-sm font-semibold transition-colors"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Resume PDF
              </a>
            )}
            {result.cover_letter_pdf && (
              <a
                href={api.downloadUrl(result.cover_letter_pdf)}
                download
                className="inline-flex items-center gap-2 px-4 py-2 bg-white/20 hover:bg-white/30 backdrop-blur rounded-lg text-sm font-semibold transition-colors"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                Cover Letter PDF
              </a>
            )}
          </div>
        </div>
      </div>

      {/* Scraped jobs summary */}
      {result.scrape_results && result.scrape_results.length > 0 && (
        <div className="bg-white rounded-2xl shadow-card p-5 mb-6">
          <h3 className="text-sm font-semibold text-dark mb-3 flex items-center gap-2">
            <svg className="w-4 h-4 text-emerald-500" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            Scraped Job Postings
          </h3>
          <div className="grid gap-2">
            {result.scrape_results.map((s, i) => (
              <div
                key={i}
                className={`flex items-center gap-3 p-3 rounded-xl text-sm ${
                  s.error ? 'bg-red-50 text-red-700' : 'bg-surface-50 text-dark'
                }`}
              >
                <div className={`flex-shrink-0 w-7 h-7 rounded-lg flex items-center justify-center text-xs font-bold ${
                  s.error ? 'bg-red-100 text-red-500' : 'bg-emerald-100 text-emerald-600'
                }`}>
                  {s.error ? '!' : i + 1}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-medium truncate">
                    {s.error ? 'Failed to scrape' : `${s.title} @ ${s.company}`}
                  </p>
                  <p className="text-xs text-muted truncate">{s.url}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tabbed card */}
      <div className="bg-white rounded-2xl shadow-card overflow-hidden">
        {/* Tab bar */}
        <div className="flex border-b border-surface-200">
          {tabs.filter((t) => t.show).map((t) => (
            <button
              key={t.key}
              onClick={() => setTab(t.key)}
              className={`flex-1 py-3.5 px-4 text-sm font-semibold transition-colors relative ${
                tab === t.key ? 'text-brand-600 bg-brand-50/40' : 'text-muted hover:text-dark hover:bg-surface-50'
              }`}
            >
              <span className="flex items-center justify-center gap-1.5">
                {t.label}
                {t.count !== undefined && (
                  <span className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-brand-100 text-brand-700 text-[10px] font-bold">
                    {t.count}
                  </span>
                )}
              </span>
              {tab === t.key && (
                <span className="absolute bottom-0 inset-x-0 h-0.5 bg-brand-500 rounded-full" />
              )}
            </button>
          ))}
        </div>

        {/* Tab content */}
        <div className="p-6">
          {/* ── Suggestions ── */}
          {tab === 'suggestions' && hasSuggestions && (
            <div className="space-y-4 animate-fade-in">
              {result.suggestions.map((s, i) => (
                <div key={i} className="group rounded-xl border border-surface-200 hover:border-brand-200 p-5 transition-colors">
                  <div className="flex items-start gap-4">
                    <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-brand-50 flex items-center justify-center">
                      <span className="text-xs font-bold text-brand-600">{i + 1}</span>
                    </div>
                    <div className="flex-1 min-w-0 space-y-3">
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className="step-badge bg-surface-100 text-dark">{s.section}</span>
                      </div>

                      {/* Original */}
                      <div className="p-3 bg-red-50/60 rounded-lg border border-red-100">
                        <p className="text-[11px] font-bold uppercase tracking-wider text-red-400 mb-1">Original</p>
                        <p className="text-sm text-red-800 line-through leading-relaxed">{s.original}</p>
                      </div>

                      {/* Suggested */}
                      <div className="p-3 bg-accent-50/60 rounded-lg border border-accent-200">
                        <p className="text-[11px] font-bold uppercase tracking-wider text-accent-500 mb-1">Suggested</p>
                        <p className="text-sm text-accent-900 font-medium leading-relaxed">{s.suggested}</p>
                      </div>

                      {/* Reason */}
                      <p className="text-xs text-muted leading-relaxed pl-1">
                        <span className="font-semibold text-dark/70">Why:</span> {s.reason}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* ── Resume ── */}
          {tab === 'resume' && (
            <div className="animate-fade-in">
              <div className="flex items-center justify-between mb-4">
                <p className="text-sm text-muted">Your enhanced resume</p>
                {result.resume_pdf && (
                  <a href={api.downloadUrl(result.resume_pdf)} download className="btn-secondary text-sm py-2 px-4">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                    Download PDF
                  </a>
                )}
              </div>
              <div className="bg-surface-50 rounded-xl border border-surface-200 p-6 max-h-[600px] overflow-y-auto">
                <pre className="whitespace-pre-wrap font-sans text-sm text-dark/90 leading-relaxed">
                  {result.improved_resume_text}
                </pre>
              </div>
            </div>
          )}

          {/* ── Cover Letter ── */}
          {tab === 'cover' && hasCover && (
            <div className="animate-fade-in">
              <div className="flex items-center justify-between mb-4">
                <p className="text-sm text-muted">Your customized cover letter</p>
                {result.cover_letter_pdf && (
                  <a href={api.downloadUrl(result.cover_letter_pdf)} download className="btn-secondary text-sm py-2 px-4">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                    Download PDF
                  </a>
                )}
              </div>
              <div className="bg-surface-50 rounded-xl border border-surface-200 p-6 max-h-[600px] overflow-y-auto">
                <pre className="whitespace-pre-wrap font-sans text-sm text-dark/90 leading-relaxed">
                  {result.cover_letter_text}
                </pre>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Action bar */}
      <div className="flex flex-col sm:flex-row justify-center gap-3 mt-8">
        <button onClick={onShowFeedback} className="btn-primary py-3 px-8">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Refine Further
        </button>
        <button onClick={onStartOver} className="btn-secondary py-3 px-8">
          New Session
        </button>
      </div>
    </div>
  );
};

export default Results;
