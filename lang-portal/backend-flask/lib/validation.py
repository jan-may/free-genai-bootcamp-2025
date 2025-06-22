"""
Input validation utilities for the German Learning Portal API
"""

def validate_pagination_params(page, per_page=None, max_per_page=100):
    """
    Validate pagination parameters
    
    Args:
        page: Page number (should be positive integer)
        per_page: Items per page (optional, should be positive integer <= max_per_page)
        max_per_page: Maximum allowed items per page
    
    Returns:
        tuple: (validated_page, validated_per_page, error_message)
    """
    error_message = None
    
    # Validate page number
    try:
        page = int(page) if page is not None else 1
        if page < 1:
            error_message = "Page number must be a positive integer"
            page = 1
    except (ValueError, TypeError):
        error_message = "Page number must be a valid integer"
        page = 1
    
    # Validate per_page if provided
    validated_per_page = per_page
    if per_page is not None:
        try:
            validated_per_page = int(per_page)
            if validated_per_page < 1:
                error_message = "Items per page must be a positive integer"
                validated_per_page = 10
            elif validated_per_page > max_per_page:
                error_message = f"Items per page cannot exceed {max_per_page}"
                validated_per_page = max_per_page
        except (ValueError, TypeError):
            error_message = "Items per page must be a valid integer"
            validated_per_page = 10
    
    return page, validated_per_page, error_message

def validate_sort_params(sort_by, order, valid_columns):
    """
    Validate sorting parameters
    
    Args:
        sort_by: Column to sort by
        order: Sort order ('asc' or 'desc')
        valid_columns: List of valid column names
    
    Returns:
        tuple: (validated_sort_by, validated_order, error_message)
    """
    error_message = None
    
    # Validate sort_by
    if sort_by not in valid_columns:
        error_message = f"Invalid sort field. Valid options: {', '.join(valid_columns)}"
        sort_by = valid_columns[0]  # Default to first valid column
    
    # Validate order
    if order not in ['asc', 'desc']:
        if error_message:
            error_message += ". Invalid sort order, must be 'asc' or 'desc'"
        else:
            error_message = "Invalid sort order, must be 'asc' or 'desc'"
        order = 'asc'
    
    return sort_by, order, error_message

def validate_positive_integer(value, field_name, allow_none=False):
    """
    Validate that a value is a positive integer
    
    Args:
        value: Value to validate
        field_name: Name of the field for error messages
        allow_none: Whether None is allowed
    
    Returns:
        tuple: (validated_value, error_message)
    """
    if value is None:
        if allow_none:
            return None, None
        else:
            return None, f"{field_name} is required"
    
    try:
        validated_value = int(value)
        if validated_value <= 0:
            return None, f"{field_name} must be a positive integer"
        return validated_value, None
    except (ValueError, TypeError):
        return None, f"{field_name} must be a valid integer"

def validate_required_fields(data, required_fields):
    """
    Validate that all required fields are present in request data
    
    Args:
        data: Request data dictionary
        required_fields: List of required field names
    
    Returns:
        list: List of error messages (empty if all valid)
    """
    errors = []
    
    if not data:
        return ["Request body is required"]
    
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == "":
            errors.append(f"Field '{field}' is required")
    
    return errors

def validate_word_review(review):
    """
    Validate a single word review object
    
    Args:
        review: Review object to validate
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not isinstance(review, dict):
        return False, "Review must be an object"
    
    # Check required fields
    if 'word_id' not in review:
        return False, "Review must contain 'word_id'"
    
    if 'is_correct' not in review:
        return False, "Review must contain 'is_correct'"
    
    # Validate word_id
    word_id, error = validate_positive_integer(review['word_id'], 'word_id')
    if error:
        return False, error
    
    # Validate is_correct
    if not isinstance(review['is_correct'], bool):
        return False, "'is_correct' must be a boolean value"
    
    return True, None

def validate_string_field(value, field_name, min_length=None, max_length=None, allow_none=False):
    """
    Validate a string field
    
    Args:
        value: Value to validate
        field_name: Name of the field for error messages
        min_length: Minimum length (optional)
        max_length: Maximum length (optional)
        allow_none: Whether None is allowed
    
    Returns:
        tuple: (validated_value, error_message)
    """
    if value is None:
        if allow_none:
            return None, None
        else:
            return None, f"{field_name} is required"
    
    if not isinstance(value, str):
        return None, f"{field_name} must be a string"
    
    value = value.strip()
    
    if min_length and len(value) < min_length:
        return None, f"{field_name} must be at least {min_length} characters long"
    
    if max_length and len(value) > max_length:
        return None, f"{field_name} must be no more than {max_length} characters long"
    
    if not allow_none and len(value) == 0:
        return None, f"{field_name} cannot be empty"
    
    return value, None