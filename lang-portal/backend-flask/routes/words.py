from flask import request, jsonify, g
from flask_cors import cross_origin
import json
from lib.validation import validate_pagination_params, validate_sort_params, validate_positive_integer
from lib.error_handler import (
    create_error_response, handle_database_error, handle_validation_error,
    handle_not_found_error, handle_generic_error, safe_execute
)

def load(app):
  # Endpoint: GET /words with pagination (50 words per page)
  @app.route('/api/words', methods=['GET'])
  @cross_origin()
  def get_words():
    try:
      cursor = app.db.cursor()

      # Validate pagination parameters
      page, _, page_error = validate_pagination_params(request.args.get('page'))
      words_per_page = 50
      offset = (page - 1) * words_per_page

      # Validate sorting parameters
      sort_by = request.args.get('sort_by', 'german')
      order = request.args.get('order', 'asc')
      valid_columns = ['german', 'pronunciation', 'english', 'correct_count', 'wrong_count', 'gender', 'plural']
      sort_by, order, sort_error = validate_sort_params(sort_by, order, valid_columns)
      
      # Collect validation errors (non-fatal, will use defaults)
      validation_warnings = []
      if page_error:
        validation_warnings.append(page_error)
      if sort_error:
        validation_warnings.append(sort_error)

      # Query to fetch words with sorting
      cursor.execute(f'''
        SELECT w.id, w.german, w.pronunciation, w.english, w.gender, w.plural,
            COALESCE(r.correct_count, 0) AS correct_count,
            COALESCE(r.wrong_count, 0) AS wrong_count
        FROM words w
        LEFT JOIN word_reviews r ON w.id = r.word_id
        ORDER BY {sort_by} {order}
        LIMIT ? OFFSET ?
      ''', (words_per_page, offset))

      words = cursor.fetchall()

      # Query the total number of words
      cursor.execute('SELECT COUNT(*) FROM words')
      total_words = cursor.fetchone()[0]
      total_pages = (total_words + words_per_page - 1) // words_per_page

      # Format the response
      words_data = []
      for word in words:
        words_data.append({
          "id": word["id"],
          "german": word["german"],
          "pronunciation": word["pronunciation"],
          "english": word["english"],
          "gender": word["gender"],
          "plural": word["plural"],
          "correct_count": word["correct_count"],
          "wrong_count": word["wrong_count"]
        })

      return jsonify({
        "words": words_data,
        "total_pages": total_pages,
        "current_page": page,
        "total_words": total_words
      })

    except Exception as e:
      return handle_database_error(e, "fetching words")
    finally:
      app.db.close()

  # Endpoint: GET /words/:id to get a single word with its details
  @app.route('/api/words/<int:word_id>', methods=['GET'])
  @cross_origin()
  def get_word(word_id):
    try:
      # Validate word_id parameter
      validated_word_id, id_error = validate_positive_integer(word_id, 'word_id')
      if id_error:
        return handle_validation_error(id_error)
      
      cursor = app.db.cursor()
      
      # Query to fetch the word and its details
      cursor.execute('''
        SELECT w.id, w.german, w.pronunciation, w.english, w.gender, w.plural,
               COALESCE(r.correct_count, 0) AS correct_count,
               COALESCE(r.wrong_count, 0) AS wrong_count,
               GROUP_CONCAT(DISTINCT g.id || '::' || g.name) as groups
        FROM words w
        LEFT JOIN word_reviews r ON w.id = r.word_id
        LEFT JOIN word_groups wg ON w.id = wg.word_id
        LEFT JOIN groups g ON wg.group_id = g.id
        WHERE w.id = ?
        GROUP BY w.id
      ''', (validated_word_id,))
      
      word = cursor.fetchone()
      
      if not word:
        return handle_not_found_error("Word", validated_word_id)
      
      # Parse the groups string into a list of group objects
      groups = []
      if word["groups"]:
        for group_str in word["groups"].split(','):
          group_id, group_name = group_str.split('::')
          groups.append({
            "id": int(group_id),
            "name": group_name
          })
      
      return jsonify({
        "word": {
          "id": word["id"],
          "german": word["german"],
          "pronunciation": word["pronunciation"],
          "english": word["english"],
          "gender": word["gender"],
          "plural": word["plural"],
          "correct_count": word["correct_count"],
          "wrong_count": word["wrong_count"],
          "groups": groups
        }
      })
      
    except Exception as e:
      return handle_database_error(e, "fetching word details")