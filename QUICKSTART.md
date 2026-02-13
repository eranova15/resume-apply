# Quick Start Guide

## For Linux/Mac Users

1. **Run the application:**
   ```bash
   ./run.sh
   ```

   Or manually:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python src/main.py
   ```

## For Windows Users

1. **Run the application:**
   ```cmd
   run.bat
   ```

   Or manually:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python src\main.py
   ```

## Testing the System

Run the automated tests:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
python tests/test_modules.py
```

## Using the Example Resume

Try the system with the provided example:
```bash
./run.sh
# When prompted, enter: examples/sample_resume.txt
```

## Configuration

### Without AI (Default)
The system works out of the box with rule-based suggestions. No setup needed!

### With AI (Optional)
For smarter suggestions:

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API key:
   ```
   OPENAI_API_KEY=sk-your-key-here
   # OR
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

3. Run the application normally

## Troubleshooting

**Problem**: "Command not found: python3"
**Solution**: Try `python` instead of `python3`

**Problem**: "Permission denied" when running ./run.sh
**Solution**: Make it executable with `chmod +x run.sh`

**Problem**: Job scraping fails
**Solution**: This is normal for many websites. The system will use demonstration data and still work.

**Problem**: PDF generation fails
**Solution**: Ensure you have write permissions in the `output/` directory

## What to Expect

1. **Input Phase**: 
   - Provide your resume (PDF, DOCX, or TXT)
   - Enter job posting URLs

2. **Analysis Phase**:
   - System scrapes job requirements
   - Compares with your resume
   - Generates prioritized suggestions

3. **Review Phase**:
   - Review suggestions
   - Accept, edit, or reject

4. **Output Phase**:
   - Optimized resume PDF in `output/`
   - Cover letter PDF in `output/`

## Tips

- Use the example resume to understand the format expected
- Valid job URLs help, but the system works with mock data for testing
- Review suggestions carefully - you decide what's accurate
- PDFs are saved in the `output/` directory with descriptive names
- You can run the system multiple times for different jobs

## Need Help?

- Check the main README.md for detailed documentation
- Review example files in `examples/`
- Run tests to verify everything works: `python tests/test_modules.py`
