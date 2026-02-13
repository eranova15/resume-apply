#!/usr/bin/env python3
"""
End-to-End Test Suite for Resume Application System
Tests both "Improve Resume" and "Apply for Jobs" workflows
"""

import sys
from pathlib import Path
import subprocess

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

def run_command(cmd, description):
    """Run a shell command and return the result"""
    print(f"\n{'='*70}")
    print(f"TEST: {description}")
    print('='*70)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    return result.returncode == 0

def test_import_modules():
    """Test that all modules can be imported"""
    print("\n" + "="*70)
    print("TEST 1: Module Import Test")
    print("="*70)
    
    try:
        from modules.resume_parser import ResumeParser
        from modules.job_scraper import JobScraper
        from modules.suggestion_engine import SuggestionEngine
        from modules.resume_generator import ResumeGenerator
        from modules.cover_letter_generator import CoverLetterGenerator
        from modules.ui_handler import UIHandler
        
        print("✓ All modules imported successfully")
        
        # Test instantiation
        parser = ResumeParser()
        scraper = JobScraper()
        engine = SuggestionEngine()
        generator = ResumeGenerator()
        cover_gen = CoverLetterGenerator()
        ui = UIHandler()
        
        print("✓ All components instantiated successfully")
        
        # Test UI methods
        assert hasattr(ui, 'get_initial_choice'), "Missing get_initial_choice method"
        assert hasattr(ui, 'get_user_decision'), "Missing get_user_decision method"
        assert hasattr(ui, 'get_resume_path'), "Missing get_resume_path method"
        assert hasattr(ui, 'get_job_urls'), "Missing get_job_urls method"
        
        print("✓ All UI methods present")
        
        return True
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_resume_parsing():
    """Test resume parsing with sample file"""
    print("\n" + "="*70)
    print("TEST 2: Resume Parsing")
    print("="*70)
    
    try:
        from modules.resume_parser import ResumeParser
        
        parser = ResumeParser()
        sample_path = Path(__file__).parent.parent / 'examples' / 'sample_resume.txt'
        
        if not sample_path.exists():
            print(f"✗ Sample resume not found: {sample_path}")
            return False
        
        resume_data = parser.parse(str(sample_path))
        
        # Validate parsed data
        assert resume_data is not None, "Resume data is None"
        assert 'raw_text' in resume_data, "Missing raw_text"
        assert 'skills' in resume_data, "Missing skills"
        assert 'contact_info' in resume_data, "Missing contact_info"
        
        print(f"✓ Resume parsed successfully")
        print(f"  - Skills found: {len(resume_data['skills'])}")
        print(f"  - Email: {resume_data['contact_info'].get('email', 'N/A')}")
        print(f"  - Sections: {', '.join(resume_data.get('sections', {}).keys())}")
        
        return True
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_job_scraping():
    """Test job scraping (will use mock data)"""
    print("\n" + "="*70)
    print("TEST 3: Job Scraping")
    print("="*70)
    
    try:
        from modules.job_scraper import JobScraper
        
        scraper = JobScraper()
        job_data = scraper.scrape("https://example.com/test-job")
        
        # Validate job data
        assert job_data is not None, "Job data is None"
        assert 'title' in job_data, "Missing title"
        assert 'requirements' in job_data, "Missing requirements"
        assert 'description' in job_data, "Missing description"
        
        print(f"✓ Job scraped successfully")
        print(f"  - Title: {job_data['title']}")
        print(f"  - Company: {job_data['company']}")
        print(f"  - Technical skills: {len(job_data['requirements'].get('technical_skills', []))}")
        
        return True
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_suggestion_generation():
    """Test suggestion generation"""
    print("\n" + "="*70)
    print("TEST 4: Suggestion Generation")
    print("="*70)
    
    try:
        from modules.resume_parser import ResumeParser
        from modules.job_scraper import JobScraper
        from modules.suggestion_engine import SuggestionEngine
        
        # Parse resume
        parser = ResumeParser()
        sample_path = Path(__file__).parent.parent / 'examples' / 'sample_resume.txt'
        resume_data = parser.parse(str(sample_path))
        
        # Scrape job
        scraper = JobScraper()
        job_data = scraper.scrape("https://example.com/test-job")
        
        # Generate suggestions
        engine = SuggestionEngine(use_ai=False)  # Use rule-based
        suggestions = engine.generate_suggestions(resume_data, job_data)
        
        # Validate suggestions
        assert suggestions is not None, "Suggestions is None"
        assert len(suggestions) > 0, "No suggestions generated"
        
        print(f"✓ Generated {len(suggestions)} suggestions")
        
        # Check suggestion structure
        for i, sugg in enumerate(suggestions[:3], 1):
            assert 'category' in sugg, f"Suggestion {i} missing category"
            assert 'priority' in sugg, f"Suggestion {i} missing priority"
            assert 'description' in sugg, f"Suggestion {i} missing description"
            print(f"  {i}. [{sugg['priority']}] {sugg['category']}: {sugg['description'][:60]}...")
        
        return True
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pdf_generation():
    """Test PDF generation"""
    print("\n" + "="*70)
    print("TEST 5: PDF Generation")
    print("="*70)
    
    try:
        from modules.resume_parser import ResumeParser
        from modules.job_scraper import JobScraper
        from modules.suggestion_engine import SuggestionEngine
        from modules.resume_generator import ResumeGenerator
        from modules.cover_letter_generator import CoverLetterGenerator
        
        # Parse resume
        parser = ResumeParser()
        sample_path = Path(__file__).parent.parent / 'examples' / 'sample_resume.txt'
        resume_data = parser.parse(str(sample_path))
        
        # Scrape job
        scraper = JobScraper()
        job_data = scraper.scrape("https://example.com/test-job")
        
        # Generate and apply suggestions
        engine = SuggestionEngine(use_ai=False)
        suggestions = engine.generate_suggestions(resume_data, job_data)
        for sugg in suggestions[:2]:
            sugg['applied'] = True
        updated_resume = engine.apply_suggestions(resume_data, suggestions)
        
        # Generate PDFs
        output_dir = Path(__file__).parent.parent / 'output'
        output_dir.mkdir(exist_ok=True)
        
        resume_path = output_dir / 'test_e2e_resume.pdf'
        cover_path = output_dir / 'test_e2e_cover_letter.pdf'
        
        generator = ResumeGenerator()
        generator.generate(updated_resume, resume_path)
        
        cover_gen = CoverLetterGenerator()
        cover_gen.generate(updated_resume, job_data, cover_path)
        
        # Validate files exist
        assert resume_path.exists(), f"Resume PDF not created: {resume_path}"
        assert cover_path.exists(), f"Cover letter PDF not created: {cover_path}"
        
        print(f"✓ Resume PDF generated: {resume_path}")
        print(f"  - Size: {resume_path.stat().st_size / 1024:.1f} KB")
        print(f"✓ Cover letter PDF generated: {cover_path}")
        print(f"  - Size: {cover_path.stat().st_size / 1024:.1f} KB")
        
        return True
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_iterative_improvement():
    """Test iterative improvement flow"""
    print("\n" + "="*70)
    print("TEST 6: Iterative Improvement Flow")
    print("="*70)
    
    try:
        from modules.resume_parser import ResumeParser
        from modules.job_scraper import JobScraper
        from modules.suggestion_engine import SuggestionEngine
        
        # Parse resume
        parser = ResumeParser()
        sample_path = Path(__file__).parent.parent / 'examples' / 'sample_resume.txt'
        resume_data = parser.parse(str(sample_path))
        
        # Scrape job
        scraper = JobScraper()
        job_data = scraper.scrape("https://example.com/test-job")
        
        # Generate initial suggestions
        engine = SuggestionEngine(use_ai=False)
        suggestions_round1 = engine.generate_suggestions(resume_data, job_data)
        print(f"✓ Round 1: Generated {len(suggestions_round1)} suggestions")
        
        # Apply suggestions (simulating "Improve" option)
        for sugg in suggestions_round1[:2]:
            sugg['applied'] = True
        current_resume = engine.apply_suggestions(resume_data, suggestions_round1)
        print(f"✓ Applied suggestions to resume")
        
        # Generate new suggestions based on improved resume
        edit_requests = "Add more quantifiable metrics and AWS experience"
        suggestions_round2 = engine.generate_suggestions(
            current_resume, job_data, edit_requests
        )
        print(f"✓ Round 2: Generated {len(suggestions_round2)} suggestions")
        
        # Apply again (second improvement cycle)
        for sugg in suggestions_round2[:1]:
            sugg['applied'] = True
        final_resume = engine.apply_suggestions(current_resume, suggestions_round2)
        print(f"✓ Applied second round of suggestions")
        
        # Verify improvements were tracked
        if '_updates' in final_resume:
            updates = final_resume['_updates']
            print(f"✓ Improvements tracked:")
            if updates.get('skills_added'):
                print(f"  - Skills added: {', '.join(updates['skills_added'])}")
        
        print(f"✓ Iterative improvement flow completed successfully")
        
        return True
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("="*70)
    print("RESUME APPLICATION SYSTEM - END-TO-END TEST SUITE")
    print("="*70)
    
    results = []
    
    # Run all tests
    results.append(("Module Import", test_import_modules()))
    results.append(("Resume Parsing", test_resume_parsing()))
    results.append(("Job Scraping", test_job_scraping()))
    results.append(("Suggestion Generation", test_suggestion_generation()))
    results.append(("PDF Generation", test_pdf_generation()))
    results.append(("Iterative Improvement", test_iterative_improvement()))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! The application is ready to use.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
