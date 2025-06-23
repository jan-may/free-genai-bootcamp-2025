import pytest
import tempfile
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app import create_app
from lib.db import Db

@pytest.fixture
def app():
    """Create and configure a test Flask application."""
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })
    
    # Initialize the test database
    with app.app_context():
        cursor = app.db.cursor()
        
        # Create tables
        app.db.setup_tables(cursor)
        
        # Insert test data
        cursor.executescript("""
            INSERT INTO groups (name, words_count) VALUES 
                ('Test Verbs', 0),
                ('Test Nouns', 0),
                ('Test Adjectives', 0);
            
            INSERT INTO words (german, pronunciation, english, parts, gender, plural) VALUES 
                ('gehen', 'ˈɡeːən', 'to go', '["geh", "en"]', NULL, NULL),
                ('Haus', 'haʊ̯s', 'house', '["Haus"]', 'das', 'Häuser'),
                ('schön', 'ʃøːn', 'beautiful', '["schön"]', NULL, NULL),
                ('arbeiten', 'ˈaʁbaɪ̯tn̩', 'to work', '["arbeit", "en"]', NULL, NULL),
                ('Katze', 'ˈkatsə', 'cat', '["Katze"]', 'die', 'Katzen');
            
            INSERT INTO word_groups (word_id, group_id) VALUES 
                (1, 1),  -- gehen in Test Verbs
                (4, 1),  -- arbeiten in Test Verbs
                (2, 2),  -- Haus in Test Nouns
                (5, 2),  -- Katze in Test Nouns
                (3, 3);  -- schön in Test Adjectives
            
            UPDATE groups SET words_count = (
                SELECT COUNT(*) FROM word_groups WHERE group_id = groups.id
            );
            
            INSERT INTO study_activities (name, url, preview_url) VALUES 
                ('Test Activity 1', 'http://example.com/activity1', 'http://example.com/preview1'),
                ('Test Activity 2', 'http://example.com/activity2', 'http://example.com/preview2');
            
            INSERT INTO word_reviews (word_id, correct_count, wrong_count, last_reviewed) VALUES
                (1, 5, 2, datetime('now')),
                (2, 3, 1, datetime('now'));
        """)
        
        app.db.commit()
    
    yield app
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create a test runner for the Flask application."""
    return app.test_cli_runner()