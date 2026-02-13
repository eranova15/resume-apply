"""
Job Scraper Module
Scrapes job listings from URLs and extracts job requirements
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
import re


class JobScraper:
    """Scrapes job postings and extracts relevant information"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape(self, url):
        """
        Scrape a job posting URL and extract information
        
        Args:
            url: Job posting URL
            
        Returns:
            dict: Job data including title, description, requirements, etc.
        """
        try:
            print(f"  Fetching job listing from: {url}")
            
            # Make request
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract job data
            job_data = {
                'url': url,
                'title': self._extract_title(soup),
                'company': self._extract_company(soup),
                'location': self._extract_location(soup),
                'description': self._extract_description(soup),
                'requirements': self._extract_requirements(soup),
                'raw_html': ''  # Removed expensive soup conversion
            }
            
            return job_data
            
        except requests.RequestException as e:
            print(f"  Warning: Could not fetch URL ({e})")
            # Return mock data for demonstration
            return self._get_mock_job_data(url)
        except Exception as e:
            print(f"  Warning: Error parsing job data ({e})")
            return self._get_mock_job_data(url)
    
    def _extract_title(self, soup):
        """Extract job title from page"""
        # Try common selectors
        selectors = [
            'h1.job-title',
            'h1.jobTitle',
            'h1[class*="title"]',
            'h1',
            'title'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text().strip()
        
        return "Unknown Position"
    
    def _extract_company(self, soup):
        """Extract company name from page"""
        selectors = [
            '[class*="company"]',
            '[class*="employer"]',
            'span.companyName'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text().strip()
        
        return "Unknown Company"
    
    def _extract_location(self, soup):
        """Extract job location from page"""
        selectors = [
            '[class*="location"]',
            '[class*="jobLocation"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text().strip()
        
        return "Unknown Location"
    
    def _extract_description(self, soup):
        """Extract full job description"""
        selectors = [
            '[class*="description"]',
            '[class*="jobDescription"]',
            '[id*="description"]',
            'article',
            'main'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                # Get text and clean it
                text = element.get_text(separator='\n').strip()
                return text
        
        # Fallback: get all text from body
        body = soup.find('body')
        if body:
            return body.get_text(separator='\n').strip()
        
        return ""
    
    def _extract_requirements(self, soup):
        """Extract specific requirements from job posting"""
        description = self._extract_description(soup)
        
        requirements = {
            'technical_skills': self._find_technical_skills(description),
            'experience_years': self._find_experience_years(description),
            'education': self._find_education_requirements(description),
            'certifications': self._find_certifications(description),
            'key_requirements': self._find_key_requirements(description)
        }
        
        return requirements
    
    def _find_technical_skills(self, text):
        """Extract technical skills mentioned"""
        # Common technical skills to look for
        common_skills = [
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 'rust',
            'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring',
            'sql', 'nosql', 'mongodb', 'postgresql', 'mysql',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes',
            'git', 'jenkins', 'ci/cd', 'agile', 'scrum',
            'machine learning', 'deep learning', 'ai', 'nlp',
            'rest api', 'graphql', 'microservices'
        ]
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in common_skills:
            if skill in text_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def _find_experience_years(self, text):
        """Extract years of experience required"""
        # Look for patterns like "5+ years", "3-5 years", etc.
        patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(\d+)-(\d+)\s*(?:years?|yrs?)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return match.group()
        
        return None
    
    def _find_education_requirements(self, text):
        """Extract education requirements"""
        education_keywords = [
            "bachelor's", "master's", "phd", "doctorate",
            "bs", "ms", "ba", "ma", "mba",
            "computer science", "engineering", "related field"
        ]
        
        text_lower = text.lower()
        found_education = []
        
        for keyword in education_keywords:
            if keyword in text_lower:
                found_education.append(keyword)
        
        return found_education
    
    def _find_certifications(self, text):
        """Extract certification requirements"""
        cert_keywords = [
            "aws certified", "azure certified", "gcp certified",
            "pmp", "scrum master", "cissp", "ceh",
            "certified"
        ]
        
        text_lower = text.lower()
        found_certs = []
        
        for cert in cert_keywords:
            if cert in text_lower:
                found_certs.append(cert)
        
        return found_certs
    
    def _find_key_requirements(self, text):
        """Extract key requirements from the description"""
        # Look for sections with "requirements", "qualifications", etc.
        requirements = []
        lines = text.split('\n')
        
        in_requirements = False
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if we're entering a requirements section
            if any(keyword in line_lower for keyword in 
                   ['requirements', 'qualifications', 'what we need', 'must have']):
                in_requirements = True
                continue
            
            # Check if we're leaving requirements section
            if in_requirements and any(keyword in line_lower for keyword in 
                   ['benefits', 'about us', 'about the company', 'perks', 'what we offer']):
                in_requirements = False
                continue
            
            # Collect requirement lines (often start with bullet points)
            if in_requirements and line.strip():
                # Clean up bullet points
                cleaned_line = re.sub(r'^[•\-\*\+]\s*', '', line.strip())
                if cleaned_line and len(cleaned_line) > 10:
                    requirements.append(cleaned_line)
        
        return requirements[:15]  # Return top 15 requirements
    
    def _get_mock_job_data(self, url):
        """Return mock job data when scraping fails"""
        return {
            'url': url,
            'title': 'Software Engineer',
            'company': 'Tech Company',
            'location': 'Remote',
            'description': '''
We are seeking a talented Software Engineer to join our team.

Requirements:
- 3+ years of experience in software development
- Strong proficiency in Python, JavaScript, or similar languages
- Experience with web frameworks (Django, React, etc.)
- Knowledge of databases (SQL and NoSQL)
- Excellent problem-solving skills
- BS in Computer Science or related field

Responsibilities:
- Design and develop scalable applications
- Collaborate with cross-functional teams
- Write clean, maintainable code
- Participate in code reviews
            ''',
            'requirements': {
                'technical_skills': ['python', 'javascript', 'react', 'django', 'sql', 'nosql'],
                'experience_years': '3+ years',
                'education': ["bachelor's", 'computer science'],
                'certifications': [],
                'key_requirements': [
                    '3+ years of experience in software development',
                    'Strong proficiency in Python, JavaScript, or similar languages',
                    'Experience with web frameworks (Django, React, etc.)',
                    'Knowledge of databases (SQL and NoSQL)',
                    'Excellent problem-solving skills',
                    "BS in Computer Science or related field"
                ]
            },
            'raw_html': ''
        }
