from flask import request, jsonify, g
from flask_cors import cross_origin
import json
from lib.validation import validate_pagination_params, validate_sort_params, validate_positive_integer
from lib.error_handler import (
    create_error_response, handle_database_error, handle_validation_error,
    handle_not_found_error, handle_generic_error
)

def load(app):
  @app.route('/api/groups', methods=['GET'])
  @cross_origin()
  def get_groups():
    try:
      cursor = app.db.cursor()

      # Validate pagination parameters
      page, _, page_error = validate_pagination_params(request.args.get('page'))
      groups_per_page = 10
      offset = (page - 1) * groups_per_page

      # Validate sorting parameters
      sort_by = request.args.get('sort_by', 'name')
      order = request.args.get('order', 'asc')
      valid_columns = ['name', 'words_count']
      sort_by, order, sort_error = validate_sort_params(sort_by, order, valid_columns)

      # Query to fetch groups with sorting and the cached word count
      cursor.execute(f'''
        SELECT id, name, words_count
        FROM groups
        ORDER BY {sort_by} {order}
        LIMIT ? OFFSET ?
      ''', (groups_per_page, offset))

      groups = cursor.fetchall()

      # Query the total number of groups
      cursor.execute('SELECT COUNT(*) FROM groups')
      total_groups = cursor.fetchone()[0]
      total_pages = (total_groups + groups_per_page - 1) // groups_per_page

      # Format the response
      groups_data = []
      for group in groups:
        groups_data.append({
          "id": group["id"],
          "group_name": group["name"],
          "word_count": group["words_count"]
        })

      # Return groups and pagination metadata
      return jsonify({
        'groups': groups_data,
        'total_pages': total_pages,
        'current_page': page
      })
    except Exception as e:
      return handle_generic_error(e, "fetching groups")

  @app.route('/api/groups/<int:id>', methods=['GET'])
  @cross_origin()
  def get_group(id):
    try:
      # Validate group ID parameter
      validated_id, id_error = validate_positive_integer(id, 'group_id')
      if id_error:
        return handle_validation_error(id_error)
      
      cursor = app.db.cursor()

      # Get group details
      cursor.execute('''
        SELECT id, name, words_count
        FROM groups
        WHERE id = ?
      ''', (validated_id,))
      
      group = cursor.fetchone()
      if not group:
        return handle_not_found_error("Group", validated_id)

      return jsonify({
        "id": group["id"],
        "group_name": group["name"],
        "word_count": group["words_count"]
      })
    except Exception as e:
      return handle_generic_error(e, "fetching group details")

  @app.route('/api/groups/<int:id>/words', methods=['GET'])
  @cross_origin()
  def get_group_words(id):
    try:
      cursor = app.db.cursor()
      
      # Get pagination parameters
      page = int(request.args.get('page', 1))
      words_per_page = 10
      offset = (page - 1) * words_per_page

      # Get sorting parameters
      sort_by = request.args.get('sort_by', 'german')
      order = request.args.get('order', 'asc')

      # Validate sort parameters
      valid_columns = ['german', 'pronunciation', 'english', 'correct_count', 'wrong_count']
      if sort_by not in valid_columns:
        sort_by = 'german'
      if order not in ['asc', 'desc']:
        order = 'asc'

      # First, check if the group exists
      cursor.execute('SELECT name FROM groups WHERE id = ?', (id,))
      group = cursor.fetchone()
      if not group:
        return handle_not_found_error("Group", id)

      # Query to fetch words with pagination and sorting
      cursor.execute(f'''
        SELECT w.*, 
               COALESCE(wr.correct_count, 0) as correct_count,
               COALESCE(wr.wrong_count, 0) as wrong_count
        FROM words w
        JOIN word_groups wg ON w.id = wg.word_id
        LEFT JOIN word_reviews wr ON w.id = wr.word_id
        WHERE wg.group_id = ?
        ORDER BY {sort_by} {order}
        LIMIT ? OFFSET ?
      ''', (id, words_per_page, offset))
      
      words = cursor.fetchall()

      # Get total words count for pagination
      cursor.execute('''
        SELECT COUNT(*) 
        FROM word_groups 
        WHERE group_id = ?
      ''', (id,))
      total_words = cursor.fetchone()[0]
      total_pages = (total_words + words_per_page - 1) // words_per_page

      # Format the response
      words_data = []
      for word in words:
        words_data.append({
          "id": word["id"],
          "german": word["german"],
          "pronunciation": word["pronunciation"],
          "gender": word["gender"],
          "plural": word["plural"],
          "english": word["english"],
          "correct_count": word["correct_count"],
          "wrong_count": word["wrong_count"]
        })

      return jsonify({
        'words': words_data,
        'total_pages': total_pages,
        'current_page': page
      })
    except Exception as e:
      return handle_generic_error(e, "fetching group words")

  @app.route('/api/groups/<int:id>/words/raw', methods=['GET'])
  @cross_origin()
  def get_group_words_raw(id):
    try:
      cursor = app.db.cursor()
      
      # First, check if the group exists
      cursor.execute('SELECT name FROM groups WHERE id = ?', (id,))
      group = cursor.fetchone()
      if not group:
        return handle_not_found_error("Group", id)

      # Query to fetch all words in the group without pagination
      cursor.execute('''
        SELECT w.id, w.german, w.pronunciation, w.english, w.gender, w.plural, w.parts,
               COALESCE(wr.correct_count, 0) as correct_count,
               COALESCE(wr.wrong_count, 0) as wrong_count
        FROM words w
        JOIN word_groups wg ON w.id = wg.word_id
        LEFT JOIN word_reviews wr ON w.id = wr.word_id
        WHERE wg.group_id = ?
        ORDER BY w.german ASC
      ''', (id,))
      
      words = cursor.fetchall()

      # Format the response as a simple array of word objects
      words_data = []
      for word in words:
        # Parse parts JSON if it exists
        parts = None
        if word["parts"]:
          try:
            import json
            parts = json.loads(word["parts"])
          except:
            parts = None
            
        words_data.append({
          "id": word["id"],
          "german": word["german"],
          "pronunciation": word["pronunciation"],
          "english": word["english"],
          "gender": word["gender"],
          "plural": word["plural"],
          "parts": parts,
          "correct_count": word["correct_count"],
          "wrong_count": word["wrong_count"]
        })

      return jsonify({
        "group_id": id,
        "group_name": group["name"],
        "words": words_data,
        "total_words": len(words_data)
      })
      
    except Exception as e:
      return handle_generic_error(e, "fetching group words raw data")

  @app.route('/api/groups/<int:id>/study_sessions', methods=['GET'])
  @cross_origin()
  def get_group_study_sessions(id):
    try:
      cursor = app.db.cursor()
      
      # Get pagination parameters
      page = int(request.args.get('page', 1))
      sessions_per_page = 10
      offset = (page - 1) * sessions_per_page

      # Get sorting parameters
      sort_by = request.args.get('sort_by', 'created_at')
      order = request.args.get('order', 'desc')  # Default to newest first

      # Map frontend sort keys to database columns
      sort_mapping = {
        'startTime': 'created_at',
        'endTime': 'last_activity_time',
        'activityName': 'a.name',
        'groupName': 'g.name',
        'reviewItemsCount': 'review_count'
      }

      # Use mapped sort column or default to created_at
      sort_column = sort_mapping.get(sort_by, 'created_at')

      # Get total count for pagination
      cursor.execute('''
        SELECT COUNT(*)
        FROM study_sessions
        WHERE group_id = ?
      ''', (id,))
      total_sessions = cursor.fetchone()[0]
      total_pages = (total_sessions + sessions_per_page - 1) // sessions_per_page

      # Get study sessions for this group with dynamic calculations
      cursor.execute(f'''
        SELECT 
          s.id,
          s.group_id,
          s.study_activity_id,
          s.created_at as start_time,
          (
            SELECT MAX(created_at)
            FROM word_review_items
            WHERE study_session_id = s.id
          ) as last_activity_time,
          a.name as activity_name,
          g.name as group_name,
          (
            SELECT COUNT(*)
            FROM word_review_items
            WHERE study_session_id = s.id
          ) as review_count
        FROM study_sessions s
        JOIN study_activities a ON s.study_activity_id = a.id
        JOIN groups g ON s.group_id = g.id
        WHERE s.group_id = ?
        ORDER BY {sort_column} {order}
        LIMIT ? OFFSET ?
      ''', (id, sessions_per_page, offset))
      
      sessions = cursor.fetchall()
      sessions_data = []
      
      for session in sessions:
        # If there's no last_activity_time, use start_time + 30 minutes
        end_time = session["last_activity_time"]
        if not end_time:
            end_time = cursor.execute('SELECT datetime(?, "+30 minutes")', (session["start_time"],)).fetchone()[0]
        
        sessions_data.append({
          "id": session["id"],
          "group_id": session["group_id"],
          "group_name": session["group_name"],
          "study_activity_id": session["study_activity_id"],
          "activity_name": session["activity_name"],
          "start_time": session["start_time"],
          "end_time": end_time,
          "review_items_count": session["review_count"]
        })

      return jsonify({
        'study_sessions': sessions_data,
        'total_pages': total_pages,
        'current_page': page
      })
    except Exception as e:
      return handle_generic_error(e, "fetching group study sessions")