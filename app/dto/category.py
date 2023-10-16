from marshmallow import Schema, fields


class CreateCategoryDTO(Schema):
    title = fields.String(required=True)
    date = fields.DateTime()
    tag = fields.String()
    description = fields.String()
    file_name = fields.String()


createCategoryDTO = CreateCategoryDTO()
updateCategoryDTO = CreateCategoryDTO()
