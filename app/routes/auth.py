import os
import jwt
from flask import Blueprint
from app.dto import login_schema
from app.utils import post, res_success, res_bad_request
from app.models import User
from app.extensions import bcrypt

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["POST"])
@post(login_schema)
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
