import React, { useState, useEffect } from 'react';
import FlowSelector from './components/FlowSelector';
import ResumeUpload from './components/ResumeUpload';
import JobInput from './components/JobInput';
import Results from './components/Results';
import Feedback from './components/Feedback';
import { api } from './services/api';
import type { FlowType, EngineResponse } from './types/api';

type AppStep = 'flow' | 'upload' | 'input' | 'results' | 'feedback';

const STEPS: { key: AppStep; label: string }[] = [
  { key: 'flow', label: 'Choose Flow' },
  { key: 'upload', label: 'Upload Resume' },
  { key: 'input', label: 'Configure' },
  { key: 'results', label: 'Results' },
];

function App() {
  const [step, setStep] = useState<AppStep>('flow');
  const [flow, setFlow] = useState<FlowType | null>(null);
  const [sessionId, setSessionId] = useState('');
  const [result, setResult] = useState<EngineResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [demoMode, setDemoMode] = useState(false);

  useEffect(() => {
    api.health().then((h) => setDemoMode(h.demo_mode)).catch(() => {});
  }, []);

  const currentStepIndex = STEPS.findIndex(
    (s) => s.key === step || (step === 'feedback' && s.key === 'results'),
  );

  const handleFlowSelect = (selectedFlow: FlowType, sid: string) => {
    setFlow(selectedFlow);
    setSessionId(sid);
    setStep('upload');
  };

  const handleResumeUploaded = () => setStep('input');

  const handleProcessComplete = (r: EngineResponse) => {
    setResult(r);
    setStep('results');
  };

  const handleShowFeedback = () => setStep('feedback');

  const handleFeedbackComplete = (r: EngineResponse) => {
    setResult(r);
    setStep('results');
  };

  const handleStartOver = () => {
    setStep('flow');
    setFlow(null);
    setSessionId('');
    setResult(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-50">
      {/* ── Top bar ── */}
      <header className="sticky top-0 z-50 glass-card border-b border-surface-200/60">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="relative w-9 h-9 bg-gradient-to-br from-brand-500 to-brand-700 rounded-lg flex items-center justify-center shadow-sm">
              <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" strokeWidth={2.2} viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <span className="text-lg font-bold tracking-tight text-dark">ResumeApply</span>
            {demoMode && (
              <span className="step-badge bg-amber-100 text-amber-700 ml-2">Demo</span>
            )}
          </div>

          <div className="flex items-center gap-4">
            {step !== 'flow' && (
              <nav className="hidden sm:flex items-center gap-1" aria-label="Progress">
                {STEPS.map((s, i) => (
                  <React.Fragment key={s.key}>
                    <div
                      className={`w-2.5 h-2.5 rounded-full transition-colors duration-300 ${
                        i <= currentStepIndex ? 'bg-brand-500' : 'bg-surface-200'
                      }`}
                      title={s.label}
                    />
                    {i < STEPS.length - 1 && (
                      <div
                        className={`w-6 h-0.5 transition-colors duration-300 ${
                          i < currentStepIndex ? 'bg-brand-400' : 'bg-surface-200'
                        }`}
                      />
                    )}
                  </React.Fragment>
                ))}
              </nav>
            )}

            {step !== 'flow' && (
              <button onClick={handleStartOver} className="btn-ghost text-sm">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                </svg>
                Start Over
              </button>
            )}
          </div>
        </div>
      </header>

      {/* ── Main ── */}
      <main className="max-w-6xl mx-auto px-6 py-10 animate-fade-in">
        {step === 'flow' && <FlowSelector onFlowSelect={handleFlowSelect} />}
        {step === 'upload' && sessionId && (
          <ResumeUpload sessionId={sessionId} onUploadComplete={handleResumeUploaded} />
        )}
        {step === 'input' && sessionId && flow && (
          <JobInput
            sessionId={sessionId}
            flow={flow}
            onProcessComplete={handleProcessComplete}
            loading={loading}
            setLoading={setLoading}
          />
        )}
        {step === 'results' && result && (
          <Results result={result} flow={flow} onShowFeedback={handleShowFeedback} onStartOver={handleStartOver} />
        )}
        {step === 'feedback' && result && sessionId && (
          <Feedback
            sessionId={sessionId}
            currentResult={result}
            onFeedbackComplete={handleFeedbackComplete}
            loading={loading}
            setLoading={setLoading}
          />
        )}
      </main>

      <footer className="py-8 text-center text-xs text-muted/60 tracking-wide select-none">
        Resume Apply &copy; {new Date().getFullYear()} &middot; AI-Powered Career Tools
      </footer>
    </div>
  );
}

export default App;
