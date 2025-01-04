from functools import wraps
from flask import jsonify, request
from http import HTTPStatus

def validate_json_content_type(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), HTTPStatus.BAD_REQUEST
        return f(*args, **kwargs)
    return decorated_function

def handle_exceptions(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    return decorated_function