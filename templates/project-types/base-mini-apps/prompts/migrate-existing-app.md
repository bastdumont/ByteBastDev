# Migrate Existing App to Base Mini App

Convert an existing web application into a Base Mini App:

## Migration Steps

### 1. Add MiniApp SDK
Install the Farcaster MiniApp SDK:
```bash
npm install @farcaster/miniapp-sdk
```

### 2. Initialize SDK
Create SDK wrapper and call `ready()` when app loads:

```typescript
// src/lib/miniapp.ts
import { sdk } from '@farcaster/miniapp-sdk';

export const initMiniApp = async () => {
  try {
    // Signal app is ready to display
    await sdk.actions.ready();

    // Get user context
    const context = await sdk.context;
    return context;
  } catch (error) {
    console.error('MiniApp initialization failed:', error);
    throw error;
  }
};
```

### 3. Create Manifest
Create `public/.well-known/farcaster.json`:

```json
{
  "accountAssociation": {
    "header": "",
    "payload": "",
    "signature": ""
  },
  "baseBuilder": {
    "ownerAddress": "0x..."
  },
  "miniapp": {
    "version": "1",
    "name": "{APP_NAME}",
    "homeUrl": "{APP_URL}",
    "iconUrl": "{APP_URL}/icon.png",
    "splashImageUrl": "{APP_URL}/splash.png",
    "splashBackgroundColor": "#000000",
    "subtitle": "{SUBTITLE}",
    "description": "{DESCRIPTION}",
    "screenshotUrls": [
      "{APP_URL}/screenshot1.png",
      "{APP_URL}/screenshot2.png",
      "{APP_URL}/screenshot3.png"
    ],
    "primaryCategory": "social",
    "tags": ["tag1", "tag2"],
    "noindex": false
  }
}
```

### 4. Add Embed Metadata
Update your HTML file (index.html or layout) to include:

```html
<meta name="fc:miniapp" content='{
  "version": "next",
  "imageUrl": "{APP_URL}/embed-image.png",
  "button": {
    "title": "Launch App",
    "action": {
      "type": "launch_miniapp",
      "name": "{APP_NAME}",
      "url": "{APP_URL}"
    }
  }
}' />
```

### 5. Update App Entry Point
Modify your app's main component to initialize the SDK:

```typescript
// src/App.tsx or src/main.tsx
import { useEffect, useState } from 'react';
import { initMiniApp } from './lib/miniapp';

function App() {
  const [isReady, setIsReady] = useState(false);
  const [context, setContext] = useState(null);

  useEffect(() => {
    initMiniApp()
      .then((ctx) => {
        setContext(ctx);
        setIsReady(true);
      })
      .catch((error) => {
        console.error('Failed to initialize:', error);
        setIsReady(true); // Still render app
      });
  }, []);

  if (!isReady) {
    return <div>Loading...</div>;
  }

  return (
    <YourExistingApp context={context} />
  );
}
```

### 6. Generate Account Association
1. Deploy your updated app with the manifest
2. Go to [Base Build Account Association](https://build.base.org/account-association)
3. Enter your app URL
4. Click "Verify" and follow instructions
5. Copy the generated credentials to your manifest

### 7. Create Assets
Prepare the following images:
- **Icon**: 512x512 PNG (app icon)
- **Splash**: 1170x2532 PNG (loading screen)
- **Screenshots**: 3-5 images showing your app
- **Embed Image**: 1200x630 PNG (for social sharing)
- **Hero Image**: 1200x630 PNG (optional, for app page)

### 8. Mobile Optimization
Ensure your app works well on mobile:
- Test on mobile viewport (375px-428px width)
- Optimize touch targets (minimum 44px)
- Use responsive design patterns
- Test on actual mobile devices

### 9. Environment Configuration
Add Base-specific environment variables:

```env
VITE_BASE_ACCOUNT_ADDRESS=0x...
VITE_APP_DOMAIN=your-app.com
VITE_FARCASTER_MANIFEST_URL=https://your-app.com/.well-known/farcaster.json
```

### 10. Deploy and Test
1. Deploy to production (Vercel recommended)
2. Verify manifest is accessible at `/.well-known/farcaster.json`
3. Test with [Base Build Preview](https://build.base.org/preview)
4. Verify account association
5. Check embed metadata

### 11. Publish
Create a post in Base App with your app URL to publish it.

## Compatibility Checklist

- [ ] SDK installed and initialized
- [ ] `sdk.actions.ready()` called after app loads
- [ ] Manifest created at `/.well-known/farcaster.json`
- [ ] All manifest required fields populated
- [ ] Account association generated and added
- [ ] Embed metadata added to HTML
- [ ] Assets created and uploaded
- [ ] Mobile optimization verified
- [ ] Deployed to production
- [ ] Manifest accessible publicly
- [ ] Tested with Base Build Preview
- [ ] Published in Base App

## Common Migration Issues

### Existing Routing
If your app uses React Router or similar:
- Mini Apps work with routing libraries
- Ensure deep links work correctly
- Test navigation within the mini app context

### State Management
- Mini Apps can use any state management (Redux, Zustand, etc.)
- Context from SDK should be integrated into your state
- Consider user's Farcaster identity in your state

### Authentication
- Mini Apps get user identity from Farcaster
- You may still need additional auth for your backend
- Consider using Base Account for onchain auth

### API Calls
- Existing API calls work normally
- Add user's Farcaster ID to requests if needed
- Consider rate limiting per user

### Asset Hosting
- Ensure all assets use HTTPS
- Use absolute URLs for manifest images
- Consider CDN for better performance

## Framework-Specific Notes

### React (Vite)
- Works out of the box
- Place manifest in `public/.well-known/`

### Next.js
- Place manifest in `public/.well-known/`
- Add metadata to `app/layout.tsx` or `pages/_document.tsx`
- Use Server Components carefully (SDK is client-side)

### Vue
- Works with Vue 3
- Use composition API for SDK integration
- Place manifest in `public/.well-known/`

### Svelte
- Works with SvelteKit
- Use onMount for SDK initialization
- Place manifest in `static/.well-known/`

Generate migration code based on the existing app framework and structure.
