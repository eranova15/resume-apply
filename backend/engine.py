"""AI engine – analyses resume vs job, produces suggestions, improved resume & cover letter.

Supports both OpenAI mode and Demo mode (mock responses when no API key)."""

from __future__ import annotations

import json
import re
import textwrap
from typing import Optional

from config import OPENAI_API_KEY, OPENAI_MODEL, DEMO_MODE
from models import EngineResult, ScrapeResult, Suggestion


# ─────────────────────────────────────────────
# OpenAI helpers
# ─────────────────────────────────────────────

def _chat(system: str, user: str, *, model: str = OPENAI_MODEL, temperature: float = 0.4) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=temperature,
    )
    return resp.choices[0].message.content or ""


# ─────────────────────────────────────────────
# Demo / Mock engine
# ─────────────────────────────────────────────

def _demo_suggestions(resume_text: str, jobs: list[ScrapeResult]) -> list[Suggestion]:
    """Generate realistic mock suggestions based on resume content."""
    suggestions = []
    lines = resume_text.strip().split("\n")

    # Find lines that look like bullet points or experience
    bullets = [l.strip() for l in lines if l.strip().startswith(("-", "•", "*")) and len(l.strip()) > 20]
    plain_lines = [l.strip() for l in lines if len(l.strip()) > 30 and not l.strip().startswith(("-", "•", "*", "#"))]

    # Get job keywords
    job_keywords = set()
    for j in jobs:
        if not j.error:
            words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', j.description[:2000])
            job_keywords.update(w for w in words if len(w) > 4)

    if bullets:
        suggestions.append(Suggestion(
            section="Experience",
            original=bullets[0].lstrip("-•* "),
            suggested=f"Spearheaded {bullets[0].lstrip('-•* ').lower()}, driving a 35% improvement in team efficiency and delivering measurable business impact",
            reason="Adding quantifiable metrics and strong action verbs makes achievements more compelling to hiring managers and ATS systems",
        ))

    if len(bullets) > 1:
        suggestions.append(Suggestion(
            section="Experience",
            original=bullets[1].lstrip("-•* "),
            suggested=f"Led cross-functional initiative to {bullets[1].lstrip('-•* ').lower()}, resulting in $500K+ annual savings and improved stakeholder satisfaction",
            reason="Quantifying business impact with dollar amounts demonstrates value creation and leadership capability",
        ))

    suggestions.append(Suggestion(
        section="Skills",
        original="Skills section needs enhancement",
        suggested="Categorize skills into Technical Skills, Soft Skills, and Tools/Technologies with proficiency levels",
        reason="Organized skill sections improve ATS matching rates by 40% and help recruiters quickly assess candidate fit",
    ))

    suggestions.append(Suggestion(
        section="Summary",
        original="Professional summary could be stronger",
        suggested="Results-driven professional with X+ years of experience delivering high-impact solutions. Proven track record of leading teams, optimizing processes, and driving revenue growth in fast-paced environments.",
        reason="A compelling summary immediately captures recruiter attention and should highlight your unique value proposition",
    ))

    if jobs and not jobs[0].error:
        suggestions.append(Suggestion(
            section="Keywords",
            original="Resume may be missing ATS keywords",
            suggested=f"Ensure resume includes relevant terms from the job posting: {', '.join(list(job_keywords)[:8]) if job_keywords else 'industry-specific terminology'}",
            reason="Matching 60%+ of job posting keywords significantly increases chances of passing ATS screening",
        ))

    return suggestions


def _demo_improve(resume_text: str, change_notes: Optional[str] = None) -> str:
    """Generate a mock improved resume."""
    lines = resume_text.strip().split("\n")
    improved_lines = []
    in_experience = False

    for line in lines:
        stripped = line.strip()

        if not stripped:
            improved_lines.append("")
            continue

        # Detect and enhance section headers
        if stripped.isupper() and len(stripped) > 2:
            in_experience = "EXPERIENCE" in stripped or "WORK" in stripped
            improved_lines.append(stripped)
            continue

        if stripped.startswith("#"):
            header = stripped.lstrip("#").strip()
            in_experience = "experience" in header.lower() or "work" in header.lower()
            improved_lines.append(stripped)
            continue

        # Enhance bullet points
        if stripped.startswith(("-", "•", "*")) and in_experience:
            bullet = stripped.lstrip("-•* ").strip()
            # Upgrade weak verbs
            replacements = {
                "worked on": "Spearheaded",
                "helped": "Facilitated",
                "did": "Executed",
                "made": "Developed",
                "was responsible for": "Led",
                "managed": "Directed",
                "created": "Architected",
                "used": "Leveraged",
                "improved": "Optimized",
            }
            for old, new in replacements.items():
                bullet = re.sub(rf'\b{old}\b', new, bullet, flags=re.IGNORECASE)

            if not re.search(r'\d+%|\$\d+|\d+ ', bullet):
                bullet = bullet.rstrip(".") + ", resulting in measurable improvements"

            improved_lines.append(f"• {bullet}")
        else:
            improved_lines.append(line)

    result = "\n".join(improved_lines)

    if change_notes:
        result += f"\n\n--- Applied changes based on: {change_notes} ---"

    return result


def _demo_cover_letter(resume_text: str, jobs: list[ScrapeResult]) -> str:
    """Generate a mock cover letter."""
    # Extract name from first line
    lines = resume_text.strip().split("\n")
    name = lines[0].strip().lstrip("#").strip() if lines else "Applicant"

    job_title = "the open position"
    company = "your company"
    for j in jobs:
        if not j.error:
            job_title = j.title if j.title != "Unknown Position" else job_title
            company = j.company if j.company != "Unknown Company" else company
            break

    return f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company}. With my extensive background and proven track record of delivering results, I am confident in my ability to make meaningful contributions to your team.

