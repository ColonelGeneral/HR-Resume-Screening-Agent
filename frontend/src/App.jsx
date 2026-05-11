import React, { useState, useEffect, useRef } from 'react'
import api from './api/client'
import './App.css'
import Header from './components/Header'
import JobUpload from './components/JobUpload'
import ResumeUpload from './components/ResumeUpload'
import EvaluationResults from './components/EvaluationResults'
import ScoreOverride from './components/ScoreOverride'
import LoadingSpinner from './components/LoadingSpinner'
import UploadCriteria from './components/UploadCriteria'

function App() {
  const workflowRef = useRef(null)
  const [currentStep, setCurrentStep] = useState('landing')
  const [jobId, setJobId] = useState(null)
  const [jobTitle, setJobTitle] = useState('')
  const [requiredSkills, setRequiredSkills] = useState([])
  const [experienceYears, setExperienceYears] = useState(0)
  const [candidates, setCandidates] = useState([])
  const [rankings, setRankings] = useState([])
  const [loading, setLoading] = useState(false)
  const [selectedEvaluation, setSelectedEvaluation] = useState(null)
  const [showOverrideModal, setShowOverrideModal] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    // Check backend health on mount
    api.checkHealth()
      .catch(() => setError('Backend server is not running'))
  }, [])

  const handleJobUpload = async (file, roleTitle) => {
    try {
      setLoading(true)
      setError(null)
      const response = await api.uploadJob(file, roleTitle)
      
      setJobId(response.data.job_id)
      setJobTitle(response.data.role_title)
      setRequiredSkills(response.data.required_skills || [])
      setExperienceYears(response.data.experience_years || 0)
      setCurrentStep('resume')
    } catch (err) {
      setError(`Job upload failed: ${err.response?.data?.detail || err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const handleResumeUpload = async (files) => {
    try {
      setLoading(true)
      setError(null)
      const response = await api.uploadCandidates(files)
      
      setCandidates(response.data.records || [])
      setCurrentStep('evaluate')
    } catch (err) {
      setError(`Resume upload failed: ${err.response?.data?.detail || err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const handleEvaluate = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await api.evaluateCandidates(jobId)
      
      setRankings(response.data.rankings || [])
      setCurrentStep('results')
    } catch (err) {
      setError(`Evaluation failed: ${err.response?.data?.detail || err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const handleOverrideScore = async (evaluationId, reviewer, newScore, reason) => {
    try {
      setLoading(true)
      setError(null)
      await api.overrideScore(evaluationId, reviewer, newScore, reason)
      
      // Refresh rankings
      const response = await api.getRankings(jobId)
      setRankings(response.data.rankings || [])
      setShowOverrideModal(false)
    } catch (err) {
      setError(`Override failed: ${err.response?.data?.detail || err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setCurrentStep('landing')
    setJobId(null)
    setJobTitle('')
    setRequiredSkills([])
    setExperienceYears(0)
    setCandidates([])
    setRankings([])
    setSelectedEvaluation(null)
    setShowOverrideModal(false)
    setError(null)
  }

  const goToCriteria = () => {
    setCurrentStep('criteria')
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const goToWorkflow = () => {
    setCurrentStep('job')
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <div className="app">
      <Header onPrimaryAction={goToCriteria} />

      {currentStep === 'landing' && (
        <section className="hero-section" aria-label="Landing page">
          <div className="hero-content">
            <div className="hero-copy">
              <span className="hero-badge">HR Hiring Intelligence</span>
              <h1>Screen resumes and LinkedIn profiles with transparent scoring.</h1>
              <p>
                Upload a job description, add candidate profiles, and get a ranked shortlist with
                clear evidence for every recommendation.
              </p>
              <div className="hero-actions">
                <button className="btn btn-primary" onClick={goToCriteria}>
                  Go to Upload Criteria
                </button>
                <button className="btn btn-ghost" onClick={goToCriteria}>
                  View Upload Criteria
                </button>
              </div>
              <div className="hero-stats">
                <div>
                  <strong>5</strong>
                  <span>scoring dimensions</span>
                </div>
                <div>
                  <strong>6</strong>
                  <span>API endpoints</span>
                </div>
                <div>
                  <strong>100%</strong>
                  <span>auditable decisions</span>
                </div>
              </div>
            </div>
            <div className="hero-panel">
              <h2>How it works</h2>
              <ol>
                <li>Review the upload criteria first</li>
                <li>Upload a job description</li>
                <li>Upload resumes or LinkedIn exports</li>
                <li>Review ranked candidates</li>
              </ol>
            </div>
          </div>

          <div className="landing-highlights">
            <article>
              <span>01</span>
              <h3>Transparent scoring</h3>
              <p>Every match is explained with evidence, weights, and reviewer overrides.</p>
            </article>
            <article>
              <span>02</span>
              <h3>HR-friendly workflow</h3>
              <p>Upload criteria first, then move into the structured candidate intake flow.</p>
            </article>
            <article>
              <span>03</span>
              <h3>Built for review</h3>
              <p>Rankings, confidence scores, and override actions stay auditable end-to-end.</p>
            </article>
          </div>
        </section>
      )}

      {currentStep === 'criteria' && (
        <section className="criteria-shell" aria-label="Upload criteria page">
          <UploadCriteria onContinue={goToWorkflow} onBack={() => setCurrentStep('landing')} />
        </section>
      )}
      
      {error && (
        <div className="error-banner">
          <span>{error}</span>
          <button onClick={() => setError(null)}>×</button>
        </div>
      )}

      {loading && <LoadingSpinner />}

      {currentStep !== 'landing' && currentStep !== 'criteria' && (
        <main className="container" ref={workflowRef} id="workflow">
          {currentStep === 'job' && (
            <JobUpload onUpload={handleJobUpload} />
          )}

          {currentStep === 'resume' && (
            <>
              <div className="step-info">
                <h3>Job Uploaded: {jobTitle}</h3>
                <p>Required Skills: {requiredSkills.slice(0, 5).join(', ')}...</p>
                <p>Experience: {experienceYears}+ years</p>
              </div>
              <ResumeUpload onUpload={handleResumeUpload} />
            </>
          )}

          {currentStep === 'evaluate' && (
            <>
              <div className="step-info">
                <h3>Resumes Uploaded</h3>
                <p>{candidates.length} candidates ready for evaluation</p>
              </div>
              <button className="btn btn-primary" onClick={handleEvaluate}>
                Start Evaluation
              </button>
            </>
          )}

          {currentStep === 'results' && (
            <>
              <EvaluationResults 
                rankings={rankings}
                jobTitle={jobTitle}
                onOverride={(evaluation) => {
                  setSelectedEvaluation(evaluation)
                  setShowOverrideModal(true)
                }}
              />
              <button className="btn btn-secondary" onClick={handleReset}>
                Evaluate New Job
              </button>
            </>
          )}
        </main>
      )}

      {showOverrideModal && selectedEvaluation && (
        <ScoreOverride
          evaluation={selectedEvaluation}
          onSubmit={handleOverrideScore}
          onClose={() => {
            setShowOverrideModal(false)
            setSelectedEvaluation(null)
          }}
        />
      )}
    </div>
  )
}

export default App
