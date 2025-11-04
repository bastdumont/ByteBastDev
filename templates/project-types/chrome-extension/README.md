# {{extension_name}} - Chrome Extension

A production-ready Chrome Extension built with TypeScript, React, and Manifest V3.

## Features

- ✅ **Manifest V3** compliant
- ✅ **TypeScript** for type safety
- ✅ **React 18** for popup UI
- ✅ **Webpack** for bundling
- ✅ **Background service worker**
- ✅ **Content scripts**
- ✅ **Options page**
- ✅ **Chrome Storage API**
- ✅ **Message passing**
- ✅ **Context menus**
- ✅ **Keyboard shortcuts**
- ✅ **Hot reload** in development

## Quick Start

### Installation

```bash
npm install
```

### Development

```bash
# Build and watch for changes
npm run dev

# Or just build once
npm run build
```

### Load Extension in Chrome

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `dist/` directory from this project
5. The extension is now installed!

### Testing Changes

When running `npm run dev`, Webpack watches for file changes and rebuilds automatically. After changes:

1. Go to `chrome://extensions/`
2. Click the refresh icon on your extension
3. Test your changes

## Project Structure

```
chrome-extension/
├── src/
│   ├── popup/              # Popup UI (React)
│   │   ├── Popup.tsx      # Main popup component
│   │   ├── popup.css      # Popup styles
│   │   └── index.tsx      # Popup entry point
│   ├── background/         # Background service worker
│   │   └── background.ts  # Background script
│   ├── content/            # Content scripts
│   │   └── content.ts     # Content script
│   ├── options/            # Options page
│   │   └── options.tsx    # Options UI
│   └── utils/              # Shared utilities
│       └── storage.ts     # Storage helpers
├── public/
│   ├── manifest.json      # Extension manifest
│   ├── popup.html         # Popup HTML
│   ├── options.html       # Options HTML
│   └── icons/             # Extension icons
├── dist/                   # Built extension (load this in Chrome)
├── webpack.config.js       # Webpack configuration
└── package.json

```

## Extension Components

### Popup (src/popup/)

The popup UI appears when clicking the extension icon:

```tsx
// Popup.tsx
import { useState, useEffect } from 'react'

const Popup = () => {
  const [count, setCount] = useState(0)

  useEffect(() => {
    chrome.storage.sync.get(['count'], (result) => {
      setCount(result.count || 0)
    })
  }, [])

  return <div>Count: {count}</div>
}
```

### Background Service Worker (src/background/)

Handles events and long-running tasks:

```typescript
// background.ts
chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.sync.set({ enabled: true })
})

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  // Handle messages from popup or content scripts
})
```

### Content Script (src/content/)

Runs in the context of web pages:

```typescript
// content.ts
// Access the DOM of web pages
const button = document.createElement('button')
button.textContent = 'Click me!'
document.body.appendChild(button)

// Listen for messages
chrome.runtime.onMessage.addListener((message) => {
  if (message.type === 'HIGHLIGHT') {
    // Highlight text on page
  }
})
```

### Options Page (src/options/)

Settings page for the extension:

```tsx
// options.tsx
const Options = () => {
  return (
    <div>
      <h1>Extension Settings</h1>
      {/* Settings form */}
    </div>
  )
}
```

## Chrome APIs Used

### Storage API

```typescript
// Save data
chrome.storage.sync.set({ key: 'value' })

// Load data
chrome.storage.sync.get(['key'], (result) => {
  console.log(result.key)
})

// Listen for changes
chrome.storage.onChanged.addListener((changes, areaName) => {
  console.log('Storage changed:', changes)
})
```

### Messaging API

```typescript
// From popup to background
chrome.runtime.sendMessage({ type: 'ACTION' }, (response) => {
  console.log(response)
})

// From content script to background
chrome.runtime.sendMessage({ type: 'PAGE_DATA', data: {...} })

// From background to content script
chrome.tabs.sendMessage(tabId, { type: 'UPDATE' })
```

### Tabs API

```typescript
// Get active tab
chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  const activeTab = tabs[0]
})

// Execute script in tab
chrome.scripting.executeScript({
  target: { tabId: tabId },
  func: () => console.log('Hello from injected script!')
})
```

### Context Menus

```typescript
chrome.contextMenus.create({
  id: 'my-menu',
  title: 'My Extension',
  contexts: ['selection', 'page']
})

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'my-menu') {
    // Handle click
  }
})
```

### Keyboard Commands

Defined in manifest.json:

```json
"commands": {
  "toggle_feature": {
    "suggested_key": {
      "default": "Ctrl+Shift+T"
    },
    "description": "Toggle feature"
  }
}
```

