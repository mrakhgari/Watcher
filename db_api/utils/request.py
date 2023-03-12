from functools import wraps
from flask import request

def json_only(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        if not request.is_json:
            return {'message': 'The request body is not valid JSON.'}, 400
        return function(*args, **kwargs)
    return decorator
