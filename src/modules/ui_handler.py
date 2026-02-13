"""
UI Handler Module
Handles user interaction via command line interface
"""

import sys
from pathlib import Path


class UIHandler:
    """Handles user interaction and input/output"""
    
    def __init__(self):
        self.separator = "=" * 60
    
    def get_resume_path(self):
        """
        Get resume file path from user
        
        Returns:
            str: Path to resume file
        """
        while True:
            print("Please enter the path to your resume file:")
            print("  Supported formats: PDF, DOCX, TXT")
            path = input("Resume path: ").strip()
            
            if not path:
                print("  Error: Path cannot be empty")
                continue
            
            path = Path(path).expanduser()
            
            if not path.exists():
                print(f"  Error: File not found: {path}")
                retry = input("  Try again? (y/n): ").strip().lower()
                if retry != 'y':
                    sys.exit(0)
                continue
            
            ext = path.suffix.lower()
            if ext not in ['.pdf', '.docx', '.txt']:
                print(f"  Error: Unsupported format: {ext}")
                print("  Please use PDF, DOCX, or TXT format")
                continue
            
            return str(path)
    
    def get_job_urls(self):
        """
        Get job posting URLs from user
        
        Returns:
            list: List of job URLs
        """
        print("\nPlease enter job posting URLs (one per line)")
        print("  Press Enter twice when done, or Ctrl+C to cancel")
        
        urls = []
        while True:
            try:
                url = input(f"Job URL {len(urls) + 1}: ").strip()
                
                if not url:
                    if urls:
                        break
                    else:
                        print("  Please enter at least one URL")
                        continue
                
                # Basic URL validation
                if not url.startswith(('http://', 'https://')):
                    print("  Warning: URL should start with http:// or https://")
                    use_anyway = input("  Use anyway? (y/n): ").strip().lower()
                    if use_anyway != 'y':
                        continue
                
                urls.append(url)
                print(f"  ✓ Added ({len(urls)} total)")
                
            except KeyboardInterrupt:
                if urls:
                    print(f"\n  Using {len(urls)} URL(s)")
                    break
                else:
                    print("\n  Cancelled")
                    sys.exit(0)
        
        return urls
    
    def display_suggestions(self, suggestions):
        """
        Display suggestions to user
        
        Args:
            suggestions: List of suggestion dictionaries
        """
        print("\n" + self.separator)
        print("SUGGESTED IMPROVEMENTS")
        print(self.separator)
        
        if not suggestions:
            print("No suggestions generated.")
            return
        
        # Group by priority
        high = [s for s in suggestions if s.get('priority') == 'HIGH']
        medium = [s for s in suggestions if s.get('priority') == 'MEDIUM']
        low = [s for s in suggestions if s.get('priority') == 'LOW']
        
        for priority, items in [('HIGH', high), ('MEDIUM', medium), ('LOW', low)]:
            if items:
                print(f"\n{priority} PRIORITY:")
                for i, sugg in enumerate(items, 1):
                    category = sugg.get('category', 'GENERAL')
                    desc = sugg.get('description', '')
                    print(f"  {i}. [{category}] {desc}")
        
        print("\n" + self.separator)
    
    def get_user_decision(self):
        """
        Get user's decision on suggestions
        
        Returns:
            str: 'accept', 'edit', or 'reject'
        """
        print("\nWhat would you like to do?")
        print("  1. Accept suggestions and generate resume + cover letter")
        print("  2. Request edits to specific areas")
        print("  3. Reject and skip this job")
        
        while True:
            choice = input("\nYour choice (1/2/3): ").strip()
            
            if choice == '1':
                return 'accept'
            elif choice == '2':
                return 'edit'
            elif choice == '3':
                confirm = input("  Are you sure you want to skip this job? (y/n): ").strip().lower()
                if confirm == 'y':
                    return 'reject'
            else:
                print("  Invalid choice. Please enter 1, 2, or 3.")
    
    def choose_resume_to_edit(self):
        """
        Let user choose which resume version to edit
        
        Returns:
            str: 'original' or 'new'
        """
        print("\nWhich resume would you like to edit?")
        print("  1. Original resume")
        print("  2. New resume (with suggestions applied)")
        
        while True:
            choice = input("\nYour choice (1/2): ").strip()
            
            if choice == '1':
                return 'original'
            elif choice == '2':
                return 'new'
            else:
                print("  Invalid choice. Please enter 1 or 2.")
    
    def display_resume_for_editing(self, resume_data):
        """
        Display resume sections for user to review
        
        Args:
            resume_data: Resume data dictionary
        """
        print("\n" + self.separator)
        print("RESUME PREVIEW")
        print(self.separator)
        
        # Show key sections
        sections = resume_data.get('sections', {})
        
        print("\nSECTIONS:")
        for section_name, section_data in sections.items():
            print(f"\n  [{section_name.upper()}]")
            content = section_data.get('content', [])
            for line in content[:5]:  # Show first 5 lines of each section
                print(f"    {line}")
            if len(content) > 5:
                print(f"    ... ({len(content) - 5} more lines)")
        
        # Show skills
        skills = resume_data.get('skills', [])
        if skills:
            print(f"\n  [SKILLS]")
            print(f"    {', '.join(skills[:15])}")
            if len(skills) > 15:
                print(f"    ... ({len(skills) - 15} more)")
        
        print("\n" + self.separator)
    
    def get_edit_requests(self):
        """
        Get specific edit requests from user
        
        Returns:
            str: User's edit requests
        """
        print("\nPlease describe the changes you'd like to make:")
        print("  (You can specify sections, content, or general feedback)")
        print("  Press Enter twice when done")
        
        lines = []
        empty_count = 0
        
        while True:
            line = input()
            
            if not line:
                empty_count += 1
                if empty_count >= 2 or (lines and empty_count >= 1):
                    break
            else:
                empty_count = 0
                lines.append(line)
        
        edit_text = '\n'.join(lines).strip()
        
        if not edit_text:
            edit_text = "Please refine the suggestions"
        
        return edit_text
    
    def confirm_action(self, message):
        """
        Get yes/no confirmation from user
        
        Args:
            message: Confirmation message
            
        Returns:
            bool: True if confirmed, False otherwise
        """
        while True:
            response = input(f"{message} (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("  Please enter 'y' or 'n'")
