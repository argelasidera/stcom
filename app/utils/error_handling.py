from flask import request
from .custom_response import res_unprocessable_entity, res_bad_request, res_server_error
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest
from functools import wraps


def post(schema):
    def outer(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            try:
                payload = schema.load(dict(request.json))
                return fn(payload)
            except ValidationError as e:
                return res_unprocessable_entity(errors=e.messages_dict)
            except BadRequest as e:
                return res_bad_request(e.description)
            except Exception:
                return res_server_error()
        return inner
    return outer
