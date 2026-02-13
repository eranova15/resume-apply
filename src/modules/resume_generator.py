"""
Resume Generator Module
Generates PDF resumes from structured data
"""

from fpdf import FPDF
from pathlib import Path
import textwrap


class ResumeGenerator:
    """Generates PDF resumes from structured resume data"""
    
    def __init__(self):
        self.font_family = 'Arial'
        self.title_size = 16
        self.heading_size = 12
        self.body_size = 10
        self.margin = 10
    
    def generate(self, resume_data, output_path):
        """
        Generate a PDF resume from structured data
        
        Args:
            resume_data: Structured resume data
            output_path: Path where PDF should be saved
        """
        pdf = FPDF()
        pdf.add_page()
        pdf.set_margins(self.margin, self.margin, self.margin)
        
        # Add content
        self._add_header(pdf, resume_data)
        self._add_contact_info(pdf, resume_data)
        self._add_summary(pdf, resume_data)
        self._add_skills(pdf, resume_data)
        self._add_experience(pdf, resume_data)
        self._add_education(pdf, resume_data)
        
        # Add footer with generation info
        if resume_data.get('_updates'):
            self._add_updates_info(pdf, resume_data)
        
        # Save PDF
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        pdf.output(str(output_path))
        
        return str(output_path)
    
    def _add_header(self, pdf, resume_data):
        """Add name header"""
        # Try to extract name from contact or first line
        name = "Professional Resume"
        
        # Try to get name from first few lines
        raw_text = resume_data.get('raw_text', '')
        if raw_text:
            first_line = raw_text.split('\n')[0].strip()
            if len(first_line) < 50 and len(first_line) > 3:
                name = first_line
        
        pdf.set_font(self.font_family, 'B', self.title_size)
        pdf.cell(0, 10, name, ln=True, align='C')
        pdf.ln(2)
    
    def _add_contact_info(self, pdf, resume_data):
        """Add contact information"""
        contact = resume_data.get('contact_info', {})
        
        contact_parts = []
        if contact.get('email'):
            contact_parts.append(contact['email'])
        if contact.get('phone'):
            contact_parts.append(contact['phone'])
        if contact.get('linkedin'):
            contact_parts.append(contact['linkedin'])
        
        if contact_parts:
            pdf.set_font(self.font_family, '', self.body_size)
            contact_text = ' | '.join(contact_parts)
            pdf.cell(0, 5, contact_text, ln=True, align='C')
            pdf.ln(5)
    
    def _add_summary(self, pdf, resume_data):
        """Add professional summary"""
        sections = resume_data.get('sections', {})
        
        if 'summary' in sections or 'objective' in sections:
            section = sections.get('summary') or sections.get('objective')
            content = section.get('content', [])
            
            if content:
                pdf.set_font(self.font_family, 'B', self.heading_size)
                pdf.cell(0, 8, 'PROFESSIONAL SUMMARY', ln=True)
                pdf.line(self.margin, pdf.get_y(), 200, pdf.get_y())
                pdf.ln(2)
                
                pdf.set_font(self.font_family, '', self.body_size)
                for line in content[:3]:  # Limit to first 3 lines
                    if line.strip():
                        self._add_wrapped_text(pdf, line.strip())
                
                pdf.ln(3)
    
    def _add_skills(self, pdf, resume_data):
        """Add skills section"""
        skills = resume_data.get('skills', [])
        
        if skills:
            pdf.set_font(self.font_family, 'B', self.heading_size)
            pdf.cell(0, 8, 'SKILLS', ln=True)
            pdf.line(self.margin, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(2)
            
            pdf.set_font(self.font_family, '', self.body_size)
            
            # Format skills in bullet points or comma-separated
            skills_text = ', '.join(skills[:20])  # Limit to 20 skills
            self._add_wrapped_text(pdf, skills_text)
            
            # Show added skills if any
            updates = resume_data.get('_updates', {})
            if updates.get('skills_added'):
                pdf.set_font(self.font_family, 'I', self.body_size - 1)
                added_text = f"(Added: {', '.join(updates['skills_added'])})"
                self._add_wrapped_text(pdf, added_text)
            
            pdf.ln(3)
    
    def _add_experience(self, pdf, resume_data):
        """Add experience section"""
        experience = resume_data.get('experience', [])
        sections = resume_data.get('sections', {})
        
        # Try to get from sections first
        if 'experience' in sections or 'work experience' in sections:
            section = sections.get('experience') or sections.get('work experience')
            content = section.get('content', [])
            
            if content:
                pdf.set_font(self.font_family, 'B', self.heading_size)
                pdf.cell(0, 8, 'EXPERIENCE', ln=True)
                pdf.line(self.margin, pdf.get_y(), 200, pdf.get_y())
                pdf.ln(2)
                
                pdf.set_font(self.font_family, '', self.body_size)
                
                for line in content[:15]:  # Limit experience lines
                    if line.strip():
                        self._add_wrapped_text(pdf, line.strip())
                        pdf.ln(1)
                
                pdf.ln(2)
        elif experience:
            pdf.set_font(self.font_family, 'B', self.heading_size)
            pdf.cell(0, 8, 'EXPERIENCE', ln=True)
            pdf.line(self.margin, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(2)
            
            pdf.set_font(self.font_family, '', self.body_size)
            for exp in experience[:3]:  # Limit to 3 experiences
                self._add_wrapped_text(pdf, exp)
                pdf.ln(2)
            
            pdf.ln(2)
    
    def _add_education(self, pdf, resume_data):
        """Add education section"""
        education = resume_data.get('education', [])
        
        if education:
            pdf.set_font(self.font_family, 'B', self.heading_size)
            pdf.cell(0, 8, 'EDUCATION', ln=True)
            pdf.line(self.margin, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(2)
            
            pdf.set_font(self.font_family, '', self.body_size)
            
            for edu in education[:5]:  # Limit to 5 education items
                if edu.strip():
                    self._add_wrapped_text(pdf, edu.strip())
                    pdf.ln(1)
            
            pdf.ln(2)
    
    def _add_updates_info(self, pdf, resume_data):
        """Add information about what was updated"""
        updates = resume_data.get('_updates', {})
        
        if any(updates.values()):
            # Add on new page if needed or at bottom
            if pdf.get_y() > 250:
                pdf.add_page()
            
            pdf.ln(5)
            pdf.set_font(self.font_family, 'I', 8)
            pdf.cell(0, 5, "This resume was optimized for the job posting", ln=True, align='C')
    
    def _add_wrapped_text(self, pdf, text, indent=0):
        """Add text with word wrapping"""
        # Calculate effective width
        effective_width = 190 - (indent * 2)
        
        # Get current font info
        font_size = pdf.font_size_pt
        
        # Estimate characters per line (rough approximation)
        chars_per_line = int(effective_width / (font_size * 0.5))
        
        # Wrap text
        lines = textwrap.wrap(text, width=chars_per_line)
        
        for line in lines:
            if indent > 0:
                pdf.cell(indent)
            pdf.cell(effective_width, 5, line, ln=True)
