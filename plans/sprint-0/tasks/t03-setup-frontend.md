# Task 03: Setup Frontend Development Environment

**Task ID**: sprint-0-t03
**Task Name**: Setup Frontend Development Environment
**Sprint**: 0
**Priority**: High
**Estimated Time**: 3 hours
**Assigned To**: [Frontend Developer]

---

## 1. Objective

Set up a complete React development environment with Vite, Tailwind CSS, and all required dependencies for building the AI Lightroom frontend.

## 2. Why This Matters

### Business Value
- **User Interface**: Frontend is what users interact with - must be polished
- **Development Speed**: Modern tooling enables rapid UI iteration
- **User Experience**: Good DX translates to better UX

### Technical Value
- **Vite Benefits**: Fast HMR, optimized builds, modern ESM
- **Tailwind CSS**: Utility-first styling, consistent design system
- **React 18**: Latest features including concurrent rendering

### Risks of Not Doing This
- **Development Blocked**: Cannot build UI without environment
- **Inconsistent Styling**: Without Tailwind, styling becomes fragmented
- **Slow Development**: Poor tooling slows iteration

## 3. Dependencies

### Prerequisites
- [x] t01-init-repo (repository structure exists)
- [x] Node.js 18+ installed locally
- [x] npm or yarn available

### Blocking
- [ ] t04-docker-config (depends on frontend setup)
- [ ] t05-env-config (depends on frontend setup)
- [ ] Sprint 5 frontend tasks (cannot start without this)

### External Dependencies
- Node.js runtime
- npm registry packages

## 4. Acceptance Criteria

### Definition of Done
- [ ] React project created with Vite
- [ ] All dependencies installed (package.json)
- [ ] Tailwind CSS configured and working
- [ ] Basic App component renders
- [ ] Dev server runs on localhost:5173
- [ ] Hot Module Replacement (HMR) working
- [ ] .env.example file created

### Success Metrics
- Dev server starts in < 5 seconds
- HMR reflects changes in < 1 second
- No console errors
- Tailwind classes applied correctly

### Edge Cases to Handle
- Node.js version not 18+
- npm install fails (network issues)
- Port 5173 already in use
- Tailwind not generating styles

## 5. Technical Implementation

### Approach

1. Create React project with Vite
2. Install all required dependencies
3. Configure Tailwind CSS
4. Create basic component structure
5. Configure development settings
6. Test server and HMR

### Key Dependencies

**package.json**
```json
{
  "name": "ai-lightroom-web",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.6.0",
    "lucide-react": "^0.294.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "autoprefixer": "^10.4.0",
    "eslint": "^8.55.0",
    "eslint-plugin-react": "^7.33.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.0",
    "postcss": "^8.4.0",
    "tailwindcss": "^3.3.0",
    "vite": "^5.0.0"
  }
}
```

### Project Structure

```
web/
├── src/
│   ├── main.jsx              # Entry point
│   ├── App.jsx               # Root component
│   ├── index.css             # Global styles + Tailwind
│   ├── components/
│   │   └── .gitkeep
│   ├── services/
│   │   └── api.js            # Axios API client
│   ├── hooks/
│   │   └── .gitkeep
│   └── utils/
│       └── .gitkeep
├── public/
│   └── favicon.ico
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
├── .env.example
└── .gitkeep
```

### Implementation Files

**web/vite.config.js**
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true,
  },
})
```

**web/tailwind.config.js**
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
      },
    },
  },
  plugins: [],
}
```

**web/postcss.config.js**
```javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

**web/src/index.css**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  @apply bg-gray-50 text-gray-900;
}
```

**web/src/main.jsx**
```javascript
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

**web/src/App.jsx**
```javascript
function App() {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-primary-600 mb-4">
          AI Lightroom
        </h1>
        <p className="text-gray-600">
          AI-powered image color adjustment tool
        </p>
      </div>
    </div>
  )
}

export default App
```

**web/src/services/api.js**
```javascript
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: Number(import.meta.env.VITE_API_TIMEOUT) || 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

export default api
```

**web/index.html**
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>AI Lightroom</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

**web/.env.example**
```env
VITE_API_URL=http://localhost:8000
VITE_API_TIMEOUT=30000
VITE_MAX_FILE_SIZE=10485760
```

### Pseudocode / Algorithm

```bash
# Step 1: Navigate to web directory
cd web

