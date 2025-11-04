import React, { useState, useEffect } from 'react'
import './popup.css'

interface StorageData {
  count: number
  enabled: boolean
}

const Popup: React.FC = () => {
  const [count, setCount] = useState<number>(0)
  const [enabled, setEnabled] = useState<boolean>(true)
  const [currentUrl, setCurrentUrl] = useState<string>('')

  useEffect(() => {
    // Load data from Chrome storage
    chrome.storage.sync.get(['count', 'enabled'], (result) => {
      setCount(result.count || 0)
      setEnabled(result.enabled !== false)
    })

    // Get current tab URL
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]?.url) {
        setCurrentUrl(tabs[0].url)
      }
    })
  }, [])

  const incrementCount = () => {
    const newCount = count + 1
    setCount(newCount)
    chrome.storage.sync.set({ count: newCount })

    // Send message to background script
    chrome.runtime.sendMessage({
      type: 'COUNT_UPDATED',
      count: newCount,
    })
  }

  const toggleEnabled = () => {
    const newEnabled = !enabled
    setEnabled(newEnabled)
    chrome.storage.sync.set({ enabled: newEnabled })

    // Send message to content script
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]?.id) {
        chrome.tabs.sendMessage(tabs[0].id, {
          type: 'TOGGLE_FEATURE',
          enabled: newEnabled,
        })
      }
    })
  }

  const openOptions = () => {
    chrome.runtime.openOptionsPage()
  }

  return (
    <div className="popup-container">
      <header className="popup-header">
        <h1>{{extension_name}}</h1>
      </header>

      <main className="popup-main">
        <div className="info-section">
          <p className="current-url">
            <strong>Current Page:</strong>
            <br />
            <span className="url-text">{currentUrl}</span>
          </p>
        </div>

        <div className="counter-section">
          <h2>Counter: {count}</h2>
          <button onClick={incrementCount} className="btn btn-primary">
            Increment
          </button>
        </div>

        <div className="toggle-section">
          <label className="toggle-label">
            <input
              type="checkbox"
              checked={enabled}
              onChange={toggleEnabled}
              className="toggle-input"
            />
            <span className="toggle-slider"></span>
            <span className="toggle-text">
              Feature {enabled ? 'Enabled' : 'Disabled'}
            </span>
          </label>
        </div>

        <div className="actions-section">
          <button onClick={openOptions} className="btn btn-secondary">
            Open Options
          </button>
        </div>
      </main>

      <footer className="popup-footer">
        <p>v1.0.0</p>
      </footer>
    </div>
  )
}

export default Popup
