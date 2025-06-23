"""Test fixtures and data for German vocabulary tests."""

def get_test_words():
    """Return a list of test German words."""
    return [
        {
            'german': 'gehen',
            'pronunciation': 'ˈɡeːən',
            'english': 'to go',
            'parts': '["geh", "en"]',
            'gender': None,
            'plural': None
        },
        {
            'german': 'Haus',
            'pronunciation': 'haʊ̯s',
            'english': 'house',
            'parts': '["Haus"]',
            'gender': 'das',
            'plural': 'Häuser'
        },
        {
            'german': 'schön',
            'pronunciation': 'ʃøːn',
            'english': 'beautiful',
            'parts': '["schön"]',
            'gender': None,
            'plural': None
        },
        {
            'german': 'arbeiten',
            'pronunciation': 'ˈaʁbaɪ̯tn̩',
            'english': 'to work',
            'parts': '["arbeit", "en"]',
            'gender': None,
            'plural': None
        },
        {
            'german': 'Katze',
            'pronunciation': 'ˈkatsə',
            'english': 'cat',
            'parts': '["Katze"]',
            'gender': 'die',
            'plural': 'Katzen'
        }
    ]

def get_test_groups():
    """Return a list of test groups."""
    return [
        {'name': 'Test Verbs', 'words_count': 2},
        {'name': 'Test Nouns', 'words_count': 2},
        {'name': 'Test Adjectives', 'words_count': 1}
    ]

def get_test_study_activities():
    """Return a list of test study activities."""
    return [
        {
            'name': 'Test Activity 1',
            'url': 'http://example.com/activity1',
            'preview_url': 'http://example.com/preview1'
        },
        {
            'name': 'Test Activity 2',
            'url': 'http://example.com/activity2',
            'preview_url': 'http://example.com/preview2'
        }
    ]

def get_test_study_session():
    """Return test study session data."""
    return {
        'group_id': 1,
        'study_activity_id': 1
    }

def get_test_word_reviews():
    """Return test word review data."""
    return [
        {'word_id': 1, 'is_correct': True},
        {'word_id': 2, 'is_correct': False},
        {'word_id': 3, 'is_correct': True}
    ]