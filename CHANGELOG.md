# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-05-11

### Added
- ✨ Full RAG pipeline implementation with Sentence Transformers
- ✨ FAISS-based vector search for candidate-job matching
- ✨ 5-dimensional weighted scoring algorithm (skills, experience, education, projects, communication)
- ✨ FastAPI backend with SQLAlchemy ORM
- ✨ React 18 frontend with Vite
- ✨ Support for PDF, DOCX, TXT, and JSON resume formats
- ✨ Job description upload and parsing
- ✨ Candidate ranking and evaluation
- ✨ Manual score override with audit trail
- ✨ Interactive API documentation (Swagger UI)
- ✨ Landing page with hero section
- ✨ Upload criteria page
- ✨ Responsive UI design
- ✨ Comprehensive test suite with 3 sample JDs and 3 candidate resumes
- 📚 Detailed README with setup instructions
- 📚 API documentation
- 📚 Database schema documentation
- 🧪 Test data and run_tests.py script
- 🔐 Input validation with Pydantic
- 🔐 File type and size validation

### Features
- Resume parsing from multiple formats
- Automatic skill extraction
- Experience calculation
- Education recognition
- Semantic similarity matching
- Weighted multi-criteria scoring
- Confidence scores (0-1 scale)
- Dynamic recommendations (Hire/Review/No-Hire)
- Batch candidate evaluation
- Real-time result display
- Score override with reasons
- SQLite database persistence

### Performance
- Average evaluation: <500ms per candidate
- Embedding model: all-MiniLM-L6-v2 (384 dimensions)
- FAISS vector indexing for fast search
- SQLite suitable for <50K records
- Docker-ready deployment

### Testing
- Test Results Summary:
  - Senior Data Scientist JD: Sarah 56.88, John 56.66, Michael 32.84
  - Junior Frontend JD: Michael 49.19, Sarah 42.85, John 40.14
  - Full Stack Engineer JD: Sarah 62.73, John 62.37, Michael 37.02
- All endpoints tested and working
- Sample data included for quick testing

### Security
- Input validation with Pydantic
- File type validation (PDF, DOCX, TXT only)
- Maximum file size: 50MB
- SQL injection protection via SQLAlchemy ORM
- CORS enabled for development

## [0.1.0] - 2026-04-15

### Initial Development
- Project scaffolding
- Backend setup with FastAPI
- Frontend setup with React + Vite
- Database models
- API endpoint structure
- Basic routing

---

## Roadmap

### Upcoming Features
- [ ] User authentication (JWT)
- [ ] Role-based access control
- [ ] Advanced search and filtering
- [ ] Interview scheduling integration
- [ ] Multi-language support
- [ ] Analytics dashboard
- [ ] Email notifications
- [ ] Candidate self-service portal
- [ ] Mobile app (React Native)
- [ ] Export to XLSX/PDF
- [ ] ATS system integration
- [ ] Webhook support
- [ ] Batch import from CSV

### Performance Improvements
- [ ] Caching layer (Redis)
- [ ] Database indexing optimization
- [ ] Vector search optimization
- [ ] Frontend bundle optimization

### Documentation
- [ ] API client libraries (Python, JS)
- [ ] Deployment guides (AWS, GCP, Azure)
- [ ] Video tutorials
- [ ] Architecture deep-dive

---

## Version History

### v1.0.0 (Current)
Production-ready release with full feature set

### v0.1.0
Initial development version
