"""Tests for groups API endpoints."""
import json
import pytest


class TestGroupsAPI:
    """Test cases for /api/groups endpoints."""
    
    def test_get_groups_list(self, client):
        """Test GET /api/groups endpoint."""
        response = client.get('/api/groups')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'groups' in data
        assert 'current_page' in data
        assert 'total_pages' in data
        
        # We have 3 test groups
        assert len(data['groups']) == 3
        
        # Check group structure
        group = data['groups'][0]
        assert 'id' in group
        assert 'group_name' in group
        assert 'word_count' in group
        
        # Check word counts
        groups = {g['group_name']: g['word_count'] for g in data['groups']}
        assert groups['Test Verbs'] == 2
        assert groups['Test Nouns'] == 2
        assert groups['Test Adjectives'] == 1
    
    def test_get_groups_with_pagination(self, client):
        """Test GET /api/groups with pagination."""
        response = client.get('/api/groups?page=1')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['current_page'] == 1
        assert len(data['groups']) == 3  # All groups fit in one page (10 per page)
        assert data['total_pages'] == 1
    
    def test_get_groups_invalid_parameters(self, client):
        """Test GET /api/groups with invalid parameters."""
        # Invalid page - should use default
        response = client.get('/api/groups?page=-1')
        assert response.status_code == 200  # Still works with default values
        
        # Invalid per_page is not supported by the API
        response = client.get('/api/groups?page=0')
        assert response.status_code == 200  # Still works with default values
    
    def test_get_group_by_id(self, client):
        """Test GET /api/groups/:id endpoint."""
        response = client.get('/api/groups/1')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['id'] == 1
        assert data['group_name'] == 'Test Verbs'
        assert data['word_count'] == 2
    
    def test_get_group_by_id_not_found(self, client):
        """Test GET /api/groups/:id with non-existent group."""
        response = client.get('/api/groups/999')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_get_group_by_id_invalid(self, client):
        """Test GET /api/groups/:id with invalid ID."""
        response = client.get('/api/groups/invalid')
        assert response.status_code == 404  # Flask returns 404 for invalid route parameters
        
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_get_group_words(self, client):
        """Test GET /api/groups/:id/words endpoint."""
        response = client.get('/api/groups/1/words')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'words' in data
        assert 'current_page' in data
        assert 'total_pages' in data
        assert len(data['words']) == 2
        
        # Check that we get the correct words for Test Verbs group
        german_words = [w['german'] for w in data['words']]
        assert 'gehen' in german_words
        assert 'arbeiten' in german_words
    
    def test_get_group_words_with_pagination(self, client):
        """Test GET /api/groups/:id/words with pagination."""
        response = client.get('/api/groups/1/words?page=1')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['current_page'] == 1
        assert len(data['words']) == 2  # All words fit in one page (10 per page)
        assert data['total_pages'] == 1
    
    def test_get_group_words_raw(self, client):
        """Test GET /api/groups/:id/words/raw endpoint."""
        response = client.get('/api/groups/1/words/raw')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'words' in data
        assert len(data['words']) == 2
        
        # Check word structure includes all fields
        word = data['words'][0]
        assert 'id' in word
        assert 'german' in word
        assert 'pronunciation' in word
        assert 'english' in word
        assert 'parts' in word
        assert 'gender' in word
        assert 'plural' in word
        assert 'correct_count' in word
        assert 'wrong_count' in word
    
    def test_get_group_words_not_found(self, client):
        """Test GET /api/groups/:id/words with non-existent group."""
        response = client.get('/api/groups/999/words')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_get_group_study_sessions(self, client):
        """Test GET /api/groups/:id/study_sessions endpoint."""
        # First create a study session
        session_data = {
            'group_id': 1,
            'study_activity_id': 1
        }
        response = client.post('/api/study_sessions',
                             data=json.dumps(session_data),
                             content_type='application/json')
        assert response.status_code == 201
        
        # Now get study sessions for the group
        response = client.get('/api/groups/1/study_sessions')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'study_sessions' in data
        assert 'current_page' in data
        assert 'total_pages' in data
        assert len(data['study_sessions']) >= 1
        
        # Check session structure
        session = data['study_sessions'][0]
        assert 'id' in session
        assert 'group_id' in session
        assert 'study_activity_id' in session
        assert 'start_time' in session
        assert 'end_time' in session
        assert 'activity_name' in session
        assert 'group_name' in session
        assert 'review_items_count' in session
    
    def test_get_group_study_sessions_empty(self, client):
        """Test GET /api/groups/:id/study_sessions with no sessions."""
        response = client.get('/api/groups/3/study_sessions')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert len(data['study_sessions']) == 0
        assert data['total_pages'] == 0