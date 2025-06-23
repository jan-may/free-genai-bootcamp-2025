"""Tests for dashboard API endpoints."""
import json
import pytest


class TestDashboardAPI:
    """Test cases for /api/dashboard endpoints."""
    
    def test_get_dashboard_stats(self, client):
        """Test GET /api/dashboard/stats endpoint."""
        response = client.get('/api/dashboard/stats')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'total_vocabulary' in data
        assert 'total_words_studied' in data
        assert 'mastered_words' in data
        assert 'success_rate' in data
        assert 'total_sessions' in data
        assert 'active_groups' in data
        assert 'current_streak' in data
        
        # Check initial values
        assert data['total_vocabulary'] == 5
        assert data['total_words_studied'] == 0
        assert data['mastered_words'] == 0
        assert data['success_rate'] == 0
        assert data['total_sessions'] == 0
        assert data['active_groups'] == 0
        assert data['current_streak'] == 0
    
    def test_get_dashboard_stats_with_sessions(self, client):
        """Test GET /api/dashboard/stats with study sessions."""
        # Create a study session
        session_data = {
            'group_id': 1,
            'study_activity_id': 1
        }
        response = client.post('/api/study_sessions',
                             data=json.dumps(session_data),
                             content_type='application/json')
        session_id = json.loads(response.data)['session_id']
        
        # Submit some reviews
        review_data = {
            'reviews': [
                {'word_id': 1, 'is_correct': True},
                {'word_id': 4, 'is_correct': False}
            ]
        }
        client.post(f'/api/study_sessions/{session_id}/review',
                  data=json.dumps(review_data),
                  content_type='application/json')
        
        # Check updated stats
        response = client.get('/api/dashboard/stats')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['total_sessions'] == 1
        assert data['total_words_studied'] == 2  # 2 different words studied
        assert abs(data['success_rate'] - 0.5) < 0.01  # 1 correct out of 2 (0.5 as decimal)
    
    def test_get_recent_session_empty(self, client):
        """Test GET /api/dashboard/recent-session with no sessions."""
        response = client.get('/api/dashboard/recent-session')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data is None
    
    def test_get_recent_session_with_data(self, client):
        """Test GET /api/dashboard/recent-session with sessions."""
        # Create multiple study sessions
        session_ids = []
        for i in range(2):
            session_data = {
                'group_id': i + 1,  # Different groups
                'study_activity_id': 1
            }
            response = client.post('/api/study_sessions',
                                 data=json.dumps(session_data),
                                 content_type='application/json')
            session_ids.append(json.loads(response.data)['session_id'])
        
        last_session_id = session_ids[-1]  # Remember the last session ID
        
        # Get recent session
        response = client.get('/api/dashboard/recent-session')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data is not None
        assert data['id'] == last_session_id
        assert 'group_id' in data
        assert 'activity_name' in data
        assert 'created_at' in data
    
    def test_dashboard_stats_accuracy_calculation(self, client):
        """Test accuracy calculation in dashboard stats."""
        # Create a session and submit mixed results
        session_data = {
            'group_id': 1,
            'study_activity_id': 1
        }
        response = client.post('/api/study_sessions',
                             data=json.dumps(session_data),
                             content_type='application/json')
        session_id = json.loads(response.data)['session_id']
        
        # Submit reviews with 3 correct and 1 wrong
        review_data = {
            'reviews': [
                {'word_id': 1, 'is_correct': True},
                {'word_id': 4, 'is_correct': True},
                {'word_id': 1, 'is_correct': True},
                {'word_id': 4, 'is_correct': False}
            ]
        }
        client.post(f'/api/study_sessions/{session_id}/review',
                  data=json.dumps(review_data),
                  content_type='application/json')
        
        # Check accuracy
        response = client.get('/api/dashboard/stats')
        data = json.loads(response.data)
        assert data['total_words_studied'] == 2  # 2 different words studied
        assert abs(data['success_rate'] - 0.75) < 0.01  # 3 correct out of 4 (0.75 as decimal)
    
    def test_dashboard_stats_multiple_sessions(self, client):
        """Test dashboard stats with multiple sessions."""
        # Create 3 sessions with different groups
        for i in range(3):
            session_data = {
                'group_id': (i % 3) + 1,
                'study_activity_id': (i % 2) + 1
            }
            response = client.post('/api/study_sessions',
                                 data=json.dumps(session_data),
                                 content_type='application/json')
            session_id = json.loads(response.data)['session_id']
            
            # Submit some reviews for each session
            review_data = {
                'reviews': [
                    {'word_id': 1, 'is_correct': i % 2 == 0}  # Alternate correct/wrong
                ]
            }
            client.post(f'/api/study_sessions/{session_id}/review',
                      data=json.dumps(review_data),
                      content_type='application/json')
        
        # Check stats
        response = client.get('/api/dashboard/stats')
        data = json.loads(response.data)
        assert data['total_sessions'] == 3
        assert data['total_words_studied'] == 1  # Only 1 word studied (word_id=1)
        # 2 correct out of 3 reviews (as decimal)
        assert abs(data['success_rate'] - 0.6667) < 0.01