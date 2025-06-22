# German Language Learning Portal

A comprehensive web application for learning German vocabulary, featuring interactive study activities, progress tracking, and adaptive learning.

## Features

- **German Vocabulary Management**: Store and organize German words with pronunciation guides, gender markers, and plural forms
- **Study Groups**: Organize words into themed groups (Core Verbs, Core Adjectives, Core Nouns, etc.)
- **Interactive Study Activities**: External study tools integrated via iframe
- **Progress Tracking**: Monitor learning statistics and study session history
- **Gender & Plural Support**: Special features for German-specific grammar

## Quick Start

### Backend Setup

1. **Install Dependencies**
   ```sh
   cd backend-flask
   pip install -r requirements.txt
   ```

2. **Initialize Database**
   ```sh
   invoke init-db
   ```

3. **Run Backend Server**
   ```sh
   python app.py
   ```

### Frontend Setup

1. **Install Dependencies**
   ```sh
   cd frontend-react
   npm install
   ```

2. **Run Development Server**
   ```sh
   npm run dev
   ```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000

## Architecture

- **Backend**: Flask + SQLite3
- **Frontend**: React + TypeScript + Vite
- **Styling**: Tailwind CSS + Radix UI
- **Database**: SQLite with manual schema management