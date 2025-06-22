# German Learning Portal - Frontend

Modern React frontend for the German language learning application, built with TypeScript and Vite.

## Technology Stack

- **React 18** with TypeScript for type safety
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **Radix UI** for accessible components
- **React Router** for navigation
- **Lucide React** for icons

## Features

- **German Word Management**: Browse, search, and view German vocabulary
- **Study Activities**: Integrated external study tools
- **Progress Tracking**: Visual dashboards and statistics
- **Responsive Design**: Works on desktop and mobile
- **Dark/Light Theme**: Automatic theme switching
- **Accessibility**: Built with Radix UI for screen reader support

## Development

### Install Dependencies

```sh
npm install
```

### Run Development Server

```sh
npm run dev
```

Available at http://localhost:5173

### Build for Production

```sh
npm run build
```

### Type Checking

```sh
npm run type-check
```

### Linting

```sh
npm run lint
```

## Project Structure

```
src/
  components/     # Reusable UI components
  pages/          # Page-level components
  services/       # API client and types
  context/        # React context providers
  hooks/          # Custom React hooks
  lib/            # Utility functions
```

## German-Specific Features

- **Gender Display**: Shows der/die/das for nouns
- **Plural Forms**: Displays plural variations
- **IPA Pronunciation**: Shows pronunciation guides
- **Grammar Support**: Special handling for German linguistic features
