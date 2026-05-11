# HR Shortlisting Agent - React Frontend

A modern React frontend for the HR Resume & LinkedIn Shortlisting Agent.

## Quick Start

### Prerequisites
- Node.js 16+ and npm

### Installation & Development

```bash
cd frontend
npm install
npm run dev
```

The app will run on `http://localhost:3000`

### Build for Production

```bash
npm run build
npm run preview
```

## Features

- **Job Upload**: Upload and parse job descriptions with automatic skill extraction
- **Resume Batch Upload**: Upload multiple candidate resumes at once
- **Intelligent Evaluation**: AI-powered candidate ranking based on 5-dimensional rubric
- **Score Details**: View detailed scoring breakdowns for each candidate
- **Score Override**: HR reviewers can override AI scores with audit trails
- **Real-time Rankings**: Sort candidates by score, recommendation, and confidence

## Architecture

### Components
- `Header.jsx` - Application header with status
- `JobUpload.jsx` - Job description upload form
- `ResumeUpload.jsx` - Resume batch upload form
- `EvaluationResults.jsx` - Rankings display with scoring details
- `ScoreOverride.jsx` - Modal for score adjustment
- `LoadingSpinner.jsx` - Loading indicator

### Services
- `api/client.js` - Axios client for backend API calls

### Styling
- CSS files co-located with components
- Responsive design with mobile support
- Theme variables for consistent styling

## API Integration

The frontend connects to the FastAPI backend at `http://127.0.0.1:8000`

### Endpoints Used
- `GET /health` - Health check
- `POST /jobs/upload` - Upload job description
- `POST /candidates/upload` - Upload resumes
- `POST /evaluate` - Run evaluation
- `GET /rankings/{job_id}` - Get rankings
- `POST /override` - Override score

## Troubleshooting

### Backend Connection Issues
If you see "Backend server is not running", ensure:
1. FastAPI server is running on port 8000
2. CORS is enabled on the backend
3. Both frontend and backend are on `localhost`

### File Upload Issues
- Maximum file size: Check backend `MAX_UPLOAD_MB` setting
- Supported formats: PDF, DOCX, TXT, JSON (LinkedIn export)
- Use drag-and-drop or click to select multiple files

## Performance

- Embeddings generation takes ~4 minutes for 3 candidates
- Parallel resume upload processing
- Results cached in browser memory during session

## Browser Support

- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)
