# Create Base Mini App

Create a complete Base Mini App with the following specifications:

## App Details
- **Name**: {app_name}
- **Category**: {category}
- **Description**: {description}

## Features to Include
{features}

## Technical Requirements
1. Set up Vite + React + TypeScript project structure
2. Install and configure @farcaster/miniapp-sdk
3. Create MiniAppWrapper component that:
   - Initializes the SDK
   - Calls sdk.actions.ready() when app loads
   - Provides context to child components
4. Implement responsive mobile-first UI with Tailwind CSS
5. Create manifest file at `public/.well-known/farcaster.json` with:
   - All required fields populated
   - Placeholder account association (to be filled later)
   - Appropriate category and tags
6. Add embed metadata to index.html
7. Set up environment variables for configuration
8. Include placeholder images for:
   - App icon (512x512)
   - Splash screen (1170x2532)
   - Screenshots (at least 3)
   - Hero/OG image (1200x630)

## File Structure
Generate the following structure:
```
src/
  ├── components/
  │   ├── App.tsx
  │   ├── MiniAppWrapper.tsx
  │   └── ui/
  ├── hooks/
  │   ├── useMiniApp.ts
  │   └── useBaseAccount.ts
  ├── lib/
  │   ├── sdk.ts
  │   └── utils.ts
  ├── styles/
  │   └── globals.css
  └── main.tsx
public/
  ├── .well-known/
  │   └── farcaster.json
  └── images/
      ├── icon.png
      ├── splash.png
      └── screenshots/
```

## Implementation Notes
- Use TypeScript for type safety
- Follow React best practices
- Optimize for mobile performance
- Include error handling
- Add loading states
- Implement proper accessibility

## Deployment Preparation
Include:
1. README.md with setup instructions
2. .env.example with all required variables
3. Deployment guide for Vercel
4. Instructions for generating account association

Generate all necessary files and code.
