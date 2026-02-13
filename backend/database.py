"""SQLite database layer for Resume Apply."""

from __future__ import annotations

import json
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Optional

from config import BASE_DIR

DB_PATH = BASE_DIR / "resume_apply.db"


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


@contextmanager
def get_db():
    conn = _connect()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Create tables if they don't exist."""
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS sessions (
                id            TEXT PRIMARY KEY,
                flow          TEXT NOT NULL DEFAULT 'apply',
                original_resume_text   TEXT DEFAULT '',
                improved_resume_text   TEXT DEFAULT '',
                original_resume_filename TEXT DEFAULT '',
                job_urls      TEXT DEFAULT '[]',
                iteration     INTEGER DEFAULT 0,
                created_at    TEXT DEFAULT (datetime('now')),
                updated_at    TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS scrape_results (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id  TEXT NOT NULL,
                url         TEXT NOT NULL,
                title       TEXT DEFAULT '',
                company     TEXT DEFAULT '',
                description TEXT DEFAULT '',
                requirements TEXT DEFAULT '[]',
                error       TEXT,
                scraped_at  TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS engine_results (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id  TEXT NOT NULL,
                iteration   INTEGER NOT NULL,
                suggestions TEXT DEFAULT '[]',
                improved_resume_text TEXT DEFAULT '',
                cover_letter_text    TEXT DEFAULT '',
                resume_pdf_path      TEXT,
                cover_letter_pdf_path TEXT,
                created_at  TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS uploaded_files (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id  TEXT NOT NULL,
                filename    TEXT NOT NULL,
                filepath    TEXT NOT NULL,
                file_size   INTEGER DEFAULT 0,
                char_count  INTEGER DEFAULT 0,
                uploaded_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_scrape_session ON scrape_results(session_id);
            CREATE INDEX IF NOT EXISTS idx_engine_session ON engine_results(session_id);
            CREATE INDEX IF NOT EXISTS idx_files_session  ON uploaded_files(session_id);
        """)


# ── Session CRUD ──

def create_session(flow: str) -> str:
    sid = uuid.uuid4().hex[:12]
    with get_db() as conn:
        conn.execute(
            "INSERT INTO sessions (id, flow) VALUES (?, ?)",
            (sid, flow),
        )
    return sid


def get_session(session_id: str) -> Optional[dict]:
    with get_db() as conn:
        row = conn.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()
        if not row:
            return None
        d = dict(row)
        d["job_urls"] = json.loads(d["job_urls"])
        return d


def update_session(session_id: str, **kwargs):
    with get_db() as conn:
        sets = []
        vals = []
        for k, v in kwargs.items():
            if k == "job_urls":
                v = json.dumps(v)
            sets.append(f"{k} = ?")
            vals.append(v)
        sets.append("updated_at = datetime('now')")
        vals.append(session_id)
        conn.execute(
            f"UPDATE sessions SET {', '.join(sets)} WHERE id = ?",
            vals,
        )


# ── Scrape results ──

def save_scrape_results(session_id: str, results: list[dict]):
    with get_db() as conn:
        # Clear old results for this session
        conn.execute("DELETE FROM scrape_results WHERE session_id = ?", (session_id,))
        for r in results:
            conn.execute(
                """INSERT INTO scrape_results
                   (session_id, url, title, company, description, requirements, error)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    session_id,
                    r.get("url", ""),
                    r.get("title", ""),
                    r.get("company", ""),
                    r.get("description", ""),
                    json.dumps(r.get("requirements", [])),
                    r.get("error"),
                ),
            )


def get_scrape_results(session_id: str) -> list[dict]:
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM scrape_results WHERE session_id = ?", (session_id,)
        ).fetchall()
        results = []
        for row in rows:
            d = dict(row)
            d["requirements"] = json.loads(d["requirements"])
            results.append(d)
        return results


# ── Engine results ──

def save_engine_result(session_id: str, iteration: int, result: dict):
    with get_db() as conn:
        conn.execute(
            """INSERT INTO engine_results
               (session_id, iteration, suggestions, improved_resume_text,
                cover_letter_text, resume_pdf_path, cover_letter_pdf_path)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                session_id,
                iteration,
                json.dumps(result.get("suggestions", [])),
                result.get("improved_resume_text", ""),
                result.get("cover_letter_text", ""),
                result.get("resume_pdf_path"),
                result.get("cover_letter_pdf_path"),
            ),
        )


def get_engine_results(session_id: str) -> list[dict]:
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM engine_results WHERE session_id = ? ORDER BY iteration",
            (session_id,),
        ).fetchall()
        results = []
        for row in rows:
            d = dict(row)
            d["suggestions"] = json.loads(d["suggestions"])
            results.append(d)
        return results


def get_latest_engine_result(session_id: str) -> Optional[dict]:
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM engine_results WHERE session_id = ? ORDER BY iteration DESC LIMIT 1",
            (session_id,),
        ).fetchone()
        if not row:
            return None
        d = dict(row)
        d["suggestions"] = json.loads(d["suggestions"])
        return d


# ── File tracking ──

def save_uploaded_file(session_id: str, filename: str, filepath: str, file_size: int, char_count: int):
    with get_db() as conn:
        conn.execute(
            """INSERT INTO uploaded_files
               (session_id, filename, filepath, file_size, char_count)
               VALUES (?, ?, ?, ?, ?)""",
            (session_id, filename, filepath, file_size, char_count),
        )


# ── Stats ──

def get_stats() -> dict:
    with get_db() as conn:
        sessions_count = conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
        scrapes_count = conn.execute("SELECT COUNT(*) FROM scrape_results").fetchone()[0]
        engine_count = conn.execute("SELECT COUNT(*) FROM engine_results").fetchone()[0]
        files_count = conn.execute("SELECT COUNT(*) FROM uploaded_files").fetchone()[0]
        return {
            "sessions": sessions_count,
            "scrapes": scrapes_count,
            "engine_runs": engine_count,
            "files_uploaded": files_count,
        }


def list_sessions(limit: int = 50) -> list[dict]:
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM sessions ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]
