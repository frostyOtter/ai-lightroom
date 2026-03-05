# AI Lightroom Frontend

React frontend for AI-powered image color adjustment.

## Setup

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env if needed
```

### Running

```bash
# Development mode
npm run dev

# Production build
npm run build

# Preview production build
npm run preview
```

### Testing

```bash
# Run tests
npm run test

# Run linter
npm run lint
```

## Project Structure

```
web/
├── src/
│   ├── main.jsx          # Entry point
│   ├── App.jsx           # Root component
│   ├── components/       # React components
│   ├── services/         # API services
│   ├── hooks/            # Custom hooks
│   └── utils/            # Utility functions
├── public/               # Static assets
├── index.html            # HTML template
└── package.json          # Dependencies
```

## Key Components

| Component | Description |
|-----------|-------------|
| `ImageUploader` | Image upload with drag-drop |
| `PreferenceInput` | Style preference text input |
| `ResultsDisplay` | Color preset visualization |
| `LoadingSpinner` | Loading indicator |
| `ErrorMessage` | Error display |

## Environment Variables

See [.env.example](./.env.example) for all options.

Required:
- `VITE_API_URL` - Backend API URL

## Troubleshooting

### Module not found
Run `npm install` to ensure all dependencies are installed.

### Port already in use
Vite will automatically use next available port.

### API connection errors
Verify `VITE_API_URL` is correct and backend is running.