Throughout my career, I have consistently demonstrated the ability to drive innovation, lead cross-functional teams, and deliver projects that exceed expectations. My combination of technical expertise and strategic thinking has enabled me to create value in every role I have held.

What excites me most about this opportunity at {company} is the chance to bring my skills to a dynamic and forward-thinking organization. I am particularly drawn to your company's commitment to excellence and innovation, which aligns perfectly with my professional values and career aspirations.

I am eager to discuss how my experience and enthusiasm can contribute to {company}'s continued success. Thank you for considering my application. I look forward to the opportunity to speak with you.

Best regards,
{name}"""


# ─────────────────────────────────────────────
# Real OpenAI engine prompts
# ─────────────────────────────────────────────

_SUGGEST_SYSTEM = textwrap.dedent("""\
    You are an expert career coach and resume consultant.
    Given a candidate's resume and a job posting, produce a JSON array of
    concrete, actionable suggestions to tailor the resume for the role.
    Each object must have keys: section, original, suggested, reason.
    Only return valid JSON – no markdown fences.
""")

_IMPROVE_SYSTEM = textwrap.dedent("""\
    You are a professional resume writer.
    Given the original resume and a list of suggestions,
    produce an improved, ATS-friendly resume in clean plain text (with
    clear section headers). Keep facts truthful – enhance wording only.
    Return ONLY the resume text, nothing else.
""")

_COVER_SYSTEM = textwrap.dedent("""\
    You are a professional cover letter writer.
    Given a resume and job posting, write a compelling, concise cover letter
    (max 400 words). Be personable yet professional.
    Return ONLY the cover letter text.
""")

_IMPROVE_STANDALONE_SYSTEM = textwrap.dedent("""\
    You are a professional resume writer and career coach.
    Given the original resume and optional user instructions,
    improve the resume: fix formatting, enhance bullet points,
    add quantifiable achievements where possible, improve action verbs,
    and make it more ATS-friendly.
    Return ONLY the improved resume text, nothing else.
""")


def _real_suggest(resume_text: str, jobs: list[ScrapeResult]) -> list[Suggestion]:
    job_block = "\n---\n".join(
        f"**{j.title} @ {j.company}**\n{j.description[:3000]}" for j in jobs if not j.error
    )
    prompt = f"## Resume\n{resume_text}\n\n## Job Postings\n{job_block}"
    raw = _chat(_SUGGEST_SYSTEM, prompt)
    try:
        data = json.loads(raw)
        return [Suggestion(**s) for s in data]
    except Exception:
        m = re.search(r"\[.*\]", raw, re.S)
        if m:
            return [Suggestion(**s) for s in json.loads(m.group())]
        return []


def _real_improve(resume_text: str, suggestions: list[Suggestion], change_notes: Optional[str] = None) -> str:
    sug_text = "\n".join(
        f"- [{s.section}] Change '{s.original}' → '{s.suggested}' ({s.reason})"
        for s in suggestions
    )
    extra = f"\n\nAdditional user instructions:\n{change_notes}" if change_notes else ""
    prompt = f"## Original Resume\n{resume_text}\n\n## Suggestions\n{sug_text}{extra}"
    return _chat(_IMPROVE_SYSTEM, prompt)


def _real_cover_letter(resume_text: str, jobs: list[ScrapeResult]) -> str:
    job_block = "\n---\n".join(
        f"**{j.title} @ {j.company}**\n{j.description[:2000]}" for j in jobs if not j.error
    )
    prompt = f"## Resume\n{resume_text}\n\n## Job Postings\n{job_block}"
    return _chat(_COVER_SYSTEM, prompt)


def _real_improve_standalone(resume_text: str, change_notes: Optional[str] = None) -> str:
    extra = f"\n\nUser instructions:\n{change_notes}" if change_notes else ""
    prompt = f"## Original Resume\n{resume_text}{extra}"
    return _chat(_IMPROVE_STANDALONE_SYSTEM, prompt)


# ─────────────────────────────────────────────
# Orchestrator
# ─────────────────────────────────────────────

def run_engine(
    resume_text: str,
    jobs: list[ScrapeResult],
    change_notes: Optional[str] = None,
    flow: str = "apply",
) -> EngineResult:
    """Full pipeline: suggest → improve → cover letter.
    Uses demo engine if no OpenAI key configured."""

    if DEMO_MODE:
        if flow == "improve":
            improved = _demo_improve(resume_text, change_notes)
            return EngineResult(
                suggestions=[],
                improved_resume_text=improved,
                cover_letter_text="",
            )
        suggestions = _demo_suggestions(resume_text, jobs)
        improved = _demo_improve(resume_text, change_notes)
        cover = _demo_cover_letter(resume_text, jobs)
        return EngineResult(
            suggestions=suggestions,
            improved_resume_text=improved,
            cover_letter_text=cover,
        )

    # Real OpenAI mode
    if flow == "improve":
        improved = _real_improve_standalone(resume_text, change_notes)
        return EngineResult(
            suggestions=[],
            improved_resume_text=improved,
            cover_letter_text="",
        )

    suggestions = _real_suggest(resume_text, jobs)
    improved = _real_improve(resume_text, suggestions, change_notes)
    cover = _real_cover_letter(improved, jobs)
    return EngineResult(
        suggestions=suggestions,
        improved_resume_text=improved,
        cover_letter_text=cover,
    )
