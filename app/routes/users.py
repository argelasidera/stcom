from flask import Blueprint
from app.models import User, users_schema
from app.utils import res_success
from app.utils import private_route

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("", methods=["GET"])
@private_route("view-user")
def get_users():
    users = User.query.all()
    dump_users = users_schema.dump(users)
    return res_success({"users": dump_users})


# Get user
def get_user():
    ...


# Create user
def create_user():
    ...


# Update user
def update_user():
    ...


# Delete user
def update_user():
    ...
