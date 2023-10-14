from marshmallow import Schema, fields


class CreateRoles(Schema):
    name = fields.String(required=True)
    permissions = fields.List(fields.Integer(), required=True)


createRoleDTO = CreateRoles()
updateRoleDTO = CreateRoles()
