"""
Cover Letter Generator Module
Generates personalized cover letters based on resume and job posting
"""

from fpdf import FPDF
from pathlib import Path
import textwrap
from datetime import datetime


class CoverLetterGenerator:
    """Generates PDF cover letters"""
    
    def __init__(self):
        self.font_family = 'Arial'
        self.title_size = 14
        self.heading_size = 12
        self.body_size = 11
        self.margin = 15
    
    def generate(self, resume_data, job_data, output_path):
        """
        Generate a PDF cover letter
        
        Args:
            resume_data: Structured resume data
            job_data: Job posting data
            output_path: Path where PDF should be saved
        """
        pdf = FPDF()
        pdf.add_page()
        pdf.set_margins(self.margin, self.margin, self.margin)
        
        # Build cover letter content
        self._add_header(pdf, resume_data)
        self._add_date(pdf)
        self._add_recipient(pdf, job_data)
        self._add_body(pdf, resume_data, job_data)
        self._add_closing(pdf, resume_data)
        
        # Save PDF
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        pdf.output(str(output_path))
        
        return str(output_path)
    
    def _add_header(self, pdf, resume_data):
        """Add sender's contact information"""
        contact = resume_data.get('contact_info', {})
        
        # Try to get name
        name = "Your Name"
        raw_text = resume_data.get('raw_text', '')
        if raw_text:
            first_line = raw_text.split('\n')[0].strip()
            if len(first_line) < 50 and len(first_line) > 3:
                name = first_line
        
        pdf.set_font(self.font_family, 'B', self.title_size)
        pdf.cell(0, 8, name, ln=True)
        
        # Add contact info
        pdf.set_font(self.font_family, '', self.body_size)
        if contact.get('email'):
            pdf.cell(0, 5, contact['email'], ln=True)
        if contact.get('phone'):
            pdf.cell(0, 5, contact['phone'], ln=True)
        
        pdf.ln(5)
    
    def _add_date(self, pdf):
        """Add current date"""
        pdf.set_font(self.font_family, '', self.body_size)
        date_str = datetime.now().strftime("%B %d, %Y")
        pdf.cell(0, 5, date_str, ln=True)
        pdf.ln(5)
    
    def _add_recipient(self, pdf, job_data):
        """Add recipient information"""
        pdf.set_font(self.font_family, '', self.body_size)
        
        company = job_data.get('company', 'Hiring Manager')
        title = job_data.get('title', 'Position')
        
        pdf.cell(0, 5, "Hiring Manager", ln=True)
        pdf.cell(0, 5, company, ln=True)
        pdf.ln(5)
        
        # Salutation
        pdf.cell(0, 5, "Dear Hiring Manager,", ln=True)
        pdf.ln(3)
    
    def _add_body(self, pdf, resume_data, job_data):
        """Add cover letter body"""
        pdf.set_font(self.font_family, '', self.body_size)
        
        # Extract info
        title = job_data.get('title', 'position')
        company = job_data.get('company', 'your company')
        skills = resume_data.get('skills', [])
        
        # Paragraph 1: Introduction
        intro = f"I am writing to express my strong interest in the {title} position at {company}. "
        intro += "With my background and skills, I believe I would be an excellent fit for this role."
        self._add_paragraph(pdf, intro)
        
        # Paragraph 2: Skills and qualifications
        skills_text = "My technical expertise includes "
        if skills:
            skills_list = ', '.join(skills[:5])
            skills_text += f"{skills_list}, "
        skills_text += "which aligns well with the requirements outlined in the job posting. "
        skills_text += "I am confident that my experience and technical capabilities will enable me to contribute effectively to your team."
        self._add_paragraph(pdf, skills_text)
        
        # Paragraph 3: Experience and achievements
        exp_text = "Throughout my career, I have successfully delivered projects and collaborated with cross-functional teams. "
        exp_text += "I am passionate about technology and continuously strive to improve my skills and stay current with industry trends. "
        exp_text += f"I am particularly excited about the opportunity to contribute to {company}'s mission."
        self._add_paragraph(pdf, exp_text)
        
        # Paragraph 4: Closing
        closing = "I would welcome the opportunity to discuss how my skills and experiences align with your needs. "
        closing += "Thank you for considering my application. I look forward to hearing from you."
        self._add_paragraph(pdf, closing)
    
    def _add_closing(self, pdf, resume_data):
        """Add closing and signature"""
        pdf.ln(3)
        pdf.set_font(self.font_family, '', self.body_size)
        pdf.cell(0, 5, "Sincerely,", ln=True)
        pdf.ln(10)
        
        # Try to get name
        name = "Your Name"
        raw_text = resume_data.get('raw_text', '')
        if raw_text:
            first_line = raw_text.split('\n')[0].strip()
            if len(first_line) < 50 and len(first_line) > 3:
                name = first_line
        
        pdf.set_font(self.font_family, 'B', self.body_size)
        pdf.cell(0, 5, name, ln=True)
    
    def _add_paragraph(self, pdf, text):
        """Add a paragraph with proper wrapping"""
        # Calculate effective width
        effective_width = 190 - (self.margin * 2)
        
        # Estimate characters per line
        chars_per_line = int(effective_width / (self.body_size * 0.45))
        
        # Wrap text
        lines = textwrap.wrap(text, width=chars_per_line)
        
        for line in lines:
            pdf.cell(0, 6, line, ln=True)
        
        pdf.ln(3)
