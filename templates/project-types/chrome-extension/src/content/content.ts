// Content script - runs in the context of web pages

console.log('{{extension_name}} content script loaded')

// Load extension state
let isEnabled = true

chrome.storage.sync.get(['enabled'], (result) => {
  isEnabled = result.enabled !== false
  if (isEnabled) {
    initialize()
  }
})

// Initialize content script functionality
function initialize() {
  console.log('Initializing content script features')

  // Example: Add a floating button to the page
  createFloatingButton()

  // Example: Observe DOM changes
  observeDOMChanges()

  // Example: Add custom styles
  injectStyles()
}

// Create a floating button
function createFloatingButton() {
  const button = document.createElement('div')
  button.id = 'extension-floating-button'
  button.textContent = '{{extension_name}}'
  button.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    padding: 10px 20px;
    background: #4285f4;
    color: white;
    border-radius: 5px;
    cursor: pointer;
    z-index: 10000;
    font-family: Arial, sans-serif;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
  `

  button.addEventListener('click', () => {
    // Send message to background script
    chrome.runtime.sendMessage({
      type: 'BUTTON_CLICKED',
      url: window.location.href,
    })

    alert('{{extension_name}} button clicked!')
  })

  document.body.appendChild(button)
}

// Observe DOM changes
function observeDOMChanges() {
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.type === 'childList') {
        // Handle new nodes
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === Node.ELEMENT_NODE) {
            // Process new elements
            processElement(node as Element)
          }
        })
      }
    })
  })

  observer.observe(document.body, {
    childList: true,
    subtree: true,
  })
}

// Process an element
function processElement(element: Element) {
  // Example: Highlight specific elements
  if (element.tagName === 'A') {
    // Process links
  }
}

// Inject custom styles
function injectStyles() {
  const style = document.createElement('style')
  style.textContent = `
    .extension-highlight {
      background-color: yellow !important;
      border: 2px solid orange !important;
    }
  `
  document.head.appendChild(style)
}

// Listen for messages from popup or background
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('Content script received message:', message)

  switch (message.type) {
    case 'TOGGLE_FEATURE':
      isEnabled = message.enabled
      if (isEnabled) {
        initialize()
      } else {
        cleanup()
      }
      sendResponse({ success: true })
      break

    case 'GET_PAGE_DATA':
      // Extract and send page data
      sendResponse({
        title: document.title,
        url: window.location.href,
        textContent: document.body.innerText.substring(0, 1000),
      })
      break

    case 'HIGHLIGHT_TEXT':
      highlightText(message.text)
      sendResponse({ success: true })
      break

    default:
      console.warn('Unknown message type:', message.type)
  }

  return true // Keep message channel open for async response
})

// Highlight text on the page
function highlightText(searchText: string) {
  const walker = document.createTreeWalker(
    document.body,
    NodeFilter.SHOW_TEXT,
    null
  )

  const textNodes: Node[] = []
  let node

  while ((node = walker.nextNode())) {
    if (node.textContent?.includes(searchText)) {
      textNodes.push(node)
    }
  }

  textNodes.forEach((textNode) => {
    const parent = textNode.parentElement
    if (parent) {
      const span = document.createElement('span')
      span.className = 'extension-highlight'
      span.textContent = textNode.textContent
      parent.replaceChild(span, textNode)
    }
  })
}

// Cleanup when disabled
function cleanup() {
  console.log('Cleaning up content script')

  // Remove floating button
  const button = document.getElementById('extension-floating-button')
  if (button) {
    button.remove()
  }

  // Remove highlights
  document.querySelectorAll('.extension-highlight').forEach((el) => {
    const text = el.textContent
    const textNode = document.createTextNode(text || '')
    el.parentNode?.replaceChild(textNode, el)
  })
}

// Page load complete
window.addEventListener('load', () => {
  console.log('Page loaded, content script ready')
})

// Export for testing
export {}
