import os
import jwt
from flask import request
from .custom_response import (
    res_unprocessable_entity,
    res_bad_request,
    res_server_error,
    res_unauthorized,
    res_forbidden,
)
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest
from functools import wraps
from app.models import User, user_schema


def post(schema):
    def outer(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            try:
                payload = schema.load(dict(request.json))
                return fn(payload, *args, **kwargs)
            except ValidationError as e:
                return res_unprocessable_entity(errors=e.messages_dict)
            except BadRequest as e:
                return res_bad_request(e.description)
            except Exception as e:
                print("post exception: ", e)
                return res_server_error()

        return inner

    return outer


def private_route(permission: str = None):
    def outer(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            try:
                # Get token from headers
                bearer = request.headers.get("Authorization")

                # Unauthorized if no bearer token
                if not bearer:
                    return res_unauthorized("Unauthorized request.")

                token = bearer.split()[1]
                data = jwt.decode(
                    token,
                    os.getenv("JWT_SECRET"),
                    algorithms=["HS256"],
                )

                # Unauthorized if has no email in the jwt
                if not data and data.get("email") is None:
                    return res_unauthorized("Unauthorized request.")

                user = User.query.filter_by(email=data.get("email")).first_or_404()

                # Unauthorized if user not found
                if user is None:
                    return res_unauthorized("Unauthorized request.")

                # Access the api if the route has no set permission
                if not permission:
                    return fn(*args, **kwargs)

                user_dump = user_schema.dump(user)

                has_permission = False

                for perm in user_dump["role"]["permissions"]:
                    # Check if the account has the linked permission
                    if perm["slug"] == permission:
                        has_permission = True
                        break

                # Access the api if has linked permission
                if has_permission:
                    return fn(*args, **kwargs)

                # Otherwise, forbid to access the api
                return res_forbidden()

            except Exception as e:
                print("post exception: ", e)
                return res_server_error()

        return inner

    return outer
