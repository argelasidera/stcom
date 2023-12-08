from flask import Blueprint
from app.utils.custom_response import res_bad_request, res_not_found, res_success
from app.dto import createRoleDTO, updateRoleDTO
from app.utils.error_handling import post, put, private_route
from app.models import role_schema_factory, Role, Permission
from app.extensions import db

bp = Blueprint("roles", __name__, url_prefix="/roles")


@bp.route("", methods=["GET"])
@private_route("view-role")
def get_roles():
    schema = role_schema_factory(many=True)
    roles = Role.query.all()
    return res_success(data=schema.dump(roles))


@bp.route("", methods=["POST"])
@private_route("add-role")
@post(createRoleDTO)
def create_role(payload):
    role = Role(name=payload.get("name"))

    check_existing_role = Role.query.filter_by(slug=role.slug).first()

    if check_existing_role:
        return res_bad_request(message="Role must be unique")

    for perm_id in payload.get("permissions"):
        permission = Permission.query.filter_by(id=perm_id).first()
        if permission:
            role.permissions.append(permission)

    db.session.add(role)
    db.session.commit()

    return res_success(message="Role created successfully.")


@bp.route("/<int:id>", methods=["PUT"])
@private_route("edit-role")
@put(updateRoleDTO)
def update_role(payload, id):
    role = Role.query.filter_by(id=id).first()

    if not role:
        return res_not_found(message="Role not found.")

    role.name = payload.get("name")

    if payload.get("permissions"):
        role.permissions = []
        for perm_id in payload.get("permissions"):
            permission = Permission.query.filter_by(id=perm_id).first()
            if permission:
                role.permissions.append(permission)

    db.session.commit()

    return res_success(message="Role created successfully.")


@bp.route("/<int:id>", methods=["DELETE"])
@private_route("add-role")
def delete_role(id):
    role = Role.query.filter_by(id=id).first()

    if not role:
        return res_not_found("Role not found.")

    db.session.delete(role)
    db.session.commit()

    return res_success(message="Role delete successfully.")
