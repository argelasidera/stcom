from flask import Blueprint
from app.models import User, users_schema
from app.utils import res_success

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("", methods=["GET"])
def get_users():
    users = User.query.all()

    dump_users = users_schema.dump(users)
    return res_success({"users": dump_users})
