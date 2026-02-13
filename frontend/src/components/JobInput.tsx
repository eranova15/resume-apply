import React, { useState } from 'react';
import { api } from '../services/api';
import type { FlowType, EngineResponse } from '../types/api';

interface Props {
  sessionId: string;
  flow: FlowType;
  onProcessComplete: (result: EngineResponse) => void;
  loading: boolean;
  setLoading: (loading: boolean) => void;
}

const JobInput: React.FC<Props> = ({ sessionId, flow, onProcessComplete, loading, setLoading }) => {
  const [jobUrls, setJobUrls] = useState<string[]>(['']);
  const [changeNotes, setChangeNotes] = useState('');
  const [error, setError] = useState('');

  const addUrl = () => setJobUrls([...jobUrls, '']);
  const removeUrl = (i: number) => setJobUrls(jobUrls.filter((_, idx) => idx !== i));
  const updateUrl = (i: number, v: string) => {
    const copy = [...jobUrls];
    copy[i] = v;
    setJobUrls(copy);
  };

  const submit = async () => {
    setError('');
    setLoading(true);
    try {
      if (flow === 'apply') {
        const valid = jobUrls.filter((u) => u.trim());
        if (!valid.length) {
          setError('Add at least one job URL');
          setLoading(false);
          return;
        }
        const result = await api.apply({ session_id: sessionId, job_urls: valid });
        onProcessComplete(result);
      } else {
        const result = await api.improve({ session_id: sessionId, change_notes: changeNotes || undefined });
        onProcessComplete(result);
      }
    } catch {
      setError('Processing failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto animate-slide-up">
      <div className="bg-white rounded-2xl shadow-card p-8 sm:p-10">
        {/* Header */}
        <div className="text-center mb-8">
          <div className={`inline-flex items-center justify-center w-16 h-16 rounded-2xl mb-4 ${
            flow === 'apply' ? 'bg-emerald-50' : 'bg-violet-50'
          }`}>
            {flow === 'apply' ? (
              <svg className="w-8 h-8 text-emerald-600" fill="none" stroke="currentColor" strokeWidth={1.8} viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            ) : (
              <svg className="w-8 h-8 text-violet-600" fill="none" stroke="currentColor" strokeWidth={1.8} viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            )}
          </div>
          <h2 className="text-2xl font-bold text-dark mb-1">
            {flow === 'apply' ? 'Paste Job Listings' : 'Improvement Notes'}
          </h2>
          <p className="text-sm text-muted">
            {flow === 'apply'
              ? 'Add URLs to the positions you want to apply for'
              : 'Optionally describe what you want improved'}
          </p>
        </div>

        {/* Apply: URL list */}
        {flow === 'apply' ? (
          <div className="space-y-3">
            {jobUrls.map((url, i) => (
              <div key={i} className="flex gap-2 items-center">
                <div className="flex-shrink-0 w-7 h-7 rounded-full bg-surface-100 flex items-center justify-center text-xs font-bold text-muted">
                  {i + 1}
                </div>
                <input
                  type="url"
                  value={url}
                  onChange={(e) => updateUrl(i, e.target.value)}
                  placeholder="https://example.com/jobs/software-engineer"
                  className="input-field flex-1"
                />
                {jobUrls.length > 1 && (
                  <button
                    onClick={() => removeUrl(i)}
                    className="flex-shrink-0 w-9 h-9 rounded-lg text-muted hover:text-red-500 hover:bg-red-50 flex items-center justify-center transition-colors"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                )}
              </div>
            ))}

            <button
              onClick={addUrl}
              className="w-full py-3 border-2 border-dashed border-surface-200 rounded-xl text-muted text-sm font-medium
                         hover:border-brand-300 hover:text-brand-600 transition-colors flex items-center justify-center gap-2"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
              </svg>
              Add another URL
            </button>
          </div>
        ) : (
          /* Improve: textarea */
          <div>
            <label className="block text-sm font-semibold text-dark mb-2">
              What should we focus on? <span className="text-muted font-normal">(optional)</span>
            </label>
            <textarea
              value={changeNotes}
              onChange={(e) => setChangeNotes(e.target.value)}
              placeholder="e.g. Strengthen action verbs, add quantifiable achievements, make the summary more compelling..."
              rows={5}
              className="input-field resize-none"
            />
            <p className="mt-2 text-xs text-muted">Leave blank for a general AI-driven improvement pass</p>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm animate-fade-in">
            {error}
          </div>
        )}

        {/* Submit */}
        <button
          onClick={submit}
          disabled={loading}
          className="btn-primary w-full mt-8 py-3.5 text-base"
        >
          {loading ? (
            <>
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
              <span>AI is working&hellip;</span>
            </>
          ) : (
            <>
              <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              {flow === 'apply' ? 'Generate Resume & Cover Letter' : 'Improve My Resume'}
            </>
          )}
        </button>

        {/* Processing info */}
        {loading && (
          <div className="mt-5 p-4 bg-brand-50 border border-brand-200 rounded-xl animate-fade-in">
            <div className="flex gap-3 items-start">
              <div className="w-8 h-8 flex-shrink-0 rounded-lg bg-brand-100 flex items-center justify-center">
                <svg className="w-4 h-4 text-brand-600" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <p className="text-sm font-semibold text-brand-900">Processing your request</p>
                <p className="text-xs text-brand-700 mt-0.5">
                  {flow === 'apply'
                    ? 'Scraping job listings, analyzing requirements, tailoring resume, drafting cover letter...'
                    : 'Analyzing resume, enhancing language, improving formatting...'}
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default JobInput;
