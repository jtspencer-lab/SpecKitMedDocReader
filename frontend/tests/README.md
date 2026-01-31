# Frontend Tests

This directory contains the test suite for the React frontend application.

## Structure

- `unit/`: Unit tests for components, services, hooks
- `e2e/`: End-to-end tests using Playwright

## Running Tests

Run all tests:
```bash
npm run test
```

Run tests in watch mode:
```bash
npm run test:watch
```

Run with coverage:
```bash
npm run test:coverage
```

Run specific test file:
```bash
npm run test -- DocumentUpload.test.tsx
```

Run E2E tests:
```bash
npx playwright test
```

## Test Patterns

- Use React Testing Library for component tests
- Mock API calls with `msw` (Mock Service Worker)
- Test user interactions, not implementation details
- Aim for >70% coverage on components
