"""Resume text extraction from uploaded PDF."""

from __future__ import annotations

from pathlib import Path

import PyPDF2


def extract_text_from_pdf(file_path: str | Path) -> str:
    """Extract plain text from a PDF file."""
    text_parts: list[str] = []
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts)
