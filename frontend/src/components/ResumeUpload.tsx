import React, { useState, useRef } from 'react';
import { api } from '../services/api';

interface Props {
  sessionId: string;
  onUploadComplete: () => void;
}

const ResumeUpload: React.FC<Props> = ({ sessionId, onUploadComplete }) => {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [preview, setPreview] = useState('');
  const [dragActive, setDragActive] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const pick = (f: File | null) => {
    if (!f) return;
    if (!f.name.toLowerCase().endsWith('.pdf')) {
      setError('Only PDF files are supported');
      return;
    }
    if (f.size > 10 * 1024 * 1024) {
      setError('File must be under 10 MB');
      return;
    }
    setFile(f);
    setError('');
    setPreview('');
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(e.type === 'dragenter' || e.type === 'dragover');
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files?.[0]) pick(e.dataTransfer.files[0]);
  };

  const upload = async () => {
    if (!file) return;
    setUploading(true);
    setError('');
    try {
      const res = await api.uploadResume(sessionId, file);
      setPreview(res.preview);
      // Give user a moment to see the preview, then advance
      setTimeout(onUploadComplete, 600);
    } catch {
      setError('Upload failed. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  const formatSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <div className="max-w-2xl mx-auto animate-slide-up">
      <div className="bg-white rounded-2xl shadow-card p-8 sm:p-10">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-brand-50 mb-4">
            <svg className="w-8 h-8 text-brand-600" fill="none" stroke="currentColor" strokeWidth={1.8} viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-dark mb-1">Upload Your Resume</h2>
          <p className="text-sm text-muted">PDF format &middot; Max 10 MB</p>
        </div>

        {/* Drop zone */}
        <div
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          className={`relative rounded-2xl border-2 border-dashed p-10 text-center transition-all duration-200 cursor-pointer
            ${dragActive
              ? 'border-brand-400 bg-brand-50/50 scale-[1.01]'
              : file
                ? 'border-accent-400 bg-accent-50/40'
                : 'border-surface-300 hover:border-brand-300 hover:bg-surface-50'
            }`}
          onClick={() => !file && inputRef.current?.click()}
        >
          <input
            ref={inputRef}
            type="file"
            accept=".pdf"
            onChange={(e) => pick(e.target.files?.[0] || null)}
            className="hidden"
          />

          {!file ? (
            <>
              <div className="w-14 h-14 mx-auto mb-4 rounded-full bg-surface-100 flex items-center justify-center">
                <svg className="w-7 h-7 text-muted" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 16v-8m0 0l-3 3m3-3l3 3M3.375 19.5h17.25" />
                </svg>
              </div>
              <p className="text-dark font-medium mb-1">Drag &amp; drop your resume here</p>
              <p className="text-sm text-muted">
                or{' '}
                <span className="text-brand-600 font-medium cursor-pointer hover:underline">
                  browse files
                </span>
              </p>
            </>
          ) : (
            <div className="flex items-center gap-4">
              <div className="flex-shrink-0 w-12 h-12 rounded-xl bg-accent-100 flex items-center justify-center">
                <svg className="w-6 h-6 text-accent-600" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="flex-1 text-left min-w-0">
                <p className="text-dark font-medium truncate">{file.name}</p>
                <p className="text-xs text-muted">{formatSize(file.size)}</p>
              </div>
              <button
                onClick={(e) => { e.stopPropagation(); setFile(null); setPreview(''); }}
                className="flex-shrink-0 w-8 h-8 rounded-lg bg-surface-100 hover:bg-red-50 flex items-center justify-center text-muted hover:text-red-500 transition-colors"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          )}
        </div>

        {/* Preview snippet */}
        {preview && (
          <div className="mt-4 p-4 bg-surface-50 rounded-xl border border-surface-200 animate-fade-in">
            <p className="text-xs font-semibold text-muted uppercase tracking-wider mb-2">Preview</p>
            <p className="text-sm text-dark/80 line-clamp-4 whitespace-pre-wrap">{preview}</p>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm animate-fade-in">
            {error}
          </div>
        )}

        {/* Upload button */}
        <button
          onClick={upload}
          disabled={!file || uploading}
          className="btn-primary w-full mt-6 py-3.5 text-base"
        >
          {uploading ? (
            <>
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
              Uploading&hellip;
            </>
          ) : (
            <>
              <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
              </svg>
              Upload &amp; Continue
            </>
          )}
        </button>
      </div>
    </div>
  );
};

export default ResumeUpload;