Handle in background:

```typescript
chrome.commands.onCommand.addListener((command) => {
  if (command === 'toggle_feature') {
    // Toggle feature
  }
})
```

## Development Tips

### Hot Reload

The extension doesn't hot reload automatically. To see changes:

1. Save your files (Webpack rebuilds automatically)
2. Go to `chrome://extensions/`
3. Click the refresh icon
4. Reload any affected pages

### Debugging

**Popup**:
- Right-click extension icon > Inspect popup

**Background Service Worker**:
- Go to `chrome://extensions/`
- Click "service worker" link

**Content Script**:
- Open DevTools on the web page
- Content script logs appear in page console

**Errors**:
- Check `chrome://extensions/` for errors
- Click "Errors" button to see details

### TypeScript Types

Chrome API types are included:

```typescript
import { Tabs } from 'chrome'

chrome.tabs.query({...}, (tabs: Tabs.Tab[]) => {
  // TypeScript knows the tab structure
})
```

## Building for Production

```bash
npm run build
```

This creates an optimized build in `dist/`:
- Minified JavaScript
- Optimized for size
- Ready for Chrome Web Store

## Publishing to Chrome Web Store

1. **Prepare**:
   - Create promotional images (128x128, 440x280, etc.)
   - Write a good description
   - Take screenshots
   - Create a privacy policy (if needed)

2. **Build**:
   ```bash
   npm run build
   ```

3. **Create ZIP**:
   ```bash
   cd dist
   zip -r extension.zip .
   ```

4. **Upload**:
   - Go to [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/devconsole)
   - Pay $5 one-time registration fee (if not already registered)
   - Click "New Item"
   - Upload `extension.zip`
   - Fill in store listing information
   - Submit for review

5. **Review Process**:
   - Typically takes a few days
   - You'll receive email when approved
   - Extension goes live automatically

## Permissions

Declared in `manifest.json`:

```json
{
  "permissions": [
    "storage",      // Chrome Storage API
    "activeTab",    // Access to active tab
    "contextMenus", // Create context menus
    "scripting"     // Execute scripts
  ],
  "host_permissions": [
    "http://*/*",   // Access HTTP sites
    "https://*/*"   // Access HTTPS sites
  ]
}
```

**Minimize permissions**: Only request what you need!

## Security Best Practices

1. **Content Security Policy**: Already configured in manifest
2. **Validate input**: Always validate data from web pages
3. **Secure storage**: Don't store sensitive data unencrypted
4. **HTTPS only**: Use HTTPS for any network requests
5. **Minimize permissions**: Request only necessary permissions
6. **Code review**: Review all dependencies

## Common Patterns

### Communicate Between Scripts

```typescript
// popup.tsx
const sendToBackground = async () => {
  const response = await chrome.runtime.sendMessage({
    type: 'GET_DATA'
  })
  console.log(response)
}

// background.ts
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === 'GET_DATA') {
    sendResponse({ data: 'Hello!' })
  }
  return true // Keep channel open for async response
})
```

### Store Settings

```typescript
// Save settings
const saveSettings = async (settings: Settings) => {
  await chrome.storage.sync.set({ settings })
}

// Load settings
const loadSettings = async (): Promise<Settings> => {
  const { settings } = await chrome.storage.sync.get('settings')
  return settings || defaultSettings
}
```

### Modify Page Content

```typescript
// content.ts
function modifyPage() {
  // Add custom styles
  const style = document.createElement('style')
  style.textContent = '.highlight { background: yellow; }'
  document.head.appendChild(style)

  // Modify elements
  document.querySelectorAll('p').forEach(el => {
    el.classList.add('highlight')
  })
}
```

## Troubleshooting

### Extension doesn't load

- Check `dist/` folder exists with built files
- Verify manifest.json is valid JSON
- Check browser console for errors

### Changes not appearing

- Rebuild: `npm run build`
- Refresh extension in `chrome://extensions/`
- Hard reload pages: Ctrl+Shift+R

### Service worker not starting

- Check for JavaScript errors in background.ts
- View service worker console in `chrome://extensions/`
- Verify service_worker path in manifest.json

### Content script not injecting

- Check matches pattern in manifest.json
- Verify web page matches pattern
- Check content script for errors

## Resources

- [Chrome Extension Documentation](https://developer.chrome.com/docs/extensions/)
- [Manifest V3 Migration Guide](https://developer.chrome.com/docs/extensions/mv3/intro/)
- [Chrome Extension API Reference](https://developer.chrome.com/docs/extensions/reference/)
- [Chrome Web Store Policies](https://developer.chrome.com/docs/webstore/program-policies/)

## License

MIT License - see LICENSE file for details.