# Step 2: Initialize npm project
npm init -y

# Step 3: Install Vite and React
npm install react react-dom
npm install -D vite @vitejs/plugin-react

# Step 4: Install Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Step 5: Install additional dependencies
npm install axios lucide-react
npm install -D eslint eslint-plugin-react eslint-plugin-react-hooks

# Step 6: Create folder structure
mkdir -p src/{components,services,hooks,utils}
mkdir -p public

# Step 7: Create all configuration files
# Create vite.config.js, tailwind.config.js, etc.

# Step 8: Run development server
npm run dev

# Step 9: Verify
# Open http://localhost:5173
# Modify App.jsx - should see changes instantly
```

## 6. Testing Strategy

### Manual Testing

**Steps**:
1. Navigate to web directory
2. Run `npm install`
3. Run `npm run dev`
4. Open http://localhost:5173 - should see "AI Lightroom" heading
5. Modify App.jsx - should see changes without refresh
6. Add Tailwind class - should see style change

**Expected Results**:
- Dev server starts without errors
- Page renders correctly
- HMR works
- Tailwind classes apply

### Performance Testing

**Benchmarks**:
- Startup time: < 5 seconds
- HMR response: < 1 second
- Bundle size: < 500KB (dev)

## 7. Checklist

### Implementation
- [ ] Create package.json with dependencies
- [ ] Install all dependencies
- [ ] Create Vite configuration
- [ ] Create Tailwind configuration
- [ ] Create PostCSS configuration
- [ ] Create index.html
- [ ] Create main.jsx entry point
- [ ] Create App.jsx component
- [ ] Create index.css with Tailwind directives
- [ ] Create api.js service
- [ ] Create .env.example
- [ ] Create folder structure

### Code Quality
- [ ] Follow React best practices
- [ ] Use functional components
- [ ] Configure ESLint
- [ ] Organize imports

### Testing
- [ ] Test dev server startup
- [ ] Test HMR functionality
- [ ] Test Tailwind CSS
- [ ] Test on multiple browsers

### Documentation
- [ ] Add comments to configuration files
- [ ] Document environment variables
- [ ] Update README with frontend setup

### Review
- [ ] Self-review code
- [ ] Verify all files present
- [ ] Test complete setup

## 8. Resources & References

**Documentation**:
- [Vite Guide](https://vitejs.dev/guide/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/docs)

**Tools & Libraries**:
- Vite - Next generation frontend tooling
- React - UI component library
- Tailwind CSS - Utility-first CSS framework

**Helpful Articles**:
- [Vite + React + Tailwind Setup](https://tailwindcss.com/docs/guides/vite)
- [React Best Practices](https://react.dev/learn)

## 9. Common Issues & Solutions

**Issue 1**: Tailwind classes not applying
- **Solution**: Check tailwind.config.js content paths include all source files
- **Prevention**: Verify configuration before starting development

**Issue 2**: HMR not working
- **Solution**: Check Vite config, ensure plugins are correctly configured
- **Prevention**: Use standard Vite React template setup

**Issue 3**: Port 5173 already in use
- **Solution**: Change port in vite.config.js or kill process
- **Prevention**: Document port usage

**Issue 4**: npm install fails
- **Solution**: Clear npm cache, try again with `--force`
- **Prevention**: Use package-lock.json for consistency

## 10. Time Tracking

| Activity | Estimated | Actual | Notes |
|----------|-----------|--------|-------|
| Create package.json | 15 min | | |
| Install dependencies | 15 min | | |
| Configure Vite | 15 min | | |
| Configure Tailwind | 20 min | | |
| Create components | 30 min | | |
| Create folder structure | 15 min | | |
| Test everything | 30 min | | |
| **Total** | **2.5 hrs** | | |

## 11. Notes

**Development Workflow**:

1. Run `npm run dev` in web directory
2. Make code changes
3. Browser auto-updates via HMR
4. Run `npm run build` for production

**Future Enhancements**:
- Add TypeScript support
- Add testing with Vitest
- Add component library (Radix UI)
- Add state management (Zustand)

---

**Task Status**: 🔴 Not Started
**Last Updated**: 2024-02-27
**Reviewer**: [Name]
