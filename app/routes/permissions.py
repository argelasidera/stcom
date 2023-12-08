from flask import Blueprint
from app.models import permission_schema_factory, Permission
from app.utils.custom_response import res_success
from app.utils.error_handling import private_route


bp = Blueprint("permissions", __name__, url_prefix="/permissions")


@bp.route("", methods=["GET"])
@private_route("view-role")
def get_permissions():
    schema = permission_schema_factory(many=True)
    permissions = Permission.query.all()
    return res_success(data=schema.dump(permissions))
