"""
Error handling utilities for the German Learning Portal API
"""

from flask import jsonify
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIError(Exception):
    """Custom API exception class"""
    def __init__(self, message, status_code=400, error_code=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

def create_error_response(message, status_code=400, error_code=None, details=None):
    """
    Create a standardized error response
    
    Args:
        message: Error message
        status_code: HTTP status code
        error_code: Optional error code for API clients
        details: Optional additional details
    
    Returns:
        tuple: (response, status_code)
    """
    error_data = {
        "error": message,
        "status_code": status_code
    }
    
    if error_code:
        error_data["error_code"] = error_code
    
    if details:
        error_data["details"] = details
    
    return jsonify(error_data), status_code

def handle_database_error(e, operation="database operation"):
    """
    Handle database-related errors with appropriate logging
    
    Args:
        e: Exception object
        operation: Description of the operation that failed
    
    Returns:
        tuple: (response, status_code)
    """
    error_message = str(e)
    logger.error(f"Database error during {operation}: {error_message}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    
    # Don't expose internal database errors to clients
    if "UNIQUE constraint failed" in error_message:
        return create_error_response(
            "A record with this data already exists",
            status_code=409,
            error_code="DUPLICATE_RECORD"
        )
    elif "FOREIGN KEY constraint failed" in error_message:
        return create_error_response(
            "Referenced record does not exist",
            status_code=400,
            error_code="INVALID_REFERENCE"
        )
    elif "NOT NULL constraint failed" in error_message:
        return create_error_response(
            "Required field is missing",
            status_code=400,
            error_code="MISSING_REQUIRED_FIELD"
        )
    else:
        return create_error_response(
            "Internal database error occurred",
            status_code=500,
            error_code="DATABASE_ERROR"
        )

def handle_validation_error(validation_errors):
    """
    Handle validation errors with detailed field information
    
    Args:
        validation_errors: List of validation error messages or single message
    
    Returns:
        tuple: (response, status_code)
    """
    if isinstance(validation_errors, list):
        if len(validation_errors) == 1:
            message = validation_errors[0]
        else:
            message = "Multiple validation errors occurred"
    else:
        validation_errors = [validation_errors]
        message = validation_errors[0]
    
    return create_error_response(
        message,
        status_code=400,
        error_code="VALIDATION_ERROR",
        details=validation_errors if len(validation_errors) > 1 else None
    )

def handle_not_found_error(resource_type, resource_id=None):
    """
    Handle resource not found errors
    
    Args:
        resource_type: Type of resource (e.g., "Word", "Group", "Study Session")
        resource_id: Optional ID of the resource
    
    Returns:
        tuple: (response, status_code)
    """
    if resource_id:
        message = f"{resource_type} with ID {resource_id} not found"
    else:
        message = f"{resource_type} not found"
    
    return create_error_response(
        message,
        status_code=404,
        error_code="RESOURCE_NOT_FOUND"
    )

def handle_method_not_allowed():
    """
    Handle method not allowed errors
    
    Returns:
        tuple: (response, status_code)
    """
    return create_error_response(
        "HTTP method not allowed for this endpoint",
        status_code=405,
        error_code="METHOD_NOT_ALLOWED"
    )

def handle_unsupported_media_type():
    """
    Handle unsupported media type errors
    
    Returns:
        tuple: (response, status_code)
    """
    return create_error_response(
        "Content-Type must be application/json",
        status_code=415,
        error_code="UNSUPPORTED_MEDIA_TYPE"
    )

def handle_json_decode_error():
    """
    Handle JSON decode errors
    
    Returns:
        tuple: (response, status_code)
    """
    return create_error_response(
        "Invalid JSON format in request body",
        status_code=400,
        error_code="INVALID_JSON"
    )

def handle_generic_error(e, operation="API operation"):
    """
    Handle generic errors with appropriate logging
    
    Args:
        e: Exception object
        operation: Description of the operation that failed
    
    Returns:
        tuple: (response, status_code)
    """
    error_message = str(e)
    logger.error(f"Unexpected error during {operation}: {error_message}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    
    return create_error_response(
        "An unexpected error occurred",
        status_code=500,
        error_code="INTERNAL_ERROR"
    )

def safe_execute(func, operation_name):
    """
    Safely execute a function with comprehensive error handling
    
    Args:
        func: Function to execute
        operation_name: Name of the operation for logging
    
    Returns:
        Result of the function or error response
    """
    try:
        return func()
    except APIError as e:
        return create_error_response(e.message, e.status_code, e.error_code)
    except ValueError as e:
        return handle_validation_error(str(e))
    except Exception as e:
        if "database" in str(e).lower() or "sqlite" in str(e).lower():
            return handle_database_error(e, operation_name)
        else:
            return handle_generic_error(e, operation_name)