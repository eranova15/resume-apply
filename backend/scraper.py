"""Job listing scraper – pulls text from common job-board URLs with robust fallbacks."""

from __future__ import annotations

import re
import time
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from models import ScrapeResult

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _extract_meta(soup: BeautifulSoup, name: str) -> str:
    for attr in ("name", "property"):
        tag = soup.find("meta", attrs={attr: re.compile(name, re.I)})
        if tag and tag.get("content"):
            return _clean(str(tag["content"]))
    return ""


def _detect_board(url: str) -> str:
    domain = urlparse(url).netloc.lower()
    for name in ("linkedin", "indeed", "glassdoor", "greenhouse", "lever", "workday"):
        if name in domain:
            return name
    return "generic"


def scrape_job(url: str) -> ScrapeResult:
    """Scrape a single job listing URL and return structured data."""
    try:
        session = requests.Session()
        session.headers.update(_HEADERS)
        resp = session.get(url, timeout=20, allow_redirects=True)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "iframe", "noscript"]):
            tag.decompose()

        title = ""
        company = ""

        # Title selectors (board-aware)
        title_selectors = [
            "h1", ".job-title", "[data-testid='jobTitle']", ".topcard__title",
            ".posting-headline h2", ".app-title", "[class*='job-title']", "[class*='jobTitle']",
        ]
        for sel in title_selectors:
            el = soup.select_one(sel)
            if el:
                title = _clean(el.get_text())
                break

        # Company selectors
        company_selectors = [
            ".company", "[data-testid='company']", ".topcard__org-name-link",
            ".employer-name", ".company-name", "[class*='company']",
        ]
        for sel in company_selectors:
            el = soup.select_one(sel)
            if el:
                company = _clean(el.get_text())
                break

        # Meta fallbacks
        if not title:
            title = _extract_meta(soup, "og:title") or _extract_meta(soup, "twitter:title")
        if not company:
            company = _extract_meta(soup, "og:site_name")

        # Split "Title - Company" patterns
        if title and not company:
            for sep in (" - ", " | ", " at "):
                if sep in title:
                    parts = title.rsplit(sep, 1)
                    title = parts[0].strip()
                    company = parts[1].strip()
                    break

        # Body text
        body_text = _clean(soup.get_text(separator="\n"))[:8000]

        # Requirements bullets
        bullets: list[str] = []
        for li in soup.select("ul li, ol li"):
            t = _clean(li.get_text())
            if 10 < len(t) < 300:
                bullets.append(t)

        return ScrapeResult(
            url=url,
            title=title or "Unknown Position",
            company=company or "Unknown Company",
            description=body_text,
            requirements=bullets[:30],
        )

    except requests.exceptions.Timeout:
        return ScrapeResult(url=url, error=f"Timeout: {url}")
    except requests.exceptions.ConnectionError:
        return ScrapeResult(url=url, error=f"Connection failed: {url}")
    except requests.exceptions.HTTPError as e:
        return ScrapeResult(url=url, error=f"HTTP {e.response.status_code}: {url}")
    except Exception as exc:
        return ScrapeResult(url=url, error=f"Error: {str(exc)[:200]}")


def scrape_jobs(urls: list[str]) -> list[ScrapeResult]:
    results = []
    for i, url in enumerate(urls):
        if i > 0:
            time.sleep(0.5)
        results.append(scrape_job(url.strip()))
    return results
