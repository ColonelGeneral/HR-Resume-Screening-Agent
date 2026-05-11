from app.services.parsing import parse_jd_text, parse_resume_text, parse_linkedin_json_profile


def test_parse_jd_extracts_skills():
    jd = "Hiring an AI Engineer with Python, FastAPI, SQL, and 3+ years of experience."
    parsed = parse_jd_text(jd, role_title="AI Engineer")
    assert "python" in parsed.required_skills
    assert parsed.role_title == "AI Engineer"
    assert parsed.experience_years == 3.0


def test_parse_resume_extracts_candidate_data():
    resume = """
    Jane Doe
    jane@example.com
    +91 9876543210
    Python FastAPI SQL Docker
    4 years of experience working as a software engineer.
    Built an AI recruitment dashboard project.
    """
    parsed = parse_resume_text(resume, source_name="resume.pdf")
    assert parsed.name == "Jane Doe"
    assert parsed.email == "jane@example.com"
    assert "python" in parsed.skills
    assert parsed.total_years_experience == 4.0


def test_parse_linkedin_json_profile():
    profile = parse_linkedin_json_profile(
        {
            "name": "John Doe",
            "headline": "Senior Python Developer",
            "skills": ["Python", "FastAPI"],
            "linkedin_url": "https://linkedin.com/in/john",
        }
    )
    assert profile.name == "John Doe"
    assert profile.linkedin_url.endswith("/john")
    assert "python" in profile.skills
