# Base Mini Apps Starter

A production-ready starter template for building mini applications on the Base App ecosystem. Base Mini Apps are lightweight applications built on the Farcaster protocol that integrate seamlessly with Base Account for onchain interactions.

## Features

- ✅ **Farcaster MiniApp SDK** integration
- ✅ **React 18** with TypeScript
- ✅ **Vite** for fast development and optimized builds
- ✅ **Tailwind CSS** for styling
- ✅ **Base Account** integration for onchain interactions
- ✅ **Manifest configuration** with account association
- ✅ **Embed metadata** for rich social previews
- ✅ **Webhook support** for notifications
- ✅ **Mobile-first** responsive design
- ✅ **Production-ready** deployment setup

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Base Account (create at [base.org](https://base.org))
- Domain for deployment (Vercel recommended)

### Installation

1. Clone or create your project:
```bash
# Using this template
npm create vite@latest my-mini-app -- --template react-ts
cd my-mini-app
```

2. Install dependencies:
```bash
npm install
npm install @farcaster/miniapp-sdk
```

3. Copy environment variables:
```bash
cp .env.example .env
```

4. Update the `.env` file:
```env
VITE_APP_NAME=My Mini App
VITE_APP_DOMAIN=your-domain.com
VITE_BASE_ACCOUNT_ADDRESS=0x...
```

5. Start development server:
```bash
npm run dev
```

6. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
base-mini-app/
├── src/
│   ├── components/          # React components
│   │   ├── App.tsx         # Main app component
│   │   ├── MiniAppWrapper.tsx  # SDK initialization wrapper
│   │   └── ui/             # Reusable UI components
│   ├── hooks/              # Custom React hooks
│   │   ├── useMiniApp.ts   # MiniApp SDK hook
│   │   └── useBaseAccount.ts # Base Account hook
│   ├── lib/                # Utility libraries
│   │   ├── sdk.ts          # SDK initialization
│   │   ├── base.ts         # Base Chain utilities
│   │   └── utils.ts        # Helper functions
│   ├── pages/              # Application pages/routes
│   ├── styles/             # Global styles
│   │   └── globals.css
│   └── main.tsx            # Application entry point
├── public/
│   ├── .well-known/
│   │   └── farcaster.json  # Farcaster manifest
│   └── images/             # App assets
│       ├── icon.png        # App icon (512x512)
│       ├── splash.png      # Splash screen (1170x2532)
│       ├── embed.png       # Embed image (1200x630)
│       └── screenshots/    # App screenshots
├── api/                    # API routes (optional)
│   └── webhook.ts          # Notification webhook
├── index.html              # HTML template with metadata
├── vite.config.ts          # Vite configuration
├── tailwind.config.js      # Tailwind configuration
├── tsconfig.json           # TypeScript configuration
└── package.json
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run type-check` - Run TypeScript type checking
- `npm run lint` - Run ESLint

## Configuration

### Farcaster Manifest

The manifest file at `public/.well-known/farcaster.json` defines your app's metadata and configuration.

#### Required Fields

```json
{
  "miniapp": {
    "version": "1",
    "name": "My Mini App",
    "homeUrl": "https://myapp.com",
    "iconUrl": "https://myapp.com/images/icon.png",
    "splashImageUrl": "https://myapp.com/images/splash.png",
    "splashBackgroundColor": "#0052FF",
    "subtitle": "Short tagline",
    "description": "Detailed app description",
    "screenshotUrls": [
      "https://myapp.com/images/screenshots/1.png",
      "https://myapp.com/images/screenshots/2.png",
      "https://myapp.com/images/screenshots/3.png"
    ],
    "primaryCategory": "social",
    "tags": ["social", "gaming", "base"]
  },
  "baseBuilder": {
    "ownerAddress": "0x..."
  }
}
```

#### Optional Fields

- `webhookUrl`: Endpoint for notifications
- `heroImageUrl`: Hero image for app listing
- `tagline`: Short promotional text
- `ogTitle`: Open Graph title
- `ogDescription`: Open Graph description
- `ogImageUrl`: Open Graph image
- `noindex`: Prevent search indexing (default: false)

### Account Association

To verify app ownership, you need to generate account association credentials:

1. Deploy your app with the manifest
2. Go to [Base Build Account Association](https://build.base.org/account-association)
3. Enter your app URL (e.g., `myapp.com`)
4. Click "Verify" and sign with your Base Account
5. Copy the generated credentials:

```json
{
  "accountAssociation": {
    "header": "eyJmaWQiOjkxNTIsInR5...",
    "payload": "eyJkb21haW4iOiJhcHAu...",
    "signature": "MHgwMDAwMDAwMDAwMD..."
  }
}
```

6. Add these to your manifest file

### Categories

Available primary categories:
- `social`: Social networking
- `gaming`: Games and entertainment
- `defi`: DeFi and finance
- `nft`: NFT marketplaces and tools
- `productivity`: Productivity tools
- `education`: Educational content
- `media`: Media and content
- `lifestyle`: Lifestyle apps

## SDK Integration

### Basic Usage

```typescript
import { sdk } from '@farcaster/miniapp-sdk';

// Initialize when app loads
await sdk.actions.ready();

// Get user context
const context = await sdk.context;
console.log(context.user); // User info
```

### React Hook

```typescript
import { useMiniApp } from '@/hooks/useMiniApp';

function MyComponent() {
  const { context, isReady } = useMiniApp();

  if (!isReady) return <div>Loading...</div>;

  return (
    <div>
      <h1>Welcome, {context?.user?.displayName}!</h1>
    </div>
  );
}
```

### Base Account Integration

```typescript
import { useBaseAccount } from '@/hooks/useBaseAccount';

function AccountComponent() {
  const { account, balance } = useBaseAccount();

  return (
    <div>
      <p>Address: {account}</p>
      <p>Balance: {balance} ETH</p>
    </div>
  );
}
```

## Asset Requirements

### App Icon
- **Size**: 512x512 pixels
- **Format**: PNG
- **Background**: Solid color or transparent
- **Location**: `public/images/icon.png`

### Splash Screen
- **Size**: 1170x2532 pixels (recommended)
- **Format**: PNG
- **Aspect Ratio**: 9:19.5 (iPhone-like)
- **Location**: `public/images/splash.png`

### Screenshots
- **Quantity**: 3-5 images
- **Size**: Match your app's viewport
- **Format**: PNG or JPG
- **Location**: `public/images/screenshots/`

### Embed Image
- **Size**: 1200x630 pixels
- **Format**: PNG or JPG
- **Use**: Social media previews
- **Location**: `public/images/embed.png`

### Hero Image (Optional)
- **Size**: 1200x630 pixels
- **Format**: PNG or JPG
- **Use**: App listing page
- **Location**: `public/images/hero.png`

## Embed Metadata

Add to your `index.html` for rich previews when shared:

```html
<meta name="fc:miniapp" content='{
  "version": "next",
  "imageUrl": "https://myapp.com/images/embed.png",
  "button": {
    "title": "Launch App",
    "action": {
      "type": "launch_miniapp",
      "name": "My Mini App",
      "url": "https://myapp.com"
    }
  }
}' />
```

## Webhooks (Optional)

To receive notifications, set up a webhook endpoint:

### 1. Configure Webhook URL

Add to your manifest:
```json
{
  "miniapp": {
    "webhookUrl": "https://myapp.com/api/webhook"
  }
}
```

### 2. Create Webhook Handler

```typescript
// api/webhook.ts
export async function POST(req: Request) {
  const payload = await req.json();

  // Verify signature
  // Process event
  // Return response

  return new Response('OK', { status: 200 });
}
```

### 3. Event Types

- User mentions your app
- User interacts with your app
- Custom events you define

## Deployment

### Vercel (Recommended)

1. Push your code to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/your-repo.git
git push -u origin main
```

2. Import project in [Vercel](https://vercel.com):
   - Connect your GitHub repository
   - Configure build settings (auto-detected for Vite)
   - Add environment variables
   - Deploy

3. Configure custom domain:
   - Add your domain in Vercel settings
   - Update DNS records as instructed
   - Wait for DNS propagation

4. Verify deployment:
   - Check that your app loads at `https://yourdomain.com`
   - Verify manifest is accessible at `https://yourdomain.com/.well-known/farcaster.json`
   - Test with [Base Build Preview](https://build.base.org/preview)

### Other Platforms

The app can be deployed to:
- **Netlify**: Similar to Vercel
- **Cloudflare Pages**: Fast global deployment
- **Railway**: Good for apps with backends
- **Render**: Full-stack hosting

Make sure to:
1. Set all environment variables
2. Configure build command: `npm run build`
3. Set output directory: `dist`
4. Enable HTTPS
5. Configure custom domain

## Publishing Your App

### 1. Pre-Launch Checklist

- [ ] App deployed and accessible
- [ ] Manifest at `/.well-known/farcaster.json`
- [ ] Account association generated
- [ ] All required fields in manifest
- [ ] Assets uploaded (icon, splash, screenshots)
- [ ] Embed metadata in HTML
- [ ] Tested on mobile devices
- [ ] Performance optimized (Lighthouse > 90)
- [ ] No console errors

### 2. Test with Base Build

1. Go to [Base Build Preview](https://build.base.org/preview)
2. Enter your app URL
3. Verify:
   - App loads correctly
   - Embeds display properly
   - Launch button works
   - Account association valid

### 3. Publish

Create a post in the Base App with your app's URL:

1. Open Base App
2. Create new post
3. Include your app URL (e.g., `https://myapp.com`)
4. The app will appear as an interactive embed
5. Users can launch your app directly from the post

### 4. Post-Launch

- Monitor app performance
- Track user engagement
- Respond to user feedback
- Iterate and improve

## Best Practices

### Performance

- Keep bundle size under 500KB
- Optimize images (use WebP)
- Lazy load non-critical components
- Use React.memo for expensive renders
- Call `sdk.actions.ready()` as soon as possible

### Mobile First

- Design for 375px-428px width
- Use responsive breakpoints
- Test on real mobile devices
- Optimize touch targets (min 44px)
- Support portrait and landscape

### User Experience

- Provide loading states
- Handle errors gracefully
- Support offline functionality
- Use native-like interactions
- Keep navigation simple

### Security

- Validate all user inputs
- Use HTTPS only
- Verify webhook signatures
- Don't store secrets client-side
- Implement rate limiting

## Development Tips

### Hot Module Replacement

Vite supports HMR out of the box. Changes to your code will reflect immediately without full page reload.

### TypeScript

Use TypeScript for type safety:
```typescript
import type { Context } from '@farcaster/miniapp-sdk';

interface UserData {
  fid: number;
  username: string;
  displayName: string;
}

const getUserData = (context: Context): UserData => {
  return {
    fid: context.user.fid,
    username: context.user.username,
    displayName: context.user.displayName,
  };
};
```

### Debugging

Enable debug mode:
```typescript
// src/lib/sdk.ts
import { sdk } from '@farcaster/miniapp-sdk';

if (import.meta.env.DEV) {
  sdk.debug = true;
}
```

### Environment Variables

Access in code:
```typescript
const appName = import.meta.env.VITE_APP_NAME;
const isDev = import.meta.env.DEV;
```

## Troubleshooting

### App Not Loading

**Problem**: Blank screen or infinite loading

**Solutions**:
- Verify `sdk.actions.ready()` is called
- Check browser console for errors
- Ensure manifest is accessible
- Test on different browsers/devices

### Manifest Not Found

**Problem**: 404 error for manifest file

**Solutions**:
- Verify file is in `public/.well-known/farcaster.json`
- Check deployment includes `public` folder
- Test URL directly: `https://yourdomain.com/.well-known/farcaster.json`
- Clear CDN cache if using one

### Account Association Failed

**Problem**: Invalid account association

**Solutions**:
- Ensure manifest is deployed and accessible
- Use correct Base Account address
- Regenerate credentials if domain changed
- Verify signature format is correct

### Embeds Not Showing

**Problem**: App doesn't show rich preview when shared

**Solutions**:
- Verify `fc:miniapp` meta tag in HTML
- Check image URLs are publicly accessible
- Test with Base Build Preview tool
- Ensure JSON in meta tag is valid

### Performance Issues

**Problem**: Slow loading or laggy interactions

**Solutions**:
- Reduce bundle size
- Optimize images
- Use code splitting
- Enable caching
- Profile with Chrome DevTools

## Resources

### Official Documentation
- [Base Mini Apps Docs](https://docs.base.org/mini-apps)
- [Quickstart Guide](https://docs.base.org/mini-apps/quickstart/migrate-existing-apps)
- [Manifest Reference](https://docs.base.org/mini-apps/core-concepts/manifest)
- [Base Build Tools](https://build.base.org)

### SDKs and Libraries
- [Farcaster MiniApp SDK](https://github.com/farcasterxyz/miniapp-sdk)
- [Base Chain Docs](https://docs.base.org)
- [OnchainKit](https://onchainkit.xyz)

### Design Resources
- [Design Guidelines](https://docs.base.org/mini-apps/design-guidelines)
- [Figma Templates](https://docs.base.org/mini-apps/design-resources)
- [Base Brand Kit](https://base.org/brand)

### Community
- [Base Discord](https://discord.gg/base)
- [Farcaster Discord](https://discord.gg/farcaster)
- [Base Developers Forum](https://forum.base.org)

### Tools
- [Base Build](https://build.base.org) - Preview and validate
- [Account Association](https://build.base.org/account-association) - Generate credentials
- [Manifest Validator](https://build.base.org/validator) - Validate manifest

## Examples

Check out these example Mini Apps:
- Social gaming app
- NFT gallery
- DeFi dashboard
- Productivity tool

## Support

For issues and questions:
- Check the [troubleshooting guide](#troubleshooting)
- Review [Base documentation](https://docs.base.org/mini-apps)
- Ask in [Base Discord](https://discord.gg/base)
- Create an issue in this repository

## License

MIT License - feel free to use this template for your projects.

## Credits

Built with:
- [React](https://react.dev/)
- [TypeScript](https://www.typescriptlang.org/)
- [Vite](https://vitejs.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Farcaster MiniApp SDK](https://github.com/farcasterxyz/miniapp-sdk)
- [Base Chain](https://base.org/)

---

**Ready to build?** Start with `npm install` and `npm run dev`!

For more information, visit [docs.base.org/mini-apps](https://docs.base.org/mini-apps)
