import React, { useState } from 'react';
import { api } from '../services/api';
import type { EngineResponse, FeedbackChoice, ResumeSource } from '../types/api';

interface Props {
  sessionId: string;
  currentResult: EngineResponse;
  onFeedbackComplete: (result: EngineResponse) => void;
  loading: boolean;
  setLoading: (loading: boolean) => void;
}

const CHOICES: { value: FeedbackChoice; label: string; desc: string; icon: JSX.Element; color: string }[] = [
  {
    value: 'accept',
    label: 'Accept',
    desc: "I'm happy — download the files",
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
    color: 'accent',
  },
  {
    value: 'change',
    label: 'Request Changes',
    desc: 'I want specific edits applied',
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
      </svg>
    ),
    color: 'amber',
  },
  {
    value: 'improve',
    label: 'Improve Further',
    desc: 'Run another AI enhancement pass',
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
      </svg>
    ),
    color: 'brand',
  },
];

const Feedback: React.FC<Props> = ({ sessionId, currentResult, onFeedbackComplete, loading, setLoading }) => {
  const [choice, setChoice] = useState<FeedbackChoice | null>(null);
  const [notes, setNotes] = useState('');
  const [source, setSource] = useState<ResumeSource>('new');
  const [error, setError] = useState('');

  const submit = async () => {
    if (!choice) { setError('Pick an option'); return; }

    if (choice === 'accept') {
      // Nothing to send — just tell the user
      alert('Your documents are ready for download on the results page.');
      return;
    }

    setError('');
    setLoading(true);
    try {
      const result = await api.feedback({
        session_id: sessionId,
        choice,
        change_notes: notes || undefined,
        resume_source: source,
      });
      onFeedbackComplete(result);
    } catch {
      setError('Feedback processing failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const colorMap: Record<string, string> = {
    accent: 'border-accent-400 bg-accent-50/50',
    amber: 'border-amber-400 bg-amber-50/50',
    brand: 'border-brand-400 bg-brand-50/50',
  };
  const dotMap: Record<string, string> = {
    accent: 'border-accent-500',
    amber: 'border-amber-500',
    brand: 'border-brand-500',
  };
  const fillMap: Record<string, string> = {
    accent: 'bg-accent-500',
    amber: 'bg-amber-500',
    brand: 'bg-brand-500',
  };

  return (
    <div className="max-w-2xl mx-auto animate-slide-up">
      <div className="bg-white rounded-2xl shadow-card p-8 sm:p-10">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-brand-50 mb-4">
            <svg className="w-8 h-8 text-brand-600" fill="none" stroke="currentColor" strokeWidth={1.8} viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-dark mb-1">What&rsquo;s next?</h2>
          <p className="text-sm text-muted">Choose how to proceed with your resume</p>
        </div>

        {/* Choice cards */}
        <div className="space-y-3 mb-6">
          {CHOICES.map((c) => {
            const selected = choice === c.value;
            return (
              <button
                key={c.value}
                onClick={() => setChoice(c.value)}
                className={`w-full p-4 rounded-xl border-2 transition-all text-left flex items-center gap-4
                  ${selected ? colorMap[c.color] : 'border-surface-200 hover:border-surface-300 bg-white'}
                `}
              >
                <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center transition-colors
                  ${selected ? dotMap[c.color] : 'border-surface-300'}
                `}>
                  {selected && <div className={`w-2.5 h-2.5 rounded-full ${fillMap[c.color]}`} />}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-semibold text-dark text-sm flex items-center gap-2">
                    {c.icon} {c.label}
                  </p>
                  <p className="text-xs text-muted mt-0.5">{c.desc}</p>
                </div>
              </button>
            );
          })}
        </div>

        {/* Conditional fields */}
        {(choice === 'change' || choice === 'improve') && (
          <div className="space-y-5 p-5 bg-surface-50 rounded-xl border border-surface-200 mb-6 animate-fade-in">
            {/* Source selector */}
            <div>
              <p className="text-sm font-semibold text-dark mb-2">Base version</p>
              <div className="flex gap-3">
                {(['new', 'old'] as ResumeSource[]).map((s) => (
                  <button
                    key={s}
                    onClick={() => setSource(s)}
                    className={`flex-1 py-2.5 px-4 rounded-lg border-2 text-sm font-medium transition-all
                      ${source === s
                        ? 'border-brand-400 bg-white text-brand-700'
                        : 'border-surface-200 bg-white text-muted hover:border-surface-300'
                      }
                    `}
                  >
                    {s === 'new' ? `Improved (v${currentResult.iteration})` : 'Original upload'}
                  </button>
                ))}
              </div>
            </div>

            {/* Notes */}
            <div>
              <label className="block text-sm font-semibold text-dark mb-2">
                Instructions <span className="text-muted font-normal">(optional)</span>
              </label>
              <textarea
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="e.g. Make the summary more impactful, add metrics to the second bullet..."
                rows={4}
                className="input-field resize-none"
              />
            </div>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm animate-fade-in">
            {error}
          </div>
        )}

        {/* Submit */}
        <button
          onClick={submit}
          disabled={loading || !choice}
          className="btn-primary w-full py-3.5 text-base"
        >
          {loading ? (
            <>
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
              Processing&hellip;
            </>
          ) : choice === 'accept' ? (
            'Confirm & Download'
          ) : (
            'Submit Feedback'
          )}
        </button>
      </div>
    </div>
  );
};

export default Feedback;
