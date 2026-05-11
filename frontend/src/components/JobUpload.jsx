import React, { useState } from 'react'
import './JobUpload.css'

function JobUpload({ onUpload }) {
  const [file, setFile] = useState(null)
  const [roleTitle, setRoleTitle] = useState('')
  const [fileName, setFileName] = useState('')

  const handleFileChange = (e) => {
    const selectedFile = e.target.files?.[0]
    if (selectedFile) {
      setFile(selectedFile)
      setFileName(selectedFile.name)
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!file || !roleTitle.trim()) {
      alert('Please select a file and enter a role title')
      return
    }
    onUpload(file, roleTitle)
  }

  return (
    <div className="job-upload">
      <div className="upload-card">
        <div className="upload-icon">📄</div>
        <h2>Upload Job Description</h2>
        <p>Start by uploading the job description (PDF, DOCX, or TXT)</p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="role-title">Job Title</label>
            <input
              id="role-title"
              type="text"
              placeholder="e.g., Senior AI Engineer"
              value={roleTitle}
              onChange={(e) => setRoleTitle(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label>Job Description File</label>
            <div className="file-input">
              <input
                type="file"
                id="job-file"
                onChange={handleFileChange}
                accept=".pdf,.docx,.txt"
              />
              <label htmlFor="job-file" className="file-input-label">
                <span>
                  {fileName ? `✓ ${fileName}` : '📁 Click to upload or drag and drop'}
                </span>
              </label>
            </div>
          </div>

          <button type="submit" className="btn btn-primary">
            Upload Job Description →
          </button>
        </form>
      </div>
    </div>
  )
}

export default JobUpload
