"""PDF generation using ReportLab."""

from __future__ import annotations

import os
import uuid
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    HRFlowable,
)

from config import OUTPUT_DIR


# ─── colour palette (modern teal / slate) ───

ACCENT = colors.HexColor("#0EA5E9")    # sky-500
DARK = colors.HexColor("#0F172A")      # slate-900
MUTED = colors.HexColor("#64748B")     # slate-500
DIVIDER = colors.HexColor("#CBD5E1")   # slate-300


def _styles():
    ss = getSampleStyleSheet()
    ss.add(ParagraphStyle(
        "ResumeName",
        parent=ss["Title"],
        fontSize=22,
        leading=26,
        textColor=DARK,
        spaceAfter=2,
        alignment=TA_CENTER,
    ))
    ss.add(ParagraphStyle(
        "ResumeSection",
        parent=ss["Heading2"],
        fontSize=13,
        leading=16,
        textColor=ACCENT,
        spaceBefore=14,
        spaceAfter=4,
        borderPadding=(0, 0, 2, 0),
    ))
    ss.add(ParagraphStyle(
        "ResumeBody",
        parent=ss["Normal"],
        fontSize=10,
        leading=14,
        textColor=DARK,
        alignment=TA_JUSTIFY,
        spaceAfter=4,
    ))
    ss.add(ParagraphStyle(
        "ResumeMeta",
        parent=ss["Normal"],
        fontSize=9,
        leading=12,
        textColor=MUTED,
        alignment=TA_CENTER,
        spaceAfter=8,
    ))
    ss.add(ParagraphStyle(
        "CoverBody",
        parent=ss["Normal"],
        fontSize=11,
        leading=16,
        textColor=DARK,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
    ))
    return ss


def _build_pdf(filename: str, story: list) -> str:
    path = OUTPUT_DIR / filename
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )
    doc.build(story)
    return str(path)


def _parse_resume_to_story(text: str, styles) -> list:
    """Convert plain-text resume (section headers + bullets) into flowables."""
    story: list = []
    lines = text.split("\n")
    first_line = True
    for line in lines:
        stripped = line.strip()
        if not stripped:
            story.append(Spacer(1, 4))
            continue
        # Detect section headers (ALL CAPS or lines ending with ':' or starting with ##)
        is_header = (
            stripped.isupper() and len(stripped) > 2
            or stripped.startswith("##")
            or (stripped.endswith(":") and len(stripped) < 60 and not stripped.startswith("-"))
        )
        cleaned = stripped.lstrip("#").strip().rstrip(":")
        if first_line and not is_header:
            story.append(Paragraph(cleaned, styles["ResumeName"]))
            story.append(HRFlowable(width="60%", thickness=1, color=ACCENT, spaceAfter=6))
            first_line = False
            continue
        first_line = False
        if is_header:
            story.append(HRFlowable(width="100%", thickness=0.5, color=DIVIDER, spaceBefore=6, spaceAfter=2))
            story.append(Paragraph(cleaned.upper(), styles["ResumeSection"]))
        elif stripped.startswith(("-", "•", "·", "*")):
            bullet_text = stripped.lstrip("-•·* ").strip()
            story.append(Paragraph(f"•  {bullet_text}", styles["ResumeBody"]))
        else:
            story.append(Paragraph(stripped, styles["ResumeBody"]))
    return story


def generate_resume_pdf(resume_text: str, tag: str = "") -> str:
    styles = _styles()
    story = _parse_resume_to_story(resume_text, styles)
    uid = tag or uuid.uuid4().hex[:8]
    return _build_pdf(f"resume_{uid}.pdf", story)


def generate_cover_letter_pdf(cover_letter_text: str, tag: str = "") -> str:
    styles = _styles()
    story: list = []
    story.append(Paragraph("Cover Letter", styles["ResumeName"]))
    story.append(HRFlowable(width="40%", thickness=1, color=ACCENT, spaceAfter=14))
    for para in cover_letter_text.split("\n\n"):
        para = para.strip()
        if para:
            story.append(Paragraph(para.replace("\n", "<br/>"), styles["CoverBody"]))
    uid = tag or uuid.uuid4().hex[:8]
    return _build_pdf(f"cover_letter_{uid}.pdf", story)
