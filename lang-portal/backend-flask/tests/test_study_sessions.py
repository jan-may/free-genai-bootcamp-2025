"""Tests for study sessions API endpoints."""
import json
import pytest


class TestStudySessionsAPI:
    """Test cases for /api/study_sessions endpoints."""
    
    def test_create_study_session(self, client):
        """Test POST /api/study_sessions endpoint."""
        session_data = {
            'group_id': 1,
            'study_activity_id': 1
        }
        
        response = client.post('/api/study_sessions',
                             data=json.dumps(session_data),
                             content_type='application/json')
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert 'session_id' in data
        assert isinstance(data['session_id'], int)
        assert data['session_id'] > 0
    
    def test_create_study_session_missing_fields(self, client):
        """Test POST /api/study_sessions with missing fields."""
        # Missing group_id
        response = client.post('/api/study_sessions',
                             data=json.dumps({'study_activity_id': 1}),
                             content_type='application/json')
        assert response.status_code == 400
        
        # Missing study_activity_id
        response = client.post('/api/study_sessions',
                             data=json.dumps({'group_id': 1}),
                             content_type='application/json')
        assert response.status_code == 400
        
        # Empty body
        response = client.post('/api/study_sessions',
                             data=json.dumps({}),
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_create_study_session_invalid_ids(self, client):
        """Test POST /api/study_sessions with invalid IDs."""
        # Invalid group_id
        response = client.post('/api/study_sessions',
                             data=json.dumps({'group_id': 999, 'study_activity_id': 1}),
                             content_type='application/json')
        assert response.status_code == 400
        
        # Invalid study_activity_id
        response = client.post('/api/study_sessions',
                             data=json.dumps({'group_id': 1, 'study_activity_id': 999}),
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_get_study_sessions_list(self, client):
        """Test GET /api/study-sessions endpoint."""
        # Create a session first
        session_data = {
            'group_id': 1,
            'study_activity_id': 1
        }
        response = client.post('/api/study_sessions',
                             data=json.dumps(session_data),
                             content_type='application/json')
        assert response.status_code == 201
        
        # Get list of sessions
        response = client.get('/api/study-sessions')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'items' in data
        assert 'total' in data
        assert 'page' in data
        assert 'per_page' in data
        assert 'total_pages' in data
        
        assert data['total'] >= 1
        assert len(data['items']) >= 1
        
        # Check session structure
        session = data['items'][0]
        assert 'id' in session
        assert 'group_id' in session
        assert 'activity_id' in session
        assert 'start_time' in session
        assert 'end_time' in session
        assert 'group_name' in session
        assert 'activity_name' in session
        assert 'review_items_count' in session
    
    def test_get_study_sessions_with_pagination(self, client):
        """Test GET /api/study-sessions with pagination."""
        # Create multiple sessions
        for i in range(3):
            session_data = {
                'group_id': 1,
                'study_activity_id': 1
            }
            client.post('/api/study_sessions',
                      data=json.dumps(session_data),
                      content_type='application/json')
        
        response = client.get('/api/study-sessions?page=1&per_page=2')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['page'] == 1
        assert data['per_page'] == 2
        assert len(data['items']) == 2
    
    def test_get_study_session_by_id(self, client):
        """Test GET /api/study-sessions/:id endpoint."""
        # Create a session
        session_data = {
            'group_id': 1,
            'study_activity_id': 1
        }
        response = client.post('/api/study_sessions',
                             data=json.dumps(session_data),
                             content_type='application/json')
        session_id = json.loads(response.data)['session_id']
        
        # Get session details
        response = client.get(f'/api/study-sessions/{session_id}')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'session' in data
        assert 'words' in data
        assert data['session']['id'] == session_id
        assert data['session']['group_id'] == 1
        assert data['session']['activity_id'] == 1
        assert 'start_time' in data['session']
        assert len(data['words']) == 2  # Test Verbs group has 2 words
    
    def test_get_study_session_not_found(self, client):
        """Test GET /api/study-sessions/:id with non-existent session."""
        response = client.get('/api/study-sessions/999')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_submit_word_reviews(self, client):
        """Test POST /api/study_sessions/:id/review endpoint."""
        # Create a session
        session_data = {
            'group_id': 1,
            'study_activity_id': 1
        }
        response = client.post('/api/study_sessions',
                             data=json.dumps(session_data),
                             content_type='application/json')
        session_id = json.loads(response.data)['session_id']
        
        # Submit reviews
        review_data = {
            'reviews': [
                {'word_id': 1, 'is_correct': True},
                {'word_id': 4, 'is_correct': False}
            ]
        }
        response = client.post(f'/api/study_sessions/{session_id}/review',
                             data=json.dumps(review_data),
                             content_type='application/json')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'message' in data
        assert 'reviews_count' in data
        assert data['reviews_count'] == 2
    
    def test_submit_word_reviews_invalid_data(self, client):
        """Test POST /api/study_sessions/:id/review with invalid data."""
        # Create a session
        session_data = {
            'group_id': 1,
            'study_activity_id': 1
        }
        response = client.post('/api/study_sessions',
                             data=json.dumps(session_data),
                             content_type='application/json')
        session_id = json.loads(response.data)['session_id']
        
        # Missing reviews field
        response = client.post(f'/api/study_sessions/{session_id}/review',
                             data=json.dumps({}),
                             content_type='application/json')
        assert response.status_code == 400
        
        # Invalid review structure
        review_data = {
            'reviews': [
                {'word_id': 1}  # Missing is_correct
            ]
        }
        response = client.post(f'/api/study_sessions/{session_id}/review',
                             data=json.dumps(review_data),
                             content_type='application/json')
        assert response.status_code == 400
        
        # Invalid word_id
        review_data = {
            'reviews': [
                {'word_id': 999, 'is_correct': True}
            ]
        }
        response = client.post(f'/api/study_sessions/{session_id}/review',
                             data=json.dumps(review_data),
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_reset_study_sessions(self, client):
        """Test POST /api/study-sessions/reset endpoint."""
        # Create some sessions
        for i in range(2):
            session_data = {
                'group_id': 1,
                'study_activity_id': 1
            }
            client.post('/api/study_sessions',
                      data=json.dumps(session_data),
                      content_type='application/json')
        
        # Reset sessions
        response = client.post('/api/study-sessions/reset')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'message' in data
        
        # Verify sessions are deleted
        response = client.get('/api/study-sessions')
        data = json.loads(response.data)
        assert data['total'] == 0
    
    def test_word_review_statistics_update(self, client):
        """Test that word review statistics are updated correctly."""
        # Create a session
        session_data = {
            'group_id': 1,
            'study_activity_id': 1
        }
        response = client.post('/api/study_sessions',
                             data=json.dumps(session_data),
                             content_type='application/json')
        session_id = json.loads(response.data)['session_id']
        
        # Submit reviews
        review_data = {
            'reviews': [
                {'word_id': 1, 'is_correct': True},
                {'word_id': 4, 'is_correct': False}
            ]
        }
        client.post(f'/api/study_sessions/{session_id}/review',
                  data=json.dumps(review_data),
                  content_type='application/json')
        
        # Check updated statistics
        response = client.get('/api/words/1')
        word_data = json.loads(response.data)
        assert word_data['correct_count'] == 6  # Was 5, now 6
        assert word_data['wrong_count'] == 2    # Remains 2
        
        response = client.get('/api/words/4')
        word_data = json.loads(response.data)
        assert word_data['correct_count'] == 0  # Remains 0
        assert word_data['wrong_count'] == 1    # Was 0, now 1