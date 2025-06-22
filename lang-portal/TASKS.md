# German Language Learning App Migration Tasks

## Database Schema Changes

### Words Table Structure
- [x] Rename `kanji` column to `german` in the words table
- [x] Rename `romaji` column to `pronunciation` (for IPA or phonetic spelling)
- [x] Update all SQL migration files in `backend-flask/sql/setup/`
- [x] Update create_table_words.sql with new column names
- [x] Add new columns if needed (e.g., `gender` for German nouns, `plural` form)

### Seed Data
- [x] Replace Japanese adjectives in `backend-flask/seed/data_adjectives.json` with German adjectives
- [x] Replace Japanese verbs in `backend-flask/seed/data_verbs.json` with German verbs
- [x] Update seed data structure to match new schema (german, pronunciation, english)
- [x] Add additional German-specific data files (nouns with articles, irregular verbs, etc.)
- [x] Update `backend-flask/seed/study_activities.json` with German-appropriate activities

## Backend API Updates

### Database Layer
- [x] Update `backend-flask/lib/db.py` if it has any Japanese-specific logic
- [x] Update all SQL queries to use new column names (german, pronunciation)

### Routes Updates
- [x] Update `backend-flask/routes/words.py` to handle new field names
- [x] Update `backend-flask/routes/groups.py` for any Japanese-specific logic
- [x] Update `backend-flask/routes/dashboard.py` for new field names in statistics
- [x] Update `backend-flask/routes/study_sessions.py` for new field structure
- [x] Update `backend-flask/routes/study_activities.py` if needed

### Migration Scripts
- [x] Update `backend-flask/migrate.py` to handle new schema
- [x] Create migration script to convert existing data (if preserving data)
- [x] Update `backend-flask/tasks.py` to seed German data

## Frontend Updates

### API Service Layer
- [x] Update `frontend-react/src/services/api.ts` interfaces:
  - [x] Change `kanji` to `german` in Word interface
  - [x] Change `romaji` to `pronunciation` in Word interface
  - [x] Add any German-specific fields (gender, plural, etc.)

### Components
- [x] Update `frontend-react/src/components/WordsTable.tsx`:
  - [x] Change column headers from Kanji/Romaji to German/Pronunciation
  - [x] Update field references in the component
- [x] Update `frontend-react/src/components/StudyActivity.tsx` if it has Japanese-specific logic
- [x] Update `frontend-react/src/components/StudySessionsTable.tsx` for new field names

### Pages
- [x] Update `frontend-react/src/pages/Words.tsx` for German terminology
- [x] Update `frontend-react/src/pages/WordShow.tsx`:
  - [x] Display German word instead of Kanji
  - [x] Show pronunciation instead of Romaji
  - [x] Add German-specific fields if added
- [x] Update `frontend-react/src/pages/Dashboard.tsx` for any Japanese references
- [x] Update `frontend-react/src/pages/StudyActivityShow.tsx` for German context
- [x] Update `frontend-react/src/pages/StudyActivityLaunch.tsx` if needed
- [x] Update `frontend-react/src/pages/GroupShow.tsx` for new field names

## UI/UX Updates

### Text and Labels
- [x] Search and replace all Japanese-specific UI text with German equivalents
- [x] Update page titles and navigation labels
- [x] Update breadcrumb text
- [x] Update any help text or instructions

### Visual Updates
- [x] Update app logo/branding if Japanese-specific
- [x] Update favicon if needed
- [x] Update any Japanese-specific icons or images
- [x] Update study activity preview images in `frontend-react/public/assets/study_activities/`

## Configuration and Documentation

### Configuration Files
- [x] Update `frontend-react/package.json` metadata (name, description)
- [x] Update `frontend-react/public/site.webmanifest` with German app info
- [x] Update `frontend-react/index.html` page title

### Documentation
- [x] Update main `Readme.md` to describe German language learning
- [x] Update `backend-flask/Readme.md` with German examples
- [x] Update `frontend-react/README.md` with German context
- [x] Update any API documentation with new field names

## External Study Activities

### Activity Integration
- [x] Identify German-appropriate study activities to replace Japanese ones
- [x] Update typing tutor (if keeping) for German keyboard layout
- [x] Update activity URLs in database seed data
- [x] Test CORS configuration with new activity URLs

## Testing and Validation

### Data Validation
- [ ] Test word creation with German words
- [ ] Verify pronunciation field works correctly
- [ ] Test special German characters (ä, ö, ü, ß)
- [ ] Verify sorting works with German alphabet

### Functionality Testing
- [ ] Test all CRUD operations with new schema
- [ ] Verify study sessions record correctly
- [ ] Test dashboard statistics with German data
- [ ] Verify pagination and search work properly

### Cross-browser Testing
- [ ] Test German character display across browsers
- [ ] Verify responsive design with longer German words
- [ ] Test theme switching with new content

## Deployment Preparation

### Database Migration
- [ ] Create backup of existing data
- [ ] Prepare migration scripts for production
- [ ] Document migration process

### Environment Setup
- [ ] Update any environment-specific configurations
- [ ] Prepare German-specific seed data for different environments
- [ ] Update deployment documentation

## Optional Enhancements

### German-Specific Features
- [ ] Add gender indicator for nouns (der/die/das)
- [ ] Add plural forms for nouns
- [ ] Add verb conjugation tables
- [ ] Add case declension support (Nominativ, Akkusativ, etc.)
- [ ] Add separable verb indicators
- [ ] Add pronunciation audio support

### Study Features
- [ ] Add German-specific study modes (gender practice, case practice)
- [ ] Add irregular verb practice
- [ ] Add sentence structure exercises
- [ ] Add German idioms and phrases section

## Final Cleanup

### Code Cleanup
- [x] Remove any unused Japanese-specific code
- [x] Update code comments to reflect German context
- [x] Ensure consistent naming throughout codebase

### Repository Updates
- [x] Update repository description
- [x] Update tags/topics for German language
- [x] Archive or remove Japanese-specific resources