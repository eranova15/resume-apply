export type FlowType = 'improve' | 'apply';
export type FeedbackChoice = 'accept' | 'change' | 'improve';
export type ResumeSource = 'old' | 'new';

export interface StartSessionRequest {
  flow: FlowType;
}

export interface StartSessionResponse {
  session_id: string;
}

export interface ApplyRequest {
  session_id: string;
  job_urls: string[];
}

export interface ImproveRequest {
  session_id: string;
  change_notes?: string;
  resume_source?: ResumeSource;
}

export interface FeedbackRequest {
  session_id: string;
  choice: FeedbackChoice;
  change_notes?: string;
  resume_source?: ResumeSource;
}

export interface Suggestion {
  section: string;
  original: string;
  suggested: string;
  reason: string;
}

export interface ScrapeResult {
  url: string;
  title: string;
  company: string;
  description: string;
  requirements: string[];
  error: string | null;
}

export interface EngineResponse {
  iteration: number;
  suggestions: Suggestion[];
  improved_resume_text: string;
  cover_letter_text?: string;
  resume_pdf?: string;
  cover_letter_pdf?: string;
  scrape_results?: ScrapeResult[];
}

export interface UploadResponse {
  filename: string;
  char_count: number;
  preview: string;
}

export interface HealthResponse {
  status: string;
  demo_mode: boolean;
}
