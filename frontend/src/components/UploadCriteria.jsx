import React from 'react'
import './UploadCriteria.css'

function UploadCriteria({ onContinue, onBack }) {
  const criteriaGroups = [
    {
      title: 'Accepted files',
      items: ['PDF resumes and job descriptions', 'DOCX documents', 'Plain text files', 'LinkedIn JSON exports']
    },
    {
      title: 'What to include',
      items: ['Candidate name and contact details', 'Skills, roles, and years of experience', 'Education and certifications', 'Projects, publications, and achievements']
    },
    {
      title: 'Before upload',
      items: ['Keep files under the configured upload limit', 'Use a single JD for one evaluation batch', 'Prefer text-based PDFs when possible', 'Remove sensitive data you do not want stored']
    }
  ]

  return (
    <section className="criteria-page">
      <div className="criteria-header">
        <div>
          <span className="criteria-chip">Upload criteria</span>
          <h2>Read these requirements before uploading any files.</h2>
          <p>
            This page is the first stop after the landing page. It explains exactly what can be uploaded,
            what the parser expects, and how to keep the workflow accurate.
          </p>
        </div>
        <button className="btn btn-primary" onClick={onContinue}>
          Continue to Upload
        </button>
      </div>

      <div className="criteria-grid">
        {criteriaGroups.map((group) => (
          <article className="criteria-card" key={group.title}>
            <h3>{group.title}</h3>
            <ul>
              {group.items.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </article>
        ))}
      </div>

      <div className="criteria-actions">
        <button className="btn btn-ghost" onClick={onBack}>
          Back to Landing
        </button>
        <button className="btn btn-secondary" onClick={onContinue}>
          Open Upload Flow
        </button>
      </div>
    </section>
  )
}

export default UploadCriteria