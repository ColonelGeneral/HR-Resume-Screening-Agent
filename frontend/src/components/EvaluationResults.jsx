import React from 'react'
import './EvaluationResults.css'

function EvaluationResults({ rankings, jobTitle, onOverride }) {
  if (!rankings || rankings.length === 0) {
    return (
      <div className="no-results">
        <p>No rankings available</p>
      </div>
    )
  }

  const getRecommendationColor = (recommendation) => {
    switch (recommendation) {
      case 'Hire':
        return 'hire'
      case 'Review':
        return 'review'
      case 'No-Hire':
        return 'no-hire'
      default:
        return 'review'
    }
  }

  const getScoreColor = (score) => {
    if (score >= 70) return '#10b981'
    if (score >= 55) return '#f59e0b'
    return '#ef4444'
  }

  return (
    <div className="evaluation-results">
      <div className="results-header">
        <h2>Evaluation Results for {jobTitle}</h2>
        <p>Candidates ranked by composite score</p>
      </div>

      <div className="rankings-container">
        {rankings.map((ranking, index) => (
          <div key={ranking.candidate_id} className="ranking-card">
            <div className="ranking-header">
              <span className="rank-badge">#{index + 1}</span>
              <h3>{ranking.candidate_name}</h3>
              <span className={`recommendation ${getRecommendationColor(ranking.recommendation)}`}>
                {ranking.recommendation}
              </span>
            </div>

            <div className="score-section">
              <div className="score-display">
                <div
                  className="score-circle"
                  style={{ borderColor: getScoreColor(ranking.total_score) }}
                >
                  <span className="score-text">{ranking.total_score.toFixed(1)}</span>
                  <span className="score-label">Score</span>
                </div>
                <div className="confidence">
                  Confidence: <strong>{(ranking.confidence * 100).toFixed(0)}%</strong>
                </div>
              </div>
            </div>

            <div className="dimensions">
              <h4>Scoring Breakdown</h4>
              {ranking.scores && Object.entries(ranking.scores).map(([key, value]) => (
                <div key={key} className="dimension">
                  <div className="dimension-header">
                    <span className="dimension-name">
                      {key.replace(/_/g, ' ').split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
                    </span>
                    <span className="dimension-value">
                      {value.score.toFixed(1)}/10 ({value.weight}%)
                    </span>
                  </div>
                  <div className="dimension-bar">
                    <div
                      className="dimension-fill"
                      style={{
                        width: `${(value.score / 10) * 100}%`,
                        background: getScoreColor((value.score / 10) * 100)
                      }}
                    ></div>
                  </div>
                  <p className="dimension-justification">{value.justification}</p>
                  {value.evidence && value.evidence.length > 0 && (
                    <div className="evidence">
                      <strong>Evidence:</strong> {value.evidence.slice(0, 5).join(', ')}
                      {value.evidence.length > 5 && '...'}
                    </div>
                  )}
                </div>
              ))}
            </div>

            <div className="rationale">
              <strong>Rationale:</strong>
              <ul>
                {ranking.rationale?.map((r, i) => (
                  <li key={i}>{r}</li>
                ))}
              </ul>
            </div>

            <button
              className="btn btn-secondary"
              onClick={() => onOverride(ranking)}
            >
              Override Score
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}

export default EvaluationResults
