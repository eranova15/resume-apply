# Setup Checklist

Complete this checklist before running the application.

## Prerequisites

### 1. Python Environment ✓
- [ ] Python 3.9+ installed
  ```bash
  python3 --version
  ```

### 2. Node.js Environment ✓  
- [ ] Node.js 18+ installed
  ```bash
  node --version
  ```

### 3. OpenAI API Key ✓
- [ ] Have an OpenAI API key
- [ ] API key has available credits
- Visit: https://platform.openai.com/api-keys

---

## Backend Setup

### 1. Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

**Required packages:**
- fastapi
- uvicorn
- openai
- pydantic
- python-dotenv
- requests
- beautifulsoup4
- PyPDF2
- reportlab

### 2. Create Environment File
```bash
cd backend
touch .env
```

**Add to .env:**
```
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-4o
```

### 3. Create Required Directories
```bash
cd backend
mkdir -p uploads outputs
```

### 4. Test Backend
```bash
cd backend
uvicorn main:app --reload
```

- [ ] Server starts without errors
- [ ] Visit http://localhost:8000/docs
- [ ] API documentation loads

---

## Frontend Setup

### 1. Install Node Dependencies
```bash
cd frontend
npm install
```

**Key dependencies:**
- react
- react-dom
- typescript
- vite
- tailwindcss
- axios

### 2. Test Frontend
```bash
cd frontend
npm run dev
```

- [ ] Development server starts
- [ ] Visit http://localhost:3000
- [ ] No console errors

---

## Integration Testing

### 1. Both Servers Running
- [ ] Backend on http://localhost:8000
- [ ] Frontend on http://localhost:3000

### 2. Test Flow
1. [ ] Select a flow (Improve or Apply)
2. [ ] Upload a test resume (PDF or TXT)
3. [ ] Provide input (job URLs or improvement notes)
4. [ ] Verify results appear
5. [ ] Test feedback loop
6. [ ] Download generated PDFs

### 3. API Communication
- [ ] No CORS errors in browser console
- [ ] API calls successful (check Network tab)
- [ ] Files upload correctly
- [ ] PDFs generate and download

---

## Optional Enhancements

### Production Setup
- [ ] Set up proper database for sessions (Redis/PostgreSQL)
- [ ] Configure production ASGI server (gunicorn)
- [ ] Build and serve frontend static files
- [ ] Set up reverse proxy (nginx)
- [ ] Configure SSL/HTTPS

### Security
- [ ] Add rate limiting
- [ ] Implement user authentication
- [ ] Sanitize file uploads
- [ ] Add CSRF protection
- [ ] Secure API keys (use secrets manager)

### Monitoring
- [ ] Add logging framework
- [ ] Set up error tracking (Sentry)
- [ ] Monitor API usage
- [ ] Track OpenAI costs

---

## Troubleshooting

### Backend Issues

**Import errors:**
```bash
pip install -r requirements.txt --force-reinstall
```

**Port already in use:**
```bash
# Find process using port 8000
lsof -i :8000
# Kill it
kill -9 <PID>
```

**OpenAI API errors:**
- Check API key is correct
- Verify you have credits
- Check model name is valid

### Frontend Issues

**Dependencies not installing:**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Port 3000 in use:**
- Vite will automatically try next available port
- Or specify port in vite.config.ts

**Build errors:**
```bash
npm run build
# Check for TypeScript errors
```

### Integration Issues

**CORS errors:**
- Verify backend CORS middleware is configured
- Check proxy in vite.config.ts
- Ensure both servers are running

**API calls failing:**
- Check Network tab in browser DevTools
- Verify API endpoint URLs
- Check backend logs for errors

---

## Quick Start (After Setup Complete)

```bash
# From project root
./start.sh
```

Or manually:

**Terminal 1:**
```bash
cd backend
uvicorn main:app --reload
```

**Terminal 2:**
```bash
cd frontend
npm run dev
```

---

## Verification Commands

### Check Backend Health
```bash
curl http://localhost:8000/api/health
# Should return: {"status":"ok"}
```

### Check Frontend Build
```bash
cd frontend
npm run build
# Should complete without errors
```

### Check All Dependencies
```bash
# Backend
cd backend
pip list | grep -E "fastapi|openai|pydantic"

# Frontend
cd frontend
npm list --depth=0
```

---

## Success Criteria ✅

Your setup is complete when:

- ✅ Backend starts without errors on port 8000
- ✅ Frontend starts without errors on port 3000
- ✅ API documentation accessible at /docs
- ✅ Can upload resume successfully
- ✅ AI processing completes without errors
- ✅ PDFs generate and download correctly
- ✅ Feedback loop works through multiple iterations
- ✅ No console errors in browser
- ✅ No Python errors in terminal

---

## Support Resources

- **Backend API Docs**: http://localhost:8000/docs
- **OpenAI Status**: https://status.openai.com
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **React Docs**: https://react.dev
- **Tailwind CSS**: https://tailwindcss.com/docs

## Next Steps

After completing setup:
1. Read [USAGE.md](USAGE.md) for user workflows
2. Review [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
3. Test both "Improve" and "Apply" flows
4. Experiment with feedback iterations
5. Customize styling in tailwind.config.js if desired

---

**Last Updated:** 2026-02-13
