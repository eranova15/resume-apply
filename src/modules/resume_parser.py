"""
Resume Parser Module
Parses resume files (PDF, DOCX) and extracts structured data
"""

import os
from pathlib import Path
import pdfplumber
from docx import Document
import json


class ResumeParser:
    """Parses resume files and extracts structured information"""
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx', '.txt']
    
    def parse(self, file_path):
        """
        Parse a resume file and return structured data
        
        Args:
            file_path: Path to resume file
            
        Returns:
            dict: Structured resume data
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Resume file not found: {file_path}")
        
        ext = file_path.suffix.lower()
        
        if ext not in self.supported_formats:
            raise ValueError(
                f"Unsupported file format: {ext}. "
                f"Supported formats: {', '.join(self.supported_formats)}"
            )
        
        # Extract text based on file type
        if ext == '.pdf':
            text = self._parse_pdf(file_path)
        elif ext == '.docx':
            text = self._parse_docx(file_path)
        elif ext == '.txt':
            text = self._parse_txt(file_path)
        else:
            raise ValueError(f"Unsupported format: {ext}")
        
        # Structure the data
        resume_data = self._structure_data(text, file_path)
        
        return resume_data
    
    def _parse_pdf(self, file_path):
        """Extract text from PDF file"""
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    
    def _parse_docx(self, file_path):
        """Extract text from DOCX file"""
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    
    def _parse_txt(self, file_path):
        """Extract text from TXT file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        return text
    
    def _structure_data(self, text, file_path):
        """
        Structure the extracted text into sections
        
        This is a simple implementation that can be enhanced with NLP
        """
        lines = text.split('\n')
        
        # Basic structure - can be enhanced with better parsing
        resume_data = {
            'original_file': str(file_path),
            'raw_text': text,
            'sections': self._identify_sections(text),
            'contact_info': self._extract_contact_info(lines),
            'skills': self._extract_skills(text),
            'experience': self._extract_experience(text),
            'education': self._extract_education(text),
        }
        
        return resume_data
    
    def _identify_sections(self, text):
        """Identify major sections in the resume"""
        common_headers = [
            'summary', 'objective', 'experience', 'education', 
            'skills', 'projects', 'certifications', 'awards',
            'work experience', 'professional experience'
        ]
        
        sections = {}
        lines = text.lower().split('\n')
        current_section = None
        
        for i, line in enumerate(lines):
            line_clean = line.strip()
            for header in common_headers:
                if header in line_clean and len(line_clean) < 50:
                    current_section = header
                    sections[header] = {'start': i, 'content': []}
                    break
            
            if current_section and line_clean:
                sections[current_section]['content'].append(text.split('\n')[i])
        
        return sections
    
    def _extract_contact_info(self, lines):
        """Extract contact information (basic implementation)"""
        import re
        
        contact = {
            'email': None,
            'phone': None,
            'linkedin': None,
            'github': None
        }
        
        # Search first 10 lines for contact info
        for line in lines[:10]:
            # Email
            email_match = re.search(r'\b[\w.-]+@[\w.-]+\.\w+\b', line)
            if email_match and not contact['email']:
                contact['email'] = email_match.group()
            
            # Phone
            phone_match = re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', line)
            if phone_match and not contact['phone']:
                contact['phone'] = phone_match.group()
            
            # LinkedIn
            if 'linkedin.com' in line.lower() and not contact['linkedin']:
                contact['linkedin'] = line.strip()
            
            # GitHub
            if 'github.com' in line.lower() and not contact['github']:
                contact['github'] = line.strip()
        
        return contact
    
    def _extract_skills(self, text):
        """Extract skills section (basic implementation)"""
        skills = []
        text_lower = text.lower()
        
        # Find skills section
        if 'skills' in text_lower:
            lines = text.split('\n')
            in_skills = False
            
            for line in lines:
                if 'skills' in line.lower() and len(line.strip()) < 50:
                    in_skills = True
                    continue
                
                if in_skills:
                    # Stop at next section
                    if any(header in line.lower() for header in 
                           ['experience', 'education', 'projects']) and len(line.strip()) < 50:
                        break
                    
                    if line.strip():
                        skills.append(line.strip())
        
        return skills
    
    def _extract_experience(self, text):
        """Extract experience section (basic implementation)"""
        experience = []
        text_lower = text.lower()
        
        if any(exp in text_lower for exp in ['experience', 'work history']):
            lines = text.split('\n')
            in_experience = False
            current_entry = []
            
            for line in lines:
                if any(exp in line.lower() for exp in ['experience', 'work history']) \
                   and len(line.strip()) < 50:
                    in_experience = True
                    continue
                
                if in_experience:
                    # Stop at next section
                    if any(header in line.lower() for header in 
                           ['education', 'skills', 'projects', 'certifications']) \
                       and len(line.strip()) < 50:
                        break
                    
                    if line.strip():
                        current_entry.append(line.strip())
        
            if current_entry:
                experience.append('\n'.join(current_entry))
        
        return experience
    
    def _extract_education(self, text):
        """Extract education section (basic implementation)"""
        education = []
        text_lower = text.lower()
        
        if 'education' in text_lower:
            lines = text.split('\n')
            in_education = False
            
            for line in lines:
                if 'education' in line.lower() and len(line.strip()) < 50:
                    in_education = True
                    continue
                
                if in_education:
                    # Stop at next section
                    if any(header in line.lower() for header in 
                           ['experience', 'skills', 'projects', 'certifications']) \
                       and len(line.strip()) < 50:
                        break
                    
                    if line.strip():
                        education.append(line.strip())
        
        return education
