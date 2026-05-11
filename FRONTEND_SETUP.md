# React Frontend Setup Guide

## What's Included

A complete React frontend with:
- ✅ Job description upload with parsing
- ✅ Batch resume upload
- ✅ Candidate evaluation and ranking display
- ✅ Detailed scoring breakdown (5 dimensions)
- ✅ Score override with audit trail
- ✅ Professional UI with responsive design
- ✅ Error handling and loading states
- ✅ Real-time API integration with FastAPI backend

## Installation Steps

### 1. Install Node.js
Download and install Node.js 16+ from https://nodejs.org/

### 2. Navigate to Frontend Directory
```bash
cd "c:\Users\sukhi\Desktop\Programming\RAG Pipleiiine TCI\frontend"
```

### 3. Install Dependencies
```bash
npm install
```

This installs:
- React & React DOM
- Vite (fast build tool)
- Axios (HTTP client)
- Vite React plugin

### 4. Start Development Server
```bash
npm run dev
```

Or use the provided batch file:
```bash
start.bat
```

The app will open at: **http://localhost:3000**

## Using the Application

### Step 1: Upload Job Description
1. Enter the job title (e.g., "Senior AI Engineer")
2. Select a job description file (PDF, DOCX, or TXT)
3. Click "Upload Job Description"

### Step 2: Upload Resumes
1. Select one or more resume files
2. Supported formats: PDF, DOCX, TXT, LinkedIn JSON export
3. Click "Upload Resumes"

### Step 3: Evaluate Candidates
1. Review the resumes uploaded
2. Click "Start Evaluation"
3. Wait for AI analysis (4-5 minutes for scoring)

### Step 4: Review Rankings
- See candidates ranked by composite score
- View detailed scoring breakdown per dimension
- Check recommendation (Hire/Review/No-Hire)
- Override scores if needed (with reason)

## Backend Prerequisite

The backend FastAPI server must be running:

```bash
cd "c:\Users\sukhi\Desktop\Programming\RAG Pipleiiine TCI"
python -m uvicorn app.main:app --reload
```

Frontend will show error if backend is not available.

## Project Structure

```
frontend/
├── public/
│   └── index.html          # Entry HTML
├── src/
│   ├── api/
│   │   └── client.js       # API service
│   ├── components/
│   │   ├── Header.jsx      # Top navigation
│   │   ├── JobUpload.jsx   # JD upload form
│   │   ├── ResumeUpload.jsx # Resume upload form
│   │   ├── EvaluationResults.jsx # Rankings display
│   │   ├── ScoreOverride.jsx    # Score modal
│   │   └── LoadingSpinner.jsx   # Loading indicator
│   ├── App.jsx             # Main app component
│   ├── App.css             # Global styles
│   ├── main.jsx            # Entry point
│   └── index.css           # Base styles
├── package.json            # Dependencies
├── vite.config.js          # Build config
├── README.md               # Frontend docs
└── start.bat              # Windows launcher
```

## Customization

### Change Backend URL
Edit `src/api/client.js`:
```javascript
const API_BASE = 'http://127.0.0.1:8000'  // Change this
```

### Modify Styling
All components have CSS files (e.g., `Header.css`, `App.css`).
CSS variables defined in root:
```css
:root {
  --primary: #2563eb;
  --success: #10b981;
  --danger: #ef4444;
  /* ... more colors ... */
}
```

## Building for Production

```bash
npm run build
```

Creates optimized production bundle in `dist/` folder.

Preview production build:
```bash
npm run preview
```

## Troubleshooting

### Port 3000 already in use
```bash
npm run dev -- --port 3001
```

### Backend connection errors
1. Verify FastAPI server running on port 8000
2. Check CORS enabled in backend (`app/main.py`)
3. Verify no firewall blocking connections

### Slow evaluation
- Embeddings take 4-5 minutes for 3 candidates
- This is normal (SentenceTransformer computation)
- Subsequent evaluations for same JD will use cached embeddings

### File upload fails
- Check file size (default max 25 MB)
- Ensure file format supported
- Try smaller test file first

## Features

✅ **Responsive Design** - Works on desktop and tablets  
✅ **Error Handling** - User-friendly error messages  
✅ **Loading States** - Visual feedback during processing  
✅ **Audit Trail** - Track all score overrides  
✅ **Professional UI** - Clean, modern design  
✅ **Fast Build** - Vite rebuilds in <1 second  

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Keyboard Shortcuts

- `Esc` - Close modal dialogs
- `Enter` - Submit forms

## Performance Tips

1. Upload resumes in batches of 5-10 for best performance
2. Use PDF files for faster parsing than images
3. Clear browser cache if experiencing stale data

## Need Help?

Check the backend logs for detailed error messages:
- Invalid file format errors
- API connection issues
- Database errors

All backend responses are displayed in the frontend error banner.
