from flask import Blueprint
from app.models import User, user_schema_factory
from app.dto import createUserDto, updateUserDto
from app.extensions import db
from app.utils import (
    private_route,
    post,
    put,
    res_success,
    res_not_found,
    res_bad_request,
)


bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("", methods=["GET"])
@private_route("view-user")
def get_users():
    schema = user_schema_factory(exclude=["password"], many=True)
    users = User.query.all()
    return res_success({"users": schema.dump(users)})


@bp.route("/<int:id>", methods=["GET"])
@private_route("add-user")
def get_user(id):
    schema = user_schema_factory(exclude=["password"])
    user = User.query.filter_by(id=id).first()
    if not user:
        return res_not_found("User not found.")
    return res_success({"user": schema.dump(user)})


@bp.route("", methods=["POST"])
@private_route("add-user", get_loggedin_user=True)
@post(createUserDto)
def create_user(payload, loggedin_user):
    user = User(
        email=payload.get("email"),
        name=payload.get("name"),
        password=payload.get("password"),
        role_id=payload.get("role_id"),
        created_by=loggedin_user.id,
    )

    check_existing_user = User.query.filter_by(email=user.email).first()

    if check_existing_user:
        return res_bad_request(message="Email must be unique.")

    db.session.add(user)
    db.session.commit()

    return res_success(message="User created successfully.")


@bp.route("/<int:id>", methods=["PUT"])
@private_route("edit-user")
@put(updateUserDto)
def update_user(payload, id):
    user = User.query.filter_by(id=id).first()

    if not user:
        return res_not_found("User not found.")

    user.name = payload.get("name")
    user.role_id = payload.get("role_id")
    db.session.commit()

    return res_success(message="User updated successfully.")


@bp.route("/<int:id>", methods=["DELETE"])
@private_route("delete-user")
def delete_user(id):
    user = User.query.filter_by(id=id).first()

    if not user:
        return res_not_found("User not found.")

    db.session.delete(user)
    db.session.commit()

    return res_success(message="User delete successfully.")
