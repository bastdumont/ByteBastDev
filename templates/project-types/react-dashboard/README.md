# React Dashboard

A modern, production-ready dashboard built with React, TypeScript, and Tailwind CSS.

## Features

- ✅ **React 18** with TypeScript
- ✅ **Vite** for fast development and building
- ✅ **Tailwind CSS** for styling
- ✅ **Recharts** for data visualization
- ✅ **TanStack Table** for advanced tables
- ✅ **TanStack Query** for data fetching
- ✅ **Zustand** for state management
- ✅ **React Router** for routing
- ✅ **React Hook Form** + Zod for forms
- ✅ **Radix UI** for accessible components
- ✅ **Dark mode** support
- ✅ **Responsive design**

## Quick Start

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

### Build

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
src/
├── components/          # Reusable components
│   ├── ui/             # UI primitives
│   ├── charts/         # Chart components
│   └── ...
├── pages/              # Page components
│   ├── OverviewPage.tsx
│   ├── AnalyticsPage.tsx
│   ├── UsersPage.tsx
│   └── SettingsPage.tsx
├── layouts/            # Layout components
│   └── DashboardLayout.tsx
├── lib/                # Utilities
│   ├── api.ts          # API client
│   └── utils.ts        # Helper functions
├── hooks/              # Custom hooks
├── store/              # Zustand stores
├── types/              # TypeScript types
├── api/                # API functions
└── App.tsx             # Root component
```

## Available Pages

- **Dashboard** (`/dashboard`) - Overview with stats and charts
- **Analytics** (`/analytics`) - Detailed analytics and metrics
- **Users** (`/users`) - User management with data table
- **Settings** (`/settings`) - Application settings

## Key Components

### Charts

- `RevenueChart` - Line chart for revenue data
- `UsersChart` - Area chart for user growth
- `SalesChart` - Bar chart for sales data

### Tables

- `UsersTable` - Advanced table with sorting, filtering, pagination
- Uses TanStack Table for powerful table functionality

### Cards

- `StatsCard` - Display key metrics
- `Card` - Generic card component

## State Management

The application uses Zustand for state management:

```typescript
// Example store
import { create } from 'zustand'

interface AppState {
  theme: 'light' | 'dark'
  setTheme: (theme: 'light' | 'dark') => void
}

export const useAppStore = create<AppState>((set) => ({
  theme: 'light',
  setTheme: (theme) => set({ theme }),
}))
```

## Data Fetching

TanStack Query is used for server state management:

```typescript
import { useQuery } from '@tanstack/react-query'

function MyComponent() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
  })

  // ...
}
```

## Styling

The project uses Tailwind CSS with a custom design system:

- **Colors**: Edit in `tailwind.config.js`
- **Components**: Located in `src/components/ui/`
- **Dark Mode**: Automatic with `class` strategy

## API Integration

Configure your API endpoint in `.env`:

```env
VITE_API_URL=http://localhost:3001/api
```

API functions are located in `src/api/`:

```typescript
// src/api/users.ts
export async function getUsers() {
  const response = await api.get('/users')
  return response.data
}
```

## Customization

### Change Theme Colors

Edit `tailwind.config.js` and `src/index.css`:

```css
:root {
  --primary: 221.2 83.2% 53.3%;
  --secondary: 210 40% 96.1%;
  /* ... */
}
```

### Add New Pages

1. Create page component in `src/pages/`
2. Add route in `App.tsx`
3. Add navigation link in `DashboardLayout.tsx`

### Add New Charts

Use Recharts components:

```typescript
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts'

export function MyChart({ data }) {
  return (
    <LineChart data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="name" />
      <YAxis />
      <Tooltip />
      <Line type="monotone" dataKey="value" stroke="#8884d8" />
    </LineChart>
  )
}
```

## Deployment

### Vercel

```bash
npm install -g vercel
vercel
```

### Netlify

```bash
npm run build
netlify deploy --prod --dir=dist
```

### Other Platforms

Build the application and serve the `dist` folder:

```bash
npm run build
```

## Environment Variables

Create a `.env` file:

```env
VITE_API_URL=https://api.yourdomain.com
VITE_APP_NAME=My Dashboard
```

Access in code:

```typescript
const apiUrl = import.meta.env.VITE_API_URL
```

## Performance

- Code splitting with React.lazy
- Image optimization
- Bundle size optimization
- Memoization with useMemo and useCallback

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

MIT License - feel free to use this for your projects.

## Resources

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [TanStack Query](https://tanstack.com/query)
- [TanStack Table](https://tanstack.com/table)
- [Recharts](https://recharts.org/)
- [Zustand](https://github.com/pmndrs/zustand)
