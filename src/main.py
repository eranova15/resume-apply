"""
Resume Application System
Main entry point for the resume optimization application
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from modules.resume_parser import ResumeParser
from modules.job_scraper import JobScraper
from modules.suggestion_engine import SuggestionEngine
from modules.resume_generator import ResumeGenerator
from modules.cover_letter_generator import CoverLetterGenerator
from modules.ui_handler import UIHandler


def main():
    """Main application flow"""
    print("=" * 60)
    print("Welcome to Resume Application System")
    print("=" * 60)
    print()
    
    # Initialize components
    ui = UIHandler()
    resume_parser = ResumeParser()
    job_scraper = JobScraper()
    suggestion_engine = SuggestionEngine()
    resume_generator = ResumeGenerator()
    cover_letter_generator = CoverLetterGenerator()
    
    # Step 1: Get user inputs
    print("Step 1: Input Collection")
    print("-" * 60)
    resume_path = ui.get_resume_path()
    job_urls = ui.get_job_urls()
    
    # Parse resume
    print("\nParsing your resume...")
    resume_data = resume_parser.parse(resume_path)
    print(f"✓ Resume parsed successfully")
    
    # Process each job
    for job_url in job_urls:
        print(f"\n{'=' * 60}")
        print(f"Processing job: {job_url}")
        print('=' * 60)
        
        # Step 2: Scrape job listing
        print("\nStep 2: Scraping job listing...")
        job_data = job_scraper.scrape(job_url)
        print(f"✓ Job listing scraped: {job_data.get('title', 'Unknown')}")
        
        # Step 3: Generate suggestions
        print("\nStep 3: Analyzing requirements and generating suggestions...")
        suggestions = suggestion_engine.generate_suggestions(resume_data, job_data)
        print(f"✓ Generated {len(suggestions)} suggestions")
        
        # Step 4: Show suggestions to user
        print("\nStep 4: Review suggestions")
        ui.display_suggestions(suggestions)
        
        # Step 5: Get user decision
        while True:
            decision = ui.get_user_decision()
            
            if decision == "accept":
                # Apply suggestions
                print("\nApplying suggestions to resume...")
                updated_resume_data = suggestion_engine.apply_suggestions(
                    resume_data, suggestions
                )
                
                # Generate new resume PDF
                print("\nGenerating optimized resume PDF...")
                output_dir = Path("output")
                output_dir.mkdir(exist_ok=True)
                
                resume_filename = f"resume_optimized_{Path(job_url).name[:20]}.pdf"
                resume_path_out = output_dir / resume_filename
                resume_generator.generate(updated_resume_data, resume_path_out)
                print(f"✓ Resume saved to: {resume_path_out}")
                
                # Generate cover letter
                print("\nGenerating cover letter...")
                cover_letter_filename = f"cover_letter_{Path(job_url).name[:20]}.pdf"
                cover_letter_path = output_dir / cover_letter_filename
                cover_letter_generator.generate(
                    updated_resume_data, job_data, cover_letter_path
                )
                print(f"✓ Cover letter saved to: {cover_letter_path}")
                
                print("\n✓ Application package complete!")
                break
                
            elif decision == "edit":
                # Let user choose which resume to edit
                resume_to_edit = ui.choose_resume_to_edit()
                
                if resume_to_edit == "original":
                    edit_data = resume_data
                else:  # new
                    edit_data = suggestion_engine.apply_suggestions(
                        resume_data, suggestions
                    )
                
                # Show resume and let user mark areas
                print("\nDisplaying resume for editing...")
                ui.display_resume_for_editing(edit_data)
                
                edit_requests = ui.get_edit_requests()
                
                # Re-run engine with edit requests
                print("\nRegenerating suggestions based on your feedback...")
                suggestions = suggestion_engine.generate_suggestions(
                    resume_data, job_data, edit_requests
                )
                
                # Show updated suggestions
                ui.display_suggestions(suggestions)
                
            elif decision == "reject":
                print("\nSkipping this job opportunity.")
                break
    
    print("\n" + "=" * 60)
    print("Thank you for using Resume Application System!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
