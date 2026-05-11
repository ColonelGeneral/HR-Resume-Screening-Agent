import React, { useState } from 'react'
import './ScoreOverride.css'

function ScoreOverride({ evaluation, onSubmit, onClose }) {
  const [reviewer, setReviewer] = useState('')
  const [newScore, setNewScore] = useState(evaluation.total_score)
  const [reason, setReason] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!reviewer.trim() || !reason.trim()) {
      alert('Please fill in all fields')
      return
    }
    onSubmit(evaluation.candidate_id, reviewer, newScore, reason)
  }

  return (
    <div className="override-modal-backdrop" onClick={onClose}>
      <div className="override-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Override Score</h2>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>

        <div className="modal-body">
          <div className="candidate-info">
            <h3>{evaluation.candidate_name}</h3>
            <div className="score-comparison">
              <div className="old-score">
                <span className="label">Current Score</span>
                <span className="value">{evaluation.total_score.toFixed(1)}</span>
              </div>
              <span className="arrow">→</span>
              <div className="new-score">
                <span className="label">New Score</span>
                <span className="value">{newScore.toFixed(1)}</span>
              </div>
            </div>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="reviewer">Your Name</label>
              <input
                id="reviewer"
                type="text"
                placeholder="e.g., HR Manager"
                value={reviewer}
                onChange={(e) => setReviewer(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label htmlFor="score">New Score</label>
              <div className="score-input-container">
                <input
                  id="score"
                  type="range"
                  min="0"
                  max="100"
                  value={newScore}
                  onChange={(e) => setNewScore(parseFloat(e.target.value))}
                  className="score-slider"
                />
                <input
                  type="number"
                  min="0"
                  max="100"
                  step="0.1"
                  value={newScore}
                  onChange={(e) => setNewScore(parseFloat(e.target.value) || 0)}
                  className="score-input"
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="reason">Reason for Override</label>
              <textarea
                id="reason"
                placeholder="Explain why you're adjusting this score..."
                value={reason}
                onChange={(e) => setReason(e.target.value)}
                rows="4"
              />
            </div>

            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" onClick={onClose}>
                Cancel
              </button>
              <button type="submit" className="btn btn-primary">
                Apply Override
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

export default ScoreOverride
