# Resume Apply

AI-powered resume optimization and job application assistant.

> **🎯 [READ THE EXECUTIVE SUMMARY](EXECUTIVE_SUMMARY.md)** for complete project status and assessment results.

## Overview

Resume Apply is a full-stack application that helps job seekers:
- **Improve their resumes** with AI-powered suggestions
- **Tailor resumes** to specific job postings
- **Generate customized cover letters** automatically
- **Iterate and refine** through an interactive feedback loop

## Architecture

### Backend (Python/FastAPI)
- **FastAPI** REST API with session management
- **OpenAI GPT-4** integration for AI-powered analysis
- **Job scraping** from various job boards
- **PDF generation** with styled formatting
- **Resume parsing** from PDF/TXT files

### Frontend (React/TypeScript)
- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **Vite** for fast development
- **Responsive design** with modern UI/UX

## Quick Start

```bash
# From project root
./start.sh
```

This starts both backend (port 8000) and frontend (port 3000) automatically.

### Manual Setup

See [SETUP.md](SETUP.md) for detailed setup instructions.

**Quick version:**

1. **Backend:**
```bash
cd backend
pip install -r requirements.txt
# Create .env with OPENAI_API_KEY
uvicorn main:app --reload
```

2. **Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Documentation

- **[SETUP.md](SETUP.md)** - Complete setup guide with checklist
- **[USAGE.md](USAGE.md)** - User workflows and usage examples
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical architecture and component details
- **[frontend/README.md](frontend/README.md)** - Frontend-specific documentation

## Features

### ✅ Dual Flow System
- **Improve Resume**: Standalone resume enhancement
- **Apply to Jobs**: Job-specific resume tailoring + cover letter generation

### ✅ AI-Powered Analysis
- Scrapes and analyzes job postings
- Generates actionable suggestions with reasons
- Tailors resume content to job requirements
- Creates compelling cover letters

### ✅ Iterative Improvement
- Review AI-generated suggestions
- Accept, request changes, or improve further
- Choose between original or improved resume as base
- Version tracking for multiple iterations

### ✅ Professional Output
- Clean, ATS-friendly resume formatting
- Styled PDF generation
- Downloadable resume and cover letter PDFs

## API Endpoints

- `POST /api/session` - Start a new session
- `POST /api/upload-resume` - Upload resume file
- `POST /api/apply` - Run apply flow (with job URLs)
- `POST /api/improve` - Run improve flow (standalone)
- `POST /api/feedback` - Submit feedback for iteration
- `GET /api/download/{filename}` - Download generated PDFs

## Tech Stack

**Backend:**
- FastAPI
- OpenAI API
- BeautifulSoup4 (scraping)
- ReportLab (PDF generation)
- PyPDF2 (PDF parsing)
- Pydantic (validation)

**Frontend:**
- React 18
- TypeScript
- Tailwind CSS
- Vite
- Axios

## Project Structure

```
resume-apply/
├── backend/
│   ├── config.py           # Configuration
│   ├── engine.py           # AI engine
│   ├── main.py             # FastAPI app
│   ├── models.py           # Data models
│   ├── pdf_gen.py          # PDF generation
│   ├── resume_parser.py    # Resume parsing
│   ├── scraper.py          # Job scraping
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API client
│   │   ├── types/          # TypeScript types
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## License

MIT