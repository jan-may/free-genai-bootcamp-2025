from flask import request, jsonify, g
from flask_cors import cross_origin
from datetime import datetime
import math
from lib.validation import (
    validate_pagination_params, validate_sort_params, validate_positive_integer,
    validate_required_fields, validate_word_review
)

def load(app):
  @app.route('/api/study_sessions', methods=['POST'])
  @cross_origin()
  def create_study_session():
    try:
      cursor = app.db.cursor()
      
      # Get and validate request data
      data = request.get_json()
      
      # Validate required fields
      field_errors = validate_required_fields(data, ['group_id', 'study_activity_id'])
      if field_errors:
        return jsonify({"error": field_errors[0]}), 400
      
      # Validate group_id
      group_id, group_error = validate_positive_integer(data.get('group_id'), 'group_id')
      if group_error:
        return jsonify({"error": group_error}), 400
      
      # Validate study_activity_id
      study_activity_id, activity_error = validate_positive_integer(data.get('study_activity_id'), 'study_activity_id')
      if activity_error:
        return jsonify({"error": activity_error}), 400
      
      # Verify group exists
      cursor.execute('SELECT id FROM groups WHERE id = ?', (group_id,))
      if not cursor.fetchone():
        return jsonify({"error": "Group not found"}), 404
      
      # Verify study activity exists
      cursor.execute('SELECT id FROM study_activities WHERE id = ?', (study_activity_id,))
      if not cursor.fetchone():
        return jsonify({"error": "Study activity not found"}), 404
      
      # Create study session
      cursor.execute('''
        INSERT INTO study_sessions (group_id, study_activity_id, created_at)
        VALUES (?, ?, datetime('now'))
      ''', (group_id, study_activity_id))
      
      session_id = cursor.lastrowid
      app.db.commit()
      
      return jsonify({"session_id": session_id}), 201
      
    except Exception as e:
      return jsonify({"error": str(e)}), 500

  @app.route('/api/study-sessions', methods=['GET'])
  @cross_origin()
  def get_study_sessions():
    try:
      cursor = app.db.cursor()
      
      # Get pagination parameters
      page = request.args.get('page', 1, type=int)
      per_page = request.args.get('per_page', 10, type=int)
      offset = (page - 1) * per_page

      # Get total count
      cursor.execute('''
        SELECT COUNT(*) as count 
        FROM study_sessions ss
        JOIN groups g ON g.id = ss.group_id
        JOIN study_activities sa ON sa.id = ss.study_activity_id
      ''')
      total_count = cursor.fetchone()['count']

      # Get paginated sessions
      cursor.execute('''
        SELECT 
          ss.id,
          ss.group_id,
          g.name as group_name,
          sa.id as activity_id,
          sa.name as activity_name,
          ss.created_at,
          COUNT(wri.id) as review_items_count
        FROM study_sessions ss
        JOIN groups g ON g.id = ss.group_id
        JOIN study_activities sa ON sa.id = ss.study_activity_id
        LEFT JOIN word_review_items wri ON wri.study_session_id = ss.id
        GROUP BY ss.id
        ORDER BY ss.created_at DESC
        LIMIT ? OFFSET ?
      ''', (per_page, offset))
      sessions = cursor.fetchall()

      return jsonify({
        'items': [{
          'id': session['id'],
          'group_id': session['group_id'],
          'group_name': session['group_name'],
          'activity_id': session['activity_id'],
          'activity_name': session['activity_name'],
          'start_time': session['created_at'],
          'end_time': session['created_at'],  # For now, just use the same time since we don't track end time
          'review_items_count': session['review_items_count']
        } for session in sessions],
        'total': total_count,
        'page': page,
        'per_page': per_page,
        'total_pages': math.ceil(total_count / per_page)
      })
    except Exception as e:
      return jsonify({"error": str(e)}), 500

  @app.route('/api/study-sessions/<id>', methods=['GET'])
  @cross_origin()
  def get_study_session(id):
    try:
      cursor = app.db.cursor()
      
      # Get session details
      cursor.execute('''
        SELECT 
          ss.id,
          ss.group_id,
          g.name as group_name,
          sa.id as activity_id,
          sa.name as activity_name,
          ss.created_at,
          COUNT(wri.id) as review_items_count
        FROM study_sessions ss
        JOIN groups g ON g.id = ss.group_id
        JOIN study_activities sa ON sa.id = ss.study_activity_id
        LEFT JOIN word_review_items wri ON wri.study_session_id = ss.id
        WHERE ss.id = ?
        GROUP BY ss.id
      ''', (id,))
      
      session = cursor.fetchone()
      if not session:
        return jsonify({"error": "Study session not found"}), 404

      # Get pagination parameters
      page = request.args.get('page', 1, type=int)
      per_page = request.args.get('per_page', 10, type=int)
      offset = (page - 1) * per_page

      # Get the words reviewed in this session with their review status
      cursor.execute('''
        SELECT 
          w.*,
          COALESCE(SUM(CASE WHEN wri.correct = 1 THEN 1 ELSE 0 END), 0) as session_correct_count,
          COALESCE(SUM(CASE WHEN wri.correct = 0 THEN 1 ELSE 0 END), 0) as session_wrong_count
        FROM words w
        JOIN word_review_items wri ON wri.word_id = w.id
        WHERE wri.study_session_id = ?
        GROUP BY w.id
        ORDER BY w.german
        LIMIT ? OFFSET ?
      ''', (id, per_page, offset))
      
      words = cursor.fetchall()

      # Get total count of words
      cursor.execute('''
        SELECT COUNT(DISTINCT w.id) as count
        FROM words w
        JOIN word_review_items wri ON wri.word_id = w.id
        WHERE wri.study_session_id = ?
      ''', (id,))
      
      total_count = cursor.fetchone()['count']

      return jsonify({
        'session': {
          'id': session['id'],
          'group_id': session['group_id'],
          'group_name': session['group_name'],
          'activity_id': session['activity_id'],
          'activity_name': session['activity_name'],
          'start_time': session['created_at'],
          'end_time': session['created_at'],  # For now, just use the same time
          'review_items_count': session['review_items_count']
        },
        'words': [{
          'id': word['id'],
          'german': word['german'],
          'pronunciation': word['pronunciation'],
          'gender': word['gender'],
          'plural': word['plural'],
          'english': word['english'],
          'correct_count': word['session_correct_count'],
          'wrong_count': word['session_wrong_count']
        } for word in words],
        'total': total_count,
        'page': page,
        'per_page': per_page,
        'total_pages': math.ceil(total_count / per_page)
      })
    except Exception as e:
      return jsonify({"error": str(e)}), 500

  @app.route('/api/study_sessions/<int:session_id>/review', methods=['POST'])
  @cross_origin()
  def submit_study_session_review(session_id):
    try:
      # Validate session_id parameter
      validated_session_id, session_error = validate_positive_integer(session_id, 'session_id')
      if session_error:
        return jsonify({"error": session_error}), 400
      
      cursor = app.db.cursor()
      
      # Get and validate request data
      data = request.get_json()
      
      # Validate required fields
      field_errors = validate_required_fields(data, ['reviews'])
      if field_errors:
        return jsonify({"error": field_errors[0]}), 400
      
      reviews = data.get('reviews', [])
      if not isinstance(reviews, list) or len(reviews) == 0:
        return jsonify({"error": "Reviews must be a non-empty array"}), 400
      
      # Verify study session exists
      cursor.execute('SELECT id FROM study_sessions WHERE id = ?', (validated_session_id,))
      if not cursor.fetchone():
        return jsonify({"error": "Study session not found"}), 404
      
      # Validate each review
      for i, review in enumerate(reviews):
        is_valid, error_msg = validate_word_review(review)
        if not is_valid:
          return jsonify({"error": f"Review {i+1}: {error_msg}"}), 400
      
      # Process each review
      for review in reviews:
        word_id = review['word_id']  # Already validated
        is_correct = review['is_correct']  # Already validated
        
        # Verify word exists
        cursor.execute('SELECT id FROM words WHERE id = ?', (word_id,))
        if not cursor.fetchone():
          return jsonify({"error": f"Word with id {word_id} not found"}), 404
        
        # Insert word review item
        cursor.execute('''
          INSERT INTO word_review_items (word_id, study_session_id, correct, created_at)
          VALUES (?, ?, ?, datetime('now'))
        ''', (word_id, validated_session_id, 1 if is_correct else 0))
        
        # Update or create word review aggregate
        cursor.execute('''
          INSERT INTO word_reviews (word_id, correct_count, wrong_count, last_reviewed)
          VALUES (?, ?, ?, datetime('now'))
          ON CONFLICT(word_id) DO UPDATE SET
            correct_count = correct_count + ?,
            wrong_count = wrong_count + ?,
            last_reviewed = datetime('now')
        ''', (
          word_id,
          1 if is_correct else 0,
          0 if is_correct else 1,
          1 if is_correct else 0,
          0 if is_correct else 1
        ))
      
      app.db.commit()
      
      return jsonify({
        "message": f"Successfully recorded {len(reviews)} word reviews",
        "session_id": validated_session_id,
        "reviews_count": len(reviews)
      }), 200
      
    except Exception as e:
      return jsonify({"error": str(e)}), 500

  @app.route('/api/study-sessions/reset', methods=['POST'])
  @cross_origin()
  def reset_study_sessions():
    try:
      cursor = app.db.cursor()
      
      # First delete all word review items since they have foreign key constraints
      cursor.execute('DELETE FROM word_review_items')
      
      # Then delete all study sessions
      cursor.execute('DELETE FROM study_sessions')
      
      app.db.commit()
      
      return jsonify({"message": "Study history cleared successfully"}), 200
    except Exception as e:
      return jsonify({"error": str(e)}), 500