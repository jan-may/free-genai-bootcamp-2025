"""Tests for words API endpoints."""
import json
import pytest


class TestWordsAPI:
    """Test cases for /api/words endpoints."""
    
    def test_get_words_list(self, client):
        """Test GET /api/words endpoint."""
        response = client.get('/api/words')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'words' in data
        assert 'total_words' in data
        assert 'current_page' in data
        assert 'total_pages' in data
        
        # We have 5 test words
        assert data['total_words'] == 5
        assert len(data['words']) == 5
        
        # Check word structure
        word = data['words'][0]
        assert 'id' in word
        assert 'german' in word
        assert 'pronunciation' in word
        assert 'english' in word
        assert 'gender' in word
        assert 'plural' in word
        assert 'correct_count' in word
        assert 'wrong_count' in word
    
    def test_get_words_with_pagination(self, client):
        """Test GET /api/words with pagination."""
        response = client.get('/api/words?page=1')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['current_page'] == 1
        assert len(data['words']) == 5  # All words fit in one page (50 per page)
        assert data['total_pages'] == 1
    
    def test_get_words_with_sorting(self, client):
        """Test GET /api/words with sorting."""
        # Sort by german ascending
        response = client.get('/api/words?sort_by=german&order=asc')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        words = data['words']
        # In SQLite, capital letters sort before lowercase letters
        assert words[0]['german'] == 'Haus'
        assert words[-1]['german'] == 'schön'
        
        # Sort by german descending
        response = client.get('/api/words?sort_by=german&order=desc')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        words = data['words']
        assert words[0]['german'] == 'schön'
        assert words[-1]['german'] == 'Haus'
    
    def test_get_words_invalid_parameters(self, client):
        """Test GET /api/words with invalid parameters."""
        # Invalid page - should use default (validation warnings but still works)
        response = client.get('/api/words?page=0')
        assert response.status_code == 200  # Still works with default values
        
        # Invalid sort field - should use default
        response = client.get('/api/words?sort_by=invalid_field')
        assert response.status_code == 200  # Still works with default sort
        
        # Invalid order - should use default
        response = client.get('/api/words?order=invalid')
        assert response.status_code == 200  # Still works with default order
    
    def test_get_word_by_id(self, client):
        """Test GET /api/words/:id endpoint."""
        response = client.get('/api/words/1')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        word = data['word']
        assert word['id'] == 1
        assert word['german'] == 'gehen'
        assert word['english'] == 'to go'
        assert 'groups' in word
        assert len(word['groups']) == 1
        assert word['groups'][0]['name'] == 'Test Verbs'
    
    def test_get_word_by_id_not_found(self, client):
        """Test GET /api/words/:id with non-existent word."""
        response = client.get('/api/words/999')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_get_word_by_id_invalid(self, client):
        """Test GET /api/words/:id with invalid ID."""
        response = client.get('/api/words/invalid')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_word_with_gender_and_plural(self, client):
        """Test word with gender and plural forms."""
        response = client.get('/api/words/2')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        word = data['word']
        assert word['german'] == 'Haus'
        assert word['gender'] == 'das'
        assert word['plural'] == 'Häuser'
    
    def test_word_review_statistics(self, client):
        """Test word review statistics are included."""
        response = client.get('/api/words')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        words = data['words']
        
        # Find word with ID 1 (has review stats)
        word_with_stats = next(w for w in words if w['id'] == 1)
        assert 'correct_count' in word_with_stats
        assert 'wrong_count' in word_with_stats
        assert word_with_stats['correct_count'] == 5
        assert word_with_stats['wrong_count'] == 2
        
        # Find word with ID 3 (no review stats)
        word_without_stats = next(w for w in words if w['id'] == 3)
        assert word_without_stats['correct_count'] == 0
        assert word_without_stats['wrong_count'] == 0