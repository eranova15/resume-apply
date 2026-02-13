#!/usr/bin/env python
"""
Test script to verify all modules work correctly
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from modules.resume_parser import ResumeParser
from modules.job_scraper import JobScraper
from modules.suggestion_engine import SuggestionEngine
from modules.resume_generator import ResumeGenerator
from modules.cover_letter_generator import CoverLetterGenerator

def test_resume_parser():
    """Test resume parser"""
    print("Testing Resume Parser...")
    parser = ResumeParser()
    
    # Test with example resume
    resume_path = Path(__file__).parent.parent / 'examples' / 'sample_resume.txt'
    resume_data = parser.parse(str(resume_path))
    
    assert resume_data is not None
    assert 'raw_text' in resume_data
    assert 'skills' in resume_data
    assert len(resume_data['skills']) > 0
    
    print(f"  ✓ Parsed resume successfully")
    print(f"  ✓ Found {len(resume_data['skills'])} skills")
    print(f"  ✓ Contact: {resume_data.get('contact_info', {}).get('email', 'N/A')}")
    
    return resume_data

def test_job_scraper():
    """Test job scraper"""
    print("\nTesting Job Scraper...")
    scraper = JobScraper()
    
    # Test with mock URL (will use mock data)
    job_data = scraper.scrape("https://example.com/job-posting")
    
    assert job_data is not None
    assert 'title' in job_data
    assert 'requirements' in job_data
    
    print(f"  ✓ Scraped job: {job_data['title']}")
    print(f"  ✓ Found {len(job_data['requirements'].get('technical_skills', []))} technical skills")
    
    return job_data

def test_suggestion_engine(resume_data, job_data):
    """Test suggestion engine"""
    print("\nTesting Suggestion Engine...")
    engine = SuggestionEngine(use_ai=False)  # Use rule-based for testing
    
    suggestions = engine.generate_suggestions(resume_data, job_data)
    
    assert suggestions is not None
    assert len(suggestions) > 0
    
    print(f"  ✓ Generated {len(suggestions)} suggestions")
    
    # Print first 3 suggestions
    for i, sugg in enumerate(suggestions[:3], 1):
        print(f"  {i}. [{sugg['category']}] {sugg['description'][:60]}...")
    
    # Test applying suggestions
    for sugg in suggestions[:2]:
        sugg['applied'] = True
    
    updated_data = engine.apply_suggestions(resume_data, suggestions)
    assert updated_data is not None
    
    print(f"  ✓ Applied suggestions successfully")
    
    return suggestions, updated_data

def test_resume_generator(resume_data):
    """Test resume generator"""
    print("\nTesting Resume Generator...")
    generator = ResumeGenerator()
    
    output_dir = Path(__file__).parent.parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    output_path = output_dir / 'test_resume.pdf'
    result = generator.generate(resume_data, output_path)
    
    assert Path(result).exists()
    print(f"  ✓ Generated resume PDF: {result}")
    
    return result

def test_cover_letter_generator(resume_data, job_data):
    """Test cover letter generator"""
    print("\nTesting Cover Letter Generator...")
    generator = CoverLetterGenerator()
    
    output_dir = Path(__file__).parent.parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    output_path = output_dir / 'test_cover_letter.pdf'
    result = generator.generate(resume_data, job_data, output_path)
    
    assert Path(result).exists()
    print(f"  ✓ Generated cover letter PDF: {result}")
    
    return result

def main():
    """Run all tests"""
    print("=" * 60)
    print("Resume Application System - Module Tests")
    print("=" * 60)
    
    try:
        # Test each module
        resume_data = test_resume_parser()
        job_data = test_job_scraper()
        suggestions, updated_data = test_suggestion_engine(resume_data, job_data)
        resume_pdf = test_resume_generator(updated_data)
        cover_letter_pdf = test_cover_letter_generator(updated_data, job_data)
        
        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        print(f"\nGenerated files:")
        print(f"  - {resume_pdf}")
        print(f"  - {cover_letter_pdf}")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
