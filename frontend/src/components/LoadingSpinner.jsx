import React from 'react'
import './LoadingSpinner.css'

function LoadingSpinner() {
  return (
    <div className="loading-backdrop">
      <div className="spinner">
        <div className="spinner-circle"></div>
        <p>Processing...</p>
      </div>
    </div>
  )
}

export default LoadingSpinner
