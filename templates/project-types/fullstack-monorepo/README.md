# {{project_name}} - Full-Stack Monorepo

A production-ready full-stack monorepo with Next.js frontend and FastAPI backend, orchestrated with Turborepo.

## Features

- ✅ **Turborepo** for monorepo management
- ✅ **Next.js 14** frontend application
- ✅ **FastAPI** Python backend
- ✅ **TypeScript** throughout frontend
- ✅ **Shared packages** (UI components, configs)
- ✅ **Single command** to run everything
- ✅ **Hot reload** for both apps
- ✅ **Type-safe** API communication
- ✅ **Docker Compose** for deployment
- ✅ **pnpm** for fast package management

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.11+
- pnpm (`npm install -g pnpm`)

### Installation

```bash
# Install all dependencies (frontend + backend)
pnpm install

# Install Python dependencies for API
cd apps/api
pip install -r requirements.txt
cd ../..
```

### Development

```bash
# Run both frontend and backend concurrently
pnpm dev

# Frontend will be at: http://localhost:3000
# Backend will be at: http://localhost:8000
# API docs at: http://localhost:8000/docs
```

Or run individually:

```bash
# Run only frontend
cd apps/web
pnpm dev

# Run only backend
cd apps/api
python main.py
```

## Project Structure

```
{{project_name}}/
├── apps/
│   ├── web/                 # Next.js frontend
│   │   ├── app/            # Next.js app directory
│   │   ├── components/     # React components
│   │   ├── lib/            # Utilities
│   │   └── package.json
│   └── api/                # FastAPI backend
│       ├── main.py         # FastAPI app
│       ├── routers/        # API routes
│       ├── models/         # Pydantic models
│       └── requirements.txt
├── packages/
│   ├── ui/                 # Shared UI components
│   │   ├── Button.tsx
│   │   └── package.json
│   ├── config/             # Shared configuration
│   └── tsconfig/           # Shared TypeScript config
├── package.json            # Root package.json
├── turbo.json              # Turborepo configuration
└── pnpm-workspace.yaml     # pnpm workspace config
```

## Turborepo Commands

```bash
# Run dev for all apps
pnpm dev

# Build all apps
pnpm build

# Run tests across all apps
pnpm test

# Lint all apps
pnpm lint

# Clean all build artifacts
pnpm clean
```

## Frontend (Next.js)

Located in `apps/web/`:

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Components**: Shared UI package
- **API Client**: Axios/fetch

### Adding Pages

```tsx
// apps/web/app/dashboard/page.tsx
export default function DashboardPage() {
  return <div>Dashboard</div>
}
```

### API Calls

```typescript
// Call backend API
const response = await fetch('http://localhost:8000/api/v1/items')
const data = await response.json()
```

## Backend (FastAPI)

Located in `apps/api/`:

- **Framework**: FastAPI
- **Language**: Python 3.11+
- **Async**: Full async/await support
- **Validation**: Pydantic models
- **Docs**: Auto-generated at `/docs`

### Adding Endpoints

```python
# apps/api/main.py
@app.get("/api/v1/users")
async def get_users():
    return {"users": []}
```

### Running API Standalone

```bash
cd apps/api
uvicorn main:app --reload
```

## Shared Packages

### UI Package (`packages/ui/`)

Shared React components used across apps:

```tsx
// packages/ui/Button.tsx
export function Button({ children, ...props }) {
  return <button {...props}>{children}</button>
}

// Use in apps/web
import { Button } from 'ui'
```

### Config Package (`packages/config/`)

Shared configuration (ESLint, Tailwind, etc.):

```js
// packages/config/tailwind.config.js
module.exports = {
  // Shared Tailwind config
}
```

## Environment Variables

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (.env)

```env
DATABASE_URL=postgresql://...
API_KEY=your-api-key
```

## Docker Deployment

### Docker Compose

```bash
# Build and run with Docker Compose
docker-compose up --build

# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

### Individual Containers

```bash
# Build frontend
docker build -t web -f apps/web/Dockerfile .

# Build backend
docker build -t api -f apps/api/Dockerfile .

# Run containers
docker run -p 3000:3000 web
docker run -p 8000:8000 api
```

## Development Workflow

### Adding a New Feature

1. **Create API endpoint** in `apps/api/main.py`
2. **Create frontend page** in `apps/web/app/`
3. **Add shared components** to `packages/ui/` if needed
4. **Test** both frontend and backend
5. **Commit** changes

### Working with Shared Packages

```bash
# Add dependency to shared package
cd packages/ui
pnpm add some-package

# Use in apps
cd apps/web
# Import from 'ui' package
```

## Testing

```bash
# Run all tests
pnpm test

# Test frontend only
cd apps/web
pnpm test

# Test backend only
cd apps/api
pytest
```

## Building for Production

```bash
# Build all apps
pnpm build

# Build creates:
# - apps/web/.next - Next.js build
# - apps/api/dist - Python build (if configured)
```

## Deployment

### Vercel (Frontend)

```bash
cd apps/web
vercel
```

### Railway/Render (Backend)

```bash
cd apps/api
# Deploy to Railway or Render
```

### Docker (Full Stack)

```bash
# Use docker-compose.yml
docker-compose up -d
```

## Monorepo Benefits

1. **Code Sharing**: Share UI components, utils, and configs
2. **Atomic Commits**: Frontend + backend changes in one commit
3. **Faster Development**: Turborepo caching and parallelization
4. **Consistent Tooling**: Same tools across all apps
5. **Type Safety**: Share types between frontend and backend

## Turborepo Features

- **Smart Caching**: Only rebuilds what changed
- **Parallel Execution**: Runs tasks in parallel when possible
- **Remote Caching**: Share cache across team (optional)
- **Pipeline**: Define task dependencies

## Common Tasks

### Add New App

```bash
mkdir apps/mobile
cd apps/mobile
# Set up new app
```

### Add New Package

```bash
mkdir packages/utils
cd packages/utils
pnpm init
# Create shared utilities
```

### Update Dependencies

```bash
# Update all packages
pnpm update --recursive

# Update specific package
pnpm update next --filter web
```

## Troubleshooting

### Port Already in Use

```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill

# Kill process on port 8000
lsof -ti:8000 | xargs kill
```

### Module Not Found

```bash
# Reinstall dependencies
pnpm install

# Clear Turborepo cache
rm -rf .turbo
```

### API Not Connecting

- Ensure API is running on port 8000
- Check CORS configuration in `apps/api/main.py`
- Verify `NEXT_PUBLIC_API_URL` environment variable

## Performance

- **Turborepo Caching**: Tasks are cached and only re-run when needed
- **Parallel Builds**: Frontend and backend build in parallel
- **Incremental Builds**: Only changed packages rebuild
- **Hot Reload**: Both apps support hot module replacement

## License

MIT

## Resources

- [Turborepo Documentation](https://turbo.build/repo/docs)
- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [pnpm Documentation](https://pnpm.io/)
