# {{project_name}} - Vue.js SPA

Modern single-page application built with Vue 3, TypeScript, and Vite.

## Features

- ✅ **Vue 3** with Composition API
- ✅ **TypeScript** for type safety
- ✅ **Vite** for lightning-fast development
- ✅ **Pinia** for state management
- ✅ **Vue Router** for navigation
- ✅ **Tailwind CSS** for styling
- ✅ **Axios** for API requests
- ✅ **VueUse** for composable utilities
- ✅ **Dark mode** support
- ✅ **Fully responsive**

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
src/
├── assets/          # Static assets and styles
├── components/      # Vue components
├── composables/     # Composition API composables
├── router/          # Vue Router configuration
├── stores/          # Pinia stores
├── views/           # Page components
├── types/           # TypeScript types
├── App.vue          # Root component
└── main.ts          # Application entry point
```

## State Management with Pinia

```typescript
// stores/counter.ts
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', {
  state: () => ({
    count: 0
  }),
  actions: {
    increment() {
      this.count++
    }
  }
})

// In component
import { useCounterStore } from '@/stores/counter'

const counter = useCounterStore()
counter.increment()
```

## Routing

```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomePage.vue')
    }
  ]
})
```

## API Integration

```typescript
// composables/useApi.ts
import axios from 'axios'

export function useApi() {
  const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL
  })

  return { api }
}
```

## Development

- Hot Module Replacement (HMR) is enabled
- TypeScript type checking
- ESLint for code quality
- Tailwind CSS with JIT mode

## Building for Production

```bash
npm run build
```

Outputs to `dist/` directory, ready for deployment.

## License

MIT
