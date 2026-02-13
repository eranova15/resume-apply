"""
Suggestion Engine Module
Analyzes resume against job requirements and generates suggestions
"""

import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()


class SuggestionEngine:
    """
    Generates suggestions to improve resume based on job requirements
    Can use AI APIs or rule-based approach
    """
    
    def __init__(self, use_ai=False):
        """
        Initialize the suggestion engine
        
        Args:
            use_ai: Whether to use AI API (requires API key) or rule-based approach
        """
        self.use_ai = use_ai
        self.ai_client = None
        
        if use_ai:
            self._init_ai_client()
    
    def _init_ai_client(self):
        """Initialize AI client (OpenAI or Anthropic)"""
        openai_key = os.getenv('OPENAI_API_KEY')
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        
        if openai_key and openai_key != 'your_openai_api_key_here':
            try:
                from openai import OpenAI
                self.ai_client = OpenAI(api_key=openai_key)
                self.ai_type = 'openai'
            except ImportError:
                print("Warning: OpenAI library not installed")
        elif anthropic_key and anthropic_key != 'your_anthropic_api_key_here':
            try:
                from anthropic import Anthropic
                self.ai_client = Anthropic(api_key=anthropic_key)
                self.ai_type = 'anthropic'
            except ImportError:
                print("Warning: Anthropic library not installed")
        else:
            print("No AI API key found, using rule-based suggestions")
            self.use_ai = False
    
    def generate_suggestions(self, resume_data, job_data, edit_requests=None):
        """
        Generate suggestions to improve resume for the job
        
        Args:
            resume_data: Parsed resume data
            job_data: Scraped job data
            edit_requests: Optional user edit requests
            
        Returns:
            list: List of suggestions
        """
        if self.use_ai and self.ai_client:
            return self._generate_ai_suggestions(resume_data, job_data, edit_requests)
        else:
            return self._generate_rule_based_suggestions(resume_data, job_data, edit_requests)
    
    def _generate_ai_suggestions(self, resume_data, job_data, edit_requests):
        """Generate suggestions using AI"""
        prompt = self._build_ai_prompt(resume_data, job_data, edit_requests)
        
        try:
            if self.ai_type == 'openai':
                response = self.ai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a professional resume writer and career coach."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                suggestions_text = response.choices[0].message.content
            elif self.ai_type == 'anthropic':
                response = self.ai_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=2000,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                suggestions_text = response.content[0].text
            
            # Parse AI response into structured suggestions
            return self._parse_ai_suggestions(suggestions_text)
            
        except Exception as e:
            print(f"  Warning: AI suggestion generation failed ({e})")
            print("  Falling back to rule-based suggestions")
            return self._generate_rule_based_suggestions(resume_data, job_data, edit_requests)
    
    def _build_ai_prompt(self, resume_data, job_data, edit_requests):
        """Build prompt for AI"""
        prompt = f"""Analyze this resume against the job posting and provide specific suggestions to improve it.

Job Title: {job_data.get('title', 'N/A')}
Company: {job_data.get('company', 'N/A')}

Job Requirements:
{json.dumps(job_data.get('requirements', {}), indent=2)}

Resume Summary:
- Skills: {', '.join(resume_data.get('skills', [])[:10])}
- Experience: {len(resume_data.get('experience', []))} entries
- Education: {', '.join(resume_data.get('education', [])[:3])}

Job Description Preview:
{job_data.get('description', '')[:800]}

Resume Preview:
{resume_data.get('raw_text', '')[:800]}

"""
        
        if edit_requests:
            prompt += f"\nUser's specific requests:\n{edit_requests}\n"
        
        prompt += """
Please provide 5-8 specific, actionable suggestions to improve this resume for this job. 
Format each suggestion as:
CATEGORY | PRIORITY | SUGGESTION

Categories: SKILLS, EXPERIENCE, EDUCATION, KEYWORDS, FORMAT, SUMMARY
Priority: HIGH, MEDIUM, LOW
"""
        
        return prompt
    
    def _parse_ai_suggestions(self, suggestions_text):
        """Parse AI response into structured suggestions"""
        suggestions = []
        lines = suggestions_text.split('\n')
        
        for line in lines:
            if '|' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 3:
                    suggestions.append({
                        'category': parts[0],
                        'priority': parts[1],
                        'description': parts[2],
                        'applied': False
                    })
        
        # If parsing failed, create generic suggestions
        if not suggestions:
            suggestions = [{
                'category': 'GENERAL',
                'priority': 'HIGH',
                'description': suggestions_text[:200],
                'applied': False
            }]
        
        return suggestions
    
    def _generate_rule_based_suggestions(self, resume_data, job_data, edit_requests):
        """Generate suggestions using rule-based approach"""
        suggestions = []
        
        # Extract data
        resume_skills = [s.lower() for s in resume_data.get('skills', [])]
        resume_text = resume_data.get('raw_text', '').lower()
        job_skills = job_data.get('requirements', {}).get('technical_skills', [])
        job_requirements = job_data.get('requirements', {}).get('key_requirements', [])
        
        # 1. Check for missing skills
        missing_skills = []
        for skill in job_skills:
            skill_lower = skill.lower()
            if skill_lower not in resume_text:
                missing_skills.append(skill)
        
        if missing_skills:
            suggestions.append({
                'category': 'SKILLS',
                'priority': 'HIGH',
                'description': f"Add these relevant skills if you have them: {', '.join(missing_skills[:5])}",
                'applied': False,
                'action': 'add_skills',
                'data': missing_skills[:5]
            })
        
        # 2. Check for keyword optimization
        important_keywords = self._extract_keywords(job_requirements)
        missing_keywords = []
        for keyword in important_keywords:
            if keyword.lower() not in resume_text:
                missing_keywords.append(keyword)
        
        if missing_keywords:
            suggestions.append({
                'category': 'KEYWORDS',
                'priority': 'HIGH',
                'description': f"Consider incorporating these keywords: {', '.join(missing_keywords[:5])}",
                'applied': False,
                'action': 'add_keywords',
                'data': missing_keywords[:5]
            })
        
        # 3. Experience alignment
        exp_years = job_data.get('requirements', {}).get('experience_years')
        if exp_years:
            suggestions.append({
                'category': 'EXPERIENCE',
                'priority': 'MEDIUM',
                'description': f"Ensure your experience section highlights that you meet the '{exp_years}' requirement",
                'applied': False,
                'action': 'highlight_experience',
                'data': exp_years
            })
        
        # 4. Summary/Objective
        if 'summary' not in resume_data.get('sections', {}):
            suggestions.append({
                'category': 'SUMMARY',
                'priority': 'HIGH',
                'description': f"Add a professional summary tailored to this {job_data.get('title', 'position')} role",
                'applied': False,
                'action': 'add_summary',
                'data': {
                    'title': job_data.get('title'),
                    'company': job_data.get('company')
                }
            })
        
        # 5. Education alignment
        job_education = job_data.get('requirements', {}).get('education', [])
        if job_education:
            suggestions.append({
                'category': 'EDUCATION',
                'priority': 'MEDIUM',
                'description': f"Ensure your education section is prominent (job requires: {', '.join(job_education[:2])})",
                'applied': False,
                'action': 'highlight_education',
                'data': job_education
            })
        
        # 6. Action verbs
        suggestions.append({
            'category': 'FORMAT',
            'priority': 'LOW',
            'description': "Use strong action verbs in experience descriptions (e.g., 'Developed', 'Led', 'Implemented')",
            'applied': False,
            'action': 'improve_verbs',
            'data': ['Developed', 'Led', 'Implemented', 'Designed', 'Optimized', 'Managed']
        })
        
        # 7. Quantify achievements
        suggestions.append({
            'category': 'EXPERIENCE',
            'priority': 'MEDIUM',
            'description': "Add quantifiable metrics to your achievements (e.g., '30% improvement', '50+ users')",
            'applied': False,
            'action': 'add_metrics',
            'data': None
            })
        
        # 8. Certifications
        job_certs = job_data.get('requirements', {}).get('certifications', [])
        if job_certs:
            suggestions.append({
                'category': 'EDUCATION',
                'priority': 'MEDIUM',
                'description': f"Highlight any certifications, especially: {', '.join(job_certs[:3])}",
                'applied': False,
                'action': 'highlight_certifications',
                'data': job_certs
            })
        
        # Handle edit requests
        if edit_requests:
            suggestions.append({
                'category': 'CUSTOM',
                'priority': 'HIGH',
                'description': f"Address user's feedback: {edit_requests[:100]}",
                'applied': False,
                'action': 'custom_edit',
                'data': edit_requests
            })
        
        return suggestions
    
    def _extract_keywords(self, requirements):
        """Extract important keywords from requirements"""
        keywords = []
        
        for req in requirements:
            # Extract multi-word important terms
            words = req.split()
            for i in range(len(words)):
                # Extract 2-3 word phrases that might be important
                if i < len(words) - 1:
                    two_word = f"{words[i]} {words[i+1]}"
                    if len(two_word) > 8 and not any(c in two_word for c in [',', '.', '(']):
                        keywords.append(two_word)
        
        return list(set(keywords))[:10]
    
    def apply_suggestions(self, resume_data, suggestions):
        """
        Apply approved suggestions to resume data
        
        Args:
            resume_data: Original resume data
            suggestions: List of suggestions to apply
            
        Returns:
            dict: Updated resume data
        """
        import copy
        updated_data = copy.deepcopy(resume_data)
        
        # Track what was added
        updates = {
            'skills_added': [],
            'keywords_added': [],
            'sections_modified': []
        }
        
        for suggestion in suggestions:
            if not suggestion.get('applied', False):
                continue
            
            action = suggestion.get('action')
            data = suggestion.get('data')
            
            if action == 'add_skills' and data:
                # Add skills to skills section
                current_skills = updated_data.get('skills', [])
                for skill in data:
                    if skill not in [s.lower() for s in current_skills]:
                        current_skills.append(skill.title())
                        updates['skills_added'].append(skill)
                updated_data['skills'] = current_skills
            
            elif action == 'add_keywords' and data:
                # Add to keywords tracking
                updates['keywords_added'].extend(data)
            
            elif action == 'add_summary' and data:
                # Add professional summary
                title = data.get('title', 'Software Engineer')
                company = data.get('company', 'target company')
                summary = f"Experienced professional seeking {title} position at {company}"
                
                sections = updated_data.get('sections', {})
                sections['summary'] = {
                    'start': 0,
                    'content': [summary]
                }
                updated_data['sections'] = sections
                updates['sections_modified'].append('summary')
        
        # Add metadata about updates
        updated_data['_updates'] = updates
        updated_data['_suggestions_applied'] = [
            s for s in suggestions if s.get('applied', False)
        ]
        
        return updated_data
