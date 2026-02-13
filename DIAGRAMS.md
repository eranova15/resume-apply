# System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACE                                  │
│                          (React + TypeScript)                                │
│                         http://localhost:3000                                │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ HTTP/JSON
                                      │ (Vite Proxy)
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           FASTAPI BACKEND                                    │
│                         http://localhost:8000                                │
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   Session    │  │   Upload     │  │   Apply/     │  │   Feedback   │   │
│  │  Management  │─▶│   Resume     │─▶│   Improve    │─▶│     Loop     │   │
│  │   (main.py)  │  │  (main.py)   │  │  (main.py)   │  │  (main.py)   │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
│                            │                  │                              │
│                            ▼                  ▼                              │
│                    ┌──────────────┐  ┌──────────────┐                       │
│                    │    Resume    │  │   Job        │                       │
│                    │    Parser    │  │   Scraper    │                       │
│                    │ (PyPDF2)     │  │ (BS4)        │                       │
│                    └──────────────┘  └──────────────┘                       │
│                                              │                               │
│                                              ▼                               │
│                                      ┌──────────────┐                        │
│                                      │   AI Engine  │                        │
│                                      │  (OpenAI)    │                        │
│                                      │  - Analyze   │                        │
│                                      │  - Suggest   │                        │
│                                      │  - Improve   │                        │
│                                      │  - Generate  │                        │
│                                      └──────────────┘                        │
│                                              │                               │
│                                              ▼                               │
│                                      ┌──────────────┐                        │
│                                      │  PDF Gen     │                        │
│                                      │ (ReportLab)  │                        │
│                                      └──────────────┘                        │
│                                              │                               │
│                                              ▼                               │
│                                      ┌──────────────┐                        │
│                                      │  Download    │                        │
│                                      │    Files     │                        │
│                                      └──────────────┘                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
                           ┌──────────────────┐
                           │   OpenAI API     │
                           │   GPT-4o/GPT-4   │
                           └──────────────────┘


═══════════════════════════════════════════════════════════════════════════════

                            DATA FLOW DIAGRAM

┌─────────────┐
│   User      │
│  Selects    │
│   Flow      │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SESSION CREATION                                     │
│  POST /api/session { flow: "improve" | "apply" }                           │
│  ← { session_id: "abc123" }                                                │
└──────────────────────────────────────────┬──────────────────────────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         RESUME UPLOAD                                        │
│  POST /api/upload-resume?session_id=abc123                                 │
│  Body: multipart/form-data (PDF/TXT)                                       │
│  → Parse with PyPDF2                                                        │
│  → Store text in session                                                    │
│  ← { ok: true, chars: 1500 }                                               │
└──────────────────────────────────────────┬──────────────────────────────────┘
                                           │
                      ┌────────────────────┴────────────────────┐
                      │                                         │
                      ▼                                         ▼
        ┌──────────────────────┐              ┌──────────────────────┐
        │   IMPROVE FLOW       │              │   APPLY FLOW         │
        │                      │              │                      │
        │ POST /api/improve    │              │ POST /api/apply      │
        │ {                    │              │ {                    │
        │   session_id,        │              │   session_id,        │
        │   change_notes       │              │   job_urls: [...]    │
        │ }                    │              │ }                    │
        │                      │              │                      │
        │ ↓                    │              │ ↓                    │
        │ AI improves resume   │              │ Scrape jobs          │
        │                      │              │ ↓                    │
        │                      │              │ AI analyzes + matches│
        │                      │              │ ↓                    │
        │                      │              │ Generate suggestions │
        │                      │              │ ↓                    │
        │                      │              │ Improve resume       │
        │                      │              │ ↓                    │
        │                      │              │ Generate cover letter│
        └──────────┬───────────┘              └──────────┬───────────┘
                   │                                     │
                   └──────────────┬──────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         GENERATE PDFs                                        │
│  → ReportLab creates styled PDFs                                            │
│  → Save to outputs/ directory                                               │
│  → Return URLs for download                                                 │
│  ← {                                                                        │
│      suggestions: [...],                                                    │
│      improved_resume_text: "...",                                           │
│      cover_letter_text: "...",                                              │
│      resume_pdf_url: "/api/download/resume_abc123_v1.pdf",                 │
│      cover_letter_pdf_url: "/api/download/cover_letter_abc123_v1.pdf"      │
│    }                                                                        │
└──────────────────────────────────────────┬──────────────────────────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         USER REVIEWS RESULTS                                 │
│  Frontend displays:                                                         │
│  - Suggestions (section, original, suggested, reason)                       │
│  - Improved resume text                                                     │
│  - Cover letter text                                                        │
│  - Download buttons                                                         │
└──────────────────────────────────────────┬──────────────────────────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FEEDBACK LOOP                                        │
│  User chooses:                                                              │
│  1. ACCEPT → Done! Download PDFs                                           │
│  2. CHANGE → Provide change notes, select resume source                    │
│  3. IMPROVE → Generate new version, optional notes                         │
│                                                                             │
│  POST /api/feedback {                                                       │
│    session_id,                                                              │
│    choice: "accept" | "change" | "improve",                                │
│    change_notes: "...",                                                     │
│    resume_source: "old" | "new"                                            │
│  }                                                                          │
│                                                                             │
│  → If not "accept", loop back to AI processing                             │
│  → iteration++                                                              │
│  → Generate new PDFs with version tag                                      │
│  ← New EngineResponse                                                      │
└──────────────────────────────────────────┬──────────────────────────────────┘
                                           │
                                           │ Loop until accepted
                                           └─────────────────┐
                                                             │
                                                             ▼
                                                    ┌──────────────┐
                                                    │   Complete   │
                                                    │  Download    │
                                                    │    PDFs      │
                                                    └──────────────┘


