# German Learning Portal - Backend

Flask-based REST API for the German language learning application.

## Database Setup

### Initialize Database with German Vocabulary

```sh
invoke init-db
```

This will:
- Create the words.db (SQLite3 database) 
- Run SQL migrations from `sql/setup/`
- Import German seed data:
  - Core German verbs (`seed/data_verbs.json`)
  - Core German adjectives (`seed/data_adjectives.json`) 
  - Core German nouns with gender/plural (`seed/data_nouns.json`)
  - Study activities configuration

### Database Schema

The database supports German-specific features:
- `german`: The German word
- `pronunciation`: IPA pronunciation guide
- `english`: English translation
- `gender`: Grammatical gender (der/die/das)
- `plural`: Plural form for nouns
- `parts`: JSON structure for word components

### Clearing Database

```sh
rm words.db
```

## Running the API Server

```sh
python app.py 
```

Starts the Flask development server on http://localhost:5000

## API Endpoints

- `GET /words` - Paginated German words with sorting
- `GET /words/{id}` - Individual word details
- `GET /groups` - Word groups (verbs, adjectives, nouns)
- `GET /groups/{id}/words` - Words in a specific group
- `GET /study-sessions` - Study session history
- `POST /study-sessions` - Create new study session
