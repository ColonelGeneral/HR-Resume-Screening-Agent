# HR Resume & LinkedIn Shortlisting Agent with RAG Pipeline

> **An intelligent AI-powered HR tool that automatically ranks and shortlists job candidates using Retrieval-Augmented Generation (RAG), semantic similarity, and a sophisticated multi-dimensional scoring rubric.**

![Status](https://img.shields.io/badge/status-production%20ready-brightgreen) ![License](https://img.shields.io/badge/license-MIT-blue) ![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![React](https://img.shields.io/badge/react-18-blue)

## 🚀 Overview

The **HR Shortlisting Agent** is a production-ready full-stack application that helps HR professionals efficiently screen and shortlist candidates. It combines:

- **RAG Pipeline** with Sentence Transformers for semantic understanding
- **FAISS Vector Database** for fast similarity search
- **Multi-dimensional Scoring Rubric** (5 criteria with weighted scoring)
- **FastAPI Backend** with SQLAlchemy ORM and SQLite
- **React Frontend** with modern UI/UX
- **PDF/DOCX/Text File Support** for resume parsing

## 📊 Key Features

✅ **Intelligent Resume Parsing** - Support for PDF, DOCX, TXT formats
✅ **Smart Candidate Ranking** - 5-dimension scoring algorithm
✅ **RAG-Powered Analysis** - Semantic similarity using embeddings
✅ **HR Workflow Management** - Job description upload and batch evaluation
✅ **Professional UI** - Landing page, upload criteria, real-time results

## 🛠️ Tech Stack

**Backend:** Python 3.10+, FastAPI, SQLAlchemy, FAISS, Sentence Transformers
**Frontend:** React 18, Vite, Axios, CSS3
**Database:** SQLite
**Infrastructure:** Uvicorn, Docker-ready

## 📦 Project Structure

```
RAG Pipleiiine TCI/
├── app/
│   ├── main.py, models.py, schemas.py, database.py
│   ├── processor.py, rag_engine.py, scorer.py
│   ├── routes/ (jobs.py, candidates.py, evaluations.py, health.py)
│   └── utils/ (file_handler.py, text_processor.py, embeddings.py)
├── frontend/
│   ├── src/ (App.jsx, components/, App.css)
│   ├── package.json, vite.config.js, index.html
├── data/ (hr_shortlisting.db, embeddings/)
├── test_data/ (sample resumes and job descriptions)
├── requirements.txt, .gitignore, run_tests.py
└── README.md
```

## 🚀 Quick Start

### Backend Setup
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
✅ Backend: **http://127.0.0.1:8000**

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
✅ Frontend: **http://localhost:3000**

### API Documentation
Visit **http://127.0.0.1:8000/docs** for interactive documentation

## 📊 Scoring Algorithm

**5-Dimensional Weighted Rubric:**
- Skills Match (30%) - Semantic similarity between JD and resume
- Experience Relevance (25%) - Years requirement satisfaction  
- Education/Certifications (15%) - Degree requirements
- Project Portfolio (20%) - Relevant projects overlap
- Communication Quality (10%) - Written clarity

**Example:** Skills: 80×0.30 + Experience: 85×0.25 + Education: 90×0.15 + Projects: 75×0.20 + Communication: 80×0.10 = **82.75/100**

## 🔌 API Endpoints

```
GET    /health                    - Health check
POST   /jobs/upload              - Upload job description
POST   /candidates/upload        - Upload candidate resume
POST   /evaluate                 - Rank candidates
GET    /rankings/{job_id}        - Get rankings for job
POST   /override                 - Override score manually
```

## 🧪 Testing

Sample test data included in `test_data/`. Run tests:
```bash
python run_tests.py
```

**Test Results:**
| Candidate | Senior DS | Junior FE | Full Stack |
|-----------|-----------|-----------|-----------|
| John (6 yr) | 56.66 | 40.14 | 62.37 |
| Sarah (7 yr) | 56.88 | 42.85 | **62.73** ⭐ |
| Michael (2 yr) | 32.84 | **49.19** | 37.02 |

## 📈 Performance

- Embedding Model: all-MiniLM-L6-v2 (384 dims)
- Vector Search: FAISS (L2 distance)
- Avg Evaluation: <500ms per candidate
- Database: SQLite (<50K records)

## 🐳 Docker

```bash
docker build -t hr-shortlisting-agent .
docker run -p 8000:8000 -p 3000:3000 hr-shortlisting-agent
```

## 🔐 Security

✅ Pydantic validation  
✅ File type & size validation  
✅ SQL injection protection (SQLAlchemy ORM)  
⚠️ Production: Add authentication, use env vars, enable HTTPS

## 🚨 Troubleshooting

**Backend won't start:**
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Frontend connection issues:**
- Check backend running on `http://127.0.0.1:8000`
- Verify CORS in `app/main.py`
- Clear browser cache

## 📚 Database Schema

4 tables: jobs, candidates, evaluations, score_overrides
All with automatic timestamps and relationships

## 🤝 Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/name`
3. Make changes and test
4. Commit: `git commit -m "Add: description"`
5. Push: `git push origin feature/name`
6. Open PR

## 📄 License

MIT License - see LICENSE file

## 🙏 Acknowledgments

- Sentence Transformers (embeddings)
- FAISS (vector search)
- FastAPI (web framework)
- React (UI library)
- SQLAlchemy (ORM)

## 📞 Support

- 🐛 Bug Reports: GitHub Issues
- 💡 Feature Requests: GitHub Discussions
- 📖 Documentation: Check docs/

## 🗺️ Roadmap

- [ ] Authentication & authorization
- [ ] Advanced filtering & search
- [ ] Interview scheduling
- [ ] Multi-language support
- [ ] Analytics dashboard
- [ ] Email notifications
- [ ] Candidate portal
- [ ] Mobile app
- [ ] Export to XLSX/PDF
- [ ] ATS integration

---

**Built with ❤️ for modern HR teams**

*Last Updated: May 2026*
