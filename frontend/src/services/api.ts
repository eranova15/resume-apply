import axios from 'axios';
import type {
  StartSessionResponse,
  ApplyRequest,
  ImproveRequest,
  FeedbackRequest,
  EngineResponse,
  UploadResponse,
  HealthResponse,
} from '../types/api';

const API_BASE = '/api';

export const api = {
  async health(): Promise<HealthResponse> {
    const { data } = await axios.get<HealthResponse>(`${API_BASE}/health`);
    return data;
  },

  async startSession(flow: 'improve' | 'apply'): Promise<StartSessionResponse> {
    const { data } = await axios.post<StartSessionResponse>(`${API_BASE}/session`, { flow });
    return data;
  },

  async uploadResume(sessionId: string, file: File): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    const { data } = await axios.post<UploadResponse>(
      `${API_BASE}/upload/${sessionId}`,
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' } },
    );
    return data;
  },

  async apply(request: ApplyRequest): Promise<EngineResponse> {
    const { data } = await axios.post<EngineResponse>(`${API_BASE}/apply`, request);
    return data;
  },

  async improve(request: ImproveRequest): Promise<EngineResponse> {
    const { data } = await axios.post<EngineResponse>(`${API_BASE}/improve`, request);
    return data;
  },

  async feedback(request: FeedbackRequest): Promise<EngineResponse> {
    const { data } = await axios.post<EngineResponse>(`${API_BASE}/feedback`, request);
    return data;
  },

  downloadUrl(filename: string): string {
    return `${API_BASE}/download/${filename}`;
  },
};
