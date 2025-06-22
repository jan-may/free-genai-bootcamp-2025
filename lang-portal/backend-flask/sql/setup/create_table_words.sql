CREATE TABLE IF NOT EXISTS words (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  german TEXT NOT NULL,
  pronunciation TEXT NOT NULL,
  english TEXT NOT NULL,
  parts TEXT NOT NULL,  -- Store parts as JSON string
  gender TEXT,  -- For nouns: der, die, das
  plural TEXT   -- For noun plural forms
);