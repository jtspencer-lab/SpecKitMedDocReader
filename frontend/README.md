# Frontend: Document Extraction & Analysis Dashboard

React/TypeScript web dashboard for document extraction review and quality assurance.

## Quick Start

### Prerequisites
- Node.js 18+
- npm or yarn

### Development Setup

1. **Install dependencies**
```bash
cd frontend
npm install
```

2. **Configure environment**
```bash
cp .env.example .env
# Update VITE_API_BASE_URL if backend is at different location
```

3. **Start development server**
```bash
npm run dev
```

App will be available at `http://localhost:5173`

### Using Docker Compose

```bash
docker-compose up --build
```

## Project Structure

```
frontend/
├── src/
│   ├── components/     # Reusable UI components
│   ├── pages/          # Page routes
│   ├── services/       # API client
│   ├── types/          # TypeScript interfaces
│   └── App.tsx         # Root component
├── tests/              # Test suite
├── public/             # Static assets
├── package.json        # Dependencies
└── Dockerfile          # Production image
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run test` - Run tests
- `npm run test:watch` - Run tests in watch mode
- `npm run test:coverage` - Run tests with coverage
- `npm run lint` - Check code quality
- `npm run lint:fix` - Fix linting issues
- `npm run format` - Format code with Prettier
- `npm run type-check` - Check TypeScript types

## Testing

Run unit tests:
```bash
npm run test
```

Run with coverage:
```bash
npm run test:coverage
```

Target: >70% coverage on components

## API Integration

The frontend communicates with the backend API at the URL specified in `.env`:

```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
```

All API requests go through `src/services/api.ts` with automatic:
- Authentication token management
- Error handling
- Timeout handling
- Request/response logging

## TypeScript

All code should have proper type annotations. Run type checking:
```bash
npm run type-check
```

## Code Quality

Enforce code style:
```bash
npm run lint:fix
npm run format
```

## Environment Variables

Key variables in `.env`:
- `VITE_API_BASE_URL`: Backend API endpoint
- `VITE_API_TIMEOUT`: Request timeout (ms)
- `VITE_MAX_FILE_SIZE`: Max file upload size
- `VITE_ITEMS_PER_PAGE`: Pagination size

## Development Guidelines

- Use functional components with hooks
- Prop types should be defined with TypeScript interfaces
- Use React Query for server state
- Use Zustand for client state
- Keep components small and focused
- Test user interactions, not implementation

## Support

See `../README.md` for full project documentation.
