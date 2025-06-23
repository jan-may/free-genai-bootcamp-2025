"""Tests for study activities API endpoints."""
import json
import pytest


class TestStudyActivitiesAPI:
    """Test cases for /api/study-activities endpoints."""
    
    def test_get_study_activities_list(self, client):
        """Test GET /api/study-activities endpoint."""
        response = client.get('/api/study-activities')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'study_activities' in data
        assert isinstance(data['study_activities'], list)
        assert len(data['study_activities']) == 2
        
        # Check activity structure
        activity = data['study_activities'][0]
        assert 'id' in activity
        assert 'name' in activity
        assert 'url' in activity
        assert 'preview_url' in activity
        
        # Check test data
        activities = {a['name']: a for a in data['study_activities']}
        assert 'Test Activity 1' in activities
        assert 'Test Activity 2' in activities
        
        activity1 = activities['Test Activity 1']
        assert activity1['url'] == 'http://example.com/activity1'
        assert activity1['preview_url'] == 'http://example.com/preview1'
    
    def test_study_activities_used_in_sessions(self, client):
        """Test that study activities are properly referenced in sessions."""
        # Create a study session with an activity
        session_data = {
            'group_id': 1,
            'study_activity_id': 1
        }
        response = client.post('/api/study_sessions',
                             data=json.dumps(session_data),
                             content_type='application/json')
        assert response.status_code == 201
        session_id = json.loads(response.data)['session_id']
        
        # Get the session and verify it includes the activity
        response = client.get(f'/api/study-sessions/{session_id}')
        assert response.status_code == 200
        
        session = json.loads(response.data)
        assert session['study_activity_id'] == 1
        
        # Get all sessions and verify activity name is included
        response = client.get('/api/study-sessions')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        session = data['study_sessions'][0]
        assert session['activity_name'] == 'Test Activity 1'
    
    def test_study_activities_order(self, client):
        """Test that study activities maintain their order."""
        response = client.get('/api/study-activities')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        activities = data['study_activities']
        
        # Should be ordered by ID
        assert activities[0]['id'] == 1
        assert activities[1]['id'] == 2
        assert activities[0]['name'] == 'Test Activity 1'
        assert activities[1]['name'] == 'Test Activity 2'
    
    def test_study_activity_urls_format(self, client):
        """Test that study activity URLs are properly formatted."""
        response = client.get('/api/study-activities')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        activities = data['study_activities']
        
        for activity in activities:
            # Check URL format
            assert activity['url'].startswith('http://')
            assert activity['preview_url'].startswith('http://')
            
            # Ensure URLs are different
            assert activity['url'] != activity['preview_url']
    
    def test_study_activities_with_no_data(self, app):
        """Test study activities endpoint with empty database."""
        # Create a new test client with empty database
        with app.app_context():
            cursor = app.db.cursor()
            cursor.execute("DELETE FROM study_activities")
            app.db.commit()
            
            client = app.test_client()
            response = client.get('/api/study-activities')
            assert response.status_code == 200
            
            data = json.loads(response.data)
            assert data['study_activities'] == []