═══════════════════════════════════════════════════════════════════════════════

                        COMPONENT INTERACTION

┌─────────────────────────────────────────────────────────────────────────────┐
│                          FRONTEND COMPONENTS                                 │
│                                                                              │
│  ┌────────────┐       ┌────────────┐       ┌────────────┐                  │
│  │   Flow     │──────▶│  Resume    │──────▶│    Job     │                  │
│  │  Selector  │       │  Upload    │       │   Input    │                  │
│  └────────────┘       └────────────┘       └────────────┘                  │
│                                                    │                         │
│                                                    ▼                         │
│                                             ┌────────────┐                   │
│                                             │  Results   │                   │
│                                             │  Display   │                   │
│                                             └──────┬─────┘                   │
│                                                    │                         │
│                                                    ▼                         │
│                                             ┌────────────┐                   │
│                                             │ Feedback   │                   │
│                                             │  Component │                   │
│                                             └──────┬─────┘                   │
│                                                    │                         │
│                                                    │ Accept?                 │
│                                                    │ No ─┐                   │
│                                                    │ Yes │                   │
│                                                    ▼     │                   │
│                                             ┌────────────┤                   │
│                                             │   Done     │                   │
│                                             └────────────┘                   │
│                                                          │                   │
│                                                          └──────┐            │
│                                                                 │            │
└─────────────────────────────────────────────────────────────────┼────────────┘
                                                                  │
                                                                  │ Loop back
                                                                  └────────────┐
                                                                               │
                                                                               ▼
                                                                         (Results)


═══════════════════════════════════════════════════════════════════════════════

                           FILE STRUCTURE

resume-apply/
│
├── 📄 README.md              → Project overview
├── 📄 SETUP.md               → Setup instructions
├── 📄 USAGE.md               → User guide
├── 📄 ARCHITECTURE.md        → Technical details
├── 📄 PROJECT_STATUS.md      → Status summary
├── 🚀 start.sh               → Quick start script
│
├── 🐍 backend/               → Python/FastAPI Backend
│   ├── config.py             → Configuration & env vars
│   ├── engine.py             → AI engine (OpenAI integration)
│   ├── main.py               → FastAPI app & endpoints
│   ├── models.py             → Pydantic data models
│   ├── pdf_gen.py            → PDF generation (ReportLab)
│   ├── resume_parser.py      → PDF text extraction (PyPDF2)
│   ├── scraper.py            → Job scraping (BeautifulSoup)
│   ├── requirements.txt      → Python dependencies
│   ├── uploads/              → Uploaded resumes
│   └── outputs/              → Generated PDFs
│
└── ⚛️  frontend/              → React/TypeScript Frontend
    ├── src/
    │   ├── components/       → React components
    │   │   ├── FlowSelector.tsx
    │   │   ├── ResumeUpload.tsx
    │   │   ├── JobInput.tsx
    │   │   ├── Results.tsx
    │   │   └── Feedback.tsx
    │   ├── services/
    │   │   └── api.ts        → API client (Axios)
    │   ├── types/
    │   │   └── api.ts        → TypeScript type definitions
    │   ├── App.tsx           → Main app component
    │   ├── main.tsx          → Entry point
    │   └── index.css         → Global styles
    ├── package.json          → Node dependencies
    ├── vite.config.ts        → Vite configuration
    ├── tailwind.config.js    → Tailwind CSS config
    └── tsconfig.json         → TypeScript config


═══════════════════════════════════════════════════════════════════════════════

                       TECHNOLOGY STACK

┌─────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  Framework:     React 18                                                    │
│  Language:      TypeScript 5.3                                              │
│  Build Tool:    Vite 5.0                                                    │
│  Styling:       Tailwind CSS 3.4                                            │
│  HTTP Client:   Axios 1.6                                                   │
│  Dev Server:    http://localhost:3000                                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              BACKEND                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  Framework:     FastAPI 0.104                                               │
│  Language:      Python 3.9+                                                 │
│  Server:        Uvicorn (ASGI)                                              │
│  AI:            OpenAI API (GPT-4o/GPT-4)                                   │
│  Scraping:      BeautifulSoup4 + Requests                                   │
│  PDF Parse:     PyPDF2                                                      │
│  PDF Gen:       ReportLab                                                   │
│  Validation:    Pydantic                                                    │
│  Dev Server:    http://localhost:8000                                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           COMMUNICATION                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  Protocol:      HTTP/JSON REST API                                          │
│  CORS:          Enabled for all origins (dev)                               │
│  Proxy:         Vite proxies /api to backend                                │
│  Session:       In-memory dict (sessionId: SessionState)                    │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════

                           KEY FEATURES

✅ Dual Flow System
   - Standalone resume improvement
   - Job-specific resume tailoring

✅ AI-Powered Analysis
   - Job requirement extraction
   - Resume-job matching
   - Actionable suggestions with reasoning
   - ATS-friendly improvements

✅ Iterative Feedback Loop
   - Accept, Change, or Improve
   - Version tracking (v1, v2, v3...)
   - Choose resume source (old/new)
   - User-guided refinements

✅ Professional Output
   - Styled PDF resumes
   - Custom cover letters
   - ATS-friendly formatting
   - Download functionality

✅ Modern UI/UX
   - Responsive design
   - Smooth animations
   - Loading states
   - Error handling
   - Drag & drop upload


═══════════════════════════════════════════════════════════════════════════════
