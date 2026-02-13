# Resume Apply - Intelligent Resume Optimization System

An intelligent system that helps you optimize your resume for specific job opportunities. It analyzes job postings, compares them with your resume, generates tailored suggestions, and creates professional PDFs along with cover letters.

## Features

- **Resume Parsing**: Supports PDF, DOCX, and TXT formats
- **Job Scraping**: Automatically extracts requirements from job posting URLs
- **Intelligent Suggestions**: AI-powered or rule-based analysis of resume vs. job requirements
- **Interactive Workflow**: Review, edit, and refine suggestions
- **PDF Generation**: Creates optimized resume PDFs
- **Cover Letter Generation**: Automatically generates personalized cover letters
- **Iterative Refinement**: Request changes and regenerate suggestions

## Workflow

1. **Input Collection**
   - Provide your resume (PDF, DOCX, or TXT)
   - Enter job opportunity URLs

2. **Analysis & Suggestions**
   - System scrapes job listings
   - Analyzes requirements vs. your resume
   - Generates specific, actionable suggestions
   - Shows suggestions grouped by priority

3. **Review & Decision**
   - **Accept**: Generate optimized resume PDF + cover letter
   - **Edit**: Choose resume version (original/new), mark areas for changes, regenerate suggestions
   - **Reject**: Skip this job opportunity

4. **Output**
   - Optimized resume PDF tailored to the job
   - Professional cover letter PDF

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/eranova15/resume-apply.git
cd resume-apply
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Configure AI API:
   - Copy `.env.example` to `.env`
   - Add your OpenAI or Anthropic API key for AI-powered suggestions
   - If no API key is provided, the system uses rule-based suggestions

```bash
cp .env.example .env
# Edit .env and add your API key
```

## Usage

### Basic Usage

Run the main application:
```bash
python src/main.py
```

Follow the interactive prompts:

1. **Enter resume path**: 
   ```
   Resume path: /path/to/your/resume.pdf
   ```

2. **Enter job URLs** (one per line, press Enter twice when done):
   ```
   Job URL 1: https://example.com/job-posting-1
   Job URL 2: https://example.com/job-posting-2
   ```

3. **Review suggestions** and choose an action:
   - Type `1` to accept and generate documents
   - Type `2` to request edits
   - Type `3` to skip

4. **Find your outputs** in the `output/` directory

### Example Session

```
============================================================
Welcome to Resume Application System
============================================================

Step 1: Input Collection
------------------------------------------------------------
Please enter the path to your resume file:
  Supported formats: PDF, DOCX, TXT
Resume path: examples/my_resume.pdf

Parsing your resume...
✓ Resume parsed successfully

Please enter job posting URLs (one per line)
  Press Enter twice when done, or Ctrl+C to cancel
Job URL 1: https://example.com/software-engineer-job
  ✓ Added (1 total)
Job URL 2: 

============================================================
Processing job: https://example.com/software-engineer-job
============================================================

Step 2: Scraping job listing...
  Fetching job listing from: https://example.com/software-engineer-job
✓ Job listing scraped: Software Engineer

Step 3: Analyzing requirements and generating suggestions...
✓ Generated 7 suggestions

Step 4: Review suggestions
============================================================
SUGGESTED IMPROVEMENTS
============================================================

HIGH PRIORITY:
  1. [SKILLS] Add these relevant skills if you have them: docker, kubernetes, aws
  2. [KEYWORDS] Consider incorporating these keywords: cloud computing, devops
  3. [SUMMARY] Add a professional summary tailored to this Software Engineer role

MEDIUM PRIORITY:
  4. [EXPERIENCE] Ensure your experience section highlights that you meet the '3+ years' requirement
  5. [EXPERIENCE] Add quantifiable metrics to your achievements

============================================================

What would you like to do?
  1. Accept suggestions and generate resume + cover letter
  2. Request edits to specific areas
  3. Reject and skip this job

Your choice (1/2/3): 1

Applying suggestions to resume...

Generating optimized resume PDF...
✓ Resume saved to: output/resume_optimized_software-engineer-job.pdf

Generating cover letter...
✓ Cover letter saved to: output/cover_letter_software-engineer-job.pdf

✓ Application package complete!
```

