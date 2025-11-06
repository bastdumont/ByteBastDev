# Optimize Base Mini App Performance

Optimize the Base Mini App for fast loading and smooth performance:

## Performance Targets
- First Contentful Paint (FCP): < 1.5s
- Time to Interactive (TTI): < 3.5s
- Total Bundle Size: < 500KB (gzipped)
- Lighthouse Score: > 90

## Optimization Tasks

### 1. Bundle Size Reduction
- [ ] Analyze bundle with `vite-bundle-visualizer`
- [ ] Remove unused dependencies
- [ ] Use dynamic imports for routes
- [ ] Tree-shake unused code
- [ ] Minimize third-party libraries

```typescript
// Lazy load routes
const Home = lazy(() => import('./pages/Home'));
const Game = lazy(() => import('./pages/Game'));

// Code splitting example
<Suspense fallback={<Loading />}>
  <Routes>
    <Route path="/" element={<Home />} />
    <Route path="/game" element={<Game />} />
  </Routes>
</Suspense>
```

### 2. Image Optimization
- [ ] Convert images to WebP format
- [ ] Implement responsive images
- [ ] Use appropriate image dimensions
- [ ] Lazy load images below the fold
- [ ] Add blur placeholders

```typescript
// Optimized image component
const OptimizedImage = ({ src, alt, ...props }) => (
  <img
    src={src}
    alt={alt}
    loading="lazy"
    decoding="async"
    {...props}
  />
);
```

### 3. Code Splitting
- [ ] Split by routes
- [ ] Split by features
- [ ] Defer non-critical code
- [ ] Use dynamic imports

```typescript
// Feature-based code splitting
const Analytics = lazy(() =>
  import(/* webpackChunkName: "analytics" */ './lib/analytics')
);
```

### 4. Caching Strategy
- [ ] Implement service worker
- [ ] Cache static assets
- [ ] Use HTTP caching headers
- [ ] Cache API responses

```typescript
// Service worker for caching
// vite-plugin-pwa config
export default {
  plugins: [
    VitePWA({
      registerType: 'autoUpdate',
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg}'],
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/api\./,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'api-cache',
              expiration: {
                maxEntries: 50,
                maxAgeSeconds: 300
              }
            }
          }
        ]
      }
    })
  ]
};
```

### 5. React Optimization
- [ ] Use React.memo for expensive components
- [ ] Implement useMemo for calculations
- [ ] Use useCallback for event handlers
- [ ] Avoid unnecessary re-renders
- [ ] Use keys properly in lists

```typescript
// Memoized component
const ExpensiveComponent = memo(({ data }) => {
  const processed = useMemo(() =>
    processData(data),
    [data]
  );

  const handleClick = useCallback(() => {
    // Handler logic
  }, []);

  return <div onClick={handleClick}>{processed}</div>;
});
```

### 6. Loading Strategy
- [ ] Show splash screen immediately
- [ ] Call sdk.actions.ready() ASAP
- [ ] Defer non-critical JS
- [ ] Prefetch critical resources
- [ ] Use skeleton screens

```typescript
// Fast initialization
useEffect(() => {
  // Critical: call ready() immediately
  sdk.actions.ready().then(() => {
    // Then load other data
    fetchData();
  });
}, []);
```

### 7. Font Optimization
- [ ] Use system fonts when possible
- [ ] Subset custom fonts
- [ ] Use font-display: swap
- [ ] Preload critical fonts

```css
/* Font optimization */
@font-face {
  font-family: 'CustomFont';
  src: url('/fonts/custom-font.woff2') format('woff2');
  font-display: swap;
  font-weight: 400;
}
```

### 8. CSS Optimization
- [ ] Remove unused CSS
- [ ] Use PurgeCSS with Tailwind
- [ ] Minimize CSS bundle
- [ ] Use CSS modules
- [ ] Avoid large CSS frameworks

```javascript
// Tailwind config with PurgeCSS
module.exports = {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  // Removes unused styles
};
```

### 9. JavaScript Optimization
- [ ] Minimize main thread work
- [ ] Defer third-party scripts
- [ ] Use web workers for heavy tasks
- [ ] Avoid layout thrashing
- [ ] Debounce expensive operations

```typescript
// Web worker for heavy computation
const worker = new Worker(
  new URL('./workers/computation.worker.ts', import.meta.url)
);

worker.postMessage({ data });
worker.onmessage = (e) => {
  setResult(e.data);
};
```

### 10. Network Optimization
- [ ] Use HTTP/2
- [ ] Enable compression (Brotli/gzip)
- [ ] Minimize HTTP requests
- [ ] Use CDN for static assets
- [ ] Implement request batching

```typescript
// Request batching
const batchRequests = async (requests) => {
  return Promise.all(
    requests.map(req => fetch(req))
  );
};
```

### 11. Monitoring
- [ ] Add performance monitoring
- [ ] Track Web Vitals
- [ ] Monitor bundle size
- [ ] Set up error tracking
- [ ] Use Lighthouse CI

```typescript
// Web Vitals monitoring
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

getCLS(console.log);
getFID(console.log);
getFCP(console.log);
getLCP(console.log);
getTTFB(console.log);
```

### 12. Build Optimization
- [ ] Enable production mode
- [ ] Use source maps for debugging only
- [ ] Enable minification
- [ ] Configure chunk splitting
- [ ] Use build caching

```typescript
// Vite build optimization
export default defineConfig({
  build: {
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
      },
    },
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          sdk: ['@farcaster/miniapp-sdk'],
        },
      },
    },
  },
});
```

## Performance Checklist

- [ ] Bundle size under 500KB
- [ ] FCP under 1.5 seconds
- [ ] TTI under 3.5 seconds
- [ ] Images optimized (WebP)
- [ ] Code splitting implemented
- [ ] Lazy loading for routes
- [ ] Service worker configured
- [ ] Fonts optimized
- [ ] CSS purged
- [ ] Third-party scripts deferred
- [ ] Monitoring setup
- [ ] Lighthouse score > 90

## Testing Performance

1. Run Lighthouse audit:
```bash
npm run build
npm run preview
# Run Lighthouse in Chrome DevTools
```

2. Analyze bundle:
```bash
npm run build -- --analyze
```

3. Test on real devices:
- Test on slow 3G
- Test on various devices
- Monitor Web Vitals

Generate optimized code and configuration files.
