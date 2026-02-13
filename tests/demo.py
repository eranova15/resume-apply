#!/usr/bin/env python
"""
Demo script that shows the Resume Application System in action
Runs through a complete workflow without requiring user input
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

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)

def print_section(text):
    """Print a formatted section"""
    print("\n" + text)
    print("-" * 60)

def main():
    """Run demonstration"""
    print_header("Resume Application System - DEMO")
    
    print("\nThis demo shows the complete workflow of the system:")
    print("1. Parse resume")
    print("2. Scrape job posting")
    print("3. Generate suggestions")
    print("4. Apply suggestions")
    print("5. Generate optimized resume PDF")
    print("6. Generate cover letter PDF")
    
    # Step 1: Parse Resume
    print_section("STEP 1: Parse Resume")
    
    resume_path = Path(__file__).parent.parent / 'examples' / 'sample_resume.txt'
    print(f"Loading resume from: {resume_path.name}")
    
    parser = ResumeParser()
    resume_data = parser.parse(str(resume_path))
    
    print(f"\n✓ Resume parsed successfully!")
    print(f"  - Contact: {resume_data['contact_info']['email']}")
    print(f"  - Skills found: {len(resume_data['skills'])}")
    print(f"  - Key skills: {', '.join(resume_data['skills'][:5])}")
    
    # Step 2: Scrape Job
    print_section("STEP 2: Scrape Job Posting")
    
    job_url = "https://example.com/senior-python-developer"
    print(f"Fetching job from: {job_url}")
    
    scraper = JobScraper()
    job_data = scraper.scrape(job_url)
    
    print(f"\n✓ Job scraped successfully!")
    print(f"  - Title: {job_data['title']}")
    print(f"  - Company: {job_data['company']}")
    print(f"  - Location: {job_data['location']}")
    print(f"  - Required skills: {', '.join(job_data['requirements']['technical_skills'][:5])}")
    print(f"  - Experience: {job_data['requirements'].get('experience_years', 'Not specified')}")
    
    # Step 3: Generate Suggestions
    print_section("STEP 3: Generate Suggestions")
    
    print("Analyzing resume against job requirements...")
    
    engine = SuggestionEngine(use_ai=False)
    suggestions = engine.generate_suggestions(resume_data, job_data)
    
    print(f"\n✓ Generated {len(suggestions)} suggestions!")
    
    # Group by priority
    high = [s for s in suggestions if s.get('priority') == 'HIGH']
    medium = [s for s in suggestions if s.get('priority') == 'MEDIUM']
    low = [s for s in suggestions if s.get('priority') == 'LOW']
    
    if high:
        print("\nHIGH PRIORITY:")
        for i, sugg in enumerate(high, 1):
            print(f"  {i}. [{sugg['category']}] {sugg['description']}")
    
    if medium:
        print("\nMEDIUM PRIORITY:")
        for i, sugg in enumerate(medium, 1):
            print(f"  {i}. [{sugg['category']}] {sugg['description']}")
    
    if low:
        print("\nLOW PRIORITY:")
        for i, sugg in enumerate(low, 1):
            print(f"  {i}. [{sugg['category']}] {sugg['description']}")
    
    # Step 4: Apply Suggestions
    print_section("STEP 4: Apply Suggestions")
    
    print("User decision: ACCEPT suggestions")
    print("Marking top suggestions as applied...")
    
    # Apply top 3 suggestions
    for i, sugg in enumerate(suggestions[:3]):
        sugg['applied'] = True
        print(f"  ✓ Applied: [{sugg['category']}] {sugg['description'][:50]}...")
    
    updated_resume_data = engine.apply_suggestions(resume_data, suggestions)
    
    print("\n✓ Suggestions applied to resume!")
    
    updates = updated_resume_data.get('_updates', {})
    if updates.get('skills_added'):
        print(f"  - Skills added: {', '.join(updates['skills_added'])}")
    if updates.get('sections_modified'):
        print(f"  - Sections modified: {', '.join(updates['sections_modified'])}")
    
    # Step 5: Generate Resume PDF
    print_section("STEP 5: Generate Optimized Resume PDF")
    
    output_dir = Path(__file__).parent.parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    resume_output = output_dir / 'demo_resume_optimized.pdf'
    
    print(f"Generating PDF: {resume_output.name}")
    
    generator = ResumeGenerator()
    generator.generate(updated_resume_data, resume_output)
    
    print(f"\n✓ Resume PDF generated!")
    print(f"  - Location: {resume_output}")
    print(f"  - Size: {resume_output.stat().st_size / 1024:.1f} KB")
    
    # Step 6: Generate Cover Letter
    print_section("STEP 6: Generate Cover Letter PDF")
    
    cover_letter_output = output_dir / 'demo_cover_letter.pdf'
    
    print(f"Generating PDF: {cover_letter_output.name}")
    
    cover_generator = CoverLetterGenerator()
    cover_generator.generate(updated_resume_data, job_data, cover_letter_output)
    
    print(f"\n✓ Cover letter PDF generated!")
    print(f"  - Location: {cover_letter_output}")
    print(f"  - Size: {cover_letter_output.stat().st_size / 1024:.1f} KB")
    
    # Summary
    print_header("DEMO COMPLETE")
    
    print("\n✅ All steps completed successfully!")
    print("\nGenerated files:")
    print(f"  1. {resume_output}")
    print(f"  2. {cover_letter_output}")
    
    print("\nThese documents are ready to be used for job applications!")
    print("\nTo run the interactive version, use:")
    print("  ./run.sh  (Linux/Mac)")
    print("  run.bat   (Windows)")
    print("  or: python src/main.py")
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
