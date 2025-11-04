// Background service worker for Chrome Extension
// Manifest V3 uses service workers instead of background pages

// Installation handler
chrome.runtime.onInstalled.addListener((details) => {
  console.log('Extension installed:', details.reason)

  // Set default values
  chrome.storage.sync.set({
    count: 0,
    enabled: true,
  })

  // Create context menu
  chrome.contextMenus.create({
    id: 'main-menu',
    title: '{{extension_name}}',
    contexts: ['all'],
  })

  chrome.contextMenus.create({
    id: 'toggle-feature',
    title: 'Toggle Feature',
    contexts: ['all'],
    parentId: 'main-menu',
  })
})

// Context menu click handler
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'toggle-feature' && tab?.id) {
    chrome.storage.sync.get(['enabled'], (result) => {
      const newEnabled = !result.enabled
      chrome.storage.sync.set({ enabled: newEnabled })

      // Notify content script
      chrome.tabs.sendMessage(tab.id!, {
        type: 'TOGGLE_FEATURE',
        enabled: newEnabled,
      })
    })
  }
})

// Message handler from popup or content scripts
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('Message received:', message)

  switch (message.type) {
    case 'COUNT_UPDATED':
      console.log('Count updated to:', message.count)
      // Perform any background tasks here
      sendResponse({ success: true })
      break

    case 'GET_DATA':
      chrome.storage.sync.get(null, (data) => {
        sendResponse({ data })
      })
      return true // Keep message channel open for async response

    default:
      console.warn('Unknown message type:', message.type)
  }
})

// Keyboard command handler
chrome.commands.onCommand.addListener((command) => {
  console.log('Command received:', command)

  if (command === 'toggle_feature') {
    chrome.storage.sync.get(['enabled'], (result) => {
      const newEnabled = !result.enabled
      chrome.storage.sync.set({ enabled: newEnabled })

      // Notify all tabs
      chrome.tabs.query({}, (tabs) => {
        tabs.forEach((tab) => {
          if (tab.id) {
            chrome.tabs.sendMessage(tab.id, {
              type: 'TOGGLE_FEATURE',
              enabled: newEnabled,
            })
          }
        })
      })
    })
  }
})

// Tab update handler
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete') {
    console.log('Tab updated:', tab.url)
    // Perform actions when tab is loaded
  }
})

// Storage change listener
chrome.storage.onChanged.addListener((changes, areaName) => {
  console.log('Storage changed:', changes, 'in', areaName)

  // React to storage changes
  if (changes.enabled) {
    console.log(
      'Feature enabled changed from',
      changes.enabled.oldValue,
      'to',
      changes.enabled.newValue
    )
  }
})

// Alarm handler (for periodic tasks)
chrome.alarms.onAlarm.addListener((alarm) => {
  console.log('Alarm triggered:', alarm.name)

  if (alarm.name === 'periodic-task') {
    // Perform periodic task
    performPeriodicTask()
  }
})

// Create a periodic alarm (runs every 5 minutes)
chrome.alarms.create('periodic-task', {
  periodInMinutes: 5,
})

// Example periodic task
async function performPeriodicTask() {
  console.log('Performing periodic task...')
  // Add your periodic logic here
}

// Export for testing (if needed)
export {}
