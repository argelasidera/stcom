from marshmallow import Schema, fields


class CreateUserDTO(Schema):
    email = fields.Email(required=True, max=60)
    password = fields.String(required=True)
    name = fields.String(required=True, max=120)
    role_id = fields.Integer()
    created_by = fields.Integer()


createUserDto = CreateUserDTO()


class UpdateUserDTO(Schema):
    name = fields.String(required=True, max=120)
    role_id = fields.Integer()


updateUserDto = UpdateUserDTO()
