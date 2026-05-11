import React, { useState } from 'react'
import './ResumeUpload.css'

function ResumeUpload({ onUpload }) {
  const [files, setFiles] = useState([])
  const [fileNames, setFileNames] = useState([])

  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files || [])
    setFiles(selectedFiles)
    setFileNames(selectedFiles.map(f => f.name))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (files.length === 0) {
      alert('Please select at least one resume')
      return
    }
    onUpload(files)
  }

  const removeFile = (index) => {
    const newFiles = files.filter((_, i) => i !== index)
    const newNames = fileNames.filter((_, i) => i !== index)
    setFiles(newFiles)
    setFileNames(newNames)
  }

  return (
    <div className="resume-upload">
      <div className="upload-card">
        <div className="upload-icon">📋</div>
        <h2>Upload Resumes</h2>
        <p>Upload candidate resumes (PDF, DOCX, TXT, or LinkedIn JSON exports)</p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Resume Files</label>
            <div className="file-input">
              <input
                type="file"
                id="resume-files"
                onChange={handleFileChange}
                accept=".pdf,.docx,.txt,.json"
                multiple
              />
              <label htmlFor="resume-files" className="file-input-label">
                <span>
                  📁 Click to upload multiple resumes or drag and drop
                </span>
              </label>
            </div>
          </div>

          {fileNames.length > 0 && (
            <div className="file-list">
              <h3>{fileNames.length} file(s) selected:</h3>
              <ul>
                {fileNames.map((name, index) => (
                  <li key={index}>
                    <span>{name}</span>
                    <button
                      type="button"
                      onClick={() => removeFile(index)}
                      className="remove-btn"
                    >
                      ✕
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          )}

          <button type="submit" className="btn btn-primary" disabled={files.length === 0}>
            Upload Resumes →
          </button>
        </form>
      </div>
    </div>
  )
}

export default ResumeUpload
