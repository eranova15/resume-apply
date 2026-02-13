from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


# ── Enums ──

class FlowType(str, Enum):
    IMPROVE = "improve"
    APPLY = "apply"


class FeedbackChoice(str, Enum):
    ACCEPT = "accept"
    CHANGE = "change"
    IMPROVE = "improve"


class ResumeSource(str, Enum):
    OLD = "old"
    NEW = "new"


# ── Request / Response schemas ──

class StartSessionRequest(BaseModel):
    flow: FlowType


class StartSessionResponse(BaseModel):
    session_id: str


class ApplyRequest(BaseModel):
    session_id: str
    job_urls: list[str]


class ImproveRequest(BaseModel):
    session_id: str
    change_notes: Optional[str] = None
    resume_source: Optional[ResumeSource] = None


class FeedbackRequest(BaseModel):
    session_id: str
    choice: FeedbackChoice
    change_notes: Optional[str] = None
    resume_source: Optional[ResumeSource] = None


class ScrapeResult(BaseModel):
    url: str
    title: str = ""
    company: str = ""
    description: str = ""
    requirements: list[str] = []
    error: Optional[str] = None


class Suggestion(BaseModel):
    section: str
    original: str
    suggested: str
    reason: str


class EngineResult(BaseModel):
    suggestions: list[Suggestion] = []
    improved_resume_text: str = ""
    cover_letter_text: str = ""
    resume_pdf_path: Optional[str] = None
    cover_letter_pdf_path: Optional[str] = None
