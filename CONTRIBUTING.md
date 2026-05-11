# Contributing to HR Shortlisting Agent

Thank you for your interest in contributing to the HR Shortlisting Agent! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help make this a welcoming community

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork:**
   ```bash
   git clone https://github.com/yourusername/HR-Shortlisting-Agent.git
   cd "RAG Pipleiiine TCI"
   ```
3. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Making Changes

### Branch Naming
Use descriptive branch names:
- `feature/add-new-scoring-dimension`
- `fix/resume-parsing-bug`
- `docs/update-readme`
- `refactor/simplify-scorer`

### Commit Messages
Write clear, descriptive commit messages:
```
Add: Description of what was added
Fix: Brief description of the bug fix
Update: Changes to existing features
Docs: Documentation updates
Refactor: Code improvements without behavior change
```

### Code Style
- Follow PEP 8 for Python
- Use type hints where possible
- Add docstrings to functions
- Keep functions focused and small
- Use descriptive variable names

### Testing
- Write tests for new features
- Ensure all tests pass: `pytest`
- Test with sample data from `test_data/`
- Run tests before submitting PR

## Submission Process

1. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Add: your meaningful message"
   ```

2. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request on GitHub:**
   - Use a descriptive title
   - Describe what changed and why
   - Reference related issues
   - Include before/after examples if applicable

4. **Wait for review:**
   - Maintainers will review your PR
   - Make requested changes
   - Respond to feedback

## Pull Request Guidelines

- **One feature per PR** - Keep changes focused
- **Updated tests** - Include tests for new functionality
- **Updated docs** - Update README or docs if needed
- **No breaking changes** - Maintain backward compatibility
- **Clean history** - Squash commits if necessary

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Refactoring

## Related Issues
Fixes #123

## Testing
Describe how you tested the changes

## Checklist
- [ ] My code follows PEP 8
- [ ] I have tested my changes
- [ ] I have updated documentation
- [ ] My commits have clear messages
```

## Areas for Contribution

### High Priority
- [ ] Authentication/Authorization
- [ ] Advanced search filtering
- [ ] Analytics dashboard
- [ ] Performance optimizations
- [ ] Test coverage improvement

### Medium Priority
- [ ] Multi-language support
- [ ] Email notifications
- [ ] Candidate portal
- [ ] Export functionality
- [ ] ATS integrations

### Good for Beginners
- [ ] Documentation improvements
- [ ] Bug fixes
- [ ] UI/UX enhancements
- [ ] Test additions
- [ ] Code cleanup

## Development Workflow

### Backend Development
```bash
# Activate venv
.venv\Scripts\activate

# Install in editable mode
pip install -e .

# Run backend
python -m uvicorn app.main:app --reload

# Run tests
pytest

# Run specific test
pytest tests/test_scorer.py::test_calculate_score
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev

# Build for production
npm run build

# Run tests (if configured)
npm test
```

## Debugging

### Backend Debugging
```python
# Add debug prints
print(f"DEBUG: variable = {variable}")

# Use debugger
import pdb; pdb.set_trace()

# Use logging
import logging
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

### Frontend Debugging
```javascript
// Browser DevTools
console.log("Debug:", variable);

// Use debugger
debugger;
```

## Common Issues

### Import Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`
- Check Python path is correct

### Database Errors
- Delete `data/hr_shortlisting.db` to reset
- Check SQLAlchemy models
- Verify database path in `.env`

### CORS Issues
- Check CORS settings in `app/main.py`
- Ensure frontend URL is in allowed origins
- Clear browser cache

### Module Not Found
```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall

# Check installed packages
pip list
```

## Documentation

### Code Documentation
- Add docstrings to all functions
- Include type hints
- Explain complex logic

Example:
```python
def calculate_skill_score(candidate: Dict, job: Dict) -> float:
    """
    Calculate skill match score between candidate and job.
    
    Args:
        candidate: Candidate dictionary with 'skills' key
        job: Job dictionary with 'required_skills' key
        
    Returns:
        float: Score between 0-100 representing skill match
        
    Example:
        >>> candidate = {'skills': ['python', 'sql']}
        >>> job = {'required_skills': ['python', 'r', 'sql']}
        >>> calculate_skill_score(candidate, job)
        66.67
    """
    # Implementation
```

### README Updates
- Update when adding features
- Include examples
- Keep formatting consistent
- Update table of contents

## Maintainer Responsibilities

If you become a maintainer:
- Review PRs in timely manner
- Be encouraging and helpful
- Maintain consistent standards
- Keep documentation updated
- Manage issues and milestones

## Recognition

Contributors will be:
- Added to CONTRIBUTORS.md
- Credited in releases
- Acknowledged in documentation

## Questions?

- **GitHub Issues** - Report bugs or request features
- **GitHub Discussions** - General questions
- **Email** - For security issues: security@example.com

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for making HR Shortlisting Agent better! 🎉