## Project Structure

```
resume-apply/
├── src/
│   ├── main.py                          # Main application entry point
│   └── modules/
│       ├── __init__.py
│       ├── resume_parser.py             # Resume parsing (PDF, DOCX, TXT)
│       ├── job_scraper.py               # Job posting scraper
│       ├── suggestion_engine.py         # Suggestion generation (AI/rule-based)
│       ├── resume_generator.py          # PDF resume generator
│       ├── cover_letter_generator.py    # PDF cover letter generator
│       └── ui_handler.py                # CLI user interface
├── output/                              # Generated PDFs (created automatically)
├── examples/                            # Example resumes
├── requirements.txt                     # Python dependencies
├── .env.example                         # Environment variables template
├── .gitignore                          # Git ignore rules
└── README.md                           # This file
```

## Configuration

### AI-Powered Suggestions

To use AI-powered suggestions (more intelligent and context-aware):

1. Get an API key from [OpenAI](https://openai.com) or [Anthropic](https://anthropic.com)
2. Add it to your `.env` file:
   ```
   OPENAI_API_KEY=sk-...
   # OR
   ANTHROPIC_API_KEY=sk-ant-...
   ```

### Rule-Based Suggestions

If no API key is configured, the system automatically uses rule-based suggestions that:
- Match keywords between job posting and resume
- Check for missing technical skills
- Validate experience requirements
- Suggest formatting improvements

## Features in Detail

### Resume Parser
- Extracts text from PDF, DOCX, and TXT files
- Identifies resume sections (summary, experience, education, skills)
- Extracts contact information
- Structures data for analysis

### Job Scraper
- Fetches job postings from URLs
- Extracts job title, company, location
- Identifies technical skills requirements
- Parses experience and education requirements
- Extracts key qualifications

### Suggestion Engine
- Compares resume against job requirements
- Generates prioritized suggestions (HIGH, MEDIUM, LOW)
- Categorizes suggestions (SKILLS, EXPERIENCE, EDUCATION, etc.)
- Supports iterative refinement based on user feedback

### Resume Generator
- Creates professional PDF resumes
- Highlights added skills and improvements
- Clean, readable formatting
- Optimized for ATS (Applicant Tracking Systems)

### Cover Letter Generator
- Creates personalized cover letters
- References specific job and company
- Highlights relevant skills from resume
- Professional formatting

## Tips for Best Results

1. **Use Clear Resume Formats**: Well-structured resumes with clear sections (Summary, Skills, Experience, Education) work best

2. **Provide Complete Job URLs**: Full job posting URLs give better results than shortened links

3. **Review Suggestions Carefully**: The system provides suggestions - you decide what's accurate and relevant

4. **Iterate**: Use the edit feature to refine suggestions if the first pass isn't quite right

5. **Keep Original Resume**: The system always preserves your original resume and creates new versions

## Troubleshooting

### Issue: "Module not found" error
**Solution**: Ensure you've activated your virtual environment and installed requirements:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: Job scraping fails
**Solution**: The system will use mock data for demonstration. For better results, ensure:
- URL is accessible (not behind login)
- Website allows scraping (check robots.txt)
- You have a stable internet connection

### Issue: PDF generation fails
**Solution**: Ensure the `output/` directory has write permissions

### Issue: AI suggestions not working
**Solution**: 
- Check your `.env` file has a valid API key
- Verify API key has sufficient credits/quota
- System will automatically fall back to rule-based suggestions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Future Enhancements

- [ ] Support for more file formats (RTF, HTML)
- [ ] Web interface
- [ ] Support for multiple resume versions
- [ ] Job board integrations (LinkedIn, Indeed, etc.)
- [ ] Resume templates
- [ ] A/B testing of different resume versions
- [ ] Analytics on suggestion acceptance rates
- [ ] Browser extension for one-click job analysis

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Note**: This tool is designed to help optimize your resume, but human review is always recommended. The suggestions are meant to guide you, not replace your judgment about what's accurate and relevant for your experience.