from marshmallow import Schema, fields, post_load
from app.utils import NotEmptyString


class CreateCategoryDTO(Schema):
    title = NotEmptyString(required=True)
    date = fields.DateTime()
    tag = fields.String()
    description = fields.String()
    file_name = fields.String()


createCategoryDTO = CreateCategoryDTO()
updateCategoryDTO = CreateCategoryDTO()
