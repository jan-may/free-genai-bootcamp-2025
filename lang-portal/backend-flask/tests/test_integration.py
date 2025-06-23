"""Integration tests for database operations and complex workflows."""
import json
import pytest


class TestDatabaseIntegration:
    """Test cases for database operations and data integrity."""
    
    def test_word_group_relationship_integrity(self, client):
        """Test that word-group relationships maintain integrity."""
        # Get initial state
        response = client.get('/api/groups')
        groups = json.loads(response.data)['groups']
        
        # Verify word counts match actual relationships
        for group in groups:
            response = client.get(f'/api/groups/{group["id"]}/words')
            words = json.loads(response.data)
            assert len(words['words']) == group['word_count']
    
    def test_cascade_delete_prevention(self, app):
        """Test that deleting referenced records is prevented."""
        with app.app_context():
            cursor = app.db.cursor()
            
            # Enable foreign key constraints for this test
            cursor.execute("PRAGMA foreign_keys = ON")
            
            # Try to delete a group that has words - should fail due to foreign key
            with pytest.raises(Exception):
                cursor.execute("DELETE FROM groups WHERE id = 1")
                app.db.commit()
            
            # Try to delete a word that has reviews - should fail
            with pytest.raises(Exception):
                cursor.execute("DELETE FROM words WHERE id = 1")
                app.db.commit()
    
    def test_review_statistics_consistency(self, client):
        """Test that review statistics remain consistent across operations."""
        # Create a session
        session_data = {
            'group_id': 1,
            'study_activity_id': 1
        }
        response = client.post('/api/study_sessions',
                             data=json.dumps(session_data),
                             content_type='application/json')
        session_id = json.loads(response.data)['session_id']
        
        # Submit multiple reviews for the same word
        review_data = {
            'reviews': [
                {'word_id': 1, 'is_correct': True},
                {'word_id': 1, 'is_correct': True},
                {'word_id': 1, 'is_correct': False}
            ]
        }
        client.post(f'/api/study_sessions/{session_id}/review',
                  data=json.dumps(review_data),
                  content_type='application/json')
        
        # Check word statistics
        response = client.get('/api/words/1')
        data = json.loads(response.data)
        word = data['word']
        assert word['correct_count'] == 7  # Was 5, +2
        assert word['wrong_count'] == 3     # Was 2, +1
        
        # Verify review items were created
        response = client.get(f'/api/study-sessions/{session_id}')
        session = json.loads(response.data)
        assert len([w for w in session['words'] if w['id'] == 1]) == 1


class TestComplexWorkflows:
    """Test cases for complex user workflows."""
    
    def test_complete_study_workflow(self, client):
        """Test a complete study session workflow."""
        # 1. Get available groups
        response = client.get('/api/groups')
        groups = json.loads(response.data)['groups']
        group_id = groups[0]['id']
        
        # 2. Get study activities
        response = client.get('/api/study-activities')
        activities = json.loads(response.data)
        activity_id = activities[0]['id']
        
        # 3. Get words for the group
        response = client.get(f'/api/groups/{group_id}/words/raw')
        words = json.loads(response.data)['words']
        word_ids = [w['id'] for w in words]
        
        # 4. Create a study session
        session_data = {
            'group_id': group_id,
            'study_activity_id': activity_id
        }
        response = client.post('/api/study_sessions',
                             data=json.dumps(session_data),
                             content_type='application/json')
        session_id = json.loads(response.data)['session_id']
        
        # 5. Submit reviews
        reviews = [
            {'word_id': word_id, 'is_correct': i % 2 == 0}
            for i, word_id in enumerate(word_ids)
        ]
        review_data = {'reviews': reviews}
        response = client.post(f'/api/study_sessions/{session_id}/review',
                             data=json.dumps(review_data),
                             content_type='application/json')
        assert response.status_code == 200
        
        # 6. Check dashboard stats
        response = client.get('/api/dashboard/stats')
        stats = json.loads(response.data)
        assert stats['total_sessions'] == 1
        assert stats['total_words_studied'] == len(word_ids)
        
        # 7. Check recent session
        response = client.get('/api/dashboard/recent-session')
        recent = json.loads(response.data)
        assert recent['id'] == session_id
    
    def test_multiple_sessions_same_group(self, client):
        """Test multiple study sessions for the same group."""
        group_id = 1
        activity_id = 1
        
        # Create 3 sessions for the same group
        session_ids = []
        for i in range(3):
            session_data = {
                'group_id': group_id,
                'study_activity_id': activity_id
            }
            response = client.post('/api/study_sessions',
                                 data=json.dumps(session_data),
                                 content_type='application/json')
            session_ids.append(json.loads(response.data)['session_id'])
            
            # Submit different reviews each time
            review_data = {
                'reviews': [
                    {'word_id': 1, 'is_correct': i == 0},  # Only correct first time
                    {'word_id': 4, 'is_correct': i != 0}   # Correct second and third
                ]
            }
            client.post(f'/api/study_sessions/{session_ids[i]}/review',
                      data=json.dumps(review_data),
                      content_type='application/json')
        
        # Check group study sessions
        response = client.get(f'/api/groups/{group_id}/study_sessions')
        sessions = json.loads(response.data)
        assert len(sessions['study_sessions']) == 3
        
        # Check word statistics
        response = client.get('/api/words/1')
        data1 = json.loads(response.data)
        word1 = data1['word']
        assert word1['correct_count'] == 6  # Was 5, +1
        assert word1['wrong_count'] == 4    # Was 2, +2
        
        response = client.get('/api/words/4')
        data4 = json.loads(response.data)
        word4 = data4['word']
        assert word4['correct_count'] == 2  # Was 0, +2
        assert word4['wrong_count'] == 1    # Was 0, +1
    
    def test_reset_functionality(self, client):
        """Test the reset functionality clears all study data."""
        # Create some study data
        session_data = {
            'group_id': 1,
            'study_activity_id': 1
        }
        response = client.post('/api/study_sessions',
                             data=json.dumps(session_data),
                             content_type='application/json')
        session_id = json.loads(response.data)['session_id']
        
        review_data = {
            'reviews': [
                {'word_id': 1, 'is_correct': True},
                {'word_id': 4, 'is_correct': False}
            ]
        }
        client.post(f'/api/study_sessions/{session_id}/review',
                  data=json.dumps(review_data),
                  content_type='application/json')
        
        # Reset
        response = client.post('/api/study-sessions/reset')
        assert response.status_code == 200
        
        # Verify everything is cleared
        response = client.get('/api/dashboard/stats')
        stats = json.loads(response.data)
        assert stats['total_sessions'] == 0
        assert stats['total_words_studied'] == 0
        
        # But words and groups should remain
        assert stats['total_vocabulary'] == 5
        
        # Word statistics should be reset
        response = client.get('/api/words/1')
        data = json.loads(response.data)
        word = data['word']
        assert word['correct_count'] == 0
        assert word['wrong_count'] == 0