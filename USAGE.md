# Resume Apply - Usage Guide

## Quick Start

### Option 1: Use the Start Script (Recommended)
```bash
./start.sh
```

This will start both backend (port 8000) and frontend (port 3000) automatically.

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Option 3: Backend Only (for API testing)
```bash
cd backend
uvicorn main:app --reload
```

Visit `http://localhost:8000/docs` for interactive API documentation.

## User Workflow

### Flow 1: Improve Resume (Standalone)

1. **Select Flow**: Choose "Improve Resume"
2. **Upload Resume**: Upload your current resume (PDF or TXT)
3. **Provide Instructions** (Optional): Specify areas to improve
4. **Review Results**: See AI-generated improvements
5. **Provide Feedback**:
   - **Accept**: You're done!
   - **Request Changes**: Specify what to modify
   - **Improve Further**: Generate another iteration

**Example Instructions:**
- "Make the experience section more impactful with quantifiable achievements"
- "Add more technical skills relevant to software engineering"
- "Improve action verbs and make it more ATS-friendly"

---

### Flow 2: Apply to Jobs

1. **Select Flow**: Choose "Apply to Jobs"
2. **Upload Resume**: Upload your current resume (PDF or TXT)
3. **Enter Job URLs**: Add one or more job posting URLs
4. **Review Results**: See:
   - **Suggestions**: Section-by-section changes with reasons
   - **Tailored Resume**: Updated resume matching job requirements
   - **Cover Letter**: Customized cover letter for the position
5. **Provide Feedback**:
   - **Accept**: Download PDFs and you're ready to apply!
   - **Request Changes**: Modify specific sections
   - **Improve Further**: Generate another version

**Supported Job Boards:**
- LinkedIn
- Indeed
- Glassdoor
- Company career pages
- Most other job posting sites

---

## Feedback Loop Options

### 1. Accept ✅
Use when you're satisfied with the results. Your PDFs are ready for download!

### 2. Request Changes 🔧
Use when you want specific modifications:

**Resume Source:**
- **New Improved Resume**: Use the latest AI-generated version as base
- **Original Resume**: Start fresh from your original upload

**Change Notes:**
Specify exactly what you want changed:
- "Add more details about my project management experience"
- "Make the skills section focus more on cloud technologies"
- "Change the summary to be more senior-level"
- "Remove some technical jargon and make it more accessible"

### 3. Improve Further 🚀
Generate another iteration with general improvements or specific instructions.

**Resume Source:**
- Choose which version to improve from

**Change Notes (Optional):**
- Provide guidance or leave blank for general improvements

---

## Tips for Best Results

### Resume Upload
- ✅ **PDF preferred** for best text extraction
- ✅ Use standard resume formats (no complex layouts)
- ✅ Include all relevant information (skills, experience, education)
- ❌ Avoid image-based PDFs (text must be selectable)

### Job URLs
- ✅ Use the full job posting URL
- ✅ Multiple jobs = better cross-matching of requirements
- ✅ Works best with detailed job descriptions
- ❌ Avoid shortened URLs or redirect links

### Change Instructions
- ✅ **Be specific**: "Add quantifiable metrics to the sales section"
- ✅ **Reference sections**: "In the experience section, emphasize leadership"
- ✅ **Set the tone**: "Make it more formal/casual/technical"
- ❌ Avoid vague requests like "make it better"

### Iterative Improvements
- Start with 1-2 job URLs to see general direction
- Use feedback loop to refine specific sections
- Typically 2-3 iterations produce optimal results
- Each iteration is versioned (v1, v2, v3...)

---

## Features Explained

### AI Suggestions (Apply Flow Only)
The AI analyzes your resume against job requirements and provides:
- **Section**: Which part of your resume (e.g., "Experience", "Skills")
- **Original**: The current text
- **Suggested**: Improved version
- **Reason**: Why this change helps

### Resume Improvements
AI enhances your resume by:
- Adding quantifiable achievements (numbers, percentages)
- Improving action verbs (led → spearheaded)
- Tailoring keywords to match job descriptions (ATS optimization)
- Restructuring bullet points for impact
- Removing redundancies and improving clarity

### Cover Letter Generation (Apply Flow Only)
AI creates a compelling cover letter that:
- Addresses the specific position and company
- Highlights relevant experience from your resume
- Shows enthusiasm and cultural fit
- Maintains professional tone
- Keeps concise (typically 300-400 words)

### PDF Downloads
Generated PDFs feature:
- Professional formatting with clean typography
- ATS-friendly layout (no complex tables or graphics)
- Branded color scheme (sky blue accents)
- Proper spacing and readability
- Section headers with visual hierarchy

---

## API Endpoints Reference

### Session Management
```
POST /api/session
Body: { "flow": "improve" | "apply" }
Returns: { "session_id": "..." }
```

### Upload Resume
```
POST /api/upload-resume?session_id={id}
Body: multipart/form-data with file
Returns: { "ok": true, "filename": "...", "chars": 1234 }
```

### Apply Flow
```
POST /api/apply
Body: {
  "session_id": "...",
  "job_urls": ["https://..."]
}
Returns: EngineResponse
```

### Improve Flow
```
POST /api/improve
Body: {
  "session_id": "...",
  "change_notes": "...", // optional
  "resume_source": "old" | "new" // optional
}
Returns: EngineResponse
```

### Feedback
```
POST /api/feedback
Body: {
  "session_id": "...",
  "choice": "accept" | "change" | "improve",
  "change_notes": "...", // optional
  "resume_source": "old" | "new" // optional
}
Returns: EngineResponse
```

### Download
```
GET /api/download/{filename}
Returns: PDF file
```

---

## Troubleshooting

### Backend Won't Start
```bash
# Check Python version
python3 --version  # Should be 3.9+

# Install dependencies
cd backend
pip install -r requirements.txt

# Check .env file exists
cat .env
```

### Frontend Won't Start
```bash
# Check Node version
node --version  # Should be 18+

# Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### API Connection Issues
- ✅ Backend must be running on port 8000
- ✅ Frontend proxy is configured in `vite.config.ts`
- ✅ Check browser console for CORS errors
- ✅ Verify both servers are running: `curl http://localhost:8000/api/health`

### OpenAI API Errors
```bash
# Verify API key
cd backend
cat .env | grep OPENAI_API_KEY

# Check API quota/billing
# Visit https://platform.openai.com/usage
```

### File Upload Failures
- Max file size: 10MB
- Accepted formats: PDF, TXT
- Ensure file is not corrupted
- Try different file if PDF text extraction fails

### Scraping Failures
- Some sites block automated scraping
- Try different job boards
- Verify URL is publicly accessible
- Check job posting still exists

---

## Advanced Usage

### Running Tests
```bash
# Backend (if tests are added)
cd backend
pytest

# Frontend
cd frontend
npm test
```

### Production Deployment

**Backend:**
```bash
# Use production ASGI server
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

**Frontend:**
```bash
cd frontend
npm run build
# Serve 'dist' folder with nginx/apache
```

### Environment Variables

**Backend (.env):**
```
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o  # or gpt-4, gpt-4-turbo-preview
```

**Frontend:**
No environment variables needed (uses proxy)

---

## Support

For issues or questions:
1. Check this guide
2. Review backend logs
3. Check browser console (F12)
4. Verify API is responding: http://localhost:8000/docs

## Version Information

- Backend API: v1.0.0
- Frontend: v1.0.0
- Last Updated: 2026-02-13
