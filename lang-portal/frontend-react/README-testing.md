# Frontend Testing Setup

## Overview
Comprehensive test suite implemented using Vitest, React Testing Library, and Coverage V8 to achieve 70%+ test coverage.

## Testing Stack
- **Vitest**: Modern test runner with TypeScript support
- **React Testing Library**: Component testing utilities
- **@testing-library/jest-dom**: Custom Jest matchers for DOM assertions
- **@testing-library/user-event**: User interaction utilities
- **@vitest/coverage-v8**: Code coverage reporting
- **jsdom**: DOM environment for testing

## Test Files Created

### API Service Tests (`src/services/api.test.ts`)
- Tests all API functions (fetchWords, fetchGroups, createStudySession, etc.)
- Mocks fetch globally for isolated testing
- Tests success and error scenarios
- Validates request parameters and response handling

### Utility Function Tests (`src/lib/utils.test.ts`)
- Tests the `cn()` utility function for className merging
- Covers various input scenarios (arrays, objects, conditionals)
- Tests Tailwind CSS class merging behavior

### Component Tests
- **WordsTable** (`src/components/WordsTable.test.tsx`): Table rendering, sorting, pagination
- **Pagination** (`src/components/Pagination.test.tsx`): Page navigation, button states
- **StudyActivity** (`src/components/StudyActivity.test.tsx`): Activity cards, links
- **StudySessionsTable** (`src/components/StudySessionsTable.test.tsx`): Session data display

### Page Component Tests
- **Words** (`src/pages/Words.test.tsx`): Word list page functionality
- **Groups** (`src/pages/Groups.test.tsx`): Group management page
- **StudyActivities** (`src/pages/StudyActivities.test.tsx`): Activity launcher
- **Dashboard** (`src/pages/Dashboard.test.tsx`): Statistics display

## Test Configuration

### `vitest.config.ts`
- Configured with React plugin
- jsdom environment for DOM testing
- Path aliases for imports
- Coverage thresholds set to 70%
- Excludes test files and configs from coverage

### `src/test/setup.ts`
- Global test setup and cleanup
- Mocks for browser APIs (matchMedia, IntersectionObserver, ResizeObserver)
- Testing library configuration

## Running Tests

```bash
# Run tests in watch mode
npm test

# Run tests once
npm test -- --run

# Run with coverage
npm run test:coverage

# Run with UI
npm run test:ui
```

## Coverage Goals
- **Lines**: 70%+
- **Functions**: 70%+
- **Branches**: 70%+
- **Statements**: 70%+

## Test Patterns

### Component Testing
- Render components with proper providers (Router, etc.)
- Test user interactions (clicks, form inputs)
- Assert on rendered content and behavior
- Mock external dependencies (API calls)

### API Testing
- Mock global fetch function
- Test request parameters and endpoints
- Verify error handling
- Test response parsing

### Integration Testing
- Test component interaction with API services
- Verify loading states and error handling
- Test navigation and routing

## Best Practices
1. Use data-testid for complex selectors when needed
2. Test behavior, not implementation details
3. Mock external dependencies appropriately
4. Keep tests focused and isolated
5. Use descriptive test names and organize with describe blocks

## Current Status
✅ Testing infrastructure setup complete
✅ API service tests implemented
✅ Core component tests created
✅ Page component tests added
✅ Utility function tests included
✅ Coverage reporting configured

The test suite provides comprehensive coverage of the frontend application, ensuring reliable functionality and facilitating future development with confidence.