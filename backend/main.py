"""FastAPI application – Resume Apply backend with SQLite persistence."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from config import DEMO_MODE, OUTPUT_DIR, UPLOAD_DIR
from database import (
    create_session,
    get_engine_results,
    get_latest_engine_result,
    get_scrape_results,
    get_session,
    get_stats,
    init_db,
    list_sessions,
    save_engine_result,
    save_scrape_results,
    save_uploaded_file,
    update_session,
)
from engine import run_engine
from models import (
    ApplyRequest,
    EngineResult,
    FeedbackChoice,
    FeedbackRequest,
    ImproveRequest,
    ScrapeResult,
    StartSessionRequest,
    StartSessionResponse,
    Suggestion,
)
from pdf_gen import generate_cover_letter_pdf, generate_resume_pdf
from resume_parser import extract_text_from_pdf
from scraper import scrape_job

app = FastAPI(title="Resume Apply", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()
    mode = "DEMO (mock AI)" if DEMO_MODE else "LIVE (OpenAI)"
    print(f"🚀 Resume Apply backend started  –  Mode: {mode}")


# ──────────────────────────────────────
# Health & info
# ──────────────────────────────────────

@app.get("/api/health")
def health():
    return {"status": "ok", "demo_mode": DEMO_MODE}


@app.get("/api/stats")
def stats():
    return get_stats()


@app.get("/api/sessions")
def sessions_list():
    return list_sessions()


# ──────────────────────────────────────
# Session management
# ──────────────────────────────────────

@app.post("/api/session", response_model=StartSessionResponse)
def start_session(req: StartSessionRequest):
    sid = create_session(req.flow.value)
    return StartSessionResponse(session_id=sid)


@app.get("/api/session/{session_id}")
def session_detail(session_id: str):
    session = get_session(session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    scrapes = get_scrape_results(session_id)
    engine = get_latest_engine_result(session_id)
    return {
        "session": session,
        "scrape_results": scrapes,
        "engine_result": engine,
    }


# ──────────────────────────────────────
# Resume upload
# ──────────────────────────────────────

@app.post("/api/upload/{session_id}")
async def upload_resume(session_id: str, file: UploadFile = File(...)):
    session = get_session(session_id)
    if not session:
        raise HTTPException(404, "Session not found")

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are supported")

    # Save file
    dest = UPLOAD_DIR / f"{session_id}_{file.filename}"
    content = await file.read()
    with open(dest, "wb") as f:
        f.write(content)

    # Extract text
    text = extract_text_from_pdf(str(dest))
    if not text.strip():
        raise HTTPException(400, "Could not extract text from PDF – is it a scanned image?")

    # Update session
    update_session(
        session_id,
        original_resume_text=text,
        original_resume_filename=file.filename,
    )

    # Track file
    save_uploaded_file(session_id, file.filename, str(dest), len(content), len(text))

    return {
        "filename": file.filename,
        "char_count": len(text),
        "preview": text[:500],
    }


# ──────────────────────────────────────
# Apply flow – scrape & engines
# ──────────────────────────────────────

@app.post("/api/apply")
def apply_flow(req: ApplyRequest):
    session = get_session(req.session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    if not session["original_resume_text"]:
        raise HTTPException(400, "Upload a resume first")
    if not req.job_urls:
        raise HTTPException(400, "Provide at least one job URL")

    # Store URLs
    update_session(req.session_id, job_urls=req.job_urls)

    # Scrape each URL
    scrape_results: list[ScrapeResult] = []
    for url in req.job_urls:
        result = scrape_job(url)
        scrape_results.append(result)

    # Save scrape results to DB
    save_scrape_results(req.session_id, [r.model_dump() for r in scrape_results])

    # Run AI engine
    iteration = session["iteration"] + 1
    engine_result: EngineResult = run_engine(
        resume_text=session["original_resume_text"],
        jobs=scrape_results,
        flow="apply",
    )

    # Generate PDFs
    tag = f"{req.session_id}_v{iteration}"
    resume_pdf = generate_resume_pdf(engine_result.improved_resume_text, tag)
    cover_pdf = generate_cover_letter_pdf(engine_result.cover_letter_text, tag)
    engine_result.resume_pdf_path = resume_pdf
    engine_result.cover_letter_pdf_path = cover_pdf

    # Save engine result
    save_engine_result(req.session_id, iteration, engine_result.model_dump())
    update_session(
        req.session_id,
        iteration=iteration,
        improved_resume_text=engine_result.improved_resume_text,
    )

    return {
        "scrape_results": [r.model_dump() for r in scrape_results],
        "suggestions": [s.model_dump() for s in engine_result.suggestions],
        "improved_resume_text": engine_result.improved_resume_text,
        "cover_letter_text": engine_result.cover_letter_text,
        "resume_pdf": os.path.basename(resume_pdf),
        "cover_letter_pdf": os.path.basename(cover_pdf),
        "iteration": iteration,
    }


# ──────────────────────────────────────
# Improve flow (standalone)
# ──────────────────────────────────────

@app.post("/api/improve")
def improve_flow(req: ImproveRequest):
    session = get_session(req.session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    if not session["original_resume_text"]:
        raise HTTPException(400, "Upload a resume first")

    # Choose source text
    source = session["original_resume_text"]
    if req.resume_source and req.resume_source.value == "new" and session["improved_resume_text"]:
        source = session["improved_resume_text"]

    iteration = session["iteration"] + 1
    engine_result: EngineResult = run_engine(
        resume_text=source,
        jobs=[],
        change_notes=req.change_notes,
        flow="improve",
    )

    # Generate PDF
    tag = f"{req.session_id}_v{iteration}"
    resume_pdf = generate_resume_pdf(engine_result.improved_resume_text, tag)
    engine_result.resume_pdf_path = resume_pdf

    save_engine_result(req.session_id, iteration, engine_result.model_dump())
    update_session(
        req.session_id,
        iteration=iteration,
        improved_resume_text=engine_result.improved_resume_text,
    )

    return {
        "improved_resume_text": engine_result.improved_resume_text,
        "resume_pdf": os.path.basename(resume_pdf),
        "iteration": iteration,
    }


# ──────────────────────────────────────
# Feedback loop
# ──────────────────────────────────────

@app.post("/api/feedback")
def feedback(req: FeedbackRequest):
    session = get_session(req.session_id)
    if not session:
        raise HTTPException(404, "Session not found")

    if req.choice == FeedbackChoice.ACCEPT:
        return {"status": "accepted", "message": "Great! Your documents are ready for download."}

    # Re-run engine with notes
    source = session["original_resume_text"]
    if req.resume_source and req.resume_source.value == "new" and session["improved_resume_text"]:
        source = session["improved_resume_text"]

    scrape_data = get_scrape_results(req.session_id)
    scrape_results = [
        ScrapeResult(
            url=s["url"],
            title=s.get("title", ""),
            company=s.get("company", ""),
            description=s.get("description", ""),
            requirements=s.get("requirements", []),
            error=s.get("error"),
        )
        for s in scrape_data
    ]

    iteration = session["iteration"] + 1
    flow = session.get("flow", "apply")
    engine_result: EngineResult = run_engine(
        resume_text=source,
        jobs=scrape_results,
        change_notes=req.change_notes,
        flow=flow,
    )

    tag = f"{req.session_id}_v{iteration}"
    resume_pdf = generate_resume_pdf(engine_result.improved_resume_text, tag)
    engine_result.resume_pdf_path = resume_pdf
    if engine_result.cover_letter_text:
        cover_pdf = generate_cover_letter_pdf(engine_result.cover_letter_text, tag)
        engine_result.cover_letter_pdf_path = cover_pdf

    save_engine_result(req.session_id, iteration, engine_result.model_dump())
    update_session(
        req.session_id,
        iteration=iteration,
        improved_resume_text=engine_result.improved_resume_text,
    )

    result = {
        "suggestions": [s.model_dump() for s in engine_result.suggestions],
        "improved_resume_text": engine_result.improved_resume_text,
        "resume_pdf": os.path.basename(resume_pdf),
        "iteration": iteration,
    }
    if engine_result.cover_letter_text:
        result["cover_letter_text"] = engine_result.cover_letter_text
        result["cover_letter_pdf"] = os.path.basename(engine_result.cover_letter_pdf_path)
    return result


# ──────────────────────────────────────
# PDF downloads
# ──────────────────────────────────────

@app.get("/api/download/{filename}")
def download(filename: str):
    path = OUTPUT_DIR / filename
    if not path.exists():
        raise HTTPException(404, "File not found")
    return FileResponse(str(path), media_type="application/pdf", filename=filename)


# ──────────────────────────────────────
# History
# ──────────────────────────────────────

@app.get("/api/history/{session_id}")
def history(session_id: str):
    session = get_session(session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    results = get_engine_results(session_id)
    scrapes = get_scrape_results(session_id)
    return {
        "session": session,
        "scrape_results": scrapes,
        "engine_results": results,
    }
