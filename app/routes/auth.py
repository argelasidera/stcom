import os
import jwt
from flask import Blueprint
from app.dto import loginDTO
from app.utils import post, res_success, res_bad_request, res_forbidden
from app.models import User, user_schema_factory
from app.extensions import bcrypt
from app.utils.error_handling import private_route

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["POST"])
@post(loginDTO)
def login(payload):
    user = User.query.filter_by(email=payload.get("email")).first()

    if user and bcrypt.check_password_hash(user.password, payload["password"]):
        token = jwt.encode(
            {"id": user.id, "email": user.email},
            os.getenv("JWT_SECRET"),
            algorithm="HS256",
        )

        return res_success(message="Login Successful!", data={"token": token})

    return res_bad_request(message="Email and password not match.")


@bp.route("/my", methods=["GET"])
@private_route(show_loggedin_user=True)
def get_myinfo(loggedin_user):
    user = User.query.filter_by(id=loggedin_user.id).first()

    if not user:
        return res_forbidden(message="User not found.")

    schema = user_schema_factory(exclude=["password"])
    return res_success(data=schema.dump(user))
