import React from 'react'
import './Header.css'

function Header({ onPrimaryAction }) {
  return (
    <header className="header header-sticky">
      <div className="header-content">
        <a className="brand" href="#top" onClick={(event) => event.preventDefault()}>
          <div className="brand-mark">HR</div>
          <div>
            <h1>HR Shortlisting Agent</h1>
            <p>Transparent resume and LinkedIn screening</p>
          </div>
        </a>
        <nav className="header-nav" aria-label="Primary navigation">
          <a href="#workflow" onClick={(event) => {
            event.preventDefault()
            onPrimaryAction?.()
          }}>
            Upload Criteria
          </a>
          <a href="#landing" onClick={(event) => event.preventDefault()}>
            Landing
          </a>
        </nav>
        <div className="header-actions">
          <div className="status-badge">
            <span className="status-dot"></span>
            Live
          </div>
          <button className="btn btn-primary header-cta" onClick={onPrimaryAction}>
            Upload Criteria
          </button>
        </div>
      </div>
    </header>
  )
}

export default Header
