from marshmallow import ValidationError, fields


class NotEmptyString(fields.String):
    def _deserialize(self, value, attr, data):
        if value == "":
            raise ValidationError(message=f"{attr} is required.")
        return super()._deserialize(value, attr, data)
